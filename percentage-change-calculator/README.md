# Percentage Change Calculator

Registry ID: `percentage-change-calculator`. Category: calculator. P1 / rank 13. Canonical route: `percentage-change-calculator/index.html`. Task 9 local development; **publication pending**, no release claimed. Current lifecycle/evidence is authoritative in TOOL_REGISTRY.json.

## Exact behavior, defaults and limits

Default: two decimal places. Percentage change = (new − starting) / abs(starting) × 100%. Starting zero always gives an error, including 0→0. Negative bases are supported with an absolute denominator, so an increase in signed value is an Increase and a decrease is a Decrease. Example −100→−50 is +50%, while −100→−150 is −50%. Difference = new − starting. Equal values show No change. Direction uses unrounded values; a tiny real change may display 0 after rounding. This explicit policy differs from a signed-denominator formula. Each numeric field accepts a complete ASCII decimal, optional sign/exponent and trimmed surrounding whitespace; no grouping, currency/percent symbols, hex, NaN or Infinity. Each field is capped at 64 UTF-16 units; magnitudes at most 1e12 and, unless zero, at least 1e-12. Nonfinite or result magnitudes above 1e15 fail clearly. JavaScript IEEE-754 arithmetic applies; rounded output uses native toFixed with 0/2/4/6 decimals (default 2), normalizing displayed negative zero. Values such as 1.005 can expose native binary rounding. Inputs are preserved; no truncation. Output is bounded below 1,000 units and is not arbitrary-precision/accounting software.

## Interface and privacy

Standalone vanilla HTML/JS, existing Tailwind Play CDN and expanded fallback CSS, no build/backend/package dependencies. Native labeled fields, visible focus, keyboard buttons, explicit errors/status, original preservation, immediate obsolete-result/action/count invalidation and Clear/default/focus reset. Deterministic tools debounce live previews by 120 ms and defer composition; UUID generation is manual. Copy completion is revision-guarded; failure selects current output for manual copy. Fixed-name `percentage-change-calculator-output.txt` UTF-8 downloads release temporary URLs on success/failure. No user-input storage/transport/logging or unsafe DOM/evaluation. Hosting/CDN and the preserved owner homepage analytics are distinct from utility input processing.

## Independent verification

`python scripts/test_tool.py --id percentage-change-calculator` runs nonempty actual framework structure/logic/browser scopes. `node --test --test-concurrency=1 tests/tools/percentage-change-calculator/*.test.mjs` runs independent logic/boundary and extended browser/hub tests. Exact fixtures/oracles, all modes/options, empty/invalid/limits, statistics, original preservation, races, copy/UTF-8 Blob/revocation/failure, simulated composition, keyboard/labels and no input transport/storage probes are scoped in the individual audit. Screenshots and actual browser checks use 320/375/768/1440 viewports. Source revisions/hashes are recorded only after real tests and source checkpoint commits.

Clipboard/composition fixtures are simulated; downloads captured in memory. No native clipboard/IME/Save-dialog, physical-device, screen-reader, cross-browser or general cryptographic certification. No publication, push or deployment is authorized by these local tests.
