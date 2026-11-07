# Production CSS pilot — SEO Task 2C

This branch is a **development candidate, not a deployment**. It starts from
`cf443c3b1facc2ae422fc6c55d546528671be1d0`, the independently verified SEO Task 2A
baseline. The read-only Task 2B report supplied the architecture and budgets.
No tool status, release date, route, analytics behavior or historical audit is
changed. Task 26 remains paused. Merge and deployment need separate owner approval.

## Scope

Only these pages replace the browser Tailwind script with a local stylesheet:

1. `index.html`
2. `text-cleaner/index.html`
3. `json-formatter/index.html`
4. `csv-viewer/index.html`
5. `image-color-picker/index.html`
6. `vat-calculator/index.html`
7. `batch-filename-planner/index.html`

Their utility classes, inline CSS, JavaScript, IDs, controls, canonical metadata
and consent loader remain. Minimal statements that previously described a
Tailwind CDN request are corrected to describe first-party styling; the exact
literal substitutions are recorded in current-source approval. No other content
or visual redesign is included. The other 81 released tool pages retain their
previous delivery; `social-counter/index.html` is a read-only legacy probe.
The privacy page, sitemap, robots, registry, CNAME and consent engine are unchanged.

## Compiler, dependencies and source scanning

The public `@tailwindcss/browser@4` response resolved to **4.3.5** during this
task. The development package therefore pins both `tailwindcss` and
`@tailwindcss/cli` to exactly **4.3.5**, with a lockfile and integrity records.
They are MIT-licensed development dependencies. The generated CSS retains the
compiler license notice. There is no new visitor-side framework, compiler,
font, icon library, service worker, analytics library or account service.

Use the repository's pinned CI Node **24.22.1** runtime. The small package lives
in `scripts/styles/`, independently of the existing browser acquisition package.
Install from the lock without running package lifecycle scripts:

```sh
npm ci --prefix scripts/styles --ignore-scripts --no-audit --no-fund
```

`styles/sources.json` explicitly lists the 89 existing public HTML sources and
`assets/consent.js`, including inline scripts that contain complete utility class
tokens. The scanner reads these 90 files only. Audit records, reports, temporary
fixtures, node_modules and provisional tool scaffolds are not scanned.
The script validates this list against the unchanged released registry.

The CSS input uses `source(none)`. The builder stages only approved source text
and supplies an explicit source directory to the pinned CLI. Page-specific CSS
and dynamic custom classes stay inline; no general-purpose unused-CSS purge is
introduced. A class assembled dynamically must be made explicitly discoverable
and tested before a future approved migration. Do not add a blanket safelist.

## Build and read-only verification

```sh
# Deliberate generation: writes generated CSS, the build record and pilot links.
node scripts/build_styles.mjs

# Validation: compiles in isolated temporary scratch, compares, writes no repo files.
node scripts/build_styles.mjs --check

# Independent current-source and asset approval, without npm/compiler execution.
python scripts/css_overlay.py --check --json

# Existing SEO and project checks.
python scripts/validate_seo.py --json --no-report
python scripts/project_status.py --check-only --no-report --json
```

Do not regenerate immediately before validating a proposed change: that would
hide stale generated output. `--check` must fail when source inputs, compiler
configuration, the lock, output bytes or delivery references are stale.

The minified asset is `assets/css/site.<first-16-SHA256-hex>.css`.
`styles/build-manifest.json` records full hashes of scanner sources, configuration,
builder, registry, package and lock, plus the generated file, exact bytes and
gzip size. Text input hashes normalize CRLF to LF only; all other characters and
trailing content remain significant. The generated stylesheet uses exact byte
hashes. Records contain no clock timestamp or machine path, so unchanged inputs
produce unchanged artifacts. Two builds and checks must agree.

The narrow `.gitattributes` rule `assets/css/*.css text eol=lf` preserves exact
stylesheet bytes on Windows checkouts that otherwise convert text to CRLF.

Generated CSS is committed for the existing main/root GitHub Pages deployment.
Pages needs no compiler or new deployment workflow. Content-addressed filenames
avoid stale asset identity; retain previous referenced assets during rollout
and rollback. Cache response headers are controlled by Pages, not promised here.
The reviewed gzip ceiling is **50 KiB**, with **30 KiB or less** preferred.
Never remove required styles merely to meet a byte budget.

## Exact current approval and historical evidence

`audit/SEO_TASK_2C_SOURCE_APPROVAL.json` is new evidence for this candidate.
It binds the seven page transformations, exact starting/preimage hashes, current
candidate hashes, CSS asset, build/lock inputs and required validation/test/CI
dependencies. The separate reviewed bootstrap pins its identity; it is an
explicit source trust anchor, not a signature or an automatic approval service.

`scripts/css_overlay.py` and its Node counterpart first validate the complete
current dependency closure and route/consumer set. Only then may they reconstruct
the exact starting source and call the unchanged historical SEO/consent projection.
Current validity and historical reconstruction are separate checks. Old published
hashes certify old published bytes, not the new stylesheet revision.

Large preservation batches capture one fully validated immutable snapshot and
reconstruct historical evidence from those exact bytes. Snapshot readers bind
the repository root and approved paths, reject altered source arguments, and
do not approve later filesystem changes. Live current-source checks reread and
hash the complete dependency closure; there is no cross-call mtime cache. This
keeps existing test deadlines without treating a cached result as live approval.

Preservation tests use a bounded `git cat-file --batch` reader for immutable
historical blobs. It requires full revision identities and safe relative paths,
and checks blob type, framing, size and object hash. This removes repeated Git
process startup while retaining the original assertions and deadlines. Current
generated progress counts are compared directly from their documentation;
documentation is not passed through the runtime-source snapshot.

Existing dated audits, frozen Task 17 and SEO Task 2A manifests, and their validator
implementations remain unchanged. Preservation consumers use the new narrow
dispatcher; old overlay-specific tests still exercise exact historical source.
Negative tests cover missing/wrong/duplicate delivery, altered CSS/build/lock/
manifest, retained compiler, modified canonical/consent/logic/history, extra
routes or consumers, trailing changes and unsafe paths/symlinks/junctions.

A future change to approved runtime/build/test inputs intentionally invalidates
the current approval. It needs a new reviewed candidate record and actual tests;
copying on-disk hashes into the manifest is not an approval workflow. Do not
rewrite historical evidence, broaden normalization or bypass validators.

## Required CI

The existing Windows Python, Ubuntu Node and Ubuntu Chromium jobs remain, with
the same action/runtime pins, permissions, triggers, deadlines and required
aggregate. Python performs the independent current-source check. The Node job
installs only the locked development compiler and runs the read-only CSS build
check before regression tests. New test files join the explicit coverage map.
The existing aggregate requires every functional job to succeed.

Development results and omissions are recorded in
`audit/SEO_TASK_2C_DEVELOPMENT_VERIFICATION.json`. The GitHub PR supplies exact-head
hosted results; old test totals are never substituted for a new run.

## Performance, visual and privacy acceptance

Compare the same seven baseline/candidate pages with the same serving rules,
browser, viewport, caching and observation window. Target three cold and three
warm samples per page/configuration. Record FCP, last observed LCP candidate,
initial CLS, resource bytes and compiler requests. Report memory pressure,
timeouts and unstable timing as **INCONCLUSIVE**. These are laboratory samples,
not field Core Web Vitals; no field INP, ranking or traffic claim is made.

Hard gates are zero browser Tailwind requests on pilot pages, successful matching
first-party CSS, no new tracking, and no unexpected functional/style regression.
Compare default/focus/error/result/file/canvas/copy/download states, desktop,
mobile, 320px reflow and print. Distinguish scripted zoom/text-size probes from
physical devices or assistive-technology testing. Existing source-bound behavior
and consent suites remain required.

The existing homepage consent panel can hide the focused search field in the
sampled mobile state (Task 2B LIVE-03). **Task 2C does not fix it or claim WCAG
conformance.** Do not make it worse. Task 2D must correct homepage placement;
Task 2E extends verified shared layout to tool families with all-consumer checks.
The measurement ID remains `G-XDHPQYJ5CH`; before-choice/reject/withdraw blocking,
deduplicated consented events, sanitized page URLs and input privacy remain intact.

## Rollback and post-merge verification

Keep this PR open for owner review after all four checks pass. Do not merge,
deploy manually, use administrator bypass, change account settings or schedule
autonomous SEO operations.

If an authorized deployment later needs rollback, revert the pilot as one coherent
change: HTML references, CSS asset selection, build configuration and current-source
approval. Retain dated evidence and unrelated work. A rollback can restore known
baseline issues; report them rather than claiming remediation.

After a separately authorized merge, record the exact deployment commit and
independently fetch all 89 canonical HTML pages, sitemap, robots, aliases and
essential assets. Verify pilot CSS hashes/MIME/references and absence of browser
compiler requests, sample tool functionality and consent, repeat controlled lab
checks on a stable host, and record a new dated public-verification artifact.
Development PASS is not public deployment verification.
