# Random Name Picker

Canonical route: `random-name-picker/index.html`.

Draw from a local list with an explicit replacement policy.

## Behavior and limits

At most 100,000 UTF-16 input units, 10,000 nonblank names and 256 units per name. CR/LF lines are trimmed and NFC-normalized; blank lines are ignored. Default duplicate removal is exact and case-sensitive after normalization. Keeping duplicates gives those entries additional chances and can produce identical names even without replacement. Draw 1–100 names; without replacement cannot exceed available entries. Each click starts a fresh pool. Unbiased 32-bit rejection sampling and partial Fisher–Yates use only crypto.getRandomValues in a secure context; at most 128 attempts per pick, failure aborts the whole result. No insecure fallback, saved history or server draw. This is not a certification for regulated lotteries.

No input uploads, tracking, saved drafts or external processing. Page/style delivery uses hosting and the existing Tailwind Play CDN; inline fallback styling works without the CDN. Existing homepage Analytics is separate. Clipboard permission may fail: current output is selected with manual-copy guidance. Text export uses a fixed UTF-8 filename and releases object URLs.

## Verification and lifecycle

Implementation and tests are part of Task 10. Only actual source-bound evidence can establish TESTED; publication remains null until a separately approved merge, deployment and independent public verification. See `audit/TASK_10_DEVELOPMENT_PLAN.md` and the per-tool verification audit.
