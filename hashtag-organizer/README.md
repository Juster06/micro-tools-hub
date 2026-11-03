# Hashtag Organizer

Canonical route: `hashtag-organizer/index.html`.

Normalize and group hashtag lists without platform account access.

## Behavior and limits

At most 100,000 UTF-16 input units, 1,000 tokens and 100 Unicode code points per tag. NFC normalization; letters/numbers/underscore may start a tag, with combining marks allowed thereafter. Whitespace and commas separate tokens; punctuation/emoji/extra # inside a tag are rejected. Output casing is applied before duplicate comparison. Ignore-case uses Unicode lowercase, not full case folding. Sort is deterministic JavaScript UTF-16 lexical order, not locale-aware collation or popularity. No platform tag-limit/account-access or performance/promotion claim.

No input uploads, tracking, saved drafts or external processing. Page/style delivery uses hosting and the existing Tailwind Play CDN; inline fallback styling works without the CDN. Existing homepage Analytics is separate. Clipboard permission may fail: current output is selected with manual-copy guidance. Text export uses a fixed UTF-8 filename and releases object URLs.

## Verification and lifecycle

Implementation and tests are part of Task 10. Only actual source-bound evidence can establish TESTED; publication remains null until a separately approved merge, deployment and independent public verification. See `audit/TASK_10_DEVELOPMENT_PLAN.md` and the per-tool verification audit.
