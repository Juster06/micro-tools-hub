// Admit only the six independently verified Task24 releases to historical counts.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {createHash} from 'node:crypto';
const root=new URL('../',import.meta.url);
const ids=['number-base-converter','unit-converter','duration-calculator','url-inspector-query-builder','list-comparison-set-operations','color-contrast-checker'];
export function task24ReleasedCount(registry){
 const added=registry.tools.filter(t=>ids.includes(t.id));assert.equal(added.length,6);
 for(const tool of added){
  assert.equal(tool.status,'RELEASED');assert.equal(tool.directory_path,tool.id);
  const v=tool.verification;assert.equal(v.source_revision,'a7da719ea6ccc4caae572f26f6ae5e707fbb70be');assert.equal(v.publication.http_status,200);assert.equal(v.publication.source_matches,true);assert.equal(v.publication.url,'https://everydaydigitalbox.com/'+tool.id+'/');
  const audit=JSON.parse(fs.readFileSync(new URL(v.evidence_path,root),'utf8'));assert.equal(audit.result,'PASS');assert.deepEqual(audit.publication,v.publication);assert.equal(audit.public_index.raw_match,true);assert.equal(audit.public_source_sha256,audit.approved_source_sha256);assert.ok(audit.public_browser_checks.length>=6);assert.ok(audit.public_browser_checks.every(c=>c.result==='PASS'));
  const source=fs.readFileSync(new URL(tool.id+'/index.html',root),'utf8').replaceAll('\r\n','\n').trimEnd();assert.equal(createHash('sha256').update(source).digest('hex'),v.source_sha256);assert.equal(audit.pages[0].source_sha256,v.source_sha256);
 }return 6;
}
