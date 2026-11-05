# Development roadmap

<!-- TASK18:START -->
## Task 18 — development checkpoint

Task 17 is complete; consent-aware GA4 and the privacy notice are preserved.
Task 18 starts from `f35f07ee5da8c5c4efdf7d3f1ffeabe75571a16a` on
`feat/task-18-six-tools` in a separate worktree. Owner authorization covers
development, tests, commits and a PR; merge/deployment/bypass are not authorized.

Locally TESTED, publication pending: YouTube Title Checker, Instagram Bio Formatter, File Signature Inspector, Image Format Converter, CSV ↔ JSON Converter.
Inventory: 93 registered, 50 RELEASED, 5 TESTED, 0 READY,
37 PLANNED, 1 BLOCKED. The 75-release planning checkpoint and
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

## Historical Task 10 — six tested utilities before integration

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

Owner review of the Task 10 PR, followed only on explicit approval by ordinary
integration and independent deployment/public-source/behavior verification.
Submit eventual release evidence through another ordinary protected-main PR.
Then review readiness of the 68 PLANNED entries; no READY tools remain. Releasing
these six would produce 24 released tools, so one additional reviewed distinct
tool is still needed for the first milestone. Do not begin another utility now.

## Task 9 — independently verified public releases

PR #13 merged normally as `44620a1f4a5d6ae58366cb392926961d0b8edf7c` at 2026-11-02T07:29:53Z. Actual successful [Pages run 41406674180](https://github.com/Juster06/micro-tools-hub/actions/runs/41406674180) and independent public browser/whole-source checks qualified each released tool. Inventory: 93 total, 18 RELEASED, 0 TESTED, 6 READY, 68 PLANNED, 1 BLOCKED; milestone 18/25 (72%).

Exact public source/live evidence is in five separate release audits. Original implementation/prior release audits unchanged; current derived blocks follow the registry. Release-metadata deployment/public agreement and native launch verification precede completion. Earlier task sections are historical. No Task 10.

## Task 9 — local five-utility batch, publication pending

Task 9 local development is complete on `feat/task-9-five-tool-batch`, based on synchronized Task 8 main `31948b0cd43a64527372bd090553847b59de1598` (tree `3694236221c04c3027341e02c8f9e138376e3e1f`). The actual proposal-only planner selected five existing READY/P1 entries at ranks 10–14; no eligible entry skipped, new registry entry, changed priority or unmet tool dependency. UUID Generator received separate cryptographic design/failure checks. Each independently progressed READY → IMPLEMENTED → TESTED / REQUIRED_PASSED after real tests and a source/test commit. Publication remains null.

The five local cards say **Tested · publication pending**. All 13 prior released cards remain unchanged; local hub has 18 cards. Inventory: 93 total, 13 RELEASED, 5 TESTED, 6 READY, 68 PLANNED, 1 BLOCKED. Released milestone stays 13/25 (52%). No push, PR, merge, deployment, RELEASED transition or Task 10.

| Utility / ID | Category / priority / rank | Canonical route | Default behavior |
| --- | --- | --- | --- |
| UUID Generator / `uuid-generator` | developer / P1 / 10 | `uuid-generator/index.html` | One lowercase UUID v4 on explicit Generate; batch/uppercase; fail closed without secure browser crypto |
| Timestamp Converter / `timestamp-converter` | developer / P1 / 11 | `timestamp-converter/index.html` | Explicit epoch seconds; milliseconds/ISO modes; exact UTC report and separate device-local display |
| Percentage Calculator / `percentage-calculator` | calculator / P1 / 12 | `percentage-calculator/index.html` | Percentage of value; part-as-percentage mode; two decimal places |
| Percentage Change Calculator / `percentage-change-calculator` | calculator / P1 / 13 | `percentage-change-calculator/index.html` | Signed change using absolute starting-value denominator; two decimal places; zero-base error |
| Discount Calculator / `discount-calculator` | calculator / P1 / 14 | `discount-calculator/index.html` | Savings/final price; nonnegative price and inclusive 0–100% discount; two decimal places |

Await owner review and separate GitHub preparation authorization. Older task checkpoints below remain historical.

## Task 8 — independent public releases

PR #12 merged normally as `5e6df5389455cf9d580d9985eaa504c43a1c1b69` at 2026-11-02T02:45:09Z. Actual successful [Pages run 41379385778](https://github.com/Juster06/micro-tools-hub/actions/runs/41379385778) and independent public browser/approved-source checks qualified each released utility. Current inventory: 93 total, 13 RELEASED, 0 TESTED, 11 READY, 68 PLANNED, 1 BLOCKED; milestone 13/25 (52%).

Actual per-tool publication/source/live results are in separate release audits; original audits remain unchanged. Final metadata deployment and Windows shortcut checks precede completion. Homepage analytics is preserved; utility input privacy is scoped separately. No Task 9.

## Task 7 — independent releases after live verification

PR #11 merged normally as `d3ddb6de807913c05832e24a77797f033b353497` at 2026-11-01T22:51:53Z. Actual successful [Pages implementation run 41359251674](https://github.com/Juster06/micro-tools-hub/actions/runs/41359251674), independent live browser behavior and exact approved public source hashes passed before each RELEASED transition. Original local audits/source checkpoints remain preserved. Current inventory: 93 total, 9 RELEASED, 0 TESTED, 15 READY, 68 PLANNED, 1 BLOCKED; milestone 9/25 (36%).

The original three implementation audits are unchanged. Separate per-tool release audits contain genuine deployment/public behavior/source evidence. Final metadata publication and native shortcut verification are recorded in the latest handoff. Do not begin Task 8 or another utility.

## Task 6 — Duplicate Line Remover released after live verification

PR #10 merged as `34ad939b7802ff2c0342d591e9773b06d78a0fbd`. Successful main/root GitHub Pages deployment, real public Edge behavior and exact approved normalized source identity passed on 2026-11-01 before RELEASED. Original local audit remains unchanged; separate `audit/DUPLICATE_LINE_REMOVER_RELEASE_VERIFICATION.json` records genuine release evidence and scope. The gated hub card uses the released Live presentation. Counts: 93 total, 6 RELEASED, 0 TESTED, 18 READY, 68 PLANNED, 1 BLOCKED; milestone 6/25 (24%).

Final release-metadata deployment and native shortcut verification are recorded in the latest handoff. No Task 7 or additional utility is authorized; Text Sorter remains a READY queue entry only.

## Task 5 — Case Converter released after live verification

PR #9 merged as `97a0912a9f6e917c4d6457e856bed45fbc325450`. The actual public Case Converter passed scoped live behavior checks and normalized deployed-source identity verification on 2026-11-01 before the RELEASED transition. The original local audit is retained; `audit/CASE_CONVERTER_RELEASE_VERIFICATION.json` records release evidence and limitations. The hub card uses the established Live label. Inventory: 93 total, 5 RELEASED, 0 TESTED, 19 READY, 68 PLANNED, 1 BLOCKED; milestone 5/25 (20%).

Task 5 final publication verification is recorded in the latest handoff. No additional utility is authorized; Duplicate Line Remover remains a READY queue entry only.

## Framework readiness — Task 4

Reusable templates, safe staged scaffolding, functional checks and validated homepage patch proposals are available. Use `python scripts/plan_tool_batch.py --count 10` to propose existing READY work in sequence; proposals are not authorization to build or publish a batch. See `TOOL_DEVELOPMENT_GUIDE.md`. Task 4 changed no tool status/count; the Task 5 checkpoint above records the subsequent utility implementation.

Source of inventory, status, priority, dependencies, and order: `TOOL_REGISTRY.json`. Run `node scripts/project.mjs sync` after changing it. The complete proposal mapping is in `audit/BACKLOG_RECONCILIATION.md`.

## Priority and effort conventions

- **P1:** the next scoped browser-native sequence. **P2:** accepted follow-up work. **P3:** specialist or high-risk work needing further design.
- **S:** a bounded interface and straightforward local transformation. **M:** several modes or more substantial validation. **L:** complex parsing, UX, formats, or performance. **XL:** feasibility/security design dominates. These are relative complexity estimates, not elapsed-time commitments.
- **READY:** features and a local approach are defined; still requires a brief implementation plan and tests. **PLANNED:** resolve scope/dependencies first. **BLOCKED:** an explicit prerequisite is unmet.

## Next twenty distinct utilities

Execute in order unless the user steers the project or a dependency/regression justifies a documented change. Current implementation states are shown below; sequence rank alone does not imply implementation or publication.

<!-- GENERATED:SEQUENCE:START -->
| Order | Tool ID | Name | Category | Complexity | Status |
| ---: | --- | --- | --- | --- | --- |
| 1 | case-converter | Case Converter | Text and Writing Tools | S | RELEASED |
| 2 | duplicate-line-remover | Duplicate Line Remover | Text and Writing Tools | S | RELEASED |
| 3 | text-sorter | Text Sorter | Text and Writing Tools | S | RELEASED |
| 4 | slug-generator | Slug Generator | Text and Writing Tools | S | RELEASED |
| 5 | find-and-replace | Find and Replace | Text and Writing Tools | S | RELEASED |
| 6 | text-reverser | Text Reverser | Text and Writing Tools | S | RELEASED |
| 7 | json-formatter | JSON Formatter | Excel and Data Tools | S | RELEASED |
| 8 | url-encoder-decoder | URL Encoder and Decoder | Developer Tools | S | RELEASED |
| 9 | base64-encoder-decoder | Base64 Encoder and Decoder | Developer Tools | S | RELEASED |
| 10 | uuid-generator | UUID Generator | Developer Tools | S | RELEASED |
| 11 | timestamp-converter | Timestamp Converter | Developer Tools | S | RELEASED |
| 12 | percentage-calculator | Percentage Calculator | Calculators | S | RELEASED |
| 13 | percentage-change-calculator | Percentage Change Calculator | Calculators | S | RELEASED |
| 14 | discount-calculator | Discount Calculator | Calculators | S | RELEASED |
| 15 | profit-margin-calculator | Profit Margin Calculator | Calculators | S | RELEASED |
| 16 | date-difference-calculator | Date Difference Calculator | Calculators | S | RELEASED |
| 17 | countdown-timer | Countdown Timer | Everyday Productivity Tools | S | RELEASED |
| 18 | random-name-picker | Random Name Picker | Everyday Productivity Tools | S | RELEASED |
| 19 | hashtag-organizer | Hashtag Organizer | Social Media Tools | S | RELEASED |
| 20 | secure-random-number-generator | Secure Random Number Generator | Security and Privacy Tools | S | RELEASED |
<!-- GENERATED:SEQUENCE:END -->

## Practical delivery sequence

1. **Text transformations (orders 1–5):** settle Unicode/case/line/whitespace behavior; preserve original text where a transformation could surprise the user; integrate each finished page.
2. **Text and developer basics (6–10):** grapheme policy, parse errors, UTF-8 encoding, URI modes, cryptographic UUID generation. Never treat Base64 as encryption.
3. **Dates and arithmetic (11–15):** explicit epoch units, finite input, formulas, zero-denominator handling, and rounding. No live financial or legal-rate claims.
4. **Productivity and social basics (16–20):** date-only arithmetic, deadline-based timers, unbiased draws, hashtag rules, and cryptographic integer sampling. Test boundaries rather than relying on happy paths.
5. **Milestone review:** those twenty plus the baseline would total 24 released tools if all are completed and published. Reassess quality, then consider Image Rotator as the next distinct utility to reach 25.
6. **Format processing:** evaluate PDF/image/CSV libraries and size limits; begin with bounded manipulations such as page rotation or image resizing. Resolve parser reuse before creating several CSV tools.
7. **Specialist work:** proceed only after feasibility/security design for PDF compression, local encryption, hostile SVG/HTML, regex workers/timeouts, complex minifiers, and EXIF removal.

For every step: check for duplicates → plan → implement → test → integrate → document → verify publication. Complete unfinished work before starting an unrelated page.

## Category catalog

This catalog includes existing and proposed utilities, with status explicitly shown. Proposed directories are reserved names only, not existing pages. Runtime library candidates are not installed dependencies. All eleven requested categories are represented.

<!-- GENERATED:CATALOG:START -->
### PDF Tools

| Tool ID | Utility | Status | Priority | Complexity | Dependencies / gate |
| --- | --- | --- | --- | --- | --- |
| pdf-merger | PDF Merger | PLANNED | P2 | M | PDF parsing/manipulation library: evaluate license, size, encryption and malformed-file behavior before selection |
| pdf-splitter | PDF Splitter | PLANNED | P2 | M | PDF parsing/manipulation library: evaluate license, size, encryption and malformed-file behavior before selection |
| pdf-rotator | PDF Rotator | PLANNED | P2 | M | PDF parsing/manipulation library: evaluate license, size, encryption and malformed-file behavior before selection |
| image-to-pdf | Image to PDF | PLANNED | P2 | M | PDF parsing/manipulation library: evaluate license, size, encryption and malformed-file behavior before selection |
| pdf-to-image | PDF to Image | PLANNED | P2 | L | PDF parsing/manipulation library: evaluate license, size, encryption and malformed-file behavior before selection |
| pdf-watermark | PDF Watermark | PLANNED | P2 | M | PDF parsing/manipulation library: evaluate license, size, encryption and malformed-file behavior before selection |
| pdf-page-numbering | PDF Page Numbering | PLANNED | P2 | M | PDF parsing/manipulation library: evaluate license, size, encryption and malformed-file behavior before selection |
| pdf-metadata-viewer | PDF Metadata Viewer | PLANNED | P2 | M | PDF parsing/manipulation library: evaluate license, size, encryption and malformed-file behavior before selection |
| pdf-compressor | PDF Compressor | BLOCKED | P3 | XL | PDF parsing/manipulation library: evaluate license, size, encryption and malformed-file behavior before selection |

### Image Tools

| Tool ID | Utility | Status | Priority | Complexity | Dependencies / gate |
| --- | --- | --- | --- | --- | --- |
| image-compressor | Image Compressor | PLANNED | P2 | M | Browser image decoding and Canvas; format support and memory limits must be tested |
| image-resizer | Image Resizer | RELEASED | P2 | M | Browser image decoding and Canvas; format support and memory limits must be tested |
| image-format-converter | Image Format Converter | TESTED | P2 | M | Browser image decoding and Canvas; format support and memory limits must be tested |
| image-cropper | Image Cropper | PLANNED | P2 | L | Browser image decoding and Canvas; format support and memory limits must be tested |
| image-rotator | Image Rotator | RELEASED | P2 | S | Browser image decoding and Canvas; format support and memory limits must be tested |
| image-watermark | Image Watermark | RELEASED | P2 | M | Browser image decoding and Canvas; format support and memory limits must be tested |
| image-color-picker | Image Color Picker | RELEASED | P2 | M | Browser image decoding and Canvas; format support and memory limits must be tested |
| passport-photo-layout-maker | Passport Photo Layout Maker | PLANNED | P2 | L | Browser image decoding and Canvas; format support and memory limits must be tested |

### Text and Writing Tools

| Tool ID | Utility | Status | Priority | Complexity | Dependencies / gate |
| --- | --- | --- | --- | --- | --- |
| text-cleaner | AI Text Footprint Cleanser | RELEASED | P2 | M | Modern browser DOM APIs |
| case-converter | Case Converter | RELEASED | P1 | S | Browser-native approach; scope review before implementation |
| duplicate-line-remover | Duplicate Line Remover | RELEASED | P1 | S | Browser-native approach; scope review before implementation |
| text-difference-checker | Text Difference Checker | RELEASED | P2 | L | Browser-native approach; scope review before implementation |
| text-sorter | Text Sorter | RELEASED | P1 | S | Browser-native approach; scope review before implementation |
| text-reverser | Text Reverser | RELEASED | P1 | S | Browser-native approach; scope review before implementation |
| find-and-replace | Find and Replace | RELEASED | P1 | S | Browser-native approach; scope review before implementation |
| slug-generator | Slug Generator | RELEASED | P1 | S | Browser-native approach; scope review before implementation |

### Excel and Data Tools

| Tool ID | Utility | Status | Priority | Complexity | Dependencies / gate |
| --- | --- | --- | --- | --- | --- |
| excel-sandbox | Excel Formula Sandbox & Analyzer | RELEASED | P2 | M | Modern browser DOM APIs |
| csv-json-converter | CSV ↔ JSON Converter | TESTED | P2 | L | CSV/workbook parsers where needed: evaluate correctness, license and bundle size |
| excel-to-csv | Excel to CSV | PLANNED | P2 | L | CSV/workbook parsers where needed: evaluate correctness, license and bundle size |
| csv-column-extractor | CSV Column Extractor | RELEASED | P2 | M | CSV/workbook parsers where needed: evaluate correctness, license and bundle size |
| duplicate-row-finder | Duplicate Row Finder | RELEASED | P2 | M | CSV/workbook parsers where needed: evaluate correctness, license and bundle size |
| csv-data-cleaner | CSV Data Cleaner | PLANNED | P2 | L | CSV/workbook parsers where needed: evaluate correctness, license and bundle size |
| csv-merger | CSV Merger | RELEASED | P2 | M | CSV/workbook parsers where needed: evaluate correctness, license and bundle size |
| json-formatter | JSON Formatter | RELEASED | P1 | S | Native JSON.parse and JSON.stringify |
| csv-viewer | CSV Viewer | RELEASED | P2 | M | CSV/workbook parsers where needed: evaluate correctness, license and bundle size |
| excel-formula-generator | Excel Formula Generator | PLANNED | P2 | L | Browser-native deterministic templates; no parser or AI service |

### Developer Tools

| Tool ID | Utility | Status | Priority | Complexity | Dependencies / gate |
| --- | --- | --- | --- | --- | --- |
| base64-encoder-decoder | Base64 Encoder and Decoder | RELEASED | P1 | S | Browser-native approach; scope review before implementation |
| url-encoder-decoder | URL Encoder and Decoder | RELEASED | P1 | S | Browser-native approach; scope review before implementation |
| uuid-generator | UUID Generator | RELEASED | P1 | S | Browser cryptographic randomness; feature-detect and fail clearly if unavailable |
| sha256-hash-checker | SHA-256 Text & File Hash Checker | RELEASED | P2 | M | Browser Web Crypto SHA-256; bounded file reads |
| regex-tester | Regex Tester | PLANNED | P2 | L | Browser Worker with termination timeout; bounded input |
| html-formatter | HTML Formatter | PLANNED | P2 | L | Reviewed non-executing HTML parser and whitespace-preservation policy |
| css-minifier | CSS Minifier | PLANNED | P2 | L | Reviewed CSS parser/minifier and license |
| javascript-minifier | JavaScript Minifier | PLANNED | P2 | L | Reviewed JavaScript parser/minifier and license; consider worker isolation |
| timestamp-converter | Timestamp Converter | RELEASED | P1 | S | Browser-native approach; scope review before implementation |

### Social Media Tools

| Tool ID | Utility | Status | Priority | Complexity | Dependencies / gate |
| --- | --- | --- | --- | --- | --- |
| social-counter | Social Media Character Counter & Live Previewer | RELEASED | P2 | M | Modern browser DOM APIs |
| hashtag-organizer | Hashtag Organizer | RELEASED | P1 | S | Browser-native approach; scope review before implementation |
| youtube-title-checker | YouTube Title Checker | TESTED | P2 | S | Browser-native approach; scope review before implementation |
| youtube-description-formatter | YouTube Description Formatter | RELEASED | P2 | M | Browser-native approach; scope review before implementation |
| instagram-bio-formatter | Instagram Bio Formatter | TESTED | P2 | M | Browser-native approach; scope review before implementation |
| social-media-line-break-tool | Social Media Line Break Tool | PLANNED | P2 | S | Browser-native approach; scope review before implementation |
| emoji-picker | Emoji Picker | PLANNED | P2 | M | Reviewed local emoji dataset and usage license |
| hashtag-counter | Hashtag Counter | PLANNED | P2 | S | Browser-native approach; scope review before implementation |
| youtube-thumbnail-preview | YouTube Thumbnail Preview | RELEASED | P2 | M | Browser-native approach; scope review before implementation |
| posting-calendar-generator | Posting Calendar Generator | RELEASED | P2 | M | Browser-native approach; scope review before implementation |
| username-generator | Username Generator | RELEASED | P2 | S | Browser-native approach; scope review before implementation |

### Calculators

| Tool ID | Utility | Status | Priority | Complexity | Dependencies / gate |
| --- | --- | --- | --- | --- | --- |
| percentage-calculator | Percentage Calculator | RELEASED | P1 | S | Browser-native approach; scope review before implementation |
| percentage-change-calculator | Percentage Change Calculator | RELEASED | P1 | S | Browser-native approach; scope review before implementation |
| vat-calculator | VAT Calculator | RELEASED | P2 | M | Browser-native approach; scope review before implementation |
| discount-calculator | Discount Calculator | RELEASED | P1 | S | Browser-native approach; scope review before implementation |
| age-calculator | Age Calculator | RELEASED | P2 | M | Browser-native approach; scope review before implementation |
| date-difference-calculator | Date Difference Calculator | RELEASED | P1 | S | Browser-native approach; scope review before implementation |
| working-days-calculator | Working Days Calculator | RELEASED | P2 | M | Browser-native approach; scope review before implementation |
| loan-repayment-calculator | Loan Repayment Calculator | RELEASED | P2 | M | Browser-native approach; scope review before implementation |
| profit-margin-calculator | Profit Margin Calculator | RELEASED | P1 | S | Browser-native approach; scope review before implementation |
| compound-interest-calculator | Compound Interest Calculator | RELEASED | P2 | M | Browser-native approach; scope review before implementation |

### Security and Privacy Tools

| Tool ID | Utility | Status | Priority | Complexity | Dependencies / gate |
| --- | --- | --- | --- | --- | --- |
| password-generator | Password Generator | PLANNED | P2 | M | Browser Web Crypto where cryptographic randomness or hashing is required |
| password-strength-checker | Password Strength Checker | PLANNED | P2 | L | Reviewed locally bundled password-strength estimator and license |
| secure-random-number-generator | Secure Random Number Generator | RELEASED | P1 | S | Browser cryptographic randomness; feature-detect and fail clearly if unavailable |
| local-text-encryption | Local Text Encryption | PLANNED | P3 | XL | Web Crypto authenticated encryption and password derivation; Separate reviewed threat model and versioned format |
| exif-metadata-viewer | EXIF Metadata Viewer | PLANNED | P2 | L | Reviewed format-specific metadata parser |
| exif-metadata-remover | EXIF Metadata Remover | PLANNED | P2 | L | Reviewed metadata parser/removal method and exported-metadata verifier |
| file-signature-inspector | File Signature Inspector | TESTED | P2 | M | Browser Web Crypto where cryptographic randomness or hashing is required |
| passphrase-generator | Passphrase Generator | PLANNED | P2 | M | Reviewed licensed word list; Browser cryptographic randomness and unbiased selection |
| qr-code-generator | QR Code Generator | PLANNED | P2 | M | Reviewed locally bundled QR encoder and license |

### File Conversion Tools

| Tool ID | Utility | Status | Priority | Complexity | Dependencies / gate |
| --- | --- | --- | --- | --- | --- |
| txt-to-pdf | TXT to PDF | PLANNED | P2 | L | Reviewed PDF text rendering library and font licensing |
| markdown-converter-previewer | Markdown Converter & Previewer | PLANNED | P2 | L | Reviewed Markdown parser and sanitizer; local bundled assets preferred |
| html-to-markdown | HTML to Markdown | PLANNED | P2 | L | Reviewed non-executing HTML-to-Markdown conversion library |
| csv-to-txt | CSV to TXT | PLANNED | P2 | M | Format-specific parsers, sanitizers or encoders: evaluate before implementation |
| json-to-txt | JSON to TXT | RELEASED | P2 | M | Format-specific parsers, sanitizers or encoders: evaluate before implementation |
| svg-to-png | SVG to PNG | PLANNED | P2 | L | Reviewed SVG sanitization and external-resource blocking; Canvas rasterization with tested dimension limits |
| png-to-ico | PNG to ICO | PLANNED | P2 | L | Reviewed local ICO encoder |
| file-size-converter | File Size Converter | RELEASED | P2 | S | Format-specific parsers, sanitizers or encoders: evaluate before implementation |
| html-previewer | HTML Previewer | PLANNED | P2 | L | Sandboxed iframe with restrictive CSP and no script/same-origin privileges |

### Everyday Productivity Tools

| Tool ID | Utility | Status | Priority | Complexity | Dependencies / gate |
| --- | --- | --- | --- | --- | --- |
| pomodoro-timer | Pomodoro Timer | RELEASED | P2 | M | Browser-native approach; scope review before implementation |
| countdown-timer | Countdown Timer | RELEASED | P1 | S | Browser-native approach; scope review before implementation |
| random-name-picker | Random Name Picker | RELEASED | P1 | S | Browser cryptographic randomness; feature-detect and fail clearly if unavailable |
| decision-wheel | Decision Wheel | PLANNED | P2 | M | Browser-native approach; scope review before implementation |
| local-to-do-list | Local To-Do List | RELEASED | P2 | M | Explicit opt-in localStorage, export format and clear-all behavior |
| invoice-generator | Invoice Generator | RELEASED | P2 | L | Browser-native approach; scope review before implementation |
| resume-builder | Resume Builder | PLANNED | P2 | L | Browser-native approach; scope review before implementation |
| meeting-agenda-generator | Meeting Agenda Generator | RELEASED | P2 | M | Browser-native approach; scope review before implementation |
| printable-calendar-generator | Printable Calendar Generator | RELEASED | P2 | M | Browser-native approach; scope review before implementation |

### Entertainment Tools

| Tool ID | Utility | Status | Priority | Complexity | Dependencies / gate |
| --- | --- | --- | --- | --- | --- |
| streaming-roulette | Free Stream Roulette | RELEASED | P2 | S | Modern browser DOM APIs |
<!-- GENERATED:CATALOG:END -->

## Deferred product work

SEO monitoring, advertising, analytics, paid services, accounts, and a backend are not part of this delivery sequence. The future 9–11-day SEO observation concept is recorded in `PROJECT_MASTER_PLAN.md` without an automation or implementation.
