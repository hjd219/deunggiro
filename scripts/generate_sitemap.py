from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
POSTS_JSON = ROOT / 'data' / 'posts.json'
SITEMAP = ROOT / 'sitemap.xml'
BASE = 'https://www.deunggiro.kr'
TODAY = date.today().isoformat()

STATIC = [
    ('/', 'weekly', '1.0'),
    ('/inheritance.html', 'monthly', '0.9'),
    ('/corporate.html', 'monthly', '0.9'),
    ('/realestate.html', 'monthly', '0.9'),
    ('/renunciation.html', 'monthly', '0.9'),
    ('/family.html', 'monthly', '0.9'),
    ('/acquisition-calculator.html', 'monthly', '0.8'),
    ('/corporate-calculator.html', 'monthly', '0.8'),
    ('/divorce-calculator.html', 'monthly', '0.8'),
    ('/posts.html', 'weekly', '0.8'),
]


def url_block(loc: str, lastmod: str, changefreq: str, priority: str) -> str:
    return (
        '  <url>\n'
        f'    <loc>{escape(loc)}</loc>\n'
        f'    <lastmod>{escape(lastmod)}</lastmod>\n'
        f'    <changefreq>{changefreq}</changefreq>\n'
        f'    <priority>{priority}</priority>\n'
        '  </url>'
    )


def main() -> None:
    posts = json.loads(POSTS_JSON.read_text(encoding='utf-8'))
    blocks = [url_block(BASE + path, TODAY, freq, priority) for path, freq, priority in STATIC]
    seen = set()
    added = 0
    for post in posts:
        slug = str(post.get('slug', '')).strip().replace('.html', '')
        if not slug or slug in seen:
            continue
        page = ROOT / 'posts' / f'{slug}.html'
        if not page.exists():
            continue
        seen.add(slug)
        lastmod = str(post.get('date') or post.get('website_date') or TODAY).strip() or TODAY
        blocks.append(url_block(f'{BASE}/posts/{slug}.html', lastmod, 'monthly', '0.7'))
        added += 1
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(blocks) + '\n</urlset>\n'
    SITEMAP.write_text(xml, encoding='utf-8')
    print(f'sitemap generated: static={len(STATIC)}, posts={added}, total={len(STATIC)+added}')


if __name__ == '__main__':
    main()
