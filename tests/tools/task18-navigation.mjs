import {test,before,beforeEach,after} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {start,source,wait,set,click} from './task18-browser.mjs';
export function navigationTests(id,name) {
  const registry=JSON.parse(fs.readFileSync(new URL('../../TOOL_REGISTRY.json',import.meta.url),'utf8'));
  const tool=registry.tools.find(t=>t.id===id);
  const routes=registry.tools.filter(t=>['IMPLEMENTED','TESTED','RELEASED'].includes(t.status)).map(t=>t.directory_path+'/index.html').sort();
  let b;before(async()=>{b=await start()});beforeEach(async()=>b.load(source(id)));after(async()=>b?.close());
  test('source has matching lifecycle/publication evidence; hub preserves canonical routes and returns',async()=>{
    assert.ok(['TESTED','RELEASED'].includes(tool.status));
    if(tool.status==='TESTED')assert.equal(tool.verification.publication,null);
    else{
      const publication=tool.verification.publication;
      assert.equal(publication.url,'https://everydaydigitalbox.com/'+id+'/');
      assert.equal(publication.http_status,200);assert.equal(publication.source_matches,true);
      assert.ok(Number.isFinite(Date.parse(publication.checked_at)));
      const audit=JSON.parse(fs.readFileSync(new URL('../../'+tool.verification.evidence_path,import.meta.url),'utf8'));
      assert.equal(audit.result,'PASS');assert.deepEqual(audit.pages[0].publication,publication);
      assert.equal(audit.public_index.raw_public_sha256,audit.public_index.raw_approved_sha256);
      assert.equal(audit.source_revision,tool.verification.source_revision);
    }
    assert.equal(await b.evaluate('document.querySelector("header a").getAttribute("href")'),'../index.html');
    await b.evaluate('document.querySelector("header a").click();true');await wait(b,'!!document.getElementById("toolGrid")');
    assert.deepEqual(await b.evaluate('Array.from(document.querySelectorAll("#toolGrid a[data-title]"),a=>a.getAttribute("href")).sort()'),routes);
    assert.equal(await b.evaluate('resultCount.textContent'),routes.length+' tools ready to use');
    assert.equal(await b.evaluate(`document.querySelector('[data-tool-id="${id}"]').getAttribute('data-availability')`),tool.status.toLowerCase());
    assert.match(await b.evaluate(`document.querySelector('[data-tool-id="${id}"]').textContent`),tool.status==='RELEASED'?/\bLive\b/:/publication pending/);
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
