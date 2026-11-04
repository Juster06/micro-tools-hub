# Loan Repayment Calculator

Canonical route: `loan-repayment-calculator/index.html`.

Enter a positive principal up to 1,000,000,000,000 with at most two decimal places, a 0–100% annual rate with up to four decimals, and 1–50 whole years. Choose 1, 2, 4 or 12 payments per year. Fixed scheduled payments use the exact unrounded amortization formula, rounded half-up to cents; each period’s interest is rounded half-up to cents. The final payment adjusts for accumulated rounding, and the loan may end early. If the scheduled payment rounds to zero, the input is rejected. Estimates exclude fees, taxes and variable rates; not financial advice. BigInt support is required.

Processing stays in the browser; hosting and the existing Tailwind styling CDN are separate network requests. Publication is pending separately authorized integration and live verification.
