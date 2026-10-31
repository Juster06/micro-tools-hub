# Verified current state — 2026-10-31

## Source and Git baseline

- Repository: <https://github.com/Juster06/micro-tools-hub>.
- Public website: <https://everydaydigitalbox.com/>.
- Audit began from a fresh clean clone of `main` at `1cf6a8ae0973918c95b6bf4a56b0a9708ace35f0`.
- Current setup branch: `docs/persistent-project-memory`.
- Existing tracked files at baseline: `CNAME`, `README.md`, homepage HTML, and one HTML page in each of `excel-sandbox`, `text-cleaner`, `streaming-roulette`, and `social-counter`.
- No AGENTS, project plan, registry, roadmap, progress tracker, architecture/decision/changelog/handoff documents, package manifest, CI configuration, or committed validation scripts existed before this setup.
- The separate owner working directory is a downloaded/editable copy without `.git`; its files must not be described as a clean Git checkout. New management documents are synchronized there without adding Git metadata or replacing tool pages.

## Inspected source

The complete README, homepage, all existing utility sources, directory inventory, `CNAME`, Git status, and recent commit history were inspected. The README accurately describes the current capabilities, but its statement about no committed validation suite needs updating for this management setup.

The homepage has four working linked cards and title-based search. Tool pages use the existing standalone HTML/Tailwind/vanilla-JavaScript architecture. No runtime source changes are needed for this planning task.

## Verification evidence

`BASELINE_VERIFICATION.json` records the source revision, browser version, tested cases, page hashes, live URLs, timestamps, and matching publication. All five pages returned HTTP 200 and matched their source after documented whitespace normalization.

Local Edge/Chromium functional checks covered hub filtering/reset, text phrase replacements/undo/copy/safe rendering/large input, formula structure/copy/errors/input limit, roulette matching/non-repetition/outbound protection, and social counts/previews/copy fallback. All pages were checked for horizontal overflow at narrow and desktop sizes; the social page had additional boundary and viewport checks.

The first roulette test attempt tried to click the visually hidden native radio input and timed out because the visible label child intercepted it. The test was corrected to click the user-facing label, and the full baseline rerun passed. This was a test interaction issue; runtime source was not changed.

The browser runs observed only the expected external Tailwind styling GETs; no test input was uploaded. This is evidence for those interactions, not a comprehensive network/security guarantee.

## Features and limitations to preserve

- Social limits: 280 / 3,000 / 2,200 / 4,000 code points; LinkedIn hook warning at more than 140; estimated previews; clean/copy fallback. X weighted counts can differ.
- Excel: structure formatter and delimiter diagnostics, 50,000 UTF-16-code-unit limit; no evaluation or complete syntax validation.
- Text: rule-based phrase replacement, word count, 200-wpm estimate, and replacement undo; not AI detection; no explicit input cap.
- Streaming: nine curated providers, six genre choices, non-repeating selection where alternatives exist; provider catalogs/rights/region availability are not live-validated here.
- Tailwind Play CDN remains an external, non-patch-pinned styling dependency. There is no backend, draft storage, accounts, real AdSense code, or analytics in the current application source.

## Not verified in this setup

Safari/Firefox and physical mobile devices; screen-reader behavior; a full vulnerability assessment; maximum performance of every tool; live provider catalogs; GitHub Pages publishing-source settings; DNS ownership/settings; collaborator/app access; account 2FA. No access, domain, or deployment settings were changed.

## Publication and new documentation

The existing utility pages are released according to the dated baseline evidence. The management files are separate new development artifacts. Their presence on a feature branch or in a local copy does not mean that `main` contains them or that a deployment has published them. Verify delivery using Git and the linked pull request before describing merge/publication status.
