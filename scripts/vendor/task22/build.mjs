// Build tooling only. Dependencies must already be installed in an isolated directory.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { createHash } from "node:crypto";
const here = path.dirname(fileURLToPath(import.meta.url)),
  root = path.resolve(here, "../../..");
const dependencies = process.argv[2];
if (!dependencies)
  throw Error(
    "Pass the absolute isolated node_modules directory; no installation is performed.",
  );
const modules = path.resolve(dependencies),
  { build } = await import(
    pathToFileURL(path.join(modules, "esbuild/lib/main.js"))
  );
const expected = JSON.parse(
  fs.readFileSync(path.join(here, "package.json"), "utf8"),
).dependencies;
for (const [name, version] of Object.entries(expected)) {
  const actual = JSON.parse(
    fs.readFileSync(
      path.join(modules, ...name.split("/"), "package.json"),
      "utf8",
    ),
  );
  if (actual.version !== version)
    throw Error("Pinned build dependency mismatch: " + name);
}
const check = process.argv.includes("--check"),
  artifacts = [];
for (const kind of ["markdown"]) {
  const built = await build({
    entryPoints: [path.join(here, "worker.mjs")],
    bundle: true,
    format: "iife",
    platform: "browser",
    minify: true,
    legalComments: "eof",
    nodePaths: [modules],
    write: false,
  });
  const code = built.outputFiles[0].text,
    encoded = JSON.stringify(code).replace(
      /[\u007f-\uffff]/g,
      (c) => "\\u" + c.charCodeAt(0).toString(16).padStart(4, "0"),
    );
  const output =
    "/* Reviewed Task22 local Worker bundle. See THIRD_PARTY_NOTICES.txt and audit/TASK_22_SECURITY_REVIEW.json. */\nwindow.EDB_TASK22_WORKER_SOURCE = " +
    encoded +
    ";\n";
  const relative = "assets/vendor/task22/" + kind + "-source.js",
    target = path.join(root, relative);
  if (check) {
    if (fs.readFileSync(target, "utf8").replace(/\r\n/g, "\n") !== output)
      throw Error("Rebuilt asset differs: " + relative);
  } else fs.writeFileSync(target, output, "utf8");
  artifacts.push({
    path: relative,
    bytes: Buffer.byteLength(output),
    sha256: createHash("sha256").update(output).digest("hex"),
  });
}
console.log(
  JSON.stringify(
    {
      mode: check
        ? "verified reproducible assets"
        : "rebuilt assets; retest and refresh source-bound audit before adoption",
      artifacts,
    },
    null,
    2,
  ),
);
