import {test,before,beforeEach,after} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {start,run,source,click,wait,ORIGIN} from './browser.mjs';
let b;const attached=new Map(),ready=new Map(),observations=[];
const pause=ms=>new Promise(r=>setTimeout(r,ms));
const canary=kind=>ORIGIN+'/assets/consent.js?edb_task21_canary='+kind;
async function until(fn,label){for(let i=0;i<150;i++){try{const v=await fn();if(v)return v;}catch{}await pause(30);}assert.fail('Child instrumentation unavailable: '+label);}
before(async()=>{
 b=await start('isolation');
 b.onEvent(m=>{if(m.method==='Target.attachedToTarget'&&m.params.targetInfo.type==='iframe'){
  const {sessionId,targetInfo}=m.params;attached.set(targetInfo.targetId,sessionId);
  ready.set(sessionId,(async()=>{try{await b.call('Network.enable',{},sessionId);await b.call('Network.setBlockedURLs',{urls:[]},sessionId);await b.call('Runtime.enable',{},sessionId);await b.call('Log.enable',{},sessionId);}catch(e){b.record.instrumentation_errors.push({stage:'child-network-monitoring',message:e.message});}finally{await b.call('Runtime.runIfWaitingForDebugger',{},sessionId);}})());
 }});
 await b.call('Target.setAutoAttach',{autoAttach:true,waitForDebuggerOnStart:false,flatten:true,filter:[{type:'iframe',exclude:false},{exclude:true}]});
});
beforeEach(async()=>{await b.load(source('html-previewer'));b.record.security_probe_active=false;await b.evaluate("window.__ran=0;localStorage.setItem('task21-gate-sentinel','untouched');true");});
after(async()=>{if(b){fs.writeFileSync(new URL('../../../reports/public-task21/isolation-observations.json',import.meta.url),JSON.stringify({browser:b.version,observations,attached_child_sessions:attached.size},null,2)+'\n');await b.close();}});
async function child(expression){
 let frameId,sessionId;const targets=await b.call('Target.getTargets'),t=targets.targetInfos.find(t=>t.type==='iframe'&&t.url==='about:srcdoc');
 if(t){sessionId=attached.get(t.targetId);if(!sessionId){({sessionId}=await b.call('Target.attachToTarget',{targetId:t.targetId,flatten:true}));}if(ready.has(sessionId))await ready.get(sessionId);frameId=(await b.call('Page.getFrameTree',{},sessionId)).frameTree.frame.id;}
 else frameId=(await b.call('Page.getFrameTree')).frameTree.childFrames?.find(x=>x.frame.url==='about:srcdoc')?.frame.id;
 if(!frameId)throw Error('Preview frame not loaded');const {executionContextId}=await b.call('Page.createIsolatedWorld',{frameId,worldName:'owner-public-security-verification'},sessionId);
 const r=await b.call('Runtime.evaluate',{contextId:executionContextId,returnByValue:true,expression},sessionId);if(r.exceptionDetails)throw Error('Child probe failed');return r.result.value;
}
const webPages=async()=> (await b.call('Target.getTargets')).targetInfos.filter(t=>t.type==='page'&&(/^(https?:|about:)/.test(t.url))).map(t=>({id:t.targetId,url:t.url})).sort((a,b)=>a.id.localeCompare(b.id));
test('public root network monitoring positive control sees a real HTTP200 request',async()=>{
 const url=canary('positive-root');assert.equal(await b.evaluate(`fetch(${JSON.stringify(url)},{cache:'no-store'}).then(r=>r.status)`),200);await until(()=>b.record.responses.find(x=>x.url===url&&x.status===200),'root positive-control response');assert.equal(b.record.canary_requests.filter(x=>x.url===url).length,1);observations.push({check:'root-network-positive-control',url,status:200,result:'PASS'});
});
test('sandboxed child network monitoring positive control sees an intentionally permitted image request',async()=>{
 // Test-only control removes the production srcdoc CSP for one synthetic image.
 // Production HTML/Worker assets remain unmodified; malicious tests use real tool output.
 b.record.security_probe_active=true;const url=canary('positive-child');await b.evaluate(`safePreview.srcdoc=${JSON.stringify('<!doctype html><html><body><h1>Network control</h1></body></html>')};true`);
 await until(()=>child("document.querySelector('h1')?.textContent==='Network control'"),'positive-control child readiness');
 await child(`(()=>{const image=document.createElement('img');image.src=${JSON.stringify(url)};document.body.append(image);return true})()`);
 const response=await until(()=>b.record.responses.find(x=>x.url===url&&x.status===200),'child positive-control response');assert.equal(b.record.canary_requests.filter(x=>x.url===url).length,1);assert.equal(await b.evaluate('safePreview.getAttribute("sandbox")'),'');observations.push({check:'child-network-positive-control',url,status:response.status,child_session_observed:response.child,result:'PASS'});
});
const fixtures={
 scripts:c=>`<script>parent.__ran=1;parent.localStorage.setItem('task21-gate-sentinel','bad');top.location='${c}';open('${c}')</script><script src="${c}"></script><p>Visible</p>`,
 handlers:c=>`<img src="${c}" onerror="parent.__ran=2"><div onmouseover="parent.__ran=3" style="background:url(${c})">Text</div>`,
 navigation:c=>`<base href="${c}" target="_top"><meta http-equiv="refresh" content="0;url=${c}"><a href="${c}" target="_top" ping="${c}">link</a>`,
 forms:c=>`<form action="${c}" target="_blank"><input name="secret" value="x"><button formtarget="_top">send</button></form><a href="${c}" target="_blank">open</a>`,
 resources:c=>`<link rel="stylesheet" href="${c}"><style>@import '${c}';div{background:url(${c})}</style><iframe src="${c}"></iframe><object data="${c}"></object><audio src="${c}" autoplay></audio><video poster="${c}"><source src="${c}"></video>`,
 foreign:c=>`<svg><foreignObject><iframe src="${c}"></iframe></foreignObject><image href="${c}" onload="parent.__ran=4"/></svg><math><mtext><img src="${c}"></mtext></math>`,
 mutation:c=>`<math><mtext><table><mglyph><style><!--</style><img title="--><img src=${c} onerror=parent.__ran=5>"></math><noscript><p title="</noscript><img src='${c}'>">x</p>`,
 templates:c=>`<template><img src="${c}"><script>parent.__ran=6</script></template><div id="location" name="parent" data-x="${c}">safe</div>`,
 rawtext:c=>`<xmp><img src="${c}" onerror="parent.__ran=7"></xmp><textarea></textarea><plaintext><script>parent.__ran=8</script>`,
 encoded:c=>`<a href="jav&#x61;script:parent.__ran=9">café 世界 😀</a><p onclick="&#x61;lert(1)">&lt;script&gt;literal&lt;/script&gt;</p>`
};
for(const[name,fixture]of Object.entries(fixtures))test('actual public preview blocks '+name+' without code/network/parent-state changes',async()=>{
 const beforeWebPages=await webPages(),count=b.record.canary_requests.length,r=await run(b,fixture(canary('malicious-'+name)));assert.equal(r.error,'');await pause(220);assert.equal(await b.evaluate('__ran'),0);assert.equal(await b.evaluate("localStorage.getItem('task21-gate-sentinel')"),'untouched');assert.equal(await b.evaluate('location.href'),source('html-previewer'));assert.equal(await b.evaluate('safePreview.getAttribute("sandbox")'),'');assert.equal(await b.evaluate('safePreview.contentDocument'),null);assert.equal(b.record.canary_requests.length,count);assert.deepEqual(b.record.exceptions,[]);assert.deepEqual(await webPages(),beforeWebPages,'No input-created web/blank popup targets');observations.push({check:name,result:'PASS',unexpected_canary_requests:0,new_web_page_targets:0});
});
test('actual public child visibly renders safe content and denies document/storage/navigation/popup/form probes',async()=>{
 const count=b.record.canary_requests.length,r=await run(b,'<h1>Hello</h1><p>Readable <strong>local</strong> preview.</p>');assert.equal(r.error,'');await until(()=>child("document.querySelector('h1')?.textContent==='Hello'"),'rendered heading');b.record.security_probe_active=true;const beforePages=(await b.call('Target.getTargets')).targetInfos.filter(t=>t.type==='page').map(t=>({id:t.targetId,url:t.url})).sort((a,b)=>a.id.localeCompare(b.id));
 const result=await child(`(()=>{const h=document.querySelector('h1'),r={heading:h.textContent,visible:h.getBoundingClientRect().width>0&&getComputedStyle(h).display!=='none',color:getComputedStyle(h).color,active:document.querySelectorAll('script,style,img,a,form,iframe,object,svg,math').length,csp:document.querySelector('meta[http-equiv="Content-Security-Policy"]').content};for(const key of ['localStorage','sessionStorage']){try{window[key].getItem('task21-gate-sentinel');r[key]='accessible'}catch(e){r[key]=e.name}}try{parent.document.body;r.parent='accessible'}catch(e){r.parent=e.name}try{parent.localStorage.getItem('task21-gate-sentinel');r.parentStorage='accessible'}catch(e){r.parentStorage=e.name}try{top.location.href=${JSON.stringify(canary('probe-top'))};r.top='allowed'}catch(e){r.top=e.name}r.popup=window.open(${JSON.stringify(canary('probe-popup'))})===null;const f=document.createElement('form');f.action=${JSON.stringify(canary('probe-form'))};f.method='POST';document.body.append(f);f.submit();f.remove();return r})()`);
 const afterPages=(await b.call('Target.getTargets')).targetInfos.filter(t=>t.type==='page').map(t=>({id:t.targetId,url:t.url})).sort((a,b)=>a.id.localeCompare(b.id));fs.writeFileSync(new URL('../../../reports/public-task21/child-probe-diagnostics.json',import.meta.url),JSON.stringify({result,beforePages,afterPages},null,2)+'\n');
 assert.equal(result.heading,'Hello');assert.equal(result.visible,true);assert.equal(result.active,0);assert.match(result.csp,/default-src 'none'/);assert.match(result.csp,/form-action 'none'/);for(const key of ['localStorage','sessionStorage','parent','parentStorage','top'])assert.equal(result[key],'SecurityError');assert.equal(result.popup,true);await pause(300);assert.equal(b.record.canary_requests.length,count);assert.equal(await b.evaluate('location.href'),source('html-previewer'));assert.equal(await b.evaluate("localStorage.getItem('task21-gate-sentinel')"),'untouched');assert.deepEqual(afterPages,beforePages,'No page target may be opened or navigated by the preview');
 await b.evaluate("safePreview.scrollIntoView({block:'center'});true");await pause(200);const shot=await b.call('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});fs.writeFileSync(new URL('../../../reports/public-task21/public-preview-rendered.png',import.meta.url),Buffer.from(shot.data,'base64'));observations.push({check:'actual-child-origin-rendering-and-navigation-probes',result:'PASS',observations:result,unexpected_canary_requests:0});
});
