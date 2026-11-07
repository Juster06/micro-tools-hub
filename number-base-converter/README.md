# Number Base Converter

Canonical route: `number-base-converter/index.html`.

TESTED — publication pending. Local source checkpoint `494fada334af7f0e1f548484e02844f3d993c83e`; evidence: `audit/NUMBER_BASE_CONVERTER_VERIFICATION.json`. No live-publication claim.

1–4096 ASCII digits, optional +/− sign; no spaces/prefixes, fractions or scientific notation. Bases 2–36; exact BigInt, normalized lowercase output ≤32768 digits. Original input preserved. Signed zero becomes 0; no two’s-complement mode.

Inputs stay in browser memory: no uploads, input logging, automatic saved drafts or external processing. Hosting and existing Tailwind CDN requests still occur. Shared analytics requires consent and excludes tool inputs. Copy places text on your system clipboard; permission may fail with manual-copy guidance. Text downloads use bounded UTF-8 Blobs and temporary URLs are released.

Native APIs only; no new runtime package. Pure inline logic and actual browser interaction have separate scoped tests.



Clipboard/download automation is simulated/captured; no native OS dialog, physical device, cross-browser or screen-reader certification. Existing PDF deferral, blocked compressor and consent/privacy code are unchanged.

Raw digits must be ASCII before case conversion: compatibility letters such as the Kelvin sign are rejected rather than silently converted to k.
