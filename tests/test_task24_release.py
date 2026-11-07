from pathlib import Path
from datetime import datetime
from functools import lru_cache
import json,hashlib,subprocess,sys,unittest
ROOT=Path(__file__).resolve().parents[1];BASE='a7da719ea6ccc4caae572f26f6ae5e707fbb70be'
sys.path.insert(0,str(ROOT/'scripts'))
from css_overlay import historical_snapshot
from git_fixtures import git_blob as frozen_git_blob
historical_source, historical_bytes = historical_snapshot(Path(__file__).resolve().parents[1])
from task24_test_support import IDS
from tool_homepage import Homepage
from task25_test_support import homepage_before_task25, registry_before_task25
@lru_cache(maxsize=None)
def blob(path):return frozen_git_blob(ROOT,BASE,path)
def load(path):
 data=json.loads(historical_source(ROOT, (ROOT/path).relative_to(ROOT).as_posix(), (ROOT/path).read_text(encoding='utf-8')))
 return registry_before_task25(data) if path=='TOOL_REGISTRY.json' else data
def norm(b):return b.replace(b'\r\n',b'\n')
def sha(b):return hashlib.sha256(b).hexdigest()
class Task24Release(unittest.TestCase):
 def test_exactly_six_transitions_and_all_other_metadata_preserved(self):
  old=json.loads(blob('TOOL_REGISTRY.json'));new=load('TOOL_REGISTRY.json');self.assertEqual(len(new['tools']),99);self.assertEqual(old['milestones'],new['milestones']);by={t['id']:t for t in new['tools']};self.assertEqual(set(by),{t['id']for t in old['tools']})
  for tool in old['tools']:
   current=by[tool['id']]
   if tool['id']not in IDS:self.assertEqual(tool,current);continue
   self.assertEqual((tool['status'],current['status']),('TESTED','RELEASED'))
   for key in set(tool)-{'status','testing_status','last_verification_date','notes','verification'}:self.assertEqual(tool[key],current[key],key)
  self.assertEqual({s:sum(t['status']==s for t in new['tools'])for s in ['RELEASED','TESTED','READY','PLANNED','BLOCKED']},{'RELEASED':81,'TESTED':0,'READY':0,'PLANNED':17,'BLOCKED':1})
 def test_all81_runtime_assets_privacy_historical_audits_and_ci_pins_unchanged(self):
  old=json.loads(blob('TOOL_REGISTRY.json'));pages=[t['directory_path']+'/index.html'for t in old['tools']if t['status']in ['TESTED','RELEASED']];self.assertEqual(len(pages),81)
  paths=pages+['CNAME','privacy.html','.github/workflows/functional-ci.yml','scripts/ci/run.py','scripts/ci/package-lock.json']+subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'assets','audit','templates'],cwd=ROOT,text=True).splitlines()
  for path in paths:self.assertEqual(norm(historical_bytes(ROOT, (ROOT/path).relative_to(ROOT).as_posix(), (ROOT/path).read_bytes())),norm(blob(path)),path)
 def test_source_evidence_matches_deployed_git_for99_responses_and_six_aliases(self):
  a=load('audit/TASK_24_PUBLIC_RELEASE_VERIFICATION.json');self.assertEqual(a['result'],'PASS');self.assertEqual(a['source_revision'],BASE);self.assertEqual(a['deployment']['run_id'],42324279460);self.assertEqual(a['post_merge_ci']['run_id'],42324279630);self.assertEqual(a['github']['main'],BASE);self.assertEqual(len(a['sources']),99);self.assertEqual(len(a['canonical_public_urls']),6)
  for path,item in a['sources'].items():self.assertEqual(item['http_status'],200);self.assertTrue(item['raw_match']);self.assertEqual(item['raw_public_sha256'],sha(blob(path)));self.assertEqual(item['raw_approved_sha256'],item['raw_public_sha256']);datetime.fromisoformat(item['checked_at'])
  for tid in IDS:
   t=next(t for t in load('TOOL_REGISTRY.json')['tools']if t['id']==tid);v=t['verification'];individual=load(v['evidence_path']);self.assertEqual(individual['source_revision'],BASE);self.assertEqual(individual['publication'],v['publication']);self.assertEqual(individual['pages'][0]['publication'],v['publication']);self.assertEqual(individual['pages'][0]['source_sha256'],v['source_sha256']);self.assertEqual(individual['public_source_sha256'],sha(blob(tid+'/index.html')));self.assertTrue(individual['canonical_public_url']['raw_match']);self.assertEqual(v['source_sha256'],sha(norm(blob(tid+'/index.html')).rstrip()));self.assertEqual(individual['verified_on'],t['last_verification_date'])
 def test_fresh_public_interactions_catalog_console_and_privacy_are_scoped(self):
  a=load('audit/TASK_24_PUBLIC_RELEASE_VERIFICATION.json');f=a['public_browser'];self.assertEqual(f['result'],'PASS');self.assertEqual(f['deployment_commit'],BASE);self.assertEqual(len(f['checks']),61);self.assertTrue(all(x['result']=='PASS'for x in f['checks']));self.assertEqual({x['tool_id']for x in f['checks']},IDS|{'homepage'})
  for tid in IDS:self.assertGreaterEqual(sum(x['tool_id']==tid for x in f['checks']),6)
  h=a['homepage'];self.assertEqual((h['cards'],h['distinct'],h['visible_cards'],h['canonical_routes_match']),(81,81,81,True));n=a['public_network'];self.assertEqual(n['google_requests'],0);self.assertEqual(n['input_transport_requests'],0);self.assertEqual(n['exceptions'],[]);self.assertEqual(n['unexpected_dependencies'],[]);self.assertTrue(all(x['method']=='GET'for x in n['requests']))
 def test_real_consent_collection_has_three204_views_without_duplicates(self):
  c=load('audit/TASK_24_PUBLIC_RELEASE_VERIFICATION.json')['consent'];self.assertEqual(c['result'],'PASS');self.assertEqual(c['measurement_id'],'G-XDHPQYJ5CH');self.assertEqual(len(c['checks']),6);self.assertTrue(all(x['result']=='PASS'for x in c['checks']));self.assertEqual(c['google_tag_loads'],3);self.assertEqual(c['uncaught_browser_errors'],0);self.assertEqual(len(c['page_views']),3);self.assertEqual(len({x['page_location']for x in c['page_views']}),3)
  for view in c['page_views']:self.assertEqual(view['event'],'page_view');self.assertEqual(view['measurement_id'],'G-XDHPQYJ5CH');self.assertEqual(view['http_response'],204);self.assertNotIn('?',view['page_location']);self.assertNotIn('#',view['page_location'])
  self.assertTrue(any('property-level reporting remains unverified'in x for x in c['limitations']))
 def test_only_six_availability_labels_change_on_homepage(self):
  source=homepage_before_task25(historical_source(ROOT, (ROOT/'index.html').relative_to(ROOT).as_posix(), (ROOT/'index.html').read_text(encoding='utf-8')),Homepage);home=Homepage(source);self.assertEqual(len(home.cards),81)
  for tid in IDS:
   card=next(c for c in Homepage(source).cards if c['attrs'].get('data-tool-id')==tid);chunk=source[card['start']:card['end']];self.assertEqual(card['attrs']['data-availability'],'released');self.assertEqual(chunk.count('Live'),1);chunk=chunk.replace('data-availability="released"','data-availability="tested"').replace('Live','Tested · publication pending');source=source[:card['start']]+chunk+source[card['end']:]
  self.assertEqual(source,norm(blob('index.html')).decode('utf-8'))
