"""Validate real Pages output against a reviewed inventory, never approve it.

The policy retains historical routes without endorsing their indexability.
Any new output, including Markdown-generated HTML, requires explicit review.
"""
from __future__ import annotations

import argparse
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import stat
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import css_overlay

POLICY = '_publishing/output-policy.json'
EXCLUDES = ['Gemfile', 'Gemfile.lock', 'node_modules', 'vendor/bundle/',
            'vendor/cache/', 'vendor/gems/', 'vendor/ruby/', 'CNAME',
            'HOMEPAGE_DESIGN.md', 'tests/test_pages_output.py']
# Exact reviewed file exclusions, not directory globs.
EXCLUDES += ['AGENTS.md', 'ARCHITECTURE.md', 'CHANGELOG.md', 'CSS_PIPELINE.md', 'DECISIONS.md', 'PROGRESS_TRACKER.md', 'PROJECT_MASTER_PLAN.md', 'ROADMAP.md', 'SEO_FOUNDATION.md', 'SESSION_HANDOFF.md', 'TOOL_CONTRACT.md', 'TOOL_DEVELOPMENT_GUIDE.md', 'audit/BACKLOG_RECONCILIATION.md', 'audit/CURRENT_STATE.md', 'audit/TASK_10_DELIVERY.md', 'audit/TASK_10_DEVELOPMENT_PLAN.md', 'audit/TASK_11_DEVELOPMENT_PLAN.md', 'audit/TASK_12_DEVELOPMENT_PLAN.md', 'audit/TASK_13_DEVELOPMENT_PLAN.md', 'audit/TASK_14_DEVELOPMENT_PLAN.md', 'audit/TASK_15_DEVELOPMENT_PLAN.md', 'audit/TASK_16_DEVELOPMENT_PLAN.md', 'audit/TASK_17_CONSENT_REVIEW.md', 'audit/TASK_18_DEVELOPMENT_PLAN.md', 'audit/TASK_19_DEVELOPMENT_PLAN.md', 'audit/TASK_20_DEVELOPMENT_PLAN.md', 'audit/TASK_24_RELEASE_TESTING.md', 'audit/TASK_7_DEVELOPMENT_PLAN.md', 'audit/TASK_8_DEVELOPMENT_PLAN.md', 'audit/TASK_9_DEVELOPMENT_PLAN.md', 'audit/task22-prototype/README.md', 'audit/task22-public/README.md', 'audit/task24-public/README.md', 'audit/task25-public/README.md', 'scripts/DASHBOARD.md', 'scripts/README.md', 'scripts/WINDOWS_LAUNCHER.md', 'scripts/ci/DESIGN.md', 'scripts/ci/MAIN_BRANCH_PROTECTION.md', 'scripts/ci/README.md', 'scripts/public-verification/task21/README.md', 'scripts/styles/DEPENDENCIES.md', 'scripts/vendor/task21/README.md', 'scripts/vendor/task22/README.md', 'templates/README.md', 'templates/structured-input.html', 'templates/text-input.html', 'templates/tool-page.html']


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
    for directory, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = [name for name in dirs if (Path(directory) / name).relative_to(root).as_posix()
                   not in css_overlay.SKIP_DIRECTORIES]
        for name in files:
            if Path(name).suffix.lower() in {'.md', '.markdown', '.mkdown', '.mkdn', '.mkd'}:
                relative = (Path(directory) / name).relative_to(root).as_posix()
                css_overlay.safe_file(root, relative)
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
    for directory, dirs, files in os.walk(site, followlinks=False):
        for name in dirs:
            target = Path(directory) / name
            info = target.lstat()
            if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
                raise ValueError('Linked generated directory is forbidden')
        for name in files:
            relative = (Path(directory) / name).relative_to(site).as_posix()
            found[relative] = css_overlay.safe_file(site, relative)
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
        source = files[name].read_text(encoding='utf-8')
        actual = metadata(source)
        if actual != policy['html'][name]:
            raise ValueError('Generated canonical/robots/redirect metadata changed: ' + name)
        if name in canonical:
            if actual['canonicals'] != [canonical[name]] or actual['noindex'] or actual['refresh']:
                raise ValueError('Approved canonical page is not indexable at its intended URL: ' + name)
            if files[name].read_bytes() != approved_bytes(root, name, policy):
                raise ValueError('Generated canonical page differs from approved source: ' + name)
    for name in policy['exact_public_files']:
        if files[name].read_bytes() != approved_bytes(root, name, policy):
            raise ValueError('Public asset or discovery file changed during generation: ' + name)
    if set(policy['public_output_hashes']) != set(canonical) | set(policy['exact_public_files']):
        raise ValueError('Production output hash coverage is incomplete')
    for name, expected_hash in policy['public_output_hashes'].items():
        if hashlib.sha256(files[name].read_bytes()).hexdigest() != expected_hash:
            raise ValueError('Public output differs from exact production bytes: ' + name)
    for name, expected_hash in policy['generated_asset_hashes'].items():
        if hashlib.sha256(files[name].read_bytes()).hexdigest() != expected_hash:
            raise ValueError('Generated theme asset changed: ' + name)
    urls = [item.text for item in ET.fromstring(files['sitemap.xml'].read_bytes()).iter()
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
