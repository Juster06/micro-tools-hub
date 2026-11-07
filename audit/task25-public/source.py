from pathlib import Path
from datetime import datetime,timezone
from html.parser import HTMLParser
import concurrent.futures,hashlib,json,os,subprocess,urllib.request
OUT=Path(__file__).resolve().parent;REPO=Path(os.environ.get('EDB_REPO_ROOT',OUT.parents[1]));COMMIT='c127f856cbd97497412ec35ed66b3b1a58c4b2dc';REVIEW=COMMIT;ORIGIN='https://everydaydigitalbox.com/'
IDS=['word-frequency-analyzer', 'unicode-inspector', 'ipv4-subnet-calculator', 'batch-filename-planner', 'file-byte-comparator', 'css-gradient-generator']
def git(*args):return subprocess.check_output(['git',*args],cwd=REPO,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'})
def blob(p):return git('show',REVIEW+':'+p)
def sha(b):return hashlib.sha256(b).hexdigest()
def normalized(b):return sha(b.decode('utf-8').replace('\r\n','\n').rstrip().encode())
def save(p,a):p.write_text(json.dumps(a,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
class Page(HTMLParser):
 def __init__(self,text):super().__init__();self.cards=[];self.scripts=[];self.title='';self.in_title=False;self.feed(text)
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t=='title':self.in_title=True
  if t=='a'and a.get('data-title'):self.cards.append(a)
  if t=='script'and a.get('src'):self.scripts.append(a['src'])
 def handle_endtag(self,t):
  if t=='title':self.in_title=False
 def handle_data(self,text):
  if self.in_title:self.title+=text
registry=json.loads(blob('TOOL_REGISTRY.json'));tools=[t for t in registry['tools']if t['status']in ['TESTED','RELEASED']]
def check(path,url=None):
 url=url or ORIGIN+path;expected=blob(path);stamp=datetime.now(timezone.utc).isoformat();req=urllib.request.Request(url,headers={'User-Agent':'EverydayDigitalBox-OwnerReleaseVerification/25.1','Cache-Control':'no-cache'})
 with urllib.request.urlopen(req,timeout=40)as r:actual=r.read(max(len(expected)+1024,1024*1024));status=r.status;final=r.url;kind=r.headers.get('Content-Type','')
 entry={'url':url,'final_url':final,'checked_at':stamp,'http_status':status,'raw_public_sha256':sha(actual),'raw_approved_sha256':sha(expected),'raw_match':actual==expected,'source_sha256':normalized(actual),'approved_normalized_sha256':normalized(expected),'content_type':kind}
 assert status==200 and actual==expected,(path,entry)
 if path.endswith('.html'):
  page=Page(actual.decode('utf-8'));entry.update(title=page.title,scripts=page.scripts);assert page.title==Page(expected.decode('utf-8')).title
  if path.split('/')[0]in IDS:
   tool=next(t for t in tools if t['id']==path.split('/')[0]);assert tool['name']in page.title
   assert page.scripts==['https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4','../assets/consent.js']
 (OUT/'public-source').mkdir(exist_ok=True);(OUT/'public-source'/path.replace('/','__')).write_bytes(actual);return path,entry
if __name__=='__main__':
 save(OUT/'approved-registry.json',registry)
 assert len(tools)==87 and sum(t['status']=='RELEASED'for t in tools)==81
 paths=['index.html','privacy.html','TOOL_REGISTRY.json','PROGRESS_TRACKER.md']+git('ls-tree','-r','--name-only',REVIEW,'assets').decode().splitlines()+[t['directory_path']+'/index.html'for t in tools]
 result={'result':'IN_PROGRESS','deployment_commit':COMMIT,'source_tree_sha':git('rev-parse',REVIEW+'^{tree}').decode().strip(),'pages_run':42338516265,'post_merge_ci_run':42338516503,'sources':{},'canonical':{}}
 try:
  with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:
   for path,entry in pool.map(check,paths):result['sources'][path]=entry
  for tid in IDS:result['canonical'][tid]=check(tid+'/index.html',ORIGIN+tid+'/')[1]
  home=Page((OUT/'public-source/index.html').read_text(encoding='utf-8'));routes=sorted(c['href']for c in home.cards);assert len(home.cards)==len(set(routes))==87;assert routes==sorted(t['directory_path']+'/index.html'for t in tools)
  result['homepage_root']=check('index.html',ORIGIN)[1]
  assert blob('CNAME').decode().strip()=='everydaydigitalbox.com';assert b'G-XDHPQYJ5CH'in(OUT/'public-source/assets__consent.js').read_bytes()
  counts={s:sum(t['status']==s for t in registry['tools'])for s in ['RELEASED','TESTED','READY','PLANNED','BLOCKED']};assert counts=={'RELEASED':81,'TESTED':6,'READY':0,'PLANNED':17,'BLOCKED':1}
  result.update(result='PASS',completed_at=datetime.now(timezone.utc).isoformat(),registry=counts,homepage={'cards':87,'distinct':87,'routes':routes,'canonical_routes_match':True,'custom_domain':'everydaydigitalbox.com'})
 except Exception as e:result.update(result='FAIL',error=str(e));raise
 finally:save(OUT/'public-source-verification.json',result)
 print(json.dumps({'result':result['result'],'source_responses':len(result['sources']),'directory_responses':6,'pages':87,'all_byte_identical':True}))
