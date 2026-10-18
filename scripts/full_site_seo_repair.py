#!/usr/bin/env python3
"""One-time conservative full-repository SEO audit and head-only repair.

Only HTML head metadata/JSON-LD, explicit noindex for unused backups, and one
new sitemap URL (public officer-manager application) can change.
Never touch visible content, canonical paths for existing URLs, publication dates
or existing sitemap entries/lastmod values.
"""
from __future__ import annotations

import argparse
import collections
from html.parser import HTMLParser
import json
import re
from pathlib import Path
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://www.deunggiro.kr"
POSTS = json.loads((ROOT / "data/posts.json").read_text(encoding="utf-8"))
POST_BY_SLUG = {str(p["slug"]): p for p in POSTS if p.get("slug")}
HEAD_CLOSE = re.compile(r"</head\s*>", re.I)
META = re.compile(r"<meta\b[^>]*>", re.I)
LINK = re.compile(r"<link\b[^>]*>", re.I)
TITLE = re.compile(r"<title\b[^>]*>([\s\S]*?)</title\s*>", re.I)
LD = re.compile(r'<script\b[^>]*type=["\x27]application/ld\+json["\x27][^>]*>([\s\S]*?)</script\s*>', re.I)
ATTR = re.compile(r'([:\w-]+)\s*=\s*(["\x27])([\s\S]*?)\2')
COUNT = collections.Counter()
ISSUES = []
CHANGED = []

class Parse(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.h1 = 0
        self.links = []
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "h1":
            self.h1 += 1
        if tag == "a" and d.get("href"):
            self.links.append(d["href"])

def attrs(tag):
    return {m.group(1).lower(): m.group(3) for m in ATTR.finditer(tag)}

def issue(path, code, detail=""):
    ISSUES.append({"path": path, "code": code, "detail": str(detail)[:200]})
    COUNT["issue_" + code] += 1

def sitemap_paths():
    xml = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    root = ET.fromstring(xml)
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    entries = root.findall("s:url", ns)
    mapping = {}
    for el in entries:
        loc = (el.findtext("s:loc", default="", namespaces=ns) or "").strip()
        parsed = urlparse(loc)
        if parsed.netloc != "www.deunggiro.kr":
            issue("sitemap.xml", "foreign_host", loc)
            continue
        path = "index.html" if parsed.path == "/" else parsed.path.lstrip("/")
        if path in mapping: issue("sitemap.xml", "duplicate_url", path)
        mapping[path] = loc
    return xml, mapping

def existing(head, kind, name):
    return [(match, attrs(match.group(0))) for match in META.finditer(head)
            if attrs(match.group(0)).get(kind, "").lower() == name.lower()]

def add_meta(head, kind, name, value):
    if not value: return head
    found = existing(head, kind, name)
    if found:
        # Existing values are kept, avoiding title/description churn and date changes.
        if len(found) > 1:
            for match, _ in reversed(found[1:]):
                head = head[:match.start()] + head[match.end():]
            COUNT["duplicate_meta_removed"] += len(found)-1
        return head
    from html import escape
    COUNT["new_" + name] += 1
    return head + '<meta ' + kind + '="' + name + '" content="' + escape(str(value), quote=True) + '">\n'

def add_canonical(head, expected):
    found = [(m, attrs(m.group(0))) for m in LINK.finditer(head)
             if "canonical" in attrs(m.group(0)).get("rel", "").lower().split()]
    if len(found) == 1 and found[0][1].get("href") == expected:
        return head
    for m, _ in reversed(found):
        head = head[:m.start()] + head[m.end():]
    COUNT["canonical_repaired"] += 1
    return head + '<link rel="canonical" href="' + expected + '">\n'

def getmeta(head, kind, name):
    found = existing(head, kind, name)
    return found[0][1].get("content","") if found else ""

def schema_types(head, path):
    types = set()
    for m in LD.finditer(head):
        try:
            obj = json.loads(m.group(1))
            nodes = obj if isinstance(obj,list) else [obj]
            for node in nodes:
                if not isinstance(node,dict): continue
                graph = node.get("@graph",[])
                for a in [node]+(graph if isinstance(graph,list) else []):
                    t=a.get("@type",[]) if isinstance(a,dict) else []
                    types.update(t if isinstance(t,list) else [t])
        except (ValueError,TypeError) as exc:
            issue(path, "invalid_jsonld", str(exc))
    return types

def json_tag(data):
    return '<script type="application/ld+json">' + json.dumps(data,ensure_ascii=False,separators=(",",":")) + '</script>\n'

def url_for(path):
    return BASE + ("/" if path == "index.html" else "/" + path)

def repair_head(path, raw, indexed):
    end = HEAD_CLOSE.search(raw)
    if not end:
        issue(path,"missing_head")
        return raw
    head = raw[:end.start()]
    tail = raw[end.start():]
    p = Parse()
    try: p.feed(raw)
    except Exception as exc: issue(path,"html_parse",str(exc))
    if indexed and p.h1 != 1: issue(path,"h1_count",p.h1)
    title_matches = TITLE.findall(head)
    title = re.sub(r"\s+"," ",title_matches[0]).strip() if title_matches else ""
    if indexed and len(title_matches)!=1: issue(path,"title_count",len(title_matches))
    canonical = url_for(path)
    if indexed:
        head = add_canonical(head,canonical)
    head = add_meta(head,"name","description", title + " | 등기로 법률정보" if indexed else "")
    desc = getmeta(head,"name","description")
    if indexed:
        for kind,name,value in (
            ("property","og:type","article" if path.startswith("posts/") else "website"),
            ("property","og:site_name","등기로"),
            ("property","og:title",title),
            ("property","og:description",desc),
            ("property","og:url",canonical),
            ("property","og:image", BASE + "/images/og-home.jpg"),
            ("name","twitter:card","summary_large_image"),
            ("name","twitter:title",getmeta(head,"property","og:title") or title),
            ("name","twitter:description",getmeta(head,"property","og:description") or desc),
            ("name","twitter:image",getmeta(head,"property","og:image") or BASE+"/images/og-home.jpg"),
        ):
            head = add_meta(head,kind,name,value)
        robots = getmeta(head,"name","robots").lower()
        if "noindex" in robots and path != "officer-manager.html": issue(path,"indexed_noindex",robots)
        if getmeta(head,"property","og:url") != canonical:
            issue(path,"og_url_mismatch",getmeta(head,"property","og:url"))
    else:
        if path.startswith("backups/") or "preview" in path or path=="admin.html":
            if not getmeta(head,"name","robots"):
                head = add_meta(head,"name","robots","noindex,nofollow")
    types = schema_types(head,path)
    if indexed and not types:
        if path.startswith("posts/"):
            post = POST_BY_SLUG.get(Path(path).stem,{})
            published = post.get("date") or "2026-01-01"
            schema = {
                "@context":"https://schema.org","@type":"BlogPosting",
                "headline":title,"url":canonical,
                "datePublished":published,"dateModified":published,
                "author":{"@type":"Person","name":"현재두 법무사"},
                "publisher":{"@type":"Organization","name":"등기로","url":BASE+"/"}
            }
        elif path.startswith("posts-pages/"):
            schema = {"@context":"https://schema.org","@type":"CollectionPage","name":title,"url":canonical}
        else:
            schema = {"@context":"https://schema.org","@type":"WebPage","name":title,"url":canonical}
        head += json_tag(schema)
        COUNT["schema_added"]+=1
    if path in ("privacy.html","disclaimer.html","officer-manager.html") and "WebPage" not in types and "WebApplication" not in types:
        head += json_tag({"@context":"https://schema.org","@type":"WebPage","name":title,"url":canonical})
        COUNT["schema_added"]+=1
    if path=="officer-manager.html":
        robots_meta = existing(head,"name","robots")
        for m,a in reversed(robots_meta):
            if "noindex" in a.get("content","").lower():
                head=head[:m.start()]+head[m.end():]
                COUNT["officer_noindex_removed"]+=1
    after = head + tail
    # Legal dates and user-facing markup must remain byte-identical.
    for fld in ("datePublished","dateModified"):
        pattern=r'"'+fld+r'"\s*:\s*"([^"]+)"'
        if re.findall(pattern,raw)!=re.findall(pattern,after):
            raise RuntimeError(path+": "+fld+" changed")
    if raw[raw.lower().index("</head"): ] != after[after.lower().index("</head") :]:
        raise RuntimeError(path+": body changed")
    if after!=raw: CHANGED.append(path)
    COUNT["audited"]+=1
    return after

def main():
    arg=argparse.ArgumentParser()
    arg.add_argument("--check",action="store_true")
    options=arg.parse_args()
    sitemap, urls = sitemap_paths()
    include=set(urls)
    # Officer-management landing tool should have crawlable public discovery.
    include.add("officer-manager.html")
    scanned=set()
    for dest in sorted(ROOT.rglob("*.html")):
        path=dest.relative_to(ROOT).as_posix()
        if ".git/" in path: continue
        scanned.add(path)
        raw=dest.read_text(encoding="utf-8",errors="replace")
        if path in include and not dest.is_file():
            issue(path,"missing_page")
        changed=repair_head(path,raw,path in include)
        if not options.check and changed!=raw:
            dest.write_text(changed,encoding="utf-8")
    for missing in sorted(include-scanned): issue(missing,"missing_page")
    # Only append a new sitemap URL; all pre-existing entries/lastmod remain verbatim.
    if "officer-manager.html" not in urls:
        addition='  <url><loc>'+url_for("officer-manager.html")+'</loc><changefreq>monthly</changefreq><priority>0.6</priority></url>\n'
        new_xml=sitemap.replace("</urlset>",addition+"</urlset>",1)
        if not options.check:
            (ROOT/"sitemap.xml").write_text(new_xml,encoding="utf-8")
        if new_xml!=sitemap: COUNT["sitemap_new_url"]+=1
    from collections import Counter
    issues_by_type=dict(Counter(i["code"] for i in ISSUES))
    report={"scanned_html":len(scanned),"sitemap_urls_existing":len(urls),
            "changed":len(CHANGED),"changed_files":CHANGED,
            "counters":dict(COUNT),"issues_by_type":issues_by_type,"issues":ISSUES}
    (ROOT/"seo-full-audit-report.json").write_text(
        json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if k not in ("issues","changed_files")},
                     ensure_ascii=False,indent=2))
    print("SEO_CHANGED",json.dumps(CHANGED[:30],ensure_ascii=False))
    print("SEO_ISSUES",json.dumps(ISSUES[:25],ensure_ascii=False))
    # Check mode requires zero further modifications and no blocking structural failures.
    if options.check and (CHANGED or COUNT["sitemap_new_url"]):
        raise SystemExit("SEO REPAIR NOT IDEMPOTENT")
    if any(x["code"] in ("missing_head","invalid_jsonld","indexed_noindex","missing_page")
           for x in ISSUES):
        raise SystemExit("SEO AUDIT HAS BLOCKING ISSUES")

if __name__=="__main__":
    main()
