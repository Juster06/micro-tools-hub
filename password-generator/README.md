# Password Generator

## Task 19.1 public verification

The deployed source from PR #34 / `7ecbe37d15d51e3393c1d0f532fa4f2afd279f0b`
was independently verified over public HTTPS with fresh scoped Chromium behavior.
See `audit/PASSWORD_GENERATOR_RELEASE_VERIFICATION.json` and `audit/TASK_19_PUBLIC_RELEASE_VERIFICATION.json`.
This separate branch proposes RELEASED metadata; its PR must not be merged without
owner authorization. Limits below continue to apply. Clipboard/download were
captured in memory; no cross-browser/native-dialog/device certification.

## Historical Task 19 development notes

Canonical route: `password-generator/index.html`.

Length 8–128; quantity 1–20; output including separating line breaks ≤2,560 characters. Selection uses browser cryptographic randomness with rejection sampling, with no fallback. No automatic generation, downloads, saved secrets or logging. Copy is an explicit sensitive-data action; clipboard/extension access and memory erasure are outside this tool’s control. Website password rules vary; no strength or security certification is claimed.

See `audit/TASK_19_DEVELOPMENT_PLAN.md` for acceptance, resource bounds, dependency decisions and testing scope. Inputs stay in the browser; optional shared site analytics requires consent. No public release is claimed. Clipboard APIs and downloads where provided are simulated in automated Chromium tests; no native-dialog, screen-reader, physical-device or cross-browser certification.

Status: **TESTED — publication pending**. Source-bound development evidence: `audit/PASSWORD_GENERATOR_VERIFICATION.json`.
