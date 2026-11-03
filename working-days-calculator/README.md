# Working Days Calculator

Canonical route: `working-days-calculator/index.html`.

Gregorian YYYY-MM-DD dates, years 0001–9999; end must not precede start and the span is limited to 36,600 days. Start is always included; choose whether the end is included. Sunday and Saturday are non-working by default, and every weekday can be changed. Enter at most 1,000 holiday dates, one per line, within 11,000 UTF-16 units. Duplicate holiday dates count once; holidays already on non-working days or outside the considered range do not remove an extra day. No official holiday calendar is applied.

Processing stays in the browser; hosting and the existing Tailwind styling CDN are separate network requests. Publication is pending separately authorized integration and live verification.
