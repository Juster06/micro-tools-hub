# Developing a utility

Read `AGENTS.md`, the latest manual handoff and [the utility contract](TOOL_CONTRACT.md) first. Work in the active Git checkout on a feature branch. Do not move that checkout: the Windows dashboard shortcuts refer to it. Explicit user scope takes precedence over the recommended queue.

## Select and inspect

```powershell
git status --short --branch
python scripts/project_status.py --check-only
python scripts/plan_tool_batch.py --count 10 --output reports/batch-plans/tool-batch-plan.json
```

Read the selected entry in `TOOL_REGISTRY.json`: ID, directory, required features, related tools, dependencies, complexity, notes and verification fields. Compare actual existing capabilities before adding anything. Planning follows sequence rank, then priority and ID; prerequisite tool references must already be TESTED/RELEASED. Descriptive dependency strings are review requirements, not installed packages. Plans distinguish eligible READY work, specialist work, unmet dependencies, existing work, BLOCKED and RELEASED. Estimated changes are filenames, not time estimates. A plan never generates or publishes tools.

## Generate safely

```powershell
python scripts/create_tool.py --id TOOL_ID --dry-run
python scripts/create_tool.py --id TOOL_ID
```

Replace `TOOL_ID` with the existing READY ID. Optional `--template text` or `--template structured` overrides the category-based default. Generator, planner, integration and tool-test commands accept `--root PATH` and otherwise find their checkout from the script, independent of the working directory. IDs/routes reject traversal, Windows device names, symlinks and junction components. Existing canonical directories/bundles are refused; failed generation removes only files/directories created by that invocation. Review concurrent writers separately; no filesystem transaction against a hostile process is promised.

The six-file bundle is under ignored `development/scaffolds/<id>/`:

```text
index.html                      development preview hub
<directory_path>/index.html     actual standalone scaffold
manifest.json                   identity/template, not lifecycle
IMPLEMENTATION.md               registry features/dependency checklist
tests/logic.cases.json           initially empty: NOT RUN
tests/browser.cases.json         initially empty: NOT RUN
```

Open its nested page locally. Its explicit `../index.html` link reaches the development preview hub; that hub links to the real hub. After promotion the same nested page link reaches the public hub. Generated placeholders remain outside canonical routes, ignored by Git, visibly unfinished and `noindex`; registry/homepage remain untouched. A generated scaffold is never functional PASS. Source fragments live in `templates/`; edit the actual scaffold for one tool, fragments only for intentional future generation changes. Generated pages contain the expanded fragments, not runtime imports.

## Implement and write cases

Define acceptance behavior before coding: modes, Unicode, invalid/empty data, boundaries, limits, error handling and actual dependency decisions. Replace the inline `edb-tool-logic` implementation and meaningful operation options. Retain the separation from UI code; set `isScaffold:false` only after actual behavior exists. For specialist tools, adapt both the interface and tests explicitly. Remove development-only text and the `noindex` meta when the real tool is ready for reviewed public integration. Do not change the registry merely to silence an unimplemented placeholder.

Logic cases use schema version 1 and unique IDs. Each case needs `input`, optional `options` and exactly one of `expected` (exact JSON value) or `error` (nonempty expected error substring). For example, a future uppercase implementation could have this **test specification**, not implementation:

```json
{"schema_version":1,"cases":[
  {"id":"uppercase-basic","input":"hello world","options":{"mode":"uppercase"},"expected":"HELLO WORLD"},
  {"id":"lowercase-basic","input":"HELLO WORLD","options":{"mode":"lowercase"},"expected":"hello world"}
]}
```

These tests alone are inadequate: add every required mode, Unicode/line endings, empty/invalid input, boundaries and representative large inputs. Generic logic runs synchronously in Node with a one-second call timeout. Async/browser-dependent behavior requires specialist coverage; see the contract. Execute only trusted repository JavaScript.

Browser cases also use `{"schema_version":1,"cases":[...]}`. Each case has `id`, optional `width` and nonempty `steps`; each case reloads the page and must include at least one assertion. Example for a future implemented tool:

```json
{"id":"clear-restores-input","steps":[
  {"action":"set","selector":"#toolInput","value":"Example"},
  {"action":"click","selector":"#clearBtn"},
  {"action":"expect","selector":"#toolInput","property":"value","equals":""},
  {"action":"expect","selector":"$page","property":"activeId","equals":"toolInput"}
]}
```

Supported actions: `set` dispatches input/change, `click`, `focus`, `key` (Tab/Enter/Escape), `viewport` (width 240–3000), `clipboard` (mode success/failure), `expect`. Expectations use CSS selectors and `value`, `textContent`, `disabled`, `hidden`, `checked`, `href`, `selectionStart`, `selectionEnd`, `exists`, `childElementCount`, `rel`, `target`, or `aria-*`/`data-*` attributes. Compare with `equals`, `includes`, `endsWith` or `oneOf`. Special selectors: `$page` with `activeId`, `url`, `overflow`; `$clipboard` with `text`; `$downloads` with `count` or `text` (last Blob). Polling allows asynchronous UI updates; assertion failure identifies the case and step without logging private input/output.

## Execute the four testing layers

```powershell
python scripts/test_tool.py --id TOOL_ID --workspace staging
python scripts/test_tool.py --id TOOL_ID --layers structural,logic
python scripts/verify_tool_templates.py
python -m unittest discover -s tests -v
node --test scripts/project.test.mjs scripts/tool-framework.test.mjs
python scripts/project_status.py
git diff --check
```

- **A: Structure.** HTML document/metadata/IDs, adapter/interface where applicable, canonical identity, script/internal resources and explicit hub navigation. This does not execute behavior.
- **B: Logic.** Actual inline transformation/calculation with explicit fixtures and failures. Empty suites, placeholders and missing adapters are NOT RUN.
- **C: Interaction.** Real installed Chromium engine via Node built-ins/CDP, isolated temporary browser profile, file URLs and blocked external HTTP(S). No npm packages or user profile. Clipboard and download APIs are simulated/captured to avoid changing host clipboard or Downloads; physical OS dialogs and real clipboard permissions still require manual verification. Test input changes, output, errors, safe rendering, clear, copy, download, keyboard and narrow layouts. This is DOM/headless verification, not visual/screen-reader certification or an online CDN check.
- **D: Integration.** Existing project checker verifies registry, routes, homepage, evidence, generated documents and links. Homepage proposal tests use temporary fixtures and real `git apply --check`. Released-page browser profiles add regression checks without editing public source or refreshing publication evidence.

Python 3.10+ standard library handles generation/planning/structure. Node **22.4+** is needed for logic/browser execution (built-in WebSocket); an installed Edge/Chrome/Chromium is needed for interaction. Set `EDB_TEST_BROWSER` or `--browser PATH` if auto-detection fails. Missing Node/browser is explicitly NOT RUN; failed startup is UNKNOWN, not PASS. Template verification creates neutral temporary fixtures only and reports under `reports/framework-template-tests.json`; it implements no registered utility.

Tool results go to ignored `reports/tool-tests/<id>.json`, separate from the four existing tracking report schemas. They bind source, cases, manifest, registry metadata and runner hashes. Changed inputs invalidate them; changes during a run yield STALE. `--no-report` suppresses writes; `--workspace canonical` selects deployed source, and `auto` prefers canonical when present. CLI exit 0 means the **requested** scopes passed, 2 means unavailable/scaffold scope, 1 means failure/unknown/stale. An exit-0 structural/browser subset may still have overall PARTIAL because isolated logic was not run. Only all three passing layers plus real implementation produce overall PASS. Dashboard test totals remain unavailable under its existing report contract; do not substitute these reports silently.

## Promote, verify and propose integration

Promotion is a deliberate developer step after implementation. Copy the nested real page to `<directory_path>/index.html`; copy cases and manifest to `tests/tools/<id>/`. Inspect the diff; never copy the staging preview hub over the real homepage. Keep development bundles ignored. Move lifecycle forward manually only with actual evidence and the existing registry schema; no framework command edits statuses or dates. An intermediate unpublished branch may have expected missing-homepage consistency errors until the complete integration is ready; resolve all before delivery rather than weakening the validator.

Record required manual verification in `audit/` using the current evidence schema demonstrated by `audit/BASELINE_VERIFICATION.json`: page path, matching normalized source SHA-256, actual tested source revision/date, result, test scope and limitations. Update the corresponding registry `verification`, testing status and date only when justified. Commit implementation before using its real revision as evidence. TESTED means behavior verified, publication still pending. Run canonical tests **after** metadata/evidence edits because they affect the input hash.

```powershell
python scripts/test_tool.py --id TOOL_ID --workspace canonical
python scripts/integrate_tool.py --id TOOL_ID
git apply --check reports/integration/TOOL_ID.patch
```

The integration command writes a proposed patch only for eligible new/framework-owned cards; it does not apply it. Review the diff, route, escaped copy, category, availability and initial search count. Preserve all existing card descriptions/links. Only after review, apply the specific patch with `git apply reports/integration/TOOL_ID.patch`, inspect the actual diff, run full project status and check hub search/back navigation. Existing manually maintained cards return NO_CHANGE and produce no patch. Ambiguous markup/duplicate routes/stale functional evidence fail closed. The public card uses TESTED “publication pending” or RELEASED “Live” labels; this does not itself confirm publication.

Before PR: rerun relevant unit/logic/browser/integration checks, inspect no credentials/personal paths/reports/local settings were staged, update manual handoff/changelog and generated tracking, commit on the feature branch, inspect a clean tree. Push/open PR only when authorized; review base/changes/CI before any separately authorized merge. After authorized deployment, actually verify live behavior and matching source, record publication evidence, then manually set RELEASED and regenerate tracking. Never infer live status from Git alone.

## Case Converter: next-task dry-run example

Case Converter is the next READY candidate at Task 4 delivery. Its existing required features and dependencies determine the eventual Task 5 scope. During Task 4 only this command was run:

```powershell
python scripts/create_tool.py --id case-converter --dry-run
```

It proposes the six ignored bundle files without writing them, adding a homepage card, implementing a case algorithm or changing READY. In separately authorized Task 5, inspect overlap/scope, generate, implement actual required modes, add expanded logic/browser cases, manually verify, promote and follow the quality gates above. Task 5 has **not** begun. A batch proposal is not permission to implement ten tools at once.
