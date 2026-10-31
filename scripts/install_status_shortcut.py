"""Install verified current-user Desktop/Start shortcuts; never pin or edit registry."""
import argparse
from pathlib import Path
import subprocess
import sys

from status_launcher import PROJECT_ROOT
from windows_shortcuts import APP_TITLE, known_folder, write_shortcut


def install(project_root=PROJECT_ROOT, executable=None, desktop=None, programs=None):
    if sys.platform != "win32":
        raise OSError("Shortcut installation requires Windows.")
    root = Path(project_root).resolve()
    launcher = root / "scripts" / "status_launcher.pyw"
    if not launcher.is_file() or not (root / "scripts" / "project_status.py").is_file():
        raise FileNotFoundError("Launcher or project_status.py missing. Use the checkout containing Task 2.5.")
    pythonw = Path(executable or sys.executable).resolve()
    if pythonw.name.casefold() != "pythonw.exe":
        pythonw = pythonw.with_name("pythonw.exe")
    if not pythonw.is_file():
        raise FileNotFoundError("pythonw.exe is missing from this Python installation. Install desktop Python with Tcl/Tk.")
    arguments = subprocess.list2cmdline([str(launcher)])
    destinations = [Path(desktop) if desktop is not None else known_folder("desktop"), Path(programs) if programs is not None else known_folder("programs")]
    results = []
    for directory in destinations:
        filename = directory / (APP_TITLE + ".lnk")
        details = write_shortcut(filename, pythonw, arguments, root)
        results.append({"path": str(filename), **details})
    return results


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    args = parser.parse_args()
    try:
        for result in install(args.project_root):
            print("Created and verified:", result["path"])
        print("Launch the shortcut, then right-click its taskbar icon and choose Pin to taskbar.")
    except (OSError, ValueError) as exc:
        print("Shortcut installation failed:", exc, file=sys.stderr)
        raise SystemExit(1)
