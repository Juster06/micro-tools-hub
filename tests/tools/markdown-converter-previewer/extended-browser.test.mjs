import {test,before,beforeEach,after} from 'node:test';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import {launchBrowser,findBrowser} from '../../../scripts/tool-tests/browser.mjs';
let b;const wait=async expression=>{for(let i=0;i<160;i++){if(await b.evaluate(expression))return;await new Promise(r=>setTimeout(r,20));}assert.fail('Expected UI state did not arrive');};
before(async()=>{b=await launchBrowser(findBrowser());});beforeEach(async()=>b.load(fileURLToPath(new URL('../../../markdown-converter-previewer/index.html',import.meta.url))));after(async()=>b?.close());
async function run(input){await b.evaluate(`toolInput.value=${JSON.stringify(input)};toolInput.dispatchEvent(new Event('input'));runBtn.click();true`);await wait("toolStatus.textContent==='Complete.'");}
test('copy and real captured HTML Blob contain sanitized output, proper MIME and no active markup',async()=>{
 await run('# Hello\n\n[ok](https://example.invalid/)\n\n![no](https://example.invalid/image)\n\n<script>parent.__ran=1</script>');
 const text=await b.evaluate('toolOutput.value');assert.match(text,/&lt;script&gt;/);assert.doesNotMatch(text,/<(?:script|img)\b/);
 await b.evaluate('copyBtn.click();downloadBtn.click();true');await wait('window.__edbClipboard.value!==null');
 assert.equal(await b.evaluate('window.__edbClipboard.value'),text);
 assert.equal(await b.evaluate('window.__edbDownloadBlob.type'),'text/html;charset=utf-8');
 const downloaded=await b.evaluate('window.__edbDownloadBlob.text()');assert.match(downloaded,/^<!doctype html>/);assert.match(downloaded,/default-src 'none'/);assert.ok(downloaded.includes(text));assert.doesNotMatch(downloaded,/<(?:script|img)\b/);assert.deepEqual(await b.evaluate('__edbDownloads'),['converted-markdown.html']);
});
test('edit, cancellation and reset invalidate results and revoke Worker URLs',async()=>{
 await b.evaluate("window.__revoked=0;const old=URL.revokeObjectURL.bind(URL);URL.revokeObjectURL=url=>{__revoked++;old(url)};toolInput.value='x'.repeat(32768);runBtn.click();cancelBtn.click();true");await new Promise(r=>setTimeout(r,120));assert.equal(await b.evaluate('toolOutput.value'),'');assert.ok(await b.evaluate('__revoked>=1'));
 await run('**Ready**');await b.evaluate("toolInput.value='Changed';toolInput.dispatchEvent(new Event('input'));true");assert.equal(await b.evaluate('copyBtn.disabled'),true);assert.equal(await b.evaluate('toolOutput.value'),'');await b.evaluate('clearBtn.click();true');assert.equal(await b.evaluate('document.activeElement.id'),'toolInput');assert.equal(await b.evaluate('safePreview.srcdoc'),'');
});
test('missing Worker, invalid UTF-8 and unsupported settings fail closed',async()=>{
 await b.evaluate("toolInput.value='😀'.repeat(8193);runBtn.click();true");assert.match(await b.evaluate('toolError.textContent'),/32 KiB/);assert.equal(await b.evaluate('downloadBtn.disabled'),true);
 await b.evaluate("window.Worker=undefined;toolInput.value='Hello';runBtn.click();true");assert.match(await b.evaluate('toolError.textContent'),/Worker/);assert.equal(await b.evaluate('copyBtn.disabled'),true);
});
test('clipboard failure selects output and gives truthful fallback',async()=>{await run('Hello');await b.evaluate("window.__edbClipboard.mode='failure';copyBtn.click();true");await wait("toolStatus.textContent.includes('Clipboard unavailable')");assert.equal(await b.evaluate('document.activeElement.id'),'toolOutput');});
test('keyboard controls and 320/375/768/1440 layouts remain usable',async()=>{
 for(const width of [320,375,768,1440]){await b.call('Emulation.setDeviceMetricsOverride',{width,height:900,deviceScaleFactor:1,mobile:false});assert.equal(await b.evaluate('document.documentElement.scrollWidth>innerWidth'),false);}
 await b.evaluate("toolInput.value='# Keyboard';runBtn.focus();true");await b.call('Input.dispatchKeyEvent',{type:'keyDown',key:'Enter',code:'Enter',windowsVirtualKeyCode:13,text:'\r'});await b.call('Input.dispatchKeyEvent',{type:'keyUp',key:'Enter',code:'Enter',windowsVirtualKeyCode:13});await wait("toolStatus.textContent==='Complete.'");assert.equal(await b.evaluate('toolOutput.value'),'<h1>Keyboard</h1>\n');
});
