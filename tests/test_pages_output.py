"""Publishing-policy mutations; real Jekyll output is separately mandatory in CI."""
from contextlib import contextmanager
import copy
import html
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '_publishing'))
import verify_site as publishing
import css_overlay as approval


class PagesOutputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='edb-pages-output-')
        cls.directory = Path(cls.temp.name)
        cls.site = cls.directory / 'site'
        cls.policy = json.loads((ROOT / publishing.POLICY).read_text(encoding='utf-8'))
        # Synthetic output only tests the guard. CI builds actual Jekyll output.
        for name in cls.policy['output_paths']:
            path = cls.site / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b'fixture')
        for name, meta in cls.policy['html'].items():
            source = '<!doctype html><html><head>'
            for url in meta['canonicals']:
                source += '<link rel="canonical" href="' + html.escape(url, quote=True) + '">'
            for agent, content in meta['robots']:
                source += '<meta name="' + agent + '" content="' + html.escape(content, quote=True) + '">'
            for content in meta['refresh']:
                source += '<meta http-equiv="refresh" content="' + html.escape(content, quote=True) + '">'
            (cls.site / name).write_text(source + '</head><body>fixture</body></html>', encoding='utf-8')
        for name in [*cls.policy['canonical_pages'], *cls.policy['exact_public_files']]:
            (cls.site / name).write_bytes(publishing.approved_bytes(ROOT, name, cls.policy))
        # The actual theme CSS is verified against production in real-build CI.
        cls.policy['generated_asset_hashes'] = {}

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    @contextmanager
    def changed(self, name, data=None):
        path = self.site / name
        old = path.read_bytes() if path.exists() else None
        path.parent.mkdir(parents=True, exist_ok=True)
        if data is None:
            path.unlink()
        else:
            path.write_bytes(data)
        try:
            yield
        finally:
            if old is None:
                path.unlink()
            else:
                path.write_bytes(old)

    def verify(self):
        return publishing.verify_output(self.site, ROOT, self.policy)

    def rejects(self):
        with self.assertRaises(ValueError):
            self.verify()

    def test_reviewed_inventory_preserves_89_canonicals_and_48_historical_routes(self):
        result = self.verify()
        self.assertEqual(result['canonical_pages'], 89)
        self.assertEqual(result['sitemap_urls'], 89)
        self.assertEqual(result['historical_html_routes_retained'], 48)
        self.assertEqual(result['output_files'], 1130)

    def test_new_markdown_html_explicit_html_noindex_and_raw_documents_are_rejected(self):
        for name, data in [
            ('INTERNAL_NOTES.html', b'<link rel="canonical" href="https://everydaydigitalbox.com/INTERNAL_NOTES.html">'),
            ('unexpected/index.html', b'<title>Explicit HTML</title>'),
            ('unexpected.htm', b'<meta name="ROBOTS" content="NOINDEX, follow">'),
            ('new-document.md', b'# Internal notes'),
            ('redirect', b'<meta http-equiv="refresh" content="0;url=/">'),
        ]:
            with self.subTest(path=name), self.changed(name, data):
                self.rejects()

    def test_all_design_document_routes_and_alternative_names_are_rejected(self):
        for name in ['HOMEPAGE_DESIGN.html', 'HOMEPAGE_DESIGN', 'HOMEPAGE_DESIGN.md',
                     'HOMEPAGE_DESIGN/index.html', 'nested/HOMEPAGE_DESIGN.html']:
            with self.subTest(path=name), self.changed(name, b'internal'):
                self.rejects()

    def test_internal_controls_cannot_leak_as_static_files(self):
        for name in ['_publishing/output-policy.json', 'scripts/_publishing_approval_identity.py',
                     'tests/test_pages_output.py', 'CNAME', 'vendor/bundle/internal.txt', 'Gemfile']:
            with self.subTest(path=name), self.changed(name, b'internal'):
                self.rejects()

    def test_historical_route_removal_is_not_silently_approved(self):
        with self.changed('AGENTS.html'):
            self.rejects()

    def test_canonical_changes_duplicates_noindex_and_refresh_fail(self):
        raw = (self.site / 'index.html').read_bytes()
        for extra in [b'<link rel="canonical" href="https://example.invalid/">',
                      b'<meta name="robots" content="noindex">',
                      b'<meta name="Googlebot" content="none">',
                      b'<meta http-equiv="refresh" content="0;url=/AGENTS.html">']:
            with self.subTest(extra=extra), self.changed('index.html', raw.replace(b'</head>', extra + b'</head>')):
                self.rejects()

    def test_historical_canonical_and_noindex_metadata_cannot_drift(self):
        for name in ['AGENTS.html', 'templates/text-input.html']:
            raw = (self.site / name).read_bytes()
            with self.changed(name, raw.replace(b'</head>', b'<meta name="robots" content="noindex"></head>')):
                self.rejects()

    def test_metadata_understands_canonical_tokens_and_case_insensitive_robot_directives(self):
        value = publishing.metadata('<LINK REL="alternate CANONICAL" HREF="https://example.test/"><META NAME="ROBOTS" CONTENT="INDEX, NoIndex"><meta http-equiv="Refresh" content="0;url=/">')
        self.assertEqual(value['canonicals'], ['https://example.test/'])
        self.assertTrue(value['noindex'])
        self.assertEqual(value['refresh'], ['0;url=/'])

    def test_generated_source_and_discovery_file_tampering_fails(self):
        for name in ['index.html', 'sitemap.xml', 'robots.txt', 'assets/consent.js',
                     'assets/css/homepage.13bda86daed58e77.css', 'assets/css/site.d8c3bb4f35a90e73.css']:
            raw = (self.site / name).read_bytes()
            with self.subTest(path=name), self.changed(name, raw + b' '):
                self.rejects()

    def test_theme_hash_is_checked(self):
        policy = copy.deepcopy(self.policy)
        policy['generated_asset_hashes'] = {'assets/css/style.css': '0' * 64}
        with self.assertRaisesRegex(ValueError, 'theme asset'):
            publishing.verify_output(self.site, ROOT, policy)

    def test_config_replacement_defaults_and_scope_are_strict(self):
        root = self.directory / 'config-fixture'
        root.mkdir(exist_ok=True)
        raw = (ROOT / '_config.yml').read_text(encoding='utf-8')
        for value in [raw.replace('  - CNAME\n', ''), raw.replace('  - node_modules\n', ''),
                      raw.replace('  - vendor/ruby/\n', ''), raw + 'include: [HOMEPAGE_DESIGN.md]\n']:
            (root / '_config.yml').write_text(value, encoding='utf-8')
            with self.assertRaises(ValueError):
                publishing.check_config(root)
        (root / '_config.yml').write_text(raw, encoding='utf-8')
        publishing.check_config(root)

    def test_new_markdown_with_existing_permalink_cannot_bypass_inventory(self):
        root = self.directory / 'markdown-fixture'
        root.mkdir(exist_ok=True)
        for name in ['new.md', 'new.markdown', 'new.mkdown', 'new.mkdn', 'new.mkd']:
            path = root / name
            path.write_text('---\npermalink: /AGENTS.html\n---\n# Internal', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'Markdown source inventory'):
                publishing.check_markdown_sources(root, [])
            path.unlink()

    def test_current_publishing_approval_and_frozen_task_2d_are_bound(self):
        value = approval.validate_current(ROOT)
        self.assertEqual(value['publishing_parent_revision'], '1634bff8449db3a5398f5e0c1d070098b3cd2f16')
        names = ['_config.yml', publishing.POLICY, '_publishing/verify_site.py',
                 'audit/SEO_TASK_2D_SOURCE_APPROVAL.json', 'scripts/homepage_approval_identity.py',
                 'HOMEPAGE_DESIGN.md', approval.MANIFEST, approval.IDENTITY]
        with tempfile.TemporaryDirectory(prefix='edb-pages-approval-') as temp:
            root = Path(temp)
            for name in [*value['files'], approval.MANIFEST, approval.IDENTITY]:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / name, path)
            for name in names:
                path = root / name
                original = path.read_bytes()
                try:
                    path.write_bytes(original + b' ')
                    with self.subTest(path=name), self.assertRaises(ValueError):
                        approval.validate_current(root)
                finally:
                    path.write_bytes(original)
            approval.validate_current(root)
