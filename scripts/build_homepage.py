"""Deterministic Option B homepage, using reviewed presentation data only."""
from pathlib import Path
import argparse,hashlib,html,json
ROOT=Path(__file__).resolve().parents[1]
def digest(b):return hashlib.sha256(b).hexdigest()
def esc(s):return html.escape(s,quote=True)
def generate(root=ROOT,check=False):
    mapping=json.loads((root/'styles/homepage-directory.json').read_text(encoding='utf-8'))
    tools={t['id']:t for t in mapping['tools']}
    registry=json.loads((root/'TOOL_REGISTRY.json').read_text(encoding='utf-8'))
    released={t['id']:t for t in registry['tools'] if t['status']=='RELEASED'}
    ids=[i for c in mapping['categories'] for i in c['tool_ids']]
    if len(ids)!=87 or len(set(ids))!=87 or set(ids)!=set(released) or set(tools)!=set(released):raise ValueError('Directory must contain exactly the 87 released tools')
    for key,t in tools.items():
        if t['directory_path_unchanged']!=released[key]['directory_path'] or t['canonical_url']!='https://everydaydigitalbox.com/'+released[key]['directory_path']+'/index.html':raise ValueError('Directory route changed')
    css=(root/'styles/homepage.css').read_text(encoding='utf-8').replace('\r\n','\n').encode()
    if b'@import' in css or b'url(' in css:raise ValueError('Homepage CSS must have no external dependency')
    asset='assets/css/homepage.'+digest(css)[:16]+'.css'
    shared=json.loads((root/'styles/build-manifest.json').read_text(encoding='utf-8'))['output']['path']
    buttons='<button type="button" data-category-filter="all" aria-pressed="true">All tools</button>'
    options='<option value="all">All categories</option>';anchors='';groups=''
    for c in mapping['categories']:
        key=c['id'];label=esc(c['label'])
        buttons+=f'<button type="button" data-category-filter="{key}" aria-pressed="false">{label}</button>'
        options+=f'<option value="{key}">{label}</option>'
        anchors+=f'<a href="#category-{key}" data-category-jump="{key}">{label}</a>'
        cards=''
        for tid in c['tool_ids']:
            t=tools[tid];search=' '.join([t['name'],t['description_from_registry'],*t['proposed_search_aliases']])
            cards+=f'''<a class="tool-card" data-title="{esc(t['name'])}" data-tool-id="{tid}" data-category="{key}" data-availability="released" data-search="{esc(search)}" href="{t['directory_path_unchanged']}/index.html" aria-labelledby="tool-{tid}-title"><small class="category-label">{label} · Live</small> <h4 id="tool-{tid}-title">{esc(t['name'])}</h4> <p>{esc(t['description_from_registry'])}</p> <span class="open-label">Open tool <span aria-hidden="true">→</span></span></a>\n'''
        groups+=f'<section class="tool-group" id="category-{key}" data-group="{key}" aria-labelledby="heading-{key}"><h3 id="heading-{key}">{label} <span class="muted">({len(c["tool_ids"])})</span></h3><div class="tool-grid">{cards}</div></section>\n'
    script=(root/'styles/homepage.js').read_text(encoding='utf-8').replace('\r\n','\n')
    source=f'''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="canonical" href="https://everydaydigitalbox.com/index.html">
<meta name="google-site-verification" content="r9GLjYMnOsZvdykkVFgNMltev3zV4XCy54VhGQO87f0" />
<meta name="color-scheme" content="light">
<meta name="description" content="Everyday Digital Box: 87 free utilities for text, CSV, code, images, calculations and everyday tasks. Find a tool by name, category or task.">
<title>Everyday Digital Box — Useful tools for everyday tasks</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 48 48'%3E%3Crect width='48' height='48' rx='10' fill='%230F2742'/%3E%3Cpath d='M12 12h24v24H12z' fill='none' stroke='%23fff' stroke-width='3'/%3E%3C/svg%3E">
<link rel="stylesheet" href="{shared}">
<link rel="stylesheet" href="{asset}">
<script defer src="assets/consent.js"></script></head>
<body class="homepage">
<a class="skip" href="#main">Skip to main content</a>
<header class="site-header"><div class="container header-inner"><a class="brand" href="index.html" aria-label="Everyday Digital Box home"><span class="brand-mark" aria-hidden="true"></span><span>Everyday<br>Digital Box</span></a><button class="mobile-menu js-control" id="menu" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button><nav id="site-nav" class="site-nav" aria-label="Primary"><a href="#tools">All Tools</a><a href="#categories">Categories</a><a href="privacy.html">Privacy</a></nav></div></header>
<main id="main" class="container" tabindex="-1"><section class="hero" aria-labelledby="home-title"><h1 id="home-title">Useful tools for everyday tasks.</h1><p>Work with text, data, images and numbers. Choose a task and get started without an account.</p>
<div class="search-area js-control"><label for="toolSearch">Find a tool</label><div class="search-row"><input id="toolSearch" type="search" placeholder="Try format JSON or resize image" aria-describedby="search-help" autocomplete="off"><button id="clearSearch" type="button">Clear</button></div><small id="search-help" class="search-help">Search names, descriptions and common tasks. Searches stay in this page.</small></div>
<div id="categories" tabindex="-1"><div class="category-controls js-control" role="group" aria-label="Filter tools by category">{buttons}</div><div class="mobile-category js-control"><label for="category-select">Category</label><select id="category-select">{options}</select></div><details class="category-jumps"><summary>Browse all eight categories</summary>{anchors}</details></div></section>
<section id="tools" tabindex="-1" aria-labelledby="directory-title"><div class="section-heading"><h2 id="directory-title">All tools</h2><p id="resultCount" class="muted" role="status" aria-live="polite" aria-atomic="true">87 tools ready to use</p></div><div id="empty" class="empty" hidden><h3>No matching tools</h3><p>Try a shorter term or clear the search and category filter.</p><button id="reset-results" type="button">Show all tools</button></div><div id="toolGrid">{groups}</div></section>
<section class="trust" aria-labelledby="privacy-heading"><h2 id="privacy-heading">Your tasks, your choice.</h2><p>Tools process your inputs in your browser. Hosting requests still occur, and some tools link to external services. Analytics is optional; the tools work whether you accept or reject it. <a href="privacy.html">Read our privacy and cookie policy.</a></p></section></main>
<footer class="site-footer"><div class="container row"><p>Everyday Digital Box</p><a href="#tools">All Tools</a><a href="privacy.html">Privacy</a><a href="https://github.com/Juster06/micro-tools-hub">Source on GitHub</a></div></footer>
<script>{script}</script></body></html>
'''
    for path,data in [(asset,css),('index.html',source.encode())]:
        p=root/path
        if check:
            actual=p.read_bytes() if path.endswith('.css') else p.read_text(encoding='utf-8').replace('\r\n','\n').encode()
            if actual!=data:raise ValueError('Stale homepage output: '+path)
        else:p.write_bytes(data)
    return {'status':'PASS','tools':87,'categories':8,'asset':asset,'css_sha256':digest(css),'css_bytes':len(css),'source_sha256':digest(source.encode())}
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    print(json.dumps(generate(check=args.check),indent=2))
