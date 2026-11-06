import { test } from "node:test";
import assert from "node:assert/strict";
import { parse } from "../../vendor/acorn-8.19.0.mjs";
import { logic } from "../task18-logic.mjs";
import { engine } from "../task21-engine.mjs";
const { call } = logic("javascript-minifier");
function strip(n) {
  if (Array.isArray(n)) return n.map(strip);
  if (n && typeof n === "object")
    return Object.fromEntries(
      Object.entries(n)
        .filter(([k]) => !["start", "end", "raw"].includes(k))
        .map(([k, v]) => [k, strip(v)]),
    );
  return n;
}
test("job adapter has explicit mode, Unicode and UTF-8 bounds", () => {
  assert.equal(call("let x=1;", { mode: "module" }).mode, "module");
  assert.throws(() => call("x", { mode: "typescript" }));
  assert.throws(() => call("😀".repeat(8193)));
  assert.throws(() => call("\udfff"));
});
test("independent Acorn ASTs agree before/after minification for representative semantics", async () => {
  for (const input of [
    "function add(a,b){ return a + b; }",
    "function f(){return\n1;}",
    "const x=/a+b/giu;const s=`hello ${2 + 3}`;",
    "class X { #x=1; f(){ return this?.#x ?? 0; } }",
    'const n=123n; const text="café 世界";',
  ]) {
    const r = await engine("javascript-minifier", input);
    assert.ok(r.ok, r.error);
    assert.deepEqual(
      strip(parse(r.text, { ecmaVersion: "latest" })),
      strip(parse(input, { ecmaVersion: "latest" })),
    );
  }
});
test("module syntax, license comments and names are retained without mangling/compression", async () => {
  const r = await engine(
    "javascript-minifier",
    "/*! licence */ export function longName(value) { return value + 0; }",
    { mode: "module" },
  );
  assert.ok(r.ok);
  assert.match(r.text, /licence/);
  assert.match(r.text, /longName\(value\)/);
  assert.match(r.text, /value\+0/);
});
test("source with a sentinel assignment is printed, never executed", async () => {
  const r = await engine(
    "javascript-minifier",
    "globalThis.__task21UnsafeInputRan = 99;",
  );
  assert.ok(r.ok);
  assert.equal(r.__testExecutionMarker, 0);
  assert.match(r.text, /99/);
});
test("syntax errors, unsupported TypeScript/JSX and over-budget input fail clearly", async () => {
  for (const input of [
    "function (",
    "const x: number = 1;",
    "const x = <div/>;",
    "x".repeat(32769),
  ])
    assert.equal((await engine("javascript-minifier", input)).ok, false);
});
test("deep or node-heavy programs are refused rather than returning partial code", async () => {
  for (const input of [
    "const x=" + "[".repeat(70) + "1" + "]".repeat(70) + ";",
    "let x=0;".repeat(1500),
  ])
    assert.equal((await engine("javascript-minifier", input)).ok, false);
});
