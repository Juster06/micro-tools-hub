# Number Base Converter

## Task 24.1 public verification — release proposal

PR #43 merged at `a7da719ea6ccc4caae572f26f6ae5e707fbb70be`; Pages42324279460 and all required
post-merge Functional CI42324279630 checks succeeded. Fresh actual public HTTPS
source and 11 scoped interaction cases passed on 2026-11-07. See `audit/NUMBER_BASE_CONVERTER_RELEASE_VERIFICATION.json`
and `audit/TASK_24_PUBLIC_RELEASE_VERIFICATION.json`. This separate proposal
requires owner authorization before merge; production metadata remains TESTED
until the release-verification PR is authorized, merged and deployed. Existing
limits and native/device/GA4 property-reporting limitations below remain.

## Historical Task 24 development

Canonical route: `number-base-converter/index.html`.

TESTED — publication pending. Local source checkpoint `494fada334af7f0e1f548484e02844f3d993c83e`; evidence: `audit/NUMBER_BASE_CONVERTER_VERIFICATION.json`. No live-publication claim.

1–4096 ASCII digits, optional +/− sign; no spaces/prefixes, fractions or scientific notation. Bases 2–36; exact BigInt, normalized lowercase output ≤32768 digits. Original input preserved. Signed zero becomes 0; no two’s-complement mode.

Inputs stay in browser memory: no uploads, input logging, automatic saved drafts or external processing. Hosting and existing Tailwind CDN requests still occur. Shared analytics requires consent and excludes tool inputs. Copy places text on your system clipboard; permission may fail with manual-copy guidance. Text downloads use bounded UTF-8 Blobs and temporary URLs are released.

Native APIs only; no new runtime package. Pure inline logic and actual browser interaction have separate scoped tests.



Clipboard/download automation is simulated/captured; no native OS dialog, physical device, cross-browser or screen-reader certification. Existing PDF deferral, blocked compressor and consent/privacy code are unchanged.

Raw digits must be ASCII before case conversion: compatibility letters such as the Kelvin sign are rejected rather than silently converted to k.
