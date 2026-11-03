# Task 10 — six-tool development plan

## Verified baseline and authorization

Main 37882847910116466cccb1f57f05b93023d343ec (PR 15 merged); clean checkout,
main CI 41560372500 all four jobs SUCCESS. Ruleset 26413762 Active, exact GitHub
Actions aggregate, strict current-main PRs/zero approvals/conversations required,
blocked force pushes/deletion; administrator emergency bypass is not authorized.
93 registered:18 RELEASED,6 READY,68 PLANNED,1 BLOCKED. Existing 18 released pages
and their evidence/registry entries, CNAME, homepage cards/Analytics, dashboard
and shortcuts will be preserved. Owner authorizes this batch, commits, branch
publication and PR, not merge/deployment/release. TESTED is not RELEASED.

The actual count 10 proposal selects exactly the six READY entries at ranks 15–20;
no PLANNED replacement or registry ID is needed. Every generator dry run precedes
its ignored scaffold. Follow the existing inline-logic/manifests/fixtures and
gated canonical promotion/homepage proposal workflow; no template rewrite.

## Selected scope and acceptance contracts

| Tool / route | Reason and behavior | Limits/errors |
| --- | --- | --- |
| Profit Margin Calculator / profit-margin-calculator/ | Cost/revenue → profit, margin and markup with separate formulas; distinct from percentage/discount tools. Live preview, precision 0/2/4/6, copy/download/clear. | Nonnegative complete ASCII decimals,64 units/field, magnitudes0 or1e-12–1e12; results≤1e15. Zero denominator gives explained N/A, not Infinity. IEEE754/toFixed disclosed. |
| Date Difference Calculator / date-difference-calculator/ | Calendar dates, UTC-day subtraction, inclusive/exclusive and signed/absolute; distinct from timestamp conversion. | Strict YYYY-MM-DD years0001–9999, actual Gregorian roundtrip; invalid/empty reject. Inclusive same day=1; reverse signed inclusive=negative(abs(distance)+1). No timezone/DST arithmetic. |
| Countdown Timer / countdown-timer/ | Duration start/pause/resume/reset, deadline-based reconciliation and accessible completion; no Pomodoro/session planner. | HH:MM:SS >0 up to24h, bounded minutes/seconds. Date.now deadline, ceil display, pause preserves fractional remainder. Background delay catches up on visibility/focus/pageshow; closed page cannot alarm; clock changes affect deadline. No audio/notifications/storage. |
| Random Name Picker / random-name-picker/ | User-entered names, trim/blank handling, explicit duplicate/within-batch replacement policies,1–100 draws. Distinct from curated stream roulette. |100000 UTF16 units,10000 names,256 units/name. NFC, exact case-sensitive dedupe default; retain duplicates makes entries separate chances. Each draw starts a fresh pool; without replacement applies within batch. Secure crypto only. |
| Hashtag Organizer / hashtag-organizer/ | Normalize pasted tags, explicit lowercase-comparison/casing policies, dedupe, counts, optional deterministic sorting and space/line grouping; no account API or popularity claim. |100000 units,1000 tokens,100 codepoints/tag. Whitespace/commas delimit; optional single #; Unicode letter/number/underscore first, letters/marks/numbers/underscore thereafter. Invalid tokens fail whole result; no hidden discarded punctuation. NFC; lowercase is not full case folding. |
| Secure Random Number Generator / secure-random-number-generator/ | Inclusive safe-integer bounds and bounded batch, distinct from UUID identifiers. | Signed decimal safe integers ±9007199254740991, min≤max, count 1–1000. BigInt range arithmetic and64-bit crypto rejection sampling, no insecure fallback. |

## Randomness design review before implementation

Only crypto.getRandomValues, feature-detected in a secure context, supplies UI
entropy. Integer sampling takes an unsigned64-bit word assembled from two
Uint32 words. For span n use L=2^64−(2^64 mod n); reject x≥L, then min+x mod n.
Each remainder has exactly floor(2^64/n) accepted representatives. Safe signed
endpoints produce span≤2^54−1, represented exactly using BigInt; never round a
floating-point range. Name indices use the corresponding unsigned32-bit bound
and partial Fisher–Yates for without-replacement batches. Max 128 rejection
attempts per pick; exhausted/failed/unavailable entropy aborts the whole result.
No modulo-only mapping, Math.random fallback, UI seed, stored entropy or claim
of guaranteed uniqueness/security tokens. Duplicate names are distinct entries
only when explicitly retained. Independent deterministic entropy fixtures test
rejection/extremes; real-browser generation/crypto failure tests verify the actual
WebCrypto path. Test entropy injection is confined to the trusted logic adapter,
not a production UI option. No new cryptographic primitive is invented.

## Quality and lifecycle gates

Implement invalidation, IME protection, truthful clipboard denial, fixed-name
UTF8 export and URL cleanup. Test normal/empty/invalid/boundary/Unicode/large
inputs, pure timer transitions (including late tick), real browser actions,
keyboard/layout/privacy, real crypto and failure paths. Canonical source/test
commit precedes source-bound audit evidence and manual TESTED metadata. Preserve
publication=null. Run canonical scopes after evidence edits; review/apply each
gated homepage patch. Extend only the existing CI coverage map/floors to include
all new suites/tools; no weakened assertion, changed existing source or new
infrastructure. Full Python/Node/browser/project regression before PR.

Final expected inventory:93 total,18 RELEASED,6 TESTED,0 READY,68 PLANNED,1 BLOCKED;
milestone remains18/25 (72%). After a separately approved merge/deploy/live
verification these six could bring released to24, not25. Next action is owner
review/integration/public verification, then review PLANNED queue readiness.
