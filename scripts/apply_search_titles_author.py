#!/usr/bin/env python3
"""One-shot high-impact search title and article author identity patch.

- Shorten ONLY the HTML <title> of 20 articles selected using historical GSC clicks.
- Link all Article.author Person objects to the existing homepage lawyer profile.
- Never change article H1, body, dates, breadcrumbs, canonical, sitemap or design.
- Idempotent: after one run a dry run reports 0 changes.
"""
from __future__ import annotations
import argparse
import html
import json
import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://www.deunggiro.kr/"
PERSON_ID = BASE + "#author-current-doo"
NEW_TITLES = {
    "naver-224355184406": "사망신고 전후 예금 인출과 상속 문제 | 등기로",
    "naver-224311428037": "귀화 후 성본창설·개명 절차와 필요서류 | 등기로",
    "naver-224345217888": "부동산경매 상계신청 방법｜채권자 직접 낙찰 | 등기로",
    "inheritance-renunciation-limited-acceptance-incheon-procedure-1rigsk": "배우자 사망신고 전 예금 인출·장례비 주의사항 | 등기로",
    "naver-224355247343": "상속등기 제적등본·기본증명서·가족관계증명서 | 등기로",
    "naver-224281565289": "부동산경매 상계신청｜채권자·임차인 낙찰 | 등기로",
    "naver-224341135343": "주주총회·이사회 의사록과 서면결의서 양식 | 등기로",
    "naver-224346166353": "상속인 연락두절 시 상속등기 해결방법 | 등기로",
    "naver-224263963206": "상속등기 없이 집 매매 가능할까? 중간생략등기 | 등기로",
    "naver-224269317609": "미등기 주택 상속등기·소유권보존등기 방법 | 등기로",
    "naver-224281470052": "법인 주주전원서면결의서 양식·작성방법 | 등기로",
    "naver-224296969029": "1인주주 주주총회 대신 서면결의 가능한 경우 | 등기로",
    "naver-224337829683": "사망 후 예금 인출과 상속포기·한정승인 주의점 | 등기로",
    "sale-real-estate-guide-bvcdri": "등기권리증 분실 시 부동산 매매·등기 방법 | 등기로",
    "naver-224259683352": "법인 감사 임기만료｜중임·퇴임·변경등기 | 등기로",
    "naver-224279836527": "부동산경매 기일입찰표·입찰봉투 작성방법 | 등기로",
    "naver-224289948822": "사망신고 후 절차｜상속·예금·부동산등기 | 등기로",
    "naver-224296508605": "비트코인·가상자산 상속절차와 처리방법 | 등기로",
    "naver-224300088135": "사망 후 은행예금 찾기｜상속인 연락두절 시 | 등기로",
    "naver-224338890579": "법인 상호변경 등기 절차·비용·상호검색 | 등기로",
}
TITLE_RE = re.compile(r"(<title\b[^>]*>)([\s\S]*?)(</title>)", re.I)
SCHEMA_RE = re.compile(
    r'(<script\b[^>]*\btype=["\x27]application/ld\+json["\x27][^>]*>)([\s\S]*?)(</script>)',
    re.I
)
AUTHOR_RE = re.compile(r'("author"\s*:\s*)(\{[^{}]*\})')
HEAD_CLOSE = re.compile(r"</head\s*>", re.I)
DATE_RE = re.compile(r'"(?:datePublished|dateModified)"\s*:\s*"([^"]+)"')


def profile(schema: dict) -> dict:
    updated = dict(schema)
    updated["@id"] = PERSON_ID
    updated["url"] = BASE
    return updated


def patch_post(source: str, slug: str, original_title: str) -> tuple[str, list[str]]:
    head_close = HEAD_CLOSE.search(source)
    if head_close is None:
        raise RuntimeError(f"{slug}: no </head>")
    head, tail = source[:head_close.start()], source[head_close.start():]
    before_dates = DATE_RE.findall(head)
    changes: list[str] = []
    if slug in NEW_TITLES:
        matches = list(TITLE_RE.finditer(head))
        if len(matches) != 1:
            raise RuntimeError(f"{slug}: expected one HTML title, got {len(matches)}")
        current = html.unescape(matches[0].group(2))
        new = NEW_TITLES[slug]
        allowed = {original_title, original_title + " | 현재두 법무사 사무소", original_title + " | 등기로", new}
        if current not in allowed:
            raise RuntimeError(f"{slug}: title unexpectedly changed: {current!r}")
        if current != new:
            head = head[:matches[0].start(2)] + html.escape(new, quote=False) + head[matches[0].end(2):]
            changes.append("search_title")

    seen = 0
    def replace_schema(m: re.Match[str]) -> str:
        nonlocal seen
        try:
            data = json.loads(m.group(2))
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"{slug}: invalid schema") from exc
        if not isinstance(data, dict) or data.get("@type") not in ("Article", "BlogPosting"):
            return m.group(0)
        author = data.get("author")
        if not isinstance(author, dict) or author.get("@type") != "Person" or author.get("name") != "현재두":
            raise RuntimeError(f"{slug}: unexpected article author: {author}")
        seen += 1
        new_author = profile(author)
        if new_author == author:
            return m.group(0)
        raw = m.group(2)
        match = AUTHOR_RE.search(raw)
        if match is None or json.loads(match.group(2)) != author:
            raise RuntimeError(f"{slug}: cannot target simple author JSON only")
        value = json.dumps(new_author, ensure_ascii=False, separators=(",", ":"))
        replaced = raw[:match.start(2)] + value + raw[match.end(2):]
        changes.append("author")
        return m.group(1) + replaced + m.group(3)

    head = SCHEMA_RE.sub(replace_schema, head)
    if seen == 0:
        raise RuntimeError(f"{slug}: missing Article author schema")
    if DATE_RE.findall(head) != before_dates:
        raise RuntimeError(f"{slug}: date fields changed")
    if slug not in NEW_TITLES and len(TITLE_RE.findall(head)) != 1:
        raise RuntimeError(f"{slug}: unexpected title mutation")
    result = head + tail
    if not result.endswith(tail):
        raise RuntimeError(f"{slug}: page body changed")
    return result, changes


def patch_home(source: str) -> tuple[str, list[str]]:
    changes = []
    section = '<section class="person">'
    named = '<section class="person" id="author-current-doo">'
    if section in source:
        if source.count(section) != 1:
            raise RuntimeError("Ambiguous author profile section")
        source = source.replace(section, named, 1)
        changes.append("profile_anchor")
    elif named not in source:
        raise RuntimeError("Missing visible author introduction on homepage")
    marker = '"@id":"https://www.deunggiro.kr/#author-current-doo"'
    if marker not in source:
        author = {
            "@context": "https://schema.org", "@type": "Person",
            "@id": PERSON_ID, "name": "현재두", "jobTitle": "법무사",
            "url": BASE, "worksFor": {"@id": BASE + "#organization"},
            "image": BASE + "assets/deunggiro-profile.png"
        }
        snippet = '<script type="application/ld+json">' + json.dumps(author, ensure_ascii=False, separators=(",", ":")) + '</script>'
        if source.count("</head>") != 1:
            raise RuntimeError("Unexpected homepage head")
        source = source.replace("</head>", snippet + "</head>", 1)
        changes.append("person_schema")
    if source.count('id="author-current-doo"') != 1:
        raise RuntimeError("Duplicate or missing homepage profile anchor")
    return source, changes


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    posts = json.loads((ROOT / "data/posts.json").read_text(encoding="utf-8"))
    indexed = {p["slug"]: p for p in posts}
    if len(NEW_TITLES) != 20 or any(slug not in indexed for slug in NEW_TITLES):
        raise RuntimeError("The selection of 20 historical-traffic pages is incorrect")
    for slug, title in NEW_TITLES.items():
        if len(title) > 47 or not title.endswith(" | 등기로"):
            raise RuntimeError(f"{slug}: suspicious new title")
    stats = Counter()
    changed = []
    homepage = ROOT / "index.html"
    old = homepage.read_text(encoding="utf-8")
    new, changes = patch_home(old)
    if old != new:
        if not args.dry_run:
            homepage.write_text(new, encoding="utf-8")
        changed.append("index.html")
        stats.update(changes)
    for post in posts:
        slug = post["slug"]
        file = ROOT / "posts" / (slug + ".html")
        if not file.is_file():
            raise RuntimeError("Missing existing post: " + slug)
        old = file.read_text(encoding="utf-8")
        new, changes = patch_post(old, slug, post["title"])
        if old != new:
            if not args.dry_run:
                file.write_text(new, encoding="utf-8")
            changed.append("posts/" + slug + ".html")
            stats.update(changes)
    print(json.dumps({
        "dry_run": args.dry_run, "posts_checked": len(posts), "changed_files": len(changed),
        "new_search_titles": stats["search_title"], "article_schemas_linked": stats["author"],
        "profile_anchor": stats["profile_anchor"], "person_schema": stats["person_schema"],
        "first_changed": changed[:12],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
