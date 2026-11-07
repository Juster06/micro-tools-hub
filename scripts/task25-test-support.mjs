import assert from 'node:assert/strict';
import fs from 'node:fs';
import {createHash} from 'node:crypto';
import {historicalSource} from './seo-overlay.mjs';

const root = new URL('../', import.meta.url);
const ids = ['word-frequency-analyzer','unicode-inspector','ipv4-subnet-calculator','batch-filename-planner','file-byte-comparator','css-gradient-generator'];
const approved = 'c127f856cbd97497412ec35ed66b3b1a58c4b2dc';

export function task25ReleasedCount(registry) {
  const added = registry.tools.filter(tool => ids.includes(tool.id));
  assert.deepEqual(added.map(tool => tool.id).sort(), [...ids].sort());
  for (const tool of added) {
    assert.equal(tool.status, 'RELEASED');
    assert.equal(tool.directory_path, tool.id);
    const v = tool.verification;
    assert.equal(v.source_revision, approved);
    assert.equal(v.publication.url, 'https://everydaydigitalbox.com/' + tool.id + '/');
    assert.equal(v.publication.http_status, 200);
    assert.equal(v.publication.source_matches, true);
    const evidencePath = 'audit/' + tool.id.toUpperCase().replaceAll('-', '_') + '_RELEASE_VERIFICATION.json';
    assert.equal(v.evidence_path, evidencePath);
    const audit = JSON.parse(fs.readFileSync(new URL(evidencePath, root), 'utf8'));
    assert.equal(audit.result, 'PASS');
    assert.equal(audit.source_revision, approved);
    assert.deepEqual(audit.publication, v.publication);
    assert.equal(audit.public_index.raw_match, true);
    assert.equal(audit.canonical_public_url.raw_match, true);
    assert.equal(audit.public_source_sha256, audit.approved_source_sha256);
    assert.ok(audit.public_browser_checks.length >= 6);
    assert.ok(audit.public_browser_checks.every(row => row.result === 'PASS'));
    const source = historicalSource(root, tool.id + '/index.html', fs.readFileSync(new URL(tool.id + '/index.html', root), 'utf8')).replaceAll('\r\n','\n').trimEnd();
    assert.equal(createHash('sha256').update(source).digest('hex'), v.source_sha256);
    assert.equal(audit.pages[0].source_sha256, v.source_sha256);
  }
  return added.length;
}
