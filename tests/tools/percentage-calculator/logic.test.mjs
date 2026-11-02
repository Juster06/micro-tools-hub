import {test} from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';
import {loadLogic} from '../../../scripts/tool-tests/runner.mjs';
const adapter=loadLogic(fileURLToPath(new URL('../../../percentage-calculator/index.html',import.meta.url)));
const defaults={"b": "80"},seed="12.5";
function invoke(input,options=defaults){adapter.context.__input=input;adapter.context.__options=options;return JSON.parse(JSON.stringify(vm.runInContext('EDB_TOOL.run(__input,__options)',adapter.context,{timeout:1000})));}
test('non-string input is rejected without coercion',()=>{for(const input of [null,undefined,1,true,{},[]])assert.throws(()=>invoke(input),/Input must be a string/);});
test('invalid option containers and unknown settings are rejected',()=>{for(const options of [null,[],false,1,'x'])assert.throws(()=>invoke(seed,options),/Options must be an object/);assert.throws(()=>invoke(seed,{...defaults,unknown:true}),/Unsupported setting/);});
test('original input and frozen options remain unchanged and repeat exactly',()=>{const options=Object.freeze({...defaults});const before=JSON.stringify(options);assert.deepEqual(invoke(seed,options),invoke(seed,options));assert.equal(JSON.stringify(options),before);});
test('raw field limits apply before trimming, including UTF-16 emoji',()=>{for(const input of [' '.repeat(64+1),'😀'.repeat(64)])assert.throws(()=>invoke(input),/UTF-16/);});
test('all precision/formula combinations use independently known eighths',()=>{for(const precision of ['0','2','4','6']){const suffix={'0':'13','2':'12.50','4':'12.5000','6':'12.500000'}[precision];assert.equal(invoke('1',{b:'8',mode:'ratio',precision}).result,suffix);assert.equal(invoke('25',{b:'50',precision}).result,suffix);}});
test('signed and over-100 percentages are supported with explicit formulas',()=>{assert.equal(invoke('-25',{b:'-80'}).result,'20.00');assert.equal(invoke('200',{b:'4'}).result,'8.00');assert.equal(invoke('1',{b:'-8',mode:'ratio'}).result,'-12.50');});
test('finite exponent input, whitespace and exact 64-unit input are accepted',()=>{assert.equal(invoke(' +1.25e1 ',{b:'8e1'}).result,'10.00');assert.equal(invoke('0'.repeat(63)+'1',{b:'100'}).result,'1.00');assert.equal(invoke('0',{b:'0'}).result,'0.00');});
test('input underflow/overflow and result expansion are rejected separately',()=>{for(const a of ['1e-400','1e-13','1e13','1e999'])assert.throws(()=>invoke(a,{b:'1'}));assert.throws(()=>invoke('1e12',{b:'1e-12',mode:'ratio'}),/Result exceeds/);assert.throws(()=>invoke('1',{b:'-0',mode:'ratio'}),/Whole must not be zero/);});
test('binary rounding and displayed negative zero follow the disclosed native policy',()=>{assert.equal(invoke('100',{b:'1.005'}).result,'1.00');assert.equal(invoke('-1e-12',{b:'1'}).result,'0.00');assert.equal(invoke('50',{b:'1.25',precision:'4'}).result,'0.6250');});
test('both numeric fields reject nonfinite/symbol inputs and invalid precision values',()=>{for(const b of ['','NaN','Infinity','0x10','12%','1,000','😀'])assert.throws(()=>invoke('1',{b}));for(const precision of ['1',2,null])assert.throws(()=>invoke('1',{b:'1',precision}),/Unsupported setting/);});
