import json, os, re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]; POSTS_JSON=ROOT/'data'/'posts.json'; OUT_DIR=ROOT/'assets'/'posts'; OUT_DIR.mkdir(parents=True,exist_ok=True)
SIZE=1080; SKY='#7FD1FF'; BLUE='#36a9e1'; NAVY='#173B6B'; INK='#20344A'; WHITE='#FFFFFF'
FONT_BOLD=['/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc','/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc']; FONT_REG=['/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc','/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc']; EMOJI_FONTS=['/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf','/usr/share/fonts/truetype/ancient-scripts/Symbola_hint.ttf']
def font(size,bold=True):
 for p in (FONT_BOLD if bold else FONT_REG):
  if os.path.exists(p):return ImageFont.truetype(p,size=size,index=0)
 return ImageFont.load_default()
def emoji_font(size):
 for p in EMOJI_FONTS:
  if os.path.exists(p):
   try:return ImageFont.truetype(p,size=size)
   except:pass
 return font(size,False)
def clean_title(t):
 t=re.sub(r'^\s*\[[^\]]+\]\s*','',t or '').strip();t=re.sub(r'\s*\|\s*',' · ',t);return re.sub(r'\s+',' ',t)
def short_title(t):
 t=clean_title(t);t=re.sub(r'\s*(총정리|완벽정리|한눈에 정리)\s*$','',t);parts=re.split(r'\s*[·,]\s*',t)
 if len(t)>34 and len(parts)>1:t=' · '.join(parts[:2])
 return t[:54].strip()
def pick_point(t):
 for k in ['상속순위','대습상속','3개월','임기만료','본점이전','본점 이전','상속재산','예금','보험금','주주전원','서면결의','대표이사','상속포기','한정승인','상속등기','취득세','증자','상호변경','목적변경','재산분할','근저당']:
  if k in t:return k
 return ''
def wrap_text(d,text,f,max_width,max_lines=3):
 words=re.split(r'(\s+|·|,|\?|!)',text);lines=[];cur=''
 for token in words:
  if not token:continue
  test=cur+token
  if cur and d.textbbox((0,0),test,font=f)[2]>max_width:lines.append(cur.strip(' ·,'));cur=token.lstrip()
  else:cur=test
 if cur.strip():lines.append(cur.strip(' ·,'))
 if len(lines)>max_lines:lines=lines[:max_lines];lines[-1]=lines[-1].rstrip(' ·,')+'…'
 return lines
def fit_title(d,text,max_width,max_lines=3):
 for size in range(90,58,-2):
  f=font(size,True);lines=wrap_text(d,text,f,max_width,max_lines)
  if len(lines)<=max_lines and all(d.textbbox((0,0),x,font=f)[2]<=max_width for x in lines):return f,lines
 f=font(58,True);return f,wrap_text(d,text,f,max_width,max_lines)
def draw_logo(img,d,category):
 fav=ROOT/'favicon.png'
 if fav.exists():
  try:
   icon=Image.open(fav).convert('RGBA');icon.thumbnail((112,112),Image.Resampling.LANCZOS);img.paste(icon,(62,62),icon)
  except:pass
 d.text((192,72),'등기로',font=font(48,True),fill=BLUE);d.text((194,134),category or '법률정보',font=font(26,True),fill=INK)
def pick_icon(t,category):
 if any(k in t for k in ['상속순위','대습상속','상속인 순위']):return '🪜'
 if any(k in t for k in ['3개월','기간','기한']):return '⏳'
 if any(k in t for k in ['임기','임기만료','날짜']):return '📅'
 if any(k in t for k in ['본점이전','본점 이전','주소변경','주소 변경']):return '📍'
 if any(k in t for k in ['조회','찾기','확인']):return '🔍'
 if any(k in t for k in ['예금','보험금','금융','퇴직금','주식']):return '🏦'
 if any(k in t for k in ['주주','서면결의','주주총회']):return '🗳️'
 if any(k in t for k in ['대표이사','임원','감사','이사']):return '🧑‍💼'
 if category=='법인등기':return '🧑‍💼'
 if category=='상속포기·한정승인':return '⏳'
 return '🔍'
def draw_emoji(img,emoji):
 layer=Image.new('RGBA',(SIZE,SIZE),(0,0,0,0));ld=ImageDraw.Draw(layer);ef=emoji_font(190)
 try:
  box=ld.textbbox((0,0),emoji,font=ef,embedded_color=True);w=box[2]-box[0];h=box[3]-box[1];ld.text(((SIZE-w)//2,790-h//2),emoji,font=ef,embedded_color=True)
 except TypeError:
  box=ld.textbbox((0,0),emoji,font=ef);w=box[2]-box[0];h=box[3]-box[1];ld.text(((SIZE-w)//2,790-h//2),emoji,font=ef,fill=NAVY)
 img.alpha_composite(layer)
def highlighted(d,line,f,y,point):
 total=d.textbbox((0,0),line,font=f)[2];x=(SIZE-total)//2
 if point and point in line:
  before,after=line.split(point,1);d.text((x,y),before,font=f,fill=INK);bw=d.textbbox((0,0),before,font=f)[2];d.text((x+bw,y),point,font=f,fill=BLUE);pw=d.textbbox((0,0),point,font=f)[2];d.text((x+bw+pw,y),after,font=f,fill=INK)
 else:d.text((x,y),line,font=f,fill=INK)
def create_thumbnail(post,path):
 img=Image.new('RGBA',(SIZE,SIZE),WHITE);d=ImageDraw.Draw(img);d.rounded_rectangle((18,18,SIZE-18,SIZE-18),radius=34,fill=WHITE,outline=SKY,width=12);draw_logo(img,d,post.get('category',''));title=short_title(post.get('title',''));point=pick_point(title);tf,lines=fit_title(d,title,870,3);lh=int(tf.size*1.32);sy=max(300,500-(lh*len(lines))//2)
 for i,line in enumerate(lines):highlighted(d,line,tf,sy+i*lh,point)
 draw_emoji(img,pick_icon(title,post.get('category','')));img.convert('RGB').save(path,'PNG',optimize=True)
def patch_article(slug,thumb):
 p=ROOT/'posts'/f'{slug}.html'
 if not p.exists():return
 s=p.read_text(encoding='utf-8');rel='/'+thumb.as_posix().lstrip('/');absu='https://www.deunggiro.kr'+rel
 if re.search(r'<meta\s+name=["\']dg-thumbnail["\']',s,re.I):s=re.sub(r'<meta\s+name=["\']dg-thumbnail["\']\s+content=["\'][^"\']*["\']\s*/?>',f'<meta name="dg-thumbnail" content="{rel}">',s,flags=re.I)
 else:s=s.replace('</head>',f'<meta name="dg-thumbnail" content="{rel}">\n</head>',1)
 for prop in ['og:image','twitter:image']:
  attr='property' if prop=='og:image' else 'name';pat=rf'<meta\s+{attr}=["\']{re.escape(prop)}["\']\s+content=["\'][^"\']*["\']\s*/?>';tag=f'<meta {attr}="{prop}" content="{absu}">'
  if re.search(pat,s,re.I):s=re.sub(pat,tag,s,flags=re.I)
  else:s=s.replace('</head>',tag+'\n</head>',1)
 p.write_text(s,encoding='utf-8')
def main():
 posts=json.loads(POSTS_JSON.read_text(encoding='utf-8'))
 for post in posts:
  slug=post.get('slug')
  if not slug:continue
  out=OUT_DIR/f'{slug}-thumbnail.png';create_thumbnail(post,out);post['thumbnail']='/assets/posts/'+out.name;patch_article(slug,out.relative_to(ROOT))
 POSTS_JSON.write_text(json.dumps(posts,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('generated',len(posts),'thumbnails with approved preview icons')
if __name__=='__main__':main()
