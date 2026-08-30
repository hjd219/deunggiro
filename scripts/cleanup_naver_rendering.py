import json
import re
from pathlib import Path
from bs4 import BeautifulSoup, Tag

ROOT = Path(__file__).resolve().parents[1]
POSTS_JSON = ROOT / 'data' / 'posts.json'
POSTS_DIR = ROOT / 'posts'

SOURCE_NOTE_PATTERNS = [
    re.compile(r'<p[^>]*class=["\'][^"\']*source-note[^"\']*["\'][^>]*>.*?</p>', re.I | re.S),
    re.compile(r'<p[^>]*>\s*네이버 블로그에 작성한 내용을.*?원문 보기.*?</p>', re.I | re.S),
]

BARE_MARKER_PATTERNS = [
    re.compile(r'(?<!<!--\s)SEO_RELATED_POSTS_STARTSEO_RELATED_POSTS_END(?!\s*-->)'),
    re.compile(r'(?m)^\s*SEO_RELATED_POSTS_START\s*$'),
    re.compile(r'(?m)^\s*SEO_RELATED_POSTS_END\s*$'),
]

NAVER_RELATED_PATTERNS = [
    re.compile(
        r'<(?:h2|h3|p)[^>]*>\s*(?:<[^>]+>\s*)*같이\s*보면\s*좋은\s*글(?:\s*</[^>]+>)*\s*</(?:h2|h3|p)>[\s\S]*?(?=<!--\s*SEO_RELATED_POSTS_START\s*-->|<section[^>]+class=["\'][^"\']*seo-related-posts|</article>)',
        re.I,
    ),
]

NAVER_CARD_PATTERNS = [
    re.compile(
        r'(?:<p[^>]*>[\s\S]*?</p>\s*){0,3}<p[^>]*>\s*(?:<[^>]+>\s*)*(?:m\.)?blog\.naver\.com(?:\s*</[^>]+>)*\s*</p>(?:\s*<(?:p|h2|h3|blockquote)[^>]*>[\s\S]*?</(?:p|h2|h3|blockquote)>){0,12}(?=<!--\s*SEO_RELATED_POSTS_START\s*-->|</article>)',
        re.I,
    ),
]

DOMAIN_RE = re.compile(r'^(?:m\.)?blog\.naver\.com$', re.I)
PREVIEW_HINT_RE = re.compile(r'(\.\.\.|…|“|”|"|네이버 블로그|blog\.naver\.com)', re.I)


def remove_inline_naver_cards(text: str) -> str:
    """본문 중간에 풀려 들어간 네이버 링크 미리보기 카드만 제거한다."""
    soup = BeautifulSoup(text, 'html.parser')
    changed = False
    for node in list(soup.find_all(['p', 'div', 'span'])):
        label = ' '.join(node.stripped_strings).strip()
        if not DOMAIN_RE.fullmatch(label):
            continue

        # 도메인 표시 자체 제거
        prev = node.find_previous_sibling()
        node.decompose()
        changed = True

        # 카드 설명문은 보통 바로 앞에 있고 말줄임표/따옴표를 포함한다.
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

        # 카드 제목이 별도 문단인 경우: 짧고, 바로 뒤의 카드 설명을 제거한 경우에 한해서만 함께 제거
        if removed and isinstance(prev, Tag):
            prev_text = ' '.join(prev.stripped_strings).strip()
            if prev.name in ('p', 'h3', 'div') and 2 <= len(prev_text) <= 80:
                # 실제 본문 소제목 보호: 숫자로 시작하거나 끝에 '구간/절차/방법/작성/결정' 같은 섹션 제목이면 남긴다.
                if not re.match(r'^\s*\d+\s', prev_text) and not re.search(r'(구간|절차|방법|작성|결정|주의사항|정리)$', prev_text):
                    prev.decompose()
                    changed = True

    return str(soup) if changed else text


def clean_html(text: str) -> str:
    out = text
    for pat in SOURCE_NOTE_PATTERNS:
        out = pat.sub('', out)
    for pat in NAVER_RELATED_PATTERNS:
        out = pat.sub('', out)
    for pat in NAVER_CARD_PATTERNS:
        out = pat.sub('', out)
    out = remove_inline_naver_cards(out)
    for pat in BARE_MARKER_PATTERNS:
        out = pat.sub('', out)
    out = re.sub(r'\s+(<!-- SEO_RELATED_POSTS_START -->)', r'\n\1', out)
    out = re.sub(r'(<!-- SEO_RELATED_POSTS_END -->)\s+', r'\1\n', out)
    return out


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
            print('CLEANED', slug)
    print(f'naver rendering cleanup: checked={checked} changed={changed}')


if __name__ == '__main__':
    main()
