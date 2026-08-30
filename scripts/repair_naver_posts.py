import html
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
POSTS_JSON = ROOT / 'data' / 'posts.json'
POSTS_DIR = ROOT / 'posts'

RULES = [
    ('상속포기·한정승인', ('상속포기', '한정승인', '특별한정승인', '상속채무')),
    ('상속재산분할', ('상속재산분할', '상속분쟁', '기여분', '특별수익')),
    ('부동산등기', ('신탁', '가압류', '근저당', '가등기', '전세권', '소유권이전', '부동산', '매매', '증여', '등기권리증')),
    ('법인등기', ('법인', '주식회사', '유한회사', '대표이사', '이사변경', '감사', '주주', '본점이전', '자본금', '증자', '감자', '상호변경', '목적변경', '해산', '청산')),
    ('가사', ('이혼', '개명', '성년후견', '한정후견', '친권', '양육비')),
    ('상속등기', ('상속등기', '대습상속', '상속취득세', '상속인', '상속지분', '상속재산', '유언', '사망')),
]


def category(text):
    text = re.sub(r'\s+', ' ', text or '')
    for c, words in RULES:
        if any(w in text for w in words):
            return c
    return '기타'


def remove_source_note(s):
    s = re.sub(r'<p[^>]*class=["\'][^"\']*source-note[^"\']*["\'][^>]*>.*?</p>', '', s, flags=re.I | re.S)
    s = re.sub(r'<p[^>]*>\s*네이버 블로그에 작성한 내용을.*?원문 보기.*?</p>', '', s, flags=re.I | re.S)
    return s


def remove_preview_components(s):
    soup = BeautifulSoup(s, 'html.parser')
    removed = 0

    # 이미 저장된 HTML 안의 네이버 링크카드/OG 링크 잔재를 통째로 제거한다.
    for el in list(soup.find_all(True)):
        if el.parent is None:
            continue
        marker = ' '.join([
            str(el.get('id') or ''),
            ' '.join(el.get('class') or []),
        ]).lower()
        if any(x in marker for x in ('se-oglink', 'se-module-oglink', 'oglink', 'link-preview', 'link_preview')):
            el.decompose()
            removed += 1

    # 도메인만 남은 문단과 대표적인 링크카드 묶음도 제거한다.
    bare_domain = re.compile(r'^(?:https?://)?(?:www\.|m\.)?[a-z0-9-]+(?:\.[a-z0-9-]+)+(?:/[^\s]*)?$', re.I)
    for p in list(soup.find_all('p')):
        if p.parent is None:
            continue
        text = ' '.join(p.stripped_strings).strip()
        if bare_domain.fullmatch(re.sub(r'\s+', '', text)):
            prev = p.find_previous_sibling()
            if prev is not None:
                prev_text = ' '.join(prev.stripped_strings).strip()
                if len(prev_text) >= 160 or any(x in prev_text for x in ('같이 보면 좋은 글', '요약표입니다', '좌우로 스크롤 가능합니다')):
                    prev.decompose()
            p.decompose()
            removed += 1

    return str(soup), removed


def repair_local(post):
    slug = str(post.get('slug', '')).replace('.html', '')
    if not slug:
        return False, 0
    page = POSTS_DIR / f'{slug}.html'
    if not page.exists():
        return False, 0

    original = page.read_text(encoding='utf-8')
    s = remove_source_note(original)
    s, removed = remove_preview_components(s)

    soup = BeautifulSoup(s, 'html.parser')
    article = soup.select_one('.article-body')
    body_text = ' '.join(article.stripped_strings) if article else ''
    title = str(post.get('title', ''))
    new_cat = category(title + ' ' + body_text[:1200])
    post['category'] = new_cat

    escaped_cat = html.escape(new_cat)
    s = re.sub(r'(<meta\s+name=["\']dg-category["\']\s+content=["\'])[^"\']*', r'\1' + escaped_cat, s, count=1, flags=re.I)
    s = re.sub(r'(<span\s+class=["\']badge["\']>).*?(</span>)', r'\1' + escaped_cat + r'\2', s, count=1, flags=re.I | re.S)

    # 기존에 잘못 들어간 대표이미지 요소는 제거하고 뒤 단계에서 썸네일을 다시 관리한다.
    s = re.sub(r'<figure[^>]+id=["\']dg-post-hero-image["\'][^>]*>.*?</figure>', '', s, flags=re.I | re.S)
    s = re.sub(r'<style[^>]+id=["\']dg-post-hero-style["\'][^>]*>.*?</style>', '', s, flags=re.I | re.S)

    if s != original:
        page.write_text(s, encoding='utf-8')
        return True, removed
    return False, removed


def main():
    posts = json.loads(POSTS_JSON.read_text(encoding='utf-8'))
    done = 0
    preview_removed = 0

    for post in posts:
        if post.get('source') != 'naver-blog':
            continue
        changed, removed = repair_local(post)
        if changed:
            done += 1
        preview_removed += removed

    POSTS_JSON.write_text(json.dumps(posts, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'LOCAL_REPAIRED={done} PREVIEW_REMOVED={preview_removed}', flush=True)


if __name__ == '__main__':
    main()
