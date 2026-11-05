# Task 18 — six additional utilities

Authorized development baseline: `f35f07ee5da8c5c4efdf7d3f1ffeabe75571a16a`.
93 registered, 50 RELEASED, 0 TESTED, 0 READY, 42 PLANNED, 1 BLOCKED.
Task 17 is complete; GA4 collection was publicly verified, property reporting was
not. The next planning checkpoint is 75 releases; registry milestones stay intact.

Implement sequentially in the owner's order. Each tool receives its own source,
focused logic/browser tests, canonical checks, committed source revision and audit
before starting the next. Registry lifecycle is manually evidence driven; publication
stays null. No merge, production deployment or administrator bypass is authorized.

## Acceptance and resource decisions

1. **YouTube Title Checker**: 10,000 Unicode code points (at most 20,000 UTF-16
   units), configurable 100-character guide, 60-code-point opening preview. Count
   normalized LF as one character; retain input including blank lines. Guidance
   flags line breaks and angle brackets; no ranking or exact truncation prediction.
   Copy/download the unchanged normalized title, reset defaults and focus.
2. **Instagram Bio Formatter**: same input bound; configurable 150-character
   planning guide, preserve line breaks or collapse repeated blank lines or trim
   line edges on explicit selection. Count resulting Unicode code points, approximate
   mobile preview via text nodes, no account access or platform rendering claim.
3. **File Signature Inspector**: read only `file.slice(0,4096)` regardless of file
   length. Recognize PNG, JPEG, GIF, WebP, PDF, ZIP, gzip, Windows PE candidate
   (MZ), ELF and RIFF/WAVE. Inspect minimal required bytes; partial signatures
   remain unknown. ZIP is a container, not proof of DOCX/XLSX or safe contents.
   No file decoding, execution, hashing or crypto dependency is needed.
4. **Image Format Converter**: static JPEG/PNG/WebP only, 5 MiB, dimensions
   1–4096 and at most 8,000,000 pixels. Bounded header parsing before decoding;
   reject APNG/animated WebP, SVG and other formats. Browser `createImageBitmap`,
   Canvas and `toBlob`; fail clearly when APIs/codecs are unavailable. Verify
   requested MIME against actual Blob type; runtime encoder support probe. PNG/WebP
   retain alpha; JPEG composites onto an explicit color (default white).
   Bound output to 32 MiB; revoke object URLs, close bitmap, release canvas on reset.
5. **CSV ↔ JSON Converter**: UTF-8 text/file input ≤2 MiB, ≤10,000 data rows,
   ≤100 columns, ≤200,000 cells and ≤100,000 UTF-16 units per cell. CSV state
   machine follows existing reviewed CSV tools; comma/tab/semicolon delimiters,
   header or array mode, BOM and CR/LF normalization, quotes and multiline fields.
   Empty/duplicate headers and ragged rows fail. CSV values remain strings.
   JSON accepts arrays of flat objects (header mode) or equal-width arrays (no
   header); cell types are string/finite number/boolean/null only. Missing keys
   and null become empty CSV cells, with disclosed loss of type distinctions.
   Union keys in first-seen order; reject nested values. Formula-risk CSV cells
   receive a leading apostrophe; explain intentional change and limited round trips.
   Bound output to 4 MiB and 4,000,000 UTF-16 units before enabling actions;
   preview at most 20 records while copy/download retain the complete bounded output.
6. **Regex Tester**: ≤500 pattern code points (≤1,000 UTF-16 units), ≤100,000
   text code points (≤200,000 units), ≤1,000 displayed matches. Explicit flags
   `d g i m s u v y`; reject duplicates and u/v together before dispatch. Pattern
   compilation and matching occur only in a dedicated Blob Worker. Start the
   200 ms evaluation deadline after the worker's ready handshake (2 s startup
   limit). Terminate on timeout, input change, cancellation, reset, completion or
   navigation; reject stale messages. Zero-length matches advance by code point
   in Unicode mode, by code unit otherwise. Match details use UTF-16 offsets;
   highlight using text nodes/mark elements, never injected markup. Count is the
   displayed count, explicitly capped rather than an invented total. Bound worker
   response text to 2,000,000 units, result JSON to 4 MiB. Actual catastrophic
   backtracking, cancellation, termination and recovery are browser test gates.

No new package or website build dependency. The existing Tailwind CDN and shared
`../assets/consent.js` loader are preserved. All six pages explain local processing,
optional consent-based analytics and hosting/CDN requests. No input storage/upload.
Native labels/buttons, visible focus, ARIA error/status, keyboard operation and
320/375/768/1440 px layouts are required. Clipboard/download APIs are simulated
in automated tests; native dialogs, screen readers, physical devices and other
browser engines remain outside this validation scope.

## Design references reviewed 2026-11-05

- YouTube title reference: https://developers.google.com/youtube/data/reference/rest/v3/videos
- Canvas encoding/fallback: https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/toBlob
- Worker termination: https://developer.mozilla.org/en-US/docs/Web/API/Worker/terminate

Guides are editable planning aids; count conventions are disclosed, not a claim
of identical platform counting. The Instagram default is a configurable guide.

## Validation and delivery

Use existing generator dry runs and ignored staging; do not alter released pages,
consent assets, privacy notice, historical audits, domain or dashboard. Add each
tool to the explicit CI coverage map with nonempty structural/logic/browser scopes.
Run focused tests and canonical gates per tool, gated homepage proposals, then full
Python, Node, real Chromium, templates, consent and source/evidence validation.
Historical deployment checks must verify historical homepage bytes from Git and
separately verify current homepage additions, without rewriting the old evidence.
Expected completed development inventory: 50 RELEASED, 6 TESTED, 36 PLANNED,
1 BLOCKED, 93 total. Open a PR and await required checks; owner approval precedes
merge, then independent live source and behavior verification precedes RELEASED.
