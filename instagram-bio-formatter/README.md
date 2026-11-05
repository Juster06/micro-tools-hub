# Instagram Bio Formatter

Canonical route: `instagram-bio-formatter/index.html`.

10,000 Unicode code points maximum. Formatting is explicit; preserve mode retains blank lines and spaces. CRLF/CR normalize to LF. The editable 150-character guide is a planning aid; the mobile preview is approximate and cannot reproduce Instagram rendering. No account access or automatic posting.

See `audit/TASK_18_DEVELOPMENT_PLAN.md` for acceptance, resource bounds, dependency decisions and testing scope. Inputs stay in the browser; optional shared site analytics requires consent. No public release is claimed. Clipboard/download APIs are simulated in automated Chromium tests; no native-dialog, screen-reader, physical-device or cross-browser certification.
