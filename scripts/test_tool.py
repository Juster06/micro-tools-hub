"""Run independent structural, JavaScript and optional real-browser tool checks."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import sys

import tracking as tr
from tool_framework import ROOT, FrameworkError, report_path, structural_check, suite_spec


def run_tests(root, tool_id, layers=("structural", "logic", "browser"), location="auto", browser=None, write_report=True):
    root = Path(root).resolve()
    spec = suite_spec(root, tool_id, location)
    result = {"schema_version": 1, "tool_id": tool_id, "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "input_hash": spec["input_hash"], "source_sha256": spec["source_sha256"], "workspace": spec["location"], "is_scaffold": None, "layers": {}}
    if "structural" in layers:
        result["layers"]["structural"] = structural_check(root, tool_id, location)
    if any(layer in layers for layer in ("logic", "browser")):
        executable = shutil.which("node")
        if executable:
            payload = {**spec, "layers": list(layers), "browser": str(browser) if browser else None}
            try:
                worker = subprocess.run([executable, str(ROOT / "scripts/tool-tests/runner.mjs")], input=json.dumps(payload), capture_output=True, text=True, encoding="utf-8", timeout=120, creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0)
                evidence = json.loads(worker.stdout)
                if worker.returncode or evidence.get("error"):
                    raise ValueError("Worker failure")
                result["is_scaffold"] = evidence["is_scaffold"]
                result["layers"].update(evidence["layers"])
            except (OSError, subprocess.SubprocessError, ValueError, KeyError):
                result["layers"]["worker"] = {"status": "UNKNOWN", "reason": "JavaScript/browser worker unavailable or failed; no pass is claimed."}
        else:
            result["layers"]["worker"] = {"status": "NOT RUN", "reason": "Node 22.4+ is required for JavaScript/browser checks."}
    # Every layer is explicit, including omitted/unavailable scopes.
    for layer in ("structural", "logic", "browser"):
        result["layers"].setdefault(layer, {"status": "NOT RUN", "passed": 0, "failed": 0, "assertions": 0})
    states = [item["status"] for item in result["layers"].values()]
    result["status"] = "FAIL" if "FAIL" in states else "UNKNOWN" if "UNKNOWN" in states else "PASS" if all(state == "PASS" for state in states) and result["is_scaffold"] is False else "NOT RUN" if result["is_scaffold"] is True else "PARTIAL"
    if suite_spec(root, tool_id, location)["input_hash"] != spec["input_hash"]:
        result["status"] = "STALE"
    if write_report:
        tr.atomic_write(report_path(root, tool_id), json.dumps(result, indent=2, ensure_ascii=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--id", required=True)
    parser.add_argument("--workspace", choices=("auto", "staging", "canonical"), default="auto")
    parser.add_argument("--layers", default="structural,logic,browser")
    parser.add_argument("--browser", type=Path)
    parser.add_argument("--no-report", action="store_true")
    args = parser.parse_args()
    try:
        layers = args.layers.split(",")
        if not layers or not set(layers) <= {"structural", "logic", "browser"}:
            raise FrameworkError("Layers must be structural,logic,browser or a comma-separated subset.")
        result = run_tests(args.root, args.id, layers, args.workspace, args.browser, not args.no_report)
        print(json.dumps(result, indent=2, ensure_ascii=True))
        if result["status"] in {"FAIL", "UNKNOWN", "STALE"}:
            return 1
        # A scoped PASS may be useful, but never implies omitted layers passed.
        return 0 if all(result["layers"][layer]["status"] == "PASS" for layer in layers) and result["is_scaffold"] is not True else 2
    except (FrameworkError, OSError, ValueError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
