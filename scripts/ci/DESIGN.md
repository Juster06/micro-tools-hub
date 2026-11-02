# Task 9.5 CI design — recorded before implementation

Stage A is local only, based on Task 9 main `93867ed9d02b702eaff250288f58ca7abba7bbab`
(tree `9e3974eff435b7ece6b1bc8387343e6956c78241`). Inventory remains 93/18
released/0 tested/6 ready/68 planned/1 blocked, milestone 72%.

The existing Python unittest discovery executes 123 tests, including four native
Windows tests (interpreter pair, Known Folders, temporary COM shortcuts, Tk table
rendering). Run the complete suite once on windows-2022 rather than silently
skipping those tests on Linux or duplicating the full suite across operating
systems. Existing production Desktop/Start menu shortcuts are never installed or
modified by CI: COM tests use temporary fixture folders.

Run Node's existing two framework/bridge files and fourteen independent logic
files once on ubuntu-24.04. Run the twenty-eight extended/navigation Node files
once, sequentially, in a separate ubuntu-24.04 browser job. These partitions
together cover the existing 375 Node tests. In addition, run fourteen JSON logic
profiles, eighteen JSON browser profiles, eighteen structural profiles and both
neutral templates through the existing Python entry points. The four specialist
tools have no isolated logic adapter: declare this unavailable scope, require
their structural/browser profiles, and never turn PARTIAL into full logic PASS.

Use Python 3.14.4 and Node 24.22.1. The Node harness uses built-in WebSocket
(minimum Node 22.4). No production code needs a dependency. Only browser acquisition
uses an exactly pinned Playwright package/lock under this CI directory; the
existing CDP harness receives its full Chromium executable through EDB_TEST_BROWSER.
Linux OS libraries are installed with Playwright's documented --with-deps command.
Do not replace browser interactions with DOM mocks, change timeouts/assertions,
add a server, modify the harness unless compatibility requires it, or use the
user's Edge profile. Existing file:// page loading, isolated temporary profiles,
HTTP(S) blocking and simulated clipboard/download/composition behavior remain.

Commit a machine-readable coverage map and fail closed on missing, empty,
unmapped or duplicate suites. CI-specific runners require nonzero executed
counts and zero failures/cancellations/skips/todos for required tests. The full
Python Windows suite permits no skips. Required JSON layers must explicitly
PASS with nonempty cases; omitted layers remain omitted rather than claimed.
Preserve subprocess exit codes and bounded timeouts. Test negative controls in
isolated disposable copies, never by mutating released source in the checkout.

Triggers: PRs targeting main, pushes to main, manual dispatch. No feature push
trigger. Read-only contents permission, no secrets, no pull_request_target,
no persisted checkout credentials. Pin actions by verified commit SHA and pin
runner OS versions. PR concurrency cancels superseded runs of the same PR only;
main runs are not cancelled. Aggregate check fails if any required job does not
succeed. No continue-on-error or success suppression.

Only allowlisted count/status summaries and the coverage map are uploaded for
seven days; raw stdout/stderr stays in ignored reports/ci locally or Actions logs,
not uploaded as artifacts. No browser profiles, screenshots or bundles. Logs and
summary distinguish actual local execution from pending GitHub execution.

There is no checked-in Pages workflow at this baseline. The separate GitHub-managed
Pages workflow was observed building main/root with Jekyll into ./_site, last
successful run 41410170246. Do not create or edit a deployment workflow or settings.
Pages currently deploys main updates independently; functional CI does not enforce
deployment blocking. Branch protection/settings are outside Stage A authorization.
Public live verification, actual installed shortcuts, physical devices, OS copy/
save dialogs and screen readers remain separate manual release checks.

Before delivery: execute the exact job commands locally with Windows Edge and
the pinned Windows Chromium; run controlled Python/Node/browser/registry/source,
missing-dependency/missing-suite/skip/timeout failures and restore baselines;
validate YAML with actionlint; inspect all preserved bytes; commit on
feat/task-9-5-functional-ci only. Do not publish, create a PR, merge, deploy,
change statuses/settings, or begin Task 10. An actual Linux/GitHub-hosted run
remains pending, regardless of local test success.

## Platform review refinement

During implementation review, select **ubuntu-22.04 for the browser job**. Both
GitHub and the pinned Playwright support it; Node-only/aggregate jobs stay on
ubuntu-24.04. Ubuntu 23.10+ applies additional AppArmor user-namespace restrictions
to downloaded Chromium builds. Choosing the supported older image avoids adding
global security overrides or --no-sandbox to the harness. This is a reasoned
platform choice, not a claim of a successful Linux run. See [Chromium's explanation](https://chromium.googlesource.com/chromium/src/+/main/docs/security/apparmor-userns-restrictions.md).
