from __future__ import annotations
import html,json,re,time
from pathlib import Path
from urllib.parse import urljoin,parse_qs,urlparse
import requests
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'/'posts.json'; MEDIA=ROOT/'assets'/'naver-images'; BLOG='hjd21'
UA={'User-Agent':'Mozilla/5.0 (compatible; DeunggiroFormat/1.4; +https://www.deunggiro.kr/)'}
EMOJI_RE=re.compile('[\U0001F000-\U0001FAFF\U00002600-\U000027BF]')
def get(u):
 r=requests.get(u,headers=UA,timeout=25); r.raise_for_status(); r.encoding='utf-8'; return r
def logno(u):
 m=re.search(r'/(\d{6,})(?:\?|$)',u); return m.group(1) if m else (parse_qs(urlparse(u).query).get('logNo') or [''])[0]
def view(u):
 s=BeautifulSoup(get(u).text,'html.parser'); f=s.select_one('iframe#mainFrame,iframe[name="mainFrame"]')
 return urljoin('https://blog.naver.com/',f['src']) if f and f.get('src') else f'https://blog.naver.com/PostView.naver?blogId={BLOG}&logNo={logno(u)}&redirect=Dlog&widgetTypeCall=true&directAccess=false'
def keep_number_emoji(v):
 saved=[]
 def stash(m): saved.append(m.group(0)); return f'__DGNUM{len(saved)-1}__'
 v=re.sub(r'(?:[1-9]\ufe0f?\u20e3|🔟)',stash,v); v=EMOJI_RE.sub('',v).replace('\ufe0f','')
 for i,x in enumerate(saved): v=v.replace(f'__DGNUM{i}__',x)
 return re.sub(r'[ \t]+',' ',v).strip()
def txt(n): return keep_number_emoji(re.sub(r'\s+',' ',' '.join(n.stripped_strings)).strip())
def fontsize(n):
 classes=' '.join(n.get('class',[]))+' '+' '.join(c for x in n.find_all(True) for c in x.get('class',[])); m=re.search(r'(?:se-fs-|se_font_size_)(?:fs)?(\d{1,2})',classes)
 if m: return max(13,min(28,int(m.group(1))))
 st=' '.join([n.get('style','')]+[x.get('style','') for x in n.find_all(True)]); m=re.search(r'font-size\s*:\s*(\d{1,2})px',st,re.I)
 return max(13,min(28,int(m.group(1)))) if m else 16
def styled_text(n):
 t=txt(n); size=fontsize(n); classes=' '.join(n.get('class',[]))+' '+' '.join(c for x in n.find_all(True) for c in x.get('class',[])); st=' '.join([n.get('style','')]+[x.get('style','') for x in n.find_all(True)])
 weight='700' if n.find(['b','strong']) or 'font-weight: bold' in st.lower() else '400'; align='center' if ('se-text-paragraph-align-center' in classes or 'text-align: center' in st.lower()) else 'right' if ('align-right' in classes or 'text-align: right' in st.lower()) else 'left'
 return f'<p class="naver-p" style="font-size:{size}px;font-weight:{weight};text-align:{align}">{html.escape(t)}</p>'
def saveimg(src,slug,i):
 try:
  if src.startswith('//'): src='https:'+src
  r=requests.get(src,headers=UA,timeout=20); r.raise_for_status(); ct=(r.headers.get('content-type') or '').lower(); ext='.png' if 'png' in ct else '.webp' if 'webp' in ct else '.gif' if 'gif' in ct else '.jpg'; d=MEDIA/slug; d.mkdir(parents=True,exist_ok=True); p=d/f'fmt-{i:02d}{ext}'; p.write_bytes(r.content); return '/'+p.relative_to(ROOT).as_posix()
 except: return ''
def promo_start_text(v):
 v=re.sub(r'\s+','',v)
 return any(k in v for k in ('현재두법무사사무소상담안내','현재두법무사상담안내','현재두법무사사무소상담','032-425-1500'))
def is_link_component(c):
 cl=' '.join(c.get('class',[])).lower()
 return ('se-oglink' in cl or 'se-link' in cl or 'se-module-link' in cl or c.select_one('.se-oglink-info,.se-module-oglink,.se-module-link,.se-link-preview') is not None or (c.find('a',href=True) is not None and not c.select_one('.se-image,.se-module-image')))
def extract(u,slug):
 s=BeautifulSoup(get(view(u)).text,'html.parser'); root=s.select_one('.se-main-container') or s.select_one('#postViewArea') or s.select_one('.post-view')
 if not root: raise RuntimeError('no body')
 comps=root.select(':scope > .se-component') or root.select('.se-component') or list(root.children)
 promo_start=len(comps)
 for i,c in enumerate(comps):
  if getattr(c,'select_one',None) and promo_start_text(txt(c)): promo_start=i; break
 out=[]; imgno=0; seen=set()
 for i,c in enumerate(comps):
  if i>=promo_start: break
  if not getattr(c,'select_one',None): continue
  # 네이버 본문에 삽입된 URL/링크카드/링크 문단은 홈페이지로 가져오지 않는다.
  if is_link_component(c): continue
  cl=' '.join(c.get('class',[]))
  if 'se-horizontalLine' in cl or c.select_one('.se-horizontalLine') or c.name=='hr': out.append('<hr class="article-divider naver-divider">'); continue
  table=c.select_one('table') if c.name!='table' else c
  if table:
   rows=[]
   for tr in table.find_all('tr'):
    cells=[]
    for td in tr.find_all(['th','td']):
     v=txt(td)
     if v: cells.append(f'<{td.name}>{html.escape(v)}</{td.name}>')
    if cells: rows.append('<tr>'+''.join(cells)+'</tr>')
   if rows: out.append('<table class="naver-table"><tbody>'+''.join(rows)+'</tbody></table>')
   continue
  imgs=c.find_all('img'); pars=c.select('.se-text-paragraph,.se-module-text p,.se-section-text p')
  if imgs and not pars:
   for im in imgs:
    # 링크가 걸린 이미지는 삽입 링크로 보고 제외한다.
    if im.find_parent('a',href=True): continue
    src=im.get('data-lazy-src') or im.get('data-src') or im.get('src') or ''
    if not src: continue
    imgno+=1; loc=saveimg(src,slug,imgno)
    if loc: out.append(f'<p class="media-paragraph naver-image"><img src="{html.escape(loc,quote=True)}" alt="" loading="lazy" decoding="async"></p>')
   continue
  if pars:
   for p in pars:
    if p.find('a',href=True): continue
    v=txt(p); k=re.sub(r'\W+','',v)
    if len(k)<2 or k in seen: continue
    seen.add(k); out.append(styled_text(p))
 body='\n'.join(out); chars=len(re.sub(r'\s+','',' '.join(BeautifulSoup(body,'html.parser').stripped_strings)))
 if chars<500: raise RuntimeError(f'short formatted body {chars}')
 return body,chars,imgno
def main():
 posts=json.loads(DATA.read_text(encoding='utf-8')); changed=0
 for p in posts:
  if p.get('source')!='naver-blog': continue
  slug=str(p.get('slug','')).replace('.html',''); path=ROOT/'posts'/f'{slug}.html'
  if not path.exists(): continue
  old=path.read_text(encoding='utf-8',errors='replace')
  if 'name="dg-naver-format" content="6"' in old: continue
  u=p.get('source_url') or (f'https://blog.naver.com/{BLOG}/{slug.removeprefix("naver-")}' if slug.startswith('naver-') else '')
  if not u: continue
  try:
   body,chars,imgs=extract(u,slug); soup=BeautifulSoup(old,'html.parser'); node=soup.select_one('.article-body')
   if not node: continue
   node.clear(); frag=BeautifulSoup(body,'html.parser')
   for x in list(frag.contents): node.append(x)
   for oldmeta in soup.select('meta[name="dg-naver-format"]'): oldmeta.decompose()
   meta=soup.new_tag('meta'); meta['name']='dg-naver-format'; meta['content']='6'; soup.head.append(meta)
   path.write_text(str(soup),encoding='utf-8'); changed+=1; print('FORMAT_REFRESHED',slug,'chars='+str(chars),'images='+str(imgs)); time.sleep(.15)
  except Exception as e: print('FORMAT_SKIP',slug,e)
 print('FORMAT_REFRESHED_TOTAL',changed)
if __name__=='__main__': main()
