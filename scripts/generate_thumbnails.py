import json, os, re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]; POSTS_JSON=ROOT/'data'/'posts.json'; OUT_DIR=ROOT/'assets'/'posts'; OUT_DIR.mkdir(parents=True,exist_ok=True)
SIZE=1080; SKY='#7FD1FF'; BLUE='#36a9e1'; NAVY='#173B6B'; INK='#20344A'; WHITE='#FFFFFF'
FONT_BOLD=['/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc','/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc']; FONT_REG=['/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc','/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc']; EMOJI_FONT='/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'
def font(size,bold=True):
 for p in (FONT_BOLD if bold else FONT_REG):
  if os.path.exists(p):return ImageFont.truetype(p,size=size,index=0)
 return ImageFont.load_default()
def clean_title(t):
 t=re.sub(r'^\s*\[[^\]]+\]\s*','',t or '').strip();t=re.sub(r'\s*\|\s*',' · ',t);return re.sub(r'\s+',' ',t)
def short_title(t):
 t=clean_title(t);t=re.sub(r'\s*(총정리|완벽정리|한눈에 정리)\s*$','',t);parts=[x.strip() for x in re.split(r'\s*[·,|]\s*',t) if x.strip()]
 if len(t)>38 and len(parts)>1:t=' · '.join(parts[:2])
 return t.strip()
def pick_point(t):
 for k in ['상속순위','대습상속','3개월','임기만료','본점이전','본점 이전','상속재산','예금','보험금','주주전원','서면결의','대표이사','상속포기','한정승인','상속등기','취득세','증자','자본금','상호변경','목적변경','재산분할','근저당','담보']:
  if k in t:return k
 return ''
def wrap_text(d,text,f,max_width):
 words=re.split(r'(\s+|·|,|\?|!)',text);lines=[];cur=''
 for token in words:
  if not token:continue
  test=cur+token
  if cur and d.textbbox((0,0),test,font=f)[2]>max_width:lines.append(cur.strip(' ·,'));cur=token.lstrip()
  else:cur=test
 if cur.strip():lines.append(cur.strip(' ·,'))
 return lines
def fit_title(d,text,max_width,max_lines=3):
 for size in range(128,68,-2):
  f=font(size,True);lines=wrap_text(d,text,f,max_width)
  if len(lines)<=max_lines and all(d.textbbox((0,0),x,font=f)[2]<=max_width for x in lines):return f,lines
 f=font(68,True);return f,wrap_text(d,text,f,max_width)[:max_lines]
def draw_logo(img,d,category):
 fav=ROOT/'favicon.png'
 if fav.exists():
  try:
   icon=Image.open(fav).convert('RGBA');icon.thumbnail((126,126),Image.Resampling.LANCZOS);img.paste(icon,(58,58),icon)
  except:pass
 d.text((202,68),'등기로',font=font(56,True),fill=BLUE);d.text((204,136),category or '법률정보',font=font(30,True),fill=INK)
def pick_icon(t,category):
 # Pick the most specific subject first; use one native color emoji, never a drawn icon.
 if any(k in t for k in ['보험금','보험','해지환급금']):return '☂️'
 if any(k in t for k in ['상속재산분할','재산분할심판','상속분쟁','분할심판','심판청구']):return '🏛️'
 if any(k in t for k in ['상속순위','대습상속','상속인 순위']):return '👨‍👩‍👧‍👦'
 if '상속포기' in t:return '✋'
 if '한정승인' in t:return '🛡️'
 if any(k in t for k in ['3개월','기간','기한']):return '⏳'
 if any(k in t for k in ['본점이전','본점 이전','주소변경','주소 변경']):return '🚚'
 if '대표이사' in t and any(k in t for k in ['변경','선임','사임','해임']):return '🔄'
 if any(k in t for k in ['상호변경','상호 변경']):return '🪧'
 if any(k in t for k in ['목적변경','목적 변경']):return '🧭'
 if any(k in t for k in ['증자','자본금']):return '📈'
 if any(k in t for k in ['근저당','담보']):return '🏦'
 if any(k in t for k in ['주주','서면결의','주주총회','결의']):return '🗳️'
 if any(k in t for k in ['예금','금융','퇴직금','주식']):return '💵'
 if any(k in t for k in ['조회','찾기','확인']):return '🔍'
 if any(k in t for k in ['임기','임기만료','날짜']):return '📅'
 if category=='부동산등기' or any(k in t for k in ['부동산등기','상속등기','소유권이전']):return '🏠'
 return '🔍'
def draw_emoji(img,emoji):
 if not os.path.exists(EMOJI_FONT):return
 try:ef=ImageFont.truetype(EMOJI_FONT,size=109)
 except:return
 tile=Image.new('RGBA',(220,220),(0,0,0,0));td=ImageDraw.Draw(tile)
 try:
  box=td.textbbox((0,0),emoji,font=ef,embedded_color=True);w=box[2]-box[0];h=box[3]-box[1];td.text(((220-w)//2,(220-h)//2),emoji,font=ef,embedded_color=True)
 except Exception:return
 bbox=tile.getbbox()
 if not bbox:return
 glyph=tile.crop(bbox);glyph.thumbnail((235,235),Image.Resampling.LANCZOS);img.alpha_composite(glyph,((SIZE-glyph.width)//2,790))
def highlighted(d,line,f,y,point):
 total=d.textbbox((0,0),line,font=f)[2];x=(SIZE-total)//2
 if point and point in line:
  before,after=line.split(point,1);d.text((x,y),before,font=f,fill=INK);bw=d.textbbox((0,0),before,font=f)[2];d.text((x+bw,y),point,font=f,fill=BLUE);pw=d.textbbox((0,0),point,font=f)[2];d.text((x+bw+pw,y),after,font=f,fill=INK)
 else:d.text((x,y),line,font=f,fill=INK)
def create_thumbnail(post,path):
 img=Image.new('RGBA',(SIZE,SIZE),WHITE);d=ImageDraw.Draw(img);d.rounded_rectangle((18,18,SIZE-18,SIZE-18),radius=34,fill=WHITE,outline=SKY,width=12);draw_logo(img,d,post.get('category',''));title=short_title(post.get('title',''));point=pick_point(title);tf,lines=fit_title(d,title,900,3);lh=int(tf.size*1.18);sy=max(285,500-(lh*len(lines))//2)
 for i,line in enumerate(lines):highlighted(d,line,tf,sy+i*lh,point)
 draw_emoji(img,pick_icon(title,post.get('category','')));img.convert('RGB').save(path,'PNG',optimize=True)
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
 POSTS_JSON.write_text(json.dumps(posts,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('generated',len(posts),'thumbnails with topic-specific color emoji and image SEO markup')
if __name__=='__main__':main()
