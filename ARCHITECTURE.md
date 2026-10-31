# Architecture

Verified baseline: 2026-10-31, source revision `1cf6a8ae0973918c95b6bf4a56b0a9708ace35f0`. Evidence: `audit/BASELINE_VERIFICATION.json`. This management change leaves the runtime HTML pages and domain configuration unchanged.

## Runtime structure

The site is static HTML. The root `index.html` contains the dashboard, four tool cards at the baseline, and a title-based search filter. Each tool is a standalone `<directory>/index.html` with inline vanilla JavaScript and a small inline stylesheet. There is no server API, database, package-based runtime, application build, service worker, or account system in the repository.

The browser loads Tailwind CSS v4 using `https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4`. This is an external runtime dependency for styling; it is not a fully offline bundle and is not pinned to an exact patch version. Tailwind Play CDN is the existing design choice, not a guarantee of production optimization. All existing tools otherwise use browser APIs and inline assets.

## Repository layout and responsibilities

```text
index.html                      dashboard and static initial count
CNAME                           existing custom domain
<tool-slug>/index.html           each implemented utility
README.md                       user/developer orientation
AGENTS.md                       permanent session instructions
PROJECT_MASTER_PLAN.md          vision and scope
TOOL_REGISTRY.json              canonical inventory, status, features and evidence
PROGRESS_TRACKER.md              generated counts plus current narrative
ROADMAP.md                      generated catalog/sequence plus delivery strategy
ARCHITECTURE.md                  verified design and constraints
DECISIONS.md                     dated significant choices
CHANGELOG.md                     meaningful change history
SESSION_HANDOFF.md               exact continuation instructions and Git context
scripts/project.mjs             check / sync / summary, Node built-ins only
scripts/project.test.mjs         management validator regression cases
audit/                          dated baseline and initial backlog reconciliation
```

Management scripts are developer tools. They do not load in the website, require a framework, add telemetry, or become a deployment build requirement. Node.js with built-in test runner and `structuredClone` support (Node 20+ recommended) runs them without installing dependencies.

## Routing and discovery

Use ordinary relative links. Tool cards point to `<slug>/index.html`; every tool links to `../index.html`. Existing nested URLs also load through the live host's directory index behavior. Preserve directory names for stable links.

The homepage normalizes NFKC, English locale lowercase, trimmed/repeated spaces, then matches each card's `data-title`. It does not currently search descriptions or registry JSON, filter categories, paginate, or generate cards from the registry. Do not assume adding a registry entry publishes a tool. Add the page and homepage card explicitly.

The management checker compares implemented entries with homepage links, initial count, existing directories, navigation, verification hashes, and generated documents. It never changes homepage HTML automatically.

## Design conventions

Retain `#020617` / slate-950 background, slate borders/panels/text, and indigo accents. Pages use system sans-serif, rounded panels, responsive grids, and readable input areas. Use visible focus, descriptive labels and headings, native buttons/inputs where possible, status text for errors/results, and reduced-motion handling. Do not use color as the only warning.

Advertisement containers are styled dashed-border placeholders. They have no actual AdSense integration. The social tool has phone-style, selectable feed cards; these are estimates, not platform-rendered embeds.

## Processing and existing limits

| Utility | Processing | Important boundary |
| --- | --- | --- |
| Social Counter | Unicode code-point counts; text-only previews; whitespace cleanup | Limits 280 / 3,000 / 2,200 / 4,000; LinkedIn hook 140; no full X weighting or guaranteed truncation |
| Excel Sandbox | Iterative tokenization, delimiter analysis and text-node formatting | Input limit 50,000 UTF-16 code units; visual indentation capped at 40 levels; no formula execution/full validation |
| Text Cleanser | Editorial phrase regex and text-node highlights | 200 wpm estimate; one saved replacement undo state; no explicit large-input cap; not AI detection |
| Stream Roulette | In-page curated catalog and random destination selection | Nine configured destinations; six filters; no current provider catalog queries or regional detection |

There are no file-processing tools yet. Planned file dependencies do not exist in the runtime. Before adding them, define supported formats, encrypted/corrupt-file handling, input/page/dimension limits, export fidelity, progress/cancellation, and memory cleanup. Large inputs may need workers or chunked processing. Do not promise PDF compression, metadata removal, font coverage, or browser codec support before verification.

## Security and privacy

- User input is rendered with text nodes or `textContent`. The social tool's `innerHTML` template uses static internal labels only; user captions never enter it.
- No current tool evaluates formulas, executes user JavaScript, calls AI APIs, uploads input, or uses draft storage. Clipboard output is an explicit action.
- Hosting and the Tailwind CDN receive ordinary request information. External streaming links open third-party sites with `noopener noreferrer`. These facts limit blanket “no network” claims.
- Future markup/SVG previews must isolate untrusted content, disable scripts and remote fetches, and prevent same-origin access. A formatter is not an excuse to execute input.
- Cryptography uses established browser primitives with explicit formats, secure-context detection, bounded resources, and failure tests. No custom cryptography or insecure fallback.
- Public source must never contain secret credentials. Public viewing does not grant editing rights; account authentication and collaborator/app permissions are managed outside these static files.
- A source scan or smoke test does not establish account security, deployment hardening, or freedom from vulnerabilities.

## Browser compatibility and QA

The existing code uses modern features including Unicode property escapes, regex lookbehind, `ResizeObserver`, optional clipboard APIs, and CSS `:has`. Target current evergreen browsers. Exact minimum versions and a complete cross-browser matrix have not been established.

The dated baseline was exercised with desktop Edge/Chromium, including mobile-sized viewports. This is not physical-device testing, Safari/Firefox testing, screen-reader certification, or a penetration assessment. The social counter additionally passed six viewport sizes and blocked-clipboard fallback checks. Detailed scope is recorded in the baseline JSON.

There was no committed test suite before this setup. The new committed tests exercise management validation, not all utility behavior. Browser smoke scripts used for the baseline were session-local and are not a portable committed UI suite. Future tool work should add reusable browser tests when warranted; do not claim this checker reruns the baseline browser interactions.

## Deployment and preservation

The existing `CNAME` is `everydaydigitalbox.com`; the homepage includes a Google site-verification meta tag. The live pages returned HTTP 200 with matching source at the baseline audit. GitHub-hosted infrastructure was observed, but repository Pages publishing-source settings and DNS administration were not inspected in this setup.

Commit/push and deployment are different events. For substantial work, open a feature-branch PR. After merge/publication, inspect the deployment and fetch the live HTML, confirm the intended implementation, and update release evidence. Preserve the domain and verification configuration. Never claim a PR is deployed merely because it exists.

## Scaling direction

Keep independent pages for now. As measured needs emerge, consider shared local assets, generated catalog metadata, category discovery, reusable parsers, and a compiled stylesheet. Preserve URLs and review architectural changes first; growth targets alone do not justify a wholesale rewrite.
