import {test,before,after}from 'node:test';import assert from 'node:assert/strict';import{fileURLToPath}from'node:url';import{launchBrowser,findBrowser}from'../../../scripts/tool-tests/browser.mjs';
let b;const wait=async e=>{for(let i=0;i<120;i++){try{if(await b.evaluate(e))return;}catch{}await new Promise(r=>setTimeout(r,25));}assert.fail('Navigation state unavailable');};
before(async()=>{b=await launchBrowser(findBrowser());});after(async()=>b?.close());
test('75 distinct cards preserve the verified release label and canonical round trip',async()=>{
 await b.load(fileURLToPath(new URL('../../../markdown-converter-previewer/index.html',import.meta.url)));assert.equal(await b.evaluate("document.querySelector('header a').getAttribute('href')"),'../index.html');await b.evaluate("document.querySelector('header a').click();true");await wait("!!document.querySelector('#toolGrid')");
 const cards=await b.evaluate("Array.from(document.querySelectorAll('.tool-card')).map(a=>({route:a.getAttribute('href'),status:a.dataset.availability,text:a.textContent}))");assert.equal(cards.length,75);assert.equal(new Set(cards.map(c=>c.route)).size,75);const own=cards.find(c=>c.route==='markdown-converter-previewer/index.html');assert.equal(own.status,'released');assert.match(own.text,/Live/);
 await b.evaluate("document.querySelector('[data-tool-id=markdown-converter-previewer]').click();true");await wait("document.querySelector('h1')?.textContent==='Markdown Converter & Previewer'");
});
test('search finds the new tool and clearing restores the catalog',async()=>{
 await b.load(fileURLToPath(new URL('../../../index.html',import.meta.url)));await b.evaluate("toolSearch.value='Markdown Converter';toolSearch.dispatchEvent(new Event('input'));true");assert.equal(await b.evaluate("Array.from(document.querySelectorAll('.tool-card')).filter(a=>!a.hidden).length"),1);await b.evaluate('clearSearch.click();true');assert.equal(await b.evaluate("Array.from(document.querySelectorAll('.tool-card')).filter(a=>!a.hidden).length"),75);
});
