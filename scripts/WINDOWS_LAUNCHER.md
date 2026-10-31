# Windows Project Status launcher

The launcher is a local desktop interface to the existing tracking command. It is separate from the public website and does not implement Task 3's Project Control Dashboard.

## Start it

Double-click **Everyday Digital Box — Project Status** on the desktop. The shortcut opens a small Tkinter window, automatically runs the checks, streams output into a scrollable view, and displays success, warnings or failure. **Run Again**, **Open Reports**, **Open Project Folder**, and **Close** are available.

The source entry point is `<active-checkout>/scripts/status_launcher.pyw`. It can also be started explicitly:

```powershell
pythonw "C:\path\to\checkout\scripts\status_launcher.pyw"
```

No PowerShell/console window is opened during shortcut launches or status subprocess execution. The child uses the same Python installation's console interpreter with CREATE_NO_WINDOW, absolute script paths, the project root as its working directory, UTF-8 output, and no shell command string.

The project root defaults to the launcher's own repository directory, regardless of the caller's working directory. It is shown inside the GUI. An optional `--project-root PATH` exists for explicit alternate contexts/testing; the installed shortcut points to the active checkout containing this launcher, not an older downloaded non-Git copy.

## Create or recreate shortcuts

From the intended checkout:

```powershell
python scripts/install_status_shortcut.py
```

Or, from any other directory:

```powershell
python "C:\path\to\checkout\scripts\install_status_shortcut.py"
```

The standard-library installer creates and reads back two current-user `.lnk` files: one on the Desktop and one in Start Menu → Programs. Windows Known Folder APIs locate the actual Desktop, including redirected/OneDrive desktops. The Start menu entry supports discovery and manual pinning. Neither shortcut requires administrator rights.

Each shortcut records the absolute `pythonw.exe` target, absolute launcher argument, project working directory, Python's default icon, and matching `EverydayDigitalBox.ProjectStatus` AppUserModelID. The installer verifies these fields before replacing the destination, and only updates shortcuts identified as its own. An unrelated same-name shortcut is refused. Re-running is supported.

No shortcut files, machine-specific paths, or installation receipts are committed to Git. The installer prints the actual installed locations. Moving the checkout, removing/switching away from the launcher files, or moving Python invalidates an existing shortcut; rerun installation from the intended checkout after such changes.

## Pin to the taskbar

1. Open the desktop shortcut.
2. Right-click its running taskbar icon and choose **Pin to taskbar**.

Alternatively, find **Everyday Digital Box — Project Status** in Start, right-click it, and use **More → Pin to taskbar** or **Show more options → Pin to taskbar**, depending on the Windows version/menu.

The launcher and shortcut share an explicit AppUserModelID so Windows can associate the window with the correct shortcut and arguments. No taskbar settings, registry pin data, taskbar files, or undocumented pinning verbs are modified. Pinning is a user action and may be unavailable under a Windows policy. If the option is unavailable, the verified desktop shortcut still works. No claim is made that a taskbar pin was installed or tested automatically.

Sources: [Microsoft taskbar instructions](https://support.microsoft.com/en-us/windows/experience/personalization/customize-the-taskbar-in-windows), [Microsoft AppUserModelID guidance](https://learn.microsoft.com/en-us/windows/win32/shell/appids).

## Dependencies and behavior

- Windows 10/11 desktop environment, with Python 3.10+ and Tcl/Tk (Tkinter). Tested here using Windows desktop Python 3.14.4 and Tk 8.6.
- `python.exe` and `pythonw.exe` from the same Python installation.
- Python standard library only: Tkinter, subprocess, threading/queue, pathlib and ctypes Windows Shell/COM calls. No paid software, third-party packages, external API, server or admin privileges.
- Existing `scripts/project_status.py`, registry and project-management files remain the source of behavior.

The window runs child I/O on a background worker and polls a queue on the Tk thread. Run Again is disabled during a run; folder controls stay usable. The view is capped at 4,000 lines, while the existing JSON reports are maintained by the tracking command. Closing during a run closes the window and lets the already-started child finish in the background, avoiding interruption of documentation writes. There is no cancellation button or forced termination.

The status command deliberately updates generated project notes and ignored local reports. Success means the command returned zero; a WARN report is labeled “Completed with warnings”. Nonzero exit codes and launch errors remain visible. Output is not uploaded or logged to an external service. Do not run multiple tracking writers/windows against the same checkout at once; there is no global cross-process lock in the existing engine.

## Testing and future extension

```sh
python -m unittest discover -s tests -v
node --test scripts/project.test.mjs
python scripts/project_status.py --check-only
```

Tests include streaming output, error/exit propagation, Unicode and paths with spaces, working-directory independence, no-console subprocess flags, Windows shortcut round trips, idempotent installation, refusal to overwrite unrelated files, and existing management regressions. Tests use temporary fixtures.

Actual GUI testing also launched the installed desktop shortcut, inspected output and layout, used Run Again, opened both folders, closed the window, and exercised responsiveness plus an explicit nonzero error with an isolated slow fixture. Initial layout clipping at the host's display scale was corrected before completing these tests. Taskbar pinning itself remains a manual action and was not changed during testing.

`StatusLauncher` keeps its project context, worker, output view and action handlers separate. Task 3 can add a dashboard-opening action later. No dashboard, embedded browser, HTTP server, new public tool, or new registry utility is introduced here.
