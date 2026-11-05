# Everyday Digital Box — WebUtils Hub

<!-- TASK18:START -->
## Task 18 — development checkpoint

Task 17 is complete; consent-aware GA4 and the privacy notice are preserved.
Task 18 starts from `f35f07ee5da8c5c4efdf7d3f1ffeabe75571a16a` on
`feat/task-18-six-tools` in a separate worktree. Owner authorization covers
development, tests, commits and a PR; merge/deployment/bypass are not authorized.

Locally TESTED, publication pending: YouTube Title Checker.
Inventory: 93 registered, 50 RELEASED, 1 TESTED, 0 READY,
41 PLANNED, 1 BLOCKED. The 75-release planning checkpoint and
existing 100-release generated target are unchanged. See
`audit/TASK_18_DEVELOPMENT_PLAN.md`, individual READMEs, tests and source-bound
verification audits for features, resource limits, actual test scope and omissions.
Focused logic, real Chromium, canonical layers and homepage navigation passed for
each completed tool. Full-batch regression and hosted checks are recorded at final delivery.

**Next major task:** Complete the remaining Task 18 tools sequentially.
Await separate owner authorization before merge/deployment; independently verify
public source and behavior before any RELEASED transition. Property-level GA4
reporting remains unverified. The two unrelated local handoff edits remain intact.
<!-- TASK18:END -->

## Task 17 — deployed consent-aware analytics

PR #30 merged as `c1c050c8594795dcab25d0e2362c0bfb472a5165`; Pages run 41811430121 and post-merge Functional CI 41811430196 succeeded. The homepage, privacy notice, consent script and all 50 released tools were independently verified against deployed source. Fresh isolated Chromium tests verified first-visit choice, rejection, acceptance, navigation and withdrawal. GA4 browser collection requests were verified; property-level reporting remains unverified. Task 17.1 finalizes documentation and source-bound deployment evidence; see `audit/TASK_17_DEPLOYMENT.json` and `audit/TASK_17_CONSENT_REVIEW.md`. No legal compliance certification is claimed.

The registry remains 93 registered, 50 RELEASED, 0 TESTED, 0 READY, 42 PLANNED and 1 BLOCKED. The next planning checkpoint is 75 released tools (50/75); the registry's existing generated growth target remains 100. The three public development templates remain unchanged. Prior per-tool publication records and the pre-deployment candidate snapshot are retained as historical evidence.

## Historical Task 16.1 — public verification before release merge

PR #28 merged as `55589d67807387a71ec9d0d407f1b37dfe6b79f3`. Pages deployment 41802029972 and post-merge Functional CI 41802030797 succeeded. The public homepage and all 50 tool routes returned HTTP 200 and matched approved source; 50 distinct visible cards and canonical links were checked. The previous 49 tools were checked by HTTP/source identity and post-merge CI, without new individual public interaction tests.

CSV Merger passed seven focused public Chromium tests and additional live parsing, header, file-handling and keyboard checks. Its source-bound release audit records the deployed hashes, timestamp, results and limitations. Clipboard and download were simulated; no physical-device, screen-reader or cross-browser certification is claimed. A binary PNG was rejected by UTF-8 validation, but filename extension and MIME type are not strictly enforced.

This release-verification branch proposes 93 registered, 50 RELEASED, 0 TESTED, 0 READY, 42 PLANNED and 1 BLOCKED; milestone 50/50 (100%). Main release metadata remains at 49 RELEASED until this PR is separately authorized, merged and deployed. The Google Analytics consent concern remains unresolved; analytics configuration is unchanged. Historical PR #21 administrator-bypass use remains unverified.

## Task 16 — CSV Merger development in progress

Task 15 is complete and publicly verified. PR #26 merged as `4bbdf90f14f33066ab9bcd2db1a31132b800b62c`; PR #27 merged as `61135c1111360a4867446bb3649996713460b44c`. Pages deployment 41773888585 and post-merge Functional CI 41773888536 succeeded. Public source identity, 49 routes and the six Task 15 utilities were verified. The registry has 49 RELEASED tools, with one release remaining to the milestone of 50.

Task 16 CSV Merger is implemented and locally TESTED on `feat/csv-merger`; publication is pending. The branch inventory is 93 registered, 49 RELEASED, 1 TESTED, 0 READY, 42 PLANNED and 1 BLOCKED. The released milestone remains 49/50 (98%). Files are processed locally with bounded UTF-8 input, exact ordered headers, bounded preview and formula-risk export safeguards. See `audit/TASK_16_DEVELOPMENT_PLAN.md` and `audit/CSV_MERGER_VERIFICATION.json` for limits and test scope. It must not be marked RELEASED until separately authorized integration and independent public verification. The previously identified Google Analytics consent concern remains unresolved; analytics configuration is outside this task. Historical administrator-bypass use for PR #21 remains unverified.

## Historical Task 15.1 — public verification before release merge

PR #26 merged as `4bbdf90f14f33066ab9bcd2db1a31132b800b62c`. Pages deployment 41768704851 and post-merge Functional CI 41768704972 succeeded. The public homepage and 49 tool routes returned HTTP 200 with exact source identity; 49 visible canonical cards were verified. The previous 43 tools were checked through source identity and post-merge CI, without new individual public interaction tests.

The six Task 15 tools passed 12 focused public Chromium tests and extra validation checks. Separate source-bound release audits record dates, deployed hashes, results and limits. Clipboard, downloads and print invocations were simulated. Thumbnail preview supports static PNG only; timer notifications may be delayed by sleep or throttling; CSV formula-risk exports are prefixed; financial results are estimates. No cross-browser, physical-device, screen-reader or native-dialog certification is claimed.

This release-verification branch proposes 93 registered, 49 RELEASED, 0 TESTED, 0 READY, 43 PLANNED and 1 BLOCKED: 49/50 (98%). Main release metadata remains at 43 RELEASED until this PR is separately authorized, merged and deployed. No administrator bypass is authorized. Historical PR #21 administrator-bypass use remains unverified.

## Task 15 — development in progress

Task 14 is complete and publicly verified. PR #24 merged as `130a18045022dfaadec330d13f89b8316c5ccf74`; PR #25 merged as `11fb4b46b235da6f61bb558360decf3bbb946f4c`. Pages deployment 41763445983 and post-merge Functional CI 41763446668 succeeded. The public homepage, all 43 canonical routes and source identity were verified. The registry records 43 RELEASED tools; the current milestone is 50, with seven releases remaining.

Task 15 development on `feat/task-15-six-tools` implements YouTube Thumbnail Preview, Pomodoro Timer, CSV Column Extractor, Duplicate Row Finder, Loan Repayment Calculator and Invoice Generator. Local inventory: 93 registered, 43 RELEASED, 6 TESTED, 0 READY, 43 PLANNED and 1 BLOCKED. The six new homepage cards read Tested · publication pending; their publication evidence is null. The released milestone remains 43/50. Source-bound local audits record test scope and limits. The six utilities cannot be marked RELEASED until independently verified after a separately authorized merge and deployment. Historical administrator-bypass use for PR #21 remains unverified.

## Historical Task 14.1 — six-tool public verification before merge

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

## Task 13 — six-tool development checkpoint

PR #21 merged as `e6e3ba3497cf92e6d17754ec4d0f3c1d3a614080`; Pages run 41741393234 and post-merge Functional CI run 41741393883 succeeded. The 31 public tool pages and homepage matched merged source, all canonical links and release counts were independently checked, and scoped public smoke tests passed for the six Task 12 tools. Task 12 is complete. The milestone is 31/50 released, with 19 releases remaining. Task 13 development is authorized on a feature branch. No claim is made that historical administrator-bypass use was independently verified; relevant audit information was unavailable.

## Historical Task 12.1 — public verification before release metadata merge

PR #20 merged as `5340f1e006bc07f8913f875505e8ee3b20a4aacc`. The [Pages deployment 41727865909](https://github.com/Juster06/micro-tools-hub/actions/runs/41727865909) and [post-merge functional CI 41727866241](https://github.com/Juster06/micro-tools-hub/actions/runs/41727866241) succeeded for that commit. Public HTTPS checks matched the merged homepage and all 31 tool page sources; all 31 canonical links, the custom domain and Analytics identifier were confirmed. The previous 25 pages were checked through public HTTP/source identity and post-merge CI, without new individual public interaction tests.

The six Task 12 utilities passed 26 public Chromium interaction tests plus additional public checks for age, rounding, calendar boundaries, empty input, title, JavaScript and dependencies. Clipboard, download and printing were simulated. Separate release audits record timestamps, normalized hashes, results and limitations. Image Rotator accepts static PNG only; SHA-256 needs a secure context and Web Crypto. No cross-browser, physical-device or native-dialog certification is claimed.

This release-verification branch proposes 93 registered, 31 RELEASED, 0 TESTED, 0 READY, 61 PLANNED, 1 BLOCKED; milestone 31/50 (62%). Main and public release metadata remain at 25 RELEASED until this PR receives separate owner approval, merges and deploys. Do not bypass branch protection.

## Historical Task 12 — six tested utilities before release verification

The Task 12 branch implements six utilities as **TESTED**, with publication evidence pending: Age Calculator (`age-calculator/index.html`), VAT Calculator (`vat-calculator/index.html`), Working Days Calculator (`working-days-calculator/index.html`), Meeting Agenda Generator (`meeting-agenda-generator/index.html`), Image Rotator (`image-rotator/index.html`) and SHA-256 Text & File Hash Checker (`sha-256-hash-checker/index.html`; registry ID `sha256-hash-checker`). The homepage cards explicitly state “Tested · publication pending”. No new utility is RELEASED.

Branch inventory: 93 registered, 25 RELEASED, 6 TESTED, 0 READY, 61 PLANNED, 1 BLOCKED. The first milestone is complete; the next target is 50 released tools. See `audit/TASK_12_DEVELOPMENT_PLAN.md` and the six source-bound verification records for limits, local test scope and outstanding publication evidence. Image Rotator accepts static PNG only (up to 5 MiB and 8 million pixels); SHA-256 requires a secure context with Web Crypto and limits files to 16 MiB. User-provided inputs stay local; hosting and the existing styling CDN remain network requests.

The branch targets `main` for ordinary protected-branch review. Do not merge or deploy without separate owner authorization. After an authorized merge and successful deployment, independently verify the public pages and only then prepare a separate release-evidence update for eligible tools.

## Task 12 — first milestone completed; six-tool batch

The first milestone is complete: PR #19 merged as `9b969e23c8bdb19b50f738f14e367288446ef798`, [Pages run 41588981491](https://github.com/Juster06/micro-tools-hub/actions/runs/41588981491) and [post-merge functional CI 41588982142](https://github.com/Juster06/micro-tools-hub/actions/runs/41588982142) passed. The public homepage, 25 unique routes, public registry, exact deployed source and a scoped File Size Converter interaction check were independently verified. The baseline is 93 registered, 25 RELEASED, 0 TESTED, 0 READY, 67 PLANNED and 1 BLOCKED; milestone 25/25 complete, next target 50. Task 12 development is authorized on a feature branch. Earlier pending-PR notes are historical.

## Historical Task 11.1 — verification before release metadata merge

PR #18 merged as `c97c2d0b2a6d7377df3915b9fcebb0bc758f63ad`. The [Pages deployment 41577979484](https://github.com/Juster06/micro-tools-hub/actions/runs/41577979484) and [post-merge CI 41577980047](https://github.com/Juster06/micro-tools-hub/actions/runs/41577980047) succeeded on that commit. Independent public HTTPS source verification matched all 25 pages and the homepage to the merged source; all 25 homepage routes were verified, and owner Analytics and custom domain remained available. The original 24 utilities were checked by source identity and post-merge CI; no new individual live interactions for those tools are claimed.

The File Size Converter passed 33 actual public Chromium checks covering SI, IEC, cross-system conversions, input limits, rounding, selectors, reset, keyboard, responsive widths and uncaught/console errors. Clipboard was simulated. The separate source-bound release audit records timestamps, hashes, deployment, scope and limitations.

This release-verification branch proposes 93 registered, 25 RELEASED, 0 TESTED, 0 READY, 67 PLANNED, 1 BLOCKED: milestone 25/25 (100%). Main and the public registry remain at 24 RELEASED until this metadata PR is separately authorized, merged and deployed. No administrator bypass or deployment is authorized by this preparation.

## Historical Task 11 — File Size Converter before publication

File Size Converter is implemented and **TESTED** on `feat/file-size-converter`; the canonical route is `file-size-converter/index.html`. The branch homepage card reads **Tested · publication pending**. Its bounded BigInt rational arithmetic distinguishes SI powers of 1000 from IEC powers of 1024, handles plain nonnegative decimals, marks rounding and reports positive values below its display threshold without silently returning zero. No external processing or API is used.

Branch inventory: 93 registered, 24 RELEASED, 1 TESTED, 0 READY, 67 PLANNED, 1 BLOCKED. The release milestone remains 24/25 (96%). Main and the live site remain at 24 RELEASED until separate authorized integration, successful deployment and independent public verification. See `audit/FILE_SIZE_CONVERTER_VERIFICATION.json` for local source-bound scope and limits.

## Task 10 completed; Task 11 development (2026-11-03)

Task 10 and PR #17 were merged as `4fe2a8a9096bdf5286c172378c3f636d88a43264`; [Pages deployment 41575470412](https://github.com/Juster06/micro-tools-hub/actions/runs/41575470412) and [post-merge CI 41575471095](https://github.com/Juster06/micro-tools-hub/actions/runs/41575471095) succeeded. The public homepage, registry, all 24 canonical sources and the six new tools were independently checked. At Task 10 completion the inventory was 93 registered, 24 RELEASED, 0 TESTED, 0 READY, 68 PLANNED, 1 BLOCKED; milestone 24/25 (96%). Previous pending-PR notes below are historical. Task 11 is authorized on a feature branch; implementation is not a public release.

## Historical Task 10.1 — publication verification before merge (2026-11-03)

PR #16 merged as `f7a7553e7fb085302c6f2e24f927a031e234c6e0`. GitHub Pages run [41572786907](https://github.com/Juster06/micro-tools-hub/actions/runs/41572786907) and post-merge functional CI run [41572787293](https://github.com/Juster06/micro-tools-hub/actions/runs/41572787293) succeeded on that commit. Independent HTTPS checks matched the homepage and all 24 tool pages to the approved source; the custom domain and owner Analytics were preserved. The public homepage displayed 24 cards and all six tested links.

Actual public Chromium interactions passed for Profit Margin Calculator, Date Difference Calculator, Countdown Timer, Random Name Picker, Hashtag Organizer and Secure Random Number Generator: normal, empty, invalid, selected edge input, primary action, reset, simulated clipboard and uncaught-error checks; timer pause/resume also passed. Separate per-tool release audits preserve exact timestamps, source hashes, deployment commit and limitations. The existing 18 tools were checked for HTTP/source identity and by post-merge automated CI; no new public browser interactions for those 18 are claimed.

This release-verification branch proposes 93 registered, 24 RELEASED, 0 TESTED, 0 READY, 68 PLANNED and 1 BLOCKED; milestone 24/25 (96%). The public registry and card labels remain at the previous state until this metadata PR is separately reviewed, merged and deployed. This PR requires ordinary protected-main review and CI, with no administrator bypass. Do not merge without owner approval.

## Historical Task 10 — six tested tools before integration

Task 10 implements the last six READY entries (ranks 15–20), each now
**TESTED / REQUIRED_PASSED**, with `publication: null`. Branch
`feat/task-10-six-tool-batch` targets protected `main`. The PR must remain open
for owner review; no merge, bypass, deployment or RELEASED transition is authorized.
The branch hub has 24 unique cards, including six **Tested · publication pending**
labels. Existing 18 released pages/entries/cards/evidence, CNAME, owner Analytics,
framework/runtime/workflow pins and the dashboard/launcher are preserved.

Inventory: **93 registered, 18 RELEASED, 6 TESTED, 0 READY, 68 PLANNED, 1 BLOCKED**.
Before development: 18 RELEASED, 0 TESTED, 6 READY. Released milestone remains
**18/25 (72%)**; implementation/testing/PR completion is not public release.

| Tool | Canonical branch route | Behavior |
| --- | --- | --- |
| Hashtag Organizer | `hashtag-organizer/index.html` | Normalize and group hashtag lists without platform account access. |
| Date Difference Calculator | `date-difference-calculator/index.html` | Compare two calendar dates without daylight-saving drift. |
| Profit Margin Calculator | `profit-margin-calculator/index.html` | Calculate profit, margin and markup with distinct labels. |
| Secure Random Number Generator | `secure-random-number-generator/index.html` | Generate unbiased integers within a validated safe-integer interval. |
| Countdown Timer | `countdown-timer/index.html` | Run a duration timer using an actual deadline rather than interval ticks. |
| Random Name Picker | `random-name-picker/index.html` | Draw from a local list with an explicit replacement policy. |

Local CI partitions passed: Python **142/142**, Node **225/225** plus **791**
inline logic fixtures, real Chromium **268/268** plus **338** browser fixtures /
**987** assertions. Both neutral templates passed (6 logic / 12 browser / 48
assertions). No mandatory failure, skip, cancellation or timeout in the final
run. Registry, source/evidence, all 24 structural profiles and full project status
passed with **zero errors and warnings**. Four legacy isolated-logic adapters
remain explicitly unavailable; their structural/browser checks still run.

See [Task 10 delivery and limitations](audit/TASK_10_DELIVERY.md). Owner review of the Task 10 PR, followed only on explicit approval by ordinary
integration and independent deployment/public-source/behavior verification.
Submit eventual release evidence through another ordinary protected-main PR.
Then review readiness of the 68 PLANNED entries; no READY tools remain. Releasing
these six would produce 24 released tools, so one additional reviewed distinct
tool is still needed for the first milestone. Do not begin another utility now.

## Task 9.5 — functional CI and active main protection

Functional CI is integrated on main through PR 14. The owner activated repository
ruleset **26413762**, [Main Branch Protection - Required Functional CI](https://github.com/Juster06/micro-tools-hub/rules/26413762).
Verified ordinary changes require PRs, zero mandatory approvals, resolved
conversations, current main and the **Required functional checks** aggregate
from GitHub Actions. Force pushes/deletion are blocked; administrators retain
Always allow emergency bypass, which agents must not use routinely.

See [CI documentation](scripts/ci/README.md), [active protection procedures](scripts/ci/MAIN_BRANCH_PROTECTION.md)
and [PR 15's final delivery record](https://github.com/Juster06/micro-tools-hub/pull/15)
for actual source identities, current PR/main CI, final merge and public checks.
All 18 tools, registry/homepage/owner Analytics, domain and dashboard/shortcuts
remain unchanged. Pages deploys independently; its saved configuration could
not be directly read, so no claim is made that every setting was verified.
Task 10 is the next development task and awaits separate authorization.
Earlier stage checkpoints below are historical.

## Historical Stage B — GitHub CI verified; PR awaiting review

[PR #14](https://github.com/Juster06/micro-tools-hub/pull/14) targets main and remains
open. Genuine [hosted run 41425207614](https://github.com/Juster06/micro-tools-hub/actions/runs/41425207614)
passed all Python, Node, real Chromium and aggregate jobs after a narrow CI-only
Windows temporary-root compatibility fix. See [CI coverage, setup and limits](scripts/ci/README.md).
All 18 tools, registry, homepage, owner Analytics, domain, dashboard and shortcuts
remain unchanged. CI does not claim branch-protection enforcement or block the
separate Pages deployment. No merge, deployment, lifecycle/settings change or Task 10.

## Historical Stage B — publication and investigation

[PR #14](https://github.com/Juster06/micro-tools-hub/pull/14) targets main and remains
open. The approved original local commit is preserved with exact published tree
identity. Real hosted verification exposed a Windows temporary-directory alias
issue; a CI-only bootstrap correction and regression guard are being verified.
See [CI documentation](scripts/ci/README.md) and the latest handoff for actual
results. No merge, deployment, repository settings or lifecycle change; no Task 10.

## Historical Stage A — local CI checkpoint

The dedicated local branch `feat/task-9-5-functional-ci` adds genuine Python,
Node and real Chromium quality gates, explicit coverage and failure propagation.
Read [CI commands, setup, platform audit and limitations](scripts/ci/README.md).
The website needs no new build/runtime dependency. All 18 released implementations,
registry entries, homepage cards, owner Analytics, domain and dashboard/shortcuts
remain unchanged. Stage A does not publish, open a PR, merge, deploy or configure
protection; no GitHub-hosted functional pass or Task 10 is claimed.

## Task 9 — five independent public releases (2026-11-02)

PR #13 merged normally as `44620a1f4a5d6ae58366cb392926961d0b8edf7c` at 2026-11-02T07:29:53Z. Actual successful [Pages run 41406674180](https://github.com/Juster06/micro-tools-hub/actions/runs/41406674180) and independent public browser/whole-source checks qualified each released tool. Inventory: 93 total, 18 RELEASED, 0 TESTED, 6 READY, 68 PLANNED, 1 BLOCKED; milestone 18/25 (72%).

| Utility | Public status / route |
| --- | --- |
| UUID Generator | [Live tool](https://everydaydigitalbox.com/uuid-generator/) · RELEASED |
| Timestamp Converter | [Live tool](https://everydaydigitalbox.com/timestamp-converter/) · RELEASED |
| Percentage Calculator | [Live tool](https://everydaydigitalbox.com/percentage-calculator/) · RELEASED |
| Percentage Change Calculator | [Live tool](https://everydaydigitalbox.com/percentage-change-calculator/) · RELEASED |
| Discount Calculator | [Live tool](https://everydaydigitalbox.com/discount-calculator/) · RELEASED |

All 18 utility implementations remain unchanged. Each new release has independent actual public browser tests, exact deployed-source SHA-256 and separate release evidence. Existing 13 released cards/entries/evidence, CNAME, owner Analytics, framework/templates/dashboard/launcher and original branch heads are preserved. Earlier task sections below are historical checkpoints. Final release-metadata deployment and dashboard observations are recorded in the latest handoff; no Task 10.

## Task 9 — local five-utility batch (2026-11-02)

Task 9 local development is complete on `feat/task-9-five-tool-batch`, based on synchronized Task 8 main `31948b0cd43a64527372bd090553847b59de1598` (tree `3694236221c04c3027341e02c8f9e138376e3e1f`). The actual proposal-only planner selected five existing READY/P1 entries at ranks 10–14; no eligible entry skipped, new registry entry, changed priority or unmet tool dependency. UUID Generator received separate cryptographic design/failure checks. Each independently progressed READY → IMPLEMENTED → TESTED / REQUIRED_PASSED after real tests and a source/test commit. Publication remains null.

The five local cards say **Tested · publication pending**. All 13 prior released cards remain unchanged; local hub has 18 cards. Inventory: 93 total, 13 RELEASED, 5 TESTED, 6 READY, 68 PLANNED, 1 BLOCKED. Released milestone stays 13/25 (52%). No push, PR, merge, deployment, RELEASED transition or Task 10.

| Utility / ID | Category / priority / rank | Canonical route | Default behavior |
| --- | --- | --- | --- |
| UUID Generator / `uuid-generator` | developer / P1 / 10 | `uuid-generator/index.html` | One lowercase UUID v4 on explicit Generate; batch/uppercase; fail closed without secure browser crypto |
| Timestamp Converter / `timestamp-converter` | developer / P1 / 11 | `timestamp-converter/index.html` | Explicit epoch seconds; milliseconds/ISO modes; exact UTC report and separate device-local display |
| Percentage Calculator / `percentage-calculator` | calculator / P1 / 12 | `percentage-calculator/index.html` | Percentage of value; part-as-percentage mode; two decimal places |
| Percentage Change Calculator / `percentage-change-calculator` | calculator / P1 / 13 | `percentage-change-calculator/index.html` | Signed change using absolute starting-value denominator; two decimal places; zero-base error |
| Discount Calculator / `discount-calculator` | calculator / P1 / 14 | `discount-calculator/index.html` | Savings/final price; nonnegative price and inclusive 0–100% discount; two decimal places |

UUID: batch 1–1,000, at most 4 UTF-16 input units, 16,000 random bytes / 36,999 output units. Real browser Web Crypto acquisition is separate from deterministic byte-formatting tests; no Math.random fallback or global-uniqueness/security-token guarantee. Timestamp: 64 input units; exact integer milliseconds within ±8,640,000,000,000,000; strict calendar/zone/precision checks, no guessed units. Local time depends on host timezone/Intl/DST and stays outside the copied UTC report. Calculators: 64 units per field; finite ASCII decimal/exponent syntax, magnitude ≤1e12 and nonzero magnitude ≥1e-12; results ≤1e15, report below 1,000 units; native IEEE-754/toFixed at 0/2/4/6 decimals, not arbitrary-precision accounting. Negative bases in change use abs(start); discount range is inclusive 0–100%. See each README and source-bound audit for complete rules.

See [Task 9 development plan](audit/TASK_9_DEVELOPMENT_PLAN.md), tool READMEs and individual audits for actual tests, source hashes and limitations. Browser processing has no input uploads or persistence; existing Tailwind styling and owner homepage analytics are separate.

## Task 8 — four verified public releases (2026-11-02)

PR #12 merged normally as `5e6df5389455cf9d580d9985eaa504c43a1c1b69` at 2026-11-02T02:45:09Z. Actual successful [Pages run 41379385778](https://github.com/Juster06/micro-tools-hub/actions/runs/41379385778) and independent public browser/approved-source checks qualified each released utility. Current inventory: 93 total, 13 RELEASED, 0 TESTED, 11 READY, 68 PLANNED, 1 BLOCKED; milestone 13/25 (52%).

| Utility | Public release and exact rules |
| --- | --- |
| Text Reverser | [Live tool](https://everydaydigitalbox.com/text-reverser/) · RELEASED · [Rules/tests](text-reverser/README.md) |
| JSON Formatter | [Live tool](https://everydaydigitalbox.com/json-formatter/) · RELEASED · [Rules/tests](json-formatter/README.md) |
| URL Encoder and Decoder | [Live tool](https://everydaydigitalbox.com/url-encoder-decoder/) · RELEASED · [Rules/tests](url-encoder-decoder/README.md) |
| Base64 Encoder and Decoder | [Live tool](https://everydaydigitalbox.com/base64-encoder-decoder/) · RELEASED · [Rules/tests](base64-encoder-decoder/README.md) |

Original implementation audits, all nine previous release source/card/evidence sets and CNAME remain unchanged. Owner-added homepage Google Analytics remains intact; input processing on these four utility pages is local without transport or persistence. Final release-metadata deployment/native checks are recorded in the latest handoff. Do not begin Task 9.

## Reusable utility development

Task 4 provides development-only scaffolding, templates, functional checks, homepage patch previews and ordered batch proposals. Read the [utility contract](TOOL_CONTRACT.md) and [developer guide](TOOL_DEVELOPMENT_GUIDE.md) before implementing a tool. Use `python scripts/plan_tool_batch.py --count 10` to inspect READY work; scaffold generation accepts existing READY entries only, and an inspected dry run precedes implementation. Select work only within the latest owner-authorized scope.

Python 3.10+ standard library runs the generator/planner/structural checks; Node 22.4+ and an installed Chromium browser enable actual logic/interaction tests. Tool users need only their browser. Public website, GitHub repository and existing dashboard shortcuts remain unchanged.

**Small tools. Everyday wins.**

Everyday Digital Box is a collection of free, focused browser utilities for everyday writing, spreadsheet work, social content, and entertainment discovery. The website is branded **WebUtils Hub**, and its GitHub repository is named **micro-tools-hub**.

The project is intended for creators, writers, students, developers, and office workers who want to finish a small task without installing software or creating an account. The live hub contains 31 released standalone tools, linked from the searchable homepage.

## Project links

| Resource | Link |
| --- | --- |
| Live website | [everydaydigitalbox.com](https://everydaydigitalbox.com/) |
| GitHub repository | [Juster06/micro-tools-hub](https://github.com/Juster06/micro-tools-hub) |
| Project owner | [Juster06 on GitHub](https://github.com/Juster06) |
| Source branch | [main](https://github.com/Juster06/micro-tools-hub/tree/main) |
| Issues and suggestions | [GitHub Issues](https://github.com/Juster06/micro-tools-hub/issues) |
| Proposed changes | [Pull requests](https://github.com/Juster06/micro-tools-hub/pulls) |

## Development continuity and project planning

Future development sessions should begin with [AGENTS.md](AGENTS.md) and [SESSION_HANDOFF.md](SESSION_HANDOFF.md), inspect Git state, and verify the actual source before choosing work. These repository files preserve project state; they do not schedule agents or guarantee that an unmerged branch is available in another checkout.

| Document | Purpose |
| --- | --- |
| [Project master plan](PROJECT_MASTER_PLAN.md) | Authoritative vision, priorities, constraints, milestones, and deferred scope |
| [Tool registry](TOOL_REGISTRY.json) | Canonical machine-readable inventory, statuses, features, dependencies, and evidence |
| [Progress tracker](PROGRESS_TRACKER.md) | Counts derived from the registry and current work |
| [Roadmap](ROADMAP.md) | Prioritized next-twenty sequence and complete category catalog |
| [Architecture](ARCHITECTURE.md) | Verified runtime structure, design, privacy, limits, and deployment boundaries |
| [Decisions](DECISIONS.md) | Reasons and consequences of significant choices |
| [Changelog](CHANGELOG.md) | Meaningful changes separated from publication claims |
| [Baseline audit](audit/CURRENT_STATE.md) | Source-backed current state and verification scope |
| [Backlog reconciliation](audit/BACKLOG_RECONCILIATION.md) | Each initial proposed utility mapped to its canonical tool |
| [Management commands](scripts/README.md) | Python status workflow, reports, synchronization, and tests; existing Node compatibility |

Tool development is the current priority. Growth milestones are aspirations; new tools are built one at a time with scoped validation. Owner-configured homepage analytics is preserved. Additional analytics, advertising integration, traffic generation, and SEO automation remain deferred. The future 9–11-day SEO observation idea is recorded in the master plan only.

On Windows, the **Everyday Digital Box — Project Status** desktop/Start menu launcher now opens the [local Project Control Dashboard](scripts/DASHBOARD.md), with overview/milestones, registry exploration, queue, validation, activity, blockers and Quick Actions. It reuses the existing tracking workflow and stays separate from the website. Create/recreate shortcuts with `python scripts/install_status_shortcut.py`; existing targets remain valid. See [Windows launcher instructions](scripts/WINDOWS_LAUNCHER.md) for manual taskbar pinning, requirements and limitations.

## What the project provides

- A responsive, dark slate and indigo dashboard with searchable tool cards.
- Nine released utilities including the Task 7 text tools, using vanilla JavaScript for browser processing.
- Standalone HTML pages that can be edited or hosted without an application build step.
- No application backend, database, user accounts, or API keys.
- Consistent navigation back to the hub from each tool.
- Features such as visible keyboard focus, descriptive labels, status messages, and reduced-motion handling.
- Styled advertisement placeholders for possible future monetization.

## Case Converter — released and live verified

[Case Converter](case-converter/index.html) offers uppercase, lowercase, Title Case, Sentence case, Capitalize Words, Alternating Case and Inverse Case, with live character/word/line counts, unchanged original input, Copy, UTF-8 download and Clear. Read [its rules and test scope](case-converter/README.md) before relying on language-specific casing. Input stays in the browser; the limit is 100,000 UTF-16 units.

Task 5 was merged through [PR #9](https://github.com/Juster06/micro-tools-hub/pull/9). [Live Case Converter](https://everydaydigitalbox.com/case-converter/) behavior and deployed source identity were verified on 2026-11-01 before its RELEASED transition. See [release evidence](audit/CASE_CONVERTER_RELEASE_VERIFICATION.json) for deployment, source hash and actual test scope. The hub uses the released “Live” presentation; current inventory is **thirteen released tools**, 13/25 (52%). Use `python scripts/test_tool.py --id case-converter` for scoped regression tests.

## Duplicate Line Remover — released and live verified

[Duplicate Line Remover](duplicate-line-remover/index.html) keeps the first unique line with optional case-insensitive matching, surrounding-whitespace comparison, blank removal and deterministic sorting. It preserves original retained text, shows five actual line statistics, updates live, and supports copy/UTF-8 download/Clear. See [rules, limits and tests](duplicate-line-remover/README.md) and [release audit](audit/DUPLICATE_LINE_REMOVER_RELEASE_VERIFICATION.json), with original local evidence retained. [PR #10](https://github.com/Juster06/micro-tools-hub/pull/10) was merged, and actual public behavior plus exact deployed source identity passed on 2026-11-01 before the RELEASED transition. [Open the live tool](https://everydaydigitalbox.com/duplicate-line-remover/). Its hub card uses the established Live presentation. Thirteen tools are released; milestone 13/25 (52%).

## Task 7 — verified public releases

PR #11 merged normally as `d3ddb6de807913c05832e24a77797f033b353497` at 2026-11-01T22:51:53Z. Actual successful [Pages implementation run 41359251674](https://github.com/Juster06/micro-tools-hub/actions/runs/41359251674), independent live browser behavior and exact approved public source hashes passed before each RELEASED transition. Original local audits/source checkpoints remain preserved. Current inventory: 93 total, 9 RELEASED, 0 TESTED, 15 READY, 68 PLANNED, 1 BLOCKED; milestone 9/25 (36%).

| Utility | Release status and rules |
| --- | --- |
| [Text Sorter](text-sorter/index.html) | [Live tool](https://everydaydigitalbox.com/text-sorter/) · RELEASED · [Rules/tests](text-sorter/README.md) |
| [Slug Generator](slug-generator/index.html) | [Live tool](https://everydaydigitalbox.com/slug-generator/) · RELEASED · [Rules/tests](slug-generator/README.md) |
| [Find and Replace](find-and-replace/index.html) | [Live tool](https://everydaydigitalbox.com/find-and-replace/) · RELEASED · [Rules/tests](find-and-replace/README.md) |

Each entry has independent implementation/live/source evidence. Six prior releases and their source/evidence remain unchanged. No additional utility is authorized.

## Available tools

| Tool | Purpose | Open the tool |
| --- | --- | --- |
| Base64 Encoder and Decoder | Encode and decode Unicode text with clear Base64 validation. | [Live tool](https://everydaydigitalbox.com/base64-encoder-decoder/) · [Source](base64-encoder-decoder/index.html) |
| URL Encoder and Decoder | Encode or decode URI components with explicit mode selection. | [Live tool](https://everydaydigitalbox.com/url-encoder-decoder/) · [Source](url-encoder-decoder/index.html) |
| JSON Formatter | Validate, pretty-print and compact JSON locally. | [Live tool](https://everydaydigitalbox.com/json-formatter/) · [Source](json-formatter/index.html) |
| Text Reverser | Reverse text by line, word, or grapheme unit. | [Live tool](https://everydaydigitalbox.com/text-reverser/) · [Source](text-reverser/index.html) |
| Find and Replace | Preview and apply literal text replacements safely. | [Live tool](https://everydaydigitalbox.com/find-and-replace/) · [Source](find-and-replace/index.html) |
| Slug Generator | Create URL-friendly slugs from text with documented Unicode rules. | [Live tool](https://everydaydigitalbox.com/slug-generator/) · [Source](slug-generator/index.html) |
| Text Sorter | Sort text lines using explicit ordering rules. | [Live tool](https://everydaydigitalbox.com/text-sorter/) · [Source](text-sorter/index.html) |
| Duplicate Line Remover | Remove repeated lines with configurable matching and accurate statistics. | [Live tool](https://everydaydigitalbox.com/duplicate-line-remover/) · [Source](duplicate-line-remover/index.html) |
| Case Converter | Seven text-case transformations with live counts, copy and UTF-8 download. | [Live tool](https://everydaydigitalbox.com/case-converter/) · [Source](case-converter/index.html) |
| Social Media Character Counter & Live Previewer | Check caption lengths, preview opening lines, and clean spaces before copying. | [Live tool](https://everydaydigitalbox.com/social-counter/) · [Source](social-counter/index.html) |
| Excel Formula Sandbox & Analyzer | Make nested formulas easier to read and inspect their structure. | [Live tool](https://everydaydigitalbox.com/excel-sandbox/) · [Source](excel-sandbox/index.html) |
| AI Text Footprint Cleanser | Highlight listed phrases and replace them with simpler wording. | [Live tool](https://everydaydigitalbox.com/text-cleaner/) · [Source](text-cleaner/index.html) |
| Free Stream Roulette | Choose a genre and discover a free streaming destination. | [Live tool](https://everydaydigitalbox.com/streaming-roulette/) · [Source](streaming-roulette/index.html) |

### Social Media Character Counter & Live Previewer

Type or paste a caption once to see all four platform counters update together:

| Platform | Configured character limit | Additional guidance |
| --- | ---: | --- |
| X / Twitter | 280 | A progress bar and text warning flag captions beyond the limit. |
| LinkedIn | 3,000 | Captions beyond 140 characters receive an opening-hook warning. |
| Instagram | 2,200 | A preview shows an approximate opening caption. |
| TikTok captions | 4,000 | A phone-style preview shows an approximate short caption opening. |

Features include remaining-character counts, word counts, warning states, four selectable feed previews, expandable preview text, an example caption, and a clear button. **Clean Spaces & Copy** removes repeated horizontal whitespace, trims line edges, preserves internal line breaks, and copies the cleaned caption. If clipboard access fails, the page provides a manual-copy fallback.

Counts use Unicode code points and include spaces and line breaks. They are not a full reproduction of each platform's publishing rules: X uses weighted counts for some characters and links. Feed previews are estimates, and actual truncation depends on device, app, line wrapping, and platform changes. LinkedIn's 140-character marker is an opening-line guide rather than a guaranteed cut-off. The tool does not publish posts or connect to social accounts.

### Excel Formula Sandbox & Analyzer

Paste an Excel formula to format it into a readable, indented structure. Matching parentheses receive matching colors, and supported function names receive syntax highlighting.

The tool provides:

- Live formatting, a sample formula, a clear button, and formatted copying.
- Function-call counts, nesting depth, and formatted-line counts.
- Basic structural diagnostics for unclosed or unexpected delimiters and quoted sections.
- Handling for quoted text, quoted sheet names, bracketed references, and comma or semicolon separators.
- A 50,000-character processing limit.

This is a structure formatter. It does not calculate formula results, execute formulas, open workbooks, or fully validate Excel syntax. Balanced delimiters alone do not guarantee a valid formula.

### AI Text Footprint Cleanser

Paste a paragraph or draft to highlight phrases from an editorial replacement list. The **Humanize Text** button replaces those listed phrases with simpler alternatives, preserving capitalization where supported. Examples include “utilize” → “use” and “furthermore” → “also”.

The page includes word count, estimated reading time, a phrase-based clutter score, an example, clearing, copying, and undoing its replacement operation. Reading time uses 200 words per minute.

Despite the tool's name, it uses predefined JavaScript rules rather than an AI model or an AI API. The clutter score reflects the proportion of words covered by its phrase list. It cannot determine authorship, detect AI-generated text, guarantee detector results, or measure overall writing quality. Review replacements for meaning and tone.

### Free Stream Roulette

Select a genre and spin to receive a streaming-platform suggestion from a curated list. Filters include Hollywood, classics, documentaries, retro TV, anime, and an all-genres option. The selection logic avoids an immediate repeat when another matching destination is available.

The configured destinations include Tubi, Pluto TV, The Roku Channel, Plex, Internet Archive, Documentary+, RetroCrush, Shout! TV, and Xumo Play.

The tool recommends a destination rather than a specific film or episode, and does not stream or host video. Its platform list is maintained in the page source, rather than fetched from a live catalog. Availability, advertising, account requirements, catalogs, and rights vary by provider and region. Opening a destination takes the visitor to that provider's website.

## Technology and architecture

| Component | Implementation |
| --- | --- |
| Page structure | HTML5 |
| Styling | Tailwind CSS through its official Play CDN, plus small inline CSS rules |
| Behavior | Vanilla client-side JavaScript in each page |
| Icons and illustrations | Inline SVG, text symbols, and CSS |
| Routing | Ordinary links between static HTML pages |
| Data processing | Local functions in the browser |
| Application backend / database | None |
| Build / package installation | Not required for the current site |
| Public domain | `everydaydigitalbox.com` |

The current pages use this Tailwind Play CDN script:

```html
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
```

Each tool keeps its markup, styling rules, and JavaScript together in its own `index.html`. There is no shared JavaScript module or frontend framework. This keeps individual tools portable; common design changes currently need to be applied across multiple pages.

Tailwind describes Play CDN as a development option. The current site uses it for the requested standalone setup; a compiled CSS build would be a possible future production improvement. See the [official Tailwind Play CDN documentation](https://tailwindcss.com/docs/installation/play-cdn).

## Repository structure

```text
micro-tools-hub/
├── index.html                  # Searchable hub and tool cards
├── README.md                   # Project documentation
├── AGENTS.md                   # Instructions for future sessions
├── PROJECT_MASTER_PLAN.md      # Vision, scope, constraints and milestones
├── TOOL_REGISTRY.json          # Canonical inventory and verification status
├── PROGRESS_TRACKER.md         # Registry-derived counts and current work
├── ROADMAP.md                  # Next twenty tools and complete category catalog
├── ARCHITECTURE.md             # Runtime design, limits and deployment
├── DECISIONS.md                # Dated decision log
├── CHANGELOG.md                # Meaningful implementation/documentation changes
├── SESSION_HANDOFF.md          # Continuation instructions and Git context
├── scripts/                    # Python tracking engine and Node compatibility
├── tests/                      # Isolated Python management tests
├── reports/                    # Generated local snapshots, ignored by Git
├── audit/                      # Current-state and baseline verification evidence
├── CNAME                       # Custom domain: everydaydigitalbox.com
├── social-counter/
│   └── index.html              # Social counters and live previews
├── excel-sandbox/
│   └── index.html              # Formula formatter and analyzer
├── text-cleaner/
│   └── index.html              # Phrase-based writing cleaner
└── streaming-roulette/
    └── index.html              # Curated streaming destination picker
```

## Run the project locally

### Open an existing copy

Open the root `index.html` in a modern browser. Use the dashboard cards to navigate to a tool. Keep the directory structure intact so relative links continue to work.

No package installation or build command is required. An internet connection is needed to load the Tailwind CDN styling. Opening external streaming destinations also requires internet access. Without a network connection, the site may appear unstyled unless the required styling is already cached.

### Clone a Git-connected working copy

If you want to make commits and push changes, install Git and clone the repository:

```powershell
git clone https://github.com/Juster06/micro-tools-hub.git
cd micro-tools-hub
```

A folder downloaded as a ZIP can be edited, but normally has no `.git` history or configured remote. Use a clone for the Git commands in this README; do not assume a downloaded folder is already connected to GitHub.

### Use a local web server

A local server is useful for checking site navigation and browser clipboard behavior. If Python is installed, run this from the project root:

```powershell
py -m http.server 8000 --bind 127.0.0.1
```

On systems that expose Python as `python`, use:

```sh
python -m http.server 8000 --bind 127.0.0.1
```

Then open [http://localhost:8000](http://localhost:8000). Stop the server with **Ctrl+C**. This server only serves the static files for local development; it is not an application backend.

Clipboard behavior depends on browser permissions and context. HTTPS or localhost is preferable for testing. Where supported, the tools provide fallback copying or instructions for manual copying.

## Privacy and external requests

The current application code processes captions, text, and formulas in the browser. It does not upload those inputs to an application server, use an AI service, or save drafts in a database or browser storage. Reloading or leaving a page can lose the current input; browser form-restoration behavior may vary.

“Client-side processing” does not mean the website makes no network requests:

- The browser requests the page from its hosting provider.
- Tailwind's styling script loads from the external CDN.
- Following a streaming-provider link loads a separate third-party website.

The homepage includes the owner-configured Google Analytics tag. The four Task 8 utility pages process input locally without input uploads, tracking or persistence; this is separate from homepage analytics. Hosting and CDN providers can receive ordinary request information such as IP addresses and browser headers. Clipboard actions place the copied content on the user's system clipboard.

The dashed **ADSENSE BANNER PLACEMENT** containers are visual placeholders. They do not load Google AdSense code or serve ads in the current implementation. The homepage analytics addition is documented above; adding real advertising or further analytics would change network/privacy behavior and requires separate authorization.

## Hosting and the custom domain

The public website is available at [https://everydaydigitalbox.com/](https://everydaydigitalbox.com/). The repository includes a root `CNAME` file containing `everydaydigitalbox.com`, and the live site is served through GitHub's infrastructure.

The root homepage also includes a Google site-verification meta tag. Preserve that tag during homepage updates unless the project owner deliberately changes the verification setup.

The project consists of static files and can be served by a static hosting provider. GitHub Pages publication settings and domain DNS records are configured outside these HTML files. Before changing deployment settings, check the repository's **Settings → Pages** configuration and the domain's DNS settings.

For the existing GitHub-hosted setup:

1. Keep the homepage at the repository root.
2. Keep each tool in its named folder with its own `index.html`.
3. Preserve `CNAME` when updating or transferring the project.
4. Commit and push changes to the branch used by the configured publishing source.
5. Check the repository's deployment status, then verify the public URLs.

A local save does not publish changes. A GitHub commit updates the source, while deployment and caching determine when visitors see it. The configured publication source must include the changed commit.

## Editing, committing, and pushing changes

Run the following only in a Git clone with the correct repository remote. Start by reviewing local changes before pulling:

```sh
git status
git remote -v
```

With a clean working tree, create a branch for a change:

```sh
git switch main
git pull --ff-only origin main
git switch -c feature/describe-your-change
```

Edit the relevant HTML or documentation files, preview the result, then stage the specific paths you changed. For a README-only update:

```sh
git diff -- README.md
git diff --check
git add README.md
git commit -m "docs: update project README"
git push -u origin feature/describe-your-change
```

Open a pull request targeting `main` so the changes can be reviewed before merging. GitHub write access is required to push to this repository; configure credentials through Git or your GitHub client rather than placing tokens in source files.

## Adding another tool

1. Create a descriptive folder such as `new-tool/` and put the complete page in `new-tool/index.html`.
2. Match the existing slate/indigo theme, spacing, typography, and accessible focus states.
3. Add a top-left **← Back to Hub** link with `href="../index.html"`.
4. Implement the tool locally in the browser and clearly explain any processing limits.
5. Add a card inside `#toolGrid` in the root `index.html`, with a matching relative link, unique heading ID, and searchable `data-title`.
6. Update the homepage's initial tool-count text. The runtime filter counts the cards automatically.
7. Check navigation and searching, then add the tool's description and links to this README.
8. Update the canonical registry entry, test/publication evidence, changelog, and session handoff. Run the synchronization and validation commands below. A registry entry alone does not create or publish a utility.

Use `textContent` when displaying user input rather than interpreting it as HTML. If a tool introduces a remote service, persistent storage, advertising, or account access, document that behavior instead of retaining an inaccurate local-only claim.

## Verification and maintenance

The website has no package manifest or build step. Python 3.10+ and its standard library run the complete developer-only tracking workflow. Run from the repository root:

```sh
python scripts/project_status.py
python -m unittest discover -s tests -v
node --test scripts/project.test.mjs
git diff --check
```

The command checks the registry, project links/source/evidence, and static HTML; updates only marked progress, roadmap and handoff content; and writes latest local JSON reports under ignored `reports/`. It preserves manual notes and does not promote tool statuses. The existing Node commands remain compatibility entry points to the same Python engine; Node 20+ is needed only for their tests.

Use `python scripts/project_status.py --check-only` for a snapshot without documentation updates, or add `--no-report` for no report writes. A downloaded non-Git copy reports Git state as UNKNOWN. These commands do not rerun browser interactions, verify live publication, push/deploy, or perform a security audit. See [management command documentation](scripts/README.md) for individual commands, reports, exit codes, and limitations.

For utility changes, check the affected behavior in a browser and inspect the developer console for errors. Save the actual test scope and results; mark a utility RELEASED only after checking both its implementation and its published version.

Suggested checks:

- Verify all homepage cards, search results, and Back to Hub links.
- Check narrow mobile and desktop layouts for horizontal overflow.
- Check keyboard focus, form labels, buttons, and status messages.
- Test empty input, pasted text, emoji, line breaks, and longer input.
- Check counts at and beyond each configured social limit, including LinkedIn's 140/141-character opening guide.
- Check preview expansion and clipboard success or blocked-permission behavior.
- Check formula examples, unbalanced delimiters, and the input limit.
- Check text replacements, their meaning, capitalization, undo, and copying.
- Check streaming filters and external destinations; update the curated list when providers change.
- Use browser network tools to verify that user input is not transmitted.
- Run `git diff --check` before committing.

Keep social-platform limits and preview assumptions under review because platform behavior can change. The current social-counter implementation was checked in desktop Chromium/Edge and across viewport widths from 320 to 1,600 pixels during its initial integration; this is not a guarantee of testing every browser or future change.

## License

No `LICENSE` file is currently included in the repository. A project license has not been declared in this README.

---

Maintained by [Juster06](https://github.com/Juster06). Visit [Everyday Digital Box](https://everydaydigitalbox.com/) to use the tools, or [open a GitHub issue](https://github.com/Juster06/micro-tools-hub/issues) to report a bug or suggest a utility.
