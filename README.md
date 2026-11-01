# Everyday Digital Box — WebUtils Hub

## Reusable utility development

Task 4 provides development-only scaffolding, templates, functional checks, homepage patch previews and ordered batch proposals. Read the [utility contract](TOOL_CONTRACT.md) and [developer guide](TOOL_DEVELOPMENT_GUIDE.md) before implementing a tool. Use `python scripts/plan_tool_batch.py --count 10` to inspect READY work; scaffold generation accepts existing READY entries only, and an inspected dry run precedes implementation. Select work only within the latest owner-authorized scope.

Python 3.10+ standard library runs the generator/planner/structural checks; Node 22.4+ and an installed Chromium browser enable actual logic/interaction tests. Tool users need only their browser. Public website, GitHub repository and existing dashboard shortcuts remain unchanged.

**Small tools. Everyday wins.**

Everyday Digital Box is a collection of free, focused browser utilities for everyday writing, spreadsheet work, social content, and entertainment discovery. The website is branded **WebUtils Hub**, and its GitHub repository is named **micro-tools-hub**.

The project is intended for creators, writers, students, developers, and office workers who want to finish a small task without installing software or creating an account. It currently contains six released standalone tools, linked from a searchable dashboard.

## Project links

| Resource | Link |
| --- | --- |
| Live website | [everydaydigitalbox.com](https://everydaydigitalbox.com/) |
| GitHub repository | [Juster06/micro-tools-hub](https://github.com/Juster06/micro-tools-hub) |
| Project owner | [Juster06 on GitHub](https://github.com/Juster06) |
| Source branch | [main](https://github.com/Juster06/micro-tools-hub/tree/main) |
| Issues and suggestions | [GitHub Issues](https://github.com/Juster06/micro-tools-hub/issues) |
| Proposed changes | [Pull requests](https://github.com/Juster06/micro-tools-hub/pulls) |

## Development continuity and project planning

Future development sessions should begin with [AGENTS.md](AGENTS.md) and [SESSION_HANDOFF.md](SESSION_HANDOFF.md), inspect Git state, and verify the actual source before choosing work. These repository files preserve project state; they do not schedule agents or guarantee that an unmerged branch is available in another checkout.

| Document | Purpose |
| --- | --- |
| [Project master plan](PROJECT_MASTER_PLAN.md) | Authoritative vision, priorities, constraints, milestones, and deferred scope |
| [Tool registry](TOOL_REGISTRY.json) | Canonical machine-readable inventory, statuses, features, dependencies, and evidence |
| [Progress tracker](PROGRESS_TRACKER.md) | Counts derived from the registry and current work |
| [Roadmap](ROADMAP.md) | Prioritized next-twenty sequence and complete category catalog |
| [Architecture](ARCHITECTURE.md) | Verified runtime structure, design, privacy, limits, and deployment boundaries |
| [Decisions](DECISIONS.md) | Reasons and consequences of significant choices |
| [Changelog](CHANGELOG.md) | Meaningful changes separated from publication claims |
| [Baseline audit](audit/CURRENT_STATE.md) | Source-backed current state and verification scope |
| [Backlog reconciliation](audit/BACKLOG_RECONCILIATION.md) | Each initial proposed utility mapped to its canonical tool |
| [Management commands](scripts/README.md) | Python status workflow, reports, synchronization, and tests; existing Node compatibility |

Tool development is the current priority. Growth milestones are aspirations; new tools are built one at a time with scoped validation. Analytics, advertising integration, traffic generation, and SEO automation are deferred. The future 9–11-day SEO observation idea is recorded in the master plan only.

On Windows, the **Everyday Digital Box — Project Status** desktop/Start menu launcher now opens the [local Project Control Dashboard](scripts/DASHBOARD.md), with overview/milestones, registry exploration, queue, validation, activity, blockers and Quick Actions. It reuses the existing tracking workflow and stays separate from the website. Create/recreate shortcuts with `python scripts/install_status_shortcut.py`; existing targets remain valid. See [Windows launcher instructions](scripts/WINDOWS_LAUNCHER.md) for manual taskbar pinning, requirements and limitations.

## What the project provides

- A responsive, dark slate and indigo dashboard with searchable tool cards.
- Six released utilities including Duplicate Line Remover, using vanilla JavaScript for browser processing.
- Standalone HTML pages that can be edited or hosted without an application build step.
- No application backend, database, user accounts, or API keys.
- Consistent navigation back to the hub from each tool.
- Features such as visible keyboard focus, descriptive labels, status messages, and reduced-motion handling.
- Styled advertisement placeholders for possible future monetization.

## Case Converter — released and live verified

[Case Converter](case-converter/index.html) offers uppercase, lowercase, Title Case, Sentence case, Capitalize Words, Alternating Case and Inverse Case, with live character/word/line counts, unchanged original input, Copy, UTF-8 download and Clear. Read [its rules and test scope](case-converter/README.md) before relying on language-specific casing. Input stays in the browser; the limit is 100,000 UTF-16 units.

Task 5 was merged through [PR #9](https://github.com/Juster06/micro-tools-hub/pull/9). [Live Case Converter](https://everydaydigitalbox.com/case-converter/) behavior and deployed source identity were verified on 2026-11-01 before its RELEASED transition. See [release evidence](audit/CASE_CONVERTER_RELEASE_VERIFICATION.json) for deployment, source hash and actual test scope. The hub uses the released “Live” presentation; current inventory is **six released tools**, 6/25 (24%). Use `python scripts/test_tool.py --id case-converter` for scoped regression tests.

## Duplicate Line Remover — released and live verified

[Duplicate Line Remover](duplicate-line-remover/index.html) keeps the first unique line with optional case-insensitive matching, surrounding-whitespace comparison, blank removal and deterministic sorting. It preserves original retained text, shows five actual line statistics, updates live, and supports copy/UTF-8 download/Clear. See [rules, limits and tests](duplicate-line-remover/README.md) and [release audit](audit/DUPLICATE_LINE_REMOVER_RELEASE_VERIFICATION.json), with original local evidence retained. [PR #10](https://github.com/Juster06/micro-tools-hub/pull/10) was merged, and actual public behavior plus exact deployed source identity passed on 2026-11-01 before the RELEASED transition. [Open the live tool](https://everydaydigitalbox.com/duplicate-line-remover/). Its hub card uses the established Live presentation. Six tools are released; milestone 6/25 (24%).

## Task 7 — three local tested tools, publication pending

These tools are implemented and independently tested on the local Task 7 feature branch. They are **not released or published**. Their local hub cards say **Tested · publication pending**; the six existing released tools and 6/25 (24%) milestone remain unchanged.

| Local tool | Function and exact rules |
| --- | --- |
| [Text Sorter](text-sorter/index.html) | Stable lexical/numeric line sorting, explicit invalid-number/blank policy, copy and UTF-8 download. [Rules/tests](text-sorter/README.md). |
| [Slug Generator](slug-generator/index.html) | Unicode/ASCII slugs with documented accent/normalization policies. [Rules/tests](slug-generator/README.md). |
| [Find and Replace](find-and-replace/index.html) | Literal replacement preview, match counts, Apply and one-level Undo. [Rules/tests](find-and-replace/README.md). |

Selection and independent test/evidence workflow: [Task 7 development plan](audit/TASK_7_DEVELOPMENT_PLAN.md). Open these pages from the unchanged active checkout; remote URLs have not been published. No push, PR, merge or deployment is part of this local task.

## Available tools

| Tool | Purpose | Open the tool |
| --- | --- | --- |
| Duplicate Line Remover | Remove repeated lines with configurable matching and accurate statistics. | [Live tool](https://everydaydigitalbox.com/duplicate-line-remover/) · [Source](duplicate-line-remover/index.html) |
| Case Converter | Seven text-case transformations with live counts, copy and UTF-8 download. | [Live tool](https://everydaydigitalbox.com/case-converter/) · [Source](case-converter/index.html) |
| Social Media Character Counter & Live Previewer | Check caption lengths, preview opening lines, and clean spaces before copying. | [Live tool](https://everydaydigitalbox.com/social-counter/) · [Source](social-counter/index.html) |
| Excel Formula Sandbox & Analyzer | Make nested formulas easier to read and inspect their structure. | [Live tool](https://everydaydigitalbox.com/excel-sandbox/) · [Source](excel-sandbox/index.html) |
| AI Text Footprint Cleanser | Highlight listed phrases and replace them with simpler wording. | [Live tool](https://everydaydigitalbox.com/text-cleaner/) · [Source](text-cleaner/index.html) |
| Free Stream Roulette | Choose a genre and discover a free streaming destination. | [Live tool](https://everydaydigitalbox.com/streaming-roulette/) · [Source](streaming-roulette/index.html) |

### Social Media Character Counter & Live Previewer

Type or paste a caption once to see all four platform counters update together:

| Platform | Configured character limit | Additional guidance |
| --- | ---: | --- |
| X / Twitter | 280 | A progress bar and text warning flag captions beyond the limit. |
| LinkedIn | 3,000 | Captions beyond 140 characters receive an opening-hook warning. |
| Instagram | 2,200 | A preview shows an approximate opening caption. |
| TikTok captions | 4,000 | A phone-style preview shows an approximate short caption opening. |

Features include remaining-character counts, word counts, warning states, four selectable feed previews, expandable preview text, an example caption, and a clear button. **Clean Spaces & Copy** removes repeated horizontal whitespace, trims line edges, preserves internal line breaks, and copies the cleaned caption. If clipboard access fails, the page provides a manual-copy fallback.

Counts use Unicode code points and include spaces and line breaks. They are not a full reproduction of each platform's publishing rules: X uses weighted counts for some characters and links. Feed previews are estimates, and actual truncation depends on device, app, line wrapping, and platform changes. LinkedIn's 140-character marker is an opening-line guide rather than a guaranteed cut-off. The tool does not publish posts or connect to social accounts.

### Excel Formula Sandbox & Analyzer

Paste an Excel formula to format it into a readable, indented structure. Matching parentheses receive matching colors, and supported function names receive syntax highlighting.

The tool provides:

- Live formatting, a sample formula, a clear button, and formatted copying.
- Function-call counts, nesting depth, and formatted-line counts.
- Basic structural diagnostics for unclosed or unexpected delimiters and quoted sections.
- Handling for quoted text, quoted sheet names, bracketed references, and comma or semicolon separators.
- A 50,000-character processing limit.

This is a structure formatter. It does not calculate formula results, execute formulas, open workbooks, or fully validate Excel syntax. Balanced delimiters alone do not guarantee a valid formula.

### AI Text Footprint Cleanser

Paste a paragraph or draft to highlight phrases from an editorial replacement list. The **Humanize Text** button replaces those listed phrases with simpler alternatives, preserving capitalization where supported. Examples include “utilize” → “use” and “furthermore” → “also”.

The page includes word count, estimated reading time, a phrase-based clutter score, an example, clearing, copying, and undoing its replacement operation. Reading time uses 200 words per minute.

Despite the tool's name, it uses predefined JavaScript rules rather than an AI model or an AI API. The clutter score reflects the proportion of words covered by its phrase list. It cannot determine authorship, detect AI-generated text, guarantee detector results, or measure overall writing quality. Review replacements for meaning and tone.

### Free Stream Roulette

Select a genre and spin to receive a streaming-platform suggestion from a curated list. Filters include Hollywood, classics, documentaries, retro TV, anime, and an all-genres option. The selection logic avoids an immediate repeat when another matching destination is available.

The configured destinations include Tubi, Pluto TV, The Roku Channel, Plex, Internet Archive, Documentary+, RetroCrush, Shout! TV, and Xumo Play.

The tool recommends a destination rather than a specific film or episode, and does not stream or host video. Its platform list is maintained in the page source, rather than fetched from a live catalog. Availability, advertising, account requirements, catalogs, and rights vary by provider and region. Opening a destination takes the visitor to that provider's website.

## Technology and architecture

| Component | Implementation |
| --- | --- |
| Page structure | HTML5 |
| Styling | Tailwind CSS through its official Play CDN, plus small inline CSS rules |
| Behavior | Vanilla client-side JavaScript in each page |
| Icons and illustrations | Inline SVG, text symbols, and CSS |
| Routing | Ordinary links between static HTML pages |
| Data processing | Local functions in the browser |
| Application backend / database | None |
| Build / package installation | Not required for the current site |
| Public domain | `everydaydigitalbox.com` |

The current pages use this Tailwind Play CDN script:

```html
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
```

Each tool keeps its markup, styling rules, and JavaScript together in its own `index.html`. There is no shared JavaScript module or frontend framework. This keeps individual tools portable; common design changes currently need to be applied across multiple pages.

Tailwind describes Play CDN as a development option. The current site uses it for the requested standalone setup; a compiled CSS build would be a possible future production improvement. See the [official Tailwind Play CDN documentation](https://tailwindcss.com/docs/installation/play-cdn).

## Repository structure

```text
micro-tools-hub/
├── index.html                  # Searchable hub and tool cards
├── README.md                   # Project documentation
├── AGENTS.md                   # Instructions for future sessions
├── PROJECT_MASTER_PLAN.md      # Vision, scope, constraints and milestones
├── TOOL_REGISTRY.json          # Canonical inventory and verification status
├── PROGRESS_TRACKER.md         # Registry-derived counts and current work
├── ROADMAP.md                  # Next twenty tools and complete category catalog
├── ARCHITECTURE.md             # Runtime design, limits and deployment
├── DECISIONS.md                # Dated decision log
├── CHANGELOG.md                # Meaningful implementation/documentation changes
├── SESSION_HANDOFF.md          # Continuation instructions and Git context
├── scripts/                    # Python tracking engine and Node compatibility
├── tests/                      # Isolated Python management tests
├── reports/                    # Generated local snapshots, ignored by Git
├── audit/                      # Current-state and baseline verification evidence
├── CNAME                       # Custom domain: everydaydigitalbox.com
├── social-counter/
│   └── index.html              # Social counters and live previews
├── excel-sandbox/
│   └── index.html              # Formula formatter and analyzer
├── text-cleaner/
│   └── index.html              # Phrase-based writing cleaner
└── streaming-roulette/
    └── index.html              # Curated streaming destination picker
```

## Run the project locally

### Open an existing copy

Open the root `index.html` in a modern browser. Use the dashboard cards to navigate to a tool. Keep the directory structure intact so relative links continue to work.

No package installation or build command is required. An internet connection is needed to load the Tailwind CDN styling. Opening external streaming destinations also requires internet access. Without a network connection, the site may appear unstyled unless the required styling is already cached.

### Clone a Git-connected working copy

If you want to make commits and push changes, install Git and clone the repository:

```powershell
git clone https://github.com/Juster06/micro-tools-hub.git
cd micro-tools-hub
```

A folder downloaded as a ZIP can be edited, but normally has no `.git` history or configured remote. Use a clone for the Git commands in this README; do not assume a downloaded folder is already connected to GitHub.

### Use a local web server

A local server is useful for checking site navigation and browser clipboard behavior. If Python is installed, run this from the project root:

```powershell
py -m http.server 8000 --bind 127.0.0.1
```

On systems that expose Python as `python`, use:

```sh
python -m http.server 8000 --bind 127.0.0.1
```

Then open [http://localhost:8000](http://localhost:8000). Stop the server with **Ctrl+C**. This server only serves the static files for local development; it is not an application backend.

Clipboard behavior depends on browser permissions and context. HTTPS or localhost is preferable for testing. Where supported, the tools provide fallback copying or instructions for manual copying.

## Privacy and external requests

The current application code processes captions, text, and formulas in the browser. It does not upload those inputs to an application server, use an AI service, or save drafts in a database or browser storage. Reloading or leaving a page can lose the current input; browser form-restoration behavior may vary.

“Client-side processing” does not mean the website makes no network requests:

- The browser requests the page from its hosting provider.
- Tailwind's styling script loads from the external CDN.
- Following a streaming-provider link loads a separate third-party website.

The current source contains no application analytics or caption/formula logging. Hosting and CDN providers can still receive ordinary request information such as IP addresses and browser headers. Clipboard actions place the copied content on the user's system clipboard.

The dashed **ADSENSE BANNER PLACEMENT** containers are visual placeholders. They do not load Google AdSense code or serve ads in the current implementation. Adding real ad scripts or analytics would change the site's network and privacy behavior and should be reflected in this documentation.

## Hosting and the custom domain

The public website is available at [https://everydaydigitalbox.com/](https://everydaydigitalbox.com/). The repository includes a root `CNAME` file containing `everydaydigitalbox.com`, and the live site is served through GitHub's infrastructure.

The root homepage also includes a Google site-verification meta tag. Preserve that tag during homepage updates unless the project owner deliberately changes the verification setup.

The project consists of static files and can be served by a static hosting provider. GitHub Pages publication settings and domain DNS records are configured outside these HTML files. Before changing deployment settings, check the repository's **Settings → Pages** configuration and the domain's DNS settings.

For the existing GitHub-hosted setup:

1. Keep the homepage at the repository root.
2. Keep each tool in its named folder with its own `index.html`.
3. Preserve `CNAME` when updating or transferring the project.
4. Commit and push changes to the branch used by the configured publishing source.
5. Check the repository's deployment status, then verify the public URLs.

A local save does not publish changes. A GitHub commit updates the source, while deployment and caching determine when visitors see it. The configured publication source must include the changed commit.

## Editing, committing, and pushing changes

Run the following only in a Git clone with the correct repository remote. Start by reviewing local changes before pulling:

```sh
git status
git remote -v
```

With a clean working tree, create a branch for a change:

```sh
git switch main
git pull --ff-only origin main
git switch -c feature/describe-your-change
```

Edit the relevant HTML or documentation files, preview the result, then stage the specific paths you changed. For a README-only update:

```sh
git diff -- README.md
git diff --check
git add README.md
git commit -m "docs: update project README"
git push -u origin feature/describe-your-change
```

Open a pull request targeting `main` so the changes can be reviewed before merging. GitHub write access is required to push to this repository; configure credentials through Git or your GitHub client rather than placing tokens in source files.

## Adding another tool

1. Create a descriptive folder such as `new-tool/` and put the complete page in `new-tool/index.html`.
2. Match the existing slate/indigo theme, spacing, typography, and accessible focus states.
3. Add a top-left **← Back to Hub** link with `href="../index.html"`.
4. Implement the tool locally in the browser and clearly explain any processing limits.
5. Add a card inside `#toolGrid` in the root `index.html`, with a matching relative link, unique heading ID, and searchable `data-title`.
6. Update the homepage's initial tool-count text. The runtime filter counts the cards automatically.
7. Check navigation and searching, then add the tool's description and links to this README.
8. Update the canonical registry entry, test/publication evidence, changelog, and session handoff. Run the synchronization and validation commands below. A registry entry alone does not create or publish a utility.

Use `textContent` when displaying user input rather than interpreting it as HTML. If a tool introduces a remote service, persistent storage, advertising, or account access, document that behavior instead of retaining an inaccurate local-only claim.

## Verification and maintenance

The website has no package manifest or build step. Python 3.10+ and its standard library run the complete developer-only tracking workflow. Run from the repository root:

```sh
python scripts/project_status.py
python -m unittest discover -s tests -v
node --test scripts/project.test.mjs
git diff --check
```

The command checks the registry, project links/source/evidence, and static HTML; updates only marked progress, roadmap and handoff content; and writes latest local JSON reports under ignored `reports/`. It preserves manual notes and does not promote tool statuses. The existing Node commands remain compatibility entry points to the same Python engine; Node 20+ is needed only for their tests.

Use `python scripts/project_status.py --check-only` for a snapshot without documentation updates, or add `--no-report` for no report writes. A downloaded non-Git copy reports Git state as UNKNOWN. These commands do not rerun browser interactions, verify live publication, push/deploy, or perform a security audit. See [management command documentation](scripts/README.md) for individual commands, reports, exit codes, and limitations.

For utility changes, check the affected behavior in a browser and inspect the developer console for errors. Save the actual test scope and results; mark a utility RELEASED only after checking both its implementation and its published version.

Suggested checks:

- Verify all homepage cards, search results, and Back to Hub links.
- Check narrow mobile and desktop layouts for horizontal overflow.
- Check keyboard focus, form labels, buttons, and status messages.
- Test empty input, pasted text, emoji, line breaks, and longer input.
- Check counts at and beyond each configured social limit, including LinkedIn's 140/141-character opening guide.
- Check preview expansion and clipboard success or blocked-permission behavior.
- Check formula examples, unbalanced delimiters, and the input limit.
- Check text replacements, their meaning, capitalization, undo, and copying.
- Check streaming filters and external destinations; update the curated list when providers change.
- Use browser network tools to verify that user input is not transmitted.
- Run `git diff --check` before committing.

Keep social-platform limits and preview assumptions under review because platform behavior can change. The current social-counter implementation was checked in desktop Chromium/Edge and across viewport widths from 320 to 1,600 pixels during its initial integration; this is not a guarantee of testing every browser or future change.

## License

No `LICENSE` file is currently included in the repository. A project license has not been declared in this README.

---

Maintained by [Juster06](https://github.com/Juster06). Visit [Everyday Digital Box](https://everydaydigitalbox.com/) to use the tools, or [open a GitHub issue](https://github.com/Juster06/micro-tools-hub/issues) to report a bug or suggest a utility.
