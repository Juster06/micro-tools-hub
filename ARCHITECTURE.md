# Architecture

Verified baseline: 2026-10-31, source revision `1cf6a8ae0973918c95b6bf4a56b0a9708ace35f0`. Evidence: `audit/BASELINE_VERIFICATION.json`. This management change leaves the runtime HTML pages and domain configuration unchanged.

## Runtime structure

The site is static HTML. The root `index.html` contains the dashboard, four tool cards at the baseline, and a title-based search filter. Each tool is a standalone `<directory>/index.html` with inline vanilla JavaScript and a small inline stylesheet. There is no server API, database, package-based runtime, application build, service worker, or account system in the repository.

The browser loads Tailwind CSS v4 using `https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4`. This is an external runtime dependency for styling; it is not a fully offline bundle and is not pinned to an exact patch version. Tailwind Play CDN is the existing design choice, not a guarantee of production optimization. All existing tools otherwise use browser APIs and inline assets.

## Repository layout and responsibilities

```text
index.html                      dashboard and static initial count
CNAME                           existing custom domain
<tool-slug>/index.html           each implemented utility
README.md                       user/developer orientation
AGENTS.md                       permanent session instructions
PROJECT_MASTER_PLAN.md          vision and scope
TOOL_REGISTRY.json              canonical inventory, status, features and evidence
PROGRESS_TRACKER.md              generated counts plus current narrative
ROADMAP.md                      generated catalog/sequence plus delivery strategy
ARCHITECTURE.md                  verified design and constraints
DECISIONS.md                     dated significant choices
CHANGELOG.md                     meaningful change history
SESSION_HANDOFF.md               exact continuation instructions and Git context
scripts/project.mjs             check / sync / summary, Node built-ins only
scripts/project.test.mjs         management validator regression cases
scripts/tracking.py             shared offline standard-library tracking engine
scripts/validate_registry.py     registry validation entry point
scripts/generate_progress.py     marked-document generation entry point
scripts/check_project.py         consistency check entry point
scripts/verify_tools.py          static structure verification entry point
scripts/generate_handoff.py      generated local Git/session snapshot
scripts/project_status.py        complete tracking workflow
tests/test_tracking.py           isolated Python unittest fixtures
reports/                        ignored, latest-only local JSON snapshots
scripts/status_launcher.pyw      Windows no-console GUI entry point
scripts/status_launcher.py       Tk view and background subprocess controller
scripts/install_status_shortcut.py current-user shortcut installer/verifier
scripts/windows_shortcuts.py     ctypes Windows Shell adapter
tests/test_status_launcher.py    isolated launcher and native shortcut tests
audit/                          dated baseline and initial backlog reconciliation
```

Management scripts are developer tools. They do not load in the website, add telemetry, or become a deployment build requirement. Python 3.10+ and its standard library run the complete workflow without dependencies. The existing Node exports/commands delegate to Python via a UTF-8 JSON bridge; they share the same validation, counts and generation logic. Node 20+ remains useful for compatibility tests.

## Automated tracking workflow

Run `python scripts/project_status.py` from the repository root. Entry points resolve their default root from their own script location; `--root` accepts a Windows or other project path, including spaces. The workflow validates the registry, checks consistency, verifies static tool structure, refreshes only existing generated blocks, rechecks consistency, generates a handoff, and saves four fixed latest reports. It records the initial consistency result too, so repaired generated drift is not concealed.

The registry retains its existing statuses and descriptive dependencies. Optional `depends_on` and `tool:<id>` dependencies encode resolvable tool references; cycle checks use an iterative graph algorithm. Optional `expected_interface_ids` declares static controls, and top-level `milestones` defines growth targets. None of these metadata additions changes a tool status or functional evidence date.

Progress status rows partition the inventory; the separate backlog subtotal overlaps IDEA/PLANNED/READY/BLOCKED. Category, priority, next-milestone percentage and recent evidence dates derive from the same registry. Generated progress has no run timestamp, so unchanged inputs produce identical content. Existing roadmap and reconciliation markers are also refreshed; manual text outside markers and LF/CRLF style are preserved.

Static verification parses HTML without executing JavaScript: required files, basic HTML5 tags, title, hub/homepage links, duplicate IDs, and declared controls. Source/evidence hashes remain checked separately. No command automatically promotes TESTED/RELEASED, runs functional tests, contacts the live site, commits, pushes, or deploys.

`reports/` contains `registry-validation.json`, `project-consistency.json`, `tool-verification.json`, and `project-status.json`. Each uses a timestamped schema with status, counts, errors, warnings and details. Reports overwrite the previous snapshot and are ignored by Git. Git collection omits authors, commit messages, remotes and raw stderr; it records only branch, commit hash and repository-relative changes. Git unavailable/non-root/unborn states become UNKNOWN rather than fabricated clean/pushed states.

The generated handoff is a dated-by-context snapshot of observed local files, not a live Git view or proof of completion. It preserves manual notes and distinguishes registry evidence from newly run tests. The generator settles its own changed-file entry, but a later commit necessarily changes HEAD. Use `python scripts/project_status.py --check-only` after committing to refresh local reports/Git state without editing documentation; combine with `--no-report` for a fully read-only status invocation. Exit codes: 0 for no critical errors (warnings allowed), 1 for validation failure, 2 for invocation/I/O failure.

Writes are atomic per file and marker changes are preflighted. Run one tracking writer per checkout; there is no cross-process transaction lock. Unexpected session termination does not trigger a hook. Agent startup/shutdown instructions are checkpoints, not a background scheduler. Full commands and limitations are documented in `scripts/README.md`.

## Local Windows launcher

Task 2.5 adds a Tkinter window outside the public site's runtime. `status_launcher.pyw` starts the GUI without a console; its worker calls the existing `project_status.py` with the same Python installation, absolute paths, explicit project-root cwd, merged UTF-8 stdout/stderr and CREATE_NO_WINDOW. A queue delivers output to the Tk thread, with one run at a time per window. Folder actions use the Windows shell. Closing leaves an already-started check free to finish its writes.

The standard-library shortcut installer uses documented Shell COM/Known Folder APIs and verifies Desktop and Start menu `.lnk` targets, arguments, working directories and AppUserModelID. It respects redirected desktops, defaults to the installed Python icon, and refuses unrelated same-name links. No pinning settings, registry configuration, admin changes or remote services are involved. Taskbar pinning remains manual.

The GUI's context, worker and actions are separated for a later dashboard-opening action; no Task 3 dashboard is implemented. See `scripts/WINDOWS_LAUNCHER.md`. Launcher files must remain in the selected checkout; moving the checkout/Python or switching to a branch without them requires recreating/restoring shortcuts.

## Routing and discovery

Use ordinary relative links. Tool cards point to `<slug>/index.html`; every tool links to `../index.html`. Existing nested URLs also load through the live host's directory index behavior. Preserve directory names for stable links.

The homepage normalizes NFKC, English locale lowercase, trimmed/repeated spaces, then matches each card's `data-title`. It does not currently search descriptions or registry JSON, filter categories, paginate, or generate cards from the registry. Do not assume adding a registry entry publishes a tool. Add the page and homepage card explicitly.

The management checker compares implemented entries with homepage links, initial count, existing directories, navigation, verification hashes, and generated documents. It never changes homepage HTML automatically.

## Design conventions

Retain `#020617` / slate-950 background, slate borders/panels/text, and indigo accents. Pages use system sans-serif, rounded panels, responsive grids, and readable input areas. Use visible focus, descriptive labels and headings, native buttons/inputs where possible, status text for errors/results, and reduced-motion handling. Do not use color as the only warning.

Advertisement containers are styled dashed-border placeholders. They have no actual AdSense integration. The social tool has phone-style, selectable feed cards; these are estimates, not platform-rendered embeds.

## Processing and existing limits

| Utility | Processing | Important boundary |
| --- | --- | --- |
| Social Counter | Unicode code-point counts; text-only previews; whitespace cleanup | Limits 280 / 3,000 / 2,200 / 4,000; LinkedIn hook 140; no full X weighting or guaranteed truncation |
| Excel Sandbox | Iterative tokenization, delimiter analysis and text-node formatting | Input limit 50,000 UTF-16 code units; visual indentation capped at 40 levels; no formula execution/full validation |
| Text Cleanser | Editorial phrase regex and text-node highlights | 200 wpm estimate; one saved replacement undo state; no explicit large-input cap; not AI detection |
| Stream Roulette | In-page curated catalog and random destination selection | Nine configured destinations; six filters; no current provider catalog queries or regional detection |

There are no file-processing tools yet. Planned file dependencies do not exist in the runtime. Before adding them, define supported formats, encrypted/corrupt-file handling, input/page/dimension limits, export fidelity, progress/cancellation, and memory cleanup. Large inputs may need workers or chunked processing. Do not promise PDF compression, metadata removal, font coverage, or browser codec support before verification.

## Security and privacy

- User input is rendered with text nodes or `textContent`. The social tool's `innerHTML` template uses static internal labels only; user captions never enter it.
- No current tool evaluates formulas, executes user JavaScript, calls AI APIs, uploads input, or uses draft storage. Clipboard output is an explicit action.
- Hosting and the Tailwind CDN receive ordinary request information. External streaming links open third-party sites with `noopener noreferrer`. These facts limit blanket “no network” claims.
- Future markup/SVG previews must isolate untrusted content, disable scripts and remote fetches, and prevent same-origin access. A formatter is not an excuse to execute input.
- Cryptography uses established browser primitives with explicit formats, secure-context detection, bounded resources, and failure tests. No custom cryptography or insecure fallback.
- Public source must never contain secret credentials. Public viewing does not grant editing rights; account authentication and collaborator/app permissions are managed outside these static files.
- A source scan or smoke test does not establish account security, deployment hardening, or freedom from vulnerabilities.

## Browser compatibility and QA

The existing code uses modern features including Unicode property escapes, regex lookbehind, `ResizeObserver`, optional clipboard APIs, and CSS `:has`. Target current evergreen browsers. Exact minimum versions and a complete cross-browser matrix have not been established.

The dated baseline was exercised with desktop Edge/Chromium, including mobile-sized viewports. This is not physical-device testing, Safari/Firefox testing, screen-reader certification, or a penetration assessment. The social counter additionally passed six viewport sizes and blocked-clipboard fallback checks. Detailed scope is recorded in the baseline JSON.

There was no committed test suite before this setup. The new committed tests exercise management validation, not all utility behavior. Browser smoke scripts used for the baseline were session-local and are not a portable committed UI suite. Future tool work should add reusable browser tests when warranted; do not claim this checker reruns the baseline browser interactions.

## Deployment and preservation

The existing `CNAME` is `everydaydigitalbox.com`; the homepage includes a Google site-verification meta tag. The live pages returned HTTP 200 with matching source at the baseline audit. GitHub-hosted infrastructure was observed, but repository Pages publishing-source settings and DNS administration were not inspected in this setup.

Commit/push and deployment are different events. For substantial work, open a feature-branch PR. After merge/publication, inspect the deployment and fetch the live HTML, confirm the intended implementation, and update release evidence. Preserve the domain and verification configuration. Never claim a PR is deployed merely because it exists.

## Scaling direction

Keep independent pages for now. As measured needs emerge, consider shared local assets, generated catalog metadata, category discovery, reusable parsers, and a compiled stylesheet. Preserve URLs and review architectural changes first; growth targets alone do not justify a wholesale rewrite.
