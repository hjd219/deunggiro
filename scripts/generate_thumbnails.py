import json, os, re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]; POSTS_JSON=ROOT/'data'/'posts.json'; OUT_DIR=ROOT/'assets'/'posts'; OUT_DIR.mkdir(parents=True,exist_ok=True)
SIZE=1080; SKY='#7FD1FF'; BLUE='#36a9e1'; NAVY='#173B6B'; INK='#20344A'; WHITE='#FFFFFF'; PALE='#DDF3FF'
FONT_BOLD=['/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc','/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc']; FONT_REG=['/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc','/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc']
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
 if any(k in t for k in ['상속재산분할','재산분할심판','상속분쟁','분할심판','심판청구']):return 'court'
 if any(k in t for k in ['상속순위','대습상속','상속인 순위']):return 'family'
 if '상속포기' in t:return 'reject'
 if '한정승인' in t:return 'shield'
 if any(k in t for k in ['3개월','기간','기한']):return 'hourglass'
 if any(k in t for k in ['본점이전','본점 이전','주소변경','주소 변경']):return 'truck'
 if '대표이사' in t and any(k in t for k in ['변경','선임','사임','해임']):return 'change'
 if any(k in t for k in ['상호변경','상호 변경']):return 'sign'
 if any(k in t for k in ['목적변경','목적 변경']):return 'compass'
 if any(k in t for k in ['증자','자본금']):return 'stock'
 if any(k in t for k in ['근저당','담보']):return 'bank'
 if any(k in t for k in ['주주','서면결의','주주총회','결의']):return 'vote'
 if any(k in t for k in ['예금','보험금','금융','퇴직금','주식']):return 'money'
 if any(k in t for k in ['조회','찾기','확인']):return 'search'
 if any(k in t for k in ['임기','임기만료','날짜']):return 'calendar'
 if category=='부동산등기' or any(k in t for k in ['부동산등기','상속등기','소유권이전']):return 'house'
 return 'search'
def draw_icon(img,key):
 d=ImageDraw.Draw(img); cx,cy=540,885; b=BLUE; n=NAVY; p=PALE; w=18
 if key=='family':
  for x,y,r in [(480,845,34),(540,825,39),(600,845,34)]:d.ellipse((x-r,y-r,x+r,y+r),fill=p,outline=b,width=12)
  d.rounded_rectangle((435,890,645,970),30,fill=p,outline=b,width=12);d.line((540,866,540,950),fill=b,width=12)
 elif key=='court':
  d.polygon([(430,845),(540,790),(650,845)],fill=b);d.rectangle((440,850,640,875),fill=n)
  for x in [465,520,575,630]:d.rectangle((x-12,875,x+12,950),fill=b)
  d.rectangle((425,950,655,975),fill=n)
 elif key=='reject':
  d.ellipse((450,795,630,975),fill=p,outline=b,width=18);d.line((480,945,600,825),fill=b,width=24)
 elif key=='shield':
  d.polygon([(540,790),(635,825),(620,915),(540,980),(460,915),(445,825)],fill=p,outline=b);d.line((540,815,540,945),fill=b,width=16);d.line((500,885,530,915,585,850),fill=n,width=15,joint='curve')
 elif key=='hourglass':
  d.line((465,800,615,800),fill=n,width=18);d.line((465,970,615,970),fill=n,width=18);d.polygon([(480,815),(600,815),(565,875),(600,955),(480,955),(515,875)],fill=p,outline=b)
 elif key=='truck':
  d.rounded_rectangle((425,835,565,930),15,fill=p,outline=b,width=12);d.polygon([(565,870),(620,870),(655,915),(655,930),(565,930)],fill=b);d.ellipse((465,915,515,965),fill=n);d.ellipse((600,915,650,965),fill=n)
 elif key=='change':
  d.arc((440,795,640,965),200,350,fill=b,width=22);d.arc((440,805,640,975),20,170,fill=n,width=22);d.polygon([(625,805),(655,835),(610,845)],fill=b);d.polygon([(455,965),(425,935),(470,925)],fill=n)
 elif key=='sign':
  d.rounded_rectangle((430,805,650,910),18,fill=p,outline=b,width=14);d.line((540,910,540,975),fill=n,width=18);d.line((490,975,590,975),fill=n,width=18);d.line((475,855,605,855),fill=b,width=15)
 elif key=='compass':
  d.ellipse((445,790,635,980),fill=p,outline=b,width=15);d.polygon([(575,835),(550,900),(505,945),(530,875)],fill=n);d.ellipse((525,870,555,900),fill=b)
 elif key=='stock':
  d.line((450,950,450,815),fill=n,width=14);d.line((450,950,645,950),fill=n,width=14);d.line((475,920,525,875,565,895,625,820),fill=b,width=20,joint='curve');d.polygon([(625,820),(590,825),(620,855)],fill=b)
 elif key=='bank':
  d.polygon([(430,845),(540,790),(650,845)],fill=b);d.rectangle((440,850,640,875),fill=n)
  for x in [470,520,570,620]:d.rectangle((x-10,875,x+10,950),fill=p,outline=b,width=6)
  d.rectangle((425,950,655,975),fill=n)
 elif key=='vote':
  d.rounded_rectangle((455,865,625,965),15,fill=p,outline=b,width=14);d.rectangle((485,835,595,875),fill=WHITE,outline=n,width=10);d.line((500,815,565,880),fill=b,width=16);d.line((565,815,500,880),fill=b,width=16)
 elif key=='money':
  d.rounded_rectangle((425,825,655,955),18,fill=p,outline=b,width=14);d.ellipse((505,850,575,930),outline=n,width=12);d.line((455,855,485,855),fill=b,width=12);d.line((595,925,625,925),fill=b,width=12)
 elif key=='calendar':
  d.rounded_rectangle((445,815,635,965),18,fill=p,outline=b,width=14);d.rectangle((445,815,635,860),fill=b);d.line((490,790,490,835),fill=n,width=14);d.line((590,790,590,835),fill=n,width=14)
  for x in [485,540,595]:
   for y in [895,935]:d.ellipse((x-8,y-8,x+8,y+8),fill=n)
 elif key=='house':
  d.polygon([(430,875),(540,790),(650,875)],fill=b);d.rectangle((465,870,615,970),fill=p,outline=n,width=12);d.rectangle((525,910,565,970),fill=b)
 else:
  d.ellipse((450,800,590,940),fill=p,outline=b,width=18);d.line((575,925,645,980),fill=n,width=24)
def highlighted(d,line,f,y,point):
 total=d.textbbox((0,0),line,font=f)[2];x=(SIZE-total)//2
 if point and point in line:
  before,after=line.split(point,1);d.text((x,y),before,font=f,fill=INK);bw=d.textbbox((0,0),before,font=f)[2];d.text((x+bw,y),point,font=f,fill=BLUE);pw=d.textbbox((0,0),point,font=f)[2];d.text((x+bw+pw,y),after,font=f,fill=INK)
 else:d.text((x,y),line,font=f,fill=INK)
def create_thumbnail(post,path):
 img=Image.new('RGBA',(SIZE,SIZE),WHITE);d=ImageDraw.Draw(img);d.rounded_rectangle((18,18,SIZE-18,SIZE-18),radius=34,fill=WHITE,outline=SKY,width=12);draw_logo(img,d,post.get('category',''));title=short_title(post.get('title',''));point=pick_point(title);tf,lines=fit_title(d,title,900,3);lh=int(tf.size*1.18);sy=max(285,500-(lh*len(lines))//2)
 for i,line in enumerate(lines):highlighted(d,line,tf,sy+i*lh,point)
 draw_icon(img,pick_icon(title,post.get('category','')));img.convert('RGB').save(path,'PNG',optimize=True)
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
 POSTS_JSON.write_text(json.dumps(posts,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('generated',len(posts),'thumbnails with flat 2D icons')
if __name__=='__main__':main()
