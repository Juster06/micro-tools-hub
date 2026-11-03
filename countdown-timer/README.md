# Countdown Timer

Canonical route: `countdown-timer/index.html`.

Run a duration timer using an actual deadline rather than interval ticks.

## Behavior and limits

Use exactly HH:MM:SS with minutes/seconds 00–59; maximum 24 hours. Start uses an actual Date.now deadline; displayed seconds round up. Pause preserves fractional milliseconds and Resume creates a new deadline. Delayed background callbacks reconcile on visibility/focus/pageshow, rather than subtracting interval ticks. System-clock changes affect this wall-clock deadline. A suspended/closed browser cannot guarantee an on-time alarm; no sound, notifications, storage or device wake-up. Reset stops the timer and restores five minutes; it does not start automatically. Copy/export captures the displayed remaining time at click.

No input uploads, tracking, saved drafts or external processing. Page/style delivery uses hosting and the existing Tailwind Play CDN; inline fallback styling works without the CDN. Existing homepage Analytics is separate. Clipboard permission may fail: current output is selected with manual-copy guidance. Text export uses a fixed UTF-8 filename and releases object URLs.

## Verification and lifecycle

Implementation and tests are part of Task 10. Only actual source-bound evidence can establish TESTED; publication remains null until a separately approved merge, deployment and independent public verification. See `audit/TASK_10_DEVELOPMENT_PLAN.md` and the per-tool verification audit.
