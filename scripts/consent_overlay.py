"""Strict reversible Task 17 consent overlay on previously published tool pages.

Publication evidence continues to refer to the earlier deployed bytes. Only the
explicit loader insertion and privacy wording below can be pending as a candidate.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

LOADER = '<script defer src="../assets/consent.js"></script>'
REPLACEMENTS = (
    ('No input uploads, tracking, saved drafts or external processing.', 'No input uploads, saved drafts or external processing. Optional site analytics requires consent.'),
    ('Existing homepage Analytics is separate.', 'Optional site analytics is separate from tool input processing.'),
    ('No user-input uploads, tracking, saved drafts or external processing.', 'No user-input uploads, saved drafts or external processing. Optional analytics requires consent.'),
    ('Existing homepage analytics is separate from this utility’s input processing.', 'Optional site analytics is separate from this utility’s input processing.'),
    ('No uploads, saved drafts, analytics, or logging.', 'No uploads, saved drafts or input logging. Optional analytics requires consent.'),
)

def normalize(text: str) -> str:
    return text.replace('\r\n', '\n').rstrip()

def digest(text: str) -> str:
    return hashlib.sha256(normalize(text).encode('utf-8')).hexdigest()

def apply_overlay(text: str) -> str:
    if text.count('</head>') != 1 or LOADER in text:
        raise ValueError('Tool page cannot receive the consent overlay')
    for old, new in REPLACEMENTS:
        if new in text:
            raise ValueError('Unexpected consent wording in original page')
        text = text.replace(old, new)
    return text.replace('</head>', LOADER + '</head>', 1)

def remove_overlay(text: str) -> str:
    if text.count(LOADER) != 1:
        raise ValueError('Consent loader must occur exactly once')
    result = text.replace(LOADER, '', 1)
    for old, new in REPLACEMENTS:
        result = result.replace(new, old)
    if apply_overlay(result) != text:
        raise ValueError('Candidate contains unapproved consent changes')
    return result

def valid_candidate(root: Path, tool: dict, text: str) -> bool:
    """Check exact current candidate, reversible previous publication and assets."""
    try:
        manifest = json.loads((root / 'audit/TASK_17_CANDIDATE.json').read_text(encoding='utf-8'))
        if manifest.get('result') != 'PASS' or manifest.get('state') != 'PENDING_DEPLOYMENT' or manifest.get('base_revision') != '8441c3202a5f23c5e2afd8cb8b89901fc21ffad3': return False
        assets = manifest['assets']
        resolved_root = root.resolve()
        for path in ('assets/consent.js', 'privacy.html'):
            asset_path = (root / path).resolve(strict=True)
            if not asset_path.is_relative_to(resolved_root) or digest(asset_path.read_text(encoding='utf-8-sig')) != assets[path]: return False
        entry = manifest['tools'][tool['id']]
        previous = tool['verification']['source_sha256']
        return entry['previous_sha256'] == previous and entry['candidate_sha256'] == digest(text) and digest(remove_overlay(text)) == previous
    except (OSError, ValueError, TypeError, KeyError, AttributeError, json.JSONDecodeError):
        return False
