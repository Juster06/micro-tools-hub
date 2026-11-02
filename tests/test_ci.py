"""CI selection and failure-propagation guards, using temporary fixtures only."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location("edb_ci", Path(__file__).resolve().parents[1] / "scripts/ci/run.py")
ci = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ci)


def tap(**overrides):
    counts = {"tests": 2, "pass": 2, "fail": 0, "cancelled": 0, "skipped": 0, "todo": 0, **overrides}
    return "\n".join(f"# {k} {v}" for k, v in counts.items()) + "\n"


class CIGateTests(unittest.TestCase):
    def test_windows_temporary_fixture_parent_is_canonical(self):
        spec = importlib.util.spec_from_file_location("edb_ci_unittest", ci.MAP.with_name("unittest_runner.py"))
        runner = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(runner)
        with tempfile.TemporaryDirectory(prefix="edb-ci-temp-parent-") as temporary:
            child = Path(temporary) / "child"
            child.mkdir()
            alias = str(child / "..")
            with patch.object(runner.sys, "platform", "win32"), patch.object(runner.tempfile, "tempdir", alias):
                runner.canonicalize_temporary_root()
                self.assertEqual(runner.tempfile.tempdir, str(Path(temporary).resolve()))

    def test_aggregate_requires_all_real_jobs_to_succeed(self):
        spec = importlib.util.spec_from_file_location("edb_required_checks", ci.MAP.with_name("required_checks.py"))
        aggregate = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(aggregate)
        states = {k: "success" for k in ("PYTHON_RESULT", "NODE_RESULT", "BROWSER_RESULT")}
        self.assertTrue(aggregate.passed(states))
        self.assertFalse(aggregate.passed({}))
        for key in states:
            for state in ("failure", "cancelled", "skipped"):
                self.assertFalse(aggregate.passed({**states, key: state}))

    def test_real_node_summary_counts(self):
        self.assertEqual(ci.node_counts(tap())["passed"], 2)

    def test_empty_failed_skipped_cancelled_or_todo_node_fails(self):
        for key, value in (("tests", 0), ("fail", 1), ("skipped", 1), ("cancelled", 1), ("todo", 1), ("pass", 1)):
            with self.subTest(key=key), self.assertRaises(ValueError):
                ci.node_counts(tap(**{key: value}))

    def test_missing_or_duplicate_summary_fails(self):
        for output in ("", "PASS", tap() + "# tests 2\n"):
            with self.subTest(output=output), self.assertRaises(ValueError):
                ci.node_counts(output)

    def test_mandatory_layer_rejects_not_run_unknown_empty_or_failed(self):
        for state, passed, failed in (("NOT RUN", 0, 0), ("UNKNOWN", 0, 0), ("PASS", 0, 0), ("FAIL", 2, 1)):
            with self.subTest(state=state), self.assertRaises(ValueError):
                ci.layer_counts({"layers": {"browser": {"status": state, "passed": passed, "failed": failed}}}, "browser")

    def test_scaffold_cannot_pass_mandatory_layer(self):
        with self.assertRaises(ValueError):
            ci.layer_counts({"is_scaffold": True, "layers": {"logic": {"status": "PASS", "passed": 1}}}, "logic")

    def test_requested_pass_does_not_claim_omitted_scope(self):
        result = {"status": "PARTIAL", "layers": {"logic": {"status": "NOT RUN"}, "browser": {"status": "PASS", "passed": 2, "failed": 0, "assertions": 4}}}
        self.assertEqual(ci.layer_counts(result, "browser")["passed"], 2)
        self.assertEqual(result["layers"]["logic"]["status"], "NOT RUN")

    def test_actual_child_assertion_failure_is_nonzero(self):
        code, _ = ci.command([sys.executable, "-c", "assert False, 'controlled fixture'"], 10)
        self.assertNotEqual(code, 0)

    def test_actual_child_timeout_is_failure(self):
        code, output = ci.command([sys.executable, "-c", "import time; time.sleep(20)"], .2)
        self.assertEqual(code, 124)
        self.assertIn("timed out", output)

    def test_missing_executable_is_not_success(self):
        with self.assertRaises(OSError):
            ci.command([str(Path(tempfile.gettempdir()) / "edb-nonexistent-command-9-5")], 1)


class CoverageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="edb-ci-coverage-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.map = self.root / "map.json"
        self.value = {"schema_version": 1, "tools": {"fixture": {"structural_job": "python-project", "logic_job": None, "browser_job": "browser-tests", "unavailable_reason": "specialist fixture"}},
                      "python_files": ["tests/test_example.py"], "node_files": ["scripts/example.test.mjs"],
                      "browser_files": ["tests/tools/fixture/extended-browser.test.mjs"]}
        self.write("TOOL_REGISTRY.json", {"tools": [{"id": "fixture", "status": "RELEASED"}]})
        self.write("tests/tools/fixture/browser.cases.json", {"schema_version": 1, "cases": [{"steps": [{"action": "expect"}]}]})
        for name in self.value["python_files"] + self.value["node_files"] + self.value["browser_files"]:
            self.write(name, "// nonempty fixture")

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content if isinstance(content, str) else json.dumps(content), encoding="utf-8")

    def check(self):
        self.map.write_text(json.dumps(self.value), encoding="utf-8")
        return ci.coverage(self.root, self.map)

    def test_complete_explicit_mapping_passes(self):
        self.assertEqual(len(self.check()["tools"]), 1)

    def test_missing_mapped_file_fails(self):
        (self.root / self.value["browser_files"][0]).unlink()
        with self.assertRaises(ValueError):
            self.check()

    def test_empty_mapped_file_fails(self):
        self.write(self.value["python_files"][0], "")
        with self.assertRaises(ValueError):
            self.check()

    def test_unmapped_new_test_fails(self):
        self.write("scripts/unreviewed.test.mjs", "// new test")
        with self.assertRaises(ValueError):
            self.check()

    def test_duplicate_test_mapping_fails(self):
        self.value["node_files"].extend(self.value["browser_files"])
        with self.assertRaises(ValueError):
            self.check()

    def test_empty_browser_cases_fail(self):
        self.write("tests/tools/fixture/browser.cases.json", {"schema_version": 1, "cases": []})
        with self.assertRaises(ValueError):
            self.check()

    def test_new_registry_tool_requires_explicit_scope(self):
        self.write("TOOL_REGISTRY.json", {"tools": [{"id": "second", "status": "TESTED"}]})
        with self.assertRaises(ValueError):
            self.check()

    def test_new_specialist_logic_cannot_be_silently_omitted(self):
        self.write("tests/tools/fixture/logic.cases.json", {"schema_version": 1, "cases": [{"input": "x", "expected": "x"}]})
        with self.assertRaises(ValueError):
            self.check()


if __name__ == "__main__":
    unittest.main()
