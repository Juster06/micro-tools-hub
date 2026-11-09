"""Validate real Pages output against a reviewed inventory, never approve it.

The current policy retires only approved exact paths and preserves all other
production bytes. Frozen predecessor policies remain usable as test fixtures.
"""
from __future__ import annotations

import argparse
import hashlib
from html import escape
from html.parser import HTMLParser
import json
import os
from pathlib import Path, PureWindowsPath
import re
import stat
import sys
from urllib.parse import quote
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import css_overlay

POLICY = '_publishing/SEO_TASK_2E4_OUTPUT_POLICY.json'
PHASE_A_POLICY = '_publishing/SEO_TASK_2E3_OUTPUT_POLICY.json'
SECURITY_SCOPE = '_publishing/SEO_TASK_2E4_SCOPE.json'
SECURITY_CHECKPOINT = '_publishing/SEO_TASK_2E4_PHASE_B.md'
SECURITY_REPORTS = ('audit/TASK_21_SECURITY_REVIEW.json', 'audit/TASK_22_SECURITY_REVIEW.json')
SECURITY_PARENT = 'eec8027b7b4c293fd4ce9e5dfd4a2bb490d61b20'
PHASE_A_POLICY_SHA256 = '558ac5176acf56a00773c2ace9926f31e2fbe6e8ccbe3018a6dd5ffc3fcef9c9'
PHASE_A_SCOPE_SHA256 = 'ce7741ae1677f91491e7d448969f73711870fc49e2901762dbc3b1cf2e1493d8'
CANDIDATES = '_publishing/SEO_TASK_2E2_CLEANUP_CANDIDATES.json'
SCOPE = '_publishing/SEO_TASK_2E3_SCOPE.json'
PREDECESSOR = '_publishing/output-policy.json'
AUDIT_CANDIDATES_SHA256 = '8639edc9a260293d63cb645c9bef49812b04d85cfc286e6234fba14177e3d481'
PREDECESSOR_SHA256 = '4c75dad3817f14e9774d743a2fc4f4f9ad9650e7aabae1a76c9d10db10831206'
EXCLUDES = ['Gemfile', 'Gemfile.lock', 'node_modules', 'vendor/bundle/',
            'vendor/cache/', 'vendor/gems/', 'vendor/ruby/', 'CNAME',
            'HOMEPAGE_DESIGN.md', 'tests/test_pages_output.py']
# Exact reviewed file exclusions, not directory globs.
EXCLUDES += ['AGENTS.md', 'ARCHITECTURE.md', 'CHANGELOG.md', 'CSS_PIPELINE.md', 'DECISIONS.md', 'PROGRESS_TRACKER.md', 'PROJECT_MASTER_PLAN.md', 'ROADMAP.md', 'SEO_FOUNDATION.md', 'SESSION_HANDOFF.md', 'TOOL_CONTRACT.md', 'TOOL_DEVELOPMENT_GUIDE.md', 'audit/BACKLOG_RECONCILIATION.md', 'audit/CURRENT_STATE.md', 'audit/TASK_10_DELIVERY.md', 'audit/TASK_10_DEVELOPMENT_PLAN.md', 'audit/TASK_11_DEVELOPMENT_PLAN.md', 'audit/TASK_12_DEVELOPMENT_PLAN.md', 'audit/TASK_13_DEVELOPMENT_PLAN.md', 'audit/TASK_14_DEVELOPMENT_PLAN.md', 'audit/TASK_15_DEVELOPMENT_PLAN.md', 'audit/TASK_16_DEVELOPMENT_PLAN.md', 'audit/TASK_17_CONSENT_REVIEW.md', 'audit/TASK_18_DEVELOPMENT_PLAN.md', 'audit/TASK_19_DEVELOPMENT_PLAN.md', 'audit/TASK_20_DEVELOPMENT_PLAN.md', 'audit/TASK_24_RELEASE_TESTING.md', 'audit/TASK_7_DEVELOPMENT_PLAN.md', 'audit/TASK_8_DEVELOPMENT_PLAN.md', 'audit/TASK_9_DEVELOPMENT_PLAN.md', 'audit/task22-prototype/README.md', 'audit/task22-public/README.md', 'audit/task24-public/README.md', 'audit/task25-public/README.md', 'scripts/DASHBOARD.md', 'scripts/README.md', 'scripts/WINDOWS_LAUNCHER.md', 'scripts/ci/DESIGN.md', 'scripts/ci/MAIN_BRANCH_PROTECTION.md', 'scripts/ci/README.md', 'scripts/public-verification/task21/README.md', 'scripts/styles/DEPENDENCIES.md', 'scripts/vendor/task21/README.md', 'scripts/vendor/task22/README.md', 'templates/README.md', 'templates/structured-input.html', 'templates/text-input.html', 'templates/tool-page.html']


def reviewed_candidates(root):
    # This digest identifies the recovered raw artifact, including its CRLFs.
    # JSON parsing is semantic; raw integrity must pass before any parsing.
    raw = css_overlay.safe_file(root, CANDIDATES).read_bytes()
    if hashlib.sha256(raw).hexdigest() != AUDIT_CANDIDATES_SHA256:
        raise ValueError('Recovered candidate record changed')
    return json.loads(raw)


EXCLUDES += [name for group in reviewed_candidates(ROOT)['exact_sets'] for name in group['exact_paths']]
EXCLUDES += list(SECURITY_REPORTS)


def phase_a_contract(root, policy):
    """Check the explicit subtraction from frozen production, not inferred output."""
    if policy.get('phase_a') != {'scope': SCOPE, 'predecessor_policy': PREDECESSOR}:
        raise ValueError('Phase A policy selection changed')
    previous_raw = css_overlay.safe_file(root, PREDECESSOR).read_bytes().replace(b'\r\n', b'\n')
    if hashlib.sha256(previous_raw).hexdigest() != PREDECESSOR_SHA256:
        raise ValueError('Frozen Task 2E.1 publishing policy changed')
    previous = json.loads(previous_raw)
    record = reviewed_candidates(root)
    scope = json.loads(css_overlay.safe_file(root, SCOPE).read_bytes())
    groups = record['exact_sets']
    if [(g['id'], len(g['exact_paths'])) for g in groups] != [('C1', 234), ('C2', 85), ('C3', 513), ('C4', 6), ('C5', 2), ('C6', 1)]:
        raise ValueError('Phase A candidate groups changed')
    candidates = [name for group in groups for name in group['exact_paths']]
    excluded = set(candidates)
    review = {row['path'] for row in record['owner_review_files']}
    runtime = set(record['required_runtime_keep_paths'])
    public = set(record['intentionally_public_keep_paths'])
    if len(candidates) != 841 or len(excluded) != 841 or len(review) != 90 or len(runtime) != 11 or len(public) != 6:
        raise ValueError('Phase A candidate/retention counts changed')
    retained = review | runtime | public | set(previous['canonical_pages'])
    if (excluded & retained or len(retained) != 196
            or set(previous['output_paths']) != excluded | retained
            or set(policy['output_paths']) != retained):
        raise ValueError('Phase A output delta differs from exact approved subtraction')
    for key, value in previous.items():
        if key not in {'output_paths', 'markdown_source_paths', 'review_note'} and policy.get(key) != value:
            raise ValueError('Phase A changed a preserved predecessor rule: ' + key)
    if set(policy['markdown_source_paths']) != set(previous['markdown_source_paths']) | {'_publishing/SEO_TASK_2E3_PHASE_A.md'}:
        raise ValueError('Phase A Markdown source change exceeds the checkpoint document')
    if (scope.get('schema_version') != 1
            or scope.get('authorization') != 'DEVELOPMENT_ONLY_NO_MERGE_NO_DEPLOYMENT'
            or scope.get('base_commit') != '34992b8f8ac3e73efbea820bb18c96dae145ff19'
            or scope.get('audit_candidates_sha256') != AUDIT_CANDIDATES_SHA256
            or scope.get('predecessor_policy_sha256') != PREDECESSOR_SHA256
            or set(scope['excluded_output_sha256']) != excluded
            or set(scope['retained_output_sha256']) != retained
            or set(scope['owner_review_keep_paths']) != review
            or set(scope['required_runtime_keep_paths']) != runtime
            or set(scope['intentionally_public_keep_paths']) != public):
        raise ValueError('Phase A scope or protected hash coverage changed')
    for values in (scope['excluded_output_sha256'], scope['retained_output_sha256']):
        if any(not re.fullmatch(r'[0-9a-f]{64}', value) for value in values.values()):
            raise ValueError('Phase A requires complete SHA-256 output evidence')
    checked_directories = set()
    for name in excluded:
        # Only ancestor checks are shared within this call; every source file's
        # lstat remains fresh. Publishing exclusion never permits source deletion.
        css_overlay.safe_file(root, name, checked_directories)
    return scope


def security_report_contract(root, policy):
    """Bind exactly two exclusions to frozen production; never learn an allowlist."""
    previous_raw = css_overlay.safe_file(root, PHASE_A_POLICY).read_bytes().replace(b'\r\n', b'\n')
    scope_raw = css_overlay.safe_file(root, SCOPE).read_bytes().replace(b'\r\n', b'\n')
    if (hashlib.sha256(previous_raw).hexdigest() != PHASE_A_POLICY_SHA256
            or hashlib.sha256(scope_raw).hexdigest() != PHASE_A_SCOPE_SHA256):
        raise ValueError('Frozen Task 2E.3 policy or scope changed')
    previous = json.loads(previous_raw)
    old_scope = phase_a_contract(root, previous)
    if (set(policy) != set(previous) | {'security_report_cleanup'}
            or policy['security_report_cleanup'] != {'scope': SECURITY_SCOPE, 'predecessor_policy': PHASE_A_POLICY}):
        raise ValueError('Security-report successor selection changed')
    for key, value in previous.items():
        if key not in {'output_paths', 'markdown_source_paths', 'review_note'} and policy.get(key) != value:
            raise ValueError('Security-report cleanup changed a preserved predecessor rule: ' + key)
    markdown = previous['markdown_source_paths'] + [SECURITY_CHECKPOINT]
    retained = {name: digest for name, digest in old_scope['retained_output_sha256'].items()
                if name not in SECURITY_REPORTS}
    removed = {name: old_scope['retained_output_sha256'][name] for name in SECURITY_REPORTS}
    if (policy['markdown_source_paths'] != markdown or len(retained) != 194
            or len(policy['output_paths']) != 194 or set(policy['output_paths']) != set(retained)):
        raise ValueError('Security-report cleanup exceeds the exact two-path subtraction')
    # Check semantic text bytes across Git checkout line endings. No file is
    # rewritten; the recovered candidate record still has a separate RAW gate.
    for name, digest in removed.items():
        source = css_overlay.safe_file(root, name).read_bytes().decode('utf-8').replace('\r\n', '\n').encode('utf-8')
        if hashlib.sha256(source).hexdigest() != digest:
            raise ValueError('Original security report source changed')
    expected = {
        'schema_version': 1, 'task': 'SEO Task 2E.4 Phase B',
        'authorization': 'DEVELOPMENT_ONLY_NO_MERGE_NO_DEPLOYMENT',
        'base_commit': SECURITY_PARENT,
        'production_workflow': 42594014512, 'production_artifact': 13662792367,
        'production_artifact_sha256': 'cfefe6c6038df2f8df1127583da0661b0c5afdf02c2dd018b68bbfab5922ffc6',
        'audit_candidates_sha256': AUDIT_CANDIDATES_SHA256,
        'predecessor_policy_sha256': PHASE_A_POLICY_SHA256,
        'predecessor_scope_sha256': PHASE_A_SCOPE_SHA256,
        'new_excluded_output_sha256': removed,
        'excluded_output_sha256': {**old_scope['excluded_output_sha256'], **removed},
        'retained_output_sha256': retained,
        'source_report_sha256': removed,
        'source_report_normalization': 'utf8-lf',
        'owner_review_keep_paths': [name for name in old_scope['owner_review_keep_paths'] if name not in SECURITY_REPORTS],
        'required_runtime_keep_paths': old_scope['required_runtime_keep_paths'],
        'intentionally_public_keep_paths': old_scope['intentionally_public_keep_paths'],
        'counts': {'baseline_outputs': 196, 'new_excluded': 2, 'excluded': 843,
                   'retained': 194, 'canonical_html': 89, 'owner_review': 88,
                   'runtime': 11, 'intentionally_public': 6},
    }
    scope = json.loads(css_overlay.safe_file(root, SECURITY_SCOPE).read_bytes())
    if scope != expected:
        raise ValueError('Security-report scope or protected hash coverage changed')
    return scope


def verify_private_values_absent(root, contents):
    """Scan approved output in memory without publishing private values in errors."""
    report = json.loads(css_overlay.safe_file(root, SECURITY_REPORTS[1]).read_bytes())
    values = [package['path'] for package in report['dependencies']['packages']]
    if len(values) != 5 or any(not isinstance(value, str) or not value for value in values):
        raise ValueError('Original security report privacy inventory changed')
    markers = set()
    for value in values:
        parts = PureWindowsPath(value).parts
        accounts = [parts[i + 1] for i, part in enumerate(parts[:-1]) if part.lower() == 'users']
        for text in [value, value.replace('\\', '/'), *accounts]:
            variants = [text, json.dumps(text)[1:-1], escape(text, quote=True),
                        quote(text, safe=''), quote(text, safe='/')]
            markers.update(variant.lower().encode('utf-8') for variant in variants)
    for data in contents.values():
        lowered = data.lower()
        if any(marker in lowered for marker in markers):
            raise ValueError('Workstation-specific data appeared in generated output')
    return len(contents)


class Metadata(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.canonicals = []
        self.robots = []
        self.refresh = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == 'link' and 'canonical' in values.get('rel', '').lower().split():
            self.canonicals.append(values.get('href', ''))
        if tag == 'meta':
            if values.get('name', '').lower() in {'robots', 'googlebot', 'bingbot'}:
                self.robots.append([values['name'].lower(), values.get('content', '').lower()])
            if values.get('http-equiv', '').lower() == 'refresh':
                self.refresh.append(values.get('content', ''))

    def result(self):
        noindex = any(set(re.split(r'[\s,;]+', content)) & {'noindex', 'none'}
                      for _, content in self.robots)
        return {'canonicals': self.canonicals, 'robots': sorted(self.robots),
                'noindex': noindex, 'refresh': self.refresh}


def metadata(text):
    parser = Metadata()
    parser.feed(text)
    return parser.result()


def approved_bytes(root, name, policy):
    data = (root / name).read_bytes()
    mode = policy['source_normalization'][name]
    if mode == 'utf8-lf':
        data = data.decode('utf-8').replace('\r\n', '\n').encode('utf-8')
    elif mode != 'bytes':
        raise ValueError('Unknown approved source normalization')
    return data


def check_config(root):
    """Deliberately accept only the reviewed, narrow exclusion-only config."""
    lines = [line.strip() for line in (root / '_config.yml').read_text(encoding='utf-8').splitlines()
             if line.strip() and not line.lstrip().startswith('#')]
    if lines != ['exclude:', *['- ' + item for item in EXCLUDES]]:
        raise ValueError('Publishing configuration changed; review defaults and scope')


def check_markdown_sources(root, expected):
    found = set()
    checked_directories = set()
    for directory, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = [name for name in dirs if (Path(directory) / name).relative_to(root).as_posix()
                   not in css_overlay.SKIP_DIRECTORIES]
        for name in files:
            if Path(name).suffix.lower() in {'.md', '.markdown', '.mkdown', '.mkdn', '.mkd'}:
                relative = (Path(directory) / name).relative_to(root).as_posix()
                css_overlay.safe_file(root, relative, checked_directories)
                found.add(relative)
    if found != set(expected):
        raise ValueError('Markdown source inventory changed; review generated routes and permalinks')


def output_files(site):
    """No ignored directories: inspect every actual published output file."""
    site = Path(site).absolute()
    if not site.is_dir():
        raise ValueError('Generated site directory is missing')
    # safe_file rejects a linked root as well as linked ancestors within it.
    found = {}
    checked_directories = set()
    for directory, dirs, files in os.walk(site, followlinks=False):
        for name in dirs:
            target = Path(directory) / name
            info = target.lstat()
            if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
                raise ValueError('Linked generated directory is forbidden')
        for name in files:
            relative = (Path(directory) / name).relative_to(site).as_posix()
            found[relative] = css_overlay.safe_file(site, relative, checked_directories)
    return found


def verify_output(site, root, policy):
    """Pure output checks; CLI separately requires the strict source approval."""
    root = Path(root)
    check_config(root)
    files = output_files(site)
    expected = set(policy['output_paths'])
    if len(expected) != len(policy['output_paths']) or set(files) != expected:
        raise ValueError('Generated output inventory mismatch: ' + json.dumps({
            'unexpected': sorted(set(files) - expected), 'missing': sorted(expected - set(files))}))
    security_cleanup = 'security_report_cleanup' in policy
    scope = (security_report_contract(root, policy) if security_cleanup else
             phase_a_contract(root, policy) if 'phase_a' in policy else None)
    # Read each output once for this invocation. No path, byte or hash result is
    # cached across calls, so subsequent mutations always get fresh validation.
    contents = {}
    def read_output(name):
        if name not in contents:
            contents[name] = files[name].read_bytes()
        return contents[name]

    if scope:
        # Reject changed production bytes before repeatedly parsing unchanged
        # HTML. Successful output still passes every semantic check below.
        for name, expected_hash in scope['retained_output_sha256'].items():
            if hashlib.sha256(read_output(name)).hexdigest() != expected_hash:
                raise ValueError('Retained production output changed: ' + name)
    privacy_files = verify_private_values_absent(root, contents) if security_cleanup else 0
    check_markdown_sources(root, policy['markdown_source_paths'])
    html = {p for p in files if p.lower().endswith(('.html', '.htm'))}
    if html != set(policy['html']):
        raise ValueError('Generated HTML policy is incomplete')
    for name in files:
        if 'homepage_design' in name.lower() or name.startswith(('_publishing/', 'scripts/_publishing_')):
            raise ValueError('Internal documentation or publishing control leaked')
    for retired in policy.get('retired_routes', []):
        original = (root / retired['source']).read_bytes().replace(b'\r\n', b'\n')
        if hashlib.sha256(original).hexdigest() != retired['source_sha256']:
            raise ValueError('Retired source history changed: ' + retired['source'])
        if any(name in files for name in retired['removed_outputs'] + retired['aliases']):
            raise ValueError('Retired documentation output reintroduced')
    canonical = policy['canonical_pages']
    if len(canonical) != 89 or len(set(canonical.values())) != 89:
        raise ValueError('Canonical policy must retain exactly 89 unique URLs')
    for name in sorted(html):
        source = read_output(name).decode('utf-8').replace('\r\n', '\n').replace('\r', '\n')
        actual = metadata(source)
        if actual != policy['html'][name]:
            raise ValueError('Generated canonical/robots/redirect metadata changed: ' + name)
        if name in canonical:
            if actual['canonicals'] != [canonical[name]] or actual['noindex'] or actual['refresh']:
                raise ValueError('Approved canonical page is not indexable at its intended URL: ' + name)
            if read_output(name) != approved_bytes(root, name, policy):
                raise ValueError('Generated canonical page differs from approved source: ' + name)
    for name in policy['exact_public_files']:
        if read_output(name) != approved_bytes(root, name, policy):
            raise ValueError('Public asset or discovery file changed during generation: ' + name)
    if set(policy['public_output_hashes']) != set(canonical) | set(policy['exact_public_files']):
        raise ValueError('Production output hash coverage is incomplete')
    for name, expected_hash in policy['public_output_hashes'].items():
        if hashlib.sha256(read_output(name)).hexdigest() != expected_hash:
            raise ValueError('Public output differs from exact production bytes: ' + name)
    for name, expected_hash in policy['generated_asset_hashes'].items():
        if hashlib.sha256(read_output(name)).hexdigest() != expected_hash:
            raise ValueError('Generated theme asset changed: ' + name)
    urls = [item.text for item in ET.fromstring(read_output('sitemap.xml')).iter()
            if item.tag.endswith('}loc')]
    if len(urls) != 89 or set(urls) != set(canonical.values()):
        raise ValueError('Generated sitemap differs from approved canonical policy')
    document = (root / 'HOMEPAGE_DESIGN.md').read_bytes().replace(b'\r\n', b'\n')
    if hashlib.sha256(document).hexdigest() != policy['preserved_document_sha256']:
        raise ValueError('Original internal design documentation was not preserved')
    return {'status': 'PASS', 'scope': 'GENERATED_OUTPUT_NOT_PUBLIC_DEPLOYMENT',
            'output_files': len(files), 'html_pages': len(html), 'canonical_pages': len(canonical),
            'historical_html_routes_retained': len(html) - len(canonical),
            'retired_html_outputs': len(policy.get('retired_routes', [])),
            'retired_output_files': len(policy.get('retired_output_paths', [])),
            'phase_a_excluded_files': len(scope['excluded_output_sha256']) - len(scope.get('new_excluded_output_sha256', {})) if scope else 0,
            'security_reports_excluded': len(scope.get('new_excluded_output_sha256', {})) if scope else 0,
            'cumulative_excluded_files': len(scope['excluded_output_sha256']) if scope else 0,
            'privacy_output_files_checked': privacy_files,
            'owner_review_files_retained': len(scope['owner_review_keep_paths']) if scope else 0,
            'retained_output_hashes_verified': len(scope['retained_output_sha256']) if scope else 0,
            'sitemap_urls': len(urls), 'exact_public_files': len(policy['exact_public_files']),
            'removed_routes': ['/HOMEPAGE_DESIGN.html', '/HOMEPAGE_DESIGN', '/HOMEPAGE_DESIGN.md'],
            'alias_limit': 'No source HTML, Markdown, extensionless file, redirect or alternative output route remains. Hosting behavior requires post-deployment HTTP verification.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    try:
        approval = css_overlay.validate_current(ROOT)
        policy = json.loads((ROOT / POLICY).read_text(encoding='utf-8'))
        result = verify_output(args.site, ROOT, policy)
        result['source_bound_files'] = len(approval['files'])
        result['policy_sha256'] = css_overlay.digest((ROOT / POLICY).read_text(encoding='utf-8'))
    except (OSError, UnicodeError, ValueError, KeyError, TypeError, ET.ParseError) as error:
        result = {'status': 'FAIL', 'error': str(error)}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2))
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
