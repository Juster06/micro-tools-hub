"""Exact SEO Task 2A candidate projection; never rewrite publication evidence.

The frozen manifest binds the reviewed main source to one canonical insertion
per public page and one CI validation call. It is not a general HTML normalizer
or an exemption for future changes. Unexpected edits fail closed.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

BASE_REVISION = "7cdd6f43800fc1ae01ee597d9bab1a7a597f7f32"
MANIFEST = "audit/SEO_TASK_2A_SOURCE_OVERLAY.json"
MANIFEST_SHA256 = "48493194140992b186e31dda1a293286ee301f2cf61bea2441283280585f60d5"
DOMAIN = "https://everydaydigitalbox.com/"


def normalize(source):
    return source.replace("\r\n", "\n")


def digest(source):
    """Keep all trailing bytes; only Git checkout newline differences normalize."""
    return hashlib.sha256(normalize(source).encode("utf-8")).hexdigest()


def manifest(root):
    path = Path(root) / MANIFEST
    if not path.exists():
        return None  # Generic pre-SEO fixtures have no overlay to project.
    if path.is_symlink() or path.resolve() != path.absolute():
        raise ValueError("SEO overlay manifest must be an ordinary repository file")
    source = path.read_bytes().decode("utf-8")
    if digest(source) != MANIFEST_SHA256:
        raise ValueError("SEO overlay manifest differs from the reviewed immutable candidate")
    value = json.loads(source)
    if (value.get("schema_version") != 1 or value.get("base_revision") != BASE_REVISION
            or value.get("state") != "PENDING_REVIEW_AND_DEPLOYMENT"
            or len(value.get("pages", {})) != 89):
        raise ValueError("SEO overlay manifest identity is invalid")
    return value


def historical_source(root, relative_path, source):
    """Undo only the exact reviewed candidate when comparing historic evidence.

    Unchanged anchored source is accepted for comparison to historic revisions.
    Unlisted files are returned untouched, preserving all existing asset checks.
    Listed files with any other content raise, including body/logic mutations.
    """
    value = manifest(root)
    if value is None:
        return source
    entry = value["pages"].get(relative_path)
    infrastructure = value.get("infrastructure", {}).get(relative_path)
    if entry is None and infrastructure is None:
        return source
    entry = entry or infrastructure
    current = digest(source)
    if current == entry["previous_sha256"]:
        return source
    if current != entry["candidate_sha256"]:
        raise ValueError("Unapproved source change outside SEO Task 2A overlay: " + relative_path)
    newline = "\r\n" if "\r\n" in source else "\n"
    if infrastructure:
        insertion = entry["insertion"].replace("\n", newline)
        anchor = entry["anchor"].replace("\n", newline)
        if source.count(insertion) != 1 or insertion + anchor not in source:
            raise ValueError("SEO CI validation insertion differs from reviewed scope")
        original = source.replace(insertion + anchor, anchor, 1)
    else:
        if entry["canonical"] != DOMAIN + relative_path:
            raise ValueError("SEO overlay canonical target differs from source route")
        tag = '  <link rel="canonical" href="' + entry["canonical"] + '">'
        inserted = "<head>" + newline + tag + newline
        previous = "<head>" + (newline if entry["head_had_newline"] else "")
        if source.count(inserted) != 1:
            raise ValueError("SEO canonical insertion is not in the reviewed head position")
        original = source.replace(inserted, previous, 1)
    if digest(original) != entry["previous_sha256"]:
        raise ValueError("SEO candidate does not reconstruct the exact audited main source")
    return original


def historical_bytes(root, relative_path, source):
    """Binary-safe companion used solely by historical preservation assertions."""
    value = manifest(root)
    if value is None or relative_path not in value["pages"] and relative_path not in value.get("infrastructure", {}):
        return source
    return historical_source(root, relative_path, source.decode("utf-8")).encode("utf-8")


def valid_candidate(root, tool, source):
    """Bind canonical-only candidate back to existing registry/consent evidence."""
    try:
        value = manifest(root)
        relative = tool["directory_path"] + "/index.html"
        if value is None or relative not in value["pages"]:
            return False
        if digest(source) != value["pages"][relative]["candidate_sha256"]:
            return False
        previous = historical_source(root, relative, source)
        recorded = tool["verification"]["source_sha256"]
        if hashlib.sha256(normalize(previous).rstrip().encode("utf-8")).hexdigest() == recorded:
            return True
        # The older 50 pages already have a separately audited consent overlay.
        from consent_overlay import valid_candidate as consent_candidate
        return consent_candidate(root, tool, previous)
    except (OSError, UnicodeError, ValueError, TypeError, KeyError, AttributeError):
        return False
