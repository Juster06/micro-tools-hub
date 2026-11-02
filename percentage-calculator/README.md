# Percentage Calculator

Registry ID: `percentage-calculator`. Category: calculator. P1 / rank 12. Canonical route: `percentage-calculator/index.html`. Task 9 public release verified 2026-11-02; [Live tool](https://everydaydigitalbox.com/percentage-calculator/). Publication/source/behavior evidence: `audit/PERCENTAGE_CALCULATOR_RELEASE_VERIFICATION.json`; original local implementation audit is preserved.

## Exact behavior, defaults and limits

Default: percentage-of-value, two decimal places. Formula mode of: (percentage / 100) × value. Mode ratio: part / whole × 100%, rejecting a zero whole. Signed percentages and values are supported under the numeric limits; there is no implicit 0–100 restriction. Labels and report formula match the selected operation. No currency, tax or financial assumptions. Each numeric field accepts a complete ASCII decimal, optional sign/exponent and trimmed surrounding whitespace; no grouping, currency/percent symbols, hex, NaN or Infinity. Each field is capped at 64 UTF-16 units; magnitudes at most 1e12 and, unless zero, at least 1e-12. Nonfinite or result magnitudes above 1e15 fail clearly. JavaScript IEEE-754 arithmetic applies; rounded output uses native toFixed with 0/2/4/6 decimals (default 2), normalizing displayed negative zero. Values such as 1.005 can expose native binary rounding. Inputs are preserved; no truncation. Output is bounded below 1,000 units and is not arbitrary-precision/accounting software.

## Interface and privacy

Standalone vanilla HTML/JS, existing Tailwind Play CDN and expanded fallback CSS, no build/backend/package dependencies. Native labeled fields, visible focus, keyboard buttons, explicit errors/status, original preservation, immediate obsolete-result/action/count invalidation and Clear/default/focus reset. Deterministic tools debounce live previews by 120 ms and defer composition; UUID generation is manual. Copy completion is revision-guarded; failure selects current output for manual copy. Fixed-name `percentage-calculator-output.txt` UTF-8 downloads release temporary URLs on success/failure. No user-input storage/transport/logging or unsafe DOM/evaluation. Hosting/CDN and the preserved owner homepage analytics are distinct from utility input processing.

## Independent verification

`python scripts/test_tool.py --id percentage-calculator` runs nonempty actual framework structure/logic/browser scopes. `node --test --test-concurrency=1 tests/tools/percentage-calculator/*.test.mjs` runs independent logic/boundary and extended browser/hub tests. Exact fixtures/oracles, all modes/options, empty/invalid/limits, statistics, original preservation, races, copy/UTF-8 Blob/revocation/failure, simulated composition, keyboard/labels and no input transport/storage probes are scoped in the individual audit. Screenshots and actual browser checks use 320/375/768/1440 viewports. Source revisions/hashes are recorded only after real tests and source checkpoint commits.

Clipboard/composition fixtures are simulated; downloads captured in memory. No native clipboard/IME/Save-dialog, physical-device, screen-reader, cross-browser or general cryptographic certification. These local tests alone do not establish publication; separate successful deployment, exact public source and actual public behavior evidence is recorded in the release audit.
