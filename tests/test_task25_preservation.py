import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from seo_overlay import historical_source, historical_bytes
from task25_test_support import BASE, IDS, git_blob, homepage_before_task25, normalized, registry_before_task25, tool_map_before_task25
from tool_homepage import Homepage


def read(path):
    return json.loads(historical_source(ROOT, (ROOT / path).relative_to(ROOT).as_posix(), (ROOT / path).read_text(encoding='utf-8')))


class Task25Preservation(unittest.TestCase):
    def test_unchanged_prior_records_and_exact_six_publicly_verified_additions(self):
        prior = json.loads(git_blob('TOOL_REGISTRY.json'))
        current = read('TOOL_REGISTRY.json')
        reconstructed = registry_before_task25(current)
        self.assertEqual({**reconstructed, 'updated_on': prior['updated_on']}, prior)
        self.assertEqual({s: sum(t['status'] == s for t in current['tools']) for s in ('RELEASED','TESTED','READY','PLANNED','BLOCKED')},
                         {'RELEASED':87,'TESTED':0,'READY':0,'PLANNED':17,'BLOCKED':1})

    def test_existing_runtime_privacy_and_ci_infrastructure_preserved(self):
        prior = json.loads(git_blob('TOOL_REGISTRY.json'))
        pages = [t['directory_path'] + '/index.html' for t in prior['tools'] if t['status'] == 'RELEASED']
        self.assertEqual(len(pages), 81)
        protected = subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'assets','templates','audit','.github/workflows'], cwd=ROOT, text=True).splitlines()
        for path in [*pages, *protected, 'CNAME','privacy.html','scripts/ci/run.py','scripts/ci/package-lock.json']:
            self.assertEqual(normalized(historical_bytes(ROOT, (ROOT / path).relative_to(ROOT).as_posix(), (ROOT / path).read_bytes())), normalized(git_blob(path)), path)

    def test_only_six_catalog_cards_and_count_added(self):
        source = historical_source(ROOT, (ROOT / 'index.html').relative_to(ROOT).as_posix(), (ROOT / 'index.html').read_text(encoding='utf-8'))
        self.assertEqual(homepage_before_task25(source, Homepage), normalized(git_blob('index.html')).decode())
        routes = {card['attrs']['href'] for card in Homepage(source).cards}
        self.assertEqual(len(routes), 87)

    def test_shared_consent_and_no_input_transport_or_markup_execution(self):
        for tid in IDS:
            source = historical_source(ROOT, (ROOT / tid / 'index.html').relative_to(ROOT).as_posix(), (ROOT / tid / 'index.html').read_text(encoding='utf-8'))
            self.assertEqual(source.count('<script defer src="../assets/consent.js"></script>'), 1)
            for forbidden in ('innerHTML', 'eval(', 'new Function', 'localStorage', 'sessionStorage', 'fetch(', 'XMLHttpRequest', 'sendBeacon', 'gtag('):
                self.assertNotIn(forbidden, source, tid)

    def test_coverage_extends_all_old_maps_and_test_floors(self):
        old = json.loads(git_blob('scripts/ci/coverage.json'))
        new = read('scripts/ci/coverage.json')
        self.assertEqual(tool_map_before_task25(new), old['tools'])
        for key in ('python_files','node_files','browser_files'):
            self.assertTrue(set(old[key]).issubset(new[key]))
        self.assertEqual(new['minimum_tests'], {'python-project':225,'node-regression':530,'browser-tests':742})
        for job, floor in old['minimum_tests'].items():
            self.assertGreater(new['minimum_tests'][job], floor)

    def test_final_scope_binds_authorized_baseline_and_six_unique_routes(self):
        plan = read('audit/TASK_25_DEVELOPMENT_PLAN.json')
        self.assertEqual(plan['approved_baseline'], BASE)
        self.assertEqual({tool['id'] for tool in plan['tools']}, IDS)
        self.assertEqual({tool['canonical_route'] for tool in plan['tools']}, {tid + '/index.html' for tid in IDS})
        for tool in plan['tools']:
            self.assertTrue(tool['final_scope_limits'])
            self.assertTrue(tool['required_features'])
