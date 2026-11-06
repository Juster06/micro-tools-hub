# HTML Previewer

Canonical route: `html-previewer/index.html`.

Preview a safe structural HTML subset in an isolated frame, with no scripts or external resources.

## Scope and limits

Structural tags only. All attributes, styling, images, active and foreign elements are omitted; anchors become plain text. No script execution, parent/storage access, navigation, popups, forms or external resources. Preview has an empty sandbox and restrictive CSP. This is a tested limited preview, not a complete HTML/CSS renderer or universal browser-isolation certification.

32 KiB UTF-8 input; 256 KiB output; 4,096 parsed nodes and 64 nesting levels. CSS/JavaScript also cap tokens at 8,192. Each job has a 2-second Worker deadline and can be cancelled. Input changes/reset terminate the job and discard its result. Timers do not guarantee a hard memory limit.

## Verification

Development in progress; no TESTED or public-release claim yet. Required tests and source-bound evidence must pass before status changes.
