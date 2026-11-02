# JSON Formatter

Registry ID: `json-formatter`. Category: data. Canonical route: `json-formatter/index.html`. Task 8 local development only; publication pending. Current lifecycle/evidence: TOOL_REGISTRY.json and the independent audit.

## Behavior and defaults

Default: native JSON.parse followed by JSON.stringify with two spaces. Choose four spaces or a tab for pretty-print; compact removes formatting whitespace. Validate preserves the original valid text exactly, without pretty-printing. Blank input is an error. All JSON root types are accepted, including null, arrays and primitives. Errors include native parse diagnostics; wording differs by browser. This is syntax validation, not a JSON Schema validator or repair tool. Duplicate object keys use the last value, native object-key ordering applies, and JavaScript IEEE-754 numeric precision/negative-zero serialization apply. Large integer precision is not preserved; use strings for exact identifiers. Nonfinite parsed numbers (such as 1e400) are rejected rather than silently serialized as null. Nesting is limited to 100 containers (strings/escapes do not add depth); output is limited to 1,000,000 UTF-16 units with an error, never truncation. Node count includes the root and every parsed property/array value, not duplicate keys discarded by JSON.parse. No Unicode normalization; JSON.stringify escaping applies. Export is UTF-8 .json.

## Interface, limits and privacy

Input limit: 100,000 UTF-16 code units, checked before processing; no silent maxlength truncation. Browser textareas normalize CR/CRLF to LF; the pure adapter preserves endings except the explicitly documented line/JSON operations. Statistics distinguish UTF-16 units from graphemes or bytes. Live preview uses 120 ms debounce with immediate invalidation of obsolete output/counts/actions. Clear restores defaults and focus. Simulated composition is deferred. Copy completion is revision-guarded; unavailable/denied clipboard selects current output with manual Ctrl+C/⌘C guidance. Exports use a fixed filename, UTF-8 Blob and object URL revocation even on failure. Empty results cannot be exported. Original input is preserved on errors.

Standalone HTML, vanilla JavaScript, existing Tailwind Play CDN v4 and expanded fallback CSS; no build/backend/new runtime dependencies. Local processing without input uploads, analytics, storage, dynamic HTML injection or evaluation. Hosting/CDN requests still occur for page/style delivery; fallback works with external requests blocked. Base64/URI transformations do not provide encryption or security validation.

## Independent testing

`python scripts/test_tool.py --id json-formatter` runs nonempty exact logic fixtures and real Edge/Chromium browser cases through the existing framework. `node --test --test-concurrency=1 tests/tools/json-formatter/*.test.mjs` adds independent boundary/error/oracle checks, stale-state/clipboard-race tests, download bytes/MIME/filename/revocation/failure, no transport/storage probes, simulated composition, labels/keyboard and hub navigation/search.

Viewport checks at 320/375/768/1440 use real Chromium and actual screenshots. Clipboard APIs, composition and download capture are simulated/in-memory. This does not certify native OS clipboard/IME/Save dialogs, physical devices, screen readers, every browser or universal performance. Exact executed totals, source revision and normalized hash are recorded in audit evidence after testing. No release/publication claim.

UTF-8 download refuses a result containing isolated UTF-16 surrogates, preserving the result/original and reporting the reason instead of allowing Blob conversion to replace them. JSON pretty/compact modes escape these values; validation preserves raw valid JSON text. URI decoding follows native behavior for literal unescaped text.
