"""Static canonical and RELEASED-only sitemap policy. No network or lifecycle writes."""
from __future__ import annotations

import argparse
from collections import Counter
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from urllib.parse import urlsplit

import tracking as tr

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://everydaydigitalbox.com"
SITEMAP_URL = ORIGIN + "/sitemap.xml"
NAMESPACE = "http://www.sitemaps.org/schemas/sitemap/0.9"
PUBLIC_PAGES = (("index.html", "homepage"), ("privacy.html", "privacy"))
RESERVED = {"con", "prn", "aux", "nul", *(f"com{i}" for i in range(1, 10)), *(f"lpt{i}" for i in range(1, 10))}
ROBOTS_TEXT = "User-agent: *\nDisallow:\nSitemap: " + SITEMAP_URL + "\n"


class SEOError(ValueError):
    """An actionable input/policy error; never a reason to publish another URL."""


def local_path(root, relative):
    """Reject traversal and symlink/junction components, including in-tree links."""
    root = Path(root).resolve()
    try:
        tr.safe_path(root, relative)
    except (ValueError, TypeError) as exc:
        raise SEOError(f"{relative}: unsafe project-relative path") from exc
    current = root
    for part in relative.split("/"):
        current = current / part
        if current.is_symlink() or (current.exists() and current.resolve() != current.absolute()):
            raise SEOError(f"{relative}: symlink/junction paths are not allowed")
    return current


def registry_data(root, registry=None):
    local_path(root, "TOOL_REGISTRY.json")
    try:
        result, value = tr.validate_registry(root, registry)
    except (TypeError, KeyError, AttributeError, OSError, UnicodeError) as exc:
        raise SEOError("TOOL_REGISTRY.json: malformed or unreadable registry; run validate_registry.py") from exc
    if result["errors"]:
        routes = {t["id"]: t.get("directory_path") for t in (value or {}).get("tools", []) if isinstance(t, dict) and isinstance(t.get("id"), str)} if isinstance(value, dict) else {}
        messages = []
        for error in result["errors"]:
            identifier = error.get("tool_id", "registry")
            route = routes.get(identifier)
            where = f"{identifier} ({route}/index.html)" if isinstance(route, str) else identifier
            messages.append(f"{where}: {error['code']} — {error['message']}")
        raise SEOError("TOOL_REGISTRY.json: " + "; ".join(messages))
    if value["project"].get("website") != ORIGIN + "/":
        raise SEOError("TOOL_REGISTRY.json: project.website must be " + ORIGIN + "/")
    return value


def canonical_url(relative):
    """Return a policy URL for the approved root pages or a safe tool route."""
    if relative not in dict(PUBLIC_PAGES):
        match = re.fullmatch(r"([a-z0-9]+(?:-[a-z0-9]+)*)/index\.html", relative)
        if not match or match[1] in RESERVED:
            raise SEOError(f"{relative}: not an approved canonical route shape")
    return ORIGIN + "/" + relative


def eligible_pages(root, registry=None):
    """Explicit public allowlist plus registry RELEASED tools; never glob HTML."""
    root = Path(root).resolve()
    value = registry_data(root, registry)
    pages = [{"path": relative, "url": canonical_url(relative), "kind": kind, "tool_id": None}
             for relative, kind in PUBLIC_PAGES]
    for tool in value["tools"]:
        # Validate routes even when excluded; bad registry paths cannot be hidden by status.
        relative = tool["directory_path"] + "/index.html"
        url = canonical_url(relative)
        local_path(root, relative)
        if tool["status"] == "RELEASED":
            pages.append({"path": relative, "url": url, "kind": "tool", "tool_id": tool["id"]})
    if len({p["url"] for p in pages}) != len(pages):
        raise SEOError("TOOL_REGISTRY.json: duplicate public canonical URLs")
    for page in pages:
        if not local_path(root, page["path"]).is_file():
            raise SEOError(page["path"] + ": canonical target is missing")
    return sorted(pages, key=lambda p: p["url"])


def url_error(url):
    if not isinstance(url, str) or not url or url != url.strip():
        return "empty or whitespace-padded URL"
    if any(c.isspace() or ord(c) < 32 for c in url) or any(c in url for c in "?#\\"):
        return "query parameters, fragments, whitespace and backslashes are not allowed"
    try:
        parsed = urlsplit(url)
    except ValueError:
        return "malformed URL"
    if parsed.scheme != "https" or parsed.netloc != "everydaydigitalbox.com":
        return "expected HTTPS and exact production domain without credentials or port"
    try:
        expected = canonical_url(parsed.path.removeprefix("/"))
    except SEOError:
        return "path is not an approved canonical route (including URL escaping)"
    return None if expected == url else "URL does not exactly match the canonical route policy"


def canonical_tag(url):
    error = url_error(url)
    if error:
        raise SEOError(f"{url}: {error}")
    return '<link rel="canonical" href="' + escape(url, quote=True) + '">'


class HeadMetadata(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.head_depth = 0
        self.head_count = 0
        self.head_openings = []
        self.inert_depth = 0
        self.head_malformed = False
        self.body_started = False
        self.text_depth = 0
        self.canonicals = []
        self.noindex = []
        self.duplicate_attributes = []

    def handle_starttag(self, tag, attrs):
        if tag == "head":
            if self.head_depth or self.body_started:
                self.head_malformed = True
            self.head_count += 1
            self.head_depth += 1
            self.head_openings.append((*self.getpos(), len(self.get_starttag_text())))
        if tag == "body":
            self.body_started = True
            if self.head_depth:
                self.head_malformed = True
        if self.head_depth and not self.inert_depth and tag not in {
            "head", "base", "basefont", "bgsound", "link", "meta", "title",
            "style", "script", "template", "noscript", "noframes",
        }:
            # Browsers implicitly close head before ordinary body elements.
            self.head_malformed = True
        if tag in ("title", "style", "script", "noframes"):
            self.text_depth += 1
        if tag in ("template", "noscript"):
            self.inert_depth += 1
        values = dict(attrs)
        if tag == "link" and any(k == "rel" and "canonical" in (v or "").lower().split() for k, v in attrs):
            self.canonicals.append({"href": values.get("href"), "in_head": self.head_depth == 1 and self.inert_depth == 0 and not self.body_started and not self.head_malformed})
            if len(dict(attrs)) != len(attrs):
                self.duplicate_attributes.append("canonical link")
        if tag == "meta" and (values.get("name") or "").lower() in ("robots", "googlebot"):
            directives = re.split(r"[\s,;]+", (values.get("content") or "").lower())
            if "noindex" in directives or "none" in directives:
                self.noindex.append(values.get("content"))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag == "head":
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag == "head":
            if self.head_depth != 1:
                self.head_malformed = True
            self.head_depth -= 1
        if tag in ("template", "noscript"):
            self.inert_depth -= 1
        if tag in ("title", "style", "script", "noframes"):
            self.text_depth = max(0, self.text_depth - 1)

    def handle_data(self, data):
        if self.head_depth and not self.inert_depth and not self.text_depth and data.strip(" \t\r\n\f"):
            # Non-whitespace text also ends the browser's metadata-only head.
            self.head_malformed = True


def metadata(source):
    parsed = HeadMetadata()
    parsed.feed(source)
    parsed.close()
    return parsed


def annotate_html(source, url):
    """Add one static tag; preserve all other bytes/newlines and fail on ambiguity.

    Existing correct annotations are unchanged. Wrong/duplicate annotations and
    noindex pages require review, rather than being silently repaired/published.
    """
    tag = canonical_tag(url)
    parsed = metadata(source)
    if parsed.head_count != 1 or parsed.head_depth != 0 or parsed.head_malformed:
        raise SEOError("HTML must have exactly one balanced static head")
    if parsed.noindex:
        raise SEOError("Refusing canonical insertion on a noindex page")
    if parsed.canonicals:
        if parsed.canonicals != [{"href": url, "in_head": True}] or parsed.duplicate_attributes:
            raise SEOError("Existing canonical is duplicate, misplaced or inconsistent; review it first")
        return source
    if not parsed.head_openings:
        raise SEOError("Missing static head")
    line, column, length = parsed.head_openings[0]
    end = sum(len(s) for s in source.splitlines(keepends=True)[:line - 1]) + column + length
    newline = "\r\n" if "\r\n" in source else "\n"
    if source[end:].startswith(newline):
        end += len(newline)
        return source[:end] + "  " + tag + newline + source[end:]
    # Compact heads get only the canonical line and its two boundary newlines.
    return source[:end] + newline + "  " + tag + newline + source[end:]


def expected_sitemap(pages):
    """UTF-8 XML with stable ordering and no invented modification dates."""
    ET.register_namespace("", NAMESPACE)
    root = ET.Element("{" + NAMESPACE + "}urlset")
    urls = [p["url"] for p in pages]
    if len(urls) != len(set(urls)):
        raise SEOError("Cannot generate a sitemap containing duplicate URLs")
    for url in sorted(urls):
        if url_error(url):
            raise SEOError(f"Cannot generate sitemap URL: {url}")
        item = ET.SubElement(root, "{" + NAMESPACE + "}url")
        ET.SubElement(item, "{" + NAMESPACE + "}loc").text = url
    ET.indent(root, space="  ")
    return ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"


def _add(errors, code, path, message):
    errors.append({"code": code, "path": path, "message": message})


def check_page(root, page, errors):
    relative, expected = page["path"], page["url"]
    try:
        source = local_path(root, relative).read_bytes().decode("utf-8")
        parsed = metadata(source)
    except (OSError, UnicodeError, SEOError) as exc:
        _add(errors, "SEO_TARGET", relative, str(exc))
        return
    if parsed.head_count != 1 or parsed.head_depth != 0 or parsed.head_malformed:
        _add(errors, "SEO_HEAD", relative, "Expected exactly one balanced static HTML head.")
    if not parsed.canonicals:
        _add(errors, "SEO_CANONICAL_MISSING", relative, "Missing canonical; run generate_sitemap.py --sync-canonicals.")
    elif len(parsed.canonicals) != 1:
        _add(errors, "SEO_CANONICAL_DUPLICATE", relative, "Expected exactly one canonical declaration.")
    for item in parsed.canonicals:
        href = item["href"]
        if not item["in_head"]:
            _add(errors, "SEO_CANONICAL_HEAD", relative, "Canonical must be in the static HTML head.")
        error = url_error(href)
        if error:
            _add(errors, "SEO_CANONICAL_URL", relative, f"Invalid canonical {href!r}: {error}.")
        elif href != expected:
            _add(errors, "SEO_CANONICAL_MISMATCH", relative, f"Expected {expected}; found {href}.")
        if isinstance(href, str) and href.startswith(ORIGIN + "/") and not error:
            try:
                if not local_path(root, href[len(ORIGIN) + 1:]).is_file():
                    _add(errors, "SEO_CANONICAL_TARGET", relative, f"Canonical target {href} is missing.")
            except SEOError as exc:
                _add(errors, "SEO_CANONICAL_TARGET", relative, str(exc))
    if parsed.duplicate_attributes:
        _add(errors, "SEO_CANONICAL_ATTRIBUTES", relative, "Canonical link has duplicate attributes.")
    if parsed.noindex:
        _add(errors, "SEO_NOINDEX", relative, "Eligible public page unexpectedly declares noindex/none.")


def check_sitemap(root, pages, errors):
    try:
        data = local_path(root, "sitemap.xml").read_bytes()
        decoded = data.decode("utf-8")
    except (OSError, UnicodeError, SEOError) as exc:
        _add(errors, "SEO_SITEMAP_READ", "sitemap.xml", f"Missing/unreadable UTF-8 sitemap: {exc}")
        return
    if re.search(r"<!\s*(?:DOCTYPE|ENTITY)", decoded, re.I):
        _add(errors, "SEO_SITEMAP_XML", "sitemap.xml", "DTD/entity declarations are not allowed.")
        return
    try:
        tree = ET.fromstring(data)
    except ET.ParseError as exc:
        _add(errors, "SEO_SITEMAP_XML", "sitemap.xml", f"Invalid XML/escaping: {exc}")
        return
    tag = lambda name: "{" + NAMESPACE + "}" + name
    if tree.tag != tag("urlset") or tree.attrib:
        _add(errors, "SEO_SITEMAP_ROOT", "sitemap.xml", "Expected sitemap protocol urlset with no extra attributes.")
    urls = []
    for entry in tree:
        locs = entry.findall(tag("loc"))
        if entry.tag != tag("url") or entry.attrib or len(locs) != 1 or len(entry) != 1 or locs[0].attrib or len(locs[0]):
            _add(errors, "SEO_SITEMAP_ENTRY", "sitemap.xml", "Each url must contain exactly one plain loc; no invented lastmod.")
            continue
        url = locs[0].text or ""
        urls.append(url)
        error = url_error(url)
        if error:
            _add(errors, "SEO_SITEMAP_URL", "sitemap.xml", f"Invalid URL {url!r}: {error}.")
    for url, count in Counter(urls).items():
        if count > 1:
            _add(errors, "SEO_SITEMAP_DUPLICATE", "sitemap.xml", f"Duplicate URL: {url}")
    expected = {p["url"] for p in pages}
    for url in sorted(expected - set(urls)):
        _add(errors, "SEO_SITEMAP_MISSING", "sitemap.xml", f"Missing eligible public URL: {url}")
    for url in sorted(set(urls) - expected):
        _add(errors, "SEO_SITEMAP_INELIGIBLE", "sitemap.xml", f"Not an eligible RELEASED tool/approved public page: {url}")
    # Git may check out LF files as CRLF on Windows; no other formatting drift is accepted.
    if data.replace(b"\r\n", b"\n") != expected_sitemap(pages):
        _add(errors, "SEO_SITEMAP_STALE", "sitemap.xml", "Generated sitemap is stale; run python scripts/generate_sitemap.py.")


def check_robots(root, errors):
    try:
        text = local_path(root, "robots.txt").read_bytes().decode("utf-8")
    except (OSError, UnicodeError, SEOError) as exc:
        _add(errors, "SEO_ROBOTS_READ", "robots.txt", f"Missing/unreadable UTF-8 robots.txt: {exc}")
        return
    # A small explicit policy is easier to audit than arbitrary crawler-specific precedence.
    records = []
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        name, separator, value = line.partition(":")
        if not separator:
            _add(errors, "SEO_ROBOTS_SYNTAX", "robots.txt", f"Line {number}: expected name: value.")
        records.append((name.strip().lower(), value.strip()))
    if [v for k, v in records if k == "sitemap"] != [SITEMAP_URL]:
        _add(errors, "SEO_ROBOTS_SITEMAP", "robots.txt", "Expected one Sitemap: " + SITEMAP_URL)
    if records != [("user-agent", "*"), ("disallow", ""), ("sitemap", SITEMAP_URL)]:
        _add(errors, "SEO_ROBOTS_POLICY", "robots.txt", "Expected the reviewed permissive policy (User-agent: *, empty Disallow, Sitemap). No blocking or crawler-specific rules.")


def validate(root=ROOT, registry=None):
    root = Path(root).resolve()
    result = {"kind": "technical-seo", "status": "FAIL", "errors": [], "warnings": [], "counts": {}}
    try:
        pages = eligible_pages(root, registry)
    except SEOError as exc:
        _add(result["errors"], "SEO_ELIGIBILITY", "TOOL_REGISTRY.json", str(exc))
        return result
    result["counts"] = {"released_tools": sum(p["kind"] == "tool" for p in pages), "public_pages": len(pages)}
    for page in pages:
        check_page(root, page, result["errors"])
    check_sitemap(root, pages, result["errors"])
    check_robots(root, result["errors"])
    result["status"] = "FAIL" if result["errors"] else "PASS"
    return result


def generate(root=ROOT, sync_canonicals=False):
    """Plan all edits before writing. Never changes registry, robots or lifecycle claims."""
    root = Path(root).resolve()
    pages = eligible_pages(root)
    edits = []
    errors = []
    for page in pages:
        path = local_path(root, page["path"])
        old = path.read_bytes()
        try:
            source = old.decode("utf-8")
            if sync_canonicals:
                updated = annotate_html(source, page["url"]).encode("utf-8")
                if updated != old:
                    edits.append((path, updated))
            else:
                check_page(root, page, errors)
        except (UnicodeError, SEOError) as exc:
            raise SEOError(page["path"] + ": " + str(exc)) from exc
    if errors:
        raise SEOError("; ".join(e["path"] + ": " + e["message"] for e in errors))
    sitemap = local_path(root, "sitemap.xml")
    xml = expected_sitemap(pages)
    if not sitemap.exists() or sitemap.read_bytes().replace(b"\r\n", b"\n") != xml:
        edits.append((sitemap, xml))
    for path, data in edits:
        path.write_bytes(data)
    return {"status": "PASS", "public_pages": len(pages), "released_tools": sum(p["kind"] == "tool" for p in pages), "changed_files": [p.relative_to(root).as_posix() for p, _ in edits], "notice": "Local generated metadata only; no publication or indexing claim."}


def cli(mode):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--json", action="store_true", help="Print machine-readable results.")
    parser.add_argument("--no-report", action="store_true", help="Compatibility flag; this command never saves a report.")
    if mode == "generate":
        parser.add_argument("--sync-canonicals", action="store_true", help="Insert missing static canonical tags only on eligible public pages.")
    args = parser.parse_args()
    try:
        result = generate(args.root, args.sync_canonicals) if mode == "generate" else validate(args.root)
    except (SEOError, OSError, UnicodeError) as exc:
        result = {"status": "FAIL", "errors": [{"code": "SEO_GENERATE", "path": "project", "message": str(exc)}], "warnings": []}
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("Technical SEO: " + result["status"])
        counts = result.get("counts", result)
        if "public_pages" in counts:
            print(f"{counts['public_pages']} public canonical pages; {counts['released_tools']} RELEASED tools.")
        for error in result.get("errors", []):
            print(f"{error['path']}: {error['code']} — {error['message']}")
        for changed in result.get("changed_files", []):
            print("Updated " + changed)
    return 1 if result["status"] == "FAIL" else 0
