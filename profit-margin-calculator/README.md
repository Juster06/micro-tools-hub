# Profit Margin Calculator

Canonical route: `profit-margin-calculator/index.html`.

Calculate profit, margin and markup with distinct labels.

## Behavior and limits

Profit = revenue − cost. Margin = profit / revenue × 100. Markup = profit / cost × 100. Losses are allowed when revenue is below cost; negative cost/revenue are rejected. Each field accepts a complete ASCII decimal with optional sign/exponent, at most 64 UTF-16 units. Magnitudes are 0 or 1e-12 through 1e12; nonfinite/results above 1e15 fail. Precision is 0/2/4/6 decimals. Native IEEE-754/toFixed arithmetic can show binary rounding and independently rounded amounts; this is currency-neutral arithmetic, not arbitrary-precision accounting. Input is never truncated.

No input uploads, tracking, saved drafts or external processing. Page/style delivery uses hosting and the existing Tailwind Play CDN; inline fallback styling works without the CDN. Existing homepage Analytics is separate. Clipboard permission may fail: current output is selected with manual-copy guidance. Text export uses a fixed UTF-8 filename and releases object URLs.

## Verification and lifecycle

Implementation and tests are part of Task 10. Only actual source-bound evidence can establish TESTED; publication remains null until a separately approved merge, deployment and independent public verification. See `audit/TASK_10_DEVELOPMENT_PLAN.md` and the per-tool verification audit.
