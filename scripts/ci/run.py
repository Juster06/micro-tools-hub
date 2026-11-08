"""Fail-closed CI partitions for existing tests; no release or deployment actions."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
MAP = Path(__file__).with_name("coverage.json")


def coverage(root=ROOT, mapping=None):
    value = json.loads((mapping or MAP).read_text(encoding="utf-8"))
    registry = json.loads((root / "TOOL_REGISTRY.json").read_text(encoding="utf-8"))
    required = {t["id"] for t in registry["tools"] if t["status"] in {"IMPLEMENTED", "TESTED", "RELEASED"}}
    if value.get("schema_version") != 1 or set(value["tools"]) != required:
        raise ValueError("Coverage map does not match implemented registry tools")
    mapped = value["python_files"] + value["node_files"] + value["browser_files"]
    actual = {p.relative_to(root).as_posix() for pattern in
              ("tests/**/test_*.py", "scripts/**/*.test.mjs", "tests/tools/**/*.test.mjs")
              for p in root.glob(pattern) if "node_modules" not in p.parts}
    if not mapped or len(mapped) != len(set(mapped)) or set(mapped) != actual:
        raise ValueError("Missing, duplicate or unmapped executable test suite")
    if not all(value[key] for key in ("python_files", "node_files", "browser_files")):
        raise ValueError("Empty required suite selection")
    for name in mapped:
        path = root / name
        if not path.is_file() or not path.read_text(encoding="utf-8").strip():
            raise ValueError("Missing or empty required test file")
    expected_json = set()
    for tid, item in value["tools"].items():
        if item["structural_job"] != "python-project" or item["logic_job"] not in {"node-regression", None} or item["browser_job"] != "browser-tests":
            raise ValueError("Unknown tool job assignment")
        for layer in ("logic", "browser"):
            path = root / "tests/tools" / tid / (layer + ".cases.json")
            if layer == "logic" and item["logic_job"] is None:
                if path.exists() or not item.get("unavailable_reason"):
                    raise ValueError("Undeclared logic scope must be reviewed")
                continue
            expected_json.add(path.relative_to(root).as_posix())
            data = json.loads(path.read_text(encoding="utf-8"))
            if data.get("schema_version") != 1 or not isinstance(data.get("cases"), list) or not data["cases"]:
                raise ValueError("Missing or empty mandatory fixture cases")
            if layer == "browser" and any(not c.get("steps") or not any(s.get("action") == "expect" for s in c["steps"]) for c in data["cases"]):
                raise ValueError("Browser fixture must assert behavior")
    actual_json = {p.relative_to(root).as_posix() for p in (root / "tests/tools").rglob("*.cases.json")}
    if actual_json != expected_json:
        raise ValueError("Unmapped JSON fixture suite")
    return value


def node_counts(output, require_pass=True):
    result = {}
    for key in ("tests", "pass", "fail", "cancelled", "skipped", "todo"):
        matches = re.findall(r"^# " + key + r" (\d+)\s*$", output, re.MULTILINE)
        if len(matches) != 1:
            raise ValueError("Missing or ambiguous Node TAP summary")
        result[key] = int(matches[0])
    if require_pass and (result["tests"] <= 0 or result["tests"] != result["pass"] or any(result[k] for k in ("fail", "cancelled", "skipped", "todo"))):
        raise ValueError("Node suite failed, empty, cancelled, skipped or todo")
    return {"tests": result["tests"], "passed": result["pass"], "failed": result["fail"],
            **{k: result[k] for k in ("cancelled", "skipped", "todo")}}


def layer_counts(value, layer):
    item = value["layers"][layer]
    if item["status"] != "PASS" or item.get("failed", 0) or (layer != "structural" and item.get("passed", 0) <= 0):
        raise ValueError("Mandatory requested layer did not execute and pass")
    if value.get("is_scaffold") is True:
        raise ValueError("Scaffold cannot satisfy a required CI layer")
    return {k: item.get(k, 0) for k in ("passed", "failed", "assertions")}


def command(args, timeout, cwd=ROOT, environment=None):
    env = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8", "WEBUTILS_PYTHON": sys.executable}
    env.update(environment or {})
    options = {"start_new_session": True} if os.name != "nt" else {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP}
    child = subprocess.Popen(args, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             text=True, encoding="utf-8", errors="replace", **options)
    try:
        output, _ = child.communicate(timeout=timeout)
        return child.returncode, output
    except subprocess.TimeoutExpired:
        # Kill only this invocation's process tree, including a stuck browser worker.
        if os.name == "nt":
            subprocess.run(["taskkill", "/PID", str(child.pid), "/T", "/F"], capture_output=True, timeout=15)
        else:
            os.killpg(child.pid, signal.SIGKILL)
        child.kill()
        output, _ = child.communicate(timeout=15)
        return 124, output + "\nCI command timed out; required scope FAILED.\n"


def whitespace_base(root=ROOT):
    base = os.environ.get("EDB_CI_DIFF_BASE", "")
    if base and re.fullmatch(r"[0-9a-f]{40}", base) and base != "0" * 40:
        return base
    if base:
        raise ValueError("Missing/invalid Git comparison parent; inspect the event")
    # Local feature/manual invocation; full-history checkout is required by CI.
    candidate = subprocess.check_output(["git", "rev-parse", "origin/main"], cwd=root, text=True).strip()
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    return "HEAD^" if candidate == head else candidate


def run(job):
    directory = ROOT / "reports/ci" / job
    directory.mkdir(parents=True, exist_ok=True)
    summary = {"schema_version": 1, "job": job, "execution": "github-hosted" if os.environ.get("GITHUB_ACTIONS") == "true" else "local",
               "generated_at": datetime.now(timezone.utc).isoformat(), "status": "FAIL", "scopes": [], "unavailable_scopes": []}
    def execute(scope, args, kind="exit", layer=None, timeout=180, minimum=0):
        print("RUN " + scope, flush=True)
        entry = {"scope": scope, "status": "FAIL", "exit_code": None}
        summary["scopes"].append(entry)
        code, output = command(args, timeout)
        (directory / (scope + ".log")).write_text(output, encoding="utf-8")
        entry["exit_code"] = code
        print(output, end="" if output.endswith("\n") else "\n", flush=True)
        if kind == "node":
            entry.update(node_counts(output, require_pass=False))
            node_counts(output)
        elif kind == "python":
            lines = [s for s in output.splitlines() if s.startswith("EDB_UNITTEST_RESULT=")]
            if len(lines) != 1:
                raise ValueError("Missing Python executed-test summary")
            counts = json.loads(lines[0].split("=", 1)[1])
            entry.update(counts)
            if counts["tests"] <= 0 or counts["passed"] != counts["tests"]:
                raise ValueError("Python tests failed, empty or skipped")
        elif kind == "layer":
            result = json.loads(output)
            entry.update({k: result["layers"][layer].get(k, 0) for k in ("passed", "failed", "assertions")})
            entry["layer_status"] = result["layers"][layer]["status"]
            layer_counts(result, layer)
        elif kind == "validation":
            result = json.loads(output)
            entry.update(errors=len(result["errors"]), warnings=len(result["warnings"]))
            if result["status"] != "PASS" or entry["errors"] or entry["warnings"]:
                raise ValueError("Project validation is not a clean PASS")
        elif kind == "templates":
            result = json.loads(output)
            if result["status"] != "PASS" or {x["template"] for x in result["results"]} != {"text", "structured"}:
                raise ValueError("Both neutral templates must pass")
            for item in result["results"]:
                for requested in ("structural", "logic", "browser"):
                    layer_counts(item, requested)
            entry["passed"] = sum(x["layers"]["browser"]["passed"] for x in result["results"])
            entry["logic_passed"] = sum(x["layers"]["logic"]["passed"] for x in result["results"])
            entry["assertions"] = sum(x["layers"]["browser"]["assertions"] for x in result["results"])
        elif kind == "preflight":
            result = json.loads(output)
            if not result.get("browser") or result.get("status") != "PASS":
                raise ValueError("Chromium preflight did not complete")
            summary["browser"] = result["browser"]
        if code:
            raise ValueError("Required command failed: " + scope)
        if entry.get("tests", 0) < minimum:
            raise ValueError("Executed-test count fell below the reviewed coverage floor")
        entry["status"] = "PASS"
    try:
        value = coverage()
        summary["coverage"] = {"python_files": len(value["python_files"]), "node_files": len(value["node_files"]),
                               "browser_files": len(value["browser_files"]), "tools": len(value["tools"])}
        summary["unavailable_scopes"] = [{"tool": tid, "scope": "isolated-logic", "status": "NOT RUN", "reason": item["unavailable_reason"]}
            for tid, item in value["tools"].items() if item["logic_job"] is None]
        if job == "python-project":
            execute("css-source-approval", [sys.executable, "scripts/css_overlay.py", "--check"])
            execute("python-unittest", [sys.executable, "scripts/ci/unittest_runner.py"], "python", timeout=240, minimum=value["minimum_tests"][job])
            for scope, script in (("registry", "validate_registry.py"), ("source-audit-homepage", "check_project.py"), ("static-tools", "verify_tools.py")):
                execute(scope, [sys.executable, "scripts/" + script, "--json", "--no-report"], "validation")
            execute("technical-seo", [sys.executable, "scripts/validate_seo.py", "--json"], "validation")
            for tid in value["tools"]:
                execute(tid + "-structure", [sys.executable, "scripts/test_tool.py", "--id", tid, "--workspace", "canonical", "--layers", "structural", "--no-report"], "layer", "structural")
            execute("project-status", [sys.executable, "scripts/project_status.py", "--check-only", "--no-report", "--json"], "validation")
            execute("whitespace-working", ["git", "diff", "--check"])
            execute("whitespace-commits", ["git", "diff", "--check", whitespace_base(), "HEAD"])
        elif job == "node-regression":
            execute("homepage-build-freshness", [sys.executable, "scripts/build_homepage.py", "--check"])
            execute("css-build-freshness", ["node", "scripts/build_styles.mjs", "--check"])
            execute("node-logic", ["node", "--test", "--test-concurrency=1", "--test-reporter=tap", *value["node_files"]], "node", timeout=300, minimum=value["minimum_tests"][job])
            for tid, item in value["tools"].items():
                if item["logic_job"]:
                    execute(tid + "-logic", [sys.executable, "scripts/test_tool.py", "--id", tid, "--workspace", "canonical", "--layers", "logic", "--no-report"], "layer", "logic")
        elif job == "browser-tests":
            execute("browser-preflight", ["node", "scripts/ci/preflight.mjs"], "preflight")
            execute("node-browser", ["node", "--test", "--test-concurrency=1", "--test-reporter=tap", *value["browser_files"]], "node", timeout=900, minimum=value["minimum_tests"][job])
            for tid in value["tools"]:
                execute(tid + "-browser", [sys.executable, "scripts/test_tool.py", "--id", tid, "--workspace", "canonical", "--layers", "browser", "--no-report"], "layer", "browser")
            execute("neutral-templates", [sys.executable, "scripts/verify_tool_templates.py"], "templates")
        else:
            raise ValueError("Unknown required job")
        summary["status"] = "PASS"
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        # Do not publish exception text: it can contain private executable/root paths.
        summary["failure"] = "Required scope or coverage failed; inspect command logs."
        print("FAIL: required scope/coverage did not pass (" + type(exc).__name__ + ").", file=sys.stderr)
    finally:
        path = directory / "summary.json"
        path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        if os.environ.get("GITHUB_STEP_SUMMARY"):
            with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as output:
                output.write("## " + job + ": " + summary["status"] + "\n\n")
                output.write("| Executed scope | Result | Tests/cases passed |\n|---|---|---:|\n")
                for item in summary["scopes"]:
                    output.write(f"| {item['scope']} | {item['status']} | {item.get('passed', 'n/a')} |\n")
                output.write("\nFour specialist isolated-logic scopes are unavailable; required structure/browser checks are separate. Public/native release verification is not claimed.\n")
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("job", choices=("python-project", "node-regression", "browser-tests"))
    raise SystemExit(run(parser.parse_args().job))
