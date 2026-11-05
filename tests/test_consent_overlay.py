"""Consent-only overlays must preserve prior published source evidence."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import subprocess
import unittest
SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0,str(SCRIPTS))
import consent_overlay as overlay

class ConsentOverlayTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='edb-consent-overlay-');self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        (self.root/'audit').mkdir();(self.root/'assets').mkdir();
        (self.root/'assets/consent.js').write_text('loader',encoding='utf8');(self.root/'privacy.html').write_text('notice',encoding='utf8')
        self.old='<html><head></head><body>No input uploads, tracking, saved drafts or external processing. Existing homepage Analytics is separate.</body></html>'
        self.candidate=overlay.apply_overlay(self.old);self.tool={'id':'sample','verification':{'source_sha256':overlay.digest(self.old)}}
        self.manifest={'result':'PASS','state':'PENDING_DEPLOYMENT','base_revision':'8441c3202a5f23c5e2afd8cb8b89901fc21ffad3','assets':{'assets/consent.js':overlay.digest('loader'),'privacy.html':overlay.digest('notice')},'tools':{'sample':{'previous_sha256':overlay.digest(self.old),'candidate_sha256':overlay.digest(self.candidate)}}}
        self.save()
    def save(self):
        (self.root/'audit/TASK_17_CANDIDATE.json').write_text(json.dumps(self.manifest),encoding='utf8')
    def test_exact_overlay_is_reversible_and_bound(self):
        self.assertEqual(overlay.remove_overlay(self.candidate),self.old);self.assertTrue(overlay.valid_candidate(self.root,self.tool,self.candidate))
    def test_unrelated_edits_and_wrong_evidence_are_rejected(self):
        self.assertFalse(overlay.valid_candidate(self.root,self.tool,self.candidate.replace('</body>','changed</body>')))
        self.tool['verification']['source_sha256']='0'*64;self.assertFalse(overlay.valid_candidate(self.root,self.tool,self.candidate))
    def test_tampered_assets_or_unpassed_manifest_are_rejected(self):
        (self.root/'assets/consent.js').write_text('tampered',encoding='utf8');self.assertFalse(overlay.valid_candidate(self.root,self.tool,self.candidate))
        (self.root/'assets/consent.js').write_text('loader',encoding='utf8');self.manifest['result']='PENDING';self.save();self.assertFalse(overlay.valid_candidate(self.root,self.tool,self.candidate))
    def test_duplicate_missing_or_repositioned_loader_rejected(self):
        for text in [self.candidate.replace(overlay.LOADER,''), self.candidate.replace(overlay.LOADER,overlay.LOADER*2),self.candidate.replace(overlay.LOADER,'').replace('</body>',overlay.LOADER+'</body>')]:
            with self.assertRaises(ValueError):overlay.remove_overlay(text)

class DeploymentEvidenceTests(unittest.TestCase):
    def test_deployed_pages_match_source_and_historical_candidate(self):
        root = SCRIPTS.parent
        audit = json.loads((root/'audit/TASK_17_DEPLOYMENT.json').read_text(encoding='utf8'))
        candidate = json.loads((root/'audit/TASK_17_CANDIDATE.json').read_text(encoding='utf8'))
        registry = json.loads((root/'TOOL_REGISTRY.json').read_text(encoding='utf8'))
        released = [tool for tool in registry['tools'] if tool['status'] == 'RELEASED' and tool['id'] in candidate['tools']]
        self.assertEqual({tool['id'] for tool in released}, set(candidate['tools']))
        paths = {'index.html', 'privacy.html', 'assets/consent.js'} | {tool['directory_path']+'/index.html' for tool in released}
        self.assertEqual(len(released), 50)
        self.assertEqual(set(audit['sources']), paths)
        for path in paths:
            entry = audit['sources'][path]
            self.assertEqual(entry['http_status'], 200, path)
            # This is dated deployment evidence, not a lock against later hub cards.
            # Current Task 18 homepage additions are independently checked below.
            source = (subprocess.check_output(['git', 'show', audit['deployment_commit']+':index.html'], cwd=root, text=True, encoding='utf8')
                      if path == 'index.html' else (root/path).read_text(encoding='utf8'))
            self.assertEqual(entry['sha256_bytes'], hashlib.sha256(source.encode('utf8')).hexdigest(), path)
            self.assertEqual(entry['sha256_normalized'], overlay.digest(source), path)
        for tool in released:
            path = tool['directory_path']+'/index.html'
            self.assertEqual(audit['sources'][path]['sha256_normalized'], candidate['tools'][tool['id']]['candidate_sha256'])
        self.assertEqual(audit['sources']['index.html']['sha256_normalized'], candidate['homepage']['candidate_sha256'])
        for path in ('assets/consent.js', 'privacy.html'):
            self.assertEqual(audit['sources'][path]['sha256_normalized'], candidate['assets'][path])

    def test_recorded_collection_evidence_has_expected_scope(self):
        audit = json.loads((SCRIPTS.parent/'audit/TASK_17_DEPLOYMENT.json').read_text(encoding='utf8'))
        self.assertEqual((audit['result'], audit['pr'], audit['deployment_commit']), ('PASS', 30, 'c1c050c8594795dcab25d0e2362c0bfb472a5165'))
        self.assertEqual((audit['pages_run'], audit['post_merge_ci_run']), (41811430121, 41811430196))
        self.assertEqual(len(audit['ga4_page_views']), 3)
        for event in audit['ga4_page_views']:
            self.assertEqual((event['event'], event['measurement_id'], event['request_count'], event['http_response']), ('page_view', 'G-XDHPQYJ5CH', 1, 204))
            self.assertTrue(event['timestamp_utc'].endswith('Z'))
        self.assertIn('GA4 browser collection requests verified; property-level reporting remains unverified.', audit['limitations'])

if __name__=='__main__':unittest.main()
