"""Dated live release evidence must agree with registry, Git and public results."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import unittest
from css_overlay import historical_snapshot
from git_fixtures import git_blob as frozen_git_blob
historical_source, historical_bytes = historical_snapshot(Path(__file__).resolve().parents[1])
ROOT=Path(__file__).resolve().parents[1]
BASE='7ecbe37d15d51e3393c1d0f532fa4f2afd279f0b'
IDS={'csv-data-cleaner', 'image-cropper', 'password-generator', 'qr-code-generator', 'passphrase-generator', 'csv-to-txt'}
def load(path):return json.loads(historical_source(ROOT, (ROOT/path).relative_to(ROOT).as_posix(), (ROOT/path).read_text(encoding='utf8')))
def git(path):return frozen_git_blob(ROOT,BASE,path)
class Task19ReleaseEvidence(unittest.TestCase):
    def test_six_releases_have_matching_dated_public_source_and_browser_evidence(self):
        registry=load('TOOL_REGISTRY.json');selected=[t for t in registry['tools'] if t['id'] in IDS]
        self.assertEqual(len(selected),6)
        for tool in selected:
            self.assertEqual(tool['status'],'RELEASED');v=tool['verification'];audit=load(v['evidence_path']);page=audit['pages'][0]
            self.assertEqual((audit['result'],audit['source_revision']),('PASS',BASE))
            self.assertEqual(audit['verified_on'],tool['last_verification_date'])
            self.assertEqual((page['source_sha256'],page['publication']),(v['source_sha256'],v['publication']))
            self.assertEqual(v['publication']['url'],'https://everydaydigitalbox.com/'+tool['directory_path']+'/')
            self.assertEqual((v['publication']['http_status'],v['publication']['source_matches']),(200,True))
            datetime.datetime.fromisoformat(v['publication']['checked_at'])
            raw=git(tool['directory_path']+'/index.html');actual_hash=hashlib.sha256(raw).hexdigest()
            for item in (audit['public_index'],audit['canonical_public_url']):
                self.assertEqual((item['http_status'],item['raw_match']),(200,True))
                self.assertEqual(item['raw_public_sha256'],actual_hash);self.assertEqual(item['raw_approved_sha256'],actual_hash)
            self.assertEqual(hashlib.sha256(raw.decode('utf8').replace('\r\n','\n').rstrip().encode()).hexdigest(),v['source_sha256'])
            self.assertEqual(audit['live_browser']['result'],'PASS');self.assertGreaterEqual(audit['live_browser']['test_count'],6)
            self.assertEqual(historical_source(ROOT, (ROOT/audit['previous_evidence']).relative_to(ROOT).as_posix(), (ROOT/audit['previous_evidence']).read_text(encoding='utf8')).replace('\r\n','\n'),git(audit['previous_evidence']).decode('utf8').replace('\r\n','\n'))
    def test_live_catalog_assets_and_real_collection_evidence_are_complete(self):
        audit=load('audit/TASK_19_PUBLIC_RELEASE_VERIFICATION.json');self.assertEqual(audit['result'],'PASS')
        self.assertEqual((audit['deployment']['commit'],audit['deployment']['run_id'],audit['deployment']['conclusion']),(BASE,42010602815,'success'))
        self.assertEqual((audit['post_merge_ci']['run_id'],audit['post_merge_ci']['required_functional_checks']),(42010604196,'success'))
        self.assertEqual((audit['homepage']['cards'],audit['homepage']['distinct'],audit['homepage']['canonical_routes_match']),(62,62,True))
        self.assertEqual(len(audit['sources']),71)
        for path,item in audit['sources'].items():
            self.assertEqual((item['http_status'],item['raw_match']),(200,True));self.assertEqual(item['raw_public_sha256'],hashlib.sha256(git(path)).hexdigest())
        self.assertEqual((audit['public_browser']['tests'],audit['public_browser']['passed'],audit['public_browser']['failed']),(48,48,0))
        self.assertEqual(audit['public_browser']['uncaught_application_errors'],0)
        self.assertTrue(all(error['url'].endswith('/favicon.ico') for error in audit['public_browser']['console_errors']))
        consent=audit['consent'];self.assertEqual(consent['result'],'PASS');self.assertEqual(len(consent['page_views']),3)
        self.assertTrue(all(c['result']=='PASS' for c in consent['checks']))
        for event in consent['page_views']:
            self.assertEqual((event['measurement_id'],event['event'],event['http_response']),('G-XDHPQYJ5CH','page_view',204))
            self.assertNotIn('?',event['page_location']);self.assertNotIn('#',event['page_location'])
        self.assertIn('GA4 browser collection requests verified; property-level reporting remains unverified.',consent['limitations'])
if __name__=='__main__':unittest.main()
