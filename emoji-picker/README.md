# Emoji Picker

Canonical route: `emoji-picker/index.html`.

Unicode Emoji18.0:3,963 fully-qualified sequences, English names and categories; Unicode, Inc., Unicode LicenseV3. <a href="../assets/data/UNICODE-LICENSE.txt">Licence and copyright</a>. Derived local data retains exact sequence/name/group order. Search ≤100 code points;100 results per page; copied sequence ≤32 code points. Tone filters match existing modifiers, including mixed-tone sequences; no fabricated variants. Platform fonts determine appearance and support. No external emoji API, font or image service.

See `audit/TASK_20_DEVELOPMENT_PLAN.md` for acceptance, resource bounds, dependency decisions and testing scope. Inputs stay in the browser; optional shared site analytics requires consent. No public release is claimed. Clipboard/download APIs are simulated in automated Chromium tests; no native-dialog, screen-reader, physical-device or cross-browser certification.

## Current release proposal

Task20.1 independently verified this utility on actual public HTTPS against
deployed main `0b055d5b837ea0bca85f8b6583eec5607f93de95`.
This branch proposes RELEASED; release metadata/Live labels require a separately
authorized PR merge/deployment. Fresh public evidence:
`audit/EMOJI_PICKER_RELEASE_VERIFICATION.json`.
Aggregate evidence,45 fresh public cases, three real204 GA4 page views and
limitations: `audit/TASK_20_PUBLIC_RELEASE_VERIFICATION.json`.
Earlier development evidence is preserved. No production code was changed.
