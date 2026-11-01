# Progress tracker

Inventory source: `TOOL_REGISTRY.json`. Run `python scripts/project_status.py` for the full tracking workflow, or `python scripts/generate_progress.py` to refresh only registry-derived documents. Existing Node commands delegate to the same Python engine. Counts are not separate manually maintained totals. Original four-tool baseline audit: 2026-10-31. Case Converter live behavior/source verification: 2026-11-01; static tracking checks do not refresh either date.

## Inventory and current milestone

<!-- GENERATED:COUNTS:START -->
| Metric | Count |
| --- | ---: |
| Total registered utilities | 93 |
| IDEA | 0 |
| PLANNED | 68 |
| READY | 18 |
| IN_PROGRESS | 0 |
| BLOCKED | 1 |
| IMPLEMENTED | 0 |
| TESTED | 0 |
| RELEASED | 6 |
| DEPRECATED | 0 |
| Backlog subtotal (IDEA + PLANNED + READY + BLOCKED) | 87 |

Status rows partition the total. The backlog subtotal overlaps those status rows; do not add it again.

Current growth milestone: **25 released tools**. Progress: 6/25 (24.0%); remaining: 19.

### Tools by category

| Category | Count |
| --- | ---: |
| PDF Tools | 9 |
| Image Tools | 8 |
| Text and Writing Tools | 8 |
| Excel and Data Tools | 10 |
| Developer Tools | 9 |
| Social Media Tools | 11 |
| Calculators | 10 |
| Security and Privacy Tools | 9 |
| File Conversion Tools | 9 |
| Everyday Productivity Tools | 9 |
| Entertainment Tools | 1 |

### Tools by priority

| Priority | Count |
| --- | ---: |
| P1 | 20 |
| P2 | 71 |
| P3 | 2 |

Current registered tool task: **none**. Session infrastructure work is recorded in the manual handoff.

Next ready tool: **Text Sorter**.

### Recently verified tools (registry evidence dates)

| Tool | Status | Last verification |
| --- | --- | --- |
| Duplicate Line Remover | RELEASED | 2026-11-01 |
| Case Converter | RELEASED | 2026-11-01 |
| AI Text Footprint Cleanser | RELEASED | 2026-10-31 |
| Free Stream Roulette | RELEASED | 2026-10-31 |
| Social Media Character Counter & Live Previewer | RELEASED | 2026-10-31 |
| Excel Formula Sandbox & Analyzer | RELEASED | 2026-10-31 |
<!-- GENERATED:COUNTS:END -->

The backlog total includes READY and BLOCKED; those rows must not be added again. TESTED means publication has not yet been verified. RELEASED means the recorded implementation and scoped behavior matched the published page at the dated check, not that it has no limitations.

## Current development task

Task 6 Duplicate Line Remover is RELEASED after PR #10 integration, successful actual Pages publication, public browser checks and exact matching source on 2026-11-01. Only its lifecycle entry advanced; the five previous released source pages and CNAME are unchanged. Counts: 93 total, 6 RELEASED, 0 TESTED, 18 READY, 68 PLANNED, 1 BLOCKED; milestone 6/25 (24%). The separate release audit and latest handoff record actual deployment/test/shortcut results and limitations. Do not begin Task 7.

## Recently completed work

- Implemented Case Converter using the Task 4 scaffold, with source-matched local test evidence, 69 JSON logic cases plus counter/boundary tests, and real browser interaction/integration coverage. The local card is marked publication pending; no release was claimed.

- Added the development framework with explicit scaffold/nonfunctional gates, temporary-fixture tests and real Chromium regression profiles; see `TOOL_DEVELOPMENT_GUIDE.md` for commands and limitations.

- Extended the installed Windows launcher into a modular offline dashboard with seven screens, read-only registry exploration, documented development ordering, validation freshness/diagnostics, Git/documents, blockers and safe local Quick Actions. Shortcut targets remain unchanged; exact tests and GUI scope are in the latest handoff.

- Read the full README and all existing page sources; inspected repository structure, Git status, and recent history.
- Confirmed the existing homepage and each utility have matching live HTML and passed the recorded Edge smoke checks.
- Reconciled the owner's full initial proposed list, including merged scopes and existing-feature mappings.
- Added session instructions, authoritative plan, architecture, decision log, changelog, roadmap, and handoff.
- Added a dependency-free Node management checker, generated-document synchronization, and negative-case validator tests.
- Added the Python standard-library tracking engine, six command entry points, latest-only local JSON reports, generated Git handoff, and isolated unittest coverage. The Node API remains available as a compatibility bridge.
- Fixed the pre-existing CRLF generated-document comparison issue found in a fresh Windows checkout. No website source or tool statuses changed.

## Next recommended tasks

<!-- GENERATED:NEXT:START -->
3. **Text Sorter** — Sort text lines using explicit ordering rules.
4. **Slug Generator** — Create URL-friendly slugs from text with documented Unicode rules.
5. **Find and Replace** — Preview and apply literal text replacements safely.
6. **Text Reverser** — Reverse text by line, word, or grapheme unit.
7. **JSON Formatter** — Validate, pretty-print and compact JSON locally.
<!-- GENERATED:NEXT:END -->

Start only after reviewing/synchronizing the management branch. For each utility, finish planning, implementation, testing, homepage integration, and evidence before selecting the next item.

## Known constraints and blockers

- PDF Compressor needs a feasibility experiment; do not implement a misleading “compression” button that merely resaves files.
- Format parsers/encoders, EXIF processing, sandboxed markup, regex timeouts, and cryptography need design/dependency review.
- Existing social counts are code points, previews are approximate, and text cleanup is rule-based.
- No full Safari/Firefox, screen-reader, or penetration audit has been performed in this baseline.
- Repository hosting settings, collaborator lists, DNS administration, and account authentication were not changed or audited here.

## Continuity

Read `AGENTS.md` and `SESSION_HANDOFF.md` first. Files on an unmerged branch are persistent on that branch, but are not automatically available to sessions starting from `main`. No recurring automation or autonomous development schedule has been created.
