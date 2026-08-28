from __future__ import annotations
import html,json,re,sys
from datetime import datetime
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import urljoin,urlparse,parse_qs
import requests
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1];POSTS_JSON=ROOT/'data'/'posts.json';POSTS_DIR=ROOT/'posts';BLOG_ID='hjd21';RSS_URL=f'https://rss.blog.naver.com/{BLOG_ID}.xml';BASE='https://www.deunggiro.kr';MAX_IMPORT=3
CATEGORY_RULES=[('상속포기·한정승인',('상속포기','한정승인','특별한정승인','상속채무','망인 예금','보험금','해지환급금')),('상속재산분할',('상속재산분할','상속분쟁','기여분','특별수익','협조거부','연락두절')),('법인등기',('법인','주식회사','유한회사','대표이사','이사','감사','주주','본점이전','자본금','증자','감자','상호변경','목적변경','해산','청산')),('가사',('협의이혼','재판이혼','이혼','개명','성년후견','한정후견','친권','양육비')),('부동산등기',('근저당','가압류','등기권리증','등기필증','매매','증여','전세권','소유권이전','부동산','재산분할등기','신탁등기')),('상속등기',('상속등기','대습상속','상속취득세','상속인','상속지분','상속재산','유언','부모님 사망','가족 사망'))]
UA={'User-Agent':'Mozilla/5.0 (compatible; DeunggiroBlogImporter/1.3; +https://www.deunggiro.kr/)'}
def get(url):
 r=requests.get(url,headers=UA,timeout=25);r.raise_for_status()
 try:r.content.decode('utf-8');r.encoding='utf-8'
 except UnicodeDecodeError:r.encoding=r.encoding or r.apparent_encoding or 'utf-8'
 return r
def norm_title(v):v=html.unescape(v or '');v=re.sub(r'^\s*\[[^\]]+\]\s*','',v);return re.sub(r'[^0-9A-Za-z가-힣]+','',v).lower()
def infer_category(title):
 for c,words in CATEGORY_RULES:
  if any(w in title for w in words):return c
 return '기타'
def log_no_from_url(url):
 m=re.search(r'/(\d{6,})(?:\?|$)',url)
 if m:return m.group(1)
 return (parse_qs(urlparse(url).query).get('logNo') or [''])[0]
def resolve_post_view(url):
 r=get(url);soup=BeautifulSoup(r.text,'html.parser');iframe=soup.select_one('iframe#mainFrame, iframe[name="mainFrame"]')
 if iframe and iframe.get('src'):return urljoin('https://blog.naver.com/',iframe['src'])
 n=log_no_from_url(url);return f'https://blog.naver.com/PostView.naver?blogId={BLOG_ID}&logNo={n}&redirect=Dlog&widgetTypeCall=true&directAccess=false' if n else url
def heading_like(txt):
 """1.부터 99.까지 숫자형 및 1️⃣ 2️⃣ 3️⃣ 키캡 번호는 소제목으로 인식. ①②③ 원문자는 일반 본문 유지."""
 t=re.sub(r'\s+',' ',txt).strip()
 numbered=bool(re.match(r'^(?:[1-9]|[1-9][0-9])[.)]\s*\S',t))
 keycap=bool(re.match(r'^(?:[1-9]|[1-9][0-9])️⃣\s*\S',t))
 return (numbered or keycap) and len(t)<=100
def clean_article(url):
 view=resolve_post_view(url);r=get(view);soup=BeautifulSoup(r.text,'html.parser');root=soup.select_one('.se-main-container') or soup.select_one('#postViewArea') or soup.select_one('.post-view')
 if root is None:raise RuntimeError('네이버 본문 영역을 찾지 못했습니다.')
 for bad in root.select('script,style,noscript,iframe,button'):bad.decompose()
 for tag in root.find_all(True):
  if tag.name=='img':
   src=tag.get('data-lazy-src') or tag.get('data-src') or tag.get('src') or '';src=('https:'+src) if src.startswith('//') else src;tag.attrs={'src':src,'alt':''} if src else {}
  elif tag.name=='a':
   href=tag.get('href') or '';tag.attrs={'href':href,'target':'_blank','rel':'noopener noreferrer'} if href.startswith('http') else {}
  else:tag.attrs={}
 parts=[]
 for el in root.find_all(['h2','h3','p','blockquote','ul','ol','img'],recursive=True):
  if el.find_parent(['p','blockquote','ul','ol']) and el.name!='img':continue
  if el.name=='img':
   src=el.get('src') or ''
   if src:parts.append(f'<p class="media-paragraph"><img src="{html.escape(src,quote=True)}" alt="" loading="lazy" decoding="async"></p>')
   continue
  txt=' '.join(el.stripped_strings)
  if not txt:continue
  circled=bool(re.match(r'^[①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳]\s*\S',txt))
  if el.name=='p' and circled:parts.append(f'<p class="circled-number">{html.escape(txt)}</p>')
  elif el.name in ('h2','h3') or (el.name=='p' and heading_like(txt)):
   level='h2' if el.name=='h2' else 'h3';parts.append(f'<{level}>{html.escape(txt)}</{level}>')
  elif el.name=='blockquote':parts.append(f'<blockquote>{html.escape(txt)}</blockquote>')
  elif el.name in ('ul','ol'):
   lis=[' '.join(li.stripped_strings) for li in el.find_all('li',recursive=False)]
   if lis:parts.append(f'<{el.name}>'+''.join(f'<li>{html.escape(x)}</li>' for x in lis if x)+f'</{el.name}>')
  else:parts.append(f'<p>{html.escape(txt)}</p>')
 body='\n'.join(parts);text=re.sub(r'\s+',' ',' '.join(root.stripped_strings)).strip();return body,text
def summary_from(text,title):
 clean=re.sub(r'^\s*\[[^\]]+\]\s*','',html.unescape(title or '')).strip();clean=re.sub(r'\s+',' ',clean)
 if len(clean)>42:clean=clean[:42].rstrip(' ,·:-')
 return f'{clean}의 핵심 절차와 준비사항을 간단히 정리합니다.'[:82].rstrip(' ,·:-')
def build_html(post,body):
 title=html.escape(post['title']);summary=html.escape(post['summary']);cat=html.escape(post['category']);date=html.escape(post['date']);slug=html.escape(post['slug'],quote=True);source=html.escape(post['source_url'],quote=True);intro_title=re.sub(r'^\s*\[[^\]]+\]\s*','',post['title']);intro=html.escape(f'{intro_title}에서 꼭 확인해야 할 핵심 내용을 순서대로 살펴보겠습니다.')
 return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} | 현재두 법무사 사무소</title><meta name="description" content="{summary}"><meta name="keywords" content="{title}"><meta property="og:type" content="article"><meta property="og:title" content="{title}"><meta property="og:description" content="{summary}"><meta property="og:url" content="{BASE}/posts/{slug}.html"><link rel="canonical" href="{BASE}/posts/{slug}.html"><meta name="dg-title" content="{title}"><meta name="dg-category" content="{cat}"><meta name="dg-date" content="{date}"><meta name="dg-summary" content="{summary}"><link rel="stylesheet" href="/assets/article-v2.css?v=7"><link rel="stylesheet" href="/assets/site-shell.css"><link rel="stylesheet" href="/assets/latest-posts.css"></head><body class="article-v2"><header class="header"></header><main class="section"><div class="container article-wrap"><article class="article"><div class="post-meta"><span class="badge">{cat}</span>{date}</div><h1>{title}</h1><p class="desc">{summary}</p><div class="article-body"><p class="article-intro"><strong>{intro}</strong></p>{body}<p class="source-note">네이버 블로그에 작성한 내용을 등기로 홈페이지 형식에 맞게 정리했습니다. <a href="{source}" target="_blank" rel="noopener noreferrer">원문 보기</a></p></div><!-- SEO_RELATED_POSTS_START --><!-- SEO_RELATED_POSTS_END --></article></div></main><section class="contact"></section><footer class="footer"></footer><script src="/assets/site-shell.js" defer></script><script src="/assets/article-v2.js" defer></script><script src="/assets/latest-posts.js" defer></script><script src="/assets/article-cta.js" defer></script></body></html>'''
def load_posts():return json.loads(POSTS_JSON.read_text(encoding='utf-8'))
def fetch_feed_items():
 r=get(RSS_URL);soup=BeautifulSoup(r.content,'xml');out=[]
 for item in soup.find_all('item'):
  title=item.title.get_text(' ',strip=True) if item.title else '';link=item.link.get_text(strip=True) if item.link else '';pub=item.pubDate.get_text(strip=True) if item.pubDate else ''
  if not title or not link:continue
  try:d=parsedate_to_datetime(pub).astimezone().strftime('%Y-%m-%d') if pub else datetime.now().strftime('%Y-%m-%d')
  except Exception:d=datetime.now().strftime('%Y-%m-%d')
  out.append({'title':html.unescape(title),'link':link,'date':d})
 return out
def looks_mojibake(text):return bool(text) and sum(text.count(m) for m in ('ë','ì','í','â€','Â','�'))>=4
def refresh_existing_imports(posts):
 refreshed=0
 for post in posts:
  if post.get('source')!='naver-blog' or not post.get('source_url'):continue
  slug=str(post.get('slug','')).replace('.html','');page=POSTS_DIR/f'{slug}.html'
  try:body,text=clean_article(post['source_url'])
  except Exception as e:print('REFRESH_SKIP',slug,e,file=sys.stderr);continue
  if len(text)<80 or looks_mojibake(text):continue
  post['summary']=summary_from(text,post.get('title',''));post['category']=infer_category(post.get('title','')+' '+text[:500]);page.write_text(build_html(post,body),encoding='utf-8');refreshed+=1;print('REFRESHED',slug)
 return refreshed
def main():
 POSTS_DIR.mkdir(exist_ok=True);posts=load_posts();refreshed=refresh_existing_imports(posts);existing_titles={norm_title(p.get('title','')) for p in posts};existing_sources={str(p.get('source_url','')).strip() for p in posts if p.get('source_url')};imported=0
 for item in fetch_feed_items():
  if imported>=MAX_IMPORT:break
  if item['link'] in existing_sources or norm_title(item['title']) in existing_titles:continue
  n=log_no_from_url(item['link'])
  if not n:continue
  try:body,text=clean_article(item['link'])
  except Exception as e:print('SKIP',item['link'],e,file=sys.stderr);continue
  if len(text)<80 or looks_mojibake(text):continue
  slug=f'naver-{n}'
  if any(str(p.get('slug','')).replace('.html','')==slug for p in posts):continue
  post={'title':item['title'],'category':infer_category(item['title']+' '+text[:500]),'date':item['date'],'slug':slug,'keywords':item['title'],'summary':summary_from(text,item['title']),'source_url':item['link'],'source':'naver-blog'};(POSTS_DIR/f'{slug}.html').write_text(build_html(post,body),encoding='utf-8');posts.insert(0,post);existing_titles.add(norm_title(post['title']));existing_sources.add(item['link']);imported+=1;print('IMPORTED',slug,post['title'])
 if imported or refreshed:POSTS_JSON.write_text(json.dumps(posts,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(f'imported={imported} refreshed={refreshed}')
if __name__=='__main__':main()
