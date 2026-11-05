# Passport Photo Layout Maker

Canonical route: `passport-photo-layout-maker/index.html`.

One static JPEG/PNG/WebP ≤5MiB,4096 per side and8 million input pixels. User dimensions10–100mm, margins0–30mm,gaps0–20mm,1–40 tiles; A4/Letter at150/300DPI, ≤10 million sheet pixels and40MiB PNG. At most2 decimal places for millimetres. Raster edges round independently to the nearest pixel (≤0.5pixel per edge); nominal photo widths can differ by1pixel after quantization. Transparent input is composited onto white. Calibration ruler reserves12mm. Print the whole sheet at100%/actual size with fit-to-page disabled; measure the100mm ruler. PNG viewers may assume a different print DPI, so use the fixed-mm print layout or set physical sheet dimensions explicitly. No jurisdiction-specific dimensions, official passport-photo acceptance, biometric/face/pose validation or guaranteed physical printer accuracy.

See `audit/TASK_20_DEVELOPMENT_PLAN.md` for acceptance, resource bounds, dependency decisions and testing scope. Inputs stay in the browser; optional shared site analytics requires consent. No public release is claimed. Clipboard/download APIs are simulated in automated Chromium tests; no native-dialog, screen-reader, physical-device or cross-browser certification.

## Current development scope

TESTED; publication pending. Source-bound evidence: `audit/PASSPORT_PHOTO_LAYOUT_MAKER_VERIFICATION.json`. Local172 Python/433 Node tests,68 focused source-checkpoint tests,32 consent tests and all68 canonical browser profiles passed. Full local browser partitions timed out at the unchanged900second deadline; interrupted/remaining files passed separately. The complete593-case pinned hosted Chromium partition and other exact-head required GitHub checks must pass. Scope, actual attempts and limitations: `audit/TASK_20_DEVELOPMENT_VERIFICATION.json`. Owner approval is required before merge/deployment; independent public verification is required before RELEASED.
