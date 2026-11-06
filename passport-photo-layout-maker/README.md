# Passport Photo Layout Maker

## Current release state

Task20 completed and publicly verified; PR36 and PR37 merged. Main baseline
`8b1c17b86da72c3641477b5fdc5ea3cafb8a1c20`, 68 released tools. Revised Task21
is authorized after PDF deferral; manual checkpoint75, generated milestone100.
Earlier development/release notes below are historical. Existing print-margin,
favicon and unverified GA4 property-reporting limitations remain unchanged.


Canonical route: `passport-photo-layout-maker/index.html`.

One static JPEG/PNG/WebP ≤5MiB,4096 per side and8 million input pixels. User dimensions10–100mm, margins0–30mm,gaps0–20mm,1–40 tiles; A4/Letter at150/300DPI, ≤10 million sheet pixels and40MiB PNG. At most2 decimal places for millimetres. Raster edges round independently to the nearest pixel (≤0.5pixel per edge); nominal photo widths can differ by1pixel after quantization. Transparent input is composited onto white. Calibration ruler reserves12mm. Print the whole sheet at100%/actual size with fit-to-page disabled; measure the100mm ruler. PNG viewers may assume a different print DPI, so use the fixed-mm print layout or set physical sheet dimensions explicitly. No jurisdiction-specific dimensions, official passport-photo acceptance, biometric/face/pose validation or guaranteed physical printer accuracy.

See `audit/TASK_20_DEVELOPMENT_PLAN.md` for acceptance, resource bounds, dependency decisions and testing scope. Inputs stay in the browser; optional shared site analytics requires consent. No public release is claimed. Clipboard/download APIs are simulated in automated Chromium tests; no native-dialog, screen-reader, physical-device or cross-browser certification.

## Current release proposal

Task20.1 independently verified this utility on actual public HTTPS against
deployed main `0b055d5b837ea0bca85f8b6583eec5607f93de95`.
This branch proposes RELEASED; release metadata/Live labels require a separately
authorized PR merge/deployment. Fresh public evidence:
`audit/PASSPORT_PHOTO_LAYOUT_MAKER_RELEASE_VERIFICATION.json`.
Aggregate evidence,45 fresh public cases, three real204 GA4 page views and
limitations: `audit/TASK_20_PUBLIC_RELEASE_VERIFICATION.json`.
Earlier development evidence is preserved. No production code was changed.
