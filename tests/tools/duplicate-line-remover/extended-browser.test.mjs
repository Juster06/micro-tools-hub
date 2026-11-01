import {test,before,beforeEach,afterEach,after} from 'node:test';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import {launchBrowser,findBrowser} from '../../../scripts/tool-tests/browser.mjs';

const source=fileURLToPath(new URL('../../../duplicate-line-remover/index.html',import.meta.url));
let browser;
before(async()=>{
  const executable=findBrowser();assert.ok(executable,'Installed Chromium required');browser=await launchBrowser(executable);
  await browser.call('Page.addScriptToEvaluateOnNewDocument',{source:"window.__errors=[];addEventListener('error',e=>{if(e.error)__errors.push(String(e.message));});addEventListener('unhandledrejection',e=>__errors.push(String(e.reason)));"});
});
beforeEach(async()=>{await browser.load(source);});
afterEach(async()=>{assert.deepEqual(await browser.evaluate('window.__errors'),[],'No uncaught JavaScript errors or promise rejections');});
after(async()=>{if(browser)await browser.close();});
const pause=ms=>new Promise(resolve=>setTimeout(resolve,ms));
async function wait(expression) {
  for(let i=0;i<200;i++){if(await browser.evaluate(`Boolean(${expression})`))return;await pause(25);}
  assert.fail('Expected DOM result did not become current');
}
const value=id=>browser.evaluate(`document.getElementById(${JSON.stringify(id)}).value`);
async function input(text){await browser.evaluate(`(text=>{const e=document.getElementById('toolInput');e.value=text;e.dispatchEvent(new Event('input',{bubbles:true}));})(${JSON.stringify(text)})`);}
const output=()=>value('toolOutput');

test('input immediately invalidates stale text, buttons and counts before rapid typing settles',async()=>{
  await input('old\nold');await wait("document.getElementById('toolOutput').value==='old'");
  const state=await browser.evaluate("(()=>{const e=document.getElementById('toolInput');for(const value of ['a\\na','ab\\nab','new\\nnew']){e.value=value;e.dispatchEvent(new Event('input'));}return {text:document.getElementById('toolOutput').value,disabled:document.getElementById('copyBtn').disabled&&document.getElementById('downloadBtn').disabled,count:document.getElementById('retainedCount').textContent};})()");
  assert.deepEqual(state,{text:'',disabled:true,count:'—'});await wait("document.getElementById('toolOutput').value==='new'");assert.equal(await value('toolInput'),'new\nnew');
});
test('rapid option changes use only latest settings and preserve original',async()=>{
  await input(' Apple \napple\nAPPLE\n');await wait("document.getElementById('toolOutput').value.length>0");
  const immediate=await browser.evaluate("(()=>{for(const [id,checked] of [['ignoreCase',true],['trimComparison',true],['sort',true],['removeBlankLines',true],['ignoreCase',false]]){const e=document.getElementById(id);e.checked=checked;e.dispatchEvent(new Event('change'));}return document.getElementById('toolOutput').value;})()");assert.equal(immediate,'');
  await wait("document.getElementById('toolOutput').value==='APPLE\\n Apple \\napple'");assert.equal(await value('toolInput'),' Apple \napple\nAPPLE\n');
});
test('late clipboard success cannot announce stale copied text after an option change',async()=>{
  await input('A\na');await wait("document.getElementById('toolOutput').value==='A\\na'");
  await browser.evaluate("navigator.clipboard.writeText=text=>new Promise(resolve=>{window.__finishCopy=()=>{window.__edbClipboard.value=text;resolve();};});document.getElementById('copyBtn').click();document.getElementById('ignoreCase').click();window.__finishCopy();true");
  await wait("document.getElementById('toolOutput').value==='A'");assert.doesNotMatch(await browser.evaluate("document.getElementById('toolStatus').textContent"),/Text copied/);assert.equal(await browser.evaluate('window.__edbClipboard.value'),'A\na');
});
test('late clipboard rejection cannot focus/select an obsolete result after Clear',async()=>{
  await input('a\na');await wait("document.getElementById('toolOutput').value==='a'");
  await browser.evaluate("navigator.clipboard.writeText=()=>new Promise((resolve,reject)=>{window.__rejectCopy=reject;});document.getElementById('copyBtn').click();document.getElementById('clearBtn').click();window.__rejectCopy(Error('Simulated denial'));true");await pause(50);
  assert.equal(await browser.evaluate('document.activeElement.id'),'toolInput');assert.match(await browser.evaluate("document.getElementById('toolStatus').textContent"),/Cleared/);assert.equal(await output(),'');
});
test('download contains exact UTF-8 bytes, safe filename and revoked temporary URL',async()=>{
  await input('Café 😀\nCafé 😀\n中文');await wait("document.getElementById('toolOutput').value==='Café 😀\\n中文'");
  await browser.evaluate("const revoke=URL.revokeObjectURL.bind(URL);URL.revokeObjectURL=url=>{window.__revoked=url;revoke(url);};document.getElementById('downloadBtn').click();true");
  assert.deepEqual(await browser.evaluate('window.__edbDownloads'),['duplicate-lines-cleaned.txt']);assert.equal(await browser.evaluate('window.__edbDownloadBlob.text()'),'Café 😀\n中文');assert.equal(await browser.evaluate('window.__edbDownloadBlob.size'),Buffer.byteLength('Café 😀\n中文'));assert.equal(await browser.evaluate('window.__edbDownloadBlob.type'),'text/plain;charset=utf-8');await wait("typeof window.__revoked==='string'");assert.match(await browser.evaluate('window.__revoked'),/^blob:/);
});
test('download failure after URL creation still revokes URL and reports failure',async()=>{
  await input('x');await wait("document.getElementById('toolOutput').value==='x'");
  await browser.evaluate("const revoke=URL.revokeObjectURL.bind(URL);URL.revokeObjectURL=url=>{window.__revoked=url;revoke(url);};HTMLAnchorElement.prototype.click=()=>{throw Error('Simulated download denial');};document.getElementById('downloadBtn').click();true");
  assert.match(await browser.evaluate("document.getElementById('toolStatus').textContent"),/Download unavailable/);await wait("typeof window.__revoked==='string'");assert.equal(await output(),'x');
});
test('full-limit repeated-line DOM results and counts are exact, and Clear responds',async()=>{
  const text='x\n'.repeat(50000);await input(text);await wait("document.getElementById('toolOutput').value==='x\\n'");assert.equal(await value('toolInput'),text);
  assert.deepEqual(await browser.evaluate("['originalCount','retainedCount','duplicateCount','blankCount','removedCount'].map(id=>document.getElementById(id).textContent)"),['50,001','2','49,999','0','49,999']);
  await browser.evaluate("document.getElementById('clearBtn').click();true");assert.equal(await value('toolInput'),'');assert.equal(await output(),'');assert.equal(await browser.evaluate('document.activeElement.id'),'toolInput');
});
test('oversized text and whitespace retain input, invalidate results and recover',async()=>{
 for(const character of ['a',' ']) {
  await input('old');await wait("document.getElementById('toolOutput').value==='old'");const text=character.repeat(100001);await input(text);
  assert.equal(await value('toolInput'),text);assert.equal(await output(),'');assert.match(await browser.evaluate("document.getElementById('toolError').textContent"),/100,000 UTF-16/);assert.equal(await browser.evaluate("document.getElementById('originalCount').textContent"),'—');assert.equal(await browser.evaluate("document.getElementById('copyBtn').disabled&&document.getElementById('downloadBtn').disabled"),true);
  await input('new\nnew');await wait("document.getElementById('toolOutput').value==='new'");assert.equal(await browser.evaluate("document.getElementById('toolError').hidden"),true);
 }
});
test('composition and options cannot expose unfinished results; Clear also restores Run',async()=>{
  await input('old');await wait("document.getElementById('toolOutput').value==='old'");
  await browser.evaluate("const e=document.getElementById('toolInput');e.dispatchEvent(new CompositionEvent('compositionstart'));e.value='中文\\n中文';e.dispatchEvent(new InputEvent('input',{isComposing:true}));document.getElementById('sort').click();true");await pause(160);
  assert.equal(await output(),'');assert.equal(await browser.evaluate("document.getElementById('runBtn').disabled"),true);
  await browser.evaluate("document.getElementById('toolInput').dispatchEvent(new CompositionEvent('compositionend'));true");await wait("document.getElementById('toolOutput').value==='中文'");
  await browser.evaluate("document.getElementById('toolInput').dispatchEvent(new CompositionEvent('compositionstart'));document.getElementById('clearBtn').click();true");assert.equal(await browser.evaluate("document.getElementById('runBtn').disabled"),false);assert.equal(await output(),'');
});
test('processing makes no transport or persistence calls and renders markup only as text',async()=>{
  await browser.evaluate("window.__transports=[];window.fetch=()=>{__transports.push('fetch');throw Error('Unexpected fetch');};XMLHttpRequest.prototype.open=()=>__transports.push('xhr');navigator.sendBeacon=()=>{__transports.push('beacon');return false;};window.WebSocket=function(){__transports.push('websocket');};window.EventSource=function(){__transports.push('eventsource');};Storage.prototype.setItem=()=>__transports.push('storage');indexedDB.open=()=>{__transports.push('indexeddb');throw Error('Unexpected database');};true");
  await input('<img src=x onerror=alert(1)>\n<img src=x onerror=alert(1)>');await browser.evaluate("document.getElementById('ignoreCase').click();true");await wait("document.getElementById('toolOutput').value==='<img src=x onerror=alert(1)>'");assert.deepEqual(await browser.evaluate('window.__transports'),[]);assert.equal(await browser.evaluate("document.querySelectorAll('main img,main script').length"),0);
});
test('missing clipboard API selects current result and gives truthful guidance',async()=>{
  await input('current');await wait("document.getElementById('toolOutput').value==='current'");
  await browser.evaluate("Object.defineProperty(navigator,'clipboard',{configurable:true,value:undefined});document.getElementById('copyBtn').click();true");
  assert.match(await browser.evaluate("document.getElementById('toolStatus').textContent"),/Clipboard unavailable/);assert.equal(await browser.evaluate('document.activeElement.id'),'toolOutput');assert.equal(await browser.evaluate("document.getElementById('toolOutput').selectionEnd"),7);
});
test('native labels, readonly output, status and keyboard checkbox controls are present',async()=>{
  for(const id of ['toolInput','toolOutput','ignoreCase','trimComparison','removeBlankLines','sort'])assert.equal(await browser.evaluate(`document.getElementById(${JSON.stringify(id)}).labels.length>0`),true);
  assert.equal(await browser.evaluate("document.getElementById('toolOutput').readOnly"),true);assert.equal(await browser.evaluate("document.getElementById('toolStatus').getAttribute('role')"),'status');
  await browser.evaluate("document.getElementById('ignoreCase').focus();true");await browser.call('Input.dispatchKeyEvent',{type:'keyDown',key:' ',code:'Space',windowsVirtualKeyCode:32,text:' '});await browser.call('Input.dispatchKeyEvent',{type:'keyUp',key:' ',code:'Space',windowsVirtualKeyCode:32});assert.equal(await browser.evaluate("document.getElementById('ignoreCase').checked"),true);
});
