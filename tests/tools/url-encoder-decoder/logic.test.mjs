import {test} from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';
import {loadLogic} from '../../../scripts/tool-tests/runner.mjs';
const adapter=loadLogic(fileURLToPath(new URL('../../../url-encoder-decoder/index.html',import.meta.url)));
function invoke(input,options={}){adapter.context.__input=input;adapter.context.__options=options;return JSON.parse(JSON.stringify(vm.runInContext('EDB_TOOL.run(__input,__options)',adapter.context,{timeout:1000})));}
const valid="abc";
test('reject invalid input types without coercion',()=>{for(const input of [null,undefined,true,0,{},[]])assert.throws(()=>invoke(input),/Text must be a string/);});
test('reject invalid option containers and unknown keys',()=>{for(const options of [null,[],false,3,'x'])assert.throws(()=>invoke(valid,options),/Options must be an object/);assert.throws(()=>invoke(valid,{unknown:true}),/Unsupported setting/);});
test('oversized inputs fail before content processing and are never truncated',()=>{for(const input of [' '.repeat(100001),'😀'.repeat(50001)])assert.throws(()=>invoke(input),/100,000 UTF-16/);});
test('options and repeated results are immutable and deterministic',()=>{const options=Object.freeze({});const a=invoke(valid,options);assert.deepEqual(invoke(valid,options),a);assert.deepEqual(options,{});assert.equal(a.outputUnits,a.text.length);assert.equal(a.inputUnits,valid.length);});
test('exact full-limit encode expansion and all four native mode oracles',()=>{const input='ࠀ'.repeat(100000),result=invoke(input);assert.equal(result.text,'%E0%A0%80'.repeat(100000));assert.equal(result.outputUnits,900000);for(const [mode,codec] of Object.entries({'encode-component':encodeURIComponent,'decode-component':decodeURIComponent,'encode-uri':encodeURI,'decode-uri':decodeURI})){const text=mode.startsWith('decode')?'https://x/%2F?q=a+b%20é':'https://x/a b?q=é+😀';assert.equal(invoke(text,{mode}).text,codec(text));}});
test('100,000-unit decode, mixed case escapes and plus handling are exact',()=>{const input='a'.repeat(100000);assert.equal(invoke(input,{mode:'decode-component'}).text,input);assert.equal(invoke('%2f%2F%2b+',{mode:'decode-component'}).text,'//++');assert.equal(invoke('%2f%2F%2b+',{mode:'decode-uri'}).text,'%2f%2F%2b+');});
test('encoding rejects lone surrogates and decoding rejects invalid UTF-8/escapes',()=>{for(const mode of ['encode-component','encode-uri'])for(const text of ['\ud800','\udfff','x\ud800y'])assert.throws(()=>invoke(text,{mode}),/Cannot encode/);for(const mode of ['decode-component','decode-uri'])for(const text of ['%','%GG','%FF','%C0%AF','%ED%A0%80','%F4%90%80%80'])assert.throws(()=>invoke(text,{mode}),/Cannot decode/);});
test('Unicode, null characters and no normalization match native codec roundtrip',()=>{for(const text of ['\0','é','é','😀👩‍💻','\ufeff','a\r\nb',"!'()*"]){assert.equal(invoke(invoke(text).text,{mode:'decode-component'}).text,text);}});
test('invalid mode types fail',()=>{for(const mode of [null,1,'form','decode'])assert.throws(()=>invoke('x',{mode}),/Unsupported setting/);});
