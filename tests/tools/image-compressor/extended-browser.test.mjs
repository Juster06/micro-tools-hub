import {test,before,beforeEach,after} from 'node:test';import assert from 'node:assert/strict';import {start,source,set,click,wait,widths,noTransport} from '../task20-browser.mjs';let b;before(async()=>b=await start());beforeEach(async()=>b.load(source('image-compressor')));after(async()=>b?.close());
import {performance} from 'node:perf_hooks';

// Native JPEG attempts can wait for Chromium idle scheduling between callbacks.
// Supply rendering turns without extending the original success deadline.
async function waitForKeyboardJpeg(browser, expression='!runBtn.disabled'){
 const deadline=performance.now()+5000,wallDeadline=Date.now()+5000;
 let active=true,timer;
 const failure=()=>new assert.AssertionError({message:`Expected browser state: ${expression}`,operator:'fail'});
 const check=()=>{if(!active||performance.now()>=deadline||Date.now()>=wallDeadline)throw failure()};
 const scoped=Object.create(browser);
 scoped.evaluate=async raw=>{
  check();
  const value=await browser.evaluate(`(()=>{
   const ready=(${raw}),expires=${wallDeadline};
   if(!ready&&Date.now()<expires){
    const state=window.__edbImageWaitFrames||(window.__edbImageWaitFrames={active:true,ids:new Set()});
    const first=requestAnimationFrame(()=>{
     state.ids.delete(first);
     if(!state.active||Date.now()>=expires||(${raw}))return;
     const second=requestAnimationFrame(()=>{state.ids.delete(second)});
     state.ids.add(second);
    });
    state.ids.add(first);
   }
   return ready;
  })()`);
  check();
  return value;
 };
 try{
  await Promise.race([
   wait(scoped,expression),
   new Promise((_,reject)=>{timer=setTimeout(()=>{active=false;reject(failure())},Math.max(0,Math.min(deadline-performance.now(),wallDeadline-Date.now())))})
  ]);
  check();
 }finally{
  active=false;clearTimeout(timer);
  // Cleanup is not a success observation and cannot extend the success window.
  await browser.evaluate(`(()=>{const state=window.__edbImageWaitFrames;if(state){state.active=false;for(const id of state.ids)cancelAnimationFrame(id);state.ids.clear();delete window.__edbImageWaitFrames}return true})()`);
 }
}

async function sample(small=false){await b.evaluate(`(async()=>{const c=document.createElement('canvas');c.width=c.height=${small?4:512};const ctx=c.getContext('2d'),p=ctx.createImageData(c.width,c.height);let seed=12345;for(let i=0;i<p.data.length;i+=4){for(let j=0;j<3;j++){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;p.data[i+j]=seed&255}p.data[i+3]=255}ctx.putImageData(p,0,0);ctx.clearRect(0,0,${small?1:64},${small?1:64});const blob=await new Promise(r=>c.toBlob(r,'image/png')),dt=new DataTransfer();dt.items.add(new File([blob],'noise.png'));toolInput.files=dt.files;toolInput.dispatchEvent(new Event('change'));window.__sourceBytes=blob.size;return true})()`)}
async function compress(){await click(b,'runBtn');await wait(b,'!runBtn.disabled');assert.equal(await b.evaluate('toolError.hidden'),true)}
test('real target-size JPEG compression returns actual smaller bytes/MIME/dimensions and filled background',async()=>{await sample();await set(b,'targetKiB','1000');await set(b,'background','#123456','change');await compress();assert.match(await b.evaluate('toolOutput.value'),/Target: 1024000 bytes — met/);await click(b,'downloadBtn');const x=await b.evaluate(`(async()=>{const blob=__edbDownloadBlob,im=await createImageBitmap(blob),c=document.createElement('canvas');c.width=im.width;c.height=im.height;const ctx=c.getContext('2d');ctx.drawImage(im,0,0);im.close();return {mime:blob.type,bytes:blob.size,smaller:blob.size<__sourceBytes,w:c.width,h:c.height,signature:Array.from(new Uint8Array(await blob.slice(0,2).arrayBuffer())),pixel:Array.from(ctx.getImageData(1,1,1,1).data)}})()`);assert.equal(x.mime,'image/jpeg');assert.equal(x.smaller,true);assert.deepEqual([x.w,x.h,x.signature],[512,512,[255,216]]);for(let i=0;i<3;i++)assert.ok(Math.abs(x.pixel[i]-[18,52,86][i])<=3);assert.equal(x.pixel[3],255)});
test('actual WebP preserves transparency and target-not-met is honestly reported',async()=>{await sample();await set(b,'outputFormat','image/webp','change');await set(b,'targetKiB','1');await compress();assert.match(await b.evaluate('toolOutput.value'),/not met/);await click(b,'downloadBtn');const x=await b.evaluate(`(async()=>{const blob=__edbDownloadBlob,im=await createImageBitmap(blob),c=document.createElement('canvas');c.width=im.width;c.height=im.height;const ctx=c.getContext('2d');ctx.drawImage(im,0,0);im.close();return {mime:blob.type,alpha:ctx.getImageData(1,1,1,1).data[3],bytes:blob.size,smaller:blob.size<__sourceBytes}})()`);assert.equal(x.mime,'image/webp');assert.equal(x.alpha,0);assert.equal(x.smaller,true);assert.ok(x.bytes>1024);assert.match(await b.evaluate('toolOutput.value'),/Attempts: 12/)});
test('no-improvement result retains the original and never offers a larger compressed file',async()=>{await sample(true);await compress();assert.match(await b.evaluate('toolOutput.value'),/No improvement/);assert.match(await b.evaluate('toolOutput.value'),/Original already fits the target/);assert.equal(await b.evaluate('downloadBtn.disabled&&!beforePreview.hidden&&afterPreview.hidden'),true)});
test('empty/oversize/header/pixel errors fail before decoder allocation',async()=>{await b.evaluate('window.__decodes=0;const real=createImageBitmap;window.createImageBitmap=(...a)=>{__decodes++;return real(...a)};true');for(const size of [0,5242881]){await b.evaluate(`(()=>{const dt=new DataTransfer();dt.items.add(new File([new Uint8Array(${size})],'bad.png'));toolInput.files=dt.files;return true})()`);await click(b,'runBtn');await wait(b,'!runBtn.disabled');assert.equal(await b.evaluate('!toolError.hidden&&downloadBtn.disabled'),true)}assert.equal(await b.evaluate('__decodes'),0);await b.evaluate(`(()=>{const x=new Uint8Array(45),v=new DataView(x.buffer);x.set([137,80,78,71,13,10,26,10]);v.setUint32(8,13);x.set([73,72,68,82],12);v.setUint32(16,4000);v.setUint32(20,2001);x.set([73,69,78,68],37);const dt=new DataTransfer();dt.items.add(new File([x],'over-pixel.png'));toolInput.files=dt.files;return true})()`);await click(b,'runBtn');await wait(b,'!runBtn.disabled');assert.match(await b.evaluate('toolError.textContent'),/dimensions/);assert.equal(await b.evaluate('__decodes'),0)});
test('wrong MIME, output cap and simulated processing deadline cannot enable a download',async()=>{for(const [type,size]of [['image/png',3],['image/jpeg',8388609]]){await b.load(source('image-compressor'));await sample();await b.evaluate(`HTMLCanvasElement.prototype.toBlob=function(cb){cb(new Blob([new Uint8Array(${size})],{type:${JSON.stringify(type)}}))};true`);await click(b,'runBtn');await wait(b,'!runBtn.disabled');assert.equal(await b.evaluate('!toolError.hidden&&downloadBtn.disabled'),true)}await b.load(source('image-compressor'));await sample();await b.evaluate(`window.__clock=performance.now();Performance.prototype.now=()=>window.__clock;HTMLCanvasElement.prototype.toBlob=function(cb){window.__clock+=10001;cb(new Blob(['x'],{type:'image/jpeg'}))};true`);await click(b,'runBtn');await wait(b,'!runBtn.disabled');assert.match(await b.evaluate('toolError.textContent'),/deadline/)});
test('reset/edit discard late encodes and revoke preview URLs',async()=>{await sample();await compress();await b.evaluate(`window.__revoked=0;const revoke=URL.revokeObjectURL.bind(URL);URL.revokeObjectURL=u=>{__revoked++;revoke(u)};const real=HTMLCanvasElement.prototype.toBlob;HTMLCanvasElement.prototype.toBlob=function(...a){setTimeout(()=>real.apply(this,a),150)};true`);await click(b,'runBtn');await click(b,'clearBtn');await new Promise(r=>setTimeout(r,250));assert.equal(await b.evaluate('toolOutput.value===""&&downloadBtn.disabled&&beforePreview.hidden&&afterPreview.hidden'),true);assert.ok(await b.evaluate('__revoked')>=1);assert.equal(await b.evaluate('document.activeElement.id'),'toolInput')});
test('keyboard, copy denial, narrow widths and local-only processing',async()=>{await sample(true);await noTransport(b,async()=>{await b.evaluate('runBtn.focus();true');await b.call('Input.dispatchKeyEvent',{type:'keyDown',key:'Enter',code:'Enter',windowsVirtualKeyCode:13,text:'\r'});await b.call('Input.dispatchKeyEvent',{type:'keyUp',key:'Enter',code:'Enter',windowsVirtualKeyCode:13});await waitForKeyboardJpeg(b)});await click(b,'copyBtn');assert.equal(await b.evaluate('__edbClipboard.value'),await b.evaluate('toolOutput.value'));await b.evaluate('__edbClipboard.mode="failure";true');await click(b,'copyBtn');assert.match(await b.evaluate('toolStatus.textContent'),/unavailable/);await widths(b)});
test('real8-million-pixel input stays bounded through the compression search deadline',async()=>{await b.evaluate(`(async()=>{const c=document.createElement('canvas');c.width=4000;c.height=2000;const ctx=c.getContext('2d');ctx.fillStyle='red';ctx.fillRect(0,0,c.width,c.height);const blob=await new Promise(r=>c.toBlob(r,'image/png'));c.width=c.height=0;const dt=new DataTransfer();dt.items.add(new File([blob],'boundary.png'));toolInput.files=dt.files;toolInput.dispatchEvent(new Event('change'));window.__started=performance.now();runBtn.click();return true})()`);const end=Date.now()+12000;while(Date.now()<end&&!await b.evaluate('!runBtn.disabled'))await new Promise(r=>setTimeout(r,25));assert.equal(await b.evaluate('!runBtn.disabled&&toolError.hidden&&!!toolOutput.value'),true);assert.ok(await b.evaluate('performance.now()-__started')<11000);assert.match(await b.evaluate('toolOutput.value'),/Original:/)});

test('Image Compressor rendering wait rejects a never-completing operation and cancels frames',async()=>{
 await b.evaluate('window.__edbImageNeverReady=false;window.__edbImageNeverTask=new Promise(()=>{});__edbImageNeverTask.then(()=>{__edbImageNeverReady=true});true');
 await assert.rejects(waitForKeyboardJpeg(b,'window.__edbImageNeverReady'),{name:'AssertionError',message:'Expected browser state: window.__edbImageNeverReady'});
 assert.equal(await b.evaluate('window.__edbImageNeverReady'),false);
 assert.equal(await b.evaluate('window.__edbImageWaitFrames===undefined'),true);
});

test('Image Compressor rendering wait rejects late background completion without a CDP timeout',async()=>{
 // Start the background task on the first short poll; leave real encoding alone.
 await b.evaluate(`window.__edbImageLate={ready:false,timer:null,completedAt:null};window.__edbImageLateReady=()=>{const s=window.__edbImageLate;if(s.timer===null)s.timer=setTimeout(()=>{s.completedAt=Date.now();s.ready=true},5200);return s.ready};true`);
 let outcome='PENDING';
 try{
  const trial=waitForKeyboardJpeg(b,'window.__edbImageLateReady()').then(()=>{outcome='PASS'},error=>{outcome='FAIL';throw error});
  await assert.rejects(trial,{name:'AssertionError',message:'Expected browser state: window.__edbImageLateReady()'});
  const failedAt=Date.now();
  assert.equal(await b.evaluate('window.__edbImageLate.ready'),false);
  assert.equal(await b.evaluate('window.__edbImageWaitFrames===undefined'),true);
  // Observing a later completion cannot retry or change the already failed wait.
  await wait(b,'window.__edbImageLate.ready');
  assert.ok(await b.evaluate('window.__edbImageLate.completedAt')>failedAt);
  assert.equal(outcome,'FAIL');
 }finally{await b.evaluate('clearTimeout(window.__edbImageLate.timer);delete window.__edbImageLate;delete window.__edbImageLateReady;true')}
});

test('Image Compressor rendering wait rejects a true short-poll response delivered after its deadline',async()=>{
 await b.evaluate(`window.__edbImageCross={ready:false,timer:null};window.__edbImageCrossReady=()=>{const s=window.__edbImageCross;if(s.timer===null)s.timer=setTimeout(()=>{s.ready=true},5050);return s.ready};true`);
 const delayed=Object.create(b),started=Date.now();let held=false,responseValue,outcome='PENDING',finish,responseTimer;
 const response=new Promise(resolve=>{finish=resolve});
 delayed.evaluate=async raw=>{
  const target=raw.includes('const ready=')&&raw.includes('window.__edbImageCrossReady()');
  if(target&&!held&&Date.now()-started>=4850){
   held=true;
   // Delay outside CDP; the browser command itself remains a short state poll.
   await new Promise(resolve=>setTimeout(resolve,Math.max(0,5300-(Date.now()-started))));
   const value=await b.evaluate(raw);responseValue=value;finish();return value;
  }
  return b.evaluate(raw);
 };
 try{
  const trial=waitForKeyboardJpeg(delayed,'window.__edbImageCrossReady()').then(()=>{outcome='PASS'},error=>{outcome='FAIL';throw error});
  await assert.rejects(trial,{name:'AssertionError',message:'Expected browser state: window.__edbImageCrossReady()'});
  assert.equal(held,true);
  await Promise.race([response,new Promise((_,reject)=>{responseTimer=setTimeout(()=>reject(Error('Late response fixture did not complete')),1500)})]);
  assert.equal(responseValue,true);assert.equal(outcome,'FAIL');
  assert.equal(await b.evaluate('window.__edbImageWaitFrames===undefined'),true);
 }finally{
  clearTimeout(responseTimer);
  await b.evaluate('clearTimeout(window.__edbImageCross.timer);delete window.__edbImageCross;delete window.__edbImageCrossReady;true');
 }
});
