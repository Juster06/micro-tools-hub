# File Byte Comparator

Canonical route `file-byte-comparator/index.html`.

Choose two local files. Offsets start at zero. If only the lengths differ, the first differing position is the shorter file’s end. Progress measures the common prefix scanned.

Two files, at most 64 MiB each, paired 256 KiB chunk reads, one pair in flight and 8 KiB report. Ten-second Worker deadline, cancellation and revision guards. Browser buffers and queued I/O are not hard heap or cancellation guarantees.

The Worker compares bytes, without decoding formats or assessing authenticity. Cancellation discards the job and result. Browser-owned buffers and queued reads are outside the application’s chunk budget.

Native browser APIs and the existing shared consent component support this page. Input, filenames and bytes stay local.

Task 25 development. Publication pending.
