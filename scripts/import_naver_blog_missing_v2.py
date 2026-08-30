from __future__ import annotations

import html
import re
import sys

from bs4 import BeautifulSoup, Tag

import import_naver_blog as base
import import_naver_blog_full as full
import import_naver_blog_missing as legacy


def _marker(node: Tag) -> str:
    return ' '.join([str(node.get('id') or ''), ' '.join(node.get('class') or [])]).lower()


def _is_link_card(node: Tag) -> bool:
    cur = node
    for _ in range(6):
        if not isinstance(cur, Tag):
            break
        m = _marker(cur)
        if any(x in m for x in base.THUMBNAIL_MARKERS):
            return True
        cur = cur.parent
    return False


def _image_src(img: Tag) -> str:
    src = (
        img.get('data-lazy-src')
        or img.get('data-src')
        or img.get('data-original')
        or img.get('data-origin-src')
        or img.get('src')
        or ''
    )
    if not src:
        srcset = img.get('data-lazy-srcset') or img.get('srcset') or ''
        if srcset:
            src = str(srcset).split(',')[0].strip().split(' ')[0]
    src = str(src).strip()
    if src.startswith('//'):
        src = 'https:' + src
    return src


def _render_text_paragraph(p: Tag) -> str:
    rich = legacy.legacy_inline_html(p)
    text = ' '.join(p.stripped_strings).strip()
    if not text:
        return ''
    if re.fullmatch(r'(?:https?://)?(?:www\.)?(?:hjd219\.github\.io|deunggiro\.kr|www\.deunggiro\.kr)/?', text, re.I):
        return ''
    return f'<p>{rich}</p>'


def clean_article_v2(url: str, slug: str = ''):
    view = base.resolve_post_view(url)
    r = base.get(view)
    soup = BeautifulSoup(r.text, 'html.parser')
    root = soup.select_one('.se-main-container') or soup.select_one('#postViewArea') or soup.select_one('.post-view')
    if root is None:
        raise RuntimeError('네이버 본문 영역을 찾지 못했습니다.')

    for bad in root.select('script,style,noscript,iframe,button'):
        bad.decompose()

    parts = []
    image_no = 0
    seen_images = set()

    components = []
    for comp in root.find_all(class_=lambda c: c and 'se-component' in (c if isinstance(c, list) else str(c).split())):
        if comp.find_parent(class_=lambda c: c and 'se-component' in (c if isinstance(c, list) else str(c).split())):
            continue
        components.append(comp)

    if components:
        for comp in components:
            if _is_link_card(comp):
                continue
            comp_text = ' '.join(comp.stripped_strings).strip()
            marker_hit = any(x in comp_text for x in base.FOOTER_IMAGE_MARKERS)
            if marker_hit and len(comp_text) < 350:
                continue

            table = comp.find('table')
            if table is not None:
                rendered = legacy.legacy_table_html(table)
                if rendered:
                    parts.append(rendered)
                continue

            imgs = comp.find_all('img')
            if imgs:
                for img in imgs:
                    if _is_link_card(img):
                        continue
                    src = _image_src(img)
                    if not src or src in seen_images:
                        continue
                    seen_images.add(src)
                    if slug:
                        image_no += 1
                        src = legacy.save_all_body_image(src, slug, image_no)
                    parts.append(f'<p class="media-paragraph"><img src="{html.escape(src, quote=True)}" alt="" loading="lazy" decoding="async"></p>')
                # 이미지 컴포넌트에 캡션 문단이 있으면 이어서 보존
                for p in comp.select('.se-caption p, .se-caption, .se-module-text p'):
                    rendered = _render_text_paragraph(p)
                    if rendered:
                        parts.append(rendered)
                continue

            paras = comp.select('p.se-text-paragraph') or comp.select('.se-module-text p') or comp.find_all('p')
            if paras:
                for p in paras:
                    if p.find_parent('table'):
                        continue
                    rendered = _render_text_paragraph(p)
                    if rendered:
                        parts.append(rendered)
                continue

            quote = comp.find('blockquote')
            if quote is not None:
                rich = legacy.legacy_inline_html(quote)
                if rich:
                    parts.append(f'<blockquote>{rich}</blockquote>')
                continue
    else:
        # 구형 에디터 fallback. 끝부분 이미지도 본문이면 보존한다.
        blocks = root.find_all(['h2','h3','p','blockquote','ul','ol','img','hr','table'], recursive=True)
        for el in blocks:
            if el.name != 'table' and el.find_parent('table'):
                continue
            if el.find_parent(['p','blockquote','ul','ol']) and el.name != 'img':
                continue
            if _is_link_card(el):
                continue
            txt = ' '.join(el.stripped_strings).strip() if el.name != 'img' else ''
            if txt and any(x in txt for x in base.FOOTER_IMAGE_MARKERS) and len(txt) < 350:
                continue
            if el.name == 'img':
                src = _image_src(el)
                if not src or src in seen_images:
                    continue
                seen_images.add(src)
                if slug:
                    image_no += 1
                    src = legacy.save_all_body_image(src, slug, image_no)
                parts.append(f'<p class="media-paragraph"><img src="{html.escape(src, quote=True)}" alt="" loading="lazy" decoding="async"></p>')
            elif el.name == 'table':
                rendered = legacy.legacy_table_html(el)
                if rendered:
                    parts.append(rendered)
            elif el.name == 'hr':
                parts.append('<hr class="article-divider">')
            elif el.name in ('h2','h3'):
                rich = legacy.legacy_inline_html(el)
                if rich:
                    parts.append(f'<{el.name}>{rich}</{el.name}>')
            elif el.name == 'blockquote':
                rich = legacy.legacy_inline_html(el)
                if rich:
                    parts.append(f'<blockquote>{rich}</blockquote>')
            elif el.name in ('ul','ol'):
                lis = [legacy.legacy_inline_html(li) for li in el.find_all('li', recursive=False)]
                lis = [x for x in lis if x]
                if lis:
                    parts.append(f'<{el.name}>' + ''.join(f'<li>{x}</li>' for x in lis) + f'</{el.name}>')
            elif el.name == 'p':
                rendered = _render_text_paragraph(el)
                if rendered:
                    parts.append(rendered)

    body = '\n'.join(parts)
    body = full.normalize_new_body_numbers(body)
    body_text = BeautifulSoup(body, 'html.parser').get_text(' ', strip=True)
    text = re.sub(r'\s+', ' ', ' '.join(root.stripped_strings)).strip()
    print(f'BODY_V2 chars={len(body_text)} images={image_no} components={len(components)}', flush=True)
    return body, text


# 기존 누락글 탐색·최대 3개 생성·희박본문 자동복구 로직은 유지하고,
# 본문/이미지 추출기만 보강 버전으로 교체한다.
legacy.clean_article_legacy = clean_article_v2

if __name__ == '__main__':
    legacy.main()
