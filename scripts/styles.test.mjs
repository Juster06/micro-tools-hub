import test, {before, after} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {ROOT, PILOT, RUNTIME, REQUIRED_SELECTORS, RECORD, configuration, safeFile,
  compile, build, hash, deliveryTag, planPages, normalize} from './build_styles.mjs';

let directory, fixture, inputs, asset;
const snapshot = root => Object.fromEntries([...inputs, RECORD, asset].map(p => [p, hash(fs.readFileSync(path.join(root,p)))]));
function withChanges(changes, action) {
  const saved = new Map();
  try {
    for (const [relative, transform] of changes) {
      const file=path.join(fixture,relative), bytes=fs.readFileSync(file);saved.set(file,bytes);
      if (transform===null)fs.unlinkSync(file);else fs.writeFileSync(file,transform(bytes));
    }
    return action();
  } finally {for(const [file,bytes]of saved)fs.writeFileSync(file,bytes);}
}
before(() => {
  directory=fs.mkdtempSync(path.join(os.tmpdir(),'edb-css-tests-'));fixture=path.join(directory,'repo');fs.mkdirSync(fixture);
  const record=JSON.parse(fs.readFileSync(path.join(ROOT,RECORD),'utf8'));inputs=Object.keys(record.input_sha256);asset=record.output.path;
  for(const relative of [...inputs,RECORD,asset]){
    const target=path.join(fixture,relative);fs.mkdirSync(path.dirname(target),{recursive:true});fs.copyFileSync(path.join(ROOT,relative),target);
  }
  fs.cpSync(path.join(ROOT,'scripts/styles/node_modules'),path.join(fixture,'scripts/styles/node_modules'),{recursive:true,dereference:true});
});
after(() => {
  if(directory){assert.equal(path.dirname(path.resolve(directory)),path.resolve(os.tmpdir()));assert.ok(path.basename(directory).startsWith('edb-css-tests-'));fs.rmSync(directory,{recursive:true,force:true});}
});

test('the explicit scanner covers only the 89 public pages and shared consent script',()=>{
  const {config,source}=configuration(fixture);assert.equal(source.size,90);assert.deepEqual(config.pilot_pages,PILOT);
  assert.equal(config.source_paths.filter(p=>p.endsWith('.html')).length,89);
  assert.ok(config.source_paths.every(p=>!/(?:audit|node_modules|development|templates)\//.test(p)));
});

test('check is repository-read-only and emits the approved static CSS identity',()=>{
  const before=snapshot(fixture),result=build({root:fixture,check:true});
  assert.equal(result.status,'PASS');assert.equal(result.path,asset);assert.ok(result.gzip_bytes<=30*1024);assert.deepEqual(snapshot(fixture),before);
});

test('fresh temporary compiler locations produce identical bytes twice',()=>{
  const first=compile(fixture),second=compile(fixture);assert.deepEqual(first.css,second.css);assert.equal(first.sha256,second.sha256);
  for(const selector of REQUIRED_SELECTORS)assert.ok(first.css.toString('utf8').includes(selector),selector);
  assert.match(first.css.toString('utf8'),/^\/\*! tailwindcss v4\.3\.5 \| MIT License/);
});

test('LF and CRLF source checkouts produce identical generated CSS and manifest validation',()=>{
  withChanges(inputs.map(p=>[p,b=>Buffer.from(normalize(b.toString('utf8')).replaceAll('\n','\r\n'))]),()=>{
    const result=build({root:fixture,check:true});assert.equal(result.path,asset);
  });
});

test('check rejects a changed generated asset without repairing it',()=>{
  withChanges([[asset,b=>Buffer.concat([b,Buffer.from('/* unexpected */')])]],()=>{
    const before=fs.readFileSync(path.join(fixture,asset));assert.throws(()=>build({root:fixture,check:true}),/stale or modified/);assert.deepEqual(fs.readFileSync(path.join(fixture,asset)),before);
  });
});

test('check rejects a missing generated asset',()=>{
  withChanges([[asset,null]],()=>assert.throws(()=>build({root:fixture,check:true}),/ENOENT/));
});

test('check rejects stale recorded inputs without refreshing the manifest',()=>{
  withChanges([['assets/consent.js',b=>Buffer.concat([b,Buffer.from('\n// unrelated edit\n')])]],()=>{
    const before=fs.readFileSync(path.join(fixture,RECORD));assert.throws(()=>build({root:fixture,check:true}),/manifest is stale or modified/);assert.deepEqual(fs.readFileSync(path.join(fixture,RECORD)),before);
  });
});

test('check rejects a changed lockfile even if compilation still succeeds',()=>{
  withChanges([['scripts/styles/package-lock.json',b=>Buffer.from(b.toString('utf8')+'\n')]],()=>assert.throws(()=>build({root:fixture,check:true}),/manifest is stale or modified/));
});

test('missing, wrong, duplicated and moved stylesheet links are rejected',()=>{
  const {source}=configuration(fixture),relative='index.html',tag=deliveryTag(relative,asset),original=source.get(relative);
  for(const broken of [original.replace(tag,''),original.replace(tag,tag.replace(asset,'assets/css/site.0000000000000000.css')),original.replace(tag,tag+'\n'+tag),original.replace(tag,'').replace('</body>',tag+'</body>')]){
    const candidate=new Map(source);candidate.set(relative,broken);assert.throws(()=>planPages(candidate,asset,true),/delivery|head/);
  }
});

test('retained and duplicate runtime compiler references are rejected',()=>{
  const {source}=configuration(fixture),original=source.get('index.html');
  for(const count of [1,2]){const candidate=new Map(source);candidate.set('index.html',original.replace('</head>',RUNTIME.repeat(count)+'</head>'));assert.throws(()=>planPages(candidate,asset,true),/delivery|compiler/);}
});

test('an unapproved eighth public consumer is rejected before compilation',()=>{
  withChanges([['social-counter/index.html',b=>Buffer.from(b.toString('utf8').replace(RUNTIME,deliveryTag('social-counter/index.html',asset)))]],()=>assert.throws(()=>configuration(fixture),/Unapproved stylesheet consumer/));
});

test('scanner allowlist cannot be enlarged or replaced with a traversal path',()=>{
  for(const bad of ['audit/BASELINE_VERIFICATION.json','../outside.html']){
    withChanges([['styles/sources.json',b=>{const config=JSON.parse(b);config.source_paths.push(bad);return Buffer.from(JSON.stringify(config));}]],()=>assert.throws(()=>configuration(fixture),/allowlist differs/));
  }
});

test('explicit path reader rejects traversal, absolute paths and backslashes',()=>{
  for(const p of ['../outside.html','/index.html','C:/index.html','text-cleaner\\index.html','text-cleaner/../index.html'])assert.throws(()=>safeFile(fixture,p),/Unsafe repository-relative/);
});

test('junction or symlink source directory is rejected without reading its target',()=>{
  const target=path.join(fixture,'text-cleaner'),saved=path.join(fixture,'saved-text-cleaner');fs.renameSync(target,saved);
  try {fs.symlinkSync(saved,target,process.platform==='win32'?'junction':'dir');assert.throws(()=>configuration(fixture),/symlink or junction/);}
  finally {if(fs.existsSync(target))fs.unlinkSync(target);fs.renameSync(saved,target);}
});

test('required disabled-state utility cannot disappear from all approved scanner inputs',()=>{
  const {config}=configuration(fixture);
  withChanges(config.source_paths.map(p=>[p,b=>Buffer.from(b.toString('utf8').replaceAll('disabled:opacity-35','disabled:opacity-36'))]),()=>{
    assert.throws(()=>compile(fixture),/Missing required responsive\/dynamic-state utility/);
  });
});

test('input cannot enable ambient or network source discovery',()=>{
  withChanges([['styles/tailwind.input.css',b=>Buffer.from(b.toString('utf8')+'\n@source "../../";\n')]],()=>assert.throws(()=>compile(fixture),/no additional discovery/));
});
