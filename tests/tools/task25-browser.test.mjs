import {test, before, after} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {fileURLToPath} from 'node:url';
import {start, source, wait, set, click, widths, noTransport} from './task19-browser.mjs';

let browser;
before(async () => { browser = await start(); });
after(async () => { await browser?.close(); });

async function selectFiles(id, expressions) {
  await browser.evaluate(`(() => {
    const selection = new DataTransfer();
    for (const file of [${expressions.join(',')}]) selection.items.add(file);
    const input = document.getElementById(${JSON.stringify(id)});
    input.files = selection.files;
    input.dispatchEvent(new Event('change', {bubbles:true}));
    return true;
  })()`);
}

async function result() {
  await click(browser, 'runBtn');
  await wait(browser, "toolStatus.textContent === 'Complete.'");
  return browser.evaluate('toolOutput.value');
}

const namePlanner = 'batch-filename-planner';
const comparator = 'file-byte-comparator';
const gradient = 'css-gradient-generator';
const tests = [
  ['word-frequency-analyzer', 'a a é e\u0301'], ['unicode-inspector', '👩‍💻 e\u0301'],
  ['ipv4-subnet-calculator', '192.0.2.131'], [namePlanner, 'a.txt'],
  [comparator, null], [gradient, '#123abc 0%\n#ffffff 100%'],
];

for (const [id, sample] of tests) {
  test(`${id} works at narrow and wide widths and keeps input local`, async () => {
    await browser.load(source(id));
    await widths(browser);
    await browser.evaluate(`window.__writes = 0;
      Storage.prototype.setItem = () => { __writes++; throw Error('Unexpected storage write'); };
      true`);
    await noTransport(browser, async () => {
      if (sample === null) {
        await selectFiles('toolInput', ["new File(['a'], 'left.txt')"]);
        await selectFiles('secondFile', ["new File(['a'], 'right.txt')"]);
      } else await set(browser, 'toolInput', sample);
      assert.ok(await result());
    });
    assert.equal(await browser.evaluate('__writes'), 0);
  });
}

test('word analyzer accepts a 100,000-unit text and refuses oversize without retaining a result', async () => {
  await browser.load(source('word-frequency-analyzer'));
  await set(browser, 'toolInput', ' a'.repeat(20000).padEnd(100000, ' '));
  assert.match(await result(), /Occurrences: 20000/);
  await set(browser, 'toolInput', ' '.repeat(100001));
  await click(browser, 'runBtn');
  assert.match(await browser.evaluate('toolError.textContent'), /100,000 UTF-16/);
  assert.equal(await browser.evaluate('toolOutput.value'), '');
  assert.equal(await browser.evaluate('copyBtn.disabled'), true);
});

test('filename planner reads only names and produces the expected formula-safe CSV', async () => {
  await browser.load(source(namePlanner));
  await browser.evaluate(`window.__reads = 0;
    for (const name of ['text', 'slice', 'arrayBuffer', 'stream']) File.prototype[name] = () => { __reads++; throw Error('Content read'); };
    window.FileReader = function () { __reads++; throw Error('Content read'); };
    true`);
  await selectFiles('nameFiles', ["new File(['a'], '+Café.tar.gz')", "new File(['b'], '.gitignore')"]);
  await set(browser, 'suffix', '-done');
  const text = await result();
  assert.match(text, /"'\+Café\.tar\.gz","'\+Café\.tar-done\.gz"/);
  assert.match(text, /"\.gitignore","\.gitignore-done"/);
  await click(browser, 'downloadBtn');
  assert.equal(await browser.evaluate('__edbDownloadBlob.type'), 'text/csv;charset=utf-8');
  assert.equal(await browser.evaluate('__edbDownloadBlob.text()'),
    'Original,Proposed\r\n"\'+Café.tar.gz","\'+Café.tar-done.gz"\r\n".gitignore",".gitignore-done"');
  assert.deepEqual(await browser.evaluate('__edbDownloads'), ['filename-plan.csv']);
  assert.equal(await browser.evaluate('__reads'), 0);
  await click(browser, 'clearBtn');
  assert.equal(await browser.evaluate('nameFiles.files.length'), 0);
});

test('filename planner handles selection collisions and refuses ambiguous or invalid input', async () => {
  await browser.load(source(namePlanner));
  await selectFiles('nameFiles', ["new File([], 'é.txt')", "new File([], 'e\\u0301.TXT')"]);
  await click(browser, 'runBtn');
  assert.match(await browser.evaluate('toolError.textContent'), /rows 1 and 2/);
  assert.equal(await browser.evaluate('downloadBtn.disabled'), true);
  await set(browser, 'toolInput', 'one.txt');
  await click(browser, 'runBtn');
  assert.match(await browser.evaluate('toolError.textContent'), /Choose files or paste names/);
  await click(browser, 'clearBtn');
  await selectFiles('nameFiles', ["new File([], 'bad\\nname.txt')"]);
  await click(browser, 'runBtn');
  assert.match(await browser.evaluate('toolError.textContent'), /portable filename/);
});

async function bytes(a, b) {
  await selectFiles('toolInput', [a]);
  await selectFiles('secondFile', [b]);
  return result();
}

test('actual file comparisons handle empty, equal, early mismatch and shorter-file EOF', async () => {
  await browser.load(source(comparator));
  assert.match(await bytes("new File([], 'a')", "new File([], 'b')"), /Identical/);
  assert.match(await bytes("new File(['abc'], 'a')", "new File(['abc'], 'b')"), /Identical/);
  assert.match(await bytes("new File(['abc'], 'same')", "new File(['bbc'], 'same')"), /First differing offset: 0 /);
  const eof = await bytes("new File(['abc'], 'a')", "new File(['abcd'], 'b')");
  assert.match(eof, /Size difference: 1 bytes/);
  assert.match(eof, /First differing offset: 3 .*shorter file ends here/);
});

test('actual Worker finds a late difference after the 256 KiB chunk boundary', async () => {
  await browser.load(source(comparator));
  const left = "new File([new Uint8Array(262144), 'same', 'x'], 'a')";
  const right = "new File([new Uint8Array(262144), 'same', 'y'], 'b')";
  assert.match(await bytes(left, right), /First differing offset: 262148 /);
});

test('actual Worker compares two 64 MiB files and the next byte is rejected before startup', async () => {
  await browser.load(source(comparator));
  await browser.evaluate(`window.__part = new Blob([new Uint8Array(262144)]);
    window.__workers = 0;
    const original = Worker;
    window.Worker = class extends original { constructor(url) { super(url); __workers++; } };
    true`);
  const size = "new File(Array(256).fill(__part), 'limit.bin')";
  const before = performance.now();
  const equal = await bytes(size, size);
  assert.match(equal, /Identical[\s\S]*File A: 67108864 bytes/);
  assert.ok(performance.now() - before < 10000);
  await selectFiles('secondFile', ["new File([...Array(256).fill(__part), 'x'], 'too-big.bin')"]);
  await click(browser, 'runBtn');
  assert.match(await browser.evaluate('toolError.textContent'), /64 MiB/);
  assert.equal(await browser.evaluate('__workers'), 1);
});

test('cancel and reselection terminate real Workers and cannot publish stale results', async () => {
  await browser.load(source(comparator));
  await browser.evaluate(`window.__terminated = 0;
    const original = Worker.prototype.terminate;
    Worker.prototype.terminate = function () { __terminated++; return original.call(this); };
    true`);
  await selectFiles('toolInput', ["new File(['first'], 'a')"]);
  await selectFiles('secondFile', ["new File(['first'], 'b')"]);
  await browser.evaluate('runBtn.click(); cancelBtn.click(); true');
  assert.equal(await browser.evaluate('__terminated'), 1);
  assert.equal(await browser.evaluate('toolStatus.textContent'), 'Comparison cancelled.');
  assert.equal(await browser.evaluate('toolOutput.value'), '');
  await browser.evaluate(`runBtn.click();
    const next = new DataTransfer(); next.items.add(new File(['other'], 'other'));
    secondFile.files = next.files; secondFile.dispatchEvent(new Event('change', {bubbles:true})); true`);
  assert.equal(await browser.evaluate('__terminated'), 2);
  assert.match(await result(), /First differing offset: 0 /);
  await click(browser, 'clearBtn');
  assert.equal(await browser.evaluate('toolInput.files.length + secondFile.files.length'), 0);
  assert.equal(await browser.evaluate('toolOutput.value'), '');
});

test('comparator handles unavailable and unresponsive Worker environments', async () => {
  await browser.load(source(comparator));
  await selectFiles('toolInput', ["new File([], 'a')"]);
  await selectFiles('secondFile', ["new File([], 'b')"]);
  await browser.evaluate('window.Worker = undefined; true');
  await click(browser, 'runBtn');
  assert.match(await browser.evaluate('toolError.textContent'), /cannot run/);
  await browser.evaluate(`window.__terminated = 0;
    window.Worker = class { postMessage() {} terminate() { __terminated++; } };
    true`);
  await click(browser, 'runBtn');
  for (let time = 0; time < 120 && !await browser.evaluate('!toolError.hidden'); time++) {
    await new Promise(resolve => setTimeout(resolve, 100));
  }
  assert.match(await browser.evaluate('toolError.textContent'), /10-second limit/);
  assert.equal(await browser.evaluate('__terminated'), 1);
  assert.equal(await browser.evaluate('copyBtn.disabled'), true);
});

test('gradient live preview applies only the validated property and clears invalid CSS', async () => {
  await browser.load(source(gradient));
  await set(browser, 'toolInput', '#ff0000 0%\n#00FF00 50%\n#0000ff 50%');
  await set(browser, 'angle', '-45.5');
  assert.match(await browser.evaluate('getComputedStyle(gradientPreview).backgroundImage'), /^linear-gradient\(-45\.5deg,/);
  await set(browser, 'type', 'radial');
  assert.match(await browser.evaluate('getComputedStyle(gradientPreview).backgroundImage'), /^radial-gradient\(/);
  assert.equal(await browser.evaluate('angle.disabled'), true);
  await set(browser, 'toolInput', 'url(https://example.invalid/) 0%\n#fff 100%');
  assert.equal(await browser.evaluate('gradientPreview.style.backgroundImage'), '');
  assert.equal(await browser.evaluate('toolOutput.value'), '');
  await click(browser, 'clearBtn');
  assert.equal(await browser.evaluate('type.value'), 'linear');
  assert.equal(await browser.evaluate('angle.value'), '90');
});

test('homepage links all 87 distinct canonical routes with six publication-pending cards', async () => {
  const registry = JSON.parse(fs.readFileSync(new URL('../../TOOL_REGISTRY.json', import.meta.url), 'utf8'));
  const expected = registry.tools.filter(tool => ['TESTED','RELEASED'].includes(tool.status));
  assert.equal(expected.filter(tool => tool.status === 'RELEASED').length, 81);
  assert.deepEqual(expected.filter(tool => tool.status === 'TESTED').map(tool => tool.id), tests.map(([id]) => id));
  await browser.load(fileURLToPath(new URL('../../index.html', import.meta.url)));
  const cards = await browser.evaluate(`Array.from(document.querySelectorAll('a.tool-card[data-title]'), link => ({
    route: link.getAttribute('href'), status: link.dataset.availability,
    visible: link.getClientRects().length > 0, text: link.textContent,
  }))`);
  assert.equal(cards.length, 87);
  assert.ok(cards.every(card => card.visible));
  assert.deepEqual(cards.map(card => card.route).sort(), expected.map(tool => tool.directory_path + '/index.html').sort());
  for (const [id] of tests) {
    const card = cards.find(item => item.route === id + '/index.html');
    assert.equal(card.status, 'tested');
    assert.match(card.text, /Tested · publication pending/);
  }
});
