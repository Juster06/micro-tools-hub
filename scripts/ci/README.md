# Functional CI — Task 9.5

## Stage C: integrated on main, independently verified

PR #14 merged normally as `3f08b910a70f105b91d26e6df8eca7c0477d504d` at
2026-11-02T23:14:09Z, with expected reviewed head
`901bcaf4d792c187c35a2bf8a1d358324371c8c2`. Complete merge tree
`fa114410eeaa83268110e2479ef72facb3624115` matches the reviewed preview.
Final PR run **41535344652** succeeded for that feature; genuine main push
[run **41543825503**](https://github.com/Juster06/micro-tools-hub/actions/runs/41543825503)
independently succeeded on the merge: Windows Python **142/142**, Ubuntu Node
**179/179** plus **639** logic fixtures, real Ubuntu Chromium **196/196** plus
**291** fixture cases/**777** assertions, templates **6 logic/12 browser/48
assertions**, and aggregate **Required functional checks**. No mandatory failures,
skips, cancellations or timeouts. Actual job logs and all three downloaded ZIPs
were checked: digest, summary/coverage allowlist, counts/log agreement, exact
published coverage map, privacy and seven-day retention. The final delivery
report separately verifies this documentation checkpoint's own main CI run.

Existing managed Pages run **41543825473** automatically deployed the merge,
using main and repository root. Public homepage, all 18 released utility pages,
registry and owner Analytics retain exact normalized source identity. No Pages
workflow/source setting changed. Pages runs independently; this CI does not gate
deployment. Hosted test success is distinct from public publication certification.

Read-only inspection found main **unprotected**, required checks off/empty, no
repository rulesets or active main rules. The connected owner account has admin
rights; no protection/settings/permissions were changed. Public repositories can
use branch protections and branch/tag rulesets with GitHub Free. A separately
authorized policy could require PRs and the actual **Required functional checks**
context from GitHub Actions, with an explicit owner/admin bypass policy. Classic
admin bypass is default unless restricted; rulesets support configured bypass
actors. Classic push allowlists have organization-repository limits; require-PR
rules remain relevant here. This connector's Administration-write permission
was not tested. See [protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
and [available rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets).
Exact subscription was not inspected; public feature availability needs no paid
upgrade. Pages/protection detail endpoints were inaccessible to unauthenticated
reads; branch/rules metadata and actual main/root build logs provide the recorded
observations. No authentication/settings changes were attempted.

Original local feature history and active checkout are preserved; local main was
safely fast-forwarded. No utility/registry/homepage/Analytics/domain/audit/test/
framework/dashboard/launcher/shortcut implementation changed. Four specialist
isolated-logic adapters remain unavailable (explicit NOT RUN); mandatory structure
and browser profiles pass. Native installed-shortcut GUI launch was not newly
tested in this stage. No lifecycle changes or Task 10. Earlier stage summaries
are historical; job/maintenance documentation below remains applicable.

## Historical Stage B: genuine hosted CI verified; PR #14 awaiting review

[Functional CI run 41425207614](https://github.com/Juster06/micro-tools-hub/actions/runs/41425207614)
completed successfully for published feature 858fc772833a2456931cd80a3ac2eeaf397fd979
on pull_request. All four jobs passed: Windows Python **142/142**, Ubuntu Node
**179/179** +**639** logic fixtures, actual Ubuntu Chromium **196/196** +**291**
fixture cases/**777** assertions, templates **6 logic/12 browser/48 assertions**,
and the aggregate. Runtime/action pins and test scopes below remain unchanged.
All three actual artifacts were digest/contents/privacy/retention verified and
counts matched against logs and that commit's coverage map. CI is operationally
verified for this PR; this work does not configure or claim branch protection
or deployment gating. [PR #14](https://github.com/Juster06/micro-tools-hub/pull/14) remains
open, non-draft, targeting main, auto-merge off; no merge, deployment, lifecycle
or settings change. Current final documentation checkpoint's exact identity/run
is recorded separately in the delivery report.

Initial run 41423878108 genuinely failed Windows short/long TEMP comparisons;
the aggregate correctly rejected its failure. Canonicalizing only the CI fixture
temporary parent and adding one guard fixed it. Existing assertions, mandatory
scopes, production code, browser sandbox and timeouts are unchanged. Hosted
guards and both actual aggregate outcomes were inspected. Remaining exclusions
below still apply; CI success is not new public live/publication verification.

### Historical Stage A and first hosted investigation

## Historical Stage B compatibility investigation

[PR #14](https://github.com/Juster06/micro-tools-hub/pull/14) publishes the approved
Stage A content against main. Initial pull_request run 41423878108 genuinely ran
on GitHub. Node passed; Windows ran all 141 tests and failed six path comparisons
because its TEMP used a short 8.3 alias while production correctly resolves long
paths. Original logs/failure summary retained. The CI bootstrap now resolves the
Windows temporary root before discovery, with one added guard (142-test floor).
No original assertion, production behavior, browser flag or timeout changed.
Full local regression and a subsequent complete hosted pass are required before
calling this operational. Stage B authorizes publication/verification only;
no merge, protection/settings edit, deployment, lifecycle transition or Task 10.

This is a **local implementation; GitHub-hosted verification is pending**. No
branch publication, PR, merge, deployment, settings/protection change or Task 10
is authorized by Stage A. The site still has 18 released tools and a 72% first
milestone. CI never changes registry lifecycle/publication evidence.

Read [the design recorded before implementation](DESIGN.md) and the executable
[coverage map](coverage.json). Workflow: `../../.github/workflows/functional-ci.yml`.
These are developer dependencies only; tool users still need only a browser.

## Jobs and exact commands

All commands run at repository root. `python` is the current interpreter;
child calls use `sys.executable` and set `WEBUTILS_PYTHON` for the existing bridge.

| Job / check name | Runner | Entry point | Required scope |
| --- | --- | --- | --- |
| python-project / Python and project validation | windows-2022 | `python scripts/ci/run.py python-project` | Complete unittest discovery, registry, lifecycle/source/audits/homepage, all 18 structural profiles, status, working/commit whitespace |
| node-regression / Node logic regression | ubuntu-24.04 | `python scripts/ci/run.py node-regression` | Two original Node framework/bridge files and all 14 independent logic files; 14 JSON logic profiles |
| browser-tests / Real Chromium browser tests | ubuntu-22.04 | `python scripts/ci/run.py browser-tests` | Real browser preflight, all 28 extended/navigation files sequentially, all 18 JSON browser profiles, both neutral templates |
| required-checks / Required functional checks | ubuntu-24.04 | `python scripts/ci/required_checks.py` | Depends on all three jobs; every result must be success, including after failure/skip/cancellation |

The detailed commands inside these entry points are:

```sh
# Python job (including four genuine native Windows fixture tests)
python scripts/ci/unittest_runner.py
python scripts/validate_registry.py --json --no-report
python scripts/check_project.py --json --no-report
python scripts/verify_tools.py --json --no-report
python scripts/test_tool.py --id TOOL_ID --workspace canonical --layers structural --no-report
python scripts/project_status.py --check-only --no-report --json
git diff --check
git diff --check EVENT_BASE HEAD

# Node job: replace NODE_FILES with the explicit node_files array in coverage.json
node --test --test-concurrency=1 --test-reporter=tap NODE_FILES
python scripts/test_tool.py --id TOOL_ID --workspace canonical --layers logic --no-report

# Browser job: replace BROWSER_FILES with browser_files in coverage.json
node scripts/ci/preflight.mjs
node --test --test-concurrency=1 --test-reporter=tap BROWSER_FILES
python scripts/test_tool.py --id TOOL_ID --workspace canonical --layers browser --no-report
python scripts/verify_tool_templates.py
```

TOOL_ID loops and file arrays are explicit in the map, not shell globs; missing,
new/unmapped, duplicate or empty suites fail before testing. Only 14 tools have
isolated logic profiles. The original social-counter, excel-sandbox, text-cleaner
and streaming-roulette have **NOT RUN** isolated logic, not full logic PASS; their
real browser and structural checks are mandatory. A scoped PARTIAL result from
`test_tool.py` is accepted only when the explicitly requested layer actually
passes; omitted layers never count as executed. New tools/tests require reviewing
and updating the map, floors and docs. No production or existing harness/assertion/
timeout changes were needed for this CI implementation.

`EVENT_BASE` is the validated 40-character PR base or push-before SHA, passed via
an environment variable without shell interpolation. Full-history checkout makes
the range available. Manual/local runs use origin/main (or HEAD^ on main), plus
working-tree whitespace. Invalid/zero event parents fail clearly for review.

## Runtime and dependency setup

Python **3.14.4**, standard library; Node **24.22.1**, built-in WebSocket/CDP;
Playwright **1.64.1**, with lockfile SHA-512 integrity for both npm packages.
Playwright supplies full **Chrome for Testing 156.0.8078.4, revision 1248**; it does
not replace the existing browser harness. The two acquisition packages are
Apache-2.0 licensed and introduce no website/runtime/build dependency. Network is
needed for Actions/runtime/npm/browser/OS-library installation, not for tool input
processing or external-site regression. Acquisition is roughly a 200 MB browser
download plus OS libraries; no browser cache or unnecessary screenshots/bundles
are uploaded. Installed dependencies stay ignored.

CI setup (performed automatically by the browser job):

```sh
npm ci --prefix scripts/ci --ignore-scripts --no-audit --no-fund
cd scripts/ci
npx --no-install playwright install --with-deps --no-shell chromium
cd ../..
node scripts/ci/browser-path.cjs --github-env
```

Linux `--with-deps` installs required system libraries on the disposable hosted
runner. Do not add `--no-sandbox` or silently use an unpinned system browser.
The package version fixes the browser revision; update package.json and lock
together, inspect the new browser metadata, and rerun both local and hosted tests.
See [official browser installation documentation](https://playwright.dev/docs/browsers).

For local Windows validation, use the same npm command and:

```powershell
node scripts/ci/node_modules/playwright/cli.js install --no-shell chromium
$env:EDB_TEST_BROWSER = (node scripts/ci/browser-path.cjs)
python scripts/ci/run.py python-project
python scripts/ci/run.py node-regression
python scripts/ci/run.py browser-tests
```

Optionally set PLAYWRIGHT_BROWSERS_PATH to an ignored/private cache location for
both install and executable lookup. Never commit an absolute executable/cache
path. Existing manual Edge/Chrome discovery and `--browser` remain unchanged.
CI preflight insists on a real configured executable and successful CDP session,
so an invalid explicit selection cannot silently fall back to the owner's Edge.

The first local pinned-browser launch failed because the downloaded Windows
binary cache lacked AppContainer read/execute permissions. The failure was
retained and correctly stopped CI at preflight. Applying read/execute access
for the standard application-package SIDs **only to that disposable downloaded
browser tree** fixed preflight; no project/profile/user-data permissions, system
settings, existing shortcuts, assertions, browser flags or timeouts were changed.
No sandbox was disabled. On Windows, inspect a similar sandbox-access diagnostic
and repair only the owned public browser installation, following [Chromium's sandbox documentation](https://github.com/chromium/chromium/blob/main/docs/design/sandbox.md);
do not apply permissions to a home directory or the project checkout.

The Linux browser job uses supported Ubuntu 22.04 to avoid the additional
AppArmor user-namespace restriction introduced in Ubuntu 23.10+, keeping the
browser sandbox enabled without global kernel/security-policy overrides.
Node-only and aggregate jobs use Ubuntu 24.04. This platform choice requires
future maintenance when runner or Playwright support changes; inspect an actual
hosted run before upgrading. See [Chromium's platform explanation](https://chromium.googlesource.com/chromium/src/+/main/docs/security/apparmor-userns-restrictions.md).

## Test audit and platform classification

| Scope | Classification and requirements |
| --- | --- |
| Tracking/framework Python logic and validators | Linux suitable with Python/Git; run once with the full Windows suite to avoid duplication |
| Native interpreter pair, Known Folders, temporary COM shortcut roundtrip, hidden Tk rendering | Windows runner required; full Python job permits zero skips, Tk installed with CPython; fixtures never reinstall owner shortcuts |
| Node bridge/framework and independent pure logic | Linux suitable; Python needed by bridge, Node 22.4+ technically required; exact CI versions above |
| JSON logic cases | Linux suitable; Python/Node, no browser, HTTP server or network |
| JSON browser, extended interactions, hub search/navigation, neutral templates | Linux suitable via existing EDB_TEST_BROWSER configuration; pinned full Chromium + OS libraries; no harness portability change needed |
| Installed owner Desktop/Start menu links and native OS clipboard/IME/Save dialogs | Manual release/host verification, not reproducible hosted CI; no claim of CI coverage |
| Actual public HTTPS behavior, deployed identity, CDN styling, hosting/Analytics delivery | Separate genuine live/deployment verification; not covered by local isolated CI |
| Physical devices, screen readers, Firefox/Safari, performance/security certification | Not appropriate to infer from these Chromium suites; excluded |

The harness loads real local file:// pages and real hub links, creates/removes an
isolated temporary profile, and blocks HTTP(S). No local HTTP server is needed.
Clipboard outcomes, downloads/Blob bytes and composition are controlled fixtures;
native keyboard/CDP events and viewport emulation remain real browser actions.
Extended suites retain console-error assertions, stale-action races, copy/download
failures, content safety and input-transport/storage checks. Existing command,
page-ready and fixture waits are unchanged. Tests remain sequential. CI command
deadlines bound stuck processes (exit 124 and isolated process-tree cleanup),
not retries or widened behavioral waits. Runner time limits also bound each job.

## Failure propagation and reporting

Each required child exit must be zero, and each supported report must prove
nonempty execution and clean PASS. Python skips/expected failures/unexpected
successes are failures. Node cancellations/skips/todos, empty or missing/ambiguous
TAP totals are failures even if Node itself exits zero. Reviewed test-count floors
are 142 Python, 179 Node logic and 196 Node browser. JSON layers need PASS and
nonzero functional cases; template verification must include both templates and
all layers. Registry/source/status warnings also fail the clean validation gate.
There is no continue-on-error, suppressed exit, empty selection PASS or placeholder
success. Exceptions are failures, never an invented PASS.

Readable stdout/stderr appears in Actions logs. Ignored `reports/ci/JOB/*.log`
holds local diagnostics; `summary.json` records actual execution origin, scope
status, exit code and supported executed/pass/failure/skip/assertion counts.
An unavailable field is not fabricated. Only summary.json and coverage.json are
uploaded, with seven-day retention: no raw logs/private paths, user input,
credentials, browser profiles or screenshots. Missing setup/runner evidence stays
failed; the upload step cannot turn it into a passing required job. Summaries also
appear in the Actions step summary. Existing dashboard report schemas are untouched.

## Triggers, security and deployment

Runs on PRs **targeting main**, pushes **to main**, and manual dispatch. Feature
branch pushes alone do not trigger it. Same-PR superseded runs may cancel; main
runs and unrelated PRs have separate groups. Permissions are only `contents: read`;
checkout does not persist credentials. No repository secrets, privileged PR event,
write token, deployment job, cache or settings mutation is used. All four official
Actions are pinned to verified release commit SHAs (version comments in YAML).
Manual dispatch follows GitHub's default-branch workflow availability rules.

At the verified baseline there was no checked-in deployment workflow. The active
GitHub-managed `dynamic/pages/pages-build-deployment` workflow builds main/root
with Jekyll to ./_site and publishes the existing custom domain. Its last inspected
successful baseline run is [41410170246](https://github.com/Juster06/micro-tools-hub/actions/runs/41410170246).
CI does not replace, edit, disable or gate it. Main updates may deploy independently
of functional check completion. A Pages success is not functional CI success.

No branch protection/ruleset enforcement is claimed or changed. In a separately
authorized stage, first publish/review the feature branch, run an actual hosted PR
build and inspect all three jobs/artifacts/aggregate result. Only after verified
hosted success consider separately authorized protection requiring **Required
functional checks** and current-main review. Deployment ordering would require
separate explicit design/settings authorization. Fork PRs use the same ordinary
read-only PR event and get no owner secrets.

## Local validation and maintenance

Local execution and negative-control results are recorded in the Task 9.5 section
of SESSION_HANDOFF.md and the delivery report. Negative mutations were confined
to disposable copies, followed by passing restored baselines; no approved runtime
source/evidence was mutated. actionlint **1.7.12** validates workflow syntax,
triggers, jobs, expressions, action inputs and dependencies; it does not execute
GitHub Actions or certify Linux system libraries. No suitable local Linux Actions
emulator was available; no Windows/WSL/system configuration was installed/changed.

An actual Ubuntu runner, GitHub event permissions, artifact delivery and native
Windows hosted desktop behavior still require a real hosted run. Locally exercised
pinned Windows Chromium establishes CDP compatibility, not Linux certification.
Do not call CI operational until the real hosted run succeeds. Public live
verification remains the Task 9 historical release evidence, not a new CI claim.
Keep runtime/action/browser pins, npm lock integrity, coverage map, test floors
and platform exclusions reviewed together. See [official Actions workflow syntax](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions)
for trigger/permission/concurrency maintenance.
