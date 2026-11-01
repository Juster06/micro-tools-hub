# Text Sorter

Registry ID: `text-sorter`. Canonical route: `text-sorter/index.html`. Category: text. Task 7 local utility; publication is **not verified**. Lifecycle and current source-bound evidence are recorded in TOOL_REGISTRY.json; no release is claimed here.

Put your lines in order, with clear alphabetical and numeric rules.

## Exact behavior and defaults

Alphabetical modes compare UTF-16 keys deterministically; they are not locale collation or natural-number ordering. By default keys use native Unicode lowercase, not full case folding. Case sensitivity and trim() apply only to comparison. Retained lines keep exact spelling and spaces; duplicates remain. Equal keys keep original order in both directions. Numeric modes accept only complete finite ASCII decimal numbers (optional sign, decimal point and exponent); no hex, Infinity, NaN, thousands separators or blank-as-zero. Untrimmed surrounding whitespace is invalid unless Trim comparison keys is selected. Invalid numeric lines stay last in original order in both directions, with a count and warning. JavaScript Number precision applies; equal rounded numeric values remain stable. LF, CRLF and CR separate records. Empty input has zero records; a trailing separator adds a blank record. Output uses LF. Optional blank removal uses trim(), including non-breaking spaces, but not zero-width spaces.

## Interface and safety

Live preview uses a 120 ms debounce and immediate invalidation of obsolete output, counts and actions. Input and option composition events defer computation. Clear restores documented defaults and input focus. Clipboard completion is revision-guarded; denied/unavailable clipboard access selects the current result and gives manual-copy instructions. UTF-8 `.txt` downloads use a fixed filename and release temporary object URLs, including on failure.

100,000 UTF-16 input units; no silent maxlength truncation. Unicode/emoji are not counted as visual graphemes. All output uses textarea values/textContent. No input transport or persistence. The external Tailwind Play CDN supplies styling; expanded inline fallback CSS preserves usability when it is blocked. No package installation, application backend or build step is needed to open this standalone page.

## Independent verification

Run `python scripts/test_tool.py --id text-sorter` and `node --test --test-concurrency=1 tests/tools/text-sorter/*.test.mjs` from the checkout. The framework runs explicit exact JSON fixtures and real installed Chromium interaction cases; additional suites cover boundaries, stale operations, composition, no user-input transport/persistence, UTF-8 downloads and error paths. Committed audit evidence records only actually executed results and hashes. Integration tests are run after local homepage preparation.

Browser tests use isolated Edge/Chromium profiles, block external HTTP(S), simulate clipboard success/denial, and capture download Blobs in memory. Composition events are simulated. Mobile checks use viewport emulation at 320 and 375 pixels, plus 768/1440. This is not screen-reader, physical-device, native IME/clipboard/save-dialog or all-browser certification. Limits are bounded host test fixtures, not universal performance guarantees. See the Task 7 plan and audit for final results.

## Task 7 verified local checkpoint

Lifecycle: TESTED / REQUIRED_PASSED; publication null. Source revision `d83e9afdd2f80c456fe9d4a534c45053dfc77b1c`; normalized HTML SHA-256 `018f431ad20d178eb16b1b1d4782f6a31ca47f5b0ea2986c4d859c3d5529b3cf`. See [scoped audit](../audit/TEXT_SORTER_VERIFICATION.json).

Passed 34 exact framework logic fixtures plus 9 independent Node logic tests; 20 framework browser cases / 47 assertions, 11 extended real browser cases, and 2 actual hub/navigation/search cases (33 browser cases total for this utility). Full project regression: Python 123/123, Node 158/158 sequentially, six released-tool framework browser regressions 56 cases/242 assertions, neutral templates 6 logic/12 browser/48 assertions, project validation zero errors/warnings. All three local hub cards remain publication pending; existing six released tools are unchanged. This checkpoint does not claim deployment or release.
