from __future__ import annotations

import html
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote

import requests
from bs4 import BeautifulSoup

import import_naver_blog_clean as core

ROOT = Path(__file__).resolve().parents[1]
POSTS_JSON = ROOT / 'data' / 'posts.json'
BLOG_ID = 'hjd21'
TITLE_LIST_URL = 'https://blog.naver.com/PostTitleListAsync.naver'
POST_LIST_URL = 'https://blog.naver.com/PostList.naver'
MAX_IMPORT = 3
MAX_LIST_PAGES = 100
LIST_PAGE_SIZE = 30

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/151 Safari/537.36',
    'Accept-Language': 'ko-KR,ko;q=0.9,en;q=0.8',
    'Referer': f'https://blog.naver.com/{BLOG_ID}',
}


def canonical_url(log_no: str) -> str:
    return f'https://blog.naver.com/{BLOG_ID}/{log_no}'


def post_id(value: str) -> str:
    m = re.search(r'(?:logNo=|/)(\d{6,})(?:\D|$)', str(value or ''))
    return m.group(1) if m else ''


def extract_log_nos(text: str) -> list[str]:
    """Extract post IDs even when Naver returns non-standard/escaped JSON."""
    text = html.unescape(str(text or ''))
    found = []
    seen = set()
    patterns = (
        r'"logNo"\s*:\s*"?(\d{6,})"?',
        r'logNo[^0-9]{0,40}(\d{6,})',
        r'[?&]logNo=(\d{6,})',
        rf'(?:blog\.naver\.com|m\.blog\.naver\.com)/{re.escape(BLOG_ID)}/(\d{{6,}})',
    )
    for pattern in patterns:
        for n in re.findall(pattern, text, re.I | re.S):
            if n not in seen:
                seen.add(n)
                found.append(n)
    return found


def fetch_page_ids(page: int) -> list[str]:
    params = {
        'blogId': BLOG_ID,
        'viewdate': '',
        'currentPage': page,
        'categoryNo': 0,
        'parentCategoryNo': 0,
        'countPerPage': LIST_PAGE_SIZE,
    }
    try:
        r = requests.get(TITLE_LIST_URL, params=params, headers=HEADERS, timeout=25)
        r.raise_for_status()
        ids = extract_log_nos(r.text)
        if ids:
            print(f'LIST_PAGE page={page} source=async ids={len(ids)}')
            return ids
        print(f'LIST_ASYNC_EMPTY page={page} bytes={len(r.content)}', file=sys.stderr)
    except Exception as e:
        print(f'LIST_ASYNC_FAIL page={page} {e}', file=sys.stderr)

    # Naver can occasionally reject/alter the async JSON. The visible post-list page
    # still carries the same logNo values, so use it as a structural fallback.
    try:
        r = requests.get(
            POST_LIST_URL,
            params={
                'blogId': BLOG_ID,
                'currentPage': page,
                'categoryNo': 0,
                'parentCategoryNo': 0,
                'from': 'postList',
            },
            headers=HEADERS,
            timeout=25,
        )
        r.raise_for_status()
        ids = extract_log_nos(r.text)
        print(f'LIST_PAGE page={page} source=html ids={len(ids)}')
        return ids
    except Exception as e:
        print(f'LIST_HTML_FAIL page={page} {e}', file=sys.stderr)
        return []


def fetch_metadata(log_no: str) -> tuple[str, str]:
    url = canonical_url(log_no)
    title = ''
    date = ''
    try:
        r = requests.get(url, headers=HEADERS, timeout=25)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        meta = soup.select_one('meta[property="og:title"]')
        if meta and meta.get('content'):
            title = html.unescape(meta['content']).strip()
        for selector in (
            'meta[property="article:published_time"]',
            'meta[name="article:published_time"]',
            'meta[property="og:article:published_time"]',
        ):
            node = soup.select_one(selector)
            if node and node.get('content'):
                date = core.clean_text(node['content'])
                break
    except Exception as e:
        print('META_FAIL', log_no, e, file=sys.stderr)

    if not title:
        # Direct PostView is usually available even when the outer blog shell is sparse.
        try:
            view = core.view_url(url)
            soup = BeautifulSoup(core.get(view).text, 'html.parser')
            node = soup.select_one('.se-title-text, .pcol1 .se_textarea, .htitle span, h3.se_textarea')
            if node:
                title = core.clean_text(' '.join(node.stripped_strings))
        except Exception as e:
            print('META_VIEW_FAIL', log_no, e, file=sys.stderr)

    title = unquote(title).strip()
    m = re.search(r'(20\d{2})[-./](\d{1,2})[-./](\d{1,2})', date)
    if m:
        date = f'{int(m.group(1)):04d}-{int(m.group(2)):02d}-{int(m.group(3)):02d}'
    else:
        date = datetime.now().strftime('%Y-%m-%d')
    return title, date


def existing_state(posts: list[dict]) -> tuple[set[str], set[str]]:
    ids = set()
    titles = set()
    for p in posts:
        n = post_id(p.get('source_url', ''))
        if not n and str(p.get('slug', '')).startswith('naver-'):
            n = str(p.get('slug', '')).removeprefix('naver-').replace('.html', '')
        if n:
            ids.add(n)
        t = core.norm(p.get('title', ''))
        if t:
            titles.add(t)
    return ids, titles


def main() -> None:
    posts = json.loads(POSTS_JSON.read_text(encoding='utf-8'))
    existing_ids, existing_titles = existing_state(posts)
    imported = 0
    scanned = 0
    empty_pages = 0
    seen_ids = set()

    for page in range(1, MAX_LIST_PAGES + 1):
        ids = fetch_page_ids(page)
        if not ids:
            empty_pages += 1
            if empty_pages >= 2:
                break
            continue
        empty_pages = 0

        new_on_page = 0
        for n in ids:
            if n in seen_ids:
                continue
            seen_ids.add(n)
            scanned += 1
            if n in existing_ids:
                continue

            title, date = fetch_metadata(n)
            if not title:
                print('SKIP_NO_TITLE', n, file=sys.stderr)
                continue
            nt = core.norm(title)
            if nt in existing_titles:
                print('SKIP_TITLE_DUP', n, title)
                existing_ids.add(n)
                continue

            url = canonical_url(n)
            slug = 'naver-' + n
            try:
                body, text, imgs = core.extract(url, slug)
                chars, mojibake = core.quality_text(text)
                print('CANDIDATE', n, 'chars='+str(chars), 'mojibake='+str(mojibake), 'images='+str(imgs))
                if chars < 500 or mojibake:
                    continue
                summary = (re.sub(r'^\s*\[[^\]]+\]\s*', '', title) + '의 핵심 절차와 준비사항을 정리합니다.')[:100]
                post = {
                    'title': title,
                    'category': core.category(title + ' ' + text[:500]),
                    'date': date,
                    'slug': slug,
                    'keywords': title,
                    'summary': summary,
                    'source_url': url,
                    'source': 'naver-blog',
                }
                saved = core.save_post(post, body)
                posts.insert(0, post)
                existing_ids.add(n)
                existing_titles.add(nt)
                imported += 1
                new_on_page += 1
                print('IMPORTED_NEW', slug, 'saved='+str(saved), title)
            except Exception as e:
                print('IMPORT_SKIP', n, e, file=sys.stderr)

            if imported >= MAX_IMPORT:
                break

        print(f'PAGE_RESULT page={page} scanned={len(ids)} imported={new_on_page}')
        if imported >= MAX_IMPORT:
            break

    POSTS_JSON.write_text(json.dumps(posts, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    core.validate_all(posts)
    print('HISTORY_SCAN', scanned, 'IMPORTED', imported, 'PAGES_SCANNED', page if 'page' in locals() else 0)


if __name__ == '__main__':
    main()
