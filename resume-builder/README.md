# Resume Builder

Canonical route: `resume-builder/index.html`.

Plain-text resume editing:10 sections,50 total items,50KiB UTF-8 draft/input; HTML ≤250KiB. Name ≤200 code points, headline300, contact1000, section title100, each item2000. Each previewed section requires a title and nonempty items. Line endings normalize to LF during editing/import. No autosave, personal-data persistence, cloud account or input transport. Draft import strictly validates version/fields/types/limits and replaces current editing fields. Contact details are literal text, never active links. PDF saving uses the browser print dialog. Fonts/pagination vary; no guaranteed ATS compatibility or hiring outcome.

See `audit/TASK_20_DEVELOPMENT_PLAN.md` for acceptance, resource bounds, dependency decisions and testing scope. Inputs stay in the browser; optional shared site analytics requires consent. No public release is claimed. Clipboard/download APIs are simulated in automated Chromium tests; no native-dialog, screen-reader, physical-device or cross-browser certification.

## Current release proposal

Task20.1 independently verified this utility on actual public HTTPS against
deployed main `0b055d5b837ea0bca85f8b6583eec5607f93de95`.
This branch proposes RELEASED; release metadata/Live labels require a separately
authorized PR merge/deployment. Fresh public evidence:
`audit/RESUME_BUILDER_RELEASE_VERIFICATION.json`.
Aggregate evidence,45 fresh public cases, three real204 GA4 page views and
limitations: `audit/TASK_20_PUBLIC_RELEASE_VERIFICATION.json`.
Earlier development evidence is preserved. No production code was changed.

A4 print/PDF page geometry passed. The static `15 mm` CSS margin declaration is ignored; browser print defaults apply. Exact page margins and physical printer calibration are not claimed.
