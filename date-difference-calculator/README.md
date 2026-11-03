# Date Difference Calculator

Canonical route: `date-difference-calculator/index.html`.

Compare two calendar dates without daylight-saving drift.

## Behavior and limits

Strict YYYY-MM-DD, no timestamps/timezones or surrounding text. Both dates must be real Gregorian dates, years 0001–9999. Arithmetic uses UTC day numbers, so daylight-saving changes cannot create fractional days. Exclusive same-day = 0; inclusive same-day = 1. Reverse signed inclusive distance is −(absolute elapsed days + 1). Weeks/remainder use the absolute counted distance; no business-day, holiday or calendar-month model is assumed.

No input uploads, tracking, saved drafts or external processing. Page/style delivery uses hosting and the existing Tailwind Play CDN; inline fallback styling works without the CDN. Existing homepage Analytics is separate. Clipboard permission may fail: current output is selected with manual-copy guidance. Text export uses a fixed UTF-8 filename and releases object URLs.

## Verification and lifecycle

Implementation and tests are part of Task 10. Only actual source-bound evidence can establish TESTED; publication remains null until a separately approved merge, deployment and independent public verification. See `audit/TASK_10_DEVELOPMENT_PLAN.md` and the per-tool verification audit.
