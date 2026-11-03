# Main branch protection — active repository ruleset

## Verified current policy (2026-11-03)

The owner manually activated [Main Branch Protection - Required Functional CI](https://github.com/Juster06/micro-tools-hub/rules/26413762),
repository ruleset **26413762**, at 2026-11-03T00:58:27Z. Authenticated ruleset
readback and the effective-main-rules endpoint independently verify Active
enforcement. Main reports protected=true. The legacy classic-protection object
is disabled; that does not disable the active ruleset. Do not create an overlapping
classic rule or change repository protection/settings as routine development.

| Actual setting | Saved value |
| --- | --- |
| Target | Branch; includes `refs/heads/main` and `~DEFAULT_BRANCH`, excludes none |
| Current default branch | `main`; the two current targets resolve to the same branch |
| Pull requests | Required for ordinary non-bypass contributors |
| Mandatory approvals | `0`; no code-owner/last-push approval requirement or reviewer list |
| Conversation resolution | `required_review_thread_resolution: true` |
| Required check | Exactly **Required functional checks** |
| Check provider | GitHub Actions, `integration_id: 15368` |
| Up-to-date requirement | `strict_required_status_checks_policy: true` |
| Force pushes | Blocked by `non_fast_forward` |
| Branch deletion | Blocked by `deletion` |
| Emergency bypass | Repository administrator role (`actor_id: 5`), `bypass_mode: always` |
| Pages merge requirement | None; Pages is not a required status/deployment check |

Authenticated readback also returns current_user_can_bypass=always for the
connected administrator. Availability was inspected without exercising bypass.
Always allow is an intentional emergency exception, not a routine agent path.
The extra-approval-for-unattributed-changes flag is true but only affects a
nonzero approval requirement; the current requirement remains zero.

`~DEFAULT_BRANCH` follows any future default-branch change as well as the explicit
main target. It is currently redundant, not an extra protected branch. A future
rename/default change needs an explicit review of the intended scope.

## Verification and evidence

Use documented GET-only readback before work:

```text
GET /repos/Juster06/micro-tools-hub/rulesets/26413762
GET /repos/Juster06/micro-tools-hub/rules/branches/main
GET /repos/Juster06/micro-tools-hub/branches/main
GET /repos/Juster06/micro-tools-hub/commits/HEAD_SHA/check-runs
```

The active-main response lists deletion, non_fast_forward, pull_request and
required_status_checks from this exact ruleset, with matching parameters. The
aggregate check's actual check-run provider is GitHub Actions App 15368. Saved
readback establishes effective enforcement for ordinary actors. It does not
pretend that a rejected merge, destructive push/deletion or bypass experiment
was performed. None was performed for this task.

Bypass actors are omitted from unauthenticated readback. The authenticated
readback did expose exactly RepositoryRole 5 /always; absence in a public response
must not be interpreted as no bypass. Check actual current settings rather than
assuming a historical screenshot or passing CI proves enforcement.

Before this final correction, main push run **41544609839** and PR 15 run
**41550495523** succeeded with Python 142/142, Node 179 logic +196 browser,
additional 639 logic cases,291 browser cases/777 assertions and templates 6/12/48.
These baseline runs predate ruleset activation. Updated PR 15 and merged-main
workflow identities/results are recorded in the [final PR delivery record](https://github.com/Juster06/micro-tools-hub/pull/15).
Only a completed run for the exact current head establishes current CI success.

## Routine Codex PR workflow

1. Read the latest handoff and actual effective rules. Fetch main and inspect
   unexpected advances. Preserve the existing checkout, original branches and
   unrelated user changes. Start a bounded feature branch.
2. Review the complete diff and relevant local regression, registry/source/
   homepage/status, whitespace and privacy checks. Keep credentials, personal
   paths, generated reports/caches and machine settings out of committed files.
3. Publish reviewed exact content without force-push/history rewriting. When
   connected publication produces a different commit SHA, preserve original
   local commits and independently fetch/verify complete Git-tree equality.
4. Open/update the PR against current main. Wait for its exact current head's
   Python, Node, real Chromium and **Required functional checks** jobs. Inspect
   actual outcomes/counts and permitted summary artifacts. Resolve conversations.
5. Confirm the PR is current with main. If main advanced, merge origin/main into
   the feature branch, resolve/review conflicts and push normally. Rerun CI;
   an earlier head's success cannot satisfy the new head.
6. With owner merge authorization, all ordinary requirements satisfied and a
   clean merge state, use a normal merge with the expected-head guard. No admin
   bypass, force merge, requirement reduction or direct main update. If GitHub
   reports a ruleset violation/missing check, stop and report it.
7. Safely fast-forward local main. Verify actual main-push CI and independent
   Pages behavior/public preservation. Record exact commit/tree/run identities
   in the durable linked delivery record and final report. Do not claim success
   while a mandatory run is pending.

No mandatory human review count was configured, but owner authorization for
agent merge actions remains necessary. A caller's administrator role is not
authorization to ignore ordinary PR requirements or use emergency bypass.

## Release metadata and handoffs

Submit registry status/publication evidence, release audits, homepage availability
and derived tracking updates through normal reviewed PRs with passing current CI.
Do not push release metadata or final documentation directly to protected main.
Public source/behavior and a matching Pages deployment must be independently
verified before a RELEASED transition; merged code, structural PASS or CI success
alone does not establish publication. No lifecycle change is authorized here.

Record completed merge/main identities in [PR 15's linked delivery record](https://github.com/Juster06/micro-tools-hub/pull/15)
and the final integration report after actual verification. SESSION_HANDOFF.md
links to this durable continuation mechanism because its own containing merge
SHA and subsequent hosted run cannot be embedded before that merge exists.
Any further tracked-file correction after merge must use a new ordinary PR;
updating the linked PR delivery record does not mutate protected main.

## Recovery and emergency procedure

For a blocked PR, inspect the exact head, context spelling, GitHub Actions source,
strict current-main condition, workflow triggers, conversation state and logs.
Fix the cause on a feature branch, merge current main if needed and rerun checks.
Do not remove the aggregate, skip mandatory tests, lower policy requirements,
enable force pushes/deletion or routinely push directly to main.

Existing repository administrators retain Always allow solely for separately
authorized incident recovery. Record the incident-specific authorization, reason,
affected commit and settings readbacks; restore ordinary operation and verify
CI and Pages afterward. Do not use bypass to prove it exists. No bypass or
protection/permission change is authorized for this documentation integration.

## Pages observation and direct-settings limitation

The managed Pages workflow remains active. Before final integration, successful
deployment run **41544608686** for main 6f86ead and its actual main/root build logs,
custom-domain URL, public homepage/source and owner Analytics were independently
verified. Automatic deployments caused by this documentation merge are recorded
accurately in the final delivery record, with all 18 released pages and registry
checked for accessibility and unchanged source.

The saved Pages configuration could not be directly inspected: unauthenticated
GET /pages returned404, and the connector did not expose that endpoint. Therefore
current saved source-branch/path, build-type, HTTPS and domain-setting fields are
**unverified as saved settings**. Do not claim every Pages field was checked.
Workflow/deployment/public evidence is separate and does not imply that direct
configuration readback succeeded. No Pages setting was modified. Pages remains
independent of functional CI; branch protection is not main-deployment gating.

## Historical preparation, superseded by the owner's ruleset

Before 2026-11-03T00:58:27Z, the readback for main 6f86ead showed protected=false,
required checks off and no rulesets/active rules. The original PR 15 proposed a
classic main rule because the connector could not configure administration
settings. Local authentication was unavailable; no credential extraction, scope
expansion or settings mutation was attempted. That earlier observation/proposal
is retained in the historical handoff/changelog and original commits. The owner
then created the current repository ruleset. The classic setup proposal is no
longer a pending action; do not apply it on top of the verified active ruleset.

## Remaining scope

Four original specialist tools have explicitly NOT RUN isolated-logic adapters;
their mandatory structure/browser scopes pass. Native installed-shortcut GUI
launch is not newly certified by this documentation task. Structural dashboard
reports are not functional test totals. Existing 18 utilities, registry/lifecycle,
homepage/Analytics/CNAME, tests/workflow, release audits and dashboard/shortcuts
remain unchanged. Task 10 is the next development task and awaits separate scope;
do not begin it automatically.

References: [active ruleset](https://github.com/Juster06/micro-tools-hub/rules/26413762),
[ruleset/effective-rules API](https://docs.github.com/en/rest/repos/rules),
[available rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets).
