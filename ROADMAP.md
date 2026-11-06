# Development roadmap

## Task 20.1 — six-tool public release verification

PR #36 merged as `0b055d5b837ea0bca85f8b6583eec5607f93de95`.
[Pages42131624570](https://github.com/Juster06/micro-tools-hub/actions/runs/42131624570)
and [post-merge Functional CI42131632444](https://github.com/Juster06/micro-tools-hub/actions/runs/42131632444)
passed for that exact commit, including all four functional jobs (172 Python,
433 Node,593 Chromium). No newer main source was present at verification.

Fresh public HTTPS checks matched approved Git bytes for all68 tool pages,
homepage, privacy, consent, registry and bundled assets:78 source responses plus
six directory URLs. All68 distinct homepage cards were visible and linked to
the correct canonical routes. The six Task20 utilities passed45 fresh public
browser cases (38 scoped cases plus7 independent acceptance/navigation cases).
Native image bytes/MIME/pixels, independent ICO parsing and Windows loading,
all8 formula strings, exact emoji copying, strict JSON and print/PDF geometry
were checked. Existing62 tools were checked by fresh HTTP/source identity and
post-merge full CI; fresh individual interactions for all62 are not claimed.

Two isolated profiles verified real consent behavior without interception:
zero Google requests before choice/after rejection/after withdrawal, exactly
three accepted page views with HTTP204 and no duplicates. Measurement ID
G-XDHPQYJ5CH, shared consent code and privacy remain unchanged. GA4 property
reporting remains unverified. Clipboard/download APIs were captured in memory;
native dialogs, physical devices, screen readers and other browsers are excluded.

Print limitation: Resume Builder's static `15 mm` margin declaration is ignored
by CSS parsing; browser print defaults apply. A4 page geometry/controls passed;
no exact15mm margin or physical calibration claim is made. Optional favicon.ico
returns404; no uncaught application errors, essential asset failures or unexpected
dependencies occurred. No production tool or consent code was changed.

This branch proposes93 registered:68 RELEASED,0 TESTED,0 READY,24 PLANNED,
1 BLOCKED. All68 homepage routes/cards are retained; only the six reviewed gated
availability labels change from publication pending to Live. The deployed
registry at the audited main still has62RELEASED/6TESTED until this release PR
is separately authorized, merged and deployed. Next manual checkpoint75;
existing generated milestone100; configuration unchanged.

Evidence: `audit/TASK_20_PUBLIC_RELEASE_VERIFICATION.json` and six separate
`*_RELEASE_VERIFICATION.json` records contain actual timestamps, raw/normalized
source hashes, deployed revision, public interactions, consent and limitations.
All earlier audits, all68 runtime pages, assets, privacy and CNAME are preserved.
All20 pre-existing worktrees and their working changes, including two unrelated
dirty handoffs, remain preserved. Task20.1 uses a separate worktree and branch
`release/task-20-six-tools-verification`.

Fresh release-branch regression passed:175 Python,433 Node and593 Chromium tests;1,332 canonical logic fixtures, all68 structural profiles and six fresh all-layer canonical release gates. The complete hosted68-profile/template browser partition and required aggregate check remain mandatory on the exact PR head. See `audit/TASK_20_1_REGRESSION.json`; local standalone browser and hosted CI scopes are distinguished.

**Next major task:** Review the Task20.1 release-verification PR and exact-head
required checks. Full mapped regression results are recorded in the final PR
description and delivery report. Do not merge/deploy without explicit owner
authorization; do not use administrator bypass. PDF Compressor retains its
existing feasibility blocker. No further tool implementation is authorized here.

## Historical Task 20 development checkpoint — six utilities TESTED; publication pending

Task 19 is complete and publicly verified. PR #34 and PR #35 merged; approved
main baseline is `1ead1c37861b80c552446afbdb952c9248370bf9`. Pages
42032230127 and post-merge CI 42032231242 succeeded for that exact commit.
The existing 62 public tools remain the release baseline; dated public evidence
is retained in `audit/TASK_19_FINAL_PUBLIC_STATE.json`.

Task 20 implements Excel Formula Generator, Emoji Picker, Image Compressor,
PNG to ICO, Resume Builder and Passport Photo Layout Maker on
`feat/task-20-six-tools`. Source checkpoint:
`e2e7b5769c484d8f649dbd795aa364fe8229b423`. Per-tool development audits bind
to that actual Git source; the containing delivery commit is identified by the
feature branch and PR head, rather than embedding its own hash here.

Inventory: 93 registered, 62 RELEASED, 6 TESTED, 0 READY, 24 PLANNED, 1 BLOCKED.
The homepage has 68 cards; the six new cards say “Tested · publication pending”.
All six publication fields remain null. Next planning checkpoint: 75 released;
existing generated milestone: 100. Milestone configuration is unchanged.

Fresh local mapped regression passed: 172 Python and 433 Node tests;
1,332 canonical logic fixtures; all 68 structural/browser profiles;
493 browser fixtures with 1,398 assertions; both neutral templates (6 logic,
12 browser fixtures, 48 assertions). Focused source-checkpoint tests: 68/68.
Full local browser partitions hit the unchanged 900-second deadline: first
Chrome attempt also had three timing/protocol failures; isolated Edge passed
544 cases with no assertion failures before timing out. The interrupted file
and every remaining mapped file passed separately. Neither timeout is counted
as a full partition PASS. The complete 593-case pinned Linux Chromium partition
and all other exact-head hosted checks must pass on the development PR.
Consent regression: 32/32 with isolated synthetic Google endpoints, including
all six new tools. Existing production consent/privacy and measurement ID
G-XDHPQYJ5CH are unchanged. GA4 property reporting remains unverified.
See `audit/TASK_20_DEVELOPMENT_VERIFICATION.json` for actual local partition
summaries, source identity, specialist checks, limitations and test history.

Preserved all 62 released pages, old assets and historical audits. All 19
original worktrees retain their original HEAD and working changes, including
two unrelated uncommitted SESSION_HANDOFF.md edits. Task 20 uses its separate
worktree. No owner shortcuts/settings, workflow/runtime pins or deadlines changed.

**Next major task:** Review the Task 20 development PR and its exact-head required
checks. Wait for explicit owner authorization before merge/deployment. After an
authorized deployment, perform separate independent public source/functionality,
existing-tool and real consent verification before proposing RELEASED status.
No merge, deployment, public availability or Task 20 RELEASED claim is made.
Physical printer calibration, screen-reader/cross-browser/native-dialog testing
and GA4 property reporting remain outside the completed automated scope.

## Historical Task 19.1 — pre-merge verification checkpoint

PR #34 merged as `7ecbe37d15d51e3393c1d0f532fa4f2afd279f0b`. Pages
[42010602815](https://github.com/Juster06/micro-tools-hub/actions/runs/42010602815)
and post-merge Functional CI
[42010604196](https://github.com/Juster06/micro-tools-hub/actions/runs/42010604196)
succeeded for that exact commit, including Required functional checks. Main had
no newer source changes at verification.

Fresh public HTTPS checks matched approved Git bytes for the homepage, all 62
tool pages, privacy notice, consent script, registry, progress and bundled assets (71 responses), plus the
six directory-index canonical URLs. All 62 distinct visible homepage cards,
canonical routes and the custom domain were verified.
The six Task 19 tools passed **48 fresh public Chromium interaction tests** with
synthetic inputs, including real Web Crypto, rejection-boundary injection,
independent QR decoding, image Blob MIME/pixels and CSV bounds. Existing 56
releases were checked through fresh HTTP/source identity and post-merge CI;
fresh individual interactions for all 56 are not claimed.

Two fresh isolated browser profiles verified actual public consent behavior.
No Google requests occurred before choice, after rejection or after withdrawal.
Accepted homepage/QR/CSV-cleaner navigations each sent exactly one real GA4 page
view for `G-XDHPQYJ5CH`, with HTTP 204; repeat acceptance did not duplicate it.
Three synthetic test page views were sent. GA4 property-level reporting remains
unverified. The shared analytics code, settings and privacy notice are unchanged.

See `audit/TASK_19_PUBLIC_RELEASE_VERIFICATION.json` and six separate
`*_RELEASE_VERIFICATION.json` records for timestamps, raw/normalized hashes,
deployed revision, browser scope and limitations. Prior development/release
audits are retained. Clipboard/download APIs were captured in memory; pixels and
output bytes used real browser codecs. No native-dialog, physical-device,
screen-reader or cross-browser certification is claimed. The optional
`/favicon.ico` returns 404 (seven recorded resource-console errors across seven
contexts); no uncaught application errors, essential asset failures or unexpected
dependencies occurred. This cosmetic icon issue is not changed in this task.

This branch proposes **93 registered, 62 RELEASED, 0 TESTED, 0 READY,
30 PLANNED, 1 BLOCKED**. Main/public registry metadata remain at 56 RELEASED and
6 TESTED until separately authorized integration. Six homepage labels are proposed
through the existing integration gate; all utility source files are unchanged.
The next planning checkpoint is 75 releases (62/75); the existing generated
milestone remains 100. Milestone configuration is unchanged.

Local Python **163/163** and Node **403/403** passed, plus **1308** inline
logic fixtures. All six canonical suites passed structural/logic/browser layers
(56 logic fixtures; 11 browser fixtures / 41 assertions). Project/source/registry
validation passed with zero errors and warnings. The full local catalog Chromium
run is still progressing at this checkpoint; no full local PASS is claimed.
The exact-head hosted PR gate must complete the full mapped Chromium, 62 browser
profiles and neutral templates. Actual hosted results are in the PR/final delivery.
See `audit/TASK_19_RELEASE_REGRESSION.json`. Existing assertions are retained,
with six-ID release counts and source-bound publication checks. Historical
Task19 development evidence remains independently checked. No workflow/runtime/
timeout or required-check relaxation.

**Next major task:** Owner review of the Task 19.1 release-verification PR and its
required checks. Await separate authorization before merge; then verify deployment
of the release metadata. No administrator bypass, deployment, new utility or
analytics/property setting change is authorized here. The two unrelated local
handoff edits are preserved. Delivery branch: `release/task-19-six-tools-verification`. Identify its containing
commit with `git rev-parse HEAD`; the handoff cannot embed its own commit hash.
Earlier sections below are historical checkpoints.

## Historical Task 19 — development checkpoint before public release

Task 18 is complete, publicly verified and deployed. PR #32 and PR #33 are merged.
Approved main: `3178f70802a96f181fd82251d417abd1dd0ad76b`; Pages
[41979618835](https://github.com/Juster06/micro-tools-hub/actions/runs/41979618835)
and post-merge Functional CI
[41979619839](https://github.com/Juster06/micro-tools-hub/actions/runs/41979619839)
succeeded for that exact commit. Task 18.2's actual public source, seven smoke/
navigation tests and consent-network results are retained in
`audit/TASK_18_FINAL_PUBLIC_STATE.json`; earlier audits remain unchanged.
GA4 collection was verified; authenticated property-level reporting remains unverified.

Task 19 implements Password Generator, CSV to TXT, Passphrase Generator,
QR Code Generator, Image Cropper and CSV Data Cleaner on `feat/task-19-six-tools`.
All six are **TESTED / REQUIRED_PASSED**, with `publication: null`.
Inventory: **93 registered, 56 RELEASED, 6 TESTED, 0 READY, 30 PLANNED, 1 BLOCKED**.
The branch homepage has 62 canonical cards; six explicitly say
**Tested · publication pending**. The existing 56 pages, registry records,
homepage cards, historical audits, consent/privacy code, CNAME, templates,
workflow/runtime pins, dashboard/launchers and original 17 worktrees are preserved.

Source checkpoint: `6d162305c35a60da25bf2f22e14d901b8dc41801`. Its tree matches local source checkpoint
`c60edf469d4c8a7c9be378fdbf4666bf43069ffd` exactly. Six separate development
audits bind canonical source hashes to the published Git source checkpoint.
See `audit/TASK_19_DEVELOPMENT_PLAN.md`, `audit/TASK_19_DEPENDENCIES.json`,
`audit/TASK_19_DEVELOPMENT_VERIFICATION.json` and each tool README.

Local results: **161/161 Python**, **403/403 Node** plus **1,308** logic fixtures,
**537/537 pinned Chromium tests**, all **62** canonical browser profiles
(487 fixtures / 1372 assertions), and both neutral templates
(12 browser fixtures / 48 assertions).
The six new tools also passed **81** focused Node/Edge tests and all canonical
layers (56 logic fixtures; 11 browser fixtures / 41 assertions). Project validation
passed with zero errors/warnings. Initial browser preflight required explicit
EDB_TEST_BROWSER selection; the complete unchanged rerun passed. No failed scope
is hidden and no assertion/deadline was weakened. Vendored whitespace was normalized with original digests retained; all 10 QR
checks passed again. The wordlist pin check also validates exact committed bytes
and portable working text. Exact-head hosted PR checks
remain mandatory; their actual result is reported on the PR and final delivery.

Consent regression: **26/26** passed, including every new page before choice,
rejection, acceptance/reacceptance, navigation and withdrawal. Google endpoints
were intercepted; no real measurements were sent in Task 19. Shared consent and
measurement ID `G-XDHPQYJ5CH` are unchanged. Clipboard/download actions were
captured in memory; no native-dialog, physical-device, screen-reader or cross-engine
certification. Secret tools provide explicit copy, with no download/persistence.
CSV uploads retain quoted CRLF data until manual edits; automatic copy/export
uses the complete computed result despite textarea display normalization.

The next planning checkpoint remains **75 released tools** (19 remaining);
the existing generated milestone remains **100** (56/100, 44 remaining).
PDF Compressor remains blocked on local feasibility, fidelity and memory use.
Two unrelated uncommitted handoff edits remain intact. Historical administrator-
bypass use remains unverified.

**Next major task:** Review the Task 19 development PR and required exact-head CI.
Await explicit owner authorization before merge/deployment. After an approved
deployment, independently verify six public routes, source identity, functionality,
all prior tools and consent; only then propose a separate release-verification PR.
The containing delivery commit is resolved with `git log -1 --format="%H %s"`;
this document cannot contain its own future commit hash. No Task 20 is authorized.

## Historical Task 18.1 — pre-merge release-verification checkpoint

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
| image-compressor | Image Compressor | RELEASED | P2 | M | Browser image decoding and Canvas; format support and memory limits must be tested |
| image-resizer | Image Resizer | RELEASED | P2 | M | Browser image decoding and Canvas; format support and memory limits must be tested |
| image-format-converter | Image Format Converter | RELEASED | P2 | M | Browser image decoding and Canvas; format support and memory limits must be tested |
| image-cropper | Image Cropper | RELEASED | P2 | L | Browser image decoding and Canvas; format support and memory limits must be tested |
| image-rotator | Image Rotator | RELEASED | P2 | S | Browser image decoding and Canvas; format support and memory limits must be tested |
| image-watermark | Image Watermark | RELEASED | P2 | M | Browser image decoding and Canvas; format support and memory limits must be tested |
| image-color-picker | Image Color Picker | RELEASED | P2 | M | Browser image decoding and Canvas; format support and memory limits must be tested |
| passport-photo-layout-maker | Passport Photo Layout Maker | RELEASED | P2 | L | Browser image decoding and Canvas; format support and memory limits must be tested |

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
| csv-json-converter | CSV ↔ JSON Converter | RELEASED | P2 | L | CSV/workbook parsers where needed: evaluate correctness, license and bundle size |
| excel-to-csv | Excel to CSV | PLANNED | P2 | L | CSV/workbook parsers where needed: evaluate correctness, license and bundle size |
| csv-column-extractor | CSV Column Extractor | RELEASED | P2 | M | CSV/workbook parsers where needed: evaluate correctness, license and bundle size |
| duplicate-row-finder | Duplicate Row Finder | RELEASED | P2 | M | CSV/workbook parsers where needed: evaluate correctness, license and bundle size |
| csv-data-cleaner | CSV Data Cleaner | RELEASED | P2 | L | CSV/workbook parsers where needed: evaluate correctness, license and bundle size |
| csv-merger | CSV Merger | RELEASED | P2 | M | CSV/workbook parsers where needed: evaluate correctness, license and bundle size |
| json-formatter | JSON Formatter | RELEASED | P1 | S | Native JSON.parse and JSON.stringify |
| csv-viewer | CSV Viewer | RELEASED | P2 | M | CSV/workbook parsers where needed: evaluate correctness, license and bundle size |
| excel-formula-generator | Excel Formula Generator | RELEASED | P2 | L | Browser-native deterministic templates; no parser or AI service |

### Developer Tools

| Tool ID | Utility | Status | Priority | Complexity | Dependencies / gate |
| --- | --- | --- | --- | --- | --- |
| base64-encoder-decoder | Base64 Encoder and Decoder | RELEASED | P1 | S | Browser-native approach; scope review before implementation |
| url-encoder-decoder | URL Encoder and Decoder | RELEASED | P1 | S | Browser-native approach; scope review before implementation |
| uuid-generator | UUID Generator | RELEASED | P1 | S | Browser cryptographic randomness; feature-detect and fail clearly if unavailable |
| sha256-hash-checker | SHA-256 Text & File Hash Checker | RELEASED | P2 | M | Browser Web Crypto SHA-256; bounded file reads |
| regex-tester | Regex Tester | RELEASED | P2 | L | Browser Worker with termination timeout; bounded input |
| html-formatter | HTML Formatter | PLANNED | P2 | L | Reviewed non-executing HTML parser and whitespace-preservation policy |
| css-minifier | CSS Minifier | PLANNED | P2 | L | Reviewed CSS parser/minifier and license |
| javascript-minifier | JavaScript Minifier | PLANNED | P2 | L | Reviewed JavaScript parser/minifier and license; consider worker isolation |
| timestamp-converter | Timestamp Converter | RELEASED | P1 | S | Browser-native approach; scope review before implementation |

### Social Media Tools

| Tool ID | Utility | Status | Priority | Complexity | Dependencies / gate |
| --- | --- | --- | --- | --- | --- |
| social-counter | Social Media Character Counter & Live Previewer | RELEASED | P2 | M | Modern browser DOM APIs |
| hashtag-organizer | Hashtag Organizer | RELEASED | P1 | S | Browser-native approach; scope review before implementation |
| youtube-title-checker | YouTube Title Checker | RELEASED | P2 | S | Browser-native approach; scope review before implementation |
| youtube-description-formatter | YouTube Description Formatter | RELEASED | P2 | M | Browser-native approach; scope review before implementation |
| instagram-bio-formatter | Instagram Bio Formatter | RELEASED | P2 | M | Browser-native approach; scope review before implementation |
| social-media-line-break-tool | Social Media Line Break Tool | PLANNED | P2 | S | Browser-native approach; scope review before implementation |
| emoji-picker | Emoji Picker | RELEASED | P2 | M | Reviewed local emoji dataset and usage license |
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
| password-generator | Password Generator | RELEASED | P2 | M | Browser Web Crypto where cryptographic randomness or hashing is required |
| password-strength-checker | Password Strength Checker | PLANNED | P2 | L | Reviewed locally bundled password-strength estimator and license |
| secure-random-number-generator | Secure Random Number Generator | RELEASED | P1 | S | Browser cryptographic randomness; feature-detect and fail clearly if unavailable |
| local-text-encryption | Local Text Encryption | PLANNED | P3 | XL | Web Crypto authenticated encryption and password derivation; Separate reviewed threat model and versioned format |
| exif-metadata-viewer | EXIF Metadata Viewer | PLANNED | P2 | L | Reviewed format-specific metadata parser |
| exif-metadata-remover | EXIF Metadata Remover | PLANNED | P2 | L | Reviewed metadata parser/removal method and exported-metadata verifier |
| file-signature-inspector | File Signature Inspector | RELEASED | P2 | M | Browser Web Crypto where cryptographic randomness or hashing is required |
| passphrase-generator | Passphrase Generator | RELEASED | P2 | M | Reviewed licensed word list; Browser cryptographic randomness and unbiased selection |
| qr-code-generator | QR Code Generator | RELEASED | P2 | M | Reviewed locally bundled QR encoder and license |

### File Conversion Tools

| Tool ID | Utility | Status | Priority | Complexity | Dependencies / gate |
| --- | --- | --- | --- | --- | --- |
| txt-to-pdf | TXT to PDF | PLANNED | P2 | L | Reviewed PDF text rendering library and font licensing |
| markdown-converter-previewer | Markdown Converter & Previewer | PLANNED | P2 | L | Reviewed Markdown parser and sanitizer; local bundled assets preferred |
| html-to-markdown | HTML to Markdown | PLANNED | P2 | L | Reviewed non-executing HTML-to-Markdown conversion library |
| csv-to-txt | CSV to TXT | RELEASED | P2 | M | Format-specific parsers, sanitizers or encoders: evaluate before implementation |
| json-to-txt | JSON to TXT | RELEASED | P2 | M | Format-specific parsers, sanitizers or encoders: evaluate before implementation |
| svg-to-png | SVG to PNG | PLANNED | P2 | L | Reviewed SVG sanitization and external-resource blocking; Canvas rasterization with tested dimension limits |
| png-to-ico | PNG to ICO | RELEASED | P2 | L | Reviewed local ICO encoder |
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
| resume-builder | Resume Builder | RELEASED | P2 | L | Browser-native approach; scope review before implementation |
| meeting-agenda-generator | Meeting Agenda Generator | RELEASED | P2 | M | Browser-native approach; scope review before implementation |
| printable-calendar-generator | Printable Calendar Generator | RELEASED | P2 | M | Browser-native approach; scope review before implementation |

### Entertainment Tools

| Tool ID | Utility | Status | Priority | Complexity | Dependencies / gate |
| --- | --- | --- | --- | --- | --- |
| streaming-roulette | Free Stream Roulette | RELEASED | P2 | S | Modern browser DOM APIs |
<!-- GENERATED:CATALOG:END -->

## Deferred product work

SEO monitoring, advertising, analytics, paid services, accounts, and a backend are not part of this delivery sequence. The future 9–11-day SEO observation concept is recorded in `PROJECT_MASTER_PLAN.md` without an automation or implementation.
