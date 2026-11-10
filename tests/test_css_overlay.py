"""Fail-closed current CSS approval and historical-source compatibility."""
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import css_overlay as css
import seo_overlay


class CSSApprovalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.approval=css.validate_current(ROOT)
        cls.temporary=tempfile.TemporaryDirectory(prefix='edb-css-approval-')
        cls.parent=Path(cls.temporary.name).resolve()
        cls.fixture=cls.parent/'repo';cls.fixture.mkdir()
        for name in [*cls.approval['files'],css.MANIFEST,css.IDENTITY]:
            target=cls.fixture/name;target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(ROOT/name,target)

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    @contextmanager
    def mutation(self,relative,transform=None,missing=False,same_mtime=False):
        path=self.fixture/relative;original=path.read_bytes();info=path.stat()
        try:
            if missing:path.unlink()
            else:
                path.write_bytes(transform(original) if transform else original+b'\nunauthorized')
                if same_mtime:os.utime(path,ns=(info.st_atime_ns,info.st_mtime_ns))
            yield
        finally:
            path.write_bytes(original);os.utime(path,ns=(info.st_atime_ns,info.st_mtime_ns))

    def rejects(self):
        with self.assertRaises((OSError,UnicodeError,ValueError)):
            css.validate_current(self.fixture)

    def test_exact_current_candidate_and_css_bytes_pass(self):
        value=css.validate_current(self.fixture)
        self.assertEqual(set(value['pilot_pages']),css.PILOT)
        self.assertEqual(len(value['site_html_paths']),92)
        asset=value['css_asset']
        self.assertEqual(hashlib.sha256((self.fixture/asset['path']).read_bytes()).hexdigest(),asset['sha256'])

    def test_every_approved_transformation_reconstructs_actual_git_main(self):
        for name,item in self.approval['transformations'].items():
            with self.subTest(path=name):
                current=(ROOT/name).read_bytes().decode('utf-8')
                old=subprocess.check_output(['git','show',css.BASE_REVISION+':'+name],cwd=ROOT).decode('utf-8')
                projected=css._project(self.approval,name,current)
                self.assertEqual(css.normalize(projected),css.normalize(old))
                self.assertEqual(css.digest(projected),item['previous_sha256'])

    def test_current_seven_pages_chain_through_unchanged_seo_manifest(self):
        for name in css.PILOT:
            current=(ROOT/name).read_bytes().decode('utf-8')
            projected=css.historical_source(ROOT,name,current)
            self.assertEqual(css.digest(projected),seo_overlay.manifest(ROOT)['pages'][name]['previous_sha256'])

    def test_full_closure_is_required_before_any_historical_projection(self):
        current=(self.fixture/'index.html').read_text(encoding='utf-8')
        with self.mutation(self.approval['css_asset']['path']):
            with self.assertRaises(ValueError):css.historical_source(self.fixture,'index.html',current)

    def test_old_baseline_is_not_approved_as_current_static_css(self):
        old=subprocess.check_output(['git','show',css.BASE_REVISION+':index.html'],cwd=ROOT).decode()
        with self.assertRaises(ValueError):css.pre_css_source(self.fixture,'index.html',old)

    def test_missing_stylesheet_link_is_rejected(self):
        tag=self.approval['transformations']['index.html']['stylesheet_tag'].encode()
        with self.mutation('index.html',lambda raw:raw.replace(tag,b'')):self.rejects()

    def test_wrong_stylesheet_is_rejected(self):
        filename=self.approval['css_asset']['path'].encode()
        with self.mutation('index.html',lambda raw:raw.replace(filename,b'assets/css/wrong.css')):self.rejects()

    def test_duplicate_stylesheet_is_rejected(self):
        tag=self.approval['transformations']['index.html']['stylesheet_tag'].encode()
        with self.mutation('index.html',lambda raw:raw.replace(tag,tag+tag)):self.rejects()

    def test_retained_or_duplicate_browser_compiler_is_rejected(self):
        script=b'<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>'
        for count in (1,2):
            with self.mutation('index.html',lambda raw:raw.replace(b'</head>',script*count+b'</head>')):self.rejects()

    def test_stylesheet_moved_outside_head_is_rejected(self):
        tag=self.approval['transformations']['index.html']['stylesheet_tag'].encode()
        with self.mutation('index.html',lambda raw:raw.replace(tag,b'').replace(b'</body>',tag+b'</body>')):self.rejects()

    def test_css_asset_missing_changed_and_same_mtime_tamper_fail(self):
        asset=self.approval['css_asset']['path']
        with self.mutation(asset,missing=True):self.rejects()
        with self.mutation(asset):self.rejects()
        with self.mutation(asset,lambda raw:b'X'+raw[1:],same_mtime=True):self.rejects()

    def test_css_asset_crlf_change_is_not_source_normalization(self):
        asset=self.approval['css_asset']['path']
        self.assertEqual(self.approval['files'][asset]['normalization'],'bytes')
        with self.mutation(asset,lambda raw:raw.replace(b'\n',b'\r\n')):self.rejects()
        with self.mutation('.gitattributes'):self.rejects()

    def test_canonical_body_and_tool_logic_mutations_fail(self):
        for transform in [lambda raw:raw.replace(b'rel="canonical"',b'rel="alternate"',1),
                          lambda raw:raw.replace(b'</body>',b'<p>unapproved</p></body>',1),
                          lambda raw:raw.replace(b'JSON.parse',b'JSON.stringify',1)]:
            with self.mutation('json-formatter/index.html',transform):self.rejects()

    def test_consent_asset_and_loader_changes_fail(self):
        with self.mutation('assets/consent.js'):self.rejects()
        with self.mutation('csv-viewer/index.html',lambda raw:raw.replace(b'assets/consent.js',b'assets/other.js')):self.rejects()

    def test_historical_evidence_and_frozen_projectors_remain_bound(self):
        for relative in ['audit/SEO_TASK_2A_SOURCE_OVERLAY.json','audit/TASK_17_CANDIDATE.json','audit/BASELINE_VERIFICATION.json','scripts/seo_overlay.py','scripts/seo-overlay.mjs','scripts/consent_overlay.py']:
            with self.subTest(path=relative),self.mutation(relative):self.rejects()

    def test_manifest_tamper_or_missing_manifest_is_not_an_approval(self):
        with self.mutation(css.MANIFEST):self.rejects()
        with self.mutation(css.MANIFEST,missing=True):self.rejects()
        with self.mutation(css.IDENTITY):self.rejects()

    def test_build_lock_scanner_test_and_ci_inputs_are_bound(self):
        for relative in ['scripts/styles/package-lock.json','scripts/styles/package.json','styles/sources.json','styles/tailwind.input.css','styles/build-manifest.json','scripts/build_styles.mjs','scripts/css_overlay.py','scripts/css-overlay.mjs','tests/test_css_overlay.py','.github/workflows/functional-ci.yml','scripts/ci/run.py','scripts/ci/coverage.json']:
            with self.subTest(path=relative),self.mutation(relative):self.rejects()

    def test_unmigrated_social_counter_cannot_become_a_consumer(self):
        tag=self.approval['transformations']['text-cleaner/index.html']['stylesheet_tag'].encode()
        with self.mutation('social-counter/index.html',lambda raw:raw.replace(b'</head>',tag+b'</head>')):self.rejects()

    def test_new_unapproved_route_is_rejected(self):
        directory=self.fixture/'unapproved-route';directory.mkdir()
        try:
            for name in ['index.html','index.htm']:
                (directory/name).write_text('<!doctype html><title>Unapproved</title>',encoding='utf-8')
                self.rejects()
                (directory/name).unlink()
        finally:
            directory.rmdir()

    def test_nested_generated_directory_names_cannot_hide_html(self):
        parent=self.fixture/'unexpected-route';parent.mkdir()
        try:
            for name in ['reports','development','node_modules','__pycache__','.git']:
                directory=parent/name;directory.mkdir()
                try:
                    (directory/'index.html').write_text('<title>Unapproved</title>',encoding='utf-8')
                    self.rejects()
                finally:
                    (directory/'index.html').unlink();directory.rmdir()
        finally:parent.rmdir()

    def test_traversal_absolute_url_and_encoded_paths_are_rejected(self):
        for relative in ['../outside','/index.html','C:/outside','index.html/../privacy.html','assets\\consent.js','https://example.com/a','%2e%2e/outside']:
            with self.subTest(path=relative),self.assertRaises(ValueError):css.safe_file(self.fixture,relative)

    def test_symlink_or_windows_junction_is_rejected_without_following(self):
        outside=self.parent/'outside';outside.mkdir(exist_ok=True)
        (outside/'file.txt').write_text('unchanged external fixture',encoding='utf-8')
        link=self.fixture/'linked-directory'
        if os.name=='nt':
            result=subprocess.run(['cmd','/c','mklink','/J',str(link),str(outside)],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        else:link.symlink_to(outside,target_is_directory=True)
        try:
            with self.assertRaises(ValueError):css.safe_file(self.fixture,'linked-directory/file.txt')
            self.rejects()
            self.assertEqual((outside/'file.txt').read_text(),'unchanged external fixture')
        finally:
            if os.name=='nt':link.rmdir()
            else:link.unlink()

    def test_security_report_successor_and_original_evidence_remain_bound(self):
        self.assertEqual(self.approval['security_report_parent_revision'], 'eec8027b7b4c293fd4ce9e5dfd4a2bb490d61b20')
        for name in ['_publishing/SEO_TASK_2E4_OUTPUT_POLICY.json', '_publishing/SEO_TASK_2E4_SCOPE.json',
                     '_publishing/SEO_TASK_2E4_PHASE_B.md', '_publishing/SEO_TASK_2E3_SOURCE_APPROVAL.json',
                     'scripts/_phase_a_publishing_approval_identity.py',
                     'audit/TASK_21_SECURITY_REVIEW.json', 'audit/TASK_22_SECURITY_REVIEW.json']:
            with self.subTest(path=name), self.mutation(name):
                self.rejects()

    def test_readme_successor_and_frozen_two_report_approval_remain_bound(self):
        self.assertEqual(self.approval['readme_parent_revision'], 'e907ae793525ab6c6a45bad5b2e19eab10f0c657')
        for name in ['_publishing/SEO_TASK_2E5_OUTPUT_POLICY.json', '_publishing/SEO_TASK_2E5_SCOPE.json',
                     '_publishing/SEO_TASK_2E5_PHASE_B.txt', '_publishing/SEO_TASK_2E4_SOURCE_APPROVAL.json',
                     'scripts/_privacy_publishing_approval_identity.py', css.MANIFEST, css.IDENTITY,
                     'README.md', 'youtube-title-checker/README.md']:
            with self.subTest(path=name), self.mutation(name):
                self.rejects()

    def test_lf_crlf_projection_preserves_trailing_bytes(self):
        name='index.html';source=css.normalize((ROOT/name).read_bytes().decode())
        for candidate in [source,source.replace('\n','\r\n')]:
            old=css.pre_css_source(ROOT,name,candidate)
            self.assertEqual(css.digest(old),self.approval['transformations'][name]['previous_sha256'])
            with self.assertRaises(ValueError):css.pre_css_source(ROOT,name,candidate+' ')

    def test_six_tool_candidates_bind_historical_registry_evidence(self):
        registry=json.loads((ROOT/'TOOL_REGISTRY.json').read_text(encoding='utf-8'))
        selected=[t for t in registry['tools'] if t['directory_path']+'/index.html' in css.PILOT]
        self.assertEqual(len(selected),6)
        for tool in selected:
            source=(ROOT/tool['directory_path']/'index.html').read_text(encoding='utf-8')
            self.assertTrue(css.valid_candidate(ROOT,tool,source))
            self.assertFalse(css.valid_candidate(ROOT,tool,source+' '))
            wrong={**tool,'verification':{**tool['verification'],'source_sha256':'0'*64}}
            self.assertFalse(css.valid_candidate(ROOT,wrong,source))

    def test_generic_historical_fixture_is_not_reinterpreted(self):
        with tempfile.TemporaryDirectory(prefix='edb-css-generic-') as temp:
            self.assertEqual(css.historical_source(Path(temp),'sample.txt','untouched\r\n '),'untouched\r\n ')

    def test_snapshot_captures_verified_bytes_without_caching_live_approval(self):
        source=(self.fixture/'index.html').read_text(encoding='utf-8')
        reader,byte_reader=css.historical_snapshot(self.fixture)
        expected=reader(self.fixture,'index.html',source)
        with self.mutation(self.approval['css_asset']['path']):
            self.assertEqual(reader(self.fixture,'index.html',source),expected)
            self.assertEqual(byte_reader(self.fixture,'index.html',source.encode()),expected.encode())
            self.rejects()
            with self.assertRaises(ValueError):css.historical_snapshot(self.fixture)
            with self.assertRaises(ValueError):css.historical_source(self.fixture,'index.html',source)

    def test_snapshot_rejects_unbound_root_path_and_source(self):
        reader,byte_reader=css.historical_snapshot(self.fixture)
        source=(self.fixture/'index.html').read_text(encoding='utf-8')
        for root,path,text in [(ROOT,'index.html',source),(self.fixture,'unknown.html',source),(self.fixture,'index.html',source+' ')]:
            with self.assertRaises(ValueError):reader(root,path,text)
        asset=self.approval['css_asset']['path'];raw=(self.fixture/asset).read_bytes()
        with self.assertRaises(ValueError):byte_reader(self.fixture,asset,raw+b' ')
        with self.mutation(css.MANIFEST,missing=True):
            with self.assertRaises(OSError):css.historical_snapshot(self.fixture)

    def test_snapshot_rejects_frozen_projector_fallback_after_capture(self):
        # A missing old manifest can make the deliberately frozen old helper
        # return its input; it cannot silently produce incomplete new evidence.
        with patch.object(css.seo_overlay,'historical_bytes',side_effect=lambda root,path,source:source):
            with self.assertRaisesRegex(ValueError,'captured SEO evidence'):
                css.historical_snapshot(self.fixture)

    def test_candidate_snapshot_binds_six_registry_records_and_exact_sources(self):
        value,accepts=css.candidate_snapshot(self.fixture)
        registry=json.loads((self.fixture/'TOOL_REGISTRY.json').read_text(encoding='utf-8'))
        tools=[t for t in registry['tools'] if t['directory_path']+'/index.html' in css.PILOT]
        self.assertEqual(len(tools),6)
        for tool in tools:
            source=(self.fixture/tool['directory_path']/'index.html').read_text(encoding='utf-8')
            self.assertTrue(accepts(self.fixture,tool,source))
            self.assertFalse(accepts(ROOT,tool,source))
            self.assertFalse(accepts(self.fixture,tool,source+' '))
            self.assertFalse(accepts(self.fixture,{**tool,'id':'unbound'},source))
        with self.mutation(value['css_asset']['path']):
            self.assertTrue(accepts(self.fixture,tools[-1],source))
            self.rejects()
            with self.assertRaises(ValueError):css.candidate_snapshot(self.fixture)

    def test_project_revalidates_live_closure_after_candidate_snapshot(self):
        import tracking
        asset=self.fixture/self.approval['css_asset']['path'];original=asset.read_bytes()
        def capture_then_mutate(root):
            result=css.candidate_snapshot(root)
            asset.write_bytes(original+b' ')
            return result
        try:
            with patch.object(tracking,'css_candidate_snapshot',side_effect=capture_then_mutate):
                result=tracking.check_project(self.fixture)
            self.assertEqual(result['details']['css_source_approval']['status'],'FAIL')
            self.assertIn('CSS_SOURCE_APPROVAL',{item['code'] for item in result['errors']})
        finally:asset.write_bytes(original)


if __name__=='__main__':unittest.main()
