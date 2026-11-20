"""One-time focused correction for the 2026-11-20 preservation-registration article.

Keeps the existing slug, dates, text, images and canonical URL unchanged.
Rebuilds only the generated blog archive listings from the corrected metadata.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from scripts.category_rules import classify_title
from scripts.generate_post_pagination import rebuild_post_pages

ROOT = Path(__file__).resolve().parents[1]
POSTS_JSON = ROOT / "data" / "posts.json"
SLUG = "legal-naver-224484378524"
CATEGORY = "부동산등기"


def verify_rule() -> None:
    examples = {
        "인천 미등기 건물, 건축물대장은 있는데 등기부가 없다면? 주택 소유권보존등기 절차": "부동산등기",
        "건축물대장만 있는 주택 보존등기 방법": "부동산등기",
        "미등기건물 상속등기절차 어떻게 되나요? 보존등기부터": "상속등기",
        "부모·배우자 사망 후 미등기 주택 상속 등기 (보존등기 방법)": "상속등기",
    }
    for title, expected in examples.items():
        got = classify_title(title)
        if got != expected:
            raise RuntimeError(f"Category regression: {title} => {got} (wanted {expected})")
    print("PRESERVATION_CLASSIFIER_TESTS_OK", len(examples))


def patch_article(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8")
    meta = re.search(r'<meta\\b(?=[^>]*\\bname=["\\\']dg-category["\\\'])[^>]*>', raw, re.I)
    if not meta:
        raise RuntimeError("Article category meta not found")
    old_meta = meta.group(0)
    new_meta, changed = re.subn(
        r'\\bcontent=(["\\\'])(?:기타|부동산등기)\\1',
        'content="부동산등기"', old_meta, count=1
    )
    if changed != 1:
        raise RuntimeError("Unexpected category meta content")
    next_html = raw[:meta.start()] + new_meta + raw[meta.end():]
    old_badge = '<span class="badge">기타</span>'
    new_badge = '<span class="badge">부동산등기</span>'
    if old_badge in next_html:
        if next_html.count(old_badge) != 1:
            raise RuntimeError("Unexpected number of category badges")
        next_html = next_html.replace(old_badge, new_badge, 1)
    elif new_badge not in next_html:
        raise RuntimeError("Category badge not found")
    if next_html == raw:
        return False
    path.write_text(next_html, encoding="utf-8")
    return True


def main() -> None:
    verify_rule()
    posts = json.loads(POSTS_JSON.read_text(encoding="utf-8"))
    hits = [post for post in posts if post.get("slug") == SLUG]
    if len(hits) != 1:
        raise RuntimeError(f"Expected exactly one post: {SLUG}; found {len(hits)}")
    post = hits[0]
    if post.get("source") != "naver-blog" or "보존등기" not in post.get("title", ""):
        raise RuntimeError("Unexpected article identity")
    if classify_title(post["title"]) != CATEGORY:
        raise RuntimeError("Preservation registration not classified as real estate")
    old = post.get("category", "")
    if old not in ("기타", CATEGORY):
        raise RuntimeError(f"Refusing to alter unrelated category: {old}")

    post["category"] = CATEGORY
    if old != CATEGORY:
        POSTS_JSON.write_text(json.dumps(posts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    article_changed = patch_article(ROOT / "posts" / f"{SLUG}.html")
    archives_changed = rebuild_post_pages(posts)
    print("PRESERVATION_CATEGORY_CORRECTED", SLUG, old, "->", CATEGORY)
    print("PRESERVATION_ARTICLE_META_CHANGED", article_changed)
    print("PRESERVATION_ARCHIVES_REBUILT", archives_changed)


if __name__ == "__main__":
    main()
