import {test,before,beforeEach,after} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {fileURLToPath} from 'node:url';
import {launchBrowser,findBrowser} from '../../../scripts/tool-tests/browser.mjs';

const source=fileURLToPath(new URL('../../../url-encoder-decoder/index.html',import.meta.url));
const registry=JSON.parse(fs.readFileSync(new URL('../../../TOOL_REGISTRY.json',import.meta.url),'utf8'));
const routes=registry.tools.filter(t=>['IMPLEMENTED','TESTED','RELEASED'].includes(t.status)).map(t=>t.directory_path+'/index.html').sort();
const caseStatus=registry.tools.find(t=>t.id==='url-encoder-decoder').status;
assert.ok(['TESTED','RELEASED'].includes(caseStatus),'Tool must have source-bound scoped verification');
const publication=registry.tools.find(t=>t.id==='url-encoder-decoder').verification.publication;
if(caseStatus==='TESTED') assert.equal(publication,null);
else {
  assert.equal(publication.http_status,200);
  assert.equal(publication.source_matches,true);
  assert.equal(publication.url,'https://everydaydigitalbox.com/url-encoder-decoder/');
  assert.ok(Number.isFinite(Date.parse(publication.checked_at)));
}
assert.equal(registry.tools.filter(t=>t.status==='RELEASED').length,9);
assert.equal(caseStatus,'TESTED');
const availability=caseStatus.toLowerCase();
let browser;
before(async()=>{const executable=findBrowser();assert.ok(executable,'Installed Chromium required');browser=await launchBrowser(executable);});
beforeEach(async()=>{await browser.load(source);});
after(async()=>{if(browser)await browser.close();});
async function wait(expression) {
  const until=Date.now()+4000;
  while(Date.now()<until) {
    try {if(await browser.evaluate(`Boolean(${expression})`))return;} catch { /* Navigation replaces the execution context. */ }
    await new Promise(resolve=>setTimeout(resolve,25));
  }
  assert.fail('Local navigation did not reach the expected document');
}
async function hub() {
  assert.equal(await browser.evaluate("document.querySelector('header a').getAttribute('href')"),'../index.html');
  await browser.evaluate("document.querySelector('header a').click();true");
  await wait("document.getElementById('toolGrid') && document.readyState==='complete'");
}
test('Back to Hub reaches real hub, preserves all canonical routes and returns to the utility',async()=>{
  await hub();
  assert.deepEqual(await browser.evaluate("Array.from(document.querySelectorAll('#toolGrid a[data-title]'),a=>a.getAttribute('href')).sort()"),routes);
  assert.equal(await browser.evaluate("document.getElementById('resultCount').textContent"),routes.length+' tools ready to use');
  assert.equal(await browser.evaluate("document.querySelector('[data-tool-id=\"url-encoder-decoder\"]').getAttribute('data-availability')"),availability);
  assert.match(await browser.evaluate("document.querySelector('[data-tool-id=\"url-encoder-decoder\"]').textContent"),caseStatus==='RELEASED'?/\bLive\b/:/publication pending/);
  await browser.evaluate("document.querySelector('[data-tool-id=\"url-encoder-decoder\"]').click();true");
  await wait("document.getElementById('toolInput') && document.readyState==='complete'");
  assert.match(await browser.evaluate('document.title'),/URL Encoder and Decoder/);
});
test('hub search finds URL Encoder and Decoder and clear restores the correct local card count',async()=>{
  await hub();
  await browser.evaluate("const input=document.getElementById('toolSearch');input.value='URL Encoder and Decoder';input.dispatchEvent(new Event('input'));true");
  assert.deepEqual(await browser.evaluate("Array.from(document.querySelectorAll('#toolGrid a[data-title]')).filter(a=>!a.hidden).map(a=>a.getAttribute('href'))"),['url-encoder-decoder/index.html']);
  assert.match(await browser.evaluate("document.getElementById('resultCount').textContent"),new RegExp('1 of '+routes.length));
  await browser.evaluate("document.getElementById('clearSearch').click();true");
  assert.equal(await browser.evaluate("document.getElementById('resultCount').textContent"),routes.length+' tools ready to use');
});
