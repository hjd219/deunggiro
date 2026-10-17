#!/usr/bin/env python3
"""Minimal, idempotent brand-head normalization for published Deunggiro URLs.

Only the HTML <head> is modified. Body, links in body, title, canonical, original
publication and modification dates, sitemap and URL paths are never rewritten.
Use --new-only after importing untracked posts to protect existing articles.
"""
from __future__ import annotations
import argparse
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://www.deunggiro.kr"
FAV = '<link rel="icon" href="https://www.deunggiro.kr/favicon.png" type="image/png">'
OG = '<meta property="og:site_name" content="등기로">'
ORG_ID = BASE + "/#organization"
HEAD_END = re.compile(r"</head\s*>", re.I)
HEAD_OPEN = re.compile(r"<head\b[^>]*>", re.I)
LINK = re.compile(r"<link\b[^>]*>", re.I)
META = re.compile(r"<meta\b[^>]*>", re.I)
JSONLD = re.compile(
    r'(<script\b[^>]*\btype=["\x27]application/ld\+json["\x27][^>]*>)([\s\S]*?)(</script>)',
    re.I,
)
ATTR = re.compile(r'([-\w:]+)\s*=\s*(["\x27])([\s\S]*?)\2')


def attributes(tag: str) -> dict[str, str]:
    return {match.group(1).lower(): match.group(3) for match in ATTR.finditer(tag)}


def favicon(head: str):
    icons = [
        link for link in LINK.finditer(head)
        if "icon" in attributes(link.group(0)).get("rel", "").lower().split()
        or attributes(link.group(0)).get("rel", "").lower() == "shortcut icon"
    ]
    if len(icons) == 1 and icons[0].group(0) == FAV:
        return head, False
    if icons:
        for found in reversed(icons):
            head = head[:found.start()] + (FAV if found == icons[0] else "") + head[found.end():]
    else:
        m = HEAD_OPEN.search(head)
        if not m:
            raise ValueError("no HTML head opening")
        head = head[:m.end()] + FAV + head[m.end():]
    return head, True


def og_site(head: str):
    tags = [
        x for x in META.finditer(head)
        if attributes(x.group(0)).get("property", "").lower() == "og:site_name"
    ]
    if len(tags) == 1 and attributes(tags[0].group(0)).get("content") == "등기로":
        return head, False
    if tags:
        for found in reversed(tags):
            head = head[:found.start()] + (OG if found == tags[0] else "") + head[found.end():]
    else:
        m = HEAD_OPEN.search(head)
        if not m:
            raise ValueError("no HTML head opening")
        head = head[:m.end()] + OG + head[m.end():]
    return head, True


def publisher_org(head: str):
    """Unify Article publisher identity, retain the real office as alternateName."""
    changes = 0

    def replace(match):
        nonlocal changes
        try:
            node = json.loads(match.group(2))
        except (ValueError, TypeError):
            return match.group(0)
        if not isinstance(node, dict) or node.get("@type") not in ("Article", "BlogPosting", "NewsArticle"):
            return match.group(0)
        org = node.get("publisher")
        if not isinstance(org, dict) or org.get("@type") != "Organization":
            return match.group(0)
        if org.get("url", "").rstrip("/") != BASE:
            return match.group(0)
        original_name = org.get("name", "")
        if original_name and original_name != "등기로":
            names = org.get("alternateName")
            names = (names if isinstance(names, list) else [names]) if names else []
            if original_name not in names:
                names.append(original_name)
            org["alternateName"] = names[0] if len(names) == 1 else names
        org["name"] = "등기로"
        org["@id"] = ORG_ID
        org["url"] = BASE + "/"
        compact = json.dumps(node, ensure_ascii=False, separators=(",", ":"))
        if compact != match.group(2):
            changes += 1
            return match.group(1) + compact + match.group(3)
        return match.group(0)

    return JSONLD.sub(replace, head), changes


def fix(source: str, post: bool):
    end = HEAD_END.search(source)
    if not end:
        raise ValueError("no HTML head closing tag")
    head = source[:end.start()]
    suffix = source[end.start():]
    changed = []
    head, f = favicon(head)
    if f:
        changed.append("favicon")
    head, o = og_site(head)
    if o:
        changed.append("og_site_name")
    if post:
        head, count = publisher_org(head)
        if count:
            changed.append("publisher_" + str(count))
    result = head + suffix
    assert result.endswith(suffix), "non-head content must be byte-for-byte preserved"
    # Compare the field values, not the entire JSON substring following them:
    # publisher normalization can legitimately change later fields in the JSON.
    for key in ("datePublished", "dateModified"):
        pattern = r'"' + key + r'"\s*:\s*"([^"]+)"'
        assert re.findall(pattern, source) == re.findall(pattern, result), "date field changed: " + key
    for key in ("dg-date", "description"):
        date_meta = re.compile(r'<meta\b[^>]*>', re.I)
        def protected_meta(markup):
            return sorted(
                (attributes(tag.group(0)).get("name"), attributes(tag.group(0)).get("content"))
                for tag in date_meta.finditer(markup)
                if attributes(tag.group(0)).get("name") == key
            )
        assert protected_meta(source) == protected_meta(result), "protected meta changed: " + key
    return result, changed


def sitemap_paths():
    root = ET.fromstring((ROOT / "sitemap.xml").read_text(encoding="utf-8"))
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    paths = []
    for el in root.findall(".//s:url/s:loc", ns):
        url = urlparse(el.text or "")
        if url.netloc != "www.deunggiro.kr":
            raise ValueError("foreign sitemap host")
        paths.append("index.html" if url.path == "/" else url.path.lstrip("/"))
    if len(paths) != len(set(paths)):
        raise ValueError("sitemap contains duplicate paths")
    return paths


def new_paths():
    listing = subprocess.check_output(
        ["git", "ls-files", "--others", "--exclude-standard", "--", "posts/"],
        cwd=ROOT, text=True
    )
    return [x for x in listing.splitlines()
            if re.fullmatch(r"posts/[a-zA-Z0-9_-]+\.html", x)]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--new-only", action="store_true")
    args = p.parse_args()
    targets = new_paths() if args.new_only else sitemap_paths()
    modified = []
    stats = Counter()
    for path in targets:
        dest = ROOT / path
        if not dest.is_file():
            raise FileNotFoundError(path)
        original = dest.read_text(encoding="utf-8")
        updated, changes = fix(original, path.startswith("posts/"))
        if updated != original:
            if not args.dry_run:
                dest.write_text(updated, encoding="utf-8")
            modified.append(path)
            stats.update(changes)
            stats["pages"] += 1
            if path.startswith("posts/"):
                stats["articles"] += 1
            elif path.startswith("posts-pages/"):
                stats["archives"] += 1
            else:
                stats["core_and_tools"] += 1
    print(json.dumps({
        "dry_run": args.dry_run,
        "new_only": args.new_only,
        "inspected": len(targets),
        "changed": len(modified),
        "changes": dict(stats),
        "first_15": modified[:15]
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
