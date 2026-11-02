# Development roadmap

## Task 8 — independent public releases

PR #12 merged normally as `5e6df5389455cf9d580d9985eaa504c43a1c1b69` at 2026-11-02T02:45:09Z. Actual successful [Pages run 41379385778](https://github.com/Juster06/micro-tools-hub/actions/runs/41379385778) and independent public browser/approved-source checks qualified each released utility. Current inventory: 93 total, 13 RELEASED, 0 TESTED, 11 READY, 68 PLANNED, 1 BLOCKED; milestone 13/25 (52%).

Actual per-tool publication/source/live results are in separate release audits; original audits remain unchanged. Final metadata deployment and Windows shortcut checks precede completion. Homepage analytics is preserved; utility input privacy is scoped separately. No Task 9.

## Task 7 — independent releases after live verification

PR #11 merged normally as `d3ddb6de807913c05832e24a77797f033b353497` at 2026-11-01T22:51:53Z. Actual successful [Pages implementation run 41359251674](https://github.com/Juster06/micro-tools-hub/actions/runs/41359251674), independent live browser behavior and exact approved public source hashes passed before each RELEASED transition. Original local audits/source checkpoints remain preserved. Current inventory: 93 total, 9 RELEASED, 0 TESTED, 15 READY, 68 PLANNED, 1 BLOCKED; milestone 9/25 (36%).

The original three implementation audits are unchanged. Separate per-tool release audits contain genuine deployment/public behavior/source evidence. Final metadata publication and native shortcut verification are recorded in the latest handoff. Do not begin Task 8 or another utility.

## Task 6 — Duplicate Line Remover released after live verification

PR #10 merged as `34ad939b7802ff2c0342d591e9773b06d78a0fbd`. Successful main/root GitHub Pages deployment, real public Edge behavior and exact approved normalized source identity passed on 2026-11-01 before RELEASED. Original local audit remains unchanged; separate `audit/DUPLICATE_LINE_REMOVER_RELEASE_VERIFICATION.json` records genuine release evidence and scope. The gated hub card uses the released Live presentation. Counts: 93 total, 6 RELEASED, 0 TESTED, 18 READY, 68 PLANNED, 1 BLOCKED; milestone 6/25 (24%).

Final release-metadata deployment and native shortcut verification are recorded in the latest handoff. No Task 7 or additional utility is authorized; Text Sorter remains a READY queue entry only.

## Task 5 — Case Converter released after live verification

PR #9 merged as `97a0912a9f6e917c4d6457e856bed45fbc325450`. The actual public Case Converter passed scoped live behavior checks and normalized deployed-source identity verification on 2026-11-01 before the RELEASED transition. The original local audit is retained; `audit/CASE_CONVERTER_RELEASE_VERIFICATION.json` records release evidence and limitations. The hub card uses the established Live label. Inventory: 93 total, 5 RELEASED, 0 TESTED, 19 READY, 68 PLANNED, 1 BLOCKED; milestone 5/25 (20%).

Task 5 final publication verification is recorded in the latest handoff. No additional utility is authorized; Duplicate Line Remover remains a READY queue entry only.

## Framework readiness — Task 4

Reusable templates, safe staged scaffolding, functional checks and validated homepage patch proposals are available. Use `python scripts/plan_tool_batch.py --count 10` to propose existing READY work in sequence; proposals are not authorization to build or publish a batch. See `TOOL_DEVELOPMENT_GUIDE.md`. Task 4 changed no tool status/count; the Task 5 checkpoint above records the subsequent utility implementation.

Source of inventory, status, priority, dependencies, and order: `TOOL_REGISTRY.json`. Run `node scripts/project.mjs sync` after changing it. The complete proposal mapping is in `audit/BACKLOG_RECONCILIATION.md`.

## Priority and effort conventions

- **P1:** the next scoped browser-native sequence. **P2:** accepted follow-up work. **P3:** specialist or high-risk work needing further design.
- **S:** a bounded interface and straightforward local transformation. **M:** several modes or more substantial validation. **L:** complex parsing, UX, formats, or performance. **XL:** feasibility/security design dominates. These are relative complexity estimates, not elapsed-time commitments.
- **READY:** features and a local approach are defined; still requires a brief implementation plan and tests. **PLANNED:** resolve scope/dependencies first. **BLOCKED:** an explicit prerequisite is unmet.

## Next twenty distinct utilities

Execute in order unless the user steers the project or a dependency/regression justifies a documented change. Current implementation states are shown below; sequence rank alone does not imply implementation or publication.

<!-- GENERATED:SEQUENCE:START -->
| Order | Tool ID | Name | Category | Complexity | Status |
| ---: | --- | --- | --- | --- | --- |
| 1 | case-converter | Case Converter | Text and Writing Tools | S | RELEASED |
| 2 | duplicate-line-remover | Duplicate Line Remover | Text and Writing Tools | S | RELEASED |
| 3 | text-sorter | Text Sorter | Text and Writing Tools | S | RELEASED |
| 4 | slug-generator | Slug Generator | Text and Writing Tools | S | RELEASED |
| 5 | find-and-replace | Find and Replace | Text and Writing Tools | S | RELEASED |
| 6 | text-reverser | Text Reverser | Text and Writing Tools | S | RELEASED |
| 7 | json-formatter | JSON Formatter | Excel and Data Tools | S | RELEASED |
| 8 | url-encoder-decoder | URL Encoder and Decoder | Developer Tools | S | RELEASED |
| 9 | base64-encoder-decoder | Base64 Encoder and Decoder | Developer Tools | S | RELEASED |
| 10 | uuid-generator | UUID Generator | Developer Tools | S | READY |
| 11 | timestamp-converter | Timestamp Converter | Developer Tools | S | READY |
| 12 | percentage-calculator | Percentage Calculator | Calculators | S | READY |
| 13 | percentage-change-calculator | Percentage Change Calculator | Calculators | S | READY |
| 14 | discount-calculator | Discount Calculator | Calculators | S | READY |
| 15 | profit-margin-calculator | Profit Margin Calculator | Calculators | S | READY |
| 16 | date-difference-calculator | Date Difference Calculator | Calculators | S | READY |
| 17 | countdown-timer | Countdown Timer | Everyday Productivity Tools | S | READY |
| 18 | random-name-picker | Random Name Picker | Everyday Productivity Tools | S | READY |
| 19 | hashtag-organizer | Hashtag Organizer | Social Media Tools | S | READY |
| 20 | secure-random-number-generator | Secure Random Number Generator | Security and Privacy Tools | S | READY |
<!-- GENERATED:SEQUENCE:END -->

## Practical delivery sequence

1. **Text transformations (orders 1–5):** settle Unicode/case/line/whitespace behavior; preserve original text where a transformation could surprise the user; integrate each finished page.
2. **Text and developer basics (6–10):** grapheme policy, parse errors, UTF-8 encoding, URI modes, cryptographic UUID generation. Never treat Base64 as encryption.
3. **Dates and arithmetic (11–15):** explicit epoch units, finite input, formulas, zero-denominator handling, and rounding. No live financial or legal-rate claims.
4. **Productivity and social basics (16–20):** date-only arithmetic, deadline-based timers, unbiased draws, hashtag rules, and cryptographic integer sampling. Test boundaries rather than relying on happy paths.
5. **Milestone review:** those twenty plus the baseline would total 24 released tools if all are completed and published. Reassess quality, then consider Image Rotator as the next distinct utility to reach 25.
6. **Format processing:** evaluate PDF/image/CSV libraries and size limits; begin with bounded manipulations such as page rotation or image resizing. Resolve parser reuse before creating several CSV tools.
7. **Specialist work:** proceed only after feasibility/security design for PDF compression, local encryption, hostile SVG/HTML, regex workers/timeouts, complex minifiers, and EXIF removal.

For every step: check for duplicates → plan → implement → test → integrate → document → verify publication. Complete unfinished work before starting an unrelated page.

## Category catalog

This catalog includes existing and proposed utilities, with status explicitly shown. Proposed directories are reserved names only, not existing pages. Runtime library candidates are not installed dependencies. All eleven requested categories are represented.

<!-- GENERATED:CATALOG:START -->
### PDF Tools

| Tool ID | Utility | Status | Priority | Complexity | Dependencies / gate |
| --- | --- | --- | --- | --- | --- |
| pdf-merger | PDF Merger | PLANNED | P2 | M | PDF parsing/manipulation library: evaluate license, size, encryption and malformed-file behavior before selection |
| pdf-splitter | PDF Splitter | PLANNED | P2 | M | PDF parsing/manipulation library: evaluate license, size, encryption and malformed-file behavior before selection |
| pdf-rotator | PDF Rotator | PLANNED | P2 | M | PDF parsing/manipulation library: evaluate license, size, encryption and malformed-file behavior before selection |
| image-to-pdf | Image to PDF | PLANNED | P2 | M | PDF parsing/manipulation library: evaluate license, size, encryption and malformed-file behavior before selection |
| pdf-to-image | PDF to Image | PLANNED | P2 | L | PDF parsing/manipulation library: evaluate license, size, encryption and malformed-file behavior before selection |
| pdf-watermark | PDF Watermark | PLANNED | P2 | M | PDF parsing/manipulation library: evaluate license, size, encryption and malformed-file behavior before selection |
| pdf-page-numbering | PDF Page Numbering | PLANNED | P2 | M | PDF parsing/manipulation library: evaluate license, size, encryption and malformed-file behavior before selection |
| pdf-metadata-viewer | PDF Metadata Viewer | PLANNED | P2 | M | PDF parsing/manipulation library: evaluate license, size, encryption and malformed-file behavior before selection |
| pdf-compressor | PDF Compressor | BLOCKED | P3 | XL | PDF parsing/manipulation library: evaluate license, size, encryption and malformed-file behavior before selection |

### Image Tools

| Tool ID | Utility | Status | Priority | Complexity | Dependencies / gate |
| --- | --- | --- | --- | --- | --- |
| image-compressor | Image Compressor | PLANNED | P2 | M | Browser image decoding and Canvas; format support and memory limits must be tested |
| image-resizer | Image Resizer | PLANNED | P2 | M | Browser image decoding and Canvas; format support and memory limits must be tested |
| image-format-converter | Image Format Converter | PLANNED | P2 | M | Browser image decoding and Canvas; format support and memory limits must be tested |
| image-cropper | Image Cropper | PLANNED | P2 | L | Browser image decoding and Canvas; format support and memory limits must be tested |
| image-rotator | Image Rotator | PLANNED | P2 | S | Browser image decoding and Canvas; format support and memory limits must be tested |
| image-watermark | Image Watermark | PLANNED | P2 | M | Browser image decoding and Canvas; format support and memory limits must be tested |
| image-color-picker | Image Color Picker | PLANNED | P2 | M | Browser image decoding and Canvas; format support and memory limits must be tested |
| passport-photo-layout-maker | Passport Photo Layout Maker | PLANNED | P2 | L | Browser image decoding and Canvas; format support and memory limits must be tested |

### Text and Writing Tools

| Tool ID | Utility | Status | Priority | Complexity | Dependencies / gate |
| --- | --- | --- | --- | --- | --- |
| text-cleaner | AI Text Footprint Cleanser | RELEASED | P2 | M | Modern browser DOM APIs |
| case-converter | Case Converter | RELEASED | P1 | S | Browser-native approach; scope review before implementation |
| duplicate-line-remover | Duplicate Line Remover | RELEASED | P1 | S | Browser-native approach; scope review before implementation |
| text-difference-checker | Text Difference Checker | PLANNED | P2 | L | Browser-native approach; scope review before implementation |
| text-sorter | Text Sorter | RELEASED | P1 | S | Browser-native approach; scope review before implementation |
| text-reverser | Text Reverser | RELEASED | P1 | S | Browser-native approach; scope review before implementation |
| find-and-replace | Find and Replace | RELEASED | P1 | S | Browser-native approach; scope review before implementation |
| slug-generator | Slug Generator | RELEASED | P1 | S | Browser-native approach; scope review before implementation |

### Excel and Data Tools

| Tool ID | Utility | Status | Priority | Complexity | Dependencies / gate |
| --- | --- | --- | --- | --- | --- |
| excel-sandbox | Excel Formula Sandbox & Analyzer | RELEASED | P2 | M | Modern browser DOM APIs |
| csv-json-converter | CSV ↔ JSON Converter | PLANNED | P2 | L | CSV/workbook parsers where needed: evaluate correctness, license and bundle size |
| excel-to-csv | Excel to CSV | PLANNED | P2 | L | CSV/workbook parsers where needed: evaluate correctness, license and bundle size |
| csv-column-extractor | CSV Column Extractor | PLANNED | P2 | M | CSV/workbook parsers where needed: evaluate correctness, license and bundle size |
| duplicate-row-finder | Duplicate Row Finder | PLANNED | P2 | M | CSV/workbook parsers where needed: evaluate correctness, license and bundle size |
| csv-data-cleaner | CSV Data Cleaner | PLANNED | P2 | L | CSV/workbook parsers where needed: evaluate correctness, license and bundle size |
| csv-merger | CSV Merger | PLANNED | P2 | M | CSV/workbook parsers where needed: evaluate correctness, license and bundle size |
| json-formatter | JSON Formatter | RELEASED | P1 | S | Native JSON.parse and JSON.stringify |
| csv-viewer | CSV Viewer | PLANNED | P2 | M | CSV/workbook parsers where needed: evaluate correctness, license and bundle size |
| excel-formula-generator | Excel Formula Generator | PLANNED | P2 | L | Browser-native deterministic templates; no parser or AI service |

### Developer Tools

| Tool ID | Utility | Status | Priority | Complexity | Dependencies / gate |
| --- | --- | --- | --- | --- | --- |
| base64-encoder-decoder | Base64 Encoder and Decoder | RELEASED | P1 | S | Browser-native approach; scope review before implementation |
| url-encoder-decoder | URL Encoder and Decoder | RELEASED | P1 | S | Browser-native approach; scope review before implementation |
| uuid-generator | UUID Generator | READY | P1 | S | Browser cryptographic randomness; feature-detect and fail clearly if unavailable |
| sha256-hash-checker | SHA-256 Text & File Hash Checker | PLANNED | P2 | M | Browser Web Crypto SHA-256; bounded file reads |
| regex-tester | Regex Tester | PLANNED | P2 | L | Browser Worker with termination timeout; bounded input |
| html-formatter | HTML Formatter | PLANNED | P2 | L | Reviewed non-executing HTML parser and whitespace-preservation policy |
| css-minifier | CSS Minifier | PLANNED | P2 | L | Reviewed CSS parser/minifier and license |
| javascript-minifier | JavaScript Minifier | PLANNED | P2 | L | Reviewed JavaScript parser/minifier and license; consider worker isolation |
| timestamp-converter | Timestamp Converter | READY | P1 | S | Browser-native approach; scope review before implementation |

### Social Media Tools

| Tool ID | Utility | Status | Priority | Complexity | Dependencies / gate |
| --- | --- | --- | --- | --- | --- |
| social-counter | Social Media Character Counter & Live Previewer | RELEASED | P2 | M | Modern browser DOM APIs |
| hashtag-organizer | Hashtag Organizer | READY | P1 | S | Browser-native approach; scope review before implementation |
| youtube-title-checker | YouTube Title Checker | PLANNED | P2 | S | Browser-native approach; scope review before implementation |
| youtube-description-formatter | YouTube Description Formatter | PLANNED | P2 | M | Browser-native approach; scope review before implementation |
| instagram-bio-formatter | Instagram Bio Formatter | PLANNED | P2 | M | Browser-native approach; scope review before implementation |
| social-media-line-break-tool | Social Media Line Break Tool | PLANNED | P2 | S | Browser-native approach; scope review before implementation |
| emoji-picker | Emoji Picker | PLANNED | P2 | M | Reviewed local emoji dataset and usage license |
| hashtag-counter | Hashtag Counter | PLANNED | P2 | S | Browser-native approach; scope review before implementation |
| youtube-thumbnail-preview | YouTube Thumbnail Preview | PLANNED | P2 | M | Browser-native approach; scope review before implementation |
| posting-calendar-generator | Posting Calendar Generator | PLANNED | P2 | M | Browser-native approach; scope review before implementation |
| username-generator | Username Generator | PLANNED | P2 | S | Browser-native approach; scope review before implementation |

### Calculators

| Tool ID | Utility | Status | Priority | Complexity | Dependencies / gate |
| --- | --- | --- | --- | --- | --- |
| percentage-calculator | Percentage Calculator | READY | P1 | S | Browser-native approach; scope review before implementation |
| percentage-change-calculator | Percentage Change Calculator | READY | P1 | S | Browser-native approach; scope review before implementation |
| vat-calculator | VAT Calculator | PLANNED | P2 | M | Browser-native approach; scope review before implementation |
| discount-calculator | Discount Calculator | READY | P1 | S | Browser-native approach; scope review before implementation |
| age-calculator | Age Calculator | PLANNED | P2 | M | Browser-native approach; scope review before implementation |
| date-difference-calculator | Date Difference Calculator | READY | P1 | S | Browser-native approach; scope review before implementation |
| working-days-calculator | Working Days Calculator | PLANNED | P2 | M | Browser-native approach; scope review before implementation |
| loan-repayment-calculator | Loan Repayment Calculator | PLANNED | P2 | M | Browser-native approach; scope review before implementation |
| profit-margin-calculator | Profit Margin Calculator | READY | P1 | S | Browser-native approach; scope review before implementation |
| compound-interest-calculator | Compound Interest Calculator | PLANNED | P2 | M | Browser-native approach; scope review before implementation |

### Security and Privacy Tools

| Tool ID | Utility | Status | Priority | Complexity | Dependencies / gate |
| --- | --- | --- | --- | --- | --- |
| password-generator | Password Generator | PLANNED | P2 | M | Browser Web Crypto where cryptographic randomness or hashing is required |
| password-strength-checker | Password Strength Checker | PLANNED | P2 | L | Reviewed locally bundled password-strength estimator and license |
| secure-random-number-generator | Secure Random Number Generator | READY | P1 | S | Browser cryptographic randomness; feature-detect and fail clearly if unavailable |
| local-text-encryption | Local Text Encryption | PLANNED | P3 | XL | Web Crypto authenticated encryption and password derivation; Separate reviewed threat model and versioned format |
| exif-metadata-viewer | EXIF Metadata Viewer | PLANNED | P2 | L | Reviewed format-specific metadata parser |
| exif-metadata-remover | EXIF Metadata Remover | PLANNED | P2 | L | Reviewed metadata parser/removal method and exported-metadata verifier |
| file-signature-inspector | File Signature Inspector | PLANNED | P2 | M | Browser Web Crypto where cryptographic randomness or hashing is required |
| passphrase-generator | Passphrase Generator | PLANNED | P2 | M | Reviewed licensed word list; Browser cryptographic randomness and unbiased selection |
| qr-code-generator | QR Code Generator | PLANNED | P2 | M | Reviewed locally bundled QR encoder and license |

### File Conversion Tools

| Tool ID | Utility | Status | Priority | Complexity | Dependencies / gate |
| --- | --- | --- | --- | --- | --- |
| txt-to-pdf | TXT to PDF | PLANNED | P2 | L | Reviewed PDF text rendering library and font licensing |
| markdown-converter-previewer | Markdown Converter & Previewer | PLANNED | P2 | L | Reviewed Markdown parser and sanitizer; local bundled assets preferred |
| html-to-markdown | HTML to Markdown | PLANNED | P2 | L | Reviewed non-executing HTML-to-Markdown conversion library |
| csv-to-txt | CSV to TXT | PLANNED | P2 | M | Format-specific parsers, sanitizers or encoders: evaluate before implementation |
| json-to-txt | JSON to TXT | PLANNED | P2 | M | Format-specific parsers, sanitizers or encoders: evaluate before implementation |
| svg-to-png | SVG to PNG | PLANNED | P2 | L | Reviewed SVG sanitization and external-resource blocking; Canvas rasterization with tested dimension limits |
| png-to-ico | PNG to ICO | PLANNED | P2 | L | Reviewed local ICO encoder |
| file-size-converter | File Size Converter | PLANNED | P2 | S | Format-specific parsers, sanitizers or encoders: evaluate before implementation |
| html-previewer | HTML Previewer | PLANNED | P2 | L | Sandboxed iframe with restrictive CSP and no script/same-origin privileges |

### Everyday Productivity Tools

| Tool ID | Utility | Status | Priority | Complexity | Dependencies / gate |
| --- | --- | --- | --- | --- | --- |
| pomodoro-timer | Pomodoro Timer | PLANNED | P2 | M | Browser-native approach; scope review before implementation |
| countdown-timer | Countdown Timer | READY | P1 | S | Browser-native approach; scope review before implementation |
| random-name-picker | Random Name Picker | READY | P1 | S | Browser cryptographic randomness; feature-detect and fail clearly if unavailable |
| decision-wheel | Decision Wheel | PLANNED | P2 | M | Browser-native approach; scope review before implementation |
| local-to-do-list | Local To-Do List | PLANNED | P2 | M | Explicit opt-in localStorage, export format and clear-all behavior |
| invoice-generator | Invoice Generator | PLANNED | P2 | L | Browser-native approach; scope review before implementation |
| resume-builder | Resume Builder | PLANNED | P2 | L | Browser-native approach; scope review before implementation |
| meeting-agenda-generator | Meeting Agenda Generator | PLANNED | P2 | M | Browser-native approach; scope review before implementation |
| printable-calendar-generator | Printable Calendar Generator | PLANNED | P2 | M | Browser-native approach; scope review before implementation |

### Entertainment Tools

| Tool ID | Utility | Status | Priority | Complexity | Dependencies / gate |
| --- | --- | --- | --- | --- | --- |
| streaming-roulette | Free Stream Roulette | RELEASED | P2 | S | Modern browser DOM APIs |
<!-- GENERATED:CATALOG:END -->

## Deferred product work

SEO monitoring, advertising, analytics, paid services, accounts, and a backend are not part of this delivery sequence. The future 9–11-day SEO observation concept is recorded in `PROJECT_MASTER_PLAN.md` without an automation or implementation.
