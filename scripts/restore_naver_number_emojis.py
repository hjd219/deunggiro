import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from bs4 import BeautifulSoup, Tag
import requests

import import_naver_blog as base

ROOT = Path(__file__).resolve().parents[1]
POSTS_JSON = ROOT / 'data' / 'posts.json'
POSTS_DIR = ROOT / 'posts'

# 0️⃣~9️⃣, 🔟, ①~⑳, ㉑~㊿
NUMBER_RE = re.compile(r'(?:[0-9]\ufe0f?\u20e3|\U0001F51F|[\u2460-\u2473\u3251-\u325f\u32b1-\u32bf])')
LEADING_PLAIN_RE = re.compile(r'^\s*(?:\d{1,2}[.)]?|[①-⑳㉑-㊿])\s*')
TAG_NAMES = ['h2', 'h3', 'p', 'li', 'blockquote', 'th', 'td']

session = requests.Session()
session.headers.update(base.UA)

def fast_get(url, **kwargs):
    kwargs.setdefault('timeout', (4, 10))
    r = session.get(url, headers=base.UA, **kwargs)
    r.raise_for_status()
    r.encoding = r.encoding or r.apparent_encoding or 'utf-8'
    return r

base.get = fast_get


def canon(text: str) -> str:
    text = NUMBER_RE.sub('', str(text or ''))
    text = LEADING_PLAIN_RE.sub('', text)
    text = re.sub(r'[^0-9A-Za-z가-힣]+', '', text).lower()
    return text


def numbered_remote_nodes(body_html: str):
    soup = BeautifulSoup(body_html, 'html.parser')
    out = []
    for tag in soup.find_all(TAG_NAMES):
        text = ' '.join(tag.stripped_strings).strip()
        if not NUMBER_RE.search(text):
            continue
        key = canon(text)
        if len(key) < 3:
            continue
        out.append((tag.name, key, str(tag)))
    return out


def fetch_one(post):
    slug = str(post.get('slug', '')).replace('.html', '').strip()
    url = str(post.get('source_url', '')).strip()
    if not slug or not url:
        return slug, [], 'missing source'
    try:
        body, _ = base.clean_article(url, slug='')
        return slug, numbered_remote_nodes(body), ''
    except Exception as e:
        return slug, [], str(e)


def restore_page(slug: str, remote_nodes) -> int:
    path = POSTS_DIR / f'{slug}.html'
    if not path.exists() or not remote_nodes:
        return 0
    raw = path.read_text(encoding='utf-8')
    soup = BeautifulSoup(raw, 'html.parser')
    body = soup.select_one('.article-body')
    if body is None:
        return 0

    local = {}
    for tag in body.find_all(TAG_NAMES):
        text = ' '.join(tag.stripped_strings).strip()
        key = canon(text)
        if len(key) >= 3:
            local.setdefault((tag.name, key), []).append(tag)
            local.setdefault(('*', key), []).append(tag)

    restored = 0
    used = set()
    for name, key, remote_html in remote_nodes:
        candidates = local.get((name, key), []) or local.get(('*', key), [])
        target = next((x for x in candidates if id(x) not in used), None)
        if target is None:
            continue
        current_text = ' '.join(target.stripped_strings).strip()
        if NUMBER_RE.search(current_text):
            used.add(id(target))
            continue
        remote_tag = BeautifulSoup(remote_html, 'html.parser').find(name)
        if remote_tag is None:
            continue
        target.clear()
        for child in list(remote_tag.contents):
            target.append(child)
        used.add(id(target))
        restored += 1

    if restored:
        path.write_text(str(soup), encoding='utf-8')
    return restored


def main():
    posts = json.loads(POSTS_JSON.read_text(encoding='utf-8'))
    targets = [p for p in posts if p.get('source') == 'naver-blog']
    total = 0
    failures = 0
    with ThreadPoolExecutor(max_workers=8) as ex:
        futures = [ex.submit(fetch_one, p) for p in targets]
        for fut in as_completed(futures):
            slug, nodes, err = fut.result()
            if err:
                failures += 1
                print('RESTORE_SKIP', slug, err, flush=True)
                continue
            n = restore_page(slug, nodes)
            total += n
            if n:
                print('RESTORED', slug, n, flush=True)
    print(f'number emoji restore: posts={len(targets)} restored_nodes={total} failures={failures}', flush=True)


if __name__ == '__main__':
    main()
