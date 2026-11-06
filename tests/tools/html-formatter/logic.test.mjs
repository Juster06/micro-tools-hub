import { test } from "node:test";
import assert from "node:assert/strict";
import { logic } from "../task18-logic.mjs";
import { engine } from "../task21-engine.mjs";
const { call } = logic("html-formatter");
test("job adapter enforces UTF-8, Unicode, option and boundary rules", () => {
  assert.equal(call("😀".repeat(8192)).input.length, 16384);
  assert.throws(() => call("😀".repeat(8193)), /32 KiB/);
  assert.throws(() => call("\ud800"), /surrogate/);
  assert.equal(call("x", { indent: 4, width: 40 }).indent, 4);
  assert.throws(() => call("x", { indent: 3 }));
});
test("actual formatter preserves significant inline/preformatted text, Unicode and entities", async () => {
  for (const input of [
    "<p>Hello <strong>世界</strong>!</p>",
    "<div><span>a</span><span>b</span></div>",
    "<pre> A\n  B </pre>",
    "<p>Tom &amp; Jerry</p>",
  ]) {
    const r = await engine("html-formatter", input);
    assert.ok(r.ok, r.error);
    assert.ok(r.text.includes(">"));
  }
});
test("indentation and width options affect structured tag formatting", async () => {
  const input =
    '<div first="long-long-long-value" second="another-long-value"><span>Hello</span></div>';
  const a = await engine("html-formatter", input, { indent: 2, width: 40 }),
    b = await engine("html-formatter", input, { indent: 4, width: 40 });
  assert.ok(a.ok && b.ok);
  assert.notEqual(a.text, b.text);
  assert.match(b.text, /\n {4}/);
});
test("content-changing formatting is rejected; raw script-looking HTML never executes", async () => {
  const r = await engine(
    "html-formatter",
    "<script>globalThis.__task21UnsafeInputRan=99</script><p>&amp;</p>",
  );
  assert.equal(r.ok, false);
  assert.match(r.error, /change parsed content/);
  assert.equal(r.__testExecutionMarker, 0);
});
test("malformed tags, nesting and UTF-8 overflow fail in the Worker", async () => {
  for (const input of [
    "<div ".repeat(5000),
    "<div>".repeat(66) + "x" + "</div>".repeat(66),
    "a".repeat(32769),
  ])
    assert.equal((await engine("html-formatter", input)).ok, false);
});
test("exact 32KiB simple input and HTML5 repair retain content", async () => {
  assert.ok(
    (await engine("html-formatter", "<p>" + "a".repeat(32761) + "</p>")).ok,
  );
  const r = await engine("html-formatter", "<div><");
  assert.ok(r.ok);
  assert.ok(r.text.includes("<"));
});
