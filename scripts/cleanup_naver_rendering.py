import json
import re
from pathlib import Path
from bs4 import BeautifulSoup, Tag

ROOT = Path(__file__).resolve().parents[1]
POSTS_JSON = ROOT / 'data' / 'posts.json'
POSTS_DIR = ROOT / 'posts'

DOMAIN_RE = re.compile(r'^(?:m\.)?blog\.naver\.com$', re.I)
PREVIEW_MARKERS = ('oglink', 'link-preview', 'link_preview', 'se-oglink', 'se-module-oglink', 'se-oglink-info')
PREVIEW_HINT_RE = re.compile(r'(\.\.\.|…|“|”|"|네이버 블로그|blog\.naver\.com)', re.I)


def marker_text(tag: Tag) -> str:
    return (' '.join([str(tag.get('id') or ''), ' '.join(tag.get('class') or [])])).lower()


def remove_preview_containers(soup: BeautifulSoup) -> bool:
    changed = False
    for node in list(soup.find_all(True)):
        if node.parent is None:
            continue
        marker = marker_text(node)
        if any(x in marker for x in PREVIEW_MARKERS):
            node.decompose()
            changed = True
    return changed


def remove_inline_naver_cards(soup: BeautifulSoup) -> bool:
    changed = False
    # p/div만 검사한다. span까지 검사하면 같은 카드의 중첩 노드를 반복 탐색해 매우 느려질 수 있다.
    for node in list(soup.find_all(['p', 'div'])):
        if node.parent is None:
            continue
        label = ' '.join(node.stripped_strings).strip()
        if not DOMAIN_RE.fullmatch(label):
            continue
        prev = node.find_previous_sibling()
        node.decompose()
        changed = True
        removed = 0
        while isinstance(prev, Tag) and removed < 2:
            prev_text = ' '.join(prev.stripped_strings).strip()
            prev_prev = prev.find_previous_sibling()
            if prev.name in ('p', 'div', 'blockquote') and len(prev_text) <= 220 and PREVIEW_HINT_RE.search(prev_text):
                prev.decompose()
                changed = True
                removed += 1
                prev = prev_prev
                continue
            break
        if removed and isinstance(prev, Tag) and prev.parent is not None:
            prev_text = ' '.join(prev.stripped_strings).strip()
            if prev.name in ('p', 'h3', 'div') and 2 <= len(prev_text) <= 80:
                if not re.match(r'^\s*\d+\s', prev_text) and not re.search(r'(구간|절차|방법|작성|결정|주의사항|정리)$', prev_text):
                    prev.decompose()
                    changed = True
    return changed


def clean_html(text: str) -> str:
    # 거대한 HTML 전체에 [\s\S]* 정규식을 반복 적용하던 방식을 제거한다.
    # BeautifulSoup으로 한 번만 파싱해 필요한 노드만 삭제한다.
    soup = BeautifulSoup(text, 'html.parser')
    changed = False

    for node in list(soup.select('.source-note')):
        node.decompose()
        changed = True

    changed = remove_preview_containers(soup) or changed

    # '같이 보면 좋은 글'은 네이버에서 풀린 관련글 영역만 제거한다.
    # 등기로 자체 SEO 관련글 마커/섹션은 건드리지 않는다.
    seo_marker = soup.find(string=lambda s: isinstance(s, str) and 'SEO_RELATED_POSTS_START' in s)
    for node in list(soup.find_all(['h2', 'h3', 'p'])):
        if node.parent is None:
            continue
        label = ' '.join(node.stripped_strings).strip()
        if re.fullmatch(r'같이\s*보면\s*좋은\s*글', label):
            cur = node
            while cur is not None:
                nxt = cur.find_next_sibling()
                cur.decompose()
                changed = True
                if nxt is None:
                    break
                # 자체 SEO 관련글 section은 보존
                classes = ' '.join(nxt.get('class') or []) if isinstance(nxt, Tag) else ''
                if 'seo-related-posts' in classes:
                    break
                cur = nxt
            break

    changed = remove_inline_naver_cards(soup) or changed

    if not changed:
        return text
    return str(soup)


def main():
    posts = json.loads(POSTS_JSON.read_text(encoding='utf-8'))
    changed = 0
    checked = 0
    for post in posts:
        if post.get('source') != 'naver-blog':
            continue
        slug = str(post.get('slug', '')).replace('.html', '').strip()
        if not slug:
            continue
        path = POSTS_DIR / f'{slug}.html'
        if not path.exists():
            continue
        checked += 1
        old = path.read_text(encoding='utf-8')
        new = clean_html(old)
        if new != old:
            path.write_text(new, encoding='utf-8')
            changed += 1
            print('CLEANED', slug, flush=True)
    print(f'naver rendering cleanup: checked={checked} changed={changed}', flush=True)


if __name__ == '__main__':
    main()
