import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {validateCurrent} from './css-overlay.mjs';
const root=new URL('../',import.meta.url),read=p=>fs.readFileSync(new URL(p,root),'utf8');
function luminance(hex){const v=hex.match(/[0-9a-f]{2}/gi).map(s=>parseInt(s,16)/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4);return .2126*v[0]+.7152*v[1]+.0722*v[2];}
test('Option B small text and action contrast meets AA for declared pairs',()=>{
 for(const [a,b] of [['172B3A','FFFFFF'],['172B3A','F6F9FC'],['526477','FFFFFF'],['526477','F6F9FC'],['FFFFFF','0F766E'],['FFFFFF','115E59'],['0F766E','F0FDFA'],['0F2742','FFFFFF']]){
  const values=[luminance(a),luminance(b)].sort((a,b)=>b-a);assert.ok((values[0]+.05)/(values[1]+.05)>=4.5,`${a} on ${b}`);
 }
});
test('Option B focus and control boundary contrast meet 3:1',()=>{
 for(const a of ['1D4ED8','64748B'])for(const b of ['FFFFFF','F6F9FC']){const v=[luminance(a),luminance(b)].sort((a,b)=>b-a);assert.ok((v[0]+.05)/(v[1]+.05)>=3);}
});
test('homepage interactions use local text rendering without input telemetry or persistence',()=>{
 const source=read('styles/homepage.js');assert.doesNotMatch(source,/innerHTML|outerHTML|insertAdjacentHTML|localStorage|sessionStorage|fetch\s*\(|sendBeacon|gtag\s*\(/);assert.match(source,/textContent/);
 const html=read('index.html');assert.doesNotMatch(html,/@tailwindcss\/browser|noindex/);assert.equal((html.match(/rel="canonical"/g)||[]).length,1);
});
test('Task 2D current approval binds own asset and frozen predecessor',()=>{
 const value=validateCurrent(root);assert.equal(value.parent_revision,'20ecae29a1f20d7903946d6cf00c3897307ee766');assert.ok(value.files[value.homepage_asset]);assert.ok(value.files['audit/SEO_TASK_2C_SOURCE_APPROVAL.json']);assert.ok(value.files['styles/homepage-directory.json']);
});
