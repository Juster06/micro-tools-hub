# HTML Formatter

Canonical route: `html-formatter/index.html`.

Indent HTML while checking that the parsed content and significant whitespace stay intact.

## Scope and limits

Prettier 3.9.10 HTML with strict whitespace and embedded-language formatting disabled. HTML5 parser normalization is compared before/after; any parsed-content change fails closed. Strict mode may put line breaks inside tag brackets. Some valid documents are refused rather than silently altered. Output is escaped text, never rendered or sanitized; downloaded HTML retains its code and resources.

32 KiB UTF-8 input; 256 KiB output; 4,096 parsed nodes and 64 nesting levels. CSS/JavaScript also cap tokens at 8,192. Each job has a 2-second Worker deadline and can be cancelled. Input changes/reset terminate the job and discard its result. Timers do not guarantee a hard memory limit.

## Verification

TESTED — publication pending. Source checkpoint `f6a4ceab5badc73510159a33ed3b13c61f85384c`; evidence: `audit/HTML_FORMATTER_VERIFICATION.json`. Scoped verification passed: 10 canonical inline logic fixtures (job preparation; actual transformation covered separately); 7 canonical Chromium interaction fixtures / 21 assertions; 6 specialized Node Worker/logic tests; 6 extended Chromium tests: actual output, clipboard/download mocks, reset, cancellation, late-result invalidation, keyboard/layout, missing Worker and actual 2-second deadline. Full mapped regression and hosted PR checks remain mandatory before owner review. No public availability or RELEASED claim.
