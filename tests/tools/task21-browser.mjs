import { test, before, beforeEach, after } from "node:test";
import assert from "node:assert/strict";
import { fileURLToPath } from "node:url";
import {
  launchBrowser,
  findBrowser,
} from "../../scripts/tool-tests/browser.mjs";
export const examples = {
  "hashtag-counter": ["Hi #One #one #two", "#One #one #two"],
  "html-formatter": ["<p>Hello</p>", "<p>Hello</p>"],
  "css-minifier": ["a { color: red; }", "a{color:red}"],
  "javascript-minifier": ["let x = 1;", "let x=1;"],
  "html-to-markdown": ["<h1>Hello</h1><p>World</p>", "# Hello\n\nWorld\n"],
  "html-previewer": [
    "<h1>Hello</h1><p>World</p>",
    "<h1>Hello</h1><p>World</p>",
  ],
};
export async function wait(b, expression) {
  for (let i = 0; i < 160; i++) {
    if (await b.evaluate(`Boolean(${expression})`)) return;
    await new Promise((r) => setTimeout(r, 20));
  }
  assert.fail("Expected UI state did not arrive");
}
export function extended(id) {
  let b;
  before(async () => {
    b = await launchBrowser(findBrowser());
  });
  beforeEach(async () =>
    b.load(
      fileURLToPath(new URL("../../" + id + "/index.html", import.meta.url)),
    ),
  );
  after(async () => b?.close());
  const setRun = async () => {
    await b.evaluate(
      `toolInput.value=${JSON.stringify(examples[id][0])};toolInput.dispatchEvent(new Event('input'));runBtn.click();true`,
    );
    await wait(
      b,
      "document.getElementById('toolStatus').textContent==='Complete.'",
    );
  };
  test("actual worker output, safe text, captured clipboard/download and reset", async () => {
    await setRun();
    assert.equal(await b.evaluate("toolOutput.value"), examples[id][1]);
    await b.evaluate("copyBtn.click();downloadBtn.click();true");
    await wait(b, "window.__edbClipboard.value!==undefined");
    assert.equal(
      await b.evaluate("window.__edbClipboard.value"),
      examples[id][1],
    );
    assert.equal(await b.evaluate("window.__edbDownloads.length"), 1);
    await b.evaluate("clearBtn.click();true");
    assert.equal(await b.evaluate("toolOutput.value"), "");
    assert.equal(await b.evaluate("document.activeElement.id"), "toolInput");
    assert.equal(await b.evaluate("copyBtn.disabled"), true);
  });
  test("cancellation and input change stop in-flight work without stale output", async () => {
    await b.evaluate(
      `toolInput.value=${JSON.stringify(examples[id][0])};runBtn.click();cancelBtn.click();true`,
    );
    await new Promise((r) => setTimeout(r, 120));
    assert.equal(await b.evaluate("toolOutput.value"), "");
    assert.match(await b.evaluate("toolStatus.textContent"), /Cancelled/);
    await b.evaluate(
      `toolInput.value=${JSON.stringify(examples[id][0])};runBtn.click();toolInput.value='Changed';toolInput.dispatchEvent(new Event('input'));true`,
    );
    await new Promise((r) => setTimeout(r, 120));
    assert.equal(await b.evaluate("toolOutput.value"), "");
    assert.equal(await b.evaluate("copyBtn.disabled"), true);
    assert.equal(await b.evaluate("runBtn.disabled"), false);
  });
  test("worker unavailable fails closed and does not enable stale actions", async () => {
    await b.evaluate(
      `window.Worker=undefined;toolInput.value=${JSON.stringify(examples[id][0])};runBtn.click();true`,
    );
    assert.equal(await b.evaluate("toolError.hidden"), false);
    assert.match(await b.evaluate("toolError.textContent"), /Worker/);
    assert.equal(await b.evaluate("copyBtn.disabled"), true);
  });
  test("narrow layout, native keyboard activation and readable limits", async () => {
    for (const width of [320, 375, 768, 1440]) {
      await b.call("Emulation.setDeviceMetricsOverride", {
        width,
        height: 900,
        deviceScaleFactor: 1,
        mobile: false,
      });
      assert.equal(
        await b.evaluate("document.documentElement.scrollWidth>innerWidth"),
        false,
      );
    }
    await b.evaluate(
      `toolInput.value=${JSON.stringify(examples[id][0])};runBtn.focus();true`,
    );
    await b.call("Input.dispatchKeyEvent", {
      type: "keyDown",
      key: "Enter",
      code: "Enter",
      windowsVirtualKeyCode: 13,
      text: "\r",
    });
    await b.call("Input.dispatchKeyEvent", {
      type: "keyUp",
      key: "Enter",
      code: "Enter",
      windowsVirtualKeyCode: 13,
    });
    await wait(b, "toolStatus.textContent==='Complete.'");
    assert.match(await b.evaluate("inputHelp.textContent"), /2-second/);
  });
  test("empty input and clipboard failure are truthful", async () => {
    await b.evaluate("runBtn.click();true");
    assert.equal(await b.evaluate("toolError.hidden"), false);
    await setRun();
    await b.evaluate(
      "window.__edbClipboard.mode='failure';copyBtn.click();true",
    );
    await wait(b, "toolStatus.textContent.includes('Clipboard unavailable')");
    assert.equal(await b.evaluate("document.activeElement.id"), "toolOutput");
  });
  test("actual UI deadline terminates a stalled Worker and retains no partial output", async () => {
    await b.evaluate(
      `if(${JSON.stringify(id)}==='hashtag-counter'){document.getElementById('edb-tool-logic').textContent='window.EDB_TOOL={analyze(){while(true){}}};';}else{window.EDB_TASK21_WORKER_SOURCE='self.onmessage=()=>{while(true){}}';}toolInput.value=${JSON.stringify(examples[id][0])};runBtn.click();true`,
    );
    await wait(
      b,
      "!toolError.hidden&&toolError.textContent.includes('2-second')",
    );
    assert.equal(await b.evaluate("toolOutput.value"), "");
    assert.equal(await b.evaluate("cancelBtn.disabled"), true);
    assert.equal(await b.evaluate("runBtn.disabled"), false);
  });
  if (id === "css-minifier")
    test("independent browser computed styles agree before and after compact printing", async () => {
      const source =
        ":root{--task21-space:3px} .task21-sample { color: rgb(12, 34, 56); padding: calc(1px + var(--task21-space)); margin:0 0 2px; background-color:rgba(1,2,3,.5); }";
      await b.evaluate(
        `toolInput.value=${JSON.stringify(source)};runBtn.click();true`,
      );
      await wait(b, "toolStatus.textContent==='Complete.'");
      const result = await b.evaluate(
        `(()=>{const css=[${JSON.stringify(source)},toolOutput.value],read=value=>{const style=document.createElement('style');style.textContent=value;const sample=document.createElement('div');sample.className='task21-sample';document.head.append(style);document.body.append(sample);const s=getComputedStyle(sample),v={color:s.color,padding:s.padding,margin:s.margin,background:s.backgroundColor};style.remove();sample.remove();return v;};return css.map(read)})()`,
      );
      assert.deepEqual(result[0], result[1]);
      assert.equal(result[1].padding, "4px");
    });
}
export function integration(id) {
  let b;
  before(async () => {
    b = await launchBrowser(findBrowser());
  });
  beforeEach(async () =>
    b.load(
      fileURLToPath(new URL("../../" + id + "/index.html", import.meta.url)),
    ),
  );
  after(async () => b?.close());
  test("hub link, current card and canonical route remain connected", async () => {
    assert.equal(
      await b.evaluate(
        "document.querySelector('header a').getAttribute('href')",
      ),
      "../index.html",
    );
    await b.evaluate("document.querySelector('header a').click();true");
    await wait(b, `!!document.querySelector('a[data-tool-id="${id}"]')`);
    const route = await b.evaluate(
      `document.querySelector('a[data-tool-id="${id}"]').getAttribute('href')`,
    );
    assert.equal(route, id + "/index.html");
    await b.evaluate(
      `document.querySelector('a[data-tool-id="${id}"]').click();true`,
    );
    await wait(
      b,
      `document.querySelector('h1')?.textContent===${JSON.stringify(id === "html-to-markdown" ? "HTML to Markdown" : { "hashtag-counter": "Hashtag Counter", "html-formatter": "HTML Formatter", "css-minifier": "CSS Minifier", "javascript-minifier": "JavaScript Minifier", "html-previewer": "HTML Previewer" }[id])}`,
    );
  });
  test("editing options invalidates the current result and defaults reset", async () => {
    await b.evaluate(
      `toolInput.value=${JSON.stringify(examples[id][0])};runBtn.click();true`,
    );
    await wait(b, "toolStatus.textContent==='Complete.'");
    await b.evaluate(
      "const control=document.querySelector('.options select');if(control){control.value=control.options[control.options.length-1].value;control.dispatchEvent(new Event('input'));}else{toolInput.value+=' ';toolInput.dispatchEvent(new Event('input'));}true",
    );
    assert.equal(await b.evaluate("copyBtn.disabled"), true);
    assert.equal(await b.evaluate("toolOutput.value"), "");
    await b.evaluate("clearBtn.click();true");
    assert.equal(
      await b.evaluate(
        "Array.from(document.querySelectorAll('.options select')).every(s=>s.value===s.dataset.default)",
      ),
      true,
    );
  });
}
