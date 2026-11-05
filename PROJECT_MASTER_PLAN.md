# Project master plan

## Task 18.1 — six-tool public release verification

PR #32 merged as `8cb97c3f1450634524a40aa9b7cf016bd6b3c78e`. Pages
[41961586696](https://github.com/Juster06/micro-tools-hub/actions/runs/41961586696)
and post-merge Functional CI
[41961587358](https://github.com/Juster06/micro-tools-hub/actions/runs/41961587358)
succeeded for that exact commit, including Required functional checks. Main had
no newer source changes at verification.

Fresh public HTTPS checks matched approved Git bytes for the homepage, all 56
tool pages, privacy notice, consent script and registry (60 responses), plus the
six directory-index canonical URLs. All 56 distinct visible homepage cards,
canonical routes, search/back navigation and the custom domain were verified.
The six Task 18 tools passed **49 fresh public Chromium interaction tests** with
synthetic inputs, including real image Blob MIME/pixel checks, CSV expansion
limits, and actual regex Worker timeout/cancellation/termination. Existing 50
releases were checked through fresh HTTP/source identity and post-merge CI;
fresh individual interactions for all 50 are not claimed.

Two fresh isolated browser profiles verified actual public consent behavior.
No Google requests occurred before choice, after rejection or after withdrawal.
Accepted homepage/title/regex navigations each sent exactly one real GA4 page
view for `G-XDHPQYJ5CH`, with HTTP 204; repeat acceptance did not duplicate it.
Three synthetic test page views were sent. GA4 property-level reporting remains
unverified. The shared analytics code, settings and privacy notice are unchanged.

See `audit/TASK_18_PUBLIC_RELEASE_VERIFICATION.json` and six separate
`*_RELEASE_VERIFICATION.json` records for timestamps, raw/normalized hashes,
deployed revision, browser scope and limitations. Prior development/release
audits are retained. Clipboard/download APIs were captured in memory; pixels and
output bytes used real browser codecs. No native-dialog, physical-device,
screen-reader or cross-browser certification is claimed. The optional
`/favicon.ico` returns 404 (eight recorded resource-console errors across seven
contexts); no uncaught application errors, essential asset failures or unexpected
dependencies occurred. This cosmetic icon issue is not changed in this task.

This branch proposes **93 registered, 56 RELEASED, 0 TESTED, 0 READY,
36 PLANNED, 1 BLOCKED**. Main/public registry metadata remain at 50 RELEASED and
6 TESTED until separately authorized integration. Six homepage labels are proposed
through the existing integration gate; all utility source files are unchanged.
The next planning checkpoint is 75 releases (56/75); the existing generated
milestone remains 100. Milestone configuration is unchanged.

Local Python **153/153** and Node **363/363** passed, plus **1252** inline
logic fixtures. All six canonical suites passed structural/logic/browser layers
(49 logic fixtures; 10 browser fixtures / 34 assertions). Project/source/registry
validation passed with zero errors and warnings. The full local catalog Chromium
run is still progressing at this checkpoint; no full local PASS is claimed.
The exact-head hosted PR gate must complete the full mapped Chromium, 56 browser
profiles and neutral templates. Actual hosted results are in the PR/final delivery.
See `audit/TASK_18_RELEASE_REGRESSION.json`. Existing assertions are retained,
with six-ID release counts and publication-aware checks replacing development-only
TESTED assumptions. No workflow/runtime/timeout or required-check relaxation.

**Next major task:** Owner review of the Task 18.1 release-verification PR and its
required checks. Await separate authorization before merge; then verify deployment
of the release metadata. No administrator bypass, deployment, new utility or
analytics/property setting change is authorized here. The two unrelated local
handoff edits are preserved. Earlier sections below are historical checkpoints.

<!-- TASK18:START -->
## Task 18 — development checkpoint

Task 17 is complete; consent-aware GA4 and the privacy notice are preserved.
Task 18 starts from `f35f07ee5da8c5c4efdf7d3f1ffeabe75571a16a` on
`feat/task-18-six-tools` in a separate worktree. Owner authorization covers
development, tests, commits and a PR; merge/deployment/bypass are not authorized.

Locally TESTED, publication pending: YouTube Title Checker, Instagram Bio Formatter, File Signature Inspector, Image Format Converter, CSV ↔ JSON Converter, Regex Tester.
Inventory: 93 registered, 50 RELEASED, 6 TESTED, 0 READY,
36 PLANNED, 1 BLOCKED. The 75-release planning checkpoint and
existing 100-release generated target are unchanged. See
`audit/TASK_18_DEVELOPMENT_PLAN.md`, individual READMEs, tests and source-bound
verification audits for features, resource limits, actual test scope and omissions.
Local validation: **151/151 Python tests**, **363/363 Node tests** plus
**1252** inline logic fixtures; six new tools pass all canonical layers
(49 logic fixtures; 10 real Chromium fixtures / 34 assertions). Their independent
focused Chromium suites pass 42 tests plus 12 homepage navigation tests. The
20-test consent suite includes all six new pages; Google endpoints are mocked,
with no measurement sent. Nine final preservation/historical-consent checks pass.
Project status and source-bound audits pass with zero errors/warnings.

The initial full local Chromium process reached 351 tests before its existing
900-second deadline; that run is TIMEOUT, not PASS. A partition retry was stopped
after observing Windows memory pressure (under 1 GiB free). Existing assertions,
CI deadlines, runtime pins and gates remain unchanged. The full mapped Chromium,
56 browser profiles and neutral templates require genuine hosted PR checks.
See `audit/TASK_18_DEVELOPMENT_VERIFICATION.json` and the final PR delivery.

Published source checkpoint trees were compared exactly with local source trees.
Audits reference the matching GitHub commits and retain original local revisions.
Local development commits are preserved before aligning this feature branch to
the GitHub-published history. All six tools remain TESTED, publication pending.

**Next major task:** Review the Task 18 PR and its required checks.
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

## Historical checkpoint — Task 10 (2026-11-03)

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

The owner authorized this bounded six-tool batch and its PR. Earlier Task 4 setup instructions below are historical; the latest handoff governs resumption.

Owner review of the Task 10 PR, followed only on explicit approval by ordinary
integration and independent deployment/public-source/behavior verification.
Submit eventual release evidence through another ordinary protected-main PR.
Then review readiness of the 68 PLANNED entries; no READY tools remain. Releasing
these six would produce 24 released tools, so one additional reviewed distinct
tool is still needed for the first milestone. Do not begin another utility now.

## Task 4 infrastructure checkpoint (2026-11-01)

The reusable development framework is implemented locally on `feat/reusable-tool-framework`, based on synchronized Task 3 main `73f5eea1c4d3b67490894cc2fe2855b9bc6c46d4`. Contract, standalone templates, safe staged generation, gated homepage proposals, actual logic/browser testing and ordered batch planning are documented in `TOOL_DEVELOPMENT_GUIDE.md`. Registry lifecycle remains manual and evidence-based; no public utility was added and growth targets are unchanged.

Next major task: **Task 5 — First End-to-End Tool Implementation**, recommended candidate Case Converter. Await that scope; Task 4's dry run and neutral template fixtures do not implement it. Publishing or merging Task 4 requires separate authorization.

This document is authoritative for project vision and scope. Source code is authoritative for implemented behavior; `TOOL_REGISTRY.json` is authoritative for inventory/status; `SESSION_HANDOFF.md` records the last session.

## Vision

Develop Everyday Digital Box / WebUtils Hub into a broad, reliable collection of free browser utilities. Help people finish practical tasks with clear controls, quick feedback, and no mandatory registration wherever practical. Keep <https://everydaydigitalbox.com/> and <https://github.com/Juster06/micro-tools-hub> public while limiting editing to authorized accounts.

Growth milestones are 25, 50, 100, 200, 300, 500, and 1,000+ released utilities. They are optional long-term targets, not delivery commitments. Count unique task-oriented utilities, not output formats, tabs, embedded counters, or unfinished placeholder pages.

## Current priorities

1. Establish persistent instructions, an accurate source-backed inventory, and repeatable handoffs.
2. Preserve and periodically verify the existing tools.
3. Build one small, useful utility at a time using the prioritized roadmap.
4. Add complete homepage integration, accessibility, error handling, and dated verification for every new utility.
5. Address measured usability/performance problems as the catalog grows.

The initial management setup does not authorize a batch implementation of new tools. Once this setup is reviewed, Case Converter is the recommended next development task. See the generated sequence in `ROADMAP.md` for the next twenty distinct utilities.

## Milestones and expansion strategy

| Stage | Outcome | Gate before advancing |
| --- | --- | --- |
| Foundation | Instructions, inventory, evidence, roadmap, consistency checks | Management checks pass; review the handoff |
| First 25 | A useful, tested starter collection | Every released entry has implementation and publication evidence |
| 50–100 | Broader category coverage | Review discovery, duplication, dependency payloads, and navigation |
| 200–500 | Sustainable category growth | Measured need for shared assets/build tooling; preserve existing URLs |
| 1,000+ | Long-term catalog aspiration | Reassess usefulness and maintenance capacity before setting commitments |

The first twenty proposed implementations would bring the baseline collection to 24, so a further distinct tool is required for 25. Image Rotator is a suggested follow-up after reviewing those twenty deliveries. This is a planning observation, not a promise to implement them in one session.

Prioritize repeated practical tasks, small local algorithms, bounded scope, and clear acceptance tests. Introduce complex PDF, spreadsheet, and hostile-markup processing after selecting appropriate libraries and validating browser resource limits. Avoid “AI-powered” branding for deterministic rules or templates.

## Categories

The registry defines PDF; Image; Text and Writing; Excel and Data; Developer; Social Media; Calculators; Security and Privacy; File Conversion; Everyday Productivity; and Entertainment tools. New categories need a distinct user need and an inventory update. Organizing documents must use the same registry category IDs.

## Constraints and quality requirements

- Retain the static HTML/CSS/JavaScript architecture unless a justified change is approved.
- Keep tasks local to the browser wherever practical. Explain network requests, storage, unsupported formats, and limitations.
- No backend, database, paid API, account system, or major framework without a technical reason and owner approval.
- Review small-library licensing, maintenance, payload, provenance, and privacy before adoption. Prefer pinned/local assets for format libraries when practical; do not add an unreviewed script to every page.
- Preserve working URLs, `CNAME`, site verification, search, navigation, and existing functionality.
- Use mobile layouts, keyboard-accessible controls, visible focus, non-color-only feedback, reduced motion, and understandable errors.
- Use bounded input/file processing, accurate results, reversible edits where useful, and truthful clipboard/download feedback.
- Never embed secrets. Security-sensitive utilities require threat modeling, established APIs, and focused failure tests.
- Make file operations explicit: choose input, process locally, inspect output, download; do not transmit files or promise universal compatibility.
- Record facts, test scope, and publication checks. A smoke test is evidence of its stated cases, not an assurance of bug-free operation.

## Backlog policy

The owner's initial 97 proposed names are reconciled to canonical entries in `audit/BACKLOG_RECONCILIATION.md`. Existing word count, reading-time, and repeated-space features are mapped to their existing utilities. JPEG/PNG/WebP conversion, bidirectional CSV/JSON conversion, text/file SHA-256 hashing, and Markdown conversion/preview share canonical utilities.

Related but distinct tasks retain separate entries where their input, output, or workflow differs. For example, curated Stream Roulette is not a user-entered Decision Wheel; image compression is not image format conversion; guided formula generation is not formula structural analysis. Revisit boundaries before implementation if requirements converge.

`PLANNED` and `READY` are inventory states, not implementations. Dependency candidates and design gates must be resolved before claiming a feature works. PDF Compressor is explicitly blocked on a local feasibility experiment demonstrating useful size reduction with acceptable fidelity and memory use.

## Future features — deferred

- **Owner-directed infrastructure:** Task 3 extends the Windows launcher into an internal local Project Control Dashboard, separate from the public website. The next major task is **Task 4 — Reusable Tool Development Framework**, requiring its own scope; do not begin it during Task 3. Do not substitute the default next READY utility for this explicit priority. Internal administration features do not increase the public tool inventory.

- **SEO monitoring concept:** later, consider traffic metrics and configurable decline thresholds, an observation period of approximately 9–11 days, an SEO review recommendation, and an action/outcome record. This is a concept only. There is no approved analytics integration, scheduled task, observation threshold, or automatic settings change.
- **Advertising:** existing layout placeholders may remain. Real AdSense integration, consent handling, and monetization are not current development priorities and need authorization.
- **Discovery at scale:** category filters, better search, related-tool links, and pagination/virtualization should follow measured needs. Do not replace the homepage preemptively.
- **Styling delivery:** a compiled Tailwind stylesheet could reduce runtime/CDN dependency; evaluate later as a separate scoped change, preserving visual design.
- **Broader QA:** reusable browser tests, additional engines, screen-reader checks, and automated release verification can be introduced incrementally. At that earlier checkpoint, no CI pipeline was configured; functional CI is now active on protected main.

## Decisions requiring a future gate

No new owner decision blocks the first recommended browser-native utility. Owner approval is required before introducing the architectural/services/access changes listed above. Library selection, PDF compression feasibility, encryption design, financial/date assumptions, official-document photo requirements, and file-format support require explicit technical review; they are not implied approvals or guaranteed capabilities.
