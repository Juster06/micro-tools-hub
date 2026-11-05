import fs from 'node:fs';import vm from 'node:vm';import {fileURLToPath} from 'node:url';import {loadLogic} from '../../scripts/tool-tests/runner.mjs';
const frames=JSON.parse(fs.readFileSync(0,'utf8')).map(f=>({size:f.size,bytes:Array.from(Buffer.from(f.png,'base64'))}));
const {context}=loadLogic(fileURLToPath(new URL('../../png-to-ico/index.html',import.meta.url)));context.frames=frames;process.stdout.write(Buffer.from(vm.runInContext('EDB_TOOL.pack(frames)',context,{timeout:1000})).toString('base64'));
