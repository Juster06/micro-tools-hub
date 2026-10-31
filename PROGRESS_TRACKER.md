# Progress tracker

Inventory source: `TOOL_REGISTRY.json`. Run `python scripts/project_status.py` for the full tracking workflow, or `python scripts/generate_progress.py` to refresh only registry-derived documents. Existing Node commands delegate to the same Python engine. Counts are not separate manually maintained totals. Last functional/publication baseline audit: 2026-10-31; static tracking checks do not refresh it.

## Inventory and current milestone

<!-- GENERATED:COUNTS:START -->
| Metric | Count |
| --- | ---: |
| Total registered utilities | 93 |
| IDEA | 0 |
| PLANNED | 68 |
| READY | 20 |
| IN_PROGRESS | 0 |
| BLOCKED | 1 |
| IMPLEMENTED | 0 |
| TESTED | 0 |
| RELEASED | 4 |
| DEPRECATED | 0 |
| Backlog subtotal (IDEA + PLANNED + READY + BLOCKED) | 89 |

Status rows partition the total. The backlog subtotal overlaps those status rows; do not add it again.

Current growth milestone: **25 released tools**. Progress: 4/25 (16.0%); remaining: 21.

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

Next ready tool: **Case Converter**.

### Recently verified tools (registry evidence dates)

| Tool | Status | Last verification |
| --- | --- | --- |
| AI Text Footprint Cleanser | RELEASED | 2026-10-31 |
| Free Stream Roulette | RELEASED | 2026-10-31 |
| Social Media Character Counter & Live Previewer | RELEASED | 2026-10-31 |
| Excel Formula Sandbox & Analyzer | RELEASED | 2026-10-31 |
<!-- GENERATED:COUNTS:END -->

The backlog total includes READY and BLOCKED; those rows must not be added again. TESTED means publication has not yet been verified. RELEASED means the recorded implementation and scoped behavior matched the published page at the dated check, not that it has no limitations.

## Current development task

Task 2 extends the existing project-memory foundation with automated validation, static verification, generated reports, and checkpoints. No new utility implementation started in this session. Git delivery and review state are recorded in `SESSION_HANDOFF.md`; this tracker does not independently assert deployment.

## Recently completed work

- Read the full README and all existing page sources; inspected repository structure, Git status, and recent history.
- Confirmed the existing homepage and each utility have matching live HTML and passed the recorded Edge smoke checks.
- Reconciled the owner's full initial proposed list, including merged scopes and existing-feature mappings.
- Added session instructions, authoritative plan, architecture, decision log, changelog, roadmap, and handoff.
- Added a dependency-free Node management checker, generated-document synchronization, and negative-case validator tests.
- Added the Python standard-library tracking engine, six command entry points, latest-only local JSON reports, generated Git handoff, and isolated unittest coverage. The Node API remains available as a compatibility bridge.
- Fixed the pre-existing CRLF generated-document comparison issue found in a fresh Windows checkout. No website source or tool statuses changed.

## Next recommended tasks

<!-- GENERATED:NEXT:START -->
1. **Case Converter** — Convert text case with an explicit choice of transformation.
2. **Duplicate Line Remover** — Remove repeated lines with controllable matching rules.
3. **Text Sorter** — Sort text lines using explicit ordering rules.
4. **Slug Generator** — Create URL-friendly slugs from text with documented Unicode rules.
5. **Find and Replace** — Preview and apply literal text replacements safely.
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
