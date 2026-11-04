# Changelog

## Task 14.1 — six-tool public verification, release PR pending

PR #24 merged as `130a18045022dfaadec330d13f89b8316c5ccf74`. The [Pages deployment 41759841983](https://github.com/Juster06/micro-tools-hub/actions/runs/41759841983) and [post-merge functional CI 41759840731](https://github.com/Juster06/micro-tools-hub/actions/runs/41759840731) succeeded for that commit. Public HTTPS checks matched the merged homepage and all 43 tool pages byte for byte; all 43 canonical links, custom domain and Analytics identifier were confirmed. The previous 37 pages were checked by public HTTP/source identity and post-merge CI, without new individual public interaction tests.

The six Task 14 utilities passed 20 focused public Chromium interaction tests and additional public edge-case checks. Clipboard, download and storage failure cases were simulated; only synthetic task data was used. Separate release audits record timestamps, exact raw and framework-normalized hashes, results and limitations. Image tools accept static PNG only. Posting Calendar records wall-time and timezone labels without resolving DST; compound-interest results are estimates with explicit per-period rounding. No cross-browser, physical-device, screen-reader or native-dialog certification is claimed.

This release-verification branch proposes 93 registered, 43 RELEASED, 0 TESTED, 0 READY, 49 PLANNED and 1 BLOCKED; milestone 43/50 (86%). Main and public release metadata remain at 37 RELEASED until this PR receives separate owner approval, merges and deploys. Do not bypass branch protection. The historical administrator-bypass question concerning PR #21 remains unverified because audit information was unavailable.

## Historical Task 14 — six tested tools before release verification

The Task 14 branch implements Image Color Picker, CSV Viewer, Image Watermark, Local To-Do List, Posting Calendar Generator and Compound Interest Calculator as **TESTED**, with publication pending. Their gated homepage cards say Tested · publication pending. Branch inventory: 93 registered, 37 RELEASED, 6 TESTED, 0 READY, 49 PLANNED and 1 BLOCKED; the live released milestone remains 37/50 (74%).

See `audit/TASK_14_DEVELOPMENT_PLAN.md` and the source-bound per-tool audits for scope and validation. Image tools accept static PNG only (5 MiB, 4096 per dimension, 8 million pixels). CSV Viewer uses a bounded local state-machine parser with no third-party parser dependency; cells are text. To-do persistence is opt-in. Posting Calendar records wall-clock dates, times and a supported IANA timezone label without resolving DST or converting to UTC. Compound interest uses end-of-period contributions and per-period half-up cent rounding; results are estimates. User input stays in the browser; hosting and the existing styling CDN are separate requests.

The feature branch requires ordinary protected-main review and CI. Do not merge or deploy without separate owner authorization; after authorized integration, independent public verification is needed before a separate release update. Historical administrator-bypass use for PR #21 was not independently verifiable because audit information was unavailable.

## Task 14 — development checkpoint

PR #22 merged as `bc749fecdd7e801d4ab75505d71f469918f4eba4` and PR #23 merged as `54f2db946a1cd947733b3ee77039cf9aba7d5fa3`. Pages run 41752171931 and post-merge Functional CI run 41752172545 succeeded for the latter commit. All 37 public tool sources and homepage matched main, canonical links and registry counts were verified, and the six Task 13 tools passed fresh public smoke tests. Task 13 is complete; the next milestone is 37/50 released, with 13 remaining. Task 14 development is authorized on a feature branch. Historical administrator-bypass use for PR #21 was not independently verified because audit information was unavailable.

## Historical Task 13.1 — public verification before release metadata merge

PR #22 merged as `bc749fecdd7e801d4ab75505d71f469918f4eba4`. The [Pages deployment 41748440143](https://github.com/Juster06/micro-tools-hub/actions/runs/41748440143) and [post-merge functional CI 41748440628](https://github.com/Juster06/micro-tools-hub/actions/runs/41748440628) succeeded for that commit. Public HTTPS checks matched the merged homepage and all 37 tool pages byte for byte; all 37 canonical links, custom domain and Analytics identifier were confirmed. The previous 31 pages were checked by public HTTP/source identity and post-merge CI, without new individual public interaction tests.

The six Task 13 utilities passed 15 focused public Chromium interaction tests and additional public edge-case checks. Clipboard, download and print invocation were simulated; the JSON output-cap error was exercised using a simulated oversized serializer result. Separate release audits record timestamps, exact raw and framework-normalized hashes, results and limitations. Image Resizer accepts static PNG only. No cross-browser, physical-device, screen-reader or native-dialog certification is claimed.

This release-verification branch proposes 93 registered, 37 RELEASED, 0 TESTED, 0 READY, 55 PLANNED and 1 BLOCKED; milestone 37/50 (74%). Main and public release metadata remain at 31 RELEASED until this PR receives separate owner approval, merges and deploys. Do not bypass branch protection. The historical administrator-bypass question concerning PR #21 remains unverified because audit information was unavailable.

## Historical Task 13 — six tested tools before release verification

The Task 13 branch implements Printable Calendar Generator, Username Generator, YouTube Description Formatter, JSON to TXT, Image Resizer and Text Difference Checker as **TESTED**, with publication pending. Their gated homepage cards say Tested · publication pending. Branch inventory: 93 registered, 31 RELEASED, 6 TESTED, 0 READY, 55 PLANNED and 1 BLOCKED; the live released milestone remains 31/50 (62%).

See `audit/TASK_13_DEVELOPMENT_PLAN.md` and the source-bound per-tool audits for limits and validation scope. The resizer supports static PNG only (5 MiB, 4096 per dimension, 8 million pixels). JSON extraction accepts the documented bounded safe path syntax. The diff checker limits input and comparison work. The username tool does not check availability or generate secure passwords. All tool data stays in the browser; hosting and the existing styling CDN are separate requests.

The feature branch requires ordinary protected-main review and CI. Do not merge or deploy without separate owner authorization; after any authorized integration, independent public verification is needed before a separate release update. Historical administrator-bypass use for PR #21 was not independently verifiable because audit information was unavailable.

## Task 12.1 — six-tool public verification, release PR pending

PR #20 merged as `5340f1e006bc07f8913f875505e8ee3b20a4aacc`. The [Pages deployment 41727865909](https://github.com/Juster06/micro-tools-hub/actions/runs/41727865909) and [post-merge functional CI 41727866241](https://github.com/Juster06/micro-tools-hub/actions/runs/41727866241) succeeded for that commit. Public HTTPS checks matched the merged homepage and all 31 tool page sources; all 31 canonical links, the custom domain and Analytics identifier were confirmed. The previous 25 pages were checked through public HTTP/source identity and post-merge CI, without new individual public interaction tests.

The six Task 12 utilities passed 26 public Chromium interaction tests plus additional public checks for age, rounding, calendar boundaries, empty input, title, JavaScript and dependencies. Clipboard, download and printing were simulated. Separate release audits record timestamps, normalized hashes, results and limitations. Image Rotator accepts static PNG only; SHA-256 needs a secure context and Web Crypto. No cross-browser, physical-device or native-dialog certification is claimed.

This release-verification branch proposes 93 registered, 31 RELEASED, 0 TESTED, 0 READY, 61 PLANNED, 1 BLOCKED; milestone 31/50 (62%). Main and public release metadata remain at 25 RELEASED until this PR receives separate owner approval, merges and deploys. Do not bypass branch protection.

## Historical Task 12 — six tested utilities before release verification

Local validation passed: Python project suite **142/142**, Node regression **254/254** plus **1,030** inline logic fixtures, and Chromium interaction suite **312/312** plus **395** browser fixtures / **1,154** assertions (including neutral templates). Project status reported zero errors and warnings. Clipboard/download are simulated in the harness; no public deployment or publication is claimed.

The Task 12 branch implements six utilities as **TESTED**, with publication evidence pending: Age Calculator (`age-calculator/index.html`), VAT Calculator (`vat-calculator/index.html`), Working Days Calculator (`working-days-calculator/index.html`), Meeting Agenda Generator (`meeting-agenda-generator/index.html`), Image Rotator (`image-rotator/index.html`) and SHA-256 Text & File Hash Checker (`sha-256-hash-checker/index.html`; registry ID `sha256-hash-checker`). The homepage cards explicitly state “Tested · publication pending”. No new utility is RELEASED.

Branch inventory: 93 registered, 25 RELEASED, 6 TESTED, 0 READY, 61 PLANNED, 1 BLOCKED. The first milestone is complete; the next target is 50 released tools. See `audit/TASK_12_DEVELOPMENT_PLAN.md` and the six source-bound verification records for limits, local test scope and outstanding publication evidence. Image Rotator accepts static PNG only (up to 5 MiB and 8 million pixels); SHA-256 requires a secure context with Web Crypto and limits files to 16 MiB. User-provided inputs stay local; hosting and the existing styling CDN remain network requests.

The branch targets `main` for ordinary protected-branch review. Do not merge or deploy without separate owner authorization. After an authorized merge and successful deployment, independently verify the public pages and only then prepare a separate release-evidence update for eligible tools.

## Historical Task 11.1 — publication verification before release metadata merge

PR #18 merged as `c97c2d0b2a6d7377df3915b9fcebb0bc758f63ad`. The [Pages deployment 41577979484](https://github.com/Juster06/micro-tools-hub/actions/runs/41577979484) and [post-merge CI 41577980047](https://github.com/Juster06/micro-tools-hub/actions/runs/41577980047) succeeded on that commit. Independent public HTTPS source verification matched all 25 pages and the homepage to the merged source; all 25 homepage routes were verified, and owner Analytics and custom domain remained available. The original 24 utilities were checked by source identity and post-merge CI; no new individual live interactions for those tools are claimed.

The File Size Converter passed 33 actual public Chromium checks covering SI, IEC, cross-system conversions, input limits, rounding, selectors, reset, keyboard, responsive widths and uncaught/console errors. Clipboard was simulated. The separate source-bound release audit records timestamps, hashes, deployment, scope and limitations.

This release-verification branch proposes 93 registered, 25 RELEASED, 0 TESTED, 0 READY, 67 PLANNED, 1 BLOCKED: milestone 25/25 (100%). Main and the public registry remain at 24 RELEASED until this metadata PR is separately authorized, merged and deployed. No administrator bypass or deployment is authorized by this preparation.

## Historical Task 11 — File Size Converter before publication

File Size Converter is implemented and **TESTED** on `feat/file-size-converter`; the canonical route is `file-size-converter/index.html`. The branch homepage card reads **Tested · publication pending**. Its bounded BigInt rational arithmetic distinguishes SI powers of 1000 from IEC powers of 1024, handles plain nonnegative decimals, marks rounding and reports positive values below its display threshold without silently returning zero. No external processing or API is used.

Branch inventory: 93 registered, 24 RELEASED, 1 TESTED, 0 READY, 67 PLANNED, 1 BLOCKED. The release milestone remains 24/25 (96%). Main and the live site remain at 24 RELEASED until separate authorized integration, successful deployment and independent public verification. See `audit/FILE_SIZE_CONVERTER_VERIFICATION.json` for local source-bound scope and limits.

## Historical Task 10.1 — publication verification before merge (2026-11-03)

PR #16 merged as `f7a7553e7fb085302c6f2e24f927a031e234c6e0`. GitHub Pages run [41572786907](https://github.com/Juster06/micro-tools-hub/actions/runs/41572786907) and post-merge functional CI run [41572787293](https://github.com/Juster06/micro-tools-hub/actions/runs/41572787293) succeeded on that commit. Independent HTTPS checks matched the homepage and all 24 tool pages to the approved source; the custom domain and owner Analytics were preserved. The public homepage displayed 24 cards and all six tested links.

Actual public Chromium interactions passed for Profit Margin Calculator, Date Difference Calculator, Countdown Timer, Random Name Picker, Hashtag Organizer and Secure Random Number Generator: normal, empty, invalid, selected edge input, primary action, reset, simulated clipboard and uncaught-error checks; timer pause/resume also passed. Separate per-tool release audits preserve exact timestamps, source hashes, deployment commit and limitations. The existing 18 tools were checked for HTTP/source identity and by post-merge automated CI; no new public browser interactions for those 18 are claimed.

This release-verification branch proposes 93 registered, 24 RELEASED, 0 TESTED, 0 READY, 68 PLANNED and 1 BLOCKED; milestone 24/25 (96%). The public registry and card labels remain at the previous state until this metadata PR is separately reviewed, merged and deployed. This PR requires ordinary protected-main review and CI, with no administrator bypass. Do not merge without owner approval.

## Task 10 — six additional utilities, publication pending (2026-11-03)

- Added Profit Margin Calculator, Date Difference Calculator, Countdown Timer, Random Name Picker, Hashtag Organizer and Secure Random Number Generator as standalone browser-local utilities with validation, copy/export/reset and accessible responsive controls.
- Added source-bound verification, manifests, explicit fixtures, independent Node/browser and hub navigation/search regression checks. Reviewed cryptographic rejection sampling before implementation; no insecure fallback.
- Qualified each canonical tool and reviewed/applied its existing gated homepage patch. Six TESTED entries retain null publication; released count stays 18.
- Extended the existing CI coverage map and raised test floors to actual counts. Fixed two legacy management tests to construct a READY fixture after the real READY queue was exhausted; retained all assertions and production logic.
- Preserved all 18 released tools, CNAME, owner homepage Analytics, dashboard and existing shortcuts.

Local CI partitions passed: Python **142/142**, Node **225/225** plus **791**
inline logic fixtures, real Chromium **268/268** plus **338** browser fixtures /
**987** assertions. Both neutral templates passed (6 logic / 12 browser / 48
assertions). No mandatory failure, skip, cancellation or timeout in the final
run. Registry, source/evidence, all 24 structural profiles and full project status
passed with **zero errors and warnings**. Four legacy isolated-logic adapters
remain explicitly unavailable; their structural/browser checks still run.

No merge, deployment, release, settings change or administrator bypass. Await owner PR review.

## Task 9.5 — final active-ruleset documentation and handoff

- Corrected the superseded unprotected/classic-rule proposal to verified Active
  repository ruleset 26413762, Main Branch Protection - Required Functional CI.
  Recorded actual main targets, PR/zero-approval/conversation requirements,
  Required functional checks from GitHub Actions App15368, strict policy, force-push/
  deletion restrictions and administrator Always allow emergency bypass.
- Preserved historical pre-activation evidence. Documented ordinary Codex and
  release-metadata PR workflows, recovery, emergency limits and the durable PR 15
  final continuation record for exact merge/main CI/public verification results.
- Preserved the Pages direct-configuration-readback limitation; workflow/public
  observations do not certify every saved setting or establish deployment gating.
- Final corrections are submitted through PR 15 with current passing checks and
  normal expected-head merge; no admin bypass, setting/test/utility/registry/
  lifecycle/dashboard/shortcut changes. Task 10 is next, not started.

## Historical Task 9.5 Stage D — proposal before owner activation

- Verified expected main, successful four-job main CI and independent Pages.
  Actual aggregate context/source is Required functional checks / GitHub Actions.
- Actual main remains unprotected with no rulesets/active rules. Connected
  account is admin, but available tools have no administration endpoint and
  no authenticated local GitHub CLI is available; no scope denial is invented.
- Documented the exact classic main-only PR/strict-check/conversation policy,
  zero mandatory approvals, retained admin emergency bypass, disabled force
  pushes/deletion, owner setup/readback, future PR/release-metadata and recovery.
- Documentation uses a feature PR. No settings/permission/deployment/workflow,
  utility/registry/lifecycle/dashboard/shortcut change or Task 10. Enforcement
  remains NOT VERIFIED until owner applies and reads back actual settings.

## Task 9.5 Stage C — functional CI integrated and verified on main

- Merged PR #14 normally at the reviewed head as
  `3f08b910a70f105b91d26e6df8eca7c0477d504d`; merge tree matches the reviewed
  `fa114410eeaa83268110e2479ef72facb3624115`. Safely fast-forwarded local main;
  original local feature branch/history and active checkout preserved.
- Genuine push run 41543825503 passed all four jobs on that merge, independently
  of successful PR run 41535344652. Actual counts: Python 142, Node 179+196,
  JSON logic 639, browser fixtures 291/777, templates 6/12/48. Mandatory failures,
  skips, cancellations and timeouts: zero. All three actual artifacts were
  downloaded and verified against logs, exact coverage, digests/privacy/retention.
- Existing Pages automatically deployed the merge in successful run 41543825473;
  actual main/root build and public source/registry/Analytics preservation checked.
  Deployment remains independent of functional CI; no deployment setting changed.
- Read-only main inspection: unprotected, checks off, no rulesets/active rules.
  Connected account has admin rights; enforcement options/limits are documented,
  without modifying protection, permissions or settings. All public utility,
  registry/lifecycle, dashboard/launcher and shortcut content remains unchanged.
- Final documentation checkpoint's own main CI/Pages and exact identity are
  verified in the delivery report. No Task 10 or new utility development.

## Task 9.5 Stage B — GitHub functional CI verified; PR #14 open

- Genuine pull_request run 41425207614 for published correction 858fc772833a2456931cd80a3ac2eeaf397fd979
  passed Windows Python 142/142, Ubuntu Node 179/179 +639 logic fixtures, actual
  Chromium 196/196 +291 browser cases/777 assertions, templates 6/12/48 and aggregate.
- Initial run 41423878108 correctly failed six Windows 8.3/long TEMP path
  comparisons and the aggregate; preserve failure evidence. CI-only canonical
  temporary-root bootstrap plus one regression guard fixed it, no weakened tests.
- Independently fetched complete 224-file trees match local checkpoints; original
  commits retained. Actual artifacts/digests/coverage/counts/privacy/seven-day
  retention verified against logs. Current PR scope remains 19 files.
- This documentation-only checkpoint records completed verification; final current
  commit/tree/hosted-run identity is in the delivery report. No production source,
  registry/homepage/Analytics/domain/dashboard/shortcut changes, merge, deployment,
  protection/settings/lifecycle changes or Task 10.

## Task 9.5 Stage B — hosted Windows fixture compatibility

- Opened PR #14 against main with exact approved 19-file content; original local
  commit preserved, independent fetched tree equality verified.
- Genuine hosted run 41423878108 exposed six Windows short/long temporary-root
  path comparisons (135/141 Python pass, zero skips). Failure evidence retained.
- Canonicalize only the CI unittest temporary root before fixture discovery;
  add one regression guard and raise the reviewed floor to 142 Python tests.
  Existing tests/assertions and production/dashboard/launcher code stay unchanged.
- Full local and subsequent hosted verification remain required. No merge,
  deployment, settings/protection/lifecycle changes or Task 10.

## Local only — Task 9.5 functional CI and quality gates (2026-11-02)

- Added SHA-pinned read-only PR-to-main/main-push/manual workflow, three genuine
  test partitions and aggregate failure gate. Runtime pins: Python 3.14.4,
  Node 24.22.1, Playwright 1.64.1 / Chromium 156.0.8078.4 revision 1248.
- Added explicit coverage map, strict nonempty/count/skip/layer/timeout checks,
  safe diagnostic summaries, locked development-only browser acquisition,
  platform classification and maintenance/deployment documentation.
- Local Python 141/141 (123 existing + 18 CI guards), Node 179 logic + 196 browser
  = 375/375, fourteen JSON logic profiles (639 cases), eighteen browser profiles
  (291 cases /777 assertions) and templates (6 logic /12 browser /48 assertions)
  passed. Complete browser partitions passed separately in Windows Edge and the
  pinned Windows Chromium; no Linux/hosted pass is inferred.
- Forty-three controlled baseline/failure/restoration invocations passed their
  expected outcomes, including 24 deliberately nonzero controls. Initial pinned
  Windows browser preflight failure was retained and fixed by read/execute ACLs
  only on its disposable public binary cache; no sandbox, assertion or timeout
  weakening. actionlint 1.7.12 passed.
- Production HTML/registry/homepage/Analytics/CNAME, previous tests/evidence,
  framework/templates/dashboard/launcher and shortcut properties remain unchanged.
  No push, PR, merge, deployment, protection/settings changes or Task 10.

## Released — Task 9 five utilities (2026-11-02)

PR #13 merged normally as `44620a1f4a5d6ae58366cb392926961d0b8edf7c` at 2026-11-02T07:29:53Z. Actual successful [Pages run 41406674180](https://github.com/Juster06/micro-tools-hub/actions/runs/41406674180) and independent public browser/whole-source checks qualified each released tool. Inventory: 93 total, 18 RELEASED, 0 TESTED, 6 READY, 68 PLANNED, 1 BLOCKED; milestone 18/25 (72%).

- Independently gated UUID, Timestamp, Percentage, Percentage Change and Discount releases; separate release audits preserve original source/test checkpoints and implementation audits.
- Utility HTML implementations unchanged; only qualified availability labels change through existing integration proposals. Owner Analytics and 13 previous source/card/entry/evidence sets preserved.
- Thirteen integration headers now include independently released Task 9 entries in global inventory totals, while preserving strict TESTED/RELEASED publication, route, search and navigation assertions. No behavior assertion/timeout weakened.
- Final release-state regressions, metadata deployment/public agreement and native Windows launch evidence follow after actual execution. No Task 10.

## 2026-11-02 — Task 9 local five-utility batch

Task 9 local development is complete on `feat/task-9-five-tool-batch`, based on synchronized Task 8 main `31948b0cd43a64527372bd090553847b59de1598` (tree `3694236221c04c3027341e02c8f9e138376e3e1f`). The actual proposal-only planner selected five existing READY/P1 entries at ranks 10–14; no eligible entry skipped, new registry entry, changed priority or unmet tool dependency. UUID Generator received separate cryptographic design/failure checks. Each independently progressed READY → IMPLEMENTED → TESTED / REQUIRED_PASSED after real tests and a source/test commit. Publication remains null.

The five local cards say **Tested · publication pending**. All 13 prior released cards remain unchanged; local hub has 18 cards. Inventory: 93 total, 13 RELEASED, 5 TESTED, 6 READY, 68 PLANNED, 1 BLOCKED. Released milestone stays 13/25 (52%). No push, PR, merge, deployment, RELEASED transition or Task 10.

Added UUID Generator, Timestamp Converter, Percentage Calculator, Percentage Change Calculator and Discount Calculator with independent pure adapters, logic/browser/hub tests, exact validation/limits/defaults, source-bound audits and local tested cards. Existing generator/test/integration gates used unchanged, with sequential canonical promotion. All 13 released sources/cards/entries/evidence, CNAME, owner analytics, shared framework/templates/dashboard/launcher, active checkout and existing shortcut identities preserved.

## Released — Task 8 four utilities (2026-11-02)

PR #12 merged normally as `5e6df5389455cf9d580d9985eaa504c43a1c1b69` at 2026-11-02T02:45:09Z. Actual successful [Pages run 41379385778](https://github.com/Juster06/micro-tools-hub/actions/runs/41379385778) and independent public browser/approved-source checks qualified each released utility. Current inventory: 93 total, 13 RELEASED, 0 TESTED, 11 READY, 68 PLANNED, 1 BLOCKED; milestone 13/25 (52%).

- Per-tool real public behavior and exact whole-HTML source checks precede RELEASED. Separate release audits preserve original implementation evidence.
- Preserved all thirteen utility implementations, nine previous cards/release entries/evidence/CNAME and owner homepage analytics. Only the four qualifying availability labels change via existing gated proposals.
- Eight lifecycle-aware integration headers retain strict publication/navigation checks and include independently released Task 8 entries in global inventory assertions. No assertion/timeout or utility behavior was weakened.
- Final regression, release-metadata deployment/public agreement and native Desktop/Start menu verification are recorded in the latest handoff. No Task 9.

## 2026-11-02 — Task 8 local four-utility batch

Task 8 is local only on `feat/task-8-four-tool-batch`, based on synchronized Task 7 main `a6ea73b24ceeeca4e6f695ad2840fd720dfb36ce`. Four existing READY/P1 entries at ranks 6–9 were selected by the actual proposal-only planner, no skipped eligible entry, unmet tool prerequisite, new registry entry or changed priority. Independent READY → IMPLEMENTED → TESTED transitions use source-bound scoped evidence; publication remains null. New cards say **Tested · publication pending**; local hub contains 13 cards, with all nine released cards unchanged. Inventory: 93 total, 9 RELEASED, 4 TESTED, 11 READY, 68 PLANNED, 1 BLOCKED. Released milestone remains 9/25 (36%). No push, PR, merge, deployment, RELEASED transition or Task 9.

Added standalone Text Reverser, JSON Formatter, URL Encoder and Decoder, and Base64 Encoder and Decoder, independent logic/browser/integration tests, exact policies/limits, four source-bound audits and the scoped development plan. Existing generation/testing/integration gates were used unchanged. Added a tested export guard against native Blob replacement of isolated UTF-16 surrogates. Preserved original source checkpoints, released pages/cards/evidence/CNAME, framework/dashboard/launcher and shortcut definitions. Final executed results and native launch scope are recorded in the latest handoff and development plan.

## Released — Task 7 verified text utilities (2026-11-01)

- PR #11 merged normally as `d3ddb6de807913c05832e24a77797f033b353497` at 2026-11-01T22:51:53Z. Actual successful [Pages implementation run 41359251674](https://github.com/Juster06/micro-tools-hub/actions/runs/41359251674), independent live browser behavior and exact approved public source hashes passed before each RELEASED transition. Original local audits/source checkpoints remain preserved. Current inventory: 93 total, 9 RELEASED, 0 TESTED, 15 READY, 68 PLANNED, 1 BLOCKED; milestone 9/25 (36%).
- Independently verified each qualifying utility with real public DOM scenarios and exact HTML/inline JS/CSS hashes. Added separate release audits; preserved original implementation audits and six prior sources/cards/evidence/CNAME.
- Updated only qualifying card availability via the existing gated proposals. Three lifecycle-aware integration headers strictly validate publication evidence; the existing Duplicate Line Remover global inventory assertion now includes the released Task 7 batch. No utility implementation, shared gate or test timeout changed.
- Final regression, metadata-deployment and native shortcut checkpoints are recorded in the latest handoff. No Task 8.

## Unreleased — Task 7 local three-tool batch (2026-11-01)

- Planner selected existing READY Text Sorter, Slug Generator and Find and Replace, in registry order. Preferred unregistered candidates were not added. Generated and inspected separate text scaffolds, implemented actual standalone pages, and committed each source/test checkpoint before evidence.
- Added deterministic stable lexical/numeric sorting with truthful invalid-numeric handling; Unicode/ASCII slug generation with explicit accent rules; and literal find/replace preview with match counts, Apply and Undo. Each has live preview, accurate statistics, bounded inputs, no silent truncation, copy/download failure handling and stale-state guards.
- Added independent exact logic fixtures, boundary/invalid-input tests and real Chromium suites including 320/375/768/1440 layouts, original preservation, rapid changes, composition, delayed clipboard, UTF-8 download cleanup, keyboard, safe rendering and processing transport/storage probes. Actual results and scope are in three separate audits and the latest handoff.
- Advanced each independently to TESTED / REQUIRED_PASSED, publication null. Prepared three gated local cards labeled Tested · publication pending. Six released sources/cards/evidence, CNAME, shared framework/templates, dashboard/launcher/shortcuts and unrelated registry entries are preserved. Inventory becomes 6 RELEASED, 3 TESTED, 15 READY, 68 PLANNED, 1 BLOCKED, 93 total; release milestone remains 24%.
- Local commits only. No push, PR, merge, deployment, new release or Task 8.

## Released — Duplicate Line Remover (Task 6, 2026-11-01)

- Merged PR #10 normally as `34ad939b7802ff2c0342d591e9773b06d78a0fbd` at 2026-11-01T05:13:30Z; preserved original local feature history and safely fast-forwarded main. Reviewed feature trees are identical.
- Verified successful GitHub Pages main/root deployment run 41276101870, actual public matching/options/statistics/actions/keyboard/mobile/navigation and all five existing public routes. Deployed normalized source SHA-256 `bf1ea35d9ddf0610f3003d3ce73ff1661275f9006d478e2a1b9f2d52fa28b9b6` exactly matches reviewed HTML/inline JS/CSS.
- Advanced only Duplicate Line Remover to RELEASED after these gates. Original implementation audit is unchanged; separate release audit records genuine publication checks. Updated only its hub availability to Live; generated inventory becomes 6 RELEASED, 0 TESTED, 18 READY, 68 PLANNED, 1 BLOCKED, 93 total and 6/25 (24%).
- Adapted its integration assertions to require valid publication and released counts for the released lifecycle. Source HTML, other five tools/cards/evidence, CNAME, shared framework/templates and dashboard/shortcut code are unchanged. Final regression and metadata-deployment/shortcut verification checkpoints appear in the latest handoff.

## Unreleased — Duplicate Line Remover (Task 6, local only, 2026-11-01)

- Used Task 4 dry run and real text scaffold, implemented in the ignored bundle and deliberately promoted the actual standalone source/tests. No shared template change.
- Added first-occurrence Set-based matching with case/trim comparison options, separate blank removal and deterministic post-deduplication sorting. Retained lines preserve original text; LF/CRLF/CR, Unicode, trailing records and all statistics have documented exact rules.
- Added live updates with immediate invalidation, copy success/denial and revision guards, UTF-8 download/URL cleanup, Clear/default reset, labels/keyboard/mobile/fallback styling and explicit 100,000 UTF-16-unit rejection without truncation.
- Added exact-output framework fixtures and additional full-limit/invalid-input/real browser tests; recorded actual local visual/source evidence. Only Duplicate Line Remover becomes TESTED, publication null; five released sources/cards, CNAME, management framework, dashboard and shortcut definitions are preserved.
- Final regression, gated homepage integration and actual native dashboard checks are recorded in the latest handoff. No push, PR, merge, deploy, RELEASED transition or Task 7.


## Released — Case Converter (Task 5, 2026-11-01)

- Merged PR #9 normally as `97a0912a9f6e917c4d6457e856bed45fbc325450`; preserved the original local feature branch and safely fast-forwarded main. Both reviewed feature commits have tree `792bd602b4a1d2fa7fc3907914531ba155ebd610`.
- Verified successful GitHub Pages main/root deployment run 41272001438, genuine public behavior and exact normalized Case Converter source SHA-256 `a72c78ed3dd52771f45aa3be0b1735fa6c36b582480282081d64e22c666f50c6`. No implementation transformation was required.
- Advanced only Case Converter to RELEASED after these gates; retained its original local audit and added a separate dated release audit. Updated only its framework-managed hub availability to Live and derived inventory to 5 RELEASED, 0 TESTED, 19 READY, 68 PLANNED, 1 BLOCKED (93 total); 5/25 = 20%.
- Adapted the tool-specific integration assertion to the registry lifecycle, preserving strict Tested/publication-pending or RELEASED/Live expectations. Public tool HTML, original four tools, CNAME, shared framework and dashboard/shortcut code are unchanged.
- Local and live checks distinguish simulated clipboard/download APIs from OS permissions/save dialogs. Final validation, metadata deployment and shortcut verification are recorded in the latest handoff.

## Unreleased — Case Converter (Task 5, local only, 2026-11-01)

- Implemented seven actual case conversions from the Task 4 generator, with documented title/sentence/Unicode rules and preserved original input/whitespace.
- Added live code-point/whitespace-token/line counters, debounced conversion with immediate stale-result invalidation, clipboard denial handling, UTF-8 download/object-URL cleanup, Clear, keyboard and mobile layouts.
- Added exact-output logic cases, counter/large-input tests and real Chromium UI/integration tests. Existing four released pages, CNAME, dashboard and launcher code remain unchanged.
- Recorded source-matched scoped local audit evidence and advanced only Case Converter to TESTED. The framework's gated homepage patch is reviewed/applied on the local feature branch, preserving existing cards; new card says publication pending.
- Released count stays four. No push, pull request, merge, deployment or live publication verification is included.

## Unreleased — Reusable tool development framework (Task 4, 2026-11-01)

- Added a new-tool contract, text/structured standalone templates, generation-time shared UI fragments and practical developer guide with a Case Converter dry-run example only.
- Added safe registry-driven scaffold generation with dry-run, existing-file protection, path checks and rollback; bundles remain ignored and unpublished.
- Added ordered dependency-aware batch proposals and gated minimal homepage patch previews; neither changes lifecycle or publishes placeholders.
- Added independently scoped structural, real Node logic and optional isolated Chromium interaction testing, hash-bound ignored reports, neutral template verification and released-page regression cases.
- Preserved all released HTML, homepage, CNAME, registry, existing tracking report schemas, dashboard code and Windows shortcut identities. Task 5 is deferred; Task 4 is committed locally only.

Meaningful project changes, with source state separated from publication. Git history is authoritative for exact commit timestamps.

## Unreleased — local Project Control Dashboard (Task 3)

- Extended the installed launcher into seven local Tk screens: overview/milestones, read-only searchable/filterable/sortable registry/details, development queue, testing/validation, activity/documents, blockers and Quick Actions/complete latest command output. Preserved shortcut targets and AppUserModelID.
- Separated data, operations, widgets, screens and coordination; added batched rendering/debounced search, hash-based evidence freshness, an OS-backed dashboard refresh lock and safe local settings/actions. Missing test totals remain unavailable; structural PASS is never treated as functional test success.
- Added temporary-fixture coverage for malformed/missing/partial data, counts, ordering, freshness, safe actions, worker/concurrency failures and 1,500-entry Windows Tk rendering. Existing management/shortcut behavior remains tested.
- Added optional local Git path settings for desktop PATH differences, no-console Git calls, native startup errors and scrollable/scaled-display overview layout. Updated architecture, continuity and usage docs; Task 4 remains separately scoped. No public website, inventory, analytics or advertising changes.

## Unreleased — Windows project-status launcher (Task 2.5)

- Added a responsive Tkinter GUI that automatically runs the existing project-status command, streams output, shows success/warnings/failure, and provides Run Again, Open Reports, Open Project Folder and Close.
- Added a verified current-user Desktop/Start menu shortcut installer using standard-library Windows Shell APIs, absolute paths, the same Python installation, a default icon and matching AppUserModelID. Taskbar pinning remains manual; no registry/settings pin manipulation is performed.
- Added temporary-fixture launcher tests and native Windows shortcut round-trip/idempotence checks. Real GUI controls, independent cwd, responsiveness and deliberate failure output were exercised; scaled-display button clipping found during GUI testing was fixed.
- Documented installation, recreation, manual pinning, dependencies, behavior and future dashboard extension points. No Task 3, public website, tool inventory or backend changes.

## Unreleased — automated tracking infrastructure (Task 2)

- Extended the existing registry and generated-document conventions with a Python standard-library tracking engine and six command entry points, including one complete project-status command.
- Added schema/dependency/cycle checks, read-only source/link/evidence consistency checks, static HTML/control verification, category/priority/milestone reports, generated Git handoff, and four ignored latest-only JSON reports.
- Retained Node commands/exports as a UTF-8 compatibility bridge to the shared Python rules.
- Fixed the pre-existing false stale-document failures caused by Windows CRLF checkouts. Added isolated unittest fixtures covering failure handling, repeat generation, note preservation, Git failures, CLI paths, and a 1,500-tool dependency chain.
- Updated checkpoint instructions, architecture, README, progress and handoff. Added milestone/interface metadata without changing existing tool statuses or functional verification dates.
- Existing website HTML and domain configuration are unchanged. No new utilities, external services, analytics, advertising, or deployment were introduced.
- Pre-merge review added regressions for malformed tool objects and verification-report structures; both now return validation failures rather than crashing.

Task 2 publication and merge are authorized by the owner's follow-up request. Its scripts never commit, push, deploy or claim that static checks are functional tests; repository delivery is a separate reviewed action. See the latest handoff for verified delivery checkpoints.

## Unreleased — persistent project-memory foundation

- Added permanent agent startup/shutdown instructions and a documented continuation procedure.
- Added an authoritative master plan, architecture, decisions, progress tracker, roadmap, and session handoff.
- Added a machine-readable canonical tool inventory, priorities, next-twenty sequence, and overlap/dependency notes.
- Reconciled every initial proposed utility to a canonical record, including existing embedded features.
- Recorded a 2026-10-31 functional smoke and matching-live-source baseline for the homepage and existing tools.
- Added dependency-free Node consistency/synchronization commands and management-validator regression tests.
- Updated the README to explain the management files and commands.
- Preserved all existing HTML, domain configuration, and functionality. No new utilities, ad/analytics scripts, or recurring automations implemented.

These documentation changes are delivered on a feature branch for review; this entry does not assert a merge or deployment. Check `SESSION_HANDOFF.md` and Git for delivery state.

## 2026-10-31 — documented and published baseline

- Expanded the project README (`1cf6a8a`).
- Integrated Social Media Character Counter & Live Previewer through PR #3 (`74886b5` merge).
- Added the custom-domain CNAME (`e956dcc`) and Google site-verification tag (`4dc4354`).
- Publication of the current baseline pages was checked again during the management setup; evidence is in `audit/BASELINE_VERIFICATION.json`.

## 2026-10-30 — initial utility hub

- Existing history records a searchable WebUtils Hub dashboard and the Text Cleanser, Excel Sandbox, and Stream Roulette utilities, merged through PR #2 (`ef135df`).
- This historical summary does not retroactively claim tests or deployment checks performed on that date.
