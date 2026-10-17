#!/usr/bin/env python3
"""Apply safe search-only title normalization for all Deunggiro legal articles.

Preserve HTML H1, body, thumbnails, OG metadata, original publication dates,
canonical, URLs, internal links, layout, sitemap and structured data verbatim.
Original article titles remain in data/posts.json. Only the HTML <title> changes.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUFFIX = " | 등기로"
MAX_BASE = 47
HEAD = re.compile(r"</head\s*>", re.I)
TITLE = re.compile(r"(<title\b[^>]*>)([\s\S]*?)(</title>)", re.I)
PARENS = re.compile(r"^(.*?)\s*[(（][^()（）]{6,}[)）]\s*$")
QUESTION = re.compile(r"^(.{24,47}?[?？])(?=\s|[(（])")
BOILERPLATE = re.compile(
    r"(?:\s*[|｜]\s*)?(?:총정리|완벽(?:한)? 정리|핵심 정리|한눈에 정리|한 번에 정리|쉽게 정리|한눈에 보기)$"
)

# Preserve the twenty expert-edited, search-performance-prioritized titles.
from scripts.apply_search_titles_author import NEW_TITLES as PRIOR_TITLES

# Manually written alternatives where mechanical clipping would drop the outcome.
MANUAL = {
    "realestate-naver-224434182517": "[인천 종중등기] 대표자 사망 후 명칭·주소 변경등기",
    "inheritance-naver-224424475718": "사망 후 상속등기·상속포기·한정승인 전체 절차",
    "renunciation-naver-224424501289": "사망신고 전 예금 인출·장례비와 상속포기·한정승인",
    "naver-224242702446": "법인 대표이사 해임 절차·주주총회 소집허가",
    "naver-224410877303": "[처리사례] 외국인이 국내에 있는 경우 협의분할 상속등기",
    "naver-224411287172": "[처리사례] 유언대용신탁 후 자녀 부동산 귀속등기",
    "naver-224410918031": "[처리사례] 채권자 소송으로 뒤늦게 사망 확인·특별한정승인",
    "naver-224410972296": "[처리사례] 한정승인 후 재산·채권자 발견과 경정",
    "naver-224411074752": "[처리사례] 해산간주 회사 계속·청산종결간주 부활등기",
    "naver-224411109357": "[처리사례] 법인 관외 본점이전·동일상호 확인",
    "naver-224254103385": "선박근저당·공장저당 설정 시 필수 기재사항",
    "naver-224254138454": "인터넷등기소 법인등기 전자신청 절차·대상",
    "naver-224408270820": "[처리사례] 배우자 한정승인·미성년 자녀 상속포기",
    "naver-224408290044": "[처리사례] 친권자 사망 후 미성년후견 변경·한정승인",
    "naver-224408253127": "[처리사례] 채권자 소송 후 특별한정승인 신청",
    "naver-224404881173": "[처리사례] 장기 행방불명·협의거부 상속인과 상속등기",
    "naver-224404912884": "[처리사례] 후순위 상속인 소장 수령 후 상속포기",
    "naver-224404962663": "[처리사례] 미국 거주 상속인 3개월 경과 후 상속포기",
    "naver-224405007300": "[처리사례] 40년 전 주소 불일치 부동산 상속등기",
    "naver-224277653704": "법인 임원 임기만료·1인주주 서면결의서 작성",
    "naver-224400605829": "[인천 상속] 미혼 자녀 사망 후 상속등기·예금·보험",
    "naver-224400625408": "부동산등기 비용 계산기｜상속·증여·매매 취득세",
    "naver-224305850112": "채권압류·가압류 경합 시 제3채무자 공탁",
    "naver-224351828550": "남편 사망 후 배우자 단독상속·예금·자동차 이전",
    "naver-224353144950": "이혼 재산분할등기 필요서류·취득세·집행문",
    "naver-224353330147": "KAMCO 공매 낙찰 후 이전등기·취득세·명도",
    "naver-224354109361": "상속·부동산등기 인감증명서 발급 주의사항",
    "naver-224366634981": "[인천 상속등기] 여러 지역 부동산 상속등기 절차",
    "naver-224374111575": "[인천 상속] 협의거부·연락두절 시 재산분할심판",
    "naver-224374856351": "[인천 상속분할] 이복형제·대습상속인 분할심판",
    "inheritance-registration-renunciation-limited-acceptance-inche-15yen8": "가족 사망 후 신고·상속등기·상속포기·한정승인",
    "ceo-company-name-change-business-purpose-capital-increase-corp-17kgzb": "[인천 1인법인] 대표변경·증자·주주전원 서면결의",
    "inheritance-renunciation-limited-acceptance-incheon-guide-u5n9so": "남편 사망 후 상속포기·한정승인과 보험·퇴직금",
    "name-change-incheon-procedure-guide-documents-4lfyb2": "[인천 개명] 개명허가 신청·필요서류·개명신고",
}


def readable_title(title: str) -> str:
    return " ".join(html.unescape(title).split()).strip()


def title_base(original: str, slug: str) -> str:
    if slug in PRIOR_TITLES:
        return PRIOR_TITLES[slug].removesuffix(SUFFIX).strip()
    if slug in MANUAL:
        return MANUAL[slug]
    src = readable_title(original)
    if len(src) <= MAX_BASE:
        return src
    cleaned = BOILERPLATE.sub("", src).strip()
    if 22 <= len(cleaned) <= MAX_BASE:
        return cleaned
    parts = re.split(r"\s*[|｜]\s*", cleaned)
    if len(parts) > 1 and 24 <= len(parts[0]) <= MAX_BASE:
        return parts[0].strip()
    m = PARENS.fullmatch(cleaned)
    if m and 24 <= len(m.group(1)) <= MAX_BASE:
        return m.group(1).strip()
    m = QUESTION.match(cleaned)
    if m:
        return m.group(1).strip()
    # Do NOT clip by character count: for legal titles this can remove the
    # outcome ('특별한정승인', '상속등기') and change the topic.
    return src


def propose(original: str, slug: str) -> str:
    base = title_base(original, slug)
    if not base or base[-1] in "·,|｜(":
        raise ValueError(f"Unnatural ending for article title: {slug}: {base!r}")
    return base + SUFFIX


def candidate_paths(new_only: bool):
    if new_only:
        text = subprocess.check_output(
            ["git", "ls-files", "--others", "--exclude-standard", "--", "posts/"],
            cwd=ROOT, text=True
        )
        return sorted(x for x in text.splitlines()
                      if re.fullmatch(r"posts/[a-zA-Z0-9_-]+\.html", x))
    return ["posts/" + str(p["slug"]) + ".html"
            for p in json.loads((ROOT / "data/posts.json").read_text(encoding="utf-8"))]


def main() -> None:
    arg = argparse.ArgumentParser()
    arg.add_argument("--dry-run", action="store_true")
    arg.add_argument("--new-only", action="store_true")
    opts = arg.parse_args()
    records = json.loads((ROOT / "data/posts.json").read_text(encoding="utf-8"))
    posts = {str(p["slug"]): p for p in records}
    if len(posts) != len(records):
        raise ValueError("Duplicate article slug in source metadata")
    if not set(PRIOR_TITLES) <= set(posts) or not set(MANUAL) <= set(posts):
        raise ValueError("Curated title list has unknown article slug")
    all_titles = {slug: propose(post["title"], slug) for slug, post in posts.items()}
    unique = Counter(all_titles.values())
    repeated = {x: n for x, n in unique.items() if n > 1}
    if repeated:
        raise ValueError(f"Duplicated search titles: {repeated}")
    very_long = {slug: len(title) for slug, title in all_titles.items() if len(title) > 60}
    if very_long:
        raise ValueError(f"Titles remain too long: {very_long}")

    targets = candidate_paths(opts.new_only)
    processed = 0
    modified = []
    shortened = 0
    unchanged = 0
    samples = []
    for rel in targets:
        slug = Path(rel).stem
        if slug not in posts:
            raise ValueError("Unregistered article: " + rel)
        file = ROOT / rel
        if not file.is_file():
            raise FileNotFoundError(rel)
        source = file.read_text(encoding="utf-8")
        marker = HEAD.search(source)
        if not marker:
            raise ValueError("Missing HTML head: " + rel)
        head, tail = source[:marker.start()], source[marker.start():]
        old = list(TITLE.finditer(head))
        if len(old) != 1:
            raise ValueError("Expected exactly one <title> in " + rel)
        new_title = all_titles[slug]
        original = readable_title(posts[slug]["title"])
        current = html.unescape(old[0].group(2))
        # Never change a title with an unexplained manual override.
        allowed = {original, original + " | 현재두 법무사 사무소",
                   original + " | 등기로", new_title}
        if slug in PRIOR_TITLES:
            allowed.add(PRIOR_TITLES[slug])
        if current not in allowed:
            raise ValueError(f"Unrecognized existing title {slug}: {current!r}")
        if current != new_title:
            next_head = head[:old[0].start(2)] + html.escape(new_title, quote=False) + head[old[0].end(2):]
            updated = next_head + tail
            if not updated.endswith(tail):
                raise ValueError("Article body altered")
            if not opts.dry_run:
                file.write_text(updated, encoding="utf-8")
            modified.append(rel)
            if len(new_title) < len(current):
                shortened += 1
            if len(samples) < 12:
                samples.append({"slug": slug, "old": current, "new": new_title})
        else:
            unchanged += 1
        processed += 1
    print(json.dumps({
        "dry_run": opts.dry_run, "new_only": opts.new_only,
        "all_title_count": len(all_titles), "files_checked": processed,
        "changed_files": len(modified), "unchanged": unchanged,
        "shorter_titles": shortened, "total_unique_titles": len(unique),
        "longest_title": max(len(x) for x in all_titles.values()),
        "changes_preview": samples
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
