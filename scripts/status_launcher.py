"""Responsive, local Tk interface to the existing project_status.py command."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys
import tkinter as tk

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


def run_status(project_root, emit, executable=None, environment=None):
    """Worker-only I/O. Emit events; never touch Tk from the background thread."""
    try:
        root = Path(project_root).resolve()
        command = status_command(root, executable)
        environment = {**(os.environ if environment is None else environment), "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
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


# Preserve the installed entry point and launcher API; presentation is modular.
from dashboard.app import Dashboard

StatusLauncher = Dashboard


def main():
    parser = argparse.ArgumentParser(description="Local project-status GUI; no public website changes.")
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--no-auto-refresh", action="store_true", help="Load saved snapshots without running the workflow on startup.")
    args = parser.parse_args()
    try:
        set_process_identity()
    except OSError:
        pass  # Taskbar grouping should never prevent the checks from running.
    window = tk.Tk()
    StatusLauncher(window, args.project_root, auto_refresh=not args.no_auto_refresh)
    window.mainloop()


if __name__ == "__main__":
    main()
