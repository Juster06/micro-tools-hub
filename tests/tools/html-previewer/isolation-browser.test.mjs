import { test, before, beforeEach, after } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import http from "node:http";
import { fileURLToPath } from "node:url";
import {
  launchBrowser,
  findBrowser,
} from "../../../scripts/tool-tests/browser.mjs";
const root = fileURLToPath(new URL("../../../", import.meta.url));
let b,
  server,
  origin,
  hits = [],
  exceptions = [],
  serial = 0;
async function wait(fn) {
  for (let i = 0; i < 200; i++) {
    if (await fn()) return;
    await new Promise((r) => setTimeout(r, 20));
  }
  assert.fail("Isolation state not reached");
}
before(async () => {
  server = http.createServer((req, res) => {
    const pathname = decodeURIComponent(
      new URL(req.url, "http://localhost").pathname,
    );
    if (pathname.startsWith("/__canary/")) {
      hits.push(pathname);
      res.end("CANARY");
      return;
    }
    const target = path.resolve(root, "." + pathname);
    if (!target.startsWith(path.resolve(root) + path.sep)) {
      res.writeHead(403);
      res.end();
      return;
    }
    fs.readFile(target, (e, data) => {
      if (e) {
        res.writeHead(404);
        res.end();
        return;
      }
      res.setHeader(
        "Content-Type",
        target.endsWith(".js")
          ? "text/javascript; charset=utf-8"
          : "text/html; charset=utf-8",
      );
      res.end(data);
    });
  });
  await new Promise((r) => server.listen(0, "127.0.0.1", r));
  origin = "http://127.0.0.1:" + server.address().port;
  b = await launchBrowser(findBrowser());
  await b.call("Network.setBlockedURLs", { urls: ["*cdn.jsdelivr.net*"] });
  b.onEvent((m) => {
    if (m.method === "Runtime.exceptionThrown")
      exceptions.push(m.params.exceptionDetails);
  });
});
beforeEach(async () => {
  const marker = ++serial;
  const hook = await b.call("Page.addScriptToEvaluateOnNewDocument", {
    source: "window.__isolationDocument=" + marker,
  });
  try {
    await b.call("Page.navigate", {
      url: origin + "/html-previewer/index.html",
    });
    await wait(async () => {
      try {
        return await b.evaluate(
          `window.__isolationDocument===${marker}&&document.readyState==='complete'&&!!window.EDB_TOOL&&!!window.EDB_TASK21_WORKER_SOURCE`,
        );
      } catch {
        return false;
      }
    });
  } finally {
    await b.call("Page.removeScriptToEvaluateOnNewDocument", {
      identifier: hook.identifier,
    });
  }
  await b.evaluate(
    "window.__ran=0;localStorage.setItem('gate-sentinel','untouched');true",
  );
  hits = [];
  exceptions = [];
});
after(async () => {
  await b?.close();
  if (server) await new Promise((r) => server.close(r));
});
async function preview(input) {
  await b.evaluate(
    `toolInput.value=${JSON.stringify(input)};toolInput.dispatchEvent(new Event('input'));runBtn.click();true`,
  );
  await wait(() => b.evaluate("toolStatus.textContent==='Complete.'"));
  assert.equal(await b.evaluate("toolError.hidden"), true);
  await new Promise((r) => setTimeout(r, 80));
}
test("network canary is reachable: interception does not hide preview requests", async () => {
  assert.equal(
    await b.evaluate(
      `fetch(${JSON.stringify(origin + "/__canary/control")}).then(r=>r.status)`,
    ),
    200,
  );
  assert.deepEqual(hits, ["/__canary/control"]);
});
const fixtures = {
  scripts: (c) =>
    `<script>parent.__ran=1;localStorage.setItem('gate-sentinel','bad');top.location='${c}/nav';open('${c}/popup')</script><script src="${c}/script"></script><p>Visible</p>`,
  handlers: (c) =>
    `<img src="${c}/img" onerror="parent.__ran=2"><div onmouseover="parent.__ran=3" style="background:url(${c}/css)">Text</div>`,
  navigation: (c) =>
    `<base href="${c}/base" target="_top"><meta http-equiv="refresh" content="0;url=${c}/refresh"><a href="${c}/anchor" target="_top" ping="${c}/ping">link</a>`,
  forms: (c) =>
    `<form action="${c}/form" target="_blank"><input name="secret" value="x"><button formtarget="_top">send</button></form><a href="${c}/popup" target="_blank">open</a>`,
  resources: (c) =>
    `<link rel="stylesheet" href="${c}/style"><style>@import '${c}/import';div{background:url(${c}/bg)}</style><iframe src="${c}/frame"></iframe><object data="${c}/object"></object><audio src="${c}/audio" autoplay></audio><video poster="${c}/poster"><source src="${c}/video"></video>`,
  foreign: (c) =>
    `<svg><foreignObject><iframe src="${c}/svg"></iframe></foreignObject><image href="${c}/image" onload="parent.__ran=4"/></svg><math><mtext><img src="${c}/math"></mtext></math>`,
  mutation: (c) =>
    `<math><mtext><table><mglyph><style><!--</style><img title="--><img src=${c}/mxss onerror=parent.__ran=5>"></math><noscript><p title="</noscript><img src='${c}/noscript'>">x</p>`,
  templates: (c) =>
    `<template><img src="${c}/template"><script>parent.__ran=6</script></template><div id="location" name="parent" data-x="${c}">safe</div>`,
  rawtext: (c) =>
    `<xmp><img src="${c}/xmp" onerror="parent.__ran=7"></xmp><plaintext><script>parent.__ran=8</script>`,
  encoded: (c) =>
    `<a href="jav&#x61;script:parent.__ran=9">café 世界 😀</a><p onclick="&#x61;lert(1)">&lt;script&gt;literal&lt;/script&gt;</p>`,
};
for (const [name, fixture] of Object.entries(fixtures))
  test(
    "actual preview blocks " + name + " without network/parent-state changes",
    async () => {
      await preview(fixture(origin + "/__canary/" + name));
      assert.equal(await b.evaluate("__ran"), 0);
      assert.equal(
        await b.evaluate("localStorage.getItem('gate-sentinel')"),
        "untouched",
      );
      assert.equal(
        await b.evaluate("location.href"),
        origin + "/html-previewer/index.html",
      );
      assert.equal(await b.evaluate("safePreview.getAttribute('sandbox')"), "");
      assert.equal(await b.evaluate("safePreview.contentDocument"), null);
      assert.deepEqual(hits, []);
      assert.deepEqual(exceptions, []);
    },
  );
test("actual child has structural content, opaque origin/storage, blocked navigation, popup and form", async () => {
  await preview(
    "<h1>Hello</h1><p>Readable <strong>local</strong> preview.</p>",
  );
  let target, frameId, sessionId;
  await wait(async () => {
    const parentTree = await b.call("Page.getFrameTree");
    const child = parentTree.frameTree.childFrames?.find(
      (entry) => entry.frame.url === "about:srcdoc",
    );
    if (child) {
      frameId = child.frame.id;
      return true;
    }
    const t = await b.call("Target.getTargets");
    target = t.targetInfos.find(
      (x) => x.type === "iframe" && x.url === "about:srcdoc",
    );
    return !!target;
  });
  if (target) {
    ({ sessionId } = await b.call("Target.attachToTarget", {
      targetId: target.targetId,
      flatten: true,
    }));
    const tree = await b.call("Page.getFrameTree", {}, sessionId);
    frameId = tree.frameTree.frame.id;
  }
  const world = await b.call(
    "Page.createIsolatedWorld",
    { frameId, worldName: "test-only-origin-probes" },
    sessionId,
  );
  const r = await b.call(
    "Runtime.evaluate",
    {
      contextId: world.executionContextId,
      returnByValue: true,
      expression: `(()=>{const r={heading:document.querySelector('h1')?.textContent,active:document.querySelectorAll('script,style,img,a,form,iframe,object,svg,math').length};for(const key of ['localStorage','sessionStorage']){try{window[key].getItem('gate-sentinel');r[key]='accessible'}catch(e){r[key]=e.name}}try{parent.document.body;r.parent='accessible'}catch(e){r.parent=e.name}try{top.location.href=${JSON.stringify(origin + "/__canary/top")};r.top='allowed'}catch(e){r.top=e.name}r.popup=window.open(${JSON.stringify(origin + "/__canary/popup")})===null;const f=document.createElement('form');f.action=${JSON.stringify(origin + "/__canary/form")};f.method='POST';document.body.append(f);f.submit();f.remove();return r})()`,
    },
    sessionId,
  );
  assert.equal(r.result.value.heading, "Hello");
  assert.equal(r.result.value.active, 0);
  for (const key of ["localStorage", "sessionStorage", "parent", "top"])
    assert.equal(r.result.value[key], "SecurityError");
  assert.equal(r.result.value.popup, true);
  await new Promise((r) => setTimeout(r, 150));
  assert.deepEqual(hits, []);
  assert.equal(
    await b.evaluate("location.href"),
    origin + "/html-previewer/index.html",
  );
});
