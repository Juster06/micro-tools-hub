"""Safe registry-driven scaffolding and quality checks; never change lifecycle status."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import hashlib
from html import escape
import json
import os
from pathlib import Path
import re
import subprocess

import tracking as tr

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"
VERSION = 1
RESERVED = {"con", "prn", "aux", "nul", *(f"com{i}" for i in range(1, 10)), *(f"lpt{i}" for i in range(1, 10))}
INPUT_IDS = ("toolInput", "runBtn", "clearBtn", "toolOutput", "copyBtn", "downloadBtn", "toolError", "toolStatus")


class FrameworkError(ValueError):
    pass


def safe_slug(value):
    if not isinstance(value, str) or len(value) > 80 or not tr.SLUG.fullmatch(value) or value.casefold() in RESERVED:
        raise FrameworkError("Tool ID and directory must be safe lowercase slugs, excluding Windows device names.")
    return value


def local_path(root, relative):
    """Reject traversal and every symlink/junction component, even inside root."""
    root = Path(root).resolve()
    try:
        result = tr.safe_path(root, relative)
    except ValueError as exc:
        raise FrameworkError("Unsafe project-relative path.") from exc
    current = root
    for part in relative.split("/"):
        current = current / part
        if current.is_symlink() or (current.exists() and current.resolve() != current.absolute()):
            raise FrameworkError("Symlink/junction paths are not supported for framework writes or inputs.")
    return result


def registry(root):
    try:
        result, value = tr.validate_registry(Path(root).resolve())
    except (ValueError, TypeError, KeyError, AttributeError) as exc:
        raise FrameworkError("Malformed registry fields; run validate_registry.py.") from exc
    if result["errors"]:
        raise FrameworkError("Registry validation failed: " + "; ".join(dict.fromkeys(e["code"] for e in result["errors"])))
    return value


def lookup(root, tool_id):
    safe_slug(tool_id)
    value = registry(root)
    tool = next((t for t in value["tools"] if t["id"] == tool_id), None)
    if tool is None:
        raise FrameworkError("Unknown registry tool ID.")
    safe_slug(tool["directory_path"])
    return value, tool


def order_key(tool):
    return (tool["sequence_rank"] is None, tool["sequence_rank"] or 0, tool["priority"], tool["id"])


def unmet(tool, value):
    by_id = {t["id"]: t for t in value["tools"]}
    return [dep for dep in tr.dependencies(tool) if by_id[dep]["status"] not in {"TESTED", "RELEASED"}]


def template_choice(tool):
    selected = "text" if tool["category"] in {"text", "social"} else "structured"
    browser_specific = any("cryptograph" in dependency.casefold() for dependency in tool["dependencies"])
    special = browser_specific or tool["category"] in {"pdf", "image", "security", "conversion", "entertainment"} or tool["implementation_complexity"] in {"M", "L", "XL"}
    return selected, special


def bundle_relative(tool):
    return f"development/scaffolds/{tool['id']}"


def render_tokens(template, values):
    def substitute(match):
        if match[1] not in values:
            raise FrameworkError("Unknown template token: " + match[1])
        return values[match[1]]
    return re.sub(r"@@([A-Z_]+)@@", substitute, template)


def scaffold_files(value, tool, template=None):
    recommended, special = template_choice(tool)
    template = template or recommended
    if template not in {"text", "structured"}:
        raise FrameworkError("Template must be text or structured.")
    manifest = {"schema_version": VERSION, "tool_id": tool["id"], "canonical_path": tool["directory_path"] + "/index.html", "template": template, "requires_specialized_implementation": special, "purpose": "Development scaffold; no lifecycle or publication claim."}
    metadata = json.dumps({"id": tool["id"], "name": tool["name"], "category": tool["category"]}, ensure_ascii=True).replace("<", "\\u003c")
    values = {"NAME": escape(tool["name"], quote=True), "DESCRIPTION": escape(tool["description"], quote=True), "ID": tool["id"], "CATEGORY": escape(next(c["name"] for c in value["categories"] if c["id"] == tool["category"])), "METADATA": metadata,
              "INPUT": (TEMPLATES / (template + "-input.html")).read_text(encoding="utf-8"), "CSS": (TEMPLATES / "fragments/base.css").read_text(encoding="utf-8"), "UI": (TEMPLATES / "fragments/tool-ui.js").read_text(encoding="utf-8")}
    page = render_tokens((TEMPLATES / "tool-page.html").read_text(encoding="utf-8"), values)
    notes = "# " + tool["name"] + " — implementation checklist\n\nNot implemented. Do not publish or advance registry status from this scaffold.\n\nCanonical route: `" + manifest["canonical_path"] + "`\n\nRequired features:\n" + "\n".join("- " + f for f in tool["required_features"]) + "\n\nDependencies / decisions:\n" + "\n".join("- " + d for d in tool["dependencies"]) + "\n\nSpecialized implementation required: " + str(special) + ". Resolve limits, modes, invalid/empty input, keyboard/mobile behavior and scope before coding.\n\nImplement the inline edb-tool-logic script and replace isScaffold:true only when real behavior exists. Add nonempty logic/browser cases; empty suites are NOT RUN. See TOOL_DEVELOPMENT_GUIDE.md.\n"
    preview = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex"><title>Development preview</title></head><body><h1>Development preview — not a public tool</h1><p>This scaffold has no functionality yet.</p><a href="{tool["directory_path"]}/index.html">{escape(tool["name"])}</a><p><a href="../../../index.html">Open the actual hub</a></p></body></html>\n'
    return {"index.html": preview, manifest["canonical_path"]: page, "manifest.json": json.dumps(manifest, indent=2) + "\n", "tests/logic.cases.json": json.dumps({"schema_version": 1, "cases": [], "instructions": "Add input/options/expected or error cases for actual logic. Empty means NOT RUN."}, indent=2) + "\n", "tests/browser.cases.json": json.dumps({"schema_version": 1, "cases": [], "instructions": "Add isolated browser cases with steps and expectations; see TOOL_DEVELOPMENT_GUIDE.md."}, indent=2) + "\n", "IMPLEMENTATION.md": notes}


def create_tool(root, tool_id, template=None, dry_run=False):
    root = Path(root).resolve()
    value, tool = lookup(root, tool_id)
    if tool["status"] != "READY":
        raise FrameworkError("Only READY entries may be scaffolded; released/blocked/active tools are protected.")
    if unmet(tool, value):
        raise FrameworkError("Unmet tool dependencies: " + ", ".join(unmet(tool, value)))
    if local_path(root, tool["directory_path"]).exists():
        raise FrameworkError("Canonical directory already exists; it will not be overwritten.")
    relative = bundle_relative(tool)
    target = local_path(root, relative)
    if target.exists():
        raise FrameworkError("Scaffold already exists; it will not be overwritten.")
    files = scaffold_files(value, tool, template)
    result = {"tool_id": tool_id, "canonical_path": tool["directory_path"] + "/index.html", "workspace": relative, "dry_run": dry_run, "files": [relative + "/" + f for f in files], "registry_status": tool["status"], "notice": "Scaffold only. Registry, homepage and public routes remain unchanged."}
    if dry_run:
        return result
    created, directories = [], []
    try:
        for directory in (target.parent.parent, target.parent, target):
            if not directory.exists():
                directory.mkdir()
                directories.append(directory)
            elif directory == target:
                raise FileExistsError("Concurrent scaffold creation")
        for relative_file, content in files.items():
            path = local_path(root, relative + "/" + relative_file)
            for directory in list(reversed(list(path.parent.parents))) + [path.parent]:
                if directory.is_relative_to(target) and not directory.exists():
                    directory.mkdir()
                    directories.append(directory)
            with path.open("x", encoding="utf-8", newline="\n") as handle:
                created.append(path)
                handle.write(content)
    except Exception as exc:
        # Only paths created exclusively by this invocation are removed.
        for path in reversed(created):
            path.unlink(missing_ok=True)
        for directory in reversed(directories):
            try:
                directory.rmdir()
            except OSError:
                pass  # Preserve any files another process added.
        raise FrameworkError("Scaffold creation failed; existing files were preserved.") from exc
    return result


def plan_batch(root, count=10):
    if type(count) is not int or not 1 <= count <= 1000:
        raise FrameworkError("Count must be between 1 and 1000.")
    root, value = Path(root).resolve(), registry(root)
    candidates, excluded = [], []
    for tool in sorted(value["tools"], key=order_key):
        dependencies = unmet(tool, value)
        if tool["status"] == "RELEASED":
            excluded.append({"tool_id": tool["id"], "classification": "Already released"})
        elif tool["status"] == "BLOCKED":
            excluded.append({"tool_id": tool["id"], "classification": "Blocked", "reason": tool["notes"]})
        elif tool["status"] == "READY":
            template, special = template_choice(tool)
            existing = local_path(root, bundle_relative(tool)).exists() or local_path(root, tool["directory_path"]).exists()
            classification = "Requires dependency" if dependencies else "Existing work — review first" if existing else "Requires specialized implementation" if special else "Ready for scaffolding"
            entry = {"tool_id": tool["id"], "name": tool["name"], "classification": classification, "priority": tool["priority"], "sequence_rank": tool["sequence_rank"], "complexity": tool.get("implementation_complexity") or "unknown", "dependencies": tool["dependencies"], "unmet_tool_dependencies": dependencies, "template": template, "estimated_files": [bundle_relative(tool) + "/" + p for p in scaffold_files(value, tool)], "canonical_path": tool["directory_path"] + "/index.html"}
            (excluded if dependencies or existing else candidates).append(entry)
    return {"schema_version": 1, "kind": "PROPOSAL_ONLY", "count_requested": count, "selected": candidates[:count], "excluded": excluded, "notice": "No files generated, no implementation, lifecycle changes or publication. No time estimates."}


def workspace(root, tool_id, location="auto"):
    root = Path(root).resolve()
    value, tool = lookup(root, tool_id)
    canonical = local_path(root, tool["directory_path"] + "/index.html")
    if location == "auto":
        location = "canonical" if canonical.is_file() else "staging"
    if location not in {"canonical", "staging"}:
        raise FrameworkError("Workspace must be auto, canonical or staging.")
    base = local_path(root, bundle_relative(tool)) if location == "staging" else root
    source = local_path(root, (bundle_relative(tool) + "/" if location == "staging" else "") + tool["directory_path"] + "/index.html")
    tests = local_path(root, bundle_relative(tool) + "/tests" if location == "staging" else "tests/tools/" + tool_id)
    manifest = local_path(root, bundle_relative(tool) + "/manifest.json" if location == "staging" else "tests/tools/" + tool_id + "/manifest.json")
    return value, tool, {"base": base, "source": source, "tests": tests, "manifest": manifest, "location": location}


def strict_json(path):
    from dashboard.data import read_json
    return read_json(path)


class Structure(tr.Page):
    def __init__(self, content):
        self.elements, self.scripts = [], []
        super().__init__(content)

    def handle_starttag(self, tag, attrs):
        super().handle_starttag(tag, attrs)
        attrs = dict(attrs)
        self.elements.append((tag, attrs))
        if tag == "script":
            self.scripts.append(attrs)


def structural_check(root, tool_id, location="auto"):
    value, tool, paths = workspace(root, tool_id, location)
    errors, warnings = [], []
    try:
        content = tr.read_text(paths["source"])
        page = Structure(content)
        if not page.doctype or any(page.tags[tag] != 1 or page.closed_tags[tag] != 1 for tag in ("html", "head", "title", "body")):
            errors.append("Expected HTML5 document with one html/head/title/body.")
        if not "".join(page.title).strip():
            errors.append("Missing usable title.")
        if any(count > 1 for count in page.ids.values()):
            errors.append("Duplicate HTML IDs.")
        links = [e[1] for e in page.elements if e[0] == "a"]
        if not any(link.get("href") == "../index.html" and "hidden" not in link for link in links):
            errors.append("Missing explicit ../index.html Back to Hub link.")
        for element, attrs in page.elements:
            for attr in ("src", "href"):
                href = attrs.get(attr)
                if not href:
                    continue
                split = tr.urlsplit(href)
                if split.scheme in {"javascript", "vbscript"}:
                    errors.append("Executable resource URL is forbidden.")
                    continue
                if split.scheme or split.netloc:
                    continue
                target = tr.link_target(paths["base"], paths["source"].relative_to(paths["base"]).as_posix(), href)
                if target and not target[0].is_file():
                    errors.append("Broken internal resource/link.")
                elif target and target[1]:
                    destination = page if target[0] == paths["source"] else tr.Page(tr.read_text(target[0]))
                    if target[1] not in destination.ids:
                        errors.append("Missing internal anchor ID.")
        expected = tool.get("expected_interface_ids", [])
        manifest = strict_json(paths["manifest"]) if paths["manifest"].exists() else None
        if manifest is not None:
            if not isinstance(manifest, dict) or manifest.get("schema_version") != VERSION or manifest.get("tool_id") != tool_id or manifest.get("canonical_path") != tool["directory_path"] + "/index.html":
                errors.append("Framework manifest identity/route mismatch.")
            expected = list(INPUT_IDS)
            metadata = [a for tag, a in page.elements if tag == "meta"]
            if not all(any(a.get("name") == name and a.get("content") for a in metadata) for name in ("description", "viewport")):
                errors.append("Missing description or viewport metadata.")
            if not any(a.get("id") == "edb-tool-logic" and not a.get("src") for a in page.scripts):
                errors.append("Missing inline edb-tool-logic adapter.")
        elif paths["location"] == "staging":
            errors.append("Missing framework manifest.")
        else:
            warnings.append("Legacy page: only existing structural/interface contract applies.")
        if any(key not in page.ids for key in expected):
            errors.append("Missing expected interface elements.")
    except (OSError, UnicodeError, ValueError, TypeError, RecursionError):
        errors.append("Unreadable/malformed source, manifest or unsafe internal path.")
    return {"status": "FAIL" if errors else "PASS", "errors": list(dict.fromkeys(errors)), "warnings": warnings, "scope": "STRUCTURAL_ONLY"}


def suite_spec(root, tool_id, location="auto"):
    root = Path(root).resolve()
    value, tool, paths = workspace(root, tool_id, location)
    files = [paths["source"]]
    cases = {}
    for layer in ("logic", "browser"):
        relative = paths["tests"].relative_to(root).as_posix() + "/" + layer + ".cases.json"
        path = local_path(root, relative)
        if not path.exists():
            cases[layer] = []
            continue
        payload = strict_json(path)
        if not isinstance(payload, dict) or payload.get("schema_version") != 1 or not isinstance(payload.get("cases"), list):
            raise FrameworkError("Invalid test-case schema.")
        case_ids = set()
        for case in payload["cases"]:
            if not isinstance(case, dict) or not isinstance(case.get("id"), str) or not case["id"].strip() or case["id"] in case_ids:
                raise FrameworkError("Test cases need unique nonempty IDs.")
            case_ids.add(case["id"])
        cases[layer] = payload["cases"]
        files.append(path)
    if paths["manifest"].exists():
        files.append(paths["manifest"])
    digest = hashlib.sha256()
    for path in sorted(files):
        digest.update(path.relative_to(root).as_posix().encode() + b"\0" + path.read_bytes())
    digest.update(json.dumps(tool, sort_keys=True).encode())
    for relative in ("tool_framework.py", "test_tool.py", "tool-tests/runner.mjs", "tool-tests/browser.mjs"):
        path = ROOT / "scripts" / relative
        if path.exists():
            digest.update(relative.encode() + path.read_bytes())
    return {"tool_id": tool_id, "source": str(paths["source"]), "source_sha256": tr.normalized_hash(tr.read_text(paths["source"])), "input_hash": digest.hexdigest(), "cases": cases, "location": paths["location"]}


def report_path(root, tool_id):
    return local_path(root, "reports/tool-tests/" + safe_slug(tool_id) + ".json")


def functional_gate(root, tool_id):
    spec = suite_spec(root, tool_id, "canonical")
    try:
        evidence = strict_json(report_path(root, tool_id))
        generated = datetime.fromisoformat(evidence["generated_at"])
        age = datetime.now(timezone.utc) - generated
        if not (evidence["schema_version"] == 1 and evidence["tool_id"] == tool_id and evidence["input_hash"] == spec["input_hash"]
                and timedelta(0) <= age <= timedelta(hours=24)
                and evidence["status"] == "PASS" and evidence["is_scaffold"] is False
                and evidence["layers"]["structural"]["status"] == "PASS"):
            raise ValueError("Report identity, freshness or completion gate failed")
        for layer in ("logic", "browser"):
            result = evidence["layers"][layer]
            if not (result["status"] == "PASS" and result["passed"] > 0 and result["failed"] == 0):
                raise ValueError("Nonempty passing functional layers required")
    except (OSError, UnicodeError, ValueError, TypeError, KeyError, RecursionError) as exc:
        raise FrameworkError("Fresh passing logic and browser evidence for canonical source is required.") from exc
    return spec
