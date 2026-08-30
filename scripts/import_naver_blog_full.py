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
        items.sort(key=lambda x: int(x['log_no']), reverse=True)
        print(f'HTML_LIST_TOTAL={len(items)}')
        return items

    print('HTML_LIST_FALLBACK_ORIGINAL')
    return base.fetch_all_blog_items()


def _is_bare_domain(text: str) -> bool:
    text = re.sub(r'\s+', '', text or '').lower()
    return bool(re.fullmatch(r'(?:https?://)?(?:www\.)?[a-z0-9-]+(?:\.[a-z0-9-]+)+(?:/[^\s]*)?', text))


def _remove_link_preview_artifacts(body: str) -> str:
    """네이버 링크/표 미리보기 카드가 긴 일반문단으로 풀리는 현상을 제거한다."""
    soup = BeautifulSoup(body, 'html.parser')
    removed = 0
    blocks = list(soup.find_all(['p', 'div']))
    for block in blocks:
        if block.parent is None:
            continue
        text = ' '.join(block.stripped_strings).strip()
        if not _is_bare_domain(text):
            continue

        # 링크 카드 마지막에 도메인만 별도 문단으로 붙는 구조.
        prev = block.find_previous_sibling()
        if prev is not None:
            prev_text = ' '.join(prev.stripped_strings).strip()
            # 카드 본문이 표/요약 전체를 한 문단으로 펼쳐 놓은 경우만 제거한다.
            preview_hint = any(x in prev_text for x in (
                '좌우로 스크롤 가능합니다', '요약표입니다', '표준세율',
                '기본 세율', '기본세율', '적용 세목', '특이사항',
            ))
            if len(prev_text) >= 180 or preview_hint:
                prev.decompose()
                removed += 1
        block.decompose()
        removed += 1

    if removed:
        print(f'LINK_PREVIEW_ARTIFACTS_REMOVED={removed}')
    return str(soup)


_original_clean_article = base.clean_article


def clean_article_without_previews(url, slug=''):
    body, text = _original_clean_article(url, slug)
    body = _remove_link_preview_artifacts(body)
    # 본문 길이 판정은 원문 텍스트를 유지한다. 링크 카드 제거는 HTML 출력에만 적용한다.
    return body, text


base.fetch_all_blog_items = fetch_all_blog_items_html
base.clean_article = clean_article_without_previews

if __name__ == '__main__':
    base.main()
