"""Launcher process/shortcut tests. Graphical interaction is tested separately."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import status_launcher as launcher
import install_status_shortcut as installer
import windows_shortcuts as shell


class LauncherTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="edb-launcher-tests-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "project with spaces café"
        (self.root / "scripts").mkdir(parents=True)

    def script(self, content):
        (self.root / "scripts/project_status.py").write_text(content, encoding="utf-8")

    def test_command_uses_absolute_paths(self):
        self.script("print('ok')")
        command = launcher.status_command(self.root)
        self.assertEqual(Path(command[0]), Path(sys.executable).resolve())
        self.assertEqual(Path(command[2]), self.root / "scripts/project_status.py")
        self.assertEqual(command[1], "-u")

    def test_pythonw_maps_to_same_installation_console_interpreter(self):
        python = Path(sys.executable)
        if sys.platform != "win32":
            self.skipTest("Windows interpreter pair")
        self.assertEqual(launcher.console_python(python.with_name("pythonw.exe")), python.resolve())

    def test_missing_script_returns_clear_error(self):
        events = []
        launcher.run_status(self.root, events.append)
        self.assertEqual(events[-1][0], "error")
        self.assertIn("Project status script not found", events[-1][1])

    def test_missing_interpreter_is_clear(self):
        self.script("print('ok')")
        with self.assertRaises(FileNotFoundError):
            launcher.status_command(self.root, self.root / "missing-python.exe")

    def test_cwd_unicode_and_combined_output(self):
        self.script("import os,sys\nprint('root=' + os.getcwd())\nprint('Unicode: café → ready')\nprint('stderr line',file=sys.stderr)\n")
        events = []
        launcher.run_status(self.root, events.append)
        output = "".join(value for kind, value in events if kind == "output")
        self.assertIn(str(self.root), output)
        self.assertIn("café → ready", output)
        self.assertIn("stderr line", output)
        self.assertEqual(events[-1], ("finished", 0))

    def test_nonzero_exit_is_preserved(self):
        self.script("print('Deliberate fixture error')\nraise SystemExit(3)\n")
        events = []
        launcher.run_status(self.root, events.append)
        self.assertEqual(events[-1], ("finished", 3))
        self.assertIn("Deliberate fixture error", events[0][1])

    def test_worker_streams_before_process_finishes(self):
        self.script("import time\nprint('started',flush=True)\ntime.sleep(.4)\nprint('finished')\n")
        first_output = threading.Event()
        events = []
        def emit(value):
            events.append(value)
            if value[0] == "output":
                first_output.set()
        worker = threading.Thread(target=launcher.run_status, args=(self.root, emit))
        worker.start()
        self.assertTrue(first_output.wait(5))
        self.assertTrue(worker.is_alive())
        worker.join(10)
        self.assertFalse(worker.is_alive())
        self.assertEqual(events[-1], ("finished", 0))

    def test_windows_process_has_no_console_and_no_shell(self):
        self.script("print('ok')")
        with patch.object(launcher.subprocess, "Popen", wraps=subprocess.Popen) as start:
            launcher.run_status(self.root, lambda value: None)
        kwargs = start.call_args.kwargs
        self.assertNotIn("shell", kwargs)
        if sys.platform == "win32":
            self.assertEqual(kwargs["creationflags"], subprocess.CREATE_NO_WINDOW)
        self.assertEqual(kwargs["cwd"], self.root)

    def test_open_folder_uses_windows_shell(self):
        with patch.object(launcher.os, "startfile", create=True) as open_file, patch.object(launcher.sys, "platform", "win32"):
            launcher.open_folder(self.root)
            open_file.assert_called_once_with(str(self.root))

    def test_missing_reports_folder_has_helpful_error(self):
        with self.assertRaises(FileNotFoundError):
            launcher.open_folder(self.root / "reports")

    @unittest.skipUnless(sys.platform == "win32", "Native Windows COM shortcut test")
    def test_shortcuts_roundtrip_idempotent_and_safe(self):
        self.script("print('ok')")
        (self.root / "scripts/status_launcher.pyw").write_text("# fixture\n", encoding="utf-8")
        desktop, programs = self.root / "Desktop", self.root / "Programs"
        results = installer.install(self.root, desktop=desktop, programs=programs)
        self.assertEqual(len(results), 2)
        for result in results:
            details = shell.read_shortcut(result["path"])
            self.assertEqual(details["app_id"], shell.APP_ID)
            self.assertEqual(Path(details["working_directory"]), self.root)
            self.assertIn('"', details["arguments"])
            self.assertEqual(Path(details["target"]).name, "pythonw.exe")
        self.assertEqual(len(installer.install(self.root, desktop=desktop, programs=programs)), 2)
        conflict = self.root / "unrelated.lnk"
        conflict.write_bytes(b"not a shell shortcut")
        before = conflict.read_bytes()
        with self.assertRaises(OSError):
            shell.write_shortcut(conflict, Path(sys.executable), "", self.root)
        self.assertEqual(conflict.read_bytes(), before)

    @unittest.skipUnless(sys.platform == "win32", "Windows known folders")
    def test_desktop_known_folder_is_absolute(self):
        self.assertTrue(shell.known_folder("desktop").is_absolute())


if __name__ == "__main__":
    unittest.main()
