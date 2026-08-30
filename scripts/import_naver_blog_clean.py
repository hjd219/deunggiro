from __future__ import annotations
import html,json,re,sys
from datetime import datetime
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import urljoin,urlparse,parse_qs
import requests
from bs4 import BeautifulSoup,NavigableString,Tag
ROOT=Path(__file__).resolve().parents[1]; POSTS_JSON=ROOT/'data'/'posts.json'; POSTS_DIR=ROOT/'posts'; MEDIA_ROOT=ROOT/'assets'/'naver-images'
BLOG_ID='hjd21'; RSS_URL=f'https://rss.blog.naver.com/{BLOG_ID}.xml'; BASE='https://www.deunggiro.kr'; MAX_IMPORT=3
UA={'User-Agent':'Mozilla/5.0 (compatible; DeunggiroBlogImporter/2.0; +https://www.deunggiro.kr/)'}
CATEGORY_RULES=[('상속포기·한정승인',('상속포기','한정승인','특별한정승인','상속채무')),('상속재산분할',('상속재산분할','상속분쟁','기여분','특별수익','협조거부','연락두절')),('법인등기',('법인','주식회사','유한회사','대표이사','이사','감사','주주','본점이전','자본금','증자','감자','상호변경','목적변경')),('가사',('협의이혼','재판이혼','이혼','개명','후견','친권','양육비')),('부동산등기',('근저당','가압류','등기권리증','매매','증여','전세권','부동산','재산분할등기')),('상속등기',('상속등기','대습상속','상속취득세','상속인','상속지분','상속재산','유언','부모님 사망'))]
def get(url):
 r=requests.get(url,headers=UA,timeout=25); r.raise_for_status(); r.encoding=r.apparent_encoding or r.encoding or 'utf-8'; return r
def norm(v): return re.sub(r'[^0-9A-Za-z가-힣]+','',html.unescape(v or '')).lower()
def category(text):
 for c,words in CATEGORY_RULES:
  if any(w in text for w in words): return c
 return '기타'
def logno(url):
 m=re.search(r'/(\d{6,})(?:\?|$)',url)
 return m.group(1) if m else (parse_qs(urlparse(url).query).get('logNo') or [''])[0]
def view_url(url):
 r=get(url); s=BeautifulSoup(r.text,'html.parser'); f=s.select_one('iframe#mainFrame,iframe[name="mainFrame"]')
 if f and f.get('src'): return urljoin('https://blog.naver.com/',f['src'])
 n=logno(url); return f'https://blog.naver.com/PostView.naver?blogId={BLOG_ID}&logNo={n}&redirect=Dlog&widgetTypeCall=true&directAccess=false' if n else url
def inline(el):
 def walk(n):
  if isinstance(n,NavigableString): return html.escape(str(n))
  if not isinstance(n,Tag): return ''
  inn=''.join(walk(c) for c in n.children); name=n.name.lower()
  if name in ('strong','b'): return f'<strong>{inn}</strong>'
  if name in ('em','i'): return f'<em>{inn}</em>'
  if name=='br': return '<br>'
  return inn
 return re.sub(r'[ \t]+',' ',' '.join(walk(c) for c in el.children)).strip()
def save_image(src,slug,i):
 try:
  r=requests.get(src,headers=UA,timeout=20); r.raise_for_status(); ct=(r.headers.get('content-type') or '').lower(); ext='.png' if 'png' in ct else '.webp' if 'webp' in ct else '.gif' if 'gif' in ct else '.jpg'; d=MEDIA_ROOT/slug; d.mkdir(parents=True,exist_ok=True); p=d/f'{i:02d}{ext}'; p.write_bytes(r.content); return '/'+p.relative_to(ROOT).as_posix()
 except Exception as e: print('IMAGE_SKIP',e,file=sys.stderr); return ''
def extract(url,slug):
 s=BeautifulSoup(get(view_url(url)).text,'html.parser'); root=s.select_one('.se-main-container') or s.select_one('#postViewArea') or s.select_one('.post-view')
 if root is None: raise RuntimeError('본문 영역 없음')
 for x in root.select('script,style,noscript,iframe,button'): x.decompose()
 parts=[]; imgno=0
 for el in root.find_all(['h2','h3','p','blockquote','ul','ol','table','img','hr'],recursive=True):
  if el.name!='table' and el.find_parent('table'): continue
  if el.find_parent(['p','blockquote','ul','ol']) and el.name!='img': continue
  txt=' '.join(el.stripped_strings).strip() if el.name!='img' else ''
  if el.name=='img':
   src=el.get('data-lazy-src') or el.get('data-src') or el.get('src') or ''; src='https:'+src if src.startswith('//') else src
   if src: imgno+=1; local=save_image(src,slug,imgno); parts.append(f'<p class="media-paragraph"><img src="{html.escape(local,quote=True)}" alt="" loading="lazy" decoding="async"></p>') if local else None
  elif el.name=='table':
   rows=[]
   for tr in el.find_all('tr'):
    cells=[]
    for cell in tr.find_all(['th','td'],recursive=False): cells.append(f'<{cell.name}>{inline(cell)}</{cell.name}>')
    if cells: rows.append('<tr>'+''.join(cells)+'</tr>')
   if rows: parts.append('<table class="naver-table"><tbody>'+''.join(rows)+'</tbody></table>')
  elif el.name=='hr': parts.append('<hr class="article-divider">')
  elif txt:
   rich=inline(el); parts.append(f'<{el.name}>{rich}</{el.name}>')
 body='\n'.join(parts); text=re.sub(r'\s+',' ',' '.join(root.stripped_strings)).strip(); return body,text,imgno
def feed():
 s=BeautifulSoup(get(RSS_URL).content,'xml'); out=[]
 for x in s.find_all('item'):
  title=x.title.get_text(' ',strip=True) if x.title else ''; link=x.link.get_text(strip=True) if x.link else ''; pub=x.pubDate.get_text(strip=True) if x.pubDate else ''
  if not title or not link: continue
  try: date=parsedate_to_datetime(pub).astimezone().strftime('%Y-%m-%d')
  except: date=datetime.now().strftime('%Y-%m-%d')
  out.append((html.unescape(title),link,date))
 print('RSS_ITEMS',len(out)); return out
def build(p,body):
 t=html.escape(p['title']); sm=html.escape(p['summary']); c=html.escape(p['category']); d=p['date']; sl=p['slug']
 return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{t} | 현재두 법무사 사무소</title><meta name="description" content="{sm}"><link rel="canonical" href="{BASE}/posts/{sl}.html"><meta name="dg-title" content="{t}"><meta name="dg-category" content="{c}"><meta name="dg-date" content="{d}"><meta name="dg-summary" content="{sm}"><link rel="stylesheet" href="/assets/article-v2.css?v=9"><link rel="stylesheet" href="/assets/site-shell.css"></head><body class="article-v2"><header class="header"></header><main class="section"><div class="container article-wrap"><article class="article"><div class="post-meta"><span class="badge">{c}</span>{d}</div><h1>{t}</h1><p class="desc">{sm}</p><div class="article-body">{body}</div><!-- SEO_RELATED_POSTS_START --><!-- SEO_RELATED_POSTS_END --></article></div></main><section class="contact"></section><footer class="footer"></footer><script src="/assets/site-shell.js" defer></script><script src="/assets/article-v2.js" defer></script></body></html>'''
def main():
 posts=json.loads(POSTS_JSON.read_text(encoding='utf-8')); sources={str(p.get('source_url','')) for p in posts}; titles={norm(p.get('title','')) for p in posts}; imported=0; checked=0
 for title,url,date in feed():
  if imported>=MAX_IMPORT: break
  if url in sources or norm(title) in titles: continue
  n=logno(url)
  if not n: continue
  checked+=1; slug='naver-'+n
  try: body,text,imgs=extract(url,slug)
  except Exception as e: print('SKIP',n,e); continue
  chars=len(re.sub(r'\s+','',text)); print('CANDIDATE',n,'chars='+str(chars),'images='+str(imgs))
  if chars<500: print('SKIP_SHORT',n); continue
  sm=(re.sub(r'^\s*\[[^\]]+\]\s*','',title)+'의 핵심 절차와 준비사항을 정리합니다.')[:100]
  p={'title':title,'category':category(title+' '+text[:500]),'date':date,'slug':slug,'keywords':title,'summary':sm,'source_url':url,'source':'naver-blog'}
  (POSTS_DIR/f'{slug}.html').write_text(build(p,body),encoding='utf-8'); posts.insert(0,p); sources.add(url); titles.add(norm(title)); imported+=1; print('IMPORTED_NEW',slug)
 POSTS_JSON.write_text(json.dumps(posts,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print('IMPORT_SCAN',checked,'IMPORTED',imported)
if __name__=='__main__': main()
