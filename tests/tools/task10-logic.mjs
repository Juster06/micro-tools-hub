import {test} from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import fs from 'node:fs';
import {fileURLToPath} from 'node:url';
import {loadLogic} from '../../scripts/tool-tests/runner.mjs';

export function logicSuite(id){
 const adapter=loadLogic(fileURLToPath(new URL(`../../${id}/index.html`,import.meta.url)));
 const ctx=adapter.context;
 const fixtures=JSON.parse(fs.readFileSync(new URL(`${id}/logic.cases.json`,import.meta.url),'utf8')).cases;
 const seed=fixtures[0];
 function call(method,...args){ctx.__args=args;return vm.runInContext(`EDB_TOOL.${method}(...__args)`,ctx,{timeout:1000});}
 test(`${id}: independently asserted fixture table`,()=>{for(const c of fixtures){if(c.error)assert.throws(()=>call('run',c.input,c.options),e=>e.message.includes(c.error),c.id);else assert.equal(call('run',c.input,c.options),c.expected,c.id);}});
 test('non-string input and invalid setting containers fail without coercion',()=>{for(const x of [null,undefined,1,true,{},[]])assert.throws(()=>call('run',x,seed.options),/Input must be a string/);for(const x of [null,[],false,1,'x'])assert.throws(()=>call('run',seed.input,x),/Options must be an object/);assert.throws(()=>call('run',seed.input,{...seed.options,unknown:true}),/Unsupported setting/);});
 test('frozen input settings and entropy remain unchanged across repeated calls',()=>{const options=Object.freeze({...seed.options,...(seed.options.entropy?{entropy:Object.freeze([...seed.options.entropy])}:{})});const before=JSON.stringify(options);assert.equal(call('run',seed.input,options),call('run',seed.input,options));assert.equal(JSON.stringify(options),before);});
 test('raw size cap applies before trimming and counts UTF-16 units',()=>{const limit=ctx.EDB_TOOL.limit;assert.throws(()=>call('run',' '.repeat(limit+1),seed.options),/UTF-16/);assert.throws(()=>call('run','😀'.repeat(limit),seed.options),/UTF-16/);});
 if(id==='countdown-timer'){
  test('deadline catch-up, pause/resume and completion preserve fractional milliseconds',()=>{const start=call('start','00:00:10',1000);Object.freeze(start);const paused=call('pause',start,2250);assert.equal(paused.remainingMs,8750);assert.equal(paused.status,'paused');assert.equal(paused.deadline,null);assert.equal(call('format',paused.remainingMs),'00:00:09');assert.equal(call('tick',paused,500000).remainingMs,8750);const resumed=call('resume',paused,100000);assert.equal(resumed.deadline,108750);assert.equal(call('tick',resumed,108749).remainingMs,1);const end=call('tick',resumed,999999);assert.equal(end.remainingMs,0);assert.equal(end.status,'completed');assert.equal(end.deadline,null);assert.equal(start.remainingMs,10000);});
  test('pause at deadline completes and running/completed states cannot resume',()=>{const s=call('start','00:00:01',100);assert.equal(call('pause',s,1100).status,'completed');assert.throws(()=>call('resume',s,200),/paused/);assert.throws(()=>call('resume',call('tick',s,1100),1200),/paused/);});
  test('24-hour endpoint and wall-clock rollback stay bounded',()=>{const s=call('start','24:00:00',1000);assert.equal(call('tick',s,0).remainingMs,86400000);assert.equal(call('tick',s,86401000).status,'completed');for(const now of [-1,NaN,Infinity,Number.MAX_SAFE_INTEGER])assert.throws(()=>call('start','00:00:01',now),/clock/);for(const state of [null,{}, {status:'running',totalMs:1000,remainingMs:1001,deadline:2000}])assert.throws(()=>call('tick',state,0),/state/);for(const value of [-1,NaN,Infinity,86400001])assert.throws(()=>call('format',value),/remaining/);});
 }else if(id==='random-name-picker'||id==='secure-random-number-generator'){
  const numeric=id==='secure-random-number-generator',input=numeric?'0':'Ada\nBob\nC',options=numeric?{b:'9'}:{};
  test('missing and throwing cryptographic providers fail with no fallback',()=>{for(const provider of [undefined,{}, {getRandomValues(){throw Error('provider failed');}}])assert.throws(()=>call('generate',input,options,provider),/cryptographic|No fallback/);});
  test('invalid inputs consume no cryptographic randomness',()=>{let calls=0;const provider={getRandomValues(a){calls++;return a;}};assert.throws(()=>call('generate','',options,provider));assert.equal(calls,0);assert.throws(()=>call('generate',input,{...options,entropy:[0]},provider),/Unsupported/);assert.equal(calls,0);});
  test('rejection consumes fresh words and never reduces a rejected value modulo range',()=>{const values=numeric?[[4294967295,4294967295],[0,7]]:[[4294967295],[2]];let count=0;const provider={getRandomValues(a){a.set(values[count++]);return a;}};assert.equal(call('generate',input,options,provider),numeric?'7':'C');assert.equal(count,2);});
  test('malformed, sparse and exhausted test entropy fail instead of silently supplying zero',()=>{for(const entropy of [new Array(2),[-1],[NaN],[4294967296],[1.5]])assert.throws(()=>call('run',input,{...options,entropy}),/unsigned/);assert.throws(()=>call('run',input,{...options,entropy:[]}),/exhausted/);});
  test('128 rejected samples abort the entire result with a bounded provider cost',()=>{let calls=0;const provider={getRandomValues(a){calls++;a.fill(4294967295);return a;}};assert.throws(()=>call('generate',input,options,provider),/rejection limit/);assert.equal(calls,128);});
  if(numeric)test('every safe-integer endpoint uses exact BigInt range arithmetic',()=>{for(const [min,max] of [[-9007199254740991n,9007199254740991n],[-9007199254740991n,-1n],[0n,9007199254740991n]]){const span=max-min+1n;for(const offset of [0n,span-1n]){const entropy=[Number(offset>>32n),Number(offset&4294967295n)];assert.equal(call('run',String(min),{b:String(max),entropy}),String(min+offset));}}});
  else test('10,000-entry pool and 100-draw batch remain bounded without mutation',()=>{const input=Array.from({length:10000},(_,i)=>'N'+i).join('\n');const opts={count:'100',entropy:Array(100).fill(0)};const result=call('run',input,opts).split('\n');assert.equal(result.length,100);assert.equal(new Set(result).size,100);assert.equal(result[99],'N99');});
 }else if(id==='hashtag-organizer'){
  test('counts reflect all tokens, canonical equivalents and first retained spelling',()=>{const result=call('analyze','#Café cafe\u0301 #CAFÉ 中文 中文');assert.equal(result.text,'#Café #中文');assert.equal(result.inputCount,5);assert.equal(result.kept,2);assert.equal(result.removed,3);});
  test('Unicode lowercase is disclosed rather than silently applying full case-folding',()=>{assert.equal(call('run','Straße STRASSE'), '#Straße #STRASSE');assert.equal(call('run','I İ i'), '#I #İ');});
  test('astral letters count as Unicode code points at tag boundary',()=>{const tag='𐐀'.repeat(100);assert.equal(call('run',tag),'#'+tag);assert.throws(()=>call('run',tag+'𐐀'),/100 Unicode/);});
 }else if(id==='profit-margin-calculator'){
  test('negative zero and native binary rounding follow the documented numeric contract',()=>{assert.match(call('run','-0',{b:'0'}),/^Profit: 0.00/);assert.match(call('run','1.005',{b:'1.005'}),/Cost: 1.00/);assert.match(call('run','1e12',{b:'1e12'}),/Revenue: 1000000000000.00/);});
  test('invalid precision and second-field numeric syntax are rejected',()=>{for(const precision of ['3',2,null])assert.throws(()=>call('run','1',{b:'2',precision}),/Unsupported/);for(const b of ['0x10','2x','1e-400','1'.repeat(65)])assert.throws(()=>call('run','1',{b}));});
 }else if(id==='date-difference-calculator'){
  test('calendar arithmetic is independent of process timezone and short-year Date quirks',()=>{assert.match(call('run','0099-12-31',{b:'0100-01-01'}),/^Days: 1\n/);assert.match(call('run','2026-10-24',{b:'2026-10-26'}),/^Days: 2\n/);assert.throws(()=>call('run','2000-01-01',{b:'2001-02-29'}),/Gregorian/);});
  test('unsupported counting settings and invalid end date fail before producing output',()=>{assert.throws(()=>call('run','2000-01-01',{b:'',inclusive:false}),/end date/);assert.throws(()=>call('run','2000-01-01',{b:'2000-01-02',inclusive:'yes'}),/Unsupported/);});
 }
}
