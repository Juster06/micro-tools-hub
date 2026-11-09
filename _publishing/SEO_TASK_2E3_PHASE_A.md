# SEO Task 2E.3 Phase A — controlled publishing cleanup

This is the successor development checkpoint to the recovered Task 2E.2 audit
of 8 November 2026. Base: `34992b8f8ac3e73efbea820bb18c96dae145ff19` (PR #51).
Branch: `seo/task-2e3-pages-cleanup`. Authorization covers development and a
review PR only. Merge, production deployment and auto-merge are not authorized.

## Exact scope

The unchanged recovered candidate record is preserved in
`SEO_TASK_2E2_CLEANUP_CANDIDATES.json`; its original authorization field records
the historical audit, not the owner's subsequent Phase A instruction.
`SEO_TASK_2E3_SCOPE.json` binds its checksum, the production artifact, all 841
excluded output hashes and all 196 retained output hashes. Approved groups are
234 audit, 85 scripts, 513 tests, six styles, two template fragments and one
registry file. Exclusions are individual file paths, never directory wildcards.

The expected real Jekyll output is 196 files: 89 canonical HTML pages and 107
non-HTML files (90 owner-review holds, 11 runtime assets and six public resources).
All 87 released tools, discovery files, runtime/worker/data/CSS bytes, consent,
accessibility, canonical routes and existing aliases remain unchanged. The
previous 48 HTML and 45 raw Markdown retirements remain absent. Source files
remain in Git for builds, tests, the dashboard and historical evidence.

## Approval and historical preservation

The Task 2E.1 `output-policy.json`, source approval and bootstrap remain frozen.
The Task 2D.2, homepage, CSS, SEO and consent evidence also remain unchanged.
The new output policy and source approval are explicit successors. Python and
Node select the same new bootstrap; historical projection requires the complete
current dependency closure first. The existing runtime/source transformations
retain their historical baseline and approved public bytes.

This document supersedes the old manual next-action text for this task without
rewriting frozen `SESSION_HANDOFF.md`, README, roadmap, registry or old audits.
The compressed theme CSS under `fixtures/` is exact production artifact data for
guard mutation tests, not evidence that a new Jekyll build has succeeded.

## Deployment boundary and validation

Authenticated baseline inspection confirmed Pages publishes `main` at `/` using
the existing legacy build. The only checked-in workflow has `contents: read`,
runs for PRs targeting main, main pushes or manual dispatch, and builds an
isolated artifact with the pinned production Jekyll action. It has no deployment
step or Pages write permission. Recheck this boundary before branch publication.

Required verification: complete Python, Node and Chromium partitions; 87 browser
profiles and both neutral templates; consent/homepage/accessibility and worker/
download regression; seven-page CSS freshness; unchanged historical negative
fixtures and new exact-delta, retained-byte, alias and tamper tests. The pinned
actual Pages build must match all 196 retained hashes and exclude all 841 paths.
No inventory learned from candidate output, assertion relaxation or timeout
increase is permitted. A synthetic guard fixture is not real artifact evidence.

Execution results, failures/omissions and exact commit/workflow identities belong
in the separate development report and PR. This specification does not claim
completed testing, public removal, deployment, ranking or performance gains.

## Remaining owner decisions

All 90 review files remain unchanged and published. `audit/TASK_22_SECURITY_REVIEW.json`
continues to contain the five workstation-path occurrences reported by Task 2E.2;
values must not appear in new logs or reports. This LOW privacy finding remains
open. No confirmed credential disclosure was established. Pages exclusions do
not remove public GitHub source/history or caches. Redaction and review-file
exclusion require separate authorization.

Performance timing remains INCONCLUSIVE / DEFERRED. Image Compressor timing
remains an UNRESOLVED RELIABILITY OBSERVATION. LIVE-03 retains its scoped resolved
production result. Task 26 stays paused; no tool or analytics work is included.

## Next action and rollback

Complete the required development checks; stop and report a failed required gate.
After passing verification, prepare a draft PR for owner review and stop. Do not
merge or deploy. After any separately authorized deployment, verify actual live
routes and aliases, canonical/runtime bytes, discovery and consent behavior.
Rollback requires the complete configuration/guard/approval selection together;
never bypass a guard or partially restore a policy. The containing development
commit is identified by the branch/PR head, not a self-referential hash here.
