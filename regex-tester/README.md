# Regex Tester

## Task 18.1 public verification

The deployed source from PR #32 / `8cb97c3f1450634524a40aa9b7cf016bd6b3c78e`
was independently verified over public HTTPS with fresh scoped Chromium behavior.
See `audit/REGEX_TESTER_RELEASE_VERIFICATION.json` and `audit/TASK_18_PUBLIC_RELEASE_VERIFICATION.json`.
This separate branch proposes RELEASED metadata; its PR must not be merged without
owner authorization. Limits below continue to apply. Clipboard/download were
captured in memory; no cross-browser/native-dialog/device certification.

## Historical Task 18 development notes

Canonical route: `regex-tester/index.html`.

Pattern ≤500 Unicode code points; text ≤100,000; up to 1,000 displayed matches. All pattern compilation/matching runs in a terminable Web Worker with a 200 ms evaluation deadline after startup (2 s startup limit). Input changes, Cancel and Reset terminate pending work. Timer scheduling can be delayed by browser throttling; no real-time guarantee. Empty matches advance safely; ∅ indicates a zero-length match. Offsets/indices use UTF-16 units. Worker detail text/serialization ≤2,000,000 units and ≤4 MiB UTF-8; unsupported engine flags/patterns return errors. No main-thread fallback. Results are JavaScript-engine behavior, not other regex dialects.

See `audit/TASK_18_DEVELOPMENT_PLAN.md` for acceptance, resource bounds, dependency decisions and testing scope. Inputs stay in the browser; optional shared site analytics requires consent. No public release is claimed. Clipboard/download APIs are simulated in automated Chromium tests; no native-dialog, screen-reader, physical-device or cross-browser certification.
