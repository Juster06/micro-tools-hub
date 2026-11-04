# Duplicate Row Finder

UTF-8 file up to 1 MiB, 500,000 UTF-16 units, 2,000 records, 100 columns, 20,000 cells and 10,000 units per field. First row is always a header and retained, including duplicate names; key columns are 1-based and distinct by position. Missing cells are treated as empty for matching. Choose case sensitivity and whether Unicode leading/trailing whitespace is trimmed for comparison; original values remain unchanged except spreadsheet-formula risk cells receive a leading apostrophe in export. Unicode case conversion follows JavaScript lowercasing, not locale-aware collation. Keeps the first data record for each key. Malformed quoted records are rejected. Formula neutralization changes affected values and should be reviewed before opening output in a spreadsheet.

Input stays local; hosting and the existing styling CDN are separate requests. Publication is pending.
