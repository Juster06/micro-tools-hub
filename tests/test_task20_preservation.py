"""Task20 adds exactly six source-bound releases while retaining the62-release baseline."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
BASE='1ead1c37861b80c552446afbdb952c9248370bf9'
IDS={'excel-formula-generator','emoji-picker','image-compressor','png-to-ico','resume-builder','passport-photo-layout-maker'}
sys.path.insert(0,str(ROOT/'scripts'))
from seo_overlay import historical_source, historical_bytes
from tool_homepage import Homepage
from task24_test_support import historical_registry,without_task24
from task25_test_support import tool_map_before_task25
from task22_test_support import assert_unchanged_or_task22,without_task22
from task21_test_support import IDS as TASK21_IDS, COUNTS as TASK21_COUNTS, assert_transition, without_cards
def blob(path,revision=BASE):return subprocess.check_output(['git','show',revision+':'+path],cwd=ROOT)
def text(path):return historical_source(ROOT, (ROOT/path).relative_to(ROOT).as_posix(), (ROOT/path).read_text(encoding='utf8'))
def load(path):
 data=json.loads(text(path))
 return historical_registry(data) if path=='TOOL_REGISTRY.json' else data
def norm(raw):return raw.replace(b'\r\n',b'\n')
class Task20Preservation(unittest.TestCase):
    def test_inventory_changes_only_the_authorized_six_and_milestones_are_identical(self):
        old=json.loads(blob('TOOL_REGISTRY.json'));new=load('TOOL_REGISTRY.json');by_id={t['id']:t for t in new['tools']}
        self.assertEqual(len(new['tools']),93);self.assertEqual(new['milestones'],old['milestones']);self.assertEqual(set(by_id),{t['id'] for t in old['tools']})
        for tool in old['tools']:
            current=by_id[tool['id']]
            if tool['id'] in IDS:
                self.assertEqual((tool['status'],current['status']),('PLANNED','RELEASED'));self.assertEqual(current['testing_status'],'REQUIRED_PASSED');self.assertTrue(current['verification']['publication']['source_matches'])
                for key in ['id','name','category','description','directory_path','priority','implementation_complexity','required_features','related_tools','sequence_rank']:self.assertEqual(tool[key],current[key])
            elif tool['id'] in TASK21_IDS:assert_transition(self,tool,current)
            else:assert_unchanged_or_task22(self,tool,current)
        self.assertEqual({s:sum(t['status']==s for t in new['tools']) for s in ['RELEASED','TESTED','READY','PLANNED','BLOCKED']},TASK21_COUNTS)
    def test_all62_runtime_pages_and_existing_assets_privacy_ci_templates_are_unchanged(self):
        registry=json.loads(blob('TOOL_REGISTRY.json'))
        paths=[t['directory_path']+'/index.html' for t in registry['tools'] if t['status']=='RELEASED']
        paths+=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'assets'],cwd=ROOT,text=True).splitlines()
        paths+=['CNAME','privacy.html','.github/workflows/functional-ci.yml','scripts/ci/run.py','scripts/ci/package-lock.json','templates/text-input.html','templates/structured-input.html']
        for path in paths:self.assertEqual(norm(historical_bytes(ROOT, (ROOT/path).relative_to(ROOT).as_posix(), (ROOT/path).read_bytes())),norm(blob(path)),path)
    def test_six_pending_cards_and_count_are_the_only_homepage_changes(self):
        current=without_cards(self,text('index.html'),Homepage)
        for tid in IDS:
            home=Homepage(current);card=next(c for c in home.cards if c['attrs'].get('data-tool-id')==tid)
            self.assertEqual(card['attrs']['href'],tid+'/index.html');self.assertEqual(card['attrs']['data-availability'],'released');self.assertIn('Live',current[card['start']:card['end']]);current=current[:card['start']-2]+current[card['end']+7:]
        home=Homepage(current);start,end=home.counts[0];current=current[:start]+'62 tools ready to use'+current[end:];self.assertEqual(current,blob('index.html').decode('utf8').replace('\r\n','\n'))
    def test_all_historical_audits_remain_byte_identical(self):
        names=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'audit'],cwd=ROOT,text=True).splitlines();self.assertGreater(len(names),90)
        for path in names:self.assertEqual(norm(historical_bytes(ROOT, (ROOT/path).relative_to(ROOT).as_posix(), (ROOT/path).read_bytes())),norm(blob(path)),path)
    def test_pinned_emoji_data_license_and_original_git_source_are_preserved(self):
        meta=load('audit/TASK_20_DEPENDENCIES.json')['runtime']['emoji'];self.assertEqual((meta['version'],meta['entries'],meta['license']),('18.0',3963,'Unicode-3.0'))
        tool=next(t for t in load('TOOL_REGISTRY.json')['tools'] if t['id']=='emoji-picker')
        for path,sha in [(meta['path'],meta['sha256']),(meta['original_path'],meta['original_sha256']),(meta['license_path'],meta['license_sha256'])]:
            self.assertEqual(hashlib.sha256(norm(historical_bytes(ROOT, (ROOT/path).relative_to(ROOT).as_posix(), (ROOT/path).read_bytes()))).hexdigest(),sha)
            self.assertEqual(hashlib.sha256(norm(blob(path,tool['verification']['source_revision']))).hexdigest(),sha)
        self.assertLessEqual(meta['bytes'],1048576);self.assertIn('UNICODE LICENSE V3',text(meta['license_path']))
        tool=next(t for t in load('TOOL_REGISTRY.json')['tools'] if t['id']=='emoji-picker');self.assertEqual(hashlib.sha256(blob(meta['original_path'],tool['verification']['source_revision'])).hexdigest(),meta['original_sha256'])
    def test_each_tested_tool_has_real_source_bound_evidence_and_all_canonical_layers(self):
        for tool in load('TOOL_REGISTRY.json')['tools']:
            if tool['id'] not in IDS:continue
            v=tool['verification'];audit=load(v['evidence_path']);page=audit['pages'][0]
            self.assertEqual((audit['result'],audit['source_revision']),('PASS',v['source_revision']));self.assertEqual(page['source_sha256'],v['source_sha256']);self.assertTrue(v['publication']['source_matches'])
            committed=blob(page['path'],v['source_revision']).decode('utf8').replace('\r\n','\n').rstrip().encode();self.assertEqual(hashlib.sha256(committed).hexdigest(),v['source_sha256']);self.assertEqual(hashlib.sha256(text(page['path']).rstrip().encode()).hexdigest(),v['source_sha256'])
            for layer in ['structural','logic','browser']:
                self.assertEqual(audit['canonical_layers'][layer]['status'],'PASS')
                if layer!='structural':self.assertGreater(audit['canonical_layers'][layer]['passed'],0)
            self.assertGreater(audit['focused_test_count'],0)
    def test_all68_tools_and_new_tests_remain_mandatory_in_ci(self):
        c=load('scripts/ci/coverage.json');self.assertEqual(len(tool_map_before_task25(c)),81)
        for tid in IDS:
            self.assertEqual(c['tools'][tid],{'structural_job':'python-project','logic_job':'node-regression','browser_job':'browser-tests'});self.assertIn('tests/tools/'+tid+'/logic.test.mjs',c['node_files'])
            for name in ['extended-browser.test.mjs','integration-browser.test.mjs']:self.assertIn('tests/tools/'+tid+'/'+name,c['browser_files'])
        self.assertIn('tests/test_task20_formats.py',c['python_files']);self.assertIn('tests/test_task20_preservation.py',c['python_files'])
        for name,floor in [('python-project',172),('node-regression',433),('browser-tests',593)]:self.assertGreaterEqual(c['minimum_tests'][name],floor)
    def test_new_tools_use_exact_shared_consent_without_direct_google_or_hidden_storage(self):
        for tid in IDS:
            source=text(tid+'/index.html');self.assertEqual(source.count('<script defer src="../assets/consent.js"></script>'),1)
            for value in ['googletagmanager.com/gtag/js','localStorage','sessionStorage','innerHTML','Math.random']:self.assertNotIn(value,source)
            self.assertNotRegex(source,r'\beval\s*\(|new\s+Function')

if __name__=='__main__':unittest.main()
