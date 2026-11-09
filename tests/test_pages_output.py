"""Publishing-policy mutations; real Jekyll output is separately mandatory in CI."""
from contextlib import contextmanager
import copy
import gzip
import hashlib
import html
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '_publishing'))
import verify_site as publishing
import css_overlay as approval


# Temporary baseline instrumentation for the authorized development diagnostic.
# Test selection, assertions, fixture behavior and CI deadlines are unchanged.
if os.environ.get('GITHUB_ACTIONS') == 'true' and os.environ.get('GITHUB_REF') == 'refs/heads/seo/task-2e3-pages-cleanup':
    class _PhaseATimingResult(unittest.TextTestResult):
        def startTest(self, test):
            super().startTest(test)
            self._phase_a_started = time.perf_counter()

        def stopTest(self, test):
            print('EDB_TEST_TIMING=' + json.dumps({'id': test.id(), 'seconds': time.perf_counter() - self._phase_a_started}), flush=True)
            super().stopTest(test)

    unittest.TextTestRunner.resultclass = _PhaseATimingResult


class PagesOutputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='edb-pages-output-')
        cls.directory = Path(cls.temp.name)
        cls.site = cls.directory / 'site'
        # Preserve the Task 2E.1 assertions as a frozen predecessor fixture.
        cls.policy = json.loads((ROOT / '_publishing/output-policy.json').read_text(encoding='utf-8'))
        cls.policy['markdown_source_paths'].append('_publishing/SEO_TASK_2E3_PHASE_A.md')
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

        cls.legacy_site = cls.directory / 'legacy-site'
        cls.legacy_policy = json.loads((ROOT / '_publishing/SEO_TASK_2D2_OUTPUT_POLICY.json').read_text(encoding='utf-8'))
        cls.legacy_policy['markdown_source_paths'] = cls.policy['markdown_source_paths']
        cls.legacy_policy['generated_asset_hashes'] = {}
        shutil.copytree(cls.site, cls.legacy_site)
        for name in set(cls.legacy_policy['output_paths']) - set(cls.policy['output_paths']):
            target = cls.legacy_site / name
            target.parent.mkdir(parents=True, exist_ok=True)
            if name in cls.legacy_policy['html']:
                meta = cls.legacy_policy['html'][name]
                content = '<html><head>'
                for url in meta['canonicals']:
                    content += '<link rel="canonical" href="' + html.escape(url, quote=True) + '">'
                for agent, value in meta['robots']:
                    content += '<meta name="' + agent + '" content="' + html.escape(value, quote=True) + '">'
                target.write_text(content + '</head></html>', encoding='utf-8')
            else:
                target.write_bytes(b'legacy fixture')

    @contextmanager
    def legacy(self):
        site, policy = self.site, self.policy
        self.site, self.policy = self.legacy_site, self.legacy_policy
        try:
            yield
        finally:
            self.site, self.policy = site, policy

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
        with self.legacy():
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
        with self.legacy(), self.changed('AGENTS.html'):
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
        with self.legacy():
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
                 'HOMEPAGE_DESIGN.md', '_publishing/SEO_TASK_2D2_SOURCE_APPROVAL.json',
                 'scripts/_publishing_approval_identity.py', approval.MANIFEST, approval.IDENTITY]
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

    def test_current_inventory_has_only_89_canonical_html_outputs(self):
        result = self.verify()
        self.assertEqual(result['canonical_pages'], 89)
        self.assertEqual(result['html_pages'], 89)
        self.assertEqual(result['historical_html_routes_retained'], 0)
        self.assertEqual(result['retired_html_outputs'], 48)
        self.assertEqual(result['retired_output_files'], 93)
        self.assertEqual(result['output_files'], 1037)

    def test_every_retired_html_markdown_and_alias_is_rejected(self):
        paths = set(self.policy['retired_output_paths'])
        for row in self.policy['retired_routes']:
            paths.update(row['aliases'])
        paths = {name + 'index.html' if name.endswith('/') else name for name in paths}
        for name in sorted(paths):
            # A directory URL is served through its index, not directory bytes.
            if (self.site / name).is_dir():
                name = name.rstrip('/') + '/index.html'
            with self.subTest(path=name), self.changed(name, b'<meta http-equiv="refresh" content="0;url=/">'):
                self.rejects()

    def test_no_approved_page_or_runtime_file_may_disappear(self):
        for name in [*self.policy['canonical_pages'], *self.policy['exact_public_files']]:
            with self.subTest(path=name), self.changed(name):
                self.rejects()

    def test_retired_history_hash_and_2e1_predecessor_are_strict(self):
        value = approval.validate_current(ROOT)
        self.assertEqual(value['historical_publishing_parent_revision'], '3d78c267b479690331fd618e2982c51cbdc6da4b')
        for row in self.policy['retired_routes']:
            import hashlib
            data = (ROOT / row['source']).read_bytes().replace(b'\r\n', b'\n')
            self.assertEqual(hashlib.sha256(data).hexdigest(), row['source_sha256'])
        policy = copy.deepcopy(self.policy)
        policy['retired_routes'][0]['source_sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'history changed'):
            publishing.verify_output(self.site, ROOT, policy)


class PhaseAOutputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='edb-phase-a-output-')
        cls.directory = Path(cls.temp.name)
        cls.site = cls.directory / 'site'
        cls.policy = json.loads((ROOT / publishing.POLICY).read_text(encoding='utf-8'))
        cls.scope = json.loads((ROOT / publishing.SCOPE).read_text(encoding='utf-8'))
        cls.candidates = publishing.reviewed_candidates(ROOT)
        # Exact source bytes plus the pinned old theme build are a guard fixture,
        # not a replacement for the mandatory new real Pages/Jekyll artifact.
        for name in cls.policy['output_paths']:
            target = cls.site / name
            target.parent.mkdir(parents=True, exist_ok=True)
            if name == 'assets/css/style.css':
                data = gzip.decompress((ROOT / '_publishing/fixtures/seo2e1-theme.css.gz').read_bytes())
            else:
                data = (ROOT / name).read_bytes()
                if not name.endswith('.css'):
                    data = data.replace(b'\r\n', b'\n')
            target.write_bytes(data)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    changed = PagesOutputTests.changed
    verify = PagesOutputTests.verify
    rejects = PagesOutputTests.rejects

    def test_recovered_raw_checksum_precedes_semantic_json_parsing(self):
        raw = (ROOT / publishing.CANDIDATES).read_bytes()
        lf = raw.replace(b'\r\n', b'\n')
        self.assertNotEqual(raw, lf)
        self.assertEqual(hashlib.sha256(raw).hexdigest(), publishing.AUDIT_CANDIDATES_SHA256)
        self.assertNotEqual(hashlib.sha256(lf).hexdigest(), publishing.AUDIT_CANDIDATES_SHA256)
        self.assertEqual(json.loads(raw), json.loads(lf))
        self.assertEqual(publishing.reviewed_candidates(ROOT), json.loads(raw))
        self.assertEqual(approval.validate_current(ROOT)['files'][publishing.CANDIDATES]['normalization'], 'bytes')

    def test_line_ending_conversion_whitespace_and_content_tampering_fail_raw_integrity(self):
        raw = (ROOT / publishing.CANDIDATES).read_bytes()
        with tempfile.TemporaryDirectory(prefix='edb-audit-raw-') as temp:
            root = Path(temp)
            target = root / publishing.CANDIDATES
            target.parent.mkdir(parents=True)
            target.write_bytes(raw)
            self.assertEqual(publishing.reviewed_candidates(root), self.candidates)
            for data in [raw.replace(b'\r\n', b'\n'), raw + b' ', raw.replace(b'841', b'840', 1), raw[:-1], b'corrupt']:
                self.assertNotEqual(data, raw)
                target.write_bytes(data)
                with self.subTest(digest=hashlib.sha256(data).hexdigest()), self.assertRaisesRegex(ValueError, 'Recovered candidate record changed'):
                    publishing.reviewed_candidates(root)

    def test_git_preserves_audit_raw_bytes_with_lf_and_crlf_checkout_settings(self):
        raw = (ROOT / publishing.CANDIDATES).read_bytes()
        attributes = (ROOT / '.gitattributes').read_bytes()
        for autocrlf in ['false', 'true', 'input']:
            with self.subTest(autocrlf=autocrlf), tempfile.TemporaryDirectory(prefix='edb-audit-git-') as temp:
                root = Path(temp) / 'repo'
                root.mkdir()
                subprocess.run(['git', 'init', '--quiet', str(root)], check=True, capture_output=True)
                target = root / publishing.CANDIDATES
                target.parent.mkdir(parents=True)
                target.write_bytes(raw)
                (root / '.gitattributes').write_bytes(attributes)
                command = ['git', '-c', 'core.autocrlf=' + autocrlf, '-C', str(root)]
                subprocess.run([*command, 'add', '.gitattributes', publishing.CANDIDATES], check=True, capture_output=True)
                self.assertEqual(subprocess.check_output([*command, 'show', ':' + publishing.CANDIDATES]), raw)
                checkout = Path(temp) / 'checkout'
                subprocess.run([*command, 'checkout-index', '--all', '--prefix=' + checkout.as_posix() + '/'], check=True, capture_output=True)
                self.assertEqual((checkout / publishing.CANDIDATES).read_bytes(), raw)
                publishing.reviewed_candidates(checkout)

    def test_git_staged_whitespace_accepts_frozen_crlf_but_rejects_real_errors(self):
        raw = (ROOT / publishing.CANDIDATES).read_bytes()
        self.assertEqual(raw.count(b'\r\n'), 1459)
        self.assertEqual(hashlib.sha256(raw).hexdigest(), publishing.AUDIT_CANDIDATES_SHA256)
        with tempfile.TemporaryDirectory(prefix='edb-audit-whitespace-') as temp:
            root = Path(temp)
            subprocess.run(['git', 'init', '--quiet', str(root)], check=True, capture_output=True)
            command = ['git', '-c', 'core.autocrlf=false', '-c',
                       'core.whitespace=blank-at-eol,blank-at-eof,space-before-tab', '-C', str(root)]
            (root / '.gitattributes').write_bytes((ROOT / '.gitattributes').read_bytes().replace(b'\r\n', b'\n'))
            target = root / publishing.CANDIDATES
            target.parent.mkdir(parents=True)
            target.write_bytes(raw)
            subprocess.run([*command, 'add', '.gitattributes', publishing.CANDIDATES], check=True, capture_output=True)
            result = subprocess.run([*command, 'diff', '--cached', '--check'], capture_output=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(subprocess.check_output([*command, 'show', ':' + publishing.CANDIDATES]), raw)
            self.assertEqual(target.read_bytes(), raw)
            self.assertEqual(publishing.reviewed_candidates(root), self.candidates)
            errors = [
                (raw.replace(b'\r\n', b' \r\n', 1), b'trailing whitespace'),
                (raw + b'\r\n', b'new blank line at eof'),
                (raw.replace(b'\r\n', b'\r\n \t', 1), b'space before tab in indent'),
            ]
            for data, diagnostic in errors:
                with self.subTest(diagnostic=diagnostic):
                    target.write_bytes(data)
                    subprocess.run([*command, 'add', publishing.CANDIDATES], check=True, capture_output=True)
                    result = subprocess.run([*command, 'diff', '--cached', '--check'], capture_output=True)
                    self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                    self.assertIn(diagnostic, result.stdout.lower())
                    with self.assertRaisesRegex(ValueError, 'Recovered candidate record changed'):
                        publishing.reviewed_candidates(root)
            # The exception must not apply to another file, even in the same directory.
            other = '_publishing/unrelated.json'
            (root / other).write_bytes(b'{}\r\n')
            subprocess.run([*command, 'add', other], check=True, capture_output=True)
            result = subprocess.run([*command, 'diff', '--cached', '--check', '--', other], capture_output=True)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn(b'trailing whitespace', result.stdout.lower())
        self.assertEqual((ROOT / publishing.CANDIDATES).read_bytes(), raw)

    def test_exact_841_subtraction_and_all_196_retained_hashes(self):
        result = self.verify()
        self.assertEqual(result['output_files'], 196)
        self.assertEqual(result['html_pages'], 89)
        self.assertEqual(result['phase_a_excluded_files'], 841)
        self.assertEqual(result['owner_review_files_retained'], 90)
        self.assertEqual(result['retained_output_hashes_verified'], 196)
        self.assertEqual(result['retired_output_files'], 93)
        previous = json.loads((ROOT / publishing.PREDECESSOR).read_text(encoding='utf-8'))
        excluded = set(self.scope['excluded_output_sha256'])
        self.assertEqual(set(previous['output_paths']) - set(self.policy['output_paths']), excluded)
        self.assertFalse(excluded & set(self.policy['output_paths']))
        self.assertEqual(len(excluded), 841)

    def test_each_approved_exclusion_cannot_reappear_as_a_raw_file(self):
        for name in self.scope['excluded_output_sha256']:
            with self.subTest(path=name), self.changed(name, b'unapproved publication'):
                self.rejects()

    def test_raw_extensionless_directory_html_and_encoded_aliases_fail(self):
        for group in self.candidates['exact_sets']:
            source = group['exact_paths'][0]
            stem = source.rsplit('.', 1)[0]
            encoded = source.replace('/', '%2F') if '/' in source else source.replace('.', '%2E')
            for name in [stem, stem + '/index.html', source + '/index.html', stem + '.html', encoded]:
                if (self.site / name).is_dir():
                    name += '/index.html'
                with self.subTest(group=group['id'], alias=name), self.changed(name, b'---\npermalink: /index.html\n---\ninternal'):
                    self.rejects()

    def test_all_90_review_holds_and_all_runtime_public_assets_are_required(self):
        names = set(self.scope['owner_review_keep_paths']) | set(self.scope['required_runtime_keep_paths']) | set(self.scope['intentionally_public_keep_paths'])
        self.assertEqual(len(names), 107)
        for name in sorted(names):
            with self.subTest(path=name), self.changed(name):
                self.rejects()

    def test_every_retained_non_html_file_requires_exact_production_bytes(self):
        for name in sorted(set(self.policy['output_paths']) - set(self.policy['canonical_pages'])):
            raw = (self.site / name).read_bytes()
            with self.subTest(path=name), self.changed(name, raw + b' '):
                self.rejects()

    def test_every_canonical_page_and_retired_output_remains_protected(self):
        for name in self.policy['canonical_pages']:
            with self.subTest(path=name), self.changed(name):
                self.rejects()
        for name in self.policy['retired_output_paths']:
            with self.subTest(path=name), self.changed(name, b'reintroduced history'):
                self.rejects()

    def test_unlisted_output_and_reintroduced_front_matter_fail(self):
        for name in ['unlisted.json', 'new.md', 'new.html', 'redirect/index.html']:
            with self.subTest(path=name), self.changed(name, b'---\npermalink: /index.html\n---\ninternal'):
                self.rejects()
        raw = (self.site / 'index.html').read_bytes()
        with self.changed('index.html', b'front matter overwrote an approved route' + raw):
            self.rejects()

    def test_phase_a_cannot_silently_expand_the_reviewed_output_delta(self):
        for field in ['canonical_pages', 'public_output_hashes', 'generated_asset_hashes', 'retired_routes']:
            policy = copy.deepcopy(self.policy)
            policy[field] = {} if isinstance(policy[field], dict) else []
            with self.subTest(field=field), self.assertRaises(ValueError):
                publishing.phase_a_contract(ROOT, policy)
        policy = copy.deepcopy(self.policy)
        policy['output_paths'].append(next(iter(self.scope['excluded_output_sha256'])))
        with self.assertRaises(ValueError):
            publishing.phase_a_contract(ROOT, policy)

    def test_successor_and_frozen_predecessors_are_bound_before_projection(self):
        value = approval.validate_current(ROOT)
        self.assertEqual(value['phase_a_parent_revision'], '34992b8f8ac3e73efbea820bb18c96dae145ff19')
        paths = [publishing.POLICY, publishing.SCOPE, publishing.CANDIDATES, publishing.PREDECESSOR,
                 '_publishing/SEO_TASK_2E1_SOURCE_APPROVAL.json', 'scripts/_historical_publishing_approval_identity.py',
                 approval.MANIFEST, approval.IDENTITY]
        with tempfile.TemporaryDirectory(prefix='edb-phase-a-approval-') as temp:
            root = Path(temp)
            for name in [*value['files'], approval.MANIFEST, approval.IDENTITY]:
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / name, target)
            for name in paths:
                path = root / name
                raw = path.read_bytes()
                try:
                    path.write_bytes(raw + b' ')
                    with self.subTest(path=name), self.assertRaises(ValueError):
                        approval.validate_current(root)
                finally:
                    path.write_bytes(raw)
            approval.validate_current(root)
