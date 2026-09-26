import html
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup, Comment

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


HUB_RULES = [
    (('/inheritance-overseas-heir.html', '해외거주·외국국적 상속인 상속등기 안내'), ('해외거주','해외 거주','외국국적','외국 국적','미국','일본','호주','영주권','시민권','아포스티유')),
    (('/inheritance-minor-heir.html', '미성년자 상속인 상속등기 안내'), ('미성년자','미성년 상속인','특별대리인')),
    (('/inheritance-missing-heir.html', '연락두절·행방불명 상속인 안내'), ('연락두절','연락 두절','행방불명','실종선고','실종 선고')),
    (('/inheritance-substitute-succession.html', '대습상속 안내'), ('대습상속','대습 상속')),
    (('/inheritance-division.html', '상속재산분할 안내'), ('상속재산분할','상속재산 분할','협의분할','협의 분할','기여분','특별수익')),
    (('/renunciation-limited-acceptance-liquidation.html', '한정승인 후 청산 안내'), ('상속재산파산','상속재산 파산','한정승인 후','청산')),
    (('/renunciation-after-procedure.html', '상속포기 후 절차 안내'), ('상속포기 후','후순위 상속인','후순위상속인')),
]

CATEGORY_HUBS = {
    '상속등기': ('/inheritance.html', '상속등기 핵심안내'),
    '상속재산분할': ('/inheritance.html', '상속등기 핵심안내'),
    '상속포기·한정승인': ('/renunciation.html', '상속포기·한정승인 핵심안내'),
    '법인등기': ('/corporate.html', '법인등기 핵심안내'),
    '부동산등기': ('/realestate.html', '부동산등기 핵심안내'),
    '가사': ('/family.html', '가사 핵심안내'),
}


def hub_link(current):
    text = ' '.join((str(current.get('title','')), str(current.get('keywords','')), str(current.get('summary',''))))
    category = str(current.get('category','')).strip()

    # 세부 주제 링크는 해당 상속 카테고리에서만 사용해 엉뚱한 허브 연결을 막는다.
    if category in ('상속등기', '상속재산분할', '상속포기·한정승인'):
        for (href, label), words in HUB_RULES:
            if any(word in text for word in words):
                if href.startswith('/renunciation') or href.startswith('/limited-acceptance'):
                    if category != '상속포기·한정승인':
                        continue
                elif category == '상속포기·한정승인' and href.startswith('/inheritance-'):
                    continue
                return href, label

    return CATEGORY_HUBS.get(category)



CALCULATOR_INTENT = (
    '비용', '취득세', '등록면허세', '법무사 보수', '법무사보수',
    '국민주택채권', '채권 할인', '채권할인', '설립비용', '변경비용'
)


def calculator_link(current):
    """계산 의도가 명확한 글에만 계산기 링크를 붙인다."""
    category = str(current.get('category','')).strip()
    text = ' '.join((str(current.get('title','')), str(current.get('keywords','')), str(current.get('summary',''))))
    if not any(word in text for word in CALCULATOR_INTENT):
        return None

    if category == '법인등기':
        job = ''
        if '본점이전' in text or '주소이전' in text or '본점주소' in text:
            job = '?job=move'
        elif '증자' in text or '자본금' in text:
            job = '?job=inc'
        elif '임원변경' in text or '대표이사' in text or '이사' in text or '감사' in text:
            job = '?job=off'
        elif '법인설립' in text or '회사설립' in text or '주식회사 설립' in text:
            job = '?job=est'
        return '/corporate-calculator.html' + job, '법인등기 비용 계산하기'

    if category in ('상속등기', '상속재산분할'):
        return '/acquisition-calculator.html?mode=inherit', '상속등기 비용 계산하기'

    if category == '부동산등기':
        if '이혼' in text or '재산분할' in text:
            mode = 'divorce'
            label = '이혼 재산분할등기 비용 계산하기'
        elif '증여' in text and '매매' not in text and '상속' not in text:
            mode = 'gift'
            label = '증여등기 비용 계산하기'
        elif '매매' in text and '증여' not in text and '상속' not in text:
            mode = 'sale'
            label = '매매등기 비용 계산하기'
        elif '상속' in text and '증여' not in text and '매매' not in text:
            mode = 'inherit'
            label = '상속등기 비용 계산하기'
        else:
            return '/acquisition-calculator.html', '부동산등기 비용 계산하기'
        return '/acquisition-calculator.html?mode=' + mode, label

    return None


def calculator_block(current):
    target = calculator_link(current)
    if not target:
        return ''
    href, label = target
    return (
        '<p class="seo-calculator-link">'
        f'<a href="{html.escape(href, quote=True)}">{html.escape(label)}</a>'
        '</p>'
    )

def hub_block(current):
    target = hub_link(current)
    if not target:
        return ''
    href, label = target
    return (
        '<p class="seo-hub-link">'
        f'<a href="{html.escape(href, quote=True)}">{html.escape(label)}</a>'
        '</p>'
    )


CORE_QUOTAS = {
    '상속등기': 30,
    '상속포기·한정승인': 25,
    '상속재산분할': 5,
    '법인등기': 20,
    '부동산등기': 15,
    '가사': 5,
}

CORE_TERMS = (
    '상속등기','상속포기','한정승인','특별한정승인','상속재산분할','대습상속','미성년',
    '해외','외국인','재외국민','필요서류','취득세','상속순위','보험금','예금',
    '법인설립','임원','대표이사','본점이전','증자','해산','청산','과태료','의사록','공증',
    '소유권이전','증여','근저당','전세권','등기권리증','미등기','성년후견','특별대리인','인천'
)


def core_score(post):
    text = ' '.join((str(post.get('title','')), str(post.get('keywords','')), str(post.get('summary',''))))
    value = 0
    for term in CORE_TERMS:
        if term in text:
            value += 10 + min(len(term), 8)
    if re.search(r'총정리|절차|방법|비용|기간|주의사항|가능|필요', text):
        value += 8
    if str(post.get('title','')).startswith('[처리사례]'):
        value += 6
    if str(post.get('title','')).startswith('[인천'):
        value += 8
    return value


def build_core_slugs(posts):
    core = set()
    for category, quota in CORE_QUOTAS.items():
        candidates = [p for p in posts if str(p.get('category','')).strip() == category]
        candidates.sort(key=lambda p: (core_score(p), str(p.get('date',''))), reverse=True)
        for p in candidates[:quota]:
            slug = str(p.get('slug','')).replace('.html','')
            if slug:
                core.add(slug)
    return core


def related_block(current, posts, core_slugs):
    ranked = []
    for p in posts:
        if str(p.get('slug','')).replace('.html','') == str(current.get('slug','')).replace('.html',''):
            continue
        candidate_score = score(current, p)
        candidate_slug = str(p.get('slug','')).replace('.html','')
        if candidate_slug in core_slugs:
            candidate_score += 35
        ranked.append((candidate_score, str(p.get('date','')), p))
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
    return START + '\n<section class="seo-related-posts" aria-label="관련 법률정보"><h2>함께 보면 좋은 글</h2><ul>' + ''.join(items) + '</ul></section>\n' + END


def remove_old_related(text):
    """깨진 마커, 중복 관련글, 빈 관련글 섹션을 모두 제거하고 한 블록만 다시 넣는다."""
    soup = BeautifulSoup(text, 'html.parser')
    changed = False

    for node in list(soup.find_all(string=True)):
        raw = str(node)
        if isinstance(node, Comment):
            if 'SEO_RELATED_POSTS_START' in raw or 'SEO_RELATED_POSTS_END' in raw:
                node.extract(); changed = True
            continue
        if 'SEO_RELATED_POSTS_START' in raw or 'SEO_RELATED_POSTS_END' in raw:
            cleaned = re.sub(r'SEO_RELATED_POSTS_(?:START|END)', '', raw).strip()
            if cleaned:
                node.replace_with(cleaned)
            else:
                parent = node.parent
                if parent and parent.name in ('p','div','span') and ' '.join(parent.stripped_strings).strip() == raw.strip():
                    parent.decompose()
                else:
                    node.extract()
            changed = True

    # 우리가 생성한 기존 허브/관련글 제거 후 매 실행마다 한 번만 다시 넣는다.
    for node in list(soup.select('.seo-hub-link, .seo-calculator-link')):
        node.decompose(); changed = True
    for sec in list(soup.select('.seo-related-posts')):
        sec.decompose(); changed = True

    # 예전 SEO 자동화가 남긴 관련글/빈 section 제거.
    # 특히 빈 section은 border-top 때문에 모바일에서 긴 빈 공간과 가로줄로 보였다.
    for sec in list(soup.find_all('section')):
        aria = str(sec.get('aria-labelledby') or '').strip()
        label = str(sec.get('aria-label') or '').strip()
        text_value = ' '.join(sec.stripped_strings).strip()
        is_related = aria == 'related-posts-title' or label in ('관련 글','관련 법률정보')
        has_related_heading = any(x in text_value for x in ('같이 보면 좋은 글','함께 보면 좋은 글'))
        if is_related or has_related_heading:
            sec.decompose(); changed = True

    return str(soup) if changed else text


def main():
    posts = json.loads(POSTS_JSON.read_text(encoding='utf-8'))
    core_slugs = build_core_slugs(posts)
    print('core SEO posts selected:', len(core_slugs))
    changed = 0
    for post in posts:
        slug = str(post.get('slug','')).replace('.html','')
        if not slug:
            continue
        path = POSTS_DIR / f'{slug}.html'
        if not path.exists():
            continue
        text = path.read_text(encoding='utf-8')
        clean = remove_old_related(text)
        block = related_block(post, posts, core_slugs)
        hub = hub_block(post)
        calculator = calculator_block(post)
        marker = '</article>'
        new = clean.replace(marker, hub + calculator + block + marker, 1) if marker in clean else clean
        if new != text:
            path.write_text(new, encoding='utf-8')
            changed += 1
    print('internal related links deduped and injected:', changed)


if __name__ == '__main__':
    main()
