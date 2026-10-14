#!/usr/bin/env python3
"""Place one contextual calculator link beside cost-related legal article text.

Adds at most one link after substantive cost information; removes stale generated links.
Does not touch titles, publication dates, structured data or existing links.
Re-running this script is idempotent for already-correct articles.
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


# Only keep a calculator link when an actual *cost section* gives readers a
# reason to calculate. A passing use of the word 비용 or a tax deadline is not enough.
COST_HEADING = re.compile(r'비용|취득세|등록면허세|법무사\s*보수|수임료|수수료|견적')
NON_COST_HEADINGS = re.compile(
    r'언제까지|납부기한|신고기한|기간|기한|과태료|벌금|장례비|병원비|양도소득세|'
    r'상속세|증여세|보험료|보험금|보증금|손해배상|소송비용|배당금'
)
PRICE_FACT = re.compile(r'\d[\d,.]*\s*(?:만원|천원|원|%|퍼센트)')
COST_EXPLANATION = re.compile(
    r'세율|산정|계산방식|계산방법|예상비용|기본보수|공과금|법무사\s*보수|'
    r'신문공고|등록면허세\s*\d|취득세율|비용은\s*[^.。]{0,90}(?:따라|달라)'
)
COST_TITLE = re.compile(r'비용|견적|취득세|등록면허세|법무사\s*보수|수임료|수수료')
GEN_LINK = re.compile(
    r'\n?<p\b[^>]*class=["\x27][^"\x27]*\bseo-calculator-inline\b[^"\x27]*["\x27][^>]*>[\s\S]*?</p>',
    re.IGNORECASE,
)


def plain(fragment: str) -> str:
    return html.unescape(re.sub(r'<[^>]*>', ' ', fragment)).strip()


def select_cost_section(post: dict, segment: str) -> int | None:
    """Return the insertion offset only for a substantive calculator-relevant section."""
    title = str(post.get('title', ''))
    title_intent = bool(COST_TITLE.search(title) and not NON_COST_HEADINGS.search(title))
    items = [(m, plain(m.group(0))) for m in PARAGRAPH.finditer(segment)]
    candidates = []

    for idx, (match, words) in enumerate(items):
        tag = match.group('tag').lower()
        if not COST_HEADING.search(words) or NON_COST_HEADINGS.search(words):
            continue
        if tag == 'p' and len(words) > 110:
            continue
        # A short, numbered paragraph often functions as a section heading
        # in Naver-imported articles; avoid incidental sentences in the intro.
        looks_like_heading = tag in ('h2', 'h3') or (
            len(words) <= 95 and bool(re.match(r'^\s*(?:\d{1,2}[️⃣.．\uFE0F\u20E3\)]*|[①-⑳])', words))
        )
        if not looks_like_heading and not (
            title_intent and re.search(r'비용은|비용\s*계산|세율|등록면허세는|취득세는', words)
        ):
            continue

        nearby = []
        for next_match, next_words in items[idx+1:idx+11]:
            # Do not steal cost information from an unrelated later section.
            if (
                next_match.group('tag').lower() in ('h2', 'h3')
                and not COST_HEADING.search(next_words)
            ):
                break
            if len(nearby) >= 3 and re.match(r'^[①-⑳]|\d+[️⃣\uFE0F\u20E3]', next_words) and not COST_HEADING.search(next_words):
                break
            nearby.append((next_match, next_words))

        facts = sum(bool(PRICE_FACT.search(t) or COST_EXPLANATION.search(t)) for _,t in nearby)
        if not facts and not (title_intent and COST_EXPLANATION.search(words)):
            continue

        score = facts*4 + (3 if looks_like_heading else 0) + (
            3 if re.search(r'비용.*계산|등록면허세.*계산|취득세.*계산|예상비용|보수', words) else 0
        )
        placement = match.end()
        for next_match, t in nearby:
            # Place the link after relevant explanation, not after a teaser/question.
            if PRICE_FACT.search(t) or COST_EXPLANATION.search(t):
                placement = next_match.end()
                break
        candidates.append((score, placement))

    if not candidates:
        return None
    candidates.sort(key=lambda row: row[0], reverse=True)
    return candidates[0][1]


def insert_calculator(post: dict, source: str) -> tuple[str, bool]:
    # Remove only links generated by this automation; preserve custom/handwritten links.
    # This also removes overly broad links inserted by an older rule.
    cleaned = GEN_LINK.sub('', source)
    target = calculator_for(post)
    if target is None:
        return cleaned, cleaned != source

    body = ARTICLE_BODY.search(cleaned)
    if body is None:
        return cleaned, cleaned != source
    ends = [cleaned.find(marker, body.end()) for marker in END_MARKERS]
    stop = min((i for i in ends if i >= 0), default=len(cleaned))
    segment = cleaned[body.end():stop]

    placement = select_cost_section(post, segment)
    if placement is None:
        return cleaned, cleaned != source

    href, label = target
    snippet = (
        '\n<p class="seo-calculator-inline">'
        f'<a href="{html.escape(href, quote=True)}">{html.escape(label)} →</a>'
        '</p>'
    )
    at = body.end() + placement
    updated = cleaned[:at] + snippet + cleaned[at:]
    return updated, updated != source


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
