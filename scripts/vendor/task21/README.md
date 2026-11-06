# Task21 reviewed Worker sources

These are build-time source modules. Website delivery uses the four checked-in
`assets/vendor/task21/*-source.js` assets; no package manager/backend/build runs
on Pages. Each asset defines a string used to create a dedicated local Blob Worker.
The parent page does not run the parser/minifier bundle. Input is sent as data.

Exact direct dependencies are in package.json and the frozen pnpm lock. Review
all tarball integrity, licences/notices, advisories and browser behavior before
updating. Runtime and tooling dependencies are distinguished in the security audit.
Do not put node_modules, package stores, personal paths or generated reports here.

To rebuild, copy package.json/lock to an isolated directory outside the project,
install with frozen lock and lifecycle scripts disabled, then run:

```text
node scripts/vendor/task21/build.mjs ABSOLUTE_ISOLATED_NODE_MODULES
node scripts/vendor/task21/build.mjs ABSOLUTE_ISOLATED_NODE_MODULES --check
```

The command never installs packages. Re-test actual assets and refresh their
source-bound hashes/evidence after a rebuild. The audit records the exact versions,
selected dependency graph, byte counts, source hashes, scoped security gates and
limits. Keep all notices and bundled legal comments. No PDF code is included.

HTML formatting uses strict whitespace and compares normalized parsed documents;
it refuses output that changes parsed content. Preview is a structural tag allowlist
with no attributes/resources/styles/scripts, plus an empty iframe sandbox and CSP.
Markdown is a documented text subset, not a rendered HTML preview. CSS is parser
printing without rule/value optimization. JS disables compression and mangling.
All operations use bounded text, explicit complexity guards, cancellation and a
2-second deadline; none claims a guaranteed browser heap bound.
