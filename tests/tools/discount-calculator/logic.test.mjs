import {test} from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';
import {loadLogic} from '../../../scripts/tool-tests/runner.mjs';
const adapter=loadLogic(fileURLToPath(new URL('../../../discount-calculator/index.html',import.meta.url)));
const defaults={"b": "25"},seed="100";
function invoke(input,options=defaults){adapter.context.__input=input;adapter.context.__options=options;return JSON.parse(JSON.stringify(vm.runInContext('EDB_TOOL.run(__input,__options)',adapter.context,{timeout:1000})));}
test('non-string input is rejected without coercion',()=>{for(const input of [null,undefined,1,true,{},[]])assert.throws(()=>invoke(input),/Input must be a string/);});
test('invalid option containers and unknown settings are rejected',()=>{for(const options of [null,[],false,1,'x'])assert.throws(()=>invoke(seed,options),/Options must be an object/);assert.throws(()=>invoke(seed,{...defaults,unknown:true}),/Unsupported setting/);});
test('original input and frozen options remain unchanged and repeat exactly',()=>{const options=Object.freeze({...defaults});const before=JSON.stringify(options);assert.deepEqual(invoke(seed,options),invoke(seed,options));assert.equal(JSON.stringify(options),before);});
test('raw field limits apply before trimming, including UTF-16 emoji',()=>{for(const input of [' '.repeat(64+1),'😀'.repeat(64)])assert.throws(()=>invoke(input),/UTF-16/);});
test('discount endpoints include zero price and full discount',()=>{assert.equal(invoke('100',{b:'0'}).finalPrice,'100.00');assert.equal(invoke('100',{b:'100'}).finalPrice,'0.00');assert.equal(invoke('0',{b:'50'}).savings,'0.00');});
test('all precision choices preserve independent exact quarter-price breakdown',()=>{for(const precision of ['0','2','4','6']){const result=invoke('100',{b:'25',precision});const zeros=precision==='0'?'':'.'+'0'.repeat(Number(precision));assert.equal(result.originalPrice,'100'+zeros);assert.equal(result.savings,'25'+zeros);assert.equal(result.finalPrice,'75'+zeros);}});
test('negative original and outside-range discounts fail, not clamp',()=>{assert.throws(()=>invoke('-1',{b:'10'}),/nonnegative/);for(const b of ['-0.1','100.000001','101'])assert.throws(()=>invoke('1',{b}),/from 0 to 100/);});
test('maximum supported price, decimal percent and exponent syntax remain bounded',()=>{assert.equal(invoke('1e12',{b:'100'}).savings,'1000000000000.00');assert.equal(invoke(' 8e1 ',{b:'1.25e1'}).finalPrice,'70.00');assert.ok(invoke('1e12',{b:'99.999999',precision:'6'}).text.length<1000);});
test('native binary rounding, independent amounts and negative zero are disclosed',()=>{assert.equal(invoke('1.005',{b:'0'}).originalPrice,'1.00');assert.equal(invoke('-0',{b:'0'}).finalPrice,'0.00');assert.equal(invoke('0.03',{b:'50'}).savings,'0.01');assert.equal(invoke('0.03',{b:'50'}).finalPrice,'0.01');});
test('both fields enforce numeric, magnitude, precision and length contracts',()=>{for(const b of ['1e-400','NaN','0x10','10%','1'.repeat(65)])assert.throws(()=>invoke('100',{b}));for(const precision of ['3',2,null])assert.throws(()=>invoke('100',{b:'10',precision}),/Unsupported setting/);});
