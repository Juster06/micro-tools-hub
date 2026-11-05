
import {test} from 'node:test';import assert from 'node:assert/strict';import {logic} from '../task18-logic.mjs';const {call}=logic('csv-to-txt');
test('escaped quotes, CRLF inside quoted data and trailing empty fields preserve values',()=>{assert.equal(call('a,b\r\n"x""y","line1\r\nline2"\r\n').output,'x"y | line1\r\nline2');assert.equal(call('a,b\nx,').output,'x | ')});
test('BOM, no-header mode, tab delimiter, column order and literal braces',()=>{assert.equal(call('\ufeffa\tb\nx\ty',{delimiter:'tab',columns:'2,1'}).output,'y | x');assert.equal(call('x,y',{header:false,template:'{{{1}}}={2}'}).output,'{x}=y')});
test('strict parsing rejects malformed input, NUL, duplicate/empty headers and surrogates',()=>{for(const s of ['a\n"x','a\nx"','a\n"x"tail','a,b\nx','a,a\nx,y',',a\nx,y','a\n\0','a\n\ud800'])assert.throws(()=>call(s))});
test('row and column boundaries accept the last permitted record/field',()=>{assert.equal(call('h\n'+Array(10000).fill('x').join('\n')).rows,10000);assert.throws(()=>call('h\n'+Array(10001).fill('x').join('\n')),/10,000/);const head=Array.from({length:100},(_,i)=>'h'+i).join(',');assert.equal(call(head).columns,100);assert.throws(()=>call(head+',extra'),/100 columns/)});
test('UTF-8 input and output bounds measure bytes and reject expansion before append',()=>{const exact='h\n'+'x'.repeat(1048574);assert.equal(call(exact,{template:'{1}'}).bytes,1048574);assert.throws(()=>call(exact+'x'),/1 MiB/);assert.throws(()=>call('h\n'+'😀'.repeat(262144)),/1 MiB/);assert.throws(()=>call('h\n'+'x'.repeat(500000),{template:'{1}'.repeat(5)}),/2 MiB/)});
test('template validation rejects expressions, unavailable/duplicate columns and unmatched braces',()=>{for(const options of [{columns:'1,1'},{columns:'0'},{columns:'3'},{template:'{constructor}'},{template:'{1+1}'},{template:'{1'},{template:'}'},{template:'x'.repeat(4097)}])assert.throws(()=>call('a,b\nx,y',options))});
test('blank lines and empty strings are explicit records, never silently dropped',()=>{assert.equal(call('h\n\n').rows,1);assert.equal(call('""',{header:false}).rows,1);assert.equal(call('h\n""').output,'')});
test('preview is bounded while complete output is retained and markup is inert data',()=>{const r=call('h\n'+Array(25).fill('<script>'+ 'x'.repeat(1000)).join('\n'));assert.equal(r.rows,25);assert.equal(r.preview.split('\n').length,20);assert.ok(r.preview.length<11000);assert.ok(r.output.length>25000)});


test('expanded output accepts exactly 2 MiB and rejects the next byte; delimiter keys are explicit',()=>{
 const input='h\n'+'x'.repeat(1048574);assert.equal(call(input,{template:'{1}{1}xxxx'}).bytes,2097152);assert.throws(()=>call(input,{template:'{1}{1}xxxxx'}),/2 MiB/);for(const delimiter of ['constructor','toString','__proto__'])assert.throws(()=>call('a\nx',{delimiter}),/delimiter/);
});
