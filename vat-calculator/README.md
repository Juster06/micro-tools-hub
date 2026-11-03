# VAT Calculator

Canonical route: `vat-calculator/index.html`.

Enter nonnegative plain decimals, at most 64 UTF-16 units and six fractional digits. Amount is at most 1,000,000,000,000; rate is 0–1,000%. Enter the rate yourself: no current national VAT rate is assumed. Add mode treats the amount as net; remove mode treats it as gross. Exact integer rational arithmetic computes rounded net and gross to two decimals with half-up rounding; displayed VAT is rounded gross minus rounded net so the breakdown reconciles. Currency-neutral display does not determine tax law, invoicing or tax advice.

Processing stays in the browser; hosting and the existing Tailwind styling CDN are separate network requests. Publication is pending separately authorized integration and live verification.
