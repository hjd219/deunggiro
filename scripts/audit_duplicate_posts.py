from __future__ import annotations

import json
import re
from difflib import SequenceMatcher
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
POSTS_JSON = ROOT / "data" / "posts.json"
POSTS_DIR = ROOT / "posts"
REPORT = ROOT / "data" / "duplicate-report.json"


def clean_slug(value: str) -> str:
    return str(value or "").strip().removesuffix(".html")


def norm_title(value: str) -> str:
    text = str(value or "").strip()
    while True:
        new = re.sub(r"^\s*\[[^\]]+\]\s*", "", text).strip()
        if new == text:
            break
        text = new
    return re.sub(r"[^0-9A-Za-z가-힣]+", "", text).lower()


def article_text(slug: str) -> str:
    path = POSTS_DIR / f"{slug}.html"
    if not path.exists():
        return ""
    soup = BeautifulSoup(path.read_text(encoding="utf-8", errors="replace"), "html.parser")
    body = soup.select_one(".article-body")
    if not body:
        return ""
    for tag in body.select("script,style,.dg-consult-cta,.related,[aria-labelledby='related-posts-title']"):
        tag.decompose()
    text = " ".join(body.stripped_strings)
    return re.sub(r"\s+", "", text)


def ratio(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b, autojunk=False).ratio()


def main() -> None:
    posts = json.loads(POSTS_JSON.read_text(encoding="utf-8"))
    rows = []
    for p in posts:
        slug = clean_slug(p.get("slug"))
        if not slug:
            continue
        rows.append({
            "slug": slug,
            "title": str(p.get("title") or "").strip(),
            "category": str(p.get("category") or "").strip(),
            "source": str(p.get("source") or "").strip(),
            "date": str(p.get("date") or "").strip(),
            "nt": norm_title(p.get("title")),
            "body": article_text(slug),
        })

    exact = []
    near = []
    topic_overlap = []

    for i, a in enumerate(rows):
        for b in rows[i + 1:]:
            title_sim = ratio(a["nt"], b["nt"])
            body_sim = ratio(a["body"], b["body"])
            same_title = bool(a["nt"] and a["nt"] == b["nt"])
            same_body = bool(a["body"] and a["body"] == b["body"])
            item = {
                "a": a["slug"], "a_title": a["title"], "a_date": a["date"],
                "b": b["slug"], "b_title": b["title"], "b_date": b["date"],
                "title_similarity": round(title_sim, 4),
                "body_similarity": round(body_sim, 4),
            }
            # 삭제 후보: 제목 또는 본문이 사실상 동일한 경우만.
            if same_body or (same_title and body_sim >= 0.90) or (title_sim >= 0.96 and body_sim >= 0.92):
                exact.append(item)
            # 매우 유사하나 자동 삭제하면 위험한 후보.
            elif title_sim >= 0.84 and body_sim >= 0.72:
                near.append(item)
            # 제목만 비슷한 정상 확장글 후보. 삭제 대상 아님.
            elif title_sim >= 0.72:
                topic_overlap.append(item)

    exact.sort(key=lambda x: (x["body_similarity"], x["title_similarity"]), reverse=True)
    near.sort(key=lambda x: (x["body_similarity"], x["title_similarity"]), reverse=True)
    topic_overlap.sort(key=lambda x: x["title_similarity"], reverse=True)

    report = {
        "posts_checked": len(rows),
        "exact_or_safe_duplicate_pairs": exact,
        "near_duplicate_pairs_review": near,
        "similar_topic_pairs_not_delete": topic_overlap[:100],
        "policy": "자동 삭제는 exact_or_safe_duplicate_pairs만 검토 대상으로 삼고, near/similar-topic은 삭제하지 않는다.",
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("DUP_AUDIT_POSTS", len(rows))
    print("DUP_AUDIT_SAFE", len(exact))
    print("DUP_AUDIT_NEAR", len(near))
    for item in exact[:20]:
        print("SAFE_DUP", item["a"], "<->", item["b"], "title", item["title_similarity"], "body", item["body_similarity"])
    for item in near[:20]:
        print("NEAR_DUP", item["a"], "<->", item["b"], "title", item["title_similarity"], "body", item["body_similarity"])


if __name__ == "__main__":
    main()
