# Color Contrast Checker

## Task 24.1 public verification — release proposal

PR #43 merged at `a7da719ea6ccc4caae572f26f6ae5e707fbb70be`; Pages42324279460 and all required
post-merge Functional CI42324279630 checks succeeded. Fresh actual public HTTPS
source and 9 scoped interaction cases passed on 2026-11-07. See `audit/COLOR_CONTRAST_CHECKER_RELEASE_VERIFICATION.json`
and `audit/TASK_24_PUBLIC_RELEASE_VERIFICATION.json`. This separate proposal
requires owner authorization before merge; production metadata remains TESTED
until the release-verification PR is authorized, merged and deployed. Existing
limits and native/device/GA4 property-reporting limitations below remain.

## Historical Task 24 development

Canonical route: `color-contrast-checker/index.html`.

TESTED — publication pending. Local source checkpoint `6437b046e5827d82d2f3dbf7668dc451c51c2614`; evidence: `audit/COLOR_CONTRAST_CHECKER_VERIFICATION.json`. No live-publication claim.

Two opaque sRGB colours: #RRGGBB or rgb(R, G, B) with integer 0–255 channels; each field ≤32 UTF-16 units. No alpha, CSS variables or arbitrary CSS. Linearize sRGB at 0.04045, luminance weights 0.2126/0.7152/0.0722; ratio (lighter+0.05)/(darker+0.05). Display four decimals; classify with unrounded ratio. AA normal 4.5:1 / large 3:1; AAA normal 7:1 / large 4.5:1; non-text UI/meaningful graphic contrast 3:1 (SC1.4.11, context/exceptions apply). Large text means ≥18pt regular or ≥14pt bold. A pair result is not whole-page accessibility certification. Report ≤4KiB.

Inputs stay in browser memory: no uploads, input logging, automatic saved drafts or external processing. Hosting and existing Tailwind CDN requests still occur. Shared analytics requires consent and excludes tool inputs. Copy places text on your system clipboard; permission may fail with manual-copy guidance. Text downloads use bounded UTF-8 Blobs and temporary URLs are released.

Native APIs only; no new runtime package. Pure inline logic and actual browser interaction have separate scoped tests.

- https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
- https://www.w3.org/WAI/WCAG22/Understanding/contrast-enhanced.html
- https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html

Clipboard/download automation is simulated/captured; no native OS dialog, physical device, cross-browser or screen-reader certification. Existing PDF deferral, blocked compressor and consent/privacy code are unchanged.
