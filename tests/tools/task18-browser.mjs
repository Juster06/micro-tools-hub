import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import {launchBrowser,findBrowser} from '../../scripts/tool-tests/browser.mjs';
export async function start() { return launchBrowser(findBrowser()); }
export function source(id) { return fileURLToPath(new URL(`../../${id}/index.html`,import.meta.url)); }
export async function wait(b,expression) {
  const until=Date.now()+5000;
  while(Date.now()<until) { if(await b.evaluate(`Boolean(${expression})`)) return; await new Promise(r=>setTimeout(r,25)); }
  assert.fail(`Expected browser state: ${expression}`);
}
export async function set(b,id,value,event='input') {
  return b.evaluate(`(()=>{const e=document.getElementById(${JSON.stringify(id)});e.value=${JSON.stringify(value)};e.dispatchEvent(new Event(${JSON.stringify(event)},{bubbles:true}));return true})()`);
}
export async function click(b,id) { return b.evaluate(`document.getElementById(${JSON.stringify(id)}).click();true`); }
export async function upload(b,expression) {
  return b.evaluate(`(()=>{const dt=new DataTransfer();dt.items.add(${expression});const e=document.getElementById('toolInput');e.files=dt.files;e.dispatchEvent(new Event('change',{bubbles:true}));return true})()`);
}
export async function widths(b) {
  for(const width of [320,375,768,1440]) {
    await b.call('Emulation.setDeviceMetricsOverride',{width,height:900,deviceScaleFactor:1,mobile:width<500});
    assert.equal(await b.evaluate('document.documentElement.scrollWidth>innerWidth'),false,`overflow at ${width}`);
  }
  await b.call('Emulation.clearDeviceMetricsOverride');
}
export async function noTransport(b,action) {
  await b.evaluate(`window.__transports=[];for(const key of ['fetch','WebSocket','XMLHttpRequest'])window[key]=function(){window.__transports.push(key);throw Error('Unexpected transport')};navigator.sendBeacon=()=>{window.__transports.push('beacon');return false};true`);
  await action(); assert.deepEqual(await b.evaluate('window.__transports'),[]);
}
