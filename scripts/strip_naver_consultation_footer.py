from __future__ import annotations

import json
import re
from pathlib import Path
from bs4 import BeautifulSoup, Tag

ROOT = Path(__file__).resolve().parents[1]
POSTS_JSON = ROOT / "data" / "posts.json"

MARKERS = (
    "현재두법무사사무소상담안내",
    "현재두법무사상담안내",
    "현재두법무사사무소상담",
    "상속상담안내",
    "법인상담안내",
    "부동산상담안내",
    "가사상담안내",
    "이혼상담안내",
    "저의사무실이궁금하신분",
    "저희사무실이궁금하신분",
    "사무실이궁금하신분은아래링크",
    "032-425-1500",
    "032-425-15",
)

def compact(value: str) -> str:
    return re.sub(r"\s+", "", value or "")

def is_promo_start(text: str) -> bool:
    v = compact(text)
    return (
        any(marker in v for marker in MARKERS)
        or (len(v) <= 80 and "상담안내" in v)
        or (len(v) <= 120 and "사무실" in v and "아래링크" in v)
    )

def trim_file(path: Path) -> bool:
    source = path.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(source, "html.parser")
    body = soup.select_one(".article-body")
    if body is None:
        return False

    children = [x for x in body.children if isinstance(x, Tag)]
    if not children:
        return False

    # 상담/사무실 홍보문구는 네이버 원문 하단에 붙는 공통 꼬리이므로
    # 시작 지점부터 article-body 끝까지 제거한다.
    cut = None
    for i, child in enumerate(children):
        if is_promo_start(" ".join(child.stripped_strings)):
            cut = i
            break
    if cut is None:
        return False

    for child in children[cut:]:
        child.decompose()
    path.write_text(str(soup), encoding="utf-8")
    return True

def main() -> None:
    posts = json.loads(POSTS_JSON.read_text(encoding="utf-8"))
    changed = 0
    for post in posts:
        if post.get("source") != "naver-blog":
            continue
        slug = str(post.get("slug", "")).replace(".html", "")
        if not slug:
            continue
        path = ROOT / "posts" / f"{slug}.html"
        if path.exists() and trim_file(path):
            changed += 1
            print("CONSULTATION_FOOTER_REMOVED", slug)
    print("CONSULTATION_FOOTER_REMOVED_TOTAL", changed)

if __name__ == "__main__":
    main()
