// Executes only reviewed, checked-in Worker bundles. Input strings are never code.
import fs from "node:fs";
import vm from "node:vm";
import { Worker } from "node:worker_threads";
export function sourceFor(id) {
  if (id === "hashtag-counter") {
    const html = fs.readFileSync(
      new URL("../../hashtag-counter/index.html", import.meta.url),
      "utf8",
    );
    const code = html.match(
      /<script id="edb-tool-logic">([\s\S]*?)<\/script>/,
    )[1];
    return (
      "self.window=self;" +
      code +
      ';self.onmessage=({data})=>{try{self.postMessage({ok:true,...EDB_TOOL.analyze(data.input,{casePolicy:data.casePolicy??"fold"})});}catch(e){self.postMessage({ok:false,error:e.message});}};'
    );
  }
  const kind = {
    "html-formatter": "format",
    "css-minifier": "css",
    "javascript-minifier": "javascript",
    "html-to-markdown": "markup",
    "html-previewer": "markup",
  }[id];
  const context = vm.createContext({ window: {} });
  vm.runInContext(
    fs.readFileSync(
      new URL(
        "../../assets/vendor/task21/" + kind + "-source.js",
        import.meta.url,
      ),
      "utf8",
    ),
    context,
    { timeout: 1000 },
  );
  return context.window.EDB_TASK21_WORKER_SOURCE;
}
export async function engine(id, input, options = {}) {
  const code = sourceFor(id);
  return await new Promise((resolve, reject) => {
    const worker = new Worker(
      `const{parentPort}=require('node:worker_threads');globalThis.self=globalThis;globalThis.__task21UnsafeInputRan=0;self.postMessage=data=>parentPort.postMessage({...data,__testExecutionMarker:globalThis.__task21UnsafeInputRan});${code}\nparentPort.on('message',data=>self.onmessage({data}));`,
      {
        eval: true,
        resourceLimits: {
          maxOldGenerationSizeMb: 96,
          maxYoungGenerationSizeMb: 16,
          stackSizeMb: 4,
        },
      },
    );
    const timer = setTimeout(() => {
      worker.terminate();
      reject(Error("Test Worker exceeded 2-second deadline"));
    }, 2000);
    worker.once("message", (r) => {
      clearTimeout(timer);
      worker.terminate();
      resolve(r);
    });
    worker.once("error", (e) => {
      clearTimeout(timer);
      worker.terminate();
      reject(e);
    });
    worker.postMessage({
      tool: id,
      input,
      indent: 2,
      width: 80,
      mode: "script",
      ...options,
    });
  });
}
