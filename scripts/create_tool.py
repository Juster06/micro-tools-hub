"""Generate an ignored, unpublished scaffold from a READY registry entry."""
import argparse
import json
from pathlib import Path
import sys

from tool_framework import ROOT, FrameworkError, create_tool


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--id", required=True)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--template", choices=("text", "structured"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        print(json.dumps(create_tool(args.root, args.id, args.template, args.dry_run), indent=2, ensure_ascii=True))
    except (FrameworkError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
