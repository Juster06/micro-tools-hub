# Image Format Converter

## Task 18.1 public verification

The deployed source from PR #32 / `8cb97c3f1450634524a40aa9b7cf016bd6b3c78e`
was independently verified over public HTTPS with fresh scoped Chromium behavior.
See `audit/IMAGE_FORMAT_CONVERTER_RELEASE_VERIFICATION.json` and `audit/TASK_18_PUBLIC_RELEASE_VERIFICATION.json`.
This separate branch proposes RELEASED metadata; its PR must not be merged without
owner authorization. Limits below continue to apply. Clipboard/download were
captured in memory; no cross-browser/native-dialog/device certification.

## Historical Task 18 development notes

Canonical route: `image-format-converter/index.html`.

Static JPEG, PNG and WebP only; animated PNG/WebP, SVG and other formats are rejected. Input ≤5 MiB, dimensions ≤4,096 per side and ≤8 million pixels; header bounds are checked before decoding. Output ≤32 MiB. Available encoders are checked at runtime and actual output MIME must match. PNG/WebP keep transparency; JPEG uses your explicit background. Browser color/orientation/quality handling may vary; conversions are re-encoded and may lose metadata. Images remain local.

See `audit/TASK_18_DEVELOPMENT_PLAN.md` for acceptance, resource bounds, dependency decisions and testing scope. Inputs stay in the browser; optional shared site analytics requires consent. No public release is claimed. Clipboard/download APIs are simulated in automated Chromium tests; no native-dialog, screen-reader, physical-device or cross-browser certification.
