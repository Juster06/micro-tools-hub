"""Task21 adds only six unpublished text/web utilities to the68-release baseline."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
BASE='8b1c17b86da72c3641477b5fdc5ea3cafb8a1c20'
sys.path.insert(0,str(ROOT/'scripts'))
from tool_homepage import Homepage
from task21_test_support import IDS,COUNTS,assert_transition,without_cards

def read(path):return (ROOT/path).read_text(encoding='utf8')
def load(path):return json.loads(read(path))
def blob(path,ref=BASE):return subprocess.check_output(['git','show',ref+':'+path],cwd=ROOT)
def normalized(raw):return raw.replace(b'\r\n',b'\n').rstrip()
def page_hash(raw):return hashlib.sha256(normalized(raw)).hexdigest()

class Task21Preservation(unittest.TestCase):
    def test_exact_inventory_and_only_six_registry_transitions(self):
        old=json.loads(blob('TOOL_REGISTRY.json'));new=load('TOOL_REGISTRY.json');byid={t['id']:t for t in new['tools']}
        self.assertEqual(len(new['tools']),93);self.assertEqual(new['milestones'],old['milestones']);self.assertEqual(set(byid),{t['id'] for t in old['tools']})
        for tool in old['tools']:
            if tool['id'] in IDS:assert_transition(self,tool,byid[tool['id']])
            else:self.assertEqual(tool,byid[tool['id']])
        self.assertEqual({s:sum(t['status']==s for t in new['tools']) for s in COUNTS},COUNTS)

    def test_all68_runtime_pages_existing_assets_privacy_domain_and_ci_pins_unchanged(self):
        old=json.loads(blob('TOOL_REGISTRY.json'));pages=[t['directory_path']+'/index.html' for t in old['tools'] if t['status']=='RELEASED'];self.assertEqual(len(pages),68)
        paths=pages+subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'assets'],cwd=ROOT,text=True).splitlines()
        paths+=['CNAME','privacy.html','.github/workflows/functional-ci.yml','scripts/ci/run.py','scripts/ci/package-lock.json','templates/text-input.html','templates/structured-input.html']
        for path in paths:self.assertEqual(normalized((ROOT/path).read_bytes()),normalized(blob(path)),path)

    def test_all_historical_audits_remain_byte_identical(self):
        paths=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'audit'],cwd=ROOT,text=True).splitlines();self.assertGreater(len(paths),100)
        for path in paths:self.assertEqual(normalized((ROOT/path).read_bytes()),normalized(blob(path)),path)

    def test_homepage_changes_only_six_pending_cards_and_count(self):
        current=read('index.html');home=Homepage(current);self.assertEqual(len(home.cards),74);self.assertEqual(len({c['attrs']['href'] for c in home.cards}),74)
        current=without_cards(self,current,Homepage);home=Homepage(current);start,end=home.counts[0];current=current[:start]+'68 tools ready to use'+current[end:]
        self.assertEqual(current,blob('index.html').decode('utf8').replace('\r\n','\n'))

    def test_new_pages_and_worker_assets_bind_to_real_git_source_and_scoped_tests(self):
        for tool in load('TOOL_REGISTRY.json')['tools']:
            if tool['id'] not in IDS:continue
            v=tool['verification'];audit=load(v['evidence_path']);self.assertEqual((audit['result'],audit['source_revision']),('PASS',v['source_revision']));self.assertEqual(audit['verified_on'],tool['last_verification_date']);self.assertIsNone(v['publication'])
            p=audit['pages'][0];self.assertEqual(p['source_sha256'],v['source_sha256']);self.assertEqual(page_hash(blob(p['path'],v['source_revision'])),v['source_sha256']);self.assertEqual(page_hash((ROOT/p['path']).read_bytes()),v['source_sha256'])
            for asset in audit['runtime_assets']:
                self.assertEqual(hashlib.sha256((ROOT/asset['path']).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),asset['sha256']);self.assertEqual(hashlib.sha256(blob(asset['path'],v['source_revision']).replace(b'\r\n',b'\n')).hexdigest(),asset['sha256'])
            for layer in ['structural','logic','browser']:
                self.assertEqual(audit['canonical_layers'][layer]['status'],'PASS')
                if layer!='structural':self.assertGreater(audit['canonical_layers'][layer]['passed'],0)
            self.assertGreater(audit['focused_node_tests'],0);self.assertGreater(audit['focused_browser_tests'],0)

    def test_dependency_versions_integrity_licences_and_no_pdf_adoption(self):
        a=load('audit/TASK_21_SECURITY_REVIEW.json');self.assertEqual(a['result'],'PASS');versions={p['name']:p['version'] for p in a['selected_packages']}
        for name,version in [('parse5','8.1.0'),('prettier','3.9.10'),('css-tree','3.2.1'),('terser','5.51.2'),('acorn','8.19.0')]:self.assertEqual(versions[name],version)
        self.assertNotIn('csso',versions);self.assertFalse(any('pdf' in p['name'].lower() for p in a['selected_packages']))
        for package in a['selected_packages']:
            self.assertTrue(package['dist']['integrity'].startswith('sha512-'));self.assertEqual(len(package['sha256']),64);self.assertEqual(package['osv'],{})
        for asset in a['artifacts']:
            data=(ROOT/asset['path']).read_bytes().replace(b'\r\n',b'\n');self.assertEqual(len(data),asset['bytes']);self.assertEqual(hashlib.sha256(data).hexdigest(),asset['sha256'])
        notices=read('assets/vendor/task21/THIRD_PARTY_NOTICES.txt')
        for label in ['parse5@8.1.0','prettier@3.9.10','css-tree@3.2.1','terser@5.51.2','acorn@8.19.0','BSD-2-Clause','MIT','CC0']:self.assertIn(label,notices)
        self.assertEqual(load('audit/TASK_21_PDF_DEFERRAL.json')['result'],'DEFER PDF UTILITIES')

    def test_isolation_gate_requires_network_positive_control_and_opaque_origin_probes(self):
        a=load('audit/TASK_21_SECURITY_REVIEW.json');self.assertTrue(all(x['status']=='PASS' for x in a['requirements']));b=a['browser_experiments'];self.assertEqual(b['status'],'PASS');self.assertEqual(b['canary_requests'],[]);self.assertEqual(b['observed_network_requests'],[])
        result={x['name']:x for x in b['results']};self.assertEqual(result['network-positive-control-with-interception-disabled']['http_status'],200)
        observations=result['actual-child-probes']['observations']
        for key in ['localStorage','sessionStorage','parent','top']:self.assertEqual(observations[key],'SecurityError')
        self.assertTrue(observations['popup']);self.assertEqual(observations['active'],0)
        source=read('html-previewer/index.html');self.assertIn('sandbox=""',source);self.assertNotIn('allow-scripts',source);self.assertNotIn('allow-same-origin',source)

    def test_all_new_pages_preserve_consent_loader_and_do_not_store_or_execute_input(self):
        self.assertEqual(normalized((ROOT/'assets/consent.js').read_bytes()),normalized(blob('assets/consent.js')))
        for tid in IDS:
            source=read(tid+'/index.html');self.assertEqual(source.count('<script defer src="../assets/consent.js"></script>'),1)
            for value in ['innerHTML','localStorage','sessionStorage','googletagmanager.com/gtag/js','gtag(']:self.assertNotIn(value,source)
            self.assertNotRegex(source,r'\beval\s*\(|new\s+Function')
        for p in (ROOT/'scripts/vendor/task21').glob('*-worker.mjs'):self.assertNotRegex(p.read_text(encoding='utf8'),r'\beval\s*\(|new\s+Function')

    def test_ci_maps_all74_tools_and_every_new_scope_without_lowering_floors(self):
        c=load('scripts/ci/coverage.json');old=json.loads(blob('scripts/ci/coverage.json'));self.assertEqual(len(c['tools']),74)
        for tid in IDS:
            self.assertEqual(c['tools'][tid],{'structural_job':'python-project','logic_job':'node-regression','browser_job':'browser-tests'})
            self.assertIn('tests/tools/'+tid+'/logic.test.mjs',c['node_files'])
            for name in ['extended-browser.test.mjs','integration-browser.test.mjs']:self.assertIn('tests/tools/'+tid+'/'+name,c['browser_files'])
        self.assertIn('tests/tools/html-previewer/isolation-browser.test.mjs',c['browser_files']);self.assertIn('scripts/consent-browser.test.mjs',c['browser_files']);self.assertIn('tests/test_task21_preservation.py',c['python_files'])
        for key,value in old['minimum_tests'].items():self.assertGreaterEqual(c['minimum_tests'][key],value)
        self.assertEqual(c['runtimes'],old['runtimes']);self.assertEqual(c['aggregate'],old['aggregate'])

if __name__=='__main__':unittest.main()
