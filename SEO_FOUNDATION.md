# Technical SEO foundation — SEO Task 2A

This is a local development proposal from main
`7cdd6f43800fc1ae01ee597d9bab1a7a597f7f32`. It does not establish a new public
deployment or Google indexing. Merge and deployment need separate owner approval.

Development results are recorded in
[SEO_TASK_2A_LOCAL_VERIFICATION.json](audit/SEO_TASK_2A_LOCAL_VERIFICATION.json).
Local Python covered 256 discovery tests plus 10 focused overlay tests; final
engine changes also passed 27 focused tests. Node passed 536 tests and all 83
logic profiles. The local Edge browser aggregate hit its unchanged 900-second
limit after 481 passes and one browser-command timeout failure, so it is
explicitly incomplete. The PR must
pass the complete required hosted Chromium checks before owner review is final.

## Canonical policy

- Origin: `https://everydaydigitalbox.com` (HTTPS, apex host, no credentials/port).
- Homepage: `https://everydaydigitalbox.com/index.html`. Existing logo and Back to
  Hub links already use this route. The `/` alias keeps working and serves the
  same static canonical annotation; no redirect or body-link migration is needed.
- Released tools: `https://everydaydigitalbox.com/<directory_path>/index.html`.
  The registry directory, not the ID or name, determines the route. For example,
  `sha256-hash-checker` uses `sha-256-hash-checker/index.html`.
- Privacy: `https://everydaydigitalbox.com/privacy.html`. It is a public notice
  linked by the site, not private visitor data. It remains indexable and is
  explicitly included, rather than discovered through a file glob.
- Each eligible page has one absolute canonical link in its static HTML head.
  Directory and query aliases remain functional and declare the same clean URL.
  Canonical annotations are signals, not redirects or indexing guarantees.
- Query strings, fragments, percent-encoded route substitutions and other hosts
  are excluded. No tool logic, body content, URLs, analytics or consent changes.

## Generation and checks

```sh
# Refresh the sitemap after an independently approved RELEASED registry change.
python scripts/generate_sitemap.py

# Explicit metadata insertion for reviewed public pages; does not remove noindex
# or repair conflicting tags. Existing correct tags are unchanged.
python scripts/generate_sitemap.py --sync-canonicals

# Read-only checks: never repair output before testing whether it is stale.
python scripts/validate_seo.py
python scripts/validate_seo.py --json --no-report
python scripts/project_status.py --check-only --no-report
```

The generator uses standard-library Python and the structurally validated
registry. The only sitemap pages are homepage + privacy + `RELEASED` tools.
Current expected count is **89 URLs = 87 released tools + 2 public pages**;
the tool count is computed, not hard-coded into generation. `TESTED`, `PLANNED`,
`BLOCKED` and every other non-RELEASED status stay out. Templates, dashboards,
audit files and provisional content are not implicitly made public or included.
The neutral tool template remains `noindex` and has no public canonical.

XML is UTF-8, namespace-correct, escaped and sorted by absolute URL. Duplicate
routes are errors. No `lastmod`, `changefreq` or `priority` is emitted. Existing
verification dates are not reliable significant-content update dates; neither
they nor the build time are repurposed as modification dates. Repeating generation
with unchanged input produces no changes, including on LF/CRLF Git checkouts.

All candidate edits are planned and validated before writing. The generator
does not write the registry, robots policy, evidence manifests, remote files or
Git state. A filesystem error can still interrupt sequential local writes;
inspect the diff, resolve the error and rerun. Validation never writes files.

## Future tool workflow

1. Use the existing noindex scaffold and development/release gates. Creating a
   source file or a canonical does not release a utility.
2. During the deliberately implemented canonical-source stage (`IN_PROGRESS` or
   `IMPLEMENTED`), review the page's indexability and run:
   `python scripts/prepare_tool_seo.py --id TOOL_ID`. It rejects noindex pages and
   does not remove the scaffold's noindex on the developer's behalf.
3. Run structural/logic/browser tests on that final source, then record its
   actual verification hash. Add the existing gated homepage integration patch.
   Preparation rejects `TESTED`/`RELEASED` tools to avoid silently invalidating
   their already-recorded evidence. Existing metadata migrations need review.
4. Use the established reviewed release/public verification process; no tool
   status changes are automated by SEO scripts.
5. Only after an eligible status is deliberately `RELEASED`, regenerate the
   sitemap and run project/SEO/full required checks. A missing release URL or
   stale sitemap fails validation, instead of silently deploying old output.

## Validation and CI

The validator identifies the affected file/URL and rejects missing, duplicate,
misplaced or invalid canonicals; wrong scheme/host/query/fragment/escaping;
missing canonical targets; unexpected noindex; invalid XML/DTD/entities; duplicate,
ineligible, missing or noncanonical sitemap entries; stale generated bytes; and
an incorrect/blocking robots policy. All public URLs must match the explicit
allowlist and registry directory convention. Existing homepage/route checks
remain in place.

`check_project.py` and `project_status.py` include the read-only SEO checks for
this production project. The existing Functional CI Python job also executes
`validate_seo.py` explicitly. Its existing required aggregate, workflow event
triggers, action pins, permissions and branch protection remain in force. New
mutation tests join the explicit coverage map; no new scheduled job or push /
deployment controller is introduced. CI never regenerates first to conceal drift.

## Minimal robots policy

`robots.txt` contains one wildcard user-agent, an empty Disallow directive and
`Sitemap: https://everydaydigitalbox.com/sitemap.xml`. It blocks neither pages
nor rendering assets. Missing robots was not itself a crawl failure in SEO 1.
Robots is not authentication, privacy protection or a reliable deindexing tool.
Template/deployment-boundary changes remain a separate task.

## Historical source evidence

The 87 tools retain their RELEASED statuses and all dated publication hashes.
The canonical edit changes current source bytes, so SEO Task 2A adds a separate
bounded source overlay anchored to the starting main commit. It accepts only
the exact canonical insertion and reconstructs the exact earlier source before
comparing historical evidence. Unrelated source edits fail that check. Existing
consent overlays remain separately validated. The old audits are historical
facts, not rewritten to claim these new annotations are deployed.

After an authorized merge/deployment, independently verify actual live tags,
URLs, XML and robots bytes. Record new dated public evidence separately; do not
label local tests as indexing or publication proof. The current overlay is a
specific metadata proposal, not a general exemption for future source changes.

## Search Console handoff (owner action after deployment)

No authenticated Search Console access or sitemap submission occurred here.
After the owner authorizes merge and verifies the public deployment:

1. Open the existing verified property for everydaydigitalbox.com. Preserve its
   ownership verification method; do not create or change it in this task.
2. In Sitemaps, submit `https://everydaydigitalbox.com/sitemap.xml` (or its relative
   path when the UI requires that). The owner may perform this or explicitly
   authorize a later authenticated task.
3. Inspect processing status and discovered URLs. Check representative URL
   Inspection records for user-declared and Google-selected canonicals.
4. Sitemap acceptance, HTTP 200 and an indexable page do not prove indexing or
   guarantee ranking. Allow for search-engine processing and investigate actual
   errors without resubmitting repeatedly.

## Scope and remaining audit findings

SEO 1's original 18 findings and severity levels are preserved below. "Addressed
locally" means implementation proposed in this branch, pending owner review,
merge and public verification. The original HTML/JSON reports are unchanged.

| Finding | Original severity | Original description | Task 2A disposition |
| --- | --- | --- | --- |
| PERF-01 | HIGH | Production pages compile Tailwind CSS in the browser | Deferred; outside this task |
| TECH-09 | HIGH | Search reporting and actual indexing are not authenticated in this audit | Deferred; outside this task |
| CONTENT-01 | MEDIUM | Homepage discovery depends on title-only search across a long undivided grid. Category data is not exposed as category navigation. | Deferred; outside this task |
| CONTENT-02 | MEDIUM | Direct cross-tool navigation is sparse despite complementary workflows. | Deferred; outside this task |
| CONTENT-03 | MEDIUM | Several tools need especially precise search promises: AI Text Footprint Cleanser is not an AI detector; Batch Filename Planner does not rename files; CSV Merger appends rather than joins; streaming tool selects destinations. | Deferred; outside this task |
| TECH-01 | MEDIUM | No explicit canonical preference across duplicate URL forms | Addressed locally; public verification pending |
| TECH-02 | MEDIUM | XML sitemap and generation pipeline are absent | Addressed locally; public verification pending |
| TECH-10 | MEDIUM | Privacy-preserving GA4 settings limit acquisition attribution | Deferred; outside this task |
| UX-01 | MEDIUM | Homepage small text falls below AA contrast | Deferred; outside this task |
| UX-02 | MEDIUM | The mobile homepage makes search and tools hard to reach | Deferred; outside this task |
| UX-03 | MEDIUM | Brand and navigation presentation vary across page generations | Deferred; outside this task |
| TECH-03 | LOW | robots.txt is absent, without an observed crawl block | Addressed locally; public verification pending |
| TECH-06 | LOW | Unique descriptions often omit useful capability detail | Deferred; outside this task |
| TECH-07 | LOW | Social metadata and site/schema identity are absent | Deferred; outside this task |
| TECH-11 | LOW | Repository documentation still describes pre-merge proposals as current | Current checkpoint clarified; historical records retained |
| TECH-12 | LOW | Some non-product development fragments are publicly served | Deferred; outside this task |
| TECH-13 | LOW | Shared favicon coverage is inconsistent | Deferred; outside this task |
| UX-04 | LOW | Small controls and persistent privacy UI merit deeper manual testing | Deferred; outside this task |

Task 26 remains paused because its Image Contact Sheet Maker memory benchmark
was inconclusive. PDF Compressor stays BLOCKED. Inventory remains 105 registered,
87 RELEASED, 0 TESTED, 0 READY, 17 PLANNED, 1 BLOCKED; milestone remains 100.
No redesign, Tailwind migration, new tools, analytics changes, automatic SEO
operations or administrator bypass is included.

References: [Google canonical guidance](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls),
[sitemap guidance](https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview).
