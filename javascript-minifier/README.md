# JavaScript Minifier

Canonical route: `javascript-minifier/index.html`.

Remove optional JavaScript formatting without running the supplied code.

## Scope and limits

Acorn 8.19.0 and Terser 5.51.2 must both accept plain JavaScript. Choose script or module. Compression, name mangling and source maps are disabled. License comments remain. TypeScript, JSX and syntax beyond both parsers are unsupported. Input and output are never executed.

32 KiB UTF-8 input; 256 KiB output; 4,096 parsed nodes and 64 nesting levels. CSS/JavaScript also cap tokens at 8,192. Each job has a 2-second Worker deadline and can be cancelled. Input changes/reset terminate the job and discard its result. Timers do not guarantee a hard memory limit.

## Verification

Development in progress; no TESTED or public-release claim yet. Required tests and source-bound evidence must pass before status changes.
