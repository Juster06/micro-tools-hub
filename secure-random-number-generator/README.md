# Secure Random Number Generator

Canonical route: `secure-random-number-generator/index.html`.

Generate unbiased integers within a validated safe-integer interval.

## Behavior and limits

Bounds must be complete signed decimal integer strings, at most 64 UTF-16 units and between −9007199254740991 and 9007199254740991; minimum ≤ maximum. Count is an integer 1–1000. Exact BigInt range arithmetic plus two Uint32 cryptographic words form an unsigned 64-bit sample. Reject values at or above 2^64 − (2^64 mod span) before modulo mapping. At most 128 attempts per output; unavailable/failed/exhausted randomness aborts the entire result with no insecure fallback. A secure context and crypto.getRandomValues are required. Duplicates are allowed; output is not a password/token or guaranteed uniqueness service.

No input uploads, tracking, saved drafts or external processing. Page/style delivery uses hosting and the existing Tailwind Play CDN; inline fallback styling works without the CDN. Existing homepage Analytics is separate. Clipboard permission may fail: current output is selected with manual-copy guidance. Text export uses a fixed UTF-8 filename and releases object URLs.

## Verification and lifecycle

Implementation and tests are part of Task 10. Only actual source-bound evidence can establish TESTED; publication remains null until a separately approved merge, deployment and independent public verification. See `audit/TASK_10_DEVELOPMENT_PLAN.md` and the per-tool verification audit.
