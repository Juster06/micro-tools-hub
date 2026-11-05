# CSV Data Cleaner

## Task 19.1 public verification

The deployed source from PR #34 / `7ecbe37d15d51e3393c1d0f532fa4f2afd279f0b`
was independently verified over public HTTPS with fresh scoped Chromium behavior.
See `audit/CSV_DATA_CLEANER_RELEASE_VERIFICATION.json` and `audit/TASK_19_PUBLIC_RELEASE_VERIFICATION.json`.
PR #34 and release-verification PR #35 are merged; the tool is RELEASED.
Final deployed main `1ead1c37861b80c552446afbdb952c9248370bf9` passed
Task19.2 public source and fresh smoke checks; see
`audit/TASK_19_FINAL_PUBLIC_STATE.json`. Limits below continue to apply. Clipboard/download were
captured in memory; no cross-browser/native-dialog/device certification.

## Historical Task 19 development notes

Canonical route: `csv-data-cleaner/index.html`.

UTF-8 CSV ≤1 MiB, ≤10,000 data rows and 100 columns; export ≤2 MiB. Strict quoting, unique/nonempty headers and rectangular records are required; no type inference or silent repair. Trimming removes JavaScript Unicode whitespace at selected field edges, including line breaks. Only selected data fields are cleaned. Export separately prefixes an apostrophe to formula-risk values (including headers and unselected columns), consistent with the other CSV tools; counts and after-preview disclose this exception. Quote escaping and CRLF record separators may change CSV syntax while preserving unmodified field values. Before/after previews show at most 20 data rows, shorten long fields and are capped together at 20,000 UTF-8 bytes. Full bounded export is retained; preview must be explicitly applied.

See `audit/TASK_19_DEVELOPMENT_PLAN.md` for acceptance, resource bounds, dependency decisions and testing scope. Inputs stay in the browser; optional shared site analytics requires consent. No public release is claimed. Clipboard APIs and downloads where provided are simulated in automated Chromium tests; no native-dialog, screen-reader, physical-device or cross-browser certification.

Status: **TESTED — publication pending**. Source-bound development evidence: `audit/CSV_DATA_CLEANER_VERIFICATION.json`.

Uploaded quoted line endings are retained until manual editing. Textarea display normalizes line endings; automatic copy and downloads use the full computed result.
