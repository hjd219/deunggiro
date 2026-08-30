from __future__ import annotations
import html,json,re,sys
from datetime import datetime
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import urljoin,urlparse,parse_qs
import requests
from bs4 import BeautifulSoup,NavigableString,Tag
ROOT=Path(__file__).resolve().parents[1]; POSTS_JSON=ROOT/'data'/'posts.json'; POSTS_DIR=ROOT/'posts'; MEDIA_ROOT=ROOT/'assets'/'naver-images'
BLOG_ID='hjd21'; RSS_URL=f'https://rss.blog.naver.com/{BLOG_ID}.xml'; BASE='https://www.deunggiro.kr'; MAX_IMPORT=3; MAX_REPAIR=100
UA={'User-Agent':'Mozilla/5.0 (compatible; DeunggiroBlogImporter/4.0; +https://www.deunggiro.kr/)'}
MOJIBAKE=('êµ','ë“','ë¡','ì§','ì—','ì›','ë¹','ê³','ë°','ì„','ìƒ','ìž','í•','ì‹','ìš','ìœ','ì•','ë¶','ì¶','ì ','ì²','ìž')
CATEGORY_RULES=[('상속포기·한정승인',('상속포기','한정승인','특별한정승인','상속채무')),('상속재산분할',('상속재산분할','상속분쟁','기여분','특별수익','협조거부','연락두절')),('법인등기',('법인','주식회사','유한회사','대표이사','이사','감사','주주','본점이전','자본금','증자','감자','상호변경','목적변경')),('가사',('협의이혼','재판이혼','이혼','개명','후견','친권','양육비')),('부동산등기',('근저당','가압류','등기권리증','매매','증여','전세권','부동산','재산분할등기')),('상속등기',('상속등기','대습상속','상속취득세','상속인','상속지분','상속재산','유언','부모님 사망'))]
def get(url):
 r=requests.get(url,headers=UA,timeout=25); r.raise_for_status(); r.encoding='utf-8'; return r
def norm(v): return re.sub(r'[^0-9A-Za-z가-힣]+','',html.unescape(v or '')).lower()
def category(text):
 for c,words in CATEGORY_RULES:
  if any(w in text for w in words): return c
 return '기타'
def logno(url):
 m=re.search(r'/(\d{6,})(?:\?|$)',url); return m.group(1) if m else (parse_qs(urlparse(url).query).get('logNo') or [''])[0]
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
    cells=[f'<{cell.name}>{inline(cell)}</{cell.name}>' for cell in tr.find_all(['th','td'],recursive=False)]
    if cells: rows.append('<tr>'+''.join(cells)+'</tr>')
   if rows: parts.append('<table class="naver-table"><tbody>'+''.join(rows)+'</tbody></table>')
  elif el.name=='hr': parts.append('<hr class="article-divider">')
  elif txt: parts.append(f'<{el.name}>{inline(el)}</{el.name}>')
 body='\n'.join(parts); text=' '.join(root.stripped_strings).strip(); return body,text,imgno
def quality_text(text):
 compact=re.sub(r'\s+','',text or ''); bad=sum(compact.count(x) for x in MOJIBAKE)
 return len(compact),bad
def inspect_file(path):
 if not path.exists(): return 0,0,'missing'
 soup=BeautifulSoup(path.read_text(encoding='utf-8',errors='replace'),'html.parser'); body=soup.select_one('.article-body')
 if body is None: return 0,0,'no-body'
 chars,bad=quality_text(' '.join(body.stripped_strings)); reason='ok' if chars>=500 and bad==0 else ('mojibake' if bad else 'short')
 return chars,bad,reason
def build(p,body):
 t=html.escape(p['title']); sm=html.escape(p.get('summary') or ''); c=html.escape(p.get('category') or '기타'); d=p.get('date') or datetime.now().strftime('%Y-%m-%d'); sl=p['slug']
 return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{t} | 현재두 법무사 사무소</title><meta name="description" content="{sm}"><link rel="canonical" href="{BASE}/posts/{sl}.html"><meta name="dg-title" content="{t}"><meta name="dg-category" content="{c}"><meta name="dg-date" content="{d}"><meta name="dg-summary" content="{sm}"><link rel="stylesheet" href="/assets/article-v2.css?v=9"><link rel="stylesheet" href="/assets/site-shell.css"></head><body class="article-v2"><header class="header"></header><main class="section"><div class="container article-wrap"><article class="article"><div class="post-meta"><span class="badge">{c}</span>{d}</div><h1>{t}</h1><p class="desc">{sm}</p><div class="article-body">{body}</div><!-- SEO_RELATED_POSTS_START --><!-- SEO_RELATED_POSTS_END --></article></div></main><section class="contact"></section><footer class="footer"></footer><script src="/assets/site-shell.js" defer></script><script src="/assets/article-v2.js" defer></script></body></html>'''
def save_post(p,body):
 slug=(p.get('slug') or '').replace('.html',''); p['slug']=slug; path=POSTS_DIR/f'{slug}.html'; candidate=build(p,body)
 soup=BeautifulSoup(candidate,'html.parser'); node=soup.select_one('.article-body'); chars,bad=quality_text(' '.join(node.stripped_strings) if node else '')
 if chars<500 or bad: raise RuntimeError(f'품질검사 실패 {slug}: chars={chars} mojibake={bad}')
 path.write_text(candidate,encoding='utf-8'); saved,bad2,reason=inspect_file(path)
 if reason!='ok': raise RuntimeError(f'저장후 품질검사 실패 {slug}: chars={saved} mojibake={bad2} reason={reason}')
 return saved
def feed():
 s=BeautifulSoup(get(RSS_URL).content,'xml'); out=[]
 for x in s.find_all('item'):
  title=x.title.get_text(' ',strip=True) if x.title else ''; link=x.link.get_text(strip=True) if x.link else ''; pub=x.pubDate.get_text(strip=True) if x.pubDate else ''
  if not title or not link: continue
  try: date=parsedate_to_datetime(pub).astimezone().strftime('%Y-%m-%d')
  except: date=datetime.now().strftime('%Y-%m-%d')
  out.append((html.unescape(title),link,date))
 if len(out)<10: raise RuntimeError('RSS 수집 비정상: '+str(len(out)))
 print('RSS_ITEMS',len(out)); return out
def repair(posts):
 bad=[]
 for p in posts:
  if p.get('source')!='naver-blog': continue
  slug=(p.get('slug') or '').replace('.html',''); chars,moji,reason=inspect_file(POSTS_DIR/f'{slug}.html')
  if reason!='ok': bad.append((p,chars,moji,reason))
 print('QUALITY_BAD',len(bad)); repaired=0
 for p,oldchars,oldmoji,reason in bad[:MAX_REPAIR]:
  slug=(p.get('slug') or '').replace('.html',''); url=p.get('source_url') or (f'https://blog.naver.com/{BLOG_ID}/{slug.removeprefix("naver-")}' if slug.startswith('naver-') else '')
  if not url: print('REPAIR_SKIP_NO_URL',slug); continue
  try:
   body,text,imgs=extract(url,slug); chars,moji=quality_text(text); print('REPAIR_CANDIDATE',slug,'reason='+reason,'old='+str(oldchars),'new='+str(chars),'mojibake='+str(moji),'images='+str(imgs))
   if chars<500 or moji: print('REPAIR_REJECT',slug); continue
   p['category']=category((p.get('title') or '')+' '+text[:500]); p['summary']=p.get('summary') or ((p.get('title') or '')+'의 핵심 절차와 준비사항을 정리합니다.')[:100]
   saved=save_post(p,body); repaired+=1; print('REPAIRED',slug,'saved='+str(saved))
  except Exception as e: print('REPAIR_SKIP',slug,e)
 print('REPAIRED_TOTAL',repaired); return len(bad),repaired
def validate_all(posts):
 bad=[]; checked=0
 for p in posts:
  if p.get('source')!='naver-blog': continue
  slug=(p.get('slug') or '').replace('.html',''); checked+=1; chars,moji,reason=inspect_file(POSTS_DIR/f'{slug}.html')
  if reason!='ok': bad.append(f'{slug}:{reason}:{chars}:{moji}')
 print('FINAL_QUALITY',checked,'BAD',len(bad))
 if bad:
  print('FINAL_BAD_LIST',','.join(bad)); raise RuntimeError('네이버 자동작성 불량글이 남아 있어 배포를 중단합니다.')
def main():
 posts=json.loads(POSTS_JSON.read_text(encoding='utf-8')); repair(posts); sources={str(p.get('source_url','')) for p in posts}; titles={norm(p.get('title','')) for p in posts}; imported=0; checked=0
 for title,url,date in feed():
  if imported>=MAX_IMPORT: break
  if url in sources or norm(title) in titles: continue
  n=logno(url)
  if not n: continue
  checked+=1; slug='naver-'+n
  try:
   body,text,imgs=extract(url,slug); chars,moji=quality_text(text); print('CANDIDATE',n,'chars='+str(chars),'mojibake='+str(moji),'images='+str(imgs))
   if chars<500 or moji: print('SKIP_BAD_SOURCE',n); continue
   sm=(re.sub(r'^\s*\[[^\]]+\]\s*','',title)+'의 핵심 절차와 준비사항을 정리합니다.')[:100]
   p={'title':title,'category':category(title+' '+text[:500]),'date':date,'slug':slug,'keywords':title,'summary':sm,'source_url':url,'source':'naver-blog'}
   saved=save_post(p,body); posts.insert(0,p); sources.add(url); titles.add(norm(title)); imported+=1; print('IMPORTED_NEW',slug,'saved='+str(saved))
  except Exception as e: print('SKIP',n,e)
 POSTS_JSON.write_text(json.dumps(posts,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); validate_all(posts); print('IMPORT_SCAN',checked,'IMPORTED',imported)
if __name__=='__main__': main()
