# Progress tracker

Inventory source: `TOOL_REGISTRY.json`. Generated blocks are updated by `node scripts/project.mjs sync` and checked by `node scripts/project.mjs check`. Counts are not separate manually maintained totals. Last baseline audit: 2026-10-31.

## Inventory and current milestone

<!-- GENERATED:COUNTS:START -->
| Metric | Count |
| --- | ---: |
| Total registered utilities | 93 |
| Released (dated smoke and publication evidence) | 4 |
| Implemented but unverified | 0 |
| Tested, publication unverified | 0 |
| In development | 0 |
| Backlog (IDEA + PLANNED + READY + BLOCKED) | 89 |
| Ready to start (subset of backlog) | 20 |
| Blocked (subset of backlog) | 1 |

Status breakdown: IDEA: 0; PLANNED: 68; READY: 20; IN_PROGRESS: 0; BLOCKED: 1; IMPLEMENTED: 0; TESTED: 0; RELEASED: 4; DEPRECATED: 0.

Current growth milestone: **25 released tools** (4/25). Growth targets are not delivery promises.

Current implementation task: **none**. Resolve unfinished work and review the handoff before beginning another utility.

Next ready tool: **Case Converter** (case-converter).
<!-- GENERATED:COUNTS:END -->

The backlog total includes READY and BLOCKED; those rows must not be added again. TESTED means publication has not yet been verified. RELEASED means the recorded implementation and scoped behavior matched the published page at the dated check, not that it has no limitations.

## Current development task

Persistent project-memory foundation: source audit, registry reconciliation, documentation, validator, and handoff. No new utility implementation started in this session. Git delivery and review state are recorded in `SESSION_HANDOFF.md`; this tracker does not independently assert deployment.

## Recently completed work

- Read the full README and all existing page sources; inspected repository structure, Git status, and recent history.
- Confirmed the existing homepage and each utility have matching live HTML and passed the recorded Edge smoke checks.
- Reconciled the owner's full initial proposed list, including merged scopes and existing-feature mappings.
- Added session instructions, authoritative plan, architecture, decision log, changelog, roadmap, and handoff.
- Added a dependency-free Node management checker, generated-document synchronization, and negative-case validator tests.

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
