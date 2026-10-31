# Project master plan

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

- **Owner-directed Task 3:** the next major development task is an internal visual Project Control Dashboard, separate from the public website. Task 2.5 provides only a Windows status launcher and extension points for opening that dashboard. Do not implement Task 3 until it is separately requested/scoped, and do not automatically substitute the default next utility for this owner-directed priority. Internal administration features do not increase the public tool inventory.

- **SEO monitoring concept:** later, consider traffic metrics and configurable decline thresholds, an observation period of approximately 9–11 days, an SEO review recommendation, and an action/outcome record. This is a concept only. There is no approved analytics integration, scheduled task, observation threshold, or automatic settings change.
- **Advertising:** existing layout placeholders may remain. Real AdSense integration, consent handling, and monetization are not current development priorities and need authorization.
- **Discovery at scale:** category filters, better search, related-tool links, and pagination/virtualization should follow measured needs. Do not replace the homepage preemptively.
- **Styling delivery:** a compiled Tailwind stylesheet could reduce runtime/CDN dependency; evaluate later as a separate scoped change, preserving visual design.
- **Broader QA:** reusable browser tests, additional engines, screen-reader checks, and automated release verification can be introduced incrementally. No CI pipeline is currently configured by this setup.

## Decisions requiring a future gate

No new owner decision blocks the first recommended browser-native utility. Owner approval is required before introducing the architectural/services/access changes listed above. Library selection, PDF compression feasibility, encryption design, financial/date assumptions, official-document photo requirements, and file-format support require explicit technical review; they are not implied approvals or guaranteed capabilities.
