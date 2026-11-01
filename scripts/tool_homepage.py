"""Minimal homepage proposals. No command in this module applies or publishes them."""
import difflib
from html import escape
from html.parser import HTMLParser
import json
import re

import tracking as tr
from tool_framework import FrameworkError, functional_gate, local_path, lookup, structural_check


class Homepage(HTMLParser):
    VOID = {"meta", "link", "input", "img", "br", "hr", "source", "area", "base", "embed", "param", "wbr", "col", "track"}

    def __init__(self, content):
        super().__init__(convert_charrefs=True)
        self.content, self.stack, self.cards = content, [], []
        self.grid_ends, self.counts = [], []
        self.lines = [0]
        for match in re.finditer("\n", content):
            self.lines.append(match.end())
        self.feed(content)
        self.close()
        if len(self.grid_ends) != 1 or len(self.counts) != 1:
            raise FrameworkError("Expected one toolGrid and one resultCount; homepage requires manual review.")

    def position(self):
        row, column = self.getpos()
        return self.lines[row - 1] + column

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag not in self.VOID:
            self.stack.append((tag, attrs, self.position(), self.position() + len(self.get_starttag_text())))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if not self.stack or self.stack[-1][0] != tag:
            raise FrameworkError("Unexpected homepage nesting; refuse to guess card boundaries.")
        opening = self.stack.pop()
        _, attrs, start, inner = opening
        if attrs.get("id") == "toolGrid":
            self.grid_ends.append(self.position())
        if attrs.get("id") == "resultCount":
            self.counts.append((inner, self.position()))
        if tag == "a" and "data-title" in attrs and any(a.get("id") == "toolGrid" for _, a, _, _ in self.stack):
            self.cards.append({"attrs": attrs, "start": start, "end": self.position() + len("</a>")})


def integration_proposal(root, tool_id):
    value, tool = lookup(root, tool_id)
    if tool["status"] not in {"TESTED", "RELEASED"}:
        raise FrameworkError("Homepage availability requires TESTED or RELEASED; scaffolds/unfinished tools cannot be integrated.")
    source = tr.read_text(local_path(root, "index.html"))
    home = Homepage(source)
    routes, identities = {}, set()
    candidate = tool["directory_path"] + "/index.html"
    existing = None
    for card in home.cards:
        attrs = card["attrs"]
        target = tr.link_target(root, "index.html", attrs.get("href"))
        if not target or target[1]:
            raise FrameworkError("Homepage card route is not a canonical local page.")
        route = target[0].relative_to(root.resolve()).as_posix()
        if route in routes or attrs.get("data-tool-id") in identities:
            raise FrameworkError("Duplicate homepage route or tool identity.")
        if attrs.get("data-tool-id"):
            identities.add(attrs["data-tool-id"])
        routes[route] = card
        if route == candidate:
            existing = card
        elif attrs.get("data-tool-id") == tool_id:
            raise FrameworkError("Tool ID already appears at another route.")
    expected = {t["directory_path"] + "/index.html" for t in value["tools"] if t["status"] in tr.IMPLEMENTED}
    if set(routes) - {candidate} != expected - {candidate}:
        raise FrameworkError("Other homepage cards disagree with registry; resolve existing integration errors first.")
    begin, end = home.counts[0]
    if source[begin:end].strip() != f"{len(home.cards)} tools ready to use":
        raise FrameworkError("Unexpected initial count text; manual homepage review required.")
    if existing and not existing["attrs"].get("data-tool-id"):
        return {"tool_id": tool_id, "action": "NO_CHANGE", "patch": "", "notice": "Existing manually maintained card preserved exactly; no retroactive migration."}
    if existing and existing["attrs"].get("data-tool-id") != tool_id:
        raise FrameworkError("Route belongs to another tool identity.")
    if structural_check(root, tool_id, "canonical")["status"] != "PASS":
        raise FrameworkError("Canonical tool structural checks must pass.")
    spec = functional_gate(root, tool_id)
    verification = tool.get("verification") or {}
    if verification.get("source_sha256") != spec["source_sha256"]:
        raise FrameworkError("Registry verification does not match current implementation.")
    # Reuse existing evidence/date/revision/link checks; only this tool's pending
    # homepage insertion/count may be absent before the proposal is applied.
    errors = tr.check_project(root, value)["errors"]
    if any(e["code"] not in {"HOMEPAGE_CARDS", "HOMEPAGE_COUNT"} for e in errors):
        raise FrameworkError("Existing consistency/evidence checks failed; resolve them before integration.")
    category = next(c["name"] for c in value["categories"] if c["id"] == tool["category"])
    label = "Live" if tool["status"] == "RELEASED" else "Tested · publication pending"
    card = f'''<a href="{candidate}" data-title="{escape(tool['name'], quote=True)}" data-tool-id="{tool_id}" data-category="{tool['category']}" data-availability="{tool['status'].lower()}" class="tool-card group flex flex-col min-h-80 rounded-2xl border border-slate-800 bg-slate-900/60 hover:border-indigo-400/60 hover:bg-slate-900 p-6" aria-labelledby="tool-{tool_id}-title">
          <p class="text-xs text-indigo-300">{escape(category)} · {label}</p>
          <h3 id="tool-{tool_id}-title" class="mt-4 text-lg font-semibold text-white">{escape(tool['name'])}</h3>
          <p class="mt-3 text-sm leading-6 text-slate-400">{escape(tool['description'])}</p>
          <span class="mt-auto pt-7 text-indigo-300">Open tool →</span>
        </a>'''
    changes = [(existing["start"], existing["end"], card)] if existing else [(home.grid_ends[0], home.grid_ends[0], "  " + card + "\n      ")]
    changes.append((begin, end, f"{len(home.cards) + (0 if existing else 1)} tools ready to use"))
    proposed = source
    for start, stop, replacement in sorted(changes, reverse=True):
        proposed = proposed[:start] + replacement + proposed[stop:]
    patch = "".join(difflib.unified_diff(tr.normalized(source).splitlines(True), tr.normalized(proposed).splitlines(True), fromfile="a/index.html", tofile="b/index.html"))
    return {"tool_id": tool_id, "action": "UPDATE_PROPOSAL" if existing else "ADD_PROPOSAL", "homepage_sha256": tr.normalized_hash(source), "source_sha256": spec["source_sha256"], "patch": patch, "notice": "Review and apply separately. This command does not modify navigation, status, push or deploy."}
