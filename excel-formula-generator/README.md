# Excel Formula Generator

Canonical route: `excel-formula-generator/index.html`.

Guided SUM, AVERAGE, COUNT, COUNTA, MIN, MAX, IF and ROUND templates. At most20 arguments and8KiB input; output ≤4KiB. References obey the Excel grid and may include quoted sheet names; no external workbook references. IF takes3 arguments; a condition compares one unqualified cell with a literal. ROUND takes2 arguments and integer precision -308..308. Literal text ≤256 code points. English function names and decimal points only; comma/semicolon chooses argument separators, not automatic locale translation. No AI interpretation, formula execution or calculation claim.

See `audit/TASK_20_DEVELOPMENT_PLAN.md` for acceptance, resource bounds, dependency decisions and testing scope. Inputs stay in the browser; optional shared site analytics requires consent. No public release is claimed. Clipboard/download APIs are simulated in automated Chromium tests; no native-dialog, screen-reader, physical-device or cross-browser certification.

## Current release proposal

Task20.1 independently verified this utility on actual public HTTPS against
deployed main `0b055d5b837ea0bca85f8b6583eec5607f93de95`.
This branch proposes RELEASED; release metadata/Live labels require a separately
authorized PR merge/deployment. Fresh public evidence:
`audit/EXCEL_FORMULA_GENERATOR_RELEASE_VERIFICATION.json`.
Aggregate evidence,45 fresh public cases, three real204 GA4 page views and
limitations: `audit/TASK_20_PUBLIC_RELEASE_VERIFICATION.json`.
Earlier development evidence is preserved. No production code was changed.
