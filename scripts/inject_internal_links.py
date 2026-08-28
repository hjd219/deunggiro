import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS_JSON = ROOT / 'data' / 'posts.json'
POSTS_DIR = ROOT / 'posts'
START = '<!-- SEO_RELATED_POSTS_START -->'
END = '<!-- SEO_RELATED_POSTS_END -->'
STOP = {
    '총정리','정리','절차','방법','기준','주의사항','주의','필요서류','서류','비용','기간','관할','신청','안내','가이드',
    '인천','법무사','법률정보','경우','관련','이란','이유','문제','확인','작성','작성방법','해야','하는','있을까','있나요','가능할까'
}


def tokens(text):
    words = re.findall(r'[가-힣A-Za-z0-9]{2,}', str(text or ''))
    return {w for w in words if w not in STOP}


def score(current, candidate):
    if current is candidate:
        return -1
    s = 0
    if str(current.get('category','')).strip() and str(current.get('category','')).strip() == str(candidate.get('category','')).strip():
        s += 100
    a = tokens(current.get('title',''))
    b = tokens(candidate.get('title',''))
    overlap = a & b
    s += len(overlap) * 18
    for w in overlap:
        s += min(len(w), 8)
    if str(candidate.get('date','')):
        s += 1
    return s


def related_block(current, posts):
    ranked = []
    for p in posts:
        if str(p.get('slug','')).replace('.html','') == str(current.get('slug','')).replace('.html',''):
            continue
        ranked.append((score(current, p), str(p.get('date','')), p))
    ranked.sort(key=lambda x: (x[0], x[1]), reverse=True)
    chosen = [x[2] for x in ranked[:3] if x[0] >= 0]
    if not chosen:
        return START + '\n' + END
    items = []
    for p in chosen:
        slug = html.escape(str(p.get('slug','')).replace('.html',''), quote=True)
        title = html.escape(str(p.get('title','')).strip())
        category = html.escape(str(p.get('category','') or '법률정보').strip())
        items.append(f'<li><a href="/posts/{slug}.html"><span>{category}</span><strong>{title}</strong></a></li>')
    return (
        START + '\n'
        '<section class="seo-related-posts" aria-label="관련 법률정보">'
        '<h2>함께 보면 좋은 글</h2><ul>' + ''.join(items) + '</ul></section>\n' + END
    )


def main():
    posts = json.loads(POSTS_JSON.read_text(encoding='utf-8'))
    pat = re.compile(re.escape(START) + r'[\s\S]*?' + re.escape(END), re.M)
    changed = 0
    for post in posts:
        if post.get('source') != 'naver-blog':
            continue
        slug = str(post.get('slug','')).replace('.html','')
        if not slug:
            continue
        path = POSTS_DIR / f'{slug}.html'
        if not path.exists():
            continue
        text = path.read_text(encoding='utf-8')
        block = related_block(post, posts)
        if pat.search(text):
            new = pat.sub(block, text, count=1)
        else:
            marker = '</article>'
            new = text.replace(marker, block + marker, 1) if marker in text else text
        if new != text:
            path.write_text(new, encoding='utf-8')
            changed += 1
    print('internal related links injected:', changed)


if __name__ == '__main__':
    main()
