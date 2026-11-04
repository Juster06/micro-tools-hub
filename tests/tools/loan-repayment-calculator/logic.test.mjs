import {test} from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';
import {loadLogic} from '../../../scripts/tool-tests/runner.mjs';
const c=loadLogic(fileURLToPath(new URL('../../../loan-repayment-calculator/index.html',import.meta.url))).context;
function run(input,options={}){c.input=input;c.options=options;return vm.runInContext('EDB_TOOL.run(input,options)',c,{timeout:1000})}
test('independent two-period annual amortization example',()=>assert.match(run('1000',{rate:'10',frequency:'1',years:'2'}),/^Estimated periodic payment: 576.19\nTotal repayment: 1152.38\nTotal interest: 152.38/));
test('zero rate payment and last period correction',()=>{const x=run('100',{rate:'0',frequency:'12',years:'1'});assert.match(x,/Estimated periodic payment: 8.33/);assert.match(x,/12 \| 8.37 \| 0.00 \| 0.00/);assert.match(x,/Total repayment: 100.00/)});
test('interest rounds half-up each period',()=>assert.match(run('0.05',{rate:'10',frequency:'1',years:'1'}),/1 \| 0.06 \| 0.01 \| 0.00/));
test('maximum size and duration are bounded and finish',()=>{const x=run('1000000000000',{rate:'0',frequency:'12',years:'50'});assert.match(x,/Total repayment: 1000000000000.00/);assert.match(x,/600 \|/)});
test('invalid and unsafe settings fail explicitly',()=>{for(const [v,o] of [['',{}],['-2',{}],['1.001',{}],['1000000000001',{}],['1',{rate:'101'}],['1',{rate:'NaN'}],['1',{years:'51'}],['1',{frequency:'3'}],['0.01',{years:'50'}],['1',{unknown:'x'}]])assert.throws(()=>run(v,o))});
