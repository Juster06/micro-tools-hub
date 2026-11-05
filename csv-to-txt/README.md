# CSV to TXT

## Task 19.1 public verification

The deployed source from PR #34 / `7ecbe37d15d51e3393c1d0f532fa4f2afd279f0b`
was independently verified over public HTTPS with fresh scoped Chromium behavior.
See `audit/CSV_TO_TXT_RELEASE_VERIFICATION.json` and `audit/TASK_19_PUBLIC_RELEASE_VERIFICATION.json`.
This separate branch proposes RELEASED metadata; its PR must not be merged without
owner authorization. Limits below continue to apply. Clipboard/download were
captured in memory; no cross-browser/native-dialog/device certification.

## Historical Task 19 development notes

Canonical route: `csv-to-txt/index.html`.

CSV input ≤1 MiB UTF-8; ≤10,000 data rows and 100 columns; output ≤2 MiB UTF-8; template ≤4,096 bytes. A leading UTF-8 BOM is removed. Quoted commas/escaped quotes/multiline fields are supported; embedded line endings are preserved. Blank lines are records; malformed quoting/ragged rows and empty/duplicate headers are rejected. Output is plain text, not a spreadsheet export. Positional templates do not execute input or infer types. Preview shows up to 20 records, 500 characters per record; complete output is retained within the cap.

See `audit/TASK_19_DEVELOPMENT_PLAN.md` for acceptance, resource bounds, dependency decisions and testing scope. Inputs stay in the browser; optional shared site analytics requires consent. No public release is claimed. Clipboard APIs and downloads where provided are simulated in automated Chromium tests; no native-dialog, screen-reader, physical-device or cross-browser certification.

Status: **TESTED — publication pending**. Source-bound development evidence: `audit/CSV_TO_TXT_VERIFICATION.json`.

Uploaded quoted line endings are retained until manual editing. Textarea display normalizes line endings; automatic copy and downloads use the full computed result.
