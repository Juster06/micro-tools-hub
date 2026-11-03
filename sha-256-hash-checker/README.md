# SHA-256 Text & File Hash Checker

Canonical route: `sha-256-hash-checker/index.html`.

Text mode hashes UTF-8 without normalization; empty text is valid, up to 100,000 UTF-16 units. Unpaired surrogate code units are rejected instead of silently changed. File mode accepts any local file up to 16 MiB, including empty files; the whole bounded file is read into memory. Optionally enter a 64-character hexadecimal SHA-256 digest for comparison (case-insensitive; surrounding whitespace ignored; 128-unit field limit). This tool requires a secure context, Web Crypto SHA-256 and browser UTF-8 encoding. There is no insecure fallback. A matching digest alone does not establish the identity or trustworthiness of a file. Hashing is not encryption.

Inputs are not uploaded or saved; hosting and the existing Tailwind CDN are separate network requests. Publication is pending.
