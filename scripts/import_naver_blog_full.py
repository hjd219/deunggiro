from __future__ import annotations

import html
import re
from datetime import datetime
from urllib.parse import parse_qs, urlparse

from bs4 import BeautifulSoup

import import_naver_blog as base

MAX_PAGES = 120
EMPTY_PAGE_LIMIT = 3


def _log_no(href: str) -> str:
    if not href:
        return ''
    n = base.log_no_from_url(href)
    if n:
        return n
    m = re.search(r'(?:logNo=|/hjd21/)(\d{6,})', href)
    return m.group(1) if m else ''


def _belongs_to_blog(href: str) -> bool:
    if not href:
        return False
    if f'/{base.BLOG_ID}/' in href:
        return True
    try:
        q = parse_qs(urlparse(href).query)
        return (q.get('blogId') or [''])[0] == base.BLOG_ID
    except Exception:
        return False


def _title_from_anchor(a) -> str:
    for key in ('data-title', 'title', 'aria-label'):
        value = (a.get(key) or '').strip()
        if value and len(value) > 2:
            return html.unescape(re.sub(r'\s+', ' ', value))
    value = ' '.join(a.stripped_strings).strip()
    return html.unescape(re.sub(r'\s+', ' ', value))


def _date_from_context(a) -> str:
    node = a
    for _ in range(5):
        if node is None:
            break
        text = ' '.join(getattr(node, 'stripped_strings', [])).strip()
        m = re.search(r'(20\d{2})[.\-/년\s]+(\d{1,2})[.\-/월\s]+(\d{1,2})', text)
        if m:
            try:
                return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3))).strftime('%Y-%m-%d')
            except ValueError:
                pass
        node = getattr(node, 'parent', None)
    return datetime.now().strftime('%Y-%m-%d')


def _extract_items(text: str):
    soup = BeautifulSoup(text, 'html.parser')
    out = []
    seen = set()
    for a in soup.find_all('a', href=True):
        href = html.unescape(a.get('href') or '')
        if not _belongs_to_blog(href):
            continue
        n = _log_no(href)
        if not n or n in seen:
            continue
        title = _title_from_anchor(a)
        # 글목록의 썸네일 링크처럼 제목이 비어 있어도 logNo는 보존한다.
        seen.add(n)
        out.append({
            'title': title,
            'link': base.canonical_blog_url(n),
            'date': _date_from_context(a),
            'log_no': n,
        })
    return out


def fetch_all_blog_items_html():
    seen = {}
    empty_pages = 0
    endpoints = (
        'https://blog.naver.com/PostList.naver',
        'https://m.blog.naver.com/PostList.naver',
    )

    for page in range(1, MAX_PAGES + 1):
        page_items = []
        errors = []
        for endpoint in endpoints:
            try:
                r = base.get(endpoint, params={
                    'blogId': base.BLOG_ID,
                    'from': 'postList',
                    'categoryNo': '0',
                    'currentPage': str(page),
                })
                page_items = _extract_items(r.text)
                if page_items:
                    break
            except Exception as e:
                errors.append(f'{endpoint}: {e}')

        new_count = 0
        for item in page_items:
            n = item['log_no']
            old = seen.get(n)
            if old is None:
                seen[n] = item
                new_count += 1
            elif not old.get('title') and item.get('title'):
                seen[n] = item

        print(f'HTML_LIST_PAGE page={page} items={len(page_items)} new={new_count}')
        if not page_items or new_count == 0:
            empty_pages += 1
        else:
            empty_pages = 0

        if errors and not page_items:
            print('HTML_LIST_PAGE_ERRORS', page, ' | '.join(errors))
        if empty_pages >= EMPTY_PAGE_LIMIT:
            break

    items = list(seen.values())
    if items:
        # 최신 logNo부터 처리한다. 빠진 글이 많아도 하루 3개 제한은 base.main()이 적용한다.
        items.sort(key=lambda x: int(x['log_no']), reverse=True)
        print(f'HTML_LIST_TOTAL={len(items)}')
        return items

    print('HTML_LIST_FALLBACK_ORIGINAL')
    return base.fetch_all_blog_items()


base.fetch_all_blog_items = fetch_all_blog_items_html

if __name__ == '__main__':
    base.main()
