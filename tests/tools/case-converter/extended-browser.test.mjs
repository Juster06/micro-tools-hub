import {test,before,beforeEach,after} from 'node:test';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import {launchBrowser,findBrowser} from '../../../scripts/tool-tests/browser.mjs';

// Additional real Chromium cases reuse the Task 4 client; no new framework.
// Clipboard/download are isolated simulations, never the host clipboard/files.
const source = fileURLToPath(new URL('../../../case-converter/index.html',import.meta.url));
let browser;
before(async () => { const executable=findBrowser(); assert.ok(executable,'Installed Chromium is required'); browser=await launchBrowser(executable); });
beforeEach(async () => { await browser.load(source); });
after(async () => { if(browser)await browser.close(); });
async function input(value) {
  await browser.evaluate(`(value=>{const input=document.getElementById('toolInput');input.value=value;input.dispatchEvent(new Event('input',{bubbles:true}));})(${JSON.stringify(value)})`);
}
async function mode(value) {
  await browser.evaluate(`(value=>{const mode=document.getElementById('toolMode');mode.value=value;mode.dispatchEvent(new Event('change'));})(${JSON.stringify(value)})`);
}
async function wait(expression) {
  const until=Date.now()+4000;
  while(Date.now()<until) {
    if(await browser.evaluate(`Boolean(${expression})`))return;
    await new Promise(resolve=>setTimeout(resolve,25));
  }
  assert.fail('Browser condition did not become true');
}
const output = () => browser.evaluate("document.getElementById('toolOutput').value");

test('100,000-unit live title conversion keeps exact input/result and statistics',async () => {
  const value='word '.repeat(20000);
  await input(value); await mode('title');
  await wait("document.getElementById('toolOutput').value.length===100000");
  assert.equal(await output(),'Word '.repeat(20000));
  assert.equal(await browser.evaluate("document.getElementById('toolInput').value"),value);
  assert.equal(await browser.evaluate("document.getElementById('wordCount').textContent"),'20,000');
  assert.equal(await browser.evaluate("document.getElementById('characterCount').textContent"),'100,000');
});
test('oversized input is retained, error shown, actions disabled, Clear recovers',async () => {
  const value='a'.repeat(100001); await input(value);
  await wait("!document.getElementById('toolError').hidden");
  assert.equal(await output(),'');
  assert.equal(await browser.evaluate("document.getElementById('toolInput').value"),value);
  assert.match(await browser.evaluate("document.getElementById('toolError').textContent"),/100,000 UTF-16/);
  assert.equal(await browser.evaluate("document.getElementById('copyBtn').disabled && document.getElementById('downloadBtn').disabled"),true);
  await browser.evaluate("document.getElementById('clearBtn').click()");
  assert.equal(await browser.evaluate("document.getElementById('toolError').hidden"),true);
  assert.equal(await browser.evaluate("document.getElementById('characterCount').textContent"),'0');
});
test('surrogate-pair limit is distinct from the displayed code-point counter',async () => {
  const value='😀'.repeat(50000); await input(value);
  await wait("document.getElementById('toolOutput').value.length===100000");
  assert.equal(await output(),value);
  assert.equal(await browser.evaluate("document.getElementById('characterCount').textContent"),'50,000');
  await input(value+'😀'); await wait("!document.getElementById('toolError').hidden");
  assert.equal(await output(),'');
  assert.equal(await browser.evaluate("document.getElementById('characterCount').textContent"),'50,001');
});
test('input change clears old output synchronously before the debounced result',async () => {
  await input('first');await wait("document.getElementById('toolOutput').value==='FIRST'");
  const immediate=await browser.evaluate("(()=>{const input=document.getElementById('toolInput');input.value='second';input.dispatchEvent(new Event('input'));return {value:document.getElementById('toolOutput').value,disabled:document.getElementById('copyBtn').disabled};})()");
  assert.deepEqual(immediate,{value:'',disabled:true});
  await wait("document.getElementById('toolOutput').value==='SECOND'");
});
test('delayed clipboard completion cannot announce stale success after an edit',async () => {
  await input('old');await wait("document.getElementById('toolOutput').value==='OLD'");
  await browser.evaluate("navigator.clipboard.writeText=value=>new Promise(resolve=>{window.__finishCopy=()=>{window.__edbClipboard.value=value;resolve();};});document.getElementById('copyBtn').click();true");
  await input('new');await browser.evaluate('window.__finishCopy();true');
  await wait("document.getElementById('toolOutput').value==='NEW'");
  assert.doesNotMatch(await browser.evaluate("document.getElementById('toolStatus').textContent"),/Text copied/);
  assert.equal(await browser.evaluate('window.__edbClipboard.value'),'OLD');
  assert.equal(await output(),'NEW');
});
test('download has safe filename, correct UTF-8 bytes and revoked object URL',async () => {
  await input('Café 😀\n');await mode('lowercase');
  await browser.evaluate("const originalRevoke=URL.revokeObjectURL.bind(URL);URL.revokeObjectURL=url=>{window.__revoked=url;originalRevoke(url);};document.getElementById('downloadBtn').click();true");
  assert.deepEqual(await browser.evaluate('window.__edbDownloads'),['case-converter-output.txt']);
  assert.equal(await browser.evaluate('window.__edbDownloadBlob.text()'),'café 😀\n');
  assert.equal(await browser.evaluate('window.__edbDownloadBlob.type'),'text/plain;charset=utf-8');
  assert.equal(await browser.evaluate('window.__edbDownloadBlob.size'),Buffer.byteLength('café 😀\n','utf8'));
  await wait('typeof window.__revoked===\'string\'');
  assert.match(await browser.evaluate('window.__revoked'),/^blob:/);
});
test('native keyboard Tab reaches the conversion button and Enter executes it',async () => {
  await input('keyboard');await browser.evaluate("document.getElementById('toolMode').focus()");
  await browser.call('Input.dispatchKeyEvent',{type:'rawKeyDown',key:'Tab',code:'Tab',windowsVirtualKeyCode:9});
  await browser.call('Input.dispatchKeyEvent',{type:'keyUp',key:'Tab',code:'Tab',windowsVirtualKeyCode:9});
  assert.equal(await browser.evaluate('document.activeElement.id'),'runBtn');
  await browser.call('Input.dispatchKeyEvent',{type:'keyDown',key:'Enter',code:'Enter',windowsVirtualKeyCode:13,text:'\r'});
  await browser.call('Input.dispatchKeyEvent',{type:'keyUp',key:'Enter',code:'Enter',windowsVirtualKeyCode:13});
  await wait("document.getElementById('toolOutput').value==='KEYBOARD'");
});
test('IME composition keeps output invalid until composition completes',async () => {
  const state=await browser.evaluate("(()=>{const input=document.getElementById('toolInput');input.dispatchEvent(new CompositionEvent('compositionstart'));input.value='中文a';input.dispatchEvent(new InputEvent('input',{isComposing:true}));return {value:document.getElementById('toolOutput').value,disabled:document.getElementById('runBtn').disabled};})()");
  assert.deepEqual(state,{value:'',disabled:true});
  await browser.evaluate("document.getElementById('toolInput').dispatchEvent(new CompositionEvent('compositionend'));true");
  await wait("document.getElementById('toolOutput').value==='中文A'");
  assert.equal(await browser.evaluate("document.getElementById('runBtn').disabled"),false);
});
test('conversion makes no fetch, XHR, beacon or storage writes',async () => {
  await browser.evaluate("window.__transports=[];window.fetch=()=>{window.__transports.push('fetch');throw Error('Unexpected fetch');};XMLHttpRequest.prototype.open=()=>window.__transports.push('xhr');navigator.sendBeacon=()=>{window.__transports.push('beacon');return false;};Storage.prototype.setItem=()=>window.__transports.push('storage');true");
  await input('Private fixture 😀');await mode('inverse');
  await wait("document.getElementById('toolOutput').value==='pRIVATE FIXTURE 😀'");
  assert.deepEqual(await browser.evaluate('window.__transports'),[]);
  for(const id of ['toolInput','toolOutput','toolMode']) {
    assert.equal(await browser.evaluate(`document.getElementById(${JSON.stringify(id)}).labels.length>0`),true);
  }
});
