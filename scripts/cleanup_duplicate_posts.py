from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS_JSON = ROOT / "data" / "posts.json"
POSTS_DIR = ROOT / "posts"

# 이미 확인된 예전 홈페이지 중복본.
DUPLICATE_LEGACY_SLUGS = {
    "corporate-formation-procedure-cost-documents-u9jgv1",
    "ceo-corporate-procedure-1-o1kz7e",
    "inheritance-partition-registration-procedure-guide-caution-1w5ku0",
    "corporate-cost-3-1f4kd9",
    "inheritance-registration-acquisition-tax-g2aqja",
    "gift-real-estate-acquisition-tax-property-division-incheon-pro-aga3r7",
    "divorce-agreement-property-division-procedure-18044u",
    "inheritance-gift-real-estate-acquisition-tax-property-division-1xfulg",
}


def clean_slug(value: str) -> str:
    return str(value or "").strip().removesuffix(".html")


def exact_title(value: str) -> str:
    """동일 제목 판정: 공백·문장부호 차이만 무시하고 단어는 절대 치환하지 않는다."""
    return re.sub(r"[^0-9A-Za-z가-힣]+", "", str(value or "").strip()).lower()


def main() -> None:
    posts = json.loads(POSTS_JSON.read_text(encoding="utf-8"))
    removed: list[str] = []
    kept: list[dict] = []
    seen_slugs: set[str] = set()
    seen_titles: set[str] = set()

    for post in posts:
        slug = clean_slug(post.get("slug"))
        title_key = exact_title(post.get("title"))
        if not slug:
            continue

        # 과거에 확인된 레거시 중복본은 계속 제거한다.
        if slug in DUPLICATE_LEGACY_SLUGS:
            removed.append(slug)
            continue

        # 같은 slug가 다시 들어오면 첫 항목만 유지한다.
        if slug in seen_slugs:
            removed.append(slug)
            continue

        # 핵심 규칙: 제목이 동일하면 먼저 나온 1개만 남기고 뒤의 글을 삭제한다.
        # 가족관계·지역명·숫자 등 단어가 하나라도 다르면 다른 제목이므로 삭제하지 않는다.
        if title_key and title_key in seen_titles:
            removed.append(slug)
            continue

        seen_slugs.add(slug)
        if title_key:
            seen_titles.add(title_key)
        kept.append(post)

    kept_slugs = {clean_slug(p.get("slug")) for p in kept}
    for slug in sorted(set(removed)):
        if not slug or slug in kept_slugs:
            continue
        path = POSTS_DIR / f"{slug}.html"
        if path.exists():
            path.unlink()

    POSTS_JSON.write_text(json.dumps(kept, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("DUPLICATE_REMOVED", len(removed), ",".join(sorted(set(removed))))
    print("POSTS_REMAIN", len(kept))


if __name__ == "__main__":
    main()
