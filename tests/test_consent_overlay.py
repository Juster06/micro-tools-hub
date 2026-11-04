"""Consent-only overlays must preserve prior published source evidence."""
import json
from pathlib import Path
import sys
import tempfile
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

if __name__=='__main__':unittest.main()
