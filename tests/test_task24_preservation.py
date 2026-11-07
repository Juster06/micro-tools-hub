import hashlib,json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE='4671204d2fb39129b0463e4b4ba8b5c8dc21e0a7'
sys.path.insert(0,str(ROOT/'scripts'))
from seo_overlay import historical_source, historical_bytes
from task24_test_support import IDS,historical_registry,without_task24
from tool_homepage import Homepage
from task25_test_support import homepage_before_task25, registry_before_task25, tool_map_before_task25
def blob(path,ref=BASE):return subprocess.check_output(['git','show',ref+':'+path],cwd=ROOT)
def normalized(b):return b.replace(b'\r\n',b'\n')
class Task24Preservation(unittest.TestCase):
 def test_exactly_six_new_records_and_original93_records_unchanged(self):
  old=json.loads(blob('TOOL_REGISTRY.json'));new=registry_before_task25(json.loads(historical_source(ROOT, (ROOT/'TOOL_REGISTRY.json').relative_to(ROOT).as_posix(), (ROOT/'TOOL_REGISTRY.json').read_text(encoding='utf-8'))));self.assertEqual(historical_registry(new)['tools'],old['tools']);self.assertEqual(new['milestones'],old['milestones']);self.assertEqual({s:sum(t['status']==s for t in new['tools'])for s in ['RELEASED','TESTED','READY','PLANNED','BLOCKED']},{'RELEASED':81,'TESTED':0,'READY':0,'PLANNED':17,'BLOCKED':1})
 def test_all75_pages_assets_privacy_historical_audits_and_workflow_unchanged(self):
  old=json.loads(blob('TOOL_REGISTRY.json'));pages=[t['directory_path']+'/index.html'for t in old['tools']if t['status']=='RELEASED'];self.assertEqual(len(pages),75)
  paths=pages+['CNAME','privacy.html','.github/workflows/functional-ci.yml','scripts/ci/run.py','scripts/ci/package-lock.json']+subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'assets','audit','templates'],cwd=ROOT,text=True).splitlines()
  for path in paths:self.assertEqual(normalized(historical_bytes(ROOT, (ROOT/path).relative_to(ROOT).as_posix(), (ROOT/path).read_bytes())),normalized(blob(path)),path)
 def test_six_verified_release_cards_are_only_homepage_changes(self):
  source=homepage_before_task25(historical_source(ROOT, (ROOT/'index.html').relative_to(ROOT).as_posix(), (ROOT/'index.html').read_text(encoding='utf-8')),Homepage);self.assertEqual(without_task24(source,Homepage),normalized(blob('index.html')).decode());cards=Homepage(source).cards;self.assertEqual(len(cards),81);self.assertEqual(len({c['attrs']['href']for c in cards}),81)
 def test_publication_evidence_binds_git_source_and_preserves_development(self):
  r=json.loads(historical_source(ROOT, (ROOT/'TOOL_REGISTRY.json').relative_to(ROOT).as_posix(), (ROOT/'TOOL_REGISTRY.json').read_text(encoding='utf-8')))
  for tool in r['tools']:
   if tool['id']not in IDS:continue
   v=tool['verification'];sha=hashlib.sha256(normalized(blob(tool['id']+'/index.html',v['source_revision'])).rstrip()).hexdigest();self.assertEqual(sha,v['source_sha256']);self.assertEqual(v['publication']['http_status'],200);self.assertIs(v['publication']['source_matches'],True);self.assertEqual(tool['status'],'RELEASED');audit=json.loads(historical_source(ROOT, (ROOT/v['evidence_path']).relative_to(ROOT).as_posix(), (ROOT/v['evidence_path']).read_text(encoding='utf-8')));previous=json.loads(historical_source(ROOT, (ROOT/audit['previous_evidence']).relative_to(ROOT).as_posix(), (ROOT/audit['previous_evidence']).read_text(encoding='utf-8')));self.assertIsNone(previous['pages'][0]['publication']);self.assertEqual(previous['result'],'PASS')
 def test_new_code_has_shared_consent_no_input_transport_or_html_evaluation(self):
  for tid in IDS:
   source=historical_source(ROOT, (ROOT/tid/'index.html').relative_to(ROOT).as_posix(), (ROOT/tid/'index.html').read_text(encoding='utf-8'));self.assertEqual(source.count('<script defer src="../assets/consent.js"></script>'),1)
   for forbidden in ['innerHTML','eval(','new Function','localStorage','sessionStorage','fetch(','XMLHttpRequest','sendBeacon','gtag(']:self.assertNotIn(forbidden,source)
 def test_new_ci_scopes_are_explicit_and_older_coverage_preserved(self):
  old=json.loads(blob('scripts/ci/coverage.json'));new=json.loads(historical_source(ROOT, (ROOT/'scripts/ci/coverage.json').relative_to(ROOT).as_posix(), (ROOT/'scripts/ci/coverage.json').read_text(encoding='utf-8')))
  for key in ['python_files','node_files','browser_files']:self.assertTrue(set(old[key])<=set(new[key]))
  for tid in old['tools']:self.assertEqual(old['tools'][tid],new['tools'][tid])
  self.assertEqual(len(tool_map_before_task25(new)),81)
  for tid in IDS:self.assertEqual(new['tools'][tid],{'structural_job':'python-project','logic_job':'node-regression','browser_job':'browser-tests'})
  for job in old['minimum_tests']:self.assertGreaterEqual(new['minimum_tests'][job],old['minimum_tests'][job])
