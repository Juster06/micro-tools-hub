import {test,before,beforeEach,afterEach,after} from 'node:test';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import {launchBrowser,findBrowser} from '../../../scripts/tool-tests/browser.mjs';
const source=fileURLToPath(new URL('../../../uuid-generator/index.html',import.meta.url));
let browser;
const seed="1",expected="00000000-0000-4000-8000-000000000000",next="2",nextExpected="00000000-0000-4000-8000-000000000000\n00000000-0000-4000-8000-000000000000";
const pause=ms=>new Promise(resolve=>setTimeout(resolve,ms));
async function wait(expression){for(let i=0;i<200;i++){if(await browser.evaluate(`Boolean(${expression})`))return;await pause(25);}assert.fail('Expected current DOM state');}
const value=id=>browser.evaluate(`document.getElementById(${JSON.stringify(id)}).value`);
async function input(text){await browser.evaluate(`(text=>{const e=document.getElementById('toolInput');e.value=text;e.dispatchEvent(new Event('input',{bubbles:true}));})(${JSON.stringify(text)})`);}
async function current(){await input(seed);await browser.evaluate("document.getElementById('runBtn').click();true");await wait(`document.getElementById('toolOutput').value===${JSON.stringify(expected)}`);}
before(async()=>{
  assert.ok(findBrowser(),'Installed Chromium required');browser=await launchBrowser(findBrowser());
  await browser.call('Page.addScriptToEvaluateOnNewDocument',{source:"window.__errors=[];addEventListener('error',e=>{if(e.error)__errors.push(String(e.message));});addEventListener('unhandledrejection',e=>__errors.push(String(e.reason)));"});
});
beforeEach(async()=>{await browser.load(source);await browser.evaluate("window.__realRandom=crypto.getRandomValues.bind(crypto);window.__randomCalls=[];crypto.getRandomValues=bytes=>{window.__randomCalls.push(bytes.length);bytes.fill(0);return bytes;};true");});
afterEach(async()=>assert.deepEqual(await browser.evaluate('window.__errors'),[]));
after(async()=>{if(browser)await browser.close();});

test('rapid input invalidates result/actions/statistics immediately and settles latest only',async()=>{
  await current();
  const immediate=await browser.evaluate(`(text=>{const e=document.getElementById('toolInput');for(const value of ['old','older',text]){e.value=value;e.dispatchEvent(new Event('input'));}return {text:document.getElementById('toolOutput').value,copy:document.getElementById('copyBtn').disabled,download:document.getElementById('downloadBtn').disabled,counts:[...document.querySelectorAll('.stat dd')].map(e=>e.textContent)};})(${JSON.stringify(next)})`);
  assert.equal(immediate.text,'');assert.equal(immediate.copy,true);assert.equal(immediate.download,true);assert.ok(immediate.counts.every(c=>c==='—'));
  await browser.evaluate("document.getElementById('runBtn').click();true");await wait(`document.getElementById('toolOutput').value===${JSON.stringify(nextExpected)}`);assert.equal(await value('toolInput'),next);
});
test('rapid setting changes invalidate obsolete preview and honor final setting',async()=>{
  await current();await browser.evaluate("document.getElementById('uppercase').click();true");assert.equal(await value('toolOutput'),'');await browser.evaluate("document.getElementById('runBtn').click();true");assert.equal(await value('toolOutput'),expected.toUpperCase());
});
test('late clipboard success cannot report an obsolete result',async()=>{
  await current();await browser.evaluate("navigator.clipboard.writeText=()=>new Promise(resolve=>{window.__resolve=resolve;});document.getElementById('copyBtn').click();true");
  await input(next);await browser.evaluate('window.__resolve();true');await browser.evaluate("document.getElementById('runBtn').click();true");await wait(`document.getElementById('toolOutput').value===${JSON.stringify(nextExpected)}`);
  assert.doesNotMatch(await browser.evaluate("document.getElementById('toolStatus').textContent"),/copied/);
});
test('late clipboard denial cannot steal focus after Clear',async()=>{
  await current();await browser.evaluate("navigator.clipboard.writeText=()=>new Promise((resolve,reject)=>{window.__reject=reject;});document.getElementById('copyBtn').click();document.getElementById('clearBtn').click();window.__reject(Error('denied'));true");await pause(30);
  assert.equal(await browser.evaluate('document.activeElement.id'),'toolInput');assert.match(await browser.evaluate("document.getElementById('toolStatus').textContent"),/Cleared/);assert.equal(await value('toolOutput'),'');
});
test('UTF-8 Blob bytes, MIME, fixed filename and URL revocation are exact',async()=>{
  await current();await browser.evaluate("const revoke=URL.revokeObjectURL.bind(URL);URL.revokeObjectURL=url=>{window.__revoked=url;revoke(url);};document.getElementById('downloadBtn').click();true");
  assert.deepEqual(await browser.evaluate('window.__edbDownloads'),['uuid-generator-output.txt']);assert.equal(await browser.evaluate('window.__edbDownloadBlob.text()'),expected);assert.equal(await browser.evaluate('window.__edbDownloadBlob.size'),Buffer.byteLength(expected));assert.equal(await browser.evaluate('window.__edbDownloadBlob.type'),'text/plain;charset=utf-8');await wait("typeof window.__revoked==='string'");
});
test('download failure cleans link and object URL with truthful message',async()=>{
  await current();await browser.evaluate("const revoke=URL.revokeObjectURL.bind(URL);URL.revokeObjectURL=url=>{window.__revoked=url;revoke(url);};HTMLAnchorElement.prototype.click=()=>{throw Error('denied');};document.getElementById('downloadBtn').click();true");
  assert.match(await browser.evaluate("document.getElementById('toolStatus').textContent"),/Download unavailable/);assert.equal(await browser.evaluate("document.querySelectorAll('a[download]').length"),0);await wait("typeof window.__revoked==='string'");assert.equal(await value('toolOutput'),expected);
});
test('oversized original is retained; no stale actions; recovery works',async()=>{
  await current();const text='x'.repeat(5);await input(text);assert.equal(await value('toolInput'),text);assert.equal(await value('toolOutput'),'');assert.equal(await browser.evaluate("document.getElementById('copyBtn').disabled&&document.getElementById('downloadBtn').disabled"),true);await browser.evaluate("document.getElementById('runBtn').click();true");assert.match(await browser.evaluate("document.getElementById('toolError').textContent"),/UTF-16/);await current();
});
test('simulated composition invalidates results and Clear restores Run/defaults',async()=>{
  await current();await browser.evaluate("document.getElementById('toolInput').dispatchEvent(new CompositionEvent('compositionstart',{bubbles:true}));true");await input(next);await pause(160);assert.equal(await value('toolOutput'),'');assert.equal(await browser.evaluate("document.getElementById('runBtn').disabled"),true);
  await browser.evaluate("document.getElementById('toolInput').dispatchEvent(new CompositionEvent('compositionend',{bubbles:true}));true");await browser.evaluate("document.getElementById('runBtn').click();true");await wait(`document.getElementById('toolOutput').value===${JSON.stringify(nextExpected)}`);
  await browser.evaluate("document.getElementById('toolInput').dispatchEvent(new CompositionEvent('compositionstart',{bubbles:true}));document.getElementById('clearBtn').click();true");assert.equal(await browser.evaluate("document.getElementById('runBtn').disabled"),false);assert.equal(await value('toolInput'),"1");assert.equal(await browser.evaluate("document.getElementById('uppercase').checked"),false);
});
test('safe rendering and processing make no probed transport/storage calls',async()=>{
  await browser.evaluate("window.__calls=[];window.fetch=()=>{__calls.push('fetch');throw Error('Unexpected fetch');};XMLHttpRequest.prototype.open=()=>__calls.push('xhr');navigator.sendBeacon=()=>{__calls.push('beacon');return false;};window.WebSocket=function(){__calls.push('socket');};window.EventSource=function(){__calls.push('events');};Storage.prototype.setItem=()=>__calls.push('storage');indexedDB.open=()=>{__calls.push('idb');throw Error('Unexpected database');};true");
  const text='<img src=x onerror=alert(1)> 😀';await input(text);await browser.evaluate("document.getElementById('runBtn').click();true");assert.equal(await value('toolInput'),text);assert.equal(await browser.evaluate("document.querySelectorAll('main img,main script').length"),0);assert.deepEqual(await browser.evaluate('window.__calls'),[]);
});
test('missing clipboard selects current result; native labels/status/output/Tab are usable',async()=>{
  await current();assert.equal(await browser.evaluate("Array.from(document.querySelectorAll('textarea,select,input')).every(e=>e.labels.length>0)"),true);assert.equal(await browser.evaluate("document.getElementById('toolOutput').readOnly"),true);assert.equal(await browser.evaluate("document.getElementById('toolStatus').getAttribute('role')"),'status');
  await browser.evaluate("Object.defineProperty(navigator,'clipboard',{configurable:true,value:undefined});document.getElementById('copyBtn').click();true");assert.equal(await browser.evaluate('document.activeElement.id'),'toolOutput');assert.equal(await browser.evaluate("document.getElementById('toolOutput').selectionEnd"),expected.length);
  await browser.call('Input.dispatchKeyEvent',{type:'rawKeyDown',key:'Tab',code:'Tab',windowsVirtualKeyCode:9});await browser.call('Input.dispatchKeyEvent',{type:'keyUp',key:'Tab',code:'Tab',windowsVirtualKeyCode:9});assert.equal(await browser.evaluate('document.activeElement.id'),'copyBtn');
});
test('actual browser cryptographic source generates fresh valid maximum batches',async()=>{await browser.evaluate('crypto.getRandomValues=window.__realRandom;true');await input('1000');await browser.evaluate("document.getElementById('runBtn').click();true");const first=await value('toolOutput'),rows=first.split('\n');assert.equal(rows.length,1000);assert.equal(first.length,36999);assert.equal(new Set(rows).size,1000);for(const row of rows)assert.match(row,/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/);await browser.evaluate("document.getElementById('runBtn').click();true");assert.notEqual(await value('toolOutput'),first);});
test('missing crypto or secure context fail closed and recover',async()=>{await current();await browser.evaluate("Object.defineProperty(window,'isSecureContext',{configurable:true,value:false});document.getElementById('runBtn').click();true");assert.equal(await value('toolOutput'),'');assert.match(await browser.evaluate("document.getElementById('toolError').textContent"),/secure context/);await browser.evaluate("Object.defineProperty(window,'isSecureContext',{configurable:true,value:true});crypto.getRandomValues=undefined;document.getElementById('runBtn').click();true");assert.equal(await value('toolOutput'),'');assert.equal(await browser.evaluate("document.getElementById('copyBtn').disabled"),true);await browser.evaluate('crypto.getRandomValues=window.__realRandom;true');await input('1');await browser.evaluate("document.getElementById('runBtn').click();true");assert.equal((await value('toolOutput')).length,36);});
test('throwing random source has no Math.random fallback and zero stale actions',async()=>{await current();await browser.evaluate("crypto.getRandomValues=()=>{throw Error('fixture crypto failure');};Math.random=()=>{throw Error('forbidden random fallback');};document.getElementById('runBtn').click();true");assert.equal(await value('toolOutput'),'');assert.match(await browser.evaluate("document.getElementById('toolError').textContent"),/generation failed/);assert.equal(await browser.evaluate("document.getElementById('copyBtn').disabled&&document.getElementById('downloadBtn').disabled"),true);});
test('generation is manual and entropy request size is exactly bounded',async()=>{await input('2');await pause(180);assert.equal(await browser.evaluate('window.__randomCalls.length'),0);await browser.evaluate("document.getElementById('runBtn').click();true");assert.deepEqual(await browser.evaluate('window.__randomCalls'),[32]);assert.equal(await value('toolOutput'),Array(2).fill(expected).join('\n'));await browser.evaluate("document.getElementById('uppercase').click();true");assert.equal(await value('toolOutput'),'');await pause(180);assert.deepEqual(await browser.evaluate('window.__randomCalls'),[32]);await browser.evaluate("document.getElementById('runBtn').click();true");assert.equal(await value('toolOutput'),Array(2).fill(expected.toUpperCase()).join('\n'));});
