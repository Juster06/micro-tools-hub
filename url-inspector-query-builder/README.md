# URL Inspector & Query Builder

Canonical route: `url-inspector-query-builder/index.html`.

TESTED — publication pending. Local source checkpoint `6437b046e5827d82d2f3dbf7668dc451c51c2614`; evidence: `audit/URL_INSPECTOR_QUERY_BUILDER_VERIFICATION.json`. No live-publication claim.

Explicit Inspect/Build uses native URL and URLSearchParams; never visits, fetches, validates destination safety or stores URLs. Credentials/userinfo, raw spaces/controls, backslashes and non-HTTP(S) schemes rejected. Input ≤8192 UTF-8 bytes (also ≤8192 UTF-16 units); ≤100 query pairs; fields ≤2048 units and combined edited fields ≤16384 UTF-8 bytes. Output URL ≤16384 UTF-8 bytes. Duplicate names and order preserved. Inspect preserves native URL representation; editing serializes query spaces as + and can change signed URLs. Fragment contents omitted from component summary but preserved in the copied URL. Query values appear only as needed for editing/output; avoid pasting secrets.

Inputs stay in browser memory: no uploads, input logging, automatic saved drafts or external processing. Hosting and existing Tailwind CDN requests still occur. Shared analytics requires consent and excludes tool inputs. Copy places text on your system clipboard; permission may fail with manual-copy guidance. Text downloads use bounded UTF-8 Blobs and temporary URLs are released.

Native APIs only; no new runtime package. Generic run tests bounded preparation only; native URL parsing/serialization is exercised separately in Node with native APIs and real Chromium.

- https://url.spec.whatwg.org/

Clipboard/download automation is simulated/captured; no native OS dialog, physical device, cross-browser or screen-reader certification. Existing PDF deferral, blocked compressor and consent/privacy code are unchanged.
