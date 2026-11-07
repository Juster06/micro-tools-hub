"""Source-bound real-public evidence permits precisely the verified Task22 release."""
from pathlib import Path
from functools import lru_cache
from datetime import datetime
import hashlib,json,subprocess,sys,unittest
ROOT=Path(__file__).resolve().parents[1];BASE='64a19c6bc1ee2dfbd81cf9ffa6b1ca00f15c8140';ID='markdown-converter-previewer'
sys.path.insert(0,str(ROOT/'scripts'));from tool_homepage import Homepage
from css_overlay import historical_snapshot
from git_fixtures import git_blob as frozen_git_blob
historical_source, historical_bytes = historical_snapshot(Path(__file__).resolve().parents[1])
from task24_test_support import historical_registry,without_task24
def load(p):
 data=json.loads(historical_source(ROOT, (ROOT/p).relative_to(ROOT).as_posix(), (ROOT/p).read_text(encoding='utf-8')))
 return historical_registry(data) if p=='TOOL_REGISTRY.json' else data
@lru_cache(maxsize=None)
def git(p):return frozen_git_blob(ROOT,BASE,p)
def norm(b):return b.replace(b'\r\n',b'\n')
def sha(b):return hashlib.sha256(b).hexdigest()
class Task22Release(unittest.TestCase):
 def test_exactly_one_verified_promotion_preserves_other92_records_and_all_identity(self):
  old=json.loads(git('TOOL_REGISTRY.json'));new=load('TOOL_REGISTRY.json');byid={t['id']:t for t in new['tools']};self.assertEqual(len(byid),93);self.assertEqual(set(byid),{t['id']for t in old['tools']});self.assertEqual(new['milestones'],old['milestones'])
  for t in old['tools']:
   n=byid[t['id']]
   if t['id']==ID:
    self.assertEqual((t['status'],n['status'],n['testing_status']),('TESTED','RELEASED','REQUIRED_PASSED'))
    for k in set(t)-{'status','notes','last_verification_date','verification'}:self.assertEqual(t[k],n[k],k)
   else:self.assertEqual(t,n,t['id'])
  self.assertEqual({s:sum(t['status']==s for t in new['tools'])for s in ['RELEASED','TESTED','READY','PLANNED','BLOCKED']},{'RELEASED':75,'TESTED':0,'READY':0,'PLANNED':17,'BLOCKED':1})
 def test_publication_binds_actual_approved_commit_page_assets_and_preserved_development_evidence(self):
  t=next(t for t in load('TOOL_REGISTRY.json')['tools']if t['id']==ID);v=t['verification'];a=load(v['evidence_path']);self.assertEqual((a['result'],a['source_revision']),('PASS',BASE));self.assertEqual(a['source_tree_sha'],subprocess.check_output(['git','rev-parse',BASE+'^{tree}'],cwd=ROOT,text=True).strip());self.assertEqual(a['verified_on'],t['last_verification_date']);self.assertEqual(sha(norm(git(ID+'/index.html')).rstrip()),v['source_sha256']);self.assertEqual(a['pages'][0]['source_sha256'],v['source_sha256']);self.assertEqual(a['pages'][0]['publication'],v['publication']);self.assertEqual(a['publication'],v['publication']);self.assertEqual(v['publication']['url'],'https://everydaydigitalbox.com/'+ID+'/');self.assertEqual(v['publication']['http_status'],200);self.assertIs(v['publication']['source_matches'],True);datetime.fromisoformat(v['publication']['checked_at'])
  for p in [a['public_index'],a['canonical_public_url']]:self.assertEqual((p['http_status'],p['raw_match']),(200,True));self.assertEqual(p['raw_public_sha256'],sha(git(ID+'/index.html')));self.assertEqual(p['raw_approved_sha256'],p['raw_public_sha256']);self.assertEqual(p['source_sha256'],v['source_sha256'])
  for asset in a['runtime_assets']:
   public=a['runtime_assets_public'][asset['path']];self.assertEqual((public['http_status'],public['raw_match']),(200,True));self.assertEqual(public['raw_public_sha256'],sha(git(asset['path'])));self.assertEqual(asset['sha256'],sha(norm(git(asset['path']))))
  self.assertEqual(norm(historical_bytes(ROOT, (ROOT/a['previous_evidence']).relative_to(ROOT).as_posix(), (ROOT/a['previous_evidence']).read_bytes())),norm(git(a['previous_evidence'])));self.assertEqual(a['live_browser']['actual_download_mime'],'text/html;charset=utf-8')
 def test_complete_public_catalog_real_browser_results_and_real_consent_are_fresh_and_bound(self):
  a=load('audit/TASK_22_PUBLIC_RELEASE_VERIFICATION.json');self.assertEqual((a['result'],a['source_revision']),('PASS',BASE));self.assertEqual((a['deployment']['run_id'],a['post_merge_ci']['run_id']),(42205116968,42205117641));self.assertEqual(a['github']['main']['sha'],BASE);self.assertEqual(a['github']['pr']['merge_commit'],BASE);self.assertTrue(a['github']['pr']['merged']);self.assertEqual(len(a['post_merge_ci']['jobs']),4);self.assertTrue(all(j['conclusion']=='success'for j in a['post_merge_ci']['jobs']));self.assertEqual(a['deployment']['sha'],BASE);self.assertEqual(a['post_merge_ci']['sha'],BASE)
  self.assertEqual(len(a['sources']),93);self.assertEqual(len(a['canonical_public_urls']),1)
  for path,s in a['sources'].items():self.assertEqual((s['http_status'],s['raw_match']),(200,True));self.assertEqual(s['raw_public_sha256'],sha(git(path)));self.assertEqual(s['raw_approved_sha256'],s['raw_public_sha256'])
  h=a['homepage'];self.assertEqual((h['cards'],h['distinct'],h['visible_cards'],h['canonical_routes_match']),(75,75,75,True));self.assertEqual(sorted(h['routes']),sorted(t['directory_path']+'/index.html'for t in load('TOOL_REGISTRY.json')['tools']if t['status']=='RELEASED'))
  b=a['public_browser'];self.assertEqual(b['total_cases'],35)
  for kind,n in [('functional',22),('isolation',13)]:self.assertEqual(b[kind],{'tests':n,'pass':n,'fail':0,'cancelled':0,'skipped':0,'todo':0})
  for record in b['records'].values():
   self.assertEqual(record['exceptions'],[]);self.assertEqual(record['unexpected_dependencies'],[]);self.assertEqual(record['instrumentation_errors'],[]);self.assertEqual(record['google_requests'],0)
   for e in record['console_errors']:self.assertTrue(e['url'].endswith('/favicon.ico')or(e['expected_security_probe']and e['classification']in['sandbox-blocked-navigation','sandbox-blocked-popup','sandbox-or-csp-blocked-form']))
  c=a['consent'];self.assertEqual(c['result'],'PASS');self.assertEqual(len(c['checks']),6);self.assertTrue(all(x['result']=='PASS'for x in c['checks']));self.assertEqual(c['google_tag_loads'],3);self.assertEqual(len(c['page_views']),3);self.assertEqual(len({v['page_location']for v in c['page_views']}),3)
  for v in c['page_views']:self.assertEqual((v['measurement_id'],v['event'],v['http_response']),('G-XDHPQYJ5CH','page_view',204));self.assertNotIn('?',v['page_location']);self.assertNotIn('#',v['page_location'])
  self.assertIn('GA4 browser collection requests verified; property-level reporting remains unverified.',c['limitations'])
 def test_actual_public_isolation_has_parent_child_controls_and_origin_navigation_denial(self):
  a=load('audit/TASK_22_PUBLIC_RELEASE_VERIFICATION.json');results={x['check']:x for x in a['isolation']['observations']};self.assertEqual(len(results),13);self.assertTrue(all(x['result']=='PASS'for x in results.values()))
  for name in ['root-network-positive-control','child-network-positive-control']:self.assertEqual(results[name]['status'],200)
  self.assertIs(results['child-network-positive-control']['child_session_observed'],True)
  for name in ['scripts','handlers','navigation','forms','resources','foreign','mutation','templates','rawtext','encoded']:self.assertEqual(results[name]['unexpected_canary_requests'],0);self.assertEqual(results[name]['new_web_page_targets'],0)
  child=a['child_probes'];self.assertEqual(child['heading'],'Hello');self.assertIs(child['visible'],True);self.assertEqual(child['active'],0)
  for k in ['localStorage','sessionStorage','parent','parentStorage','top']:self.assertEqual(child[k],'SecurityError')
  self.assertIs(child['popup'],True);self.assertIn("default-src 'none'",child['csp']);self.assertIn("form-action 'none'",child['csp'])
  requests=a['public_browser']['records']['isolation']['canary_requests'];self.assertEqual(len(requests),2);self.assertTrue(all('positive-'in x['url']for x in requests))
  for item in a['reproduction_scripts']:self.assertEqual(sha(norm(historical_bytes(ROOT, (ROOT/item['path']).relative_to(ROOT).as_posix(), (ROOT/item['path']).read_bytes()))),item['sha256'])
 def test_release_preserves_all75_runtime_pages_assets_historical_audits_and_only_changes_one_card_label(self):
  old=json.loads(git('TOOL_REGISTRY.json'));pages=[t['directory_path']+'/index.html'for t in old['tools']if t['status']in ['TESTED','RELEASED']];self.assertEqual(len(pages),75)
  paths=pages+['CNAME','privacy.html','.github/workflows/functional-ci.yml','scripts/ci/run.py','scripts/ci/package-lock.json']+subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'assets','audit','scripts/vendor'],cwd=ROOT,text=True).splitlines()
  for path in paths:self.assertEqual(norm(historical_bytes(ROOT, (ROOT/path).relative_to(ROOT).as_posix(), (ROOT/path).read_bytes())),norm(git(path)),path)
  current=without_task24(historical_source(ROOT, (ROOT/'index.html').relative_to(ROOT).as_posix(), (ROOT/'index.html').read_text(encoding='utf-8')),Homepage);card=next(c for c in Homepage(current).cards if c['attrs'].get('data-tool-id')==ID);chunk=current[card['start']:card['end']];self.assertEqual(card['attrs']['data-availability'],'released');self.assertEqual(chunk.count('Live'),1);chunk=chunk.replace('data-availability="released"','data-availability="tested"').replace('Live','Tested · publication pending');self.assertEqual(current[:card['start']]+chunk+current[card['end']:],norm(git('index.html')).decode())
  a=load('audit/TASK_22_PUBLIC_RELEASE_VERIFICATION.json');self.assertEqual(a['milestones'],{'next_planning_checkpoint':75,'generated_registry_milestone':100,'configuration_changed':False});self.assertEqual(a['preservation']['original_worktrees'],25);self.assertTrue(a['preservation']['original_worktrees_unchanged']);self.assertEqual(len(a['preservation']['dirty_files_preserved']),2)
if __name__=='__main__':unittest.main()
