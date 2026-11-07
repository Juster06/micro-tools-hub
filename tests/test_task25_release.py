from datetime import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from task25_test_support import DEPLOYMENT, IDS, git_blob, normalized, registry_before_task25
from tool_homepage import Homepage


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def digest(data):
    return hashlib.sha256(data).hexdigest()


def approved(path):
    return git_blob(path, DEPLOYMENT)


class Task25PublicRelease(unittest.TestCase):
    def test_only_six_tested_records_transition_and_other_metadata_is_preserved(self):
        prior = json.loads(approved('TOOL_REGISTRY.json'))
        new = read('TOOL_REGISTRY.json')
        registry_before_task25(new)
        self.assertEqual({k:v for k,v in new.items() if k not in ('tools','updated_on')},
                         {k:v for k,v in prior.items() if k not in ('tools','updated_on')})
        self.assertEqual(len(new['tools']), 105)
        mutable = {'status','last_verification_date','verification','notes','testing_status'}
        for before, after in zip(prior['tools'], new['tools'], strict=True):
            if before['id'] not in IDS:
                self.assertEqual(before, after)
            else:
                self.assertEqual((before['status'], after['status']), ('TESTED','RELEASED'))
                self.assertEqual({k:v for k,v in before.items() if k not in mutable},
                                 {k:v for k,v in after.items() if k not in mutable})
        self.assertEqual({s:sum(t['status']==s for t in new['tools']) for s in ('RELEASED','TESTED','READY','PLANNED','BLOCKED')},
                         {'RELEASED':87,'TESTED':0,'READY':0,'PLANNED':17,'BLOCKED':1})

    def test_all_87_runtime_pages_existing_assets_audits_and_ci_pins_are_unchanged(self):
        prior = json.loads(approved('TOOL_REGISTRY.json'))
        pages = [t['directory_path'] + '/index.html' for t in prior['tools'] if t['status'] in ('TESTED','RELEASED')]
        self.assertEqual(len(pages), 87)
        paths = subprocess.check_output(['git','ls-tree','-r','--name-only',DEPLOYMENT,'assets','audit','templates','.github/workflows'],cwd=ROOT,text=True).splitlines()
        for path in [*pages,*paths,'CNAME','privacy.html','scripts/ci/run.py','scripts/ci/package-lock.json']:
            self.assertEqual(normalized((ROOT / path).read_bytes()), normalized(approved(path)), path)

    def test_public_source_evidence_binds_105_responses_and_seven_aliases_to_git(self):
        audit = read('audit/TASK_25_PUBLIC_RELEASE_VERIFICATION.json')
        self.assertEqual(audit['source_revision'], DEPLOYMENT)
        self.assertEqual(audit['deployment']['run_id'], 42338516265)
        self.assertEqual(audit['post_merge_ci']['run_id'], 42338516503)
        self.assertEqual(len(audit['post_merge_ci']['jobs']), 4)
        self.assertTrue(all(job['conclusion']=='success' for job in audit['post_merge_ci']['jobs']))
        self.assertEqual(len(audit['sources']), 105)
        self.assertEqual(set(audit['canonical_public_urls']), IDS)
        rows = [*audit['sources'].items(), *((tid + '/index.html', item) for tid,item in audit['canonical_public_urls'].items()), ('index.html', audit['homepage']['root'])]
        for path, item in rows:
            self.assertEqual(item['http_status'], 200)
            self.assertTrue(item['raw_match'])
            self.assertEqual(item['raw_public_sha256'], digest(approved(path)), path)
            self.assertEqual(item['raw_public_sha256'], item['raw_approved_sha256'])
            datetime.fromisoformat(item['checked_at'])
        for path, sha in audit['reproduction_sources'].items():
            self.assertEqual(digest(normalized((ROOT / path).read_bytes())), sha)

    def test_fresh_browser_results_include_native_worker_and_safe_csv_evidence(self):
        audit = read('audit/TASK_25_PUBLIC_RELEASE_VERIFICATION.json')
        functional = audit['public_browser'];rows = functional['checks']
        self.assertEqual(functional['deployment_commit'], DEPLOYMENT)
        self.assertEqual(len(rows), 43)
        self.assertEqual({row['tool_id'] for row in rows}, IDS | {'homepage'})
        self.assertTrue(all(row['result']=='PASS' for row in rows))
        self.assertEqual(audit['homepage']['visible_cards'], 87)
        worker = next(row['observed'] for row in rows if 'bounded pairs' in row['check'])
        self.assertEqual(worker['slices'], [[0,262144],[0,262144],[262144,524288],[262144,524288]])
        self.assertEqual(worker['read_sizes'], [262144]*4)
        self.assertEqual(worker['peak_reads_in_flight'], 2)
        csv = next(row['observed'] for row in rows if 'byte-exact formula-protected CSV' in row['check'])
        self.assertEqual((csv['file_content_reads'],csv['filesystem_picker_calls']), (0,0))
        self.assertEqual(csv['csv_type'], 'text/csv;charset=utf-8')
        network = audit['public_network']
        self.assertEqual(network['exceptions'], [])
        self.assertEqual(network['unexpected_dependencies'], [])
        self.assertEqual((network['google_requests'],network['input_transport_requests']), (0,0))
        self.assertTrue(all(row['method']=='GET' for row in network['requests']))

    def test_real_analytics_collection_has_unique_accepted_views_and_denial_checks(self):
        c = read('audit/TASK_25_PUBLIC_RELEASE_VERIFICATION.json')['consent']
        self.assertEqual(c['result'], 'PASS')
        self.assertEqual(c['deployment_commit'], DEPLOYMENT)
        self.assertEqual(c['measurement_id'], 'G-XDHPQYJ5CH')
        self.assertEqual(len(c['checks']), 6)
        self.assertTrue(all(row['result']=='PASS' for row in c['checks']))
        self.assertEqual(c['google_tag_loads'], 3)
        self.assertEqual(c['uncaught_browser_errors'], 0)
        views = c['page_views']
        self.assertEqual(len(views), 3)
        self.assertEqual({row['page_location'] for row in views}, {
            'https://everydaydigitalbox.com/','https://everydaydigitalbox.com/word-frequency-analyzer/index.html',
            'https://everydaydigitalbox.com/css-gradient-generator/index.html',
        })
        for row in views:
            self.assertEqual((row['event'],row['http_response'],row['measurement_id']), ('page_view',204,'G-XDHPQYJ5CH'))
        self.assertTrue(any('property-level reporting remains unverified' in text for text in c['limitations']))

    def test_only_six_homepage_labels_change_and_generated_milestone_is_preserved(self):
        source = (ROOT / 'index.html').read_text(encoding='utf-8')
        home = Homepage(source)
        self.assertEqual(len(home.cards), 87)
        cards = [card for card in home.cards if card['attrs'].get('data-tool-id') in IDS]
        self.assertEqual(len(cards), 6)
        for card in sorted(cards,key=lambda row:row['start'],reverse=True):
            start,end = card['start'],card['end'];chunk = source[start:end]
            self.assertEqual(card['attrs']['data-availability'], 'released')
            self.assertEqual(chunk.count('Live'), 1)
            source = source[:start] + chunk.replace('data-availability="released"','data-availability="tested"').replace('Live','Tested · publication pending') + source[end:]
        self.assertEqual(source, normalized(approved('index.html')).decode())
        tracker = (ROOT / 'PROGRESS_TRACKER.md').read_text(encoding='utf-8').split('<!-- GENERATED:COUNTS:START -->',1)[1].split('<!-- GENERATED:COUNTS:END -->',1)[0]
        self.assertIn('| RELEASED | 87 |', tracker)
        self.assertIn('87/100 (87.0%); remaining: 13.', tracker)
