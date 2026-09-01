from __future__ import annotations

import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
POSTS_JSON = ROOT / 'data' / 'posts.json'
POSTS_DIR = ROOT / 'posts'

CORPORATE_WORDS = (
    '법인', '주식회사', '유한회사', '유한책임회사', '대표이사', '이사', '감사',
    '주주', '주주총회', '이사회', '본점이전', '상호변경', '목적변경', '자본금',
    '증자', '감자', '가수금', '설립등기', '변경등기'
)

RENUNCIATION_WORDS = (
    '상속포기', '한정승인', '특별한정승인', '상속채무', '상속빚', '상속 빚'
)

RENUNCIATION_FOCUS_PHRASES = (
    '상속포기 절차', '상속포기 신청', '상속포기·한정승인', '상속포기 한정승인',
    '한정승인 절차', '한정승인 신청', '특별한정승인', '상속포기 전', '상속포기 시',
    '[인천 상속포기]', '[상속포기', '[인천 한정승인]', '[한정승인'
)

INHERITANCE_DIVISION_WORDS = (
    '상속재산분할', '상속분쟁', '기여분', '특별수익', '유류분',
    '상속회복청구', '상속재산분할심판'
)

STRONG_INHERITANCE_WORDS = (
    '상속등기', '상속절차', '대습상속', '상속취득세', '상속지분',
    '상속인 자격', '상속인자격', '상속재산 조회', '상속재산조회',
    '상속예금', '상속 주식', '상속주식', '상속인 명의', '상속인명의',
    '상속순위', '누가 상속인', '상속인은 누구'
)

INHERITANCE_CONTEXT_WORDS = (
    '상속인', '상속재산', '유언', '유언공증',
    '부모님 사망', '부모 사망', '남편 사망', '아내 사망', '배우자 사망',
    '형제 사망', '자녀 사망'
)

FAMILY_WORDS = (
    '협의이혼', '재판이혼', '재판상이혼', '이혼소송', '이혼신고', '숙려기간',
    '친권', '양육권', '양육비', '면접교섭', '가사사건', '개명', '성년후견',
    '한정후견', '미성년후견', '특별대리인'
)

REAL_ESTATE_WORDS = (
    '근저당', '전세권', '등기권리증', '매매', '증여', '부동산', '소유권이전',
    '부동산 이전', '부동산이전', '이전등기', '취득세', '재산분할등기'
)

STRONG_REAL_ESTATE_PHRASES = (
    '부동산 등기 취득세', '부동산등기 취득세', '부동산 이전 절차', '부동산 이전절차',
    '부동산이전 절차', '부동산이전절차', '취득세율 총정리', '취득세 총정리',
    '매매·상속·증여', '매매 상속 증여', '증여·상속·이혼 재산분할',
    '이혼 재산분할등기', '재산분할등기 부동산'
)

SLUG_OVERRIDES = {
    'naver-224347168343': '부동산등기',
    'inheritance-gift-real-estate-acquisition-tax-property-division-1xfulg': '부동산등기',
    'naver-224397194690': '상속등기',
    'inheritance-registration-acquisition-tax-incheon-procedure-doc-v9aban': '상속등기',
    'naver-224331473807': '상속등기',
    'naver-224337740704': '상속등기',
    'naver-224395763010': '상속등기',
    'naver-224376060472': '상속등기',
    'inheritance-registration-renunciation-limited-acceptance-inche-15yen8': '상속등기',
}


def has_any(text: str, words: tuple[str, ...]) -> bool:
    return any(word in text for word in words)


def is_inheritance_overview(text: str) -> bool:
    # 사망 후 전체 흐름을 설명하는 글은 제목에 상속포기가 함께 있어도 상속등기로 묶는다.
    if '상속등기' in text and '상속절차' in text:
        return True
    if '상속등기' in text and ('해야 할 일' in text or '총정리' in text) and has_any(text, INHERITANCE_CONTEXT_WORDS):
        return True
    return False


def classify(title: str, current: str, slug: str = '') -> str:
    slug = str(slug or '').replace('.html', '')
    if slug in SLUG_OVERRIDES:
        return SLUG_OVERRIDES[slug]

    t = re.sub(r'\s+', ' ', str(title or '')).strip()

    # 1. 법인은 명확한 독립 업무라 최우선.
    if has_any(t, CORPORATE_WORDS):
        return '법인등기'

    # 2. 제목 자체가 상속등기/상속절차 전체 흐름을 약속하면 상속포기 단어가 있어도 상속등기.
    if is_inheritance_overview(t):
        return '상속등기'

    # 3. 명시적인 상속등기 제목은 취득세·부동산 단어보다 우선.
    if '[인천 상속등기]' in t or '[상속등기]' in t or t.startswith('상속등기'):
        return '상속등기'

    # 4. 상속포기·한정승인 자체가 제목의 핵심인 글.
    if has_any(t, RENUNCIATION_FOCUS_PHRASES):
        return '상속포기·한정승인'

    # 5. 부동산 이전·취득세가 제목의 핵심인 복합 글.
    if has_any(t, STRONG_REAL_ESTATE_PHRASES):
        return '부동산등기'

    # 6. 상속재산분할·분쟁은 별도 카테고리.
    if has_any(t, INHERITANCE_DIVISION_WORDS):
        return '상속재산분할'

    # 7. 상속절차/상속등기/상속인 판단이 명시되면 친권·이혼 같은 배경 단어보다 상속 우선.
    if has_any(t, STRONG_INHERITANCE_WORDS):
        return '상속등기'

    # 8. 포기·한정승인 관련 단어가 남아 있는 경우.
    if has_any(t, RENUNCIATION_WORDS):
        return '상속포기·한정승인'

    # 9. 일반적인 부동산 이전·취득세·매매·증여 글.
    if has_any(t, REAL_ESTATE_WORDS):
        return '부동산등기'

    # 10. 실제 친권·후견·이혼절차 자체가 핵심이면 가사.
    if has_any(t, FAMILY_WORDS):
        return '가사'

    # 11. 그 밖의 사망·상속 문맥은 상속등기.
    if has_any(t, INHERITANCE_CONTEXT_WORDS):
        return '상속등기'

    # 12. 연락두절/협조거부라는 단어만으로 분할로 보내지 않는다.
    if ('상속' in t and ('협조거부' in t or '연락두절' in t) and ('협의' in t or '분할' in t)):
        return '상속재산분할'

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
        slug = str(post.get('slug') or '')
        new = classify(post.get('title', ''), old, slug)
        if new == old:
            continue
        post['category'] = new
        changed += 1
        if patch_html(slug, new):
            html_changed += 1
        print('CATEGORY_FIX', slug, old, '->', new, post.get('title'))

    if changed:
        POSTS_JSON.write_text(json.dumps(posts, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    print('CATEGORY_FIX_TOTAL', 'posts='+str(changed), 'html='+str(html_changed))


if __name__ == '__main__':
    main()
