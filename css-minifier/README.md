# CSS Minifier

## Task21.1 release proposal

Fresh public verification passed against deployed `9fa032140639550abd9a0449ed7ef5198354bd40`; evidence:
`audit/CSS_MINIFIER_RELEASE_VERIFICATION.json`. Proposed RELEASED
status awaits owner review/merge/deployment; the current deployed registry remains
TESTED. Original development scope below is historical. Known interface/format
limitations remain; no runtime, dependency, privacy or consent change.

Canonical route: `css-minifier/index.html`.

Compact CSS with a reviewed parser and generator, without rule merging.

## Scope and limits

CSS-Tree 3.2.1 parses and prints CSS. No rule merging or value optimization. Strings, custom-property raw values and license comments are preserved; license comments may move after a leading UTF-8 @charset. Only UTF-8 @charset exports are supported. Unsupported constructs may remain raw or fail; browser-specific syntax needs review. CSS is never applied or fetched.

32 KiB UTF-8 input; 256 KiB output; 4,096 parsed nodes and 64 nesting levels. CSS/JavaScript also cap tokens at 8,192. Each job has a 2-second Worker deadline and can be cancelled. Input changes/reset terminate the job and discard its result. Timers do not guarantee a hard memory limit.

## Verification

TESTED — publication pending. Source checkpoint `f6a4ceab5badc73510159a33ed3b13c61f85384c`; evidence: `audit/CSS_MINIFIER_VERIFICATION.json`. Scoped verification passed: 9 canonical inline logic fixtures (job preparation; actual transformation covered separately); 7 canonical Chromium interaction fixtures / 21 assertions; 6 specialized Node Worker/logic tests; 7 extended Chromium tests: actual output, clipboard/download mocks, reset, cancellation, late-result invalidation, keyboard/layout, missing Worker and actual 2-second deadline. Full mapped regression and hosted PR checks remain mandatory before owner review. No public availability or RELEASED claim.
