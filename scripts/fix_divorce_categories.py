from __future__ import annotations

# CATEGORY_AUDIT_V2

import json
from pathlib import Path

from bs4 import BeautifulSoup

from category_rules import classify_title_with_reason

ROOT = Path(__file__).resolve().parents[1]
POSTS_JSON = ROOT / 'data' / 'posts.json'
POSTS_DIR = ROOT / 'posts'


def patch_html(slug: str, category: str) -> bool:
    path = POSTS_DIR / f"{str(slug or '').replace('.html', '')}.html"
    if not path.exists():
        return False

    original = path.read_text(encoding='utf-8', errors='replace')
    soup = BeautifulSoup(original, 'html.parser')
    changed = False

    meta = soup.select_one('meta[name="dg-category"]')
    if meta is None:
        meta = soup.new_tag('meta')
        meta['name'] = 'dg-category'
        meta['content'] = category
        if soup.head:
            soup.head.append(meta)
            changed = True
    elif meta.get('content') != category:
        meta['content'] = category
        changed = True

    badge = soup.select_one('.post-meta .badge')
    if badge is not None and badge.get_text(strip=True) != category:
        badge.string = category
        changed = True

    if changed:
        path.write_text(str(soup), encoding='utf-8')
    return changed


def main() -> None:
    posts = json.loads(POSTS_JSON.read_text(encoding='utf-8'))
    changed = 0
    html_changed = 0
    audited = 0
    reasons: dict[str, int] = {}

    for post in posts:
        audited += 1
        old = str(post.get('category') or '').strip()
        slug = str(post.get('slug') or '').strip()
        new, reason = classify_title_with_reason(post.get('title', ''), old)
        reasons[reason] = reasons.get(reason, 0) + 1

        if new == old:
            continue

        post['category'] = new
        changed += 1
        if patch_html(slug, new):
            html_changed += 1
        print('CATEGORY_FIX', slug, old or '(없음)', '->', new, '[' + reason + ']', post.get('title'))

    if changed:
        POSTS_JSON.write_text(json.dumps(posts, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    print('CATEGORY_AUDIT_TOTAL', audited)
    print('CATEGORY_FIX_TOTAL', 'posts='+str(changed), 'html='+str(html_changed))
    print('CATEGORY_REASON_COUNTS', json.dumps(reasons, ensure_ascii=False, sort_keys=True))


if __name__ == '__main__':
    main()
