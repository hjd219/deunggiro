import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
POSTS_JSON = ROOT / 'data' / 'posts.json'
POSTS_DIR = ROOT / 'posts'

KEYCAP = {str(i): f'{i}\ufe0f\u20e3' for i in range(1, 10)}
KEYCAP['10'] = '\U0001F51F'

CIRCLED_RE = re.compile(r'[①-⑳㉑-㊿]')
KEYCAP_RE = re.compile(r'(?:[1-9]\ufe0f?\u20e3|\U0001F51F)')
PLAIN_HEADING_RE = re.compile(r'^\s*(10|[1-9])(?:\s*[.)]\s*|\s+)')
ELEVEN_PLUS_RE = re.compile(r'^\s*(1[1-9]|[2-9]\d)(?:\s*[.)]\s*|\s+)')


def normalize_heading(tag):
    text = tag.get_text('', strip=False)
    if not text or CIRCLED_RE.match(text.lstrip()) or KEYCAP_RE.match(text.lstrip()):
        return False
    if ELEVEN_PLUS_RE.match(text):
        return False
    m = PLAIN_HEADING_RE.match(text)
    if not m:
        return False

    replacement = KEYCAP[m.group(1)] + ' '
    for node in tag.descendants:
        if getattr(node, 'name', None) is None and str(node).strip():
            original = str(node)
            if PLAIN_HEADING_RE.match(original):
                node.replace_with(PLAIN_HEADING_RE.sub(replacement, original, count=1))
                return True
            break
    return False


def is_strong_number_heading(p):
    strong = p.find('strong', recursive=False)
    if strong is None:
        return False
    if ''.join(p.stripped_strings) != ''.join(strong.stripped_strings):
        return False
    text = strong.get_text('', strip=False)
    if not PLAIN_HEADING_RE.match(text) or ELEVEN_PLUS_RE.match(text):
        return False
    prev = p.find_previous_sibling()
    return prev is not None and getattr(prev, 'name', None) == 'hr'


def process_page(path: Path):
    raw = path.read_text(encoding='utf-8')
    soup = BeautifulSoup(raw, 'html.parser')
    body = soup.select_one('.article-body')
    if body is None:
        return 0

    changed = 0
    for tag in body.find_all(['h2', 'h3']):
        if normalize_heading(tag):
            changed += 1

    for p in body.find_all('p', recursive=False):
        if is_strong_number_heading(p) and normalize_heading(p):
            changed += 1

    if changed:
        path.write_text(str(soup), encoding='utf-8')
    return changed


def main():
    posts = json.loads(POSTS_JSON.read_text(encoding='utf-8'))
    total = 0
    pages = 0
    for post in posts:
        if post.get('source') != 'naver-blog':
            continue
        slug = str(post.get('slug', '')).replace('.html', '').strip()
        if not slug:
            continue
        path = POSTS_DIR / f'{slug}.html'
        if not path.exists():
            continue
        n = process_page(path)
        if n:
            pages += 1
            total += n
            print('NUMBERED', slug, n, flush=True)
    print(f'heading number normalization: pages={pages} headings={total}', flush=True)


if __name__ == '__main__':
    main()
