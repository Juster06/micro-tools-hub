
import {test} from 'node:test';import assert from 'node:assert/strict';import {logic} from '../task18-logic.mjs';
const {call}=logic('youtube-title-checker');
test('code points distinguish supplementary emoji, combining marks and ZWJ components',()=>{assert.equal(call('😀').count,1);assert.equal(call('e\u0301').count,2);assert.equal(call('👩‍💻').count,3)});
test('10,000 ASCII and supplementary code points are accepted; both next boundaries reject',()=>{for(const x of ['a','😀']){assert.equal(call(x.repeat(10000)).count,10000);assert.throws(()=>call(x.repeat(10001)),/10,000/)}});
test('preview caps display without truncating copied output',()=>{const r=call('😀'.repeat(61));assert.equal(r.preview,'😀'.repeat(60)+'…');assert.equal(r.text,'😀'.repeat(61))});
test('guidance at 99, 100, 101 and editable guide boundaries',()=>{assert.match(call('a'.repeat(99)).guidance,/1 remaining/);assert.match(call('a'.repeat(100)).guidance,/0 remaining/);assert.match(call('a'.repeat(101)).guidance,/1 over/);for(const v of [-1,10001,1.5,'',NaN,Infinity])assert.throws(()=>call('x',{guide:v}),/Guide/)});
test('normalization preserves whitespace, blank lines and markup as data',()=>{const x=' <script>\r\n\r\n😀 ';assert.equal(call(x).text,' <script>\n\n😀 ');assert.match(call(x).guidance,/Angle brackets/)});
