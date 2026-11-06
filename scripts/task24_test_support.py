"""Strictly project the six authorized Task24 additions out of older audits.

Historical baseline assertions remain exact after this checked projection. The
new Task24 preservation suite independently binds the entire 75-release baseline.
"""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
IDS={'number-base-converter','unit-converter','duration-calculator','url-inspector-query-builder','list-comparison-set-operations','color-contrast-checker'}
def historical_registry(registry):
    assert len(registry['tools'])==99
    added=[t for t in registry['tools']if t['id']in IDS]
    assert len(added)==6 and {t['id']for t in added}==IDS
    for tool in added:
        assert tool['directory_path']==tool['id']
        assert tool['status']=='TESTED' and tool['testing_status']=='REQUIRED_PASSED'
        verification=tool['verification'];assert verification['publication']is None
        source=(ROOT/tool['directory_path']/'index.html').read_text(encoding='utf-8').replace('\r\n','\n').rstrip().encode()
        assert verification['source_sha256']==hashlib.sha256(source).hexdigest()
        audit=json.loads((ROOT/verification['evidence_path']).read_text(encoding='utf-8'))
        assert audit['result']=='PASS' and audit['source_revision']==verification['source_revision']
        assert audit['pages'][0]['source_sha256']==verification['source_sha256']
        assert audit['pages'][0]['publication']is None
        assert all(audit['automated_tool_report']['layers'][layer]['status']=='PASS'for layer in ['structural','logic','browser'])
    return {**registry,'tools':[t for t in registry['tools']if t['id']not in IDS]}
def without_task24(source,Homepage):
    found=[c for c in Homepage(source).cards if c['attrs'].get('data-tool-id')in IDS]
    if not found:
        assert len(Homepage(source).cards)==75
        return source
    assert len(found)==6 and len(Homepage(source).cards)==81
    assert {c['attrs']['data-tool-id']for c in found}==IDS
    for tid in sorted(IDS):
        card=next(c for c in Homepage(source).cards if c['attrs'].get('data-tool-id')==tid)
        assert card['attrs']['href']==tid+'/index.html'
        assert card['attrs']['data-availability']=='tested'
        assert source[card['start']:card['end']].count('Tested · publication pending')==1
        assert source[card['start']-2:card['start']]=='  '
        assert source[card['end']:card['end']+7]=='\n      '
        source=source[:card['start']-2]+source[card['end']+7:]
    home=Homepage(source);start,end=home.counts[0]
    assert source[start:end]=='81 tools ready to use'
    return source[:start]+'75 tools ready to use'+source[end:]
