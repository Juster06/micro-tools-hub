import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {pathToFileURL,fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {historicalSource} from './seo-overlay.mjs';

const root = new URL('../', import.meta.url);
// Test the frozen SEO adapter on its exact Git-bound baseline fixtures.
// The new CSS dependency gate and current candidates have their own test suite.
const fixtures = new Map();
const read = relative => {
  if(!fixtures.has(relative))fixtures.set(relative,execFileSync('git',['show','cf443c3b1facc2ae422fc6c55d546528671be1d0:'+relative],{cwd:fileURLToPath(root),encoding:'utf8',windowsHide:true}));
  return fixtures.get(relative);
};
const manifest = JSON.parse(read('audit/SEO_TASK_2A_SOURCE_OVERLAY.json'));
const hash = value => createHash('sha256').update(value.replaceAll('\r\n', '\n')).digest('hex');

test('Node historical projection reconstructs all 89 exact audited preimages', () => {
  assert.equal(Object.keys(manifest.pages).length, 89);
  for (const [relative, entry] of Object.entries(manifest.pages)) {
    const source = read(relative);
    assert.equal(hash(source), entry.candidate_sha256, relative);
    assert.equal(hash(historicalSource(root, relative, source)), entry.previous_sha256, relative);
  }
});

test('both compact and multiline heads project with LF and CRLF intact', () => {
  for (const relative of ['index.html', 'privacy.html']) {
    const lf = read(relative).replaceAll('\r\n', '\n');
    const original = historicalSource(root, relative, lf);
    assert.equal(historicalSource(root, relative, lf.replaceAll('\n', '\r\n')), original.replaceAll('\n', '\r\n'));
    assert.equal(historicalSource(root, relative, original), original);
  }
});

test('duplicate or displaced canonicals, body changes and trailing bytes are rejected', () => {
  const relative = 'index.html', source = read(relative).replaceAll('\r\n', '\n');
  const line = '  <link rel="canonical" href="' + manifest.pages[relative].canonical + '">\n';
  for (const candidate of [source.replace(line, line + line), source.replace(line, '').replace('</head>', line + '</head>'),
    source.replace('</body>', 'changed</body>'), source + ' ']) {
    assert.throws(() => historicalSource(root, relative, candidate), /Unapproved source change/);
  }
});

test('unlisted runtime assets remain byte-for-byte input for historical checks', () => {
  const changed = 'changed code\r\n  ';
  assert.equal(historicalSource(root, 'assets/consent.js', changed), changed);
});

test('manifest edits cannot approve another source hash', () => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'edb-seo-overlay-'));
  try {
    fs.mkdirSync(path.join(directory, 'audit'));
    const changed = structuredClone(manifest);
    changed.pages['index.html'].candidate_sha256 = '0'.repeat(64);
    fs.writeFileSync(path.join(directory, 'audit/SEO_TASK_2A_SOURCE_OVERLAY.json'), JSON.stringify(changed));
    assert.throws(() => historicalSource(pathToFileURL(directory + path.sep), 'index.html', read('index.html')), /manifest differs/);
  } finally { fs.rmSync(directory, {recursive:true, force:true}); }
});

test('generic fixtures without this frozen overlay are returned untouched', () => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'edb-seo-generic-'));
  try { assert.equal(historicalSource(pathToFileURL(directory + path.sep), 'index.html', 'fixture\r\n '), 'fixture\r\n '); }
  finally { fs.rmSync(directory, {recursive:true, force:true}); }
});
