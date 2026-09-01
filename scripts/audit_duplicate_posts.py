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

# 같은 템플릿에서 가족관계·지역·사건명만 치환한 글을 잡기 위한 정규화.
ROLE_WORDS = [
    "배우자", "남편", "아내", "부모님", "부모", "아버지", "어머니", "부친", "모친",
    "자녀", "자식", "아들", "딸", "형제자매", "형제", "자매", "형", "오빠", "언니", "누나",
    "동생", "미혼인 형", "미혼인 언니", "미혼인 동생",
]
LOCATION_WORDS = ["인천", "서울", "경기", "부천", "김포", "송도", "청라"]


def clean_slug(value: str) -> str:
    return str(value or "").strip().removesuffix(".html")


def strip_prefixes(text: str) -> str:
    text = str(text or "").strip()
    while True:
        new = re.sub(r"^\s*\[[^\]]+\]\s*", "", text).strip()
        if new == text:
            break
        text = new
    return text


def normalize_template_terms(text: str) -> str:
    text = strip_prefixes(text)
    # 긴 표현부터 바꿔서 '미혼인 형'이 '형'보다 먼저 처리되게 한다.
    for word in sorted(ROLE_WORDS, key=len, reverse=True):
        text = text.replace(word, "가족")
    for word in sorted(LOCATION_WORDS, key=len, reverse=True):
        text = text.replace(word, "지역")
    # 숫자·날짜 차이도 템플릿 비교에서는 의미를 낮춘다.
    text = re.sub(r"\d+(?:[.,]\d+)*", "숫자", text)
    return re.sub(r"[^0-9A-Za-z가-힣]+", "", text).lower()


def norm_title(value: str) -> str:
    return normalize_template_terms(value)


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


def shingles(text: str, size: int = 12) -> set[str]:
    if not text:
        return set()
    text = normalize_template_terms(text)
    if len(text) <= size:
        return {text} if text else set()
    return {text[i:i + size] for i in range(len(text) - size + 1)}


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def main() -> None:
    posts = json.loads(POSTS_JSON.read_text(encoding="utf-8"))
    rows = []
    for p in posts:
        slug = clean_slug(p.get("slug"))
        if not slug:
            continue
        body = article_text(slug)
        rows.append({
            "slug": slug,
            "title": str(p.get("title") or "").strip(),
            "category": str(p.get("category") or "").strip(),
            "source": str(p.get("source") or "").strip(),
            "date": str(p.get("date") or "").strip(),
            "nt": norm_title(p.get("title")),
            "body": body,
            "nb": normalize_template_terms(body),
            "shingles": shingles(body),
        })

    exact = []
    near = []
    topic_overlap = []

    for i, a in enumerate(rows):
        for b in rows[i + 1:]:
            title_sim = ratio(a["nt"], b["nt"])
            body_sim = ratio(a["body"], b["body"])
            normalized_body_sim = ratio(a["nb"], b["nb"])
            shingle_sim = jaccard(a["shingles"], b["shingles"])
            same_title = bool(a["nt"] and a["nt"] == b["nt"])
            same_body = bool(a["body"] and a["body"] == b["body"])
            item = {
                "a": a["slug"], "a_title": a["title"], "a_date": a["date"],
                "b": b["slug"], "b_title": b["title"], "b_date": b["date"],
                "title_similarity": round(title_sim, 4),
                "body_similarity": round(body_sim, 4),
                "normalized_body_similarity": round(normalized_body_sim, 4),
                "template_shingle_similarity": round(shingle_sim, 4),
            }

            # 안전한 중복 후보: 완전 동일뿐 아니라 가족관계/지역명만 치환된 템플릿형 글도 포함.
            if (
                same_body
                or (same_title and normalized_body_sim >= 0.86)
                or (title_sim >= 0.94 and normalized_body_sim >= 0.84)
                or (title_sim >= 0.86 and normalized_body_sim >= 0.90)
                or (title_sim >= 0.82 and shingle_sim >= 0.72)
            ):
                exact.append(item)
            # 유사도가 높지만 자동 삭제하면 위험한 후보.
            elif (
                (title_sim >= 0.76 and normalized_body_sim >= 0.72)
                or shingle_sim >= 0.55
                or normalized_body_sim >= 0.82
            ):
                near.append(item)
            elif title_sim >= 0.68:
                topic_overlap.append(item)

    exact.sort(key=lambda x: (x["normalized_body_similarity"], x["template_shingle_similarity"], x["title_similarity"]), reverse=True)
    near.sort(key=lambda x: (x["normalized_body_similarity"], x["template_shingle_similarity"], x["title_similarity"]), reverse=True)
    topic_overlap.sort(key=lambda x: x["title_similarity"], reverse=True)

    report = {
        "posts_checked": len(rows),
        "exact_or_safe_duplicate_pairs": exact,
        "near_duplicate_pairs_review": near,
        "similar_topic_pairs_not_delete": topic_overlap[:150],
        "policy": "가족관계·지역명 등 일부 단어만 치환한 템플릿형 글도 중복 후보로 잡는다. 자동 삭제는 하지 않고 후보를 검토한다.",
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("DUP_AUDIT_POSTS", len(rows))
    print("DUP_AUDIT_SAFE", len(exact))
    print("DUP_AUDIT_NEAR", len(near))
    for item in exact[:30]:
        print(
            "SAFE_DUP", item["a"], "<->", item["b"],
            "title", item["title_similarity"],
            "body", item["body_similarity"],
            "norm", item["normalized_body_similarity"],
            "shingle", item["template_shingle_similarity"],
        )
    for item in near[:30]:
        print(
            "NEAR_DUP", item["a"], "<->", item["b"],
            "title", item["title_similarity"],
            "body", item["body_similarity"],
            "norm", item["normalized_body_similarity"],
            "shingle", item["template_shingle_similarity"],
        )


if __name__ == "__main__":
    main()
