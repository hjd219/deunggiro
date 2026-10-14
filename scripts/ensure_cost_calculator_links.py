#!/usr/bin/env python3
"""Place one contextual calculator link beside cost-related legal article text.

Only inserts a single HTML link after the first cost-related heading/paragraph.
Does not touch titles, publication dates, structured data or existing links.
Re-running this script is a no-op for already-linked articles.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / 'data' / 'posts.json'
POSTS_DIR = ROOT / 'posts'

COST_TERMS = re.compile(
    r'비용|취득세|등록면허세|법무사\s*보수|수임료|인지대|송달료|수수료|공과금|견적|청산보수|채권\s*할인'
)
ARTICLE_BODY = re.compile(
    r'<div\b[^>]*class\s*=\s*["\x27][^"\x27]*\barticle-body\b[^"\x27]*["\x27][^>]*>',
    re.IGNORECASE,
)
PARAGRAPH = re.compile(
    r'<(?P<tag>h2|h3|p)\b[^>]*>[\s\S]*?</(?P=tag)\s*>',
    re.IGNORECASE,
)
LINK_CLASS = 'seo-calculator-inline'
END_MARKERS = (
    '<!-- SEO_CORE_LINK_START -->',
    '<!-- SEO_RELATED_POSTS_START -->',
    '</article>',
)


def calculator_for(post: dict) -> tuple[str, str] | None:
    category = str(post.get('category', '')).strip()
    title = str(post.get('title', ''))
    text = ' '.join((title, str(post.get('keywords', '')), str(post.get('summary', ''))))

    if category == '상속포기·한정승인':
        return '/renunciation-calculator.html', '상속포기·한정승인 예상 비용 계산하기'
    if category in ('상속등기', '상속재산분할'):
        return '/acquisition-calculator.html?mode=inherit', '상속등기 취득세·비용 계산하기'
    if category == '법인등기':
        job = ''
        if any(word in title for word in ('본점이전', '주소이전', '본점주소')):
            job = '?job=move'
        elif any(word in title for word in ('증자', '자본금')):
            job = '?job=inc'
        elif any(word in title for word in ('임원변경', '대표이사', '이사변경', '감사변경')):
            job = '?job=off'
        elif any(word in title for word in ('법인설립', '회사설립', '주식회사 설립')):
            job = '?job=est'
        return '/corporate-calculator.html' + job, '법인등기 예상 비용 계산하기'
    if category == '부동산등기':
        if '이혼' in text or '재산분할' in text:
            mode, label = 'divorce', '이혼 재산분할등기 비용 계산하기'
        elif '증여' in title:
            mode, label = 'gift', '증여등기 비용 계산하기'
        elif '매매' in title:
            mode, label = 'sale', '매매등기 비용 계산하기'
        elif '상속' in title:
            mode, label = 'inherit', '상속등기 비용 계산하기'
        else:
            return '/acquisition-calculator.html', '부동산등기 취득세·비용 계산하기'
        return '/acquisition-calculator.html?mode=' + mode, label
    if category == '가사' and ('재산분할' in title and '이혼' in title):
        return '/acquisition-calculator.html?mode=divorce', '이혼 재산분할등기 비용 계산하기'
    return None


def insert_calculator(post: dict, source: str) -> tuple[str, bool]:
    target = calculator_for(post)
    if target is None or f'class="{LINK_CLASS}"' in source:
        return source, False

    body = ARTICLE_BODY.search(source)
    if body is None:
        return source, False
    stop_candidates = [source.find(marker, body.end()) for marker in END_MARKERS]
    ends = [i for i in stop_candidates if i >= 0]
    stop = min(ends) if ends else len(source)
    segment = source[body.end():stop]

    cost_matches = []
    for match in PARAGRAPH.finditer(segment):
        words = html.unescape(re.sub(r'<[^>]+>', ' ', match.group(0)))
        if COST_TERMS.search(words):
            cost_matches.append(match)
    if not cost_matches:
        return source, False

    # Prefer a relevant cost section; otherwise follow the first cost paragraph.
    chosen = next((m for m in cost_matches if m.group('tag').lower() in ('h2', 'h3')), cost_matches[0])
    href, label = target
    snippet = (
        '\n<p class="seo-calculator-inline">'
        f'<a href="{html.escape(href, quote=True)}">{html.escape(label)} →</a>'
        '</p>'
    )
    at = body.end() + chosen.end()
    return source[:at] + snippet + source[at:], True


def main() -> None:
    posts = json.loads(POSTS.read_text(encoding='utf-8'))
    seen = set()
    eligible = added = untouched = missing = 0
    per_category: dict[str, int] = {}
    for post in posts:
        slug = str(post.get('slug', '')).strip().removesuffix('.html')
        if not slug or slug in seen:
            continue
        seen.add(slug)
        file = POSTS_DIR / (slug + '.html')
        if not file.is_file():
            missing += 1
            continue
        existing = file.read_text(encoding='utf-8')
        if calculator_for(post):
            eligible += 1
        updated, changed = insert_calculator(post, existing)
        if changed:
            file.write_text(updated, encoding='utf-8')
            added += 1
            cat = str(post.get('category', ''))
            per_category[cat] = per_category.get(cat, 0) + 1
        else:
            untouched += 1
    print('COST_CALCULATORS', json.dumps(
        dict(posts=len(seen), eligible_categories=eligible, links_added=added,
             untouched=untouched, missing=missing, by_category=per_category),
        ensure_ascii=False,
    ))
    if missing:
        raise SystemExit('Missing article HTML')


if __name__ == '__main__':
    main()
