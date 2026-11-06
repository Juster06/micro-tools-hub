# Hashtag Counter

Current status: Task 21 complete and publicly verified; PR #38 and #39 merged. RELEASED at main `93f2589b244f933e353d4d93ee145e35ed354399`. The development checkpoint below is historical.

## Task21.1 release proposal

Fresh public verification passed against deployed `9fa032140639550abd9a0449ed7ef5198354bd40`; evidence:
`audit/HASHTAG_COUNTER_RELEASE_VERIFICATION.json`. Proposed RELEASED
status awaits owner review/merge/deployment; the current deployed registry remains
TESTED. Original development scope below is historical. Known interface/format
limitations remain; no runtime, dependency, privacy or consent change.

Canonical route: `hashtag-counter/index.html`.

Extract hashtags from full captions, count occurrences and compare duplicates.

## Scope and limits

100,000 UTF-16 input units; 10,000 occurrences; 100 Unicode code points per tag; 1 MiB output. Tags start with a letter, number or underscore, followed by letters, numbers, combining marks or underscore. NFC normalization is applied. A hash following a letter/number/mark, underscore, #, slash, @, dot, =, %, & or hyphen is ignored. HTTP(S), www and // URL tokens through their next whitespace are excluded. C# and attached fragments are excluded. Punctuation/emoji ends a tag. This is an explicit caption policy, not universal social-platform compatibility.

Each job has a 2-second Worker deadline and can be cancelled. Input changes/reset terminate the job and discard its result. Timers do not guarantee a hard memory limit.

## Verification

TESTED — publication pending. Source checkpoint `f6a4ceab5badc73510159a33ed3b13c61f85384c`; evidence: `audit/HASHTAG_COUNTER_VERIFICATION.json`. Scoped verification passed: 11 canonical inline logic fixtures; 7 canonical Chromium interaction fixtures / 21 assertions; 5 specialized Node Worker/logic tests; 6 extended Chromium tests: actual output, clipboard/download mocks, reset, cancellation, late-result invalidation, keyboard/layout, missing Worker and actual 2-second deadline. Full mapped regression and hosted PR checks remain mandatory before owner review. No public availability or RELEASED claim.
