# CSV Column Extractor

UTF-8 local file up to 1 MiB; input up to 500,000 UTF-16 units, 2,000 records, 100 columns, 20,000 cells and 10,000 units per field. First row is included as data (typically headers). Specify unique 1-based column numbers in desired order, for example 3,1; identical headers remain distinct by position. Short rows are padded with empty cells. Quoted delimiters, doubled quotes and multiline fields are supported; malformed quotes are rejected. Output is comma-delimited CSV. Cells beginning with =, +, -, @, tab or leading whitespace before a formula marker are prefixed with an apostrophe to reduce spreadsheet formula injection; this intentionally changes those cells. Inspect output before using it in a spreadsheet. Input is processed locally.

Input stays local; hosting and the existing styling CDN are separate requests. Publication is pending.
