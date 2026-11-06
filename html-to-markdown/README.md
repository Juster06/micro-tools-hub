# HTML to Markdown

Canonical route: `html-to-markdown/index.html`.

Convert common HTML structures to Markdown text without executing or rendering markup.

## Scope and limits

Bounded parse5 8.1.0 conversion supports headings, paragraphs, lists, links, emphasis and code blocks. Whitespace outside code normalizes. Scripts/styles/foreign content are omitted; unsupported structures flatten or omit with a notice. Only explicit HTTP(S), mailto, fragment and local relative link forms retain destinations. Tables, forms, styling and exact browser layout are unsupported. Output is plain text, not a rendered Markdown preview.

32 KiB UTF-8 input; 256 KiB output; 4,096 parsed nodes and 64 nesting levels. CSS/JavaScript also cap tokens at 8,192. Each job has a 2-second Worker deadline and can be cancelled. Input changes/reset terminate the job and discard its result. Timers do not guarantee a hard memory limit.

## Verification

Development in progress; no TESTED or public-release claim yet. Required tests and source-bound evidence must pass before status changes.
