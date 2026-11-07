# File Byte Comparator

## Task 25.1 public verification

The deployed page matched main `c127f856cbd97497412ec35ed66b3b1a58c4b2dc`. All 8 fresh public browser cases passed on 2026-11-07. The release proposal is backed by [the publication audit](../audit/FILE_BYTE_COMPARATOR_RELEASE_VERIFICATION.json).

Canonical route `file-byte-comparator/index.html`.

Choose two local files. Offsets start at zero. If only the lengths differ, the first differing position is the shorter file’s end. Progress measures the common prefix scanned.

Two files, at most 64 MiB each, paired 256 KiB chunk reads, one pair in flight and 8 KiB report. Ten-second Worker deadline, cancellation and revision guards. Browser buffers and queued I/O are not hard heap or cancellation guarantees.

The Worker compares bytes, without decoding formats or assessing authenticity. Cancellation discards the job and result. Browser-owned buffers and queued reads are outside the application’s chunk budget.

Native browser APIs and the existing shared consent component support this page. Input, filenames and bytes stay local.

The Task 25 development status was TESTED. Local source revision `593f679c7dd953ce4f4a5aee99d5e4fdc1614215` and [verification evidence](../audit/FILE_BYTE_COMPARATOR_VERIFICATION.json).
