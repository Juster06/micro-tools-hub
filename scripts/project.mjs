// Compatibility API: the Python standard-library engine owns all tracking rules.
import path from 'node:path';
import crypto from 'node:crypto';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
export const normalizedHash=text=>crypto.createHash('sha256').update(text.replace(/\r\n/g,'\n').trimEnd()).digest('hex');

function bridge(action,registry) {
  const candidates=process.env.WEBUTILS_PYTHON ? [[process.env.WEBUTILS_PYTHON,[]]] : [['python',[]],['python3',[]],['py',['-3']]];
  for(const [executable,prefix]of candidates) {
    const result=spawnSync(executable,[...prefix,path.join(root,'scripts','tracking.py'),'--bridge',action,'--root',root],{encoding:'utf8',input:registry===undefined?'':JSON.stringify(registry),maxBuffer:32*1024*1024,timeout:60000,windowsHide:true});
    if(result.status===0) {
      try { return JSON.parse(result.stdout); } catch { /* Try another Python launcher. */ }
    }
  }
  throw new Error('Python 3.10+ is required for the tracking engine. Set WEBUTILS_PYTHON to its executable if needed.');
}
const messages=result=>result.errors.map(item=>item.code==='ROOT_FIELDS'?'Missing registry root fields':item.message);
export const validateRegistry=registry=>messages(bridge('registry',registry));
export const validateProject=registry=>messages(bridge('project',registry));
export const summarize=registry=>bridge('summary',registry);

if(process.argv[1] && path.resolve(process.argv[1])===fileURLToPath(import.meta.url)) {
  try {
    const action=process.argv[2]||'check';
    if(!['check','sync','summary'].includes(action))throw new Error('Usage: node scripts/project.mjs [check|sync|summary]');
    const result=bridge({check:'project',sync:'sync',summary:'summary'}[action]);
    if(action==='summary')console.log(JSON.stringify(result,null,2));
    else if(result.errors.length){console.error(messages(result).join('\n'));process.exitCode=1;}
    else console.log(action==='sync'?'Generated registry documents synchronized by Python.':`PASS: registry, source evidence, links and generated documents agree (${result.warnings.length} warnings).`);
  }catch(error){console.error(error.message);process.exitCode=1;}
}
