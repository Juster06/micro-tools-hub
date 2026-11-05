# Task 20 — final scope and review before implementation

Approved main: `1ead1c37861b80c552446afbdb952c9248370bf9`, tree
`a0630e1865aba3ef0cace7fe4ccd83e0f2ebc31a`. PR34/35 merged; Pages42032230127
and post-merge CI42032231242 succeeded. Baseline:93 registered,62RELEASED,
0TESTED,0READY,30PLANNED,1BLOCKED. Fresh Task19.2 source/7smoke/real-consent
evidence is preserved separately in TASK_19_FINAL_PUBLIC_STATE.json. Those
public checks are earlier evidence, not publication evidence for Task20.
The original19 worktrees and two unrelated handoff edits are protected.

Owner authorizes exactly six existing IDs, implementation/testing/commits and
development PR. No merge, deployment, RELEASED transition, administrator bypass,
architecture/service/settings/consent changes or tool substitution. Checkpoint75;
generated milestone100 unchanged. TASK_20_SCOPE.json supplies detailed cases/limits.

## Final acceptance and distinctions

1. Excel Formula Generator: SUM/AVERAGE/COUNT/COUNTA/MIN/MAX/IF/ROUND only.
   Native typed argument rows (reference/number/text/boolean/condition), add/remove,
   English names, comma/semicolon argument separator, explanations/examples.
   Conditions are one unqualified A1 cell compared with a number/boolean/quoted
   literal; no arbitrary formula evaluation, external workbook references or AI.
   Reference grammar includes absolute cells, rectangular ranges and quoted sheets;
   Excel grid bounds enforced. IF exactly3 arguments; ROUND exactly2 with integral
   precision -308..308. Input <=8KiB,20args; output <=4KiB. Literal quotes escaped.
   Distinct from existing structural Excel Sandbox inspection.
2. Emoji Picker: pinned Unicode18.0 fully-qualified data,3963 unique sequences,
   names/groups/valid tone variants. Search <=100code points,100results per page,
   exact copy <=32code points, filters/reset and keyboard pagination. Native glyphs,
   no emoji API, external font or images. Runtime data <1MiB. Dataset references
   are trusted bundled data, never untrusted executable interpolation.
3. Image Compressor: static JPEG/PNG/WebP input <=5MiB,4096per side,8M pixels;
   explicit JPEG/WebP output/quality ceiling/target bytes; at most12 encodes within
   approximately10s,output <=8MiB. Sample a bounded quality grid and choose the
   highest tested quality meeting the target; if impossible report that honestly.
   No promise of globally optimal quality/exact target or lossless PNG optimization.
   Keep only candidate size/quality metadata and one selected Blob, releasing
   nonselected candidates rather than retaining12 output images.
   Report actual input/output size/savings; no-improvement keeps the original and
   does not call larger output compressed. No resizing. Preview/download of a
   smaller result, explicit JPEG background and reset. Distinct from a single
   quality-controlled format conversion; do not duplicate that existing UI alone.
4. PNG to ICO: native PNG decode and reviewed bounded ICO header/PNG-frame packer.
   Six selectable sizes16/32/48/64/128/256,transparent containment padding,
   <=5MiB PNG,4096per side,8M pixels,6frames,1MiB output. Actual data CRC/directory/
   offsets/sizes and independent Windows reader tests required. No BMP-only legacy
   compatibility claim. All source/encoder code is local and reviewable.
5. Resume Builder: plain-text heading/contact and section/item editing, max10sections
   and50items, keyboard add/remove/up/down, safe DOM preview and printable layout.
   Explicit validated versioned JSON import/export, <=50KiB, HTML <=250KiB;
   no autosave or personal-data storage/transport. Browser print-to-PDF only, no
   PDF library. No rich text, remote assets, ATS or hiring-outcome guarantee.
6. Passport Photo Layout Maker: one static portrait <=5MiB/4096side/8M pixels,
   user sizes10..100mm, A4/Letter,150/300dpi, margins/gaps, explicit count <=40,
   containment/white padding (no silent stretching/cropping), <=10M sheet pixels,
   PNG <=40MiB. Explicit sheet-fit errors; independent mm/pixel positions, preview,
   native print and100mm calibration ruler with100%/actual-size guidance.
   No face recognition, biometrics, jurisdiction rules or official acceptance.

## Dependency, resource and safety review

No backend, paid API, new framework or production package manager. Existing
Tailwind CDN and the unchanged shared consent loader remain. Unicode licenseV3,
original source, derived wrapper/version/hashes and attribution are pinned in
TASK_20_DEPENDENCIES.json. Only fully-qualified records are exposed; variation
selectors/ZWJ/tone sequences copied intact. Platform glyph differences disclosed.
Microsoft ICO directory and PNG payload documentation reviewed; independent native
reader/PNG decoding supplements our own binary checks. No custom image compression
codec: measured native Canvas encoders, actual MIME/signatures and bounded attempts.
Before browser decode reuse existing static image header checks, then recheck decoded
dimensions; deadlines, revision tokens, bitmap close and object-URL revocation.

Print uses fixed physical CSS page dimensions/margins plus a raster sheet computed
by round(mm*dpi/25.4). PNG exports also set a CRC-checked pHYs chunk to
round(dpi/0.0254) pixels per metre; only this metadata changes, with IDAT bytes
retained. Native PNG signatures/CRC/chunk bounds and sheet dimensions are verified. Quantization <=0.5pixel per coordinate; generated PDF page
dimensions and print CSS are testable, while physical printer calibration remains
user-controlled. Resume uses textContent/createElement; escaped standalone export
with restrictive CSP. Import strictly validates keys/types/lengths/version and
does not merge arbitrary objects into application state. No automatic drafts.

## Verification and lifecycle

For each tool: framework planner and scaffold dry run, READY scaffold, canonical
source, nonempty structural/logic/browser fixtures, focused independent Node and
real Chromium tests covering invalid/empty/Unicode/bounds, mobile/keyboard,
copy/download/reset and safe local processing. All68 canonical profiles, both
templates and full Python/Node/Chromium CI required. Consent tests add all six
new pages with isolated mock Google endpoints; no new real GA measurements or
public availability claim. Preserve prior62 HTML/registry records, all historical
audits, analytics/privacy/CNAME, workflow/runtime/deadline pins and existing checks.
Source checkpoint commit required before source-bound development audit. Only
after passing required scope: TESTED, publication:null, gated pending homepage
cards. Never RELEASED before separate authorized deployment and public verification.
