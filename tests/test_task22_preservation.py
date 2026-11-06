"""One Task22 addition preserves the entire 74-release source baseline."""
from pathlib import Path
from functools import lru_cache
import hashlib,json,subprocess,sys,unittest
ROOT=Path(__file__).resolve().parents[1];BASE='93f2589b244f933e353d4d93ee145e35ed354399'
sys.path.insert(0,str(ROOT/'scripts'))
from task22_test_support import ID,COUNTS,assert_unchanged_or_task22,without_task22
from tool_homepage import Homepage
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
@lru_cache(maxsize=None)
def git(p,ref=BASE):return subprocess.check_output(['git','show',ref+':'+p],cwd=ROOT)
def norm(b):return b.replace(b'\r\n',b'\n')
def sha(b):return hashlib.sha256(b).hexdigest()
class Task22Preservation(unittest.TestCase):
 def test_exactly_one_authorized_transition_and_unchanged_metadata(self):
  old=json.loads(git('TOOL_REGISTRY.json'));new=load('TOOL_REGISTRY.json');byid={t['id']:t for t in new['tools']};self.assertEqual(len(new['tools']),93);self.assertEqual(set(byid),{t['id'] for t in old['tools']});self.assertEqual(old['milestones'],new['milestones'])
  for t in old['tools']:assert_unchanged_or_task22(self,t,byid[t['id']])
  self.assertEqual({s:sum(t['status']==s for t in new['tools'])for s in COUNTS},COUNTS)
 def test_all74_released_pages_and_existing_assets_audits_privacy_ci_unchanged(self):
  old=json.loads(git('TOOL_REGISTRY.json'));pages=[t['directory_path']+'/index.html'for t in old['tools']if t['status']=='RELEASED'];self.assertEqual(len(pages),74)
  paths=pages+['CNAME','privacy.html','.github/workflows/functional-ci.yml','scripts/ci/run.py','scripts/ci/package-lock.json']+subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'assets','audit','scripts/vendor/task21'],cwd=ROOT,text=True).splitlines()
  for p in paths:self.assertEqual(norm((ROOT/p).read_bytes()),norm(git(p)),p)
 def test_one_pending_card_is_the_only_hub_change(self):
  source=(ROOT/'index.html').read_text(encoding='utf-8');home=Homepage(source);self.assertEqual(len(home.cards),75);self.assertEqual(len({c['attrs']['href']for c in home.cards}),75);self.assertEqual(without_task22(self,source,Homepage),norm(git('index.html')).decode())
 def test_release_evidence_binds_real_source_and_verified_publication(self):
  t=next(t for t in load('TOOL_REGISTRY.json')['tools']if t['id']==ID);v=t['verification'];a=load(v['evidence_path']);self.assertEqual(a['result'],'PASS');self.assertEqual(v['publication']['http_status'],200);self.assertIs(v['publication']['source_matches'],True);self.assertEqual(a['publication'],v['publication']);self.assertEqual(a['source_revision'],v['source_revision']);self.assertEqual(a['source_tree_sha'],subprocess.check_output(['git','rev-parse',v['source_revision']+'^{tree}'],cwd=ROOT,text=True).strip());self.assertEqual(sha(norm(git(ID+'/index.html',v['source_revision'])).rstrip()),v['source_sha256']);self.assertEqual(sha(norm((ROOT/ID/'index.html').read_bytes()).rstrip()),v['source_sha256'])
  for asset in a['runtime_assets']:self.assertEqual(sha(norm((ROOT/asset['path']).read_bytes())),asset['sha256']);self.assertEqual(sha(norm(git(asset['path'],v['source_revision']))),asset['sha256'])
  for layer in ['structural','logic','browser']:self.assertEqual(a['canonical_layers'][layer]['status'],'PASS')
 def test_security_review_has_versions_integrity_advisory_review_and_positive_controls(self):
  a=load('audit/TASK_22_SECURITY_REVIEW.json');self.assertEqual(a['result'],'PASS');pkgs=a['dependencies']['packages'];self.assertEqual({p['name']:p['version']for p in pkgs},{'marked':'18.1.3','parse5':'8.1.0','entities':'9.0.0','esbuild':'0.28.2','@esbuild/win32-x64':'0.28.2'})
  for p in pkgs:self.assertTrue(p['dist']['integrity'].startswith('sha512-'));self.assertEqual(len(p['sha256']),64);self.assertEqual(p['osv'],{})
  g=a['preimplementation_gate'];self.assertEqual((g['tests'],g['passed'],g['failed']),(30,30,0));self.assertEqual((g['root_canary_http'],g['child_canary_http']),(200,200));self.assertEqual(g['unexpected_canary_requests'],0);self.assertEqual(a['advisory_review']['patched'],'18.0.2')
  self.assertEqual(a['followup_rendering_budget_gate']['passed'],31)
  self.assertEqual(a['bundle']['sha256'],sha(norm((ROOT/'assets/vendor/task22/markdown-source.js').read_bytes())))
  for item in a['prototype_archive']:self.assertEqual(sha(norm((ROOT/item['path']).read_bytes())),item['sha256'])
 def test_page_does_not_store_or_evaluate_input_and_retains_consent(self):
  source=(ROOT/ID/'index.html').read_text(encoding='utf-8');self.assertEqual(source.count('<script defer src="../assets/consent.js"></script>'),1);self.assertIn('sandbox=""',source);self.assertIn('referrerpolicy="no-referrer"',source)
  for text in ['localStorage','sessionStorage','innerHTML','gtag(','allow-scripts','allow-same-origin']:self.assertNotIn(text,source)
  self.assertNotRegex(source,r'\beval\s*\(|new\s+Function');self.assertEqual(norm((ROOT/'assets/consent.js').read_bytes()),norm(git('assets/consent.js')))
 def test_ci_adds_mandatory_scope_without_changing_pins_or_deadlines(self):
  old=json.loads(git('scripts/ci/coverage.json'));new=load('scripts/ci/coverage.json');self.assertEqual(len(new['tools']),75)
  for key in ['runtimes','aggregate','minimum_tests','jobs']:self.assertEqual(old[key],new[key])
  for key in ['python_files','node_files','browser_files']:self.assertTrue(set(old[key])<=set(new[key]))
  self.assertEqual(new['tools'][ID],{'structural_job':'python-project','logic_job':'node-regression','browser_job':'browser-tests'})
if __name__=='__main__':unittest.main()
