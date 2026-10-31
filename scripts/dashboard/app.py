"""Main-thread dashboard coordinator and explicit user actions."""
from datetime import datetime
import queue
import tkinter as tk
from tkinter import filedialog, ttk

from .data import summary_text
from .operations import BackgroundJobs, open_local, save_git_setting
from .pages import Activity, Blockers, DevelopmentQueue, Overview, Registry, Validation, heading
from .widgets import ACCENT, BG, ReadOnlyText, configure_style


class QuickActions(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        heading(self, "Quick actions & command output", "Refresh runs the existing workflow and updates generated notes/reports. All operations stay local.")
        actions = ttk.Frame(self)
        actions.pack(fill="x", pady=(0, 10))
        for index, (label, command) in enumerate((("Open Reports", lambda: app.open_path("reports")), ("Open Project Folder", lambda: app.open_path()), ("Open Documentation", lambda: app.open_path("scripts/DASHBOARD.md")), ("Copy Summary", app.copy_summary))):
            ttk.Button(actions, text=label, command=command).grid(row=index // 2, column=index % 2, sticky="ew", padx=(0, 8), pady=3)
            actions.columnconfigure(index % 2, weight=1)
        ttk.Label(self, text="Git executable (optional local setting)", foreground=ACCENT).pack(anchor="w")
        settings = ttk.Frame(self)
        settings.pack(fill="x", pady=(5, 5))
        settings.columnconfigure(0, weight=1)
        self.git_path = tk.StringVar()
        ttk.Entry(settings, textvariable=self.git_path).grid(row=0, column=0, sticky="ew")
        ttk.Button(settings, text="Browse…", command=self.browse).grid(row=0, column=1, padx=6)
        self.save = ttk.Button(settings, text="Save Git Path", command=lambda: app.save_settings(self.git_path.get()))
        self.save.grid(row=0, column=2)
        ttk.Label(self, text="Leave blank for discovery. Saved only under ignored local reports; reload with the button below.", style="Muted.TLabel", wraplength=760).pack(anchor="w")
        self.reload = ttk.Button(self, text="Reload Saved Data", command=app.reload_data)
        self.reload.pack(anchor="w", pady=(8, 8))
        ttk.Label(self, text="COMPLETE OUTPUT — MOST RECENT REFRESH", style="Heading.TLabel").pack(anchor="w", pady=(0, 5))
        self.output = ReadOnlyText(self, height=9)
        self.output.pack(fill="both", expand=True)
        self.output.set("No command has run in this window yet. Refresh Project Status to capture its complete output.")

    def browse(self):
        filename = filedialog.askopenfilename(title="Select Git executable", filetypes=[("Git executable", "git.exe"), ("All files", "*")])
        if filename:
            self.git_path.set(filename)

    def update(self, snapshot):
        self.git_path.set(snapshot.settings.get("git_executable", ""))


class Dashboard:
    def __init__(self, window, project_root=None, auto_refresh=True):
        from pathlib import Path
        self.window, self.project_root = window, Path(project_root or Path(__file__).resolve().parents[2]).resolve()
        self.events, self.snapshot = queue.Queue(), None
        self.jobs = BackgroundJobs(self.project_root, self.events.put)
        self.closed, self.running, self.auto_refresh = False, False, auto_refresh
        self.refresh_result, self.job_error = None, False
        window.title("Everyday Digital Box — Project Control Dashboard")
        width = min(1180, max(750, window.winfo_screenwidth() - 80))
        height = min(740, max(450, window.winfo_screenheight() - 100))
        window.geometry(f"{width}x{height}")
        window.minsize(min(900, width), min(520, height))
        window.configure(bg=BG)
        configure_style(window)
        outer = ttk.Frame(window, padding=18)
        outer.pack(fill="both", expand=True)
        outer.columnconfigure(1, weight=1)
        outer.rowconfigure(1, weight=1)
        header = ttk.Frame(outer)
        header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 16))
        header.columnconfigure(0, weight=1)
        ttk.Label(header, text="Everyday Digital Box", style="Title.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(header, text="PROJECT CONTROL DASHBOARD  /  LOCAL WORKSPACE", foreground=ACCENT).grid(row=1, column=0, sticky="w", pady=(3, 3))
        ttk.Label(header, text=str(self.project_root), style="Muted.TLabel", wraplength=750).grid(row=2, column=0, sticky="w")
        self.refresh_button = ttk.Button(header, text="Refresh Project Status", style="Primary.TButton", command=self.run_again)
        self.refresh_button.grid(row=0, column=1, rowspan=2, sticky="ne", padx=(15, 0))
        sidebar = ttk.Frame(outer)
        sidebar.grid(row=1, column=0, sticky="ns", padx=(0, 18))
        ttk.Label(sidebar, text="WORKSPACE", style="Muted.TLabel").pack(anchor="w", pady=(0, 9))
        self.content = ttk.Frame(outer)
        self.content.grid(row=1, column=1, sticky="nsew")
        self.content.columnconfigure(0, weight=1)
        self.content.rowconfigure(1, weight=1)
        self.notice = tk.StringVar(value="Loading local data…")
        self.notice_label = ttk.Label(self.content, textvariable=self.notice, wraplength=900, foreground="#fbbf24")
        self.notice_label.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        page_host = ttk.Frame(self.content)
        page_host.grid(row=1, column=0, sticky="nsew")
        page_host.columnconfigure(0, weight=1)
        page_host.rowconfigure(0, weight=1)
        self.pages, self.navigation = {}, {}
        for title, screen in (("Overview", Overview), ("Tool Registry", Registry), ("Development Queue", DevelopmentQueue), ("Testing & Validation", Validation), ("Project Activity", Activity), ("Blockers", Blockers), ("Quick Actions", QuickActions)):
            page = screen(page_host, self)
            page.grid(row=0, column=0, sticky="nsew")
            self.pages[title] = page
            button = ttk.Button(sidebar, text=title, style="Nav.TButton", command=lambda n=title: self.show(n), width=22)
            button.pack(fill="x", pady=3)
            self.navigation[title] = button
        ttk.Label(sidebar, text="OFFLINE · READ-ONLY REGISTRY", style="Muted.TLabel", wraplength=170).pack(side="bottom", anchor="w", pady=(15, 0))
        footer = ttk.Frame(outer)
        footer.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(14, 0))
        footer.columnconfigure(0, weight=1)
        self.status = tk.StringVar(value="Preparing workspace…")
        self.status_label = ttk.Label(footer, textvariable=self.status, foreground=ACCENT)
        self.status_label.grid(row=0, column=0, sticky="w")
        ttk.Button(footer, text="View Command Output", command=lambda: self.show("Quick Actions")).grid(row=0, column=1, padx=8)
        ttk.Button(footer, text="Close", command=self.close).grid(row=0, column=2)
        self.progress = ttk.Progressbar(footer, mode="indeterminate")
        self.progress.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(8, 0))
        self.show("Overview")
        window.protocol("WM_DELETE_WINDOW", self.close)
        window.bind("<Escape>", lambda _: self.close())
        window.after(80, self.pump)
        window.after(100, self.reload_data)

    def show(self, title):
        self.pages[title].tkraise()
        for name, button in self.navigation.items():
            button.configure(style="Active.Nav.TButton" if name == title else "Nav.TButton")

    def set_busy(self, busy, label):
        self.running = busy
        self.refresh_button.state(["disabled"] if busy else ["!disabled"])
        quick = self.pages["Quick Actions"]
        for button in (quick.save, quick.reload):
            button.state(["disabled"] if busy else ["!disabled"])
        if busy:
            self.progress.start(15)
        else:
            self.progress.stop()
            self.progress["value"] = 0
        self.status.set(label)

    def reload_data(self):
        if self.running or not self.jobs.start():
            return False
        self.job_error = False
        self.set_busy(True, "Loading saved data…")
        return True

    def run_again(self):
        if self.running or not self.jobs.start(refresh=True):
            return False
        self.refresh_result, self.job_error = None, False
        self.pages["Quick Actions"].output.set(f"Project status refresh · {datetime.now().strftime('%H:%M:%S')}\nProject: {self.project_root}\n\n")
        self.set_busy(True, "Running project checks…")
        return True

    def apply_snapshot(self, snapshot):
        self.snapshot = snapshot
        for page in self.pages.values():
            page.update(snapshot)
        unavailable = [r for r in snapshot.reports if r.state in {"STALE", "UNKNOWN", "NOT RUN", "FAIL", "WARNING"}]
        self.notice.set(f"{len(snapshot.issues)} data issue(s) · {len(unavailable)} check(s) need attention. See Testing & Validation." if snapshot.issues or unavailable else "Registry valid · current validation reports available · functional test results tracked separately")
        self.notice_label.configure(foreground="#fbbf24" if snapshot.issues or unavailable else "#6ee7b7")

    def pump(self):
        if self.closed:
            return
        for _ in range(100):
            try:
                kind, value = self.events.get_nowait()
            except queue.Empty:
                break
            if kind == "output":
                self.pages["Quick Actions"].output.append(value)
            elif kind == "refresh_result":
                self.refresh_result = value
                self.pages["Quick Actions"].output.append(f"\nProcess finished — exit code {value['code'] if value['code'] is not None else 'unavailable'}\n")
            elif kind == "snapshot":
                self.apply_snapshot(value)
            elif kind == "job_error":
                self.job_error = True
                self.notice.set(value.splitlines()[0])
                self.pages["Quick Actions"].output.append("\n" + value + "\n")
                self.show("Quick Actions")
            elif kind == "idle":
                result = self.refresh_result if value else None
                failed = self.job_error or (result is not None and (result["error"] or result["code"] != 0))
                label = (f"Failed — exit code {result['code']} · see output" if result and result["code"] is not None else "Failed — see command output") if failed else "Saved data loaded"
                if value and not failed:
                    state = next((r.state for r in self.snapshot.reports if r.name == "project-status"), "UNKNOWN") if self.snapshot else "UNKNOWN"
                    label = f"Succeeded — exit code 0 · project status {state}"
                self.set_busy(False, label)
                self.status_label.configure(foreground="#fda4af" if failed else ACCENT)
                if self.auto_refresh:
                    self.auto_refresh = False
                    self.window.after(100, self.run_again)
        self.window.after(60, self.pump)

    def open_path(self, relative=None):
        try:
            open_local(self.project_root, relative)
        except (OSError, ValueError) as exc:
            self.action_error(str(exc))

    def action_error(self, message):
        self.notice.set(message)
        self.pages["Quick Actions"].output.append("\nAction failed: " + message + "\n")
        self.show("Quick Actions")

    def copy_summary(self):
        if not self.snapshot:
            self.action_error("Data not loaded yet. Wait for loading to finish.")
            return
        try:
            self.window.clipboard_clear()
            self.window.clipboard_append(summary_text(self.snapshot))
            self.status.set("Project summary copied (no local paths or Git identities)")
        except tk.TclError as exc:
            self.action_error(f"Clipboard unavailable: {exc}")

    def save_settings(self, value):
        if self.running:
            return
        try:
            save_git_setting(self.project_root, value)
            self.status.set("Git path saved locally. Reloading data…")
            self.reload_data()
        except (OSError, ValueError) as exc:
            self.action_error(str(exc))

    def close(self):
        self.closed = True
        # Non-daemon workers retain the refresh lock until their writes complete.
        self.window.destroy()
