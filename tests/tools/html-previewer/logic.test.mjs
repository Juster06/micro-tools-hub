import { test } from "node:test";
import assert from "node:assert/strict";
import { logic } from "../task18-logic.mjs";
import { engine } from "../task21-engine.mjs";
const { call } = logic("html-previewer");
test("input preparation has fixed byte/deadline settings and rejects unsupported options", () => {
  assert.equal(call("<p>x</p>").deadline, 2000);
  assert.throws(() => call("x", { allowScripts: true }));
  assert.throws(() => call("a".repeat(32769)));
  assert.throws(() => call("\udfff"));
});
test("structural content stays visible while all attributes and active content disappear", async () => {
  const r = await engine(
    "html-previewer",
    '<h1 id=x>Hello</h1><p style="color:red" onclick="alert(1)"><a href="https://example.invalid/">safe text</a><img src="https://example.invalid/x"></p><script>globalThis.__task21UnsafeInputRan=99</script><svg><text>x</text></svg>',
  );
  assert.ok(r.ok);
  assert.equal(r.text, "<h1>Hello</h1><p>safe text</p>");
  assert.equal(r.__testExecutionMarker, 0);
  assert.match(r.preview, /default-src 'none'/);
});
test("mutation/foreign/template/raw-text fixtures cannot introduce executable tags", async () => {
  for (const input of [
    "<template><script>bad()</script></template><p>x</p>",
    "<svg><foreignObject><img src=x onerror=bad()></foreignObject></svg>",
    '<math><mtext><table><mglyph><style><!--</style><img title="--><img src=x onerror=bad()>">',
    "<xmp><script>bad()</script></xmp>",
  ]) {
    const r = await engine("html-previewer", input);
    assert.ok(r.ok);
    assert.doesNotMatch(
      r.text,
      /<(?:script|style|img|svg|math|iframe|object|form|input|a)(?:\s|>)/i,
    );
    assert.equal(r.__testExecutionMarker, 0);
  }
});
test("node, depth, byte and attribute limits stop processing with no partial output", async () => {
  for (const input of [
    "<p>x</p>".repeat(2200),
    "<div>".repeat(66) + "x" + "</div>".repeat(66),
    "a".repeat(32769),
    "<p " +
      Array.from({ length: 65 }, (_, i) => "a" + i + '="x"').join(" ") +
      ">x</p>",
  ]) {
    const r = await engine("html-previewer", input);
    assert.equal(r.ok, false);
    assert.equal(r.text, undefined);
  }
});
test("exact 32KiB safe input and escaped literal markup remain local structural HTML", async () => {
  const r = await engine("html-previewer", "<p>" + "a".repeat(32761) + "</p>");
  assert.ok(r.ok);
  const escaped = await engine(
    "html-previewer",
    "<p>&lt;script&gt;café 世界&lt;/script&gt;</p>",
  );
  assert.ok(escaped.ok);
  assert.match(escaped.text, /&lt;script&gt;/);
  assert.ok(Buffer.byteLength(escaped.preview) <= 262144);
});
