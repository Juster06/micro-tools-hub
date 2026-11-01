# Slug Generator

Registry ID: `slug-generator`. Canonical route: `slug-generator/index.html`. Category: text. Task 7 utility released after independent public behavior/deployed-source verification on 2026-11-01. Current lifecycle: RELEASED / REQUIRED_PASSED. [Live tool](https://everydaydigitalbox.com/slug-generator/); [release audit](../audit/SLUG_GENERATOR_RELEASE_VERIFICATION.json). Original local evidence is retained unchanged.

Turn a title or phrase into a tidy, URL-friendly slug.

## Exact behavior and defaults

One slug for the entire input. Native Unicode lowercase runs first. Remove accent marks is on by default: normalize NFD and remove Unicode combining marks. This also affects non-Latin combining marks; it is not transliteration. With removal off, normalize NFC and retain marks within tokens that start with a letter or number. Unicode mode retains Unicode letters/numbers and subsequent marks. ASCII mode retains a–z and 0–9 only; non-ASCII runs become separators, not approximate spellings. Characters such as ß and ø are not transliterated. Punctuation, apostrophes, hyphens, whitespace, emoji and symbols separate tokens. Join tokens with one hyphen; no doubled, leading or trailing hyphens. Empty or symbol-only input produces an empty slug with zero segments. Accent preservation in ASCII mode can split accented words. This is not universal linguistic segmentation or a guarantee of URL availability, uniqueness or reserved-word safety. Use proper URL encoding when inserting Unicode slugs into URLs.

## Interface and safety

Live preview uses a 120 ms debounce and immediate invalidation of obsolete output, counts and actions. Input and option composition events defer computation. Clear restores documented defaults and input focus. Clipboard completion is revision-guarded; denied/unavailable clipboard access selects the current result and gives manual-copy instructions. UTF-8 `.txt` downloads use a fixed filename and release temporary object URLs, including on failure.

100,000 UTF-16 input units; no silent maxlength truncation. Unicode/emoji are not counted as visual graphemes. All output uses textarea values/textContent. No input transport or persistence. The external Tailwind Play CDN supplies styling; expanded inline fallback CSS preserves usability when it is blocked. No package installation, application backend or build step is needed to open this standalone page.

## Independent verification

Run `python scripts/test_tool.py --id slug-generator` and `node --test --test-concurrency=1 tests/tools/slug-generator/*.test.mjs` from the checkout. The framework runs explicit exact JSON fixtures and real installed Chromium interaction cases; additional suites cover boundaries, stale operations, composition, no user-input transport/persistence, UTF-8 downloads and error paths. Committed audit evidence records only actually executed results and hashes. Integration tests are run after local homepage preparation.

Browser tests use isolated Edge/Chromium profiles, block external HTTP(S), simulate clipboard success/denial, and capture download Blobs in memory. Composition events are simulated. Mobile checks use viewport emulation at 320 and 375 pixels, plus 768/1440. This is not screen-reader, physical-device, native IME/clipboard/save-dialog or all-browser certification. Limits are bounded host test fixtures, not universal performance guarantees. See the Task 7 plan and audit for final results.

## Historical Task 7 verified local checkpoint

Lifecycle: TESTED / REQUIRED_PASSED; publication null. Source revision `65d47800bc74a9023690d67c2aa7f856b151f918`; normalized HTML SHA-256 `682769f856e500f5db53dc6781eeedfb1486a3bec7f7c35fc4cb7119b0a90ea8`. See [scoped audit](../audit/SLUG_GENERATOR_VERIFICATION.json).

Passed 33 exact framework logic fixtures plus 9 independent Node logic tests; 17 framework browser cases / 42 assertions, 11 extended real browser cases, and 2 actual hub/navigation/search cases (30 browser cases total for this utility). Full project regression: Python 123/123, Node 158/158 sequentially, six released-tool framework browser regressions 56 cases/242 assertions, neutral templates 6 logic/12 browser/48 assertions, project validation zero errors/warnings. All three local hub cards remain publication pending; existing six released tools are unchanged. This checkpoint does not claim deployment or release.

## Verified release

PR #11 merged normally as `d3ddb6de807913c05832e24a77797f033b353497` at 2026-11-01T22:51:53Z. Actual successful [Pages implementation run 41359251674](https://github.com/Juster06/micro-tools-hub/actions/runs/41359251674), independent live browser behavior and exact approved public source hashes passed before each RELEASED transition. Original local audits/source checkpoints remain preserved. Current inventory: 93 total, 9 RELEASED, 0 TESTED, 15 READY, 68 PLANNED, 1 BLOCKED; milestone 9/25 (36%).

This utility independently passed 28 actual public browser cases/checkpoints. Complete public HTML/inline JavaScript/CSS matches its approved hash. Copy APIs were simulated and UTF-8 download Blob/content/bytes/revocation inspected in memory. Release metadata deployment and final local regressions/shortcut results are recorded in the latest handoff and release audit; implementation source remains unchanged. No Task 8 work is authorized.
