import {test,before,beforeEach,after} from 'node:test';import assert from 'node:assert/strict';import {start,source,set,click,wait,widths,noTransport} from '../task20-browser.mjs';let b;before(async()=>b=await start());beforeEach(async()=>b.load(source('passport-photo-layout-maker')));after(async()=>b?.close());
// Headless Chromium can leave native PNG row encoding waiting for an idle turn.
// Request rendering turns while polling, without extending the existing budget.
async function waitForKeyboardPng(browser, expression='!runBtn.disabled') {
  const deadline=Date.now()+5000;
  let active=true,timer;
  const failure=()=>new assert.AssertionError({message:`Expected browser state: ${expression}`,operator:'fail'});
  const scoped=Object.create(browser);
  scoped.evaluate=async raw=>{
    if(!active||Date.now()>=deadline)throw failure();
    const value=await browser.evaluate(`(()=>{
      const value=(${raw}),deadline=${deadline};
      if(!value&&Date.now()<deadline){
        const state=window.__edbPassportWaitFrames||(window.__edbPassportWaitFrames={ids:new Set(),active:true});
        const first=requestAnimationFrame(()=>{
          state.ids.delete(first);
          if(!state.active||Date.now()>=deadline||(${raw}))return;
          const second=requestAnimationFrame(()=>{state.ids.delete(second)});
          state.ids.add(second);
        });
        state.ids.add(first);
      }
      return value;
    })()`);
    if(!active||Date.now()>=deadline)throw failure();
    return value;
  };
  try {
    await Promise.race([
      wait(scoped,expression),
      new Promise((_,reject)=>{timer=setTimeout(()=>reject(failure()),Math.max(0,deadline-Date.now()))})
    ]);
    if(Date.now()>=deadline)throw failure();
  } finally {
    active=false;
    clearTimeout(timer);
    await browser.evaluate(`(()=>{const state=window.__edbPassportWaitFrames;if(state){state.active=false;for(const id of state.ids)cancelAnimationFrame(id);state.ids.clear();delete window.__edbPassportWaitFrames;}return true})()`);
  }
}
async function sample(type='image/png'){await b.evaluate(`(async()=>{const c=document.createElement('canvas');c.width=4;c.height=3;const ctx=c.getContext('2d');ctx.fillStyle='red';ctx.fillRect(0,0,4,3);ctx.clearRect(0,0,1,1);const blob=await new Promise(r=>c.toBlob(r,${JSON.stringify(type)})),dt=new DataTransfer();dt.items.add(new File([blob],'portrait'));toolInput.files=dt.files;toolInput.dispatchEvent(new Event('change'));return true})()`)}
async function generate(){await click(b,'runBtn');await wait(b,'!runBtn.disabled');assert.equal(await b.evaluate('toolError.hidden'),true);await click(b,'downloadBtn')}
test('actual A4PNG dimensions, tile positions, containment padding, white alpha and gap pixels match independent geometry',async()=>{await sample();await set(b,'count','2');await generate();const r=await b.evaluate(`(async()=>{const blob=__edbDownloadBlob,im=await createImageBitmap(blob),c=document.createElement('canvas');c.width=im.width;c.height=im.height;const ctx=c.getContext('2d');ctx.drawImage(im,0,0);im.close();const raw=new Uint8Array(await blob.arrayBuffer()),view=new DataView(raw.buffer);let resolution=null;for(let p=8;p<raw.length;){const n=view.getUint32(p);if(String.fromCharCode(...raw.slice(p+4,p+8))==='pHYs')resolution=[view.getUint32(p+8),view.getUint32(p+12),raw[p+16]];p+=n+12;}return {resolution,type:blob.type,w:c.width,h:c.height,signature:Array.from(new Uint8Array(await blob.slice(0,8).arrayBuffer())),pixels:[[0,0],[60,60],[162,192],[275,192],[398,192]].map(([x,y])=>Array.from(ctx.getImageData(x,y,1,1).data))}})()`);assert.deepEqual([r.type,r.w,r.h],['image/png',1240,1754]);assert.deepEqual(r.signature,[137,80,78,71,13,10,26,10]);assert.deepEqual(r.resolution,[5906,5906,1]);assert.deepEqual(r.pixels,[[255,255,255,255],[255,255,255,255],[255,0,0,255],[255,255,255,255],[255,0,0,255]])});
test('Letter300 DPI actual output and calibrated physical print/PDF page dimensions agree',async()=>{await sample();await set(b,'paper','Letter','change');await set(b,'dpi','300','change');await generate();assert.deepEqual(await b.evaluate(`(async()=>{const im=await createImageBitmap(__edbDownloadBlob),r=[im.width,im.height];im.close();return r})()`),[2550,3300]);assert.match(await b.evaluate('toolOutput.value'),/100%\/actual size/);await b.evaluate('window.__prints=0;window.print=()=>{__prints++};true');await click(b,'printBtn');assert.equal(await b.evaluate('__prints'),1);await b.call('Emulation.setEmulatedMedia',{media:'print'});const styles=await b.evaluate('({w:getComputedStyle(sheetPreview).width,h:getComputedStyle(sheetPreview).height,header:getComputedStyle(document.querySelector("header")).display})');assert.equal(styles.header,'none');assert.ok(Math.abs(parseFloat(styles.w)-816)<.1);assert.ok(Math.abs(parseFloat(styles.h)-1056)<.1);const pdf=await b.call('Page.printToPDF',{preferCSSPageSize:true,printBackground:true});const raw=Buffer.from(pdf.data,'base64').toString('latin1'),m=/\/MediaBox\s*\[\s*0\s+0\s+([\d.]+)\s+([\d.]+)\s*\]/.exec(raw);assert.ok(m);assert.ok(Math.abs(Number(m[1])-612)<1&&Math.abs(Number(m[2])-792)<1);await b.call('Emulation.setEmulatedMedia',{media:''})});
test('JPEG/PNG/WebP input work without external processing; the ruler can be explicitly omitted',async()=>{for(const type of ['image/jpeg','image/png','image/webp']){await sample(type);await b.evaluate('calibration.checked=false;calibration.dispatchEvent(new Event("change"));true');await generate();assert.equal(await b.evaluate('__edbDownloadBlob.type'),'image/png');assert.equal(await b.evaluate('sheetPreview.hidden'),false)}});
test('invalid fit and settings never silently reduce requested tiles or keep stale exports',async()=>{await sample();await generate();await set(b,'photoWidth','100');await set(b,'photoHeight','100');await set(b,'margin','30');await set(b,'count','3');await click(b,'runBtn');await wait(b,'!runBtn.disabled');assert.match(await b.evaluate('toolError.textContent'),/do not fit/);assert.equal(await b.evaluate('downloadBtn.disabled&&printBtn.disabled&&sheetPreview.hidden'),true);await set(b,'count','41');await click(b,'runBtn');await wait(b,'!runBtn.disabled');assert.match(await b.evaluate('toolError.textContent'),/range/)});
test('invalid file, wrong output MIME and40 MiB output cap fail safely',async()=>{await click(b,'runBtn');await wait(b,'!runBtn.disabled');assert.equal(await b.evaluate('!toolError.hidden'),true);for(const [mime,size]of [['image/jpeg',3],['image/png',41943041]]){await sample();await b.evaluate('window.__realBlob=HTMLCanvasElement.prototype.toBlob;true');try{await b.evaluate(`HTMLCanvasElement.prototype.toBlob=cb=>cb(new Blob([new Uint8Array(${size})],{type:${JSON.stringify(mime)}}));true`);await click(b,'runBtn');await wait(b,'!runBtn.disabled');assert.equal(await b.evaluate('!toolError.hidden&&downloadBtn.disabled&&printBtn.disabled'),true)}finally{await b.evaluate('HTMLCanvasElement.prototype.toBlob=__realBlob;true')}}});
test('reset during encoding discards late results and restores every control/focus',async()=>{await sample();await b.evaluate('const real=HTMLCanvasElement.prototype.toBlob;HTMLCanvasElement.prototype.toBlob=function(...a){setTimeout(()=>real.apply(this,a),150)};true');await click(b,'runBtn');await click(b,'clearBtn');await new Promise(r=>setTimeout(r,250));assert.deepEqual(await b.evaluate('[toolInput.files.length,paper.value,dpi.value,photoWidth.value,photoHeight.value,margin.value,gap.value,count.value,calibration.checked,toolOutput.value,printBtn.disabled,document.activeElement.id]'),[0,'A4','150','35','45','10','5','8',true,'',true,'toolInput']);assert.equal(await b.evaluate('sheetPreview.hidden'),true)});
test('keyboard build/copy, responsive widths and no image transport',async()=>{await sample();await noTransport(b,async()=>{await b.evaluate('runBtn.focus();true');await b.call('Input.dispatchKeyEvent',{type:'keyDown',key:'Enter',code:'Enter',windowsVirtualKeyCode:13,text:'\r'});await b.call('Input.dispatchKeyEvent',{type:'keyUp',key:'Enter',code:'Enter',windowsVirtualKeyCode:13});await waitForKeyboardPng(b)});assert.equal(await b.evaluate('toolError.hidden'),true);await click(b,'copyBtn');assert.equal(await b.evaluate('__edbClipboard.value'),await b.evaluate('toolOutput.value'));await widths(b)});
test('real8-million-pixel portrait and40 tiles render an actual300 DPI A4 sheet within caps',async()=>{await b.evaluate(`(async()=>{const c=document.createElement('canvas');c.width=4000;c.height=2000;const ctx=c.getContext('2d');ctx.fillStyle='red';ctx.fillRect(0,0,c.width,c.height);const blob=await new Promise(r=>c.toBlob(r,'image/png'));c.width=c.height=0;const dt=new DataTransfer();dt.items.add(new File([blob],'boundary.png'));toolInput.files=dt.files;toolInput.dispatchEvent(new Event('change'));return true})()`);await set(b,'dpi','300','change');await set(b,'count','40');await set(b,'photoWidth','10');await set(b,'photoHeight','10');await generate();const x=await b.evaluate(`(async()=>{const blob=__edbDownloadBlob,im=await createImageBitmap(blob),value={w:im.width,h:im.height,bytes:blob.size};im.close();return value})()`);assert.deepEqual([x.w,x.h],[2480,3508]);assert.ok(x.w*x.h<=10000000&&x.bytes<=41943040);assert.match(await b.evaluate('toolOutput.value'),/Tiles: 40/)});

test('Passport rendering wait rejects a never-completing operation and cancels frames',async()=>{
  await b.evaluate('window.__edbNeverComplete=new Promise(()=>{});window.__edbControlReady=false;__edbNeverComplete.then(()=>{__edbControlReady=true});true');
  await assert.rejects(waitForKeyboardPng(b,'window.__edbControlReady'),{name:'AssertionError',message:'Expected browser state: window.__edbControlReady'});
  assert.equal(await b.evaluate('window.__edbControlReady'),false);
  assert.equal(await b.evaluate('window.__edbPassportWaitFrames===undefined'),true);
});

test('Passport rendering wait rejects late background completion without a CDP timeout',async()=>{
  // Start on the first poll, so setup latency cannot consume the control delay.
  // Each CDP request returns promptly; this task never replaces PNG encoding.
  await b.evaluate(`window.__edbLateControl={ready:false,timer:null,completedAt:null};
    window.__edbLateReady=()=>{const state=window.__edbLateControl;if(state.timer===null){state.timer=setTimeout(()=>{state.completedAt=Date.now();state.ready=true},5200)}return state.ready};true`);
  try {
    await assert.rejects(waitForKeyboardPng(b,'window.__edbLateReady()'),{name:'AssertionError',message:'Expected browser state: window.__edbLateReady()'});
    const failedAt=Date.now();
    assert.equal(await b.evaluate('window.__edbLateControl.ready'),false);
    assert.equal(await b.evaluate('window.__edbPassportWaitFrames===undefined'),true);
    // A separate observation after rejection cannot change the failed wait.
    await wait(b,'window.__edbLateControl.ready');
    assert.equal(await b.evaluate('window.__edbLateControl.ready'),true);
    assert.ok(await b.evaluate('window.__edbLateControl.completedAt')>failedAt);
  } finally {
    await b.evaluate('clearTimeout(window.__edbLateControl.timer);delete window.__edbLateReady;delete window.__edbLateControl;true');
  }
});
