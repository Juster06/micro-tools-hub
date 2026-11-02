import {test} from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';
import {loadLogic} from '../../../scripts/tool-tests/runner.mjs';
const adapter=loadLogic(fileURLToPath(new URL('../../../percentage-change-calculator/index.html',import.meta.url)));
const defaults={"b": "125"},seed="100";
function invoke(input,options=defaults){adapter.context.__input=input;adapter.context.__options=options;return JSON.parse(JSON.stringify(vm.runInContext('EDB_TOOL.run(__input,__options)',adapter.context,{timeout:1000})));}
test('non-string input is rejected without coercion',()=>{for(const input of [null,undefined,1,true,{},[]])assert.throws(()=>invoke(input),/Input must be a string/);});
test('invalid option containers and unknown settings are rejected',()=>{for(const options of [null,[],false,1,'x'])assert.throws(()=>invoke(seed,options),/Options must be an object/);assert.throws(()=>invoke(seed,{...defaults,unknown:true}),/Unsupported setting/);});
test('original input and frozen options remain unchanged and repeat exactly',()=>{const options=Object.freeze({...defaults});const before=JSON.stringify(options);assert.deepEqual(invoke(seed,options),invoke(seed,options));assert.equal(JSON.stringify(options),before);});
test('raw field limits apply before trimming, including UTF-16 emoji',()=>{for(const input of [' '.repeat(64+1),'😀'.repeat(64)])assert.throws(()=>invoke(input),/UTF-16/);});
test('negative base policy covers increase, decrease and crossing zero',()=>{assert.equal(invoke('-100',{b:'-50'}).percent,'50.00');assert.equal(invoke('-100',{b:'-150'}).percent,'-50.00');assert.equal(invoke('-100',{b:'100'}).percent,'200.00');assert.equal(invoke('100',{b:'-100'}).percent,'-200.00');});
test('direction uses unrounded delta, even when display is zero',()=>{const value=invoke('1',{b:'1.000000000001'});assert.equal(value.direction,'Increase');assert.equal(value.percent,'0.00');assert.equal(invoke('1',{b:'1'}).direction,'No change');});
test('every precision is exact for independently known quarter change',()=>{for(const precision of ['0','2','4','6'])assert.equal(invoke('80',{b:'100',precision}).percent,{'0':'25','2':'25.00','4':'25.0000','6':'25.000000'}[precision]);});
test('zero base errors include signed zero and zero-to-zero',()=>{for(const a of ['0','-0','0e12'])for(const b of ['0','1'])assert.throws(()=>invoke(a,{b}),/Starting value must not be zero/);});
test('numeric and result boundaries reject underflow and excessive ratios',()=>{assert.equal(invoke('1e12',{b:'-1e12'}).difference,'-2000000000000.00');assert.throws(()=>invoke('1e-12',{b:'1e12'}),/Result exceeds/);for(const b of ['1e-400','1e13','1,000','NaN'])assert.throws(()=>invoke('1',{b}));});
test('all precision/container errors and field-length guards remain strict',()=>{for(const precision of ['3',2,null])assert.throws(()=>invoke('1',{b:'2',precision}),/Unsupported setting/);assert.throws(()=>invoke('1',{b:'1'.repeat(65)}),/64 UTF-16/);assert.equal(invoke(' 8e1 ',{b:'1e2'}).percent,'25.00');});
