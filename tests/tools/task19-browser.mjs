// Task 19 test-only wrapper: verify a fresh document after each same-URL reload.
// Keep the established CDP harness, isolated profiles and clipboard/download mocks.
import assert from 'node:assert/strict';
import {randomUUID} from 'node:crypto';
import {start as existingStart} from './task18-browser.mjs';
export {source,wait,set,click,upload,widths,noTransport} from './task18-browser.mjs';

export async function start(){
 const b=await existingStart(),originalLoad=b.load.bind(b),close=b.close.bind(b);
 const exceptions=[],unexpected=[];
 b.onEvent(message=>{
  if(message.method==='Runtime.exceptionThrown')exceptions.push(message.params.exceptionDetails);
  if(message.method==='Network.requestWillBeSent'){
   const url=message.params.request.url;
   if(/^https?:/.test(url)&&!url.startsWith('https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4'))unexpected.push(url);
  }
 });
 b.load=async source=>{
  const token=randomUUID(),script=await b.call('Page.addScriptToEvaluateOnNewDocument',{source:`window.__edb19Document=${JSON.stringify(token)}`});
  try{
   await originalLoad(source);
   const end=Date.now()+7000;let ready=false;
   while(Date.now()<end){try{ready=await b.evaluate(`window.__edb19Document===${JSON.stringify(token)}&&document.readyState==='complete'`);}catch{}if(ready)break;await new Promise(r=>setTimeout(r,20));}
   assert.ok(ready,'A fresh, fully loaded test document is required');
   if(!await b.evaluate('!!window.__edbClipboard'))await b.evaluate(`(()=>{
    window.__edbClipboard={mode:'success',value:null};window.__edbDownloads=[];
    Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async value=>{if(window.__edbClipboard.mode==='failure')throw Error('Fixture clipboard denial');window.__edbClipboard.value=value;}}});
    const create=URL.createObjectURL.bind(URL);URL.createObjectURL=blob=>{window.__edbDownloadBlob=blob;return create(blob);};
    document.addEventListener('click',event=>{const link=event.target.closest?.('a[download]');if(link){event.preventDefault();window.__edbDownloads.push(link.download);}},true);return true;
   })()`);
  }finally{await b.call('Page.removeScriptToEvaluateOnNewDocument',{identifier:script.identifier});}
 };
 b.close=async()=>{await close();assert.deepEqual(exceptions,[],'No uncaught application JavaScript errors');assert.deepEqual(unexpected,[],'No unexpected HTTP(S) requests from utility processing');};
 return b;
}
