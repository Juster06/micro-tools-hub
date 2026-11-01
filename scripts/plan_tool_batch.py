"""Propose ordered READY work without creating or publishing any utility."""
import argparse
import json
from pathlib import Path
import sys

import tracking as tr
from tool_framework import ROOT, FrameworkError, local_path, plan_batch


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--output", help="Optional ignored reports/batch-plans/... JSON path; otherwise stdout only.")
    args = parser.parse_args()
    try:
        result = json.dumps(plan_batch(args.root, args.count), indent=2, ensure_ascii=True) + "\n"
        if args.output:
            if not args.output.startswith("reports/batch-plans/") or not args.output.endswith(".json"):
                raise FrameworkError("Plan output must be under reports/batch-plans/ and end in .json; other report schemas are protected.")
            tr.atomic_write(local_path(args.root, args.output), result)
        print(result, end="")
    except (FrameworkError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
