import json
import re
from pathlib import Path
from bs4 import BeautifulSoup, Tag, Comment

ROOT = Path(__file__).resolve().parents[1]
POSTS_JSON = ROOT / 'data' / 'posts.json'
POSTS_DIR = ROOT / 'posts'

DOMAIN_RE = re.compile(r'^(?:m\.)?blog\.naver\.com$', re.I)
PREVIEW_MARKERS = ('oglink', 'link-preview', 'link_preview', 'se-oglink', 'se-module-oglink', 'se-oglink-info')
PREVIEW_HINT_RE = re.compile(r'(\.\.\.|…|“|”|"|네이버 블로그|blog\.naver\.com)', re.I)
SEO_MARKER_RE = re.compile(r'^\s*SEO_RELATED_POSTS_(?:START|END)\s*$', re.I)


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


def remove_visible_seo_markers(soup: BeautifulSoup) -> bool:
    """SEO_RELATED_POSTS_START/END가 텍스트로 화면에 노출되는 경우만 제거한다.
    HTML 주석 마커는 내부링크 갱신용이므로 보존한다.
    """
    changed = False
    for text_node in list(soup.find_all(string=True)):
        if isinstance(text_node, Comment):
            continue
        if SEO_MARKER_RE.fullmatch(str(text_node)):
            parent = text_node.parent
            if isinstance(parent, Tag) and parent.name in ('p', 'div', 'span') and ' '.join(parent.stripped_strings).strip() == str(text_node).strip():
                parent.decompose()
            else:
                text_node.extract()
            changed = True
    return changed


def clean_html(text: str) -> str:
    soup = BeautifulSoup(text, 'html.parser')
    changed = False

    for node in list(soup.select('.source-note')):
        node.decompose()
        changed = True

    changed = remove_preview_containers(soup) or changed
    changed = remove_visible_seo_markers(soup) or changed

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
