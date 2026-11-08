"""Task 19 may add six tested utilities without altering any released source/evidence."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
BASE='3178f70802a96f181fd82251d417abd1dd0ad76b'
IDS={'password-generator','csv-to-txt','passphrase-generator','qr-code-generator','image-cropper','csv-data-cleaner'}
TASK20_IDS={'excel-formula-generator', 'resume-builder', 'emoji-picker', 'passport-photo-layout-maker', 'image-compressor', 'png-to-ico'}
sys.path.insert(0,str(ROOT/'scripts'))
from css_overlay import historical_snapshot
from git_fixtures import git_blob as frozen_git_blob
historical_source, historical_bytes = historical_snapshot(Path(__file__).resolve().parents[1])
from tool_homepage import Homepage
from task24_test_support import historical_registry,without_task24
from task25_test_support import tool_map_before_task25
from task22_test_support import assert_unchanged_or_task22,without_task22
from task21_test_support import IDS as TASK21_IDS, COUNTS as TASK21_COUNTS, assert_transition, without_cards

def raw(path,revision=BASE):
    return frozen_git_blob(ROOT,revision,path)

def text(path):
    return historical_source(ROOT, (ROOT/path).relative_to(ROOT).as_posix(), (ROOT/path).read_text(encoding='utf8'))

def normalized(value):
    return value.replace('\r\n','\n').rstrip().encode('utf8')

class Task19Preservation(unittest.TestCase):
    def test_inventory_changes_only_selected_six_and_preserves_all_prior_records(self):
        old=json.loads(raw('TOOL_REGISTRY.json'));new=historical_registry(json.loads(text('TOOL_REGISTRY.json')))
        self.assertEqual(len(new['tools']),93);self.assertEqual(new['milestones'],old['milestones'])
        by_id={t['id']:t for t in new['tools']};self.assertEqual(set(by_id),{t['id'] for t in old['tools']})
        for tool in old['tools']:
            current=by_id[tool['id']]
            if tool['id'] in IDS:
                self.assertEqual((tool['status'],current['status']),('PLANNED','RELEASED'))
                self.assertEqual(current['verification']['publication']['source_matches'],True)
                for key in ['id','name','category','description','directory_path','priority','required_features','related_tools','sequence_rank']:
                    self.assertEqual(current[key],tool[key])
            elif tool['id'] in TASK20_IDS:self.assertEqual((tool['status'],current['status']),('PLANNED','RELEASED'));self.assertTrue(current['verification']['publication']['source_matches'])
            elif tool['id'] in TASK21_IDS:assert_transition(self,tool,current)
            else:assert_unchanged_or_task22(self,tool,current)
        counts={status:sum(t['status']==status for t in new['tools']) for status in ['RELEASED','TESTED','READY','PLANNED','BLOCKED']}
        self.assertEqual(counts,TASK21_COUNTS)

    def test_all_56_released_runtime_sources_and_privacy_domain_settings_unchanged(self):
        old=json.loads(raw('TOOL_REGISTRY.json'))
        for tool in old['tools']:
            if tool['status']=='RELEASED':
                path=tool['directory_path']+'/index.html'
                self.assertEqual(text(path),raw(path).decode('utf8').replace('\r\n','\n'))
        for path in ['CNAME','assets/consent.js','privacy.html','.github/workflows/functional-ci.yml','scripts/ci/package-lock.json','scripts/ci/run.py','templates/text-input.html','templates/structured-input.html']:
            self.assertEqual(text(path),raw(path).decode('utf8').replace('\r\n','\n'))

    def test_only_six_gated_cards_and_initial_count_change_in_the_hub(self):
        current=without_cards(self,text('index.html'),Homepage)
        for tid in TASK20_IDS:
            home=Homepage(current);card=next(c for c in home.cards if c['attrs'].get('data-tool-id')==tid)
            self.assertEqual(card['attrs']['href'],tid+'/index.html');self.assertEqual(card['attrs']['data-availability'],'released')
            self.assertIn('Live',current[card['start']:card['end']])
            current=current[:card['start']-2]+current[card['end']+7:]
        for tid in IDS:
            home=Homepage(current);card=next(c for c in home.cards if c['attrs'].get('data-tool-id')==tid)
            self.assertEqual(card['attrs']['href'],tid+'/index.html');self.assertEqual(card['attrs']['data-availability'],'released')
            self.assertIn('Live',current[card['start']:card['end']])
            current=current[:card['start']-2]+current[card['end']+7:]
        home=Homepage(current);start,end=home.counts[0];current=current[:start]+'56 tools ready to use'+current[end:]
        self.assertEqual(current,raw('index.html').decode('utf8').replace('\r\n','\n'))

    def test_all_historical_audit_records_remain_unchanged(self):
        names=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'audit'],cwd=ROOT,text=True).splitlines()
        self.assertGreater(len(names),70)
        for path in names:self.assertEqual(historical_bytes(ROOT, (ROOT/path).relative_to(ROOT).as_posix(), (ROOT/path).read_bytes()).replace(b'\r\n',b'\n'),raw(path).replace(b'\r\n',b'\n'))

    def test_dependency_payload_hashes_licenses_and_wordlist_content_are_pinned(self):
        manifest=json.loads(text('audit/TASK_19_DEPENDENCIES.json'))
        for item in [*manifest['runtime'].values(),*manifest['test_only'].values()]:
            content=historical_bytes(ROOT, (ROOT/item['path']).relative_to(ROOT).as_posix(), (ROOT/item['path']).read_bytes()).replace(b'\r\n',b'\n')
            self.assertEqual(hashlib.sha256(content).hexdigest(),item['sha256'])
            self.assertEqual(len(content),item['bytes'])
        self.assertEqual(manifest['runtime']['qrcodegen']['license'],'MIT')
        self.assertEqual(hashlib.sha256(text('audit/vendor-source/qrcodegen-1.8.0.ts').encode()).hexdigest(),manifest['runtime']['qrcodegen']['source_sha256'])
        self.assertEqual(manifest['runtime']['qrcodegen']['upstream_source_sha256'],'c4749095a91bf9696e3a303998b9905e467094f53041e64393e65e6d887737fd')
        for path,key in [('audit/vendor-source/qrcodegen-1.8.0.ts','upstream_source_sha256'),('assets/vendor/qrcodegen-1.8.0.js','pre_normalization_compiled_sha256')]:
            original=raw(path,'139d87f76d16fd22c4aabfba570b94bb2d348202')
            self.assertEqual(hashlib.sha256(original).hexdigest(),manifest['runtime']['qrcodegen'][key])
            cleaned='\n'.join(line.rstrip(' \t') for line in original.decode('utf8').splitlines()).rstrip()+'\n'
            self.assertEqual(cleaned,text(path))
        self.assertEqual(manifest['test_only']['jsqr']['license'],'Apache-2.0')
        self.assertIn('Creative Commons Attribution 4.0',text('assets/data/EFF-WORDLIST-LICENSE.txt'))
        pairs=[line.split('\t') for line in text('assets/data/eff-large-wordlist.txt').splitlines()]
        self.assertEqual(len(pairs),7776);self.assertEqual(len({p[0] for p in pairs}),7776);self.assertEqual(len({p[1] for p in pairs}),7776)
        wrapper=text('assets/data/eff-wordlist.js')
        words=json.loads(wrapper.split('Object.freeze(',1)[1].rsplit(');',1)[0]);self.assertEqual(words,[p[1] for p in pairs])
        self.assertEqual(hashlib.sha256(wrapper.encode()).hexdigest(),manifest['runtime']['wordlist']['wrapper_sha256'])
        self.assertIn('Apache License',text('tests/vendor/jsQR-LICENSE.txt'))

    def test_six_development_audits_bind_real_git_source_and_successful_canonical_layers(self):
        registry=historical_registry(json.loads(text('TOOL_REGISTRY.json')))
        for tool in registry['tools']:
            if tool['id'] not in IDS:continue
            verification=tool['verification'];audit=json.loads(text(verification['evidence_path']));page=audit['pages'][0]
            self.assertEqual(audit['result'],'PASS');self.assertEqual(audit['source_revision'],verification['source_revision'])
            source=raw(tool['directory_path']+'/index.html',verification['source_revision']).decode('utf8')
            self.assertEqual(hashlib.sha256(normalized(source)).hexdigest(),verification['source_sha256'])
            self.assertEqual(hashlib.sha256(normalized(text(page['path']))).hexdigest(),page['source_sha256'])
            self.assertEqual(page['source_sha256'],verification['source_sha256'])
            self.assertEqual(verification['publication']['source_matches'],True)
            development=json.loads(text(audit['previous_evidence']))
            self.assertEqual(development['result'],'PASS')
            self.assertEqual(development['pages'][0]['source_sha256'],verification['source_sha256'])
            self.assertEqual(hashlib.sha256(normalized(raw(page['path'],development['source_revision']).decode('utf8'))).hexdigest(),verification['source_sha256'])
            for layer in ['structural','logic','browser']:
                self.assertEqual(development['canonical_layers'][layer]['status'],'PASS')
                if layer!='structural':self.assertGreater(development['canonical_layers'][layer]['passed'],0)

    def test_new_pages_use_only_shared_consent_and_local_reviewed_dependencies(self):
        for tid in IDS:
            source=text(tid+'/index.html')
            self.assertEqual(source.count('<script defer src="../assets/consent.js"></script>'),1)
            self.assertNotIn('googletagmanager.com/gtag/js',source);self.assertNotIn('gtag(',source)
            self.assertNotIn('Math.random',source);self.assertNotIn('localStorage',source)
            self.assertNotIn('jsQR-1.4.0',source)

    def test_coverage_includes_all_new_tools_and_existing_mandatory_scopes(self):
        coverage=json.loads(text('scripts/ci/coverage.json'))
        self.assertEqual(len(tool_map_before_task25(coverage)),81)
        for tid in IDS:
            self.assertEqual(coverage['tools'][tid],{'structural_job':'python-project','logic_job':'node-regression','browser_job':'browser-tests'})
            self.assertIn('tests/tools/'+tid+'/logic.test.mjs',coverage['node_files'])
            for name in ['extended-browser.test.mjs','integration-browser.test.mjs']:
                self.assertIn('tests/tools/'+tid+'/'+name,coverage['browser_files'])
        for key,floor in [('python-project',153),('node-regression',363),('browser-tests',478)]:self.assertGreaterEqual(coverage['minimum_tests'][key],floor)

if __name__=='__main__':unittest.main()
