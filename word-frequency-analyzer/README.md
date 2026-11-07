# Word Frequency Analyzer

## Task 25.1 public verification

The deployed page matched main `c127f856cbd97497412ec35ed66b3b1a58c4b2dc`. All 8 fresh public browser cases passed on 2026-11-07. The release proposal is backed by [the publication audit](../audit/WORD_FREQUENCY_ANALYZER_RELEASE_VERIFICATION.json).

Canonical route `word-frequency-analyzer/index.html`.

Letters and numbers start words. Attached marks and internal straight or curly apostrophes stay with the word. Hyphens split words. Emoji are skipped, and continuous CJK text counts as a run. Ties use locale-independent UTF-16 ordering.

Input allows 100,000 UTF-16 units, 20,000 tokens and 256 units per term. Output is capped at 1,000 ranked rows and 256 KiB. Unicode letters/numbers, attached marks and internal apostrophes form tokens. Hyphens split tokens and emoji are excluded. NFC and native lowercase are explicit options.

The ranking uses a documented token rule, with no linguistic segmentation, stemming or stop-word detection.

Native browser APIs and the existing shared consent component support this page. Input, filenames and bytes stay local.

The Task 25 development status was TESTED. Local source revision `593f679c7dd953ce4f4a5aee99d5e4fdc1614215` and [verification evidence](../audit/WORD_FREQUENCY_ANALYZER_VERIFICATION.json).
