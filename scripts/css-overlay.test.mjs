import {test,after} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {pathToFileURL,fileURLToPath} from 'node:url';
import {execFileSync,spawnSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {validateCurrent,preCssSource,historicalSource,historicalSnapshot,safeFile,pilotPages} from './css-overlay.mjs';

const root=new URL('../',import.meta.url),rootDirectory=fileURLToPath(root);
const approval=validateCurrent(root);
const parent=fs.mkdtempSync(path.join(os.tmpdir(),'edb-css-node-'));
const fixture=path.join(parent,'repo');fs.mkdirSync(fixture);
for(const name of [...Object.keys(approval.files),'_publishing/SEO_TASK_2E5_SOURCE_APPROVAL.json','scripts/_readme_publishing_approval_identity.py']){
  const target=path.join(fixture,name);fs.mkdirSync(path.dirname(target),{recursive:true});fs.copyFileSync(path.join(rootDirectory,name),target);
}
const fixtureURL=pathToFileURL(fixture+path.sep);
const hash=text=>createHash('sha256').update(text.replaceAll('\r\n','\n')).digest('hex');
function mutate(name,run,transform=raw=>Buffer.concat([raw,Buffer.from('\nunauthorized')])){
  const filename=path.join(fixture,name),raw=fs.readFileSync(filename);
  try{fs.writeFileSync(filename,transform(raw));run();}finally{fs.writeFileSync(filename,raw);}
}
function pythonResult(directory,relative=null){
  const code='import json,sys;from pathlib import Path;sys.path.insert(0,sys.argv[1]);import css_overlay as c;r=Path(sys.argv[2]);v=c.validate_current(r);print(json.dumps({"asset":v["css_asset"]["sha256"],"files":len(v["files"]),"projected":c.digest(c.pre_css_source(r,sys.argv[3],(r/sys.argv[3]).read_bytes().decode("utf-8"))) if len(sys.argv)>3 else None}))';
  return spawnSync(process.env.WEBUTILS_PYTHON||'python',['-c',code,path.join(rootDirectory,'scripts'),directory,...(relative?[relative]:[])],{encoding:'utf8',windowsHide:true,timeout:60000});
}
after(()=>{
  const resolved=path.resolve(parent);
  if(path.dirname(resolved)!==path.resolve(os.tmpdir())||!path.basename(resolved).startsWith('edb-css-node-'))throw Error('Unsafe test cleanup path');
  fs.rmSync(resolved,{recursive:true,force:true});
});

test('Node gate validates the full seven-page candidate and exact asset',()=>{
  const value=validateCurrent(fixtureURL);assert.equal(value.pilot_pages.length,7);assert.equal(value.site_html_paths.length,92);
  assert.equal(createHash('sha256').update(fs.readFileSync(path.join(fixture,value.css_asset.path))).digest('hex'),value.css_asset.sha256);
});
test('all seven candidates reconstruct the actual main commit with Python/Node parity',()=>{
  for(const relative of pilotPages){
    const source=fs.readFileSync(new URL(relative,root),'utf8');
    const baseline=execFileSync('git',['show','cf443c3b1facc2ae422fc6c55d546528671be1d0:'+relative],{cwd:rootDirectory,encoding:'utf8',windowsHide:true});
    assert.equal(preCssSource(root,relative,source).replaceAll('\r\n','\n'),baseline.replaceAll('\r\n','\n'));
    const result=pythonResult(rootDirectory,relative);assert.equal(result.status,0,result.stderr);
    assert.equal(JSON.parse(result.stdout).projected,hash(baseline));
  }
});
test('frozen SEO chain still reconstructs exact historical hashes',()=>{
  const seo=JSON.parse(fs.readFileSync(new URL('audit/SEO_TASK_2A_SOURCE_OVERLAY.json',root),'utf8'));
  for(const relative of pilotPages)assert.equal(hash(historicalSource(root,relative,fs.readFileSync(new URL(relative,root),'utf8'))),seo.pages[relative].previous_sha256);
});
test('missing/wrong/duplicated/moved CSS links and compiler insertions fail closed',()=>{
  const tag=approval.transformations['index.html'].stylesheet_tag;
  const script='<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>';
  for(const transform of [s=>s.replace(tag,''),s=>s.replace(tag,tag+tag),s=>s.replace(tag,'<link rel="stylesheet" href="wrong.css">'),s=>s.replace(tag,'').replace('</body>',tag+'</body>'),s=>s.replace('</head>',script+'</head>'),s=>s.replace('</head>',script+script+'</head>')])mutate('index.html',()=>assert.throws(()=>validateCurrent(fixtureURL)),raw=>Buffer.from(transform(raw.toString('utf8'))));
});
test('changed and missing CSS bytes prevent historical projection in both runtimes',()=>{
  const source=fs.readFileSync(path.join(fixture,'index.html'),'utf8');
  mutate(approval.css_asset.path,()=>{assert.throws(()=>historicalSource(fixtureURL,'index.html',source));assert.notEqual(pythonResult(fixture).status,0);});
  const target=path.join(fixture,approval.css_asset.path),raw=fs.readFileSync(target);
  try{fs.unlinkSync(target);assert.throws(()=>validateCurrent(fixtureURL));assert.notEqual(pythonResult(fixture).status,0);}finally{fs.writeFileSync(target,raw);}
});
test('CSS line endings are exact bytes and Git checkout policy is bound',()=>{
  assert.equal(approval.files[approval.css_asset.path].normalization,'bytes');
  mutate(approval.css_asset.path,()=>{assert.throws(()=>validateCurrent(fixtureURL));assert.notEqual(pythonResult(fixture).status,0);},raw=>Buffer.from(raw.toString('utf8').replaceAll('\n','\r\n')));
  mutate('.gitattributes',()=>assert.throws(()=>validateCurrent(fixtureURL)));
});
test('canonical, body, consent and source-argument mutations are rejected',()=>{
  for(const relative of ['json-formatter/index.html','assets/consent.js','privacy.html'])mutate(relative,()=>assert.throws(()=>validateCurrent(fixtureURL)));
  const source=fs.readFileSync(path.join(fixture,'index.html'),'utf8');
  assert.throws(()=>preCssSource(fixtureURL,'index.html',source+' '));
  mutate('index.html',()=>assert.throws(()=>validateCurrent(fixtureURL)),raw=>Buffer.from(raw.toString('utf8').replace('rel="canonical"','rel="alternate"')));
});
test('manifest/bootstrap, lock, build, CI and historical evidence tamper is rejected',()=>{
  for(const relative of ['_publishing/SEO_TASK_2D2_SOURCE_APPROVAL.json','scripts/_publishing_approval_identity.py','_publishing/SEO_TASK_2D2_OUTPUT_POLICY.json','_publishing/SEO_TASK_2E1_SOURCE_APPROVAL.json','scripts/_historical_publishing_approval_identity.py','_config.yml','_publishing/output-policy.json','_publishing/verify_site.py','audit/SEO_TASK_2D_SOURCE_APPROVAL.json','scripts/homepage_approval_identity.py','styles/homepage-directory.json','styles/homepage.js','styles/homepage.css',approval.homepage_asset,'audit/SEO_TASK_2C_SOURCE_APPROVAL.json','scripts/css_approval_identity.py','scripts/styles/package-lock.json','styles/sources.json','styles/build-manifest.json','scripts/build_styles.mjs','.github/workflows/functional-ci.yml','scripts/ci/run.py','scripts/ci/coverage.json','audit/SEO_TASK_2A_SOURCE_OVERLAY.json','audit/TASK_17_CANDIDATE.json','scripts/seo_overlay.py','scripts/seo-overlay.mjs','scripts/consent_overlay.py'])mutate(relative,()=>assert.throws(()=>validateCurrent(fixtureURL)));
});
test('same-size same-mtime source tamper cannot hide behind a cache',()=>{
  const filename=path.join(fixture,approval.css_asset.path),info=fs.statSync(filename),raw=fs.readFileSync(filename);
  try{const modified=Buffer.from(raw);modified[0]^=1;fs.writeFileSync(filename,modified);fs.utimesSync(filename,info.atime,info.mtime);assert.throws(()=>validateCurrent(fixtureURL));}finally{fs.writeFileSync(filename,raw);}
});

test('Phase A selection and frozen predecessor remain strict in Python and Node',()=>{
  assert.equal(approval.phase_a_parent_revision,'34992b8f8ac3e73efbea820bb18c96dae145ff19');
  for(const relative of ['_publishing/SEO_TASK_2E3_SOURCE_APPROVAL.json','scripts/_phase_a_publishing_approval_identity.py','_publishing/SEO_TASK_2E3_OUTPUT_POLICY.json','_publishing/SEO_TASK_2E3_SCOPE.json','_publishing/SEO_TASK_2E2_CLEANUP_CANDIDATES.json','_publishing/SEO_TASK_2E1_SOURCE_APPROVAL.json','scripts/_historical_publishing_approval_identity.py','_publishing/output-policy.json']){
    mutate(relative,()=>{assert.throws(()=>validateCurrent(fixtureURL));assert.notEqual(pythonResult(fixture).status,0);});
  }
});
test('unapproved consumer and unapproved HTML route are rejected',()=>{
  const tag=approval.transformations['text-cleaner/index.html'].stylesheet_tag;
  mutate('social-counter/index.html',()=>assert.throws(()=>validateCurrent(fixtureURL)),raw=>Buffer.from(raw.toString('utf8').replace('</head>',tag+'</head>')));
  const directory=path.join(fixture,'unexpected-route');fs.mkdirSync(directory);
  try{for(const name of ['index.html','index.htm']){fs.writeFileSync(path.join(directory,name),'<title>Unapproved</title>');assert.throws(()=>validateCurrent(fixtureURL));fs.unlinkSync(path.join(directory,name));}}finally{fs.rmdirSync(directory);}
});

test('two-report successor and original source evidence remain bound in both runtimes',()=>{
  assert.equal(approval.security_report_parent_revision,'eec8027b7b4c293fd4ce9e5dfd4a2bb490d61b20');
  for(const relative of ['_publishing/SEO_TASK_2E4_SOURCE_APPROVAL.json','scripts/_privacy_publishing_approval_identity.py',
    '_publishing/SEO_TASK_2E4_OUTPUT_POLICY.json','_publishing/SEO_TASK_2E4_SCOPE.json','_publishing/SEO_TASK_2E4_PHASE_B.md',
    'audit/TASK_21_SECURITY_REVIEW.json','audit/TASK_22_SECURITY_REVIEW.json']){
    mutate(relative,()=>{assert.throws(()=>validateCurrent(fixtureURL));assert.notEqual(pythonResult(fixture).status,0);});
  }
});
test('README successor and frozen two-report approval remain bound in both runtimes',()=>{
  assert.equal(approval.readme_parent_revision,'e907ae793525ab6c6a45bad5b2e19eab10f0c657');
  for(const relative of ['_publishing/SEO_TASK_2E5_SOURCE_APPROVAL.json','scripts/_readme_publishing_approval_identity.py',
    '_publishing/SEO_TASK_2E5_OUTPUT_POLICY.json','_publishing/SEO_TASK_2E5_SCOPE.json','_publishing/SEO_TASK_2E5_PHASE_B.txt',
    '_publishing/SEO_TASK_2E4_SOURCE_APPROVAL.json','scripts/_privacy_publishing_approval_identity.py',
    'README.md','youtube-title-checker/README.md']){
    mutate(relative,()=>{assert.throws(()=>validateCurrent(fixtureURL));assert.notEqual(pythonResult(fixture).status,0);});
  }
});
test('nested generated-directory names cannot hide an unapproved HTML route',()=>{
  const outer=path.join(fixture,'unexpected-route');fs.mkdirSync(outer);
  try{
    for(const name of ['reports','development','node_modules','__pycache__','.git']){
      const directory=path.join(outer,name);fs.mkdirSync(directory);
      try{fs.writeFileSync(path.join(directory,'index.html'),'<title>Unapproved</title>');assert.throws(()=>validateCurrent(fixtureURL));assert.notEqual(pythonResult(fixture).status,0);}finally{fs.unlinkSync(path.join(directory,'index.html'));fs.rmdirSync(directory);}
    }
  }finally{fs.rmdirSync(outer);}
});
test('lexical escapes and linked directory traversal fail before reads',()=>{
  for(const relative of ['../outside','/index.html','C:/outside','assets\\consent.js','index.html/../privacy.html','%2e%2e/outside'])assert.throws(()=>safeFile(fixtureURL,relative));
  const outside=path.join(parent,'outside'),link=path.join(fixture,'linked-directory');fs.mkdirSync(outside);fs.writeFileSync(path.join(outside,'file.txt'),'external fixture');
  fs.symlinkSync(outside,link,'junction');
  try{assert.throws(()=>safeFile(fixtureURL,'linked-directory/file.txt'));assert.throws(()=>validateCurrent(fixtureURL));assert.equal(fs.readFileSync(path.join(outside,'file.txt'),'utf8'),'external fixture');}finally{fs.unlinkSync(link);}
});
test('old baseline cannot silently satisfy current static CSS approval',()=>{
  const old=execFileSync('git',['show','cf443c3b1facc2ae422fc6c55d546528671be1d0:index.html'],{cwd:rootDirectory,encoding:'utf8',windowsHide:true});
  assert.throws(()=>preCssSource(fixtureURL,'index.html',old));
});
test('CRLF and LF retain exact trailing-byte policy across the new projection',()=>{
  const source=fs.readFileSync(path.join(fixture,'index.html'),'utf8').replaceAll('\r\n','\n');
  const lf=preCssSource(fixtureURL,'index.html',source),crlf=preCssSource(fixtureURL,'index.html',source.replaceAll('\n','\r\n'));
  assert.equal(crlf,lf.replaceAll('\n','\r\n'));assert.throws(()=>preCssSource(fixtureURL,'index.html',source+' '));
});
test('immutable historical snapshot remains evidence while live tamper is rejected',()=>{
  const snapshot=historicalSnapshot(fixtureURL),source=fs.readFileSync(path.join(fixture,'index.html'),'utf8');
  const expected=snapshot.historicalSource(fixtureURL,'index.html',source);
  mutate(approval.css_asset.path,()=>{
    assert.equal(snapshot.historicalSource(fixtureURL,'index.html',source),expected);
    assert.throws(()=>validateCurrent(fixtureURL));assert.throws(()=>historicalSnapshot(fixtureURL));
    assert.throws(()=>historicalSource(fixtureURL,'index.html',source));
  });
});
test('historical snapshot rejects unbound roots paths and changed source',()=>{
  const snapshot=historicalSnapshot(fixtureURL),source=fs.readFileSync(path.join(fixture,'index.html'),'utf8');
  assert.throws(()=>snapshot.historicalSource(root,'index.html',source));
  assert.throws(()=>snapshot.historicalSource(fixtureURL,'unknown.html',source));
  assert.throws(()=>snapshot.historicalSource(fixtureURL,'index.html',source+' '));
});
test('snapshot rejects frozen projector fallback after verified capture',()=>{
  const exists=fs.existsSync;
  fs.existsSync=filename=>String(filename).includes('SEO_TASK_2A_SOURCE_OVERLAY.json')?false:exists(filename);
  try{assert.throws(()=>historicalSnapshot(fixtureURL),/captured SEO evidence/);}finally{fs.existsSync=exists;}
});
