import {test} from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';
import {loadLogic} from './tool-tests/runner.mjs';

function adapter(id) {
  return loadLogic(fileURLToPath(new URL(`../${id}/index.html`, import.meta.url))).context;
}
const tool = id => adapter(id).EDB_TOOL;

test('word input and token caps accept the boundary and reject the next unit', () => {
  const {run} = tool('word-frequency-analyzer');
  assert.match(run(' '.repeat(100000)), /Occurrences: 0/);
  assert.throws(() => run(' '.repeat(100001)), /100,000 UTF-16/);
  assert.match(run('a '.repeat(20000)), /Occurrences: 20000/);
  assert.throws(() => run('a '.repeat(20001)), /20,000 word tokens/);
});

test('word reports retain complete counts when ranking rows or output bytes are capped', () => {
  const {run} = tool('word-frequency-analyzer');
  const numbered = Array.from({length: 1001}, (_, i) => 'w' + i).join(' ');
  assert.match(run(numbered), /Unique words: 1001[\s\S]*Showing 1000 of 1001 ranked words/);
  const long = Array.from({length: 390}, (_, i) => '界'.repeat(250) + i).join(' ');
  const report = run(long);
  assert.ok(Buffer.byteLength(report) <= 256 * 1024);
  assert.match(report, /Showing \d+ of 390 ranked words/);
});

test('Unicode UTF-8 bytes agree with native encoding across widths and preserve full bounded counts', () => {
  const {run} = tool('unicode-inspector');
  for (const value of ['a', 'é', '€', '😀', '👩‍💻', 'e\u0301', '\n', '\u202e']) {
    const report = run(value);
    assert.match(report, new RegExp(`UTF-8 bytes: ${Buffer.byteLength(value)}\\b`));
    for (const point of value) {
      const hexBytes = Buffer.from(point).toString('hex').toUpperCase().match(/../g).join(' ');
      assert.ok(report.includes(` | ${hexBytes} | `));
    }
  }
  const report = run('a'.repeat(8192));
  assert.match(report, /Code points: 8192/);
  assert.match(report, /Showing \d+ of 8192 diagnostic rows/);
  assert.ok(Buffer.byteLength(report) <= 128 * 1024);
});

test('Unicode inspector reports unavailable grapheme data and identifies compatibility normalization', () => {
  const context = adapter('unicode-inspector');
  vm.runInContext('Intl.Segmenter = undefined', context);
  const report = context.EDB_TOOL.run('Ａ');
  assert.match(report, /Grapheme clusters: Unavailable/);
  assert.match(report, /NFC: unchanged/);
  assert.match(report, /NFKC: changed/);
});

test('IPv4 arithmetic matches unsigned numeric intervals for every prefix', () => {
  const {run} = tool('ipv4-subnet-calculator');
  const decimal = 203 * 256 ** 3 + 113 * 256 + 253;
  const address = number => [3, 2, 1, 0].map(power => Math.floor(number / 256 ** power) % 256).join('.');
  for (let prefix = 0; prefix <= 32; prefix++) {
    const size = 2 ** (32 - prefix);
    const start = Math.floor(decimal / size) * size;
    const report = run('203.0.113.253', {prefix: String(prefix)});
    assert.ok(report.includes(`Network address: ${address(start)}\n`));
    assert.ok(report.includes(`Address range: ${address(start)} – ${address(start + size - 1)}\n`));
    assert.ok(report.includes(`Total addresses: ${size}\n`));
  }
});

test('filename manifest caps apply independently of the 500-name cap', () => {
  const {run} = tool('batch-filename-planner');
  const maximumNames = Array.from({length: 500}, (_, i) => `f${i}`);
  assert.equal(run(maximumNames.join('\n')).split('\r\n').length, 501);
  assert.throws(() => run([...maximumNames, 'overflow'].join('\n')), /500 names/);
  const long = Array.from({length: 100}, (_, i) => '界'.repeat(250) + i);
  assert.throws(() => run(long.join('\n')), /128 KiB output limit/);
});

test('file names from the picker are validated as complete names and CSV cells are quoted', () => {
  const {analyze, run} = tool('batch-filename-planner');
  assert.throws(() => analyze(['first\nsecond.txt']), /portable filename rules/);
  assert.match(run(' a,b.txt\n@calc.txt'), /" a,b.txt"," a,b.txt"\r\n"'@calc.txt","'@calc.txt"/);
  assert.match(analyze(['A.txt', 'a.TXT']).error, /rows 1 and 2/);
  assert.equal(analyze(['A.txt', 'a.TXT'], {numbering: 'on'}).error, '');
});

test('gradient grammar permits eight stops and rejects arbitrary CSS and nonfinite numbers', () => {
  const {run} = tool('css-gradient-generator');
  const input = Array.from({length: 8}, (_, i) => `#123456 ${i * 10}%`).join('\n');
  assert.match(run(input, {type: 'radial'}), /radial-gradient\(circle at center,/);
  assert.throws(() => run(input + '\n#123456 80%'), /between 2 and 8/);
  assert.throws(() => run(input, {angle: 'Infinity'}), /Angle/);
  assert.throws(() => run('#000000 0%; color: red\n#ffffff 100%'), /use #RRGGBB/);
});

const chunk = 256 * 1024;
function tracedFile(size, reads, difference = -1, short = false) {
  return {
    size,
    slice(start, end) {
      reads.slices.push([start, end]);
      return {async arrayBuffer() {
        reads.active++;
        reads.maxActive = Math.max(reads.active, reads.maxActive);
        await Promise.resolve();
        const bytes = new Uint8Array(end - start - (short ? 1 : 0));
        if (difference >= start && difference < end) bytes[difference - start] = 1;
        reads.active--;
        return bytes.buffer;
      }};
    },
  };
}

async function executeWorker(left, right) {
  const messages = [];
  const self = {postMessage: message => messages.push(message)};
  vm.runInNewContext(tool('file-byte-comparator').workerSource(), {self});
  await self.onmessage({data: {left, right}});
  return messages;
}

function tracker() { return {slices: [], active: 0, maxActive: 0}; }

test('worker finds the first mismatch at a chunk boundary and stops further reads', async () => {
  const reads = tracker();
  const size = 3 * chunk + 4;
  const messages = await executeWorker(tracedFile(size, reads), tracedFile(size, reads, chunk));
  assert.match(messages.at(-1).text, /First differing offset: 262144 \(zero-based\)/);
  assert.deepEqual(reads.slices, [[0, chunk], [0, chunk], [chunk, chunk * 2], [chunk, chunk * 2]]);
  assert.equal(reads.maxActive, 2);
});

test('worker compares an equal prefix through the end and reports shorter-file EOF', async () => {
  const reads = tracker();
  const messages = await executeWorker(tracedFile(chunk + 1, reads), tracedFile(chunk + 2, reads));
  assert.match(messages.at(-1).text, /First differing offset: 262145 .*shorter file ends here/);
  assert.ok(reads.slices.every(([start, end]) => end - start <= chunk));
  assert.equal(reads.active, 0);
});

test('worker refuses oversize or truncated reads and never reports equality for them', async () => {
  const reads = tracker();
  const oversize = await executeWorker(tracedFile(64 * 1024 * 1024 + 1, reads), tracedFile(1, reads));
  assert.ok(oversize.at(-1).error);
  assert.deepEqual(reads.slices, []);
  const truncated = await executeWorker(tracedFile(12, reads, -1, true), tracedFile(12, reads));
  assert.ok(truncated.at(-1).error);
  assert.equal(truncated.at(-1).text, undefined);
});
