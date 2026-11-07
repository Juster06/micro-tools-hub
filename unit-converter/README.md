# Unit Converter

Canonical route: `unit-converter/index.html`.

TESTED — publication pending. Local source checkpoint `0457799fc71faae98ecc27c04a4946ac3b4756a2`; evidence: `audit/UNIT_CONVERTER_VERIFICATION.json`. No live-publication claim.

One finite decimal ≤64 UTF-16 units and magnitude ≤1e12. Result finite and magnitude ≤1e18; rounded to 12 significant digits with IEEE-754 arithmetic (not exact decimal metrology). Signed quantities allowed; temperatures below absolute zero rejected. Length/mass/area/volume use documented fixed factors; temperature uses offsets. No bytes, time, money, live rates or medical dosing. Report ≤8KiB.

Inputs stay in browser memory: no uploads, input logging, automatic saved drafts or external processing. Hosting and existing Tailwind CDN requests still occur. Shared analytics requires consent and excludes tool inputs. Copy places text on your system clipboard; permission may fail with manual-copy guidance. Text downloads use bounded UTF-8 Blobs and temporary URLs are released.

Native APIs only; no new runtime package. Pure inline logic and actual browser interaction have separate scoped tests.

- https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b8

Clipboard/download automation is simulated/captured; no native OS dialog, physical device, cross-browser or screen-reader certification. Existing PDF deferral, blocked compressor and consent/privacy code are unchanged.

## Conversion definitions

The result shows the selected factor or temperature formula. Factors below map to the category base; source factor divided by target factor gives the multiplier. Decimal definitions are represented as binary floating-point Numbers.

| Category base | Unit factors |
| --- | --- |
| metre | m 1; cm 0.01; mm 0.001; km 1000; in 0.0254; ft 0.3048; yd 0.9144; mi 1609.344 |
| kilogram | kg 1; g 0.001; mg 0.000001; lb 0.45359237; oz 0.028349523125 |
| square metre | m2 1; cm2 0.0001; km2 1000000; ft2 0.09290304; acre 4046.8564224 |
| litre | L 1; mL 0.001; m3 1000; USgal 3.785411784; Impgal 4.54609 |

Temperature uses K=C+273.15 and K=(F+459.67)×5/9, with inverse relations. Same-unit conversions retain the input Number after validating absolute zero.
