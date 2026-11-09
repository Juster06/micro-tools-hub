import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import {fileURLToPath} from 'node:url';
import {launchBrowser,findBrowser} from './tool-tests/browser.mjs';
const root=fileURLToPath(new URL('../',import.meta.url));
const mapping=JSON.parse(fs.readFileSync(path.join(root,'styles/homepage-directory.json'),'utf8'));
const delay=ms=>new Promise(r=>setTimeout(r,ms));
async function fixture(action){
 const server=http.createServer((req,res)=>{const filename=path.resolve(root,'.'+new URL(req.url,'http://localhost').pathname);if(!filename.startsWith(root)||!fs.existsSync(filename)||!fs.statSync(filename).isFile()){res.writeHead(404);res.end();return;}res.setHeader('Content-Type',filename.endsWith('.css')?'text/css':filename.endsWith('.js')?'application/javascript':'text/html; charset=utf-8');res.end(fs.readFileSync(filename));});
 await new Promise(r=>server.listen(0,'127.0.0.1',r));let b;
 try{
  b=await launchBrowser(findBrowser());const origin='http://127.0.0.1:'+server.address().port;let google=[],errors=[];
  b.onEvent(({method,params:p})=>{if(method==='Runtime.exceptionThrown')errors.push(p.exceptionDetails);if(method==='Fetch.requestPaused'){google.push(p.request.url);b.call('Fetch.fulfillRequest',{requestId:p.requestId,responseCode:200,responseHeaders:[{name:'Content-Type',value:'application/javascript'}],body:Buffer.from('window.__syntheticGoogle=true;').toString('base64')}).catch(e=>errors.push(String(e)));}});
  await b.call('Network.setBlockedURLs',{urls:[]});await b.call('Fetch.enable',{patterns:[{urlPattern:'*googletagmanager.com/*'},{urlPattern:'*google-analytics.com/*'}]});
  b.evaluate=async expression=>{const r=await b.call('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true,userGesture:true});if(r.exceptionDetails)throw Error(r.exceptionDetails.exception?.description||r.exceptionDetails.text);return r.result?.value;};
  const load=async()=>{await b.call('Page.navigate',{url:origin+'/index.html?private=synthetic-query#main'});const end=Date.now()+7000;while(Date.now()<end){if(await b.evaluate('document.readyState==="complete"&&!!document.getElementById("edb-consent-root")'))return;await delay(30);}throw Error('Homepage did not initialize');};
  await load();await action(b,google,load);assert.deepEqual(errors,[]);
 }finally{if(b)await b.close();await new Promise(r=>server.close(r));}
}
const set=async(b,value)=>{await b.evaluate(`toolSearch.value=${JSON.stringify(value)};toolSearch.dispatchEvent(new Event('input',{bubbles:true}));true`);};
const visible=b=>b.evaluate('[...document.querySelectorAll(".tool-card")].filter(x=>!x.hidden).map(x=>x.dataset.toolId)');
test('homepage search, reviewed aliases, category filters, clear and safe zero results',async()=>fixture(async(b,google)=>{
 assert.equal((await visible(b)).length,87);
 for(const [query,expected] of [['Age Calculator',['percentage-calculator','age-calculator']],['Percentage Calculator',['percentage-calculator']],['File Size Converter',['file-size-converter']],['Password Generator',['password-generator']]]){await set(b,query);assert.deepEqual(await visible(b),expected);assert.equal(await b.evaluate('resultCount.textContent'),`${expected.length} of 87 tools match`);}
 for(const c of mapping.search_acceptance_cases.filter(x=>x.must_include)){await set(b,'  '+c.query.toUpperCase().replaceAll(' ','   ')+'  ');const ids=await visible(b);for(const id of c.must_include)assert.ok(ids.includes(id),c.query);}
 await set(b,'<img src=x onerror=alert(1)>');assert.equal((await visible(b)).length,0);assert.equal(await b.evaluate('empty.hidden'),false);assert.equal(await b.evaluate('document.querySelectorAll("img").length'),0);
 await b.evaluate('document.getElementById("clearSearch").click();true');assert.equal((await visible(b)).length,87);assert.equal(await b.evaluate('document.activeElement.id'),'toolSearch');
 for(const c of mapping.categories){await b.evaluate(`document.querySelector('[data-category-filter="${c.id}"]').click();true`);assert.deepEqual((await visible(b)).sort(),[...c.tool_ids].sort());}
 await b.evaluate('document.getElementById("reset-results").click();true');assert.equal(await b.evaluate('resultCount.textContent'),'87 tools ready to use');assert.deepEqual(google,[]);
}));
test('LIVE-03: in-flow consent, menu keyboard, reflow, enlarged text and reduced motion',async()=>fixture(async(b)=>{
 const evidence=[];
 for(const width of [320,390,768,1365])for(const enlarged of [false,true]){
  await b.call('Emulation.setDeviceMetricsOverride',{width,height:900,deviceScaleFactor:1,mobile:false});
  await b.evaluate(`document.documentElement.style.fontSize=${JSON.stringify(enlarged?'200%':'100%')};document.body.style.fontSize="1rem";true`);
  // Let viewport/media-query updates finish before opening and navigating the menu.
  await b.evaluate('new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))');
  assert.equal(await b.evaluate('document.documentElement.scrollWidth>innerWidth'),false,`reflow ${width} enlarged ${enlarged}: `+JSON.stringify(await b.evaluate('[...document.querySelectorAll("body *")].filter(e=>{const r=e.getBoundingClientRect();return r.right>innerWidth||r.left<0||e.scrollWidth>e.clientWidth+1}).map(e=>({tag:e.tagName,id:e.id,cls:e.className,text:e.textContent.slice(0,50),right:e.getBoundingClientRect().right,scroll:e.scrollWidth,client:e.clientWidth}))')));
  for(const id of ['toolSearch','clearSearch','edb-consent-accept','edb-consent-reject']){
   const v=await b.evaluate(`(()=>{const e=document.getElementById('${id}');e.focus();const r=e.getBoundingClientRect();const hit=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return {id:e.id,visible:r.top>=0&&r.bottom<=innerHeight,hit:e===hit||e.contains(hit),height:r.height,width:r.width,top:r.top,bottom:r.bottom,outline:getComputedStyle(e).outlineWidth,panel:getComputedStyle(document.getElementById('edb-consent-panel')).position}})()`);
   assert.ok(v.visible&&v.hit,JSON.stringify({viewportWidth:width,enlarged,...v}));assert.ok(v.height>=44);assert.equal(v.panel,'static');evidence.push({viewportWidth:width,enlarged,...v});
  }
  if(width<640){await b.evaluate('menu.focus();true');await b.call('Input.dispatchKeyEvent',{type:'keyDown',key:'Enter',code:'Enter',windowsVirtualKeyCode:13,text:'\r'});await b.call('Input.dispatchKeyEvent',{type:'keyUp',key:'Enter',code:'Enter',windowsVirtualKeyCode:13});assert.equal(await b.evaluate('menu.getAttribute("aria-expanded")'),'true');}
  await b.evaluate('document.querySelector("#site-nav a").focus();true');
  for(let index=0;index<3;index++){
   if(index){await b.call('Input.dispatchKeyEvent',{type:'rawKeyDown',key:'Tab',code:'Tab',windowsVirtualKeyCode:9});await b.call('Input.dispatchKeyEvent',{type:'keyUp',key:'Tab',code:'Tab',windowsVirtualKeyCode:9});}
   const navFocus=await b.evaluate('(()=>{const e=document.activeElement,r=e.getBoundingClientRect(),hit=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return {label:e.textContent,withinNav:!!e.closest("#site-nav"),visible:r.top>=0&&r.bottom<=innerHeight,hit:e===hit||e.contains(hit)}})()');assert.ok(navFocus.withinNav&&navFocus.visible&&navFocus.hit,JSON.stringify(navFocus));evidence.push({viewportWidth:width,enlarged,navigation:navFocus});
  }
  if(width<640){await b.call('Input.dispatchKeyEvent',{type:'keyDown',key:'Escape',code:'Escape',windowsVirtualKeyCode:27});assert.equal(await b.evaluate('menu.getAttribute("aria-expanded")'),'false');assert.equal(await b.evaluate('document.activeElement.id'),'menu');}
 }
 await b.call('Emulation.setEmulatedMedia',{features:[{name:'prefers-reduced-motion',value:'reduce'}]});assert.equal(await b.evaluate('getComputedStyle(document.querySelector(".tool-card")).transitionDuration'),'0s');
 const dir=path.join(root,'reports/homepage-qa');fs.mkdirSync(dir,{recursive:true});fs.writeFileSync(path.join(dir,'layout.json'),JSON.stringify({browser:b.version,checks:evidence,scope:'Scripted keyboard/layout probes; no screen reader or complete WCAG conformance claim'},null,2));
 for(const width of [390,1365]){await b.call('Emulation.setDeviceMetricsOverride',{width,height:900,deviceScaleFactor:1,mobile:false});await b.evaluate('document.documentElement.style.fontSize="100%";document.body.style.fontSize="100%";toolSearch.focus();window.scrollTo(0,0);true');const shot=await b.call('Page.captureScreenshot',{format:'png'});fs.writeFileSync(path.join(dir,`homepage-${width}.png`),Buffer.from(shot.data,'base64'));}
}));
test('no JavaScript retains complete canonical directory and category navigation',async()=>fixture(async(b)=>{
 await b.call('Emulation.setScriptExecutionDisabled',{value:true});await b.call('Page.reload');await delay(350);
 assert.equal(await b.evaluate('document.querySelectorAll("#toolGrid .tool-card").length'),87);assert.equal(await b.evaluate('[...document.querySelectorAll(".tool-card")].every(x=>x.getBoundingClientRect().height>0)'),true);assert.equal(await b.evaluate('document.querySelectorAll("[data-category-jump]").length'),8);assert.equal(await b.evaluate('getComputedStyle(document.getElementById("site-nav")).display'),'flex');await b.call('Emulation.setScriptExecutionDisabled',{value:false});
}));
test('isolated rejection preserves local search and prevents Google requests',async()=>fixture(async(b,google)=>{
 assert.deepEqual(google,[]);await b.evaluate('document.getElementById("edb-consent-reject").click();true');await set(b,'private marker');assert.deepEqual(google,[]);assert.equal(await b.evaluate('window["ga-disable-G-XDHPQYJ5CH"]'),true);
}));
test('isolated acceptance deduplicates sanitized views; withdrawal blocks later tracking',async()=>fixture(async(b,google)=>{
 assert.deepEqual(google,[]);await b.evaluate('document.getElementById("edb-consent-accept").click();true');await delay(200);await set(b,'PRIVATE_SEARCH_MARKER');await b.evaluate('document.getElementById("edb-consent-settings").click();document.getElementById("edb-consent-accept").click();true');
 const commands=await b.evaluate('(window.dataLayer||[]).map(x=>Array.from(x))');const views=commands.filter(x=>x[0]==='event');assert.equal(views.length,1);assert.equal(views[0][1],'page_view');assert.ok(!JSON.stringify(commands).includes('PRIVATE_SEARCH_MARKER'));assert.ok(!views[0][2].page_location.includes('?'));assert.equal(views[0][2].page_referrer,'');
 await b.evaluate('document.getElementById("edb-consent-settings").click();document.getElementById("edb-consent-reject").click();true');const n=google.length;await set(b,'JSON');assert.equal(google.length,n);assert.equal(await b.evaluate('window["ga-disable-G-XDHPQYJ5CH"]'),true);assert.equal(await b.evaluate('JSON.parse(localStorage.getItem("edb.analytics-consent.v1")).choice'),'rejected');assert.ok((await visible(b)).includes('json-formatter'));
}));
