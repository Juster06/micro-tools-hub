"""Responsive, local Tk interface to the existing project_status.py command."""
from __future__ import annotations

import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import queue
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import ttk

from windows_shortcuts import APP_TITLE, set_process_identity

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def console_python(executable=None):
    python = Path(executable or sys.executable).resolve()
    if python.name.casefold() == "pythonw.exe":
        python = python.with_name("python.exe")
    if not python.is_file():
        raise FileNotFoundError("Python interpreter not found. Repair Python or recreate the desktop shortcut.")
    return python


def status_command(project_root, executable=None):
    project_root = Path(project_root).resolve()
    script = project_root / "scripts" / "project_status.py"
    if not script.is_file():
        raise FileNotFoundError(f"Project status script not found: {script}. Open the correct checkout or recreate the shortcut.")
    return [str(console_python(executable)), "-u", str(script)]


def run_status(project_root, emit, executable=None):
    """Worker-only I/O. Emit events; never touch Tk from the background thread."""
    try:
        root = Path(project_root).resolve()
        command = status_command(root, executable)
        environment = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
        flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        with subprocess.Popen(command, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace", bufsize=1, env=environment, creationflags=flags) as process:
            for line in process.stdout:
                emit(("output", line))
            code = process.wait()
        emit(("finished", code))
    except (OSError, ValueError) as exc:
        emit(("error", f"Could not run project checks: {exc}"))


def open_folder(path):
    path = Path(path).resolve()
    if not path.is_dir():
        raise FileNotFoundError(f"Folder is not available yet: {path}")
    if sys.platform != "win32":
        raise OSError("Open Folder buttons require Windows.")
    os.startfile(str(path))


class StatusLauncher:
    """Project context and action handlers can later host a dashboard-opening action."""
    def __init__(self, window, project_root=PROJECT_ROOT):
        self.window = window
        self.project_root = Path(project_root).resolve()
        self.events = queue.Queue()
        self.busy = False
        self.runs = 0
        self.closed = False
        window.title(APP_TITLE)
        window.geometry("880x590")
        window.minsize(650, 440)
        window.configure(bg="#020617")
        style = ttk.Style(window)
        style.theme_use("clam")
        style.configure("EDB.TFrame", background="#020617")
        style.configure("EDB.TLabel", background="#020617", foreground="#e2e8f0", font=("Segoe UI", 10))
        style.configure("Title.EDB.TLabel", font=("Segoe UI", 18, "bold"))
        style.configure("EDB.TButton", background="#1e293b", foreground="#e2e8f0", padding=(12, 9), font=("Segoe UI", 10))
        style.map("EDB.TButton", background=[("active", "#334155")], foreground=[("disabled", "#64748b")])
        style.configure("Primary.EDB.TButton", background="#4f46e5")
        style.configure("EDB.Horizontal.TProgressbar", troughcolor="#0f172a", background="#818cf8", bordercolor="#020617")
        frame = ttk.Frame(window, style="EDB.TFrame", padding=22)
        frame.pack(fill="both", expand=True)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(5, weight=1)
        ttk.Label(frame, text="Everyday Digital Box", style="Title.EDB.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(frame, text="PROJECT STATUS", style="EDB.TLabel", foreground="#a5b4fc").grid(row=1, column=0, sticky="w", pady=(2, 12))
        self.project_label = ttk.Label(frame, text=f"Project: {self.project_root}", style="EDB.TLabel", wraplength=820)
        self.project_label.grid(row=2, column=0, sticky="ew")
        frame.bind("<Configure>", lambda event: self.project_label.configure(wraplength=max(200, event.width - 44)))
        self.status = tk.StringVar(value="Preparing project checks…")
        self.status_label = ttk.Label(frame, textvariable=self.status, style="EDB.TLabel", foreground="#a5b4fc")
        self.status_label.grid(row=3, column=0, sticky="w", pady=(12, 6))
        self.progress = ttk.Progressbar(frame, mode="indeterminate", style="EDB.Horizontal.TProgressbar")
        self.progress.grid(row=4, column=0, sticky="ew", pady=(0, 12))
        results = ttk.Frame(frame, style="EDB.TFrame")
        results.grid(row=5, column=0, sticky="nsew")
        self.output = tk.Text(results, width=1, height=1, wrap="word", bg="#0f172a", fg="#e2e8f0", insertbackground="#e2e8f0", selectbackground="#4338ca", font=("Consolas", 10), relief="flat", padx=12, pady=12, state="disabled", takefocus=True)
        scrollbar = ttk.Scrollbar(results, orient="vertical", command=self.output.yview)
        self.output.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.output.pack(side="left", fill="both", expand=True)
        actions = ttk.Frame(frame, style="EDB.TFrame")
        actions.grid(row=6, column=0, sticky="ew", pady=(14, 8))
        self.run_button = ttk.Button(actions, text="Run Again", command=self.run_again, style="Primary.EDB.TButton")
        self.run_button.pack(side="left")
        ttk.Button(actions, text="Open Reports", command=lambda: self.open_path(self.project_root / "reports"), style="EDB.TButton").pack(side="left", padx=8)
        ttk.Button(actions, text="Open Project Folder", command=lambda: self.open_path(self.project_root), style="EDB.TButton").pack(side="left")
        ttk.Button(actions, text="Close", command=self.close, style="EDB.TButton").pack(side="right")
        ttk.Label(frame, text="Checks refresh generated project notes and local reports.", style="EDB.TLabel", foreground="#94a3b8").grid(row=7, column=0, sticky="w")
        window.protocol("WM_DELETE_WINDOW", self.close)
        window.bind("<Escape>", lambda _: self.close())
        window.after(100, self.pump)
        window.after(150, self.run_again)

    def append(self, text):
        self.output.configure(state="normal")
        self.output.insert("end", text)
        # Bound the view, not the underlying tracking reports.
        if int(self.output.index("end-1c").split(".")[0]) > 4000:
            self.output.delete("1.0", "1000.0")
        self.output.see("end")
        self.output.configure(state="disabled")

    def run_again(self):
        if self.busy:
            return
        self.busy = True
        self.runs += 1
        self.run_button.state(["disabled"])
        self.status.set(f"Running project checks… (run {self.runs})")
        self.status_label.configure(foreground="#a5b4fc")
        self.progress.start(12)
        self.append(f"\n── Run {self.runs} · {datetime.now().strftime('%H:%M:%S')} ──\n")
        self.append(f"Project: {self.project_root}\n")
        # Non-daemon worker lets an already-started write finish safely if the
        # window is closed. It only emits queue events and never calls Tk.
        threading.Thread(target=run_status, args=(self.project_root, self.events.put), daemon=False).start()

    def finish(self, code=None, error=None):
        self.busy = False
        self.run_button.state(["!disabled"])
        self.progress.stop()
        self.progress["value"] = 0
        if error:
            self.append(error + "\n")
        succeeded = error is None and code == 0
        warning = False
        if succeeded:
            try:
                warning = json.loads((self.project_root / "reports" / "project-status.json").read_text(encoding="utf-8"))["status"] == "WARN"
            except (OSError, ValueError, KeyError, TypeError):
                pass
        label = "Completed with warnings" if warning else "Succeeded" if succeeded else "Failed"
        self.status.set(f"{label} — run {self.runs}" + (f" · exit code {code}" if code is not None else ""))
        self.status_label.configure(foreground="#fbbf24" if warning else "#6ee7b7" if succeeded else "#fda4af")

    def pump(self):
        if self.closed:
            return
        for _ in range(200):
            try:
                kind, value = self.events.get_nowait()
            except queue.Empty:
                break
            if kind == "output":
                self.append(value)
            elif kind == "finished":
                self.finish(code=value)
            elif kind == "error":
                self.finish(error=value)
        self.window.after(80, self.pump)

    def open_path(self, path):
        try:
            open_folder(path)
        except OSError as exc:
            self.append(f"Could not open folder: {exc}\n")
            if not self.busy:
                self.status.set("Folder unavailable — see output")
                self.status_label.configure(foreground="#fbbf24")

    def close(self):
        self.closed = True
        self.window.destroy()


def main():
    parser = argparse.ArgumentParser(description="Local project-status GUI; no public website changes.")
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    args = parser.parse_args()
    try:
        set_process_identity()
    except OSError:
        pass  # Taskbar grouping should never prevent the checks from running.
    window = tk.Tk()
    StatusLauncher(window, args.project_root)
    window.mainloop()


if __name__ == "__main__":
    main()
