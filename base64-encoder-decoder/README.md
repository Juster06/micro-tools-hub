# Base64 Encoder and Decoder

Registry ID: `base64-encoder-decoder`. Category: developer. Canonical route: `base64-encoder-decoder/index.html`. Task 8 local development only; publication pending. Current lifecycle/evidence: TOOL_REGISTRY.json and the independent audit.

## Behavior and defaults

Default: encode Unicode text as strict UTF-8 bytes, then standard padded Base64 using + and /. Decode accepts only the standard alphabet with canonical padding and zero unused pad bits; no URL-safe alphabet, arbitrary whitespace or omitted required padding. ASCII-whitespace removal is optional for decode only and removes space, tab, CR and LF, not other Unicode whitespace. Empty input produces empty output. Encoding rejects lone UTF-16 surrogates; decoding rejects invalid UTF-8, overlong byte sequences, surrogate encodings and binary data that is not UTF-8 text. BOM and composed/decomposed Unicode are preserved with no normalization. UTF-8 byte statistics count the original encoded or decoded bytes; text counts use UTF-16 units. Output cap 400,000 UTF-16 units, bounded by the input cap (at most 300,000 UTF-8 bytes when encoding). This is a text converter, not binary-file support, encryption or secret protection. Export .txt.

## Interface, limits and privacy

Input limit: 100,000 UTF-16 code units, checked before processing; no silent maxlength truncation. Browser textareas normalize CR/CRLF to LF; the pure adapter preserves endings except the explicitly documented line/JSON operations. Statistics distinguish UTF-16 units from graphemes or bytes. Live preview uses 120 ms debounce with immediate invalidation of obsolete output/counts/actions. Clear restores defaults and focus. Simulated composition is deferred. Copy completion is revision-guarded; unavailable/denied clipboard selects current output with manual Ctrl+C/⌘C guidance. Exports use a fixed filename, UTF-8 Blob and object URL revocation even on failure. Empty results cannot be exported. Original input is preserved on errors.

Standalone HTML, vanilla JavaScript, existing Tailwind Play CDN v4 and expanded fallback CSS; no build/backend/new runtime dependencies. Local processing without input uploads, analytics, storage, dynamic HTML injection or evaluation. Hosting/CDN requests still occur for page/style delivery; fallback works with external requests blocked. Base64/URI transformations do not provide encryption or security validation.

## Independent testing

`python scripts/test_tool.py --id base64-encoder-decoder` runs nonempty exact logic fixtures and real Edge/Chromium browser cases through the existing framework. `node --test --test-concurrency=1 tests/tools/base64-encoder-decoder/*.test.mjs` adds independent boundary/error/oracle checks, stale-state/clipboard-race tests, download bytes/MIME/filename/revocation/failure, no transport/storage probes, simulated composition, labels/keyboard and hub navigation/search.

Viewport checks at 320/375/768/1440 use real Chromium and actual screenshots. Clipboard APIs, composition and download capture are simulated/in-memory. This does not certify native OS clipboard/IME/Save dialogs, physical devices, screen readers, every browser or universal performance. Exact executed totals, source revision and normalized hash are recorded in audit evidence after testing. No release/publication claim.
