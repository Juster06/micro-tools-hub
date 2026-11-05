# YouTube Title Checker

Canonical route: `youtube-title-checker/index.html`.

10,000 Unicode code points maximum; CRLF/CR normalize to LF. The editable 100-character guide and 60-character opening preview are planning aids, not ranking predictions or exact YouTube truncation. Copy/download preserve the complete normalized title. <a href="https://developers.google.com/youtube/data/reference/rest/v3/videos" target="_blank" rel="noopener noreferrer">YouTube title reference</a> (reviewed 5 November 2026).

See `audit/TASK_18_DEVELOPMENT_PLAN.md` for acceptance, resource bounds, dependency decisions and testing scope. Inputs stay in the browser; optional shared site analytics requires consent. No public release is claimed. Clipboard/download APIs are simulated in automated Chromium tests; no native-dialog, screen-reader, physical-device or cross-browser certification.
