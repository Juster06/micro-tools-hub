# List Comparison & Set Operations

## Task 24.1 public verification — release proposal

PR #43 merged at `a7da719ea6ccc4caae572f26f6ae5e707fbb70be`; Pages42324279460 and all required
post-merge Functional CI42324279630 checks succeeded. Fresh actual public HTTPS
source and 11 scoped interaction cases passed on 2026-11-07. See `audit/LIST_COMPARISON_SET_OPERATIONS_RELEASE_VERIFICATION.json`
and `audit/TASK_24_PUBLIC_RELEASE_VERIFICATION.json`. This separate proposal
requires owner authorization before merge; production metadata remains TESTED
until the release-verification PR is authorized, merged and deployed. Existing
limits and native/device/GA4 property-reporting limitations below remain.

## Historical Task 24 development

Canonical route: `list-comparison-set-operations/index.html`.

TESTED — publication pending. Local source checkpoint `6437b046e5827d82d2f3dbf7668dc451c51c2614`; evidence: `audit/LIST_COMPARISON_SET_OPERATIONS_VERIFICATION.json`. No live-publication claim.

Each list ≤50000 UTF-16 units/10000 lines, each line ≤2000 units; CRLF/CR normalize to LF. Empty input is an empty list. Default exact case/spacing, no normalization, empty keys omitted. Optional trim→NFC→lowercase affects comparison keys only. Keep the first original spelling/spacing; union/intersection/first-only use first-list order, second-only uses second-list order, symmetric difference appends first-only then second-only. Duplicates within each list count once. A kept empty item is a blank output line. Output ≤100000 units/400KiB UTF-8; no fuzzy or multiset matching.

Inputs stay in browser memory: no uploads, input logging, automatic saved drafts or external processing. Hosting and existing Tailwind CDN requests still occur. Shared analytics requires consent and excludes tool inputs. Copy places text on your system clipboard; permission may fail with manual-copy guidance. Text downloads use bounded UTF-8 Blobs and temporary URLs are released.

Native APIs only; no new runtime package. Pure inline logic and actual browser interaction have separate scoped tests.



Clipboard/download automation is simulated/captured; no native OS dialog, physical device, cross-browser or screen-reader certification. Existing PDF deferral, blocked compressor and consent/privacy code are unchanged.
