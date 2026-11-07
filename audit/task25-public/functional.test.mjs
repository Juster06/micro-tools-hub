import {test,before,after} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {ORIGIN,source,start,set,click,run,wait,checkRecord} from './public.mjs';
import {observeWorker} from './worker-probe.mjs';

const ids=['word-frequency-analyzer','unicode-inspector','ipv4-subnet-calculator','batch-filename-planner','file-byte-comparator','css-gradient-generator'];
const [word,unicode,ip,filename,file,gradient] = ids;
const stops = '#6366F1 0%\n#22D3EE 100%';
let b;
const record={result:'IN_PROGRESS',deployment_commit:'c127f856cbd97497412ec35ed66b3b1a58c4b2dc',started_at:new Date().toISOString(),scope:'Fresh interactions on public HTTPS. Production responses are unchanged. Clipboard and downloads are captured in memory. One real Worker is instrumented through Chromium DevTools to observe native Blob read sizes and concurrency.',checks:[]};
before(async()=>{b=await start();record.browser=b.version;});
after(async()=>{
  try {
    if(b){await b.close();checkRecord(b.record);record.console_errors=b.record.console_errors;record.unexpected_javascript_errors=b.record.exceptions.length;record.unexpected_dependencies=b.record.unexpected_dependencies;record.input_transport_requests=b.record.input_transport_requests;}
    record.result=record.checks.length===43&&record.checks.every(c=>c.result==='PASS')?'PASS':'FAIL';
    assert.equal(record.result,'PASS');
  } catch(error) {
    record.result='FAIL';
    throw error;
  } finally {
    record.completed_at=new Date().toISOString();
    fs.writeFileSync(new URL('./public-functional-verification.json',import.meta.url),JSON.stringify(record,null,2)+'\n');
  }
});
function check(id,name,fn){
  test(`${id}: ${name}`,async()=>{
    const row={tool_id:id,check:name,checked_at:new Date().toISOString(),result:'FAIL'};
    try{await b.load(id==='homepage'?ORIGIN+'/':source(id));const result=await fn();if(result)row.observed=result;row.result='PASS';}
    finally{record.checks.push(row);}
  });
}
async function output(input, options={}){const r=await run(b,input,options);assert.equal(r.error,'');assert.equal(r.status,'Complete.');return r.text;}
async function invalid(input, options, pattern){const r=await run(b,input,options);assert.match(r.error,pattern);assert.equal(r.text,'');assert.equal(await b.evaluate('copyBtn.disabled && downloadBtn.disabled'),true);}
async function selectFiles(id, expressions){await b.evaluate(`(() => {
  const list=new DataTransfer();for(const item of [${expressions.join(',')}])list.items.add(item);
  const el=document.getElementById(${JSON.stringify(id)});el.files=list.files;el.dispatchEvent(new Event('change',{bubbles:true}));return true;
})()`);}
async function compare(left,right){await selectFiles('toolInput',[left]);await selectFiles('secondFile',[right]);await click(b,'runBtn');await wait(b,"toolStatus.textContent==='Complete.'");return b.evaluate('toolOutput.value');}
function frequencies(total,unique,rows=''){return `Occurrences: ${total}\nUnique words: ${unique}\nWord\tCount${rows?'\n'+rows:''}`;}

check(word,'known Unicode tokens and punctuation boundaries',async()=>{
  const text=await output("é é can’t can't well-known 🙂 中文",{normalization:'NFC'});
  assert.equal(text,frequencies(7,6,"é\t2\ncan't\t1\ncan’t\t1\nknown\t1\nwell\t1\n中文\t1"));
  return {occurrences:7,unique:6};
});
check(word,'case-sensitive and native lowercase counts',async()=>{
  assert.equal(await output('Dog DOG dog dog'),frequencies(4,3,'dog\t2\nDOG\t1\nDog\t1'));
  assert.equal(await output('Dog DOG dog dog',{caseMode:'lowercase'}),frequencies(4,1,'dog\t4'));
});
check(word,'NFC opt-in and literal spelling',async()=>{
  assert.equal(await output('é é é'),frequencies(3,2,'é\t2\né\t1'));
  assert.equal(await output('é é é',{normalization:'NFC'}),frequencies(3,1,'é\t3'));
});
check(word,'alphabetical, frequency and least-first ordering',async()=>{
  const input='z z b a';assert.equal(await output(input),frequencies(4,3,'z\t2\na\t1\nb\t1'));
  assert.equal(await output(input,{order:'alphabetical'}),frequencies(4,3,'a\t1\nb\t1\nz\t2'));
  assert.equal(await output(input,{order:'least'}),frequencies(4,3,'a\t1\nb\t1\nz\t2'));
  assert.equal(await output(''),frequencies(0,0));
});
check(word,'100,000 input units and 20,000 tokens at the boundary',async()=>{
  assert.equal(await output('a '.repeat(20000).padEnd(100000,' ')),frequencies(20000,1,'a\t20000'));
  await invalid(' '.repeat(100001),{},/100,000 UTF-16/);await invalid('a '.repeat(20001),{},/20,000 word tokens/);await invalid('a'.repeat(257),{},/256 UTF-16/);
});
check(word,'ranking and byte budgets disclose omissions',async()=>{
  assert.match(await output(Array.from({length:1001},(_,i)=>'w'+i).join(' ')),/Unique words: 1001[\s\S]*Showing 1000 of 1001/);
  const report=await output(Array.from({length:390},(_,i)=>'界'.repeat(250)+i).join(' '));
  assert.ok(Buffer.byteLength(report)<=256*1024);assert.match(report,/Showing \d+ of 390 ranked words/);
});

check(unicode,'known supplementary, combining and emoji cluster boundaries',async()=>{
  const text=await output('👩‍💻é😀');
  for(const expected of ['Code points: 6','UTF-16 units: 9','UTF-8 bytes: 18','Grapheme clusters: 3',
      '0 | U+1F469 | D83D DC69 | F0 9F 91 A9 | Symbol | cluster start',
      '2 | U+200D | 200D | E2 80 8D | Format character | within cluster',
      '6 | U+0301 | 0301 | CC 81 | Combining mark | within cluster',
      '7 | U+1F600 | D83D DE00 | F0 9F 98 80 | Symbol | cluster start'])assert.ok(text.includes(expected),expected);
  return {code_points:6,utf16_units:9,utf8_bytes:18,clusters:3};
});
check(unicode,'character categories and normalization without guessed names',async()=>{
  const text=await output('Ａé\u202e\ue000');
  for(const term of ['U+FF21','Letter','NFC: changed','NFKC: changed','U+202E','Format character','U+E000','Private use'])assert.ok(text.includes(term));
  assert.ok(!text.includes('\u202e')&&!text.includes('\ue000'));assert.match(await b.evaluate('inputHelp.textContent'),/Descriptions are character categories/);
});
check(unicode,'lone surrogates and unavailable Segmenter are explicitly labeled',async()=>{
  const lone=await output('\ud800');assert.match(lone,/U\+D800 .* N\/A \| Lone surrogate/);assert.match(lone,/UTF-8 bytes: Unavailable/);
  await b.evaluate('Intl.Segmenter=undefined;true');const fallback=await output('👩‍💻');assert.match(fallback,/Code points: 3/);assert.match(fallback,/Grapheme clusters: Unavailable/);
});
check(unicode,'8,192-unit input, capped rows and byte report',async()=>{
  const text=await output('a'.repeat(8192));assert.match(text,/Code points: 8192/);assert.match(text,/Showing \d+ of 8192 diagnostic rows/);assert.ok(Buffer.byteLength(text)<=128*1024);
  await invalid('a'.repeat(8193),{},/8,192 UTF-16/);
});

check(ip,'independent /24 mask, network, broadcast, range and counts',async()=>{
  const text=await output('192.0.2.130',{prefix:'24'});
  for(const value of ['Subnet mask: 255.255.255.0','Network address: 192.0.2.0','Broadcast address: 192.0.2.255','Address range: 192.0.2.0 – 192.0.2.255','Total addresses: 256','Conventional host slots: 254'])assert.ok(text.includes(value),value);
  return {mask:'255.255.255.0',network:'192.0.2.0',broadcast:'192.0.2.255',total:256};
});
check(ip,'/0 exact unsigned address range and count',async()=>{
  const text=await output('255.255.255.255',{prefix:'0'});assert.match(text,/Subnet mask: 0\.0\.0\.0/);assert.match(text,/Address range: 0\.0\.0\.0 – 255\.255\.255\.255/);assert.match(text,/Total addresses: 4294967296/);
});
check(ip,'/31 point-to-point and /32 host-route boundaries',async()=>{
  const p31=await output('192.0.2.131',{prefix:'31'});assert.match(p31,/Subnet mask: 255\.255\.255\.254/);assert.match(p31,/192\.0\.2\.130 – 192\.0\.2\.131/);assert.match(p31,/Total addresses: 2/);assert.match(p31,/Broadcast address: None[\s\S]*RFC 3021/);
  const p32=await output('255.255.255.255',{prefix:'32'});assert.match(p32,/Subnet mask: 255\.255\.255\.255/);assert.match(p32,/Total addresses: 1\nSingle address/);assert.match(p32,/Limited broadcast/);
});
check(ip,'reject invalid addresses and prefixes without retaining output',async()=>{
  for(const x of ['256.0.0.1','01.2.3.4','0x7f.0.0.1','127.1','１.2.3.4',''])await invalid(x,{prefix:'24'},/four decimal IPv4 octets/);
  for(const prefix of ['33','-1','01','1.5','/24'])await invalid('192.0.2.1',{prefix},/CIDR prefix/);
});
check(ip,'private and shared ranges labeled separately',async()=>{
  assert.match(await output('172.31.255.255',{prefix:'12'}),/Private use \(172\.16\.0\.0\/12\)/);
  assert.match(await output('100.64.0.1',{prefix:'10'}),/Shared address space \(100\.64\.0\.0\/10\)/);
});

check(filename,'Unicode paste, affixes, numbering, dotfiles and case conversion',async()=>{
  assert.equal(await output('Café.tar.gz\n.gitignore',{prefix:'IMG-',suffix:'-DONE',numbering:'on',start:'7',padding:'3',letterCase:'lower'}),
    'Original,Proposed\n"Café.tar.gz","img-007-café.tar-done.gz"\n".gitignore","img-008-.gitignore-done"');
});
check(filename,'selected File metadata only and byte-exact formula-protected CSV',async()=>{
  await b.evaluate(`window.__reads=0;window.__fs=0;
    for(const key of ['text','slice','arrayBuffer','stream'])File.prototype[key]=()=>{__reads++;throw Error('content read')};
    window.FileReader=function(){__reads++;throw Error('content read')};
    for(const key of ['showOpenFilePicker','showSaveFilePicker','showDirectoryPicker'])window[key]=()=>{__fs++;throw Error('filesystem operation')};true`);
  await selectFiles('nameFiles',["new File(['edb251-local-only'],'+Café.tar.gz')","new File(['edb251-local-only'],'＝run.txt')","new File([], 'a,b.txt')"]);
  await set(b,'suffix','-done');await click(b,'runBtn');await wait(b,"toolStatus.textContent==='Complete.'");await click(b,'downloadBtn');
  const csv='Original,Proposed\r\n"\'+Café.tar.gz","\'+Café.tar-done.gz"\r\n"\'＝run.txt","\'＝run-done.txt"\r\n"a,b.txt","a,b-done.txt"';
  assert.equal(await b.evaluate('__edbDownloadBlob.type'),'text/csv;charset=utf-8');assert.equal(await b.evaluate('__edbDownloadBlob.text()'),csv);assert.deepEqual(await b.evaluate('__edbDownloads'),['filename-plan.csv']);
  assert.deepEqual(await b.evaluate('[__reads,__fs,Array.from(nameFiles.files,f=>f.name)]'),[0,0,['+Café.tar.gz','＝run.txt','a,b.txt']]);
  await click(b,'clearBtn');assert.equal(await b.evaluate('nameFiles.files.length'),0);
  return {file_content_reads:0,filesystem_picker_calls:0,csv_type:'text/csv;charset=utf-8',csv_bytes:Buffer.byteLength(csv)};
});
check(filename,'case and Unicode collisions deny copy and export',async()=>{
  for(const input of ['A.txt\na.TXT','é.txt\né.TXT']){
    const r=await run(b,input);assert.match(r.error,/Destination collision between rows 1 and 2/);assert.match(r.text,/Original,Proposed/);assert.equal(await b.evaluate('copyBtn.disabled&&downloadBtn.disabled'),true);
  }
});
check(filename,'portable reserved names, invalid characters and output limits',async()=>{
  for(const input of ['COM¹.txt','NUL.jpg','bad/name','a?.txt','trailing.','x '])await invalid(input,{},/portable filename rules/);
  await invalid('a.txt',{prefix:'NUL.'},/Proposed name 1 is invalid/);
  await invalid(Array.from({length:501},(_,i)=>'f'+i).join('\n'),{prefix:''},/500 names/);
  await invalid(Array.from({length:100},(_,i)=>'界'.repeat(250)+i).join('\n'),{},/128 KiB output limit/);
});

check(file,'empty and identical actual File selections',async()=>{
  assert.match(await compare("new File([],'a')","new File([],'b')"),/Identical[\s\S]*File A: 0 bytes[\s\S]*First differing offset: None/);
  assert.match(await compare("new File(['edb251-local-only'],'same')","new File(['edb251-local-only'],'different-name')"),/Identical/);
});
check(file,'early difference and shorter-file EOF with unequal lengths',async()=>{
  const early=await compare("new File(['abc'],'same')","new File(['Xbcd'],'same')");assert.match(early,/Size difference: 1 bytes\nFirst differing offset: 0 \(zero-based\)/);
  const eof=await compare("new File(['abc'],'a')","new File(['abcd'],'b')");assert.match(eof,/First differing offset: 3 \(zero-based, shorter file ends here\)/);
});
check(file,'actual native Worker shows bounded pairs at the chunk boundary',async()=>{
  const metrics=await observeWorker(b,async()=>{
    const left="new File([new Uint8Array(786432)],'a')",right="new File([new Uint8Array(262144),new Uint8Array([1]),new Uint8Array(524287)],'b')";
    assert.match(await compare(left,right),/First differing offset: 262144 \(zero-based\)/);
  });
  assert.deepEqual(metrics.slices,[[0,262144],[0,262144],[262144,524288],[262144,524288]]);
  assert.deepEqual(metrics.read_sizes,[262144,262144,262144,262144]);assert.equal(metrics.peak_reads_in_flight,2);
  return metrics;
});
check(file,'late difference after several chunks',async()=>{
  const left="new File([new Uint8Array(786432),'x'],'a')",right="new File([new Uint8Array(786432),'y'],'b')";
  assert.match(await compare(left,right),/First differing offset: 786432 \(zero-based\)/);
});
check(file,'64 MiB pair succeeds and oversize never starts a Worker',async()=>{
  await b.evaluate(`window.__part=new Blob([new Uint8Array(262144)]);window.__workers=0;const NativeWorker=Worker;window.Worker=class extends NativeWorker{constructor(url){super(url);__workers++}};true`);
  const fixture="new File(Array(256).fill(__part),'limit.bin')",start=performance.now();
  assert.match(await compare(fixture,fixture),/Identical[\s\S]*File A: 67108864 bytes/);
  const elapsed=Math.round(performance.now()-start);assert.ok(elapsed<10000);
  await selectFiles('secondFile',["new File([...Array(256).fill(__part),'x'],'big.bin')"]);await click(b,'runBtn');await wait(b,'!toolError.hidden');assert.match(await b.evaluate('toolError.textContent'),/64 MiB/);assert.equal(await b.evaluate('__workers'),1);
  return {bytes_per_file:67108864,observed_elapsed_ms:elapsed,worker_starts_after_oversize:1};
});
check(file,'cancellation, reselection and reset discard prior native Worker results',async()=>{
  await b.evaluate(`window.__terminated=0;const native=Worker.prototype.terminate;Worker.prototype.terminate=function(){__terminated++;return native.call(this)};true`);
  await selectFiles('toolInput',["new File(['a'],'a')"]);await selectFiles('secondFile',["new File(['a'],'b')"]);
  await b.evaluate('runBtn.click();cancelBtn.click();true');assert.equal(await b.evaluate('__terminated'),1);assert.equal(await b.evaluate('toolStatus.textContent'),'Comparison cancelled.');assert.equal(await b.evaluate('toolOutput.value'),'');
  await b.evaluate(`runBtn.click();const next=new DataTransfer();next.items.add(new File(['b'],'b'));secondFile.files=next.files;secondFile.dispatchEvent(new Event('change',{bubbles:true}));true`);
  assert.equal(await b.evaluate('__terminated'),2);await click(b,'runBtn');await wait(b,"toolStatus.textContent==='Complete.'");assert.match(await b.evaluate('toolOutput.value'),/First differing offset: 0/);
  await click(b,'clearBtn');assert.equal(await b.evaluate('toolInput.files.length+secondFile.files.length'),0);assert.equal(await b.evaluate('toolOutput.value'),'');
});

check(gradient,'live linear preview, exact angle and generated CSS',async()=>{
  await set(b,'toolInput',stops);assert.equal(await b.evaluate('toolOutput.value'),'background-image: linear-gradient(90deg, #6366f1 0%, #22d3ee 100%);');
  await set(b,'angle','-45.5');assert.match(await b.evaluate('getComputedStyle(gradientPreview).backgroundImage'),/^linear-gradient\(-45\.5deg,/);
});
check(gradient,'centered radial mode disables angle and preserves hard stops',async()=>{
  const css=await output('#FF0000 25%\n#00FF00 25%',{type:'radial'});assert.equal(css,'background-image: radial-gradient(circle at center, #ff0000 25%, #00ff00 25%);');
  assert.equal(await b.evaluate('angle.disabled'),true);assert.match(await b.evaluate('getComputedStyle(gradientPreview).backgroundImage'),/^radial-gradient\(/);
});
check(gradient,'validate colour grammar, numeric angles, positions and order',async()=>{
  await invalid('#gggggg 0%\n#ffffff 100%',{},/use #RRGGBB/);await invalid(stops,{angle:'361'},/between -360 and 360/);
  await invalid('#000000 80%\n#ffffff 20%',{},/nondecreasing/);await invalid('#000000 0%\n#ffffff 101%',{},/between 0 and 100/);assert.equal(await b.evaluate('gradientPreview.hidden'),true);
});
check(gradient,'eight stops allowed and nine rejected',async()=>{
  const input=Array.from({length:8},(_,i)=>`#123456 ${i*10}%`).join('\n');assert.match(await output(input),/70%\);$/);await invalid(input+'\n#123456 80%',{},/between 2 and 8/);
});
check(gradient,'CSS and markup injection probes stay inert',async()=>{
  for(const input of ['url(https://example.invalid/edb251-local-only) 0%\n#ffffff 100%','#000000 0%; background:url(https://example.invalid/edb251-local-only)\n#ffffff 100%','<img src="https://example.invalid/edb251-local-only"> 0%\n#ffffff 100%','var(--evil) 0%\n#ffffff 100%'])await invalid(input,{},/use #RRGGBB/);
  assert.equal(await b.evaluate('gradientPreview.style.backgroundImage'), '');assert.equal(await b.evaluate('document.querySelectorAll("img").length'),0);
});

const samples={[word]:'a a é',[unicode]:'👩‍💻',[ip]:'192.0.2.1',[filename]:'local.txt',[gradient]:stops};
async function seed(id){if(id===file){await selectFiles('toolInput',["new File(['a'],'a')"]);await selectFiles('secondFile',["new File(['a'],'b')"]);}else await set(b,'toolInput',samples[id]);}
for(const id of ids){
  check(id,'copy success, denied clipboard fallback and reset',async()=>{
    await seed(id);await click(b,'runBtn');await wait(b,"toolStatus.textContent==='Complete.'");const value=await b.evaluate('toolOutput.value');assert.ok(value);
    await click(b,'copyBtn');await wait(b,"toolStatus.textContent==='Copied.'");assert.equal((await b.evaluate('__edbClipboard.value')).replaceAll('\r\n','\n'),value);
    await b.evaluate("__edbClipboard.mode='failure';true");await click(b,'copyBtn');await wait(b,"toolStatus.textContent.includes('Output selected')");assert.equal(await b.evaluate('document.activeElement.id'),'toolOutput');
    await click(b,'clearBtn');assert.equal(await b.evaluate('toolInput.value+toolOutput.value'),'');assert.equal(await b.evaluate('document.activeElement.id'),'toolInput');assert.equal(await b.evaluate('copyBtn.disabled&&downloadBtn.disabled'),true);
  });
  check(id,'native keyboard operation and no overflow at four widths',async()=>{
    await seed(id);await b.evaluate('runBtn.focus();true');
    for(const type of ['keyDown','keyUp'])await b.call('Input.dispatchKeyEvent',{type,key:'Enter',code:'Enter',windowsVirtualKeyCode:13,...(type==='keyDown'?{text:'\r'}:{})});
    await wait(b,"toolStatus.textContent==='Complete.'");
    try{for(const width of [320,375,768,1440]){await b.call('Emulation.setDeviceMetricsOverride',{width,height:900,deviceScaleFactor:1,mobile:false});assert.equal(await b.evaluate('document.documentElement.scrollWidth>innerWidth'),false);}}
    finally{await b.call('Emulation.clearDeviceMetricsOverride');}
  });
}
check('homepage','87 distinct visible canonical cards and six tested labels',async()=>{
  const cards=await b.evaluate(`Array.from(document.querySelectorAll('a.tool-card[data-title]'),a=>({route:a.getAttribute('href'),visible:a.getClientRects().length>0&&getComputedStyle(a).visibility==='visible',status:a.dataset.availability,text:a.textContent}))`);
  const registry=JSON.parse(fs.readFileSync(new URL('./approved-registry.json',import.meta.url),'utf8'));
  const expected=registry.tools.filter(t=>['RELEASED','TESTED'].includes(t.status)).map(t=>t.directory_path+'/index.html').sort();
  assert.equal(cards.length,87);assert.ok(cards.every(c=>c.visible));assert.equal(new Set(cards.map(c=>c.route)).size,87);assert.deepEqual(cards.map(c=>c.route).sort(),expected);
  for(const id of ids){const card=cards.find(c=>c.route===id+'/index.html');assert.equal(card.status,'tested');assert.match(card.text,/Tested · publication pending/);}
  assert.equal(await b.evaluate('resultCount.textContent'),'87 tools ready to use');
  return {visible_cards:87,previously_released:81,publication_pending:6};
});
