"""Preserve historical evidence and constrain Task 18 to new gated hub cards."""
import json
from pathlib import Path
import subprocess
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from tool_homepage import Homepage
from task22_test_support import assert_unchanged_or_task22,without_task22
from task21_test_support import IDS as TASK21_IDS, COUNTS as TASK21_COUNTS, assert_transition, without_cards
IDS={'youtube-title-checker','instagram-bio-formatter','file-signature-inspector','image-format-converter','csv-json-converter','regex-tester'}
TASK19_IDS={'password-generator','csv-to-txt','passphrase-generator','qr-code-generator','image-cropper','csv-data-cleaner'}
TASK20_IDS={'excel-formula-generator', 'resume-builder', 'emoji-picker', 'passport-photo-layout-maker', 'image-compressor', 'png-to-ico'}
BASE='f35f07ee5da8c5c4efdf7d3f1ffeabe75571a16a'
def blob(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT,text=True,encoding='utf8')
class Task18Preservation(unittest.TestCase):
    def test_only_gated_cards_and_count_change_in_homepage(self):
        current=(ROOT/'index.html').read_text(encoding='utf8')
        current=without_cards(self,current,Homepage)
        # Remove only the separately authorized Task 19 cards before reconstructing Task 18.
        for tid in TASK19_IDS|TASK20_IDS:
            home=Homepage(current)
            cards=[c for c in home.cards if c['attrs'].get('data-tool-id')==tid]
            if cards:
                card=cards[0];self.assertEqual(card['attrs']['href'],tid+'/index.html')
                tool=next(t for t in json.loads((ROOT/'TOOL_REGISTRY.json').read_text(encoding='utf8'))['tools'] if t['id']==tid)
                self.assertEqual(card['attrs']['data-availability'],tool['status'].lower())
                self.assertIn('Live' if tool['status']=='RELEASED' else 'Tested · publication pending',current[card['start']:card['end']])
                current=current[:card['start']-2]+current[card['end']+7:]
        registry=json.loads((ROOT/'TOOL_REGISTRY.json').read_text(encoding='utf8'))
        added=[t for t in registry['tools'] if t['id'] in IDS and t['status'] in ('TESTED','RELEASED')]
        for tool in reversed(added):
            # Registry order differs from insertion order; locate the exact current range.
            home=Homepage(current)
            card=next(c for c in home.cards if c['attrs'].get('data-tool-id')==tool['id'])
            self.assertEqual(card['attrs']['href'],tool['directory_path']+'/index.html')
            self.assertEqual(card['attrs']['data-availability'],tool['status'].lower())
            self.assertIn('Live' if tool['status']=='RELEASED' else 'Tested · publication pending',current[card['start']:card['end']])
            self.assertEqual(current[card['start']-2:card['start']],'  ')
            self.assertEqual(current[card['end']:card['end']+7],'\n      ')
            current=current[:card['start']-2]+current[card['end']+7:]
        home=Homepage(current);begin,end=home.counts[0]
        current=current[:begin]+'50 tools ready to use'+current[end:]
        self.assertEqual(current,blob('index.html'))
    def test_all_prior_registry_records_and_runtime_files_unchanged(self):
        old=json.loads(blob('TOOL_REGISTRY.json'));new=json.loads((ROOT/'TOOL_REGISTRY.json').read_text(encoding='utf8'))
        by_id={t['id']:t for t in new['tools']}
        self.assertEqual(len(new['tools']),93);self.assertEqual(old['milestones'],new['milestones'])
        for tool in old['tools']:
            if tool['id'] in TASK21_IDS:assert_transition(self,tool,by_id[tool['id']])
            elif tool['id'] not in IDS|TASK19_IDS|TASK20_IDS:assert_unchanged_or_task22(self,tool,by_id[tool['id']])
            if tool['status']=='RELEASED':
                path=tool['directory_path']+'/index.html';self.assertEqual((ROOT/path).read_text(encoding='utf8'),blob(path))
        for path in ['CNAME','assets/consent.js','privacy.html','audit/TASK_17_CANDIDATE.json','audit/TASK_17_DEPLOYMENT.json']:
            self.assertEqual((ROOT/path).read_text(encoding='utf8'),blob(path))
    def test_new_pages_have_exact_shared_loader_and_no_direct_google_tag(self):
        for tid in IDS:
            page=ROOT/tid/'index.html'
            if not page.exists():continue
            source=page.read_text(encoding='utf8')
            self.assertEqual(source.count('<script defer src="../assets/consent.js"></script>'),1)
            self.assertNotIn('googletagmanager.com/gtag/js',source)
            self.assertNotIn('gtag(',source)
if __name__=='__main__':unittest.main()
