# CSV Viewer

Comma, semicolon or tab delimiter. Up to 500,000 UTF-16 input units, 1 MiB UTF-8 file, 2,000 records, 100 columns, 20,000 cells and 10,000 units per field. CRLF and CR normalize to LF. Quoted delimiters, doubled quotes and multiline fields are supported; malformed quotes are rejected. First record can be a header; otherwise generic column labels are used. Ragged records display blank missing cells. Table text is never interpreted as HTML or spreadsheet formulas. The parser is a local bounded state machine; no third-party parser is bundled.

Input stays local; hosting and the existing styling CDN are separate requests. Publication is pending.
