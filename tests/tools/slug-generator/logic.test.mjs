import {test} from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';
import {loadLogic} from '../../../scripts/tool-tests/runner.mjs';
const adapter=loadLogic(fileURLToPath(new URL('../../../slug-generator/index.html',import.meta.url)));
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
test('full-limit single token is preserved without truncation',()=>{
  const text='a'.repeat(100000);assert.deepEqual(invoke(text),{text,inputUnits:100000,outputUnits:100000,segments:1});
});
test('50,000 segments produce exact hyphens/counts at input limit',()=>{
  assert.deepEqual(invoke('a '.repeat(50000)),{text:'a-'.repeat(49999)+'a',inputUnits:100000,outputUnits:99999,segments:50000});
});
test('all settings at limit retain documented accent/ASCII behavior',()=>{
  const input='é '.repeat(50000);
  for(const mode of ['unicode','ascii'])for(const stripAccents of [true,false]){
    const result=invoke(input,{mode,stripAccents});
    const token=stripAccents?'e':mode==='unicode'?'é':'';
    assert.equal(result.text,token?(token+'-').repeat(49999)+token:'');assert.equal(result.segments,token?50000:0);
  }
});
test('full-limit symbols produce an honestly empty slug',()=>assert.deepEqual(invoke('😀'.repeat(50000)),{text:'',inputUnits:100000,outputUnits:0,segments:0}));
test('invalid policy and accent types fail explicitly',()=>{
  for(const mode of [null,'ASCII',2])assert.throws(()=>invoke('a',{mode}),/Unsupported setting/);
  for(const stripAccents of [null,0,'false',{}])assert.throws(()=>invoke('a',{stripAccents}),/Unsupported setting/);
});
