import hashlib,json,subprocess,sys,tempfile,unittest,shutil
from pathlib import Path
from html.parser import HTMLParser
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import css_overlay as approval
from build_homepage import generate
from git_fixtures import git_blob, close_readers
class Directory(HTMLParser):
    def __init__(self):super().__init__();self.cards=[];self.groups=[];self.links=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'data-title' in a:self.cards.append(a)
        if 'data-group' in a:self.groups.append(a['data-group'])
        if tag=='link':self.links.append(a)
class HomepageTests(unittest.TestCase):
    def test_reproducible_generated_homepage(self):self.assertEqual(generate(check=True)['tools'],87)
    def test_complete_unique_released_directory_and_category_mapping(self):
        parser=Directory();parser.feed((ROOT/'index.html').read_text(encoding='utf-8'))
        mapping=json.loads((ROOT/'styles/homepage-directory.json').read_text(encoding='utf-8'))
        registry=json.loads((ROOT/'TOOL_REGISTRY.json').read_text(encoding='utf-8'))
        released={x['id']:x for x in registry['tools'] if x['status']=='RELEASED'}
        self.assertEqual(len(parser.cards),87);self.assertEqual({c['data-tool-id'] for c in parser.cards},set(released))
        self.assertEqual(len(parser.groups),8)
        for group in mapping['categories']:
            self.assertEqual({c['data-tool-id'] for c in parser.cards if c['data-category']==group['id']},set(group['tool_ids']))
        for card in parser.cards:self.assertEqual(card['href'],released[card['data-tool-id']]['directory_path']+'/index.html')
    def test_all_frozen_audits_registry_consent_seo_are_identical_to_parent(self):
        self.addCleanup(close_readers)
        names=subprocess.check_output(['git','ls-tree','-r','--name-only','20ecae29a1f20d7903946d6cf00c3897307ee766','audit'],cwd=ROOT,text=True).splitlines()
        names+=['TOOL_REGISTRY.json','assets/consent.js','privacy.html','sitemap.xml','robots.txt','CNAME','scripts/seo_overlay.py','scripts/seo-overlay.mjs','scripts/consent_overlay.py','scripts/css_approval_identity.py']
        # One read-only batch, immutable objects; checkout LF normalization only.
        for name in names:
            old=git_blob(ROOT,'20ecae29a1f20d7903946d6cf00c3897307ee766',name)
            self.assertEqual((ROOT/name).read_bytes().replace(b'\r\n',b'\n'),old.replace(b'\r\n',b'\n'),name)
    def test_historical_comparison_rejects_disposable_tampering_and_accepts_restoration(self):
        revision='20ecae29a1f20d7903946d6cf00c3897307ee766'
        names=subprocess.check_output(['git','ls-tree','-r','--name-only',revision,'audit'],cwd=ROOT,text=True).splitlines()
        names+=['TOOL_REGISTRY.json','assets/consent.js','privacy.html','sitemap.xml','robots.txt','CNAME','scripts/seo_overlay.py','scripts/seo-overlay.mjs','scripts/consent_overlay.py','scripts/css_approval_identity.py']
        self.assertEqual(len(names),266)
        with tempfile.TemporaryDirectory(prefix='edb-homepage-history-control-') as temporary:
            root=Path(temporary)/'repository'
            subprocess.run(['git','clone','--shared','--no-checkout','--quiet',str(ROOT),str(root)],check=True,capture_output=True,timeout=30)
            for name in names:
                target=root/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((ROOT/name).read_bytes())
            probe=HomepageTests('test_all_frozen_audits_registry_consent_seo_are_identical_to_parent')
            expected=[((root,revision,name),{}) for name in names]
            try:
                with patch(__name__+'.ROOT',root),patch(__name__+'.git_blob',wraps=git_blob) as reads:
                    probe.test_all_frozen_audits_registry_consent_seo_are_identical_to_parent()
                    self.assertEqual(reads.call_args_list,expected)
                    target=root/names[-1];original=target.read_bytes()
                    try:
                        target.write_bytes(original+b' unauthorized change')
                        reads.reset_mock()
                        with self.assertRaises(AssertionError):
                            probe.test_all_frozen_audits_registry_consent_seo_are_identical_to_parent()
                        self.assertEqual(reads.call_args_list,expected)
                    finally:
                        target.write_bytes(original)
                    reads.reset_mock()
                    probe.test_all_frozen_audits_registry_consent_seo_are_identical_to_parent()
                    self.assertEqual(reads.call_args_list,expected)
            finally:
                probe.doCleanups()
    def test_new_approval_dependencies_fail_closed(self):
        value=approval.validate_current(ROOT)
        with tempfile.TemporaryDirectory(prefix='edb-homepage-approval-') as temp:
            root=Path(temp)
            for name in [*value['files'],approval.MANIFEST,approval.IDENTITY]:
                p=root/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,p)
            for name in ['index.html',value['homepage_asset'],'styles/homepage.css','styles/homepage.js','styles/homepage-directory.json','scripts/build_homepage.py',approval.MANIFEST,approval.IDENTITY,'audit/SEO_TASK_2C_SOURCE_APPROVAL.json']:
                p=root/name;raw=p.read_bytes()
                try:
                    p.write_bytes(raw+b' ')
                    with self.assertRaises((ValueError,OSError)):approval.validate_current(root)
                finally:p.write_bytes(raw)
            self.assertEqual(approval.validate_current(root)['parent_revision'],'20ecae29a1f20d7903946d6cf00c3897307ee766')
