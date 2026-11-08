// Development-only, deterministic static CSS build. --check never writes the repository.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {gzipSync} from 'node:zlib';
import {spawnSync} from 'node:child_process';

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
export const VERSION = '4.3.5';
export const BASE = 'cf443c3b1facc2ae422fc6c55d546528671be1d0';
export const PILOT = ['index.html', 'text-cleaner/index.html', 'json-formatter/index.html',
  'csv-viewer/index.html', 'image-color-picker/index.html', 'vat-calculator/index.html',
  'batch-filename-planner/index.html'];
export const RUNTIME = '<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>';
export const REQUIRED_SELECTORS = ['.hidden', '.block', '.text-amber-300', '.text-slate-500',
  '.disabled\\:opacity-35', '.disabled\\:opacity-40', '.disabled\\:cursor-not-allowed',
  '.active\\:bg-indigo-700', '.hover\\:text-indigo-200', '.sm\\:text-5xl', '.sm\\:px-8'];
export const RECORD = 'styles/build-manifest.json';
const INPUT = 'styles/tailwind.input.css';
const CONFIG = 'styles/sources.json';
const PACKAGE = 'scripts/styles/package.json';
const LOCK = 'scripts/styles/package-lock.json';
const BUILDER = 'scripts/build_styles.mjs';
export const WORDING = {
  'index.html': ['Tool processing runs locally; styling loads from Tailwind’s Play CDN.', 'Tool processing runs locally; styles load from this site.'],
  'text-cleaner/index.html': ['All text processing happens in this browser; only the Tailwind styling script loads externally.', 'All text processing happens in this browser. Styles load from this site; hosting requests and optional consented analytics still occur.'],
  'json-formatter/index.html': ['Page delivery and Tailwind Play CDN styling make ordinary network requests; inline CSS keeps the page usable without the CDN.', 'Page and first-party style delivery make ordinary network requests; inline CSS keeps the page usable if the stylesheet is unavailable.'],
  'csv-viewer/index.html': ['Hosting and the existing styling CDN are separate network requests.', 'Page and first-party style delivery make ordinary hosting requests.'],
  'image-color-picker/index.html': ['Hosting and the existing styling CDN are separate network requests.', 'Page and first-party style delivery make ordinary hosting requests.'],
  'vat-calculator/index.html': ['Page/style delivery uses hosting and the existing Tailwind Play CDN; inline fallback styling works without the CDN.', 'Page and first-party style delivery use hosting; inline fallback styling works if the stylesheet is unavailable.'],
};
export const normalize = text => text.replaceAll('\r\n', '\n');
export const hash = bytes => createHash('sha256').update(bytes).digest('hex');
const samePath = (left, right) => process.platform === 'win32' ? left.toLowerCase() === right.toLowerCase() : left === right;
const read = (root, relative) => fs.readFileSync(safeFile(root, relative), 'utf8');

export function safeFile(root, relative) {
  root = path.resolve(root);
  if (typeof relative !== 'string' || !/^[a-zA-Z0-9_@.-]+(?:\/[a-zA-Z0-9_@.-]+)*$/.test(relative) || relative.split('/').some(p => p === '.' || p === '..')) {
    throw Error('Unsafe repository-relative CSS input path');
  }
  let current = root;
  for (const component of relative.split('/')) {
    current = path.join(current, component);
    if (fs.lstatSync(current).isSymbolicLink()) throw Error('CSS input path must not traverse a symlink or junction: ' + relative);
  }
  if (!fs.statSync(current).isFile() || !samePath(fs.realpathSync(current), current)) throw Error('CSS input is not an ordinary file: ' + relative);
  return current;
}

export function configuration(root = ROOT) {
  const config = JSON.parse(read(root, CONFIG));
  const registry = JSON.parse(read(root, 'TOOL_REGISTRY.json'));
  const expected = ['index.html', 'privacy.html', 'assets/consent.js', ...registry.tools.filter(t => t.status === 'RELEASED').map(t => t.directory_path + '/index.html')].sort();
  if (config.schema_version !== 1 || config.base_revision !== BASE || JSON.stringify(config.pilot_pages) !== JSON.stringify(PILOT)
      || JSON.stringify(config.source_paths) !== JSON.stringify(expected) || new Set(expected).size !== 90) {
    throw Error('CSS source/consumer allowlist differs from the approved 89-page baseline');
  }
  const source = new Map(config.source_paths.map(p => [p, read(root, p)]));
  for (const [relative, text] of source) {
    if (relative.endsWith('.html') && !PILOT.includes(relative) && /assets\/css\/site\.[a-f0-9]+\.css/.test(text)) {
      throw Error('Unapproved stylesheet consumer: ' + relative);
    }
  }
  return {config, source};
}

function packages(root) {
  const value = JSON.parse(read(root, PACKAGE));
  const lock = JSON.parse(read(root, LOCK));
  const expected = {'@tailwindcss/cli': VERSION, tailwindcss: VERSION};
  if (JSON.stringify(value.devDependencies) !== JSON.stringify(expected) || lock.lockfileVersion !== 3
      || JSON.stringify(lock.packages[''].devDependencies) !== JSON.stringify(expected)) throw Error('CSS compiler dependencies are not exactly pinned');
  for (const name of Object.keys(expected)) {
    const installed = JSON.parse(read(root, 'scripts/styles/node_modules/' + name + '/package.json'));
    const recorded = lock.packages['node_modules/' + name];
    if (installed.version !== VERSION || recorded.version !== VERSION || !recorded.integrity?.startsWith('sha512-') || !recorded.resolved?.startsWith('https://registry.npmjs.org/')) {
      throw Error('Installed/locked CSS compiler version differs; run the documented npm ci command');
    }
  }
  return {cli: safeFile(root, 'scripts/styles/node_modules/@tailwindcss/cli/dist/index.mjs'),
    css: safeFile(root, 'scripts/styles/node_modules/tailwindcss/index.css')};
}

export function compile(root = ROOT) {
  root = path.resolve(root);
  const {config, source} = configuration(root);
  const compiler = packages(root);
  const input = read(root, INPUT);
  const importTag = '@import "tailwindcss" source(none);';
  if (input.split(importTag).length !== 2 || (input.match(/@(?:import|source)\b/g) || []).length !== 1) throw Error('CSS input must have exactly the pinned local import and no additional discovery');
  const scratch = fs.mkdtempSync(path.join(os.tmpdir(), 'edb-static-css-'));
  try {
    const scans = path.join(scratch, 'sources'); fs.mkdirSync(scans);
    for (const [index, [relative, text]] of [...source].entries()) {
      fs.writeFileSync(path.join(scans, String(index).padStart(3, '0') + path.extname(relative)), normalize(text), 'utf8');
    }
    const importPath = compiler.css.replaceAll('\\', '/');
    if (/["\n\r]/.test(importPath)) throw Error('Unsupported compiler installation path');
    const staged = input.replace(importTag, '@import "' + importPath + '" source(none);') + '\n@source "./sources";\n';
    const inputPath = path.join(scratch, 'input.css'), outputPath = path.join(scratch, 'output.css');
    fs.writeFileSync(inputPath, normalize(staged), 'utf8');
    const result = spawnSync(process.execPath, [compiler.cli, '-i', inputPath, '-o', outputPath, '--minify'],
      {cwd:scratch, windowsHide:true, encoding:'utf8', timeout:60000, maxBuffer:1024*1024});
    if (result.error || result.status !== 0) throw Error('Pinned CSS compiler failed: ' + (result.error?.message || result.stderr || result.stdout));
    const css = fs.readFileSync(outputPath);
    if (!css.length || /@import\b|url\(\s*["']?\s*(?:https?:|\/\/)/i.test(css.toString('utf8'))) throw Error('Generated CSS is empty or has an external dependency');
    for (const selector of REQUIRED_SELECTORS) {
      if (!css.toString('utf8').includes(selector)) throw Error('Missing required responsive/dynamic-state utility: ' + selector);
    }
    const compressed = gzipSync(css, {level:9}).length;
    if (compressed > 50 * 1024) throw Error('Generated CSS exceeds the reviewed 50 KiB gzip ceiling; stop for budget review');
    return {css, gzipBytes:compressed, sha256:hash(css), config, source};
  } finally {
    if (!samePath(path.dirname(path.resolve(scratch)), path.resolve(os.tmpdir())) || !path.basename(scratch).startsWith('edb-static-css-')) throw Error('Unsafe CSS scratch cleanup target');
    fs.rmSync(scratch, {recursive:true, force:true});
  }
}

export function deliveryTag(relative, asset) {
  return '<link rel="stylesheet" href="' + (relative === 'index.html' ? '' : '../') + asset + '">';
}

export function planPages(source, asset, check = false) {
  const planned = new Map();
  for (const relative of PILOT) {
    let text = source.get(relative);
    const tag = deliveryTag(relative, asset);
    if (check) {
      if (text.split(tag).length !== 2 || /@tailwindcss\/browser/.test(text)) throw Error('Missing, duplicate or stale pilot CSS delivery: ' + relative);
    } else {
      const priorLinks = [...text.matchAll(/<link rel="stylesheet" href="(?:\.\.\/)?assets\/css\/site\.[a-f0-9]{16}\.css">/g)];
      if (text.split(RUNTIME).length === 2 && priorLinks.length === 0) text = text.replace(RUNTIME, tag);
      else if (!/@tailwindcss\/browser/.test(text) && priorLinks.length === 1) text = text.replace(priorLinks[0][0], tag);
      else throw Error('Unexpected CSS delivery state: ' + relative);
      const wording = WORDING[relative];
      if (wording && text.includes(wording[0])) {
        if (text.split(wording[0]).length !== 2) throw Error('Unexpected styling wording multiplicity');
        text = text.replace(wording[0], wording[1]);
      }
    }
    if (text.split(tag).length !== 2 || /@tailwindcss\/browser/.test(text)) throw Error('Unexpected pilot compiler reference');
    const head = text.match(/<head>([\s\S]*?)<\/head>/i)?.[1];
    if (!head || !head.includes(tag)) throw Error('Stylesheet must remain in the head: ' + relative);
    planned.set(relative, text);
  }
  return planned;
}

export function recordFor(root, result, source) {
  const asset = 'assets/css/site.' + result.sha256.slice(0, 16) + '.css';
  const inputs = Object.fromEntries([...source].map(([relative, text]) => [relative, hash(normalize(text))]));
  for (const relative of [CONFIG, INPUT, PACKAGE, LOCK, BUILDER, 'TOOL_REGISTRY.json']) inputs[relative] = hash(normalize(read(root, relative)));
  return {schema_version:1, base_revision:BASE, compiler:{package:'@tailwindcss/cli', version:VERSION, minified:true},
    normalization:'Input text hashes normalize CRLF to LF only; generated CSS hash covers exact bytes. No timestamps, local paths or secrets.',
    pilot_pages:PILOT, source_paths:result.config.source_paths, required_selectors:REQUIRED_SELECTORS,
    input_sha256:Object.fromEntries(Object.entries(inputs).sort(([a],[b])=>a<b?-1:a>b?1:0)),
    output:{path:asset, sha256:result.sha256, bytes:result.css.length, gzip_bytes:result.gzipBytes},
    budgets:{preferred_gzip_bytes:30*1024, maximum_gzip_bytes:50*1024, preferred_met:result.gzipBytes<=30*1024}};
}

function writablePath(root, relative) {
  const absolute = path.resolve(root, relative);
  if (path.relative(root, absolute).startsWith('..') || path.isAbsolute(path.relative(root, absolute))) throw Error('Unsafe CSS output path');
  let current = path.resolve(root);
  for (const part of relative.split('/').slice(0,-1)) {
    current = path.join(current, part);
    if (fs.existsSync(current)) {
      if (fs.lstatSync(current).isSymbolicLink() || !fs.statSync(current).isDirectory()) throw Error('CSS output path traverses non-directory or junction');
    } else fs.mkdirSync(current);
  }
  if (fs.existsSync(absolute) && fs.lstatSync(absolute).isSymbolicLink()) throw Error('CSS output is a symlink');
  return absolute;
}

export function build({root = ROOT, check = false} = {}) {
  root=path.resolve(root);
  const result=compile(root), asset='assets/css/site.'+result.sha256.slice(0,16)+'.css';
  const pages=planPages(result.source,asset,check);
  for (const [relative,text] of pages) result.source.set(relative,text);
  const record=recordFor(root,result,result.source), serialized=JSON.stringify(record,null,2)+'\n';
  if (check) {
    const existing=fs.readFileSync(safeFile(root,asset));
    if (!existing.equals(result.css)) throw Error('Generated CSS is stale or modified');
    if (normalize(read(root,RECORD))!==serialized) throw Error('CSS input/build manifest is stale or modified');
  } else {
    const output=writablePath(root,asset);
    if (fs.existsSync(output) && !fs.readFileSync(output).equals(result.css)) throw Error('Content-named CSS file has unexpected bytes');
    fs.writeFileSync(output,result.css);
    for(const [relative,text]of pages)fs.writeFileSync(safeFile(root,relative),text,'utf8');
    fs.writeFileSync(writablePath(root,RECORD),serialized,'utf8');
  }
  return {status:'PASS',mode:check?'check':'build',...record.output,pilot_pages:PILOT.length,source_files:result.source.size,preferred_budget_met:record.budgets.preferred_met};
}

if (process.argv[1] && samePath(path.resolve(process.argv[1]),fileURLToPath(import.meta.url))) {
  try {
    if (process.argv.slice(2).some(arg=>arg!=='--check') || process.argv.slice(2).length>1) throw Error('Usage: node scripts/build_styles.mjs [--check]');
    console.log(JSON.stringify(build({check:process.argv.includes('--check')}),null,2));
  } catch(error) {console.error(error.message);process.exitCode=1;}
}
