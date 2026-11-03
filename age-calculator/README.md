# Age Calculator

Canonical route: `age-calculator/index.html`.

Enter Gregorian dates in YYYY-MM-DD, years 0001–9999. Birth date cannot follow the reference date. If the reference is empty, the device's local calendar date is used. The age is computed in calendar months anchored to the original birth date; each month anniversary clamps to the final day of the month. A February 29 anniversary is February 28 in a non-leap year. Arithmetic uses UTC day numbers and has no daylight-saving offset. No input is saved or uploaded.

Processing stays in the browser; hosting and the existing Tailwind styling CDN are separate network requests. Publication is pending separately authorized integration and live verification.
