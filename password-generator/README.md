# Password Generator

Canonical route: `password-generator/index.html`.

Length 8–128; quantity 1–20; output including separating line breaks ≤2,560 characters. Selection uses browser cryptographic randomness with rejection sampling, with no fallback. No automatic generation, downloads, saved secrets or logging. Copy is an explicit sensitive-data action; clipboard/extension access and memory erasure are outside this tool’s control. Website password rules vary; no strength or security certification is claimed.

See `audit/TASK_19_DEVELOPMENT_PLAN.md` for acceptance, resource bounds, dependency decisions and testing scope. Inputs stay in the browser; optional shared site analytics requires consent. No public release is claimed. Clipboard APIs and downloads where provided are simulated in automated Chromium tests; no native-dialog, screen-reader, physical-device or cross-browser certification.

Status: **TESTED — publication pending**. Source-bound development evidence: `audit/PASSWORD_GENERATOR_VERIFICATION.json`.
