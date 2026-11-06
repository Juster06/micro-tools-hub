import * as css from "css-tree";
import { preflight } from "./css-preflight.mjs";
const enc = new TextEncoder();
self.onmessage = ({ data }) => {
  try {
    const input = data.input;
    if (typeof input !== "string" || !input.trim()) throw Error("Enter CSS.");
    if (input.length > 32768 || enc.encode(input).length > 32768)
      throw Error("Input exceeds 32 KiB UTF-8.");
    if (!input.isWellFormed()) throw Error("Unpaired Unicode surrogate.");
    preflight(input);
    let nodes = 0,
      depth = 0;
    const comments = [];
    const ast = css.parse(input, {
      onParseError: (e) => {
        throw e;
      },
      onComment(value) {
        if (value.startsWith("!")) comments.push("/*" + value + "*/");
      },
    });
    css.walk(ast, {
      enter() {
        if (++nodes > 4096 || ++depth > 64)
          throw Error("CSS complexity exceeds 4,096 nodes or 64 levels.");
      },
      leave() {
        depth--;
      },
    });
    let text = css.generate(ast);
    const first = ast.children.first;
    if (first?.type === "Atrule" && first.name.toLowerCase() === "charset") {
      const directive = css.generate(first);
      if (!/^[^\"]*\"utf-8\";$/i.test(directive))
        throw Error("Only UTF-8 @charset is supported for UTF-8 download.");
      text = directive + comments.join("") + text.slice(directive.length);
    } else text = comments.join("") + text;
    if (enc.encode(text).length > 262144)
      throw Error("Output exceeds 256 KiB.");
    self.postMessage({
      ok: true,
      text,
      warning:
        "CSS-Tree 3.2.1 parses and prints compact syntax without rule merging, identifier changes or value optimization. Custom-property raw values and license comments are retained. Unsupported syntax is rejected or preserved as raw text.",
    });
  } catch (e) {
    self.postMessage({
      ok: false,
      error: e instanceof Error ? e.message : "Unable to minify CSS.",
    });
  }
};
