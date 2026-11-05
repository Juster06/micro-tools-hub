# Task 19 — scoped development and design review

Baseline main: `3178f70802a96f181fd82251d417abd1dd0ad76b`; 93 registered,
56 RELEASED, 36 PLANNED, 1 BLOCKED. Both Task 18 PRs are merged. Pages
41979618835 and post-merge CI 41979619839 succeeded for this exact commit.
Task 18.2 independently checked 61 public sources + six directory routes,
56 visible canonical Live cards and seven fresh browser smoke/navigation cases.
Consent acceptance/rejection/withdrawal were checked with real collection HTTP 204.
This is prior public evidence, not fresh publication evidence for Task 19.

Owner scope: six selected registry entries; implementation, testing, commits and
development PR only. No merge, deployment, administrator bypass, RELEASED
transition, privacy/consent behavior/settings changes or new tool IDs.
Original 17 worktrees are preserved; two unrelated handoff edits are protected.
Checkpoint 75; existing generated milestone 100 remains unchanged.

## Distinctness and acceptance

1. Password Generator: character-pool passwords, unlike numeric draws/UUIDs.
   Length 8–128, quantity 1–20, serialized output including newlines ≤2,560.
   Selected sets form a pool; each result need not contain every selected set.
   No forced insertion/shuffling that would silently bias the distribution.
2. CSV to TXT: positional field placeholders and selected CSV columns; existing
   JSON to TXT accepts JSON, and CSV converters do not provide row templates.
   UTF-8 CSV ≤1 MiB, ≤10,000 data rows, ≤100 columns, output ≤2 MiB.
   Delimiter/header choice; strict quoting/ragged-row errors; CR/LF retained inside
   quoted fields. Templates ≤4,096 bytes: {1} is column 1, {{/}} literal braces.
   Blank template joins selected fields with ` | `. No executable interpolation.
3. Passphrase Generator: 6–12 independently selected words, 1–10 phrases, space/
   hyphen/underscore separators, serialized output ≤4,096 characters. Distinct
   memorable-word task shares the reviewed random-index algorithm, not passwords.
4. QR Code Generator: text ≤1,000 UTF-8 bytes, explicit L/M/Q/H correction,
   local encoder, four-module quiet zone, PNG ≤2,048 per side and ≤4 MiB.
   No URL service, logos, destination fetching or scanning-safety certification.
5. Image Cropper: numeric x/y/width/height and free/1:1/4:3/16:9 ratio checks;
   PNG export, exact integer coordinates against decoded orientation. Existing
   resizer/rotator/converter do not offer arbitrary crop rectangles.
   Static JPEG/PNG/WebP ≤5 MiB, ≤4,096 per side, ≤8M decoded pixels, ≤32 MiB PNG.
   Complete keyboard workflow; no dragging required. Unsupported animations fail.
6. CSV Data Cleaner: column-scoped trimming and explicit empty-value preserve/
   replace/reject policy. Preview before Apply/export; existing viewer inspects
   and duplicate-row tool handles deduplication, neither performs these transforms.
   Same CSV bounds as above; 20-row bounded before/after preview; no type inference.
   Order: strict parse → selected-column trim → selected empty-value policy →
   preview → explicit Apply → CSV quoting and formula safeguards. Unselected
   cleaned values stay identical; export safeguards may prefix formula-risk cells
   in any column/header and are separately counted/disclosed in the preview.

## Security/dependency review before implementation

No architecture change, paid library, backend, new framework or account system.
See TASK_19_DEPENDENCIES.json for versions, licence/attribution, payloads and hashes.
QR: Nayuki v1.8.0 MIT, immutable upstream commit; inspected transport-free TS/JS,
compiled once with pinned TypeScript 5.9.3. jsQR 1.4.0 Apache-2.0 is an independent
test-only decoder; retain its licence. No dependency is downloaded by deployed
tool processing. Existing Tailwind page-delivery requests remain disclosed.
Wordlist: preserve/hash original EFF list, validate all 7,776 distinct words and
dice-code coverage, locally bundle an attributed frozen wrapper. EFF CC BY 4.0
policy reviewed; no contrary source notice found. No artificial wordlist substitutes.

Randomness design: require secure context and crypto.getRandomValues. Draw unsigned
32-bit values; reject the incomplete modulo interval before mapping into the pool.
Bound retries and fail closed on unavailable/throwing/nonproductive randomness.
No Math.random fallback, saved drafts, auto-generation, secret logs, downloads or
input telemetry. Secret outputs clear on settings changes/reset/pagehide; JS memory
erasure and system clipboard privacy cannot be certified. Clipboard requires an
explicit user action. Canonical logic fixtures validate settings; specialized Node
tests inject deterministic random words only to exercise rejection paths, and real
Chromium tests verify actual Web Crypto use separately.

CSV parser is a bounded state machine, never eval/Function/HTML parsing. Reject
invalid UTF-8 upload, NUL, unterminated quotes, text after a closing quote, embedded
quotes in unquoted fields and ragged records. Count output UTF-8 bytes incrementally
before append, including template expansion/header repetition. Missing cells are
malformed rows; empty cells have explicit policy. Rendering uses textContent/value.
Image review reuses the approved bounded static header-validation approach before
createImageBitmap, rechecks actual dimensions, revokes URLs/closes bitmaps, guards
against stale async results, bounds output, and makes no metadata-removal guarantee.

## Validation and release boundary

Each tool: inspected framework generator dry run, staged scaffold, canonical
promotion, nonempty structural/logic/browser suites, focused tests for all modes,
invalid/empty/Unicode/boundaries, copy/export/reset, responsive widths and keyboard.
Specialized tests: unbiased sampling/failures, exact wordlist hashes, independent
QR decoding including exported PNG pixels, crop pixels/transparency, malformed CSV,
expansion limits and preview/apply invalidation. Consent tests cover every new page
before choice, rejection, acceptance/reacceptance, navigation and withdrawal.
Mocks are limited to clipboard/download capture and isolated Google test endpoints;
no real Google measurements or public availability claims for these unpublished tools.
Preserve all 56 released HTML sources/records/evidence and shared consent/privacy.
Full Python/Node/Chromium required CI scopes and templates remain mandatory.
TESTED requires actual matching-source evidence; publication remains null.

Final dependency formatting: remove trailing line whitespace from the copied TypeScript and compiled JavaScript, and extra licence EOF blank lines. No licence wording or algorithm changes. Preserve upstream/raw digests alongside normalized delivered hashes; ten QR tests passed again after normalization.
