# CSV to TXT

Canonical route: `csv-to-txt/index.html`.

CSV input ≤1 MiB UTF-8; ≤10,000 data rows and 100 columns; output ≤2 MiB UTF-8; template ≤4,096 bytes. A leading UTF-8 BOM is removed. Quoted commas/escaped quotes/multiline fields are supported; embedded line endings are preserved. Blank lines are records; malformed quoting/ragged rows and empty/duplicate headers are rejected. Output is plain text, not a spreadsheet export. Positional templates do not execute input or infer types. Preview shows up to 20 records, 500 characters per record; complete output is retained within the cap.

See `audit/TASK_19_DEVELOPMENT_PLAN.md` for acceptance, resource bounds, dependency decisions and testing scope. Inputs stay in the browser; optional shared site analytics requires consent. No public release is claimed. Clipboard/download APIs are simulated in automated Chromium tests; no native-dialog, screen-reader, physical-device or cross-browser certification.
