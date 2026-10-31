"""Dashboard behavior tests. All registry/report writes use temporary fixtures."""
import copy
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import queue
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import tracking as tr
import status_launcher
from dashboard import data as d, operations as op


def tool(tid="sample", status="READY", rank=1, **extra):
    return {"id": tid, "name": tid.title(), "category": "text", "status": status, "priority": "P1", "sequence_rank": rank, "description": "Fixture scope", "directory_path": tid, "implementation_complexity": "S", "dependencies": [], "depends_on": [], "required_features": ["Fixture feature"], "testing_status": "NOT_STARTED", "last_verification_date": None, "notes": "Fixture notes", "related_tools": [], "verification": None, **extra}


class DashboardDataTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="edb-dashboard-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.registry = {"schema_version": 1, "updated_on": "2026-10-31", "project": {"name": "Fixture", "website": "https://example.invalid/", "repository": "https://example.invalid/repo"}, "status_definitions": {s: s for s in tr.STATUSES}, "categories": [{"id": "text", "name": "Text"}], "tools": [tool()], "proposal_resolutions": [], "milestones": list(d.MILESTONES)}
        self.save_registry()
        for name in d.DOCS:
            (self.root / name).write_text("# Manual fixture notes\n", encoding="utf-8")

    def save_registry(self):
        (self.root / "TOOL_REGISTRY.json").write_text(json.dumps(self.registry), encoding="utf-8")

    def report(self, name="project-status", **extra):
        value = {**tr.report(name), **extra}
        path = self.root / "reports" / tr.REPORT_FILES[name]
        path.parent.mkdir(exist_ok=True)
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def test_registry_counts_come_from_actual_registry(self):
        self.report(counts={"total": 9999})
        snapshot = d.load_snapshot(self.root)
        self.assertTrue(snapshot.registry_valid)
        self.assertEqual(snapshot.counts["total"], 1)
        self.assertEqual(snapshot.counts["ready"], 1)

    def test_all_statuses_and_no_double_count(self):
        tools = [tool(str(i), state) for i, state in enumerate(tr.STATUSES)]
        counts = tr.summarize({"tools": tools, "categories": [], "milestones": list(d.MILESTONES)})
        self.assertEqual(sum(counts["by_status"].values()), counts["total"])
        self.assertEqual(counts["released"], 1)
        self.assertEqual(counts["tested"], 1)

    def test_milestones_use_only_released_and_cap_at_100(self):
        self.assertEqual(d.milestone_progress(4)[0], (25, 16.0))
        self.assertEqual(d.milestone_progress(1200)[-1], (1000, 100.0))
        self.assertEqual(len(d.milestone_progress(0)), 7)

    def test_missing_reports_are_not_run(self):
        self.assertEqual(d.load_report(self.root, "project-status").state, "NOT RUN")

    def test_invalid_reports_are_unknown(self):
        path = self.report()
        for invalid in ("{bad", "[]", '{"schema_version":2}', '{"x":1,"x":2}', "{\"x\":NaN}"):
            path.write_text(invalid, encoding="utf-8")
            with self.subTest(invalid=invalid):
                result = d.load_report(self.root, "project-status")
                self.assertEqual(result.state, "UNKNOWN")
                self.assertIn("Cannot read", result.reason)

    def test_report_diagnostics_and_warning(self):
        self.report(status="WARN", warnings=[{"code": "FIXTURE", "message": "Fixture warning", "path": "sample/index.html"}])
        result = d.load_report(self.root, "project-status")
        self.assertEqual(result.state, "WARNING")
        self.assertEqual(result.payload["warnings"][0]["path"], "sample/index.html")

    def test_contradictory_pass_with_error_is_failure(self):
        self.report(errors=[{"message": "Failure"}])
        self.assertEqual(d.load_report(self.root, "project-status").state, "FAIL")

    def test_old_and_future_timestamps(self):
        now = datetime.now(timezone.utc)
        for hours, expected in ((-25, "STALE"), (1, "UNKNOWN")):
            self.report(generated_at=(now + timedelta(hours=hours)).isoformat())
            self.assertEqual(d.load_report(self.root, "project-status", now=now).state, expected)

    def test_provenance_detects_input_and_report_changes(self):
        for name in tr.REPORT_FILES:
            self.report(name)
        op.save_provenance(self.root)
        self.assertTrue(all(r.state == "PASS" for r in d.load_snapshot(self.root).reports))
        (self.root / "changed.py").write_text("# changed input", encoding="utf-8")
        self.assertTrue(all(r.state == "STALE" for r in d.load_snapshot(self.root).reports))
        op.save_provenance(self.root)
        path = self.root / "reports/project-status.json"
        path.write_text(path.read_text() + "\n", encoding="utf-8")
        self.assertEqual(d.load_snapshot(self.root).reports[-1].state, "STALE")

    def test_old_reports_cannot_be_rebound_to_new_inputs(self):
        for name in tr.REPORT_FILES:
            self.report(name, generated_at=(datetime.now(timezone.utc) - timedelta(hours=1)).isoformat())
        with self.assertRaises(OSError):
            op.save_provenance(self.root, datetime.now(timezone.utc))

    def test_unchanged_recent_reports_and_concurrent_input_edits_not_rebound(self):
        for name in tr.REPORT_FILES:
            self.report(name)
        before = {name: d.file_hash(self.root / "reports" / filename) for name, filename in tr.REPORT_FILES.items()}
        with self.assertRaisesRegex(OSError, "did not change"):
            op.save_provenance(self.root, before_reports=before)
        inputs = d.fingerprint(self.root, exclude=op.GENERATED_DOCS)
        (self.root / "new.py").write_text("# external edit", encoding="utf-8")
        with self.assertRaisesRegex(OSError, "inputs changed"):
            op.save_provenance(self.root, before_inputs=inputs)

    def test_permission_denied_report_is_unknown(self):
        with patch.object(d, "read_json", side_effect=PermissionError("fixture denied")):
            result = d.load_report(self.root, "project-status")
        self.assertEqual(result.state, "UNKNOWN")
        self.assertIn("denied", result.reason)

    def test_corrupt_provenance_does_not_certify_reports(self):
        self.report()
        (self.root / "reports/dashboard-refresh.json").write_text("[]", encoding="utf-8")
        self.assertEqual(d.load_snapshot(self.root).reports[-1].state, "STALE")

    def test_partial_optional_fields_and_empty_registry(self):
        self.registry["tools"] = [{"id": "partial", "name": "Partial", "category": "text", "status": "BLOCKED"}]
        self.save_registry()
        snapshot = d.load_snapshot(self.root)
        self.assertFalse(snapshot.registry_valid)
        self.assertEqual(snapshot.counts["total"], 1)
        self.assertEqual(d.blockers(snapshot.tools)[0][1], "Reason not documented.")
        self.registry["tools"] = []
        self.save_registry()
        self.assertEqual(d.load_snapshot(self.root).counts["total"], 0)

    def test_invalid_registry_still_opens_partial_snapshot(self):
        (self.root / "TOOL_REGISTRY.json").write_text("{invalid", encoding="utf-8")
        snapshot = d.load_snapshot(self.root)
        self.assertFalse(snapshot.registry_valid)
        self.assertTrue(snapshot.issues)
        self.assertEqual(snapshot.counts["total"], 0)

    def test_search_filters_and_sorting(self):
        tools = [tool("zulu", priority="P2"), tool("alpha", status="PLANNED", category="data"), tool("beta")]
        self.assertEqual([t["id"] for t in d.filter_tools(tools)], ["alpha", "beta", "zulu"])
        self.assertEqual(d.filter_tools(tools, query="ZUL")[0]["id"], "zulu")
        self.assertEqual(d.filter_tools(tools, category="data")[0]["id"], "alpha")
        self.assertEqual(len(d.filter_tools(tools, status="READY", priority="P1")), 1)
        for key in ("name", "category", "status", "priority"):
            forward = d.filter_tools(tools, sort=key)
            self.assertEqual(d.filter_tools(tools, sort=key, reverse=True), list(reversed(forward)))

    def test_queue_matches_existing_ranking_and_dependencies(self):
        tools = [tool("second", rank=2), tool("first", rank=1), tool("waiting", rank=3, depends_on=["not-ready"]), tool("not-ready", status="PLANNED", rank=None)]
        self.assertEqual([t["id"] for t in d.queue_order(tools)], ["first", "second"])
        self.assertIn("not-ready: PLANNED", d.dependency_issues(tools[2], tools))
        self.assertEqual(d.queue_order(tools)[0], tr.next_tool({"tools": tools}))

    def test_blocker_reason_and_required_action_preserved(self):
        item = tool(status="BLOCKED", notes="Needs feasibility review", required_action="Run experiment")
        self.assertEqual(d.blockers([item])[0][1], "Needs feasibility review")

    def test_missing_git_and_documents_are_explicit(self):
        (self.root / "CHANGELOG.md").unlink()
        with patch.object(tr, "git_snapshot", return_value={"status": "UNKNOWN", "branch": "UNKNOWN"}):
            snapshot = d.load_snapshot(self.root)
        self.assertIn("unavailable", snapshot.documents["CHANGELOG.md"])
        self.assertTrue(any("Git unavailable" in i for i in snapshot.issues))

    def test_clipboard_summary_excludes_local_paths_and_git_identity(self):
        snapshot = d.load_snapshot(self.root)
        summary = d.summary_text(snapshot)
        self.assertNotIn(str(self.root), summary)
        self.assertIn("Push/deployment not verified", summary)
        self.assertIn("Structural checks are not functional tests", summary)

    def test_settings_and_file_actions_are_local_and_allowlisted(self):
        op.save_git_setting(self.root, "")
        self.assertEqual(d.load_settings(self.root)[0]["git_executable"], "")
        with self.assertRaises(ValueError):
            op.save_git_setting(self.root, "untrusted.exe")
        with self.assertRaises(ValueError):
            op.open_local(self.root, "../outside.txt")
        with patch.object(op.os, "startfile", create=True) as start, patch.object(op.sys, "platform", "win32"):
            op.open_local(self.root, "SESSION_HANDOFF.md")
            start.assert_called_once_with(str(self.root / "SESSION_HANDOFF.md"))

    def test_refresh_lock_rejects_second_writer(self):
        with op.refresh_lock(self.root):
            with self.assertRaises(OSError):
                with op.refresh_lock(self.root):
                    self.fail("Concurrent writer acquired the lock")
        with op.refresh_lock(self.root):
            pass

    def test_background_refresh_streams_and_prevents_duplicates(self):
        scripts = self.root / "scripts"
        scripts.mkdir()
        (scripts / "project_status.py").write_text("import time\nprint('fixture started',flush=True)\ntime.sleep(.4)\nraise SystemExit(3)\n", encoding="utf-8")
        events = queue.Queue()
        jobs = op.BackgroundJobs(self.root, events.put)
        self.assertTrue(jobs.start(refresh=True))
        self.assertFalse(jobs.start(refresh=True))
        jobs.thread.join(10)
        self.assertFalse(jobs.busy)
        values = list(events.queue)
        self.assertTrue(any(k == "output" and "fixture started" in v for k, v in values))
        self.assertEqual(next(v for k, v in values if k == "refresh_result")["code"], 3)
        self.assertTrue(any(k == "snapshot" for k, _ in values))
        self.assertEqual(values[-1], ("idle", True))

    def test_worker_exception_surfaces_and_releases_guard(self):
        events = []
        jobs = op.BackgroundJobs(self.root, events.append)
        with patch.object(op, "load_snapshot", side_effect=PermissionError("fixture denied")):
            self.assertTrue(jobs.start())
            jobs.thread.join(5)
        self.assertFalse(jobs.busy)
        self.assertTrue(any(k == "job_error" and "fixture denied" in v for k, v in events))

    def test_registry_supports_1500_entries_without_recursion(self):
        self.registry["tools"] = [tool(f"sample-{i}", rank=i + 1) for i in range(1500)]
        self.save_registry()
        snapshot = d.load_snapshot(self.root)
        self.assertTrue(snapshot.registry_valid)
        self.assertEqual(snapshot.counts["total"], 1500)
        self.assertEqual(d.queue_order(snapshot.tools)[0]["id"], "sample-0")
        self.assertEqual(len(d.filter_tools(snapshot.tools, query="Sample-14")), 111)

    def test_existing_launcher_entry_point_is_dashboard(self):
        from dashboard.app import Dashboard
        self.assertIs(status_launcher.StatusLauncher, Dashboard)
        self.assertTrue(callable(status_launcher.run_status))


@unittest.skipUnless(sys.platform == "win32", "Native Windows Tk integration")
class DashboardTkTests(unittest.TestCase):
    def test_batched_render_all_screens_and_main_thread_responsiveness(self):
        import tkinter as tk
        from dashboard.app import Dashboard
        temp = tempfile.TemporaryDirectory(prefix="edb-dashboard-tk-")
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        window = tk.Tk()
        self.addCleanup(window.destroy)
        window.withdraw()
        app = Dashboard(window, root, auto_refresh=False)
        # No scheduled worker is run against the actual project.
        snapshot = d.Snapshot(root, tools=[tool(f"row-{i}", rank=i + 1) for i in range(1500)], categories={"text": "Text"}, registry_valid=True, git={"status": "UNKNOWN"})
        snapshot.counts = tr.summarize({"tools": snapshot.tools, "categories": [{"id": "text"}], "milestones": list(d.MILESTONES)})
        snapshot.reports = [d.Report(name) for name in tr.REPORT_FILES]
        app.apply_snapshot(snapshot)
        # Cancel startup callbacks before pumping the table's scheduled batches.
        for job in window.tk.call("after", "info"):
            if "reload_data" in str(window.tk.call("after", "info", job)):
                window.after_cancel(job)
        ticks = []
        window.after(1, lambda: ticks.append(True))
        deadline = time.monotonic() + 8
        while time.monotonic() < deadline and len(app.pages["Tool Registry"].table.tree.get_children()) < 1500:
            window.update()
            time.sleep(.002)
        self.assertTrue(ticks)
        self.assertEqual(len(app.pages["Tool Registry"].table.tree.get_children()), 1500)
        for name in app.pages:
            app.show(name)
        app.pages["Tool Registry"].select("row-1499")
        self.assertIn("Row-1499", app.pages["Tool Registry"].details.text.get("1.0", "end"))
        app.pages["Tool Registry"].query.set("row-1499")
        app.pages["Tool Registry"].render()
        self.assertEqual(len(app.pages["Tool Registry"].table.tree.get_children()), 1)
        app.closed = True


if __name__ == "__main__":
    unittest.main()
