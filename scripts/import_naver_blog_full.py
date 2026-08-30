from __future__ import annotations

import html
import re
import sys
from datetime import datetime
from urllib.parse import parse_qs, urlparse

from bs4 import BeautifulSoup

import import_naver_blog as base

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


def _existing_state():
    log_nos = set()
    sources = set()
    titles = set()
    for p in base.load_posts():
        source = str(p.get('source_url', '')).strip()
        if source:
            sources.add(source)
        title = base.norm_title(p.get('title', ''))
        if title:
            titles.add(title)
        n = _log_no(source)
        if not n:
            m = re.fullmatch(r'naver-(\d{6,})', str(p.get('slug', '')).replace('.html', ''))
            n = m.group(1) if m else ''
        if n:
            log_nos.add(n)
    return log_nos, sources, titles


def _normalize_item(item):
    item = dict(item)
    n = item.get('log_no') or _log_no(item.get('link', ''))
    if not n:
        return None
    item['log_no'] = n
    item['link'] = base.canonical_blog_url(n)
    item['title'] = html.unescape(str(item.get('title') or '')).strip()
    item['date'] = item.get('date') or datetime.now().strftime('%Y-%m-%d')
    return item


def _is_missing(item, log_nos, sources, titles):
    n = item.get('log_no') or _log_no(item.get('link', ''))
    if not n or n in log_nos:
        return False
    if item.get('link') in sources:
        return False
    # 로그번호가 없는 예외 자료에만 제목 비교를 보조적으로 사용한다.
    if not n:
        title = base.norm_title(item.get('title', ''))
        if title and title in titles:
            return False
    return True


def fetch_async_items():
    seen = {}
    stale_pages = 0
    for page in range(1, MAX_PAGES + 1):
        try:
            r = fast_get(base.TITLE_LIST_URL, params={
                'blogId': base.BLOG_ID,
                'viewdate': '',
                'currentPage': page,
                'categoryNo': 0,
                'parentCategoryNo': '',
                'countPerPage': base.LIST_PAGE_SIZE,
            })
            payload = base.decode_title_list_response(r.text)
            items = base.extract_entries_from_payload(payload)
        except Exception as e:
            print(f'ASYNC_LIST_ERROR page={page} {e}', flush=True)
            break

        new_count = 0
        for raw in items:
            item = _normalize_item(raw)
            if not item:
                continue
            n = item['log_no']
            if n not in seen:
                seen[n] = item
                new_count += 1

        print(f'ASYNC_LIST_PAGE page={page} items={len(items)} new={new_count}', flush=True)
        stale_pages = stale_pages + 1 if new_count == 0 else 0
        if stale_pages >= EMPTY_PAGE_LIMIT:
            break
    print(f'ASYNC_LIST_TOTAL={len(seen)}', flush=True)
    return list(seen.values())


def fetch_rss_items():
    out = []
    try:
        for raw in base.fetch_feed_items():
            item = _normalize_item(raw)
            if item:
                out.append(item)
    except Exception as e:
        print('RSS_LIST_ERROR', e, flush=True)
    print(f'RSS_LIST_TOTAL={len(out)}', flush=True)
    return out


def _belongs_to_blog(href: str) -> bool:
    if not href:
        return False
    if f'/{base.BLOG_ID}/' in href:
        return True
    try:
        return (parse_qs(urlparse(href).query).get('blogId') or [''])[0] == base.BLOG_ID
    except Exception:
        return False


def fetch_html_items():
    seen = {}
    endpoints = ('https://blog.naver.com/PostList.naver', 'https://m.blog.naver.com/PostList.naver')
    stale_pages = 0
    for page in range(1, MAX_PAGES + 1):
        page_items = []
        for endpoint in endpoints:
            try:
                r = fast_get(endpoint, params={'blogId': base.BLOG_ID, 'from': 'postList', 'categoryNo': '0', 'currentPage': str(page)})
                soup = BeautifulSoup(r.text, 'html.parser')
                local_seen = set()
                for a in soup.find_all('a', href=True):
                    href = html.unescape(a.get('href') or '')
                    if not _belongs_to_blog(href):
                        continue
                    n = _log_no(href)
                    if not n or n in local_seen:
                        continue
                    local_seen.add(n)
                    title = ''
                    for key in ('data-title', 'title', 'aria-label'):
                        title = (a.get(key) or '').strip()
                        if len(title) > 2:
                            break
                    if not title:
                        title = ' '.join(a.stripped_strings).strip()
                    page_items.append({'title': title, 'link': base.canonical_blog_url(n), 'date': datetime.now().strftime('%Y-%m-%d'), 'log_no': n})
                if page_items:
                    break
            except Exception:
                continue

        new_count = 0
        for item in page_items:
            n = item['log_no']
            if n not in seen:
                seen[n] = item
                new_count += 1
        print(f'HTML_LIST_PAGE page={page} items={len(page_items)} new={new_count}', flush=True)
        stale_pages = stale_pages + 1 if new_count == 0 else 0
        if stale_pages >= EMPTY_PAGE_LIMIT:
            break
    print(f'HTML_LIST_TOTAL={len(seen)}', flush=True)
    return list(seen.values())


def fetch_all_blog_items_robust():
    log_nos, sources, titles = _existing_state()
    merged = {}
    for source_name, items in (
        ('async', fetch_async_items()),
        ('rss', fetch_rss_items()),
        ('html', fetch_html_items()),
    ):
        for raw in items:
            item = _normalize_item(raw)
            if not item:
                continue
            n = item['log_no']
            old = merged.get(n)
            if old is None or (not old.get('title') and item.get('title')):
                merged[n] = item
        print(f'LIST_MERGED_AFTER_{source_name.upper()}={len(merged)}', flush=True)

    items = sorted(merged.values(), key=lambda x: int(x['log_no']), reverse=True)
    missing = [x for x in items if _is_missing(x, log_nos, sources, titles)]
    print(f'MISSING_CANDIDATES={len(missing)}', flush=True)
    for item in missing[:10]:
        print(f'MISSING {item["log_no"]} {item.get("title", "")[:90]}', flush=True)

    # 누락 글을 앞에 배치해 base.main()이 MAX_IMPORT=3개를 바로 작성하게 한다.
    missing_ids = {x['log_no'] for x in missing}
    return missing + [x for x in items if x['log_no'] not in missing_ids]


KEYCAP = {str(i): f'{i}\ufe0f\u20e3' for i in range(1, 10)}
KEYCAP['10'] = '\U0001F51F'
PLAIN_NUM = re.compile(r'^\s*(10|[1-9])(?:\s*[.)]\s*|\s+)')
ELEVEN_PLUS = re.compile(r'^\s*(1[1-9]|[2-9]\d)(?:\s*[.)]\s*|\s+)')
CIRCLED = re.compile(r'[①-⑳㉑-㊿]')
KEYCAP_RE = re.compile(r'(?:[1-9]\ufe0f?\u20e3|\U0001F51F)')


def _normalize_number_node(tag):
    text = tag.get_text('', strip=False)
    if not text or CIRCLED.match(text.lstrip()) or KEYCAP_RE.match(text.lstrip()) or ELEVEN_PLUS.match(text):
        return False
    m = PLAIN_NUM.match(text)
    if not m:
        return False
    replacement = KEYCAP[m.group(1)] + ' '
    for node in tag.descendants:
        if getattr(node, 'name', None) is None and str(node).strip():
            original = str(node)
            if PLAIN_NUM.match(original):
                node.replace_with(PLAIN_NUM.sub(replacement, original, count=1))
                return True
            break
    return False


def normalize_new_body_numbers(body: str) -> str:
    soup = BeautifulSoup(body, 'html.parser')
    changed = 0
    for tag in soup.find_all(['h2', 'h3']):
        changed += int(_normalize_number_node(tag))
    for p in soup.find_all('p', recursive=False):
        strong = p.find('strong', recursive=False)
        if strong is None or ''.join(p.stripped_strings) != ''.join(strong.stripped_strings):
            continue
        prev = p.find_previous_sibling()
        if prev is not None and getattr(prev, 'name', None) == 'hr':
            changed += int(_normalize_number_node(p))
    if changed:
        print(f'NEW_BODY_NUMBER_EMOJIS={changed}', flush=True)
    return str(soup)


def _is_bare_domain(text: str) -> bool:
    text = re.sub(r'\s+', '', text or '').lower()
    return bool(re.fullmatch(r'(?:https?://)?(?:www\.)?[a-z0-9-]+(?:\.[a-z0-9-]+)+(?:/[^\s]*)?', text))


def _remove_link_preview_artifacts(body: str) -> str:
    soup = BeautifulSoup(body, 'html.parser')
    for block in list(soup.find_all(['p', 'div'])):
        if block.parent is None:
            continue
        text = ' '.join(block.stripped_strings).strip()
        if _is_bare_domain(text):
            block.decompose()
    return str(soup)


_original_clean_article = base.clean_article


def clean_article_fast(url, slug=''):
    print(f'ARTICLE_FETCH_START {url}', flush=True)
    body, text = _original_clean_article(url, slug)
    body = _remove_link_preview_artifacts(body)
    body = normalize_new_body_numbers(body)
    print(f'ARTICLE_FETCH_DONE {url} chars={len(text)}', flush=True)
    return body, text


base.get = fast_get
base.save_image = fast_save_image
base.fetch_all_blog_items = fetch_all_blog_items_robust
base.clean_article = clean_article_fast

if __name__ == '__main__':
    base.main()
