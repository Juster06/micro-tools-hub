# Optional reproducible Task 22 bundle

Pinned build-only package manifest and pnpm lockfile. Copy both to an isolated directory outside the repository, run `pnpm install --frozen-lockfile --ignore-scripts`, then `node scripts/vendor/task22/build.mjs ABSOLUTE_NODE_MODULES --check`. Omit `--check` only for a reviewed rebuild followed by retesting and fresh source-bound evidence. No install or build is needed to use the static website.

Runtime: Marked 18.1.3 MIT, parse5 8.1.0 MIT, entities 9.0.0 BSD-2-Clause. Build only: esbuild 0.28.2 MIT and its platform executable. See local third-party notices and audit/TASK_22_SECURITY_REVIEW.json. Existing Task 21 bounded HTML parser and CSP are imported unchanged at build time; the new bundle is standalone. No dependency directories are committed.
