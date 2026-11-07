# Word Frequency Analyzer

Canonical route `word-frequency-analyzer/index.html`.

Letters and numbers start words. Attached marks and internal straight or curly apostrophes stay with the word. Hyphens split words. Emoji are skipped, and continuous CJK text counts as a run. Ties use locale-independent UTF-16 ordering.

100,000 UTF-16 units; 20,000 tokens; 256 units per term; 1,000 ranked rows and 256 KiB output. Unicode letters/numbers, attached marks and internal apostrophes form tokens. Hyphens split tokens and emoji are excluded. NFC and native lowercase are explicit options.

The ranking uses a documented token rule, with no linguistic segmentation, stemming or stop-word detection.

Native browser APIs and the existing shared consent component support this page. Input, filenames and bytes stay local.

Task 25 development. Publication pending.
