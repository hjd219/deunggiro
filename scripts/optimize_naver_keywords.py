import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS_JSON = ROOT / 'data' / 'posts.json'
POSTS_DIR = ROOT / 'posts'

STOP = {
    '총정리','완벽정리','한눈에','정리','절차','방법','필요서류','서류','비용','기간','관할','기준','주의사항','주의',
    '어떻게','되나요','하나요','할까요','해야','하는','경우','관련','최신','안내','가이드','대한','위한','부터','까지',
    '얼마나','나올까','무엇','무슨','가능','가능할까','확인','핵심','내용','준비','문제','실제','총정리취득세'
}

PRIORITY = (
    '상속등기','상속포기','한정승인','상속재산분할','상속취득세','대습상속','특별한정승인',
    '법인등기','법인설립','1인법인','대표이사','임원변경','본점이전','목적변경','상호변경','자본금','증자','감자',
    '부동산등기','소유권이전','부동산매매','부동산증여','증여등기','근저당','가압류','전세권','취득세',
    '협의이혼','재판이혼','개명','성년후견'
)


def clean_title(v):
    v = html.unescape(str(v or ''))
    v = re.sub(r'^\s*\[[^\]]+\]\s*', '', v)
    v = re.sub(r'[|·,:!?()\[\]{}↔→]+', ' ', v)
    return re.sub(r'\s+', ' ', v).strip()


def body_text(slug):
    p = POSTS_DIR / f'{slug}.html'
    if not p.exists():
        return ''
    s = p.read_text(encoding='utf-8')
    m = re.search(r'<div class=["\']article-body["\']>(.*?)</div>', s, re.I | re.S)
    if m:
        s = m.group(1)
    s = re.sub(r'<script[\s\S]*?</script>|<style[\s\S]*?</style>', ' ', s, flags=re.I)
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', html.unescape(s)).strip()


def keywords(title, category, body):
    title_clean = clean_title(title)
    source = title_clean + ' ' + str(category or '') + ' ' + str(body or '')[:900]
    compact = re.sub(r'\s+', '', source)
    out = []

    def add(v):
        v = re.sub(r'\s+', ' ', str(v or '')).strip(' ,·|-')
        if not v or v in STOP or len(v) < 2 or len(v) > 24 or v in out:
            return
        out.append(v)

    add(category)
    if category and not str(category).startswith('인천'):
        add('인천 ' + str(category))

    for term in PRIORITY:
        if term in compact or term in source:
            add(term)

    parts = [x.strip() for x in re.split(r'\s+(?:절차|비용|필요서류|방법|기간|기준|총정리)\b', title_clean, maxsplit=1) if x.strip()]
    if parts:
        subject = parts[0]
        if 2 <= len(subject) <= 24:
            add(subject)

    words = re.findall(r'[가-힣A-Za-z0-9]{2,}', source)
    freq = {}
    first = {}
    for i, w in enumerate(words):
        if w in STOP or re.fullmatch(r'20\d{2}', w):
            continue
        freq[w] = freq.get(w, 0) + 1
        first.setdefault(w, i)
    ranked = sorted(freq, key=lambda w: (-(freq[w] * 10 + min(len(w), 8)), first[w]))
    for w in ranked:
        add(w)
        if len(out) >= 8:
            break

    return ', '.join(out[:8])


def patch_meta(path, value):
    if not path.exists():
        return False
    s = path.read_text(encoding='utf-8')
    safe = html.escape(value, quote=True)
    pat = re.compile(r'<meta\s+name=["\']keywords["\']\s+content=["\'][^"\']*["\']\s*/?>', re.I)
    tag = f'<meta name="keywords" content="{safe}">'
    if pat.search(s):
        new = pat.sub(tag, s, count=1)
    else:
        new = s.replace('</head>', tag + '\n</head>', 1)
    if new != s:
        path.write_text(new, encoding='utf-8')
        return True
    return False


def main():
    posts = json.loads(POSTS_JSON.read_text(encoding='utf-8'))
    changed_posts = 0
    changed_pages = 0
    for post in posts:
        if post.get('source') != 'naver-blog':
            continue
        slug = str(post.get('slug', '')).replace('.html', '').strip()
        if not slug:
            continue
        value = keywords(post.get('title', ''), post.get('category', ''), body_text(slug))
        if not value:
            continue
        if post.get('keywords') != value:
            post['keywords'] = value
            changed_posts += 1
        if patch_meta(POSTS_DIR / f'{slug}.html', value):
            changed_pages += 1
    POSTS_JSON.write_text(json.dumps(posts, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'naver SEO keywords optimized: posts={changed_posts}, pages={changed_pages}')


if __name__ == '__main__':
    main()
