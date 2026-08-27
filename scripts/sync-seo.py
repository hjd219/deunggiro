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
        thumb_html = (
            f'<img class="post-thumb" src="{html.escape(thumb)}" '
            f'alt="{title}" loading="lazy">'
        )
        cls = "post-card"
    else:
        thumb_html = ""
        cls = "post-card no-thumb"

    summary_html = f"<p>{summary}</p>" if summary else ""
    return (
        f'<a class="{cls}" href="{href}">'
        f'{thumb_html}<div class="post-content">'
        f'<div class="post-meta"><span class="badge">{category}</span>{date}</div>'
        f'<h3>{title}</h3>{summary_html}</div></a>'
    )


def sync_posts_html(posts):
    source = POSTS_HTML.read_text(encoding="utf-8")
    static_cards = "\n".join(card(p) for p in posts if p.get("slug"))
    replacement = (
        '<div id="posts" class="post-grid">\n'
        '<!-- SEO_STATIC_POSTS_START -->\n'
        f'{static_cards}\n'
        '<!-- SEO_STATIC_POSTS_END -->\n'
        '</div>'
    )

    pattern = re.compile(
        r'<div id="posts" class="post-grid">.*?</div>\s*<div id="pagination"',
        re.S,
    )
    if not pattern.search(source):
        raise RuntimeError("posts.html post grid not found")

    source = pattern.sub(replacement + '\n<div id="pagination"', source, count=1)
    POSTS_HTML.write_text(source, encoding="utf-8")


def sitemap_entry(url, lastmod, priority, changefreq):
    return (
        "  <url>\n"
        f"    <loc>{html.escape(url)}</loc>\n"
        f"    <lastmod>{html.escape(lastmod)}</lastmod>\n"
        f"    <changefreq>{changefreq}</changefreq>\n"
        f"    <priority>{priority}</priority>\n"
        "  </url>"
    )


def sync_sitemap(posts):
    latest = max((str(p.get("date", "")) for p in posts if p.get("date")), default="")
    entries = []
    for path, priority, changefreq in STATIC_URLS:
        lastmod = latest or "2026-08-27"
        entries.append(sitemap_entry(BASE + path, lastmod, priority, changefreq))

    seen = set()
    for p in posts:
        slug = re.sub(r"\.html$", "", str(p.get("slug", "")))
        if not slug or slug in seen:
            continue
        seen.add(slug)
        date = str(p.get("date", "")) or latest or "2026-08-27"
        entries.append(
            sitemap_entry(f"{BASE}/posts/{slug}.html", date, "0.7", "monthly")
        )

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(entries)
        + '\n</urlset>\n'
    )
    SITEMAP.write_text(xml, encoding="utf-8")


def main():
    posts = load_posts()
    sync_posts_html(posts)
    sync_sitemap(posts)
    print(f"Synced {len(posts)} posts")


if __name__ == "__main__":
    main()
