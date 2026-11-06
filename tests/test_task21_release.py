"""Fresh public source/behavior evidence and strict six-tool release preservation."""
from pathlib import Path
from datetime import datetime
import hashlib,json,subprocess,sys,unittest
from functools import lru_cache
ROOT=Path(__file__).resolve().parents[1];BASE='9fa032140639550abd9a0449ed7ef5198354bd40'
sys.path.insert(0,str(ROOT/'scripts'))
from tool_homepage import Homepage
from task22_test_support import assert_unchanged_or_task22,without_task22
IDS={'hashtag-counter','html-formatter','css-minifier','javascript-minifier','html-to-markdown','html-previewer'}
def load(p):return json.loads((ROOT/p).read_text(encoding='utf8'))
@lru_cache(maxsize=None)
def git(p):return subprocess.check_output(['git','show',BASE+':'+p],cwd=ROOT)
def norm(b):return b.replace(b'\r\n',b'\n')
def sha(b):return hashlib.sha256(b).hexdigest()
class Task21Release(unittest.TestCase):
 def test_exact_six_transitions_preserve_every_other_record_and_all_tool_metadata(self):
  old=json.loads(git('TOOL_REGISTRY.json'));new=load('TOOL_REGISTRY.json');byid={t['id']:t for t in new['tools']}
  self.assertEqual(len(new['tools']),93);self.assertEqual(new['milestones'],old['milestones']);self.assertEqual(set(byid),{t['id'] for t in old['tools']})
  for t in old['tools']:
   n=byid[t['id']]
   if t['id'] in IDS:
    self.assertEqual((t['status'],n['status'],n['testing_status']),('TESTED','RELEASED','REQUIRED_PASSED'))
    for key in set(t)-{'status','notes','last_verification_date','verification'}:self.assertEqual(t[key],n[key],key)
   else:assert_unchanged_or_task22(self,t,n)
  self.assertEqual({s:sum(t['status']==s for t in new['tools']) for s in ['RELEASED','TESTED','READY','PLANNED','BLOCKED']},{'RELEASED':74,'TESTED':1,'READY':0,'PLANNED':17,'BLOCKED':1})

 def test_six_public_audits_bind_real_git_pages_assets_dates_and_individual_behavior(self):
  for t in load('TOOL_REGISTRY.json')['tools']:
   if t['id'] not in IDS:continue
   v=t['verification'];a=load(v['evidence_path']);p=a['pages'][0];raw=git(p['path'])
   self.assertEqual((a['result'],a['source_revision']),('PASS',BASE));self.assertEqual(a['verified_on'],t['last_verification_date']);self.assertEqual(a['source_tree_sha'],subprocess.check_output(['git','rev-parse',BASE+'^{tree}'],cwd=ROOT,text=True).strip())
   self.assertEqual(sha(norm(raw).rstrip()),v['source_sha256']);self.assertEqual(p['source_sha256'],v['source_sha256']);self.assertEqual(p['publication'],v['publication']);self.assertIs(v['publication']['source_matches'],True);self.assertEqual(v['publication']['http_status'],200);datetime.fromisoformat(v['publication']['checked_at'])
   self.assertEqual(v['publication']['url'],'https://everydaydigitalbox.com/'+t['directory_path']+'/')
   for s in [a['public_index'],a['canonical_public_url']]:
    self.assertEqual((s['http_status'],s['raw_match']),(200,True));self.assertEqual(s['raw_public_sha256'],sha(raw));self.assertEqual(s['raw_approved_sha256'],sha(raw));self.assertEqual(s['source_sha256'],v['source_sha256']);datetime.fromisoformat(s['checked_at'])
   for asset in a['runtime_assets']:
    s=a['runtime_assets_public'][asset['path']];self.assertEqual((s['http_status'],s['raw_match']),(200,True));self.assertEqual(s['raw_public_sha256'],sha(git(asset['path'])));self.assertEqual(asset['sha256'],sha(norm(git(asset['path']))))
   self.assertEqual(a['live_browser']['result'],'PASS');self.assertEqual(a['live_browser']['test_count'],2 if t['id']=='html-previewer' else 4);self.assertEqual(len(a['live_browser']['cases']),a['live_browser']['test_count']);self.assertEqual(a['live_browser']['isolation_cases'],13 if t['id']=='html-previewer' else 0)
   self.assertEqual(norm((ROOT/a['previous_evidence']).read_bytes()),norm(git(a['previous_evidence'])))

 def test_full_public_catalog_source_identity_and_real_consent_are_fresh_and_complete(self):
  a=load('audit/TASK_21_PUBLIC_RELEASE_VERIFICATION.json');self.assertEqual(a['result'],'PASS');self.assertEqual(a['source_revision'],BASE);self.assertEqual((a['deployment']['run_id'],a['post_merge_ci']['run_id']),(42159767277,42159767505));self.assertEqual(a['github']['main']['sha'],BASE);self.assertTrue(a['github']['pr']['merged']);self.assertEqual(len(a['github']['post_merge_ci']['jobs']),4);self.assertTrue(all(j['conclusion']=='success' for j in a['github']['post_merge_ci']['jobs']))
  self.assertEqual(len(a['sources']),90);self.assertEqual(len(a['canonical_public_urls']),6)
  for path,s in a['sources'].items():self.assertEqual((s['http_status'],s['raw_match']),(200,True));self.assertEqual(s['raw_public_sha256'],sha(git(path)));self.assertEqual(s['raw_approved_sha256'],s['raw_public_sha256'])
  h=a['homepage'];self.assertEqual((h['cards'],h['distinct'],h['visible_cards'],h['canonical_routes_match']),(74,74,74,True));self.assertEqual(sorted(h['routes']),sorted(t['directory_path']+'/index.html' for t in load('TOOL_REGISTRY.json')['tools'] if t['status']=='RELEASED'))
  b=a['public_browser'];self.assertEqual(b['total_cases'],36)
  for kind,n in [('functional',23),('isolation',13)]:self.assertEqual(b[kind],{'tests':n,'pass':n,'fail':0,'cancelled':0,'skipped':0,'todo':0})
  self.assertEqual((b['uncaught_application_errors'],b['functional_google_requests'],b['unexpected_dependencies']),(0,0,[]))
  c=a['consent'];self.assertEqual(c['result'],'PASS');self.assertEqual(len(c['checks']),6);self.assertTrue(all(x['result']=='PASS' for x in c['checks']));self.assertEqual(c['google_tag_loads'],3);self.assertEqual(len(c['page_views']),3)
  for p in c['page_views']:self.assertEqual((p['measurement_id'],p['event'],p['http_response']),('G-XDHPQYJ5CH','page_view',204));self.assertNotIn('?',p['page_location']);self.assertNotIn('#',p['page_location'])
  self.assertEqual(len({p['page_location'] for p in c['page_views']}),3);self.assertIn('GA4 browser collection requests verified; property-level reporting remains unverified.',c['limitations'])

 def test_public_isolation_has_parent_child_positive_controls_and_actual_denial_probes(self):
  a=load('audit/TASK_21_PUBLIC_RELEASE_VERIFICATION.json');results={x['check']:x for x in a['isolation']['observations']};self.assertEqual(len(results),13);self.assertTrue(all(x['result']=='PASS' for x in results.values()))
  for name in ['root-network-positive-control','child-network-positive-control']:self.assertEqual(results[name]['status'],200)
  self.assertIs(results['child-network-positive-control']['child_session_observed'],True)
  for name in ['scripts','handlers','navigation','forms','resources','foreign','mutation','templates','rawtext','encoded']:self.assertEqual(results[name]['unexpected_canary_requests'],0);self.assertEqual(results[name]['new_web_page_targets'],0)
  p=a['child_probes'];self.assertEqual(p['heading'],'Hello');self.assertIs(p['visible'],True);self.assertEqual(p['active'],0);self.assertIn("default-src 'none'",p['csp']);self.assertIn("form-action 'none'",p['csp'])
  for k in ['localStorage','sessionStorage','parent','parentStorage','top']:self.assertEqual(p[k],'SecurityError')
  self.assertIs(p['popup'],True)
  for kind,r in a['public_browser']['records'].items():
   self.assertEqual(r['exceptions'],[]);self.assertEqual(r['unexpected_dependencies'],[]);self.assertEqual(r['instrumentation_errors'],[]);self.assertEqual(r['google_requests'],0)
   for error in r['console_errors']:self.assertTrue(error['url'].endswith('/favicon.ico') or (error['expected_security_probe'] and error.get('classification') in ['sandbox-blocked-navigation','sandbox-blocked-popup','sandbox-or-csp-blocked-form']))
  requests=a['public_browser']['records']['isolation']['canary_requests'];self.assertEqual(len(requests),2);self.assertTrue(all('positive-' in r['url'] for r in requests))

 def test_release_does_not_change_any_runtime_asset_historical_audit_or_unrelated_hub_markup(self):
  old=json.loads(git('TOOL_REGISTRY.json'));pages=[t['directory_path']+'/index.html' for t in old['tools'] if t['status'] in ['TESTED','RELEASED']];self.assertEqual(len(pages),74)
  paths=pages+['CNAME','privacy.html','.github/workflows/functional-ci.yml','scripts/ci/run.py','scripts/ci/package-lock.json']
  paths+=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'assets','audit','scripts/vendor/task21'],cwd=ROOT,text=True).splitlines()
  for path in paths:self.assertEqual(norm((ROOT/path).read_bytes()),norm(git(path)),path)
  current=without_task22(self,(ROOT/'index.html').read_text(encoding='utf8'),Homepage)
  for tid in IDS:
   card=next(c for c in Homepage(current).cards if c['attrs'].get('data-tool-id')==tid);chunk=current[card['start']:card['end']];self.assertEqual(chunk.count('Live'),1);self.assertEqual(card['attrs']['data-availability'],'released');chunk=chunk.replace('data-availability="released"','data-availability="tested"').replace('Live','Tested · publication pending');current=current[:card['start']]+chunk+current[card['end']:]
  self.assertEqual(current,norm(git('index.html')).decode('utf8'))
  a=load('audit/TASK_21_PUBLIC_RELEASE_VERIFICATION.json');self.assertEqual(a['milestones'],{'next_planning_checkpoint':75,'generated_registry_milestone':100,'configuration_changed':False});self.assertEqual(a['preservation']['original_worktrees'],23);self.assertTrue(a['preservation']['original_worktrees_unchanged']);self.assertEqual(len(a['preservation']['dirty_files_preserved']),2)
  for item in a['reproduction_scripts']:self.assertEqual(sha((ROOT/item['path']).read_bytes().replace(b'\r\n',b'\n')),item['sha256'])
if __name__=='__main__':unittest.main()
