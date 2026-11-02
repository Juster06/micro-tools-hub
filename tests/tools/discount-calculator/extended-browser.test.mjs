import {test,before,beforeEach,afterEach,after} from 'node:test';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import {launchBrowser,findBrowser} from '../../../scripts/tool-tests/browser.mjs';
const source=fileURLToPath(new URL('../../../discount-calculator/index.html',import.meta.url));
let browser;const second="25";
const seed="100",expected="Original price: 100.00\nDiscount: 25%\nSavings: 25.00\nFinal price: 75.00\nFormula: savings = price × discount / 100; final = price − savings",next="200",nextExpected="Original price: 200.00\nDiscount: 25%\nSavings: 50.00\nFinal price: 150.00\nFormula: savings = price × discount / 100; final = price − savings";
const pause=ms=>new Promise(resolve=>setTimeout(resolve,ms));
async function wait(expression){for(let i=0;i<200;i++){if(await browser.evaluate(`Boolean(${expression})`))return;await pause(25);}assert.fail('Expected current DOM state');}
const value=id=>browser.evaluate(`document.getElementById(${JSON.stringify(id)}).value`);
async function input(text){await browser.evaluate(`(text=>{const e=document.getElementById('toolInput');e.value=text;e.dispatchEvent(new Event('input',{bubbles:true}));})(${JSON.stringify(text)})`);}
async function current(){await input(seed);await wait(`document.getElementById('toolOutput').value===${JSON.stringify(expected)}`);}
before(async()=>{
  assert.ok(findBrowser(),'Installed Chromium required');browser=await launchBrowser(findBrowser());
  await browser.call('Page.addScriptToEvaluateOnNewDocument',{source:"window.__errors=[];addEventListener('error',e=>{if(e.error)__errors.push(String(e.message));});addEventListener('unhandledrejection',e=>__errors.push(String(e.reason)));"});
});
beforeEach(async()=>{await browser.load(source);await browser.evaluate(`document.getElementById('secondValue').value=${JSON.stringify(second)};true`);});
afterEach(async()=>assert.deepEqual(await browser.evaluate('window.__errors'),[]));
after(async()=>{if(browser)await browser.close();});

test('rapid input invalidates result/actions/statistics immediately and settles latest only',async()=>{
  await current();
  const immediate=await browser.evaluate(`(text=>{const e=document.getElementById('toolInput');for(const value of ['old','older',text]){e.value=value;e.dispatchEvent(new Event('input'));}return {text:document.getElementById('toolOutput').value,copy:document.getElementById('copyBtn').disabled,download:document.getElementById('downloadBtn').disabled,counts:[...document.querySelectorAll('.stat dd')].map(e=>e.textContent)};})(${JSON.stringify(next)})`);
  assert.equal(immediate.text,'');assert.equal(immediate.copy,true);assert.equal(immediate.download,true);assert.ok(immediate.counts.every(c=>c==='—'));
  await wait(`document.getElementById('toolOutput').value===${JSON.stringify(nextExpected)}`);assert.equal(await value('toolInput'),next);
});
test('rapid setting changes invalidate obsolete preview and honor final setting',async()=>{
  await current();await browser.evaluate("for(const precision of ['0','4','6','2']){const e=document.getElementById('precision');e.value=precision;e.dispatchEvent(new Event('change'));}true");assert.equal(await value('toolOutput'),'');await wait(`document.getElementById('toolOutput').value===${JSON.stringify(expected)}`);
});
test('late clipboard success cannot report an obsolete result',async()=>{
  await current();await browser.evaluate("navigator.clipboard.writeText=()=>new Promise(resolve=>{window.__resolve=resolve;});document.getElementById('copyBtn').click();true");
  await input(next);await browser.evaluate('window.__resolve();true');await wait(`document.getElementById('toolOutput').value===${JSON.stringify(nextExpected)}`);
  assert.doesNotMatch(await browser.evaluate("document.getElementById('toolStatus').textContent"),/copied/);
});
test('late clipboard denial cannot steal focus after Clear',async()=>{
  await current();await browser.evaluate("navigator.clipboard.writeText=()=>new Promise((resolve,reject)=>{window.__reject=reject;});document.getElementById('copyBtn').click();document.getElementById('clearBtn').click();window.__reject(Error('denied'));true");await pause(30);
  assert.equal(await browser.evaluate('document.activeElement.id'),'toolInput');assert.match(await browser.evaluate("document.getElementById('toolStatus').textContent"),/Cleared/);assert.equal(await value('toolOutput'),'');
});
test('UTF-8 Blob bytes, MIME, fixed filename and URL revocation are exact',async()=>{
  await current();await browser.evaluate("const revoke=URL.revokeObjectURL.bind(URL);URL.revokeObjectURL=url=>{window.__revoked=url;revoke(url);};document.getElementById('downloadBtn').click();true");
  assert.deepEqual(await browser.evaluate('window.__edbDownloads'),['discount-calculator-output.txt']);assert.equal(await browser.evaluate('window.__edbDownloadBlob.text()'),expected);assert.equal(await browser.evaluate('window.__edbDownloadBlob.size'),Buffer.byteLength(expected));assert.equal(await browser.evaluate('window.__edbDownloadBlob.type'),'text/plain;charset=utf-8');await wait("typeof window.__revoked==='string'");
});
test('download failure cleans link and object URL with truthful message',async()=>{
  await current();await browser.evaluate("const revoke=URL.revokeObjectURL.bind(URL);URL.revokeObjectURL=url=>{window.__revoked=url;revoke(url);};HTMLAnchorElement.prototype.click=()=>{throw Error('denied');};document.getElementById('downloadBtn').click();true");
  assert.match(await browser.evaluate("document.getElementById('toolStatus').textContent"),/Download unavailable/);assert.equal(await browser.evaluate("document.querySelectorAll('a[download]').length"),0);await wait("typeof window.__revoked==='string'");assert.equal(await value('toolOutput'),expected);
});
test('oversized original is retained; no stale actions; recovery works',async()=>{
  await current();const text='x'.repeat(65);await input(text);assert.equal(await value('toolInput'),text);assert.equal(await value('toolOutput'),'');assert.equal(await browser.evaluate("document.getElementById('copyBtn').disabled&&document.getElementById('downloadBtn').disabled"),true);await browser.evaluate("document.getElementById('runBtn').click();true");assert.match(await browser.evaluate("document.getElementById('toolError').textContent"),/UTF-16/);await current();
});
test('simulated composition invalidates results and Clear restores Run/defaults',async()=>{
  await current();await browser.evaluate("document.getElementById('toolInput').dispatchEvent(new CompositionEvent('compositionstart',{bubbles:true}));true");await input(next);await pause(160);assert.equal(await value('toolOutput'),'');assert.equal(await browser.evaluate("document.getElementById('runBtn').disabled"),true);
  await browser.evaluate("document.getElementById('toolInput').dispatchEvent(new CompositionEvent('compositionend',{bubbles:true}));true");await wait(`document.getElementById('toolOutput').value===${JSON.stringify(nextExpected)}`);
  await browser.evaluate("document.getElementById('toolInput').dispatchEvent(new CompositionEvent('compositionstart',{bubbles:true}));document.getElementById('clearBtn').click();true");assert.equal(await browser.evaluate("document.getElementById('runBtn').disabled"),false);assert.equal(await value('toolInput'),"");assert.equal(await value('precision'),'2');assert.equal(await value('secondValue'),'');
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
test('second field invalidates all output/counts immediately and restores only current calculation',async()=>{await current();const state=await browser.evaluate("const e=document.getElementById('secondValue');e.value='NaN';e.dispatchEvent(new Event('input'));({output:document.getElementById('toolOutput').value,disabled:document.getElementById('copyBtn').disabled,counts:[...document.querySelectorAll('.stat dd')].map(e=>e.textContent)})");assert.equal(state.output,'');assert.equal(state.disabled,true);assert.ok(state.counts.every(v=>v==='—'));await browser.evaluate("document.getElementById('runBtn').click();true");assert.match(await browser.evaluate("document.getElementById('toolError').textContent"),/finite decimal/);await browser.evaluate(`document.getElementById('secondValue').value=${JSON.stringify(second)};true`);await current();});
test('precision changes preserve inputs and show exact fixed decimal output',async()=>{await current();for(const precision of ['0','4','6','2']){await browser.evaluate(`(() => {const e=document.getElementById('precision');e.value=${JSON.stringify(precision)};e.dispatchEvent(new Event('change'));return true;})()`);assert.equal(await value('toolOutput'),'');await wait('document.getElementById("toolOutput").value.length>0');assert.equal(await value('toolInput'),seed);assert.equal(await value('secondValue'),second);assert.equal(await browser.evaluate("document.getElementById('precisionCount').textContent"),precision);}assert.equal(await value('toolOutput'),expected);});
test('secondary oversized input is preserved, disables export and recovers',async()=>{await current();await browser.evaluate("const e=document.getElementById('secondValue');e.value='1'.repeat(65);e.dispatchEvent(new Event('input'));document.getElementById('runBtn').click();true");assert.equal((await value('secondValue')).length,65);assert.equal(await value('toolOutput'),'');assert.match(await browser.evaluate("document.getElementById('toolError').textContent"),/64 UTF-16/);await browser.evaluate(`document.getElementById('secondValue').value=${JSON.stringify(second)};true`);await current();});
