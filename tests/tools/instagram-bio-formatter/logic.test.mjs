
import {test} from 'node:test';import assert from 'node:assert/strict';import {logic} from '../task18-logic.mjs';const {call}=logic('instagram-bio-formatter');
test('preserve mode retains whitespace and trailing blank lines',()=>{assert.equal(call('  bio \r\n\r\n').text,'  bio \n\n');assert.equal(call('\n').lines,2)});
test('format modes are explicit and do not collapse ordinary content',()=>{assert.equal(call('a\n\n\n\n b',{mode:'blank-lines'}).text,'a\n\n b');assert.equal(call('a\n\n b',{mode:'blank-lines'}).text,'a\n\n b');assert.equal(call(' a b \n c ',{mode:'trim-lines'}).text,'a b\nc')});
test('Unicode and both 10,000 code-point boundaries are enforced',()=>{assert.equal(call('👩‍💻é').count,5);for(const c of ['x','😀']){assert.equal(call(c.repeat(10000)).count,10000);assert.throws(()=>call(c.repeat(10001)),/10,000/)}});
test('guidance at 149, 150 and 151 is advisory',()=>{for(const [n,p] of [[149,/1 remaining/],[150,/0 remaining/],[151,/1 over/]])assert.match(call('x'.repeat(n)).guidance,p);assert.equal(call('abcdef',{guide:1}).text,'abcdef')});
test('invalid modes, options and guide values reject without output',()=>{assert.throws(()=>call('a',{bad:1}),/Unsupported/);for(const g of ['',0,1.2,10001,Infinity])assert.throws(()=>call('a',{guide:g}),/Guide/);assert.throws(()=>call('a',{mode:'unknown'}),/Unknown/)});
