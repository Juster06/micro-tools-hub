# QR Code Generator

## Task 19.1 public verification

The deployed source from PR #34 / `7ecbe37d15d51e3393c1d0f532fa4f2afd279f0b`
was independently verified over public HTTPS with fresh scoped Chromium behavior.
See `audit/QR_CODE_GENERATOR_RELEASE_VERIFICATION.json` and `audit/TASK_19_PUBLIC_RELEASE_VERIFICATION.json`.
PR #34 and release-verification PR #35 are merged; the tool is RELEASED.
Final deployed main `1ead1c37861b80c552446afbdb952c9248370bf9` passed
Task19.2 public source and fresh smoke checks; see
`audit/TASK_19_FINAL_PUBLIC_STATE.json`. Limits below continue to apply. Clipboard/download were
captured in memory; no cross-browser/native-dialog/device certification.

## Historical Task 19 development notes

Canonical route: `qr-code-generator/index.html`.

Input ≤1,000 UTF-8 bytes; output ≤2,048 pixels per side and ≤4 MiB. Local pinned Nayuki QR encoder v1.8.0 (MIT); no QR service, URL shortener or content upload. UTF-8 encoding is explicit; correction L/M/Q/H is not silently upgraded. Black modules on white with a four-module quiet zone; no logos or styling that damages codes. PNG export only. Scanner support varies; no destination-safety or scan-success guarantee.

See `audit/TASK_19_DEVELOPMENT_PLAN.md` for acceptance, resource bounds, dependency decisions and testing scope. Inputs stay in the browser; optional shared site analytics requires consent. No public release is claimed. Clipboard APIs and downloads where provided are simulated in automated Chromium tests; no native-dialog, screen-reader, physical-device or cross-browser certification.

Status: **TESTED — publication pending**. Source-bound development evidence: `audit/QR_CODE_GENERATOR_VERIFICATION.json`.
