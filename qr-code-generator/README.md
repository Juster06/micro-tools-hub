# QR Code Generator

Canonical route: `qr-code-generator/index.html`.

Input ≤1,000 UTF-8 bytes; output ≤2,048 pixels per side and ≤4 MiB. Local pinned Nayuki QR encoder v1.8.0 (MIT); no QR service, URL shortener or content upload. UTF-8 encoding is explicit; correction L/M/Q/H is not silently upgraded. Black modules on white with a four-module quiet zone; no logos or styling that damages codes. PNG export only. Scanner support varies; no destination-safety or scan-success guarantee.

See `audit/TASK_19_DEVELOPMENT_PLAN.md` for acceptance, resource bounds, dependency decisions and testing scope. Inputs stay in the browser; optional shared site analytics requires consent. No public release is claimed. Clipboard/download APIs are simulated in automated Chromium tests; no native-dialog, screen-reader, physical-device or cross-browser certification.
