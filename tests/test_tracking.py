"""Isolated standard-library tests; never write into the real project data."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import tracking as tr


class TrackingTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="webutils-tests-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "project with spaces"
        self.root.mkdir()
        self.registry = {
            "schema_version": 1, "updated_on": "2026-10-31",
            "project": {"name": "Fixture", "repository": "https://example.invalid/repo", "website": "https://example.invalid/"},
            "status_definitions": {s: s for s in tr.STATUSES},
            "categories": [{"id": "text", "name": "Text Tools"}],
            "milestones": [25, 50, 100],
            "proposal_resolutions": [{"proposed_name": "Planned sample", "tool_id": "planned-tool", "disposition": "NEW_TOOL", "reason": "Separate task"}],
            "tools": [self.tool("sample-tool", "IMPLEMENTED"), self.tool("planned-tool", "READY", rank=1)]}
        for filename in tr.REQUIRED_DOCS:
            self.write(filename, "# Manual notes\n\nKeep this: café and creator decisions.\n")
        for filename, blocks in {"PROGRESS_TRACKER.md": ["COUNTS", "NEXT"], "ROADMAP.md": ["SEQUENCE", "CATALOG"], "audit/BACKLOG_RECONCILIATION.md": ["RESOLUTIONS"], "SESSION_HANDOFF.md": ["STATUS"]}.items():
            self.write(filename, "MANUAL PREFIX — café\n" + "\n".join(f"<!-- GENERATED:{b}:START -->\n<!-- GENERATED:{b}:END -->" for b in blocks) + "\nMANUAL SUFFIX — preserve this.\n")
        self.write("audit/INITIAL_BACKLOG.json", json.dumps({"proposed_names": ["Planned sample"]}))
        self.write("sample-tool/index.html", '<!DOCTYPE html><html><head><title>Sample utility</title></head><body><a href="../index.html">← Back to Hub</a><textarea id="editor"></textarea><button id="copy">Copy</button></body></html>')
        self.write("index.html", '<!DOCTYPE html><html><head><title>Hub</title></head><body><p>1 tools ready to use</p><a data-title="Sample" href="sample-tool/index.html">Sample</a></body></html>')
        self.save()
        self.assertEqual(tr.generate_progress(self.root)["errors"], [])

    def tool(self, tid, status, rank=None):
        return {"id": tid, "name": tid.replace("-", " ").title(), "category": "text", "description": "Fixture utility.", "directory_path": tid, "status": status, "priority": "P1" if rank else "P2", "implementation_complexity": "S", "dependencies": ["Browser DOM"], "required_features": ["Copy result"], "testing_status": "NOT_STARTED", "last_verification_date": None, "notes": "Fixture only.", "sequence_rank": rank, "related_tools": [], "verification": None, "expected_interface_ids": ["editor", "copy"]}

    def write(self, relative, content):
        filename = self.root / relative
        filename.parent.mkdir(parents=True, exist_ok=True)
        filename.write_bytes(content.encode("utf-8"))

    def save(self):
        self.write("TOOL_REGISTRY.json", json.dumps(self.registry, ensure_ascii=False, indent=2))

    def codes(self, report):
        return {entry["code"] for entry in report["errors"]}

    def assert_registry_error(self, code):
        self.save()
        result, _ = tr.validate_registry(self.root)
        self.assertIn(code, self.codes(result))

    def test_valid_registry_and_structure(self):
        self.assertEqual(tr.validate_registry(self.root)[0]["status"], "PASS")
        self.assertEqual(tr.check_project(self.root)["status"], "PASS")
        self.assertEqual(tr.verify_tools(self.root)["status"], "PASS")

    def test_invalid_json_without_input_disclosure(self):
        self.write("TOOL_REGISTRY.json", '{"password":"DO_NOT_ECHO", invalid}')
        result, _ = tr.validate_registry(self.root)
        self.assertIn("INVALID_JSON", self.codes(result))
        self.assertNotIn("DO_NOT_ECHO", json.dumps(result))

    def test_duplicate_json_keys(self):
        self.write("TOOL_REGISTRY.json", '{"tools":[],"tools":[]}')
        self.assertEqual(tr.validate_registry(self.root)[0]["status"], "FAIL")

    def test_nonstandard_json_constant(self):
        self.write("TOOL_REGISTRY.json", '{"value":NaN}')
        self.assertEqual(tr.validate_registry(self.root)[0]["status"], "FAIL")

    def test_missing_required_field(self):
        del self.registry["tools"][0]["dependencies"]
        self.assert_registry_error("REQUIRED_FIELDS")

    def test_invalid_root_types(self):
        for invalid in ([], None, {"tools": {}}):
            self.write("TOOL_REGISTRY.json", json.dumps(invalid))
            self.assertEqual(tr.validate_registry(self.root)[0]["status"], "FAIL")

    def test_duplicate_ids(self):
        self.registry["tools"].append(copy.deepcopy(self.registry["tools"][0]))
        self.assert_registry_error("DUPLICATE_ID")

    def test_duplicate_directories(self):
        self.registry["tools"][1]["directory_path"] = "sample-tool"
        self.assert_registry_error("DUPLICATE_DIRECTORY")

    def test_invalid_status(self):
        self.registry["tools"][0]["status"] = "DONE"
        self.assert_registry_error("INVALID_STATUS")

    def test_invalid_status_type(self):
        self.registry["tools"][0]["status"] = []
        self.assert_registry_error("INVALID_STATUS")

    def test_missing_category(self):
        self.registry["tools"][0]["category"] = "missing"
        self.assert_registry_error("MISSING_CATEGORY")

    def test_malformed_category(self):
        self.registry["categories"] = [None]
        self.assert_registry_error("CATEGORY_FIELDS")

    def test_bad_dependencies(self):
        self.registry["tools"][0]["dependencies"] = {"secret": "not a list"}
        self.assert_registry_error("INVALID_LIST")

    def test_missing_tool_dependency(self):
        self.registry["tools"][1]["depends_on"] = ["missing-tool"]
        self.assert_registry_error("DEPENDENCY_REFERENCE")

    def test_tool_prefixed_dependency(self):
        self.registry["tools"][1]["dependencies"] = ["tool:missing-tool"]
        self.assert_registry_error("DEPENDENCY_REFERENCE")

    def test_dependency_cycle(self):
        self.registry["tools"][0]["depends_on"] = ["planned-tool"]
        self.registry["tools"][1]["depends_on"] = ["sample-tool"]
        self.assert_registry_error("DEPENDENCY_CYCLE")

    def test_next_task_respects_unfinished_dependency(self):
        self.registry["tools"][1]["depends_on"] = ["sample-tool"]
        self.assertIsNone(tr.next_tool(self.registry))

    def test_missing_related_tool(self):
        self.registry["tools"][0]["related_tools"] = ["unknown"]
        self.assert_registry_error("TOOL_REFERENCE")

    def test_missing_implemented_directory(self):
        shutil.rmtree(self.root / "sample-tool")
        self.assertIn("MISSING_IMPLEMENTATION", self.codes(tr.validate_registry(self.root)[0]))

    def test_missing_entrypoint(self):
        (self.root / "sample-tool/index.html").unlink()
        self.assertIn("MISSING_IMPLEMENTATION", self.codes(tr.validate_registry(self.root)[0]))

    def test_planned_directory_not_required(self):
        self.assertFalse((self.root / "planned-tool").exists())
        self.assertEqual(tr.validate_registry(self.root)[0]["status"], "PASS")

    def test_planned_tool_cannot_claim_tests(self):
        self.registry["tools"][1]["testing_status"] = "SMOKE_PASSED"
        self.assert_registry_error("PLANNED_TEST_CLAIM")

    def test_released_requires_publication_and_functional_evidence(self):
        self.registry["tools"][0]["status"] = "RELEASED"
        self.assert_registry_error("PUBLICATION_EVIDENCE")

    def test_unsafe_directory_path(self):
        self.registry["tools"][0]["directory_path"] = "../elsewhere"
        self.assert_registry_error("DIRECTORY_PATH")

    def test_broken_homepage_link(self):
        self.write("index.html", '<p>1 tools ready to use</p><a href="missing/index.html" data-title="Missing">Missing</a>')
        result = tr.check_project(self.root)
        self.assertIn("BROKEN_INTERNAL_LINK", self.codes(result))
        self.assertIn("HOMEPAGE_CARDS", self.codes(result))

    def test_homepage_attributes_can_be_in_any_order(self):
        self.assertEqual(tr.check_project(self.root)["status"], "PASS")

    def test_unregistered_source_directory(self):
        self.write("unregistered/index.html", "<html></html>")
        self.assertIn("UNREGISTERED_TOOL", self.codes(tr.check_project(self.root)))

    def test_missing_documentation(self):
        (self.root / "ARCHITECTURE.md").unlink()
        self.assertIn("MISSING_DOCUMENTATION", self.codes(tr.check_project(self.root)))

    def test_empty_registry(self):
        self.registry["tools"] = []
        self.registry["proposal_resolutions"] = []
        self.save()
        result, r = tr.validate_registry(self.root)
        self.assertEqual(result["status"], "WARN")
        self.assertEqual(result["counts"]["total"], 0)
        self.assertIsNone(tr.next_tool(r))

    def test_repeated_progress_generation_is_identical(self):
        before = (self.root / "PROGRESS_TRACKER.md").read_bytes()
        tr.generate_progress(self.root)
        tr.generate_progress(self.root)
        self.assertEqual(before, (self.root / "PROGRESS_TRACKER.md").read_bytes())

    def test_manual_notes_preserved(self):
        tr.generate_progress(self.root)
        tr.generate_handoff(self.root)
        for filename in ("PROGRESS_TRACKER.md", "SESSION_HANDOFF.md", "ROADMAP.md"):
            content = tr.read_text(self.root / filename)
            self.assertTrue(content.startswith("MANUAL PREFIX — café\n"))
            self.assertTrue(content.endswith("MANUAL SUFFIX — preserve this.\n"))

    def test_crlf_checkout_is_not_reported_stale(self):
        for filename in ("PROGRESS_TRACKER.md", "ROADMAP.md", "audit/BACKLOG_RECONCILIATION.md"):
            self.write(filename, tr.read_text(self.root / filename).replace("\n", "\r\n"))
        self.assertEqual(tr.check_project(self.root)["status"], "PASS")
        before = (self.root / "PROGRESS_TRACKER.md").read_bytes()
        tr.generate_progress(self.root)
        self.assertEqual(before, (self.root / "PROGRESS_TRACKER.md").read_bytes())

    def test_invalid_markers_do_not_overwrite_any_documents(self):
        self.write("ROADMAP.md", "manual file with no markers")
        before = (self.root / "PROGRESS_TRACKER.md").read_bytes()
        result = tr.generate_progress(self.root)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(before, (self.root / "PROGRESS_TRACKER.md").read_bytes())

    def test_git_unavailable(self):
        with patch.object(tr.subprocess, "run", side_effect=FileNotFoundError):
            self.assertEqual(tr.git_snapshot(self.root)["working_tree"], "UNKNOWN")

    def test_git_failed_stderr_is_not_reported(self):
        failure = subprocess.CalledProcessError(1, "git", stderr="credential=DO_NOT_ECHO")
        with patch.object(tr.subprocess, "run", side_effect=failure):
            snapshot = tr.git_snapshot(self.root)
        self.assertEqual(snapshot["branch"], "UNKNOWN")
        self.assertNotIn("DO_NOT_ECHO", json.dumps(snapshot))

    def test_git_timeout(self):
        with patch.object(tr.subprocess, "run", side_effect=subprocess.TimeoutExpired("git", 10)):
            self.assertEqual(tr.git_snapshot(self.root)["latest_commit"], "UNKNOWN")

    def test_missing_title_and_navigation(self):
        self.write("sample-tool/index.html", '<!DOCTYPE html><html><head><title> </title></head><body><textarea id="editor"></textarea></body></html>')
        result = tr.verify_tools(self.root)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("title" in e["message"] for e in result["errors"]))

    def test_missing_expected_interface(self):
        self.registry["tools"][0]["expected_interface_ids"].append("missing-control")
        self.save()
        self.assertEqual(tr.verify_tools(self.root)["status"], "FAIL")

    def test_structure_never_promotes_status(self):
        before = (self.root / "TOOL_REGISTRY.json").read_bytes()
        tr.verify_tools(self.root)
        self.assertEqual(before, (self.root / "TOOL_REGISTRY.json").read_bytes())

    def test_untrusted_javascript_not_executed(self):
        original = tr.read_text(self.root / "sample-tool/index.html")
        self.write("sample-tool/index.html", original + '<script>throw new Error("DO NOT EXECUTE")</script>')
        self.assertEqual(tr.verify_tools(self.root)["status"], "PASS")

    def test_validation_does_not_change_files(self):
        before = {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        tr.validate_registry(self.root)
        tr.check_project(self.root)
        tr.verify_tools(self.root)
        after = {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_path_traversal_link(self):
        self.write("index.html", '<p>1 tools ready to use</p><a href="../outside.html">Bad</a>')
        self.assertIn("UNSAFE_INTERNAL_PATH", self.codes(tr.check_project(self.root)))

    def test_reports_have_bounded_history_and_no_absolute_root(self):
        tr.project_status(self.root)
        tr.project_status(self.root)
        paths = list((self.root / "reports").glob("*.json"))
        self.assertEqual(len(paths), 4)
        for filename in paths:
            data = json.loads(filename.read_text(encoding="utf-8"))
            self.assertTrue({"generated_at", "check_name", "status", "counts", "errors", "warnings", "details"}.issubset(data))
            self.assertNotIn(str(self.root), json.dumps(data))

    def test_invalid_registry_preserves_generated_manual_files(self):
        before = {name: (self.root / name).read_bytes() for name in ("PROGRESS_TRACKER.md", "SESSION_HANDOFF.md")}
        self.write("TOOL_REGISTRY.json", "not json")
        result = tr.project_status(self.root)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(before, {name: (self.root / name).read_bytes() for name in before})

    def test_status_repairs_stale_generated_sections_and_records_initial_failure(self):
        self.registry["tools"][1]["priority"] = "P2"
        self.registry["tools"][1]["sequence_rank"] = None
        self.save()
        result = tr.project_status(self.root)
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["details"]["initial_consistency"]["status"], "FAIL")
        self.assertEqual(result["details"]["checks"]["project-consistency"], "PASS")

    def test_status_does_not_hide_missing_sources(self):
        (self.root / "sample-tool/index.html").unlink()
        result = tr.project_status(self.root)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("MISSING_IMPLEMENTATION", self.codes(result))

    def test_status_counts_are_a_partition(self):
        counts = tr.summarize(self.registry)
        self.assertEqual(sum(counts["by_status"].values()), counts["total"])
        self.assertEqual(sum(counts["by_category"].values()), counts["total"])
        self.assertEqual(sum(counts["by_priority"].values()), counts["total"])

    def test_large_registry_and_deep_dependency_chain(self):
        self.registry["tools"] = [self.tool(f"planned-{i}", "PLANNED") for i in range(1500)]
        self.registry["proposal_resolutions"] = []
        for index, tool in enumerate(self.registry["tools"]):
            if index:
                tool["depends_on"] = [f"planned-{index-1}"]
        self.save()
        result, _ = tr.validate_registry(self.root)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["counts"]["total"], 1500)

    def test_all_cli_entrypoints_support_paths_with_spaces(self):
        for command in ("validate_registry", "check_project", "verify_tools", "generate_progress", "generate_handoff", "project_status"):
            with self.subTest(command=command):
                completed = subprocess.run([sys.executable, str(SCRIPTS / (command + ".py")), "--root", str(self.root), "--json"], capture_output=True, text=True, encoding="utf-8", cwd=self.temporary.name)
                self.assertEqual(completed.returncode, 0, completed.stderr)
                self.assertIn(json.loads(completed.stdout)["status"], ("PASS", "WARN"))

    def test_cli_exit_codes_for_validation_and_invocation(self):
        self.write("TOOL_REGISTRY.json", "bad json")
        result = subprocess.run([sys.executable, str(SCRIPTS / "validate_registry.py"), "--root", str(self.root), "--json"], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 1)
        result = subprocess.run([sys.executable, str(SCRIPTS / "validate_registry.py"), "--unknown"], capture_output=True)
        self.assertEqual(result.returncode, 2)

    def test_unicode_json_bridge_uses_utf8_on_windows(self):
        self.registry["tools"][1]["name"] = "CSV ↔ JSON — café"
        self.save()
        tr.generate_progress(self.root)
        result = subprocess.run([sys.executable, str(SCRIPTS / "tracking.py"), "--bridge", "project", "--root", str(self.root)], input=json.dumps(self.registry, ensure_ascii=False), capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(json.loads(result.stdout)["errors"], [])

    def test_broken_documentation_link(self):
        self.write("README.md", "[Missing document](absent.md)")
        self.assertIn("BROKEN_DOCUMENT_LINK", self.codes(tr.check_project(self.root)))

    def test_invalid_website_type_is_a_validation_error(self):
        self.registry["project"]["website"] = ["invalid"]
        self.registry["tools"][0]["status"] = "RELEASED"
        self.assert_registry_error("PROJECT_URL")

    def test_check_only_status_does_not_update_documentation(self):
        before = {name: (self.root / name).read_bytes() for name in ("PROGRESS_TRACKER.md", "SESSION_HANDOFF.md")}
        result = tr.project_status(self.root, write_reports=False, update_documents=False)
        self.assertFalse(result["details"]["documentation_updates_enabled"])
        self.assertEqual(before, {name: (self.root / name).read_bytes() for name in before})

    def test_known_git_snapshot_uses_no_author_or_remote_data(self):
        if not shutil.which("git"):
            self.skipTest("Git unavailable")
        def git(*args):
            subprocess.run(["git", "-C", str(self.root), *args], check=True, capture_output=True)
        git("init", "-q")
        git("add", ".")
        git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "Fixture")
        snapshot = tr.git_snapshot(self.root)
        self.assertEqual(snapshot["status"], "KNOWN")
        self.assertEqual(snapshot["working_tree"], "Clean")
        self.write("new-file.txt", "uncommitted")
        snapshot = tr.git_snapshot(self.root)
        self.assertEqual(snapshot["working_tree"], "Dirty")
        self.assertTrue(any(c["path"] == "new-file.txt" for c in snapshot["changes"]))
        self.assertNotIn("fixture@example.invalid", json.dumps(snapshot))

    def test_malformed_tool_objects_produce_consolidated_report(self):
        self.registry["tools"] = [None, 42, "not a tool"]
        self.save()
        result = tr.project_status(self.root)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("TOOL_OBJECT", self.codes(result))
        self.assertEqual(result["details"]["current_task"], "UNKNOWN")

    def test_malformed_verification_report_is_an_error(self):
        tool = self.registry["tools"][0]
        tool.update(status="TESTED", testing_status="REQUIRED_PASSED", last_verification_date="2026-10-31", verification={"source_revision": "f" * 40, "source_sha256": tr.normalized_hash(tr.read_text(self.root / "sample-tool/index.html")), "evidence_path": "audit/test-evidence.json", "test_scope": ["fixture only"]})
        self.save()
        for malformed in ([], {"pages": [None]}, {"pages": "not an array"}):
            with self.subTest(malformed=malformed):
                self.write("audit/test-evidence.json", json.dumps(malformed))
                result = tr.check_project(self.root)
                self.assertIn("EVIDENCE_UNREADABLE", self.codes(result))


if __name__ == "__main__":
    unittest.main()
