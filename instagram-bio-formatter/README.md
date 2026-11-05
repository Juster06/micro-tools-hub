# Instagram Bio Formatter

## Task 18.1 public verification

The deployed source from PR #32 / `8cb97c3f1450634524a40aa9b7cf016bd6b3c78e`
was independently verified over public HTTPS with fresh scoped Chromium behavior.
See `audit/INSTAGRAM_BIO_FORMATTER_RELEASE_VERIFICATION.json` and `audit/TASK_18_PUBLIC_RELEASE_VERIFICATION.json`.
This separate branch proposes RELEASED metadata; its PR must not be merged without
owner authorization. Limits below continue to apply. Clipboard/download were
captured in memory; no cross-browser/native-dialog/device certification.

## Historical Task 18 development notes

Canonical route: `instagram-bio-formatter/index.html`.

10,000 Unicode code points maximum. Formatting is explicit; preserve mode retains blank lines and spaces. CRLF/CR normalize to LF. The editable 150-character guide is a planning aid; the mobile preview is approximate and cannot reproduce Instagram rendering. No account access or automatic posting.

See `audit/TASK_18_DEVELOPMENT_PLAN.md` for acceptance, resource bounds, dependency decisions and testing scope. Inputs stay in the browser; optional shared site analytics requires consent. No public release is claimed. Clipboard/download APIs are simulated in automated Chromium tests; no native-dialog, screen-reader, physical-device or cross-browser certification.
