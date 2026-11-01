"""Produce a validated homepage patch proposal; never apply it automatically."""
import argparse
import json
from pathlib import Path
import sys

import tracking as tr
from tool_framework import ROOT, FrameworkError, local_path
from tool_homepage import integration_proposal


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--id", required=True)
    args = parser.parse_args()
    try:
        root = args.root.resolve()
        proposal = integration_proposal(root, args.id)
        if proposal["patch"]:
            relative = "reports/integration/" + args.id + ".patch"
            tr.atomic_write(local_path(root, relative), proposal.pop("patch"))
            proposal["patch_path"] = relative
        print(json.dumps(proposal, indent=2, ensure_ascii=True))
    except (FrameworkError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
