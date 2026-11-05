# Image Cropper

Canonical route: `image-cropper/index.html`.

Static JPEG/PNG/WebP input ≤5 MiB; dimensions ≤4,096 per side and ≤8 million decoded pixels. Headers are bounded before decoding; actual decoded bounds are rechecked. Crop coordinates are whole pixels in decoded orientation; no scaling or silent clipping. PNG export ≤32 MiB preserves alpha where the decoder supports it. Animated images, SVG and unsupported/corrupt input are rejected. Browser color/orientation handling can vary; exported images are re-encoded and metadata preservation/removal is not certified. Local processing only.

See `audit/TASK_19_DEVELOPMENT_PLAN.md` for acceptance, resource bounds, dependency decisions and testing scope. Inputs stay in the browser; optional shared site analytics requires consent. No public release is claimed. Clipboard APIs and downloads where provided are simulated in automated Chromium tests; no native-dialog, screen-reader, physical-device or cross-browser certification.

Status: **TESTED — publication pending**. Source-bound development evidence: `audit/IMAGE_CROPPER_VERIFICATION.json`.
