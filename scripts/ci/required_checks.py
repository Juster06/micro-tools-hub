"""Aggregate real Actions job results; skipped/cancelled/missing jobs never pass."""
import json
import os


def passed(results):
    return all(results.get(name) == "success" for name in ("PYTHON_RESULT", "NODE_RESULT", "BROWSER_RESULT"))


def main():
    results = {name: os.environ.get(name, "missing") for name in ("PYTHON_RESULT", "NODE_RESULT", "BROWSER_RESULT")}
    success = passed(results)
    print(json.dumps({"status": "PASS" if success else "FAIL", "required_jobs": results}))
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as output:
            output.write("## Required functional checks: " + ("PASS" if success else "FAIL") + "\n\n")
            for name, result in results.items():
                output.write(f"- {name}: {result}\n")
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
