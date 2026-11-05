# File Signature Inspector

## Task 18.1 public verification

The deployed source from PR #32 / `8cb97c3f1450634524a40aa9b7cf016bd6b3c78e`
was independently verified over public HTTPS with fresh scoped Chromium behavior.
See `audit/FILE_SIGNATURE_INSPECTOR_RELEASE_VERIFICATION.json` and `audit/TASK_18_PUBLIC_RELEASE_VERIFICATION.json`.
This separate branch proposes RELEASED metadata; its PR must not be merged without
owner authorization. Limits below continue to apply. Clipboard/download were
captured in memory; no cross-browser/native-dialog/device certification.

## Historical Task 18 development notes

Canonical route: `file-signature-inspector/index.html`.

Only the first 4 KiB are read, even for large files. Known signatures: PNG, JPEG, GIF, WebP, PDF, ZIP, gzip, MZ, ELF and WAVE. Truncated/unrecognized headers return Unknown. ZIP-based documents are not distinguished by contents. The first 64 bytes are shown as hex; no contents are decoded or executed. Signatures and extensions are hints, not malware detection or file safety certification.

See `audit/TASK_18_DEVELOPMENT_PLAN.md` for acceptance, resource bounds, dependency decisions and testing scope. Inputs stay in the browser; optional shared site analytics requires consent. No public release is claimed. Clipboard/download APIs are simulated in automated Chromium tests; no native-dialog, screen-reader, physical-device or cross-browser certification.
