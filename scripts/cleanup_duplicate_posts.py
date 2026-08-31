from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS_JSON = ROOT / "data" / "posts.json"
POSTS_DIR = ROOT / "posts"

# 네이버에서 다시 수집된 동일 주제의 최신 글을 남기고,
# 예전에 홈페이지에서 따로 작성했던 중복본만 목록/파일에서 제거한다.
DUPLICATE_LEGACY_SLUGS = {
    "corporate-formation-procedure-cost-documents-u9jgv1",
    "ceo-corporate-procedure-1-o1kz7e",
    "inheritance-partition-registration-procedure-guide-caution-1w5ku0",
    "corporate-cost-3-1f4kd9",
    "inheritance-registration-acquisition-tax-g2aqja",
    "gift-real-estate-acquisition-tax-property-division-incheon-pro-aga3r7",
    "divorce-agreement-property-division-procedure-18044u",
}


def clean_slug(value: str) -> str:
    return str(value or "").strip().removesuffix(".html")


def main() -> None:
    posts = json.loads(POSTS_JSON.read_text(encoding="utf-8"))
    kept = []
    removed = []

    for post in posts:
        slug = clean_slug(post.get("slug"))
        if slug in DUPLICATE_LEGACY_SLUGS:
            removed.append(slug)
            continue
        kept.append(post)

    for slug in DUPLICATE_LEGACY_SLUGS:
        path = POSTS_DIR / f"{slug}.html"
        if path.exists():
            path.unlink()

    POSTS_JSON.write_text(
        json.dumps(kept, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("DUPLICATE_REMOVED", len(removed), ",".join(sorted(removed)))
    print("POSTS_REMAIN", len(kept))


if __name__ == "__main__":
    main()
