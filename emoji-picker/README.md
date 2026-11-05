# Emoji Picker

Canonical route: `emoji-picker/index.html`.

Unicode Emoji18.0:3,963 fully-qualified sequences, English names and categories; Unicode, Inc., Unicode LicenseV3. <a href="../assets/data/UNICODE-LICENSE.txt">Licence and copyright</a>. Derived local data retains exact sequence/name/group order. Search ≤100 code points;100 results per page; copied sequence ≤32 code points. Tone filters match existing modifiers, including mixed-tone sequences; no fabricated variants. Platform fonts determine appearance and support. No external emoji API, font or image service.

See `audit/TASK_20_DEVELOPMENT_PLAN.md` for acceptance, resource bounds, dependency decisions and testing scope. Inputs stay in the browser; optional shared site analytics requires consent. No public release is claimed. Clipboard/download APIs are simulated in automated Chromium tests; no native-dialog, screen-reader, physical-device or cross-browser certification.

## Current development scope

TESTED; publication pending. Source-bound evidence: `audit/EMOJI_PICKER_VERIFICATION.json`. Local172 Python/433 Node tests,68 focused source-checkpoint tests,32 consent tests and all68 canonical browser profiles passed. Full local browser partitions timed out at the unchanged900second deadline; interrupted/remaining files passed separately. The complete593-case pinned hosted Chromium partition and other exact-head required GitHub checks must pass. Scope, actual attempts and limitations: `audit/TASK_20_DEVELOPMENT_VERIFICATION.json`. Owner approval is required before merge/deployment; independent public verification is required before RELEASED.
