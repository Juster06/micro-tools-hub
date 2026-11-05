# Image Compressor

Canonical route: `image-compressor/index.html`.

Static JPEG/PNG/WebP ≤5MiB, ≤4096 per side and8 million decoded pixels; output JPEG/WebP ≤8MiB. Bounded12 quality attempts from the chosen ceiling down to0.05, approximately10s total deadline. Native encoders may not be interruptible immediately. Highest tested quality meeting the target is chosen; otherwise the smallest tested reduction is offered with target-not-met disclosure. If nothing is smaller, the original is retained and no compressed download is offered. No silent resizing, exact target/global optimum guarantee or lossless PNG optimizer. Re-encoding may alter metadata/color handling; compare the preview.

See `audit/TASK_20_DEVELOPMENT_PLAN.md` for acceptance, resource bounds, dependency decisions and testing scope. Inputs stay in the browser; optional shared site analytics requires consent. No public release is claimed. Clipboard/download APIs are simulated in automated Chromium tests; no native-dialog, screen-reader, physical-device or cross-browser certification.

## Current development scope

Implementation and focused tests are present. Publication is unverified; this tool must not be marked RELEASED. Final source-bound development evidence and full regression results will be recorded before delivery.
