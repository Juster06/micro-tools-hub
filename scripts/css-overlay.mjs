// Exact Task 2C current-source gate; frozen SEO/consent projectors remain unchanged.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
import {historicalSource as seoHistoricalSource} from './seo-overlay.mjs';

const base = 'cf443c3b1facc2ae422fc6c55d546528671be1d0';
const manifestPath = '_publishing/SEO_TASK_2D2_SOURCE_APPROVAL.json';
const identityPath = 'scripts/_publishing_approval_identity.py';
const identitySource = fs.readFileSync(new URL('./_publishing_approval_identity.py', import.meta.url), 'utf8').replaceAll('\r\n', '\n');
const identityMatch = /^# Reviewed bootstrap trust anchor; deliberately outside the self-referential manifest\.\nMANIFEST_SHA256 = '([0-9a-f]{64})'\n$/.exec(identitySource);
if (!identityMatch) throw new Error('Invalid CSS approval bootstrap identity');
const manifestHash = identityMatch[1];
export const pilotPages = new Set(['index.html','text-cleaner/index.html','json-formatter/index.html','csv-viewer/index.html','image-color-picker/index.html','vat-calculator/index.html','batch-filename-planner/index.html']);
const skipped = new Set(['.git','reports','development','scripts/ci/node_modules','scripts/styles/node_modules','scripts/__pycache__','scripts/ci/__pycache__','tests/__pycache__']);
const normalize = source => source.replaceAll('\r\n','\n');
const hash = source => createHash('sha256').update(normalize(source)).digest('hex');
const rootPath = root => path.resolve(root instanceof URL ? fileURLToPath(root) : root);
const decode = bytes => new TextDecoder('utf-8',{fatal:true,ignoreBOM:true}).decode(bytes);

export function safeFile(root, relative, checkedDirectories=null) {
  if (typeof relative !== 'string' || !/^[A-Za-z0-9_.-]+(?:\/[A-Za-z0-9_.-]+)*$/.test(relative) || relative.split('/').some(x=>x==='.'||x==='..')) throw new Error('Unsafe CSS approval path: '+relative);
  const resolved=rootPath(root);let current=resolved;
  const components=[null,...relative.split('/')];let info;
  for(const [position,component] of components.entries()){
    if(component!==null)current=path.join(current,component);
    if(position<components.length-1&&checkedDirectories?.has(current))continue;
    info=fs.lstatSync(current);
    if(info.isSymbolicLink())throw new Error('CSS approval path is a symlink or junction: '+relative);
    if(position<components.length-1){
      if(!info.isDirectory())throw new Error('CSS approval parent is not a directory: '+relative);
      checkedDirectories?.add(current);
    }
  }
  // Lexically safe paths with no linked ancestors remain inside this root.
  // Directory checks are shared only within one validation; file bytes and
  // file lstat results are always fresh, regardless of size or mtime.
  if(!info.isFile())throw new Error('CSS approval path is not an ordinary repository file: '+relative);
  return current;
}

function siteHtmlPaths(root,checkedDirectories) {
  const found=[];
  function visit(directory){
    for(const entry of fs.readdirSync(directory,{withFileTypes:true})){
      const target=path.join(directory,entry.name),relative=path.relative(root,target).split(path.sep).join('/');
      if(skipped.has(relative))continue;
      const info=fs.lstatSync(target);
      if(info.isSymbolicLink())throw new Error('Unexpected deployable symlink/junction: '+relative);
      if(info.isDirectory())visit(target);
      else if(/\.html?$/i.test(entry.name)){safeFile(root,relative,checkedDirectories);found.push(relative);}
    }
  }
  visit(root);return found.sort();
}

export function manifest(root) {
  const raw=decode(fs.readFileSync(safeFile(root,manifestPath)));
  if(hash(raw)!==manifestHash)throw new Error('CSS approval manifest differs from the reviewed candidate');
  if(normalize(decode(fs.readFileSync(safeFile(root,identityPath))))!==identitySource)throw new Error('CSS approval bootstrap identity changed');
  const value=JSON.parse(raw);
  if(value.schema_version!==1||value.base_revision!==base||value.state!=='DEVELOPMENT_CANDIDATE_NOT_DEPLOYED'||JSON.stringify([...value.pilot_pages].sort())!==JSON.stringify([...pilotPages].sort()))throw new Error('CSS approval identity or pilot scope is invalid');
  if(manifestPath in value.files||identityPath in value.files)throw new Error('CSS approval contains a circular trust dependency');
  if([...pilotPages].some(p=>!value.files[p]||!value.transformations[p]))throw new Error('CSS approval is missing an approved pilot page');
  return value;
}

export function validateCurrent(root,capture=null) {
  root=rootPath(root);const value=manifest(root);
  const checkedDirectories=new Set(),htmlSources=new Map();
  for(const [relative,entry]of Object.entries(value.files)){
    let data=fs.readFileSync(safeFile(root,relative,checkedDirectories));
    if(entry.normalization==='utf8-lf')data=Buffer.from(normalize(decode(data)));
    else if(entry.normalization!=='bytes')throw new Error('Unknown CSS approval hash mode');
    if(createHash('sha256').update(data).digest('hex')!==entry.sha256)throw new Error('Unapproved current CSS dependency: '+relative);
    capture?.set(relative,data);
    if(value.site_html_paths.includes(relative))htmlSources.set(relative,decode(data));
  }
  if(JSON.stringify(siteHtmlPaths(root,checkedDirectories))!==JSON.stringify([...value.site_html_paths].sort()))throw new Error('Unapproved HTML route or consumer set');
  const asset=value.css_asset;
  if(!value.files[asset.path]||value.files[asset.path].sha256!==asset.sha256||value.files[asset.path].normalization!=='bytes'||!/^assets\/css\/site\.[0-9a-f]{16}\.css$/.test(asset.path)||asset.path.split('.').at(-2)!==asset.sha256.slice(0,16))throw new Error('CSS asset path/hash is outside the approved naming policy');
  for(const relative of value.site_html_paths){
    const source=htmlSources.get(relative);
    if(pilotPages.has(relative)){
      const link=value.transformations[relative].stylesheet_tag;
      if(source.split(link).length!==2||source.includes('@tailwindcss/browser'))throw new Error('Missing/duplicate stylesheet or retained compiler: '+relative);
      if(!source.split('</head>',1)[0].includes(link))throw new Error('Stylesheet moved outside head: '+relative);
    }else if(source.includes(asset.path.split('/').at(-1)))throw new Error('Unapproved stylesheet consumer: '+relative);
  }
  return value;
}

function hasPolicy(root,source=''){
  return [manifestPath,identityPath,'styles/build-manifest.json'].some(p=>fs.existsSync(path.join(rootPath(root),p)))||source.includes('assets/css/site.');
}

function project(value,relative,source){
  const entry=value.transformations[relative];if(!entry)return source;
  if(hash(source)!==entry.candidate_sha256)throw new Error('Unapproved CSS source argument: '+relative);
  let previous=normalize(source);
  for(const operation of [...entry.operations].reverse()){
    // Offsets are Unicode scalar positions, matching Python's manifest generator.
    const chars=Array.from(previous),start=operation.candidate_start,end=operation.candidate_end;
    if(chars.slice(start,end).join('')!==operation.candidate)throw new Error('CSS transformation differs from the approved position');
    previous=chars.slice(0,start).join('')+operation.previous+chars.slice(end).join('');
  }
  if(hash(previous)!==entry.previous_sha256)throw new Error('CSS candidate does not reconstruct the exact main preimage');
  return source.includes('\r\n')?previous.replaceAll('\n','\r\n'):previous;
}

export function preCssSource(root,relative,source){
  if(!hasPolicy(root,source))return source;
  return project(validateCurrent(root),relative,source);
}

export function historicalSource(root,relative,source){
  return seoHistoricalSource(root,relative,preCssSource(root,relative,source));
}

// Preservation-only readers of an immutable, fully validated snapshot. These
// never report live approval: validateCurrent remains a fresh filesystem gate.
export function historicalSnapshot(root){
  const boundRoot=rootPath(root),url=pathToFileURL(boundRoot+path.sep),captured=new Map();
  const value=validateCurrent(boundRoot,captured),projected=new Map();
  const seo=JSON.parse(decode(captured.get('audit/SEO_TASK_2A_SOURCE_OVERLAY.json')));
  for(const [relative,data] of captured){
    if(!(relative in value.transformations)&&!(relative in seo.pages))continue;
    let previous=project(value,relative,decode(data));
    if(relative in seo.pages){
      previous=seoHistoricalSource(url,relative,previous);
      if(hash(previous)!==seo.pages[relative].previous_sha256)throw new Error('Snapshot does not reconstruct captured SEO evidence: '+relative);
    }
    const bytes=Buffer.from(previous);
    if(!bytes.equals(data))projected.set(relative,bytes);
  }
  function snapshotSource(candidateRoot,relative,source){
    if(rootPath(candidateRoot)!==boundRoot||!captured.has(relative))throw new Error('Historical snapshot root/path is not bound');
    const data=Buffer.from(value.files[relative].normalization==='utf8-lf'?normalize(source):source);
    if(!data.equals(captured.get(relative)))throw new Error('Source differs from the immutable historical snapshot: '+relative);
    if(!projected.has(relative))return source;
    const previous=decode(projected.get(relative));
    return source.includes('\r\n')?previous.replaceAll('\n','\r\n'):previous;
  }
  return Object.freeze({historicalSource:snapshotSource});
}
