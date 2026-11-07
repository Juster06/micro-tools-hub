"""Mutation tests for release eligibility, canonical signals and generated artifacts."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import seo
import tracking as tr


class SEOTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="edb-seo-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / "project with spaces"
        self.root.mkdir()
        self.value = {
            "schema_version": 1, "updated_on": "2026-11-07",
            "project": {"name": "Fixture", "repository": "https://example.invalid/repo", "website": seo.ORIGIN + "/"},
            "categories": [{"id": "text", "name": "Text"}],
            "status_definitions": {s: s for s in tr.STATUSES},
            "proposal_resolutions": [], "milestones": [100],
            "tools": [self.tool("zeta-tool", "RELEASED"), self.tool("alpha-tool", "RELEASED", "actual-route"),
                      self.tool("waiting-tool", "TESTED"), self.tool("future-tool", "PLANNED"), self.tool("blocked-tool", "BLOCKED")]}
        self.save_registry()
        for path in ["index.html", "privacy.html", "zeta-tool/index.html", "actual-route/index.html", "waiting-tool/index.html"]:
            self.write(path, '<!doctype html>\n<html lang="en"><head>\n<title>Fixture</title>\n</head><body>Unchanged content &amp; café</body></html>\n')
        self.write("templates/tool-page.html", '<html><head><meta name="robots" content="noindex"></head><body>Not public</body></html>')
        self.write("robots.txt", seo.ROBOTS_TEXT)
        seo.generate(self.root, sync_canonicals=True)

    def tool(self, tid, status, directory=None):
        verification = {"source_revision": "a" * 40, "source_sha256": "b" * 64, "evidence_path": "audit/fixture.json", "test_scope": ["fixture"], "publication": {"url": seo.ORIGIN + "/" + (directory or tid) + "/", "checked_at": "2026-11-07T00:00:00Z", "http_status": 200, "source_matches": True}}
        tested = status in ("TESTED", "RELEASED")
        return {"id": tid, "name": tid, "category": "text", "description": "Fixture", "directory_path": directory or tid,
                "status": status, "priority": "P2", "implementation_complexity": "S", "dependencies": [], "required_features": ["fixture"],
                "testing_status": "SMOKE_PASSED" if tested else "NOT_STARTED", "last_verification_date": "2026-11-07" if tested else None,
                "notes": "Fixture only", "sequence_rank": None, "related_tools": [], "verification": verification if tested else None}

    def write(self, relative, content):
        p = self.root / relative
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(content if isinstance(content, bytes) else content.encode("utf-8"))

    def read(self, relative):
        return (self.root / relative).read_bytes().decode("utf-8")

    def save_registry(self):
        self.write("TOOL_REGISTRY.json", json.dumps(self.value))

    def codes(self):
        return {e["code"] for e in seo.validate(self.root)["errors"]}

    def replace(self, relative, old, new):
        source = self.read(relative)
        self.assertIn(old, source)
        self.write(relative, source.replace(old, new))

    def test_public_allowlist_released_only_with_real_directory_routes(self):
        result = seo.validate(self.root)
        self.assertEqual(result["status"], "PASS", result)
        self.assertEqual(result["counts"], {"released_tools": 2, "public_pages": 4})
        urls = [p["url"] for p in seo.eligible_pages(self.root)]
        self.assertEqual(urls, sorted([seo.ORIGIN + "/" + p for p in ["index.html", "privacy.html", "actual-route/index.html", "zeta-tool/index.html"]]))
        self.assertNotIn("canonical", self.read("waiting-tool/index.html"))
        self.assertNotIn("canonical", self.read("templates/tool-page.html"))

    def test_generation_is_idempotent_and_registry_unchanged(self):
        before = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(seo.generate(self.root, True)["changed_files"], [])
        self.assertEqual(seo.generate(self.root)["changed_files"], [])
        self.assertTrue(all(p.read_bytes() == b for p, b in before.items()))
        self.assertNotIn("lastmod", self.read("sitemap.xml"))

    def test_missing_canonical_is_actionable_and_read_only(self):
        self.replace("actual-route/index.html", "  " + seo.canonical_tag(seo.ORIGIN + "/actual-route/index.html") + "\n", "")
        old = self.read("actual-route/index.html")
        result = seo.validate(self.root)
        self.assertIn("SEO_CANONICAL_MISSING", {e["code"] for e in result["errors"]})
        self.assertTrue(any(e["path"] == "actual-route/index.html" for e in result["errors"]))
        self.assertEqual(self.read("actual-route/index.html"), old)

    def test_duplicate_canonical_tags_rejected(self):
        tag = seo.canonical_tag(seo.ORIGIN + "/index.html")
        self.replace("index.html", tag, tag + tag)
        self.assertIn("SEO_CANONICAL_DUPLICATE", self.codes())
        with self.assertRaises(seo.SEOError):
            seo.generate(self.root, True)

    def test_invalid_domain_scheme_query_fragment_and_escaping_rejected(self):
        original = self.read("index.html")
        for url in ["/index.html", "http://everydaydigitalbox.com/index.html", "https://evil.invalid/index.html",
                    "https://everydaydigitalbox.com:443/index.html", "https://user@everydaydigitalbox.com/index.html",
                    seo.ORIGIN + "/index.html?", seo.ORIGIN + "/index.html#", seo.ORIGIN + "/index.html?x=1",
                    seo.ORIGIN + "/%69ndex.html", seo.ORIGIN + "/../index.html", "https://[bad/index.html"]:
            with self.subTest(url=url):
                self.write("index.html", original.replace(seo.ORIGIN + "/index.html", url))
                self.assertIn("SEO_CANONICAL_URL", self.codes())

    def test_wrong_valid_target_is_not_accepted_as_self_canonical(self):
        self.replace("index.html", seo.ORIGIN + "/index.html", seo.ORIGIN + "/privacy.html")
        self.assertIn("SEO_CANONICAL_MISMATCH", self.codes())

    def test_missing_canonical_target_detected(self):
        self.replace("index.html", seo.ORIGIN + "/index.html", seo.ORIGIN + "/nonexistent/index.html")
        self.assertIn("SEO_CANONICAL_TARGET", self.codes())

    def test_released_missing_source_fails_eligibility(self):
        (self.root / "actual-route/index.html").unlink()
        result = seo.validate(self.root)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("actual-route", str(result))

    def test_canonical_outside_head_or_in_inert_template_rejected(self):
        original = self.read("index.html")
        tag = seo.canonical_tag(seo.ORIGIN + "/index.html")
        for source in [original.replace(tag, "").replace("<body>", "<body>" + tag), original.replace(tag, "<template>" + tag + "</template>")]:
            with self.subTest(source=source):
                self.write("index.html", source)
                self.assertIn("SEO_CANONICAL_HEAD", self.codes())
        for prefix in ["<div>body content</div>", "body text", "&nbsp;", "</title>body text"]:
            with self.subTest(implicit_head_close=prefix):
                self.write("index.html", original.replace(tag, prefix + tag))
                self.assertTrue({"SEO_HEAD", "SEO_CANONICAL_HEAD"}.issubset(self.codes()))

    def test_duplicate_rel_and_href_attributes_rejected(self):
        self.replace("index.html", 'rel="canonical"', 'rel="canonical" rel="stylesheet"')
        self.assertIn("SEO_CANONICAL_ATTRIBUTES", self.codes())

    def test_noindex_and_none_on_released_pages_rejected(self):
        original = self.read("index.html")
        for directive in ['<meta name="robots" content="noindex, follow">', '<meta name="googlebot" content="NONE">']:
            with self.subTest(directive=directive):
                self.write("index.html", original.replace("</head>", directive + "</head>"))
                self.assertIn("SEO_NOINDEX", self.codes())
                with self.assertRaises(seo.SEOError):
                    seo.generate(self.root, True)

    def test_sitemap_invalid_xml_and_raw_ampersand_fail(self):
        for xml in ["<urlset>", '<urlset xmlns="' + seo.NAMESPACE + '"><url><loc>' + seo.ORIGIN + '/index.html?a=1&b=2</loc></url></urlset>']:
            with self.subTest(xml=xml):
                self.write("sitemap.xml", xml)
                self.assertIn("SEO_SITEMAP_XML", self.codes())

    def test_sitemap_entity_declarations_rejected(self):
        self.write("sitemap.xml", '<!DOCTYPE urlset [<!ENTITY value "unsafe">]><urlset xmlns="' + seo.NAMESPACE + '"></urlset>')
        self.assertIn("SEO_SITEMAP_XML", self.codes())

    def test_sitemap_duplicate_missing_and_ineligible_entries(self):
        xml = self.read("sitemap.xml")
        entry = "  <url>\n    <loc>" + seo.ORIGIN + "/index.html</loc>\n  </url>"
        self.replace("sitemap.xml", "</urlset>", entry + "\n</urlset>")
        self.assertIn("SEO_SITEMAP_DUPLICATE", self.codes())
        self.write("sitemap.xml", xml.replace(entry, ""))
        self.assertIn("SEO_SITEMAP_MISSING", self.codes())
        for slug in ["waiting-tool", "future-tool", "blocked-tool", "templates"]:
            with self.subTest(slug=slug):
                self.write("sitemap.xml", xml.replace("/index.html</loc>", "/" + slug + "/index.html</loc>", 1))
                self.assertIn("SEO_SITEMAP_INELIGIBLE", self.codes())

    def test_sitemap_wrong_root_namespace_and_lastmod_fail(self):
        xml = self.read("sitemap.xml")
        self.write("sitemap.xml", xml.replace(seo.NAMESPACE, "https://wrong.invalid/"))
        self.assertIn("SEO_SITEMAP_ROOT", self.codes())
        self.write("sitemap.xml", xml.replace("</loc>", "</loc><lastmod>2026-11-07</lastmod>", 1))
        self.assertIn("SEO_SITEMAP_ENTRY", self.codes())

    def test_stale_sitemap_format_and_order_detected(self):
        xml = self.read("sitemap.xml")
        self.write("sitemap.xml", xml.replace("  <url>", " <url>"))
        self.assertIn("SEO_SITEMAP_STALE", self.codes())
        self.assertEqual(seo.generate(self.root)["changed_files"], ["sitemap.xml"])
        self.assertEqual(seo.validate(self.root)["status"], "PASS")

    def test_git_crlf_sitemap_is_not_spurious_staleness(self):
        self.write("sitemap.xml", self.read("sitemap.xml").replace("\n", "\r\n"))
        self.assertEqual(seo.validate(self.root)["status"], "PASS")
        self.assertEqual(seo.generate(self.root)["changed_files"], [])

    def test_no_sitemap_and_no_robots_report_friendly_errors(self):
        (self.root / "sitemap.xml").unlink()
        (self.root / "robots.txt").unlink()
        self.assertTrue({"SEO_SITEMAP_READ", "SEO_ROBOTS_READ"}.issubset(self.codes()))

    def test_robots_sitemap_duplicates_external_and_blocking_rules_fail(self):
        for robots in [seo.ROBOTS_TEXT.replace(seo.SITEMAP_URL, "http://evil.invalid/sitemap.xml"),
                       seo.ROBOTS_TEXT + "Sitemap: " + seo.SITEMAP_URL + "\n",
                       seo.ROBOTS_TEXT.replace("Disallow:", "Disallow: /"),
                       seo.ROBOTS_TEXT + "Disallow: /assets/\n",
                       "User-agent: Googlebot\nDisallow:\nSitemap: " + seo.SITEMAP_URL + "\n"]:
            with self.subTest(robots=robots):
                self.write("robots.txt", robots)
                self.assertIn("SEO_ROBOTS_POLICY", self.codes())

    def test_robots_allows_explanatory_comments_but_not_unknown_directives(self):
        self.write("robots.txt", "# Sitemap discovery, not access control\n" + seo.ROBOTS_TEXT)
        self.assertEqual(seo.validate(self.root)["status"], "PASS")
        self.write("robots.txt", seo.ROBOTS_TEXT + "Crawl-delay: 10\n")
        self.assertIn("SEO_ROBOTS_POLICY", self.codes())

    def test_registry_bad_routes_duplicate_directories_domain_and_status_fail(self):
        original = copy.deepcopy(self.value)
        for route in ["../escape", "/absolute", "bad?query", "bad%2fpath", "con"]:
            with self.subTest(route=route):
                self.value = copy.deepcopy(original)
                self.value["tools"][3]["directory_path"] = route
                self.save_registry()
                self.assertIn("SEO_ELIGIBILITY", self.codes())
        self.value = copy.deepcopy(original)
        self.value["tools"][3]["directory_path"] = "actual-route"
        self.save_registry()
        self.assertIn("SEO_ELIGIBILITY", self.codes())
        self.value = copy.deepcopy(original)
        self.value["project"]["website"] = "https://evil.invalid/"
        self.save_registry()
        self.assertIn("SEO_ELIGIBILITY", self.codes())

    def test_symlink_inputs_are_rejected_before_read_or_write(self):
        with patch.object(Path, "is_symlink", return_value=True):
            with self.assertRaises(seo.SEOError):
                seo.generate(self.root, True)
            self.assertIn("SEO_ELIGIBILITY", self.codes())

    def test_sync_plans_every_page_before_any_mutation(self):
        self.replace("index.html", "  " + seo.canonical_tag(seo.ORIGIN + "/index.html") + "\n", "")
        self.replace("zeta-tool/index.html", "</head>", '<meta name="robots" content="noindex"></head>')
        before = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        with self.assertRaises(seo.SEOError):
            seo.generate(self.root, True)
        self.assertTrue(all(p.read_bytes() == b for p, b in before.items()))

    def test_exact_annotation_preserves_crlf_compact_and_comment_heads(self):
        url = seo.ORIGIN + "/privacy.html"
        tag = seo.canonical_tag(url)
        for source, expected in [
            ("<html><head>\r\n<title>x</title></head><body>café</body></html>", "<html><head>\r\n  " + tag + "\r\n<title>x</title></head><body>café</body></html>"),
            ("<html><head><title>x</title></head><body>x</body></html>", "<html><head>\n  " + tag + "\n<title>x</title></head><body>x</body></html>"),
            ("<!-- <head>fake</head> -->\n<html><head>\n</head><body></body></html>", "<!-- <head>fake</head> -->\n<html><head>\n  " + tag + "\n</head><body></body></html>")]:
            with self.subTest(source=source):
                actual = seo.annotate_html(source, url)
                self.assertEqual(actual, expected)
                self.assertEqual(seo.annotate_html(actual, url), actual)

    def test_canonical_in_script_and_comments_does_not_count(self):
        source = '<html><head>\n<script>const example="<head><link rel=canonical href=bad>";</script><!-- <link rel="canonical" href="bad"> --></head><body></body></html>'
        actual = seo.annotate_html(source, seo.ORIGIN + "/index.html")
        self.assertEqual(len(seo.metadata(actual).canonicals), 1)
        self.assertTrue(actual.endswith(source[source.index("<script>"):]))
        # HTMLParser in the pinned Python 3.14 must preserve browser title RCDATA semantics.
        title_example = '<html><head><title>' + seo.canonical_tag(seo.ORIGIN + '/index.html') + '</title></head><body></body></html>'
        self.write("index.html", title_example)
        self.assertIn("SEO_CANONICAL_MISSING", self.codes())

    def test_generator_does_not_repair_bad_canonical_by_default(self):
        self.replace("index.html", seo.ORIGIN + "/index.html", seo.ORIGIN + "/privacy.html")
        before = self.read("sitemap.xml")
        with self.assertRaises(seo.SEOError):
            seo.generate(self.root)
        self.assertEqual(self.read("sitemap.xml"), before)

    def test_cli_json_validation_is_read_only_and_failure_is_nonzero(self):
        command = [sys.executable, str(SCRIPTS / "validate_seo.py"), "--root", str(self.root), "--json", "--no-report"]
        success = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(success.returncode, 0, success.stderr)
        self.assertEqual(json.loads(success.stdout)["warnings"], [])
        self.write("sitemap.xml", "broken")
        failed = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(failed.returncode, 1)
        self.assertEqual(json.loads(failed.stdout)["status"], "FAIL")
        self.assertEqual(self.read("sitemap.xml"), "broken")


if __name__ == "__main__":
    unittest.main()
