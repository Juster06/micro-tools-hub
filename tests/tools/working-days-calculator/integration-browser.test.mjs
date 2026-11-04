import {test,before,beforeEach,after} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {fileURLToPath} from 'node:url';
import {launchBrowser,findBrowser} from '../../../scripts/tool-tests/browser.mjs';

const source=fileURLToPath(new URL('../../../working-days-calculator/index.html',import.meta.url));
const registry=JSON.parse(fs.readFileSync(new URL('../../../TOOL_REGISTRY.json',import.meta.url),'utf8'));
const routes=registry.tools.filter(t=>['IMPLEMENTED','TESTED','RELEASED'].includes(t.status)).map(t=>t.directory_path+'/index.html').sort();
const caseStatus=registry.tools.find(t=>t.id==='working-days-calculator').status;
assert.ok(['TESTED','RELEASED'].includes(caseStatus),'Tool must have source-bound scoped verification');
const publication=registry.tools.find(t=>t.id==='working-days-calculator').verification.publication;
if(caseStatus==='TESTED') assert.equal(publication,null);
else {
  assert.equal(publication.http_status,200);
  assert.equal(publication.source_matches,true);
  assert.equal(publication.url,'https://everydaydigitalbox.com/working-days-calculator/');
  assert.ok(Number.isFinite(Date.parse(publication.checked_at)));
}
const task9Ids=["uuid-generator","timestamp-converter","percentage-calculator","percentage-change-calculator","discount-calculator"];
const task9Released=registry.tools.filter(t=>task9Ids.includes(t.id)&&t.status==='RELEASED').length;
const task10Ids=["profit-margin-calculator","date-difference-calculator","countdown-timer","random-name-picker","hashtag-organizer","secure-random-number-generator"];
const task10Released=registry.tools.filter(t=>task10Ids.includes(t.id)&&t.status==='RELEASED').length;
const task11Released=registry.tools.filter(t=>t.id==='file-size-converter'&&t.status==='RELEASED').length;
const task12Ids=["age-calculator","vat-calculator","working-days-calculator","meeting-agenda-generator","image-rotator","sha256-hash-checker"];
const task12Released=registry.tools.filter(t=>task12Ids.includes(t.id)&&t.status==='RELEASED').length;
const task13Ids=["printable-calendar-generator","username-generator","youtube-description-formatter","json-to-txt","image-resizer","text-difference-checker"];
const task13Released=registry.tools.filter(t=>task13Ids.includes(t.id)&&t.status==='RELEASED').length;
const task14Ids=["image-color-picker","csv-viewer","image-watermark","local-to-do-list","posting-calendar-generator","compound-interest-calculator"];
const task14Released=registry.tools.filter(t=>task14Ids.includes(t.id)&&t.status==='RELEASED').length;
const task15Ids=["youtube-thumbnail-preview","pomodoro-timer","csv-column-extractor","duplicate-row-finder","loan-repayment-calculator","invoice-generator"];
const task15Released=registry.tools.filter(t=>task15Ids.includes(t.id)&&t.status==='RELEASED').length;
assert.equal(registry.tools.filter(t=>t.status==='RELEASED').length,13+task9Released+task10Released+task11Released+task12Released+task13Released+task14Released+task15Released);
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
  assert.equal(await browser.evaluate("document.querySelector('[data-tool-id=\"working-days-calculator\"]').getAttribute('data-availability')"),availability);
  assert.match(await browser.evaluate("document.querySelector('[data-tool-id=\"working-days-calculator\"]').textContent"),caseStatus==='RELEASED'?/\bLive\b/:/publication pending/);
  await browser.evaluate("document.querySelector('[data-tool-id=\"working-days-calculator\"]').click();true");
  await wait("document.getElementById('toolInput') && document.readyState==='complete'");
  assert.match(await browser.evaluate('document.title'),/Working Days Calculator/);
});
test('hub search finds Working Days Calculator and clear restores the correct local card count',async()=>{
  await hub();
  await browser.evaluate("const input=document.getElementById('toolSearch');input.value='Working Days Calculator';input.dispatchEvent(new Event('input'));true");
  assert.deepEqual(await browser.evaluate("Array.from(document.querySelectorAll('#toolGrid a[data-title]')).filter(a=>!a.hidden).map(a=>a.getAttribute('href'))"),['working-days-calculator/index.html']);
  assert.match(await browser.evaluate("document.getElementById('resultCount').textContent"),new RegExp('1 of '+routes.length));
  await browser.evaluate("document.getElementById('clearSearch').click();true");
  assert.equal(await browser.evaluate("document.getElementById('resultCount').textContent"),routes.length+' tools ready to use');
});
