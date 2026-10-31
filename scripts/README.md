# Project-management commands

Run from the repository root with a current Node.js release (Node 20+ recommended). No dependency installation, credentials, or network access is required. These are development commands, not a website build.

```sh
node scripts/project.mjs summary
node scripts/project.mjs sync
node scripts/project.mjs check
node --test scripts/project.test.mjs
git diff --check
```

- `summary`: prints inventory totals derived from registry statuses.
- `sync`: updates only marked generated blocks in progress, roadmap, and reconciliation documents. It does not create pages, alter statuses, rewrite narrative, modify the homepage, or verify publication.
- `check`: validates required registry fields, status names, unique IDs/names/paths, safe directories, category/reference integrity, proposal mappings, sequence ranks, homepage counts/links, Back to Hub links, evidence/source hashes, and generated-document agreement.
- Tests: exercise actual rejection of duplicate identities/paths, invalid statuses/references, false publication claims, planned test claims, mismatched source evidence, and derived-count changes.

`last_verification_date` is a YYYY-MM-DD string or `null`. Planned entries must not have passing-test or release evidence. RELEASED entries use dated evidence under `audit/`, with source revision, SHA-256 of normalized HTML, behavior scope, and a checked matching publication. Hash normalization converts CRLF to LF and trims trailing file whitespace; it does not ignore arbitrary changes.

The baseline evidence is historical. This command does not contact the website, detect account permission problems, identify every semantic duplicate, prove source safety, or run browser UI tests. A future session must perform the relevant behavior and publication checks before refreshing evidence. Extend the evidence format/checker deliberately when adding new test suites.

After changing registry data, run `sync`, then `check` and tests. Review the diff so that generated counts/tables and surrounding narrative remain truthful. Node scripts do not need to be deployed or executed by the hosting provider.
