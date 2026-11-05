# Resume Builder

Canonical route: `resume-builder/index.html`.

Plain-text resume editing:10 sections,50 total items,50KiB UTF-8 draft/input; HTML ≤250KiB. Name ≤200 code points, headline300, contact1000, section title100, each item2000. Each previewed section requires a title and nonempty items. Line endings normalize to LF during editing/import. No autosave, personal-data persistence, cloud account or input transport. Draft import strictly validates version/fields/types/limits and replaces current editing fields. Contact details are literal text, never active links. PDF saving uses the browser print dialog. Fonts/pagination vary; no guaranteed ATS compatibility or hiring outcome.

See `audit/TASK_20_DEVELOPMENT_PLAN.md` for acceptance, resource bounds, dependency decisions and testing scope. Inputs stay in the browser; optional shared site analytics requires consent. No public release is claimed. Clipboard/download APIs are simulated in automated Chromium tests; no native-dialog, screen-reader, physical-device or cross-browser certification.

## Current development scope

Implementation and focused tests are present. Publication is unverified; this tool must not be marked RELEASED. Final source-bound development evidence and full regression results will be recorded before delivery.
