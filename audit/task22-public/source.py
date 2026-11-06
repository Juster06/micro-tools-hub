"""Fresh actual HTTPS byte identity for the approved deployed Git source."""
from pathlib import Path
from datetime import datetime,timezone
from html.parser import HTMLParser
import concurrent.futures,hashlib,json,os,subprocess,urllib.request
OUT=Path(__file__).resolve().parent;REPO=Path(os.environ.get('EDB_REPO_ROOT',OUT.parent/'task22'));COMMIT='64a19c6bc1ee2dfbd81cf9ffa6b1ca00f15c8140';ORIGIN='https://everydaydigitalbox.com/';ID='markdown-converter-previewer'
def git(*args):return subprocess.check_output(['git',*args],cwd=REPO,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'})
def blob(p):return git('show',COMMIT+':'+p)
def sha(b):return hashlib.sha256(b).hexdigest()
def normalized(b):return sha(b.decode('utf-8').replace('\r\n','\n').rstrip().encode())
def save(p,a):p.write_text(json.dumps(a,indent=2)+'\n',encoding='utf-8',newline='\n')
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
 url=url or ORIGIN+path;expected=blob(path);req=urllib.request.Request(url,headers={'User-Agent':'EverydayDigitalBox-OwnerReleaseVerification/22.1','Cache-Control':'no-cache'});stamp=datetime.now(timezone.utc).isoformat()
 with urllib.request.urlopen(req,timeout=40)as response:actual=response.read(max(len(expected)+1024,1024*1024));status=response.status;final=response.url;kind=response.headers.get('Content-Type','')
 entry={'url':url,'final_url':final,'checked_at':stamp,'http_status':status,'raw_public_sha256':sha(actual),'raw_approved_sha256':sha(expected),'raw_match':actual==expected,'source_sha256':normalized(actual),'approved_normalized_sha256':normalized(expected),'content_type':kind}
 assert status==200 and actual==expected,(path,entry)
 if path.endswith('.html'):
  page=Page(actual.decode('utf-8'));entry.update(title=page.title,scripts=page.scripts);assert page.title==Page(expected.decode('utf-8')).title
  if path==ID+'/index.html':assert page.scripts==['https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4','../assets/consent.js','../assets/vendor/task22/markdown-source.js'];assert 'Markdown Converter & Previewer'in page.title
 (OUT/'public-source').mkdir(exist_ok=True);(OUT/'public-source'/path.replace('/','__')).write_bytes(actual);return path,entry
if __name__=='__main__':
 assert len(tools)==75 and sum(t['status']=='RELEASED'for t in tools)==74
 paths=['index.html','privacy.html','TOOL_REGISTRY.json','PROGRESS_TRACKER.md']+git('ls-tree','-r','--name-only',COMMIT,'assets').decode().splitlines()+[t['directory_path']+'/index.html'for t in tools]
 result={'result':'IN_PROGRESS','deployment_commit':COMMIT,'source_tree_sha':git('rev-parse',COMMIT+'^{tree}').decode().strip(),'pages_run':42205116968,'post_merge_ci_run':42205117641,'sources':{},'canonical':{}}
 try:
  with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:
   for path,entry in pool.map(check,paths):result['sources'][path]=entry
  result['canonical'][ID]=check(ID+'/index.html',ORIGIN+ID+'/')[1]
  page=Page((OUT/'public-source/index.html').read_text(encoding='utf-8'));routes=sorted(c['href']for c in page.cards);assert len(page.cards)==len(set(routes))==75;assert routes==sorted(t['directory_path']+'/index.html'for t in tools)
  assert blob('CNAME').decode().strip()=='everydaydigitalbox.com';assert b'G-XDHPQYJ5CH'in (OUT/'public-source/assets__consent.js').read_bytes()
  deployed=json.loads((OUT/'public-source/TOOL_REGISTRY.json').read_text(encoding='utf-8'));counts={s:sum(t['status']==s for t in deployed['tools'])for s in ['RELEASED','TESTED','READY','PLANNED','BLOCKED']};assert counts=={'RELEASED':74,'TESTED':1,'READY':0,'PLANNED':17,'BLOCKED':1}
  result.update(result='PASS',completed_at=datetime.now(timezone.utc).isoformat(),registry=counts,homepage={'cards':75,'distinct':75,'routes':routes,'canonical_routes_match':True,'custom_domain':'everydaydigitalbox.com'})
 except Exception as e:result.update(result='FAIL',error=str(e));raise
 finally:save(OUT/'public-source-verification.json',result)
 print(json.dumps({'result':result['result'],'source_responses':len(result['sources']),'directory_responses':1,'pages':75,'all_byte_identical':True}))
