import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';
import {loadLogic} from '../../../scripts/tool-tests/runner.mjs';

const adapter = loadLogic(fileURLToPath(new URL('../../../case-converter/index.html', import.meta.url)));
function invoke(method, input, mode) {
  adapter.context.__fixtureInput = input;
  adapter.context.__fixtureMode = mode;
  return vm.runInContext(method === 'statistics' ? 'EDB_TOOL.statistics(__fixtureInput)' : 'EDB_TOOL.run(__fixtureInput,{mode:__fixtureMode})', adapter.context, {timeout:1000});
}
const counts = [
  ['empty', '', {characters:0,words:0,lines:0}],
  ['space', ' ', {characters:1,words:0,lines:1}],
  ['repeated whitespace', 'a  b\tc\n', {characters:7,words:3,lines:2}],
  ['Windows CRLF and emoji', 'Hi 😀\r\nnext', {characters:10,words:3,lines:2}],
  ['mixed line endings', 'a\rb\nc\r\nd\n', {characters:9,words:4,lines:5}],
  ['combining accent and joined emoji', 'e\u0301 👩‍💻', {characters:6,words:2,lines:1}],
  ['non-Latin token', '你好世界', {characters:4,words:1,lines:1}],
  ['emoji token', '😀😀', {characters:2,words:1,lines:1}],
  ['trailing blank lines', 'a\n\n', {characters:3,words:1,lines:3}],
  ['Unicode whitespace', 'a\u00a0b\u2003c', {characters:5,words:3,lines:1}]
];
for (const [name,input,expected] of counts) test('statistics: '+name, () => {
  assert.deepEqual(JSON.parse(JSON.stringify(invoke('statistics',input))), expected);
});

const longCases = [
  ['uppercase','a'.repeat(100000),'A'.repeat(100000)],
  ['lowercase','B'.repeat(100000),'b'.repeat(100000)],
  ['title','z'.repeat(100000),'Z'+'z'.repeat(99999)],
  ['sentence','a'.repeat(100000),'A'+'a'.repeat(99999)],
  ['capitalize','x'.repeat(100000),'X'+'x'.repeat(99999)],
  ['alternating','ab '.repeat(33333),'aB '.repeat(33333)],
  ['inverse','aB '.repeat(33333),'Ab '.repeat(33333)]
];
for (const [mode,input,expected] of longCases) test('long input exact result: '+mode, () => {
  assert.equal(invoke('run',input,mode),expected);
});
test('oversized input is rejected without truncation in every mode', () => {
  for (const [mode] of longCases) assert.throws(() => invoke('run','a'.repeat(100001),mode), /100,000 UTF-16/);
});
test('statistics rejects non-text input', () => {
  assert.throws(() => invoke('statistics',null), /Text must be a string/);
});
test('all seven modes preserve punctuation and whitespace', () => {
  const text = '  a\tb!?\r\nc — 123 😀\r\n';
  const punctuation = '  \t!?\r\n — 123 😀\r\n';
  for (const [mode] of longCases) assert.equal(invoke('run',text,mode).replace(/[a-z]/gi,''),punctuation);
});
