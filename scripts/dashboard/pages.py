"""Dashboard screens. All methods execute on the Tk main thread."""
import tkinter as tk
from tkinter import ttk

import tracking as tr
from .data import DOCS, UNAVAILABLE_TESTS, blockers, dependency_issues, filter_tools, milestone_progress, queue_order, strings, text
from .widgets import ACCENT, FG, MUTED, PANEL, ReadOnlyText, ScrollableBody, Table


def heading(parent, title, subtitle):
    ttk.Label(parent, text=title, style="Heading.TLabel").pack(anchor="w")
    ttk.Label(parent, text=subtitle, style="Muted.TLabel", wraplength=740).pack(anchor="w", pady=(4, 12))


def tool_details(tool, snapshot):
    deps = strings(tool.get("dependencies")) + ["tool:" + item for item in strings(tool.get("depends_on"))]
    waiting = dependency_issues(tool, snapshot.tools)
    fields = [("Tool", f"{tool['name']} ({tool['id']})"), ("Description", text(tool.get("description"))), ("Category", snapshot.categories.get(tool["category"], tool["category"])), ("Status", tool["status"]), ("Priority / complexity", f"{text(tool.get('priority'))} / {text(tool.get('implementation_complexity'))}"), ("Dependencies", "; ".join(deps) or "None documented"), ("Implementation notes", text(tool.get("notes"))), ("Testing status", text(tool.get("testing_status"))), ("Last verification", text(tool.get("last_verification_date"), "Not verified")), ("Directory", text(tool.get("directory_path"))), ("Known blockers", text(tool.get("blocker_reason"), text(tool.get("notes"), "Reason not documented.")) if tool["status"] == "BLOCKED" else "; ".join(waiting) or "None documented")]
    return "\n\n".join(f"{label}: {value}" for label, value in fields)


class Overview(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        scroller = ScrollableBody(self)
        scroller.pack(fill="both", expand=True)
        body = scroller.body
        heading(body, "Project overview", "Live registry inventory • local validation snapshots • released tools drive milestone progress")
        cards = ttk.Frame(body)
        cards.pack(fill="x")
        self.values = {}
        for index, (key, label) in enumerate((("total", "Registered"), ("released", "Released"), ("tested", "Tested"), ("implemented", "Implemented"), ("in_progress", "In progress"), ("ready", "Ready"), ("planned", "Planned"), ("blocked", "Blocked"))):
            cards.columnconfigure(index % 4, weight=1)
            card = tk.Frame(cards, background=PANEL, highlightbackground="#334155", highlightthickness=1, padx=12, pady=9)
            card.grid(row=index // 4, column=index % 4, sticky="nsew", padx=(0, 8), pady=(0, 8))
            tk.Label(card, text=label, bg=PANEL, fg=MUTED, font=("Segoe UI", 9)).pack(anchor="w")
            value = tk.StringVar(value="—")
            tk.Label(card, textvariable=value, bg=PANEL, fg=FG, font=("Segoe UI", 23, "bold")).pack(anchor="w")
            self.values[key] = value
        bottom = ttk.Frame(body)
        bottom.pack(fill="both", expand=True, pady=(10, 0))
        bottom.columnconfigure(0, weight=1)
        bottom.columnconfigure(1, weight=1)
        bottom.rowconfigure(1, weight=1, minsize=270)
        ttk.Label(bottom, text="RELEASE MILESTONES", style="Heading.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 8))
        ttk.Label(bottom, text="PROJECT SNAPSHOT", style="Heading.TLabel").grid(row=0, column=1, sticky="w", padx=(14, 0), pady=(0, 8))
        bars = ttk.Frame(bottom)
        bars.grid(row=1, column=0, sticky="new")
        bars.columnconfigure(1, weight=1)
        self.milestones = []
        for row, (goal, _) in enumerate(milestone_progress(0)):
            ttk.Label(bars, text=f"{goal:,}", width=7).grid(row=row, column=0, sticky="w", pady=6)
            bar = ttk.Progressbar(bars, maximum=100)
            bar.grid(row=row, column=1, sticky="ew", padx=8)
            label = ttk.Label(bars, text="—", width=15)
            label.grid(row=row, column=2, sticky="e")
            self.milestones.append((bar, label))
        self.info = ReadOnlyText(bottom, height=8)
        self.info.grid(row=1, column=1, sticky="nsew", padx=(14, 0))

    def update(self, snapshot):
        for key, variable in self.values.items():
            variable.set(f"{snapshot.counts[key]:,}")
        released = snapshot.counts["released"]
        for (goal, percent), (bar, label) in zip(milestone_progress(released), self.milestones):
            bar["value"] = percent
            label.configure(text=f"{released}/{goal:,} · {percent:.1f}%")
        next_item = next(iter(queue_order(snapshot.tools)), None)
        status = next((r for r in snapshot.reports if r.name == "project-status"), None)
        successful = status.generated_at if status and status.state == "PASS" else "Unavailable for current inputs"
        times = [r.generated_at for r in snapshot.reports if r.payload]
        recent = sorted((t for t in snapshot.tools if t.get("last_verification_date")), key=lambda t: t["last_verification_date"], reverse=True)[:4]
        self.info.set(f"Current milestone: {snapshot.counts['milestone'] or 'Review required'} released tools\n\nNext ready utility: {next_item['name'] if next_item else 'None'}\nOwner-directed next major task: {snapshot.next_action}\n\nLast successful validation (current inputs): {successful}\nLast report generation: {max(times) if times else 'Unavailable'}\nLoaded: {snapshot.loaded_at}\n\nRecent registry verification records:\n" + "\n".join(f"• {t['name']} — {t['status']} ({t['last_verification_date']})" for t in recent) + "\n\nRecorded verification dates are historical evidence, not tests run by this dashboard.")


class Registry(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app, self.snapshot, self.pending = app, None, None
        self.sort_key, self.reverse = "name", False
        heading(self, "Tool registry", "Read-only inventory. Select a row for details; click a column heading to sort.")
        controls = ttk.Frame(self)
        controls.pack(fill="x", pady=(0, 8))
        self.query, self.category, self.status, self.priority = (tk.StringVar(value=v) for v in ("", "All", "All", "All"))
        ttk.Label(controls, text="Search name / ID").grid(row=0, column=0, sticky="w")
        ttk.Label(controls, text="Category").grid(row=0, column=1, sticky="w", padx=8)
        ttk.Label(controls, text="Status").grid(row=0, column=2, sticky="w")
        ttk.Label(controls, text="Priority").grid(row=0, column=3, sticky="w", padx=8)
        controls.columnconfigure(0, weight=1)
        ttk.Entry(controls, textvariable=self.query, width=18).grid(row=1, column=0, sticky="ew")
        self.categories = ttk.Combobox(controls, textvariable=self.category, state="readonly", width=20, values=["All"])
        self.categories.grid(row=1, column=1, padx=8)
        ttk.Combobox(controls, textvariable=self.status, state="readonly", width=14, values=["All", *tr.STATUSES]).grid(row=1, column=2)
        ttk.Combobox(controls, textvariable=self.priority, state="readonly", width=6, values=["All", "P1", "P2", "P3"]).grid(row=1, column=3, padx=8)
        self.count = ttk.Label(self, style="Muted.TLabel")
        self.count.pack(anchor="w", pady=(0, 5))
        split = ttk.Panedwindow(self, orient="vertical")
        split.pack(fill="both", expand=True)
        self.table = Table(split, [("id", "Tool ID", 170), ("name", "Tool name", 310), ("category", "Category", 160), ("status", "Status", 110), ("priority", "Priority", 85), ("implementation_complexity", "Complexity", 95), ("dependencies", "Dependencies", 300), ("directory_path", "Directory", 180), ("last_verification_date", "Last verified", 120)], select=self.select, sort=self.sort)
        self.details = ReadOnlyText(split, height=6)
        self.details.set("Select a tool to inspect its documented scope, testing status and blockers.")
        split.add(self.table, weight=3)
        split.add(self.details, weight=2)
        for var in (self.query, self.category, self.status, self.priority):
            var.trace_add("write", self.schedule)

    def schedule(self, *_):
        if self.pending:
            self.after_cancel(self.pending)
        self.pending = self.after(150, self.render)

    def sort(self, key):
        self.reverse = not self.reverse if self.sort_key == key else False
        self.sort_key = key
        self.render()

    def update(self, snapshot):
        self.snapshot = snapshot
        self.categories["values"] = ["All", *snapshot.categories.values()]
        if self.category.get() not in self.categories["values"]:
            self.category.set("All")
        self.render()

    def render(self):
        self.pending = None
        if not self.snapshot:
            return
        category = next((k for k, v in self.snapshot.categories.items() if v == self.category.get()), "All")
        rows = filter_tools(self.snapshot.tools, self.query.get(), category, self.status.get(), self.priority.get(), self.sort_key, self.reverse)
        self.count.configure(text=f"{len(rows):,} of {len(self.snapshot.tools):,} tools • sorted by {self.sort_key} {'↓' if self.reverse else '↑'}")
        self.table.render([(t["id"], (t["id"], t["name"], self.snapshot.categories.get(t["category"], t["category"]), t["status"], text(t.get("priority"), "—"), text(t.get("implementation_complexity"), "—"), "; ".join(t["dependencies"] + ["tool:" + d for d in t["depends_on"]]) or "—", text(t.get("directory_path"), "—"), text(t.get("last_verification_date"), "Not verified")), ("blocked",) if t["status"] == "BLOCKED" else ()) for t in rows])

    def select(self, tool_id):
        tool = next((t for t in self.snapshot.tools if t["id"] == tool_id), None)
        if tool:
            self.details.set(tool_details(tool, self.snapshot))


class DevelopmentQueue(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.snapshot = None
        heading(self, "Development queue", "Existing sequence_rank → priority → tool ID. READY dependencies must be TESTED or RELEASED. No new scoring or automatic implementation.")
        self.recommendation = ttk.Label(self, foreground=ACCENT, wraplength=750)
        self.recommendation.pack(anchor="w", pady=(0, 8))
        split = ttk.Panedwindow(self, orient="vertical")
        split.pack(fill="both", expand=True)
        tabs = ttk.Notebook(split)
        split.add(tabs, weight=3)
        self.tables = {}
        for title in ("Next 20", "Ready", "Planned", "In progress", "Dependencies"):
            table = Table(tabs, [("name", "Tool name", 240), ("category", "Category", 160), ("priority", "Priority", 80), ("complexity", "Complexity", 90), ("readiness", "Readiness", 110), ("dependencies", "Dependencies", 290), ("blockers", "Blocking issues", 340)], select=self.select)
            tabs.add(table, text=title)
            self.tables[title] = table
        self.details = ReadOnlyText(split, height=5)
        split.add(self.details, weight=1)

    def update(self, snapshot):
        self.snapshot = snapshot
        ordered = queue_order(snapshot.tools)
        by_id = {t["id"]: t for t in snapshot.tools}
        waiting = {t["id"]: dependency_issues(t, by_id) for t in snapshot.tools}
        next_id = ordered[0]["id"] if ordered else None
        self.recommendation.configure(text=f"Next ready utility: {ordered[0]['name'] if ordered else 'None'} • Next major task: {snapshot.next_action}")
        groups = {"Next 20": ordered[:20], "Ready": ordered, "Planned": sorted((t for t in snapshot.tools if t["status"] == "PLANNED"), key=lambda t: (t.get("priority", ""), t["name"])), "In progress": [t for t in snapshot.tools if t["status"] == "IN_PROGRESS"], "Dependencies": [t for t in snapshot.tools if waiting[t["id"]]]}
        for title, tools in groups.items():
            self.tables[title].render([(t["id"], (t["name"], snapshot.categories.get(t["category"], t["category"]), text(t.get("priority")), text(t.get("implementation_complexity")), t["status"], "; ".join(t["dependencies"] + ["tool:" + d for d in t["depends_on"]]) or "None documented", "; ".join(waiting[t["id"]]) or "None documented"), ("next",) if t["id"] == next_id else ()) for t in tools])
        self.details.set("Select a row for implementation notes and blockers. Planned entries have no sequence unless documented; their display order is priority then name, not a new readiness score.")

    def select(self, tool_id):
        tool = next((t for t in self.snapshot.tools if t["id"] == tool_id), None)
        if tool:
            self.details.set(tool_details(tool, self.snapshot))


class Validation(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.snapshot = None
        heading(self, "Testing & validation", "PASS / FAIL / WARNING are recorded outcomes. STALE, NOT RUN and UNKNOWN describe evidence availability. Structural checks do not run functional tests.")
        split = ttk.Panedwindow(self, orient="vertical")
        self.table = Table(split, [("check", "Check", 180), ("state", "Current state", 115), ("recorded", "Recorded result", 120), ("time", "Generated (UTC)", 220)], select=self.select)
        ttk.Label(self, text="PYTHON / NODE FUNCTIONAL TESTS", style="Heading.TLabel").pack(anchor="w", pady=(14, 4))
        ttk.Label(self, text=UNAVAILABLE_TESTS, foreground="#fbbf24").pack(anchor="w", pady=(0, 8))
        split.pack(fill="both", expand=True)
        self.details = ReadOnlyText(split, height=8)
        split.add(self.table, weight=2)
        split.add(self.details, weight=3)

    def update(self, snapshot):
        self.snapshot = snapshot
        self.table.render([(r.name, (r.name, r.state, r.recorded, r.generated_at), ()) for r in snapshot.reports])
        self.details.set("Select a check to inspect diagnostics, affected files, timestamps and available corrective guidance.\n\n" + "\n\n".join(snapshot.issues) if snapshot.issues else "Select a check to inspect its diagnostics and freshness. Test counts are unavailable because Task 2 reports do not record test-run totals. Historical handoff counts are not current test results.")

    def select(self, name):
        report = next(r for r in self.snapshot.reports if r.name == name)
        lines = [f"{name}: {report.state} (recorded: {report.recorded})", f"Report generation / recorded execution: {report.generated_at}", report.reason, "Execution duration: not recorded by the existing report schema."]
        for severity in ("errors", "warnings"):
            entries = report.payload.get(severity, [])
            lines.append(f"\n{severity.upper()}: {len(entries)}")
            for item in entries:
                lines.append("\n" + "\n".join(f"{k}: {v}" for k, v in item.items()))
        info = report.payload.get("information", [])
        if isinstance(info, list):
            lines += ["\n" + str(v) for v in info]
        details = report.payload.get("details", {})
        if isinstance(details, dict):
            import json
            lines.append("\nReport details (static check scope):\n" + json.dumps(details, indent=2, ensure_ascii=False))
        self.details.set("\n".join(lines))


class Activity(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        heading(self, "Project activity", "Local Git observations and saved project memory. Push and deployment are not verified by this offline application.")
        self.git = ttk.Label(self, wraplength=760, foreground=ACCENT)
        self.git.pack(anchor="w", pady=(0, 8))
        actions = ttk.Frame(self)
        actions.pack(fill="x", pady=(0, 8))
        for index, name in enumerate(DOCS):
            ttk.Button(actions, text=name.removesuffix(".md"), command=lambda n=name: app.open_path(n)).grid(row=index // 2, column=index % 2, sticky="w", padx=(0, 8), pady=3)
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True)
        self.documents = {}
        for name in DOCS:
            view = ReadOnlyText(self.tabs, height=10)
            self.tabs.add(view, text={"SESSION_HANDOFF.md": "Session handoff", "CHANGELOG.md": "Changelog", "ROADMAP.md": "Roadmap", "PROJECT_MASTER_PLAN.md": "Master plan"}[name])
            self.documents[name] = view

    def update(self, snapshot):
        git = snapshot.git
        self.git.configure(text=f"Branch: {git.get('branch', 'UNKNOWN')}  •  Working tree: {git.get('working_tree', 'UNKNOWN')}\nLatest commit: {git.get('latest_commit', 'UNKNOWN')}" + ("\n" + git.get("reason", "") if git.get("status") == "UNKNOWN" else "") + f"\nNext major task: {snapshot.next_action}")
        for name, view in self.documents.items():
            view.set(snapshot.documents.get(name, "Unavailable"))


class Blockers(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.snapshot = None
        heading(self, "Blockers", "Only documented reasons and dependencies. This screen never changes registry status.")
        split = ttk.Panedwindow(self, orient="vertical")
        split.pack(fill="both", expand=True)
        self.table = Table(split, [("id", "Tool ID", 170), ("name", "Name", 200), ("category", "Category", 160), ("reason", "Documented reason", 520)], select=self.select)
        self.details = ReadOnlyText(split, height=9)
        split.add(self.table, weight=2)
        split.add(self.details, weight=3)

    def update(self, snapshot):
        self.snapshot = snapshot
        items = blockers(snapshot.tools)
        self.table.render([(t["id"], (t["id"], t["name"], snapshot.categories.get(t["category"], t["category"]), reason), ("blocked",)) for t, reason in items])
        self.details.set(f"{len(items)} blocked tools. Select a row for dependencies and documented decisions." if items else "No tools are currently marked BLOCKED.")

    def select(self, tool_id):
        tool = next(t for t in self.snapshot.tools if t["id"] == tool_id)
        self.details.set(tool_details(tool, self.snapshot) + "\n\nRequired decision / action: " + text(tool.get("required_action"), "See the documented reason above; no separate action field is recorded."))
