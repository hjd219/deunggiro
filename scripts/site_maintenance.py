import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS_JSON = ROOT / 'data' / 'posts.json'
POSTS_PAGE = ROOT / 'posts.html'

CATEGORY_RULES = [
    ('상속포기·한정승인', ('상속포기','한정승인','특별한정승인','상속채무','사망신고 전 예금','망인 예금','보험금','해지환급금')),
    ('상속재산분할', ('상속재산분할심판','상속재산분할청구','상속분쟁','기여분','특별수익','협조거부','연락두절')),
    ('법인등기', ('법인','주식회사','유한회사','대표이사','이사','감사','주주','본점이전','자본금','증자','감자','상호변경','목적변경','해산','청산')),
    ('가사', ('협의이혼','재판이혼','이혼','개명','성년후견','한정후견','친권','양육비','가사사건')),
    ('부동산등기', ('근저당','가압류','등기권리증','등기필증','매매','증여','전세권','소유권이전','부동산','재산분할등기','신탁등기')),
    ('상속등기', ('상속등기','대습상속','상속취득세','상속인','상속지분','상속재산','유언','사망 후 상속','부모님 사망')),
]

COMMON_CSS = [
    '<link rel="stylesheet" href="/assets/article-v2.css?v=9">',
    '<link rel="stylesheet" href="/assets/site-shell.css">',
    '<link rel="stylesheet" href="/assets/latest-posts.css">',
]
COMMON_JS = [
    '<script src="/assets/site-shell.js" defer></script>',
    '<script src="/assets/article-v2.js?v=4" defer></script>',
    '<script src="/assets/latest-posts.js" defer></script>',
    '<script src="/assets/article-cta.js" defer></script>',
]


def infer_category(title: str, current: str = '') -> str:
    current = (current or '').strip()
    text = re.sub(r'\s+', ' ', title or '')
    # 이혼 관련 글은 재산분할등기·부동산 등의 단어가 함께 있어도 항상 가사로 분류한다.
    if '이혼' in text:
        return '가사'
    if current and current != '기타': return current
    for category, words in CATEGORY_RULES:
        if any(word in text for word in words): return category
    return current or '기타'


def dedupe_se_ids(text: str):
    seen = {}; changed = 0
    pat = re.compile(r'\bid=(["\'])(SE-[^"\']+)\1', re.I)
    def repl(m):
        nonlocal changed
        quote, value = m.group(1), m.group(2); seen[value] = seen.get(value, 0) + 1
        if seen[value] == 1: return m.group(0)
        changed += 1; return f'id={quote}{value}-{seen[value]}{quote}'
    return pat.sub(repl, text), changed


def dedupe_head_meta(text: str):
    m = re.search(r'(<head\b[^>]*>)([\s\S]*?)(</head>)', text, re.I)
    if not m: return text, 0
    head = m.group(2); seen = set(); removed = 0
    tag_pat = re.compile(r'<meta\b[^>]*>', re.I)
    def repl(mt):
        nonlocal removed
        tag = mt.group(0)
        name = re.search(r'\bname\s*=\s*["\']([^"\']+)["\']', tag, re.I)
        prop = re.search(r'\bproperty\s*=\s*["\']([^"\']+)["\']', tag, re.I)
        equiv = re.search(r'\bhttp-equiv\s*=\s*["\']([^"\']+)["\']', tag, re.I)
        if name: key=('name',name.group(1).lower())
        elif prop: key=('property',prop.group(1).lower())
        elif equiv: key=('http-equiv',equiv.group(1).lower())
        else: return tag
        if key in seen:
            removed += 1; return ''
        seen.add(key); return tag
    new_head = tag_pat.sub(repl, head)
    new = text[:m.start()] + m.group(1) + new_head + m.group(3) + text[m.end():]
    return new, removed


def clear_legacy_related_actions(text: str):
    changed = 0; pat = re.compile(r'<div\s+class=["\']related["\'][^>]*>([\s\S]*?)</div>', re.I)
    def repl(m):
        nonlocal changed
        plain = re.sub(r'<[^>]+>', ' ', m.group(1)); plain = re.sub(r'\s+', ' ', html.unescape(plain)).strip()
        if not plain or '032-425-1500' in plain or '법률정보 목록' in plain:
            changed += 1; return ''
        return m.group(0)
    return pat.sub(repl, text), changed


def ensure_common_assets(text: str):
    original = text
    for href in COMMON_CSS:
        path = re.search(r'href="([^"]+)"', href).group(1).split('?')[0]
        text = re.sub(rf'<link[^>]+href=["\']{re.escape(path)}(?:\?[^"\']*)?["\'][^>]*>', '', text, flags=re.I)
    text = text.replace('</head>', ''.join(COMMON_CSS) + '</head>', 1)
    for src_tag in COMMON_JS:
        path = re.search(r'src="([^"]+)"', src_tag).group(1).split('?')[0]
        text = re.sub(rf'<script[^>]+src=["\']{re.escape(path)}(?:\?[^"\']*)?["\'][^>]*>\s*</script>', '', text, flags=re.I)
    text = text.replace('</body>', ''.join(COMMON_JS) + '</body>', 1)
    return text, text != original


def sync_category_meta(text: str, category: str) -> str:
    safe = html.escape(category, quote=True); pat = re.compile(r'<meta\s+name=["\']dg-category["\']\s+content=["\'][^"\']*["\']\s*/?>', re.I); tag = f'<meta name="dg-category" content="{safe}">'
    if pat.search(text): text = pat.sub(tag, text, count=1)
    elif '</head>' in text: text = text.replace('</head>', tag + '\n</head>', 1)
    text = re.sub(r'(<span\s+class=["\']badge["\']>)[\s\S]*?(</span>)', rf'\1{safe}\2', text, count=1, flags=re.I)
    return text


def card(post: dict) -> str:
    slug=str(post.get('slug','')).strip().replace('.html',''); title=str(post.get('title','')).strip(); category=str(post.get('category','') or '법률정보').strip(); date=str(post.get('date','')).strip(); summary=str(post.get('summary','')).strip(); thumb=str(post.get('thumbnail','')).strip() or f'/assets/posts/{slug}-thumbnail.png'
    return f'<a class="post-card" href="/posts/{html.escape(slug, quote=True)}.html"><img class="post-thumb" src="{html.escape(thumb, quote=True)}" alt="{html.escape(title, quote=True)}" loading="lazy" decoding="async" onerror="this.onerror=null;this.src=\'/favicon.png\'"><div class="post-content"><div class="post-meta"><span class="badge">{html.escape(category)}</span>{html.escape(date)}</div><h3>{html.escape(title)}</h3><p>{html.escape(summary)}</p></div></a>'


def rebuild_posts_page(posts):
    if not POSTS_PAGE.exists(): return False
    text=POSTS_PAGE.read_text(encoding='utf-8'); ordered=sorted(posts,key=lambda p:(str(p.get('date','')),str(p.get('slug',''))),reverse=True); block='\n'.join(card(p) for p in ordered if p.get('slug')); pat=re.compile(r'<!-- SEO_STATIC_POSTS_START -->[\s\S]*?<!-- SEO_STATIC_POSTS_END -->',re.M); marked='<!-- SEO_STATIC_POSTS_START -->\n'+block+'\n<!-- SEO_STATIC_POSTS_END -->'
    if not pat.search(text): return False
    new=pat.sub(marked,text,count=1)
    if new!=text: POSTS_PAGE.write_text(new,encoding='utf-8'); return True
    return False


def main():
    posts=json.loads(POSTS_JSON.read_text(encoding='utf-8')); category_changes=[]; duplicate_id_fixes=0; duplicate_meta_fixes=0; legacy_related_clears=0; common_asset_fixes=0
    for post in posts:
        slug=str(post.get('slug','')).strip().replace('.html',''); old=str(post.get('category','') or '').strip(); new=infer_category(str(post.get('title','')),old)
        if new!=old: post['category']=new; category_changes.append((slug,old or '(없음)',new))
        if not slug: continue
        p=ROOT/'posts'/f'{slug}.html'
        if not p.exists(): continue
        text=p.read_text(encoding='utf-8'); text2,fixed=dedupe_se_ids(text); duplicate_id_fixes+=fixed; text2,cleared=clear_legacy_related_actions(text2); legacy_related_clears+=cleared; text2=sync_category_meta(text2,post.get('category') or new); text2,meta_removed=dedupe_head_meta(text2); duplicate_meta_fixes+=meta_removed; text2,asset_changed=ensure_common_assets(text2); common_asset_fixes+=1 if asset_changed else 0
        if text2!=text: p.write_text(text2,encoding='utf-8')
    POSTS_JSON.write_text(json.dumps(posts,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); rebuilt=rebuild_posts_page(posts)
    print('category changes:',len(category_changes)); print('duplicate SE id fixes:',duplicate_id_fixes); print('duplicate meta tags removed:',duplicate_meta_fixes); print('legacy related button blocks cleared:',legacy_related_clears); print('common article shell assets fixed:',common_asset_fixes); print('posts.html static cards rebuilt:',rebuilt)

if __name__=='__main__': main()
