# Markdown Converter & Previewer — Task 22

Current status: **RELEASED and publicly verified**. PR #41 is merged; the public registry records 75 RELEASED tools at main `2234bffef4cf376357ccb7cae3d1c0ec105d08c8`. Task 22.2 fresh public functionality, isolation and real consent checks passed on 2026-11-06. Pages deployment 42218207674 and all four post-merge Functional CI 42218207882 checks passed. See the current project handoff and `audit/MARKDOWN_CONVERTER_PREVIEWER_RELEASE_VERIFICATION.json`; historical audit evidence remains unchanged. GA4 property-level reporting remains unverified.

Task 22 is complete. Task 23 has not begun and requires separate owner authorization.

## Historical Task 22.1 release-verification proposal

Current status: Task 22.1 public source, functionality, isolation and real consent verification passed at `64a19c6bc1ee2dfbd81cf9ffa6b1ca00f15c8140`. RELEASED transition is proposed in the separate release-verification branch, awaiting owner authorization to merge/deploy. The currently deployed registry remains 74 RELEASED / 1 TESTED. See `audit/MARKDOWN_CONVERTER_PREVIEWER_RELEASE_VERIFICATION.json`.

## Historical development checkpoint

Development: publication pending. This tool is not independently publicly verified or RELEASED.

Converts the common GFM subset locally in a fresh disposable Worker using pinned Marked 18.1.3 and independent parse5 8.1.0 allowlist serialization. HTML source is shown as text. Raw HTML is escaped; images become alt text. Tables, fenced code, strikethrough and autolinks are supported without styling/extensions. Task-list checkbox controls, HTML interpretation, math, diagrams, syntax highlighting, IDs and custom attributes are unsupported.

Only explicit HTTP(S) export links without credentials survive URL validation. Relative, mailto, data, javascript, file and blob destinations are removed. Preview removes all links; it uses an empty sandbox, opaque origin, no-referrer and restrictive CSP. Download is a standalone UTF-8 HTML document with CSP, not raw parser output. Copy is the sanitized fragment. No drafts are stored and no input is uploaded. Hosting and existing styling CDN requests still occur; analytics remains consent-controlled.

Limits: 32 KiB UTF-8 input; 128 KiB intermediate HTML, fragment, and complete preview/download documents individually; 4,096 Markdown token objects and HTML nodes; depth 64; attributes at most 64 per HTML element; 2-second Worker deadline. Reset, editing and cancellation terminate workers and discard results. These controls are not a hard browser heap guarantee.

The generic framework adapter validates job preparation; specialized Node/browser suites execute the real parser and sanitizer. Clipboard/download APIs are captured in browser tests; native OS permissions/dialogs and screen-reader/device certification are excluded. Public release verification remains a separate authorized task. PDF processing remains deferred.

A cumulative 128 KiB link-rendering budget rejects repeated long reference destinations before concatenating the complete HTML string. The additional 31-case scratch gate passed before adopting this guard; the maintained production suite includes its amplification regression.
