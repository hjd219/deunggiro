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


def literal_title(value: str) -> str:
    # [인천 상속] 같은 앞머리와 문장부호/공백만 제거한 실제 제목 비교값.
    text = strip_prefixes(str(value or ""))
    return re.sub(r"[^0-9A-Za-z가-힣]+", "", text).lower()


def normalize_template_terms(text: str) -> str:
    text = strip_prefixes(text)
    for word in sorted(ROLE_WORDS, key=len, reverse=True):
        text = text.replace(word, "가족")
    for word in sorted(LOCATION_WORDS, key=len, reverse=True):
        text = text.replace(word, "지역")
    text = re.sub(r"\d+(?:[.,]\d+)*", "숫자", text)
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
    return re.sub(r"\s+", "", " ".join(body.stripped_strings))


def ratio(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b, autojunk=False).ratio()


def shingles(text: str, size: int = 12) -> set[str]:
    text = normalize_template_terms(text)
    if not text:
        return set()
    if len(text) <= size:
        return {text}
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
        title = str(p.get("title") or "").strip()
        body = article_text(slug)
        rows.append({
            "slug": slug, "title": title, "date": str(p.get("date") or "").strip(),
            "literal_title": literal_title(title),
            "template_title": normalize_template_terms(title),
            "body": body,
            "nb": normalize_template_terms(body),
            "shingles": shingles(body),
        })

    exact_title = []
    template_duplicate = []
    near = []
    topic_overlap = []

    for i, a in enumerate(rows):
        for b in rows[i + 1:]:
            literal_same = bool(a["literal_title"] and a["literal_title"] == b["literal_title"])
            template_same = bool(a["template_title"] and a["template_title"] == b["template_title"])
            title_sim = ratio(a["template_title"], b["template_title"])
            body_sim = ratio(a["body"], b["body"])
            normalized_body_sim = ratio(a["nb"], b["nb"])
            shingle_sim = jaccard(a["shingles"], b["shingles"])
            item = {
                "a": a["slug"], "a_title": a["title"], "a_date": a["date"],
                "b": b["slug"], "b_title": b["title"], "b_date": b["date"],
                "title_similarity": round(title_sim, 4),
                "body_similarity": round(body_sim, 4),
                "normalized_body_similarity": round(normalized_body_sim, 4),
                "template_shingle_similarity": round(shingle_sim, 4),
            }

            # 사용자 기준 1: 제목이 같으면 본문 유사도와 무관하게 중복 확정.
            if literal_same:
                exact_title.append(item)
                continue

            # 사용자 기준 2: 가족관계/지역명 등 대상만 치환되어 제목 구조가 같으면 중복 후보.
            if template_same:
                template_duplicate.append(item)
                continue

            # 그 밖의 고유사도는 검토 후보일 뿐 자동 중복 확정하지 않는다.
            if (
                (title_sim >= 0.86 and normalized_body_sim >= 0.90)
                or (title_sim >= 0.82 and shingle_sim >= 0.72)
                or normalized_body_sim >= 0.92
            ):
                near.append(item)
            elif title_sim >= 0.68:
                topic_overlap.append(item)

    exact_title.sort(key=lambda x: (x["a_title"], x["a_date"], x["b_date"]))
    template_duplicate.sort(key=lambda x: (x["title_similarity"], x["normalized_body_similarity"]), reverse=True)
    near.sort(key=lambda x: (x["normalized_body_similarity"], x["template_shingle_similarity"]), reverse=True)
    topic_overlap.sort(key=lambda x: x["title_similarity"], reverse=True)

    report = {
        "posts_checked": len(rows),
        "exact_title_duplicates": exact_title,
        "template_title_duplicates": template_duplicate,
        "near_duplicate_pairs_review": near,
        "similar_topic_pairs_not_delete": topic_overlap[:150],
        "policy": "제목이 일치하면 중복 확정. 가족관계·지역명 등 대상만 치환되어 제목 구조가 같으면 중복 후보. 나머지는 유사도 참고용.",
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("DUP_AUDIT_POSTS", len(rows))
    print("DUP_EXACT_TITLE", len(exact_title))
    print("DUP_TEMPLATE_TITLE", len(template_duplicate))
    print("DUP_NEAR", len(near))
    for item in exact_title[:50]:
        print("EXACT_TITLE_DUP", item["a"], "<->", item["b"], "::", item["a_title"])
    for item in template_duplicate[:50]:
        print("TEMPLATE_TITLE_DUP", item["a"], "<->", item["b"], "::", item["a_title"], "<->", item["b_title"])


if __name__ == "__main__":
    main()
