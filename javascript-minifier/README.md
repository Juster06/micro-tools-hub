# JavaScript Minifier

Canonical route: `javascript-minifier/index.html`.

Remove optional JavaScript formatting without running the supplied code.

## Scope and limits

Acorn 8.19.0 and Terser 5.51.2 must both accept plain JavaScript. Choose script or module. Compression, name mangling and source maps are disabled. License comments remain. TypeScript, JSX and syntax beyond both parsers are unsupported. Input and output are never executed.

32 KiB UTF-8 input; 256 KiB output; 4,096 parsed nodes and 64 nesting levels. CSS/JavaScript also cap tokens at 8,192. Each job has a 2-second Worker deadline and can be cancelled. Input changes/reset terminate the job and discard its result. Timers do not guarantee a hard memory limit.

## Verification

TESTED — publication pending. Source checkpoint `f6a4ceab5badc73510159a33ed3b13c61f85384c`; evidence: `audit/JAVASCRIPT_MINIFIER_VERIFICATION.json`. Scoped verification passed: 10 canonical inline logic fixtures (job preparation; actual transformation covered separately); 7 canonical Chromium interaction fixtures / 21 assertions; 6 specialized Node Worker/logic tests; 6 extended Chromium tests: actual output, clipboard/download mocks, reset, cancellation, late-result invalidation, keyboard/layout, missing Worker and actual 2-second deadline. Full mapped regression and hosted PR checks remain mandatory before owner review. No public availability or RELEASED claim.
