from __future__ import annotations

import json
import re
import subprocess
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
POSTS_JSON = ROOT / 'data' / 'posts.json'
SITEMAP = ROOT / 'sitemap.xml'
BASE = 'https://www.deunggiro.kr'
TODAY = date.today().isoformat()


def git_lastmod(path: Path, fallback: str = '') -> str:
    """Use the file's actual last Git modification date; never stamp unchanged URLs with today."""
    try:
        rel = path.relative_to(ROOT).as_posix()
        out = subprocess.check_output(
            ['git', 'log', '-1', '--format=%ad', '--date=short', '--', rel],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        if re.fullmatch(r'\d{4}-\d{2}-\d{2}', out):
            return out
    except Exception:
        pass
    value = str(fallback or '').strip()
    return value if re.fullmatch(r'\d{4}-\d{2}-\d{2}', value) else TODAY

STATIC = [
    ('/', 'weekly', '1.0'),
    ('/inheritance.html', 'monthly', '0.9'),
    ('/inheritance-division.html', 'monthly', '0.8'),
    ('/inheritance-minor-heir.html', 'monthly', '0.8'),
    ('/inheritance-missing-heir.html', 'monthly', '0.8'),
    ('/inheritance-overseas-heir.html', 'monthly', '0.8'),
    ('/inheritance-substitute-succession.html', 'monthly', '0.8'),
    ('/corporate.html', 'monthly', '0.9'),
    ('/realestate.html', 'monthly', '0.9'),
    ('/renunciation.html', 'monthly', '0.9'),
    ('/renunciation-after-procedure.html', 'monthly', '0.8'),
    ('/renunciation-limited-acceptance-liquidation.html', 'monthly', '0.8'),
    ('/renunciation-death-insurance.html', 'monthly', '0.8'),
    ('/renunciation-deceased-deposit.html', 'monthly', '0.8'),
    ('/family.html', 'monthly', '0.9'),
    ('/acquisition-calculator.html', 'monthly', '0.8'),
    ('/corporate-calculator.html', 'monthly', '0.8'),
    ('/renunciation-calculator.html', 'monthly', '0.8'),
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
    blocks = [
        url_block(BASE + path, git_lastmod(ROOT / ('index.html' if path == '/' else path.lstrip('/'))), freq, priority)
        for path, freq, priority in STATIC
    ]
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
        stored_date = str(post.get('website_date') or post.get('date') or '').strip()
        # Post HTML is routinely rewritten by SEO/link automation; Git mtime is therefore not a content-modified signal.
        lastmod = stored_date if re.fullmatch(r'\d{4}-\d{2}-\d{2}', stored_date) else git_lastmod(page)
        blocks.append(url_block(f'{BASE}/posts/{slug}.html', lastmod, 'monthly', '0.7'))
        added += 1
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(blocks) + '\n</urlset>\n'
    SITEMAP.write_text(xml, encoding='utf-8')
    print(f'sitemap generated: static={len(STATIC)}, posts={added}, total={len(STATIC)+added}')


if __name__ == '__main__':
    main()
