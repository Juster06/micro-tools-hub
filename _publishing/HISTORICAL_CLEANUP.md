# SEO Task 2E.1 historical publishing correction

Development baseline: `3d78c267b479690331fd618e2982c51cbdc6da4b`, PR #50 merged.
This correction retires the exact difference between the former publishing
policy's 137 HTML outputs and 89 approved canonical pages: 48 routes.
The owner authorized all 44 internal documentation/template pages and four
verification guides (task22-public, task24-public, task25-public and task21).
The complete mapping, source hashes and output paths are in output-policy.json.

## Source and dependency review

There are 45 Markdown sources (including README index generation) and three
explicit HTML template sources. All 48 original sources remain unchanged in Git.
No approved canonical page references a retired route, and none of its directly
referenced runtime assets is removed. The retained development test references
to templates and roadmap files continue to read the original local Git sources.
Runtime directories are not excluded. Existing directory and host aliases for
approved tools retain their index.html backing files and canonical hashes.

The previous production artifact contains both representations of all 45
Markdown sources. Explicit subtraction therefore predicts 93 removed files and
1,037 retained files. This is an expectation derived from production; the actual
pinned Jekyll artifact must match it before development can pass. The policy is
never generated from candidate output during validation.

## Publishing and approval safeguards

_config.yml retains every Task 2D.2 exclusion, including Jekyll 3 defaults,
GitHub Pages CNAME handling, HOMEPAGE_DESIGN.md and the existing publishing test.
It adds only the 48 exact source files. No directory exclusion, pipeline switch,
.nojekyll or robots/noindex workaround is introduced. The existing CI Node job
still uses actions/jekyll-build-pages at revision
44a6e6beabd48582f863aeeb6cb2151cc1716697 and builds only an isolated artifact.

The new source approval binds the current config, policy, guard and tests while
retaining the unchanged Task 2D.2 manifest/bootstrap and a frozen copy of its
output policy. The original Task 2A/2C/2D and consent history remain intact.
The inherited parent_revision and publishing_parent_revision still describe
their original layers; historical_publishing_parent_revision names this baseline.

Every retired HTML/raw/alternative output fails the new inventory. All 89 public
canonical bytes, discovery files and assets retain their production hashes.
Negative tests for former historical-route policy are preserved using an isolated
legacy fixture; they do not permit those routes in the current approved policy.
Additional tests enforce every retirement, canonical/runtime removal prevention,
retired-source hashes and the predecessor chain. No test timeout is relaxed.

## Historical preservation and privacy

This internal document serves as the new development handoff so the 48 original
source documents, including historical SESSION_HANDOFF.md and CHANGELOG.md,
remain byte-for-byte preserved after checkout normalization. The new external
report records actual tests and hosted job identities for the containing commit.

The repository remains public. Pages exclusion does not remove GitHub source or
search-engine caches. Scoped pattern review found operational details in some
retired documents and no credential-pattern matches; that is not a comprehensive
secret or personal-data certification. No sensitive values are reproduced,
history rewritten or credentials rotated.

## Rollback and next step

Review the development PR and all four required checks. No merge or deployment
is authorized by this task. Preserve prior worktrees, edits and reports.
If rollback is required after a separately authorized merge, revert the complete
correction and its approval selection together; that restores historical Pages
exposure. Do not partially remove a guard to bypass validation.

After an authorized merge, independently verify the exact main, successful Pages
and all four post-merge jobs; check all 48 HTML URLs, 45 raw Markdown URLs,
extensionless/directory aliases and redirects with cache-aware HTTP evidence.
Compare the deployed inventory, all 89 canonicals, 87 tools, sitemap, robots,
runtime assets, homepage search/navigation/no-JavaScript access, consent and
LIVE-03. Save a new dated report before claiming production cleanup.

Performance timing remains INCONCLUSIVE / DEFERRED and the memory investigation
is parked. Image Compressor timing remains an UNRESOLVED RELIABILITY OBSERVATION;
no code/assertion change. LIVE-03 retains its previous scoped production result
and existing required browser regressions. No Task 26 or tool redesign is included.
