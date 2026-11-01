# Task 7 — controlled local three-tool batch

Base: clean `main` / fetched `origin/main` at `5d331d671df4f9f17647f9adad3c8ac9debd19ef`. Branch: `feat/task-7-three-tool-batch`. Owner authorizes local implementation and commits only; no push, PR, merge, deployment or RELEASED transition.

## Selection

The actual planner (`python scripts/plan_tool_batch.py --count 3`) selected these existing READY entries in sequence. Word Frequency Counter and Whitespace Cleaner are not registered entries; no new IDs or priorities are introduced. The existing reconciliation maps extra-space cleanup to Social Counter. This batch uses the permitted next eligible candidates.

| ID / route | Name | Category | Priority / rank | Dependencies | Start |
| --- | --- | --- | --- | --- | --- |
| text-sorter / text-sorter/index.html | Text Sorter | text | P1 / 3 | Existing Tailwind Play CDN v4; no unmet tool prerequisites | READY |
| slug-generator / slug-generator/index.html | Slug Generator | text | P1 / 4 | Existing Tailwind Play CDN v4; no unmet tool prerequisites | READY |
| find-and-replace / find-and-replace/index.html | Find and Replace | text | P1 / 5 | Existing Tailwind Play CDN v4; no unmet tool prerequisites | READY |

All three canonical routes were absent. Planner and all three generator dry runs were inspected before generation. Each generated six-file bundle stays ignored under development/scaffolds. Use the text template's standalone structure, expanded inline fallback styling, metadata and deterministic adapter; implement tool-specific UI and behavior without changing shared templates/framework.

## Acceptance and semantics

- Text Sorter: stable UTF-16 lexical ascending/descending and strict finite decimal numeric ascending/descending. Native lowercase comparison by default, optional case sensitivity and comparison trimming; original retained spelling/spacing preserved. Keep duplicates. Optional blank-line removal using trim. Invalid numeric lines remain last in original order in either direction and receive an explicit count/warning; never convert to zero. Equal keys preserve first-occurrence order. LF/CRLF/CR records, empty input zero records, trailing separator another record, LF output.
- Slug Generator: lowercase Unicode letter/number tokens with combining marks, joined by one hyphen. Default Unicode mode with NFD accent-mark removal; optional accent preservation using NFC. Optional ASCII mode retains a–z/0–9 only, without transliteration. Punctuation, whitespace, symbols and emoji separate tokens; no leading/trailing/doubled hyphens. Original input preserved. Document that a slug is not an availability/reserved-word/URL guarantee.
- Find and Replace: literal non-overlapping global replacement, case-sensitive by default, optional Unicode regex simple case-insensitive matching of an escaped literal. No regex entry or replacement-template syntax: dollar signs are literal. Nonempty search required, match count, preserved original, explicit Apply result and one-level Undo. Manual input changes discard undo. Preserve all line endings in pure logic; browser textareas normalize line endings. Search/replacement bounded at 10,000 UTF-16 units; output bounded at 1,000,000 before joining, with explicit failure and no truncation.
- Each: 100,000 UTF-16 input units, no maxlength truncation; live preview with immediate stale-result/action/count invalidation, composition guards, revision-guarded copy, UTF-8 download with URL cleanup, Clear restores defaults/focus. Safe text-only DOM, no input persistence/transports. Existing CDN styling request plus inline fallback; no runtime dependency added.

## Files, tests and integration

Each page has its own index.html, README, tests/tools/ID manifest, exact JSON logic/browser cases, additional Node logic/browser suites and scoped audit. Commit each source/test checkpoint before recording its revision. Advance independently READY → IMPLEMENTED → TESTED only after actual passing evidence. Keep publication null.

Run staging/canonical framework tests and independent Node tests, including invalid settings, exact Unicode/line/count cases, limits, stale async behavior, transport/storage probes, keyboard, and widths 320/375/768/1440. Review actual screenshots with CDN blocked. Use sequential browser-heavy suites. Keep existing tests/assertions intact.

After fresh canonical evidence, use integrate_tool.py for each card; review/check/apply each patch sequentially against the evolving hub, then confirm idempotence and actual search/back navigation. New cards must say Tested · publication pending. Preserve existing six card blocks exactly. Expected local inventory: 93 total, 6 RELEASED, 3 TESTED, 15 READY, 68 PLANNED, 1 BLOCKED; released milestone stays 24%.

Full final Python/Node suites, all six released-page regressions, neutral templates, registry/source/consistency checks and project status must pass. Preserve CNAME, released source/evidence, all unrelated registry entries, framework, dashboard/launcher and shortcut definitions. Verify actual existing shortcut launch and native counts where practical. Reports/screenshots/scaffolds/settings stay ignored or outside the repository. Review privacy/artifacts/whitespace, commit integration/documentation locally, and finish with clean feature branch. No further utility is authorized.

Potential conflicts: all three cards share the homepage, so proposals apply sequentially; evidence hashes bind each tool's metadata/source/tests and must be rerun after metadata changes. Active dashboard refresh and CLI writers must not overlap. Performance checks are bounded host fixtures, not invented timing guarantees.
