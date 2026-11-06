import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {Worker} from 'node:worker_threads';
import vm from 'node:vm';
const context=vm.createContext({window:{}});vm.runInContext(fs.readFileSync(new URL('../../../assets/vendor/task22/markdown-source.js',import.meta.url),'utf8'),context,{timeout:1000});const code=context.window.EDB_TASK22_WORKER_SOURCE;
export async function run(input){const started=performance.now();return new Promise((resolve,reject)=>{const w=new Worker(`const{parentPort}=require('node:worker_threads');globalThis.self=globalThis;self.postMessage=r=>parentPort.postMessage(r);${code};parentPort.on('message',data=>self.onmessage({data}));`,{eval:true,resourceLimits:{maxOldGenerationSizeMb:96,maxYoungGenerationSizeMb:16,stackSizeMb:4}});const timer=setTimeout(()=>{w.terminate();reject(Error('Deadline exceeded'));},2000);w.once('message',r=>{clearTimeout(timer);w.terminate();resolve({...r,elapsed:performance.now()-started});});w.once('error',e=>{clearTimeout(timer);w.terminate();reject(e);});w.postMessage({input});});}
for(const [name,input,expected]of [
 ['headings','# Hello','<h1>Hello</h1>'],['emphasis','**bold** and *soft*','<p><strong>bold</strong> and <em>soft</em></p>'],['code','```js\n<x>\n```','<pre><code>&lt;x&gt;\n</code></pre>'],['Unicode','café 世界 😀','<p>café 世界 😀</p>'],['patched whitespace advisory','x\n\t\v\n','<p>x\n\t\v</p>']
])test(name+' independently expected HTML',async()=>{const r=await run(input);assert.equal(r.ok,true,r.error);assert.equal(r.text,expected+String.fromCharCode(10));});
for(const[name,input]of [['byte limit','😀'.repeat(8193)],['ASCII limit','x'.repeat(32769)],['node limit','- x\n'.repeat(2500)],['nesting','> '.repeat(80)+'x'],['output expansion','<'.repeat(32768)]])test(name+' rejects without partial output',async()=>{const r=await run(input);assert.equal(r.ok,false);assert.equal(r.text,undefined);assert.match(r.error,/exceed|complexity/i);});
for(const[name,input]of [['near limit','a'.repeat(32768)],['unbalanced brackets','['.repeat(12000)+'x'],['malformed foreign HTML','<svg><foreignObject><script>alert(1)</svg>'],['table','| A | B |\n|---|---|\n|1|2|']])test(name+' completes bounded conversion',async()=>{const r=await run(input);assert.equal(r.ok,true,r.error);assert.ok(Buffer.byteLength(r.download)<=131072);assert.ok(r.elapsed<2000);});
for(const [name,input,expected]of [
 ['paragraph escaping','a & b < c','<p>a &amp; b &lt; c</p>\n'],
 ['unordered list','- one\n- two','<ul>\n<li>one</li>\n<li>two</li>\n</ul>\n'],
 ['ordered list','1. one\n2. two','<ol>\n<li>one</li>\n<li>two</li>\n</ol>\n'],
 ['blockquote','> quote','<blockquote>\n<p>quote</p>\n</blockquote>\n'],
 ['inline code','`<x>`','<p><code>&lt;x&gt;</code></p>\n'],
 ['table','| A | B |\n|---|---|\n|1|2|','<table>\n<thead>\n<tr>\n<th>A</th>\n<th>B</th>\n</tr>\n</thead>\n<tbody><tr>\n<td>1</td>\n<td>2</td>\n</tr>\n</tbody></table>\n']
])test(name+' agrees with independent expected structure',async()=>{const r=await run(input);assert.equal(r.ok,true,r.error);assert.equal(r.text,expected);});
test('only reviewed HTTP(S) URLs survive export; all preview links are inert',async()=>{
 const r=await run('[ok](https://example.invalid/a?x=1&y=2) [bad](javascript:alert) [relative](/x) [credentials](https://u:p@example.invalid/) [data](data:text/html,x)');assert.ok(r.ok);assert.equal((r.text.match(/<a /g)||[]).length,1);assert.match(r.text,/x=1&amp;y=2/);assert.doesNotMatch(r.preview,/<a\b|javascript:|data:text/);
});
test('raw HTML, handlers, frames, SVG and remote images cannot become active markup',async()=>{
 const r=await run('<script>alert(1)</script>\n\n<svg onload="bad()"></svg>\n\n![alt](https://example.invalid/a)\n\n<iframe src="https://example.invalid/"></iframe>');assert.ok(r.ok);assert.doesNotMatch(r.text,/<(?:script|svg|img|iframe)\b/i);assert.match(r.text,/&lt;script&gt;/);assert.ok(r.text.includes('alt'));
});
