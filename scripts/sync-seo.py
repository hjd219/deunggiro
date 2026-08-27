from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS_JSON = ROOT / "data" / "posts.json"
POSTS_HTML = ROOT / "posts.html"
SITEMAP = ROOT / "sitemap.xml"
BASE = "https://www.deunggiro.kr"

STATIC_URLS = [
    ("/", "1.0", "weekly"),
    ("/inheritance.html", "0.9", "monthly"),
    ("/corporate.html", "0.9", "monthly"),
    ("/realestate.html", "0.9", "monthly"),
    ("/renunciation.html", "0.9", "monthly"),
    ("/family.html", "0.9", "monthly"),
    ("/acquisition-calculator.html", "0.8", "monthly"),
    ("/corporate-calculator.html", "0.8", "monthly"),
    ("/divorce-calculator.html", "0.8", "monthly"),
    ("/posts.html", "0.8", "weekly"),
]

FOOTER_STYLE = r'''
/* HOME_FOOTER_SYNC */
.contact{background:#172840;color:#fff;padding:54px 0!important}
.contact-grid{display:grid!important;grid-template-columns:1fr auto!important;gap:30px!important;align-items:center!important}
.contact .label{color:#9fd9f4!important;font-size:12px!important;font-weight:900!important;letter-spacing:1.3px!important}
.contact h2{font-size:34px!important;line-height:1.35!important;letter-spacing:-1.2px!important;margin:5px 0 10px!important;color:#fff!important}
.contact p{color:#cbd5e1!important;margin:0!important;font-size:14px!important}
.contact .phone{font-size:31px!important;font-weight:900!important;color:#fff!important;text-decoration:none!important}
.footer{background:#172840!important;color:#c9d5e7!important;border-top:1px solid rgba(255,255,255,.1)!important;padding:38px 0 44px!important;font-size:13px!important}
.footer-route-grid{display:grid!important;grid-template-columns:minmax(0,1.15fr) minmax(360px,.85fr)!important;gap:72px!important;align-items:start!important}
.footer-brand{font-size:24px!important;color:#fff!important;font-weight:900!important;margin-bottom:5px!important}
.footer-office{font-size:16px!important;color:#e8eef8!important;font-weight:800!important;margin-bottom:17px!important}
.footer-info{font-size:14px!important;line-height:2!important}
.footer-info strong{display:inline-block!important;width:44px!important;color:#fff!important;margin-right:0!important}
.footer-channel-row{display:flex!important;align-items:center!important;gap:7px!important;flex-wrap:wrap!important;margin-top:14px!important}
.footer-social{display:inline-flex!important;align-items:center!important;gap:6px!important;color:#fff!important;font-size:13px!important;font-weight:800!important}
.footer-social-icon{display:inline-flex!important;align-items:center!important;justify-content:center!important;width:19px!important;height:19px!important;border-radius:5px!important;color:#fff!important;font-size:11px!important;font-weight:900!important}
.naver-icon{background:#03c75a!important}.youtube-icon{background:#ff0033!important}
.footer-social-dot{color:#8191aa!important}
.footer-route{padding-left:34px!important;border-left:1px solid rgba(255,255,255,.13)!important}
.footer-route-title{color:#fff!important;font-size:21px!important;font-weight:900!important;letter-spacing:-.7px!important;margin-bottom:3px!important}
.footer-route-sub{color:#9fb9df!important;font-size:12px!important;font-weight:800!important;margin-bottom:16px!important}
.footer-route-list{display:grid!important;gap:9px!important;font-size:13px!important;line-height:1.55!important}
.footer-route-list>div{display:grid!important;grid-template-columns:24px 1fr!important;gap:7px!important;align-items:start!important}
.footer-route-list b{color:#fff!important;margin-right:7px!important}
.footer-route-actions{display:flex!important;gap:8px!important;flex-wrap:wrap!important;margin-top:17px!important}
.footer-route-actions a{display:inline-flex!important;align-items:center!important;min-height:37px!important;padding:0 12px!important;border:1px solid rgba(255,255,255,.22)!important;border-radius:7px!important;color:#fff!important;font-size:11px!important;font-weight:900!important;background:rgba(255,255,255,.045)!important;text-decoration:none!important}
@media(max-width:800px){
 .contact{padding:36px 0!important}.contact-grid{grid-template-columns:1fr!important;gap:18px!important}.contact h2{font-size:25px!important}.contact .phone{font-size:24px!important}
 .footer{padding:28px 0 32px!important}.footer-route-grid{grid-template-columns:1fr!important;gap:24px!important}.footer-route{padding-left:0!important;padding-top:24px!important;border-left:0!important;border-top:1px solid rgba(255,255,255,.13)!important}.footer-info{font-size:12px!important}.footer-route-title{font-size:18px!important}.footer-route-list{font-size:12px!important}
}
'''

FOOTER_HTML = r'''
<section class="contact"><div class="container contact-grid"><div><div class="label">CONSULTATION</div><h2>복잡한 등기절차, 등기로에서 확인하세요.</h2><p>상속 · 법인 · 부동산 등 필요한 절차와 준비서류를 확인할 수 있습니다.</p></div><a class="phone" href="tel:0324251500">032-425-1500</a></div></section>
<footer class="footer"><div class="container footer-route-grid"><div><div class="footer-brand">등기로</div><div class="footer-office">현재두 법무사 사무소</div><div class="footer-info"><div><strong>주소</strong> 인천 미추홀구 경원대로 873, 201호(주안동, 인성빌딩) · 인천가정법원 옆</div><div><strong>전화</strong> <a href="tel:0324251500" style="color:#fff;font-weight:800">032-425-1500</a></div></div><div class="footer-channel-row"><a class="footer-social" href="https://blog.naver.com/hjd21" target="_blank" rel="noopener noreferrer"><span class="footer-social-icon naver-icon">N</span>네이버 블로그</a><span class="footer-social-dot">·</span><a class="footer-social" href="https://youtube.com/channel/UCHs3WtBFAiV8bOsQUB-n-Ew?si=tTUgTZWRKg98bvYa" target="_blank" rel="noopener noreferrer"><span class="footer-social-icon youtube-icon">▶</span>유튜브</a></div></div><div class="footer-route"><div class="footer-route-title">찾아오시는 길</div><div class="footer-route-sub">인천가정법원 옆 · 인성빌딩 2층</div><div class="footer-route-list"><div><span>🚇</span><span><b>1호선</b> 주안역·간석역 1번 출구 도보 이용</span></div><div><span>🚇</span><span><b>인천지하철 2호선</b> 석바위시장역 하차 후 석바위 지하상가 5번 출구 도보 이용</span></div><div><span>⏱</span><span><b>도보시간</b> 간석역 약 15분 · 주안역 약 19분 · 석바위시장역 약 12분</span></div></div><div class="footer-route-actions"><a href="https://map.naver.com/p/search/%EC%9D%B8%EC%B2%9C%20%EB%AF%B8%EC%B6%94%ED%99%80%EA%B5%AC%20%EA%B2%BD%EC%9B%90%EB%8C%80%EB%A1%9C%20873" target="_blank" rel="noopener noreferrer">네이버 지도에서 보기 →</a><a href="tel:0324251500">방문문의 032-425-1500</a></div></div></div></footer>
'''


def load_posts():
    data = json.loads(POSTS_JSON.read_text(encoding="utf-8-sig"))
    if isinstance(data, dict):
        data = data.get("posts", [])
    if not isinstance(data, list):
        raise ValueError("data/posts.json must be an array")
    return data


def card(post):
    title = html.escape(str(post.get("title", "")))
    category = html.escape(str(post.get("category", "")))
    date = html.escape(str(post.get("date", "")))
    summary = html.escape(str(post.get("summary", "")))
    slug = re.sub(r"\.html$", "", str(post.get("slug", "")))
    href = f"/posts/{html.escape(slug)}.html"
    thumb = str(post.get("thumbnail", "") or "")
    if thumb:
        thumb_html = f'<img class="post-thumb" src="{html.escape(thumb)}" alt="{title}" loading="lazy">'
        cls = "post-card"
    else:
        thumb_html = ""
        cls = "post-card no-thumb"
    summary_html = f"<p>{summary}</p>" if summary else ""
    return f'<a class="{cls}" href="{href}">{thumb_html}<div class="post-content"><div class="post-meta"><span class="badge">{category}</span>{date}</div><h3>{title}</h3>{summary_html}</div></a>'


def sync_posts_html(posts):
    source = POSTS_HTML.read_text(encoding="utf-8")
    static_cards = "\n".join(card(p) for p in posts if p.get("slug"))
    replacement = '<div id="posts" class="post-grid">\n<!-- SEO_STATIC_POSTS_START -->\n' + static_cards + '\n<!-- SEO_STATIC_POSTS_END -->\n</div>'
    pattern = re.compile(r'<div id="posts" class="post-grid">.*?</div>\s*<div id="pagination"', re.S)
    if not pattern.search(source):
        raise RuntimeError("posts.html post grid not found")
    source = pattern.sub(replacement + '\n<div id="pagination"', source, count=1)

    if "/* HOME_FOOTER_SYNC */" not in source:
        source = source.replace("</style>", FOOTER_STYLE + "\n</style>", 1)
    else:
        source = re.sub(r'/\* HOME_FOOTER_SYNC \*/.*?(?=</style>)', FOOTER_STYLE.strip() + "\n", source, flags=re.S)

    source = re.sub(r'<section class="contact">.*?</footer>', FOOTER_HTML.strip(), source, count=1, flags=re.S)
    POSTS_HTML.write_text(source, encoding="utf-8")


def sitemap_entry(url, lastmod, priority, changefreq):
    return "  <url>\n" + f"    <loc>{html.escape(url)}</loc>\n" + f"    <lastmod>{html.escape(lastmod)}</lastmod>\n" + f"    <changefreq>{changefreq}</changefreq>\n" + f"    <priority>{priority}</priority>\n" + "  </url>"


def sync_sitemap(posts):
    latest = max((str(p.get("date", "")) for p in posts if p.get("date")), default="")
    entries = [sitemap_entry(BASE + path, latest or "2026-08-27", priority, changefreq) for path, priority, changefreq in STATIC_URLS]
    seen = set()
    for p in posts:
        slug = re.sub(r"\.html$", "", str(p.get("slug", "")))
        if not slug or slug in seen:
            continue
        seen.add(slug)
        date = str(p.get("date", "")) or latest or "2026-08-27"
        entries.append(sitemap_entry(f"{BASE}/posts/{slug}.html", date, "0.7", "monthly"))
    SITEMAP.write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(entries) + '\n</urlset>\n', encoding="utf-8")


def main():
    posts = sorted(load_posts(), key=lambda p: str(p.get("date", "")), reverse=True)
    sync_posts_html(posts)
    sync_sitemap(posts)
    print(f"Synced {len(posts)} posts")


if __name__ == "__main__":
    main()
