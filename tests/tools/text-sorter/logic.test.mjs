import {test} from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';
import {loadLogic} from '../../../scripts/tool-tests/runner.mjs';
const adapter=loadLogic(fileURLToPath(new URL('../../../text-sorter/index.html',import.meta.url)));
const defaults={};
function invoke(input,options=defaults){adapter.context.__input=input;adapter.context.__options=options;return JSON.parse(JSON.stringify(vm.runInContext('EDB_TOOL.run(__input,__options)',adapter.context,{timeout:1000})));}
test('reject invalid option containers and unknown properties',()=>{
  for(const options of [null,[],false,'x',3])assert.throws(()=>invoke('x',options),/Options must be an object/);
  assert.throws(()=>invoke('x',{...defaults,unexpected:true}),/Unsupported setting/);
});
test('reject invalid input types without coercion',()=>{
  for(const input of [null,undefined,123,{},[],true])assert.throws(()=>invoke(input),/Text must be a string/);
});
test('full UTF-16 limit including emoji is exact, oversized is never truncated',()=>{
  const text='😀'.repeat(50000);assert.equal(invoke(text).inputUnits,100000);
  assert.throws(()=>invoke(text+'😀'),/100,000 UTF-16/);
  assert.throws(()=>invoke(' '.repeat(100001)),/100,000 UTF-16/);
});
test('input/options are not mutated',()=>{
  const options=Object.freeze({...defaults}),copy={...options};const input='A\r\n é 😀\n';invoke(input,options);assert.deepEqual(options,copy);assert.equal(input,'A\r\n é 😀\n');
});
test('100,001 records retain all duplicates, blanks and correct line counts',()=>{
  const input='\n'.repeat(100000);assert.deepEqual(invoke(input),{text:input,inputUnits:100000,outputUnits:100000,originalLines:100001,retainedLines:100001,invalidNumeric:0});
});
test('50,000 repeated records plus trailing blank stay exact and stable',()=>{
  const input='x\n'.repeat(50000),text='\n'+'x\n'.repeat(49999)+'x';
  assert.deepEqual(invoke(input),{text,inputUnits:100000,outputUnits:100000,originalLines:50001,retainedLines:50001,invalidNumeric:0});
});
test('all 32 mode/boolean combinations at the exact input boundary',()=>{
  const input=' B \na\nA\n\n'+'x'.repeat(99991);assert.equal(input.length,100000);
  for(const mode of ['az','za','numeric-asc','numeric-desc'])for(let mask=0;mask<8;mask++){
    const result=invoke(input,{mode,caseSensitive:!!(mask&1),trimComparison:!!(mask&2),removeBlankLines:!!(mask&4)});
    assert.equal(result.originalLines,5);assert.equal(result.retainedLines,mask&4?4:5);assert.equal(result.invalidNumeric,mode.startsWith('numeric')?result.retainedLines:0);assert.equal(result.text.includes(' B '),true);assert.equal(result.outputUnits,result.text.length);
  }
});
test('signed zero and overflow/invalid keys preserve stable order',()=>{
  assert.equal(invoke('-0\n+0\n0\n0.0\n1e999\nNaN',{mode:'numeric-desc'}).text,'-0\n+0\n0\n0.0\n1e999\nNaN');
});
test('invalid settings fail, including string booleans',()=>{
  for(const key of ['caseSensitive','trimComparison','removeBlankLines'])for(const bad of [null,0,'false',{}])assert.throws(()=>invoke('x',{[key]:bad}),/Unsupported setting/);
  assert.throws(()=>invoke('x',{mode:'locale'}),/Unsupported setting/);
});
