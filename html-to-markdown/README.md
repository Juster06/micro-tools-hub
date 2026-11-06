# HTML to Markdown

Canonical route: `html-to-markdown/index.html`.

Convert common HTML structures to Markdown text without executing or rendering markup.

## Scope and limits

Bounded parse5 8.1.0 conversion supports headings, paragraphs, lists, links, emphasis and code blocks. Whitespace outside code normalizes. Scripts/styles/foreign content are omitted; unsupported structures flatten or omit with a notice. Only explicit HTTP(S), mailto, fragment and local relative link forms retain destinations. Tables, forms, styling and exact browser layout are unsupported. Output is plain text, not a rendered Markdown preview.

32 KiB UTF-8 input; 256 KiB output; 4,096 parsed nodes and 64 nesting levels. CSS/JavaScript also cap tokens at 8,192. Each job has a 2-second Worker deadline and can be cancelled. Input changes/reset terminate the job and discard its result. Timers do not guarantee a hard memory limit.

## Verification

TESTED — publication pending. Source checkpoint `f6a4ceab5badc73510159a33ed3b13c61f85384c`; evidence: `audit/HTML_TO_MARKDOWN_VERIFICATION.json`. Scoped verification passed: 9 canonical inline logic fixtures (job preparation; actual transformation covered separately); 7 canonical Chromium interaction fixtures / 21 assertions; 6 specialized Node Worker/logic tests; 6 extended Chromium tests: actual output, clipboard/download mocks, reset, cancellation, late-result invalidation, keyboard/layout, missing Worker and actual 2-second deadline. Full mapped regression and hosted PR checks remain mandatory before owner review. No public availability or RELEASED claim.
