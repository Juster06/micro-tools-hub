"""Reconstruct the verified Task 24 state after checking the six Task 25 records."""
from pathlib import Path
from functools import lru_cache
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = '3e6b3d256d731cacdac8d6098937e2a5a9ba1378'
DEPLOYMENT = 'c127f856cbd97497412ec35ed66b3b1a58c4b2dc'
IDS = frozenset({
    'word-frequency-analyzer', 'unicode-inspector', 'ipv4-subnet-calculator',
    'batch-filename-planner', 'file-byte-comparator', 'css-gradient-generator',
})
JOBS = {'structural_job': 'python-project', 'logic_job': 'node-regression', 'browser_job': 'browser-tests'}


def normalized(data):
    return data.replace(b'\r\n', b'\n')


@lru_cache(maxsize=None)
def git_blob(path, revision=BASE):
    return subprocess.check_output(['git', 'show', revision + ':' + path], cwd=ROOT)


def registry_before_task25(registry):
    added = [tool for tool in registry['tools'] if tool['id'] in IDS]
    if not added:
        return registry
    assert len(registry['tools']) == 105 and len(added) == 6 and {t['id'] for t in added} == IDS
    for tool in added:
        tid = tool['id']
        path = tid + '/index.html'
        assert tool['directory_path'] == tid and tool['status'] == 'RELEASED' and tool['testing_status'] == 'REQUIRED_PASSED'
        verification = tool['verification']
        publication = verification['publication']
        assert publication['url'] == 'https://everydaydigitalbox.com/' + tid + '/'
        assert publication['http_status'] == 200 and publication['source_matches'] is True
        revision = verification['source_revision']
        assert revision == DEPLOYMENT
        expected = normalized(git_blob(path, revision)).rstrip()
        assert normalized((ROOT / path).read_bytes()).rstrip() == expected
        assert hashlib.sha256(expected).hexdigest() == verification['source_sha256']
        audit_prefix = 'audit/' + tid.upper().replace('-', '_')
        expected_audit = audit_prefix + '_RELEASE_VERIFICATION.json'
        assert verification['evidence_path'] == expected_audit
        audit = json.loads((ROOT / expected_audit).read_text(encoding='utf-8'))
        assert audit['result'] == 'PASS' and audit['source_revision'] == revision
        assert audit['verified_on'] == tool['last_verification_date']
        assert audit['pages'][0]['path'] == path and audit['pages'][0]['publication'] == publication == audit['publication']
        assert audit['pages'][0]['source_sha256'] == verification['source_sha256']
        assert audit['public_index']['raw_match'] is True and audit['canonical_public_url']['raw_match'] is True
        assert audit['public_source_sha256'] == audit['approved_source_sha256'] == hashlib.sha256(git_blob(path, revision)).hexdigest()
        assert len(audit['public_browser_checks']) >= 6 and all(row['result'] == 'PASS' for row in audit['public_browser_checks'])
        assert audit['previous_evidence'] == audit_prefix + '_VERIFICATION.json'
        previous = json.loads((ROOT / audit['previous_evidence']).read_text(encoding='utf-8'))
        assert previous['result'] == 'PASS' and previous['pages'][0]['publication'] is None
        assert all(audit['automated_tool_report']['layers'][layer]['status'] == 'PASS' for layer in ('structural','logic','browser'))
    return {**registry, 'tools': [tool for tool in registry['tools'] if tool['id'] not in IDS]}


def homepage_before_task25(source, Homepage):
    home = Homepage(source)
    cards = [card for card in home.cards if card['attrs'].get('data-tool-id') in IDS]
    if not cards:
        return source
    assert len(home.cards) == 87 and len(cards) == 6 and {c['attrs']['data-tool-id'] for c in cards} == IDS
    start, end = home.counts[0]
    assert source[start:end] == '87 tools ready to use'
    for card in sorted(cards, key=lambda item: item['start'], reverse=True):
        attrs = card['attrs']
        assert attrs['href'] == attrs['data-tool-id'] + '/index.html' and attrs['data-availability'] == 'released'
        assert source[card['start']:card['end']].count('Live') == 1
        assert source[card['start'] - 2:card['start']] == '  ' and source[card['end']:card['end'] + 7] == '\n      '
        source = source[:card['start'] - 2] + source[card['end'] + 7:]
    return source[:start] + '81 tools ready to use' + source[end:]


def tool_map_before_task25(coverage):
    tools = coverage['tools']
    assert len(tools) == 87 and all(tools.get(tid) == JOBS for tid in IDS)
    return {tid: jobs for tid, jobs in tools.items() if tid not in IDS}
