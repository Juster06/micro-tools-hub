# HTML Previewer

## Task21.1 release proposal

Fresh public verification passed against deployed `9fa032140639550abd9a0449ed7ef5198354bd40`; evidence:
`audit/HTML_PREVIEWER_RELEASE_VERIFICATION.json`. Proposed RELEASED
status awaits owner review/merge/deployment; the current deployed registry remains
TESTED. Original development scope below is historical. Known interface/format
limitations remain; no runtime, dependency, privacy or consent change.

Canonical route: `html-previewer/index.html`.

Preview a safe structural HTML subset in an isolated frame, with no scripts or external resources.

## Scope and limits

Structural tags only. All attributes, styling, images, active and foreign elements are omitted; anchors become plain text. No script execution, parent/storage access, navigation, popups, forms or external resources. Preview has an empty sandbox and restrictive CSP. This is a tested limited preview, not a complete HTML/CSS renderer or universal browser-isolation certification.

32 KiB UTF-8 input; 256 KiB output; 4,096 parsed nodes and 64 nesting levels. CSS/JavaScript also cap tokens at 8,192. Each job has a 2-second Worker deadline and can be cancelled. Input changes/reset terminate the job and discard its result. Timers do not guarantee a hard memory limit.

## Verification

TESTED — publication pending. Source checkpoint `f6a4ceab5badc73510159a33ed3b13c61f85384c`; evidence: `audit/HTML_PREVIEWER_VERIFICATION.json`. Scoped verification passed: 9 canonical inline logic fixtures (job preparation; actual transformation covered separately); 7 canonical Chromium interaction fixtures / 21 assertions; 5 specialized Node Worker/logic tests; 6 extended Chromium tests: actual output, clipboard/download mocks, reset, cancellation, late-result invalidation, keyboard/layout, missing Worker and actual 2-second deadline; 12 actual HTTP preview-isolation tests: canary positive control, malicious fixtures, opaque-origin/storage, blocked top navigation/popup/form. Full mapped regression and hosted PR checks remain mandatory before owner review. No public availability or RELEASED claim.
