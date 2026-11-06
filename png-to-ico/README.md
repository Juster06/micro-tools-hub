# PNG to ICO

## Current release state

Task20 completed and publicly verified; PR36 and PR37 merged. Main baseline
`8b1c17b86da72c3641477b5fdc5ea3cafb8a1c20`, 68 released tools. Revised Task21
is authorized after PDF deferral; manual checkpoint75, generated milestone100.
Earlier development/release notes below are historical. Existing print-margin,
favicon and unverified GA4 property-reporting limitations remain unchanged.


Canonical route: `png-to-ico/index.html`.

Static PNG ≤5MiB,4096 per side and8 million decoded pixels. Select1–6 sizes:16,32,48,64,128,256; ICO ≤1MiB. Native browser PNG frames are validated as square32-bit RGBA with correct chunk CRCs before packing the reviewed ICO directory. Transparency and aspect ratio preserved with padding; resampling may soften small artwork. Intended for modern PNG-capable ICO readers, not legacy BMP-only compatibility. No upload or external encoder; native encoder/decode deadlines approximately10s.

See `audit/TASK_20_DEVELOPMENT_PLAN.md` for acceptance, resource bounds, dependency decisions and testing scope. Inputs stay in the browser; optional shared site analytics requires consent. No public release is claimed. Clipboard/download APIs are simulated in automated Chromium tests; no native-dialog, screen-reader, physical-device or cross-browser certification.

## Current release proposal

Task20.1 independently verified this utility on actual public HTTPS against
deployed main `0b055d5b837ea0bca85f8b6583eec5607f93de95`.
This branch proposes RELEASED; release metadata/Live labels require a separately
authorized PR merge/deployment. Fresh public evidence:
`audit/PNG_TO_ICO_RELEASE_VERIFICATION.json`.
Aggregate evidence,45 fresh public cases, three real204 GA4 page views and
limitations: `audit/TASK_20_PUBLIC_RELEASE_VERIFICATION.json`.
Earlier development evidence is preserved. No production code was changed.
