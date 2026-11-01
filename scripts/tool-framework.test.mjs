import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {loadLogic,runLogicCases} from './tool-tests/runner.mjs';

function fixture(t,body='return "Result: "+input;',scaffold=false) {
  const directory=fs.mkdtempSync(path.join(os.tmpdir(),'edb-logic-tests-'));
  t.after(()=>{assert.equal(path.dirname(directory),path.resolve(os.tmpdir()));assert(path.basename(directory).startsWith('edb-logic-tests-'));fs.rmSync(directory,{recursive:true,force:true});});
  const source=path.join(directory,'index.html');
  fs.writeFileSync(source,`<script id="edb-tool-logic">window.EDB_TOOL={isScaffold:${scaffold},run(input,options){${body}}};</script>`);
  return loadLogic(source);
}

test('actual trusted logic executes with Unicode, lines and explicit options',t=>{
  const adapter=fixture(t,'return input+options.suffix;');
  const result=runLogicCases(adapter,[{id:'unicode',input:'café 😀\nline',options:{suffix:'!'},expected:'café 😀\nline!'}]);
  assert.equal(result.status,'PASS');assert.equal(result.passed,1);
});
test('input is data and never evaluated as code',t=>{
  const adapter=fixture(t),payload="';globalThis.changed=true;//";
  assert.equal(runLogicCases(adapter,[{id:'literal',input:payload,expected:'Result: '+payload}]).status,'PASS');
  assert.equal(adapter.context.changed,undefined);
});
test('placeholder scaffolds never receive functional PASS',t=>{
  assert.equal(runLogicCases(fixture(t,'return input;',true),[{id:'x',input:'x',expected:'x'}]).status,'NOT RUN');
});
test('empty and missing logic scopes are NOT RUN',t=>{
  assert.equal(runLogicCases(fixture(t),[]).status,'NOT RUN');assert.equal(runLogicCases(null,[]).status,'NOT RUN');
});
test('wrong results fail with honest per-case counts',t=>{
  const result=runLogicCases(fixture(t),[{id:'pass',input:'x',expected:'Result: x'},{id:'fail',input:'x',expected:'wrong'}]);
  assert.equal(result.status,'FAIL');assert.equal(result.passed,1);assert.equal(result.failed,1);
});
test('error expectations require actual matching errors',t=>{
  const adapter=fixture(t,'throw new Error("Fixture rejection");');
  assert.equal(runLogicCases(adapter,[{id:'expected',input:'x',error:'rejection'}]).status,'PASS');
  assert.equal(runLogicCases(adapter,[{id:'mismatch',input:'x',error:'different'}]).status,'FAIL');
});
test('structured JSON logic outputs compare across VM realms',t=>{
  assert.equal(runLogicCases(fixture(t,'return {value:input,items:[1,true,null]};'),[{id:'structured',input:'x',expected:{value:'x',items:[1,true,null]}}]).status,'PASS');
});
test('NaN cannot masquerade as JSON null',t=>{
  assert.equal(runLogicCases(fixture(t,'return NaN;'),[{id:'nonfinite',input:'x',expected:null}]).status,'FAIL');
});
test('async/custom logic is not falsely treated as synchronous JSON logic',t=>{
  assert.equal(runLogicCases(fixture(t,'return Promise.resolve(input);'),[{id:'async',input:'x',expected:'x'}]).status,'FAIL');
});
test('malformed cases cannot pass vacuously',t=>{
  assert.equal(runLogicCases(fixture(t),[{id:'no-expectation',input:'x'}]).status,'FAIL');
});
test('synchronous infinite logic is bounded by VM timeout',t=>{
  assert.equal(runLogicCases(fixture(t,'while(true){}'),[{id:'timeout',input:'x',expected:'x'}]).status,'FAIL');
});
