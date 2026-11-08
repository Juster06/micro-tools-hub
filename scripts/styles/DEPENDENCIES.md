# Static CSS compiler dependencies

These packages run only during development and CI. The website loads the
generated first-party stylesheet, not these JavaScript packages or their native
bindings. No new frontend JavaScript, remote font, service worker or tracker is
introduced.

`tailwindcss` and `@tailwindcss/cli` are both pinned to **4.3.5**, the version
reported by the live browser compiler's `X-JSD-Version` header during Task 2C.
Both use the MIT license. The lockfile pins transitive versions and npm registry
integrity hashes. Its dependency metadata includes MIT, MPL-2.0, ISC, 0BSD,
Apache-2.0 and BSD-3-Clause licensed development packages. Platform-specific
optional packages provide prebuilt native bindings; no package lifecycle scripts
are required by the supported one-shot build. Install with `--ignore-scripts`.

The generated stylesheet retains Tailwind's version/MIT license banner.
`licenses/tailwindcss-MIT.txt` preserves the complete upstream license notice.
Dependency license files are also distributed in their installed npm packages;
`node_modules` must not be committed or served as website assets.

## Commands (repository root)

```sh
npm ci --prefix scripts/styles --ignore-scripts --no-audit --no-fund
node scripts/build_styles.mjs
node scripts/build_styles.mjs --check
node --test scripts/styles.test.mjs
npm audit --prefix scripts/styles --json
```

The supported Node line is 24 (minimum 24.15.0); existing CI pins 24.22.1.
The local bootstrap used official npm 12.2.2 with its registry SHA-512 integrity
verified because npm was absent from the host PATH. That bootstrap is a scratch
tool outside the repository, not a new website dependency. Standard npm clients
supporting lockfile v3 can use the committed lock. No implicit `npx` download is
used by the build.

`styles/sources.json` explicitly lists the 89 public HTML files and the shared
consent script. The build copies only these files into an isolated temporary
scanner directory, with automatic discovery disabled. Inline script text keeps
complete dynamic class strings visible to the compiler. Custom state rules and
all existing inline CSS remain in their original pages. Required focus/action,
disabled, warning and responsive selectors have an explicit output smoke gate;
browser/state regression remains necessary because a selector check alone does
not prove appearance or behavior.

`styles/build-manifest.json` binds final source/input hashes and the complete
output digest. Input hashes normalize only CRLF to LF; output hashes cover exact
CSS bytes. Builds contain no timestamp or absolute local path. The `--check`
operation compiles to its own temporary directory and compares bytes, references
and recorded inputs without changing repository files. A stale result fails.
It does not regenerate assets first. Old content-named assets are retained;
deleting unreferenced assets requires a separate reviewed cleanup.

Only seven approved pages receive the new stylesheet. Six short network-delivery
descriptions are corrected to first-party styling. Tool logic, inline styles,
canonicals and consent behavior remain unchanged. A distinct strict source
approval manifest, maintained separately, protects historical release evidence.
