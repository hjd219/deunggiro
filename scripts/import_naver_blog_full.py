from __future__ import annotations

import html
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from bs4 import BeautifulSoup

import import_naver_blog as base

# 일일 자동수집은 무한 과거 탐색을 하지 않는다.
# 15페이지 안에서 홈페이지에 없는 최신 글 3개를 찾으면 즉시 종료한다.
MAX_PAGES = 15
EMPTY_PAGE_LIMIT = 3
MAX_LOCAL_IMAGES = 6
HTTP_TIMEOUT = (4, 10)
IMAGE_TIMEOUT = (4, 8)

_session = base.requests.Session()
_session.headers.update(base.UA)


def fast_get(url, **kwargs):
    kwargs.setdefault('timeout', HTTP_TIMEOUT)
    r = _session.get(url, **kwargs)
    r.raise_for_status()
    try:
        r.content.decode('utf-8')
        r.encoding = 'utf-8'
    except UnicodeDecodeError:
        r.encoding = r.encoding or r.apparent_encoding or 'utf-8'
    return r


def fast_save_image(src, slug, index):
    # 본문 이미지가 수십 장인 글 때문에 Actions가 수십 분 멈추는 것을 방지한다.
    # 앞 6장만 로컬 저장하고 나머지는 원격 주소를 그대로 사용한다.
    if index > MAX_LOCAL_IMAGES:
        print(f'IMAGE_REMOTE_ONLY index={index}', flush=True)
        return src
    try:
        with _session.get(src, timeout=IMAGE_TIMEOUT, stream=True) as r:
            r.raise_for_status()
            length = int(r.headers.get('content-length') or 0)
            if length > 8 * 1024 * 1024:
                print(f'IMAGE_TOO_LARGE index={index} bytes={length}', flush=True)
                return src
            chunks = []
            total = 0
            for chunk in r.iter_content(64 * 1024):
                if not chunk:
                    continue
                total += len(chunk)
                if total > 8 * 1024 * 1024:
                    print(f'IMAGE_TOO_LARGE_STREAM index={index}', flush=True)
                    return src
                chunks.append(chunk)
            if not chunks:
                return src
            folder = base.MEDIA_ROOT / slug
            folder.mkdir(parents=True, exist_ok=True)
            path = folder / f'{index:02d}{base.image_ext(r, src)}'
            path.write_bytes(b''.join(chunks))
            return '/' + path.relative_to(base.ROOT).as_posix()
    except Exception as e:
        print('IMAGE_SKIP', src, e, file=sys.stderr, flush=True)
        return src


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
        out.append({'title': title, 'link': base.canonical_blog_url(n), 'date': _date_from_context(a), 'log_no': n})
    return out


def _existing_state():
    posts = base.load_posts()
    log_nos = set()
    sources = set()
    titles = set()
    for p in posts:
        source = str(p.get('source_url', '')).strip()
        if source:
            sources.add(source)
        title = base.norm_title(p.get('title', ''))
        if title:
            titles.add(title)
        n = base.log_no_from_url(source)
        if not n:
            m = re.fullmatch(r'naver-(\d{6,})', str(p.get('slug', '')).replace('.html', ''))
            n = m.group(1) if m else ''
        if n:
            log_nos.add(n)
    return log_nos, sources, titles


def _is_missing(item, log_nos, sources, titles):
    n = item.get('log_no') or _log_no(item.get('link', ''))
    if not n or n in log_nos:
        return False
    if item.get('link') in sources:
        return False
    title = base.norm_title(item.get('title', ''))
    if title and title in titles:
        return False
    return True


def fetch_all_blog_items_html():
    existing_log_nos, existing_sources, existing_titles = _existing_state()
    seen = {}
    missing_seen = set()
    empty_pages = 0
    endpoints = ('https://blog.naver.com/PostList.naver', 'https://m.blog.naver.com/PostList.naver')

    for page in range(1, MAX_PAGES + 1):
        page_items = []
        errors = []
        for endpoint in endpoints:
            try:
                r = fast_get(endpoint, params={'blogId': base.BLOG_ID, 'from': 'postList', 'categoryNo': '0', 'currentPage': str(page)})
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
            if _is_missing(item, existing_log_nos, existing_sources, existing_titles):
                missing_seen.add(n)

        print(f'HTML_LIST_PAGE page={page} items={len(page_items)} new={new_count} missing={len(missing_seen)}', flush=True)
        if len(missing_seen) >= base.MAX_IMPORT:
            print(f'HTML_LIST_EARLY_STOP missing={len(missing_seen)} target={base.MAX_IMPORT}', flush=True)
            break

        if not page_items or new_count == 0:
            empty_pages += 1
        else:
            empty_pages = 0
        if errors and not page_items:
            print('HTML_LIST_PAGE_ERRORS', page, ' | '.join(errors), flush=True)
        if empty_pages >= EMPTY_PAGE_LIMIT:
            break

    items = list(seen.values())
    if items:
        items.sort(key=lambda x: int(x['log_no']), reverse=True)
        print(f'HTML_LIST_TOTAL={len(items)}', flush=True)
        return items
    print('HTML_LIST_FALLBACK_RSS', flush=True)
    return base.fetch_feed_items()


def _is_bare_domain(text: str) -> bool:
    text = re.sub(r'\s+', '', text or '').lower()
    return bool(re.fullmatch(r'(?:https?://)?(?:www\.)?[a-z0-9-]+(?:\.[a-z0-9-]+)+(?:/[^\s]*)?', text))


def _remove_link_preview_artifacts(body: str) -> str:
    soup = BeautifulSoup(body, 'html.parser')
    removed = 0
    blocks = list(soup.find_all(['p', 'div']))
    for block in blocks:
        if block.parent is None:
            continue
        text = ' '.join(block.stripped_strings).strip()
        if not _is_bare_domain(text):
            continue
        prev = block.find_previous_sibling()
        if prev is not None:
            prev_text = ' '.join(prev.stripped_strings).strip()
            preview_hint = any(x in prev_text for x in ('좌우로 스크롤 가능합니다', '요약표입니다', '표준세율', '기본 세율', '기본세율', '적용 세목', '특이사항'))
            if len(prev_text) >= 180 or preview_hint:
                prev.decompose()
                removed += 1
        block.decompose()
        removed += 1
    if removed:
        print(f'LINK_PREVIEW_ARTIFACTS_REMOVED={removed}', flush=True)
    return str(soup)


_original_clean_article = base.clean_article


def clean_article_without_previews(url, slug=''):
    print(f'ARTICLE_FETCH_START {url}', flush=True)
    body, text = _original_clean_article(url, slug)
    body = _remove_link_preview_artifacts(body)
    print(f'ARTICLE_FETCH_DONE {url} chars={len(text)}', flush=True)
    return body, text


def skip_existing_remote_refresh(posts):
    count = sum(1 for p in posts if p.get('source') == 'naver-blog')
    print(f'REFRESH_EXISTING_SKIPPED={count}', flush=True)
    return 0


# base importer의 모든 네트워크 요청/이미지 저장도 제한된 버전으로 교체한다.
base.get = fast_get
base.save_image = fast_save_image
base.fetch_all_blog_items = fetch_all_blog_items_html
base.clean_article = clean_article_without_previews
base.refresh_existing_imports = skip_existing_remote_refresh

if __name__ == '__main__':
    base.main()
