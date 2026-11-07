import {task24ReleasedCount} from '../../../scripts/task24-test-support.mjs';
import {test,before,after}from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';import{fileURLToPath}from'node:url';import{launchBrowser,findBrowser}from'../../../scripts/tool-tests/browser.mjs';
const registry=JSON.parse(fs.readFileSync(new URL('../../../TOOL_REGISTRY.json',import.meta.url),'utf8'));
const task24=['number-base-converter','unit-converter','duration-calculator','url-inspector-query-builder','list-comparison-set-operations','color-contrast-checker'];
const expectedRoutes=registry.tools.filter(t=>['TESTED','RELEASED'].includes(t.status)).map(t=>t.directory_path+'/index.html').sort();
assert.equal(registry.tools.filter(t=>t.status==='RELEASED').length,81);assert.equal(expectedRoutes.length,81);
assert.equal(task24ReleasedCount(registry),6);
let b;const wait=async e=>{for(let i=0;i<120;i++){try{if(await b.evaluate(e))return;}catch{}await new Promise(r=>setTimeout(r,25));}assert.fail('Navigation state unavailable');};
before(async()=>{b=await launchBrowser(findBrowser());});after(async()=>b?.close());
test('81 distinct cards preserve all 81 releases, six verified new labels and canonical round trip',async()=>{
 await b.load(fileURLToPath(new URL('../../../markdown-converter-previewer/index.html',import.meta.url)));assert.equal(await b.evaluate("document.querySelector('header a').getAttribute('href')"),'../index.html');await b.evaluate("document.querySelector('header a').click();true");await wait("!!document.querySelector('#toolGrid')");
 const cards=await b.evaluate("Array.from(document.querySelectorAll('.tool-card')).map(a=>({route:a.getAttribute('href'),status:a.dataset.availability,text:a.textContent}))");assert.equal(cards.length,81);assert.equal(new Set(cards.map(c=>c.route)).size,81);assert.deepEqual(cards.map(c=>c.route).sort(),expectedRoutes);const own=cards.find(c=>c.route==='markdown-converter-previewer/index.html');assert.equal(own.status,'released');assert.match(own.text,/Live/);
 for(const id of task24){const card=cards.find(c=>c.route===id+'/index.html');assert.equal(card.status,'released');assert.match(card.text,/Live/);}
 await b.evaluate("document.querySelector('[data-tool-id=markdown-converter-previewer]').click();true");await wait("document.querySelector('h1')?.textContent==='Markdown Converter & Previewer'");
});
test('search finds the new tool and clearing restores the catalog',async()=>{
 await b.load(fileURLToPath(new URL('../../../index.html',import.meta.url)));await b.evaluate("toolSearch.value='Markdown Converter';toolSearch.dispatchEvent(new Event('input'));true");assert.equal(await b.evaluate("Array.from(document.querySelectorAll('.tool-card')).filter(a=>!a.hidden).length"),1);await b.evaluate('clearSearch.click();true');assert.equal(await b.evaluate("Array.from(document.querySelectorAll('.tool-card')).filter(a=>!a.hidden).length"),81);
});
