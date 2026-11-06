# HTML Formatter

Canonical route: `html-formatter/index.html`.

Indent HTML while checking that the parsed content and significant whitespace stay intact.

## Scope and limits

Prettier 3.9.10 HTML with strict whitespace and embedded-language formatting disabled. HTML5 parser normalization is compared before/after; any parsed-content change fails closed. Strict mode may put line breaks inside tag brackets. Some valid documents are refused rather than silently altered. Output is escaped text, never rendered or sanitized; downloaded HTML retains its code and resources.

32 KiB UTF-8 input; 256 KiB output; 4,096 parsed nodes and 64 nesting levels. CSS/JavaScript also cap tokens at 8,192. Each job has a 2-second Worker deadline and can be cancelled. Input changes/reset terminate the job and discard its result. Timers do not guarantee a hard memory limit.

## Verification

Development in progress; no TESTED or public-release claim yet. Required tests and source-bound evidence must pass before status changes.
