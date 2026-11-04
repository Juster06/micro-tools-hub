# Compound Interest Calculator

Canonical route: `compound-interest-calculator/index.html`.

Amounts are nonnegative plain decimals with up to 2 fractional digits, each at most 1,000,000,000,000 currency units. Annual rate is 0–100% with up to 4 fractional digits. Choose 1, 2, 4 or 12 compounding periods per year and 0–50 whole years. Interest is rounded half-up to cents each period, then the contribution is added at the end of that period. Total contributions include the initial principal. Results above 1,000,000,000,000,000 units are rejected. Browser BigInt is required. Fees, taxes, inflation and variable rates are excluded; results are estimates, not guaranteed returns.

Processing stays in the browser; hosting and the existing Tailwind styling CDN are separate network requests. Publication is pending separately authorized integration and live verification.
