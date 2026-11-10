"""Discover every reviewed test and report exact execution in isolated groups."""
import argparse
from collections import Counter
import hashlib
import inspect
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
import uuid

ROOT = Path(__file__).resolve().parents[2]
GROUPS = ("historical", "current-project")
GROUP_MARKER = "EDB_UNITTEST_GROUP_RESULT="
COUNT_KEYS = ("tests", "failed", "skipped", "expected_failures", "unexpected_successes", "passed")


def strict_json(source):
    def unique(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise ValueError("Duplicate JSON key")
            value[key] = item
        return value
    def invalid_constant(value):
        raise ValueError("Non-finite JSON number")
    return json.loads(source, object_pairs_hook=unique, parse_constant=invalid_constant)


def partition_plan(mapping):
    if not isinstance(mapping, dict):
        raise ValueError("Invalid Python coverage document")
    files = mapping.get("python_files")
    if (not isinstance(files, list) or not files or any(not isinstance(n, str) or
            not re.fullmatch(r"tests/test_[A-Za-z0-9_]+\.py", n) for n in files)
            or len(files) != len(set(files))):
        raise ValueError("Invalid mapped Python files")
    groups = mapping.get("python_partitions")
    if (not isinstance(groups, list) or len(groups) != len(GROUPS)
            or any(not isinstance(g, dict) for g in groups)
            or tuple(g.get("id") for g in groups) != GROUPS):
        raise ValueError("Missing or unknown Python group")
    plan, owners, modules = {}, set(), set()
    allowed_modules = {Path(n).stem for n in files}
    for group in groups:
        classes = group.get("classes")
        if set(group) != {"id", "classes"} or not isinstance(classes, list) or not classes:
            raise ValueError("Empty or invalid Python group")
        ids = []
        for entry in classes:
            if not isinstance(entry, dict) or set(entry) != {"id", "methods"}:
                raise ValueError("Invalid Python class assignment")
            owner, methods = entry["id"], entry["methods"]
            if (not isinstance(owner, str) or not re.fullmatch(r"test_[A-Za-z0-9_]+\.[A-Za-z_][A-Za-z0-9_]*", owner)
                    or owner in owners or owner.split(".")[0] not in allowed_modules):
                raise ValueError("Duplicate or unmapped Python class")
            if (not isinstance(methods, list) or not methods or any(not isinstance(n, str) or
                    not re.fullmatch(r"test_[A-Za-z0-9_]+", n) for n in methods)
                    or len(methods) != len(set(methods))):
                raise ValueError("Empty or duplicate Python test assignment")
            owners.add(owner)
            modules.add(owner.split(".")[0])
            ids.extend(owner + "." + method for method in methods)
        plan[group["id"]] = sorted(ids)
    if modules != allowed_modules:
        raise ValueError("Mapped Python module has no assigned tests")
    return plan


def all_ids(plan):
    return sorted(name for group in GROUPS for name in plan[group])


def require_ids(actual, expected):
    if (not isinstance(actual, list) or any(not isinstance(n, str) for n in actual)
            or Counter(actual) != Counter(expected) or len(actual) != len(set(actual))):
        raise ValueError("Missing, duplicate or unexpected Python test IDs")


def source_contract(root=ROOT):
    # Every call performs live validation; no approval or inventory result cache.
    scripts = str(ROOT / "scripts")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    import css_overlay
    approval = css_overlay.validate_current(root)
    raw = css_overlay.safe_file(root, "scripts/ci/coverage.json").read_bytes().replace(b"\r\n", b"\n")
    digest = hashlib.sha256(raw).hexdigest()
    if digest != approval["files"]["scripts/ci/coverage.json"]["sha256"]:
        raise ValueError("Coverage changed after source validation")
    mapping = strict_json(raw)
    plan = partition_plan(mapping)
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True, timeout=15).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", head):
        raise ValueError("Invalid checkout identity")
    identity = {"checkout": head, "approval_sha256": css_overlay.MANIFEST_SHA256, "coverage_sha256": digest}
    return mapping, plan, identity


def flatten(suite):
    for test in suite:
        if isinstance(test, unittest.TestSuite):
            yield from flatten(test)
        else:
            yield test


def validate_discovered(tests, mapping, plan, root, errors=()):
    if errors or any(not isinstance(t, unittest.TestCase) for t in tests):
        raise ValueError("Python discovery failed")
    require_ids([t.id() for t in tests], all_ids(plan))
    expected_origins = {(root / n).resolve() for n in mapping["python_files"]}
    origins = set()
    for test in tests:
        owner = type(test).__module__ + "." + type(test).__qualname__
        if test.id().rsplit(".", 1)[0] != owner:
            raise ValueError("Unexpected Python test identity")
        origins.add(Path(inspect.getfile(type(test))).resolve())
    if origins != expected_origins:
        raise ValueError("Discovered Python test origin is not mapped")


class ExactResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.started_ids = []
        self.succeeded_ids = []

    def startTest(self, test):
        self.started_ids.append(test.id())
        super().startTest(test)

    def addSuccess(self, test):
        self.succeeded_ids.append(test.id())
        super().addSuccess(test)


def run_selected(tests, stream=None):
    result = unittest.TextTestRunner(verbosity=2, resultclass=ExactResult, stream=stream).run(unittest.TestSuite(tests))
    counts = {"tests": result.testsRun, "failed": len(result.failures) + len(result.errors),
              "skipped": len(result.skipped), "expected_failures": len(result.expectedFailures),
              "unexpected_successes": len(result.unexpectedSuccesses), "passed": len(result.succeeded_ids)}
    return {"counts": counts, "started_ids": result.started_ids, "succeeded_ids": result.succeeded_ids}


def validate_group_result(value, group, invocation, plan, identity):
    keys = {"schema_version", "group", "invocation", "identity", "discovered_ids", "counts", "started_ids", "succeeded_ids"}
    if (not isinstance(value, dict) or set(value) != keys or type(value.get("schema_version")) is not int
            or value["schema_version"] != 1 or value.get("group") != group
            or value.get("invocation") != invocation or value.get("identity") != identity
            or group not in (*GROUPS, "all")):
        raise ValueError("Python group identity differs from this invocation")
    expected = all_ids(plan) if group == "all" else plan[group]
    require_ids(value.get("discovered_ids"), all_ids(plan))
    require_ids(value.get("started_ids"), expected)
    require_ids(value.get("succeeded_ids"), expected)
    counts = value.get("counts")
    if (not isinstance(counts, dict) or set(counts) != set(COUNT_KEYS)
            or any(type(counts[k]) is not int or counts[k] < 0 for k in COUNT_KEYS)
            or counts["tests"] != len(expected) or counts["passed"] != len(expected)
            or any(counts[k] for k in COUNT_KEYS if k not in {"tests", "passed"})):
        raise ValueError("Python group failed, skipped or did not execute exactly once")


def parse_group_result(output):
    lines = [line for line in output.splitlines() if line.startswith(GROUP_MARKER)]
    if len(lines) != 1:
        raise ValueError("Missing or ambiguous Python group result")
    return strict_json(lines[0][len(GROUP_MARKER):])


def reconcile_groups(values, plan):
    if [v["group"] for v in values] != list(GROUPS):
        raise ValueError("Not every required Python group completed")
    require_ids([name for value in values for name in value["started_ids"]], all_ids(plan))
    require_ids([name for value in values for name in value["succeeded_ids"]], all_ids(plan))
    return {key: sum(value["counts"][key] for value in values) for key in COUNT_KEYS}


def canonicalize_temporary_root():
    # Hosted Windows TEMP can use an 8.3 alias. Production resolves paths; give
    # fixtures the same canonical parent without weakening any path assertions.
    if sys.platform == "win32":
        tempfile.tempdir = str(Path(tempfile.gettempdir()).resolve())


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--group", choices=GROUPS)
    parser.add_argument("--invocation")
    args = parser.parse_args(argv)
    if (bool(args.group) != bool(args.invocation) or args.invocation is not None
            and not re.fullmatch(r"[0-9a-f]{32}", args.invocation)):
        parser.error("A group requires a fresh invocation identity")
    canonicalize_temporary_root()
    group, invocation = args.group or "all", args.invocation or uuid.uuid4().hex
    try:
        mapping, plan, identity = source_contract()
        loader = unittest.TestLoader()
        tests = list(flatten(loader.discover(str(ROOT / "tests"))))
        validate_discovered(tests, mapping, plan, ROOT, loader.errors)
        selected_ids = set(all_ids(plan) if group == "all" else plan[group])
        # Filter actual discovered objects: preserve native ordering and class fixtures.
        result = run_selected([test for test in tests if test.id() in selected_ids])
        after_mapping, after_plan, after_identity = source_contract()
        if (after_mapping, after_plan, after_identity) != (mapping, plan, identity):
            raise ValueError("Python source contract changed during execution")
        result.update(schema_version=1, group=group, invocation=invocation,
                      identity=identity, discovered_ids=[test.id() for test in tests])
        print((GROUP_MARKER if args.group else "EDB_UNITTEST_RESULT=") +
              json.dumps(result if args.group else result["counts"]), flush=True)
        validate_group_result(result, group, invocation, plan, identity)
        return 0
    except (OSError, ValueError, TypeError, KeyError, subprocess.SubprocessError) as error:
        print("FAIL: Python inventory/execution/source contract (" + type(error).__name__ + ").", file=sys.stderr)
        return 1
    finally:
        from git_fixtures import close_readers
        close_readers()


if __name__ == "__main__":
    raise SystemExit(main())
