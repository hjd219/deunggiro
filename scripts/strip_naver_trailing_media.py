from __future__ import annotations

"""Remove duplicate map/preview images imported after an article's closing credits.

This intentionally leaves article illustrations, diagrams, the site's own
thumbnail, and unrelated page content untouched.
"""

import argparse
import json
import re
import subprocess
from pathlib import Path

from bs4 import BeautifulSoup, Tag

ROOT = Path(__file__).resolve().parents[1]
POSTS_JSON = ROOT / "data" / "posts.json"
MEDIA_PREFIX = "/assets/naver-images/"
FOOTER_LABELS = (
    re.compile(r"^작성\s*[:：]\s*(?:등기로|현재두)", re.I),
    re.compile(r"^법령\s*검토\s*기준\s*[:：]", re.I),
    re.compile(r"^관련\s*법령\s*[:：]", re.I),
)


def is_footer_label(value: str) -> bool:
    value = re.sub(r"\s+", " ", value or "").strip()
    return any(pattern.search(value) for pattern in FOOTER_LABELS)


def is_naver_media_block(node: Tag) -> bool:
    # Restrict deletions to textless, standalone Naver-imported media.
    if node.name not in ("p", "div", "figure"):
        return False
    if node.get_text(" ", strip=True):
        return False
    if node.find(("iframe", "video", "table", "svg")):
        return False
    imgs = node.find_all("img")
    if not imgs:
        return False
    return all(
        str(img.get("src") or "").startswith(MEDIA_PREFIX)
        for img in imgs
    )


def clean_html(source: str) -> tuple[str, int]:
    soup = BeautifulSoup(source, "html.parser")
    body = soup.select_one(".article-body")
    if body is None:
        return source, 0

    children = [node for node in body.children if isinstance(node, Tag)]
    # The article closing credit/legislation line must be among the last
    # four nonempty text blocks; an incidental earlier reference is not enough.
    text_indices = [
        i for i, node in enumerate(children)
        if node.get_text(" ", strip=True)
    ]
    if not text_indices:
        return source, 0
    last_text_index = text_indices[-1]
    footer_positions = [
        i for i in text_indices
        if is_footer_label(children[i].get_text(" ", strip=True))
        and last_text_index - i <= 3
    ]
    if not footer_positions:
        return source, 0

    final_footer = max(footer_positions)
    trailing = children[final_footer + 1:]
    # If more prose or substantive content follows the credits, it is not
    # demonstrably the duplicated Naver footer; do not modify that page.
    if any(
        node.get_text(" ", strip=True)
        for node in trailing
    ):
        return source, 0

    victims = [node for node in trailing if is_naver_media_block(node)]
    if not victims:
        return source, 0

    for node in victims:
        node.decompose()
    return str(soup), len(victims)


def newly_imported_paths() -> set[str]:
    result = subprocess.check_output(
        ["git", "ls-files", "--others", "--exclude-standard", "--", "posts/"],
        cwd=ROOT, text=True, encoding="utf-8"
    )
    return set(result.splitlines())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--new-only", action="store_true",
                        help="Only touch untracked, newly imported HTML pages")
    args = parser.parse_args()
    allowed = newly_imported_paths() if args.new_only else None

    posts = json.loads(POSTS_JSON.read_text(encoding="utf-8"))
    checked = 0
    changed = 0
    removed = 0
    for post in posts:
        if post.get("source") != "naver-blog":
            continue
        slug = str(post.get("slug") or "").removesuffix(".html")
        if not slug:
            continue
        path = ROOT / "posts" / (slug + ".html")
        if allowed is not None and path.relative_to(ROOT).as_posix() not in allowed:
            continue
        if not path.is_file():
            continue
        checked += 1
        raw = path.read_text(encoding="utf-8", errors="replace")
        cleaned, count = clean_html(raw)
        if not count:
            continue
        path.write_text(cleaned, encoding="utf-8")
        changed += 1
        removed += count
        print("NAVER_TRAILING_MEDIA_REMOVED", slug, "count=" + str(count))

    print("NAVER_TRAILING_MEDIA_RESULT", "checked=" + str(checked),
          "posts=" + str(changed), "images=" + str(removed))


if __name__ == "__main__":
    main()
