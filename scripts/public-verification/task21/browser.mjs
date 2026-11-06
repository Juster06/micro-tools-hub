// Actual public HTTPS; no production response substitution or request blocking.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {randomUUID} from 'node:crypto';
import {launchBrowser,findBrowser} from '../../tool-tests/browser.mjs';
export const ORIGIN='https://everydaydigitalbox.com';
const registry=JSON.parse(fs.readFileSync(new URL('../../../TOOL_REGISTRY.json',import.meta.url),'utf8'));
const paths=new Set(['/', '/index.html','/privacy.html','/favicon.ico','/assets/consent.js','/assets/vendor/task21/format-source.js','/assets/vendor/task21/css-source.js','/assets/vendor/task21/javascript-source.js','/assets/vendor/task21/markup-source.js',...registry.tools.filter(t=>['TESTED','RELEASED'].includes(t.status)).flatMap(t=>['/'+t.directory_path+'/','/'+t.directory_path+'/index.html'])]);
const canary=u=>u.origin===ORIGIN&&u.pathname==='/assets/consent.js'&&u.searchParams.has('edb_task21_canary');
export const source=id=>ORIGIN+'/'+id+'/index.html';
export async function wait(b,expression,timeout=6500){const end=Date.now()+timeout;while(Date.now()<end){try{if(await b.evaluate(`Boolean(${expression})`))return;}catch{}await new Promise(r=>setTimeout(r,25));}assert.fail('Expected live browser state: '+expression);}
export async function set(b,id,value){return b.evaluate(`(()=>{const e=document.getElementById(${JSON.stringify(id)});e.value=${JSON.stringify(value)};e.dispatchEvent(new Event('input',{bubbles:true}));return true})()`);}
export async function click(b,id){return b.evaluate(`document.getElementById(${JSON.stringify(id)}).click();true`);}
export async function run(b,input,options={}){await set(b,'toolInput',input);for(const[k,v]of Object.entries(options))await set(b,k,v);await click(b,'runBtn');await wait(b,"!runBtn.disabled&&(toolStatus.textContent==='Complete.'||!toolError.hidden)");return b.evaluate("({text:toolOutput.value,error:toolError.hidden?'':toolError.textContent,status:toolStatus.textContent,summary:toolSummary.textContent,warning:toolWarning.textContent})");}
export async function widths(b){for(const width of [320,375,768,1440]){await b.call('Emulation.setDeviceMetricsOverride',{width,height:900,deviceScaleFactor:1,mobile:false});assert.equal(await b.evaluate('document.documentElement.scrollWidth>innerWidth'),false,`public overflow at ${width}`);}await b.call('Emulation.clearDeviceMetricsOverride');}
export async function start(label='functional'){
 fs.mkdirSync(new URL('../../../reports/public-task21/',import.meta.url),{recursive:true});
 const b=await launchBrowser(findBrowser());await b.call('Network.setBlockedURLs',{urls:[]});await b.call('Log.enable');
 const record={label,started_at:new Date().toISOString(),browser:b.version,scope:'Fresh actual public HTTPS; no request interception, production response substitution or external-request blocking. Clipboard/download captured only. Synthetic QA inputs; no request bodies/console arguments retained.',pages:[],requests:[],responses:[],console_errors:[],exceptions:[],unexpected_dependencies:[],google_requests:0,canary_requests:[],instrumentation_errors:[]};b.record=record;
 const requestIds=new Map();
 b.onEvent(m=>{const p=m.params;
  if(m.method==='Network.requestWillBeSent'){
   let u;try{u=new URL(p.request.url);}catch{return;}
   const allowed=(u.origin===ORIGIN&&paths.has(u.pathname)&&!u.search)||(u.origin==='https://cdn.jsdelivr.net'&&u.pathname==='/npm/@tailwindcss/browser@4')||canary(u);
   const safe=canary(u)?u.href:allowed?u.origin+u.pathname:/^https?:$/.test(u.protocol)?u.origin+'/[unexpected-path]':u.protocol+'[local-object]';
   const request={url:safe,type:p.type,method:p.request.method,child:!!m.sessionId};record.requests.push(request);requestIds.set((m.sessionId??'')+':'+p.requestId,safe);
   if(canary(u))record.canary_requests.push(request);
   if(/googletagmanager\.com|google-analytics\.com/.test(u.hostname))record.google_requests++;
   if(/^https?:$/.test(u.protocol)&&!allowed)record.unexpected_dependencies.push(request);
  }
  if(m.method==='Network.responseReceived')record.responses.push({url:requestIds.get((m.sessionId??'')+':'+p.requestId)??'[unassociated]',status:p.response.status,type:p.type,mime:p.response.mimeType,child:!!m.sessionId});
  if(m.method==='Log.entryAdded'&&p.entry.level==='error'){const text=p.entry.text??'';const classification=/unsafe attempt to initiate navigation/i.test(text)?'sandbox-blocked-navigation':/blocked opening/i.test(text)&&/sandbox/i.test(text)?'sandbox-blocked-popup':/blocked form submission|form-action/i.test(text)?'sandbox-or-csp-blocked-form':null;record.console_errors.push({source:p.entry.source,url:p.entry.url||'',expected_security_probe:!!record.security_probe_active,classification,message:'Console error recorded; text omitted to avoid capturing input.'});}
  if(m.method==='Runtime.exceptionThrown')record.exceptions.push({url:p.exceptionDetails.url||'',line:p.exceptionDetails.lineNumber,column:p.exceptionDetails.columnNumber,child:!!m.sessionId});
 });
 b.load=async url=>{assert.ok(url.startsWith(ORIGIN+'/'));const token=randomUUID(),hook=await b.call('Page.addScriptToEvaluateOnNewDocument',{source:`window.__publicDocument=${JSON.stringify(token)}`});try{await b.call('Page.navigate',{url});await wait(b,`window.__publicDocument===${JSON.stringify(token)}&&location.href===${JSON.stringify(url)}&&document.readyState==='complete'&&!!document.getElementById('edb-consent-root')`,20000);}finally{await b.call('Page.removeScriptToEvaluateOnNewDocument',{identifier:hook.identifier});}
  if(await b.evaluate('!document.getElementById("edb-consent-panel").hidden'))await click(b,'edb-consent-reject');
  record.pages.push({url,checked_at:new Date().toISOString(),title:await b.evaluate('document.title')});
  await b.evaluate(`(()=>{window.__edbClipboard={mode:'success',value:null};window.__edbDownloads=[];Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async value=>{if(window.__edbClipboard.mode==='failure')throw Error('Fixture clipboard denial');window.__edbClipboard.value=value;}}});const create=URL.createObjectURL.bind(URL);URL.createObjectURL=blob=>{window.__edbDownloadBlob=blob;return create(blob);};document.addEventListener('click',event=>{const a=event.target.closest?.('a[download]');if(a){event.preventDefault();window.__edbDownloads.push(a.download);}},true);return true})()`);
 };
 const close=b.close.bind(b);b.close=async()=>{record.finished_at=new Date().toISOString();fs.writeFileSync(new URL('../../../reports/public-task21/live-'+label+'.json',import.meta.url),JSON.stringify(record,null,2)+'\n');await close();assert.equal(record.google_requests,0);assert.deepEqual(record.unexpected_dependencies,[]);assert.deepEqual(record.exceptions,[]);assert.deepEqual(record.instrumentation_errors,[]);assert.deepEqual(record.responses.filter(r=>r.status>=400&&!r.url.endsWith('/favicon.ico')),[]);assert.ok(record.console_errors.every(e=>e.url.endsWith('/favicon.ico')||(e.expected_security_probe&&e.classification)),'Unexpected public console error');};
 return b;
}
