from __future__ import annotations

import json
import re
import subprocess
from datetime import date
from pathlib import Path
from xml.etree import ElementTree as ET
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


def save_new_urls_only(blocks: list[str]) -> int:
    """Preserve every existing sitemap entry; append only genuinely new URLs."""
    if not SITEMAP.exists():
        xml = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + '\n'.join(blocks) + '\n</urlset>\n'
        )
        SITEMAP.write_text(xml, encoding='utf-8')
        print(f'sitemap created: urls={len(blocks)}')
        return len(blocks)

    original = SITEMAP.read_text(encoding='utf-8')
    root = ET.fromstring(original)  # Fail rather than silently replace a broken sitemap.
    ns = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
    if root.tag != ns + 'urlset':
        raise ValueError('Unexpected sitemap XML root/namespace')

    known = set()
    for entry in root.findall(ns + 'url'):
        loc = entry.findtext(ns + 'loc')
        if not loc:
            raise ValueError('Existing sitemap entry without loc')
        if loc in known:
            raise ValueError(f'Duplicate URL in existing sitemap: {loc}')
        known.add(loc)

    additions = []
    for block in blocks:
        loc = ET.fromstring(block).findtext('loc')
        if not loc:
            raise ValueError('Generated sitemap entry without loc')
        if loc not in known:
            additions.append(block)
            known.add(loc)

    if not additions:
        print(f'sitemap unchanged: existing_urls={len(known)} new_urls=0')
        return 0

    closing = re.search(r'</urlset>\s*\Z', original)
    if not closing:
        raise ValueError('Missing closing urlset tag in existing sitemap')
    # Insert before the closing element; never reformat/rewrite existing <url> blocks.
    updated = (
        original[:closing.start()]
        + ''.join(block + '\n' for block in additions)
        + original[closing.start():]
    )
    ET.fromstring(updated)
    SITEMAP.write_text(updated, encoding='utf-8')
    print(f'sitemap appended: existing_urls={len(known) - len(additions)} new_urls={len(additions)} total={len(known)}')
    return len(additions)


def main() -> None:
    posts = json.loads(POSTS_JSON.read_text(encoding='utf-8'))
    blocks = [
        url_block(BASE + path, git_lastmod(ROOT / ('index.html' if path == '/' else path.lstrip('/'))), freq, priority)
        for path, freq, priority in STATIC
    ]
    # Pagination documents have real article anchors and self-canonicals.
    # Use Git history for stable modification dates; never date-stamp unchanged pages.
    for paginated in sorted((ROOT / 'posts-pages').glob('*.html')):
        if not re.fullmatch(r'(info|core|case)-[1-9][0-9]*\.html', paginated.name):
            continue
        blocks.append(url_block(f'{BASE}/posts-pages/{paginated.name}', git_lastmod(paginated), 'monthly', '0.5'))
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
        # Per-site policy, post dates always remain the original publication date.
        # Never use website_date, file modification time, or today for posts.
        lastmod = str(post.get('date') or '').strip()
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', lastmod):
            raise ValueError(f'Original publication date missing for post: {slug}')
        blocks.append(url_block(f'{BASE}/posts/{slug}.html', lastmod, 'monthly', '0.7'))
        added += 1
    save_new_urls_only(blocks)



if __name__ == '__main__':
    main()
