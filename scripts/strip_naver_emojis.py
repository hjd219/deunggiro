import json
import re
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString

ROOT = Path(__file__).resolve().parents[1]
POSTS_JSON = ROOT / 'data' / 'posts.json'
POSTS_DIR = ROOT / 'posts'

EMOJI_RE = re.compile(
    '['
    '\U0001F1E6-\U0001F1FF'
    '\U0001F300-\U0001FAFF'
    '\u2300-\u23FF'
    '\u2600-\u26FF'
    '\u2700-\u27BF'
    ']',
    flags=re.UNICODE,
)
EXTRA_RE = re.compile(r'[\uFE0E\uFE0F\u200D\u20E3]')

# 사용자가 본문 구조에 사용하는 번호 이모지는 보존한다.
# 1️⃣~9️⃣, 0️⃣, 🔟 및 동그라미 숫자 ①~⑳을 유지한다.
KEYCAP_RE = re.compile(r'(?:[0-9]\ufe0f?\u20e3|\U0001F51F)')
CIRCLED_RE = re.compile(r'[\u2460-\u2473]')


def _protect_number_emoji(text):
    protected = []

    def repl(m):
        token = f'__DG_NUM_EMOJI_{len(protected)}__'
        protected.append(m.group(0))
        return token

    text = KEYCAP_RE.sub(repl, text)
    text = CIRCLED_RE.sub(repl, text)
    return text, protected


def _restore_number_emoji(text, protected):
    for i, value in enumerate(protected):
        text = text.replace(f'__DG_NUM_EMOJI_{i}__', value)
    return text


def strip_emoji(value):
    if value is None:
        return value
    text = str(value)
    text, protected = _protect_number_emoji(text)
    text = EMOJI_RE.sub('', text)
    text = EXTRA_RE.sub('', text)
    text = _restore_number_emoji(text, protected)
    text = re.sub(r'[ \t]{2,}', ' ', text)
    text = re.sub(r' *\n *', '\n', text)
    return text.strip()


def clean_html(path):
    raw = path.read_text(encoding='utf-8')
    soup = BeautifulSoup(raw, 'html.parser')
    changed = False

    for node in list(soup.find_all(string=True)):
        if not isinstance(node, NavigableString):
            continue
        if node.parent and node.parent.name in ('script', 'style'):
            continue
        new = strip_emoji(str(node))
        if new != str(node):
            node.replace_with(new)
            changed = True

    for tag in soup.find_all(True):
        for attr in ('title', 'content', 'alt', 'aria-label'):
            if tag.has_attr(attr):
                old = tag.get(attr)
                if isinstance(old, str):
                    new = strip_emoji(old)
                    if new != old:
                        tag[attr] = new
                        changed = True

    if changed:
        path.write_text(str(soup), encoding='utf-8')
    return changed


def main():
    posts = json.loads(POSTS_JSON.read_text(encoding='utf-8'))
    changed_posts = 0
    changed_pages = 0

    for post in posts:
        if post.get('source') != 'naver-blog':
            continue
        touched = False
        for key in ('title', 'keywords', 'summary'):
            old = post.get(key)
            if isinstance(old, str):
                new = strip_emoji(old)
                if new != old:
                    post[key] = new
                    touched = True
        if touched:
            changed_posts += 1

        slug = str(post.get('slug', '')).replace('.html', '')
        page = POSTS_DIR / f'{slug}.html'
        if page.exists() and clean_html(page):
            changed_pages += 1

    POSTS_JSON.write_text(json.dumps(posts, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'naver emojis removed except number emojis: posts={changed_posts}, pages={changed_pages}')


if __name__ == '__main__':
    main()
