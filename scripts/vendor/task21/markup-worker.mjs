import { preview, markdown } from "./markup-core.mjs";
self.onmessage = ({ data }) => {
  try {
    if (!["html-previewer", "html-to-markdown"].includes(data.tool))
      throw Error("Unknown operation.");
    self.postMessage({
      ok: true,
      ...(data.tool === "html-previewer"
        ? preview(data.input)
        : markdown(data.input)),
    });
  } catch (e) {
    self.postMessage({
      ok: false,
      error: e instanceof Error ? e.message : "Unable to process HTML.",
    });
  }
};
