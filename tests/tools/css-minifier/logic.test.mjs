import { test } from "node:test";
import assert from "node:assert/strict";
import { logic } from "../task18-logic.mjs";
import { engine } from "../task21-engine.mjs";
const { call } = logic("css-minifier");
test("job adapter validates exact UTF-8 bounds, Unicode and unknown options", () => {
  assert.equal(call("a".repeat(32768)).input.length, 32768);
  assert.throws(() => call("界".repeat(10923)), /32 KiB/);
  assert.throws(() => call("\udfff"));
  assert.throws(() => call("a{}", { mode: "unsafe" }));
});
test("parser/generator compacts normal CSS without merging rules", async () => {
  const r = await engine(
    "css-minifier",
    "/*comment*/ a { color: red; padding: 0px 0px; } a { color: blue; }",
  );
  assert.ok(r.ok);
  assert.equal(r.text, "a{color:red;padding:0px 0px}a{color:blue}");
});
test("strings, escapes, custom-property tokens and license comments are preserved", async () => {
  const r = await engine(
    "css-minifier",
    '/*! license */ .x { --a: red/**/blue; --space: calc(1px + 2px); content: "a; } b"; }',
  );
  assert.ok(r.ok, r.error);
  assert.match(r.text, /\/\*! license \*\//);
  assert.match(r.text, /red\/\*\*\/blue/);
  assert.match(r.text, /calc\(1px \+ 2px\)/);
  assert.match(r.text, /"a; } b"/);
});
test("modern media-range, nesting, layer and property syntax stay parseable", async () => {
  for (const input of [
    "@media(width > 20px){.x{color:red}}",
    "@layer base { .x { & .y { color:red; } } }",
    '@property --x { syntax: "<length>"; inherits: false; initial-value: 0px; }',
  ]) {
    const r = await engine("css-minifier", input);
    assert.ok(r.ok, r.error);
  }
});
test("malformed quotes, comments, URLs, brackets and excess complexity are rejected", async () => {
  for (const input of [
    'a{content:"bad',
    "/* unclosed",
    "a{background:url(x",
    "a{color:red]",
    "a{".repeat(70) + "}".repeat(70),
    "a".repeat(32769),
  ])
    assert.equal(
      (await engine("css-minifier", input)).ok,
      false,
      input.slice(0, 20),
    );
});
test("UTF-8 charset stays first and mismatched encoding is refused", async () => {
  const a = await engine(
    "css-minifier",
    '@charset "UTF-8"; /*! license */ a { color: red; }',
  );
  assert.ok(a.ok, a.error);
  assert.match(a.text, /^@charset "UTF-8";/);
  assert.match(a.text, /license/);
  assert.equal(
    (await engine("css-minifier", '@charset "ISO-8859-1";a{color:red}')).ok,
    false,
  );
});
