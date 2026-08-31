from __future__ import annotations

import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
POSTS_JSON = ROOT / 'data' / 'posts.json'
POSTS_DIR = ROOT / 'posts'

FAMILY_WORDS = (
    '협의이혼', '재판이혼', '재판상이혼', '이혼소송', '이혼신고', '숙려기간',
    '친권', '양육권', '양육비', '면접교섭', '가사사건', '개명', '성년후견', '한정후견'
)

REAL_ESTATE_WORDS = (
    '재산분할등기', '소유권이전', '부동산 이전', '부동산이전', '이전등기',
    '등기절차', '등기 필요서류', '취득세', '등기신청', '등기원인', '집행문'
)


def classify(title: str, current: str) -> str:
    t = re.sub(r'\s+', ' ', str(title or '')).strip()

    # '이혼'이라는 단어 하나만으로 가사 처리하지 않는다.
    # 부동산 이전·등기가 핵심인 제목이면 부동산등기를 우선한다.
    if any(word in t for word in REAL_ESTATE_WORDS):
        return '부동산등기'

    # 실제 이혼절차 자체가 핵심인 경우에만 가사로 분류한다.
    if any(word in t for word in FAMILY_WORDS):
        return '가사'

    return current


def patch_html(slug: str, category: str) -> bool:
    path = POSTS_DIR / f"{slug.replace('.html', '')}.html"
    if not path.exists():
        return False

    text = path.read_text(encoding='utf-8', errors='replace')
    soup = BeautifulSoup(text, 'html.parser')
    changed = False

    meta = soup.select_one('meta[name="dg-category"]')
    if meta is not None and meta.get('content') != category:
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

    for post in posts:
        old = str(post.get('category') or '')
        new = classify(post.get('title', ''), old)
        if new == old:
            continue
        post['category'] = new
        changed += 1
        if patch_html(str(post.get('slug') or ''), new):
            html_changed += 1
        print('CATEGORY_FIX', post.get('slug'), old, '->', new, post.get('title'))

    if changed:
        POSTS_JSON.write_text(json.dumps(posts, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    print('DIVORCE_CATEGORY_FIX', 'posts='+str(changed), 'html='+str(html_changed))


if __name__ == '__main__':
    main()
