#!/usr/bin/env python3
"""Remove only duplicate legacy SEO_HUB_LINK cards from legal post HTML.

The old and new card must point to the same hub to be considered duplicate.
Keep SEO_CORE_LINK, other links, author bylines, article body, and dates as-is.
No-op for previously cleaned posts.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / 'data' / 'posts.json'
POSTS_DIR = ROOT / 'posts'
LEGACY = re.compile(
    r'<!--\s*SEO_HUB_LINK_START\s*-->[\s\S]*?<!--\s*SEO_HUB_LINK_END\s*-->\s*',
    re.I,
)
CORE = re.compile(
    r'<!--\s*SEO_CORE_LINK_START\s*-->([\s\S]*?)<!--\s*SEO_CORE_LINK_END\s*-->',
    re.I,
)
ANCHOR = re.compile(r'<a\b[^>]*\bhref=["\x27]([^"\x27]+)["\x27]', re.I)


def destination(markup: str) -> str | None:
    match = ANCHOR.search(markup)
    if not match:
        return None
    href = match.group(1).strip()
    url = urlsplit(href)
    # Compare local paths only; don't treat external or parameterized URLs as equivalent.
    if url.netloc and url.netloc != 'www.deunggiro.kr':
        return None
    if url.query or url.fragment or not url.path.startswith('/'):
        return None
    return url.path


def remove_duplicates(source: str) -> tuple[str, int, int]:
    core = CORE.search(source)
    core_url = destination(core.group(1)) if core else None
    removed = 0
    skipped = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal removed, skipped
        old_url = destination(match.group(0))
        if core_url and old_url == core_url:
            removed += 1
            return ''
        skipped += 1
        return match.group(0)

    return LEGACY.sub(replace, source), removed, skipped


def main() -> None:
    posts = json.loads(POSTS.read_text(encoding='utf-8'))
    seen = set()
    changed = removed = skipped = missing = 0
    for item in posts:
        slug = str(item.get('slug', '')).strip().removesuffix('.html')
        if not slug or slug in seen:
            continue
        seen.add(slug)
        path = POSTS_DIR / f'{slug}.html'
        if not path.is_file():
            missing += 1
            continue
        old = path.read_text(encoding='utf-8')
        new, count, warnings = remove_duplicates(old)
        if count:
            path.write_text(new, encoding='utf-8')
            changed += 1
            removed += count
        skipped += warnings
    print(
        'LEGACY_HUB_DEDUP',
        f'checked={len(seen)}',
        f'changed={changed}',
        f'duplicates_removed={removed}',
        f'nonmatching_legacy_kept={skipped}',
        f'missing={missing}',
    )
    if missing or skipped:
        raise SystemExit('Review missing pages or legacy links with different destinations')


if __name__ == '__main__':
    main()
