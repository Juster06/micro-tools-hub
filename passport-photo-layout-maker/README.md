# Passport Photo Layout Maker

Canonical route: `passport-photo-layout-maker/index.html`.

One static JPEG/PNG/WebP ≤5MiB,4096 per side and8 million input pixels. User dimensions10–100mm, margins0–30mm,gaps0–20mm,1–40 tiles; A4/Letter at150/300DPI, ≤10 million sheet pixels and40MiB PNG. At most2 decimal places for millimetres. Raster edges round independently to the nearest pixel (≤0.5pixel per edge); nominal photo widths can differ by1pixel after quantization. Transparent input is composited onto white. Calibration ruler reserves12mm. Print the whole sheet at100%/actual size with fit-to-page disabled; measure the100mm ruler. PNG viewers may assume a different print DPI, so use the fixed-mm print layout or set physical sheet dimensions explicitly. No jurisdiction-specific dimensions, official passport-photo acceptance, biometric/face/pose validation or guaranteed physical printer accuracy.

See `audit/TASK_20_DEVELOPMENT_PLAN.md` for acceptance, resource bounds, dependency decisions and testing scope. Inputs stay in the browser; optional shared site analytics requires consent. No public release is claimed. Clipboard/download APIs are simulated in automated Chromium tests; no native-dialog, screen-reader, physical-device or cross-browser certification.

## Current development scope

Implementation and focused tests are present. Publication is unverified; this tool must not be marked RELEASED. Final source-bound development evidence and full regression results will be recorded before delivery.
