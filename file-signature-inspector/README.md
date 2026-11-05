# File Signature Inspector

Canonical route: `file-signature-inspector/index.html`.

Only the first 4 KiB are read, even for large files. Known signatures: PNG, JPEG, GIF, WebP, PDF, ZIP, gzip, MZ, ELF and WAVE. Truncated/unrecognized headers return Unknown. ZIP-based documents are not distinguished by contents. The first 64 bytes are shown as hex; no contents are decoded or executed. Signatures and extensions are hints, not malware detection or file safety certification.

See `audit/TASK_18_DEVELOPMENT_PLAN.md` for acceptance, resource bounds, dependency decisions and testing scope. Inputs stay in the browser; optional shared site analytics requires consent. No public release is claimed. Clipboard/download APIs are simulated in automated Chromium tests; no native-dialog, screen-reader, physical-device or cross-browser certification.
