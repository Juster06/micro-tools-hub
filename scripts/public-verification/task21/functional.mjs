import {test,before,after} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {parse} from '../../../tests/vendor/acorn-8.19.0.mjs';
import {start,source,run,click,set,wait,widths,ORIGIN} from './browser.mjs';
let b;before(async()=>{b=await start('functional');});after(async()=>b?.close());
const examples={'hashtag-counter':['Hello #One #one #two','#One #one #two'],'html-formatter':['<p>Hello</p>','<p>Hello</p>'],'css-minifier':['a { color: red; }','a{color:red}'],'javascript-minifier':['let x = 1;','let x=1;'],'html-to-markdown':['<h1>Hello</h1><p>World</p>','# Hello\n\nWorld\n'],'html-previewer':['<h1>Hello</h1><p>World</p>','<h1>Hello</h1><p>World</p>']};
const success=r=>assert.equal(r.error,'',r.error);
async function page(id){await b.load(source(id));}
for(const[id,[input,expected]]of Object.entries(examples))test(id+': real Worker result, copy/download/reset, native keyboard and responsive layout',async()=>{
 await page(id);const r=await run(b,input);success(r);assert.equal(r.text,expected);
 await click(b,'copyBtn');await wait(b,'window.__edbClipboard.value!==null');assert.equal(await b.evaluate('__edbClipboard.value'),expected);
 await click(b,'downloadBtn');assert.equal(await b.evaluate('__edbDownloads.length'),1);assert.equal(await b.evaluate('__edbDownloadBlob.type'),'text/plain;charset=utf-8');
 const downloaded=await b.evaluate('__edbDownloadBlob.text()');if(id==='html-previewer'){assert.ok(downloaded.includes(expected));assert.ok(downloaded.includes("default-src 'none'"));}else assert.equal(downloaded,expected);
 await widths(b);await click(b,'clearBtn');assert.equal(await b.evaluate('toolInput.value'), '');assert.equal(await b.evaluate('toolOutput.value'),'');assert.equal(await b.evaluate('document.activeElement.id'),'toolInput');assert.equal(await b.evaluate('copyBtn.disabled'),true);
 await set(b,'toolInput',input);await b.evaluate('runBtn.focus();true');await b.call('Input.dispatchKeyEvent',{type:'keyDown',key:'Enter',code:'Enter',windowsVirtualKeyCode:13,text:'\r'});await b.call('Input.dispatchKeyEvent',{type:'keyUp',key:'Enter',code:'Enter',windowsVirtualKeyCode:13});await wait(b,"toolStatus.textContent==='Complete.'");assert.equal(await b.evaluate('toolOutput.value'),expected);
});
test('hashtag-counter: complete caption, URL/fragments/C#, punctuation and duplicate policy',async()=>{
 await page('hashtag-counter');const r=await run(b,'C# C#code word#no /#fragment https://example.invalid/a?#no www.example.invalid/#no (#Yes), 😀#世界 #_tag #2tag #Yes');success(r);assert.equal(r.text,'#Yes #世界 #_tag #2tag #Yes');assert.match(r.summary,/5 occurrences · 4 unique tags · 1 repeated tags.*#Yes ×2/);
});
test('hashtag-counter: NFC, exact/lowercase policies and documented non-full-case-folding',async()=>{
 await page('hashtag-counter');let r=await run(b,'#cafe\u0301 #café #CAFÉ #Straße #STRASSE');success(r);assert.equal(r.text,'#café #café #CAFÉ #Straße #STRASSE');assert.match(r.summary,/5 occurrences · 3 unique/);r=await run(b,'#A #a',{casePolicy:'exact'});assert.match(r.summary,/2 unique/);await click(b,'clearBtn');assert.equal(await b.evaluate('casePolicy.value'),'fold');
});
test('hashtag-counter: invalid Unicode, tag/input/occurrence boundaries and no-tag result',async()=>{
 await page('hashtag-counter');for(const value of ['\udfff','#'+'界'.repeat(101),'x'.repeat(100001),'#a '.repeat(10001)]){const r=await run(b,value);assert.ok(r.error);assert.equal(r.text,'');}
 let r=await run(b,'#'+'界'.repeat(100));success(r);assert.match(r.summary,/1 occurrences/);r=await run(b,'C# ##no #😀 plain');success(r);assert.equal(r.text,'');
});
test('html-formatter: indentation and preferred width options change structured formatting',async()=>{
 await page('html-formatter');const input='<div first="long-long-long-value" second="another-long-value"><span>Hello</span></div>';
 const wide=await run(b,input,{indent:'2',width:'120'}),narrow=await run(b,input,{indent:'2',width:'40'}),four=await run(b,input,{indent:'4',width:'40'});for(const r of[wide,narrow,four])success(r);assert.notEqual(wide.text,narrow.text);assert.notEqual(narrow.text,four.text);assert.match(four.text,/\n {4}/);await click(b,'clearBtn');assert.equal(await b.evaluate('indent.value+":"+width.value'),'2:80');
});
test('html-formatter: meaningful inline/pre whitespace retained; content-changing script case refuses and never executes',async()=>{
 await page('html-formatter');for(const input of ['<p>Hello <strong>世界</strong>!</p>','<div><span>a</span><span>b</span></div>','<pre> A\n  B </pre>']){const r=await run(b,input);success(r);if(input.startsWith('<pre>')){const texts=await b.evaluate(`[${JSON.stringify(input)},${JSON.stringify(r.text)}].map(s=>new DOMParser().parseFromString(s,'text/html').querySelector('pre').textContent)`);assert.deepEqual(texts,[' A\n  B ',' A\n  B ']);}else assert.equal(r.text,input);}
 await b.evaluate('window.__submittedScriptExecuted=0;true');const r=await run(b,'<script>globalThis.__submittedScriptExecuted=99</script><p>&amp;</p>');assert.match(r.error,/change parsed content/);assert.equal(r.text,'');assert.equal(await b.evaluate('__submittedScriptExecuted'),0);assert.equal(await b.evaluate('document.querySelectorAll("script[data-untrusted]").length'),0);
});
test('html-formatter: malformed, nesting/byte overflow fail; bounded HTML5 repair is disclosed',async()=>{
 await page('html-formatter');for(const input of ['<div '.repeat(5000),'<div>'.repeat(66)+'x'+'</div>'.repeat(66),'界'.repeat(10923)])assert.ok((await run(b,input)).error);
 const r=await run(b,'<div><');success(r);assert.ok(r.text.includes('<'));assert.match(r.warning,/HTML5 normalization/);
});
test('css-minifier: independent compact expected string, ordinary/license comments and byte savings',async()=>{
 await page('css-minifier');const input='/*comment*/ a { color: red; padding: 0px 0px; } a { color: blue; }';const r=await run(b,input);success(r);assert.equal(r.text,'a{color:red;padding:0px 0px}a{color:blue}');assert.equal(r.summary,`${Buffer.byteLength(input)} input bytes → ${Buffer.byteLength(r.text)} output bytes (saved ${Buffer.byteLength(input)-Buffer.byteLength(r.text)} bytes).`);
 const licence=await run(b,'/*! licence */ .x { content: "a; } b"; --a: red/**/blue; }');success(licence);assert.match(licence.text,/\/\*! licence \*\//);assert.match(licence.text,/"a; } b"/);assert.match(licence.text,/red\/\*\*\/blue/);
});
test('css-minifier: escapes/custom properties/modern media-range have independently expected browser styles',async()=>{
 await page('css-minifier');const input=':root { --edb-gap: 3px; } @media(width > 20px){.edb-check {color:rgb(12,34,56);padding:calc(1px + var(--edb-gap));margin:0 0 2px} .edb-check::before {content:"\\41 ";}}';const r=await run(b,input);success(r);assert.match(r.text,/content:"A"/);
 const result=await b.evaluate(`(()=>{const read=css=>{const style=document.createElement('style');style.textContent=css;const node=document.createElement('div');node.className='edb-check';document.head.append(style);document.body.append(node);const s=getComputedStyle(node),v={color:s.color,padding:s.padding,margin:s.margin,content:getComputedStyle(node,'::before').content};style.remove();node.remove();return v;};return [${JSON.stringify(input)},${JSON.stringify(r.text)}].map(read)})()`);
 assert.deepEqual(result,[{color:'rgb(12, 34, 56)',padding:'4px',margin:'0px 0px 2px',content:'"A"'},{color:'rgb(12, 34, 56)',padding:'4px',margin:'0px 0px 2px',content:'"A"'}]);
});
test('css-minifier: layer/nesting/property syntax, UTF8 charset ordering and invalid cases',async()=>{
 await page('css-minifier');for(const input of ['@layer base { .x { & .y { color:red; } } }','@property --x { syntax: "<length>"; inherits: false; initial-value: 0px; }','@charset "UTF-8"; /*! licence */ a { color:red; }']){const r=await run(b,input);success(r);if(input.startsWith('@charset'))assert.match(r.text,/^@charset "UTF-8";/);}
 for(const input of ['a{content:"bad','/* unclosed','a{background:url(x','a{color:red]','a'.repeat(32769),'@charset "ISO-8859-1";a{color:red}'])assert.ok((await run(b,input)).error);
});
function strip(n){if(Array.isArray(n))return n.map(strip);if(n&&typeof n==='object')return Object.fromEntries(Object.entries(n).filter(([k])=>!['start','end','raw'].includes(k)).map(([k,v])=>[k,strip(v)]));return n;}
test('javascript-minifier: independent AST equality for ASI, regex, template, private fields, Unicode and bigint',async()=>{
 await page('javascript-minifier');for(const input of ['function f(){return\n1;}','const x=/a+b/giu;const s=`hello ${2 + 3}`;','class X { #x=1; f(){ return this?.#x ?? 0; } }','const n=123n; const text="café 世界";']){const r=await run(b,input);success(r);assert.deepEqual(strip(parse(r.text,{ecmaVersion:'latest'})),strip(parse(input,{ecmaVersion:'latest'})));assert.match(r.summary,new RegExp('^'+Buffer.byteLength(input)+' input bytes → '+Buffer.byteLength(r.text)+' output bytes'));}
});
test('javascript-minifier: script/module options, retained names/licence and submitted throw/loop never execute',async()=>{
 await page('javascript-minifier');const r=await run(b,'/*! licence */ export function longName(value) { return value + 0; }',{toolMode:'module'});success(r);assert.match(r.text,/licence/);assert.match(r.text,/longName\(value\)/);assert.match(r.text,/value\+0/);
 for(const input of ['throw new Error("submitted code must remain text");','while (true) {}','globalThis.__submittedScriptExecuted=99;']){const out=await run(b,input,{toolMode:'script'});success(out);assert.deepEqual(strip(parse(out.text,{ecmaVersion:'latest'})),strip(parse(input,{ecmaVersion:'latest'})));}assert.equal(await b.evaluate('globalThis.__submittedScriptExecuted??0'),0);
});
test('javascript-minifier: malformed/unsupported syntax and limits clear stale output',async()=>{
 await page('javascript-minifier');for(const input of ['function (','const x: number = 1;','const x = <div/>;','x'.repeat(32769),'const x='+'['.repeat(70)+'1'+']'.repeat(70)+';']){const r=await run(b,input);assert.ok(r.error);assert.equal(r.text,'');assert.equal(await b.evaluate('copyBtn.disabled'),true);}
});
test('html-to-markdown: independently expected headings, paragraph, list, link, emphasis and Unicode',async()=>{
 await page('html-to-markdown');const r=await run(b,'<h1>Title 世界</h1><p>A <strong>bold</strong> <em>word</em> &amp; <a href="https://example.invalid/a(b)">link</a>.</p><ul><li>one</li><li>two</li></ul>');success(r);assert.equal(r.text,'# Title 世界\n\nA **bold** *word* & [link](https://example.invalid/a%28b%29).\n\n- one\n- two\n');
});
test('html-to-markdown: code fences preserve internal whitespace/backticks; unsafe input is inert text',async()=>{
 await page('html-to-markdown');let r=await run(b,'<pre><code>```\n  line\n```</code></pre>');success(r);assert.equal(r.text,'````\n```\n  line\n```\n````\n');
 await b.evaluate('window.__submittedScriptExecuted=0;true');r=await run(b,'<script>globalThis.__submittedScriptExecuted=99</script><style>p{color:red}</style><svg><text>foreign</text></svg><p>safe <a href="jav&#x61;script:alert(1)">bad</a></p>');success(r);assert.equal(r.text,'safe bad\n');assert.equal(await b.evaluate('__submittedScriptExecuted'),0);assert.match(r.warning,/omitted/);
});
test('html-to-markdown: unsupported table/image structures are disclosed and depth/node limits refuse',async()=>{
 await page('html-to-markdown');const r=await run(b,'<table><tr><td>cell</td></tr></table><img src="https://example.invalid/not-loaded" alt="alternative">');success(r);assert.match(r.text,/cellalternative/);assert.match(r.warning,/Unsupported structures/);for(const input of ['<p>x</p>'.repeat(2200),'<div>'.repeat(66)+'x'+'</div>'.repeat(66)])assert.ok((await run(b,input)).error);
});
test('html-previewer: structural sanitized source, sandbox/CSP, validation and reset',async()=>{
 await page('html-previewer');const r=await run(b,'<h1 class="removed">Hello</h1><p>Safe <strong>text</strong></p><a href="https://example.invalid/">plain link</a>');success(r);assert.equal(r.text,'<h1>Hello</h1><p>Safe <strong>text</strong></p>plain link');assert.equal(await b.evaluate('safePreview.getAttribute("sandbox")'),'');assert.equal(await b.evaluate('safePreview.contentDocument'),null);assert.ok(await b.evaluate('safePreview.srcdoc.includes("default-src \'none\'")'));
 await click(b,'clearBtn');assert.equal(await b.evaluate('safePreview.getAttribute("srcdoc")'),'');for(const input of ['','<div>'.repeat(66)+'x'+'</div>'.repeat(66),'a'.repeat(32769)])assert.ok((await run(b,input)).error);
});
test('public homepage:74 visible distinct cards, exact canonical routes, search and real tool navigation',async()=>{
 await b.load(ORIGIN+'/');const cards=await b.evaluate("Array.from(document.querySelectorAll('a[data-title]')).map(a=>({href:a.getAttribute('href'),visible:!!a.getClientRects().length&&getComputedStyle(a).visibility!=='hidden'}))");assert.equal(cards.length,74);assert.equal(new Set(cards.map(c=>c.href)).size,74);assert.ok(cards.every(c=>c.visible));const registry=JSON.parse(fs.readFileSync(new URL('../../../TOOL_REGISTRY.json',import.meta.url),'utf8'));assert.deepEqual(cards.map(c=>c.href).sort(),registry.tools.filter(t=>['TESTED','RELEASED'].includes(t.status)).map(t=>t.directory_path+'/index.html').sort());
 for(const id of Object.keys(examples)){await b.load(source(id));await b.evaluate("document.querySelector('header a').click();true");await wait(b,"location.pathname==='/'||location.pathname==='/index.html'");await wait(b,"document.querySelectorAll('a[data-title]').length===74");await set(b,'toolSearch',registry.tools.find(t=>t.id===id).name);await wait(b,`!document.querySelector('a[data-tool-id="${id}"]').hidden`);await click(b,'clearSearch');assert.equal(await b.evaluate("Array.from(document.querySelectorAll('a[data-title]')).filter(a=>!a.hidden).length"),74);await b.evaluate(`document.querySelector('a[data-tool-id="${id}"]').click();true`);await wait(b,`location.pathname==='/${id}/index.html'&&!!window.EDB_TOOL`);}
});
