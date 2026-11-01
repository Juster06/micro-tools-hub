"""Verify both templates with temporary neutral fixtures, never a real utility."""
import argparse
import json
from pathlib import Path
import tempfile

import tracking as tr
from test_tool import run_tests
from tool_framework import ROOT, create_tool, local_path


def fixture_entry(tid, rank, category):
    return {"id": tid, "name": "Framework " + tid, "category": category, "description": "Neutral test fixture, not a website utility.", "directory_path": tid, "status": "READY", "priority": "P1", "implementation_complexity": "S", "dependencies": [], "required_features": ["Fixture behavior only"], "testing_status": "NOT_STARTED", "last_verification_date": None, "notes": "Temporary harness verification", "sequence_rank": rank, "related_tools": [], "verification": None}


def browser_cases():
    def set_(value):
        return {"action": "set", "selector": "#toolInput", "value": value}
    def click(selector):
        return {"action": "click", "selector": selector}
    def expect(selector, prop, value=None, **other):
        return {"action": "expect", "selector": selector, "property": prop, **(other or {"equals": value})}
    payload = '<img src=x onerror=alert(1)> café 😀\nnext'
    return [
        {"id": "empty-input-error-and-focus", "steps": [click("#runBtn"), expect("#toolError", "textContent", includes="Enter input"), expect("#copyBtn", "disabled", True), click("#clearBtn"), expect("$page", "activeId", "toolInput")]},
        {"id": "actual-output-safety-copy-download-clear", "steps": [set_(payload), click("#runBtn"), expect("#toolOutput", "value", "Result: " + payload), expect("#toolOutput img", "exists", False), click("#copyBtn"), expect("$clipboard", "value", "Result: " + payload), click("#downloadBtn"), expect("$downloads", "count", 1), expect("$downloads", "text", "Result: " + payload), click("#clearBtn"), expect("#toolInput", "value", ""), expect("#toolOutput", "value", ""), expect("#copyBtn", "disabled", True)]},
        {"id": "actual-error-path", "steps": [set_("invalid"), click("#runBtn"), expect("#toolError", "textContent", "Fixture rejected"), expect("#toolOutput", "value", "")]},
        {"id": "input-change-invalidates-old-result", "steps": [set_("first"), click("#runBtn"), expect("#toolOutput", "value", "Result: first"), set_("second"), expect("#toolOutput", "value", ""), expect("#copyBtn", "disabled", True), click("#runBtn"), expect("#toolOutput", "value", "Result: second")]},
        {"id": "clipboard-failure-not-success", "steps": [set_("clipboard"), click("#runBtn"), expect("#toolOutput", "value", "Result: clipboard"), {"action": "clipboard", "mode": "failure"}, click("#copyBtn"), expect("#toolStatus", "textContent", includes="Automatic copy unavailable"), expect("#toolOutput", "selectionStart", 0), expect("#toolOutput", "selectionEnd", len("Result: clipboard"))]},
        {"id": "narrow-layout-and-keyboard-clear", "width": 375, "steps": [set_("keyboard"), {"action": "focus", "selector": "#clearBtn"}, {"action": "key", "key": "Enter"}, expect("#toolInput", "value", ""), expect("$page", "activeId", "toolInput"), expect("$page", "overflow", False)]},
    ]


def verify(browser=None):
    results = []
    with tempfile.TemporaryDirectory(prefix="edb-template-verification-") as temporary:
        root = Path(temporary)
        value = {"schema_version": 1, "updated_on": "2026-10-31", "project": {"name": "Template fixtures", "website": "https://example.invalid/", "repository": "https://example.invalid/repo"}, "status_definitions": {s: s for s in tr.STATUSES}, "categories": [{"id": "text", "name": "Text"}, {"id": "data", "name": "Data"}], "milestones": [25, 50, 100], "tools": [fixture_entry("text-fixture", 1, "text"), fixture_entry("structured-fixture", 2, "data")], "proposal_resolutions": []}
        (root / "TOOL_REGISTRY.json").write_text(json.dumps(value), encoding="utf-8")
        (root / "index.html").write_text("<!doctype html><title>Fixture hub</title>", encoding="utf-8")
        for template in ("text", "structured"):
            tid = template + "-fixture"
            created = create_tool(root, tid, template)
            directory = root / created["workspace"]
            source = directory / tid / "index.html"
            html = source.read_text(encoding="utf-8").replace("isScaffold: true", "isScaffold: false").replace("throw new Error('Not implemented — replace this placeholder with the actual tool logic.');", "if (input === 'invalid') throw new Error('Fixture rejected'); return 'Result: ' + input;")
            source.write_text(html, encoding="utf-8")
            logic = [{"id": "normal", "input": "hello", "expected": "Result: hello"}, {"id": "unicode-lines", "input": "café 😀\nnext", "expected": "Result: café 😀\nnext"}, {"id": "invalid", "input": "invalid", "error": "Fixture rejected"}]
            for layer, cases in (("logic", logic), ("browser", browser_cases())):
                (directory / "tests" / (layer + ".cases.json")).write_text(json.dumps({"schema_version": 1, "cases": cases}), encoding="utf-8")
            results.append({"template": template, **run_tests(root, tid, browser=browser, write_report=False)})
    return {"schema_version": 1, "kind": "TEMPLATE_FRAMEWORK_TEST_ONLY", "status": "PASS" if all(r["status"] == "PASS" for r in results) else "FAIL", "results": results, "scope": "Temporary neutral fixtures only. No Case Converter or other registry utility is implemented."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--browser", type=Path)
    args = parser.parse_args()
    result = verify(args.browser)
    tr.atomic_write(local_path(ROOT, "reports/framework-template-tests.json"), json.dumps(result, indent=2, ensure_ascii=True) + "\n")
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
