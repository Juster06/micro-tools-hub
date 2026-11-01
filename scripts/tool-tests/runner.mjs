// Executes trusted repository logic with fixture values, never user-supplied code.
// node:vm is a test adapter, not a security boundary for untrusted repositories.
import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import {pathToFileURL} from 'node:url';
import {runBrowserCases} from './browser.mjs';

function portable(value) {
  if(value===null || typeof value==='string' || typeof value==='boolean')return value;
  if(typeof value==='number'&&Number.isFinite(value))return value;
  if(Array.isArray(value))return Array.from(value,portable);
  if(value && Object.prototype.toString.call(value)==='[object Object]')return Object.fromEntries(Object.entries(value).map(([key,value])=>[key,portable(value)]));
  throw Error('Logic output must be JSON-representable and finite');
}

export function loadLogic(source) {
  const html=fs.readFileSync(source,'utf8');
  const script=/<script\b(?=[^>]*\bid\s*=\s*["']edb-tool-logic["'])[^>]*>([\s\S]*?)<\/script\s*>/i.exec(html);
  if(!script)return null;
  const context=vm.createContext({});context.window=context;
  vm.runInContext(script[1],context,{timeout:1000});
  if(!context.EDB_TOOL || typeof context.EDB_TOOL.run!=='function' || typeof context.EDB_TOOL.isScaffold!=='boolean')throw Error('Invalid logic adapter');
  return {context,isScaffold:context.EDB_TOOL.isScaffold};
}

export function runLogicCases(adapter,cases) {
  const result={status:'NOT RUN',passed:0,failed:0,assertions:0,failures:[],scope:'Deterministic inline JavaScript logic, executed in Node with explicit fixtures.'};
  if(!adapter || adapter.isScaffold || !cases.length)return result;
  for(const test of cases) {
    try {
      if(!Object.hasOwn(test,'input') || (Object.hasOwn(test,'expected')===Object.hasOwn(test,'error')))throw Error('Case needs input and exactly one expected/error');
      adapter.context.__input=structuredClone(test.input);adapter.context.__options=structuredClone(test.options||{});
      let actual,problem;
      try {actual=vm.runInContext('EDB_TOOL.run(__input,__options)',adapter.context,{timeout:1000});}catch(error){problem=error;}
      if(Object.hasOwn(test,'error')) {assert.equal(typeof test.error,'string');assert(test.error.length>0);assert(problem && String(problem.message).includes(test.error));}
      else {assert(!problem);assert.deepEqual(portable(actual),test.expected);}
      result.passed++;result.assertions++;
    } catch {result.failed++;result.failures.push({id:test.id,reason:'Logic result, expected error or case validation failed; inspect the case locally.'});}
  }
  result.status=result.failed?'FAIL':'PASS';return result;
}

export async function runSpec(spec) {
  let adapter,adapterError=false;
  try {adapter=loadLogic(spec.source);}catch {adapterError=true;}
  const result={is_scaffold:adapter?.isScaffold??null,layers:{}};
  if(spec.layers.includes('logic'))result.layers.logic=adapterError?{status:'FAIL',passed:0,failed:1,assertions:0,reason:'Logic adapter could not execute.'}:runLogicCases(adapter,spec.cases.logic);
  if(spec.layers.includes('browser'))result.layers.browser=await runBrowserCases(spec.source,spec.cases.browser,spec.browser);
  return result;
}

if(process.argv[1] && pathToFileURL(process.argv[1]).href===import.meta.url) {
  try {const spec=JSON.parse(fs.readFileSync(0,'utf8'));process.stdout.write(JSON.stringify(await runSpec(spec)));}
  catch {process.stdout.write(JSON.stringify({error:'Tool test worker failed. Check trusted source and test schemas.'}));process.exitCode=1;}
}
