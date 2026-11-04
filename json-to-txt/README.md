# JSON to TXT

Canonical route: `json-to-txt/index.html`.

Input up to 100,000 UTF-16 units; JSON nesting at most 100. Path is $ for root or dot-separated ASCII identifier keys, optionally followed by one array index [0] or wildcard [*] per segment, for example users[*].name. Dangerous prototype-related keys are rejected. Missing fields are counted; output is bounded to 10,000 values and 500,000 units. JavaScript JSON numeric precision applies; use strings for exact large integers.

Processing stays in the browser; hosting and the existing Tailwind styling CDN are separate network requests. Publication is pending separately authorized integration and live verification.
