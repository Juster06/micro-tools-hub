import {test} from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';
import {loadLogic} from '../../../scripts/tool-tests/runner.mjs';
const adapter=loadLogic(fileURLToPath(new URL('../../../text-reverser/index.html',import.meta.url)));
function invoke(input,options={}){adapter.context.__input=input;adapter.context.__options=options;return JSON.parse(JSON.stringify(vm.runInContext('EDB_TOOL.run(__input,__options)',adapter.context,{timeout:1000})));}
const valid="abc";
test('reject invalid input types without coercion',()=>{for(const input of [null,undefined,true,0,{},[]])assert.throws(()=>invoke(input),/Text must be a string/);});
test('reject invalid option containers and unknown keys',()=>{for(const options of [null,[],false,3,'x'])assert.throws(()=>invoke(valid,options),/Options must be an object/);assert.throws(()=>invoke(valid,{unknown:true}),/Unsupported setting/);});
test('oversized inputs fail before content processing and are never truncated',()=>{for(const input of [' '.repeat(100001),'😀'.repeat(50001)])assert.throws(()=>invoke(input),/100,000 UTF-16/);});
test('options and repeated results are immutable and deterministic',()=>{const options=Object.freeze({});const a=invoke(valid,options);assert.deepEqual(invoke(valid,options),a);assert.deepEqual(options,{});assert.equal(a.outputUnits,a.text.length);assert.equal(a.inputUnits,valid.length);});
test('exact full-limit graphemes and code-unit statistics',()=>{const input='😀'.repeat(50000);assert.deepEqual(invoke(input),{text:input,inputUnits:100000,outputUnits:100000,units:50000,policy:'Grapheme clusters'});});
test('full-limit word and line records retain all whitespace and blanks',()=>{assert.equal(invoke('a '.repeat(50000),{mode:'word'}).text,'a '.repeat(50000));const input='\n'.repeat(100000);assert.equal(invoke(input,{mode:'line'}).units,100001);assert.equal(invoke(input,{mode:'line'}).text,input);});
test('explicit code-point fallback preserves surrogate pairs and discloses cluster splitting',()=>{vm.runInContext('globalThis.__segmenter=Intl.Segmenter;Intl.Segmenter=undefined;',adapter.context);try{assert.deepEqual(invoke('a👩‍💻é'),{text:'́e💻‍👩a',inputUnits:8,outputUnits:8,units:6,policy:'Code-point fallback — emoji clusters may separate'});}finally{vm.runInContext('Intl.Segmenter=__segmenter;',adapter.context);}});
test('mixed line separators/trailing blank exact; words preserve all original whitespace slots',()=>{assert.equal(invoke('a\r\nb\rc\n',{mode:'line'}).text,'\nc\nb\na');assert.equal(invoke(' \ta,\r\nb!  c ',{mode:'word'}).text,' \tc\r\nb!  a, ');});
test('bad reversal options fail',()=>{for(const mode of [null,0,'characters',true])assert.throws(()=>invoke('a',{mode}),/Unsupported setting/);});
