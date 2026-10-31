# Decision log

## 2026-10-31 — Repository files are the continuity mechanism

**Decision:** Use AGENTS, handoff, master plan, registry, progress, roadmap, architecture, decision log, and changelog files in the repository.

**Reason:** Future sessions need inspectable project state rather than assumed conversation memory.

**Alternatives:** Depend on past chat, a private project-management service, or a database.

**Consequences:** Every session reads and updates the files; Git delivery state matters. An unmerged branch is not automatically available on `main`. This establishes no scheduler or unattended activity.

## 2026-10-31 — Keep the current static architecture

**Decision:** Retain standalone HTML, inline vanilla JavaScript, and the existing slate/indigo Tailwind Play CDN design.

**Reason:** Current utilities work without accounts, build tooling, or a backend. Initial work is organization and planning.

**Alternatives:** Rewrite with a framework, add a database/backend, or compile shared styling immediately.

**Consequences:** Runtime source remains unchanged in this setup. Duplication across pages is accepted for now; shared assets and compiled CSS remain a measured future improvement. Developer-only Node checks introduce no website build requirement.

## 2026-10-31 — Canonicalize overlapping proposals

**Decision:** Map Word Counter and Reading Time Calculator to existing Text Cleanser features; map Extra Space Remover to existing Social Counter cleanup. Combine JPEG/PNG/WebP conversion, bidirectional CSV/JSON conversion, text/file SHA-256 checks, and Markdown conversion/preview into canonical utilities.

**Reason:** Avoid duplicate implementations and inflated tool counts while retaining every proposed need.

**Alternatives:** Create a separate page for every initial name or drop overlaps silently.

**Consequences:** All original proposals remain traceable in the reconciliation table. Related distinct tasks retain separate IDs; future scope changes must explain a split before reserving another ID.

## 2026-10-31 — Status and publication require evidence

**Decision:** Use the requested status vocabulary and source hashes, dated test scope, and live source-match evidence for released tools. Label existing verification as a smoke baseline.

**Reason:** “Implemented”, “tested”, and “published” describe different facts. HTTP 200 alone can serve an error/old page.

**Alternatives:** Mark files released when created or count every planned directory as a tool.

**Consequences:** Source changes invalidate the recorded hash until retested; planned entries carry no verification date. The checker does not contact the network or rerun UI behavior, so future sessions must perform appropriate tests before updating evidence.

## 2026-10-31 — Browser-native transformations first

**Decision:** Prioritize twenty bounded transformations/calculators/productivity tasks before large-format and security-heavy work. Case Converter is first. PDF Compressor is blocked on feasibility evidence.

**Reason:** Grow useful functionality while reducing dependency and resource risks. Basic tasks have clear acceptance cases and no external service requirement.

**Alternatives:** Start all PDF tools, introduce an AI backend, or optimize traffic first.

**Consequences:** Library-dependent work remains planned; cryptography, hostile previews, compression, and complex parsers have design gates. Milestones do not imply deadlines.

## 2026-10-31 — Preserve public access and defer promotion automation

**Decision:** Keep website/code public and leave access/domain settings unchanged. Defer real ads, analytics, SEO monitoring, and the proposed 9–11-day observation concept.

**Reason:** The owner wants public use with authorized editing and currently prioritizes utility development.

**Alternatives:** Make the repository private, add ad/traffic scripts, or schedule recurring SEO changes.

**Consequences:** No credentials or account settings enter these documents; no automation is created. Architecture/services/access changes need the relevant owner approval.
