import { parse } from "acorn";
import { minify } from "terser";
const enc = new TextEncoder();
self.onmessage = async ({ data }) => {
  try {
    const input = data.input;
    if (typeof input !== "string" || !input.trim())
      throw Error("Enter JavaScript.");
    if (input.length > 32768 || enc.encode(input).length > 32768)
      throw Error("Input exceeds 32 KiB UTF-8.");
    if (!["script", "module"].includes(data.mode))
      throw Error("Choose script or module.");
    let tokens = 0;
    const ast = parse(input, {
      ecmaVersion: "latest",
      sourceType: data.mode,
      allowHashBang: true,
      onToken() {
        if (++tokens > 8192) throw Error("JavaScript exceeds 8,192 tokens.");
      },
    });
    let count = 0,
      stack = [[ast, 0]];
    while (stack.length) {
      const [n, d] = stack.pop();
      if (!n || typeof n !== "object") continue;
      if (typeof n.type === "string") {
        if (++count > 4096 || d > 64)
          throw Error(
            "JavaScript complexity exceeds 4,096 nodes or 64 levels.",
          );
      }
      for (const [key, v] of Object.entries(n)) {
        if (["start", "end", "raw"].includes(key)) continue;
        if (Array.isArray(v))
          for (const c of v)
            if (c && typeof c === "object") stack.push([c, d + 1]);
            else {
            }
        else if (v && typeof v === "object") stack.push([v, d + 1]);
      }
    }
    const result = await minify(input, {
      module: data.mode === "module",
      compress: false,
      mangle: false,
      sourceMap: false,
      format: { comments: "some", ascii_only: false, semicolons: true },
    });
    const text = result.code;
    if (typeof text !== "string" || enc.encode(text).length > 262144)
      throw Error("Output exceeds 256 KiB.");
    self.postMessage({
      ok: true,
      text,
      warning:
        "Plain JavaScript script/module syntax accepted by both Acorn and Terser. No TypeScript/JSX; compression and name mangling are disabled. License comments are retained. Code is parsed and printed, never executed.",
    });
  } catch (e) {
    self.postMessage({
      ok: false,
      error: e instanceof Error ? e.message : "Unable to minify JavaScript.",
    });
  }
};
