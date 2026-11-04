# Text Difference Checker

Canonical route: `text-difference-checker/index.html`.

Line-level comparison normalizes CRLF/CR to LF. Each input is limited to 20,000 UTF-16 units and 400 lines; the product of line counts must be at most 80,000. Empty text has zero lines. Deterministic longest-common-subsequence comparison prefers removal for ties. Prefixes are [unchanged], [removed] and [added]; content is not executed. No character-level diff is claimed.

Processing stays in the browser; hosting and the existing Tailwind styling CDN are separate network requests. Publication is pending separately authorized integration and live verification.
