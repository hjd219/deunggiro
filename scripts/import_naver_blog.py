from __future__ import annotations
import html
import json
import re
import sys
from datetime import datetime
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import parse_qs, urljoin, urlparse
import requests
from bs4 import BeautifulSoup, NavigableString, Tag
ROOT = Path(__file__).resolve().parents[1]
POSTS_JSON = ROOT / 'data' / 'posts.json'
POSTS_DIR = ROOT / 'posts'
MEDIA_ROOT = ROOT / 'assets' / 'naver-images'
BLOG_ID = 'hjd21'
RSS_URL = f'https://rss.blog.naver.com/{BLOG_ID}.xml'
TITLE_LIST_URL = 'https://blog.naver.com/PostTitleListAsync.naver'
BASE = 'https://www.deunggiro.kr'
MAX_IMPORT = 3
MAX_LIST_PAGES = 100
LIST_PAGE_SIZE = 30
CATEGORY_RULES = [('상속포기·한정승인', ('상속포기', '한정승인', '특별한정승인', '상속채무', '망인 예금', '보험금', '해지환급금')), ('상속재산분할', ('상속재산분할', '상속분쟁', '기여분', '특별수익', '협조거부', '연락두절')), ('법인등기', ('법인', '주식회사', '유한회사', '대표이사', '이사', '감사', '주주', '본점이전', '자본금', '증자', '감자', '상호변경', '목적변경', '해산', '청산')), ('가사', ('협의이혼', '재판이혼', '이혼', '개명', '성년후견', '한정후견', '친권', '양육비')), ('부동산등기', ('근저당', '가압류', '등기권리증', '등기필증', '매매', '증여', '전세권', '소유권이전', '부동산', '재산분할등기', '신탁등기')), ('상속등기', ('상속등기', '대습상속', '상속취득세', '상속인', '상속지분', '상속재산', '유언', '부모님 사망', '가족 사망'))]
FOOTER_IMAGE_MARKERS = ('현재두법무사', '현재두 법무사', '032-425-1500', '경원대로 873', '상담 안내', '상담안내')
THUMBNAIL_MARKERS = ('thumbnail', 'oglink', 'link-preview', 'link_preview', 'se-oglink')
UA = {'User-Agent': 'Mozilla/5.0 (compatible; DeunggiroBlogImporter/2.0; +https://www.deunggiro.kr/)'}

def get(url, **kwargs):
    r = requests.get(url, headers=UA, timeout=25, **kwargs); r.raise_for_status()
    try: r.content.decode('utf-8'); r.encoding='utf-8'
    except UnicodeDecodeError: r.encoding=r.encoding or r.apparent_encoding or 'utf-8'
    return r

def norm_title(v):
    v=html.unescape(v or ''); v=re.sub('^\\s*\\[[^\\]]+\\]\\s*','',v); return re.sub('[^0-9A-Za-z가-힣]+','',v).lower()
def infer_category(title):
    for c,words in CATEGORY_RULES:
        if any(w in title for w in words): return c
    return '기타'
def log_no_from_url(url):
    m=re.search('/(\\d{6,})(?:\\?|$)',url); return m.group(1) if m else (parse_qs(urlparse(url).query).get('logNo') or [''])[0]
def canonical_blog_url(log_no): return f'https://blog.naver.com/{BLOG_ID}/{log_no}'
def resolve_post_view(url):
    r=get(url); soup=BeautifulSoup(r.text,'html.parser'); iframe=soup.select_one('iframe#mainFrame, iframe[name="mainFrame"]')
    if iframe and iframe.get('src'): return urljoin('https://blog.naver.com/',iframe['src'])
    n=log_no_from_url(url); return f'https://blog.naver.com/PostView.naver?blogId={BLOG_ID}&logNo={n}&redirect=Dlog&widgetTypeCall=true&directAccess=false' if n else url

def image_ext(resp,url):
    ct=(resp.headers.get('content-type') or '').lower()
    if 'png' in ct:return '.png'
    if 'webp' in ct:return '.webp'
    if 'gif' in ct:return '.gif'
    if 'jpeg' in ct or 'jpg' in ct:return '.jpg'
    ext=Path(urlparse(url).path).suffix.lower(); return ext if ext in ('.jpg','.jpeg','.png','.gif','.webp') else '.jpg'
def save_image(src,slug,index):
    try:
        r=requests.get(src,headers=UA,timeout=30); r.raise_for_status()
        if not r.content:return src
        folder=MEDIA_ROOT/slug; folder.mkdir(parents=True,exist_ok=True); path=folder/f'{index:02d}{image_ext(r,src)}'; path.write_bytes(r.content); return '/'+path.relative_to(ROOT).as_posix()
    except Exception as e: print('IMAGE_SKIP',src,e,file=sys.stderr); return src

def inline_html(el):
    def walk(node):
        if isinstance(node,NavigableString): return html.escape(str(node))
        if not isinstance(node,Tag): return ''
        name=node.name.lower(); inner=''.join(walk(c) for c in node.children)
        if name in ('strong','b'):return f'<strong>{inner}</strong>'
        if name in ('em','i'):return f'<em>{inner}</em>'
        if name=='u':return f'<u>{inner}</u>'
        if name=='br':return '<br>'
        if name=='a':
            href=node.get('href') or ''
            return f'<a href="{html.escape(href,quote=True)}" target="_blank" rel="noopener noreferrer">{inner}</a>' if href.startswith('http') else inner
        return inner
    return re.sub('[ \\t]+',' ',' '.join(walk(c) for c in el.children)).strip()

def table_html(table):
    rows=[]
    for tr in table.find_all('tr'):
        cells=[]
        for cell in tr.find_all(['th','td'],recursive=False):
            attrs=[]
            for key in ('colspan','rowspan'):
                val=cell.get(key)
                if val and str(val).isdigit(): attrs.append(f'{key}="{val}"')
            content=inline_html(cell); tag='th' if cell.name=='th' else 'td'; attr=' '+' '.join(attrs) if attrs else ''
            cells.append(f'<{tag}{attr}>{content}</{tag}>')
        if cells: rows.append('<tr>'+''.join(cells)+'</tr>')
    return '<table class="naver-table"><tbody>'+''.join(rows)+'</tbody></table>' if rows else ''

def is_thumbnail_image(el):
    node=el
    for _ in range(5):
        if not isinstance(node,Tag):break
        marker=' '.join([str(node.get('id') or ''),' '.join(node.get('class') or [])]).lower()
        if any(x in marker for x in THUMBNAIL_MARKERS):return True
        node=node.parent
    return False

def has_substantive_text_after(blocks,index):
    for nxt in blocks[index+1:]:
        if nxt.name in ('img','hr'):continue
        txt=' '.join(nxt.stripped_strings).strip()
        if not txt:continue
        if any(marker in txt for marker in FOOTER_IMAGE_MARKERS):continue
        return True
    return False

def clean_article(url,slug=''):
    view=resolve_post_view(url); r=get(view); soup=BeautifulSoup(r.text,'html.parser'); root=soup.select_one('.se-main-container') or soup.select_one('#postViewArea') or soup.select_one('.post-view')
    if root is None: raise RuntimeError('네이버 본문 영역을 찾지 못했습니다.')
    for bad in root.select('script,style,noscript,iframe,button'): bad.decompose()
    # 링크 미리보기 카드는 본문 텍스트/표로 오인되지 않도록 수집 전에 제거한다.
    for node in list(root.find_all(True)):
        marker=(' '.join([str(node.get('id') or ''),' '.join(node.get('class') or [])])).lower()
        if any(x in marker for x in THUMBNAIL_MARKERS): node.decompose()
    blocks=[]
    for el in root.find_all(['h2','h3','p','blockquote','ul','ol','img','hr','table'],recursive=True):
        if el.name!='table' and el.find_parent('table'):continue
        if el.find_parent(['p','blockquote','ul','ol']) and el.name!='img':continue
        # 네이버 표 모듈 내부의 문단은 table 자체만 수집한다.
        if el.name!='table' and el.find_parent(class_=re.compile(r'(?:se-table|table)',re.I)):continue
        blocks.append(el)
    image_no=0; footer_zone=False; parts=[]
    for idx,el in enumerate(blocks):
        txt=' '.join(el.stripped_strings).strip() if el.name!='img' else ''
        if txt and any(marker in txt for marker in FOOTER_IMAGE_MARKERS): footer_zone=True
        if el.name=='img':
            if footer_zone or is_thumbnail_image(el) or not has_substantive_text_after(blocks,idx):continue
            src=el.get('data-lazy-src') or el.get('data-src') or el.get('src') or ''; src='https:'+src if src.startswith('//') else src
            if not src:continue
            if slug:image_no+=1; src=save_image(src,slug,image_no)
            parts.append(f'<p class="media-paragraph"><img src="{html.escape(src,quote=True)}" alt="" loading="lazy" decoding="async"></p>'); continue
        if el.name=='table':
            rendered=table_html(el)
            if rendered:parts.append(rendered)
            continue
        if el.name=='hr':parts.append('<hr class="article-divider">'); continue
        if not txt:continue
        # 도메인 한 줄만 남는 링크카드 잔재 제거
        if re.fullmatch(r'(?:https?://)?(?:www\.)?(?:hjd219\.github\.io|deunggiro\.kr|www\.deunggiro\.kr)/?',txt,re.I):continue
        rich=inline_html(el)
        if el.name=='h2':parts.append(f'<h2>{rich}</h2>')
        elif el.name=='h3':parts.append(f'<h3>{rich}</h3>')
        elif el.name=='blockquote':parts.append(f'<blockquote>{rich}</blockquote>')
        elif el.name in ('ul','ol'):
            lis=[inline_html(li) for li in el.find_all('li',recursive=False) if inline_html(li)]
            if lis:parts.append(f'<{el.name}>'+''.join(f'<li>{x}</li>' for x in lis)+f'</{el.name}>')
        else:parts.append(f'<p>{rich}</p>')
    body='\n'.join(parts); text=re.sub('\\s+',' ',' '.join(root.stripped_strings)).strip(); return body,text

def summary_from(text,title):
    clean=re.sub('^\\s*\\[[^\\]]+\\]\\s*','',html.unescape(title or '')).strip(); clean=re.sub('\\s+',' ',clean)
    if len(clean)>42:clean=clean[:42].rstrip(' ,·:-')
    return f'{clean}의 핵심 절차와 준비사항을 간단히 정리합니다.'[:82].rstrip(' ,·:-')

def build_html(post,body):
    title=html.escape(post['title']); summary=html.escape(post['summary']); cat=html.escape(post['category']); date=html.escape(post['date']); slug=html.escape(post['slug'],quote=True); source=html.escape(post['source_url'],quote=True); intro_title=re.sub('^\\s*\\[[^\\]]+\\]\\s*','',post['title']); intro=html.escape(f'{intro_title}에서 꼭 확인해야 할 핵심 내용을 순서대로 살펴보겠습니다.')
    return f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} | 현재두 법무사 사무소</title><meta name="description" content="{summary}"><meta name="keywords" content="{title}"><meta property="og:type" content="article"><meta property="og:title" content="{title}"><meta property="og:description" content="{summary}"><meta property="og:url" content="{BASE}/posts/{slug}.html"><link rel="canonical" href="{BASE}/posts/{slug}.html"><meta name="dg-title" content="{title}"><meta name="dg-category" content="{cat}"><meta name="dg-date" content="{date}"><meta name="dg-summary" content="{summary}"><link rel="stylesheet" href="/assets/article-v2.css?v=9"><link rel="stylesheet" href="/assets/site-shell.css"><link rel="stylesheet" href="/assets/latest-posts.css"></head><body class="article-v2"><header class="header"></header><main class="section"><div class="container article-wrap"><article class="article"><div class="post-meta"><span class="badge">{cat}</span>{date}</div><h1>{title}</h1><p class="desc">{summary}</p><div class="article-body"><p class="article-intro"><strong>{intro}</strong></p>{body}<p class="source-note">네이버 블로그에 작성한 내용을 등기로 홈페이지 형식에 맞게 정리했습니다. <a href="{source}" target="_blank" rel="noopener noreferrer">원문 보기</a></p></div><!-- SEO_RELATED_POSTS_START --><!-- SEO_RELATED_POSTS_END --></article></div></main><section class="contact"></section><footer class="footer"></footer><script src="/assets/site-shell.js" defer></script><script src="/assets/article-v2.js" defer></script><script src="/assets/latest-posts.js" defer></script><script src="/assets/article-cta.js" defer></script></body></html>'

def load_posts(): return json.loads(POSTS_JSON.read_text(encoding='utf-8'))
def parse_date(value):
    value=str(value or '').strip()
    for pattern in ('(20\\d{2})[.\\-/](\\d{1,2})[.\\-/](\\d{1,2})','(20\\d{2})(\\d{2})(\\d{2})'):
        m=re.search(pattern,value)
        if m:return f'{int(m.group(1)):04d}-{int(m.group(2)):02d}-{int(m.group(3)):02d}'
    return datetime.now().strftime('%Y-%m-%d')
def fetch_feed_items():
    r=get(RSS_URL); soup=BeautifulSoup(r.content,'xml'); out=[]
    for item in soup.find_all('item'):
        title=item.title.get_text(' ',strip=True) if item.title else ''; link=item.link.get_text(strip=True) if item.link else ''; pub=item.pubDate.get_text(strip=True) if item.pubDate else ''
        if not title or not link:continue
        try:d=parsedate_to_datetime(pub).astimezone().strftime('%Y-%m-%d') if pub else datetime.now().strftime('%Y-%m-%d')
        except Exception:d=datetime.now().strftime('%Y-%m-%d')
        out.append({'title':html.unescape(title),'link':link,'date':d})
    return out

def decode_title_list_response(text):
    text=text.strip().lstrip('\ufeff')
    if text.startswith(")]}'"):text=text.split('\n',1)[-1]
    try:return json.loads(text)
    except Exception:pass
    m=re.search('\\{.*\\}',text,re.S)
    if m:
        try:return json.loads(m.group(0))
        except Exception:pass
    return None

def normalize_list_entry(raw):
    if not isinstance(raw,dict):return None
    n=str(raw.get('logNo') or raw.get('log_no') or raw.get('postNo') or '').strip()
    if not re.fullmatch('\\d{6,}',n):return None
    title=raw.get('title') or raw.get('postTitle') or raw.get('subject') or ''
    if isinstance(title,dict):title=title.get('value') or title.get('text') or ''
    title=BeautifulSoup(html.unescape(str(title)),'html.parser').get_text(' ',strip=True); date_value=raw.get('addDate') or raw.get('postAddDate') or raw.get('writeDate') or raw.get('regDate') or raw.get('date') or ''
    return {'title':title,'link':canonical_blog_url(n),'date':parse_date(date_value),'log_no':n}
def extract_entries_from_payload(payload):
    if not isinstance(payload,dict):return []
    candidates=[]
    for key in ('postList','post_list','posts','list'):
        value=payload.get(key)
        if isinstance(value,list):candidates=value;break
    if not candidates:
        for value in payload.values():
            if isinstance(value,dict):
                nested=extract_entries_from_payload(value)
                if nested:return nested
    return [x for raw in candidates if (x:=normalize_list_entry(raw))]
def fetch_all_blog_items():
    seen=set();out=[];consecutive_empty=0
    for page in range(1,MAX_LIST_PAGES+1):
        try:r=get(TITLE_LIST_URL,params={'blogId':BLOG_ID,'viewdate':'','currentPage':page,'categoryNo':0,'parentCategoryNo':'','countPerPage':LIST_PAGE_SIZE});payload=decode_title_list_response(r.text);items=extract_entries_from_payload(payload)
        except Exception as e:print('LIST_PAGE_SKIP',page,e,file=sys.stderr);break
        if not items:
            consecutive_empty+=1
            if consecutive_empty>=2:break
            continue
        consecutive_empty=0;new_count=0
        for item in items:
            n=item['log_no']
            if n in seen:continue
            seen.add(n);out.append(item);new_count+=1
        print(f'LIST_PAGE page={page} items={len(items)} new={new_count}')
        if len(items)<LIST_PAGE_SIZE:break
    if out:print(f'LIST_TOTAL={len(out)}');return out
    print('LIST_FALLBACK_RSS',file=sys.stderr);return fetch_feed_items()

def looks_mojibake(text):
    return '\ufffd' in str(text or '')

def main():
    posts=load_posts(); existing={norm_title(p.get('title','')) for p in posts}; added=0
    for item in fetch_all_blog_items():
        if added>=MAX_IMPORT:break
        if norm_title(item['title']) in existing:continue
        slug='naver-'+item.get('log_no','')
        try:body,text=clean_article(item['link'],slug)
        except Exception as e:print('IMPORT_SKIP',item['link'],e,file=sys.stderr);continue
        if not body:continue
        title=item['title']; post={'slug':slug,'title':title,'summary':summary_from(text,title),'category':infer_category(title),'date':item['date'],'source':'naver-blog','source_url':item['link']}
        POSTS_DIR.mkdir(parents=True,exist_ok=True);(POSTS_DIR/f'{slug}.html').write_text(build_html(post,body),encoding='utf-8');posts.insert(0,post);existing.add(norm_title(title));added+=1
    POSTS_JSON.write_text(json.dumps(posts,ensure_ascii=False,indent=2),encoding='utf-8');print('IMPORTED',added)

if __name__=='__main__':main()
