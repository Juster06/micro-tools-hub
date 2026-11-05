# CSV ↔ JSON Converter

## Task 18.1 public verification

The deployed source from PR #32 / `8cb97c3f1450634524a40aa9b7cf016bd6b3c78e`
was independently verified over public HTTPS with fresh scoped Chromium behavior.
See `audit/CSV_JSON_CONVERTER_RELEASE_VERIFICATION.json` and `audit/TASK_18_PUBLIC_RELEASE_VERIFICATION.json`.
This separate branch proposes RELEASED metadata; its PR must not be merged without
owner authorization. Limits below continue to apply. Clipboard/download were
captured in memory; no cross-browser/native-dialog/device certification.

## Historical Task 18 development notes

Canonical route: `csv-json-converter/index.html`.

Input ≤2 MiB UTF-8; ≤10,000 data rows, 100 columns, 200,000 total cells, 100,000 UTF-16 units per cell. Output ≤4 MiB UTF-8 and 4,000,000 code units. Preview shows only the first 20 data records; copy/download use the full bounded result. CSV quotes, multiline fields, BOM and comma/tab/semicolon are supported. CRLF/CR normalize to LF. Empty/duplicate headers, ragged records, duplicate JSON keys and nested values are rejected. CSV cells stay strings. JSON object keys are unioned in first-seen JavaScript key order; missing fields/null become empty cells; numbers/booleans become text. JSON numbers use JavaScript double precision; keep large identifiers as strings. These type distinctions do not survive a round trip. Formula-risk CSV cells (including headers) receive an apostrophe, intentionally changing values; protection is not a guarantee for every spreadsheet/import setting. No remote parser or account.

See `audit/TASK_18_DEVELOPMENT_PLAN.md` for acceptance, resource bounds, dependency decisions and testing scope. Inputs stay in the browser; optional shared site analytics requires consent. No public release is claimed. Clipboard/download APIs are simulated in automated Chromium tests; no native-dialog, screen-reader, physical-device or cross-browser certification.
