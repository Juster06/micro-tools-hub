import { test } from "node:test";
import assert from "node:assert/strict";
import vm from "node:vm";
import { logic } from "../task18-logic.mjs";
import { engine } from "../task21-engine.mjs";
const { call, context } = logic("hashtag-counter");
function analyze(input, options = {}) {
  context.sourceInput = input;
  context.sourceOptions = options;
  return JSON.parse(
    vm.runInContext(
      "JSON.stringify(EDB_TOOL.analyze(sourceInput,sourceOptions))",
      context,
      { timeout: 1000 },
    ),
  );
}
test("caption extraction excludes URLs, attached fragments and C# while preserving occurrence order", () => {
  const r = analyze(
    "C# C#code word#no /#fragment https://example.invalid/a?#no www.example.invalid/#no (#Yes), 😀#世界 #_tag #2tag",
  );
  assert.equal(r.text, "#Yes #世界 #_tag #2tag");
  assert.equal(r.occurrences, 4);
  assert.equal(r.unique, 4);
});
test("NFC normalization and explicit exact/lowercase duplicate policies", () => {
  const r = analyze("#cafe\u0301 #café #CAFÉ");
  assert.equal(r.unique, 1);
  assert.equal(r.duplicates[0].count, 3);
  assert.equal(r.text, "#café #café #CAFÉ");
  assert.equal(analyze("#A #a", { casePolicy: "exact" }).unique, 2);
  assert.equal(analyze("#Straße #STRASSE").unique, 2);
});
test("all caption/tag/occurrence boundaries fail without truncation", () => {
  assert.equal(call("a".repeat(100000)), "");
  assert.throws(() => call("a".repeat(100001)), /100,000/);
  assert.equal(analyze("#" + "界".repeat(100)).occurrences, 1);
  assert.throws(() => call("#" + "界".repeat(101)), /100 Unicode/);
  assert.equal(analyze("#a ".repeat(10000)).occurrences, 10000);
  assert.throws(() => call("#a ".repeat(10001)), /10,000/);
});
test("empty, malformed Unicode, invalid settings and non-tags have explicit results", () => {
  for (const value of ["", null, {}, "\udfff"])
    assert.throws(() => call(value));
  assert.throws(() => call("#a", { casePolicy: "unsupported" }));
  assert.throws(() => call("#a", { extra: true }));
  assert.equal(call("##no #😀 #\u0301x plain"), "");
});
test("real Worker performs the same extraction and never executes script-looking captions", async () => {
  const r = await engine(
    "hashtag-counter",
    "<script>globalThis.__task21UnsafeInputRan=99</script> #hello",
  );
  assert.ok(r.ok);
  assert.equal(r.text, "#hello");
  assert.equal(r.__testExecutionMarker, 0);
});
