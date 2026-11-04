import {test} from 'node:test';import assert from 'node:assert/strict';import vm from 'node:vm';import {fileURLToPath} from 'node:url';import {loadLogic} from '../../../scripts/tool-tests/runner.mjs';
const c=loadLogic(fileURLToPath(new URL('../../../duplicate-row-finder/index.html',import.meta.url))).context;function run(input,options={}){c.input=input;c.options=options;return vm.runInContext('EDB_TOOL.run(input,options)',c,{timeout:1000})}
test('selected columns, case and trimming keep first and preserve source',()=>assert.equal(run('name,k\n Ada ,x\nada,x\nADA,y',{columns:'1,2',ignoreCase:true,trimSpace:true}),'name,k\r\n Ada ,x\r\nADA,y'));
test('quoted multiline values are compared as complete fields',()=>assert.equal(run('n,v\n"a,\nb",1\n"a,\nb",2',{columns:'1'}),'n,v\r\n"a,\nb",1'));
test('formula-risk output fields are escaped',()=>assert.equal(run('n,v\nX,=1+1\nY," +SUM(1)"',{columns:'1'}),"n,v\r\nX,'=1+1\r\nY,' +SUM(1)"));
test('reject malformed and excessive inputs',()=>{for(const [v,o] of [['',{}],['a,"b',{}],['a,b',{columns:'0'}],['a,b',{columns:'1,1'}],['x'.repeat(10001),{}],['x\n'.repeat(2001),{}]])assert.throws(()=>run(v,o))});
