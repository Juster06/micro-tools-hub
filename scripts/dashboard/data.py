"""Read-only snapshots and presentation queries, independent of Tk."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil

import tracking as tr

DOCS = ("SESSION_HANDOFF.md", "CHANGELOG.md", "ROADMAP.md", "PROJECT_MASTER_PLAN.md")
MILESTONES = (25, 50, 100, 200, 300, 500, 1000)
UNAVAILABLE_TESTS = "Test results unavailable — run tests to update."


def read_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("duplicate JSON keys")
            result[key] = value
        return result
    def constant(_):
        raise ValueError("nonstandard JSON number")
    return json.loads(Path(path).read_text(encoding="utf-8-sig"), object_pairs_hook=pairs, parse_constant=constant)


def timestamp(value):
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.astimezone(timezone.utc) if parsed.tzinfo else None
    except (ValueError, TypeError, AttributeError):
        return None


def text(value, fallback="Not documented"):
    return value if isinstance(value, str) and value.strip() else fallback


def strings(value):
    return [v for v in value if isinstance(v, str)] if isinstance(value, list) else []


def source_files(root):
    """Bounded to relevant project inputs, never Git objects, reports or packages."""
    for directory, subdirs, filenames in os.walk(root):
        subdirs[:] = sorted(d for d in subdirs if d not in {".git", "reports", "node_modules", "__pycache__", ".venv", "venv"} and not (Path(directory) / d).is_symlink())
        for filename in sorted(filenames):
            path = Path(directory) / filename
            if not path.is_symlink() and (path.suffix in {".py", ".pyw", ".md", ".html", ".json", ".mjs"} or filename == "CNAME"):
                yield path


def fingerprint(root, exclude=()):
    digest = hashlib.sha256()
    for path in source_files(root):
        if path.relative_to(root).as_posix() in exclude:
            continue
        digest.update(path.relative_to(root).as_posix().encode("utf-8") + b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_settings(root):
    path = root / "reports" / "dashboard-settings.json"
    if not path.exists():
        return {}, None
    try:
        value = read_json(path)
        if not isinstance(value, dict) or not isinstance(value.get("git_executable", ""), str):
            raise ValueError("expected a Git executable string")
        return value, None
    except (OSError, ValueError, UnicodeError, RecursionError) as exc:
        return {}, f"Local settings unavailable: {exc}"


def find_git(settings):
    configured = settings.get("git_executable")
    if configured:
        path = Path(configured)
        return str(path) if path.is_absolute() and path.is_file() else None
    discovered = shutil.which("git")
    if discovered:
        return discovered
    for base in (os.environ.get("ProgramFiles"), os.environ.get("LOCALAPPDATA")):
        if base:
            for relative in ("Git/cmd/git.exe", "Programs/Git/cmd/git.exe"):
                path = Path(base) / relative
                if path.is_file():
                    return str(path)
    return None


@dataclass
class Report:
    name: str
    state: str = "NOT RUN"
    recorded: str = "UNKNOWN"
    generated_at: str = "Unavailable"
    reason: str = "Report missing — refresh project status."
    payload: dict = field(default_factory=dict)


def load_report(root, name, now=None, provenance=None, input_hash=None):
    result = Report(name)
    path = root / "reports" / tr.REPORT_FILES[name]
    try:
        value = read_json(path)
        if not isinstance(value, dict) or value.get("schema_version") != 1 or value.get("check_name") != name:
            raise ValueError("unsupported report schema or mismatched check name")
        if value.get("status") not in {"PASS", "WARN", "FAIL"} or not all(isinstance(value.get(k), list) for k in ("errors", "warnings")):
            raise ValueError("invalid report status/errors/warnings")
        if not all(isinstance(item, dict) and isinstance(item.get("message"), str) for key in ("errors", "warnings") for item in value[key]):
            raise ValueError("invalid diagnostic entry")
        generated = timestamp(value.get("generated_at"))
        if not generated:
            raise ValueError("missing or invalid report timestamp")
        result.payload, result.generated_at = value, value["generated_at"]
        result.recorded = "WARNING" if value["status"] == "WARN" else value["status"]
        if value["errors"]:
            result.recorded = "FAIL"
        elif value["warnings"] and result.recorded == "PASS":
            result.recorded = "WARNING"
        now = now or datetime.now(timezone.utc)
        age = now - generated
        stale = age > timedelta(hours=24)
        reason = "Older than 24 hours." if stale else "Timestamp-based legacy snapshot; refresh to capture input hashes."
        if age < -timedelta(minutes=5):
            result.state, result.reason = "UNKNOWN", "Report timestamp is in the future; check the system clock."
            return result
        if provenance is not None:
            if not input_hash or provenance.get("input_hash") != input_hash or provenance.get("reports", {}).get(name) != file_hash(path):
                stale, reason = True, "Project inputs or report files changed since the captured refresh."
            elif not stale:
                reason = "Input and report hashes match the captured refresh."
        else:
            latest = max((p.stat().st_mtime for p in source_files(root)), default=0)
            if latest > generated.timestamp() + 2:
                stale, reason = True, "Project files are newer than this legacy report."
        result.state = "STALE" if stale else result.recorded
        result.reason = reason
    except FileNotFoundError:
        pass
    except (OSError, ValueError, UnicodeError, RecursionError, AttributeError, TypeError) as exc:
        result.state, result.reason = "UNKNOWN", f"Cannot read report: {exc}. Refresh to regenerate it."
    return result


def filter_tools(tools, query="", category="All", status="All", priority="All", sort="name", reverse=False):
    query = query.strip().casefold()
    filtered = [t for t in tools if (not query or query in (t["name"] + " " + t["id"]).casefold()) and (category == "All" or t["category"] == category) and (status == "All" or t["status"] == status) and (priority == "All" or t.get("priority") == priority)]
    return sorted(filtered, key=lambda t: (str(t.get(sort) or "").casefold(), t["id"]), reverse=reverse)


def dependency_issues(tool, tools):
    by_id = tools if isinstance(tools, dict) else {t["id"]: t for t in tools}
    return [f"{dep}: {by_id.get(dep, {}).get('status', 'missing')}" for dep in tr.dependencies(tool) if by_id.get(dep, {}).get("status") not in {"TESTED", "RELEASED"}]


def queue_order(tools):
    # Same documented ordering as tracking.next_tool: sequence, priority, stable ID.
    by_id = {t["id"]: t for t in tools}
    return sorted((t for t in tools if t["status"] == "READY" and not dependency_issues(t, by_id)), key=lambda t: (t.get("sequence_rank") is None, t.get("sequence_rank") or 0, t.get("priority", ""), t["id"]))


def blockers(tools):
    return [(t, text(t.get("blocker_reason"), text(t.get("notes"), "Reason not documented."))) for t in tools if t["status"] == "BLOCKED"]


def milestone_progress(released):
    return [(goal, min(100.0, 100 * released / goal)) for goal in MILESTONES]


@dataclass
class Snapshot:
    root: Path
    tools: list = field(default_factory=list)
    categories: dict = field(default_factory=dict)
    counts: dict = field(default_factory=dict)
    reports: list = field(default_factory=list)
    issues: list = field(default_factory=list)
    git: dict = field(default_factory=dict)
    documents: dict = field(default_factory=dict)
    registry_valid: bool = False
    loaded_at: str = ""
    git_executable: str = ""
    status_definitions: dict = field(default_factory=dict)
    next_action: str = "Review the current session handoff."
    settings: dict = field(default_factory=dict)


def load_snapshot(root):
    root = Path(root).resolve()
    snapshot = Snapshot(root, loaded_at=datetime.now(timezone.utc).isoformat(timespec="seconds"))
    try:
        validation, registry = tr.validate_registry(root)
    except (ValueError, TypeError, KeyError, AttributeError) as exc:
        validation = tr.report("registry-validation")
        tr.issue(validation, "errors", "REGISTRY_SHAPE", f"Malformed registry fields: {exc}")
        registry = tr.load_registry(root, validation)
    snapshot.issues.extend(f"Registry {i['code']}: {i['message']}" for kind in ("errors", "warnings") for i in validation[kind])
    snapshot.registry_valid = not validation["errors"]
    if isinstance(registry, dict):
        snapshot.categories = {c["id"]: c["name"] for c in registry.get("categories", []) if isinstance(c, dict) and isinstance(c.get("id"), str) and isinstance(c.get("name"), str)}
        definitions = registry.get("status_definitions", {})
        snapshot.status_definitions = definitions if isinstance(definitions, dict) else {}
        seen = set()
        for raw in registry.get("tools", []):
            if not isinstance(raw, dict) or not all(isinstance(raw.get(k), str) for k in ("id", "name", "category")) or raw.get("status") not in tr.STATUSES or raw["id"] in seen:
                continue
            tool = dict(raw)
            tool["priority"] = text(raw.get("priority"), "UNKNOWN")
            tool["last_verification_date"] = raw.get("last_verification_date") if tr.valid_date(raw.get("last_verification_date")) else None
            tool["dependencies"], tool["depends_on"] = strings(raw.get("dependencies")), strings(raw.get("depends_on"))
            tool["sequence_rank"] = raw.get("sequence_rank") if type(raw.get("sequence_rank")) is int and raw["sequence_rank"] > 0 else None
            seen.add(tool["id"])
            snapshot.tools.append(tool)
    snapshot.counts = tr.summarize({"tools": snapshot.tools, "categories": [{"id": k} for k in snapshot.categories], "milestones": list(MILESTONES)})
    if not snapshot.registry_valid:
        snapshot.issues.insert(0, "Registry validation failed. Counts and tables show readable entries only; resolve errors before relying on totals.")
    settings, issue = load_settings(root)
    snapshot.settings = settings
    if issue:
        snapshot.issues.append(issue)
    snapshot.git_executable = find_git(settings) or ""
    snapshot.git = tr.git_snapshot(root, git_executable=snapshot.git_executable or "git")
    if snapshot.git["status"] == "UNKNOWN":
        snapshot.issues.append("Git unavailable or checkout not recognized. Set Git executable in Quick Actions if needed.")
    provenance = None
    path = root / "reports/dashboard-refresh.json"
    if path.exists():
        try:
            provenance = read_json(path)
            if not isinstance(provenance, dict) or provenance.get("schema_version") != 1 or not isinstance(provenance.get("reports"), dict):
                raise ValueError("invalid provenance schema")
        except (OSError, ValueError, UnicodeError, RecursionError) as exc:
            provenance = {}
            snapshot.issues.append(f"Refresh provenance unavailable: {exc}")
    try:
        input_hash = fingerprint(root)
    except OSError as exc:
        input_hash, provenance = None, {}
        snapshot.issues.append(f"Could not verify input freshness: {exc}")
    snapshot.reports = [load_report(root, name, provenance=provenance, input_hash=input_hash) for name in tr.REPORT_FILES]
    for name in DOCS:
        try:
            snapshot.documents[name] = (root / name).read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError) as exc:
            snapshot.documents[name] = f"Document unavailable: {exc}"
            snapshot.issues.append(f"{name}: unavailable.")
    match = re.search(r"^\*\*Next major task:\*\*\s*(.+)$", snapshot.documents.get("SESSION_HANDOFF.md", ""), re.MULTILINE)
    if match:
        snapshot.next_action = match.group(1)
    return snapshot


def summary_text(snapshot):
    counts = snapshot.counts
    next_item = next(iter(queue_order(snapshot.tools)), None)
    return "\n".join(["Everyday Digital Box — Project Status", f"Registry: {'valid' if snapshot.registry_valid else 'INVALID / partial data'}; registered {counts['total']}; released {counts['released']}; tested {counts['tested']}; implemented {counts['implemented']}.", f"Ready {counts['ready']}; planned {counts['planned']}; in progress {counts['in_progress']}; blocked {counts['blocked']}.", f"Milestone: {counts['milestone'] or 'review required'} released tools.", f"Next ready utility: {next_item['name'] if next_item else 'None'} (owner-directed tasks remain in handoff).", "Checks: " + "; ".join(f"{r.name}: {r.state}" for r in snapshot.reports), f"Snapshot: {snapshot.loaded_at}", "Structural checks are not functional tests. Push/deployment not verified."])
