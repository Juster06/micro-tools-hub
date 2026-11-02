# Task 8 — controlled four-utility development plan

Date: 2026-11-02. Local implementation/testing/commits only. No push, pull request, merge, deployment, RELEASED transition or Task 9.

## Selection and baseline

Verified clean synchronized main `a6ea73b24ceeeca4e6f695ad2840fd720dfb36ce`, tree `2311a7f11a5b948a5964b31e333f78f46014beaf`. Read-only planner `python scripts/plan_tool_batch.py --count 4` selected the first four eligible READY entries. Planner has proposal-only behavior, not a separate dry-run flag. No unmet tool dependencies, occupied routes, changed priorities or skipped eligible entries.

| ID / name | Category | Priority / rank | Complexity | Canonical route | Dependencies |
| --- | --- | --- | --- | --- | --- |
| text-reverser / Text Reverser | text | P1 / 6 | S | text-reverser/index.html | Existing Tailwind Play CDN v4; native Intl.Segmenter with explicit code-point fallback |
| json-formatter / JSON Formatter | data | P1 / 7 | S | json-formatter/index.html | Existing Tailwind; native JSON.parse/stringify |
| url-encoder-decoder / URL Encoder and Decoder | developer | P1 / 8 | S | url-encoder-decoder/index.html | Existing Tailwind; native URI codecs |
| base64-encoder-decoder / Base64 Encoder and Decoder | developer | P1 / 9 | S | base64-encoder-decoder/index.html | Existing Tailwind; local UTF-8/standard Base64 codec |

## Acceptance behavior before implementation

All inputs capped at 100,000 UTF-16 units, no truncation. Live preview preserves input, invalidates obsolete output/counts/actions immediately, debounces updates, defers composition, restores defaults/focus on Clear, and guards asynchronous clipboard completion. Output is text-only. Export uses a fixed filename, UTF-8 Blob and revoked object URL. Empty output cannot be exported. No input network calls, storage, eval or injected HTML. Standalone slate/indigo pages retain explicit ../index.html navigation, labels/focus/status, existing Tailwind CDN and expanded inline fallback CSS.

* Text Reverser: default grapheme reversal of the whole input using Intl.Segmenter; explicit code-point fallback warning when unavailable. Word mode reverses non-whitespace tokens while preserving whitespace slots; punctuation remains attached. Line mode splits CRLF/CR/LF, reverses records and emits LF, including trailing blank records. Empty input has zero units. No normalization; input/output unit and reversed-unit statistics. Output cannot grow beyond the input cap.
* JSON Formatter: native JSON.parse and JSON.stringify; default pretty-print, two spaces; four spaces/tab and compact/validate modes. Validate preserves original valid input exactly. All JSON root types accepted; blank/invalid JSON rejected with parse error. Duplicate keys use native last-wins and key ordering; native IEEE-754 precision applies. Reject nonfinite parsed numbers, nesting deeper than 100 containers and formatted output exceeding 1,000,000 UTF-16 units, without truncation. Depth scanner respects JSON strings/escapes. Count parsed value nodes including root, input/output units; root type displayed separately. Export .json. No repair, schema validation or lossless number representation claim.
* URL Encoder and Decoder: explicit component encode (default), component decode, full-URI encode/decode. Native codec semantics; plus signs are literal, never form-space conversion. decodeURI preserves reserved escapes. Malformed escapes, invalid UTF-8 and lone-surrogate encoding fail clearly. No URL navigation/normalization/network. Output cap 1,000,000 units; export .txt.
* Base64 Encoder and Decoder: default standard padded Base64 encode of strict UTF-8 text. Decode requires canonical alphabet, padding and zero pad bits; optional removal of ASCII space/tab/CR/LF only, off by default and relevant only to decode. Reject URL-safe alphabet, unpadded non-multiple-of-four data, invalid UTF-8, lone-surrogate encoding and binary content that is not UTF-8. Preserve BOM and Unicode, no normalization. UTF-8 bytes, input/output units; output cap 400,000 units. Export .txt. Prominent Base64 is not encryption disclosure. No binary files or cryptography.

## Implementation, evidence and integration sequence

Run generator --dry-run, inspect six proposed ignored files per tool, then generate. Implement independently in ignored staging. Add canonical HTML/README plus manifest, exact JSON logic fixtures, browser DSL, independent Node logic/boundary tests, extended browser races/privacy/export tests and hub integration tests under tests/tools/ID. Promote one tool at a time to honor unchanged homepage gate; manually record READY → IMPLEMENTED before source testing/checkpoint, then matching committed revision/normalized hash and genuine scoped audit before TESTED. Rerun canonical tests after metadata edits, review/check/apply generated homepage patch, verify idempotence. No shared framework/gate modification.

Real Edge/Chromium cases cover every setting, boundaries, invalid input, Unicode, deterministic exact outputs/statistics, copy success/denial, captured UTF-8 downloads/revocation/failure, stale results, rapid changes, simulated composition, transport/storage probes, keyboard and 320/375/768/1440 layouts. Capture/review actual screenshots. Do not claim OS clipboard, Save dialog, native IME, physical devices or screen-reader certification.

Expected changes: four tool directories, four test directories, four independent audit JSON files, this plan, registry, homepage and relevant README/progress/roadmap/changelog/handoff. One source/test checkpoint per tool and one final integration/evidence/docs commit. Generated bundles/reports/screenshots/machine paths stay ignored/outside Git. Preserve all nine released source pages/cards/registry entries/audits, CNAME, framework/dashboard/launcher, original feature branches and existing shortcut bytes/properties/AppID.

Run full Python and sequential full Node suites, all nine released framework regressions, templates, registry/consistency/source/homepage checks and full project status. Verify existing Desktop and Start menu shortcuts separately if practical, from unrelated cwd without reinstalling; report actual inventory and validation freshness, never inferred functional totals. Expected final inventory 93 total / 9 RELEASED / 4 TESTED / 11 READY / 68 PLANNED / 1 BLOCKED, 9/25 (36%). Privacy/allowlist/whitespace/protected-content/source-history review before final local commit; postcommit check-only and clean-tree verification. Next action is owner review/authorization of GitHub preparation, not Task 9.

## Final executed verification — 2026-11-02

Python **123/123** and complete sequential Node **249/249**, zero failures/skips. Assertions/timeouts and all existing suites unchanged. Actual Edge engine: Edg/156.0.4314.58.

| Tool | Exact JSON logic | Additional Node logic | Framework browser / assertions | Extended browser | Hub integration |
| --- | ---: | ---: | ---: | ---: | ---: |
| text-reverser | 30 | 9 | 16 / 33 | 12 | 2 |
| json-formatter | 35 | 9 | 19 / 37 | 12 | 2 |
| url-encoder-decoder | 36 | 9 | 16 / 31 | 12 | 2 |
| base64-encoder-decoder | 44 | 9 | 17 / 33 | 11 | 2 |

New tool totals: 145 exact JSON logic fixtures plus 36 independent Node logic tests; 68 framework browser cases plus 47 extended and 8 real hub integration cases = 123 browser cases. Independent source/option/limit/error/oracle checks, captured download bytes/MIME/filenames/revocation/failures, stale clipboard/input/settings, simulated composition, labels/keyboard and transport/storage probes passed. Final source hashes match actual committed revisions.

Nine released-tool regressions: 235 existing isolated logic fixtures; 111 framework browser cases / 385 assertions, plus their unchanged Node suites. Four original specialist tools have no isolated logic adapters: logic stays NOT RUN and combined subset status PARTIAL, with required structural/browser PASS; no fabricated complete PASS. Neutral templates: 6 logic / 12 browser / 48 assertions. Registry, consistency, structural source/navigation/evidence verification, full project status and whitespace checks PASS with zero errors/warnings. Homepage route/card/search/back navigation passed; all four proposal reruns produced empty patches. Actual screenshots at 320/375/768/1440 were reviewed. Original nine source/card blocks/registry entries/release audits/CNAME unchanged; no framework/dashboard/launcher modifications.

Both actual existing Windows Desktop and Start menu shortcuts were launched separately from an unrelated working directory and directly observed in the native dashboard. Each automatic project status workflow completed exit 0; Overview showed 93 total, 9 RELEASED, 4 TESTED, 11 READY, 68 PLANNED, 1 BLOCKED, 9/25 (36%). Testing/Validation showed four current PASS reports and explicit unavailable functional totals. Shortcut bytes/target/arguments/cwd/AppID verified unchanged, no reinstall or registry edit. Final postcommit check-only/provenance and read-only saved-data reload are performed without altering tracked documentation.

Changed-file privacy/allowlist/source-history review: 37 added / 7 modified files; no credentials, personal Windows paths, generated reports/bundles/screenshots, temporary files, local settings or machine artifacts included. All 89 other registry entries, previous audits and original local branch heads preserved. No push, PR, merge or deployment. Known scope: installed Edge only, emulated viewports; simulated clipboard/composition and in-memory downloads, not physical devices, screen reader, OS clipboard/IME/Save dialogs or universal performance. JSON numeric precision follows native IEEE-754; Base64 is UTF-8 text only and not encryption; absent Segmenter uses disclosed code-point fallback. Existing Tailwind styling delivery remains external. No remaining local blocker; await owner review and separate GitHub preparation authorization, do not start Task 9.
