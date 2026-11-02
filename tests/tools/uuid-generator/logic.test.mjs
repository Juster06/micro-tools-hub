import {test} from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';
import {loadLogic} from '../../../scripts/tool-tests/runner.mjs';
const adapter=loadLogic(fileURLToPath(new URL('../../../uuid-generator/index.html',import.meta.url)));
const defaults={"entropy": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},seed="1";
function invoke(input,options=defaults){adapter.context.__input=input;adapter.context.__options=options;return JSON.parse(JSON.stringify(vm.runInContext('EDB_TOOL.run(__input,__options)',adapter.context,{timeout:1000})));}
test('non-string input is rejected without coercion',()=>{for(const input of [null,undefined,1,true,{},[]])assert.throws(()=>invoke(input),/Input must be a string/);});
test('invalid option containers and unknown settings are rejected',()=>{for(const options of [null,[],false,1,'x'])assert.throws(()=>invoke(seed,options),/Options must be an object/);assert.throws(()=>invoke(seed,{...defaults,unknown:true}),/Unsupported setting/);});
test('original input and frozen options remain unchanged and repeat exactly',()=>{const options=Object.freeze({...defaults});const before=JSON.stringify(options);assert.deepEqual(invoke(seed,options),invoke(seed,options));assert.equal(JSON.stringify(options),before);});
test('raw field limits apply before trimming, including UTF-16 emoji',()=>{for(const input of [' '.repeat(4+1),'😀'.repeat(4)])assert.throws(()=>invoke(input),/UTF-16/);});
test('RFC v4 known byte vectors, uppercase and input entropy immutability',()=>{const entropy=Object.freeze(Array.from({length:16},(_,i)=>i)),op=Object.freeze({entropy,uppercase:true});assert.deepEqual(invoke('1',op),{text:'00010203-0405-4607-8809-0A0B0C0D0E0F',count:1,characters:36,entropyBytes:16});assert.equal(entropy[6],6);assert.equal(entropy[8],8);});
test('sparse/undefined/noninteger/typed entropy arrays fail instead of emitting corrupt IDs',()=>{for(const entropy of [new Array(16),Array(16).fill(undefined),new Uint8Array(16),[NaN,...Array(15).fill(0)],[Infinity,...Array(15).fill(0)],[true,...Array(15).fill(0)]])assert.throws(()=>invoke('1',{entropy}),/entropy|setting/);});
test('every entropy byte value has exact v4/variant bits with only six overwritten bits',()=>{for(let value=0;value<256;value++){const result=invoke('1',{entropy:Array(16).fill(value)}).text;assert.match(result,/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/);const bytes=Buffer.from(result.replaceAll('-',''),'hex');for(let i=0;i<16;i++)assert.equal(bytes[i],i===6?(value&15)|64:i===8?(value&63)|128:value);}});
test('maximum batch size is exactly 1,000 records and 36,999 characters',()=>{const result=invoke('1000',{entropy:Array(16000).fill(255)});assert.equal(result.text,'ffffffff-ffff-4fff-bfff-ffffffffffff\n'.repeat(1000).slice(0,-1));assert.equal(result.characters,36999);assert.equal(result.count,1000);assert.equal(result.entropyBytes,16000);});
test('pure adapter has no crypto, DOM or Math.random dependency',()=>{vm.runInContext("Math.random=()=>{throw Error('Noncryptographic random fallback');};",adapter.context);assert.equal(invoke('1').text,'00000000-0000-4000-8000-000000000000');assert.equal(vm.runInContext('typeof crypto',adapter.context),'undefined');});
test('count validation rejects fractional, Unicode and over-bounds input before formatting',()=>{for(const input of ['0','1001','-1','1.2','١','1e3','10000'])assert.throws(()=>invoke(input));assert.equal(invoke('0001').count,1);});
