import {
  parse,
  parseFragment,
  defaultTreeAdapter as native,
  serialize,
} from "parse5";
export const LIMITS = Object.freeze({
  input: 32768,
  output: 262144,
  nodes: 4096,
  depth: 64,
  attributes: 64,
  deadline: 2000,
});
const utf8 = new TextEncoder();
export function inputGuard(input, maximum = LIMITS.input) {
  if (typeof input !== "string") throw Error("Enter text.");
  if (input.length > maximum || utf8.encode(input).length > maximum)
    throw Error("Input exceeds " + maximum / 1024 + " KiB UTF-8.");
  if (!input.trim()) throw Error("Enter HTML.");
  if (
    /[\uD800-\uDFFF]/u.test(
      input.replace(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g, ""),
    )
  )
    throw Error("Unpaired Unicode surrogate.");
  return input;
}
export function boundedParse(input, document = false, maximum = LIMITS.input) {
  inputGuard(input, maximum);
  let nodes = 0;
  const charge = () => {
    if (++nodes > LIMITS.nodes) throw Error("HTML exceeds 4,096 nodes.");
  };
  const depth = (parent) => {
    let n = 0;
    for (let p = parent; p; p = p.parentNode)
      if (++n > LIMITS.depth) throw Error("HTML exceeds 64 nesting levels.");
  };
  const adapter = {
    ...native,
    createDocument() {
      charge();
      return native.createDocument();
    },
    createDocumentFragment() {
      charge();
      return native.createDocumentFragment();
    },
    createElement(tag, ns, attrs) {
      charge();
      if (attrs.length > LIMITS.attributes)
        throw Error("HTML exceeds 64 attributes per element.");
      return native.createElement(tag, ns, attrs);
    },
    createCommentNode(text) {
      charge();
      return native.createCommentNode(text);
    },
    createTextNode(text) {
      charge();
      return native.createTextNode(text);
    },
    appendChild(p, n) {
      depth(p);
      native.appendChild(p, n);
    },
    insertBefore(p, n, r) {
      depth(p);
      native.insertBefore(p, n, r);
    },
    insertText(p, text) {
      depth(p);
      if (!p.childNodes.at(-1) || p.childNodes.at(-1).nodeName !== "#text")
        charge();
      native.insertText(p, text);
    },
    insertTextBefore(p, text, r) {
      depth(p);
      const before = p.childNodes[p.childNodes.indexOf(r) - 1];
      if (!before || before.nodeName !== "#text") charge();
      native.insertTextBefore(p, text, r);
    },
    adoptAttributes(n, attrs) {
      if (n.attrs.length + attrs.length > LIMITS.attributes)
        throw Error("HTML exceeds 64 attributes per element.");
      native.adoptAttributes(n, attrs);
    },
  };
  const tree = (document ? parse : parseFragment)(input, {
    treeAdapter: adapter,
    scriptingEnabled: true,
  });
  let seen = 0,
    stack = [[tree, 0]];
  while (stack.length) {
    const [n, d] = stack.pop();
    if (++seen > LIMITS.nodes || d > LIMITS.depth)
      throw Error("HTML complexity limit exceeded.");
    for (const c of n.childNodes ?? []) stack.push([c, d + 1]);
    if (n.content) stack.push([n.content, d + 1]);
  }
  return tree;
}
export function outputGuard(text) {
  if (utf8.encode(text).length > LIMITS.output)
    throw Error("Output exceeds 256 KiB.");
  return text;
}
export const canonicalHTML = (input, generatedOutput = false) =>
  serialize(
    boundedParse(input, true, generatedOutput ? LIMITS.output : LIMITS.input),
  );
const escape = (text) =>
  text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const allowed = new Set(
  "div span p h1 h2 h3 h4 h5 h6 ul ol li blockquote pre code em strong b i u s del sub sup br hr table thead tbody tfoot tr td th caption dl dt dd abbr".split(
    " ",
  ),
);
const removed = new Set(
  "script style template noscript iframe frame frameset object embed img image picture source audio video track link meta base input button select option textarea form dialog portal fencedframe".split(
    " ",
  ),
);
export const CSP =
  "default-src 'none';script-src 'none';style-src 'none';img-src 'none';font-src 'none';media-src 'none';connect-src 'none';frame-src 'none';object-src 'none';base-uri 'none';form-action 'none'";
export function preview(input) {
  const tree = boundedParse(input);
  let parts = [],
    bytes = 0,
    omissions = 0;
  const add = (s) => {
    bytes += utf8.encode(s).length;
    if (bytes > LIMITS.output) throw Error("Output exceeds 256 KiB.");
    parts.push(s);
  };
  function visit(n) {
    if (n.nodeName === "#text") {
      add(escape(n.value));
      return;
    }
    if (
      (n.namespaceURI && n.namespaceURI !== "http://www.w3.org/1999/xhtml") ||
      removed.has(n.tagName)
    ) {
      omissions++;
      return;
    }
    const keep = allowed.has(n.tagName);
    if (n.attrs?.length) omissions += n.attrs.length;
    if (n.tagName && !keep) omissions++;
    if (keep) add("<" + n.tagName + ">");
    for (const c of n.childNodes ?? []) visit(c);
    if (keep && !["br", "hr"].includes(n.tagName)) add("</" + n.tagName + ">");
  }
  visit(tree);
  const text = parts.join("");
  return {
    text,
    preview:
      '<!doctype html><html><head><meta http-equiv="Content-Security-Policy" content="' +
      CSP +
      '"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>' +
      text +
      "</body></html>",
    warning: omissions
      ? "Active, foreign, unsupported elements and all attributes were omitted."
      : "Safe structural HTML subset; styles, resources and interactive behavior are not supported.",
  };
}
const mdEscape = (t) =>
  t.replace(/\\/g, "\\\\").replace(/([`*_{}\[\]<>])/g, "\\$1");
function safeLink(value) {
  if (typeof value !== "string" || /[\u0000-\u0020\u007f]/.test(value))
    return null;
  if (!/^(https?:\/\/|mailto:|#|\/(?!\/)|\.\.?\/)/i.test(value)) return null;
  return value.replace(/[()]/g, (c) => (c === "(" ? "%28" : "%29"));
}
export function markdown(input) {
  const root = boundedParse(input);
  let unsupported = 0;
  const textOf = (n) =>
    n.nodeName === "#text"
      ? n.value
      : (n.childNodes ?? []).map(textOf).join("");
  function join(parts) {
    let out = "";
    for (let part of parts) {
      if (out.endsWith("\n") && !part.trim()) continue;
      if (out.endsWith("\n") && part.startsWith("\n")) {
        let a = 0,
          b = 0;
        while (out[out.length - 1 - a] === "\n") a++;
        while (part[b] === "\n") b++;
        part = part.slice(Math.min(b, Math.max(0, a + b - 2)));
      }
      out += part;
    }
    return out;
  }
  function node(n, level = 0) {
    if (n.nodeName === "#text") return mdEscape(n.value.replace(/\s+/g, " "));
    if (
      (n.namespaceURI && n.namespaceURI !== "http://www.w3.org/1999/xhtml") ||
      ["script", "style", "template", "noscript"].includes(n.tagName)
    ) {
      unsupported++;
      return "";
    }
    const children = () =>
      join((n.childNodes ?? []).map((c) => node(c, level)));
    if (/^h[1-6]$/.test(n.tagName ?? ""))
      return (
        "\n\n" +
        "#".repeat(Number(n.tagName[1])) +
        " " +
        children().trim() +
        "\n\n"
      );
    if (
      ["p", "div", "section", "article", "header", "footer", "main"].includes(
        n.tagName,
      )
    )
      return "\n\n" + children().trim() + "\n\n";
    if (n.tagName === "br") return "  \n";
    if (n.tagName === "hr") return "\n\n---\n\n";
    if (["strong", "b", "em", "i", "del", "s"].includes(n.tagName)) {
      const m = ["strong", "b"].includes(n.tagName)
        ? "**"
        : ["em", "i"].includes(n.tagName)
          ? "*"
          : "~~";
      return m + children() + m;
    }
    if (n.tagName === "a") {
      const label = children(),
        href = safeLink(n.attrs.find((x) => x.name === "href")?.value);
      if (!href) {
        unsupported++;
        return label;
      }
      return "[" + label + "](" + href + ")";
    }
    if (n.tagName === "pre") {
      const value = textOf(n),
        runs = value.match(/`+/g) ?? [],
        fence = "`".repeat(Math.max(3, ...runs.map((x) => x.length + 1)));
      return (
        "\n\n" + fence + "\n" + value.replace(/\n$/, "") + "\n" + fence + "\n\n"
      );
    }
    if (n.tagName === "code") {
      const value = textOf(n),
        runs = value.match(/`+/g) ?? [],
        fence = "`".repeat(Math.max(1, ...runs.map((x) => x.length + 1)));
      const pad = /^`|`$|^ | $/.test(value) ? " " : "";
      return fence + pad + value + pad + fence;
    }
    if (n.tagName === "blockquote")
      return (
        "\n\n" +
        children()
          .trim()
          .split("\n")
          .map((s) => "> " + s)
          .join("\n") +
        "\n\n"
      );
    if (["ul", "ol"].includes(n.tagName)) {
      let index = 1;
      const start = Number(n.attrs?.find((a) => a.name === "start")?.value);
      if (
        n.tagName === "ol" &&
        Number.isInteger(start) &&
        start > 0 &&
        start <= 1000000
      )
        index = start;
      return (
        "\n" +
        (n.childNodes ?? [])
          .filter((c) => c.tagName === "li")
          .map((c) => {
            const prefix = n.tagName === "ol" ? index++ + ". " : "- ";
            const value = (c.childNodes ?? [])
              .map((x) => node(x, level + 1))
              .join("")
              .trim();
            return (
              "  ".repeat(level) +
              prefix +
              value.replace(/\n(?!\n)/g, "\n" + "  ".repeat(level + 1))
            );
          })
          .join("\n") +
        "\n"
      );
    }
    if (n.tagName === "img") {
      unsupported++;
      return mdEscape(n.attrs.find((x) => x.name === "alt")?.value ?? "");
    }
    if (n.tagName && !["span", "li"].includes(n.tagName)) unsupported++;
    return children();
  }
  const text = outputGuard(node(root).trim() + "\n");
  return {
    text,
    warning: unsupported
      ? "Unsupported structures were flattened or omitted; scripts/styles are omitted and unsafe links lose their destination."
      : "Common Markdown subset. Whitespace outside code is normalized; no visual rendering or automatic link navigation.",
  };
}
