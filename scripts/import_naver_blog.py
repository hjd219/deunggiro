from __future__ import annotations

import html
import json
import re
import sys
from datetime import datetime
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse, parse_qs

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
POSTS_JSON = ROOT / 'data' / 'posts.json'
POSTS_DIR = ROOT / 'posts'
BLOG_ID = 'hjd21'
RSS_URL = f'https://rss.blog.naver.com/{BLOG_ID}.xml'
BASE = 'https://www.deunggiro.kr'
MAX_IMPORT = 3

CATEGORY_RULES = [
    ('상속포기·한정승인', ('상속포기','한정승인','특별한정승인','상속채무','망인 예금','보험금','해지환급금')),
    ('상속재산분할', ('상속재산분할','상속분쟁','기여분','특별수익','협조거부','연락두절')),
    ('법인등기', ('법인','주식회사','유한회사','대표이사','이사','감사','주주','본점이전','자본금','증자','감자','상호변경','목적변경','해산','청산')),
    ('가사', ('협의이혼','재판이혼','이혼','개명','성년후견','한정후견','친권','양육비')),
    ('부동산등기', ('근저당','가압류','등기권리증','등기필증','매매','증여','전세권','소유권이전','부동산','재산분할등기','신탁등기')),
    ('상속등기', ('상속등기','대습상속','상속취득세','상속인','상속지분','상속재산','유언','부모님 사망','가족 사망')),
]

UA = {'User-Agent': 'Mozilla/5.0 (compatible; DeunggiroBlogImporter/1.1; +https://www.deunggiro.kr/)'}


def get(url: str) -> requests.Response:
    r = requests.get(url, headers=UA, timeout=25)
    r.raise_for_status()
    # 네이버 페이지는 UTF-8인데 apparent_encoding이 ISO-8859-1/Windows 계열로
    # 잘못 추정되는 경우가 있어 한글이 ë²•ì... 형태로 깨질 수 있다.
    # 실제 바이트가 UTF-8로 정상 해석되면 UTF-8을 우선 사용한다.
    try:
        r.content.decode('utf-8')
        r.encoding = 'utf-8'
    except UnicodeDecodeError:
        if not r.encoding:
            r.encoding = r.apparent_encoding or 'utf-8'
    return r


def norm_title(v: str) -> str:
    v = html.unescape(v or '')
    v = re.sub(r'^\s*\[[^\]]+\]\s*', '', v)
    return re.sub(r'[^0-9A-Za-z가-힣]+', '', v).lower()


def infer_category(title: str) -> str:
    for category, words in CATEGORY_RULES:
        if any(w in title for w in words):
            return category
    return '기타'


def log_no_from_url(url: str) -> str:
    m = re.search(r'/(\d{6,})(?:\?|$)', url)
    if m:
        return m.group(1)
    q = parse_qs(urlparse(url).query)
    return (q.get('logNo') or [''])[0]


def resolve_post_view(url: str) -> str:
    r = get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    iframe = soup.select_one('iframe#mainFrame, iframe[name="mainFrame"]')
    if iframe and iframe.get('src'):
        return urljoin('https://blog.naver.com/', iframe['src'])
    log_no = log_no_from_url(url)
    if log_no:
        return f'https://blog.naver.com/PostView.naver?blogId={BLOG_ID}&logNo={log_no}&redirect=Dlog&widgetTypeCall=true&directAccess=false'
    return url


def clean_article(url: str) -> tuple[str, str]:
    view = resolve_post_view(url)
    r = get(view)
    soup = BeautifulSoup(r.text, 'html.parser')
    root = soup.select_one('.se-main-container') or soup.select_one('#postViewArea') or soup.select_one('.post-view')
    if root is None:
        raise RuntimeError('네이버 본문 영역을 찾지 못했습니다.')

    for bad in root.select('script,style,noscript,iframe,button'):
        bad.decompose()
    for tag in root.find_all(True):
        if tag.name == 'img':
            src = tag.get('data-lazy-src') or tag.get('data-src') or tag.get('src') or ''
            if src.startswith('//'):
                src = 'https:' + src
            tag.attrs = {'src': src, 'alt': ''} if src else {}
        elif tag.name == 'a':
            href = tag.get('href') or ''
            tag.attrs = {'href': href, 'target': '_blank', 'rel': 'noopener noreferrer'} if href.startswith('http') else {}
        else:
            tag.attrs = {}

    parts = []
    for el in root.find_all(['h2','h3','p','blockquote','ul','ol','img'], recursive=True):
        if el.find_parent(['p','blockquote','ul','ol']) and el.name != 'img':
            continue
        if el.name == 'img':
            src = el.get('src') or ''
            if src:
                parts.append(f'<p><img src="{html.escape(src, quote=True)}" alt="" loading="lazy" decoding="async"></p>')
            continue
        txt = ' '.join(el.stripped_strings)
        if not txt:
            continue
        if el.name in ('h2','h3'):
            parts.append(f'<{el.name}>{html.escape(txt)}</{el.name}>')
        elif el.name == 'blockquote':
            parts.append(f'<blockquote>{html.escape(txt)}</blockquote>')
        elif el.name in ('ul','ol'):
            lis = [' '.join(li.stripped_strings) for li in el.find_all('li', recursive=False)]
            if lis:
                parts.append(f'<{el.name}>' + ''.join(f'<li>{html.escape(x)}</li>' for x in lis if x) + f'</{el.name}>')
        else:
            parts.append(f'<p>{html.escape(txt)}</p>')

    body = '\n'.join(parts)
    text = re.sub(r'\s+', ' ', ' '.join(root.stripped_strings)).strip()
    return body, text


def summary_from(text: str, title: str) -> str:
    text = re.sub(r'\s+', ' ', text or '').strip()
    if len(text) >= 45:
        return text[:155].rstrip(' ,·')
    return f'{title} 관련 절차와 핵심 내용을 정리한 등기로 법률정보입니다.'[:155]


def build_html(post: dict, body: str) -> str:
    title = html.escape(post['title'])
    summary = html.escape(post['summary'])
    cat = html.escape(post['category'])
    date = html.escape(post['date'])
    slug = html.escape(post['slug'], quote=True)
    source = html.escape(post['source_url'], quote=True)
    intro_title = re.sub(r'^\s*\[[^\]]+\]\s*', '', post['title'])
    intro = html.escape(f'이 글에서는 {intro_title}에 관해 핵심 절차와 준비사항을 홈페이지용으로 정리합니다.')
    return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | 현재두 법무사 사무소</title><meta name="description" content="{summary}"><meta name="keywords" content="{title}">
<meta property="og:type" content="article"><meta property="og:title" content="{title}"><meta property="og:description" content="{summary}"><meta property="og:url" content="{BASE}/posts/{slug}.html">
<link rel="canonical" href="{BASE}/posts/{slug}.html"><meta name="dg-title" content="{title}"><meta name="dg-category" content="{cat}"><meta name="dg-date" content="{date}"><meta name="dg-summary" content="{summary}">
<link rel="stylesheet" href="/assets/article-v2.css?v=4"><link rel="stylesheet" href="/assets/site-shell.css"><link rel="stylesheet" href="/assets/latest-posts.css"></head>
<body class="article-v2"><header class="header"><div class="container header-inner"><a class="logo" href="/"><span>등기로</span><small>현재두 법무사 사무소 · 인천</small></a><nav class="nav"><a href="/inheritance.html">상속</a><a href="/corporate.html">법인등기</a><a href="/realestate.html">부동산등기</a><a href="/posts.html">법률정보</a></nav><a class="btn btn-primary mobile-only" href="tel:0324251500">전화상담</a></div></header>
<main class="section"><div class="container article-wrap"><article class="article"><div class="post-meta"><span class="badge">{cat}</span>{date}</div><h1>{title}</h1><p class="desc">{summary}</p><div class="article-body"><p><strong>{intro}</strong></p>{body}<p style="margin-top:28px;font-size:13px;color:#667085">네이버 블로그에 작성한 내용을 등기로 홈페이지 형식에 맞게 정리했습니다. <a href="{source}" target="_blank" rel="noopener noreferrer">원문 보기</a></p></div><!-- SEO_RELATED_POSTS_START --><!-- SEO_RELATED_POSTS_END --></article></div></main>
<section class="contact"><div class="container contact-grid"><div><div class="label">CONSULTATION</div><h2>복잡한 등기절차, 등기로에서 확인하세요.</h2><p>상속 · 법인 · 부동산 등 필요한 절차와 준비서류를 확인할 수 있습니다.</p></div><a class="phone" href="tel:0324251500">032-425-1500</a></div></section>
<footer class="footer"><div class="container"><strong>등기로 · 현재두 법무사 사무소</strong><div>인천 미추홀구 경원대로 873, 201호 · 032-425-1500</div></div></footer>
<script src="/assets/latest-posts.js" defer></script><script src="/assets/article-cta.js" defer></script></body></html>'''


def load_posts() -> list[dict]:
    return json.loads(POSTS_JSON.read_text(encoding='utf-8'))


def fetch_feed_items() -> list[dict]:
    r = get(RSS_URL)
    soup = BeautifulSoup(r.content, 'xml')
    out = []
    for item in soup.find_all('item'):
        title = item.title.get_text(' ', strip=True) if item.title else ''
        link = item.link.get_text(strip=True) if item.link else ''
        pub = item.pubDate.get_text(strip=True) if item.pubDate else ''
        if not title or not link:
            continue
        try:
            d = parsedate_to_datetime(pub).astimezone().strftime('%Y-%m-%d') if pub else datetime.now().strftime('%Y-%m-%d')
        except Exception:
            d = datetime.now().strftime('%Y-%m-%d')
        out.append({'title': html.unescape(title), 'link': link, 'date': d})
    return out


def looks_mojibake(text: str) -> bool:
    if not text:
        return False
    markers = ('ë','ì','í','â€','Â','�')
    score = sum(text.count(m) for m in markers)
    return score >= 4


def repair_existing_imports(posts: list[dict]) -> int:
    repaired = 0
    for post in posts:
        if post.get('source') != 'naver-blog' or not post.get('source_url'):
            continue
        slug = str(post.get('slug','')).replace('.html','')
        page = POSTS_DIR / f'{slug}.html'
        page_text = page.read_text(encoding='utf-8', errors='ignore') if page.exists() else ''
        if not (looks_mojibake(str(post.get('summary',''))) or looks_mojibake(page_text)):
            continue
        try:
            body, text = clean_article(post['source_url'])
        except Exception as e:
            print('REPAIR_SKIP', slug, e, file=sys.stderr)
            continue
        if len(text) < 80 or looks_mojibake(text):
            print('REPAIR_SKIP_BAD_TEXT', slug, file=sys.stderr)
            continue
        post['summary'] = summary_from(text, post.get('title',''))
        post['category'] = infer_category(post.get('title','') + ' ' + text[:500])
        page.write_text(build_html(post, body), encoding='utf-8')
        repaired += 1
        print('REPAIRED', slug, post.get('title',''))
    return repaired


def main():
    POSTS_DIR.mkdir(exist_ok=True)
    posts = load_posts()
    repaired = repair_existing_imports(posts)
    existing_titles = {norm_title(p.get('title','')) for p in posts}
    existing_sources = {str(p.get('source_url','')).strip() for p in posts if p.get('source_url')}
    imported = 0

    for item in fetch_feed_items():
        if imported >= MAX_IMPORT:
            break
        if item['link'] in existing_sources or norm_title(item['title']) in existing_titles:
            continue
        log_no = log_no_from_url(item['link'])
        if not log_no:
            continue
        try:
            body, text = clean_article(item['link'])
        except Exception as e:
            print('SKIP', item['link'], e, file=sys.stderr)
            continue
        if len(text) < 80 or looks_mojibake(text):
            continue
        slug = f'naver-{log_no}'
        if any(str(p.get('slug','')).replace('.html','') == slug for p in posts):
            continue
        post = {
            'title': item['title'],
            'category': infer_category(item['title'] + ' ' + text[:500]),
            'date': item['date'],
            'slug': slug,
            'keywords': item['title'],
            'summary': summary_from(text, item['title']),
            'source_url': item['link'],
            'source': 'naver-blog'
        }
        (POSTS_DIR / f'{slug}.html').write_text(build_html(post, body), encoding='utf-8')
        posts.insert(0, post)
        existing_titles.add(norm_title(post['title']))
        existing_sources.add(item['link'])
        imported += 1
        print('IMPORTED', slug, post['title'])

    if imported or repaired:
        POSTS_JSON.write_text(json.dumps(posts, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('NAVER_IMPORT_COUNT', imported)
    print('NAVER_REPAIR_COUNT', repaired)


if __name__ == '__main__':
    main()
