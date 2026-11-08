# SEO Task 2D — Option B homepage development

This is a development proposal based on publicly verified main
`20ecae29a1f20d7903946d6cf00c3897307ee766`. Task 2C's required CI rerun
passed; its original Image Compressor wait failure remains an unresolved
reliability observation. Performance measurements remain deferred. Task 26
remains paused. No merge or deployment is authorized by this document.

## Scope and generation

The homepage adopts the reviewed Task 2B Option B palette, system fonts,
compact header, responsive disclosure navigation, local search and eight
presentation categories. `styles/homepage-directory.json` preserves the
reviewed mapping and aliases for exactly 87 RELEASED tools. It does not
change registry categories, routes, statuses or publication records.

`scripts/build_homepage.py` emits ordinary static HTML with all 87 primary
directory links, category anchors and a content-named first-party stylesheet.
JavaScript adds filtering; no-JavaScript visitors retain navigation and links.
Search is transient in page memory, uses textContent, and sends no telemetry.
Normalized phrase matching extends the original name search to reviewed descriptions
and aliases. Counts update synchronously in a polite live region. The existing
clearSearch identifier and readable card text boundaries are retained.
Clear resets both search and category. Category anchors restore the complete
directory before navigating so an earlier filter cannot hide their targets.

The stylesheet is sourced from `styles/homepage.css`; behavior is sourced
from `styles/homepage.js`. There are no new packages, external fonts, runtime
frameworks, dark mode or new indexable category pages. The original shared
Tailwind CLI remains pinned. The regenerated shared CSS drops utilities no
longer required by the homepage; the other six pilot pages change only their
CSS asset reference. All six require computed-style and functional regression
coverage. Their tool logic remains unchanged.

Deliberate generation order (inspect every resulting diff):

```sh
python scripts/build_homepage.py
node scripts/build_styles.mjs
python scripts/build_homepage.py
node scripts/build_styles.mjs --check
python scripts/build_homepage.py --check
```

The second homepage generation incorporates the shared CSS content name.
CI runs only the check commands; it never regenerates source to hide drift.

## LIVE-03 and privacy

Homepage-scoped selectors place the existing consent panel and Privacy settings
button in normal document flow after the footer. This removes their fixed
overlay geometry on the homepage. The shared `assets/consent.js` runtime is
byte-identical to the baseline: acceptance, rejection, expiry, withdrawal,
deduplication and focus restoration keep their existing implementation.
Equal accept/reject controls remain available; tools never require acceptance.
Long consent text and controls wrap at enlarged text sizes.

Browser evidence must show focused search/navigation remain visible with the
panel open at 320, 390, 768 and desktop widths, normal and enlarged text.
Automated labels, contrast, focus, reflow and target checks do not establish
full WCAG conformance or replace screen-reader/manual device testing.
The project prefers 44 CSS-pixel targets; WCAG 2.2 AA SC 2.5.8 has a distinct
24 CSS-pixel minimum with exceptions. No full conformance claim is made.

## Current source approval and immutable history

`audit/SEO_TASK_2D_SOURCE_APPROVAL.json` is a new, separately pinned current
candidate record. `scripts/homepage_approval_identity.py` is its reviewed
literal hash trust anchor, not a cryptographic signature. The existing
Python/Node CSS approval entry points now select this new record. The frozen
Task 2C manifest and bootstrap, all historical audits, Task 2A projectors and
consent projector remain unchanged and bound as dependencies.

The new record binds the complete existing dependency closure plus homepage
data, generator, CSS, JavaScript, generated asset and tests. It records the
immediate parent main SHA. Its historical projection base remains the same
pre-CSS commit so existing preservation assertions keep their original meaning.
Changed approved files use exact, hash-bound full preimages; no broad stripping
or semantic normalization approves arbitrary source. All current dependencies
must validate before a preimage is returned. Snapshot readers remain bound to
root/path/source and are historical evidence, not live authorization caches.
The project gate rechecks live bytes before returning.

New negative tests reject changes to homepage source, data, assets, generator,
new manifest/identity and frozen predecessor. Existing mutation, path, route,
consumer, trailing-byte, bootstrap and snapshot assertions remain required.
Any future change to bound inputs requires separate reviewed current evidence;
updating the trust anchor alone does not constitute behavioral verification.

## Validation and limitations

Run complete required Python and Node partitions and the required hosted
Chromium partition. Browser workloads remain sequential. Targeted homepage
tests use isolated local contexts and synthetic intercepted Google responses;
they verify site-side gating, not real Google ingestion. The old consent suite
also remains required. No local memory investigation, large-image benchmark,
speed claim, traffic claim or ranking claim is included.

## Rollback and public verification

Before merge, close the PR to retain production unchanged. After an independently
authorized deployment, a rollback must be a separately reviewed coherent revert
of the homepage, generated styles/references, current approval, build/test wiring
and current documentation. Retain all frozen evidence and prior CSS assets.
Rollback restores the prior known LIVE-03 obstruction; disclose that limitation.

After authorized merge, verify the exact commit, successful Pages and mandatory
CI, then independently fetch all 89 canonical HTML pages, sitemap, robots and
assets. Check all 87 directory destinations, eight groups, search/navigation,
no-JavaScript access, CSS hashes/MIME, six existing CSS consumers and isolated
consent behavior. Reproduce the LIVE-03 focus test on public mobile layouts.
Development evidence alone must not be described as a public accessibility fix.
