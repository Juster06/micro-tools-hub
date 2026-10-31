# Automated project tracking

Use **Python 3.10+**, with its standard library only. These commands are development utilities, not a website build or backend. No credentials, network connection, third-party packages, analytics, scheduled task, or JavaScript execution is required.

## Complete workflow

From the repository root:

```powershell
python scripts/project_status.py
```

If Windows exposes Python through its launcher, use `py -3 scripts/project_status.py`. The scripts locate the default project root relative to themselves, so they also work when invoked from another current directory. For a different checkout:

```powershell
python scripts/project_status.py --root "C:\path with spaces\micro-tools-hub"
```

The command validates the registry, records initial consistency, verifies static HTML, refreshes generated progress/roadmap/reconciliation blocks, rechecks consistency, generates a handoff, and writes four latest JSON reports. Critical failures remain visible. Initial stale generated content that was repaired remains recorded under `details.initial_consistency`.

## Individual commands

| Command | Purpose |
| --- | --- |
| `python scripts/validate_registry.py` | JSON/schema, required fields, unique identities/paths, status/evidence consistency, categories, references, dependency cycles, expected implementations |
| `python scripts/check_project.py` | Read-only source/document/link/evidence consistency |
| `python scripts/verify_tools.py` | Static HTML structure, title, hub/homepage links, declared controls |
| `python scripts/generate_progress.py` | Refresh existing generated blocks using canonical registry data |
| `python scripts/generate_handoff.py` | Refresh only the handoff's STATUS block with local facts and current validation |
| `python scripts/project_status.py` | Run the full workflow |

Common flags: `--root PATH`, `--json` for machine-readable stdout, and `--no-report` to avoid JSON report files. `--no-report` does **not** disable document generation.

For a status snapshot without editing documentation:

```sh
python scripts/project_status.py --check-only
```

Combine `--check-only --no-report` for a fully read-only status command. Validators never modify website source, registry statuses, or manual notes; they may write their report unless `--no-report` is supplied. Exit codes are **0** for no critical errors (warnings allowed), **1** for validation failure, and **2** for invocation or I/O failure. Report status is PASS, WARN, or FAIL; these are check results, not new tool lifecycle statuses.

## Data and generated content

`TOOL_REGISTRY.json` remains the single inventory. Existing status definitions are unchanged. Status counts partition the total; the backlog subtotal includes IDEA, PLANNED, READY and BLOCKED and must not be added a second time. Category, priority, growth target, percentage, active tools, next ready tool, and dated recent verification all derive from it.

- Top-level `milestones` is an ascending list of growth targets. The next target is greater than the recorded RELEASED count; beyond the last target, the command says REQUIRES REVIEW.
- Existing free-text `dependencies` describe APIs/candidates, not installed packages. `tool:<id>` strings and optional `depends_on` lists declare actual tool references; missing IDs, self-references and cycles are errors. Next-tool selection skips unmet tool dependencies.
- Optional `expected_interface_ids` names static HTML controls to check. The current four utilities declare these controls. Missing declarations produce a warning; natural-language feature descriptions are not guessed into tests.
- Planned entries do not need source directories. IMPLEMENTED/TESTED/RELEASED entries do. An existing source page under a planned entry is a consistency error.
- TESTED/RELEASED still require appropriate behavior/evidence and publication rules. Structural verification never promotes a tool, refreshes a verification date, or proves a functional test passed.

Generated sections use `<!-- GENERATED:NAME:START -->` and `<!-- GENERATED:NAME:END -->`. Preserve exactly one ordered pair for each section. Generation preflights all affected documents and refuses missing/ambiguous markers. Manual content outside markers and existing LF/CRLF line endings are preserved; unchanged input produces byte-identical progress output. The existing roadmap and backlog reconciliation blocks share the same engine.

Writes are atomic per file; there is no cross-process transaction lock. Run one writer per checkout. On an interrupted session, inspect actual source, reports and Git; there is no termination hook or automatic cleanup guarantee.

## Reports and Git snapshots

The ignored `reports/` directory contains only these latest snapshots:

```text
reports/
├── project-status.json
├── registry-validation.json
├── tool-verification.json
└── project-consistency.json
```

Reports contain schema version, UTC generation timestamp, check name, status, counts, errors, warnings, informational notes, and verification details. They are overwritten, not accumulated or committed. No report includes Git author/email, commit messages, credential-helper data, remotes, raw command stderr, or absolute project paths. Relative changed-file names can be present, which is another reason to keep these reports local.

Git is optional for tracking counts. If it is absent, fails, has no HEAD, or the project is a downloaded non-Git copy, Git values become UNKNOWN with a warning. A parent repository is not misreported as this project's repository. No remote fetch is performed, so push/deployment state remains UNKNOWN. No command commits, pushes, merges, deploys, or schedules itself.

Handoff generation records counts, active/next tool, recorded recent verification, blockers, current local checks, branch, observed HEAD, and uncommitted relative changes. It distinguishes recorded evidence from newly executed tests. It settles the snapshot after writing its own generated block; a subsequent commit changes HEAD, so a committed handoff cannot contain its own resulting SHA. Use `--check-only` after a commit for up-to-date local reports without dirtying the handoff again.

## Existing Node compatibility

The existing `node scripts/project.mjs check`, `sync`, `summary`, and exported validation/count functions remain available. They delegate to `tracking.py` through a UTF-8 JSON bridge rather than maintaining a second set of rules. Node 20+ is recommended for the compatibility test suite. If launcher discovery fails, set the task-specific `WEBUTILS_PYTHON` variable to the Python executable.

For backward compatibility, the Node summary's `planned` field retains its original backlog-subtotal meaning; Python reports distinguish `planned` (PLANNED only) from `backlog`. Both derive from the same status counts.

## Tests

```sh
python -m unittest discover -s tests -v
node --test scripts/project.test.mjs
git diff --check
```

Python tests use temporary project fixtures, never production documents. They cover malformed JSON/schema, duplicates, missing files, planned tools, references/cycles, links, marker safety, manual text, repeat generation, CRLF/UTF-8, Git absence/failure, reports, CLI exit codes, and a 1,500-tool dependency chain. Node tests check the preserved compatibility API.

## Limits

These are offline management/static checks. They do not run utility JavaScript, functional or browser tests, assess account security, prove accessibility, check third-party URLs, or verify current publication. Existing `audit/` reports are historical evidence; hashes detect source changes but do not constitute a new test run. Add appropriate functional tests and live checks before recording a new TESTED/RELEASED result. Markdown file links and static HTML links are checked where practical; dynamic targets and fragments may require manual review.
