"""Exact seven-page CSS approval, separate from immutable historical evidence.

The reviewed bootstrap pins the manifest; the manifest binds current runtime,
build, validation, test and CI inputs. Historical projection is allowed only
after the complete current dependency closure passes. No files are written.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys

from _publishing_approval_identity import MANIFEST_SHA256
import seo_overlay

BASE_REVISION = 'cf443c3b1facc2ae422fc6c55d546528671be1d0'
MANIFEST = '_publishing/SEO_TASK_2D2_SOURCE_APPROVAL.json'
IDENTITY = 'scripts/_publishing_approval_identity.py'
PILOT = frozenset({'index.html', 'text-cleaner/index.html', 'json-formatter/index.html',
                  'csv-viewer/index.html', 'image-color-picker/index.html',
                  'vat-calculator/index.html', 'batch-filename-planner/index.html'})
# Exact generated/dependency roots only. A nested reports/ or node_modules/
# directory can still contain a deployable route and must never disappear.
SKIP_DIRECTORIES = frozenset({'.git', 'reports', 'development',
                             'scripts/ci/node_modules', 'scripts/styles/node_modules',
                             'scripts/__pycache__', 'scripts/ci/__pycache__',
                             'tests/__pycache__'})
# Immutable byte payload sharing only. Every snapshot still rereads, validates
# paths and hashes the full live closure before using any interned bytes.
_snapshot_payloads = {}


def normalize(source):
    return source.replace('\r\n', '\n')


def digest(source):
    return hashlib.sha256(normalize(source).encode('utf-8')).hexdigest()


def safe_file(root, relative, _checked_directories=None):
    """Reject lexical escapes and every symlink/junction/reparse component."""
    if (not isinstance(relative, str) or not re.fullmatch(r'[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*', relative)
            or any(part in {'.', '..'} for part in relative.split('/'))):
        raise ValueError('Unsafe CSS approval path: ' + str(relative))
    root = Path(root).absolute()
    current = root
    parts = relative.split('/')
    for position, component in enumerate((None, *parts)):
        if component is not None:
            current = current / component
        # This set exists for one validation call only. All file bytes and all
        # file lstat results are fresh, including same-size/same-mtime changes.
        if _checked_directories is not None and position < len(parts) and current in _checked_directories:
            continue
        info = current.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
            raise ValueError('CSS approval path is a symlink or junction: ' + relative)
        if position < len(parts):
            if not stat.S_ISDIR(info.st_mode):
                raise ValueError('CSS approval parent is not a directory: ' + relative)
            if _checked_directories is not None:
                _checked_directories.add(current)
    # Safe lexical components plus non-linked directory ancestors establish
    # containment without resolving the same root twice per dependency.
    if not stat.S_ISREG(info.st_mode):
        raise ValueError('CSS approval path is not an ordinary repository file: ' + relative)
    return current


def file_digest(root, relative, entry):
    data = safe_file(root, relative).read_bytes()
    mode = entry['normalization']
    if mode == 'utf8-lf':
        data = normalize(data.decode('utf-8')).encode('utf-8')
    elif mode != 'bytes':
        raise ValueError('Unknown CSS approval hash mode')
    return hashlib.sha256(data).hexdigest()


def site_html_paths(root, _checked_directories=None):
    """Inspect deployable HTML, without following links or scanning dependencies."""
    found = set()
    for directory, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(name for name in dirs if (Path(directory) / name).relative_to(root).as_posix() not in SKIP_DIRECTORIES)
        for name in dirs:
            p = Path(directory) / name
            info = p.lstat()
            if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
                raise ValueError('Unexpected deployable symlink/junction: ' + p.relative_to(root).as_posix())
        for name in files:
            if name.lower().endswith(('.html', '.htm')):
                relative = (Path(directory) / name).relative_to(root).as_posix()
                safe_file(root, relative, _checked_directories)
                found.add(relative)
    return found


def manifest(root):
    raw = safe_file(root, MANIFEST).read_bytes().decode('utf-8')
    if digest(raw) != MANIFEST_SHA256:
        raise ValueError('CSS approval manifest differs from the reviewed candidate')
    expected_identity = ("# Reviewed bootstrap trust anchor; deliberately outside the self-referential manifest.\n"
                         "MANIFEST_SHA256 = '" + MANIFEST_SHA256 + "'\n")
    if normalize(safe_file(root, IDENTITY).read_bytes().decode('utf-8')) != expected_identity:
        raise ValueError('CSS approval bootstrap identity changed')
    value = json.loads(raw)
    if (value.get('schema_version') != 1 or value.get('base_revision') != BASE_REVISION
            or value.get('state') != 'DEVELOPMENT_CANDIDATE_NOT_DEPLOYED'
            or set(value.get('pilot_pages', [])) != PILOT
            or len(value['pilot_pages']) != len(PILOT)):
        raise ValueError('CSS approval identity or pilot scope is invalid')
    if set(value['files']) & {MANIFEST, IDENTITY}:
        raise ValueError('CSS approval contains a circular trust dependency')
    if not PILOT <= value['files'].keys() or not PILOT <= value['transformations'].keys():
        raise ValueError('CSS approval is missing an approved pilot page')
    return value


def validate_current(root, *, _capture=None):
    """Fail closed on missing approval, stale bytes, new routes or unsafe paths."""
    root = Path(root).absolute()
    value = manifest(root)
    checked_directories = set()
    html_sources = {}
    for relative, entry in value['files'].items():
        data = safe_file(root, relative, checked_directories).read_bytes()
        if entry['normalization'] == 'utf8-lf':
            data = normalize(data.decode('utf-8')).encode('utf-8')
        elif entry['normalization'] != 'bytes':
            raise ValueError('Unknown CSS approval hash mode')
        if hashlib.sha256(data).hexdigest() != entry['sha256']:
            raise ValueError('Unapproved current CSS dependency: ' + relative)
        if _capture is not None:
            _capture[relative] = _snapshot_payloads.setdefault(data, data)
        if relative in value['site_html_paths']:
            html_sources[relative] = data.decode('utf-8')
    if site_html_paths(root, checked_directories) != set(value['site_html_paths']):
        raise ValueError('Unapproved HTML route or consumer set')
    asset = value['css_asset']
    if (asset['path'] not in value['files'] or value['files'][asset['path']]['sha256'] != asset['sha256']
            or value['files'][asset['path']]['normalization'] != 'bytes'):
        raise ValueError('CSS asset is not bound into the current dependency closure')
    if not re.fullmatch(r'assets/css/site\.[0-9a-f]{16}\.css', asset['path']):
        raise ValueError('CSS asset path is outside the approved naming policy')
    if asset['path'].split('.')[-2] != asset['sha256'][:16]:
        raise ValueError('CSS content filename does not match its hash')
    for relative in value['site_html_paths']:
        source = html_sources[relative]
        if relative in PILOT:
            link = value['transformations'][relative]['stylesheet_tag']
            if source.count(link) != 1 or '@tailwindcss/browser' in source:
                raise ValueError('Missing/duplicate stylesheet or retained compiler: ' + relative)
            head = source.split('</head>', 1)[0]
            if link not in head:
                raise ValueError('Stylesheet moved outside head: ' + relative)
        elif asset['path'].split('/')[-1] in source:
            raise ValueError('Unapproved stylesheet consumer: ' + relative)
    return value


def _has_policy(root, source=''):
    root = Path(root)
    return any((root / path).exists() for path in (MANIFEST, IDENTITY, 'styles/build-manifest.json')) or 'assets/css/site.' in source


def _project(value, relative, source):
    entry = value['transformations'].get(relative)
    if entry is None:
        return source
    if digest(source) != entry['candidate_sha256']:
        raise ValueError('Unapproved CSS source argument: ' + relative)
    previous = normalize(source)
    for operation in reversed(entry['operations']):
        start, end = operation['candidate_start'], operation['candidate_end']
        if previous[start:end] != operation['candidate']:
            raise ValueError('CSS transformation differs from the approved position')
        previous = previous[:start] + operation['previous'] + previous[end:]
    if digest(previous) != entry['previous_sha256']:
        raise ValueError('CSS candidate does not reconstruct the exact main preimage')
    return previous.replace('\n', '\r\n') if '\r\n' in source else previous


def pre_css_source(root, relative, source):
    """Return exact cf443c3 source only after current candidate validation."""
    if not _has_policy(root, source):
        return source
    return _project(validate_current(root), relative, source)


def historical_source(root, relative, source):
    return seo_overlay.historical_source(root, relative, pre_css_source(root, relative, source))


def historical_bytes(root, relative, source):
    if not _has_policy(root):
        return seo_overlay.historical_bytes(root, relative, source)
    value = validate_current(root)
    if relative not in value['transformations']:
        return seo_overlay.historical_bytes(root, relative, source)
    return seo_overlay.historical_bytes(root, relative, _project(value, relative, source.decode('utf-8')).encode('utf-8'))


def historical_snapshot(root):
    """Return readers of one immutable verified snapshot, never live approval.

    Preservation batches compare historical evidence to these captured bytes.
    The current gate remains separate and always rereads the live dependency
    closure. Readers bind this root and reject unbound or modified arguments.
    """
    root = Path(root).absolute()
    captured = {}
    value = validate_current(root, _capture=captured)
    seo = json.loads(captured[seo_overlay.MANIFEST].decode('utf-8'))
    seo_paths = set(seo['pages']) | set(seo.get('infrastructure', {}))
    projected = {}
    for relative, data in captured.items():
        previous = data
        if relative in value['transformations']:
            previous = _project(value, relative, data.decode('utf-8')).encode('utf-8')
        if relative in seo_paths:
            previous = seo_overlay.historical_bytes(root, relative, previous)
            entry = seo['pages'].get(relative) or seo['infrastructure'][relative]
            if digest(previous.decode('utf-8')) != entry['previous_sha256']:
                raise ValueError('Snapshot does not reconstruct captured SEO evidence: ' + relative)
        if previous != data:
            projected[relative] = previous

    def checked_snapshot(candidate_root, relative, source):
        if Path(candidate_root).absolute() != root or relative not in captured:
            raise ValueError('Historical snapshot root/path is not bound: ' + str(relative))
        data = source
        if value['files'][relative]['normalization'] == 'utf8-lf':
            data = normalize(source.decode('utf-8')).encode('utf-8')
        if data != captured[relative]:
            raise ValueError('Source differs from the immutable historical snapshot: ' + relative)
        if relative not in projected:
            return source
        previous = projected[relative]
        return previous.replace(b'\n', b'\r\n') if b'\r\n' in source else previous

    def snapshot_source(candidate_root, relative, source):
        return checked_snapshot(candidate_root, relative, source.encode('utf-8')).decode('utf-8')

    return snapshot_source, checked_snapshot


def candidate_snapshot(root):
    """Bind candidate checks to one verified snapshot within a project check.

    This reader is evidence for captured bytes, not a reusable live approval.
    The project checker performs another fresh gate before returning success.
    """
    root = Path(root).absolute()
    captured = {}
    value = validate_current(root, _capture=captured)
    records = json.loads(captured['TOOL_REGISTRY.json'].decode('utf-8'))['tools']
    approved = {}
    for tool in records:
        relative = tool['directory_path'] + '/index.html'
        if relative not in PILOT:
            continue
        source = captured[relative].decode('utf-8')
        previous = _project(value, relative, source)
        if not seo_overlay.valid_candidate(root, tool, previous):
            raise ValueError('CSS snapshot is not bound to registry evidence: ' + relative)
        approved[relative] = tool

    def accepts(candidate_root, tool, source):
        try:
            relative = tool['directory_path'] + '/index.html'
            return (Path(candidate_root).absolute() == root
                    and relative in approved and tool == approved[relative]
                    and normalize(source).encode('utf-8') == captured[relative])
        except (TypeError, KeyError, AttributeError, UnicodeError):
            return False

    return value, accepts


def valid_candidate(root, tool, source):
    try:
        relative = tool['directory_path'] + '/index.html'
        if relative not in PILOT:
            return False
        previous = pre_css_source(root, relative, source)
        if previous == source:
            return False
        return seo_overlay.valid_candidate(root, tool, previous)
    except (OSError, UnicodeError, ValueError, TypeError, KeyError, AttributeError):
        return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', required=True)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    try:
        value = validate_current(Path(__file__).resolve().parents[1])
        result = {'status': 'PASS', 'pilot_pages': len(PILOT), 'bound_files': len(value['files']),
                  'base_revision': BASE_REVISION, 'state': value['state'], 'css_asset': value['css_asset']}
    except (OSError, UnicodeError, ValueError, TypeError, KeyError) as error:
        result = {'status': 'FAIL', 'error': str(error)}
    print(json.dumps(result, indent=2) if args.json else 'CSS source approval: ' + result['status'] + (' — ' + result['error'] if 'error' in result else ''))
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
