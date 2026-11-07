"""Prepare one implemented tool's canonical before recording verification hashes.

Does not remove noindex, change registry status, update the sitemap or publish.
Released pages use the separately reviewed generate_sitemap.py --sync-canonicals
workflow; this command cannot silently invalidate existing release evidence.
"""
import argparse
import json
from pathlib import Path
import sys

import seo
from tool_framework import ROOT, FrameworkError, local_path, lookup


def prepare(root, tool_id):
    root = Path(root).resolve()
    _, tool = lookup(root, tool_id)
    if tool["status"] not in {"IN_PROGRESS", "IMPLEMENTED"}:
        raise ValueError("Prepare SEO only while IN_PROGRESS or IMPLEMENTED, before test/publication evidence is recorded.")
    relative = tool["directory_path"] + "/index.html"
    target = local_path(root, relative)
    original = target.read_bytes()
    source = original.decode("utf-8")
    url = "https://everydaydigitalbox.com/" + relative
    updated = seo.annotate_html(source, url).encode("utf-8")
    if updated != original:
        target.write_bytes(updated)
    return {"path": relative, "canonical_url": url, "changed": updated != original,
            "notice": "Local metadata preparation only; run tests before recording source hashes. No status change or publication."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--id", required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(prepare(args.root, args.id), indent=2))
        return 0
    except (OSError, UnicodeError, ValueError, FrameworkError) as exc:
        print("ERROR: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
