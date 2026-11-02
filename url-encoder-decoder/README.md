# URL Encoder and Decoder

Registry ID: `url-encoder-decoder`. Category: developer. Canonical route: `url-encoder-decoder/index.html`. Task 8 local development only; publication pending. Current lifecycle/evidence: TOOL_REGISTRY.json and the independent audit.

## Behavior and defaults

Default: encodeURIComponent. Component decoding uses decodeURIComponent; full-URI modes use encodeURI/decodeURI. Full-URI encoding preserves reserved syntax such as :/?#&=+, while component encoding escapes it. Native component encoding leaves A–Z a–z 0–9 - _ . ! ~ * apostrophe and parentheses unchanged. decodeURI preserves percent escapes for reserved characters; component decoding decodes them. Plus signs stay plus on decode; encode-component produces %2B for plus. This is not application/x-www-form-urlencoded, a URL parser/validator, navigation or normalization. Malformed percent escapes/invalid encoded UTF-8 fail clearly; encoding rejects lone UTF-16 surrogates. Empty text produces empty output. No trimming or Unicode normalization. Output cap is 1,000,000 UTF-16 units; the 100,000 input-unit cap bounds native codec expansion below it. Export .txt.

## Interface, limits and privacy

Input limit: 100,000 UTF-16 code units, checked before processing; no silent maxlength truncation. Browser textareas normalize CR/CRLF to LF; the pure adapter preserves endings except the explicitly documented line/JSON operations. Statistics distinguish UTF-16 units from graphemes or bytes. Live preview uses 120 ms debounce with immediate invalidation of obsolete output/counts/actions. Clear restores defaults and focus. Simulated composition is deferred. Copy completion is revision-guarded; unavailable/denied clipboard selects current output with manual Ctrl+C/⌘C guidance. Exports use a fixed filename, UTF-8 Blob and object URL revocation even on failure. Empty results cannot be exported. Original input is preserved on errors.

Standalone HTML, vanilla JavaScript, existing Tailwind Play CDN v4 and expanded fallback CSS; no build/backend/new runtime dependencies. Local processing without input uploads, analytics, storage, dynamic HTML injection or evaluation. Hosting/CDN requests still occur for page/style delivery; fallback works with external requests blocked. Base64/URI transformations do not provide encryption or security validation.

## Independent testing

`python scripts/test_tool.py --id url-encoder-decoder` runs nonempty exact logic fixtures and real Edge/Chromium browser cases through the existing framework. `node --test --test-concurrency=1 tests/tools/url-encoder-decoder/*.test.mjs` adds independent boundary/error/oracle checks, stale-state/clipboard-race tests, download bytes/MIME/filename/revocation/failure, no transport/storage probes, simulated composition, labels/keyboard and hub navigation/search.

Viewport checks at 320/375/768/1440 use real Chromium and actual screenshots. Clipboard APIs, composition and download capture are simulated/in-memory. This does not certify native OS clipboard/IME/Save dialogs, physical devices, screen readers, every browser or universal performance. Exact executed totals, source revision and normalized hash are recorded in audit evidence after testing. No release/publication claim.

UTF-8 download refuses a result containing isolated UTF-16 surrogates, preserving the result/original and reporting the reason instead of allowing Blob conversion to replace them. JSON pretty/compact modes escape these values; validation preserves raw valid JSON text. URI decoding follows native behavior for literal unescaped text.
