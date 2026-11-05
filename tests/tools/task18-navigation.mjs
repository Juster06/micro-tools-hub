import {test,before,beforeEach,after} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {start,source,wait,set,click} from './task18-browser.mjs';
export function navigationTests(id,name) {
  const registry=JSON.parse(fs.readFileSync(new URL('../../TOOL_REGISTRY.json',import.meta.url),'utf8'));
  const tool=registry.tools.find(t=>t.id===id);
  const routes=registry.tools.filter(t=>['IMPLEMENTED','TESTED','RELEASED'].includes(t.status)).map(t=>t.directory_path+'/index.html').sort();
  let b;before(async()=>{b=await start()});beforeEach(async()=>b.load(source(id)));after(async()=>b?.close());
  test('tested source has no publication claim; hub preserves canonical routes and returns',async()=>{
    assert.equal(tool.status,'TESTED');assert.equal(tool.verification.publication,null);
    assert.equal(await b.evaluate('document.querySelector("header a").getAttribute("href")'),'../index.html');
    await b.evaluate('document.querySelector("header a").click();true');await wait(b,'!!document.getElementById("toolGrid")');
    assert.deepEqual(await b.evaluate('Array.from(document.querySelectorAll("#toolGrid a[data-title]"),a=>a.getAttribute("href")).sort()'),routes);
    assert.equal(await b.evaluate('resultCount.textContent'),routes.length+' tools ready to use');
    assert.equal(await b.evaluate(`document.querySelector('[data-tool-id="${id}"]').getAttribute('data-availability')`),'tested');
    assert.match(await b.evaluate(`document.querySelector('[data-tool-id="${id}"]').textContent`),/publication pending/);
    await b.evaluate(`document.querySelector('[data-tool-id="${id}"]').click();true`);await wait(b,'!!document.getElementById("toolInput")');
    assert.match(await b.evaluate('document.title'),new RegExp(name));
  });
  test('homepage search finds the selected tool and reset restores full count',async()=>{
    await b.evaluate('document.querySelector("header a").click();true');await wait(b,'!!document.getElementById("toolGrid")');
    await set(b,'toolSearch',name);
    assert.deepEqual(await b.evaluate('Array.from(document.querySelectorAll("#toolGrid a[data-title]")).filter(a=>!a.hidden).map(a=>a.getAttribute("href"))'),[id+'/index.html']);
    await click(b,'clearSearch');assert.equal(await b.evaluate('resultCount.textContent'),routes.length+' tools ready to use');
  });
}
