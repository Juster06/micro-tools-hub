"""Run genuine unittest discovery and reject empty selections or mandatory skips."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


def canonicalize_temporary_root():
    # Hosted Windows TEMP can use an 8.3 alias. Production resolves paths; give
    # fixtures the same canonical parent without weakening any path assertions.
    if sys.platform == "win32":
        tempfile.tempdir = str(Path(tempfile.gettempdir()).resolve())


def main():
    canonicalize_temporary_root()
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    counts = {"tests": result.testsRun, "failed": len(result.failures) + len(result.errors),
              "skipped": len(result.skipped), "expected_failures": len(result.expectedFailures),
              "unexpected_successes": len(result.unexpectedSuccesses)}
    counts["passed"] = counts["tests"] - sum(counts[k] for k in
        ("failed", "skipped", "expected_failures", "unexpected_successes"))
    print("EDB_UNITTEST_RESULT=" + json.dumps(counts))
    return 0 if result.wasSuccessful() and counts["tests"] > 0 and all(counts[k] == 0 for k in
        ("failed", "skipped", "expected_failures", "unexpected_successes")) else 1


if __name__ == "__main__":
    raise SystemExit(main())
