# Utility contract

This contract applies to new Everyday Digital Box utilities. `TOOL_REGISTRY.json` remains the source of truth for identity, scope, dependencies and lifecycle. See [the development guide](TOOL_DEVELOPMENT_GUIDE.md) for commands. A template, successful page load or structural PASS is not a working utility.

## Mandatory requirements for new utilities

| Area | Required behavior |
| --- | --- |
| Identity | Use an existing unique registry ID, name, description and category. Preserve its canonical `<directory_path>/index.html` route. Resolve overlapping features before adding an ID. |
| Document | Standalone HTML5, meaningful title/description, UTF-8, viewport, one main heading, logical landmarks and unique element IDs. Top-left Back to Hub must use `href="../index.html"`. |
| Implementation | Implement every agreed acceptance feature and mode. No placeholder success, fake output, silent truncation or unimplemented controls. Keep deterministic computation separate from DOM presentation where practical. |
| Input | Label controls, define types, defaults, Unicode semantics, empty/invalid/boundary behavior and measured size limits. Describe unsupported data. Do not execute input as code. |
| Output | Display untrusted text with `.value`/`.textContent`. Preserve meaningful whitespace; show actionable errors. Invalidate obsolete output when input/options change. Prevent late asynchronous results from replacing current results. |
| Actions | Clear/reset must clear result/error state and restore documented defaults/focus where applicable. Copy/download must reflect the current result and report failure truthfully. Release object URLs. |
| Accessibility | Native keyboard-operable controls, associated labels, visible focus, readable contrast, meaningful headings, status announcements and accessible errors. Do not rely solely on color. |
| Responsive UI | Usable narrow mobile and desktop layouts, readable text, no unintended horizontal scrolling, reduced-motion support where relevant. |
| Privacy | Process locally by default; no hidden input storage, telemetry, uploads, secrets, analytics or unnecessary external requests. Explain actual dependencies and any required network behavior. |
| Dependencies | No backend, database, paid API or frontend framework without scoped owner approval. Review libraries for license, size, version, privacy, offline behavior and maintenance. The existing Tailwind Play CDN remains an external styling request. |
| Evidence | Test actual behavior, interaction and integration; record precise scope and omissions. Never promote lifecycle automatically. Publication requires live matching-source evidence under the existing registry/audit rules. |

The base templates emit inline CSS/JS, Tailwind Play CDN, labeled input/mode/output, Run, Clear, Copy, Download, error/status messages and a privacy/limit notice. Shared fragments are expanded at generation time, so deployed pages need no development server, Python, Node or shared JavaScript runtime. Review the starting 100,000 UTF-16-code-unit limit for the actual operation; it is a guard, not a performance certification.

## Adapter and template conventions

For the supplied templates, retain `script#edb-tool-logic` with `window.EDB_TOOL = {isScaffold: boolean, allowEmpty: boolean, run(input, options) { ... }}`. The default `run` throws an explicit not-implemented error. Set `isScaffold:false` only after replacing that placeholder with real behavior. `options.mode` is the selected operation; add and test meaningful modes. The default UI accepts a string and renders a string or JSON-representable result.

The generic Node logic adapter supports deterministic synchronous functions with JSON-representable finite results; it supplies no DOM. Browser APIs, workers, asynchronous algorithms, randomness, timers and file pipelines require appropriately scoped browser cases or a reviewed specialist test adapter. Do not describe these as generic logic PASS when they were not executed. Node's VM executes trusted repository code for testing; it is not a sandbox for untrusted repositories.

Generated manifests identify the ID, canonical path and template, not lifecycle status. In staging, the manifest is at the bundle root; for canonical source, keep it under `tests/tools/<id>/manifest.json`. The generic structural adapter requires `toolInput`, `runBtn`, `clearBtn`, `toolOutput`, `copyBtn`, `downloadBtn`, `toolError`, `toolStatus`, description/viewport metadata and inline logic. The mode control, labels and keyboard semantics also require behavioral/manual review; a parser alone cannot establish accessibility.

## Recommendations and justified exceptions

Prefer small pure functions, concise useful descriptions, slate/indigo styling, examples, explicit operation descriptions, realistic performance measurements and offline fallback styling. Keep templates understandable rather than abstracting every variation.

Structured templates are starting points: calculators may replace the textarea with labeled numeric fields, format tools may add panes, and file tools may add drop/file controls and workers. For a different interface, document its contract and extend the structural/logic test adapter deliberately before claiming full coverage. Do not weaken generic gates to manufacture PASS. Security-sensitive randomness needs browser cryptography; hostile formats/previews and compression need explicit design and feasibility review.

Existing released pages keep their own IDs/layouts and manually maintained homepage copy. Without a framework manifest, the runner applies the existing registry interface contract, reports a legacy warning and leaves unavailable isolated logic testing as NOT RUN. This exception prevents a forced retrofit; browser smoke tests do not establish exhaustive compatibility or fresh publication evidence.

## Quality gates and lifecycle

| Gate | Evidence | Lifecycle effect |
| --- | --- | --- |
| Scaffold | Valid registry lookup; safe ignored development bundle; placeholder explicitly labeled | None; READY stays READY |
| Implementation | Required behavior exists, placeholder replaced, limits/errors documented, source reviewed | Manually choose IN_PROGRESS/IMPLEMENTED under existing rules; do not present an unfinished public page |
| Automated testing | Nonempty actual logic and browser suites plus structural/integration checks; current source/test/metadata/runner hashes | No automatic promotion. A full framework PASS requires all three layers and `isScaffold:false` |
| Manual verification | Required browser/keyboard/layout/privacy review, dated scope, matching source hash and valid source revision in audit evidence | Manually record TESTED only when the existing registry validation requirements are satisfied |
| Integration | Gated homepage patch reviewed/applied separately; unique route/card/count, existing descriptions preserved; complete project validation | No automatic lifecycle change or publication claim |
| Publication | Owner-authorized delivery and actual live matching-source verification with dated audit evidence | Manually record RELEASED; a local commit or HTTP 200 is insufficient |

IDEA, PLANNED, READY, IN_PROGRESS, BLOCKED, IMPLEMENTED, TESTED, RELEASED and DEPRECATED remain the only lifecycle statuses. PASS, PARTIAL, FAIL, NOT RUN, UNKNOWN and STALE in tool test reports describe check scope, never new lifecycle states. The homepage preview requires TESTED/RELEASED, canonical structural PASS, fresh (at most 24 hours) nonempty logic/browser PASS, matching verification hash and existing project/audit checks. Existing legacy cards return NO_CHANGE, without retroactive reformatting or a new verification claim.
