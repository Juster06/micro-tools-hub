// Optional real Chromium interaction tests using Node built-ins and an isolated profile.
// No installation, development server, user profile or third-party site is required.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawn} from 'node:child_process';
import {pathToFileURL} from 'node:url';

const pause = ms => new Promise(resolve => setTimeout(resolve, ms));
export function findBrowser(explicit) {
  if (explicit) return fs.existsSync(explicit) ? explicit : null;
  const candidates = [process.env.EDB_TEST_BROWSER,
    process.env['ProgramFiles(x86)'] && path.join(process.env['ProgramFiles(x86)'], 'Microsoft/Edge/Application/msedge.exe'),
    process.env.ProgramFiles && path.join(process.env.ProgramFiles, 'Google/Chrome/Application/chrome.exe'),
    '/usr/bin/chromium', '/usr/bin/chromium-browser', '/usr/bin/google-chrome'];
  return candidates.find(candidate => candidate && fs.existsSync(candidate)) || null;
}

export async function launchBrowser(executable) {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'edb-tool-browser-'));
  const child = spawn(executable, ['--headless=new', '--remote-debugging-port=0', '--remote-debugging-address=127.0.0.1', '--user-data-dir=' + directory, '--no-first-run', '--no-default-browser-check', '--disable-extensions', '--disable-background-networking', 'about:blank'], {windowsHide:true, stdio:'ignore'});
  let launchError = false, socket, serial = 0;
  child.on('error', () => { launchError = true; });
  const pending = new Map();
  const client = {
    async close() {
      try { if (socket?.readyState === WebSocket.OPEN) await client.call('Browser.close'); } catch { /* Closing terminates the socket too. */ }
      socket?.close();
      for (let attempt=0;attempt<30 && child.exitCode===null;attempt++) await pause(50);
      if (child.exitCode===null) child.kill();
      for (let attempt=0;attempt<20 && child.exitCode===null;attempt++) await pause(50);
      // Only remove the exact isolated profile this invocation created.
      if (path.dirname(path.resolve(directory)) !== path.resolve(os.tmpdir()) || !path.basename(directory).startsWith('edb-tool-browser-')) throw Error('Unexpected browser profile path');
      try { fs.rmSync(directory, {recursive:true,force:true,maxRetries:4,retryDelay:100}); } catch { /* Windows may briefly retain a browser-owned file. */ }
    },
    call(method, params={}) {
      return new Promise((resolve,reject) => {
        const id=++serial;
        const timeout=setTimeout(() => {pending.delete(id);reject(Error('Browser command timed out'));},5000);
        pending.set(id,{resolve,reject,timeout});
        socket.send(JSON.stringify({id,method,params}));
      });
    },
    async evaluate(expression) {
      const result=await client.call('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true,userGesture:true});
      if(result.exceptionDetails) throw Error('Browser page evaluation failed');
      return result.result?.value;
    },
    async load(source) {
      await client.call('Page.navigate',{url:pathToFileURL(source).href});
      let ready=false;
      for(let i=0;i<100;i++) {
        ready=await client.evaluate(`location.href===${JSON.stringify(pathToFileURL(source).href)} && document.readyState==='complete'`);
        if(ready) break;
        await pause(30);
      }
      if(!ready) throw Error('Local page did not finish loading');
      // Simulate clipboard success/failure without touching the Windows clipboard.
      // Capture downloads in memory so tests do not write to a user's Downloads folder.
      await client.evaluate(`(() => {
        window.__edbClipboard={mode:'success',value:null}; window.__edbDownloads=[];
        Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async value=>{if(window.__edbClipboard.mode==='failure')throw Error('Fixture clipboard denial');window.__edbClipboard.value=value;}}});
        const execute=document.execCommand?.bind(document);document.execCommand=(command,...args)=>{if(command==='copy'){if(window.__edbClipboard.mode==='failure')return false;const element=document.activeElement;window.__edbClipboard.value=element?.value?.slice(element.selectionStart,element.selectionEnd)??String(getSelection());return true;}return execute?.(command,...args);};
        const create=URL.createObjectURL.bind(URL); URL.createObjectURL=blob=>{window.__edbDownloadBlob=blob;return create(blob);};
        document.addEventListener('click',event=>{const link=event.target.closest?.('a[download]');if(link){event.preventDefault();window.__edbDownloads.push(link.download);}},true);
        return true;
      })()`);
    }
  };
  try {
    let port;
    for(let attempt=0;attempt<200;attempt++) {
      // Windows browser launchers may exit 0 after handing off to their child.
      if(launchError || (child.exitCode!==null && child.exitCode!==0)) throw Error('Browser startup failed');
      try {port=Number(fs.readFileSync(path.join(directory,'DevToolsActivePort'),'utf8').split('\n')[0]);}catch{}
      if(port)break;
      await pause(50);
    }
    if(!port)throw Error('Browser debug endpoint unavailable');
    const targets=await (await fetch(`http://127.0.0.1:${port}/json/list`,{signal:AbortSignal.timeout(5000)})).json();
    const target=targets.find(target=>target.type==='page');
    if(!target?.webSocketDebuggerUrl)throw Error('Browser page unavailable');
    socket=new WebSocket(target.webSocketDebuggerUrl);
    await new Promise((resolve,reject)=>{socket.addEventListener('open',resolve,{once:true});socket.addEventListener('error',reject,{once:true});});
    socket.addEventListener('message',event=>{
      const message=JSON.parse(event.data), request=pending.get(message.id);
      if(!request)return;
      pending.delete(message.id);clearTimeout(request.timeout);
      message.error?request.reject(Error('Browser protocol rejected command')):request.resolve(message.result);
    });
    socket.addEventListener('close',()=>{for(const request of pending.values()){clearTimeout(request.timeout);request.reject(Error('Browser disconnected'));}pending.clear();});
    await client.call('Page.enable');await client.call('Runtime.enable');await client.call('Network.enable');
    await client.call('Network.setBlockedURLs',{urls:['http://*','https://*']});
    await client.call('Emulation.setEmulatedMedia',{features:[{name:'prefers-reduced-motion',value:'reduce'}]});
    client.version=(await client.call('Browser.getVersion')).product;
    return client;
  } catch(error) {await client.close();throw error;}
}

async function readProperty(client, step) {
  const allowed=new Set(['value','textContent','disabled','hidden','checked','href','selectionStart','selectionEnd','activeId','url','overflow','count','text','exists','childElementCount','rel','target']);
  if(!allowed.has(step.property) && !/^(?:aria|data)-[a-z-]+$/.test(step.property||''))throw Error('Unsupported expectation property');
  return client.evaluate(`(async ({selector,property}) => {
    if(selector==='$clipboard')return window.__edbClipboard.value;
    if(selector==='$downloads')return property==='count'?window.__edbDownloads.length:await window.__edbDownloadBlob?.text();
    if(selector==='$page')return property==='activeId'?document.activeElement.id:property==='overflow'?document.documentElement.scrollWidth>innerWidth:location.href;
    const element=document.querySelector(selector);if(property==='exists')return Boolean(element);if(!element)throw Error('Missing expectation element');
    return /^(aria|data)-/.test(property)?element.getAttribute(property):element[property];
  })(${JSON.stringify({selector:step.selector,property:step.property})})`);
}

export async function runBrowserCases(source,cases,explicitBrowser) {
  const result={status:'NOT RUN',passed:0,failed:0,assertions:0,failures:[],scope:'Real Chromium DOM; clipboard/download APIs simulated; external HTTP(S) blocked.'};
  if(!cases.length)return result;
  const executable=findBrowser(explicitBrowser);
  if(!executable){result.reason='No installed Chromium browser found. Set EDB_TEST_BROWSER or --browser.';return result;}
  let client;
  try {
    client=await launchBrowser(executable);result.browser=client.version;
    for(const test of cases) {
      let assertions=0,stepIndex=-1;
      try {
        if(!Array.isArray(test.steps) || !test.steps.length)throw Error('Browser case needs steps');
        await client.load(source);
        if(test.width)await client.call('Emulation.setDeviceMetricsOverride',{width:test.width,height:800,deviceScaleFactor:1,mobile:false});
        for(const step of test.steps) {
          stepIndex++;
          if(step.action==='expect') {
            if(!Object.hasOwn(step,'equals')&&!Object.hasOwn(step,'includes')&&!Object.hasOwn(step,'endsWith')&&!Array.isArray(step.oneOf))throw Error('Expectation needs a comparison');
            let matches=false;
            for(let i=0;i<80;i++) {
              const actual=await readProperty(client,step);
              matches=Object.hasOwn(step,'equals')?JSON.stringify(actual)===JSON.stringify(step.equals):Array.isArray(step.oneOf)?step.oneOf.some(value=>JSON.stringify(actual)===JSON.stringify(value)):Object.hasOwn(step,'includes')?String(actual).includes(step.includes):String(actual).endsWith(step.endsWith);
              if(matches)break;await pause(25);
            }
            if(!matches)throw Error('Expectation mismatch');assertions++;
          } else if(step.action==='clipboard') {
            if(!['success','failure'].includes(step.mode))throw Error('Invalid clipboard fixture');
            await client.evaluate(`window.__edbClipboard.mode=${JSON.stringify(step.mode)}`);
          } else if(step.action==='viewport') {
            if(!Number.isInteger(step.width)||step.width<240||step.width>3000)throw Error('Invalid viewport');
            await client.call('Emulation.setDeviceMetricsOverride',{width:step.width,height:800,deviceScaleFactor:1,mobile:false});
          } else if(step.action==='key') {
            if(!['Tab','Enter','Escape'].includes(step.key))throw Error('Unsupported test key');
            const key={key:step.key,code:step.key,windowsVirtualKeyCode:{Tab:9,Enter:13,Escape:27}[step.key],nativeVirtualKeyCode:{Tab:9,Enter:13,Escape:27}[step.key]};
            await client.call('Input.dispatchKeyEvent',{...key,type:step.key==='Enter'?'keyDown':'rawKeyDown',...(step.key==='Enter'?{text:'\r',unmodifiedText:'\r'}:{})});
            await client.call('Input.dispatchKeyEvent',{...key,type:'keyUp'});
          } else if(['set','click','focus'].includes(step.action)) {
            await client.evaluate(`(({selector,action,value})=>{const element=document.querySelector(selector);if(!element)throw Error('Missing action element');if(action==='set'){element.value=value;element.dispatchEvent(new Event('input',{bubbles:true}));element.dispatchEvent(new Event('change',{bubbles:true}));}else element[action]();return true;})(${JSON.stringify({selector:step.selector,action:step.action,value:step.value})})`);
          } else throw Error('Unknown browser action');
        }
        if(!assertions)throw Error('Case has no assertions');
        result.passed++;result.assertions+=assertions;
      } catch(error) {result.failed++;const safe=['Expectation mismatch','Browser page evaluation failed','Missing expectation element','Case has no assertions','Browser case needs steps','Unknown browser action','Unsupported test key','Invalid viewport','Unsupported expectation property','Expectation needs a comparison'];result.failures.push({id:test.id,step:stepIndex,reason:safe.includes(error.message)?error.message:'Browser action or case validation failed; inspect the case locally.'});}
    }
    result.status=result.failed?'FAIL':'PASS';
  } catch {result.status='UNKNOWN';result.reason='Browser could not start or connect. Verify the installed browser and local policy.';}
  finally {if(client)await client.close();}
  return result;
}
