# Batch Filename Planner

Canonical route `batch-filename-planner/index.html`.

Use one source at a time. Prefix and numbering go before the base name. A suffix goes before the last extension. A leading-only dot belongs to a dotfile. Case applies to the full target. The CSV prefixes formula-like cells with an apostrophe for spreadsheet safety.

Up to 500 names, 255 UTF-16 units per name, 64 per affix, 128 KiB UTF-8 input and manifest. Reject Windows-invalid portable names and NFC/lowercase target collisions. Only File.name is read.

The tool previews mappings and checks a restrictive, case-insensitive NFC collision policy. It never reads file contents or changes files. Existing names outside the selection and filesystem-specific rules are outside this check.

Native browser APIs and the existing shared consent component support this page. Input, filenames and bytes stay local.

Task 25 development. Publication pending.
