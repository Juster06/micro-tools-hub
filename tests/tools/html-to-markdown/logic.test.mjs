import { test } from "node:test";
import assert from "node:assert/strict";
import { logic } from "../task18-logic.mjs";
import { engine } from "../task21-engine.mjs";
const { call } = logic("html-to-markdown");
test("job validation bounds text without rendering or evaluating it", () => {
  assert.equal(call("<script>x()</script>").input, "<script>x()</script>");
  assert.throws(() => call("界".repeat(10923)));
  assert.throws(() => call("\udfff"));
});
test("headings, paragraphs, emphasis, lists and code blocks convert as documented", async () => {
  const r = await engine(
    "html-to-markdown",
    "<h1>Hello</h1><p>A <strong>bold</strong> <em>word</em>.</p><ul><li>one</li><li>two</li></ul><pre><code>a &lt; b</code></pre>",
  );
  assert.ok(r.ok);
  for (const s of [
    "# Hello",
    "**bold**",
    "*word*",
    "- one",
    "- two",
    "```\na < b\n```",
  ])
    assert.ok(r.text.includes(s), s);
});
test("Unicode/entities are text and unsafe/obfuscated link destinations are omitted", async () => {
  const r = await engine(
    "html-to-markdown",
    '<p>café 世界 &amp; 😀 <a href="jav&#x61;script:alert(1)">bad</a> <a href="https://example.invalid/a(b)">good</a></p>',
  );
  assert.ok(r.ok);
  assert.match(r.text, /café 世界 & 😀/);
  assert.doesNotMatch(r.text, /javascript|alert/);
  assert.match(r.text, /\[good\]\(https:\/\/example.invalid\/a%28b%29\)/);
});
test("raw scripts/styles/foreign content are omitted without execution", async () => {
  const r = await engine(
    "html-to-markdown",
    "<script>globalThis.__task21UnsafeInputRan=99</script><style>p{color:red}</style><svg><text>foreign</text></svg><p>safe</p>",
  );
  assert.ok(r.ok);
  assert.equal(r.text, "safe\n");
  assert.equal(r.__testExecutionMarker, 0);
  assert.match(r.warning, /omitted/);
});
test("code fences grow to preserve embedded backticks and pre whitespace", async () => {
  const r = await engine(
    "html-to-markdown",
    "<pre><code>```\n  line\n```</code></pre>",
  );
  assert.ok(r.ok);
  assert.match(r.text, /````\n```\n  line\n```\n````/);
});
test("malformed HTML repair is bounded and node/depth/input excess fails", async () => {
  assert.ok((await engine("html-to-markdown", "<p>Hello")).ok);
  for (const input of [
    "a".repeat(32769),
    "<div>".repeat(66) + "x" + "</div>".repeat(66),
    "<p>x</p>".repeat(2200),
  ])
    assert.equal((await engine("html-to-markdown", input)).ok, false);
});
