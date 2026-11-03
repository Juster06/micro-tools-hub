# Main branch protection — requested policy and owner setup

## Current state: NOT CONFIGURED (2026-11-03)

Task 9.5 Stage D authorizes the policy below. It has **not been applied**.
Actual main `6f86ead99c1e7183b625349ca4d4e2f9da804186` is unprotected;
required-check enforcement is off/empty, repository rulesets and active main rules
are empty. Functional CI is operational: main push run **41544609839** passed all
four jobs on that exact commit; Pages run **41544608686** succeeded separately.

The connected Juster06 account has repository admin permission. However, the
available GitHub connector exposes no branch-protection/ruleset administration
endpoint. Installation metadata does not disclose its Administration-write grant;
account admin rights do not establish that grant. No denial response or missing
scope is invented. The local GitHub CLI is unavailable and standard GH_TOKEN /
GITHUB_TOKEN authentication is absent. Plugin discovery found only the already
installed GitHub integration for this capability. No credentials were extracted,
permissions expanded, undocumented API called or security boundary bypassed.
An owner action or a supported authenticated administration interface is required.

This guide is a proposed configuration, not executable enforcement. A merged
Markdown file cannot configure GitHub settings. Do not report Stage D complete
until actual settings have been applied and read back.

## Exact policy

Use **one classic branch protection rule matching exactly `main`**. This is the
simplest supported method and preserves the requested emergency admin bypass.
Do not add an overlapping ruleset or match unrelated branches.

| Setting | Requested value |
| --- | --- |
| Require a pull request before merging | Enabled |
| Required human approvals | Zero; Require approvals disabled |
| Require status checks before merging | Enabled |
| Required check | `Required functional checks`, source GitHub Actions |
| Require branches to be up to date | Enabled / strict=true |
| Require conversation resolution | Enabled |
| Allow force pushes | Disabled |
| Allow deletions | Disabled |
| Apply requirements to administrators / disallow bypass | Disabled; retain emergency admin bypass |
| Require Pages deployment | Disabled; no Pages job is a required check |
| Additional signing, linear-history or merge-queue requirements | Not added |

The actual current check-run API reports the exact context above with GitHub
Actions App ID **15368** (`github-actions`); do not confuse it with the installation
ID or require the individual Pages build/deploy contexts. Repository admin bypass
is intentional: this policy constrains the ordinary path, not the emergency admin
path. Agents must still use ordinary PRs and passing CI; do not exercise bypass
merely to test availability.

## Owner setup in GitHub

1. Open [repository branch settings](https://github.com/Juster06/micro-tools-hub/settings/branches)
   while signed in as the repository owner/admin.
2. Inspect existing protection and rulesets first. If another actor has configured
   a rule since this snapshot, compare it and reconcile deliberately; do not
   overwrite legitimate newer settings or create overlap.
3. Add a classic protection rule for the literal branch pattern `main`.
4. Enable Require a pull request before merging. Leave Require approvals and
   other review-count requirements unchecked (zero mandatory approvals).
5. Enable Require status checks to pass before merging and Require branches to
   be up to date before merging. Select **Required functional checks** from
   **GitHub Actions**. Do not select Pages/deploy/build.
6. Enable Require conversation resolution before merging. Leave Allow force
   pushes, Allow deletions and Do not allow bypassing the above settings unchecked.
   Do not add unrelated optional restrictions.
7. Save, reopen the rule and compare every requested setting. If an option cannot
   be represented, stop instead of substituting a weaker/different policy.

An owner with an already authenticated administration client may alternatively
use the documented `PUT /repos/Juster06/micro-tools-hub/branches/main/protection`
endpoint with the reviewed body below. It requires Administration-write. Read
current settings first and avoid replacing newly configured rules. No API token
belongs in this repository, documentation, issue, PR or chat.

```json
{
  "required_status_checks": {
    "strict": true,
    "contexts": [],
    "checks": [
      {
        "context": "Required functional checks",
        "app_id": 15368
      }
    ]
  },
  "enforce_admins": false,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": false,
    "require_code_owner_reviews": false,
    "required_approving_review_count": 0,
    "require_last_push_approval": false
  },
  "restrictions": null,
  "required_conversation_resolution": true,
  "allow_force_pushes": false,
  "allow_deletions": false
}
```

The non-null pull-request-review configuration with approval count zero retains
the PR requirement. `restrictions: null` adds no organization-specific push
allowlist. Administrator enforcement is false by explicit owner policy.

## Required readback and safe enforcement verification

Use the actual GitHub UI or documented authenticated GET endpoints:

```text
GET /repos/Juster06/micro-tools-hub/branches/main
GET /repos/Juster06/micro-tools-hub/branches/main/protection
GET /repos/Juster06/micro-tools-hub/rulesets?includes_parents=true
GET /repos/Juster06/micro-tools-hub/rules/branches/main
GET /repos/Juster06/micro-tools-hub/commits/HEAD_SHA/check-runs
```

Confirm protected=true; a non-null PR requirement with zero approvals;
required_status_checks.strict=true; exactly the named aggregate check from App
15368; conversation resolution enabled; force pushes/deletion disabled;
enforce_admins.enabled=false. Verify that no unrelated rule was created. Save a
dated sanitized settings readback; an API success response alone is insufficient.

For a harmless documentation PR, inspect the ordinary merge requirements while
the aggregate is pending and again after it succeeds. Resolve conversation
threads and ensure the head is current with main. Do not merge a failing PR,
make intentionally failing utility changes, force-push/delete a branch, or click
an administrator bypass button. A signed-in admin's ability to override is not
proof of ordinary enforcement. If no non-bypass identity or ordinary merge-state
view is available, report that observation limit rather than changing account
permissions to manufacture a test. Preserve any actual pending/blocked and
passing/eligible readbacks that are available. Existing main/PR test runs prove
CI execution, not policy enforcement.

At the Stage D preparation checkpoint, enforcement testing is **NOT RUN** because
no protection has been applied through the available interface. No failing PR,
bypass operation or destructive test was performed. A passing documentation PR
only demonstrates continuing functional CI; it cannot establish required-check
enforcement while main is unprotected.

## Future Codex PR workflow

- Fetch origin and read the current handoff plus actual main protection before
  work. Use a feature branch; keep production scope bounded and private/generated
  artifacts out of commits. Do not assume account admin means bypass is intended.
- Run relevant local tests and project validation; publish reviewed exact content
  without force pushes. If publishing identities differ, independently fetch and
  verify complete tree equality while preserving original commits.
- Open a PR targeting current main. Wait for the exact current head's Python,
  Node, real Chromium and **Required functional checks** jobs. Inspect actual
  results/counts/artifacts; resolve conversations.
- If behind main, merge current origin/main into the feature branch, resolve and
  review conflicts, push normally and rerun CI. Do not rewrite original history
  or rely on an earlier head's passing checks. An update-to-main requirement is
  not satisfied by an old run on a different commit.
- Merge only with owner authorization, an expected-head guard, no blocking
  requirements and the ordinary path. Verify resulting main-push CI and the
  independent automatic Pages behavior. Never use emergency admin bypass merely
  because it is available. Do not silently lower requirements to unblock a PR.

## Release metadata

Publication/lifecycle evidence still requires separate owner-authorized release
verification. Submit registry, release-audit, homepage availability and derived
tracking updates through a reviewed feature PR with current passing CI, even
when the release consists only of metadata/docs. Do not push release metadata
directly to main, treat a merged tool as RELEASED, or equate Pages/structural PASS
with public functional publication evidence. Verify main CI, automatic Pages and
actual expected public source/behavior separately after the authorized merge.
This task does not authorize a new utility or lifecycle change.

## Recovery and emergency bypass

For a stuck required check, inspect the exact head, context spelling/App source,
workflow triggers and logs; fix the cause on a feature branch and rerun. Bring
the PR current with main, resolve discussions and verify again. Do not remove
the check, weaken tests or enable force pushes/deletions as a routine workaround.

If legitimate emergency recovery is needed, the existing repository admin may
use its retained bypass only with explicit incident-specific owner authorization.
Record the reason, affected commit and readbacks; restore ordinary operation and
verify CI and Pages afterward. Do not test bypass by using it now. Rule edits,
removal, added bypass actors, permission expansion and materially different policy
require separate authorization. No permanent credential should be created or
shared merely to complete this setup.

## Limits and references

Classic protection and branch rulesets are supported on public repositories with
GitHub Free; no paid upgrade is required for this requested branch policy.
The exact subscription and connector Administration-write grant were not exposed.
Pages deployment remains independently triggered by main; protection alone does
not make Pages wait for main's functional CI. No utility, CI workflow, deployment
configuration, registry/lifecycle, dashboard or shortcut changes are included.
Task 10 remains unstarted.

Official references: [protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches),
[documented update/readback API](https://docs.github.com/en/rest/branches/branch-protection),
[managing a protection rule](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule).
