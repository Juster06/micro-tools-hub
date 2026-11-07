"""Preparation belongs before publication evidence; it cannot publish a tool."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import tracking as tr
from prepare_tool_seo import prepare


class PreparationTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="edb-seo-prepare-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.tool = {"id": "fixture", "name": "Fixture", "category": "text", "description": "Example",
                     "directory_path": "fixture", "status": "IMPLEMENTED", "priority": "P2",
                     "implementation_complexity": "S", "dependencies": [], "required_features": ["Example"],
                     "testing_status": "NOT_STARTED", "last_verification_date": None, "notes": "Fixture",
                     "sequence_rank": None, "related_tools": [], "verification": None}
        self.registry = {"schema_version": 1, "updated_on": "2026-11-07", "project": {"website": "https://everydaydigitalbox.com/"},
                         "status_definitions": {s: s for s in tr.STATUSES}, "categories": [{"id": "text", "name": "Text"}],
                         "proposal_resolutions": [], "tools": [self.tool]}
        self.page = self.root / "fixture/index.html"
        self.page.parent.mkdir()
        self.original = b'<!doctype html>\r\n<html><head>\r\n<title>Fixture</title>\r\n</head><body>Untouched</body></html>\r\n'
        self.page.write_bytes(self.original)
        self.save()

    def save(self):
        (self.root / "TOOL_REGISTRY.json").write_text(json.dumps(self.registry), encoding="utf-8")

    def test_prepare_is_idempotent_preserves_body_newlines_and_status(self):
        before = (self.root / "TOOL_REGISTRY.json").read_bytes()
        self.assertTrue(prepare(self.root, "fixture")["changed"])
        line = b'  <link rel="canonical" href="https://everydaydigitalbox.com/fixture/index.html">\r\n'
        self.assertEqual(self.page.read_bytes().replace(line, b"", 1), self.original)
        self.assertFalse(prepare(self.root, "fixture")["changed"])
        self.assertEqual((self.root / "TOOL_REGISTRY.json").read_bytes(), before)
        self.assertFalse((self.root / "sitemap.xml").exists())

    def test_noindex_is_not_removed_or_made_public(self):
        body = self.original.replace(b'<title>', b'<meta name="robots" content="noindex"><title>')
        self.page.write_bytes(body)
        with self.assertRaises(ValueError):
            prepare(self.root, "fixture")
        self.assertEqual(self.page.read_bytes(), body)

    def test_pending_or_released_status_cannot_be_prepared(self):
        for status in ["PLANNED", "BLOCKED", "READY", "TESTED", "RELEASED"]:
            with self.subTest(status=status):
                self.tool["status"] = status
                self.save()
                with self.assertRaises(ValueError):
                    prepare(self.root, "fixture")
                self.assertEqual(self.page.read_bytes(), self.original)

    def test_unknown_or_unsafe_id_writes_nothing(self):
        for value in ["missing", "../fixture", "fixture/index.html"]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                prepare(self.root, value)
        self.assertEqual(self.page.read_bytes(), self.original)


if __name__ == "__main__":
    unittest.main()
