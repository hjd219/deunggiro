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


def core_title(value: str) -> str:
    """비교용 제목. 앞의 [인천], [부동산취득세] 같은 말머리만 제거한다."""
    title = str(value or "").strip()
    while True:
        new = re.sub(r"^\s*\[[^\]]+\]\s*", "", title).strip()
        if new == title:
            break
        title = new
    return re.sub(r"[^0-9A-Za-z가-힣]+", "", title).lower()


def main() -> None:
    posts = json.loads(POSTS_JSON.read_text(encoding="utf-8"))

    # 같은 slug가 중복 등록된 경우 첫 항목만 유지한다.
    seen_slugs: set[str] = set()
    duplicate_slugs: set[str] = set(DUPLICATE_LEGACY_SLUGS)
    for post in posts:
        slug = clean_slug(post.get("slug"))
        if not slug:
            continue
        if slug in seen_slugs:
            duplicate_slugs.add(slug)
        else:
            seen_slugs.add(slug)

    # 네이버 원문과 예전 홈페이지 글의 핵심 제목이 완전히 같으면
    # 네이버 수집본을 기준본으로 남기고 예전 홈페이지 글만 제거한다.
    groups: dict[str, list[dict]] = {}
    for post in posts:
        key = core_title(post.get("title"))
        if key:
            groups.setdefault(key, []).append(post)

    for group in groups.values():
        if len(group) < 2:
            continue
        naver = [p for p in group if p.get("source") == "naver-blog"]
        if not naver:
            continue
        for post in group:
            if post.get("source") != "naver-blog":
                slug = clean_slug(post.get("slug"))
                if slug:
                    duplicate_slugs.add(slug)

    kept = []
    removed = []
    kept_slug_once: set[str] = set()
    for post in posts:
        slug = clean_slug(post.get("slug"))
        if slug in duplicate_slugs:
            # 같은 slug 자체가 중복된 경우 첫 번째 정상 항목까지 지우지 않도록 처리.
            if slug in seen_slugs and slug in kept_slug_once:
                removed.append(slug)
                continue
            if slug in DUPLICATE_LEGACY_SLUGS or post.get("source") != "naver-blog":
                removed.append(slug)
                continue
        if slug:
            kept_slug_once.add(slug)
        kept.append(post)

    # 제거 대상 중 네이버 원문 파일은 절대 삭제하지 않는다.
    kept_slugs = {clean_slug(p.get("slug")) for p in kept}
    for slug in set(removed):
        if slug in kept_slugs:
            continue
        path = POSTS_DIR / f"{slug}.html"
        if path.exists():
            path.unlink()

    POSTS_JSON.write_text(
        json.dumps(kept, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("DUPLICATE_REMOVED", len(removed), ",".join(sorted(set(removed))))
    print("POSTS_REMAIN", len(kept))


if __name__ == "__main__":
    main()
