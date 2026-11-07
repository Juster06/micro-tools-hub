# Batch Filename Planner

## Task 25.1 public verification

The deployed page matched main `c127f856cbd97497412ec35ed66b3b1a58c4b2dc`. All 6 fresh public browser cases passed on 2026-11-07. The release proposal is backed by [the publication audit](../audit/BATCH_FILENAME_PLANNER_RELEASE_VERIFICATION.json).

Canonical route `batch-filename-planner/index.html`.

Use one source at a time. Prefix and numbering go before the base name. A suffix goes before the last extension. A leading-only dot belongs to a dotfile. Case applies to the full target. The CSV prefixes formula-like cells with an apostrophe for spreadsheet safety.

Up to 500 names, 255 UTF-16 units per name, 64 per affix, 128 KiB UTF-8 input and manifest. Reject Windows-invalid portable names and NFC/lowercase target collisions. Only File.name is read.

The tool previews mappings and checks a restrictive, case-insensitive NFC collision policy. It never reads file contents or changes files. Existing names outside the selection and filesystem-specific rules are outside this check.

Native browser APIs and the existing shared consent component support this page. Input, filenames and bytes stay local.

The Task 25 development status was TESTED. Local source revision `593f679c7dd953ce4f4a5aee99d5e4fdc1614215` and [verification evidence](../audit/BATCH_FILENAME_PLANNER_VERIFICATION.json).

[Windows naming rules](https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file) informed the portable naming policy. The preview includes case-insensitive NFC collision checks and leaves destination validation to the user.
