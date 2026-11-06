# Hashtag Counter

Canonical route: `hashtag-counter/index.html`.

Extract hashtags from full captions, count occurrences and compare duplicates.

## Scope and limits

100,000 UTF-16 input units; 10,000 occurrences; 100 Unicode code points per tag; 1 MiB output. Tags start with a letter, number or underscore, followed by letters, numbers, combining marks or underscore. NFC normalization is applied. A hash following a letter/number/mark, underscore, #, slash, @, dot, =, %, & or hyphen is ignored. HTTP(S), www and // URL tokens through their next whitespace are excluded. C# and attached fragments are excluded. Punctuation/emoji ends a tag. This is an explicit caption policy, not universal social-platform compatibility.

Each job has a 2-second Worker deadline and can be cancelled. Input changes/reset terminate the job and discard its result. Timers do not guarantee a hard memory limit.

## Verification

Development in progress; no TESTED or public-release claim yet. Required tests and source-bound evidence must pass before status changes.
