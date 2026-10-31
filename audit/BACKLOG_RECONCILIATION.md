# Initial backlog reconciliation

Source: the owner's 2026-10-31 project brief. Every proposed name maps to exactly one canonical tool ID in `TOOL_REGISTRY.json`. Combined names count as one utility; embedded existing features do not increase the released count. The full generated catalog and next-twenty sequence are in `ROADMAP.md`.

`NEW_TOOL` means a distinct proposed task. `COMBINED` means a mode of a shared planned utility. `EXISTING_FEATURE` means source already provides that capability, with its documented limitations. This is not a claim that the entire backlog has been implemented.

<!-- GENERATED:RESOLUTIONS:START -->
| Proposed utility | Canonical tool ID | Resolution | Reason |
| --- | --- | --- | --- |
| Word Counter | text-cleaner | EXISTING_FEATURE | Word count is already present; improve that tool if requirements justify it. |
| Reading Time Calculator | text-cleaner | EXISTING_FEATURE | Existing 200-words-per-minute estimate; do not count it as another shipped page. |
| Extra Space Remover | social-counter | EXISTING_FEATURE | Clean Spaces & Copy already covers repeated horizontal whitespace; generalization belongs to that utility unless distinct requirements justify separation. |
| JPG to PNG | image-format-converter | COMBINED | Use one image conversion interface. |
| PNG to JPG | image-format-converter | COMBINED | Use one image conversion interface with a transparency background choice. |
| Image to WebP | image-format-converter | COMBINED | Use the same format converter and detect support. |
| CSV to JSON | csv-json-converter | COMBINED | One bidirectional conversion utility. |
| JSON to CSV | csv-json-converter | COMBINED | One bidirectional conversion utility. |
| SHA-256 Hash Generator | sha256-hash-checker | COMBINED | Share digest generation and comparison for text and bounded files. |
| File Hash Checker | sha256-hash-checker | COMBINED | File mode belongs to the same hash utility. |
| Markdown to HTML | markdown-converter-previewer | COMBINED | Share parser and sanitizer with Markdown preview. |
| Markdown Previewer | markdown-converter-previewer | COMBINED | One conversion and preview utility. |
| PDF Merger | pdf-merger | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| PDF Splitter | pdf-splitter | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| PDF Rotator | pdf-rotator | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Image to PDF | image-to-pdf | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| PDF to Image | pdf-to-image | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| PDF Watermark | pdf-watermark | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| PDF Page Numbering | pdf-page-numbering | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| PDF Metadata Viewer | pdf-metadata-viewer | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| PDF Compressor | pdf-compressor | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Image Compressor | image-compressor | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Image Resizer | image-resizer | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Image Cropper | image-cropper | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Image Rotator | image-rotator | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Image Watermark | image-watermark | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Image Color Picker | image-color-picker | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Passport Photo Layout Maker | passport-photo-layout-maker | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Case Converter | case-converter | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Duplicate Line Remover | duplicate-line-remover | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Text Difference Checker | text-difference-checker | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Text Sorter | text-sorter | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Text Reverser | text-reverser | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Find and Replace | find-and-replace | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Slug Generator | slug-generator | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Excel to CSV | excel-to-csv | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| CSV Column Extractor | csv-column-extractor | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Duplicate Row Finder | duplicate-row-finder | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| CSV Data Cleaner | csv-data-cleaner | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| CSV Merger | csv-merger | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| JSON Formatter | json-formatter | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| CSV Viewer | csv-viewer | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Excel Formula Generator | excel-formula-generator | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Base64 Encoder and Decoder | base64-encoder-decoder | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| URL Encoder and Decoder | url-encoder-decoder | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| UUID Generator | uuid-generator | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Regex Tester | regex-tester | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| HTML Formatter | html-formatter | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| CSS Minifier | css-minifier | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| JavaScript Minifier | javascript-minifier | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Timestamp Converter | timestamp-converter | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Hashtag Organizer | hashtag-organizer | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| YouTube Title Checker | youtube-title-checker | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| YouTube Description Formatter | youtube-description-formatter | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Instagram Bio Formatter | instagram-bio-formatter | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Social Media Line Break Tool | social-media-line-break-tool | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Emoji Picker | emoji-picker | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Hashtag Counter | hashtag-counter | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| YouTube Thumbnail Preview | youtube-thumbnail-preview | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Posting Calendar Generator | posting-calendar-generator | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Username Generator | username-generator | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Percentage Calculator | percentage-calculator | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Percentage Change Calculator | percentage-change-calculator | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| VAT Calculator | vat-calculator | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Discount Calculator | discount-calculator | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Age Calculator | age-calculator | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Date Difference Calculator | date-difference-calculator | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Working Days Calculator | working-days-calculator | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Loan Repayment Calculator | loan-repayment-calculator | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Profit Margin Calculator | profit-margin-calculator | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Compound Interest Calculator | compound-interest-calculator | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Password Generator | password-generator | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Password Strength Checker | password-strength-checker | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Secure Random Number Generator | secure-random-number-generator | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Local Text Encryption | local-text-encryption | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| EXIF Metadata Viewer | exif-metadata-viewer | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| EXIF Metadata Remover | exif-metadata-remover | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| File Signature Inspector | file-signature-inspector | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Passphrase Generator | passphrase-generator | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| QR Code Generator | qr-code-generator | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| TXT to PDF | txt-to-pdf | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| HTML to Markdown | html-to-markdown | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| CSV to TXT | csv-to-txt | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| JSON to TXT | json-to-txt | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| SVG to PNG | svg-to-png | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| PNG to ICO | png-to-ico | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| File Size Converter | file-size-converter | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| HTML Previewer | html-previewer | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Pomodoro Timer | pomodoro-timer | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Countdown Timer | countdown-timer | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Random Name Picker | random-name-picker | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Decision Wheel | decision-wheel | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Local To-Do List | local-to-do-list | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Invoice Generator | invoice-generator | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Resume Builder | resume-builder | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Meeting Agenda Generator | meeting-agenda-generator | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
| Printable Calendar Generator | printable-calendar-generator | NEW_TOOL | Distinct primary task; scope and dependencies recorded in the canonical entry. |
<!-- GENERATED:RESOLUTIONS:END -->

## Similar but distinct

- Stream Roulette selects curated streaming destinations; Decision Wheel chooses from user-entered options.
- Formula Sandbox formats/analyzes existing formulas; Formula Generator proposes deterministic templates from explicit fields.
- Image compression changes encoding/quality; resizing changes dimensions; cropping changes bounds; conversion changes format. Share helpers where justified, but preserve distinct primary tasks.
- Social Counter's line-break preservation does not implement a dedicated line-break-formatting workflow; that proposal remains planned.
- CSV tools can reuse a reviewed parser, but viewing, selecting columns, merging rows, and transforming formats have different outputs.

## Dependency and feasibility gates

No new library has been installed. PDF manipulation/rendering, workbook parsing, QR/ICO encoding, metadata handling, Markdown sanitization, and minifiers require review before implementation. Cryptography and hostile-input previews need explicit designs. PDF compression remains blocked until a measured local experiment demonstrates an honest, useful result.
