# CSS Minifier

Canonical route: `css-minifier/index.html`.

Compact CSS with a reviewed parser and generator, without rule merging.

## Scope and limits

CSS-Tree 3.2.1 parses and prints CSS. No rule merging or value optimization. Strings, custom-property raw values and license comments are preserved; license comments may move after a leading UTF-8 @charset. Only UTF-8 @charset exports are supported. Unsupported constructs may remain raw or fail; browser-specific syntax needs review. CSS is never applied or fetched.

32 KiB UTF-8 input; 256 KiB output; 4,096 parsed nodes and 64 nesting levels. CSS/JavaScript also cap tokens at 8,192. Each job has a 2-second Worker deadline and can be cancelled. Input changes/reset terminate the job and discard its result. Timers do not guarantee a hard memory limit.

## Verification

Development in progress; no TESTED or public-release claim yet. Required tests and source-bound evidence must pass before status changes.
