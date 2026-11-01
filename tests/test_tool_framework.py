"""Temporary-fixture framework tests; never generate a real website utility."""
import copy
from datetime import datetime, timezone
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
import tool_framework as fw
from tool_homepage import Homepage, integration_proposal
from test_tool import run_tests


def entry(tid="fixture-tool", rank=1, **extra):
    return {"id": tid, "name": tid.title(), "category": "text", "description": "Fixture description", "directory_path": tid, "status": "READY", "priority": "P1", "implementation_complexity": "S", "dependencies": ["Tailwind CSS Play CDN v4"], "required_features": ["Documented fixture behavior"], "testing_status": "NOT_STARTED", "last_verification_date": None, "notes": "Fixture only", "sequence_rank": rank, "related_tools": [], "verification": None, **extra}


class FrameworkTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="edb-framework-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.value = {"schema_version": 1, "updated_on": "2026-10-31", "project": {"name": "Fixture", "website": "https://example.invalid/", "repository": "https://example.invalid/repo"}, "status_definitions": {s: s for s in tr.STATUSES}, "categories": [{"id": "text", "name": "Text"}, {"id": "pdf", "name": "PDF"}, {"id": "data", "name": "Data"}], "milestones": [25, 50, 100], "tools": [entry()], "proposal_resolutions": []}
        self.save()
        self.home = '<!doctype html><html><head><title>Hub</title></head><body><p id="resultCount">0 tools ready to use</p><div id="toolGrid"></div></body></html>\n'
        (self.root / "index.html").write_text(self.home, encoding="utf-8")

    def save(self):
        (self.root / "TOOL_REGISTRY.json").write_text(json.dumps(self.value), encoding="utf-8")

    def create(self, template=None):
        return fw.create_tool(self.root, "fixture-tool", template)

    def implemented_fixture(self):
        result = self.create()
        page = self.root / result["workspace"] / "fixture-tool/index.html"
        content = page.read_text(encoding="utf-8").replace("isScaffold: true", "isScaffold: false").replace("throw new Error('Not implemented — replace this placeholder with the actual tool logic.');", "if (input === 'invalid') throw new Error('Fixture rejected'); return 'Result: ' + input;")
        page.write_text(content, encoding="utf-8")
        cases = [{"id": "ordinary", "input": "hello", "expected": "Result: hello"}, {"id": "unicode-lines", "input": "café 😀\nnext", "expected": "Result: café 😀\nnext"}, {"id": "error", "input": "invalid", "error": "Fixture rejected"}]
        tests = page.parent.parent / "tests"
        (tests / "logic.cases.json").write_text(json.dumps({"schema_version": 1, "cases": cases}), encoding="utf-8")
        return page, tests

    def test_lookup_and_unsafe_unknown_identifiers(self):
        self.assertEqual(fw.lookup(self.root, "fixture-tool")[1]["status"], "READY")
        for bad in ("../escape", "a/b", "a\\b", "C:drive", "CON", "con", "aux", "Upper", "x" * 81, "unknown-id"):
            with self.subTest(bad=bad), self.assertRaises(fw.FrameworkError):
                fw.lookup(self.root, bad)

    def test_duplicate_route_and_missing_metadata_rejected(self):
        self.value["tools"].append(entry("second", rank=2, directory_path="fixture-tool"))
        self.save()
        with self.assertRaisesRegex(fw.FrameworkError, "Registry validation"):
            self.create()
        self.value["tools"] = [entry()]
        del self.value["tools"][0]["description"]
        self.save()
        with self.assertRaises(fw.FrameworkError):
            self.create()

    def test_malformed_registry_rejected_without_side_effects(self):
        for invalid in ("{broken", "[]", '{"tools":{}}', '{"x":1,"x":2}'):
            (self.root / "TOOL_REGISTRY.json").write_text(invalid, encoding="utf-8")
            with self.assertRaises(fw.FrameworkError):
                self.create()
        self.assertFalse((self.root / "development").exists())

    def test_dry_run_is_read_only(self):
        before = (self.root / "TOOL_REGISTRY.json").read_bytes()
        result = fw.create_tool(self.root, "fixture-tool", dry_run=True)
        self.assertEqual(len(result["files"]), 6)
        self.assertFalse((self.root / "development").exists())
        self.assertEqual((self.root / "TOOL_REGISTRY.json").read_bytes(), before)
        self.assertEqual((self.root / "index.html").read_text(), self.home)

    def test_text_and_structured_rendering_structure_and_no_status_change(self):
        before = (self.root / "TOOL_REGISTRY.json").read_bytes()
        self.value["tools"][0]["description"] = '<script>alert("unsafe")</script> & input'
        self.save()
        result = self.create("structured")
        html = (self.root / result["workspace"] / "fixture-tool/index.html").read_text(encoding="utf-8")
        self.assertIn("&lt;script&gt;", html)
        self.assertNotIn('<script>alert("unsafe")', html)
        self.assertIn("<fieldset>", html)
        self.assertEqual(fw.structural_check(self.root, "fixture-tool")["status"], "PASS")
        self.assertEqual(json.loads((self.root / "TOOL_REGISTRY.json").read_text())["tools"][0]["status"], "READY")
        self.assertFalse((self.root / "fixture-tool").exists())

    def test_existing_workspace_never_overwritten(self):
        result = self.create()
        page = self.root / result["workspace"] / "fixture-tool/index.html"
        before = page.read_bytes()
        with self.assertRaisesRegex(fw.FrameworkError, "already exists"):
            self.create()
        self.assertEqual(page.read_bytes(), before)

    def test_existing_canonical_directory_never_overwritten(self):
        directory = self.root / "fixture-tool"
        directory.mkdir()
        (directory / "owner.txt").write_text("owner work")
        with self.assertRaisesRegex(fw.FrameworkError, "Canonical directory"):
            self.create()
        self.assertEqual((directory / "owner.txt").read_text(), "owner work")

    def test_released_and_active_entries_protected(self):
        self.value["tools"][0].update(status="IN_PROGRESS")
        self.save()
        with self.assertRaisesRegex(fw.FrameworkError, "Only READY"):
            self.create()
        with patch.object(fw, "lookup", return_value=(self.value, entry(status="RELEASED"))):
            with self.assertRaisesRegex(fw.FrameworkError, "released"):
                self.create()

    def test_generation_rolls_back_own_files_on_failure(self):
        original = Path.open
        def fail(path, *args, **kwargs):
            if path.name == "manifest.json" and args and args[0] == "x":
                raise PermissionError("fixture failure")
            return original(path, *args, **kwargs)
        with patch.object(Path, "open", fail), self.assertRaises(fw.FrameworkError):
            self.create()
        self.assertFalse((self.root / "development/scaffolds/fixture-tool").exists())
        self.assertEqual((self.root / "index.html").read_text(), self.home)

    def test_unsafe_paths_and_symlinks_rejected(self):
        for relative in ("../x", "/outside", "a/../../x", "a\\x", "C:/outside"):
            with self.assertRaises(fw.FrameworkError):
                fw.local_path(self.root, relative)
        original = Path.is_symlink
        with patch.object(Path, "is_symlink", lambda p: p.name == "development" or original(p)):
            with self.assertRaisesRegex(fw.FrameworkError, "Symlink"):
                self.create()

    def test_batch_order_dependencies_specialization_and_no_writes(self):
        self.value["tools"] += [entry("second", rank=2, category="pdf"), entry("waiting", rank=3, depends_on=["dependency"]), entry("dependency", rank=None, priority="P2", status="PLANNED"), entry("blocked", rank=None, priority="P3", status="BLOCKED", notes="Feasibility decision")]
        self.save()
        plan = fw.plan_batch(self.root, 10)
        self.assertEqual([t["tool_id"] for t in plan["selected"]], ["fixture-tool", "second"])
        self.assertEqual(plan["selected"][0]["tool_id"], tr.next_tool(self.value)["id"])
        self.assertEqual(plan["selected"][1]["classification"], "Requires specialized implementation")
        self.assertEqual({t["classification"] for t in plan["excluded"]}, {"Requires dependency", "Blocked"})
        self.assertFalse((self.root / "development").exists())
        for bad in (0, -1, 1001):
            with self.assertRaises(fw.FrameworkError):
                fw.plan_batch(self.root, bad)

    def test_individual_case_symlink_is_rejected(self):
        self.implemented_fixture()
        original = Path.is_symlink
        with patch.object(Path, "is_symlink", lambda p: p.name == "logic.cases.json" or original(p)):
            with self.assertRaisesRegex(fw.FrameworkError, "Symlink"):
                fw.suite_spec(self.root, "fixture-tool")

    def test_cli_dry_run_from_unrelated_directory(self):
        result = subprocess.run([sys.executable, str(SCRIPTS / 'create_tool.py'), '--root', str(self.root), '--id', 'fixture-tool', '--dry-run'], cwd=SCRIPTS.parent.parent, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)['dry_run'])
        self.assertFalse((self.root / 'development').exists())

    def test_batch_output_cannot_overwrite_tracking_or_local_settings(self):
        reports=self.root/'reports'; reports.mkdir()
        protected=reports/'project-status.json'; protected.write_text('owner report')
        command=[sys.executable,str(SCRIPTS/'plan_tool_batch.py'),'--root',str(self.root),'--count','1','--output']
        result=subprocess.run(command+['reports/project-status.json'],capture_output=True,text=True)
        self.assertEqual(result.returncode,1)
        self.assertEqual(protected.read_text(),'owner report')
        result=subprocess.run(command+['reports/batch-plans/fixture.json'],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(json.loads((reports/'batch-plans/fixture.json').read_text())['kind'],'PROPOSAL_ONLY')

    def test_existing_scaffold_excluded_from_planned_batch(self):
        self.create()
        self.assertEqual(fw.plan_batch(self.root)["selected"], [])

    def test_structure_detects_duplicate_ids_broken_links_and_manifest(self):
        result = self.create()
        source = self.root / result["workspace"] / "fixture-tool/index.html"
        html = source.read_text(encoding="utf-8")
        source.write_text(html.replace('</main>', '<a href="missing.html">broken</a><i id="toolInput"></i></main>'), encoding="utf-8")
        result = fw.structural_check(self.root, "fixture-tool")
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("Duplicate HTML IDs.", result["errors"])
        self.assertIn("Broken internal resource/link.", result["errors"])

    def test_placeholder_and_empty_suites_never_pass_as_functionality(self):
        self.create()
        result = run_tests(self.root, "fixture-tool")
        self.assertEqual(result["status"], "NOT RUN")
        self.assertEqual(result["layers"]["logic"]["status"], "NOT RUN")
        self.assertEqual(result["layers"]["browser"]["status"], "NOT RUN")
        self.assertEqual(result["layers"]["structural"]["status"], "PASS")

    def test_actual_logic_cases_discovery_and_failures(self):
        _, tests = self.implemented_fixture()
        result = run_tests(self.root, "fixture-tool", layers=("structural", "logic"))
        self.assertEqual(result["layers"]["logic"]["passed"], 3)
        self.assertEqual(result["status"], "PARTIAL")
        (tests / "logic.cases.json").write_text(json.dumps({"schema_version": 1, "cases": [{"id": "wrong", "input": "hello", "expected": "wrong"}]}))
        self.assertEqual(run_tests(self.root, "fixture-tool", layers=("logic",))["status"], "FAIL")

    def test_invalid_case_schema_and_duplicate_case_ids_fail(self):
        _, tests = self.implemented_fixture()
        for payload in ({"schema_version": 1, "cases": {}}, {"schema_version": 1, "cases": [{"id": "same"}, {"id": "same"}]}):
            (tests / "logic.cases.json").write_text(json.dumps(payload))
            with self.assertRaises(fw.FrameworkError):
                fw.suite_spec(self.root, "fixture-tool")

    def test_freshness_binds_source_tests_metadata_and_runner(self):
        page, _ = self.implemented_fixture()
        first = fw.suite_spec(self.root, "fixture-tool")["input_hash"]
        page.write_text(page.read_text(encoding="utf-8") + "\n<!-- changed -->", encoding="utf-8")
        self.assertNotEqual(fw.suite_spec(self.root, "fixture-tool")["input_hash"], first)

    def test_missing_browser_is_not_pass(self):
        page, tests = self.implemented_fixture()
        (tests / "browser.cases.json").write_text(json.dumps({"schema_version": 1, "cases": [{"id": "unavailable", "steps": [{"action": "expect", "selector": "#toolInput", "property": "value", "equals": ""}]}]}))
        result = run_tests(self.root, "fixture-tool", browser=self.root / "no-browser.exe")
        self.assertEqual(result["layers"]["browser"]["status"], "NOT RUN")
        self.assertNotEqual(result["status"], "PASS")

    def test_report_generation_keeps_existing_report_schema_and_no_local_paths(self):
        self.implemented_fixture()
        result = run_tests(self.root, "fixture-tool", layers=("logic",))
        report = fw.report_path(self.root, "fixture-tool").read_text()
        self.assertNotIn(str(self.root), report)
        self.assertEqual(json.loads(report)["tool_id"], "fixture-tool")
        self.assertFalse((self.root / "reports/project-status.json").exists())

    def test_unfinished_homepage_integration_refused(self):
        with self.assertRaisesRegex(fw.FrameworkError, "TESTED or RELEASED"):
            integration_proposal(self.root, "fixture-tool")
        self.assertEqual((self.root / "index.html").read_text(), self.home)

    def test_homepage_parser_refuses_ambiguity(self):
        with self.assertRaises(fw.FrameworkError):
            Homepage(self.home.replace('</body>', '<div id="toolGrid"></div></body>'))

    def test_legacy_released_card_preserved_without_retrofit(self):
        value = copy.deepcopy(self.value)
        value["tools"][0]["status"] = "RELEASED"
        source = self.home.replace('0 tools', '1 tools').replace('<div id="toolGrid">', '<div id="toolGrid"><a href="fixture-tool/index.html" data-title="Custom existing title"><span>Original owner copy</span></a>')
        (self.root / "index.html").write_text(source)
        with patch('tool_homepage.lookup', return_value=(value, value["tools"][0])):
            proposal = integration_proposal(self.root, "fixture-tool")
        self.assertEqual(proposal["action"], "NO_CHANGE")
        self.assertEqual((self.root / "index.html").read_text(), source)

    def test_homepage_proposal_adds_only_card_and_count_and_checks_stale_gate(self):
        self.implemented_fixture()
        bundle = self.root / 'development/scaffolds/fixture-tool'
        (self.root / "fixture-tool").mkdir()
        shutil.copyfile(bundle / "fixture-tool/index.html", self.root / "fixture-tool/index.html")
        tests = self.root / "tests/tools/fixture-tool"
        tests.parent.mkdir(parents=True)
        shutil.copytree(bundle / "tests", tests)
        shutil.copyfile(bundle / "manifest.json", tests / "manifest.json")
        self.value["tools"][0]["status"] = "TESTED"
        tool = self.value["tools"][0]
        # Mock registry lookup/legacy project evidence only; independently exercise
        # real structural parsing, exact report freshness and homepage patching.
        spec = None
        with patch.object(fw, "lookup", return_value=(self.value, tool)), patch('tool_homepage.lookup', return_value=(self.value, tool)), patch.object(tr, "check_project", return_value={"errors": []}):
            spec = fw.suite_spec(self.root, 'fixture-tool', 'canonical')
            tool["verification"] = {"source_sha256": spec["source_sha256"]}
            spec = fw.suite_spec(self.root, 'fixture-tool', 'canonical')
            evidence = {"schema_version":1,"tool_id":"fixture-tool","generated_at":datetime.now(timezone.utc).isoformat(),"input_hash":spec["input_hash"],"status":"PASS","is_scaffold":False,"layers":{k:{"status":"PASS","passed":1,"failed":0} for k in ("structural","logic","browser")}}
            destination = fw.report_path(self.root,'fixture-tool');destination.parent.mkdir(parents=True);destination.write_text(json.dumps(evidence))
            proposal = integration_proposal(self.root, 'fixture-tool')
            self.assertIn('data-tool-id="fixture-tool"', proposal['patch'])
            self.assertIn('+', proposal['patch'])
            self.assertEqual((self.root/'index.html').read_text(), self.home)
            patch_file=self.root/'proposal.patch';patch_file.write_text(proposal['patch'],encoding='utf-8')
            subprocess.run(['git','init','-q',str(self.root)],check=True,capture_output=True)
            applied=subprocess.run(['git','-C',str(self.root),'apply','--check',str(patch_file)],capture_output=True)
            self.assertEqual(applied.returncode,0)
            # A Windows CRLF checkout must accept the same minimal proposal.
            (self.root/'index.html').write_bytes(self.home.replace('\n','\r\n').encode())
            crlf_proposal=integration_proposal(self.root,'fixture-tool')
            patch_file.write_text(crlf_proposal['patch'],encoding='utf-8',newline='\n')
            applied=subprocess.run(['git','-C',str(self.root),'apply','--check',str(patch_file)],capture_output=True)
            self.assertEqual(applied.returncode,0,applied.stderr.decode())
            destination.write_text(json.dumps({**evidence,'is_scaffold':True}))
            with self.assertRaises(fw.FrameworkError):
                fw.functional_gate(self.root,'fixture-tool')
            destination.write_text(json.dumps(evidence))
            (self.root/'fixture-tool/index.html').write_text('changed')
            with self.assertRaises(fw.FrameworkError):
                integration_proposal(self.root,'fixture-tool')

    def test_dashboard_counts_queue_and_blockers_unchanged(self):
        from dashboard.data import load_snapshot, queue_order
        self.value['tools'].append(entry('blocked',rank=None,status='BLOCKED',notes='Documented blocker'))
        self.save()
        before=load_snapshot(self.root)
        self.create()
        after=load_snapshot(self.root)
        self.assertEqual(before.counts,after.counts)
        self.assertEqual(after.counts['blocked'],1)
        self.assertEqual(queue_order(after.tools)[0]['id'],'fixture-tool')


if __name__ == '__main__':
    unittest.main()
