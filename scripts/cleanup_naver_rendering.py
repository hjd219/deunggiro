import json
import re
from pathlib import Path

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

# 네이버 본문 끝에 붙는 '같이 보면 좋은 글' 링크 미리보기 묶음.
# 홈페이지에는 별도의 '함께 보면 좋은 글' 내부링크 블록이 생성되므로 중복 블록은 제거한다.
NAVER_RELATED_PATTERNS = [
    re.compile(
        r'<(?:h2|h3|p)[^>]*>\s*(?:<[^>]+>\s*)*같이\s*보면\s*좋은\s*글(?:\s*</[^>]+>)*\s*</(?:h2|h3|p)>[\s\S]*?(?=<!--\s*SEO_RELATED_POSTS_START\s*-->|<section[^>]+class=["\'][^"\']*seo-related-posts|</article>)',
        re.I,
    ),
    re.compile(
        r'<(?:h2|h3|p)[^>]*>\s*(?:<[^>]+>\s*)*같이\s*보면\s*좋은\s*글(?:\s*</[^>]+>)*\s*</(?:h2|h3|p)>[\s\S]*?(?:blog\.naver\.com[\s\S]*?)(?=<!--\s*SEO_RELATED_POSTS_START\s*-->|</article>)',
        re.I,
    ),
]

# 링크카드가 제목 없이 남은 경우도 제거. 네이버 도메인을 포함하는 연속 문단/링크 묶음만 대상으로 한다.
NAVER_CARD_PATTERNS = [
    re.compile(
        r'(?:<p[^>]*>[\s\S]*?</p>\s*){0,3}<p[^>]*>\s*(?:<[^>]+>\s*)*blog\.naver\.com(?:\s*</[^>]+>)*\s*</p>(?:\s*<(?:p|h2|h3|blockquote)[^>]*>[\s\S]*?</(?:p|h2|h3|blockquote)>){0,12}(?=<!--\s*SEO_RELATED_POSTS_START\s*-->|</article>)',
        re.I,
    ),
]


def clean_html(text: str) -> str:
    out = text
    for pat in SOURCE_NOTE_PATTERNS:
        out = pat.sub('', out)
    for pat in NAVER_RELATED_PATTERNS:
        out = pat.sub('', out)
    for pat in NAVER_CARD_PATTERNS:
        out = pat.sub('', out)
    for pat in BARE_MARKER_PATTERNS:
        out = pat.sub('', out)
    # 유효한 내부링크 주석은 유지하되, 바로 앞뒤에 남은 공백만 정리한다.
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
