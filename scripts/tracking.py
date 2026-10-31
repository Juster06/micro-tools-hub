"""Shared, offline project tracking engine. No third-party modules or JavaScript execution."""
from __future__ import annotations

import argparse
from collections import Counter, deque
from datetime import date, datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unicodedata
from urllib.parse import unquote, urlsplit

DEFAULT_ROOT = Path(__file__).resolve().parent.parent
STATUSES = ("IDEA", "PLANNED", "READY", "IN_PROGRESS", "BLOCKED", "IMPLEMENTED", "TESTED", "RELEASED", "DEPRECATED")
IMPLEMENTED = {"IMPLEMENTED", "TESTED", "RELEASED"}
BACKLOG = {"IDEA", "PLANNED", "READY", "BLOCKED"}
REQUIRED_DOCS = ("AGENTS.md", "SESSION_HANDOFF.md", "PROJECT_MASTER_PLAN.md", "PROGRESS_TRACKER.md", "ROADMAP.md", "ARCHITECTURE.md", "DECISIONS.md", "CHANGELOG.md", "README.md")
REQUIRED_FIELDS = ("id", "name", "category", "description", "directory_path", "status", "priority", "implementation_complexity", "dependencies", "required_features", "testing_status", "last_verification_date", "notes", "sequence_rank", "related_tools", "verification")
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
REPORT_FILES = {"registry-validation": "registry-validation.json", "project-consistency": "project-consistency.json", "tool-verification": "tool-verification.json", "project-status": "project-status.json"}


def read_text(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        return handle.read()


def normalized(text):
    return text.replace("\r\n", "\n")


def normalized_hash(text):
    return hashlib.sha256(normalized(text).rstrip().encode("utf-8")).hexdigest()


def atomic_write(path, text):
    """Replace only on change; failure leaves the previous document intact."""
    path = Path(path)
    if path.exists() and read_text(path) == text:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="", dir=path.parent, prefix=".tracking-", suffix=".tmp", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(text)
        temporary.replace(path)
    finally:
        if temporary and temporary.exists():
            temporary.unlink()
    return True


def report(name):
    return {"schema_version": 1, "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "check_name": name, "status": "PASS", "counts": {}, "errors": [], "warnings": [], "information": [], "details": {}}


def issue(result, severity, code, message, **context):
    result[severity].append({"code": code, "message": message, **context})


def finish(result):
    result["status"] = "FAIL" if result["errors"] else "WARN" if result["warnings"] else "PASS"
    return result


def safe_path(root, relative):
    """Reject traversal, Windows drive paths and symlink escapes, on every OS."""
    if not isinstance(relative, str) or not relative or "\\" in relative or relative.startswith("/") or re.match(r"^[A-Za-z]:", relative):
        raise ValueError("unsafe relative path")
    if any(part in ("", ".", "..") for part in relative.split("/")):
        raise ValueError("unsafe relative path")
    target = (root / relative).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError("path escapes project")
    return target


def valid_date(value):
    try:
        return isinstance(value, str) and date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def valid_timestamp(value):
    try:
        return isinstance(value, str) and datetime.fromisoformat(value.replace("Z", "+00:00")).tzinfo is not None
    except ValueError:
        return False


def string_list(value, nonempty=False):
    return isinstance(value, list) and (bool(value) or not nonempty) and all(isinstance(item, str) and item.strip() for item in value)


def load_registry(root, result):
    try:
        # Reject duplicate JSON keys and non-standard NaN/Infinity constants.
        def pairs(items):
            obj = {}
            for key, value in items:
                if key in obj:
                    raise ValueError("duplicate JSON object key")
                obj[key] = value
            return obj
        def invalid_constant(_):
            raise ValueError("non-standard JSON numeric constant")
        value = json.loads(read_text(root / "TOOL_REGISTRY.json"), object_pairs_hook=pairs, parse_constant=invalid_constant)
        return value
    except json.JSONDecodeError as exc:
        issue(result, "errors", "INVALID_JSON", f"TOOL_REGISTRY.json: invalid JSON at line {exc.lineno}, column {exc.colno}.")
    except (ValueError, OSError, UnicodeError, RecursionError):
        issue(result, "errors", "REGISTRY_UNREADABLE", "TOOL_REGISTRY.json: missing, unreadable, duplicate keys, or invalid JSON encoding/value.")
    return None


def dependencies(tool):
    return list(tool.get("depends_on", [])) + [item[5:] for item in tool.get("dependencies", []) if isinstance(item, str) and item.startswith("tool:")]


def validate_registry(root, registry=None):
    root = Path(root)
    result = report("registry-validation")
    r = load_registry(root, result) if registry is None else registry
    if result["errors"]:
        return finish(result), None
    if not isinstance(r, dict) or not all(isinstance(r.get(key), kind) for key, kind in (("tools", list), ("categories", list), ("proposal_resolutions", list), ("status_definitions", dict), ("project", dict))):
        issue(result, "errors", "ROOT_FIELDS", "Missing registry root fields or incorrect root types.")
        return finish(result), None
    def error(code, message, **context):
        issue(result, "errors", code, message, **context)
    if r.get("schema_version") != 1 or isinstance(r.get("schema_version"), bool):
        error("SCHEMA_VERSION", "Unsupported schema_version; expected 1.")
    if not valid_date(r.get("updated_on")):
        error("REGISTRY_DATE", "Invalid updated_on date; expected YYYY-MM-DD.")
    if set(r["status_definitions"]) != set(STATUSES) or not all(isinstance(v, str) and v.strip() for v in r["status_definitions"].values()):
        error("STATUS_DEFINITIONS", "Status definitions must contain exactly the supported statuses with descriptions.")
    if not isinstance(r["project"].get("website"), str) or not r["project"]["website"].startswith("https://"):
        error("PROJECT_URL", "Project website must be an HTTPS URL.")
    milestones = r.get("milestones", [25, 50, 100, 200, 300, 500, 1000])
    if not isinstance(milestones, list) or not milestones or not all(type(n) is int and n > 0 for n in milestones) or milestones != sorted(set(milestones)):
        error("MILESTONES", "Milestones must be unique ascending positive integers.")
    categories = set()
    for c in r["categories"]:
        if not isinstance(c, dict) or not isinstance(c.get("id"), str) or not SLUG.fullmatch(c["id"]) or not isinstance(c.get("name"), str) or not c["name"].strip():
            error("CATEGORY_FIELDS", "Each category needs a safe id and nonempty name.")
        elif c["id"] in categories:
            error("DUPLICATE_CATEGORY", "Duplicate category identifier.", category=c["id"])
        else:
            categories.add(c["id"])
    ids, dirs, names, ranks = set(), set(), set(), set()
    good_tools = []
    for index, t in enumerate(r["tools"]):
        if not isinstance(t, dict):
            error("TOOL_OBJECT", f"Tool at index {index} must be an object.")
            continue
        missing = [key for key in REQUIRED_FIELDS if key not in t]
        if missing:
            error("REQUIRED_FIELDS", f"Tool at index {index}: missing {', '.join(missing)}.")
            continue
        if not isinstance(t["id"], str) or not SLUG.fullmatch(t["id"]):
            error("TOOL_ID", f"Tool at index {index}: invalid id.")
            continue
        tid = t["id"]
        if not isinstance(t["status"], str):
            error("INVALID_STATUS", "unknown status; expected a string", tool_id=tid)
            continue
        if tid in ids:
            error("DUPLICATE_ID", "duplicate id", tool_id=tid)
        ids.add(tid)
        if not isinstance(t["directory_path"], str) or not SLUG.fullmatch(t["directory_path"]):
            error("DIRECTORY_PATH", "Directory must be one safe relative slug.", tool_id=tid)
        else:
            directory = t["directory_path"].casefold()
            if directory in dirs:
                error("DUPLICATE_DIRECTORY", "duplicate directory", tool_id=tid)
            dirs.add(directory)
            try:
                source = safe_path(root, t["directory_path"] + "/index.html")
                if t["status"] in IMPLEMENTED and not source.is_file():
                    error("MISSING_IMPLEMENTATION", "Implemented status requires a directory and index.html.", tool_id=tid)
                elif t["status"] in BACKLOG and source.exists():
                    error("PLANNED_HAS_SOURCE", "Source exists but registry still claims a planned utility.", tool_id=tid)
            except ValueError:
                error("DIRECTORY_ESCAPE", "Tool directory escapes the project through a symlink.", tool_id=tid)
        for field in ("name", "description", "notes"):
            if not isinstance(t[field], str) or not t[field].strip():
                error("EMPTY_FIELD", f"Nonempty {field} is required.", tool_id=tid)
        name = unicodedata.normalize("NFKC", str(t["name"])).casefold().strip()
        if name in names:
            error("DUPLICATE_NAME", "Duplicate normalized tool name.", tool_id=tid)
        names.add(name)
        if not isinstance(t["category"], str) or t["category"] not in categories:
            error("MISSING_CATEGORY", "Missing or unknown category.", tool_id=tid)
        if not isinstance(t["status"], str) or t["status"] not in STATUSES:
            error("INVALID_STATUS", "unknown status", tool_id=tid)
        if t["priority"] not in ("P1", "P2", "P3"):
            error("INVALID_PRIORITY", "Priority must be P1, P2, or P3.", tool_id=tid)
        if t["implementation_complexity"] not in ("S", "M", "L", "XL"):
            error("INVALID_COMPLEXITY", "Complexity must be S, M, L, or XL.", tool_id=tid)
        lists_valid = True
        for field in ("dependencies", "required_features", "related_tools", "depends_on", "expected_interface_ids"):
            if field in t and not string_list(t[field], nonempty=field == "required_features"):
                error("INVALID_LIST", f"{field} must be an array of nonempty strings.", tool_id=tid)
                lists_valid = False
        if not lists_valid:
            continue
        if "expected_interface_ids" in t and len(t["expected_interface_ids"]) != len(set(t["expected_interface_ids"])):
            error("INTERFACE_IDS", "Repeated declared interface ID.", tool_id=tid)
        if len(t["dependencies"]) != len(set(t["dependencies"])):
            error("DUPLICATE_DEPENDENCY", "Repeated dependency declaration.", tool_id=tid)
        if t["testing_status"] not in ("NOT_STARTED", "SMOKE_PASSED", "REQUIRED_PASSED", "FAILED", "PARTIAL"):
            error("TESTING_STATUS", "Unknown testing_status.", tool_id=tid)
        verification_date = t["last_verification_date"]
        if verification_date is not None and not valid_date(verification_date):
            error("VERIFICATION_DATE", "Invalid last_verification_date.", tool_id=tid)
        elif verification_date and valid_date(r.get("updated_on")) and verification_date > r["updated_on"]:
            error("VERIFICATION_DATE", "Verification date is after registry updated_on.", tool_id=tid)
        if t["status"] in BACKLOG and (t["testing_status"] != "NOT_STARTED" or t["verification"] is not None or verification_date is not None):
            error("PLANNED_TEST_CLAIM", "A planned tool cannot claim tests or verification.", tool_id=tid)
        rank = t["sequence_rank"]
        if rank is not None:
            if type(rank) is not int or rank < 1 or rank in ranks:
                error("SEQUENCE_RANK", "Sequence ranks must be positive unique integers.", tool_id=tid)
            else:
                ranks.add(rank)
            if t["priority"] != "P1":
                error("SEQUENCE_PRIORITY", "Sequenced tool must be P1.", tool_id=tid)
        if t["status"] in ("TESTED", "RELEASED"):
            v = t["verification"]
            valid = isinstance(v, dict) and bool(v.get("source_revision")) and isinstance(v.get("source_sha256"), str) and bool(re.fullmatch(r"[a-f0-9]{64}", v["source_sha256"])) and isinstance(v.get("evidence_path"), str) and string_list(v.get("test_scope"), nonempty=True) and bool(verification_date)
            if not valid or t["testing_status"] not in ("SMOKE_PASSED", "REQUIRED_PASSED"):
                error("TEST_EVIDENCE", "Tested status requires passing test evidence.", tool_id=tid)
            if t["status"] == "RELEASED":
                p = v.get("publication") if isinstance(v, dict) else None
                website = r["project"].get("website", "")
                website = website if isinstance(website, str) else ""
                if not isinstance(p, dict) or p.get("http_status") != 200 or p.get("source_matches") is not True or not valid_timestamp(p.get("checked_at")) or not isinstance(p.get("url"), str) or not website or not p["url"].startswith(website.rstrip("/") + "/"):
                    error("PUBLICATION_EVIDENCE", "RELEASED requires verified publication.", tool_id=tid)
        good_tools.append(t)
    if ranks and max(ranks) != len(ranks):
        error("SEQUENCE_GAP", "Sequence ranks must be contiguous from 1.")
    tool_map = {t["id"]: t for t in good_tools}
    indegree = {tid: 0 for tid in tool_map}
    outgoing = {tid: [] for tid in tool_map}
    for t in good_tools:
        for related in t["related_tools"]:
            if related not in ids or related == t["id"]:
                error("TOOL_REFERENCE", "invalid related tool", tool_id=t["id"])
        for dependency in dependencies(t):
            if dependency not in tool_map or dependency == t["id"]:
                error("DEPENDENCY_REFERENCE", "Dependency references a nonexistent tool or itself.", tool_id=t["id"])
            else:
                indegree[t["id"]] += 1
                outgoing[dependency].append(t["id"])
    queue = deque(tid for tid, count in indegree.items() if count == 0)
    visited = 0
    while queue:
        current = queue.popleft()
        visited += 1
        for dependent in outgoing[current]:
            indegree[dependent] -= 1
            if not indegree[dependent]:
                queue.append(dependent)
    if visited < len(indegree):
        error("DEPENDENCY_CYCLE", "Tool dependency graph contains a cycle.")
    proposals = set()
    for p in r["proposal_resolutions"]:
        if not isinstance(p, dict) or not all(isinstance(p.get(k), str) and p[k].strip() for k in ("proposed_name", "tool_id", "disposition", "reason")):
            error("PROPOSAL_FIELDS", "Invalid proposal resolution fields.")
            continue
        if p["proposed_name"] in proposals:
            error("DUPLICATE_PROPOSAL", "Duplicate proposal.")
        proposals.add(p["proposed_name"])
        if p["tool_id"] not in ids:
            error("PROPOSAL_REFERENCE", "Proposal references nonexistent tool.")
        if p["disposition"] not in ("NEW_TOOL", "COMBINED", "EXISTING_FEATURE"):
            error("PROPOSAL_DISPOSITION", "Invalid proposal disposition.")
        if p["disposition"] == "EXISTING_FEATURE" and tool_map.get(p["tool_id"], {}).get("status") not in IMPLEMENTED:
            error("EXISTING_FEATURE", "Existing feature is not implemented.")
    if not r["tools"]:
        issue(result, "warnings", "EMPTY_REGISTRY", "Registry contains no tools; totals are zero and next task requires review.")
    if not result["errors"]:
        result["counts"] = summarize(r)
    result["details"]["dependency_policy"] = "Free-text dependency descriptions are metadata, not proof of installation. depends_on and tool:<id> encode checked tool references."
    return finish(result), r


def summarize(r):
    tools = r["tools"]
    by_status = {s: sum(t["status"] == s for t in tools) for s in STATUSES}
    released = by_status["RELEASED"]
    goal = next((n for n in r.get("milestones", [25, 50, 100, 200, 300, 500, 1000]) if n > released), None)
    return {"total": len(tools), "by_status": by_status, "released": released, "tested": by_status["TESTED"], "implemented": by_status["IMPLEMENTED"], "in_progress": by_status["IN_PROGRESS"], "planned": by_status["PLANNED"], "ready": by_status["READY"], "blocked": by_status["BLOCKED"], "backlog": sum(by_status[s] for s in BACKLOG), "by_category": {c["id"]: sum(t["category"] == c["id"] for t in tools) for c in r["categories"]}, "by_priority": {p: sum(t["priority"] == p for t in tools) for p in ("P1", "P2", "P3")}, "milestone": goal, "milestone_percent": round(100 * released / goal, 2) if goal else None, "remaining_to_milestone": goal - released if goal else None}


def next_tool(r):
    tools = {t["id"]: t for t in r["tools"]}
    ready = [t for t in r["tools"] if t["status"] == "READY" and all(tools[d]["status"] in ("TESTED", "RELEASED") for d in dependencies(t))]
    return min(ready, key=lambda t: (t["sequence_rank"] is None, t["sequence_rank"] or 0, t["priority"], t["id"]), default=None)


def markdown(value):
    return str(value).replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def progress_blocks(r):
    s = summarize(r)
    lines = ["| Metric | Count |", "| --- | ---: |", f"| Total registered utilities | {s['total']} |"]
    lines += [f"| {status} | {count} |" for status, count in s["by_status"].items()]
    lines += [f"| Backlog subtotal (IDEA + PLANNED + READY + BLOCKED) | {s['backlog']} |", "", "Status rows partition the total. The backlog subtotal overlaps those status rows; do not add it again.", "", f"Current growth milestone: **{s['milestone'] or 'REQUIRES REVIEW'} released tools**. Progress: {s['released']}/{s['milestone'] or 'UNKNOWN'} ({s['milestone_percent'] if s['milestone_percent'] is not None else 'UNKNOWN'}%); remaining: {s['remaining_to_milestone'] if s['remaining_to_milestone'] is not None else 'UNKNOWN'}.", "", "### Tools by category", "", "| Category | Count |", "| --- | ---: |"]
    lines += [f"| {markdown(c['name'])} | {s['by_category'][c['id']]} |" for c in r["categories"]]
    lines += ["", "### Tools by priority", "", "| Priority | Count |", "| --- | ---: |"] + [f"| {p} | {n} |" for p, n in s["by_priority"].items()]
    active = [t["name"] for t in r["tools"] if t["status"] == "IN_PROGRESS"]
    recommendation = next_tool(r)
    lines += ["", f"Current registered tool task: **{markdown(', '.join(active)) if active else 'none'}**. Session infrastructure work is recorded in the manual handoff.", "", f"Next ready tool: **{markdown(recommendation['name']) if recommendation else 'REQUIRES REVIEW'}**.", "", "### Recently verified tools (registry evidence dates)", "", "| Tool | Status | Last verification |", "| --- | --- | --- |"]
    recent = sorted((t for t in r["tools"] if t["last_verification_date"]), key=lambda t: (t["last_verification_date"], t["id"]), reverse=True)[:10]
    lines += [f"| {markdown(t['name'])} | {t['status']} | {t['last_verification_date']} |" for t in recent] or ["| None recorded | UNKNOWN | UNKNOWN |"]
    ordered = sorted((t for t in r["tools"] if t["sequence_rank"] is not None), key=lambda t: t["sequence_rank"])
    ready = [t for t in ordered if t["status"] == "READY"]
    sequence = "| Order | Tool ID | Name | Category | Complexity | Status |\n| ---: | --- | --- | --- | --- | --- |\n" + "\n".join(f"| {t['sequence_rank']} | {t['id']} | {markdown(t['name'])} | {next(c['name'] for c in r['categories'] if c['id'] == t['category'])} | {t['implementation_complexity']} | {t['status']} |" for t in ordered)
    catalog = []
    for c in r["categories"]:
        body = [f"### {c['name']}", "", "| Tool ID | Utility | Status | Priority | Complexity | Dependencies / gate |", "| --- | --- | --- | --- | --- | --- |"]
        for t in tools_in_category(r, c["id"]):
            deps = "; ".join(d for d in t["dependencies"] if not d.startswith("Tailwind")) or "Browser-native approach; scope review before implementation"
            body.append(f"| {t['id']} | {markdown(t['name'])} | {t['status']} | {t['priority']} | {t['implementation_complexity']} | {markdown(deps)} |")
        catalog.append("\n".join(body))
    resolutions = "| Proposed utility | Canonical tool ID | Resolution | Reason |\n| --- | --- | --- | --- |\n" + "\n".join(f"| {markdown(p['proposed_name'])} | {p['tool_id']} | {p['disposition']} | {markdown(p['reason'])} |" for p in r["proposal_resolutions"])
    upcoming = "\n".join(f"{t['sequence_rank']}. **{t['name']}** — {t['description']}" for t in ready[:5]) or "No sequenced READY tool; review the handoff."
    return {"PROGRESS_TRACKER.md": {"COUNTS": "\n".join(lines), "NEXT": upcoming}, "ROADMAP.md": {"SEQUENCE": sequence, "CATALOG": "\n\n".join(catalog)}, "audit/BACKLOG_RECONCILIATION.md": {"RESOLUTIONS": resolutions}}


def tools_in_category(r, category):
    return [t for t in r["tools"] if t["category"] == category]


def replace_block(text, key, content):
    start, end = f"<!-- GENERATED:{key}:START -->", f"<!-- GENERATED:{key}:END -->"
    if text.count(start) != 1 or text.count(end) != 1 or text.index(end) <= text.index(start):
        raise ValueError(f"Missing, duplicate or reversed generated markers: {key}")
    a, b = text.index(start) + len(start), text.index(end)
    newline = "\r\n" if "\r\n" in text else "\n"
    value = normalized(content).replace("\n", newline)
    return text[:a] + newline + value + newline + text[b:]


def generate_progress(root, registry=None):
    validation, r = validate_registry(root, registry)
    result = report("progress-generation")
    result["errors"] = validation["errors"].copy()
    result["warnings"] = validation["warnings"].copy()
    if result["errors"]:
        return finish(result)
    result["counts"] = summarize(r)
    prepared = {}
    for filename, blocks in progress_blocks(r).items():
        try:
            text = read_text(safe_path(root, filename))
            for key, value in blocks.items():
                text = replace_block(text, key, value)
            prepared[filename] = text
        except (OSError, UnicodeError, ValueError):
            issue(result, "errors", "GENERATED_MARKERS", "Document missing/unreadable or generated markers invalid; no generated documents were changed.", path=filename)
    if not result["errors"]:
        changed = [name for name, value in prepared.items() if atomic_write(safe_path(root, name), value)]
        result["details"]["changed_documents"] = changed
        result["information"].append("Preserved all content outside existing generated blocks; refreshed progress and pre-existing roadmap/reconciliation blocks.")
    return finish(result)


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.tags, self.ids, self.links, self.closed_tags = Counter(), Counter(), [], Counter()
        self.doctype = False
        self.title = []
        self.in_title = False
        self.anchor = None
        self.feed(text)
        self.close()

    def handle_decl(self, decl):
        self.doctype = self.doctype or decl.lower().strip() == "doctype html"

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags[tag] += 1
        if attrs.get("id"):
            self.ids[attrs["id"]] += 1
        if tag == "title":
            self.in_title = True
        if tag == "a":
            self.anchor = {"href": attrs.get("href"), "text": "", "hidden": "hidden" in attrs, "card": "data-title" in attrs}
            self.links.append(self.anchor)
        if attrs.get("src"):
            self.links.append({"href": attrs["src"], "text": "", "resource": True})

    def handle_endtag(self, tag):
        self.closed_tags[tag] += 1
        if tag == "title":
            self.in_title = False
        if tag == "a":
            self.anchor = None

    def handle_data(self, value):
        if self.in_title:
            self.title.append(value)
        if self.anchor is not None:
            self.anchor["text"] += value


def link_target(root, source, href):
    if not href:
        return None
    split = urlsplit(href)
    if split.scheme or split.netloc:
        return None
    decoded = unquote(split.path)
    # URLs use / on Windows too. Block encoded separators and symlink escapes.
    if "\\" in decoded or re.match(r"^[A-Za-z]:", decoded):
        raise ValueError("unsafe internal URL")
    target = (root / decoded.lstrip("/")) if decoded.startswith("/") else (root / source).parent / decoded if decoded else root / source
    target = target.resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError("link escapes project")
    if target.is_dir():
        target = target / "index.html"
    return target, split.fragment


def verify_tools(root, registry=None):
    validation, r = validate_registry(root, registry)
    result = report("tool-verification")
    result["errors"] = validation["errors"].copy()
    if result["errors"]:
        return finish(result)
    result["details"]["verification_kind"] = "STATIC_ONLY; no JavaScript, functional tests, or live requests executed; registry statuses unchanged."
    try:
        homepage = Page(read_text(root / "index.html"))
        home_targets = set()
        for link in homepage.links:
            try:
                target = link_target(root, "index.html", link["href"])
                if target:
                    home_targets.add(target[0])
            except ValueError:
                pass
    except (OSError, UnicodeError, ValueError):
        issue(result, "errors", "HOMEPAGE_UNREADABLE", "Homepage missing or unreadable.")
        return finish(result)
    checks = []
    for t in r["tools"]:
        if t["status"] not in IMPLEMENTED:
            continue
        file = t["directory_path"] + "/index.html"
        source = safe_path(root, file)
        entry = {"tool_id": t["id"], "path": file, "status": "PASS", "checks": [], "errors": [], "warnings": []}
        try:
            html = Page(read_text(source))
            for tag in ("html", "head", "body", "title"):
                if html.tags[tag] != 1 or html.closed_tags[tag] != 1:
                    entry["errors"].append(f"Expected one {tag} element.")
            if not html.doctype:
                entry["errors"].append("Missing HTML5 doctype.")
            title = " ".join("".join(html.title).split())
            if not title or title.casefold() in ("untitled", "document", "new page"):
                entry["errors"].append("Missing usable page title.")
            back = [link for link in html.links if not link.get("resource") and link.get("text", "").strip() and not link.get("hidden") and link_target(root, file, link.get("href")) == ((root / "index.html").resolve(), "")]
            if not back:
                entry["errors"].append("Missing usable Back to Hub link.")
            if source not in home_targets:
                entry["errors"].append("Tool is not linked from homepage.")
            duplicate_ids = [key for key, count in html.ids.items() if count > 1]
            if duplicate_ids:
                entry["errors"].append("Duplicate static interface IDs.")
            expected = t.get("expected_interface_ids", [])
            missing = [key for key in expected if key not in html.ids]
            if missing:
                entry["errors"].append("Missing declared interface elements: " + ", ".join(missing))
            if not expected:
                entry["warnings"].append("No declared expected_interface_ids; semantic controls cannot be verified reliably.")
            entry["checks"] = ["required source file", "HTML5 structure", "usable title", "hub navigation", "homepage inclusion", "static ID uniqueness", "declared interface IDs only"]
        except (OSError, UnicodeError, ValueError):
            entry["errors"].append("Tool source is missing, unreadable, or has an unsafe link.")
        entry["status"] = "FAIL" if entry["errors"] else "WARN" if entry["warnings"] else "PASS"
        for message in entry["errors"]:
            issue(result, "errors", "TOOL_STRUCTURE", message, tool_id=t["id"], path=file)
        for message in entry["warnings"]:
            issue(result, "warnings", "INTERFACE_SCOPE", message, tool_id=t["id"], path=file)
        checks.append(entry)
    result["counts"] = {"tools_checked": len(checks), "passed": sum(t["status"] == "PASS" for t in checks), "failed": sum(t["status"] == "FAIL" for t in checks)}
    result["details"]["tools"] = checks
    return finish(result)


def check_project(root, registry=None):
    validation, r = validate_registry(root, registry)
    result = report("project-consistency")
    result["errors"] = validation["errors"].copy()
    result["warnings"] = validation["warnings"].copy()
    if result["errors"]:
        return finish(result)
    result["counts"] = summarize(r)
    for filename in REQUIRED_DOCS:
        if not (root / filename).is_file():
            issue(result, "errors", "MISSING_DOCUMENTATION", "Missing documentation: " + filename, path=filename)
    try:
        initial = json.loads(read_text(root / "audit/INITIAL_BACKLOG.json"))["proposed_names"]
        mapped = {p["proposed_name"] for p in r["proposal_resolutions"]}
        if not isinstance(initial, list) or not all(isinstance(n, str) and n in mapped for n in initial):
            issue(result, "errors", "MISSING_PROPOSAL", "Initial backlog proposals are missing mappings.")
    except (OSError, UnicodeError, ValueError, KeyError, TypeError):
        issue(result, "errors", "INITIAL_BACKLOG", "Initial backlog audit is missing or invalid.")
    for filename, blocks in progress_blocks(r).items():
        try:
            old = read_text(root / filename)
            expected = old
            for key, value in blocks.items():
                expected = replace_block(expected, key, value)
            if normalized(expected) != normalized(old):
                issue(result, "errors", "GENERATED_STALE", filename + ": generated data is stale; run python scripts/generate_progress.py", path=filename)
        except (OSError, UnicodeError, ValueError):
            issue(result, "errors", "GENERATED_MARKERS", "Missing document or invalid generated section markers.", path=filename)
    tools = {t["directory_path"]: t for t in r["tools"]}
    for directory in root.iterdir():
        if directory.is_dir() and not directory.name.startswith(".") and (directory / "index.html").is_file() and directory.name not in tools:
            issue(result, "errors", "UNREGISTERED_TOOL", "Unregistered utility directory.", path=directory.name)
    expected_cards = {(root / (t["directory_path"] + "/index.html")).resolve() for t in r["tools"] if t["status"] in IMPLEMENTED}
    files = ["index.html"] + [t["directory_path"] + "/index.html" for t in r["tools"] if t["status"] in IMPLEMENTED]
    parsed = {}
    for filename in files:
        try:
            parsed[filename] = Page(read_text(safe_path(root, filename)))
        except (OSError, UnicodeError, ValueError):
            issue(result, "errors", "HTML_UNREADABLE", "Missing or unreadable HTML entry point.", path=filename)
    home = parsed.get("index.html")
    if home:
        card_targets = []
        for link in home.links:
            if link.get("card"):
                try:
                    target = link_target(root, "index.html", link["href"])
                    if target:
                        card_targets.append(target[0])
                except ValueError:
                    pass
        if set(card_targets) != expected_cards or len(card_targets) != len(expected_cards):
            issue(result, "errors", "HOMEPAGE_CARDS", "Homepage tool links do not match implemented registry paths, or contain duplicates.")
        if not re.search(rf">\s*{len(expected_cards)} tools ready to use\s*</p>", read_text(root / "index.html")):
            issue(result, "errors", "HOMEPAGE_COUNT", "Initial homepage tool count differs from the registry.")
    for filename, html in parsed.items():
        for link in html.links:
            href = link["href"]
            try:
                if href and urlsplit(href).scheme.lower() in ("javascript", "vbscript"):
                    issue(result, "errors", "UNSAFE_LINK", "Executable navigation URL is not permitted.", path=filename)
                    continue
                target = link_target(root, filename, href)
                if target and not target[0].is_file():
                    issue(result, "errors", "BROKEN_INTERNAL_LINK", "Broken internal link target.", path=filename)
                elif target and target[1] and target[0].suffix.lower() == ".html":
                    destination = target[0].relative_to(root.resolve()).as_posix()
                    if destination not in parsed:
                        parsed_page = Page(read_text(target[0]))
                    else:
                        parsed_page = parsed[destination]
                    if unquote(target[1]) not in parsed_page.ids:
                        issue(result, "warnings", "FRAGMENT_NOT_STATIC", "Fragment ID not found in static HTML; it may be generated by JavaScript.", path=filename)
            except (ValueError, OSError, UnicodeError):
                issue(result, "errors", "UNSAFE_INTERNAL_PATH", "Invalid internal link or path outside the project.", path=filename)
    for filename in (*REQUIRED_DOCS, "scripts/README.md", "audit/CURRENT_STATE.md", "audit/BACKLOG_RECONCILIATION.md"):
        if not (root / filename).is_file():
            continue
        try:
            # Ignore examples in fenced code; check file targets, not external URLs.
            prose = re.sub(r"```.*?```", "", read_text(root / filename), flags=re.S)
            for match in re.finditer(r"\[[^\]]+\]\(([^)\s]+)\)", prose):
                target = link_target(root, filename, match.group(1))
                if target and not target[0].is_file():
                    issue(result, "errors", "BROKEN_DOCUMENT_LINK", "Broken internal documentation link.", path=filename)
        except (ValueError, OSError, UnicodeError):
            issue(result, "errors", "DOCUMENT_LINK_PATH", "Invalid or unsafe documentation link.", path=filename)
    for t in r["tools"]:
        if t["status"] not in ("TESTED", "RELEASED"):
            continue
        v, filename = t["verification"], t["directory_path"] + "/index.html"
        try:
            if normalized_hash(read_text(safe_path(root, filename))) != v["source_sha256"]:
                issue(result, "errors", "SOURCE_EVIDENCE_STALE", "Source changed since verification; retest and update evidence.", tool_id=t["id"])
            evidence = json.loads(read_text(safe_path(root, v["evidence_path"])))
            if not isinstance(evidence, dict) or not isinstance(evidence.get("pages"), list) or not all(isinstance(page, dict) for page in evidence["pages"]):
                raise ValueError("Invalid verification report structure")
            page = next((p for p in evidence.get("pages", []) if p.get("path") == filename), None)
            if evidence.get("result") != "PASS" or not page or page.get("source_sha256") != v["source_sha256"] or evidence.get("source_revision") != v["source_revision"] or evidence.get("verified_on") != t["last_verification_date"]:
                issue(result, "errors", "EVIDENCE_MISMATCH", "Stored verification evidence does not match registry source/revision/date.", tool_id=t["id"])
            if t["status"] == "RELEASED" and page and page.get("publication") != v.get("publication"):
                issue(result, "errors", "PUBLICATION_MISMATCH", "Recorded publication evidence does not match audit report.", tool_id=t["id"])
        except (OSError, UnicodeError, ValueError, TypeError, KeyError):
            issue(result, "errors", "EVIDENCE_UNREADABLE", "Missing, invalid or unsafe verification evidence.", tool_id=t["id"])
    result["information"].append("Read-only local consistency checks; external URLs and live publication were not checked.")
    return finish(result)


def git_snapshot(root, git_executable="git"):
    """Only report branch, hashes and relative change names; never remotes/authors/messages."""
    def run(args):
        return subprocess.run([git_executable, "-C", str(root), *args], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=10, check=True, creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0).stdout.strip()
    try:
        top = Path(run(["rev-parse", "--show-toplevel"])).resolve()
        if top != root.resolve():
            return {"status": "UNKNOWN", "reason": "Project root is not the Git repository root.", "branch": "UNKNOWN", "latest_commit": "UNKNOWN", "working_tree": "UNKNOWN", "changes": []}
        commit = run(["rev-parse", "--verify", "HEAD"])
        branch = run(["branch", "--show-current"]) or "DETACHED HEAD"
        raw = subprocess.run([git_executable, "-C", str(root), "status", "--porcelain=v1", "-z", "--untracked-files=normal"], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=10, check=True, creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0).stdout
        parts, changes, index = raw.split("\0"), [], 0
        while index < len(parts):
            item = parts[index]
            index += 1
            if not item:
                continue
            changes.append({"state": item[:2], "path": item[3:].replace("\\", "/")})
            if "R" in item[:2] or "C" in item[:2]:
                index += 1  # Original rename/copy path is not needed in reports.
        return {"status": "KNOWN", "branch": branch, "latest_commit": commit, "working_tree": "Dirty" if changes else "Clean", "changes": changes, "push_status": "UNKNOWN; no remote verification performed", "deployment": "UNKNOWN; not checked"}
    except (OSError, subprocess.SubprocessError, ValueError):
        return {"status": "UNKNOWN", "reason": "Git unavailable, command failed, or root is not a Git checkout.", "branch": "UNKNOWN", "latest_commit": "UNKNOWN", "working_tree": "UNKNOWN", "changes": []}


def handoff_block(r, git, checks):
    s, next_item = summarize(r), next_tool(r)
    active = [t["name"] for t in r["tools"] if t["status"] == "IN_PROGRESS"]
    lines = ["Snapshot of local files at generation; it does not assert later commits, pushes, functional tests, or deployment.", "", f"- Milestone: {s['milestone'] or 'REQUIRES REVIEW'} released tools; {s['released']} currently recorded released.", f"- Tool status counts: {'; '.join(f'{k}: {v}' for k, v in s['by_status'].items())}.", f"- Current registered tool task: {markdown(', '.join(active)) if active else 'none; see manual session notes for infrastructure work'}.", f"- Next ready tool: {markdown(next_item['name']) if next_item else 'REQUIRES REVIEW'}.", f"- Git branch: {markdown(git['branch'])}.", f"- Latest commit observed before generation: {git['latest_commit']}.", f"- Working tree at snapshot: {git['working_tree']}.", "- Push/deployment status: UNKNOWN; this offline command does not verify either.", "", "### Recorded recent completions", "", "These are registry verification records, not new tests or tasks executed by this generator."]
    recent = sorted((t for t in r["tools"] if t["last_verification_date"]), key=lambda t: (t["last_verification_date"], t["id"]), reverse=True)[:10]
    lines += [f"- {markdown(t['name'])}: {t['status']}, evidence dated {t['last_verification_date']}." for t in recent] or ["- UNKNOWN; no dated verification records."]
    lines += ["", "### Known tool blockers"]
    lines += [f"- {markdown(t['name'])}: {markdown(t['notes'])}" for t in r["tools"] if t["status"] == "BLOCKED"] or ["- None recorded."]
    lines += ["", "### Outstanding automated validation"]
    for check in checks:
        lines.append(f"- {check['check_name']}: {check['status']} ({len(check['errors'])} errors, {len(check['warnings'])} warnings).")
        lines += [f"  - {item['code']}: {markdown(item['message'])}" for item in check["errors"] + check["warnings"]]
    lines += ["", "### Uncommitted changes (repository-relative)"]
    lines += [f"- `{item['state']}` {markdown(item['path'])}" for item in git["changes"]] or ["- None observed." if git["status"] == "KNOWN" else "- UNKNOWN."]
    lines += ["", "Unexpected termination has no cleanup guarantee. Re-run project_status.py and inspect actual source/Git before resuming. This snapshot cannot embed its own resulting commit hash."]
    return "\n".join(lines)


def generate_handoff(root, registry=None, checks=None):
    validation, r = validate_registry(root, registry)
    result = report("handoff-generation")
    result["errors"] = validation["errors"].copy()
    if result["errors"]:
        return finish(result)
    checks = checks if checks is not None else [validation, check_project(root, r), verify_tools(root, r)]
    try:
        filename = safe_path(root, "SESSION_HANDOFF.md")
        original = read_text(filename)
        # Preflight marker validation; never create a replacement for missing manual notes.
        replace_block(original, "STATUS", "")
        for _ in range(2):
            git = git_snapshot(root)
            text = replace_block(read_text(filename), "STATUS", handoff_block(r, git, checks))
            atomic_write(filename, text)
        result["details"]["git"] = git_snapshot(root)
        if result["details"]["git"]["status"] == "UNKNOWN":
            issue(result, "warnings", "GIT_UNKNOWN", "Git state is UNKNOWN; no commit/push/deployment claim was made.")
        result["counts"] = summarize(r)
    except (OSError, UnicodeError, ValueError):
        issue(result, "errors", "HANDOFF_MARKERS", "Handoff unreadable or STATUS markers invalid; manual notes were preserved.")
    return finish(result)


def save_report(root, result):
    filename = REPORT_FILES.get(result["check_name"])
    if filename:
        # Reports are fixed latest snapshots, never accumulating histories.
        destination = safe_path(root, "reports/" + filename)
        atomic_write(destination, json.dumps(result, ensure_ascii=False, indent=2) + "\n")


def project_status(root, write_reports=True, update_documents=True):
    root = Path(root).resolve()
    validation, r = validate_registry(root)
    initial = check_project(root, r) if not validation["errors"] else check_project(root)
    structure = verify_tools(root, r) if not validation["errors"] else verify_tools(root)
    generation = generate_progress(root, r) if update_documents and not validation["errors"] else None
    consistency = check_project(root, r) if not validation["errors"] else initial
    handoff = generate_handoff(root, r, [validation, consistency, structure]) if generation and not generation["errors"] else None
    result = report("project-status")
    checks = [validation, consistency, structure] + ([generation] if generation else []) + ([handoff] if handoff else [])
    for check in checks:
        for key in ("errors", "warnings"):
            for entry in check[key]:
                annotated = {"check": check["check_name"], **entry}
                if annotated not in result[key]:
                    result[key].append(annotated)
    result["counts"] = summarize(r) if r and not validation["errors"] else {}
    git = git_snapshot(root)
    if git["status"] == "UNKNOWN" and not any(i["code"] == "GIT_UNKNOWN" for i in result["warnings"]):
        issue(result, "warnings", "GIT_UNKNOWN", "Git state unavailable; UNKNOWN is reported rather than a clean/pushed state.")
    if not validation["errors"] and len([t for t in r["tools"] if t["status"] == "IN_PROGRESS"]) > 1:
        issue(result, "warnings", "MULTIPLE_ACTIVE_TOOLS", "More than one tool is IN_PROGRESS; review unfinished work before choosing another.")
    result["details"] = {"checks": {c["check_name"]: c["status"] for c in checks}, "git": git, "current_task": [t["name"] for t in r["tools"] if t["status"] == "IN_PROGRESS"] if r and not validation["errors"] else "UNKNOWN", "next_task": (next_tool(r) or {}).get("name", "REQUIRES REVIEW") if r and not validation["errors"] else "UNKNOWN", "initial_consistency": {"status": initial["status"], "errors": initial["errors"], "warnings": initial["warnings"]}, "documentation_updates_enabled": update_documents, "scope": "OFFLINE_STATIC_ONLY; no automatic tool status changes, functional tests, pushes or deployment."}
    finish(result)
    if write_reports:
        for item in (validation, consistency, structure, result):
            save_report(root, item)
    return result


def display(result):
    print(f"{result['check_name']}: {result['status']} ({len(result['errors'])} errors, {len(result['warnings'])} warnings)")
    if result["check_name"] == "project-status":
        print("EVERYDAY DIGITAL BOX — PROJECT STATUS")
        counts = result["counts"]
        print(f"Current milestone: {counts.get('milestone', 'UNKNOWN')} released tools")
        print(f"Total registered tools: {counts.get('total', 'UNKNOWN')}")
        for key, count in counts.get("by_status", {}).items():
            print(f"{key}: {count}")
        print(f"Backlog subtotal: {counts.get('backlog', 'UNKNOWN')} (not an extra status)")
        print(f"Current registered tool task: {result['details']['current_task'] or 'none'}")
        print(f"Next recommended task: {result['details']['next_task']}")
        print(f"Git branch: {result['details']['git']['branch']}")
        print(f"Working tree: {result['details']['git']['working_tree']}")
        for name, status in result["details"]["checks"].items():
            print(f"{name}: {status}")
    for severity in ("errors", "warnings"):
        for item in result[severity]:
            location = item.get("tool_id") or item.get("path") or "project"
            print(f"{severity[:-1].upper()} [{item['code']}] {location}: {item['message']}")


def run_cli(action):
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Offline project management; static checks do not prove functional correctness.")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--json", action="store_true", help="Print machine-readable report")
    parser.add_argument("--no-report", action="store_true", help="Do not save JSON reports (generators still update marked documentation)")
    if action == "status":
        parser.add_argument("--check-only", action="store_true", help="Validate and snapshot Git without updating generated documentation")
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        if action == "validate":
            result, _ = validate_registry(root)
        elif action == "check":
            result = check_project(root)
        elif action == "verify":
            result = verify_tools(root)
        elif action == "progress":
            result = generate_progress(root)
        elif action == "handoff":
            result = generate_handoff(root)
        else:
            result = project_status(root, not args.no_report, not args.check_only)
        if action != "status" and not args.no_report:
            save_report(root, result)
        if args.json:
            print(json.dumps(result, ensure_ascii=False))
        else:
            display(result)
        return 1 if result["errors"] else 0
    except (OSError, UnicodeError, ValueError) as exc:
        # Do not echo raw exception paths, file contents, or command stderr.
        print("Tracking command could not read/write its project files; check permissions, encoding, markers and project root.", file=sys.stderr)
        return 2


def bridge():
    """Stable JSON protocol for existing Node exports; one validation/counting engine."""
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--bridge", choices=("registry", "project", "summary", "sync"), required=True)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        raw = sys.stdin.read()
        registry = json.loads(raw) if raw.strip() else None
        result, r = validate_registry(root, registry)
        if args.bridge == "summary" and not result["errors"]:
            s = summarize(r)
            print(json.dumps({**s, "planned": s["backlog"], "implemented_unverified": s["implemented"], "tested_unpublished": s["tested"]}))
        else:
            if args.bridge == "project":
                result = check_project(root, registry)
            elif args.bridge == "sync":
                result = generate_progress(root, registry)
            print(json.dumps(result))
        return 0
    except (OSError, UnicodeError, ValueError):
        print(json.dumps({"errors": [{"message": "Registry bridge input/read failed."}], "warnings": []}))
        return 0


if __name__ == "__main__":
    sys.exit(bridge())
