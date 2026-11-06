import { format } from "prettier/standalone";
import html from "prettier/plugins/html";
import { boundedParse, canonicalHTML, outputGuard } from "./markup-core.mjs";
self.onmessage = async ({ data }) => {
  try {
    boundedParse(data.input, true);
    if (![2, 4].includes(data.indent) || ![40, 80, 120].includes(data.width))
      throw Error("Unsupported formatting option.");
    let text = await format(data.input, {
      parser: "html",
      plugins: [html],
      tabWidth: data.indent,
      useTabs: false,
      printWidth: data.width,
      htmlWhitespaceSensitivity: "strict",
      embeddedLanguageFormatting: "off",
      endOfLine: "lf",
    });
    if (!data.input.endsWith("\n")) text = text.replace(/\n$/, "");
    outputGuard(text);
    if (canonicalHTML(text, true) !== canonicalHTML(data.input))
      throw Error(
        "Formatting would change parsed content or significant whitespace. Input left unchanged; simplify the markup.",
      );
    self.postMessage({
      ok: true,
      text,
      warning:
        "HTML5 normalization is checked against the parsed document. Strict whitespace mode may break lines inside tag brackets. Embedded JS/CSS is not formatted.",
    });
  } catch (e) {
    self.postMessage({
      ok: false,
      error: e instanceof Error ? e.message : "Unable to format HTML.",
    });
  }
};
