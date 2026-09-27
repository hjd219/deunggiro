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
        core=soup.select_one(".seo-core-link a[href]")
        # 대표 핵심글 자체이거나 기타 카테고리는 자기 자신 링크를 만들지 않으므로 core-link가 없어도 정상이다.
        if not core and str(post.get("category","")).strip() not in ("기타",):
            core_marker=soup.find(string=lambda s:s and "SEO_CORE_LINK_START" in str(s))
            if not core_marker: issues.append("core-link-marker")
        related=soup.select(".seo-related-posts a[href]")
        if len(related)!=3: issues.append(f"related-links={len(related)}")
        if f"<loc>{expected}</loc>" not in sitemap: issues.append("sitemap")
        category=str(post.get("category","")).strip()
        expected_hub={"상속등기":"/inheritance.html","상속재산분할":"/inheritance.html","상속포기·한정승인":"/renunciation.html","법인등기":"/corporate.html","부동산등기":"/realestate.html","가사":"/family.html","기타":"/posts.html"}.get(category,"/posts.html")
        expected_hub_url=BASE+expected_hub
        breadcrumb_ok=False
        for tag in soup.find_all("script",attrs={"type":"application/ld+json"}):
            raw=tag.string or tag.get_text() or ""
            if '"@type":"BreadcrumbList"' in raw and expected_hub_url in raw:
                breadcrumb_ok=True; break
        if not breadcrumb_ok: issues.append("breadcrumb-jsonld-hub")
        ogurl=soup.find("meta",attrs={"property":re.compile("^og:url$",re.I)})
        if not ogurl or str(ogurl.get("content","")).strip()!=expected: issues.append("og:url")
        if issues: bad.append(f"{slug}:"+",".join(issues))
    static_expected=[
        "/", "/inheritance.html", "/inheritance-division.html", "/inheritance-minor-heir.html",
        "/inheritance-missing-heir.html", "/inheritance-overseas-heir.html", "/inheritance-substitute-succession.html",
        "/corporate.html", "/realestate.html", "/renunciation.html",
        "/renunciation-after-procedure.html", "/renunciation-limited-acceptance-liquidation.html",
        "/renunciation-death-insurance.html", "/renunciation-deceased-deposit.html",
        "/family.html", "/acquisition-calculator.html", "/corporate-calculator.html", "/posts.html",
    ]
    for rel in static_expected:
        loc=BASE + rel
        if f"<loc>{loc}</loc>" not in sitemap: bad.append(f"STATIC_SITEMAP_MISSING:{rel}")
    for rel in ("/renunciation-after.html","/limited-acceptance-liquidation.html"):
        if f"<loc>{BASE + rel}</loc>" in sitemap: bad.append(f"STATIC_SITEMAP_LEGACY:{rel}")
    legacy_full=[]
    for page in sorted((ROOT / "posts").glob("*.html")):
        txt=page.read_text(encoding="utf-8", errors="ignore")
        if "전체 안내" in txt:
            legacy_full.append((page.stem, txt.count("전체 안내")))
    print("LEGACY_FULL_GUIDE_AUDIT", "posts=", len(legacy_full), "occurrences=", sum(n for _,n in legacy_full))
    if legacy_full:
        for slug,n in legacy_full[:100]: print("LEGACY_FULL_GUIDE", slug, n)
        bad.extend(f"LEGACY_FULL_GUIDE:{slug}:{n}" for slug,n in legacy_full)

    print(f"SEO_QUALITY_GATE checked={checked} bad={len(bad)}")
    if bad:
        print("\n".join(bad[:100]))
        if len(bad)>100: print(f"... 외 {len(bad)-100}건")
        raise SystemExit(1)


if __name__=="__main__":
    main()
