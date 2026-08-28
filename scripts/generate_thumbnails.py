import json, os, re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]; POSTS_JSON=ROOT/'data'/'posts.json'; OUT_DIR=ROOT/'assets'/'posts'; OUT_DIR.mkdir(parents=True,exist_ok=True)
SIZE=1080; SKY='#7FD1FF'; BLUE='#36a9e1'; INK='#20344A'; WHITE='#FFFFFF'
FONT_BOLD=['/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc','/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc']; FONT_REG=['/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc','/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc']
def font(size,bold=True):
 for p in (FONT_BOLD if bold else FONT_REG):
  if os.path.exists(p):return ImageFont.truetype(p,size=size,index=0)
 return ImageFont.load_default()
def clean_title(t):
 t=re.sub(r'^\s*\[[^\]]+\]\s*','',t or '').strip();t=re.sub(r'\s*\|\s*',' · ',t);return re.sub(r'\s+',' ',t)
def short_title(t):
 t=clean_title(t)
 if re.search(r'가족\s*\([^)]*부모[^)]*배우자[^)]*형제[^)]*\).*사망',t):return '가족 사망 후 해야 할 일 총정리'
 m=re.match(r'^(.+?(?:총정리|완벽정리|한눈에 정리))(?=\s*[,·]|$)',t)
 if m and len(t)>38:return m.group(1).strip()
 if len(t)>42 and ',' in t:
  head=t.split(',',1)[0].strip()
  if len(head)>=12:return head
 return t.strip()
def pick_point(t):
 # Automatic phrase extraction: no per-topic keyword list is required.
 text=re.sub(r'[\[\](){}]',' ',t);text=re.sub(r'\s+',' ',text).strip()
 stop={'총정리','완벽정리','한눈에','정리','절차','방법','필요서류','서류','비용','기간','관할','기준','주의사항','해야','할','일','후','시','경우','어떻게','하나요','부터','까지','관련','최신','글','인천'}
 # Prefer meaningful Korean noun phrases immediately before common legal/action words.
 patterns=[
  r'([가-힣A-Za-z0-9]{2,12}\s*[가-힣A-Za-z0-9]{0,8})(변경등기|변경|이전|말소|설정|설립|증자|감자|해임|선임|사임|포기|승인|등기|분할|심판|신청|허가|신고)',
  r'([가-힣A-Za-z0-9]{2,16})(보험금|해지환급금|유족연금|퇴직금|취득세|과태료)',
 ]
 for pat in patterns:
  m=re.search(pat,text)
  if m:
   phrase=''.join(x for x in m.groups() if x).strip()
   phrase=re.sub(r'^(부모님|부모|남편|아내|배우자|가족)\s+(사망\s+후\s+)?','',phrase).strip()
   if 2<=len(phrase)<=18:return phrase
 # Score chunks from the title and choose a compact subject phrase.
 chunks=[c.strip() for c in re.split(r'[·,|:/?！!]|\s+-\s+',text) if c.strip()]
 candidates=[]
 for c in chunks:
  words=[w for w in c.split() if w not in stop and len(w)>1]
  if not words:continue
  for n in (2,1):
   for i in range(max(0,len(words)-n+1)):
    p=' '.join(words[i:i+n]).strip()
    if 2<=len(p)<=16:
     score=len(p)+(5 if n==2 else 0)
     if any(s in p for s in ['총정리','절차','방법','서류','기간','관할']):score-=8
     candidates.append((score,p))
 if candidates:return max(candidates,key=lambda x:x[0])[1]
 words=[w for w in text.split() if w not in stop and len(w)>1]
 return words[0] if words else ''
def wrap_text(d,text,f,max_width):
 words=re.split(r'(\s+|·|,|\?|!)',text);lines=[];cur=''
 for token in words:
  if not token:continue
  test=cur+token
  if cur and d.textbbox((0,0),test,font=f)[2]>max_width:lines.append(cur.strip(' ·,'));cur=token.lstrip()
  else:cur=test
 if cur.strip():lines.append(cur.strip(' ·,'))
 return lines
def fit_title(d,text,max_width,max_lines=4):
 for size in range(136,62,-2):
  f=font(size,True);lines=wrap_text(d,text,f,max_width)
  if len(lines)<=max_lines and all(d.textbbox((0,0),x,font=f)[2]<=max_width for x in lines):return f,lines
 f=font(62,True);return f,wrap_text(d,text,f,max_width)[:max_lines]
def draw_logo(img,d,category):
 fav=ROOT/'favicon.png'
 if fav.exists():
  try:
   icon=Image.open(fav).convert('RGBA');icon.thumbnail((126,126),Image.Resampling.LANCZOS);img.paste(icon,(58,58),icon)
  except:pass
 d.text((202,68),'등기로',font=font(56,True),fill=BLUE);d.text((204,136),category or '법률정보',font=font(30,True),fill=INK)
def highlighted(d,line,f,y,point):
 total=d.textbbox((0,0),line,font=f)[2];x=(SIZE-total)//2
 if point and point in line:
  before,after=line.split(point,1);d.text((x,y),before,font=f,fill=INK);bw=d.textbbox((0,0),before,font=f)[2];d.text((x+bw,y),point,font=f,fill=BLUE);pw=d.textbbox((0,0),point,font=f)[2];d.text((x+bw+pw,y),after,font=f,fill=INK)
 else:d.text((x,y),line,font=f,fill=INK)
def create_thumbnail(post,path):
 img=Image.new('RGBA',(SIZE,SIZE),WHITE);d=ImageDraw.Draw(img);d.rounded_rectangle((18,18,SIZE-18,SIZE-18),radius=34,fill=WHITE,outline=SKY,width=12);draw_logo(img,d,post.get('category',''));title=short_title(post.get('title',''));point=pick_point(title);tf,lines=fit_title(d,title,900,4);lh=int(tf.size*1.2);block=lh*len(lines);sy=max(275,(SIZE-block)//2+45)
 for i,line in enumerate(lines):highlighted(d,line,tf,sy+i*lh,point)
 img.convert('RGB').save(path,'PNG',optimize=True)
def patch_article(post,thumb):
 slug=post.get('slug');p=ROOT/'posts'/f'{slug}.html'
 if not p.exists():return
 s=p.read_text(encoding='utf-8');rel='/'+thumb.as_posix().lstrip('/');absu='https://www.deunggiro.kr'+rel;pageu=f'https://www.deunggiro.kr/posts/{slug}.html'
 title=post.get('title','').strip();summary=post.get('summary','').strip();date=post.get('date','').strip()
 if re.search(r'<meta\s+name=["\']dg-thumbnail["\']',s,re.I):s=re.sub(r'<meta\s+name=["\']dg-thumbnail["\']\s+content=["\'][^"\']*["\']\s*/?>',f'<meta name="dg-thumbnail" content="{rel}">',s,flags=re.I)
 else:s=s.replace('</head>',f'<meta name="dg-thumbnail" content="{rel}">\n</head>',1)
 meta_tags=[('property','og:image',absu),('property','og:image:secure_url',absu),('property','og:image:width','1080'),('property','og:image:height','1080'),('property','og:image:type','image/png'),('name','twitter:image',absu),('name','twitter:card','summary_large_image')]
 for attr,key,val in meta_tags:
  pat=rf'<meta\s+{attr}=["\']{re.escape(key)}["\']\s+content=["\'][^"\']*["\']\s*/?>';tag=f'<meta {attr}="{key}" content="{val}">'
  if re.search(pat,s,re.I):s=re.sub(pat,tag,s,flags=re.I)
  else:s=s.replace('</head>',tag+'\n</head>',1)
 if re.search(r'<meta\s+name=["\']robots["\']',s,re.I):
  def add_large(m):
   tag=m.group(0);cm=re.search(r'content=["\']([^"\']*)',tag,re.I);content=cm.group(1) if cm else ''
   if 'max-image-preview:' in content:return tag
   new=(content+', max-image-preview:large').strip(' ,')
   return re.sub(r'content=["\'][^"\']*["\']',f'content="{new}"',tag,flags=re.I) if cm else tag
  s=re.sub(r'<meta\s+name=["\']robots["\'][^>]*>',add_large,s,count=1,flags=re.I)
 else:s=s.replace('</head>','<meta name="robots" content="index,follow,max-image-preview:large">\n</head>',1)
 schema={"@context":"https://schema.org","@type":"Article","mainEntityOfPage":{"@type":"WebPage","@id":pageu},"headline":title,"description":summary or title,"image":{"@type":"ImageObject","url":absu,"width":1080,"height":1080},"datePublished":date,"dateModified":date,"author":{"@type":"Organization","name":"현재두 법무사 사무소"},"publisher":{"@type":"Organization","name":"등기로","url":"https://www.deunggiro.kr/"}}
 schema_tag='<script type="application/ld+json" id="dg-article-schema">'+json.dumps(schema,ensure_ascii=False,separators=(',',':'))+'</script>'
 if re.search(r'<script[^>]+id=["\']dg-article-schema["\'][^>]*>.*?</script>',s,re.I|re.S):s=re.sub(r'<script[^>]+id=["\']dg-article-schema["\'][^>]*>.*?</script>',schema_tag,s,count=1,flags=re.I|re.S)
 else:s=s.replace('</head>',schema_tag+'\n</head>',1)
 hero=f'<figure id="dg-post-hero-image" class="dg-post-hero-image"><img src="{rel}" alt="{title.replace("&","&amp;").replace(chr(34),"&quot;")}" width="1080" height="1080" loading="eager" fetchpriority="high" decoding="async"></figure>'
 hero_style='<style id="dg-post-hero-style">.dg-post-hero-image{max-width:720px;margin:24px auto 32px}.dg-post-hero-image img{display:block;width:100%;height:auto;border-radius:18px}</style>'
 if 'id="dg-post-hero-style"' not in s:s=s.replace('</head>',hero_style+'\n</head>',1)
 if re.search(r'<figure[^>]+id=["\']dg-post-hero-image["\'][^>]*>.*?</figure>',s,re.I|re.S):s=re.sub(r'<figure[^>]+id=["\']dg-post-hero-image["\'][^>]*>.*?</figure>',hero,s,count=1,flags=re.I|re.S)
 else:
  m=re.search(r'</h1>',s,re.I)
  if m:s=s[:m.end()]+hero+s[m.end():]
 p.write_text(s,encoding='utf-8')
def main():
 posts=json.loads(POSTS_JSON.read_text(encoding='utf-8'))
 for post in posts:
  slug=post.get('slug')
  if not slug:continue
  out=OUT_DIR/f'{slug}-thumbnail.png';create_thumbnail(post,out);post['thumbnail']='/assets/posts/'+out.name;patch_article(post,out.relative_to(ROOT))
 POSTS_JSON.write_text(json.dumps(posts,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('generated',len(posts),'thumbnails without icons and with automatic highlight phrases')
if __name__=='__main__':main()
