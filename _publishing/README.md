# SEO Task 2D.2 — internal documentation publishing correction

Baseline main: `1634bff8449db3a5398f5e0c1d070098b3cd2f16` (PR #49 merged).
Finding SEO-2D1-01 remains a production blocker until authorized deployment and
independent public verification. This branch is corrective development only.

## Cause and decision

Production Pages workflow 42440717015 used `actions/jekyll-build-pages` revision
`44a6e6beabd48582f863aeeb6cb2151cc1716697`, container v1.0.13,
github-pages 232, Jekyll 3.10.0 and jekyll-theme-primer 0.6.0.
The mandatory optional-front-matter plugin renders Markdown without front matter.
The theme adds a self canonical; no noindex was present. The artifact contained
both HOMEPAGE_DESIGN.html and HOMEPAGE_DESIGN.md. Public verification also found
the extensionless HTML alias. No prior Jekyll config or .nojekyll existed.

Option A is selected: an explicit `_config.yml` exclusion leaves the original
document and its Git references intact. Jekyll 3 replaces the exclude array;
therefore Gemfile, Gemfile.lock, node_modules, vendor/bundle/, vendor/cache/,
vendor/gems/, vendor/ruby/ and Pages' CNAME exclusion are all retained. Only the
design document and this correction's new Python test are additionally excluded.
New policy, approval and documentation use the default-excluded `_publishing/`
directory; the bootstrap's filename begins with an underscore.

Option B, moving the document under an underscore directory, would also avoid
publication, but changes its path and references in the historical source chain.
Explicit exclusion is narrower while its replacement-array risk is tested.
No broad route removal, robots rule, noindex rule or pipeline disable is used.

Sources: [Jekyll 3.10 defaults](https://github.com/jekyll/jekyll/blob/v3.10.0/lib/jekyll/configuration.rb),
[Pages 232 configuration](https://github.com/github/pages-gem/blob/v232/lib/github-pages/configuration.rb),
[production builder](https://github.com/actions/jekyll-build-pages/blob/44a6e6beabd48582f863aeeb6cb2151cc1716697/action.yml).

## Generated-output gate

The existing required Node job now builds the actual Pages output, before npm
installs or other test reports, using the production action revision. There is
no deploy step or Pages write permission. The build and verification must both
succeed for that job and the unchanged four-job aggregate to pass.

`python _publishing/verify_site.py --site reports/pages-site --report reports/ci/pages-output.json`

The policy is reviewed from production artifact 13601019321. It expects exactly
1,130 files: the prior 1,132 minus the two design-document files. All 137 remaining
HTML outputs are inspected: 89 canonical pages and 48 historical routes. These
48 are retained for compatibility, not newly approved for indexing. Their route,
canonical, robots/noindex and refresh metadata must remain unchanged. Changing
that historical exposure requires a separate review.

The 89 canonical HTML files, source CSS, consent script, sitemap and robots must
match source bytes. The theme stylesheet has its production hash pinned. The
original design document is hash checked in Git. Any new generated file fails,
including Markdown HTML, raw Markdown, an explicit HTML file, an extensionless
route or a redirect. Unknown noindex pages also fail: noindex is not permission
to publish internal material. An exact Markdown input list prevents a new file
using a permalink to overwrite an existing historical route undetected.

No inventory or source approval is learned from the candidate output in CI.
Updating either requires an explicit reviewed change. Unit mutation tests cover
metadata, additional/missing output, internal aliases, defaults, source inventory,
assets, discovery files and current/historical approval tampering.

## Source history

`SEO_TASK_2D2_SOURCE_APPROVAL.json` is the new current source record. It binds all
current inputs plus the unchanged Task 2D manifest/bootstrap, which retain their
original meaning. Python and Node gates select the new record. Historical full
preimages still reconstruct the same frozen Task 2A/2C/consent evidence; no dated
audit or release record is rewritten. `parent_revision` retains the inherited
homepage layer's Task 2C parent; `publishing_parent_revision` identifies this
correction's immediate main baseline. The new bootstrap pins the new manifest;
neither is circularly included in its own dependency list.

## Validation and limitations

The external dated development report and PR record actual local/hosted results
for the containing commit, including the real Jekyll artifact. The four existing
CI jobs continue to exercise 87 tools, homepage search/eight groups/no-JavaScript
links, consent and LIVE-03. No assertion or timeout is relaxed.

Local Ruby/Docker is unavailable; real publishing verification runs on the
existing GitHub-hosted Ubuntu job. Artifact checks do not prove public removal
or CDN alias behavior. Performance timing remains INCONCLUSIVE / DEFERRED; the
owner's local memory investigation is parked. Image Compressor timing remains
an UNRESOLVED RELIABILITY OBSERVATION. No benchmark or tool change is included.

## Rollback and next authorized step

Before merge, close/revise this PR if necessary; main is unchanged. After an
authorized merge, an owner-authorized revert of the complete correction restores
the old config/gates and source approval together, but re-exposes the document;
do not apply a partial rollback that bypasses current-source approval.

After separate merge/deployment authorization, verify the exact deployed commit,
successful Pages deployment and four CI jobs. HTTP-check HOMEPAGE_DESIGN.html,
HOMEPAGE_DESIGN and HOMEPAGE_DESIGN.md plus redirects/alternate routes; they must
no longer serve the internal document. Verify all 89 canonical pages, 89 sitemap
URLs, robots, 87 tool links, homepage search/navigation, CSS, consent and LIVE-03.
Record a new dated public report. Only then reconsider Task 2D completion.
Task 26 remains paused and Task 2E is outside this task.
