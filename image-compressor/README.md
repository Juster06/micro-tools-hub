# Image Compressor

Canonical route: `image-compressor/index.html`.

Static JPEG/PNG/WebP ≤5MiB, ≤4096 per side and8 million decoded pixels; output JPEG/WebP ≤8MiB. Bounded12 quality attempts from the chosen ceiling down to0.05, approximately10s total deadline. Native encoders may not be interruptible immediately. Highest tested quality meeting the target is chosen; otherwise the smallest tested reduction is offered with target-not-met disclosure. If nothing is smaller, the original is retained and no compressed download is offered. No silent resizing, exact target/global optimum guarantee or lossless PNG optimizer. Re-encoding may alter metadata/color handling; compare the preview.

See `audit/TASK_20_DEVELOPMENT_PLAN.md` for acceptance, resource bounds, dependency decisions and testing scope. Inputs stay in the browser; optional shared site analytics requires consent. No public release is claimed. Clipboard/download APIs are simulated in automated Chromium tests; no native-dialog, screen-reader, physical-device or cross-browser certification.

## Current development scope

TESTED; publication pending. Source-bound evidence: `audit/IMAGE_COMPRESSOR_VERIFICATION.json`. Local172 Python/433 Node tests,68 focused source-checkpoint tests,32 consent tests and all68 canonical browser profiles passed. Full local browser partitions timed out at the unchanged900second deadline; interrupted/remaining files passed separately. The complete593-case pinned hosted Chromium partition and other exact-head required GitHub checks must pass. Scope, actual attempts and limitations: `audit/TASK_20_DEVELOPMENT_VERIFICATION.json`. Owner approval is required before merge/deployment; independent public verification is required before RELEASED.
