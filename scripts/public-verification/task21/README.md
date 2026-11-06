# Task21 public verification reproduction

Manual, owner-authorized live HTTPS verification; deliberately excluded from
offline CI. Never run these against an unapproved deployment or automatically.
Production responses are not replaced and network requests are not blocked.
Use the dated approved source/hash audit first; these drivers do not certify
future source automatically. Requires Node24, the existing installed Chromium
CDP harness and bundled test Acorn; no new package or website dependency.

```text
node --test --test-concurrency=1 scripts/public-verification/task21/functional.mjs
node --test --test-concurrency=1 scripts/public-verification/task21/isolation.mjs
node scripts/public-verification/task21/consent.mjs
```

Set EDB_TEST_BROWSER to an installed Chromium executable when needed. Output is
ignored under reports/public-task21. Clipboard/downloads are captured in memory;
native OS dialogs are not exercised. Only fixed synthetic fixtures are used.
The consent driver sends exactly three real synthetic GA page views in two
isolated profiles and does not access authenticated property reporting.

Isolation monitoring uses passive child-session CDP instrumentation. Positive
controls fetch an approved same-origin asset from the parent and an intentionally
permitted test-only child image. Malicious tests use the real production Worker
and its restrictive srcdoc. Direct child-origin probes run trusted test code via
DevTools; supplied HTML scripts remain disabled. Browser-internal UI targets are
distinguished from input-created web/blank popups; inventories are compared.

These scoped checks are not a browser isolation certification or hard heap bound.
Keep the unchanged offline functional suites and required hosted CI separate.
