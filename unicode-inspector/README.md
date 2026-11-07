# Unicode Inspector

Canonical route `unicode-inspector/index.html`.

Inspect UTF-16 offsets, code points, hexadecimal UTF-8 bytes, grapheme boundaries and normalization summaries. Descriptions are character categories. Control characters are represented by labels and code points.

8,192 UTF-16 input units, 4,096 diagnostic rows and 128 KiB report. Character category descriptions, no names database. Intl.Segmenter is optional. Show invalid lone surrogates and escaped controls, and label capped output.

Native Unicode data and segmentation can differ across engines. A lone surrogate has no valid UTF-8 encoding. This tool does not identify confusables or certify that text is safe.

Native browser APIs and the existing shared consent component support this page. Input, filenames and bytes stay local.

Task 25 status is TESTED. Publication is pending. Local source revision `593f679c7dd953ce4f4a5aee99d5e4fdc1614215` and [verification evidence](../audit/UNICODE_INSPECTOR_VERIFICATION.json).
