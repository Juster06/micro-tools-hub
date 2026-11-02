import {test} from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';
import {loadLogic} from '../../../scripts/tool-tests/runner.mjs';
const adapter=loadLogic(fileURLToPath(new URL('../../../base64-encoder-decoder/index.html',import.meta.url)));
function invoke(input,options={}){adapter.context.__input=input;adapter.context.__options=options;return JSON.parse(JSON.stringify(vm.runInContext('EDB_TOOL.run(__input,__options)',adapter.context,{timeout:1000})));}
const valid="abc";
test('reject invalid input types without coercion',()=>{for(const input of [null,undefined,true,0,{},[]])assert.throws(()=>invoke(input),/Text must be a string/);});
test('reject invalid option containers and unknown keys',()=>{for(const options of [null,[],false,3,'x'])assert.throws(()=>invoke(valid,options),/Options must be an object/);assert.throws(()=>invoke(valid,{unknown:true}),/Unsupported setting/);});
test('oversized inputs fail before content processing and are never truncated',()=>{for(const input of [' '.repeat(100001),'😀'.repeat(50001)])assert.throws(()=>invoke(input),/100,000 UTF-16/);});
test('options and repeated results are immutable and deterministic',()=>{const options=Object.freeze({});const a=invoke(valid,options);assert.deepEqual(invoke(valid,options),a);assert.deepEqual(options,{});assert.equal(a.outputUnits,a.text.length);assert.equal(a.inputUnits,valid.length);});
test('RFC vectors and varied Unicode match independent Node Buffer oracle',()=>{for(const text of ['','f','fo','foo','foob','fooba','foobar','\0','😀é中文','é','\ufeffa','\r\n',String.fromCodePoint(...Array.from({length:1000},(_,i)=>32+i))]){const encoded=Buffer.from(text,'utf8').toString('base64');assert.equal(invoke(text).text,encoded);assert.equal(invoke(encoded,{mode:'decode'}).text,text);assert.equal(invoke(text).bytes,Buffer.byteLength(text));}});
test('maximum input/output encoding limits are exact and permitted',()=>{const input='ࠀ'.repeat(100000),result=invoke(input);assert.equal(result.text,Buffer.from(input).toString('base64'));assert.equal(result.outputUnits,400000);assert.equal(result.bytes,300000);assert.equal(invoke('😀'.repeat(50000)).bytes,200000);});
test('full-limit decode accepts canonical text and accurately counts bytes',()=>{const input='YWFh'.repeat(25000),result=invoke(input,{mode:'decode'});assert.equal(result.text,'a'.repeat(75000));assert.equal(result.bytes,75000);assert.equal(result.outputUnits,75000);});
test('strict canonical validation rejects pad bits/placement/alphabet/UTF-8 and lone surrogates',()=>{for(const text of ['Zh==','Zm9=','====','Z===','Zg=','Zg','Zg==AAAA','AA=A','____',' Zg==','Zg==\u00a0'])assert.throws(()=>invoke(text,{mode:'decode'}),/Invalid Base64/);for(const text of ['/w==','wK8=','7aCA','9JCAgA=='])assert.throws(()=>invoke(text,{mode:'decode'}),/not valid UTF-8/);assert.throws(()=>invoke('\ud800'),/unpaired UTF-16/);});
test('ASCII whitespace opt-in is exact and never removes Unicode spaces',()=>{assert.equal(invoke(' \tZg==\r\n',{mode:'decode',ignoreWhitespace:true}).text,'f');assert.throws(()=>invoke('Zg==\u00a0',{mode:'decode',ignoreWhitespace:true}),/Invalid Base64/);assert.equal(invoke(' ',{ignoreWhitespace:true}).text,'IA==');for(const options of [{mode:null},{ignoreWhitespace:'true'}])assert.throws(()=>invoke('x',options),/Unsupported setting/);});
