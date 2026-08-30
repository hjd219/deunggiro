from __future__ import annotations
import html,json,re,time
from io import BytesIO
from pathlib import Path
from urllib.parse import urljoin,parse_qs,urlparse
import requests
from bs4 import BeautifulSoup
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'/'posts.json'; MEDIA=ROOT/'assets'/'naver-images'; BLOG='hjd21'; FORMAT_VERSION='12'
UA={'User-Agent':'Mozilla/5.0 (compatible; DeunggiroFormat/1.9; +https://www.deunggiro.kr/)'}
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
def normalize_img_url(src):
 src=html.unescape((src or '').strip())
 if src.startswith('//'): src='https:'+src
 if src.startswith('http://'): src='https://'+src[7:]
 if src.startswith('data:'): return ''
 return src
def _linkdata_src(holder):
 raw=holder.get('data-linkdata') if getattr(holder,'get',None) else ''
 if not raw: return ''
 try:
  data=json.loads(html.unescape(raw))
  for k in ('originalSrc','originalImageUrl','imageUrl','src'):
   src=normalize_img_url(data.get(k))
   if src: return src
 except Exception:
  decoded=html.unescape(raw)
  for k in ('originalSrc','originalImageUrl','imageUrl','src'):
   m=re.search(rf'"{k}"\s*:\s*"([^"]+)"',decoded)
   if m:
    src=normalize_img_url(m.group(1).replace('\\/','/'))
    if src: return src
 return ''
def image_candidates(node):
 out=[]
 def add(v):
  v=normalize_img_url(v)
  if v and v not in out and (v.startswith('http') or 'pstatic.net' in v): out.append(v)
 holders=[]
 if getattr(node,'attrs',None): holders.append(node)
 if getattr(node,'find_all',None): holders.extend(node.find_all(attrs={'data-linkdata':True}))
 if getattr(node,'find_parent',None):
  p=node.find_parent(attrs={'data-linkdata':True})
  if p: holders.append(p)
 for h in holders: add(_linkdata_src(h))
 imgs=[]
 if getattr(node,'name',None)=='img': imgs.append(node)
 if getattr(node,'select',None): imgs.extend(node.select('img'))
 for img in imgs:
  for a in ('data-original','data-lazy-src','data-src','src'): add(img.get(a))
 return out
def download_best(candidates):
 best=None
 for src in candidates:
  try:
   r=requests.get(src,headers=UA,timeout=20); r.raise_for_status(); data=r.content
   try:
    with Image.open(BytesIO(data)) as im: w,h=im.size
   except Exception: w=h=0
   score=(w*h,len(data))
   if best is None or score>best[0]: best=(score,src,data,r.headers.get('content-type') or '',w,h)
  except Exception as e: print('FORMAT_IMAGE_CANDIDATE_SKIP',str(e))
 return best
def saveimg(candidates,slug,i,skip_if_small=False):
 best=download_best(candidates)
 if not best: return ''
 score,src,data,ct,w,h=best
 if skip_if_small and w<450 and h<450 and len(data)<120000:
  print('FORMAT_TRAILING_THUMB_SKIP',slug,f'{w}x{h}',len(data)); return ''
 ext='.png' if 'png' in ct.lower() else '.webp' if 'webp' in ct.lower() else '.gif' if 'gif' in ct.lower() else '.jpg'
 d=MEDIA/slug; d.mkdir(parents=True,exist_ok=True); p=d/f'fmt-{i:02d}{ext}'; p.write_bytes(data)
 print('FORMAT_IMAGE_BEST',slug,i,f'{w}x{h}',len(data),src)
 return '/'+p.relative_to(ROOT).as_posix()
def promo_start_text(v):
 v=re.sub(r'\s+','',v)
 return any(k in v for k in ('현재두법무사사무소상담안내','현재두법무사상담안내','현재두법무사사무소상담','032-425-1500'))
def is_link_component(c):
 cl=' '.join(c.get('class',[])).lower()
 return ('se-oglink' in cl or 'se-module-oglink' in cl or 'se-module-link' in cl or c.select_one('.se-oglink-info,.se-module-oglink,.se-module-link,.se-link-preview') is not None)
def extract(u,slug):
 s=BeautifulSoup(get(view(u)).text,'html.parser'); root=s.select_one('.se-main-container') or s.select_one('#postViewArea') or s.select_one('.post-view')
 if not root: raise RuntimeError('no body')
 comps=root.select(':scope > .se-component') or root.select('.se-component') or list(root.children)
 promo_start=len(comps)
 for i,c in enumerate(comps):
  if getattr(c,'select_one',None) and promo_start_text(txt(c)): promo_start=i; break
 out=[]; imgno=0; seen=set(); seen_imgs=set()
 for i,c in enumerate(comps):
  if i>=promo_start: break
  if not getattr(c,'select_one',None): continue
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
  text_nodes=c.select('.se-text-paragraph,.se-module-text p,.se-section-text p')
  if text_nodes:
   for n in text_nodes:
    if n.find('a',href=True): continue
    v=txt(n); k=re.sub(r'\W+','',v)
    if len(k)<2 or k in seen: continue
    seen.add(k); out.append(styled_text(n))
   continue
  image_node=c.select_one('.se-module-image') or c.select_one('[data-linktype="img"]') or c.select_one('img') or c.select_one('[data-linkdata]')
  if image_node:
   candidates=image_candidates(image_node)
   key='|'.join(candidates)
   if not candidates or key in seen_imgs: continue
   seen_imgs.add(key); imgno+=1
   trailing=(promo_start-len(comps) != 0 and i >= max(0,promo_start-4)) or (promo_start==len(comps) and i>=max(0,len(comps)-3))
   loc=saveimg(candidates,slug,imgno,skip_if_small=trailing)
   if loc: out.append(f'<p class="media-paragraph naver-image"><img src="{html.escape(loc,quote=True)}" alt="" loading="lazy" decoding="async"></p>')
 body='\n'.join(out); chars=len(re.sub(r'\s+','',' '.join(BeautifulSoup(body,'html.parser').stripped_strings)))
 if chars<500: raise RuntimeError(f'short formatted body {chars}')
 print('FORMAT_EXTRACT',slug,'components='+str(len(comps)),'source_images='+str(len(root.select('img,[data-linktype="img"],[data-linkdata]'))),'saved_images='+str(imgno))
 return body,chars,imgno
def main():
 posts=json.loads(DATA.read_text(encoding='utf-8')); changed=0
 for p in posts:
  if p.get('source')!='naver-blog': continue
  slug=str(p.get('slug','')).replace('.html',''); path=ROOT/'posts'/f'{slug}.html'
  if not path.exists(): continue
  old=path.read_text(encoding='utf-8',errors='replace')
  if f'name="dg-naver-format" content="{FORMAT_VERSION}"' in old: continue
  u=p.get('source_url') or (f'https://blog.naver.com/{BLOG}/{slug.removeprefix("naver-")}' if slug.startswith('naver-') else '')
  if not u: continue
  try:
   body,chars,imgs=extract(u,slug); soup=BeautifulSoup(old,'html.parser'); node=soup.select_one('.article-body')
   if not node: continue
   node.clear(); frag=BeautifulSoup(body,'html.parser')
   for x in list(frag.contents): node.append(x)
   for oldmeta in soup.select('meta[name="dg-naver-format"]'): oldmeta.decompose()
   meta=soup.new_tag('meta'); meta['name']='dg-naver-format'; meta['content']=FORMAT_VERSION; soup.head.append(meta)
   path.write_text(str(soup),encoding='utf-8'); changed+=1; print('FORMAT_REFRESHED',slug,'chars='+str(chars),'images='+str(imgs)); time.sleep(.15)
  except Exception as e: print('FORMAT_SKIP',slug,e)
 print('FORMAT_REFRESHED_TOTAL',changed)
if __name__=='__main__': main()
