# PNG to ICO

Canonical route: `png-to-ico/index.html`.

Static PNG ≤5MiB,4096 per side and8 million decoded pixels. Select1–6 sizes:16,32,48,64,128,256; ICO ≤1MiB. Native browser PNG frames are validated as square32-bit RGBA with correct chunk CRCs before packing the reviewed ICO directory. Transparency and aspect ratio preserved with padding; resampling may soften small artwork. Intended for modern PNG-capable ICO readers, not legacy BMP-only compatibility. No upload or external encoder; native encoder/decode deadlines approximately10s.

See `audit/TASK_20_DEVELOPMENT_PLAN.md` for acceptance, resource bounds, dependency decisions and testing scope. Inputs stay in the browser; optional shared site analytics requires consent. No public release is claimed. Clipboard/download APIs are simulated in automated Chromium tests; no native-dialog, screen-reader, physical-device or cross-browser certification.

## Current development scope

TESTED; publication pending. Source-bound evidence: `audit/PNG_TO_ICO_VERIFICATION.json`. Local172 Python/433 Node tests,68 focused source-checkpoint tests,32 consent tests and all68 canonical browser profiles passed. Full local browser partitions timed out at the unchanged900second deadline; interrupted/remaining files passed separately. The complete593-case pinned hosted Chromium partition and other exact-head required GitHub checks must pass. Scope, actual attempts and limitations: `audit/TASK_20_DEVELOPMENT_VERIFICATION.json`. Owner approval is required before merge/deployment; independent public verification is required before RELEASED.
