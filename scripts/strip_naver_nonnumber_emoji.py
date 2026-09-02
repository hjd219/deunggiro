from __future__ import annotations

import html
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'posts.json'
POSTS_DIR = ROOT / 'posts'
EMOJI_RE = re.compile('[\U0001F000-\U0001FAFF\U00002600-\U000027BF]')
NUM_RE = re.compile(r'(?:[1-9]\ufe0f?\u20e3|🔟)')


def keep_number_emoji(value: str) -> str:
    value = html.unescape(value or '')
    saved = []

    def stash(m):
        saved.append(m.group(0))
        return f'__DGNUM{len(saved)-1}__'

    value = NUM_RE.sub(stash, value)
    value = EMOJI_RE.sub('', value).replace('\ufe0f', '')
    for i, token in enumerate(saved):
        value = value.replace(f'__DGNUM{i}__', token)
    return re.sub(r'\s+', ' ', value).strip()


def set_meta(soup, name: str, value: str) -> None:
    node = soup.select_one(f'meta[name="{name}"]')
    if node is not None:
        node['content'] = value


def main() -> None:
    posts = json.loads(DATA.read_text(encoding='utf-8'))
    json_changed = 0
    html_changed = 0

    for p in posts:
        if p.get('source') != 'naver-blog':
            continue

        old_title = str(p.get('title') or '')
        old_summary = str(p.get('summary') or '')
        old_keywords = str(p.get('keywords') or '')
        title = keep_number_emoji(old_title)
        summary = keep_number_emoji(old_summary)
        keywords = keep_number_emoji(old_keywords)

        if title != old_title or summary != old_summary or keywords != old_keywords:
            p['title'] = title
            p['summary'] = summary
            p['keywords'] = keywords
            json_changed += 1

        slug = str(p.get('slug') or '').replace('.html', '')
        path = POSTS_DIR / f'{slug}.html'
        if not path.exists():
            continue

        original = path.read_text(encoding='utf-8', errors='replace')
        soup = BeautifulSoup(original, 'html.parser')

        h1 = soup.select_one('h1')
        if h1 is not None:
            h1.string = title

        desc = soup.select_one('.desc')
        if desc is not None:
            desc.string = summary

        title_tag = soup.select_one('title')
        if title_tag is not None:
            title_tag.string = f'{title} | 현재두 법무사 사무소'

        set_meta(soup, 'description', summary)
        set_meta(soup, 'dg-title', title)
        set_meta(soup, 'dg-summary', summary)

        rendered = str(soup)
        if rendered != original:
            path.write_text(rendered, encoding='utf-8')
            html_changed += 1

    DATA.write_text(json.dumps(posts, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('NAVER_EMOJI_CLEAN JSON', json_changed, 'HTML', html_changed)


if __name__ == '__main__':
    main()
