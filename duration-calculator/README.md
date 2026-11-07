# Duration Calculator

Canonical route: `duration-calculator/index.html`.

TESTED — publication pending. Local source checkpoint `6437b046e5827d82d2f3dbf7668dc451c51c2614`; evidence: `audit/DURATION_CALCULATOR_VERIFICATION.json`. No live-publication claim.

Use [+-]HH:MM:SS[.mmm], 1–6 hour digits (0–999999), minutes/seconds 00–59 and 1–3 optional fractional-second digits. At most 100 lines, 64 UTF-16 units per line and 6598 total input units. Blank lines rejected. Exact BigInt milliseconds; normalized output includes three fractional digits, ≥2 hour digits and no negative zero. Output ≤64KiB. Elapsed durations only: no dates/timezones/calendar months or running alarm.

Inputs stay in browser memory: no uploads, input logging, automatic saved drafts or external processing. Hosting and existing Tailwind CDN requests still occur. Shared analytics requires consent and excludes tool inputs. Copy places text on your system clipboard; permission may fail with manual-copy guidance. Text downloads use bounded UTF-8 Blobs and temporary URLs are released.

Native APIs only; no new runtime package. Pure inline logic and actual browser interaction have separate scoped tests.



Clipboard/download automation is simulated/captured; no native OS dialog, physical device, cross-browser or screen-reader certification. Existing PDF deferral, blocked compressor and consent/privacy code are unchanged.
