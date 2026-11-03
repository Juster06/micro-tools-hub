import {test} from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';
import {loadLogic} from '../../../scripts/tool-tests/runner.mjs';
const a=loadLogic(fileURLToPath(new URL('../../../file-size-converter/index.html',import.meta.url))).context;
function run(input,options={}){a.input=input;a.options=options;return vm.runInContext('EDB_TOOL.run(input,options)',a,{timeout:1000});}
test('SI, IEC and mixed units have exact independent known vectors',()=>{assert.equal(run('1000'),'1 kB');assert.equal(run('1024',{from:'B',to:'KiB'}),'1 KiB');assert.equal(run('1',{from:'MiB',to:'kB'}),'1048.576 kB');assert.equal(run('1',{from:'MB',to:'KiB'}),'976.5625 KiB');});
test('zero, decimals, same units and arbitrary precision remain exact',()=>{assert.equal(run('0',{from:'PB',to:'B'}),'0 B');assert.equal(run('.5',{from:'KiB',to:'B'}),'512 B');assert.equal(run('123456789012345678901234567890',{from:'PB',to:'B'}),'123456789012345678901234567890000000000000000 B');});
test('rounding and sub-resolution positive values are explicitly disclosed',()=>{assert.match(run('1',{from:'B',to:'KiB'}),/^0.0009765625 KiB$/);assert.match(run('1',{from:'B',to:'PiB'}),/^< 0.000000000001 PiB$/);assert.match(run('1',{from:'kB',to:'MiB'}),/^≈ /);});
test('invalid data, options, oversized inputs and excessive fractional precision fail',()=>{for(const x of ['', ' ', '-1','1e3','1,0','😀','1'.repeat(61),'0.'+'1'.repeat(31)])assert.throws(()=>run(x));for(const opts of [null,[],{from:'KB'},{to:'bits'},{unknown:'x'}])assert.throws(()=>run('1',opts));for(const x of [null,1,{},[]])assert.throws(()=>run(x),/Input must be a string/);});
test('frozen settings are unchanged and repeated conversions are deterministic',()=>{const settings=Object.freeze({from:'GiB',to:'MB'});assert.equal(run('2',settings),run('2',settings));assert.deepEqual(settings,{from:'GiB',to:'MB'});});
