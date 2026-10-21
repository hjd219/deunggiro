#!/usr/bin/env python3
"""One-time, idempotent normalization of website case titles and case classification.

Preserves article bodies, URL slugs, publication dates and existing sitemap timestamps.
Only the website is changed; source Naver blog is not modified.
"""
from __future__ import annotations
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / 'data/posts.json'
CASE_LABEL = re.compile(r'^\s*\[처리사례\]\s*')
CASE_SUFFIX = re.compile(r'사례\s*[.!?。…]*$')
PREFIX_ANY = re.compile(r'\[처리사례\]\s*')
MOVED = 'inheritance-naver-224448667537'
CHURCH = 'realestate-naver-224434200680'
OLD_SUMMARY = '상속등기·절차·필요서류·주의사항'
NEW_SUMMARY = '상속포기·한정승인·절차·대응방법·주의사항'

def write(path: Path, value: str) -> bool:
    if path.read_text(encoding='utf-8') == value:
        return False
    path.write_text(value, encoding='utf-8')
    return True

def patch_exact(path: str, old: str, new: str) -> bool:
    f = ROOT / path
    s = f.read_text(encoding='utf-8')
    if old not in s:
        if new in s:
            return False
        raise RuntimeError(f'{path}: missing expected code anchor {old[:90]!r}')
    return write(f, s.replace(old, new))

def patch_article(post: dict) -> bool:
    f = ROOT / 'posts' / (post['slug'] + '.html')
    if not f.is_file():
        raise RuntimeError(f'Missing article: {f}')
    source = f.read_text(encoding='utf-8')
    marker = re.search(r'<div class=["\x27]article-body["\x27][^>]*>', source, flags=re.I)
    stop = source.find('<!-- SEO_RELATED_POSTS_START -->', marker.end()) if marker else -1
    if not marker or stop < 0:
        raise RuntimeError(f'Cannot protect article body: {f}')
    before = PREFIX_ANY.sub('', source[:marker.start()])
    body = source[marker.start():stop]
    after = PREFIX_ANY.sub('', source[stop:])
    if post['slug'] == MOVED:
        before = before.replace(OLD_SUMMARY, NEW_SUMMARY)
        before = before.replace('content="상속등기" name="dg-category"',
                                'content="상속포기·한정승인" name="dg-category"')
        before = before.replace('name="dg-category" content="상속등기"',
                                'name="dg-category" content="상속포기·한정승인"')
        before = before.replace('<span class="badge">상속등기</span>',
                                '<span class="badge">상속포기·한정승인</span>')
        before = before.replace('"name":"상속등기","item":"https://www.deunggiro.kr/inheritance.html"',
                                '"name":"상속포기·한정승인","item":"https://www.deunggiro.kr/renunciation.html"')
        before = before.replace('<a href="/inheritance.html">상속등기</a>',
                                '<a href="/renunciation.html">상속포기·한정승인</a>')
    result = before + body + after
    assert result[result.index(marker.group()):result.index('<!-- SEO_RELATED_POSTS_START -->')] == body, f'Body unexpectedly changed: {f}'
    if post['slug'] in labeled:
        if '[처리사례]' in result[:result.index(marker.group())]:
            raise RuntimeError(f'Unremoved title prefix {f}')
    return write(f, result)

def short_title(raw: str) -> str:
    s = re.sub(r'^\s*(?:\[[^\]]{1,45}\]\s*)+', '', raw)
    s = re.sub(r'^\s*\(처리사례\)\s*', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    part = re.split(r'\s*[｜|]\s*', s)[0].strip()
    if len(part) >= 7:
        s = part
    s = re.sub(r'^인천\s+(?=\S)', '', s)
    s = re.sub(r'\s*(?:쉽게\s*정리|완벽\s*정리|핵심\s*정리|총정리|완벽하게\s*정리)\s*$', '', s).strip()
    if len(s) <= 24:
        return s
    cut = s[:24]
    last = cut.rfind(' ')
    cut = cut[:last] if last >= 15 else s[:22]
    return re.sub(r'[\s,，·]+$', '', cut) + '…'

def rebuild_service_cards(posts: list[dict]) -> int:
    categories = {
        'inheritance': ('inheritance.html', ('상속등기', '상속재산분할')),
        'renunciation': ('renunciation.html', ('상속포기·한정승인',)),
        'corporate': ('corporate.html', ('법인등기',)),
        'realestate': ('realestate.html', ('부동산등기',)),
        'family': ('family.html', ('가사',)),
    }
    n = 0
    track = re.compile(r'(<div class="dg-blog-track"[^>]*>)[\s\S]*?(</div><p class="dg-blog-note")')
    for name, (page, cats) in categories.items():
        f = ROOT / page
        old = f.read_text(encoding='utf-8')
        selected = [p for p in posts if p.get('category') in cats]
        cards = []
        for p in selected:
            e = lambda t: html.escape(str(t or ''), quote=True)
            url = '/posts/' + str(p['slug']) + '.html'
            thumb = p.get('thumbnail') or '/favicon.png'
            date = p.get('date', '')
            cards.append(
                f'<a class="dg-blog-card" href="{e(url)}" aria-label="{e(p["title"])}">'
                f'<img class="dg-blog-thumb" loading="lazy" decoding="async" src="{e(thumb)}" alt="" '
                'onerror="this.onerror=null;this.src=\x27/favicon.png\x27">'
                f'<div class="dg-blog-card-content"><time datetime="{e(date)}">{e(date)}</time>'
                f'<h3 title="{e(p["title"])}">{e(short_title(p["title"]))}</h3></div></a>'
            )
        if not track.search(old):
            raise RuntimeError(f'Missing service blog track: {page}')
        updated = track.sub(lambda m: m.group(1) + ''.join(cards) + m.group(2), old, count=1)
        updated = re.sub(r'(<span class="dg-blog-status" aria-live="polite">)\d+개 글(</span>)',
                         lambda m: m.group(1) + str(len(selected)) + '개 글' + m.group(2), updated, count=1)
        n += int(write(f, updated))
    return n

def apply() -> None:
    global labeled
    posts = json.loads(POSTS.read_text(encoding='utf-8'))
    labeled = set()
    new_case = set()
    for p in posts:
        previous = p['title']
        if CASE_LABEL.match(previous):
            labeled.add(p['slug'])
            p['title'] = CASE_LABEL.sub('', previous)
            if p.get('keywords'):
                p['keywords'] = CASE_LABEL.sub('', p['keywords'])
        if p['slug'] in labeled or CASE_SUFFIX.search(p['title']) or p['slug'] == CHURCH:
            p['is_case'] = True
            new_case.add(p['slug'])
        if p['slug'] == MOVED:
            p['category'] = '상속포기·한정승인'
            p['summary'] = p['summary'].replace(OLD_SUMMARY, NEW_SUMMARY)
    assert len(posts) >= 397, 'Post count unexpectedly decreased'
    assert not any('[처리사례]' in p['title'] for p in posts)
    if len(new_case) < 38:
        raise RuntimeError(f'Unexpectedly few case articles: {len(new_case)}')
    print('CASE_TITLE_CLEANUP', 'removed', len(labeled), 'cases', len(new_case), 'posts', len(posts))
    write(POSTS, json.dumps(posts, ensure_ascii=False, indent=2) + '\n')

    # Future scheduled imports: normalize the source title *before* saving the local copy.
    core_path = 'scripts/import_naver_blog_clean.py'
    core_marker = "def norm(v): return re.sub(r'[^0-9A-Za-z가-힣]+','',html.unescape(v or '')).lower()"
    core_new = (
        "def strip_case_prefix(title):\n"
        " return re.sub(r'^\\s*\\[처리사례\\]\\s*', '', str(title or '')).strip()\n"
        "def is_case_title(title):\n"
        " return bool(re.match(r'^\\s*\\[처리사례\\]', str(title or '')) or "
        "re.search(r'사례\\s*[.!?。…]*$', strip_case_prefix(title)))\n"
        + core_marker
    )
    patch_exact(core_path, core_marker, core_new)
    importer = ROOT / 'scripts/import_naver_blog.py'
    imp = importer.read_text(encoding='utf-8')
    imp = imp.replace('            title, date = fetch_metadata(n)\n            if not title:',
                      '            source_title, date = fetch_metadata(n)\n'
                      '            title = core.strip_case_prefix(source_title)\n            if not title:')
    imp = imp.replace("                    'title': title,\n                    'category': core.category(title),",
                      "                    'title': title,\n"
                      "                    **({'is_case': True} if core.is_case_title(source_title) else {}),\n"
                      "                    'category': core.category(title),")
    if 'core.is_case_title(source_title)' not in imp:
        raise RuntimeError('Importer is_case field not patched')
    write(importer, imp)

    pycategory = ROOT / 'scripts/category_rules.py'
    s = pycategory.read_text(encoding='utf-8')
    anchor = '    # 기존 상속포기·한정승인 글은 해당 핵심어가 있으면 불필요하게 다른 상속 카테고리로 옮기지 않는다.'
    if anchor not in s:
        raise RuntimeError('Category rule anchor not found')
    s = s.replace(anchor,
        "    if '상속포기한사례' in re.sub(r'\\s+', '', t):\n"
        "        return CATEGORY_RENUNCIATION, 'renunciation-case-explicit'\n\n" + anchor)
    write(pycategory, s)

    opt = ROOT / 'scripts/optimize_post_titles.py'
    s = opt.read_text(encoding='utf-8')
    write(opt, s.replace('[처리사례] ', ''))
    # Browser case tab uses stable metadata, or a title ending in '사례'.
    page = ROOT / 'posts.html'
    s = page.read_text(encoding='utf-8')
    old = "function isCase(p){const t=(p.title||'')+' '+(p.summary||'');return /처리사례|실제사례|실제 사례|허가 사례|선임 사례|등기 사례|신청 사례|경정 사례/.test(t)}"
    new = "function isCase(p){return p.is_case===true||/사례\\s*[.!?。…]*$/.test((p.title||'').trim())}"
    if old not in s:
        raise RuntimeError('Browser case JS anchor missing')
    write(page, s.replace(old, new))

    pagination = ROOT / 'scripts/generate_post_pagination.py'
    s = pagination.read_text(encoding='utf-8')
    s = s.replace("CASE_RE = re.compile(r'처리사례|실제사례|실제 사례|허가 사례|선임 사례|등기 사례|신청 사례|경정 사례')",
                  "CASE_RE = re.compile(r'사례\\s*[.!?。…]*$')")
    old = "return bool(CASE_RE.search(str(p.get('title', '')) + ' ' + str(p.get('summary', ''))))"
    new = "return p.get('is_case') is True or bool(CASE_RE.search(str(p.get('title', '')).strip()))"
    if old not in s:
        raise RuntimeError('Pagination case code anchor missing')
    write(pagination, s.replace(old, new))

    servicejs = ROOT / 'assets/service-blog.js'
    s = servicejs.read_text(encoding='utf-8')
    old = "var isCase=function(p){return /^\\s*\\[(?:처리사례|해결사례|진행사례)\\]/.test(p.title||'')||!!explicitCaseSlugs[p.slug]};"
    new = "var isCase=function(p){return p.is_case===true||/사례\\s*[.!?。…]*$/.test((p.title||'').trim())||!!explicitCaseSlugs[p.slug]};"
    if old not in s:
        raise RuntimeError('Service case JS anchor missing')
    write(servicejs, s.replace(old, new))

    legacyjs = ROOT / 'assets/posts-case-tabs.js'
    s = legacyjs.read_text(encoding='utf-8')
    old = "const CASE_RE=/^\\s*\\[?처리사례\\]?/;"
    if old not in s:
        raise RuntimeError('Legacy case regex anchor missing')
    s = s.replace(old, "const CASE_RE=/사례\\s*[.!?。…]*$/;")
    s = s.replace("const isCase=p=>CASE_RE.test(String(p.title||''));",
                  "const isCase=p=>p.is_case===true||CASE_RE.test(String(p.title||'').trim());")
    write(legacyjs, s)

    # Remove the prefix in all article title metadata, but preserve article-body HTML exactly.
    changed = sum(patch_article(p) for p in posts)
    pages = rebuild_service_cards(posts)
    rss = ROOT / 'rss.xml'
    s = rss.read_text(encoding='utf-8')
    write(rss, re.sub(r'(<title>)\[처리사례\]\s*', r'\1', s))
    # Regenerate crawlable static archive pages from the existing site generator.
    from generate_post_pagination import rebuild_post_pages
    rebuilt = rebuild_post_pages(posts)
    print('CASE_TITLE_DONE', 'articles_changed', changed,
          'service_pages', pages, 'archive_rebuilt', bool(rebuilt), 'case_total', len(new_case))

if __name__ == '__main__':
    apply()
