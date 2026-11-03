import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { validateRegistry, validateProject, summarize } from './project.mjs';
const original=JSON.parse(fs.readFileSync(new URL('../TOOL_REGISTRY.json',import.meta.url),'utf8'));
const copy=()=>structuredClone(original);
// Registry growth can exhaust READY work. Create that state in the fixture,
// rather than requiring an unfinished READY tool in the production inventory.
const readyFixture=()=>{const r=copy(),tool=r.tools.find(t=>t.status==='PLANNED');assert.ok(tool,'Fixture needs an unimplemented backlog entry');tool.status='READY';return {r,tool};};
test('current registry and repository are consistent',()=>assert.deepEqual(validateProject(original),[]));
test('duplicate identities and directories are rejected',()=>{const r=copy();r.tools.push(structuredClone(r.tools[0]));const errors=validateRegistry(r);assert(errors.some(e=>e.includes('duplicate id')));assert(errors.some(e=>e.includes('duplicate directory')));});
test('unknown statuses and broken related-tool references are rejected',()=>{const r=copy();r.tools[0].status='DONE';r.tools[0].related_tools=['missing-tool'];const errors=validateRegistry(r);assert(errors.some(e=>e.includes('unknown status')));assert(errors.some(e=>e.includes('invalid related tool')));});
test('unverified publication cannot be marked RELEASED',()=>{const r=copy();r.tools[0].verification.publication.source_matches=false;assert(validateRegistry(r).some(e=>e.includes('verified publication')));});
test('planned tools cannot claim passing tests',()=>{const {r,tool}=readyFixture();tool.testing_status='SMOKE_PASSED';assert(validateRegistry(r).some(e=>e.includes('planned tool cannot claim tests')));});
test('incorrect source evidence is rejected',()=>{const r=copy();r.tools[0].verification.source_sha256='0'.repeat(64);assert(validateProject(r).some(e=>e.toLowerCase().includes('source changed since verification')));});
test('invalid paths and duplicate proposal aliases are rejected',()=>{const r=copy();r.tools[0].directory_path='../outside';r.proposal_resolutions.push({...r.proposal_resolutions[0]});const errors=validateRegistry(r);assert(errors.some(e=>e.includes('safe relative slug')));assert(errors.some(e=>e.includes('Duplicate proposal')));});
test('counts are derived, including blocked as a backlog subset',()=>{const {r,tool}=readyFixture(),before=summarize(r);tool.status='IN_PROGRESS';const after=summarize(r);assert.equal(after.total,before.total);assert.equal(after.planned,before.planned-1);assert.equal(after.in_progress,before.in_progress+1);assert.equal(after.ready,before.ready-1);});
test('generated document drift is rejected',()=>{const r=copy();r.tools.find(t=>t.status==='PLANNED').priority='P3';assert(validateProject(r).some(e=>e.includes('ROADMAP.md: generated data is stale')));});
test('missing root schema and original-proposal mappings are rejected',()=>{assert.deepEqual(validateRegistry({}),['Missing registry root fields']);const r=copy();r.proposal_resolutions.shift();assert(validateProject(r).some(e=>e.includes('Initial backlog proposals are missing mappings')));});
