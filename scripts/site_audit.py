#!/usr/bin/env python3
"""Read-only SEO audit for GitHub Pages. Does not change sitemap or content."""
import collections
import datetime as dt
import html.parser
import json
import os
import pathlib
import sys
import urllib.parse
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
HOST = "www.deunggiro.kr"
ISSUES = []
STATS = {}

def issue(level, code, location, detail):
    ISSUES.append(dict(level=level, code=code, location=location, detail=detail))

class Page(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.canonical = []
        self.titles = 0
        self.h1 = 0
        self.description = 0
        self.noindex = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "link" and "canonical" in a.get("rel", "").lower().split():
            self.canonical.append(a.get("href", ""))
        if tag == "title": self.titles += 1
        if tag == "h1": self.h1 += 1
        if tag == "meta":
            if a.get("name", "").lower() == "description": self.description += 1
            if a.get("name", "").lower() == "robots" and "noindex" in a.get("content", "").lower(): self.noindex = True

def local_path(url):
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme and (parsed.scheme not in ("http", "https") or parsed.hostname not in (HOST, "deunggiro.kr")):
        return None
    if url.startswith(("mailto:", "tel:", "javascript:", "data:")) or url.startswith("//"):
        return None
    path = urllib.parse.unquote(parsed.path).lstrip("/")
    if not path or path.endswith("/"): path += "index.html"
    return path

def run():
    try:
        sitemap = ET.parse(ROOT / "sitemap.xml")
        rss = ET.parse(ROOT / "rss.xml")
    except (ET.ParseError, OSError) as exc:
        issue("error", "XML_INVALID", "sitemap.xml/rss.xml", str(exc))
        return
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    entries = sitemap.findall(".//s:url", ns)
    urls = []
    for entry in entries:
        url = entry.findtext("s:loc", default="", namespaces=ns).strip()
        urls.append(url)
        path = local_path(url)
        if not path or not (ROOT / path).is_file():
            issue("error", "SITEMAP_TARGET_MISSING", url, "Target is absent from repository")
        lastmod = entry.findtext("s:lastmod", default="", namespaces=ns).strip()
        if lastmod:
            try:
                day = dt.date.fromisoformat(lastmod[:10])
                if day > dt.datetime.now(dt.timezone.utc).date() + dt.timedelta(days=1):
                    issue("warning", "LASTMOD_FUTURE", url, lastmod)
            except ValueError:
                issue("warning", "LASTMOD_INVALID", url, lastmod)
    for url, n in collections.Counter(urls).items():
        if n > 1: issue("error", "SITEMAP_DUPLICATE", url, str(n))
    items = rss.findall(".//item")
    if len(items) != 100:
        issue("warning", "RSS_ITEM_COUNT", "rss.xml", f"Expected 100, found {len(items)}")
    html_files = sorted(ROOT.rglob("*.html"))
    inbound = collections.Counter()
    parsed_pages = {}
    for f in html_files:
        relative = f.relative_to(ROOT).as_posix()
        if relative.startswith((".git/", "node_modules/")): continue
        try:
            parser = Page()
            parser.feed(f.read_text(encoding="utf-8"))
        except (UnicodeError, OSError) as exc:
            issue("error", "HTML_READ_ERROR", relative, str(exc))
            continue
        parsed_pages[relative] = parser
        if relative in {local_path(u) for u in urls}:
            expected = "https://" + HOST + ("/" if relative == "index.html" else "/" + relative)
            if len(parser.canonical) != 1 or parser.canonical[0] != expected:
                issue("warning", "CANONICAL_MISMATCH", relative, f"expected {expected}, found {parser.canonical}")
            if parser.titles != 1: issue("warning", "TITLE_COUNT", relative, str(parser.titles))
            if parser.description != 1: issue("warning", "DESCRIPTION_COUNT", relative, str(parser.description))
            if parser.h1 != 1: issue("warning", "H1_COUNT", relative, str(parser.h1))
            if parser.noindex: issue("error", "SITEMAP_NOINDEX", relative, "Indexed URL has noindex")
        for href in parser.links:
            resolved = urllib.parse.urljoin("https://" + HOST + "/" + relative, href)
            target = local_path(resolved)
            if target is None: continue
            inbound[target] += 1
            if not (ROOT / target).is_file():
                issue("warning", "BROKEN_INTERNAL_LINK", relative, href)
    for url in urls:
        target = local_path(url)
        if target and target != "index.html" and inbound[target] == 0:
            issue("warning", "NO_HTML_INBOUND", target, "No static HTML anchor found; JS links may exist")
    STATS.update(sitemap_urls=len(urls), unique_urls=len(set(urls)), rss_items=len(items),
                 scanned_html=len(parsed_pages), errors=sum(i["level"] == "error" for i in ISSUES),
                 warnings=sum(i["level"] == "warning" for i in ISSUES))
    report = {"generated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(), "stats": STATS, "issues": ISSUES}
    out = ROOT / "seo-audit-report.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(STATS, ensure_ascii=False))
    for i in ISSUES[:30]: print(f'{i["level"]}: {i["code"]} {i["location"]} {i["detail"]}')
    if len(ISSUES) > 30: print(f"... {len(ISSUES)-30} more; see report artifact")
    if STATS["errors"]: sys.exit(1)

if __name__ == "__main__": run()
