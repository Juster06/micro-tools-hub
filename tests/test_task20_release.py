"""Source-bound fresh public evidence for exactly the six Task20 release proposals."""
import datetime,hashlib,json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE='0b055d5b837ea0bca85f8b6583eec5607f93de95'
IDS={'excel-formula-generator','emoji-picker','image-compressor','png-to-ico','resume-builder','passport-photo-layout-maker'}
COUNTS=dict(zip(['excel-formula-generator','emoji-picker','image-compressor','png-to-ico','resume-builder','passport-photo-layout-maker'],[5,6,9,8,7,9]))
sys.path.insert(0,str(ROOT/'scripts'));from tool_homepage import Homepage
from task22_test_support import assert_unchanged_or_task22,without_task22
from task21_test_support import IDS as TASK21_IDS, COUNTS as TASK21_COUNTS, assert_transition, without_cards
def load(p):return json.loads((ROOT/p).read_text(encoding='utf8'))
def git(p):return subprocess.check_output(['git','show',BASE+':'+p],cwd=ROOT)
def norm(b):return b.replace(b'\r\n',b'\n')
class Task20Release(unittest.TestCase):
 def test_six_releases_have_real_dated_matching_public_git_and_interaction_evidence(self):
  tools=[t for t in load('TOOL_REGISTRY.json')['tools'] if t['id'] in IDS];self.assertEqual(len(tools),6)
  for t in tools:
   v=t['verification'];a=load(v['evidence_path']);p=a['pages'][0];raw=git(t['directory_path']+'/index.html');sha=hashlib.sha256(raw).hexdigest()
   self.assertEqual((t['status'],t['testing_status'],a['result'],a['source_revision']),('RELEASED','REQUIRED_PASSED','PASS',BASE));self.assertEqual(a['verified_on'],t['last_verification_date'])
   self.assertEqual(p['publication'],v['publication']);self.assertEqual(p['source_sha256'],v['source_sha256']);self.assertEqual(hashlib.sha256(raw.decode('utf8').replace('\r\n','\n').rstrip().encode()).hexdigest(),v['source_sha256'])
   self.assertEqual(v['publication']['url'],'https://everydaydigitalbox.com/'+t['directory_path']+'/');self.assertEqual((v['publication']['http_status'],v['publication']['source_matches']),(200,True));datetime.datetime.fromisoformat(v['publication']['checked_at'])
   for item in [a['public_index'],a['canonical_public_url']]:
    self.assertEqual((item['http_status'],item['raw_match']),(200,True));self.assertEqual(item['raw_public_sha256'],sha);self.assertEqual(item['raw_approved_sha256'],sha)
   self.assertEqual((a['live_browser']['result'],a['live_browser']['test_count']),('PASS',COUNTS[t['id']]))
   for layer in ['structural','logic','browser']:
    self.assertEqual(a['canonical_layers'][layer]['status'],'PASS')
    if layer!='structural':self.assertGreater(a['canonical_layers'][layer]['passed'],0)
   self.assertEqual(norm((ROOT/a['previous_evidence']).read_bytes()),norm(git(a['previous_evidence'])))
 def test_fresh_public_catalog_assets_real_consent_and_print_scope_are_complete(self):
  a=load('audit/TASK_20_PUBLIC_RELEASE_VERIFICATION.json');self.assertEqual(a['result'],'PASS');self.assertEqual((a['deployment']['commit'],a['deployment']['run_id'],a['post_merge_ci']['run_id']),(BASE,42131624570,42131632444))
  self.assertTrue(a['github']['pr']['merged']);self.assertEqual(a['github']['main']['sha'],BASE);self.assertEqual(len(a['github']['post_merge_ci']['jobs']),4);self.assertTrue(all(j['conclusion']=='success' for j in a['github']['post_merge_ci']['jobs']))
  self.assertEqual((a['homepage']['cards'],a['homepage']['distinct'],a['homepage']['canonical_routes_match']),(68,68,True));self.assertEqual(len(a['sources']),78)
  for path,s in a['sources'].items():
   self.assertEqual((s['http_status'],s['raw_match']),(200,True));self.assertEqual(s['raw_public_sha256'],hashlib.sha256(git(path)).hexdigest());self.assertEqual(s['raw_approved_sha256'],s['raw_public_sha256'])
  b=a['public_browser'];self.assertEqual((b['tests'],b['passed'],b['failed'],b['skipped']),(45,45,0,0));self.assertEqual(b['uncaught_application_errors'],0);self.assertEqual(b['functional_google_requests'],0);self.assertEqual(b['unexpected_dependencies'],[]);self.assertTrue(all(e['url'].endswith('/favicon.ico') for e in b['console_errors']))
  c=a['consent'];self.assertEqual(c['result'],'PASS');self.assertTrue(all(x['result']=='PASS' for x in c['checks']));self.assertEqual(len(c['page_views']),3);self.assertEqual(c['google_tag_loads'],3)
  for e in c['page_views']:
   self.assertEqual((e['measurement_id'],e['event'],e['http_response']),('G-XDHPQYJ5CH','page_view',204));self.assertNotIn('?',e['page_location']);self.assertNotIn('#',e['page_location'])
  self.assertEqual(len({e['page_location'] for e in c['page_views']}),3);self.assertIn('GA4 browser collection requests verified; property-level reporting remains unverified.',c['limitations'])
  obs=a['print_layout_observation'];self.assertFalse(obs['spaced_mm_supported']);self.assertTrue(obs['contiguous_mm_supported']);self.assertEqual(obs['page_rules'][0]['size'],'a4');self.assertIn('browser print defaults',obs['assessment'])
 def test_release_changes_preserve_all_prior_records_runtime_audits_and_exact_hub_markup(self):
  old=json.loads(git('TOOL_REGISTRY.json'));new=load('TOOL_REGISTRY.json');by_id={t['id']:t for t in new['tools']};self.assertEqual(new['milestones'],old['milestones']);self.assertEqual(len(new['tools']),93)
  for t in old['tools']:
   if t['id'] in IDS:
    self.assertEqual(t['status'],'TESTED');self.assertEqual(by_id[t['id']]['status'],'RELEASED')
    for key in ['id','name','description','directory_path','required_features','dependencies','priority','implementation_complexity','related_tools','sequence_rank','expected_interface_ids']:self.assertEqual(t[key],by_id[t['id']][key])
   elif t['id'] in TASK21_IDS:assert_transition(self,t,by_id[t['id']])
   else:assert_unchanged_or_task22(self,t,by_id[t['id']])
   if t['status'] in ['TESTED','RELEASED']:
    p=t['directory_path']+'/index.html';self.assertEqual(norm((ROOT/p).read_bytes()),norm(git(p)))
  for folder in ['audit','assets']:
   paths=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,folder],cwd=ROOT,text=True).splitlines()
   for p in paths:self.assertEqual(norm((ROOT/p).read_bytes()),norm(git(p)),p)
  for p in ['CNAME','privacy.html','.github/workflows/functional-ci.yml','scripts/ci/run.py','scripts/ci/package-lock.json']:self.assertEqual(norm((ROOT/p).read_bytes()),norm(git(p)))
  current=without_cards(self,(ROOT/'index.html').read_text(encoding='utf8'),Homepage)
  for tid in IDS:
   card=next(c for c in Homepage(current).cards if c['attrs'].get('data-tool-id')==tid);self.assertEqual(card['attrs']['data-availability'],'released');chunk=current[card['start']:card['end']];self.assertEqual(chunk.count('Live'),1);chunk=chunk.replace('data-availability="released"','data-availability="tested"').replace('Live','Tested · publication pending');current=current[:card['start']]+chunk+current[card['end']:]
  home=Homepage(current);start,end=home.counts[0];current=current[:start]+'68 tools ready to use'+current[end:];self.assertEqual(current,norm(git('index.html')).decode());self.assertEqual({s:sum(t['status']==s for t in new['tools']) for s in ['RELEASED','TESTED','READY','PLANNED','BLOCKED']},TASK21_COUNTS)
if __name__=='__main__':unittest.main()
