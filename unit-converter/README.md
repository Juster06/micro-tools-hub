# Unit Converter

Canonical route: `unit-converter/index.html`.

Task 24 development; publication unverified.

One finite decimal ≤64 UTF-16 units and magnitude ≤1e12. Result finite and magnitude ≤1e18; rounded to 12 significant digits with IEEE-754 arithmetic (not exact decimal metrology). Signed quantities allowed; temperatures below absolute zero rejected. Length/mass/area/volume use documented fixed factors; temperature uses offsets. No bytes, time, money, live rates or medical dosing. Report ≤8KiB.

Inputs stay in browser memory: no uploads, input logging, automatic saved drafts or external processing. Hosting and existing Tailwind CDN requests still occur. Shared analytics requires consent and excludes tool inputs. Copy places text on your system clipboard; permission may fail with manual-copy guidance. Text downloads use bounded UTF-8 Blobs and temporary URLs are released.

Native APIs only; no new runtime package. Pure inline logic and actual browser interaction have separate scoped tests.

- https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b8

Clipboard/download automation is simulated/captured; no native OS dialog, physical device, cross-browser or screen-reader certification. Existing PDF deferral, blocked compressor and consent/privacy code are unchanged.
