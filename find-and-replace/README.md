# Find and Replace

Registry ID: `find-and-replace`. Canonical route: `find-and-replace/index.html`. Category: text. Task 7 utility released after independent public behavior/deployed-source verification on 2026-11-01. Current lifecycle: RELEASED / REQUIRED_PASSED. [Live tool](https://everydaydigitalbox.com/find-and-replace/); [release audit](../audit/FIND_AND_REPLACE_RELEASE_VERIFICATION.json). Original local evidence is retained unchanged.

Preview literal replacements, keep your original, and apply only when ready.

## Exact behavior and defaults

Literal global, non-overlapping matches, left to right. Search text is escaped; no regex entry is executed. Replacement strings, including dollar signs, are inserted exactly, not interpreted as replacement templates. Case-sensitive is on by default. Off uses JavaScript Unicode regex simple case folding (iu), not locale-specific or full case folding; offsets refer to original text. Canonically different accent sequences stay different. Empty search is guarded with an explicit message, including on empty input; an empty replacement deletes matches. Search and replacement each allow 10,000 UTF-16 units; output is capped at 1,000,000 units before joining. Input, search and replacement are never silently truncated. Pure logic preserves LF/CRLF/CR and all Unicode text; browser textareas normalize line endings to LF. Preview never changes original input. Apply result explicitly replaces input and saves one undo snapshot; Undo restores that input once without resetting current search settings. Manual input edits discard undo. Changing options retains the last applicable undo snapshot. Apply is disabled for unchanged or oversized results; copy/download remain available for valid nonempty results. No draft is persisted.

## Interface and safety

Live preview uses a 120 ms debounce and immediate invalidation of obsolete output, counts and actions. Input and option composition events defer computation. Clear restores documented defaults and input focus. Clipboard completion is revision-guarded; denied/unavailable clipboard access selects the current result and gives manual-copy instructions. UTF-8 `.txt` downloads use a fixed filename and release temporary object URLs, including on failure.

100,000 UTF-16 input units; no silent maxlength truncation. Unicode/emoji are not counted as visual graphemes. All output uses textarea values/textContent. No input transport or persistence. The external Tailwind Play CDN supplies styling; expanded inline fallback CSS preserves usability when it is blocked. No package installation, application backend or build step is needed to open this standalone page.

## Independent verification

Run `python scripts/test_tool.py --id find-and-replace` and `node --test --test-concurrency=1 tests/tools/find-and-replace/*.test.mjs` from the checkout. The framework runs explicit exact JSON fixtures and real installed Chromium interaction cases; additional suites cover boundaries, stale operations, composition, no user-input transport/persistence, UTF-8 downloads and error paths. Committed audit evidence records only actually executed results and hashes. Integration tests are run after local homepage preparation.

Browser tests use isolated Edge/Chromium profiles, block external HTTP(S), simulate clipboard success/denial, and capture download Blobs in memory. Composition events are simulated. Mobile checks use viewport emulation at 320 and 375 pixels, plus 768/1440. This is not screen-reader, physical-device, native IME/clipboard/save-dialog or all-browser certification. Limits are bounded host test fixtures, not universal performance guarantees. See the Task 7 plan and audit for final results.

## Historical Task 7 verified local checkpoint

Lifecycle: TESTED / REQUIRED_PASSED; publication null. Source revision `588f761e819ce9a9ae04732584bea5b7ce8ccb3d`; normalized HTML SHA-256 `b6a0d254ee8de1047bec187c58e2aea71c67c00cc4734bc48f523cd347f9e058`. See [scoped audit](../audit/FIND_AND_REPLACE_VERIFICATION.json).

Passed 33 exact framework logic fixtures plus 9 independent Node logic tests; 18 framework browser cases / 54 assertions, 12 extended real browser cases, and 2 actual hub/navigation/search cases (32 browser cases total for this utility). Full project regression: Python 123/123, Node 158/158 sequentially, six released-tool framework browser regressions 56 cases/242 assertions, neutral templates 6 logic/12 browser/48 assertions, project validation zero errors/warnings. All three local hub cards remain publication pending; existing six released tools are unchanged. This checkpoint does not claim deployment or release.

## Verified release

PR #11 merged normally as `d3ddb6de807913c05832e24a77797f033b353497` at 2026-11-01T22:51:53Z. Actual successful [Pages implementation run 41359251674](https://github.com/Juster06/micro-tools-hub/actions/runs/41359251674), independent live browser behavior and exact approved public source hashes passed before each RELEASED transition. Original local audits/source checkpoints remain preserved. Current inventory: 93 total, 9 RELEASED, 0 TESTED, 15 READY, 68 PLANNED, 1 BLOCKED; milestone 9/25 (36%).

This utility independently passed 29 actual public browser cases/checkpoints. Complete public HTML/inline JavaScript/CSS matches its approved hash. Copy APIs were simulated and UTF-8 download Blob/content/bytes/revocation inspected in memory. Release metadata deployment and final local regressions/shortcut results are recorded in the latest handoff and release audit; implementation source remains unchanged. No Task 8 work is authorized.
