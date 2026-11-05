# PNG to ICO

Canonical route: `png-to-ico/index.html`.

Static PNG ≤5MiB,4096 per side and8 million decoded pixels. Select1–6 sizes:16,32,48,64,128,256; ICO ≤1MiB. Native browser PNG frames are validated as square32-bit RGBA with correct chunk CRCs before packing the reviewed ICO directory. Transparency and aspect ratio preserved with padding; resampling may soften small artwork. Intended for modern PNG-capable ICO readers, not legacy BMP-only compatibility. No upload or external encoder; native encoder/decode deadlines approximately10s.

See `audit/TASK_20_DEVELOPMENT_PLAN.md` for acceptance, resource bounds, dependency decisions and testing scope. Inputs stay in the browser; optional shared site analytics requires consent. No public release is claimed. Clipboard/download APIs are simulated in automated Chromium tests; no native-dialog, screen-reader, physical-device or cross-browser certification.

## Current development scope

Implementation and focused tests are present. Publication is unverified; this tool must not be marked RELEASED. Final source-bound development evidence and full regression results will be recorded before delivery.
