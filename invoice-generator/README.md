# Invoice Generator

All fields stay in browser memory. Invoice number is at most 80 UTF-16 units; seller/customer details at most 500 each; each of 1–20 descriptions at most 200. Quantities are positive plain decimals up to 1,000,000 with at most 3 fractional digits. Unit prices are nonnegative amounts up to 1,000,000 with at most 2 decimals. Tax is user-entered 0–100% with up to 2 decimals. Each line quantity × unit price is rounded half-up to cents, subtotal sums rounded lines, then tax is rounded half-up once on subtotal; total is subtotal plus tax. BigInt required. No accounting, legal or tax compliance is claimed. Print preview uses the browser print dialog.

Input stays local; hosting and the existing styling CDN are separate requests. Publication is pending.
