from __future__ import annotations

import html
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup, NavigableString, Tag

import import_naver_blog as base
import import_naver_blog_full as full

MAX_IMPORT = 3
MAX_REPAIR = 6
MAX_IMAGE_BYTES = 8 * 1024 * 1024


def legacy_inline_html(el):
    def walk(node):
        if isinstance(node, NavigableString):
            return html.escape(str(node))
        if not isinstance(node, Tag):
            return ''
        name = node.name.lower()
        inner = ''.join(walk(c) for c in node.children)
        if name in ('strong', 'b'):
            return f'<strong>{inner}</strong>'
        if name in ('em', 'i'):
            return f'<em>{inner}</em>'
        if name == 'u':
            return f'<u>{inner}</u>'
        if name == 'br':
            return '<br>'
        if name == 'a':
            href = node.get('href') or ''
            if href.startswith('http'):
                return f'<a href="{html.escape(href, quote=True)}" target="_blank" rel="noopener noreferrer">{inner}</a>'
            return inner
        return inner
    return re.sub(r'[ \t]+', ' ', ' '.join(walk(c) for c in el.children)).strip()


def legacy_table_html(table):
    rows = []
    for tr in table.find_all('tr'):
        cells = []
        for cell in tr.find_all(['th', 'td'], recursive=False):
            attrs = []
            for key in ('colspan', 'rowspan'):
                val = cell.get(key)
                if val and str(val).isdigit():
                    attrs.append(f'{key}="{val}"')
            tag = 'th' if cell.name == 'th' else 'td'
            attr = (' ' + ' '.join(attrs)) if attrs else ''
            cells.append(f'<{tag}{attr}>{legacy_inline_html(cell)}</{tag}>')
        if cells:
            rows.append('<tr>' + ''.join(cells) + '</tr>')
    return '<table class="naver-table"><tbody>' + ''.join(rows) + '</tbody></table>' if rows else ''


def save_all_body_image(src, slug, index):
    try:
        r = base.requests.get(src, headers=base.UA, timeout=20, stream=True)
        r.raise_for_status()
        total = 0
        chunks = []
        for chunk in r.iter_content(64 * 1024):
            if not chunk:
                continue
            total += len(chunk)
            if total > MAX_IMAGE_BYTES:
                print(f'IMAGE_REMOTE_ONLY_TOO_LARGE {index}', flush=True)
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


def _is_thumbnail_image(el):
    node = el
    for _ in range(5):
        if not isinstance(node, Tag):
            break
        marker = ' '.join([str(node.get('id') or ''), ' '.join(node.get('class') or [])]).lower()
        if any(x in marker for x in base.THUMBNAIL_MARKERS):
            return True
        node = node.parent
    return False


def _has_text_after(blocks, index):
    for nxt in blocks[index + 1:]:
        if nxt.name in ('img', 'hr'):
            continue
        txt = ' '.join(nxt.stripped_strings).strip()
        if not txt:
            continue
        if any(marker in txt for marker in base.FOOTER_IMAGE_MARKERS):
            continue
        return True
    return False


def clean_article_legacy(url, slug=''):
    """예전에 잘 동작하던 단순 본문 순서 추출 방식으로 문단·표·이미지를 함께 보존한다."""
    view = base.resolve_post_view(url)
    r = base.get(view)
    soup = BeautifulSoup(r.text, 'html.parser')
    root = soup.select_one('.se-main-container') or soup.select_one('#postViewArea') or soup.select_one('.post-view')
    if root is None:
        raise RuntimeError('네이버 본문 영역을 찾지 못했습니다.')

    for bad in root.select('script,style,noscript,iframe,button'):
        bad.decompose()

    blocks = []
    for el in root.find_all(['h2', 'h3', 'p', 'blockquote', 'ul', 'ol', 'img', 'hr', 'table'], recursive=True):
        if el.name != 'table' and el.find_parent('table'):
            continue
        if el.find_parent(['p', 'blockquote', 'ul', 'ol']) and el.name != 'img':
            continue
        blocks.append(el)

    image_no = 0
    footer_zone = False
    parts = []
    for idx, el in enumerate(blocks):
        txt = ' '.join(el.stripped_strings).strip() if el.name != 'img' else ''
        if txt and any(marker in txt for marker in base.FOOTER_IMAGE_MARKERS):
            footer_zone = True

        if el.name == 'img':
            if footer_zone or _is_thumbnail_image(el) or not _has_text_after(blocks, idx):
                continue
            src = el.get('data-lazy-src') or el.get('data-src') or el.get('src') or ''
            if src.startswith('//'):
                src = 'https:' + src
            if not src:
                continue
            if slug:
                image_no += 1
                src = save_all_body_image(src, slug, image_no)
            parts.append(f'<p class="media-paragraph"><img src="{html.escape(src, quote=True)}" alt="" loading="lazy" decoding="async"></p>')
            continue

        if el.name == 'table':
            rendered = legacy_table_html(el)
            if rendered:
                parts.append(rendered)
            continue
        if el.name == 'hr':
            parts.append('<hr class="article-divider">')
            continue
        if not txt:
            continue

        # 링크카드의 도메인 한 줄만 제거하고 주변 본문은 건드리지 않는다.
        if re.fullmatch(r'(?:https?://)?(?:www\.)?(?:hjd219\.github\.io|deunggiro\.kr|www\.deunggiro\.kr)/?', txt, re.I):
            continue

        rich = legacy_inline_html(el)
        if el.name == 'h2':
            parts.append(f'<h2>{rich}</h2>')
        elif el.name == 'h3':
            parts.append(f'<h3>{rich}</h3>')
        elif el.name == 'blockquote':
            parts.append(f'<blockquote>{rich}</blockquote>')
        elif el.name in ('ul', 'ol'):
            lis = [legacy_inline_html(li) for li in el.find_all('li', recursive=False)]
            lis = [x for x in lis if x]
            if lis:
                parts.append(f'<{el.name}>' + ''.join(f'<li>{x}</li>' for x in lis) + f'</{el.name}>')
        else:
            parts.append(f'<p>{rich}</p>')

    body = '\n'.join(parts)
    body = full.normalize_new_body_numbers(body)
    text = re.sub(r'\s+', ' ', ' '.join(root.stripped_strings)).strip()
    print(f'LEGACY_BODY chars={len(BeautifulSoup(body, "html.parser").get_text(" ", strip=True))} images={image_no}', flush=True)
    return body, text


def _article_body_stats(path: Path):
    try:
        soup = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
        body = soup.select_one('.article-body')
        if body is None:
            return 0, 0
        # 자동 intro/관련글은 본문 품질 판정에서 제외
        for node in body.select('.article-intro,.seo-related-posts,.source-note'):
            node.decompose()
        return len(body.get_text(' ', strip=True)), len(body.find_all('img'))
    except Exception:
        return 0, 0


def repair_sparse_existing(posts):
    repaired = 0
    for post in posts:
        if repaired >= MAX_REPAIR:
            break
        if post.get('source') != 'naver-blog':
            continue
        slug = str(post.get('slug') or '').replace('.html', '')
        if not slug.startswith('naver-'):
            continue
        path = base.POSTS_DIR / f'{slug}.html'
        if not path.exists():
            continue
        text_len, image_count = _article_body_stats(path)
        # 테스트 수집처럼 표/몇 문장만 남은 글만 자동 복구한다.
        if text_len >= 900:
            continue
        source_url = str(post.get('source_url') or '').strip()
        if not source_url:
            continue
        try:
            body, text = clean_article_legacy(source_url, slug)
        except Exception as e:
            print(f'REPAIR_SKIP {slug} {e}', flush=True)
            continue
        new_len = len(BeautifulSoup(body, 'html.parser').get_text(' ', strip=True))
        if new_len <= text_len or new_len < 500:
            print(f'REPAIR_NOT_BETTER {slug} old={text_len} new={new_len}', flush=True)
            continue
        post['summary'] = base.summary_from(text, post.get('title', ''))
        path.write_text(base.build_html(post, body), encoding='utf-8')
        repaired += 1
        print(f'REPAIRED_SPARSE {slug} old={text_len} new={new_len} images={body.count("<img")}', flush=True)
    print(f'REPAIRED_SPARSE_TOTAL={repaired}', flush=True)
    return repaired


def main():
    posts = base.load_posts()
    repair_sparse_existing(posts)

    existing_log_nos, existing_sources, _ = full._existing_state()
    items = full.fetch_all_blog_items_robust()

    added = 0
    checked = 0
    for item in items:
        if added >= MAX_IMPORT:
            break
        n = item.get('log_no') or full._log_no(item.get('link', ''))
        if not n:
            continue
        checked += 1
        source_url = base.canonical_blog_url(n)
        slug = f'naver-{n}'
        path = base.POSTS_DIR / f'{slug}.html'
        if n in existing_log_nos or source_url in existing_sources or path.exists():
            continue

        title = str(item.get('title') or '').strip()
        if len(title) < 2:
            continue
        try:
            body, text = clean_article_legacy(source_url, slug)
        except Exception as e:
            print(f'IMPORT_SKIP_FETCH {n} {e}', flush=True)
            continue
        body_text_len = len(BeautifulSoup(body, 'html.parser').get_text(' ', strip=True))
        if body_text_len < 500:
            print(f'IMPORT_SKIP_SPARSE {n} chars={body_text_len}', flush=True)
            continue

        today = datetime.now().strftime('%Y-%m-%d')
        post = {
            'slug': slug,
            'title': title,
            'summary': base.summary_from(text, title),
            'category': base.infer_category(title),
            'date': today,
            'source': 'naver-blog',
            'source_url': source_url,
            'website_date': today,
        }
        base.POSTS_DIR.mkdir(parents=True, exist_ok=True)
        path.write_text(base.build_html(post, body), encoding='utf-8')
        posts.insert(0, post)
        existing_log_nos.add(n)
        existing_sources.add(source_url)
        added += 1
        print(f'IMPORTED_NEW {n} chars={body_text_len} images={body.count("<img")} {title[:90]}', flush=True)

    base.POSTS_JSON.write_text(json.dumps(posts, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'IMPORT_SCAN checked={checked} imported={added}', flush=True)
    print('IMPORTED', added, flush=True)


if __name__ == '__main__':
    main()
