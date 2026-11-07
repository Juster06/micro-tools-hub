# Task 24.1 release proposal — validation scope

The public deployment under review is main commit
`a7da719ea6ccc4caae572f26f6ae5e707fbb70be`. Its Pages run 42324279460
and all required post-merge Functional CI checks in 42324279630 passed.
Those results are separate from validation of this release proposal.

Fresh public results: 99 HTTP 200 responses match approved Git bytes, six
directory aliases match, all 81 canonical cards are visible, 61 public interaction
and catalog cases pass, and six grouped real-consent checks pass. Exactly three
accepted page views returned HTTP 204, with no duplicate page views. See the
global publication audit and six separate release audits for source hashes,
timestamps, behavior, network observations and limitations.

Fresh canonical proposal suites passed for all six tools:

| Tool | Logic cases | Browser cases | Browser assertions |
| --- | ---: | ---: | ---: |
| Number Base Converter | 24 | 13 | 49 |
| Unit Converter | 25 | 14 | 51 |
| Duration Calculator | 22 | 15 | 53 |
| URL Inspector & Query Builder | 18 | 11 | 45 |
| List Comparison & Set Operations | 24 | 9 | 41 |
| Color Contrast Checker | 17 | 14 | 51 |
| Total | 130 | 76 | 290 |

Structural checks and all six canonical integration gates passed. Integration
produced no patch because the six reviewed Live labels are already present in
this proposal. Project validation reports zero errors and zero warnings.

The first complete Node logic run found one old consent-catalog total expecting
75 released pages (518 passed, one failed). The assertion now accepts exactly the
six additional releases only after validating their source-bound publication
evidence. The fresh rerun passed all 519 Node tests with no skips. Consent runtime
code and existing page assertions are unchanged.

At this pre-commit snapshot, complete Python discovery, all 77 canonical Node
logic profiles, and the full Chromium partition have been started; their final
outcomes must be read from the delivery report and PR checks, not inferred here.
Six new source/preservation/public-evidence Python tests passed independently.
The required exact-head hosted checks remain a delivery gate. They must pass
before this proposal is ready for owner review. No deadline or test scope has
been relaxed: Python floor 213, Node 519, browser 720, 81 tool browser profiles
and two neutral templates. Windows local deadline limitations from previous
tasks remain documented; they do not waive hosted checks.

All 81 runtime tool pages, assets, privacy notice, historical audits, functional
workflow, dependency pins and deadlines remain unchanged. Existing regression
count assertions were extended through a strict Task 24 release-evidence helper;
the older tools' functional assertions remain mandatory.

No merge or deployment is authorized by this report. Final required CI results
and exact proposal head are linked in the PR and owner-facing delivery report.
