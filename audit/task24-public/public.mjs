import assert from 'node:assert/strict';
import fs from 'node:fs';
import {randomUUID} from 'node:crypto';
import {launchBrowser,findBrowser} from './browser-transport.mjs';
export const ORIGIN='https://everydaydigitalbox.com';
const registry=JSON.parse(fs.readFileSync(new URL('./approved-registry.json',import.meta.url),'utf8'));
const sources=JSON.parse(fs.readFileSync(new URL('./public-source-verification.json',import.meta.url),'utf8'));
const allowedPaths=new Set(['/', '/favicon.ico',...Object.keys(sources.sources).map(p=>'/'+p),...registry.tools.filter(t=>['TESTED','RELEASED'].includes(t.status)).map(t=>'/'+t.directory_path+'/')]);
export const source=id=>ORIGIN+'/'+id+'/index.html';
export async function wait(b,expr,timeout=20000){const end=Date.now()+timeout;while(Date.now()<end){try{if(await b.evaluate(`Boolean(${expr})`))return;}catch{}await new Promise(r=>setTimeout(r,30));}assert.fail('Expected public browser state not reached: '+expr);}
export const set=(b,id,value)=>b.evaluate(`(()=>{const e=document.getElementById(${JSON.stringify(id)});e.value=${JSON.stringify(value)};e.dispatchEvent(new Event('input',{bubbles:true}));return true})()`);
export const click=(b,id)=>b.evaluate(`document.getElementById(${JSON.stringify(id)}).click();true`);
export async function run(b,input,options={}){await set(b,'toolInput',input);for(const[k,v]of Object.entries(options))await set(b,k,v);await click(b,'runBtn');await wait(b,"toolStatus.textContent==='Complete.'||!toolError.hidden");return b.evaluate("({text:toolOutput.value,error:toolError.hidden?'':toolError.textContent,status:toolStatus.textContent})");}
export async function start(){
 const b=await launchBrowser(findBrowser());await b.call('Network.setBlockedURLs',{urls:[]});await b.call('Log.enable');
 // Deny OS file writes as a second guard; the actual page's download action is
 // captured in memory below without substituting any deployed source/response.
 await b.call('Browser.setDownloadBehavior',{behavior:'deny'});
 const record={started_at:new Date().toISOString(),browser:b.version,scope:'Fresh public HTTPS, actual deployed HTML/JS/CDN/consent; no response substitution, external-request blocking or Google stubs. Synthetic QA inputs; clipboard/download capture only.',pages:[],requests:[],responses:[],console_errors:[],exceptions:[],unexpected_dependencies:[],google_requests:0,input_transport_requests:0};b.record=record;
 const requestIds=new Map();
 b.onEvent(m=>{
  const p=m.params;
  if(m.method==='Network.requestWillBeSent'){
   let u;try{u=new URL(p.request.url);}catch{return;}
   const allowed=(u.origin===ORIGIN&&allowedPaths.has(u.pathname)&&!u.search)||(u.origin==='https://cdn.jsdelivr.net'&&u.pathname==='/npm/@tailwindcss/browser@4');
   const safe=allowed?u.origin+u.pathname:/^https?:$/.test(u.protocol)?u.origin+'/[unexpected-path]':u.protocol+'[local-object]';
   const item={url:safe,type:p.type,method:p.request.method};record.requests.push(item);requestIds.set(p.requestId,safe);
   if(/googletagmanager\.com|google-analytics\.com/.test(u.hostname))record.google_requests++;
   if(/^https?:$/.test(u.protocol)&&!allowed)record.unexpected_dependencies.push(item);
   if((p.request.url+' '+(p.request.postData||'')).includes('edb241-local-only'))record.input_transport_requests++;
  }
  if(m.method==='Network.responseReceived')record.responses.push({url:requestIds.get(p.requestId)||'[unassociated]',status:p.response.status,mime:p.response.mimeType,type:p.type});
  if(m.method==='Log.entryAdded'&&p.entry.level==='error')record.console_errors.push({source:p.entry.source,url:p.entry.url||'',message:'Browser console error; text omitted to avoid retaining inputs.'});
  if(m.method==='Runtime.consoleAPICalled'&&p.type==='error')record.console_errors.push({source:'console-api',url:'',message:'Console.error called; arguments omitted.'});
  if(m.method==='Runtime.exceptionThrown')record.exceptions.push({url:p.exceptionDetails.url||'',line:p.exceptionDetails.lineNumber,column:p.exceptionDetails.columnNumber});
 });
 b.load=async url=>{
  assert.ok(url.startsWith(ORIGIN+'/'));const token=randomUUID(),hook=await b.call('Page.addScriptToEvaluateOnNewDocument',{source:`window.__publicDocument=${JSON.stringify(token)}`});
  try{await b.call('Page.navigate',{url});await wait(b,`window.__publicDocument===${JSON.stringify(token)}&&location.href===${JSON.stringify(url)}&&document.readyState==='complete'&&!!document.getElementById('edb-consent-root')`);}finally{await b.call('Page.removeScriptToEvaluateOnNewDocument',{identifier:hook.identifier});}
  if(await b.evaluate('!document.getElementById("edb-consent-panel").hidden'))await click(b,'edb-consent-reject');
  record.pages.push({url,checked_at:new Date().toISOString(),title:await b.evaluate('document.title')});
  await b.evaluate(`(()=>{window.__edbClipboard={mode:'success',value:null};window.__edbDownloads=[];window.__edbRevoked=0;Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async text=>{if(__edbClipboard.mode==='failure')throw Error('Fixture clipboard denial');__edbClipboard.value=text;}}});const create=URL.createObjectURL.bind(URL),revoke=URL.revokeObjectURL.bind(URL);URL.createObjectURL=blob=>{window.__edbDownloadBlob=blob;return create(blob)};URL.revokeObjectURL=url=>{__edbRevoked++;revoke(url)};document.addEventListener('click',e=>{const a=e.target.closest?.('a[download]');if(a){e.preventDefault();__edbDownloads.push(a.download)}},true);return true})()`);
 };
 const close=b.close.bind(b);b.close=async()=>{record.completed_at=new Date().toISOString();fs.writeFileSync(new URL('./live-functional.json',import.meta.url),JSON.stringify(record,null,2)+'\n');await close();};
 return b;
}
export function checkRecord(r){
 assert.equal(r.google_requests,0);assert.equal(r.input_transport_requests,0);assert.deepEqual(r.exceptions,[]);assert.deepEqual(r.unexpected_dependencies,[]);assert.ok(r.console_errors.every(e=>e.url.endsWith('/favicon.ico')),'Unexpected public console error');assert.deepEqual(r.responses.filter(x=>x.status>=400&&!x.url.endsWith('/favicon.ico')),[]);
}
