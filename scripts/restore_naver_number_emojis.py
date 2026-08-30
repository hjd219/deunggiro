import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
POSTS_JSON = ROOT / 'data' / 'posts.json'
POSTS_DIR = ROOT / 'posts'

# 대제목: 1~9 → 1️⃣~9️⃣, 10 → 🔟. 11 이상은 일반 숫자 유지.
KEYCAP = {str(i): f'{i}\ufe0f\u20e3' for i in range(1, 10)}
KEYCAP['10'] = '\U0001F51F'

# 원숫자는 소제목 등에 쓰므로 그대로 유지한다.
CIRCLED_RE = re.compile(r'[①-⑳㉑-㊿]')
KEYCAP_RE = re.compile(r'(?:[1-9]\ufe0f?\u20e3|\U0001F51F)')
PLAIN_HEADING_RE = re.compile(r'^\s*(10|[1-9])\s*[.)]\s*')
ELEVEN_PLUS_RE = re.compile(r'^\s*(1[1-9]|[2-9]\d)\s*[.)]\s*')


def normalize_heading(tag):
    """h2/h3의 맨 앞 번호만 안전하게 통일한다."""
    text = tag.get_text('', strip=False)
    if not text or CIRCLED_RE.match(text.lstrip()):
        return False

    # 이미 1️⃣~9️⃣/🔟이면 그대로 둔다.
    if KEYCAP_RE.match(text.lstrip()):
        return False

    # 11번 이상은 일반 숫자를 유지한다.
    if ELEVEN_PLUS_RE.match(text):
        return False

    m = PLAIN_HEADING_RE.match(text)
    if not m:
        return False

    replacement = KEYCAP[m.group(1)] + ' '
    # 제목 내부의 strong/em 등 구조를 깨지 않기 위해 첫 텍스트 노드만 바꾼다.
    for node in tag.descendants:
        if getattr(node, 'name', None) is None and str(node).strip():
            original = str(node)
            nm = PLAIN_HEADING_RE.match(original)
            if nm:
                node.replace_with(PLAIN_HEADING_RE.sub(replacement, original, count=1))
                return True
            break
    return False


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
