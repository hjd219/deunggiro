from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS_JSON = ROOT / "data" / "posts.json"
REPORT = ROOT / "data" / "duplicate-report.json"


def clean_slug(value: str) -> str:
    return str(value or "").strip().removesuffix(".html")


def norm_title(value: str) -> str:
    # 제목 자체가 같은지만 판정한다. 가족관계/지역명/숫자 등 단어 치환은 하지 않는다.
    # 공백과 문장부호 차이만 무시한다.
    text = str(value or "").strip()
    return re.sub(r"[^0-9A-Za-z가-힣]+", "", text).lower()


def main() -> None:
    posts = json.loads(POSTS_JSON.read_text(encoding="utf-8"))
    groups: dict[str, list[dict]] = defaultdict(list)

    for p in posts:
        slug = clean_slug(p.get("slug"))
        title = str(p.get("title") or "").strip()
        key = norm_title(title)
        if not slug or not key:
            continue
        groups[key].append({
            "slug": slug,
            "title": title,
            "date": str(p.get("date") or "").strip(),
            "category": str(p.get("category") or "").strip(),
            "source": str(p.get("source") or "").strip(),
        })

    duplicate_groups = []
    for items in groups.values():
        if len(items) < 2:
            continue
        duplicate_groups.append({
            "title": items[0]["title"],
            "count": len(items),
            "posts": items,
        })

    duplicate_groups.sort(key=lambda x: (-x["count"], x["title"]))
    duplicate_posts = sum(group["count"] - 1 for group in duplicate_groups)

    report = {
        "posts_checked": sum(len(v) for v in groups.values()),
        "duplicate_title_groups": duplicate_groups,
        "duplicate_posts_excluding_one_canonical_each": duplicate_posts,
        "policy": "중복은 제목이 일치하는 경우만 판정한다. 공백·문장부호 차이만 무시하며 가족관계·지역명·숫자 등 단어가 다르면 중복으로 판정하지 않는다.",
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("DUP_AUDIT_POSTS", report["posts_checked"])
    print("DUP_TITLE_GROUPS", len(duplicate_groups))
    print("DUP_TITLE_EXTRA_POSTS", duplicate_posts)
    for group in duplicate_groups:
        print("TITLE_DUP", group["count"], "::", group["title"])
        for item in group["posts"]:
            print(" -", item["slug"], item["date"])


if __name__ == "__main__":
    main()
