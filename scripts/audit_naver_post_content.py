import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from bs4 import BeautifulSoup, Comment

import import_naver_blog as base

ROOT = Path(__file__).resolve().parents[1]
POSTS_JSON = ROOT / 'data' / 'posts.json'
POSTS_DIR = ROOT / 'posts'

VISIBLE_BAD_RE = re.compile(
    r'(?:SEO_RELATED_POSTS_(?:START|END)|hjd219\.github\.io|(?:m\.)?blog\.naver\.com)',
    re.I,
)
PLAIN_1_TO_10_RE = re.compile(r'^\s*(?:10|[1-9])\s*[.)]\s*')
NUMBER_EMOJI_RE = re.compile(r'^(?:[1-9]\ufe0f?\u20e3|\U0001F51F)')
CIRCLED_RE = re.compile(r'^[①-⑳㉑-㊿]')


def local_audit(post):
    slug = str(post.get('slug', '')).replace('.html', '').strip()
    path = POSTS_DIR / f'{slug}.html'
    issues = []
    if not path.exists():
        return slug, issues + ['MISSING_HTML'], 0

    text = path.read_text(encoding='utf-8', errors='replace')
    soup = BeautifulSoup(text, 'html.parser')
    body = soup.select_one('.article-body')
    if body is None:
        return slug, issues + ['MISSING_ARTICLE_BODY'], 0

    visible = ' '.join(body.stripped_strings)
    if VISIBLE_BAD_RE.search(visible):
        issues.append('VISIBLE_LINK_OR_MARKER_RESIDUE')
    if soup.select('.source-note'):
        issues.append('SOURCE_NOTE_REMAINS')

    related = soup.select('.seo-related-posts')
    if len(related) != 1:
        issues.append(f'RELATED_BLOCK_COUNT={len(related)}')

    # HTML 주석은 START/END 각각 1개까지만 허용.
    comments = [str(x) for x in soup.find_all(string=lambda x: isinstance(x, Comment))]
    starts = sum('SEO_RELATED_POSTS_START' in x for x in comments)
    ends = sum('SEO_RELATED_POSTS_END' in x for x in comments)
    if starts > 1 or ends > 1:
        issues.append(f'RELATED_MARKERS={starts}/{ends}')

    # 대제목 1~10은 번호 이모지여야 하고 원숫자는 허용한다.
    for tag in body.find_all(['h2', 'h3']):
        heading = ' '.join(tag.stripped_strings).strip()
        if not heading or CIRCLED_RE.match(heading) or NUMBER_EMOJI_RE.match(heading):
            continue
        if PLAIN_1_TO_10_RE.match(heading):
            issues.append('PLAIN_HEADING_1_TO_10')
            break

    # 지나치게 긴 한 문단은 표가 평문으로 풀렸을 가능성이 있어 후보로 표시.
    for p in body.find_all('p'):
        t = ' '.join(p.stripped_strings).strip()
        if len(t) >= 260 and sum(x in t for x in ('구분', '세율', '취득', '주택', '농지', '법인', '기준')) >= 3:
            issues.append('POSSIBLE_FLATTENED_TABLE')
            break

    return slug, issues, len(body.find_all('table'))


def remote_table_count(post):
    slug = str(post.get('slug', '')).replace('.html', '').strip()
    url = str(post.get('source_url', '')).strip()
    if not url:
        return slug, None, 'NO_SOURCE_URL'
    try:
        body, _ = base.clean_article(url, slug='')
        return slug, len(BeautifulSoup(body, 'html.parser').find_all('table')), ''
    except Exception as e:
        return slug, None, f'{type(e).__name__}: {e}'


def main():
    posts = json.loads(POSTS_JSON.read_text(encoding='utf-8'))
    targets = [p for p in posts if p.get('source') == 'naver-blog']

    local = {}
    issues = []
    for post in targets:
        slug, found, tables = local_audit(post)
        local[slug] = tables
        for item in found:
            issues.append((slug, item))

    fetch_errors = []
    remote_counts = {}
    with ThreadPoolExecutor(max_workers=8) as ex:
        futures = [ex.submit(remote_table_count, p) for p in targets]
        for fut in as_completed(futures):
            slug, count, err = fut.result()
            if err:
                fetch_errors.append((slug, err))
            else:
                remote_counts[slug] = count

    for slug, remote_count in remote_counts.items():
        local_count = local.get(slug, 0)
        if remote_count > local_count:
            issues.append((slug, f'MISSING_TABLE remote={remote_count} local={local_count}'))

    print(f'CONTENT_AUDIT posts={len(targets)} issues={len(issues)} fetch_errors={len(fetch_errors)}')
    for slug, issue in issues:
        print('ISSUE', slug, issue)
    for slug, err in fetch_errors[:20]:
        print('FETCH_SKIP', slug, err)

    # 네트워크 실패는 감사 실패로 보지 않되, 실제 본문 오류는 실패 처리한다.
    if issues:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
