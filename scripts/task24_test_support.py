"""Strictly project the six authorized Task24 additions out of older audits.

Historical baseline assertions remain exact after this checked projection. The
new Task24 preservation suite independently binds the entire 75-release baseline.
"""
from pathlib import Path
import hashlib,json
from css_overlay import historical_snapshot
historical_source, historical_bytes = historical_snapshot(Path(__file__).resolve().parents[1])
from task25_test_support import homepage_before_task25, registry_before_task25
ROOT=Path(__file__).resolve().parents[1]
IDS={'number-base-converter','unit-converter','duration-calculator','url-inspector-query-builder','list-comparison-set-operations','color-contrast-checker'}
def historical_registry(registry):
    registry = registry_before_task25(registry)
    assert len(registry['tools'])==99
    added=[t for t in registry['tools']if t['id']in IDS]
    assert len(added)==6 and {t['id']for t in added}==IDS
    for tool in added:
        assert tool['directory_path']==tool['id']
        assert tool['status']=='RELEASED' and tool['testing_status']=='REQUIRED_PASSED'
        verification=tool['verification'];publication=verification['publication']
        assert verification['source_revision']=='a7da719ea6ccc4caae572f26f6ae5e707fbb70be'
        assert publication['url']=='https://everydaydigitalbox.com/'+tool['id']+'/'
        assert publication['http_status']==200 and publication['source_matches']is True
        source=historical_source(ROOT, (ROOT/tool['directory_path']/'index.html').relative_to(ROOT).as_posix(), (ROOT/tool['directory_path']/'index.html').read_text(encoding='utf-8')).replace('\r\n','\n').rstrip().encode()
        assert verification['source_sha256']==hashlib.sha256(source).hexdigest()
        audit=json.loads(historical_source(ROOT, (ROOT/verification['evidence_path']).relative_to(ROOT).as_posix(), (ROOT/verification['evidence_path']).read_text(encoding='utf-8')))
        assert audit['result']=='PASS' and audit['source_revision']==verification['source_revision']
        assert audit['pages'][0]['source_sha256']==verification['source_sha256']
        assert audit['pages'][0]['publication']==publication==audit['publication']
        assert audit['public_index']['raw_match']is True
        assert audit['public_source_sha256']==audit['approved_source_sha256']
        assert audit['canonical_public_url']['raw_match']is True
        assert audit['public_browser_checks']and all(c['result']=='PASS'for c in audit['public_browser_checks'])
        previous=json.loads(historical_source(ROOT, (ROOT/audit['previous_evidence']).relative_to(ROOT).as_posix(), (ROOT/audit['previous_evidence']).read_text(encoding='utf-8')))
        assert previous['result']=='PASS'and previous['pages'][0]['publication']is None
        assert all(audit['automated_tool_report']['layers'][layer]['status']=='PASS'for layer in ['structural','logic','browser'])
    return {**registry,'tools':[t for t in registry['tools']if t['id']not in IDS]}
def without_task24(source,Homepage):
    source = homepage_before_task25(source, Homepage)
    found=[c for c in Homepage(source).cards if c['attrs'].get('data-tool-id')in IDS]
    if not found:
        assert len(Homepage(source).cards)==75
        return source
    assert len(found)==6 and len(Homepage(source).cards)==81
    assert {c['attrs']['data-tool-id']for c in found}==IDS
    for tid in sorted(IDS):
        card=next(c for c in Homepage(source).cards if c['attrs'].get('data-tool-id')==tid)
        assert card['attrs']['href']==tid+'/index.html'
        assert card['attrs']['data-availability']=='released'
        assert source[card['start']:card['end']].count('Live')==1
        assert source[card['start']-2:card['start']]=='  '
        assert source[card['end']:card['end']+7]=='\n      '
        source=source[:card['start']-2]+source[card['end']+7:]
    home=Homepage(source);start,end=home.counts[0]
    assert source[start:end]=='81 tools ready to use'
    return source[:start]+'75 tools ready to use'+source[end:]
