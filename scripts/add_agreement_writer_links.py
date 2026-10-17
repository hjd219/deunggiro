#!/usr/bin/env python3
"""One-time SEO links to the two existing agreement PDF form wizards.

Links only relevant posts. Keep every existing title, URL, date, metadata,
structured-data script, sitemap and legal explanation unchanged.
"""
from __future__ import annotations
import argparse
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data/posts.json"
POST_DIR = ROOT / "posts"

INHERIT_HREF = "/inheritance.html#dg-inherit-agreement"
DIVORCE_HREF = "/family.html#dg-divorce-chapter"
TARGETS = {
    "inherit": {
        "href": INHERIT_HREF,
        "trigger": re.compile(r"상속재산분할협의서|협의분할|상속재산분할협의"),
        "find": re.compile(r"상속재산\s*분할\s*협의서|상속재산분할협의서|협의분할|상속재산분할\s*협의"),
        "line": '공동상속인 사이에 분할 내용이 정해졌다면 <a href="' + INHERIT_HREF + '">상속재산분할협의서 자동작성·PDF 출력</a>에서 협의서 초안을 만들 수 있습니다.',
    },
    "divorce": {
        "href": DIVORCE_HREF,
        "trigger": re.compile(r"협의이혼|이혼\s*합의서|이혼합의서"),
        "find": re.compile(r"협의이혼\s*합의서|이혼\s*합의서|협의이혼"),
        "line": '협의이혼에서 재산분할·친권·양육비 등을 정리할 때는 <a href="' + DIVORCE_HREF + '">협의이혼합의서 자동작성·PDF 출력</a>으로 합의서 초안을 만들 수 있습니다.',
    },
}
P_RE = re.compile(r"<p\b[^>]*>[\s\S]*?</p\s*>", re.I)
TAG_RE = re.compile(r"<[^>]+>")
ART_START = re.compile(r'<div\b[^>]*\bclass\s*=\s*["\x27][^"\x27]*\barticle-body\b[^"\x27]*["\x27][^>]*>', re.I)
ART_END = re.compile(r"<!-- SEO_CORE_LINK_START -->|<!-- SEO_RELATED_POSTS_START -->|</article\s*>", re.I)
P_TEMPLATE = '<p class="naver-p" style="font-size:16px;font-weight:400;text-align:left">{text}</p>'


def eligible(post):
    title = str(post.get("title", ""))
    category = str(post.get("category", ""))
    slug = str(post.get("slug", ""))
    selected = []

    # The announcement explicitly introduces BOTH tools.
    announcement = slug == "inheritance-naver-224442456428"
    if (announcement or category in ("상속등기", "상속재산분할") or
            (category == "부동산등기" and "협의분할" in title)):
        if TARGETS["inherit"]["trigger"].search(title):
            if not re.search(r"연락두절|협의거부|협조거부|상속재산분할심판|사해행위취소", title):
                selected.append("inherit")

    if (announcement or category in ("가사", "부동산등기")):
        if TARGETS["divorce"]["trigger"].search(title):
            # A drafting link is not helpful for post-divorce disputes or court-only proceedings.
            if not re.search(r"협의이혼 후|이혼 후|이혼소송|재판이혼|재판상\s*이혼", title):
                selected.append("divorce")

    return selected


def patch(post, source, selected):
    begin = ART_START.search(source)
    if not begin:
        return source, [], ["missing-article-body"]
    end = ART_END.search(source, begin.end())
    if not end:
        return source, [], ["missing-article-end"]
    a, b = begin.end(), end.start()
    body = source[a:b]
    appended = []
    skipped = []

    # All additions are inside .article-body, immediately after an existing
    # paragraph about the agreement, without changing that paragraph.
    for key in selected:
        info = TARGETS[key]
        if re.search(r'<a\b[^>]*href=["\x27]' + re.escape(info["href"]) + r'["\x27]', source, re.I):
            skipped.append(key + ":already-linked")
            continue
        paragraphs = list(P_RE.finditer(body))[:100]
        chosen = None
        for m in paragraphs:
            plain = TAG_RE.sub(" ", m.group(0))
            plain = re.sub(r"\s+", " ", plain)
            if info["find"].search(plain) and len(plain) > 30:
                chosen = m
                break
        if chosen is None:
            skipped.append(key + ":no-relevant-paragraph")
            continue
        snippet = P_TEMPLATE.format(text=info["line"])
        body = body[:chosen.end()] + "\n" + snippet + body[chosen.end():]
        appended.append(key)

    if not appended:
        return source, appended, skipped
    updated = source[:a] + body + source[b:]
    assert updated[:a] == source[:a]
    assert updated.endswith(source[b:])
    for key in appended:
        assert updated.count('href="' + TARGETS[key]["href"] + '"') == source.count('href="' + TARGETS[key]["href"] + '"') + 1
    return updated, appended, skipped


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    assert (ROOT / "inheritance.html").read_text(encoding="utf8").find('id="dg-inherit-agreement"') >= 0
    assert (ROOT / "family.html").read_text(encoding="utf8").find('id="dg-divorce-chapter"') >= 0
    posts = json.loads(REGISTRY.read_text(encoding="utf-8"))
    stats = Counter()
    written = []
    per_tool = {"inherit": [], "divorce": []}
    for post in posts:
        selected = eligible(post)
        if not selected:
            continue
        stats["candidate_posts"] += 1
        path = POST_DIR / (str(post.get("slug")).removesuffix(".html") + ".html")
        if not path.is_file():
            raise SystemExit("Missing article file " + str(path))
        source = path.read_text(encoding="utf-8")
        updated, added, skipped = patch(post, source, selected)
        for reason in skipped:
            stats[reason] += 1
        for kind in added:
            stats[kind + "_links_added"] += 1
            per_tool[kind].append(path.name)
        if updated != source:
            if not args.dry_run:
                path.write_text(updated, encoding="utf-8")
            written.append(path.name)
    print(json.dumps({
        "registered_posts": len(posts),
        "dry_run": args.dry_run,
        "stats": dict(stats),
        "changed_posts": len(written),
        "changed_list": written,
        "per_tool": per_tool,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
