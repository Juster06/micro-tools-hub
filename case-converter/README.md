# Case Converter

Standalone browser utility at `case-converter/index.html`, generated with the Task 4 text template and adapted without changing the shared templates. Open the page directly or use a local static preview. No build, account, server processing or data storage is required; styling uses the existing Tailwind Play CDN. See `TOOL_REGISTRY.json` for lifecycle. Merged through PR #9 and verified live at https://everydaydigitalbox.com/case-converter/ on 2026-11-01 before RELEASED status. Deployed normalized source matches the approved implementation; `audit/CASE_CONVERTER_RELEASE_VERIFICATION.json` records actual publication checks while the original local audit is preserved.

Type/paste text, choose one of seven styles and compare the live result with the unchanged original. Updates debounce for 120 ms; editing clears old output immediately. Convert text reruns the selected style. Clear all restores uppercase, empty text/result, zero counters and input focus. During IME composition the result stays invalid until composition completes.

| Mode | Deterministic rule |
| --- | --- |
| UPPERCASE | Native Unicode `toUpperCase()` |
| lowercase | Native Unicode `toLowerCase()` |
| Title Case | Lowercase first. Capitalize significant words, first/last word of each line and the word after a colon. Minor words: a, an, the, and, as, at, but, by, for, from, in, nor, of, on, or, per, to, via, vs. |
| Sentence case | Lowercase first, then capitalize the first letter and after `.`, `?`, `!`, CR or LF. Protect adjacent-letter dots, decimal digit-dot-digit sequences, initials and a fixed abbreviation list. |
| Capitalize Words | Lowercase first, then capitalize the first Unicode letter in each word. |
| Alternating Case | Begin lowercase; alternate across cased Unicode input letters. Spaces, numbers, punctuation, marks, emoji and letters without case do not advance the pattern. |
| Inverse Case | Native lower/upper mappings flip cased letters; uncased and non-letter characters remain unchanged. Titlecase letters map to lowercase. |

Title/word capitalization uses Unicode letter/number/combining-mark runs; internal straight or curly apostrophes remain within a word, hyphens separate words. Thus `don't` becomes `Don't`, `o’NEILL` becomes `O’neill`, and `mother-in-law` becomes `Mother-in-Law` in Title Case or `Mother-In-Law` in Capitalize Words. These are consistent rules, not every language's editorial or surname conventions. Numbers may precede the capitalized first letter (`3d` → `3D`).

Sentence abbreviations: mr., mrs., ms., dr., prof., sr., jr., st., vs., etc., e.g., i.e., a.m., p.m. Ambiguous sentence endings after these abbreviations/initials can remain lowercase; joined dots such as `example.com` are not sentence boundaries. This is a casing tool, not a grammar/proper-name detector: names/acronyms are lowercased too, and language-specific rules may need manual correction.

No accent stripping or Unicode normalization is applied. Native casing can expand a character (`ß` → `SS`, `İ` → `i` plus combining dot) and depends on the browser's Unicode support. Alternation advances once per cased input letter, even when its mapped output expands. It is not locale-specific Turkish/Lithuanian casing or universal titlecasing. Whitespace/punctuation are preserved by the logic, including CRLF/CR/LF; native browser textareas normalize entered line endings to LF, which is what copy/download use.

## Statistics and limits

- Characters: Unicode code points, including spaces/line endings, not grapheme clusters. Combining accents and joined emoji may count as multiple characters.
- Words: groups of non-whitespace characters according to JavaScript whitespace; emoji/non-Latin runs can count as tokens. No universal linguistic segmentation is claimed.
- Lines: empty text is zero; otherwise one plus each CRLF, standalone CR or LF, including trailing blank lines.
- Limit: **100,000 UTF-16 code units**, checked before conversion. The visible character counter uses a different, documented measure (50,000 single-code-point emoji may use 100,000 units). Oversized input remains intact; output/actions clear and an actionable error appears. No silent truncation. Whitespace-only input updates counts but requests actual text rather than producing a misleading result.

The Node long-input cases exercise every mode at/near the limit with exact expected output and a one-second VM call timeout. On the verified host each long logic call completed within that timeout; this does not certify every device. Browser tests additionally execute a full-limit multiword title conversion and emoji/oversize boundaries.

## Copy, download, privacy and access

Copy uses `navigator.clipboard.writeText`; only its resolved promise announces success. Denial/unavailability selects the readonly result and explains Ctrl+C/⌘C without claiming a copy. A revision guard prevents a late copy completion from announcing stale success after input changes. Download uses a UTF-8 text Blob, the fixed filename `case-converter-output.txt` and a temporary object URL revoked after one second; feedback describes the download request, not a guaranteed OS save.

User text is never uploaded, logged, persisted or used as HTML/code. Status/error rendering uses text; input/output use textarea values. Network requests for page/style delivery are separate from local text processing. Native labels/select/buttons, visible focus, skip link, live status, error alert, keyboard Tab/Enter and responsive two-pane/stacked layouts are provided. Current Edge/Chrome/Firefox/Safari versions supporting Unicode property escapes and modern JavaScript are intended; only the recorded Edge engine has been executed here. This is not screen-reader or all-browser certification.

## Tests

```powershell
python scripts/test_tool.py --id case-converter --workspace canonical
node --test tests/tools/case-converter/logic.test.mjs tests/tools/case-converter/extended-browser.test.mjs tests/tools/case-converter/integration-browser.test.mjs
```

The JSON logic cases assert all seven actual modes; the Node suite adds exact boundary results and counter rules. The real Chromium DSL suite tests modes, stats, switching, copy success/denial, UTF-8 download, clear, empty input, safe text, stale results, keyboard and 320/375/768/1440px overflow. Extended tests reuse the Task 4 CDP client for large/oversized text, immediate invalidation, delayed copy, filename/UTF-8/object-URL revocation, keyboard, composition events and absence of transport/storage calls.

Headless tests isolate the browser profile, block external HTTP(S), and simulate clipboard/download APIs; no host clipboard or Downloads file is changed. Composition events are simulated, not an OS IME certification. Local integration tests additionally follow Back to Hub, verify registry-derived routes/count and the lifecycle-appropriate availability label, search/reset, and return to the tool. Manual screenshot review supplements DOM tests. Audit evidence records actual results, scope, source revision/hash and publication status separately; generated test reports remain ignored.

Live verification used the actual public HTTPS pages with external delivery enabled: all seven modes, preserved original, statistics, Clear, hub navigation, keyboard, mobile and no uncaught JavaScript errors. Clipboard success/denial were simulated; the production download Blob, UTF-8 bytes, filename and revocation were inspected in memory. No host clipboard, OS save dialog or screen reader was certified. Desktop/mobile public screenshots were reviewed.
