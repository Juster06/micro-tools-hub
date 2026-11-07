"""Canonical candidates preserve exact historical evidence without widening it."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import seo
import seo_overlay as overlay
import tracking


class SEOOverlayTests(unittest.TestCase):
    def setUp(self):
        self.manifest = overlay.manifest(ROOT)

    def source(self, path):
        return (ROOT / path).read_text(encoding='utf-8')

    def test_all_89_current_pages_reconstruct_exact_frozen_main_and_generator(self):
        registry = json.loads(self.source('TOOL_REGISTRY.json'))
        expected = {'index.html', 'privacy.html'} | {
            tool['directory_path'] + '/index.html' for tool in registry['tools']
            if tool['status'] == 'RELEASED'}
        self.assertEqual(set(self.manifest['pages']), expected)
        self.assertEqual(len(expected), 89)
        for path, entry in self.manifest['pages'].items():
            with self.subTest(path=path):
                source = self.source(path)
                self.assertEqual(overlay.digest(source), entry['candidate_sha256'])
                previous = overlay.historical_source(ROOT, path, source)
                self.assertEqual(overlay.digest(previous), entry['previous_sha256'])
                self.assertEqual(seo.annotate_html(previous, entry['canonical']), source)

    def test_manifest_preimages_match_actual_git_baseline_for_both_head_forms(self):
        for path in ('index.html', 'privacy.html', 'sha-256-hash-checker/index.html',
                     'word-frequency-analyzer/index.html', 'scripts/ci/run.py'):
            with self.subTest(path=path):
                baseline = subprocess.check_output(
                    ['git', 'show', overlay.BASE_REVISION + ':' + path], cwd=ROOT).decode('utf-8')
                projected = overlay.historical_source(ROOT, path, self.source(path))
                self.assertEqual(overlay.normalize(projected), overlay.normalize(baseline))

    def test_crlf_and_lf_round_trip_without_ignoring_trailing_bytes(self):
        for path in ('index.html', 'privacy.html'):
            source = self.source(path)
            for newline in ('\n', '\r\n'):
                candidate = source.replace('\n', newline)
                previous = overlay.historical_source(ROOT, path, candidate)
                self.assertEqual(seo.annotate_html(previous, self.manifest['pages'][path]['canonical']), candidate)
                with self.assertRaises(ValueError):
                    overlay.historical_source(ROOT, path, candidate + ' ')

    def test_missing_duplicated_moved_wrong_canonical_and_body_changes_fail_closed(self):
        path = 'word-frequency-analyzer/index.html'
        source = self.source(path)
        line = '  ' + seo.canonical_tag(self.manifest['pages'][path]['canonical']) + '\n'
        mutations = [source.replace(line, line * 2), source.replace(line, '').replace('</head>', line + '</head>'),
                     source.replace('/word-frequency-analyzer/index.html', '/other/index.html', 1),
                     source.replace('</body>', '<p>Changed behavior or copy</p></body>')]
        for mutation in mutations:
            with self.assertRaises(ValueError):
                overlay.historical_source(ROOT, path, mutation)
        tool = next(tool for tool in json.loads(self.source('TOOL_REGISTRY.json'))['tools']
                    if tool['id'] == 'word-frequency-analyzer')
        self.assertFalse(overlay.valid_candidate(ROOT, tool, source.replace(line, '')))

    def test_manifest_edit_cannot_authorize_another_candidate(self):
        with tempfile.TemporaryDirectory(prefix='edb-seo-manifest-') as temporary:
            root = Path(temporary)
            (root / 'audit').mkdir()
            value = copy.deepcopy(self.manifest)
            value['pages']['index.html']['candidate_sha256'] = '0' * 64
            (root / overlay.MANIFEST).write_text(json.dumps(value), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'immutable candidate'):
                overlay.historical_source(root, 'index.html', self.source('index.html'))
            # The declared normalization is CRLF only, not universal newlines.
            raw = (ROOT / overlay.MANIFEST).read_bytes().replace(b'\r\n', b'\n')
            (root / overlay.MANIFEST).write_bytes(raw.replace(b'\n', b'\r'))
            with self.assertRaisesRegex(ValueError, 'immutable candidate'):
                overlay.manifest(root)

    def test_only_exact_ci_validation_call_is_projected(self):
        path = 'scripts/ci/run.py'
        source = self.source(path)
        entry = self.manifest['infrastructure'][path]
        previous = overlay.historical_source(ROOT, path, source)
        self.assertNotIn(entry['insertion'], previous)
        self.assertEqual(source.replace(entry['insertion'] + entry['anchor'], entry['anchor'], 1), previous)
        for mutation in (source + '# unrelated change\n', source.replace(entry['insertion'], entry['insertion'] * 2)):
            with self.assertRaises(ValueError):
                overlay.historical_source(ROOT, path, mutation)

    def test_87_candidates_bind_to_unchanged_registry_and_older_consent_evidence(self):
        registry_source = self.source('TOOL_REGISTRY.json')
        baseline = subprocess.check_output(['git', 'show', overlay.BASE_REVISION + ':TOOL_REGISTRY.json'], cwd=ROOT).decode('utf-8')
        self.assertEqual(overlay.normalize(registry_source), overlay.normalize(baseline))
        released = [tool for tool in json.loads(registry_source)['tools'] if tool['status'] == 'RELEASED']
        self.assertEqual(len(released), 87)
        for tool in released:
            with self.subTest(tool=tool['id']):
                source = self.source(tool['directory_path'] + '/index.html')
                self.assertTrue(overlay.valid_candidate(ROOT, tool, source))
                self.assertFalse(overlay.valid_candidate(ROOT, tool, source + 'changed'))
                wrong = copy.deepcopy(tool)
                wrong['verification']['source_sha256'] = '0' * 64
                self.assertFalse(overlay.valid_candidate(ROOT, wrong, source))

    def test_unlisted_assets_and_generic_fixtures_are_never_normalized(self):
        binary = b'\x00\xff\r\n  '
        self.assertEqual(overlay.historical_bytes(ROOT, 'assets/example.bin', binary), binary)
        text = 'arbitrary changed runtime source\r\n  '
        self.assertEqual(overlay.historical_source(ROOT, 'assets/consent.js', text), text)
        with tempfile.TemporaryDirectory(prefix='edb-seo-fixture-') as temporary:
            self.assertEqual(overlay.historical_source(Path(temporary), 'index.html', text), text)

    def test_consent_runtime_mutation_is_not_hidden_by_seo_projection(self):
        with tempfile.TemporaryDirectory(prefix='edb-seo-consent-') as temporary:
            root = Path(temporary)
            for path in (overlay.MANIFEST, 'audit/TASK_17_CANDIDATE.json', 'assets/consent.js', 'privacy.html'):
                (root / path).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / path, root / path)
            registry = json.loads(self.source('TOOL_REGISTRY.json'))
            old_tools = json.loads(self.source('audit/TASK_17_CANDIDATE.json'))['tools']
            tool = next(tool for tool in registry['tools'] if tool['id'] in old_tools)
            source = self.source(tool['directory_path'] + '/index.html')
            self.assertTrue(overlay.valid_candidate(root, tool, source))
            with (root / 'assets/consent.js').open('a', encoding='utf-8') as handle:
                handle.write('\n// unauthorized runtime edit')
            self.assertFalse(overlay.valid_candidate(root, tool, source))

    def test_project_check_calls_read_only_seo_without_recursive_registry_checks(self):
        with patch.object(seo, 'validate', wraps=seo.validate) as validate:
            result = tracking.check_project(ROOT)
        self.assertEqual(result['errors'], [])
        self.assertEqual(result['details']['technical_seo']['status'], 'PASS')
        self.assertEqual(result['details']['technical_seo']['counts']['public_pages'], 89)
        self.assertEqual(validate.call_count, 1)
        self.assertIn('registry', validate.call_args.kwargs)


if __name__ == '__main__':
    unittest.main()
