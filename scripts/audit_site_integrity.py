from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from collections import Counter, defaultdict
import json, re, xml.etree.ElementTree as ET

ROOT = Path(".")
IGNORE_DIRS = {".git", ".github", "scripts", "docs"}
files = {p.as_posix().removeprefix("./") for p in ROOT.rglob("*") if p.is_file() and not any(part in IGNORE_DIRS for part in p.parts) and "_site" not in p.parts}
htmls = sorted(x for x in files if x.endswith(".html"))
missing = defaultdict(set)
missing_by_page = defaultdict(set)
canonicals = {}
noindex = []
missing_canonicals = []
duplicate_canonicals = defaultdict(list)
titles = defaultdict(list)
empty_titles = []
h1_missing = []
external_unusual = []
path_issues = []
flags = defaultdict(list)
refs = defaultdict(set)

def resolve(source, raw):
    val = raw.strip()
    if not val or val.startswith(("#", "mailto:", "tel:", "javascript:", "data:", "blob:", "//")):
        return None
    u = urlsplit(val)
    if u.scheme and u.scheme not in ("http", "https"):
        return None
    if u.netloc and u.netloc.lower() not in ("www.deunggiro.kr", "deunggiro.kr"):
        return None
    path = unquote(u.path)
    if not path and u.netloc:
        path = "/"
    if path.startswith("/"):
        norm = Path(path.lstrip("/"))
    else:
        norm = Path(source).parent / path
    parts = []
    for part in norm.parts:
        if part in ("", "."):
            continue
        if part == "..":
            if parts: parts.pop()
            continue
        parts.append(part)
    name = "/".join(parts) or "index.html"
    if name.endswith("/"): name += "index.html"
    return name

class Scan(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.source=source
        self.title=False
        self.titletext=[]
        self.h1=0
        self.canonical=None
        self.robot=[]
        self.attr_errors=[]
    def handle_starttag(self, tag, attrs):
        d=dict(attrs)
        if tag=="title": self.title=True
        if tag=="h1": self.h1+=1
        if tag=="meta" and d.get("name","").lower() in ("robots","googlebot"):
            self.robot.append(d.get("content",""))
        if tag=="link" and "canonical" in d.get("rel","").lower():
            self.canonical=d.get("href")
        for key in ("href", "src", "poster", "data-src"):
            raw=d.get(key,"")
            if not raw: continue
            if key=="href" and tag not in ("a","link","area","iframe"):
                continue
            if tag=="link" and "canonical" in d.get("rel","").lower():
                continue
            path=resolve(self.source,raw)
            if path is None:continue
            if raw.startswith("#"): continue
            if path not in files and path+"/index.html" not in files:
                missing[(path,tag,key)].add(self.source)
                missing_by_page[self.source].add(path)
            else:
                refs[path].add(self.source)
        for raw in d.get("srcset","").split(","):
            raw=raw.strip().split(" ")[0]
            if raw:
                path=resolve(self.source,raw)
                if path and path not in files:
                    missing[(path,"srcset","srcset")].add(self.source)
                    missing_by_page[self.source].add(path)
    def handle_data(self, data):
        if self.title:self.titletext.append(data)
    def handle_endtag(self,tag):
        if tag=="title":self.title=False

for source in htmls:
    p=Scan(source)
    try:
        p.feed((ROOT/source).read_text(encoding="utf-8",errors="replace"))
    except Exception as e:
        flags["html_parse_errors"].append({"page":source,"error":str(e)})
        continue
    title=" ".join(p.titletext).strip()
    if not title: empty_titles.append(source)
    else: titles[title].append(source)
    if p.h1==0: h1_missing.append(source)
    if any("noindex" in x.lower() for x in p.robot): noindex.append(source)
    if not p.canonical: missing_canonicals.append(source)
    else:
        canonicals[source]=p.canonical
        duplicate_canonicals[p.canonical].append(source)
        expected="https://www.deunggiro.kr/"+("" if source=="index.html" else source)
        if p.canonical!=expected:
            flags["nonself_canonical"].append({"page":source,"canonical":p.canonical,"expected":expected})

sitemap_urls=[]
try:
    tree=ET.parse("sitemap.xml")
    sitemap_urls=[x.text for x in tree.findall(".//{*}loc") if x.text]
except Exception as e:
    flags["sitemap_error"].append(str(e))
missing_sitemap_targets=[]
for url in sitemap_urls:
    t=resolve("index.html",url)
    if t not in files: missing_sitemap_targets.append(url)
sitemap_pages={resolve("index.html",url) for url in sitemap_urls}
html_not_in_sitemap=[x for x in htmls if x not in sitemap_pages]
dup_titles={k:v for k,v in titles.items() if len(v)>1}
dup_canons={k:v for k,v in duplicate_canonicals.items() if len(v)>1}

# Search code and stylesheets for explicit missing resource references, avoiding false positives from variable JS.
css_missing=defaultdict(set)
css_files=sorted(x for x in files if x.endswith(".css"))
for source in css_files:
    raw=(ROOT/source).read_text(encoding="utf-8",errors="replace")
    for value in re.findall(r"url\(\s*['\"]?([^)'\"\s]+)",raw):
        t=resolve(source,value)
        if t and t not in files:
            css_missing[t].add(source)
missing_sorted=sorted([{"target":target,"tag":tag,"attribute":attr,"count":len(sources),"sources":sorted(sources)[:25]} for (target,tag,attr),sources in missing.items()],key=lambda x:(-x["count"],x["target"]))
report={
"counts":{"total_files":len(files),"html_files":len(htmls),"css_files":len(css_files),"sitemap_urls":len(sitemap_urls),"html_with_missing_refs":len(missing_by_page),"missing_ref_variants":len(missing_sorted),"missing_sitemap_targets":len(missing_sitemap_targets),"noindex_pages":len(noindex),"nonself_canonical_pages":len(flags["nonself_canonical"]),"duplicate_titles":len(dup_titles),"duplicate_canonicals":len(dup_canons)},
"missing_references":missing_sorted,
"missing_sitemap_targets":missing_sitemap_targets,
"noindex":noindex,
"nonself_canonical":flags["nonself_canonical"],
"duplicate_canonicals":dup_canons,
"duplicate_titles":dup_titles,
"html_not_in_sitemap":html_not_in_sitemap,
"missing_canonicals":missing_canonicals,
"empty_titles":empty_titles,
"h1_missing":h1_missing,
"css_missing":{k:sorted(v) for k,v in css_missing.items()},
"flags":dict(flags)
}
Path("site-integrity-report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
print("SITE_INTEGRITY_SUMMARY "+json.dumps(report["counts"],ensure_ascii=False))
print("MISSING_REFERENCES_TOP_80")
for row in missing_sorted[:80]:
    print(json.dumps(row,ensure_ascii=False))
for name in ("missing_sitemap_targets","noindex","nonself_canonical","duplicate_canonicals","duplicate_titles","css_missing"):
    print(name.upper(),json.dumps(report[name],ensure_ascii=False)[:12000])
