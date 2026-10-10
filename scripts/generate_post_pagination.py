#!/usr/bin/env python3
"""Build stable, crawlable ten-article HTML pages for each legal-information mode.

The HTML files have real numbered links and self-canonicals. Dynamic search and
category controls remain progressive enhancements in posts.html's shared script.
No changes are made to article HTML or stored post dates.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / 'data' / 'posts.json'
INDEX = ROOT / 'posts.html'
OUT = ROOT / 'posts-pages'
MODES = ('info', 'core', 'case')
PAGE_SIZE = 10
CASE_RE = re.compile(r'처리사례|실제사례|실제 사례|허가 사례|선임 사례|등기 사례|신청 사례|경정 사례')
FIRST_RE = re.compile(r'<!-- SEO_INITIAL_POSTS_START -->[\s\S]*?<!-- SEO_INITIAL_POSTS_END -->')
NAV_RE = re.compile(r'(<nav id="pagination" class="pagination" aria-label="게시글 페이지">)[\s\S]*?(</nav>)')
CORE_RE = re.compile(r'const CORE_HUBS=new Set\((\[[^\n]*?\])\);')
INTRO = {
    'info': '인천 상속등기·상속포기·한정승인·법인등기·부동산등기의 법률정보와 실무정보를 안내합니다.',
    'core': '업무별로 먼저 확인하면 좋은 핵심 안내를 모았습니다.',
    'case': '실제 진행한 처리사례를 업무 종류별로 확인하세요.',
}
MODE_TITLE = {'info': '법률정보', 'core': '핵심정보', 'case': '실제 처리사례'}
BASE = 'https://www.deunggiro.kr'


def page_path(mode: str, page: int) -> str:
    return '/posts.html' if mode == 'info' and page == 1 else f'/posts-pages/{mode}-{page}.html'


def card(post: dict) -> str:
    def esc(t):
        return html.escape(str(t or ''), quote=True)
    slug = str(post.get('slug', '')).strip().removesuffix('.html')
    thumb = str(post.get('thumbnail') or f'/assets/posts/{slug}-thumbnail.png')
    return (
        f'<a class="post-card" href="/posts/{esc(slug)}.html">'
        f'<img class="post-thumb" src="{esc(thumb)}" alt="{esc(post.get("title"))}" loading="lazy" decoding="async" '
        'onerror="this.onerror=null;this.src=\'/favicon.png\'">'
        '<div class="post-content"><div class="post-meta">'
        f'<span class="badge">{esc(post.get("category") or "법률정보")}</span>{esc(post.get("date"))}</div>'
        f'<h3>{esc(post.get("title"))}</h3><p>{esc(post.get("summary"))}</p></div></a>'
    )


def initial_cards(items: list[dict]) -> str:
    return '<!-- SEO_INITIAL_POSTS_START -->\n' + '\n'.join(card(x) for x in items) + '\n<!-- SEO_INITIAL_POSTS_END -->'


def page_numbers(total: int, current: int) -> list[int | str]:
    out = []
    for n in range(1, total + 1):
        if n == 1 or n == total or abs(n - current) <= 2:
            out.append(n)
        elif not out or out[-1] != '…':
            out.append('…')
    return out


def pagination(mode: str, current: int, total: int) -> str:
    def link(n: int, label: str) -> str:
        active = 'active' if n == current else ''
        aria = 'aria-current="page"' if n == current else ''
        return f'<a class="page-btn {active}" href="{page_path(mode, n)}#legal-post-list" {aria}>{label}</a>'
    def disabled(label: str) -> str:
        return f'<span class="page-btn is-disabled" aria-disabled="true">{label}</span>'
    return ''.join((
        link(current - 1, '이전') if current > 1 else disabled('이전'),
        ''.join('<span>…</span>' if x == '…' else link(x, str(x)) for x in page_numbers(total, current)),
        link(current + 1, '다음') if current < total else disabled('다음'),
    ))


def write_if_changed(path: Path, value: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding='utf-8') == value:
        return False
    path.write_text(value, encoding='utf-8')
    return True


def rebuild_post_pages(posts: list[dict]) -> bool:
    template = INDEX.read_text(encoding='utf-8')
    core_match = CORE_RE.search(template)
    if not core_match or not FIRST_RE.search(template) or not NAV_RE.search(template):
        raise ValueError('Crawlable pagination template or CORE_HUBS missing')
    core = set(json.loads(core_match.group(1)))
    def is_case(p):
        return bool(CASE_RE.search(str(p.get('title', '')) + ' ' + str(p.get('summary', ''))))
    modes = {
        'info': [p for p in posts if not is_case(p) and p.get('slug') not in core],
        'core': [p for p in posts if p.get('slug') in core],
        'case': [p for p in posts if is_case(p)],
    }
    seen = {str(p.get('slug')) for group in modes.values() for p in group}
    if len(seen) != len({str(p.get('slug')) for p in posts}):
        raise ValueError('Some legal articles would have no paginated link')
    counts = {mode: max(1, (len(items) + PAGE_SIZE - 1) // PAGE_SIZE) for mode, items in modes.items()}
    changed = 0

    # posts.html is the canonical, static HTML landing page for information page 1.
    main = FIRST_RE.sub(lambda _m: initial_cards(modes['info'][:PAGE_SIZE]), template, count=1)
    main = NAV_RE.sub(lambda m: m.group(1) + pagination('info', 1, counts['info']) + m.group(2), main, count=1)
    changed += int(write_if_changed(INDEX, main))

    expected = set()
    for mode, items in modes.items():
        for number in range(1, counts[mode] + 1):
            if mode == 'info' and number == 1:
                continue
            path = OUT / f'{mode}-{number}.html'
            expected.add(path.name)
            current = main
            subset = items[(number-1) * PAGE_SIZE:number * PAGE_SIZE]
            current = FIRST_RE.sub(lambda _m: initial_cards(subset), current, count=1)
            current = NAV_RE.sub(lambda m: m.group(1) + pagination(mode, number, counts[mode]) + m.group(2), current, count=1)
            loc = BASE + page_path(mode, number)
            title = f'{MODE_TITLE[mode]} {number}페이지 | 등기로'
            summary = f'{MODE_TITLE[mode]} {number}페이지. 인천 법무사 현재두 사무소의 실제 법률정보와 사건 처리 안내 글을 모았습니다.'
            current = re.sub(r'<title>[\s\S]*?</title>', '<title>' + html.escape(title, quote=True) + '</title>', current, count=1)
            current = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1)+html.escape(summary, quote=True)+m.group(2), current, count=1)
            for tag, text in (('og:title',title), ('og:description',summary), ('og:url',loc)):
                pattern = r'(<meta property="' + re.escape(tag) + r'" content=")[^"]*(")'
                current = re.sub(pattern, lambda m: m.group(1)+html.escape(text, quote=True)+m.group(2), current, count=1)
            current = re.sub(r'(<link rel="canonical" href=")[^"]*(")', lambda m: m.group(1)+loc+m.group(2), current, count=1)
            current = current.replace('"url":"https://www.deunggiro.kr/posts.html"', '"url":"' + loc + '"')
            current = re.sub(r'(<p class="desc" id="legal-desc">)[\s\S]*?(</p>)', lambda m: m.group(1)+INTRO[mode]+m.group(2), current, count=1)
            current = re.sub(r'(<a class="mode-tab)(?: active)?(" data-mode="(info|core|case)")', lambda m: m.group(1)+(' active' if m.group(3)==mode else '')+m.group(2), current)
            changed += int(write_if_changed(path, current))

    for old in OUT.glob('*.html'):
        if re.fullmatch(r'(info|core|case)-[0-9]+\.html', old.name) and old.name not in expected:
            old.unlink()
            changed += 1
    print('CRAWLABLE_POST_PAGES', json.dumps({'modes':counts, 'files':len(expected), 'changed':changed}, ensure_ascii=False))
    return bool(changed)


if __name__ == '__main__':
    rebuild_post_pages(json.loads(POSTS.read_text(encoding='utf-8')))
