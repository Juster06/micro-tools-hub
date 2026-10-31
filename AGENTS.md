# Everyday Digital Box — instructions for development agents

## Identity and purpose

Everyday Digital Box is the public website at <https://everydaydigitalbox.com/>, branded WebUtils Hub. Repository: <https://github.com/Juster06/micro-tools-hub>. Build useful free utilities; prioritize reliable tool development over marketing. Growth targets are aspirations, not deadlines or permission for unattended work.

These instructions apply to this repository and its descendants. Read them at the start of every session. They do not create a recurring task or cause an agent to run when no session is active. Continuity depends on reading the saved files in the checked-out branch.

## Session startup

1. Read this file, `SESSION_HANDOFF.md`, `PROJECT_MASTER_PLAN.md`, `PROGRESS_TRACKER.md`, `ROADMAP.md`, and `TOOL_REGISTRY.json`.
2. Read the complete `README.md` on first contact or when it changes. Read `ARCHITECTURE.md` and relevant `DECISIONS.md` entries before changing behavior.
3. Inspect `git status --short --branch`, remotes, branch, and recent commits. Fetch remote state when available. Do not overwrite unrelated work or assume a downloaded ZIP is a Git clone.
4. Read relevant source and tests. Actual source determines what is implemented; investigate disagreement with documents before proceeding.
5. Run `python scripts/project_status.py`. It validates first, refreshes marked progress/roadmap/handoff blocks, and saves ignored local reports. Inspect Git status again after generation. Review failures and unfinished work before selecting unrelated work. Use `--check-only` for a snapshot without documentation updates.
6. Confirm the active branch contains the latest handoff. Unmerged branch documentation is not automatically present in `main` or another machine.

## Choosing work and avoiding duplicates

### Local Project Control Dashboard

Task 3 extends the installed Windows launcher; read `scripts/DASHBOARD.md` for its module boundaries and report freshness contract. Preserve `scripts/status_launcher.pyw`, shortcut targets and AppUserModelID. Keep registry exploration read-only, background work outside Tk, and widget updates on the main thread. Read the latest manual `**Next major task:**` handoff field before selecting a READY utility. Task 4 requires separate scope and must not begin during Task 3.

Structural reports are not functional test totals. Missing test-run reports display unavailable; never reuse historical handoff counts as current results. Input/report hashes and host-specific Git settings remain ignored in `reports/`. The dashboard lock coordinates dashboard refreshes only; avoid concurrent independent CLI writers. For dashboard changes, run Python/Node suites and project status, use temporary corrupt/slow/large fixtures, and record actual Windows GUI scope without inventing results.

- Follow the latest explicit user instruction. Otherwise resolve the handoff's unfinished task, then select the lowest available `sequence_rank` in the registry that is `READY` and has no unmet prerequisite.
- Check IDs, names, descriptions, `related_tools`, proposal resolutions, existing pages, and homepage search before creating a tool. Search code for the actual capability, not just a matching page title.
- Prefer enhancing a canonical tool or adding a mode when the same primary task already exists. Record a reason before splitting a shared interface.
- Treat the initial backlog as proposals with scoped acceptance features. `READY` does not mean implemented. Never invent a page, test result, publication, or completion date.
- Work on one bounded utility at a time. Milestone targets do not authorize building hundreds of pages at once.
- For a new tool, define acceptance behavior, dependencies, size limits, error cases, and test scope before writing its implementation.

## Technology and repository conventions

- Prefer static HTML, small inline CSS, vanilla browser JavaScript, and the existing Tailwind Play CDN setup. Keep each tool at `<slug>/index.html`; the root `index.html` is the hub.
- No backend, database, paid API, account system, or major framework without a clear technical reason and owner approval. Small maintained libraries may be used after documenting license, payload, offline behavior, versioning, and privacy implications.
- A dependency mentioned as a candidate in the registry is not installed or approved by that mention. Evaluate it before use. Tooling-only Python scripts and the Node compatibility commands do not introduce a website runtime or build requirement.
- Preserve all working pages, the `CNAME`, and the Google site-verification tag. Preserve the public website/code and restrict changes to authorized accounts; do not change visibility or access settings without a specific instruction.
- Use lowercase hyphenated directory names and stable unique IDs. Do not recycle an old ID for a different task.
- Match slate/indigo styling, responsive spacing, clear labels, visible focus states, keyboard controls, reduced motion, and readable errors. Every utility needs a top-left `href="../index.html"` Back to Hub link.
- Integrate a completed utility with a unique homepage card and searchable `data-title`. Update the initial homepage count, README, registry, and roadmap as needed.
- Keep source and documentation UTF-8. Keep credentials and machine-specific paths out of committed files. Do not commit generated screenshots, personal input, caches, or dependency directories.

## Coding and privacy standards

- Use descriptive names and small functions. Validate input and explain errors. Do not silently truncate, discard data, or report a failed copy/download as successful.
- Display user input as text. Do not use `eval`, execute supplied formulas, or inject untrusted HTML. Markup previews require a reviewed sandbox/sanitization design.
- Prefer local processing. No input uploads, tracking, analytics, real advertising, external SEO services, or automatic social posting without authorization. Existing ad containers remain placeholders.
- Do not add secret API keys to frontend code. Do not commit credentials or force-push history without authorization.
- Use browser cryptographic APIs for security-sensitive randomness. Do not substitute `Math.random` or invent encryption algorithms. Cryptography and hostile-format handling need a separate design review.
- Define realistic file and text limits based on measured memory and responsiveness. Revoke object URLs and release buffers. Explain unsupported/encrypted/corrupt input honestly.
- Local draft persistence must be explicit and documented; no silent storage of sensitive input. “Local processing” does not imply that hosting/CDN requests do not exist.

## Validation and status rules

- Run `python scripts/project_status.py`, `python -m unittest discover -s tests -v`, and `node --test scripts/project.test.mjs` for tracking-system changes; run `git diff --check` before committing. Python 3.10+ with its standard library is sufficient for the tracking workflow; Node is needed only for compatibility checks.
- For a utility change, test normal, empty, invalid, boundary, and representative large inputs; narrow mobile and desktop layouts; keyboard interaction; errors; copy/download behavior; safe rendering; and network behavior. Document browser/version, exact scope, results, and omissions.
- Use existing tests when applicable. Do not replace behavior validation with a JSON check. The management checker is not a security audit or full UI test suite.
- Update `audit/` evidence and source hashes when tested implementation changes. For additional test formats, extend the checker deliberately rather than weakening release gates.
- `IMPLEMENTED`: source exists, tests outstanding. `TESTED`: required scoped tests passed, publication unverified. `RELEASED`: behavior verified and live publication checked with dated matching-source evidence. A HTTP 200 alone is insufficient.
- Existing releases have a dated Edge smoke-test baseline, not exhaustive compatibility certification. Record regressions honestly; downgrade verification status when evidence no longer matches source.
- Planned entries have `last_verification_date: null` and no test/publication claim. Record blocked prerequisites in notes. Status definitions live in `TOOL_REGISTRY.json`.
- Update registry data first; run `python scripts/generate_progress.py` to derive progress counts, roadmap tables, and backlog mappings. The existing `node scripts/project.mjs sync` delegates to the same engine. Do not manually edit generated blocks or count merged features as separate tools.
- `depends_on` and dependency strings written as `tool:<id>` are checked tool references, including cycles. Other dependency strings remain descriptive candidates, not proof that a package exists. Optional `expected_interface_ids` declares static controls the verifier can reliably check.
- Static HTML verification never changes TESTED/RELEASED status or refreshes functional/publication dates. Reports are offline local snapshots, not functional test results. Keep `reports/` ignored; do not publish credentials, authors, remote URLs, or absolute local paths in reports.

## Branches, publication, and session shutdown

1. Use a feature branch for substantial changes. Review the diff and keep unrelated owner changes intact. Do not delete working tools without approval.
2. Run appropriate tests and record results and omissions. Reconcile registry, generated progress/roadmap, README, decisions, and changelog.
3. Update `SESSION_HANDOFF.md` with completed work, files changed, tests/results, known issues, unfinished work, exact next action, branch, and known commit references.
4. Run `python scripts/project_status.py` and review its consolidated errors/warnings, generated progress, and handoff. Update manual completion notes, blockers and changelog with actual evidence. Unexpected termination does not guarantee cleanup: the next session must recover from source, registry and Git.
5. Commit/push within the user's authorized scope. Verify the remote branch/commit before claiming a push. Opening a PR is not merging or deploying it; report pending review separately.
6. Inspect final Git status. State what remains uncommitted or unpublished. A handoff cannot embed its own commit hash; give the known baseline/checkpoint and the command/ref that identifies the containing delivery commit.
7. Save continuity files in the repository and synchronize explicitly requested local copies without overwriting unrelated edits. Do not promise automatic recall of uncommitted files from another checkout.

## Checkpoint after a utility

Run its relevant functional tests, inspect consistency issues, update the registry using the actual result, regenerate tracking information, update the changelog and manual handoff, and record the next task. Run the consistency checker again after integration. Resolve errors before moving on; structural checks alone cannot establish a release. Do not push or deploy without authorization. The status command itself performs neither action.

## Deferred scope

Record future traffic/SEO monitoring only in the master plan. Do not schedule it, add analytics, change SEO automatically, or integrate advertising now. A possible configurable review after a sustained decline over approximately 9–11 days remains an unapproved future concept.
