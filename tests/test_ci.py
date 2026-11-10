"""CI selection and failure-propagation guards, using temporary fixtures only."""
import importlib.util
import copy
from contextlib import redirect_stdout, redirect_stderr
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
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


class PythonPartitionTests(unittest.TestCase):
    def setUp(self):
        scripts = str(ci.ROOT / "scripts")
        if scripts not in sys.path:
            sys.path.insert(0, scripts)
            self.addCleanup(lambda: sys.path.remove(scripts))
        self.protocol = ci.unittest_protocol()
        self.temporary = tempfile.TemporaryDirectory(prefix="edb-python-groups-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.logs = self.root / "logs"
        self.logs.mkdir()
        self.mapping = {"python_files": ["tests/test_sample.py"], "python_partitions": [
            {"id": "historical", "classes": [{"id": "test_sample.First", "methods": ["test_one", "test_two"]}]},
            {"id": "current-project", "classes": [{"id": "test_sample.Second", "methods": ["test_other"]}]}]}
        self.plan = self.protocol.partition_plan(self.mapping)
        self.identity = {"checkout": "1" * 40, "approval_sha256": "2" * 64, "coverage_sha256": "3" * 64}
        self.invocation = "a" * 32

    def record(self, group, invocation=None):
        ids = self.plan[group]
        counts = {key: 0 for key in self.protocol.COUNT_KEYS}
        counts.update(tests=len(ids), passed=len(ids))
        return {"schema_version": 1, "group": group, "invocation": invocation or self.invocation,
                "identity": dict(self.identity), "discovered_ids": self.protocol.all_ids(self.plan),
                "started_ids": list(ids), "succeeded_ids": list(ids), "counts": counts}

    def validate(self, value, group="historical"):
        self.protocol.validate_group_result(value, group, self.invocation, self.plan, self.identity)

    def successful_command(self, args, timeout, cwd):
        self.assertEqual(timeout, 240)
        self.assertEqual(cwd, self.root)
        group = args[args.index("--group") + 1]
        invocation = args[args.index("--invocation") + 1]
        return 0, self.protocol.GROUP_MARKER + json.dumps(self.record(group, invocation)) + "\n"

    def fixture_suite(self):
        name = "test_partition_probe"
        path = self.root / "tests" / (name + ".py")
        path.parent.mkdir(exist_ok=True)
        path.write_text("import unittest\nevents=[]\n"
                        "class First(unittest.TestCase):\n"
                        " @classmethod\n def setUpClass(cls): events.append('setup-first')\n"
                        " @classmethod\n def tearDownClass(cls): events.append('cleanup-first')\n"
                        " def test_one(self): events.append('one')\n"
                        " def test_two(self): events.append('two')\n"
                        "class Second(unittest.TestCase):\n"
                        " @classmethod\n def setUpClass(cls): events.append('setup-second')\n"
                        " @classmethod\n def tearDownClass(cls): events.append('cleanup-second')\n"
                        " def test_other(self): events.append('other')\n", encoding="utf-8", newline="\n")
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        self.assertNotIn(name, sys.modules)
        sys.modules[name] = module
        self.addCleanup(lambda: sys.modules.pop(name, None))
        spec.loader.exec_module(module)
        mapping = json.loads(json.dumps(self.mapping).replace("test_sample", name))
        plan = self.protocol.partition_plan(mapping)
        tests = list(self.protocol.flatten(unittest.TestLoader().loadTestsFromModule(module)))
        return module, mapping, plan, tests

    def test_manifest_requires_two_nonempty_disjoint_complete_groups(self):
        mutations = [lambda m: m["python_partitions"].pop(),
                     lambda m: m["python_partitions"].reverse(),
                     lambda m: m["python_partitions"][0].update(id="unknown"),
                     lambda m: m["python_partitions"][0].update(classes=[]),
                     lambda m: m["python_partitions"][1]["classes"].append(m["python_partitions"][0]["classes"][0]),
                     lambda m: m["python_partitions"][0]["classes"][0]["methods"].append("test_one"),
                     lambda m: m["python_partitions"][0]["classes"][0].update(methods=[]),
                     lambda m: m["python_partitions"][0]["classes"][0].update(methods=["../test_escape"]),
                     lambda m: m["python_partitions"][0]["classes"][0].update(id="test_other.First"),
                     lambda m: m["python_files"].append("tests/test_unassigned.py"),
                     lambda m: m["python_files"].append("tests/test_sample.py")]
        for mutate in mutations:
            value = copy.deepcopy(self.mapping)
            mutate(value)
            with self.assertRaises(ValueError):
                self.protocol.partition_plan(value)

    def test_strict_json_rejects_duplicate_keys_and_nonfinite_values(self):
        self.assertEqual(self.protocol.strict_json('{"a":1}'), {"a": 1})
        for source in ['{"a":1,"a":2}', '{"x":{"a":1,"a":2}}', '{"a":NaN}', '{"a":Infinity}']:
            with self.subTest(source=source), self.assertRaises(ValueError):
                self.protocol.strict_json(source)

    def test_distinct_class_aliases_remain_distinct_required_test_ids(self):
        value = copy.deepcopy(self.mapping)
        value["python_partitions"][1]["classes"][0]["methods"] = ["test_one"]
        plan = self.protocol.partition_plan(value)
        self.assertEqual(len(self.protocol.all_ids(plan)), 3)
        self.assertIn("test_sample.First.test_one", self.protocol.all_ids(plan))
        self.assertIn("test_sample.Second.test_one", self.protocol.all_ids(plan))

    def test_missing_new_duplicate_and_unmapped_discovered_cases_fail(self):
        module, mapping, plan, tests = self.fixture_suite()
        self.protocol.validate_discovered(tests, mapping, plan, self.root)
        for selection in [tests[:-1], tests + [tests[0]], tests[1:] + [tests[1]]]:
            with self.assertRaises(ValueError):
                self.protocol.validate_discovered(selection, mapping, plan, self.root)
        module.First.test_new = lambda case: None
        new_tests = list(self.protocol.flatten(unittest.TestLoader().loadTestsFromModule(module)))
        with self.assertRaises(ValueError):
            self.protocol.validate_discovered(new_tests, mapping, plan, self.root)
        with patch.object(self.protocol.inspect, "getfile", return_value=str(self.root / "outside.py")):
            with self.assertRaises(ValueError):
                self.protocol.validate_discovered(tests, mapping, plan, self.root)
        with self.assertRaises(ValueError):
            self.protocol.validate_discovered(tests, mapping, plan, self.root, ["import failed"])

    def test_real_discovery_import_errors_cannot_be_selected_away(self):
        _, mapping, plan, _ = self.fixture_suite()
        (self.root / "tests/test_broken_partition_probe.py").write_text("raise RuntimeError('import failure')\n", encoding="utf-8")
        loader = unittest.TestLoader()
        tests = list(self.protocol.flatten(loader.discover(str(self.root / "tests"))))
        self.addCleanup(lambda: sys.path.remove(str(self.root / "tests")) if str(self.root / "tests") in sys.path else None)
        self.assertTrue(loader.errors)
        with self.assertRaises(ValueError):
            self.protocol.validate_discovered(tests, mapping, plan, self.root, loader.errors)

    def test_selection_preserves_native_order_and_whole_class_fixtures(self):
        module, mapping, plan, tests = self.fixture_suite()
        self.protocol.validate_discovered(tests, mapping, plan, self.root)
        observed = []
        for group in self.protocol.GROUPS:
            result = self.protocol.run_selected([t for t in tests if t.id() in plan[group]], io.StringIO())
            self.assertEqual(result["started_ids"], plan[group])
            self.assertEqual(result["succeeded_ids"], plan[group])
            observed.extend(result["started_ids"])
        self.assertEqual(observed, self.protocol.all_ids(plan))
        self.assertEqual(module.events, ["setup-first", "one", "two", "cleanup-first", "setup-second", "other", "cleanup-second"])

    def test_all_unsuccessful_unittest_outcomes_are_rejected(self):
        required_id = self.plan["current-project"][0]
        for outcome in ["success", "failure", "error", "skip", "expected", "unexpected", "subtest"]:
            class Example(unittest.TestCase):
                def id(self):
                    return required_id
                def test_case(self):
                    if outcome in {"failure", "expected"}:
                        self.fail("controlled failure")
                    elif outcome == "error":
                        raise RuntimeError("controlled error")
                    elif outcome == "skip":
                        self.skipTest("controlled skip")
                    elif outcome == "subtest":
                        with self.subTest(value="negative"):
                            self.fail("controlled subtest failure")
            if outcome in {"expected", "unexpected"}:
                unittest.expectedFailure(Example.test_case)
            value = self.record("current-project")
            value.update(self.protocol.run_selected([Example("test_case")], io.StringIO()))
            if outcome == "success":
                self.validate(value, "current-project")
            else:
                with self.subTest(outcome=outcome), self.assertRaises(ValueError):
                    self.validate(value, "current-project")

    def test_class_setup_and_teardown_failures_cannot_pass(self):
        required_id = self.plan["current-project"][0]
        for failing_fixture in ["setup", "teardown"]:
            class Example(unittest.TestCase):
                @classmethod
                def setUpClass(cls):
                    if failing_fixture == "setup":
                        raise RuntimeError("controlled setup failure")
                @classmethod
                def tearDownClass(cls):
                    if failing_fixture == "teardown":
                        raise RuntimeError("controlled teardown failure")
                def id(self):
                    return required_id
                def test_case(self):
                    pass
            value = self.record("current-project")
            value.update(self.protocol.run_selected([Example("test_case")], io.StringIO()))
            self.assertEqual(value["counts"]["failed"], 1)
            with self.assertRaises(ValueError):
                self.validate(value, "current-project")

    def test_same_count_substitution_duplicate_and_unfinished_ids_fail(self):
        self.validate(self.record("historical"))
        for field in ["discovered_ids", "started_ids", "succeeded_ids"]:
            for mutation in [lambda ids: ids[:-1], lambda ids: ids + [ids[0]], lambda ids: ids[:-1] + [ids[0]]]:
                value = self.record("historical")
                value[field] = mutation(value[field])
                with self.subTest(field=field), self.assertRaises(ValueError):
                    self.validate(value)

    def test_protocol_identity_counts_and_single_summary_are_strict(self):
        mutations = [lambda v: v.update(schema_version=True), lambda v: v.update(group="unknown"),
                     lambda v: v.update(invocation="b" * 32), lambda v: v.update(identity={}),
                     lambda v: v.update(process_seconds=0), lambda v: v["counts"].update(passed=True),
                     lambda v: v["counts"].update(tests=3), lambda v: v["counts"].update(failed=-1),
                     lambda v: v["counts"].update(skipped=1), lambda v: v["counts"].update(extra=0)]
        for mutate in mutations:
            value = self.record("historical")
            mutate(value)
            with self.assertRaises(ValueError):
                self.validate(value)
        good = self.protocol.GROUP_MARKER + json.dumps(self.record("historical"))
        self.validate(self.protocol.parse_group_result(good))
        for output in ["", good + "\n" + good, self.protocol.GROUP_MARKER + "{invalid"]:
            with self.assertRaises(ValueError):
                self.protocol.parse_group_result(output)

    def test_reconciliation_requires_both_groups_and_exact_union(self):
        values = [self.record(group) for group in self.protocol.GROUPS]
        self.assertEqual(self.protocol.reconcile_groups(values, self.plan)["passed"], 3)
        for bad in [values[:1], values[::-1], [values[0], values[0]]]:
            with self.assertRaises(ValueError):
                self.protocol.reconcile_groups(bad, self.plan)
        altered = copy.deepcopy(values)
        altered[1]["started_ids"] = [altered[0]["started_ids"][0]]
        with self.assertRaises(ValueError):
            self.protocol.reconcile_groups(altered, self.plan)

    def test_parent_executes_sequential_groups_at_240_seconds_with_fresh_acceptance(self):
        entry = {"status": "FAIL"}
        contract = (self.mapping, self.plan, self.identity)
        with patch.object(ci, "unittest_protocol", return_value=self.protocol), \
                patch.object(self.protocol, "source_contract", return_value=contract) as source, \
                patch.object(ci, "command", side_effect=self.successful_command) as commands, redirect_stdout(io.StringIO()):
            ci.execute_python_groups(entry, self.logs, 3, self.root)
        self.assertEqual(commands.call_count, 2)
        self.assertEqual(source.call_count, 2)
        self.assertEqual([row["group"] for row in entry["groups"]], list(self.protocol.GROUPS))
        self.assertEqual(len({row["invocation"] for row in entry["groups"]}), 2)
        self.assertTrue(all(row["timeout_seconds"] == 240 and row["status"] == "PASS" for row in entry["groups"]))
        self.assertEqual((entry["status"], entry["tests"], entry["passed"]), ("PASS", 3, 3))

    def test_parent_rejects_failed_missing_malformed_and_stale_child_results(self):
        contract = (self.mapping, self.plan, self.identity)
        for fault in ["exit", "timeout", "missing", "malformed", "duplicate", "stale"]:
            def command(args, timeout, cwd):
                code, output = self.successful_command(args, timeout, cwd)
                if fault == "exit":
                    return 1, output
                if fault == "timeout":
                    return 124, output
                if fault == "missing":
                    return 0, ""
                if fault == "malformed":
                    return 0, self.protocol.GROUP_MARKER + "{invalid"
                if fault == "duplicate":
                    return 0, output + output
                value = self.protocol.parse_group_result(output)
                value["invocation"] = "stale"
                return 0, self.protocol.GROUP_MARKER + json.dumps(value)
            entry = {"status": "FAIL"}
            with patch.object(ci, "unittest_protocol", return_value=self.protocol), \
                    patch.object(self.protocol, "source_contract", return_value=contract), \
                    patch.object(ci, "command", side_effect=command) as commands, redirect_stdout(io.StringIO()):
                with self.assertRaises(ValueError):
                    ci.execute_python_groups(entry, self.logs, 3, self.root)
            self.assertEqual(commands.call_count, 1)
            self.assertEqual(entry["status"], "FAIL")

    def test_parent_rejects_second_group_failure_without_partial_success(self):
        def command(args, timeout, cwd):
            code, output = self.successful_command(args, timeout, cwd)
            return (1 if "current-project" in args else code), output
        entry = {"status": "FAIL"}
        with patch.object(ci, "unittest_protocol", return_value=self.protocol), \
                patch.object(self.protocol, "source_contract", return_value=(self.mapping, self.plan, self.identity)), \
                patch.object(ci, "command", side_effect=command) as commands, redirect_stdout(io.StringIO()):
            with self.assertRaises(ValueError):
                ci.execute_python_groups(entry, self.logs, 3, self.root)
        self.assertEqual(commands.call_count, 2)
        self.assertEqual([v["status"] for v in entry["groups"]], ["PASS", "FAIL"])
        self.assertEqual(entry["status"], "FAIL")
        self.assertNotIn("passed", entry)

    def test_parent_revalidates_source_after_both_successful_children(self):
        entry = {"status": "FAIL"}
        with patch.object(ci, "unittest_protocol", return_value=self.protocol), \
                patch.object(self.protocol, "source_contract", side_effect=[(self.mapping, self.plan, self.identity), ValueError("changed source")]) as source, \
                patch.object(ci, "command", side_effect=self.successful_command) as commands, redirect_stdout(io.StringIO()):
            with self.assertRaises(ValueError):
                ci.execute_python_groups(entry, self.logs, 3, self.root)
        self.assertEqual((commands.call_count, source.call_count), (2, 2))
        self.assertEqual(entry["status"], "FAIL")

    def test_live_contract_rejects_same_timestamp_tampering_and_accepts_restoration(self):
        root = self.root / "repository"
        subprocess.run(["git", "clone", "--shared", "--no-checkout", "--quiet", str(ci.ROOT), str(root)],
                       check=True, capture_output=True, timeout=30)
        import css_overlay
        approved = css_overlay.validate_current(ci.ROOT)
        for name in set(approved["files"]) | {css_overlay.MANIFEST, css_overlay.IDENTITY}:
            target = root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ci.ROOT / name, target)
        original_contract = self.protocol.source_contract(root)
        target = root / "scripts/ci/coverage.json"
        raw, metadata = target.read_bytes(), target.stat()
        try:
            target.write_bytes(bytes([raw[0] ^ 1]) + raw[1:])
            os.utime(target, ns=(metadata.st_atime_ns, metadata.st_mtime_ns))
            self.assertEqual(target.stat().st_size, metadata.st_size)
            self.assertEqual(target.stat().st_mtime_ns, metadata.st_mtime_ns)
            with self.assertRaises(ValueError):
                self.protocol.source_contract(root)
        finally:
            target.write_bytes(raw)
            os.utime(target, ns=(metadata.st_atime_ns, metadata.st_mtime_ns))
        self.assertEqual(self.protocol.source_contract(root), original_contract)

    def test_child_rechecks_source_and_cleans_up_before_success(self):
        _, mapping, plan, _ = self.fixture_suite()
        contract = (mapping, plan, self.identity)
        import git_fixtures
        for after in [contract, ValueError("changed source")]:
            output = io.StringIO()
            with patch.object(self.protocol, "ROOT", self.root), \
                    patch.object(self.protocol, "source_contract", side_effect=[contract, after]) as source, \
                    patch.object(git_fixtures, "close_readers") as cleanup, redirect_stdout(output), redirect_stderr(io.StringIO()):
                code = self.protocol.main(["--group", "historical", "--invocation", self.invocation])
            self.assertEqual(source.call_count, 2)
            cleanup.assert_called_once_with()
            if isinstance(after, Exception):
                self.assertEqual(code, 1)
                self.assertNotIn(self.protocol.GROUP_MARKER, output.getvalue())
            else:
                self.assertEqual(code, 0)
                value = self.protocol.parse_group_result(output.getvalue())
                self.protocol.validate_group_result(value, "historical", self.invocation, plan, self.identity)
        self.addCleanup(lambda: sys.path.remove(str(self.root / "tests")) if str(self.root / "tests") in sys.path else None)


if __name__ == "__main__":
    unittest.main()
