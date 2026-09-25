from __future__ import annotations

import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://www.deunggiro.kr"

def main():
    posts=json.loads((ROOT/"data/posts.json").read_text(encoding="utf-8"))
    sitemap=(ROOT/"sitemap.xml").read_text(encoding="utf-8")
    bad=[]; checked=0
    for post in posts:
        slug=str(post.get("slug","")).strip().replace(".html","")
        if not slug: continue
        path=ROOT/"posts"/f"{slug}.html"
        if not path.exists():
            bad.append(f"{slug}:HTML 없음"); continue
        checked+=1
        soup=BeautifulSoup(path.read_text(encoding="utf-8",errors="replace"),"html.parser")
        issues=[]
        title=soup.find("title")
        if not title or not title.get_text(strip=True): issues.append("title")
        desc=soup.find("meta",attrs={"name":re.compile("^description$",re.I)})
        if not desc or not str(desc.get("content","")).strip(): issues.append("description")
        expected=f"{BASE}/posts/{slug}.html"
        canonical=soup.find("link",rel=lambda v:v and "canonical" in (v if isinstance(v,list) else [v]))
        if not canonical or str(canonical.get("href","")).strip()!=expected: issues.append("canonical")
        h1=soup.find_all("h1")
        if len(h1)!=1 or not h1[0].get_text(" ",strip=True): issues.append(f"H1={len(h1)}")
        robots=soup.find("meta",attrs={"name":re.compile("^robots$",re.I)})
        if robots and "noindex" in str(robots.get("content","")).lower(): issues.append("noindex")
        if not soup.select_one(".seo-hub-link a[href]"): issues.append("hub-link")
        if f"<loc>{expected}</loc>" not in sitemap: issues.append("sitemap")
        if issues: bad.append(f"{slug}:"+",".join(issues))
    print(f"SEO_QUALITY_GATE checked={checked} bad={len(bad)}")
    if bad:
        print("\n".join(bad[:100]))
        if len(bad)>100: print(f"... 외 {len(bad)-100}건")
        raise SystemExit(1)

if __name__=="__main__":
    main()
