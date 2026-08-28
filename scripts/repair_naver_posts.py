import html, json, re, sys
from pathlib import Path
from urllib.parse import urljoin, urlparse, parse_qs
import requests
from bs4 import BeautifulSoup, NavigableString, Tag

ROOT=Path(__file__).resolve().parents[1]
POSTS_JSON=ROOT/'data'/'posts.json'; POSTS_DIR=ROOT/'posts'; MEDIA_ROOT=ROOT/'assets'/'naver-images'
UA={'User-Agent':'Mozilla/5.0 (compatible; DeunggiroBlogRepair/1.0; +https://www.deunggiro.kr/)'}
RULES=[
 ('상속포기·한정승인',('상속포기','한정승인','특별한정승인','상속채무')),
 ('상속재산분할',('상속재산분할','상속분쟁','기여분','특별수익')),
 ('부동산등기',('신탁','가압류','근저당','가등기','전세권','소유권이전','부동산','매매','증여','등기권리증')),
 ('법인등기',('법인','주식회사','유한회사','대표이사','이사변경','감사','주주','본점이전','자본금','증자','감자','상호변경','목적변경','해산','청산')),
 ('가사',('이혼','개명','성년후견','한정후견','친권','양육비')),
 ('상속등기',('상속등기','대습상속','상속취득세','상속인','상속지분','상속재산','유언','사망')),
]
FOOT=('현재두법무사','현재두 법무사','032-425-1500','경원대로 873','상담 안내','상담안내')

def get(url):
 r=requests.get(url,headers=UA,timeout=30); r.raise_for_status(); r.encoding='utf-8'; return r

def logno(url):
 m=re.search(r'/(\d{6,})(?:\?|$)',url)
 if m:return m.group(1)
 return (parse_qs(urlparse(url).query).get('logNo') or [''])[0]

def view_url(url):
 r=get(url); soup=BeautifulSoup(r.text,'html.parser'); f=soup.select_one('iframe#mainFrame,iframe[name="mainFrame"]')
 if f and f.get('src'):return urljoin('https://blog.naver.com/',f['src'])
 n=logno(url); return f'https://blog.naver.com/PostView.naver?blogId=hjd21&logNo={n}&redirect=Dlog&widgetTypeCall=true&directAccess=false'

def category(title):
 text=re.sub(r'\s+',' ',title or '')
 for c,words in RULES:
  if any(w in text for w in words):return c
 return '기타'

def inline(el):
 def walk(n):
  if isinstance(n,NavigableString):return html.escape(str(n))
  if not isinstance(n,Tag):return ''
  inner=''.join(walk(x) for x in n.children); name=n.name.lower()
  cls=' '.join(n.get('class') or [])
  style=(n.get('style') or '').lower()
  bold=name in ('b','strong') or 'font-weight:700' in style or 'font-weight: 700' in style or 'se-fs-' in cls and 'se-ff-' not in cls and False
  if bold:return f'<strong>{inner}</strong>'
  if name in ('em','i'):return f'<em>{inner}</em>'
  if name=='u':return f'<u>{inner}</u>'
  if name=='br':return '<br>'
  if name=='a':
   href=n.get('href') or ''
   return f'<a href="{html.escape(href,quote=True)}" target="_blank" rel="noopener noreferrer">{inner}</a>' if href.startswith('http') else inner
  return inner
 return re.sub(r'[ \t]+',' ',' '.join(walk(x) for x in el.children)).strip()

def save_image(src,slug,no):
 try:
  r=requests.get(src,headers=UA,timeout=30); r.raise_for_status()
  ct=(r.headers.get('content-type') or '').lower(); ext='.png' if 'png' in ct else '.webp' if 'webp' in ct else '.gif' if 'gif' in ct else '.jpg'
  d=MEDIA_ROOT/slug; d.mkdir(parents=True,exist_ok=True); p=d/f'{no:02d}{ext}'; p.write_bytes(r.content); return '/'+p.relative_to(ROOT).as_posix()
 except Exception:return src

def table_html(t):
 rows=[]
 for tr in t.find_all('tr'):
  cells=[]
  for cell in tr.find_all(['th','td']):
   attrs=''.join(f' {k}="{cell.get(k)}"' for k in ('colspan','rowspan') if str(cell.get(k) or '').isdigit())
   cells.append(f'<{cell.name}{attrs}>{inline(cell)}</{cell.name}>')
  if cells:rows.append('<tr>'+''.join(cells)+'</tr>')
 return '<table class="naver-table"><tbody>'+''.join(rows)+'</tbody></table>' if rows else ''

def extract(url,slug):
 soup=BeautifulSoup(get(view_url(url)).text,'html.parser'); root=soup.select_one('.se-main-container') or soup.select_one('#postViewArea') or soup.select_one('.post-view')
 if not root:raise RuntimeError('본문 영역 없음')
 for x in root.select('script,style,noscript,iframe,button'):x.decompose()
 parts=[]; seen=set(); image_no=0; footer=False
 components=root.select('.se-component')
 if not components: components=[root]
 for comp in components:
  txt=' '.join(comp.stripped_strings).strip()
  if txt and any(x in txt for x in FOOT):footer=True
  if footer:continue
  classes=' '.join(comp.get('class') or [])
  if 'se-horizontalLine' in classes or 'se-horizontal-line' in classes:
   parts.append('<hr class="article-divider">'); continue
  table=comp.find('table')
  if table:
   rendered=table_html(table)
   if rendered:parts.append(rendered)
   continue
  imgs=comp.find_all('img')
  if imgs and ('se-image' in classes or not txt):
   for img in imgs:
    src=img.get('data-lazy-src') or img.get('data-src') or img.get('src') or ''
    if src.startswith('//'):src='https:'+src
    if not src:continue
    image_no+=1; src=save_image(src,slug,image_no); parts.append(f'<p class="media-paragraph"><img src="{html.escape(src,quote=True)}" alt="" loading="lazy" decoding="async"></p>')
   continue
  paras=comp.select('.se-text-paragraph')
  if not paras:paras=comp.find_all(['h2','h3','p','blockquote'],recursive=True)
  for p in paras:
   plain=' '.join(p.stripped_strings).strip()
   if not plain or plain in seen:continue
   if any(x in plain for x in FOOT):footer=True;break
   seen.add(plain); rich=inline(p)
   # 네이버 원문의 제목/문단 속성만 따르고 번호 모양으로 재분류하지 않는다.
   tag='p'
   if p.name in ('h2','h3'):tag=p.name
   elif p.find_parent(class_=re.compile(r'se-module-text')):
    style=' '.join(p.get('class') or [])+' '+(p.get('style') or '')
    if 'se-fs-fs24' in style or 'se-fs-fs28' in style or 'se-fs-fs32' in style:tag='h3'
   parts.append(f'<{tag}>{rich}</{tag}>')
 return '\n'.join(parts)

def rebuild(post,body):
 p=POSTS_DIR/f"{post['slug']}.html"
 if not p.exists():return
 s=p.read_text(encoding='utf-8'); cat=html.escape(post['category']);
 s=re.sub(r'(<meta\s+name=["\']dg-category["\']\s+content=["\'])[^"\']*',r'\1'+cat,s,count=1,flags=re.I)
 s=re.sub(r'(<span\s+class=["\']badge["\']>).*?(</span>)',r'\1'+cat+r'\2',s,count=1,flags=re.I|re.S)
 s=re.sub(r'<figure[^>]+id=["\']dg-post-hero-image["\'][^>]*>.*?</figure>','',s,flags=re.I|re.S)
 s=re.sub(r'<style[^>]+id=["\']dg-post-hero-style["\'][^>]*>.*?</style>','',s,flags=re.I|re.S)
 m=re.search(r'(<div class="article-body">)(.*?)(</div><!-- SEO_RELATED_POSTS_START -->)',s,re.I|re.S)
 if not m:return
 source=html.escape(post['source_url'],quote=True)
 intro_title=re.sub(r'^\s*\[[^\]]+\]\s*','',post['title'])
 intro=f'<p class="article-intro"><strong>{html.escape(intro_title)}에서 꼭 확인해야 할 핵심 내용을 순서대로 살펴보겠습니다.</strong></p>'
 note=f'<p class="source-note">네이버 블로그에 작성한 내용을 등기로 홈페이지 형식에 맞게 정리했습니다. <a href="{source}" target="_blank" rel="noopener noreferrer">원문 보기</a></p>'
 s=s[:m.start()]+m.group(1)+intro+body+note+m.group(3)+s[m.end():]
 p.write_text(s,encoding='utf-8')

def main():
 posts=json.loads(POSTS_JSON.read_text(encoding='utf-8')); done=0
 for post in posts:
  if post.get('source')!='naver-blog' or not post.get('source_url'):continue
  slug=str(post.get('slug','')).replace('.html',''); post['slug']=slug
  try:
   body=extract(post['source_url'],slug)
   plain=re.sub(r'<[^>]+>',' ',body)
   if len(re.sub(r'\s+','',plain))<80:raise RuntimeError('추출 본문이 너무 짧음')
   post['category']=category(post.get('title','')); rebuild(post,body); done+=1; print('REPAIRED',slug,post['category'])
  except Exception as e:print('REPAIR_SKIP',slug,e,file=sys.stderr)
 POSTS_JSON.write_text(json.dumps(posts,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print('repaired',done)
if __name__=='__main__':main()
