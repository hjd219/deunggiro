#!/usr/bin/env python3
"""Add a stable visible author byline and a consistent Person author to posts.

Only the author byline and Article.author are touched. Publication dates,
article body, breadcrumbs, and internal links are intentionally unchanged.
Safe to run repeatedly; no-op on already-correct files.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS_FILE = ROOT / "data" / "posts.json"
POSTS_DIR = ROOT / "posts"
BYLINE = '\n<p class="dg-author-byline">작성자 <span>현재두 법무사</span></p>'
AUTHOR = {"@type": "Person", "name": "현재두", "jobTitle": "법무사"}
SCRIPT = re.compile(
    r'(<script\b[^>]*\btype\s*=\s*["\']application/ld\+json["\'][^>]*>)'
    r'([\s\S]*?)(</script>)',
    re.IGNORECASE,
)
ARTICLE = re.compile(r"<article\b[^>]*>", re.IGNORECASE)
H1 = re.compile(r"<h1\b[^>]*>[\s\S]*?</h1>", re.IGNORECASE)
BYLINE_PRESENT = re.compile(r'class\s*=\s*["\'][^"\']*\bdg-author-byline\b', re.IGNORECASE)


def patch_article_author(markup: str) -> tuple[str, int]:
    updated = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal updated
        try:
            node = json.loads(match.group(2))
        except json.JSONDecodeError:
            return match.group(0)
        if not isinstance(node, dict) or node.get("@type") != "Article":
            return match.group(0)
        if node.get("author") == AUTHOR:
            return match.group(0)
        node["author"] = AUTHOR
        updated += 1
        return match.group(1) + json.dumps(node, ensure_ascii=False, separators=(",", ":")) + match.group(3)

    return SCRIPT.sub(replace, markup), updated


def patch_visible_author(markup: str) -> tuple[str, bool]:
    if BYLINE_PRESENT.search(markup):
        return markup, False
    article = ARTICLE.search(markup)
    if not article:
        return markup, False
    heading = H1.search(markup, article.end())
    if not heading:
        return markup, False
    return markup[:heading.end()] + BYLINE + markup[heading.end():], True


def main() -> None:
    posts = json.loads(POSTS_FILE.read_text(encoding="utf-8"))
    seen = set()
    edited = added = schema_updated = missing = 0
    for post in posts:
        slug = str(post.get("slug", "")).strip().removesuffix(".html")
        if not slug or slug in seen:
            continue
        seen.add(slug)
        file = POSTS_DIR / f"{slug}.html"
        if not file.is_file():
            missing += 1
            continue
        before = file.read_text(encoding="utf-8")
        after, schema_count = patch_article_author(before)
        after, added_byline = patch_visible_author(after)
        if after != before:
            file.write_text(after, encoding="utf-8")
            edited += 1
        schema_updated += schema_count
        added += int(added_byline)
    print(
        "AUTHOR_BYLINES",
        f"posts={len(seen)}",
        f"edited={edited}",
        f"bylines_added={added}",
        f"article_authors_updated={schema_updated}",
        f"missing={missing}",
    )
    if missing:
        raise SystemExit("Missing article HTML while ensuring author bylines")


if __name__ == "__main__":
    main()
