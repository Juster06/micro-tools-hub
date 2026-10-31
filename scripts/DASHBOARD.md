# Local Project Control Dashboard

The Task 3 dashboard extends the existing Windows launcher. It is a developer application, separate from the public website. It works offline using Python 3.10+ with Tcl/Tk and the standard library. Git is optional for local activity metadata; Node is needed only for the existing compatibility tests. No server, database, external API, administrator access, telemetry or website changes are introduced.

## Start and refresh

Double-click the existing **Everyday Digital Box — Project Status** Desktop or Start menu shortcut. Both still target the same Python installation and `scripts/status_launcher.pyw`; the AppUserModelID is unchanged. The window title is now **Everyday Digital Box — Project Control Dashboard**.

From any directory, use desktop Python with an absolute path to `<checkout>/scripts/status_launcher.pyw`. For console diagnostics use `python <checkout>/scripts/status_launcher.py`. Add `--project-root <checkout>` to inspect another checkout, or `--no-auto-refresh` to load saved snapshots without running the workflow on startup.

Startup loads saved reports in a background worker, then automatically runs the existing `python scripts/project_status.py` workflow, preserving the launcher behavior. **Refresh Project Status** runs it again; **Reload Saved Data** only reads current files. Refresh updates marked project documents and ignored reports, so it can legitimately leave Git dirty. Nothing commits, pushes, deploys or implements tools automatically.

Run `python scripts/install_status_shortcut.py` to safely recreate shortcuts after moving Python or the checkout. Existing targets need no update for Task 3. Pin manually by launching the shortcut, right-clicking its taskbar icon and selecting **Pin to taskbar**, if Windows policy permits. See `WINDOWS_LAUNCHER.md` for installation details.

## Screens

- **Overview:** actual registry totals; released-only progress toward 25, 50, 100, 200, 300, 500 and 1,000; next eligible utility; validation/report timestamps; historical verification records. The overview scrolls on smaller/scaled displays.
- **Tool Registry:** read-only search by ID/name; category, status and priority filters; clickable sortable columns; horizontal/vertical scrolling; selected-tool details. Filters debounce for 150 ms and rows render in batches of 80. Optional missing fields show explicit fallbacks.
- **Development Queue:** next twenty eligible entries, all eligible READY tools, planned tools, in-progress tools and unmet tool dependencies. Recommendations reuse `sequence_rank`, then priority, then ID, with dependencies TESTED/RELEASED. Planned display order is priority/name and is not a readiness score. No tasks start automatically.
- **Testing & Validation:** the four existing reports, timestamps, diagnostics, affected paths and available report details. Select a row to inspect errors and warnings.
- **Project Activity:** a fresh local Git observation, current handoff, changelog, roadmap and master plan with safe local-opening buttons. Recent task completion notes remain in the handoff/changelog; registry verification records are identified separately.
- **Blockers:** every BLOCKED entry, its documented notes/reason, dependencies and any explicit action. Missing reasons say “Reason not documented.”
- **Quick Actions:** existing folder actions, documentation, privacy-conscious Copy Summary, complete most-recent command output, reload and an optional local Git executable setting. Close is always available in the footer.

Owner-directed work is read from `**Next major task:**` in the current handoff. It remains separate from the registry's next READY public utility. Task 4 is not started by Task 3.

## Evidence and freshness

Registry counts are calculated from `TOOL_REGISTRY.json` using the shared tracking status vocabulary. The dashboard runs the existing registry validator; invalid data gets a prominent warning and readable entries are shown as partial information. It never changes lifecycle statuses or invents missing verification.

Task 2 reports use schema version 1, `check_name`, `generated_at`, `status`, `errors`, `warnings`, `counts` and `details`. These are structural checks, not functional or browser tests. There is currently **no structured Python/Node test-run report** in this workflow. The dashboard therefore shows **“Test results unavailable — run tests to update.”** It does not parse old handoff test counts into current results. Run `python -m unittest discover -s tests -v` and `node --test scripts/project.test.mjs` separately; retain actual outcomes in the handoff. A future structured test-result producer/reader can be added deliberately.

Report display states are separate from registry lifecycle states:

| State | Meaning |
| --- | --- |
| PASS | Recorded structural check passed for the loaded snapshot |
| FAIL | Recorded errors/failure |
| WARNING | Recorded WARN/noncritical warnings |
| NOT RUN | Report file is missing |
| UNKNOWN | Unreadable/invalid schema, JSON, timestamp, or future-dated report |
| STALE | Older than 24 hours, or inputs/report hashes changed since refresh |

After a command generates all four reports, ignored `reports/dashboard-refresh.json` binds their SHA-256 hashes to relevant project source/document inputs. A failed validation can also have fresh FAIL reports; freshness does not imply success. Reports predating a failed/interrupted invocation, unchanged recent report bytes, and source inputs changed during checks are not rebound as fresh. Expected generated-document writes are excluded from the during-run source comparison, then included in the completed snapshot hash. Legacy reports without this sidecar use their timestamp and project input mtimes with a two-second rounding allowance. These legacy timestamps cannot prove an unchanged historical source tree; refresh to capture hashes.

Data is a point-in-time snapshot. Reload or refresh after external edits; the app is not a live filesystem watcher. Existing report schemas do not record execution duration or retain the last passing run after a failure overwrites it. Such unavailable fields are identified explicitly. Push and deployment remain unverified offline.

## Architecture and extension

| Module | Responsibility |
| --- | --- |
| `status_launcher.pyw` | Existing no-console entry point; native startup error message |
| `status_launcher.py` | Existing interpreter/process helpers, CLI and dashboard adapter |
| `dashboard/data.py` | Read-only loading, schema checks, safe partial data, report freshness, counts, filters, queue and summaries |
| `dashboard/operations.py` | Background jobs, cross-window refresh lock, freshness capture and allowlisted local file/settings actions |
| `dashboard/widgets.py` | Dark ttk styles, scrollable views and batched tables |
| `dashboard/pages.py` | Overview, registry, queue, validation, activity and blockers |
| `dashboard/app.py` | Navigation, Quick Actions, main-thread event loop and user actions |

Potentially slow loading, hashing, Git and subprocess I/O run outside Tk's main thread. Workers send queue events; only the UI thread touches widgets. One job runs per window; `reports/dashboard-refresh.lock` also excludes other dashboard refreshes for the same checkout using OS file locks. OS locks release if the process dies. Manually launched tracking CLI commands do not acquire that dashboard lock; avoid running independent writers concurrently. Closing while busy leaves the non-daemon worker to finish its writes safely.

For future updates, add pure data behavior/tests to `data.py`, worker behavior to `operations.py`, and presentation to the view modules. Retain shortcut entry points. Add an explicit report schema and source-freshness contract before displaying test totals; do not infer them from structural PASS or documentation prose. Keep the local dashboard out of the public website inventory.

## Troubleshooting and local settings

- **Git UNKNOWN only from desktop:** desktop Python can inherit a PATH without Git. In Quick Actions browse to the existing `git.exe`, then Save Git Path. Blank restores automatic discovery from PATH or standard Windows Git locations. It is saved only in ignored `reports/dashboard-settings.json`; do not commit that host-specific path. An invalid configured path does not silently substitute another executable.
- **Missing/invalid reports:** the window still opens. Inspect Testing & Validation, then refresh. Inspect command output for permission or validation errors. Missing documentation and JSON are reported separately, not silently repaired.
- **Another refresh is running:** wait for the other dashboard; do not delete locks or start another writer. Close does not cancel an active write.
- **Startup error / missing Tk:** use desktop Python with Tcl/Tk, preserve the entire `scripts/dashboard` package, and recreate the shortcut if paths moved. The `.pyw` entry point displays a native error dialog even if importing Tk fails.
- **Small display:** resize the window; use Overview's scrollbar, table scrollbars and the draggable registry details divider. Tabs and keyboard focus remain native Windows controls. This is not a screen-reader certification.
- **Clipboard/file-opening failure:** the app shows the failure in Quick Actions. Summary excludes local paths, author identities and remotes. Command output is complete for the latest refresh in the current window; it is not retained across application restarts.

## Validation scope

Automated tests use temporary registries, reports and subprocess fixtures. They cover partial/malformed data, counts, milestones, searching/filtering/sorting, queue order/dependencies, missing Git, stale evidence, safe local actions, job failure and duplicate refresh prevention. Windows Tk integration renders and filters 1,500 entries while the event loop remains active. Existing tracking and native shortcut tests remain in place. Manual GUI evidence and exact final suite counts are recorded in `SESSION_HANDOFF.md`; only actual executed checks may be claimed.
