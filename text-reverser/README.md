# Text Reverser

Registry ID: `text-reverser`. Category: text. Canonical route: `text-reverser/index.html`. Task 8 public release verified 2026-11-02; [Live tool](https://everydaydigitalbox.com/text-reverser/). Separate publication evidence: audit/TEXT_REVERSER_RELEASE_VERIFICATION.json. Current lifecycle/evidence: TOOL_REGISTRY.json and the independent audit.

## Behavior and defaults

Default: reverse grapheme clusters across the whole input using native Intl.Segmenter (und locale). Emoji sequences and combining marks remain together where supported; engine Unicode versions may differ. Without Segmenter, reverse Unicode code points and show an explicit fallback warning: compound emoji/marks can separate. Word mode reverses non-whitespace tokens while keeping each original whitespace slot (including tabs and line endings); punctuation stays attached to its token. Whitespace means JavaScript \s, not linguistic word segmentation. Line mode splits CRLF, CR or LF, reverses records and joins with LF. Empty input has zero units; a trailing separator adds a blank record. No normalization. Output never exceeds input size. Unit count follows the selected policy, not UTF-16 character count.

## Interface, limits and privacy

Input limit: 100,000 UTF-16 code units, checked before processing; no silent maxlength truncation. Browser textareas normalize CR/CRLF to LF; the pure adapter preserves endings except the explicitly documented line/JSON operations. Statistics distinguish UTF-16 units from graphemes or bytes. Live preview uses 120 ms debounce with immediate invalidation of obsolete output/counts/actions. Clear restores defaults and focus. Simulated composition is deferred. Copy completion is revision-guarded; unavailable/denied clipboard selects current output with manual Ctrl+C/⌘C guidance. Exports use a fixed filename, UTF-8 Blob and object URL revocation even on failure. Empty results cannot be exported. Original input is preserved on errors.

Standalone HTML, vanilla JavaScript, existing Tailwind Play CDN v4 and expanded fallback CSS; no build/backend/new runtime dependencies. Local processing without input uploads, analytics, storage, dynamic HTML injection or evaluation. Hosting/CDN requests still occur for page/style delivery; fallback works with external requests blocked. Base64/URI transformations do not provide encryption or security validation.

## Independent testing

`python scripts/test_tool.py --id text-reverser` runs nonempty exact logic fixtures and real Edge/Chromium browser cases through the existing framework. `node --test --test-concurrency=1 tests/tools/text-reverser/*.test.mjs` adds independent boundary/error/oracle checks, stale-state/clipboard-race tests, download bytes/MIME/filename/revocation/failure, no transport/storage probes, simulated composition, labels/keyboard and hub navigation/search.

Viewport checks at 320/375/768/1440 use real Chromium and actual screenshots. Clipboard APIs, composition and download capture are simulated/in-memory. This does not certify native OS clipboard/IME/Save dialogs, physical devices, screen readers, every browser or universal performance. Exact executed totals, source revision and normalized hash are recorded in audit evidence after testing. Actual deployment/public-source/behavior evidence is recorded in the separate release audit.

UTF-8 download refuses a result containing isolated UTF-16 surrogates, preserving the result/original and reporting the reason instead of allowing Blob conversion to replace them. JSON pretty/compact modes escape these values; validation preserves raw valid JSON text. URI decoding follows native behavior for literal unescaped text.
