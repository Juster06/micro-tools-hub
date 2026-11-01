import {test} from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';
import {loadLogic} from '../../../scripts/tool-tests/runner.mjs';
const adapter=loadLogic(fileURLToPath(new URL('../../../find-and-replace/index.html',import.meta.url)));
const defaults={find:'x'};
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
test('full-limit replacement returns exact result and count',()=>{
  assert.deepEqual(invoke('x'.repeat(100000),{find:'x',replacement:'y'}),{text:'y'.repeat(100000),inputUnits:100000,outputUnits:100000,matches:100000});
});
test('output exactly one million is allowed; expansion above it fails',()=>{
  const result=invoke('x'.repeat(100000),{find:'x',replacement:'y'.repeat(10)});assert.equal(result.text,'y'.repeat(1000000));assert.equal(result.matches,100000);
  assert.throws(()=>invoke('x'.repeat(100000),{find:'x',replacement:'y'.repeat(11)}),/1,000,000 UTF-16/);
});
test('search/replacement limits are independent and strict',()=>{
  const text='x'.repeat(10000);assert.equal(invoke(text,{find:text,replacement:'z'.repeat(10000)}).matches,1);
  for(const options of [{find:text+'x'},{find:'x',replacement:text+'x'},{find:null},{find:'x',replacement:42},{find:'x',caseSensitive:'true'}])assert.throws(()=>invoke('x',options),/Unsupported setting/);
});
test('every regex metacharacter is literal and dollar replacement unexpanded',()=>{
  const text='.*+?^${}()|[]\\';for(const find of text)assert.equal(invoke(text,{find,replacement:'$&'}).text,text.split(find).join('$&'));
});
test('no match does not expand output or execute markup',()=>{
  const input='<img src=x onerror=alert(1)>'.repeat(1000),result=invoke(input,{find:'never',replacement:'x'.repeat(10000)});assert.equal(result.text,input);assert.equal(result.matches,0);
});
