import vm from 'node:vm';
import {fileURLToPath} from 'node:url';
import {loadLogic} from '../../scripts/tool-tests/runner.mjs';
export function logic(id) {
  const context=loadLogic(fileURLToPath(new URL(`../../${id}/index.html`,import.meta.url))).context;
  const call=(input,options={})=>{context.input=input;context.options=options;return JSON.parse(JSON.stringify(vm.runInContext('EDB_TOOL.run(input, options)',context,{timeout:1000})));};
  return {call,context};
}
