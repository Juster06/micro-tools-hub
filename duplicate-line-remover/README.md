# Duplicate Line Remover

Standalone browser utility at `duplicate-line-remover/index.html`, generated from the Task 4 text template, then implemented and promoted deliberately. No build, backend, accounts, extra packages or input storage. Existing Tailwind Play CDN styling has complete inline fallback styles. The registry and dated audit define lifecycle; local tests do not establish publication. Task 6 delivery is local TESTED/publication pending, never RELEASED.

Type or paste lines, then inspect the automatically updated result. Four native checkboxes change matching/output without editing the original. A 120 ms debounce invalidates old output, action buttons and result counts immediately. Remove duplicates runs immediately. Clear restores empty input/output, zero counters, all options off and input focus. Composition keeps results invalid until completion; asynchronous clipboard announcements cannot overwrite a newer state.

## Defaults and exact rules

| Setting | Default | When enabled |
| --- | --- | --- |
| Case-insensitive matching | Off; case-sensitive | Lowercase comparison keys using native JavaScript `toLowerCase()`; retain first spelling |
| Ignore surrounding whitespace | Off; exact whitespace | `trim()` comparison keys only; retain first line's complete original whitespace |
| Remove blank lines | Off | Remove empty/whitespace-only records before deduplication; count separately |
| Sort results alphabetically | Off; original order | Sort retained comparison keys lexicographically by UTF-16 code units; keep original retained text |

For each line, optionally trim its comparison key, optionally lowercase it, then use a Set for duplicate lookup. First occurrence wins exactly. Blank removal takes priority over duplicate detection: a removed blank is counted once as blank, never also as a duplicate. With blank removal off, distinct blanks remain according to the current comparison settings; later equal blanks are duplicates. Internal whitespace is never collapsed. There is no output-trimming option or hidden text modification.

Sorting occurs only after deduplication, uses the same selected keys and preserves occurrence order for equal keys. Equal keys are normally already deduplicated. This deterministic alphabetical-style order is not locale-aware collation or natural numeric order: uppercase/leading spaces affect ordering with matching options off, and 10 sorts before 2. Accents, non-Latin scripts, emoji, combining marks and zero-width characters are retained. No accent stripping or Unicode normalization occurs. Native lowercase is not full Unicode case folding or locale-specific casing; Straße and STRASSE stay distinct, İ maps to i plus combining dot, and Greek lowercase can depend on context.

## Line endings, statistics and limits

- LF, CRLF and CR separate records. CRLF is one separator. Unicode U+2028/U+2029 are not line separators for this tool.
- Empty input has zero records. Any nonempty input has one plus its separators, including a trailing empty record. Textareas normalize entered CRLF/CR to LF; pure logic accepts all three. Output always joins retained records with LF.
- Blank means `line.trim().length === 0`, including tabs, non-breaking spaces and the JavaScript whitespace set. Zero-width space U+200B is not blank.
- Result object: `text`, `originalLines`, `retainedLines`, `removedDuplicates`, `removedBlankLines`, `totalRemoved`. Retained plus total removed equals original; total removed equals duplicates plus blanks. Counts describe logical records, not a second parse of the joined output.
- A single retained empty record produces empty text with retained count one. This is distinct from zero retained records in the statistics. Copy/download are disabled if the result has no characters; useful feedback explains that state. Whitespace-only nonempty output can be copied/downloaded.
- Limit: **100,000 UTF-16 code units**, consistent with Case Converter. Emoji can use two units per code point. No maxlength truncation: oversized input remains intact, current output/actions clear and an actionable error appears. Oversized input line count is unavailable (—), avoiding an unbounded scan; no invented retained/removal statistics are shown for errors or pending results.
- Set-based matching scans the input once; optional sorting adds O(k log k) comparisons for k retained lines. Native string processing and comparator costs still depend on line lengths. Exact full-limit and repeated/unique-line cases run in Node and real Edge; measurements certify only the recorded host, not every device.

## Actions, accessibility and privacy

Copy captures only the current output and announces success only after the clipboard promise resolves. Denial/unavailability selects the output and explains Ctrl+C/⌘C, without claiming success. Revision guards suppress late success/failure announcements after input/options/Clear changes. Download uses UTF-8 Blob MIME `text/plain;charset=utf-8`, filename `duplicate-lines-cleaned.txt`, a temporary link and object URL revoked after one second, including failure after URL creation. Feedback reports the request, not a guaranteed OS save.

User text remains in textarea values and textContent; it is not HTML, code, an upload, a log or a saved draft. No fetch/XHR/beacon/WebSocket/storage/IndexedDB processing calls are needed. Page/style delivery may use the network independently. Native labels, fieldset/legend, checkboxes/buttons, skip link, visible focus, polite status, alert errors, reduced motion, responsive stacked panes and narrow layout are provided. Current modern browsers are intended; only the recorded Edge engine is executed. No screen-reader, physical mobile, OS clipboard/IME/save-dialog or all-browser certification is claimed.

## Tests and local status

```powershell
python scripts/test_tool.py --id duplicate-line-remover --workspace canonical
node --test tests/tools/duplicate-line-remover/logic.test.mjs tests/tools/duplicate-line-remover/extended-browser.test.mjs tests/tools/duplicate-line-remover/integration-browser.test.mjs
python scripts/project_status.py
```

Exact JSON logic fixtures cover all sixteen settings, output and all statistics, first-retained whitespace/case, line endings, Unicode and invalid inputs. Additional Node cases construct full-size and oversized fixtures without committing huge repeated literals. Real Chromium DSL and extended tests cover actions, rapid changes/stale output, composition, limits, safe rendering, labels/keyboard, mobile, no processing transports/storage, UTF-8 bytes/filename/revocation and delayed clipboard races. Host APIs are simulated/captured in isolated profiles with external HTTP(S) blocked; no host clipboard or Downloads file is changed. Integration follows the actual hub/back/search/return links and asserts TESTED/publication pending. Manual screenshot review supplements DOM checks; the dated audit records actual results and limitations. Generated reports and development bundles stay ignored.

Task 6 does not push, open a PR, merge, deploy, refresh release evidence for other tools or begin another utility. A separately authorized PR/review/publication/source-verification workflow is required before RELEASED.
