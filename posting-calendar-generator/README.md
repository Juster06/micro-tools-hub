# Posting Calendar Generator

Canonical route: `posting-calendar-generator/index.html`.

Start/end are valid Gregorian dates; inclusive span at most 366 days. Select one or more weekdays and weekly or every-two-week cadence, anchored to the start-date seven-day blocks. One entry per chosen day. Enter a 24-hour wall time and an IANA timezone supported by the browser. The output records date, wall time and zone label only: it does not resolve daylight-saving gaps, ambiguity or convert to UTC. Confirm local times separately. CSV is escaped; no platform connection or publishing.

Processing stays in the browser; hosting and the existing Tailwind styling CDN are separate network requests. Publication is pending separately authorized integration and live verification.
