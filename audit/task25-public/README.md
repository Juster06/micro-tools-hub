# Reproduce the Task 25.1 public audit

Copy these five scripts and `../task24-public/browser-transport.mjs` into a
scratch directory. Set `EDB_REPO_ROOT` to a full-history checkout containing
the approved deployment commit. Run `python source.py`, then
`node --test functional.test.mjs`, then `node public-consent.mjs`. Use Node 24
and an installed Chromium browser.

The audit checks the deployed baseline. A later authorized metadata deployment
can cause the historical source and card checks to fail. The Worker probe uses
Chromium DevTools to observe the real script and native Blob calls. The consent
test sends three synthetic page views to the real collection endpoint.
