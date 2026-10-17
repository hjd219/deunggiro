#!/usr/bin/env python3
"""One-time, conservative contextual-link pass over existing legal articles.

Only changes visible paragraph text *inside* .article-body by wrapping a short
existing phrase in a real <a href>. Does not regenerate posts, dates, meta tags,
structured data, sitemaps, lists, designs or external content.
"""
import argparse
import html
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "posts"
REGISTRY = ROOT / "data/posts.json"

# Rule: (relevant words in the article title, an exact short phrase to link,
#        existing destination path). Each article gains at most ONE contextual link.
RULES = {
    "상속등기": [
        (r"미성년|특별대리인|친권|후견", r"특별대리인|미성년 자녀|미성년 상속인", "/inheritance-minor-heir.html"),
        (r"해외|외국|미국|일본|호주|시민권|영주권|아포스티유", r"외국국적 상속인|해외거주 상속인|해외 거주 상속인|외국인 상속인|아포스티유", "/inheritance-overseas-heir.html"),
        (r"연락두절|행방불명|연락이 되지|연락되지|실종", r"연락두절 상속인|연락이 되지 않는 상속인|행방불명 상속인", "/inheritance-missing-heir.html"),
        (r"대습상속", r"대습상속", "/inheritance-substitute-succession.html"),
        (r"분할|협의|기여분|특별수익", r"상속재산분할협의서|상속재산분할|협의분할", "/inheritance-division.html"),
        (r"취득세|비용|무주택|세율", r"상속 취득세|상속등기 비용|취득세", "/acquisition-calculator.html?mode=inherit"),
        (r".", r"상속등기", "/inheritance.html"),
    ],
    "상속재산분할": [
        (r"협의서|자동작성|양식", r"상속재산분할협의서", "/inheritance.html#dg-inherit-agreement"),
        (r".", r"상속재산분할|협의분할|상속재산분할협의서", "/inheritance-division.html"),
    ],
    "상속포기·한정승인": [
        (r"후순위|선순위|상속포기 후", r"후순위 상속인|선순위 상속인|상속포기 심판문", "/renunciation-after-procedure.html"),
        (r"특별한정", r"특별한정승인", "/posts/naver-224239702465.html"),
        (r"청산|재산파산|신문공고|채권신고", r"상속재산파산|청산절차|신문공고|채권신고", "/renunciation-limited-acceptance-liquidation.html"),
        (r"보험|해지환급", r"사망보험금|해지환급금|보험금", "/renunciation-death-insurance.html"),
        (r"예금|인출|통장|계좌|장례비", r"고인 예금|예금 인출|사망신고 전|예금", "/renunciation-deceased-deposit.html"),
        (r"비용|수임료|보수", r"상속포기 비용|한정승인 비용|법무사 보수", "/renunciation-calculator.html"),
        (r".", r"상속포기|한정승인", "/renunciation.html"),
    ],
    "법인등기": [
        (r"비용|등록면허세|견적", r"법인설립 비용|법인등기 비용|등록면허세|설립비용", "/corporate-calculator.html"),
        (r".", r"법인설립|법인등기|임원변경등기|본점이전등기|상호변경등기|목적변경등기|증자등기|회사계속등기", "/corporate.html"),
    ],
    "부동산등기": [
        (r"취득세|비용|세율|견적", r"취득세|부동산등기 비용|등록면허세", "/acquisition-calculator.html"),
        (r"상속등기", r"상속등기", "/inheritance.html"),
        (r".", r"부동산등기|소유권이전등기|매매등기|증여등기|부동산 등기", "/realestate.html"),
    ],
    "가사": [
        (r"협의이혼합의서|이혼합의서 자동작성", r"협의이혼합의서|이혼합의서", "/family.html#dg-divorce-chapter"),
        (r".", r"협의이혼|친권자|양육비|성년후견|한정후견|미성년후견|성본변경|개명|친양자|재산분할|가사사건", "/family.html"),
    ],
}

PARAGRAPH = re.compile(r"<p\b[^>]*>(.*?)</p\s*>", re.I | re.S)
BODY_START = re.compile(r'<div\b[^>]*\bclass\s*=\s*["\x27][^"\x27]*\barticle-body\b[^"\x27]*["\x27][^>]*>', re.I)
BODY_END = re.compile(r"<!-- SEO_CORE_LINK_START -->|<!-- SEO_RELATED_POSTS_START -->|</article\s*>", re.I)
EXISTING_CONTEXT = re.compile(
    r'<a\b[^>]*\bhref\s*=\s*["\x27]/(?!acquisition-calculator\.html|corporate-calculator\.html|renunciation-calculator\.html)',
    re.I,
)



CALCULATOR_BASES = (
    "/acquisition-calculator.html",
    "/corporate-calculator.html",
    "/renunciation-calculator.html",
)
SHORT_GENERATED_CALC_WORDS = {
    "상속 취득세", "상속등기 비용", "취득세", "부동산등기 비용",
    "법인설립 비용", "법인등기 비용", "등록면허세", "설립비용",
    "상속포기 비용", "한정승인 비용", "법무사 보수",
}
BODY_LINK = re.compile(r'<a href="([^"]+)">([^<>]+)</a>', re.I)


def repair_body(post, body):
    """Remove an accidental same-page link and duplicate new calculator anchors."""
    own_href = "/posts/" + str(post.get("slug", "")).removesuffix(".html") + ".html"
    def unwrap_self(match):
        return match.group(2) if match.group(1) == own_href else match.group(0)
    body = BODY_LINK.sub(unwrap_self, body)

    inline = re.findall(
        r'<p\b[^>]*class=["\x27][^"\x27]*\bseo-calculator-inline\b[^"\x27]*["\x27][^>]*>(.*?)</p>',
        body, re.I | re.S
    )
    originals = [
        href.split("?", 1)[0]
        for fragment in inline
        for href in re.findall(r'<a\b[^>]*href=["\x27]([^"\x27]+)', fragment, re.I)
    ]
    if originals:
        def unwrap_duplicate(match):
            href, phrase = match.group(1), match.group(2)
            if (href.split("?", 1)[0] in originals
                    and phrase.strip() in SHORT_GENERATED_CALC_WORDS):
                return phrase
            return match.group(0)
        body = BODY_LINK.sub(unwrap_duplicate, body)
    return body


def already_has_generated_calculator(body):
    return any(
        match.group(1).split("?", 1)[0] in CALCULATOR_BASES
        and match.group(2).strip() in SHORT_GENERATED_CALC_WORDS
        for match in BODY_LINK.finditer(body)
    )

def choose(post, body):
    title = str(post.get("title") or "")
    category = str(post.get("category") or "")
    rules = RULES.get(category, [])
    paragraphs = list(PARAGRAPH.finditer(body))
    own_href = "/posts/" + str(post.get("slug") or "").removesuffix(".html") + ".html"
    for title_regex, phrase_regex, href in rules:
        if href == own_href:
            continue
        if not re.search(title_regex, title, re.I):
            continue
        # A calculator already linked from a cost section needs no duplicate link.
        if (href.split("?", 1)[0] in CALCULATOR_BASES
                and re.search(r'<a\b[^>]*href=["\x27]' + re.escape(href.split("?", 1)[0]), body, re.I)):
            continue
        # Avoid broken links: destinations must exist in the checked-out repo.
        if not (ROOT / href.lstrip("/").split("?", 1)[0].split("#", 1)[0]).is_file():
            continue
        phrase = re.compile(phrase_regex)
        for p in paragraphs[:160]:
            raw = p.group(1)
            # Do not link inside existing HTML tags, rich spans or nested anchors.
            if "<" in raw or len(raw.strip()) < 25:
                continue
            hit = phrase.search(html.unescape(raw))
            if not hit:
                continue
            # For encoded entities, only match literal source text.
            hit = phrase.search(raw)
            if not hit:
                continue
            if len(hit.group(0)) < 3:
                continue
            return p, hit, href
    return None


def patch(post, source):
    match = BODY_START.search(source)
    if not match:
        return source, "no-body"
    end = BODY_END.search(source, match.end())
    if not end:
        return source, "no-end"
    start_offset, end_offset = match.end(), end.start()
    old_body = source[start_offset:end_offset]
    body = repair_body(post, old_body)

    def assemble(value):
        return source[:start_offset] + value + source[end_offset:]

    if EXISTING_CONTEXT.search(body) or already_has_generated_calculator(body):
        return assemble(body), "repaired-overlap" if body != old_body else "existing-context"
    selected = choose(post, body)
    if selected is None:
        return assemble(body), "repaired-overlap" if body != old_body else "no-relevant-phrase"
    paragraph, phrase, href = selected
    raw = paragraph.group(1)
    linked = raw[:phrase.start()] + '<a href="' + html.escape(href, quote=True) + '">' + raw[phrase.start():phrase.end()] + '</a>' + raw[phrase.end():]
    # Visible content remains byte-for-byte unchanged.
    assert linked.replace('<a href="' + html.escape(href, quote=True) + '">', '', 1).replace('</a>', '', 1) == raw
    new_body = body[:paragraph.start(1)] + linked + body[paragraph.end(1):]
    updated = assemble(new_body)
    assert updated[:start_offset] == source[:start_offset]
    assert updated.endswith(source[end_offset:])
    return updated, href


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    posts = json.loads(REGISTRY.read_text(encoding="utf-8"))
    results = Counter()
    changed_by_category = Counter()
    changed_urls = Counter()
    seen = set()
    changed_files = []
    for post in posts:
        slug = str(post.get("slug") or "").removesuffix(".html")
        if not slug or slug in seen:
            continue
        seen.add(slug)
        path = POSTS / (slug + ".html")
        if not path.is_file():
            results["missing-post"] += 1
            continue
        source = path.read_text(encoding="utf-8")
        updated, reason = patch(post, source)
        if updated == source:
            results[reason] += 1
            continue
        if not args.dry_run:
            path.write_text(updated, encoding="utf-8")
        changed_files.append(path.name)
        changed_by_category[str(post.get("category"))] += 1
        changed_urls[reason] += 1
        results["context-links-added"] += 1
    print(json.dumps({
        "registered_posts": len(posts),
        "unique_posts": len(seen),
        "dry_run": args.dry_run,
        "results": dict(results),
        "changed_by_category": dict(changed_by_category),
        "target_links": dict(changed_urls),
        "first_25_changed": changed_files[:25],
    }, ensure_ascii=False, indent=2))
    if results["missing-post"]:
        raise SystemExit("Registered articles missing; refusing silent partial success.")


if __name__ == "__main__":
    main()
