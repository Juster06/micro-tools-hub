# Project master plan

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
