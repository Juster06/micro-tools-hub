import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';
import {loadLogic} from '../../../scripts/tool-tests/runner.mjs';

const adapter=loadLogic(fileURLToPath(new URL('../../../duplicate-line-remover/index.html',import.meta.url)));
function invoke(input,options={},method='run') {
  adapter.context.__input=input;adapter.context.__options=options;
  return JSON.parse(JSON.stringify(vm.runInContext(`EDB_TOOL.${method}(__input,__options)`,adapter.context,{timeout:1000})));
}
const records=Array.from({length:10000},(_,i)=>'L'+String(i).padStart(8,'0'));
const unique=records.join('\n')+'\n';
for(let mask=0;mask<16;mask++) {
  const options=Object.fromEntries(['ignoreCase','trimComparison','removeBlankLines','sort'].map((key,index)=>[key,Boolean(mask&(1<<index))]));
  test('full 100,000-unit unique input: settings '+mask,()=>{
    assert.equal(unique.length,100000);
    const text=options.removeBlankLines?records.join('\n'):options.sort?'\n'+records.join('\n'):unique;
    assert.deepEqual(invoke(unique,options),{text,originalLines:10001,retainedLines:options.removeBlankLines?10000:10001,removedDuplicates:0,removedBlankLines:options.removeBlankLines?1:0,totalRemoved:options.removeBlankLines?1:0});
  });
}
test('50,000 repeated lines preserve first record and exact counts',()=>{
  assert.deepEqual(invoke('x\n'.repeat(50000)),{text:'x\n',originalLines:50001,retainedLines:2,removedDuplicates:49999,removedBlankLines:0,totalRemoved:49999});
});
test('full-limit separators count 100,001 records without confusing an empty output',()=>{
  assert.deepEqual(invoke('\n'.repeat(100000)),{text:'',originalLines:100001,retainedLines:1,removedDuplicates:100000,removedBlankLines:0,totalRemoved:100000});
});
test('one full-limit line remains byte-for-byte unchanged',()=>{
  const text='a'.repeat(100000);assert.deepEqual(invoke(text),{text,originalLines:1,retainedLines:1,removedDuplicates:0,removedBlankLines:0,totalRemoved:0});
});
test('full-limit whitespace respects blank removal',()=>{
  const text=' '.repeat(100000);assert.equal(invoke(text).text,text);assert.deepEqual(invoke(text,{removeBlankLines:true}),{text:'',originalLines:1,retainedLines:0,removedDuplicates:0,removedBlankLines:1,totalRemoved:1});
});
test('oversized text including whitespace is rejected for every option combination',()=>{
  for(let mask=0;mask<16;mask++) {
    const options=Object.fromEntries(['ignoreCase','trimComparison','removeBlankLines','sort'].map((key,index)=>[key,Boolean(mask&(1<<index))]));
    for(const text of ['a'.repeat(100001),' '.repeat(100001)])assert.throws(()=>invoke(text,options),/100,000 UTF-16/);
  }
});
test('emoji limit is UTF-16 units, with no normalization or truncation',()=>{
  const text='😀'.repeat(50000);assert.equal(invoke(text).text,text);assert.throws(()=>invoke(text+'😀'),/100,000 UTF-16/);
});
test('invalid option containers and types fail explicitly',()=>{
  for(const options of [null,[],false,'sort'])assert.throws(()=>invoke('x',options),/Options must be an object/);
  for(const key of ['ignoreCase','trimComparison','removeBlankLines','sort'])for(const value of [null,1,'false',[],{}])assert.throws(()=>invoke('x',{[key]:value}),/supported booleans/);
});
test('input and options are not mutated',()=>{
  const text=' Apple \napple\n\n',options=Object.freeze({ignoreCase:true,trimComparison:true,removeBlankLines:true,sort:true});
  assert.equal(invoke(text,options).text,' Apple ');assert.equal(text,' Apple \napple\n\n');assert.deepEqual(options,{ignoreCase:true,trimComparison:true,removeBlankLines:true,sort:true});
});
test('line counting agrees with mixed endings and empty input',()=>{
  for(const [text,count] of [['',0],['\n',2],['a\r\nb\rc\n',4],['a\u2028b',1]])assert.equal(invoke(text,{},'countLines'),count);
  assert.throws(()=>invoke(null,{},'countLines'),/Text must be a string/);
});
