import json, os, re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
POSTS_JSON = ROOT / 'data' / 'posts.json'
OUT_DIR = ROOT / 'assets' / 'posts'
OUT_DIR.mkdir(parents=True, exist_ok=True)
SIZE = 1080
SKY = '#77CCFF'
BLUE = '#2457A6'
NAVY = '#183B6B'
INK = '#20344A'
MUTED = '#6B7280'
WHITE = '#FFFFFF'
BG = '#F8FCFF'

FONT_CANDIDATES = [
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc',
]
REG_CANDIDATES = [
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
]

def font(size, bold=True):
    candidates = FONT_CANDIDATES if bold else REG_CANDIDATES
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size=size, index=0)
    return ImageFont.load_default()

def clean_title(title):
    t = re.sub(r'^\s*\[[^\]]+\]\s*', '', title or '').strip()
    t = re.sub(r'\s*\|\s*', ' · ', t)
    t = re.sub(r'\s+', ' ', t)
    return t

def char_width(ch):
    if ord(ch) < 128:
        return 0.58
    return 1.0

def wrap_title(text, max_units):
    lines, cur, units = [], '', 0
    for token in re.split(r'(\s+|·|,|·|\u00b7)', text):
        if token == '':
            continue
        tu = sum(char_width(c) for c in token)
        if cur and units + tu > max_units:
            lines.append(cur.strip(' ·,'))
            cur, units = token.lstrip(), tu
        else:
            cur += token
            units += tu
    if cur.strip():
        lines.append(cur.strip(' ·,'))
    return lines

def fit_title(draw, text, box_w, max_lines=4):
    for fs in range(72, 45, -2):
        f = font(fs, True)
        units = max(8, int(box_w / (fs * 0.93)))
        lines = wrap_title(text, units)
        if len(lines) <= max_lines:
            widths = [draw.textbbox((0,0), x, font=f)[2] for x in lines]
            if max(widths or [0]) <= box_w:
                return f, lines
    f = font(46, True)
    lines = wrap_title(text, max(8, int(box_w / 43)))[:max_lines]
    if len(lines) == max_lines and ''.join(lines) != text.replace(' ', ''):
        lines[-1] = lines[-1].rstrip(' .·,') + '…'
    return f, lines

def rounded(draw, xy, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def draw_doc_icon(draw, x, y, scale=1.0):
    w, h = int(150*scale), int(185*scale)
    # shadow
    rounded(draw, (x+18,y+18,x+w+18,y+h+18), 24, '#D8EAF7')
    rounded(draw, (x,y,x+w,y+h), 24, WHITE, '#C5DCEB', 3)
    draw.polygon([(x+w-50,y),(x+w,y+50),(x+w,y)], fill='#E8F5FC')
    for i in range(4):
        yy=y+62+i*25
        draw.rounded_rectangle((x+28,yy,x+w-28,yy+8), radius=4, fill=SKY if i==0 else '#C9D5DF')

def draw_house_icon(draw, x, y, scale=1.0):
    w=int(190*scale); h=int(150*scale)
    draw.polygon([(x,y+58),(x+w//2,y),(x+w,y+58)], fill=BLUE)
    rounded(draw,(x+24,y+55,x+w-24,y+h),18,'#DFF3FF','#B6DFF7',3)
    rounded(draw,(x+77,y+92,x+116,y+h),8,WHITE)

def draw_building_icon(draw, x, y, scale=1.0):
    w=int(165*scale); h=int(185*scale)
    rounded(draw,(x,y,x+w,y+h),20,'#E5F5FF','#B8DEF6',3)
    rounded(draw,(x+48,y-28,x+w-18,y+h),18,BLUE)
    for r in range(4):
        for c in range(2):
            xx=x+67+c*42; yy=y+2+r*37
            rounded(draw,(xx,yy,xx+20,yy+18),4,WHITE)
    rounded(draw,(x+73,y+h-42,x+112,y+h),7,WHITE)

def draw_scale_icon(draw, x, y, scale=1.0):
    s=scale
    cx=x+90*s; top=y+20*s
    draw.line((cx,top,cx,y+170*s), fill=NAVY, width=max(4,int(8*s)))
    draw.line((x+25*s,y+63*s,x+155*s,y+63*s), fill=NAVY, width=max(4,int(8*s)))
    draw.line((x+35*s,y+63*s,x+12*s,y+120*s), fill=NAVY, width=max(2,int(5*s)))
    draw.line((x+145*s,y+63*s,x+168*s,y+120*s), fill=NAVY, width=max(2,int(5*s)))
    draw.arc((x-10*s,y+100*s,x+70*s,y+150*s),0,180,fill=SKY,width=max(3,int(6*s)))
    draw.arc((x+110*s,y+100*s,x+190*s,y+150*s),0,180,fill=SKY,width=max(3,int(6*s)))
    draw.line((x+40*s,y+170*s,x+140*s,y+170*s),fill=NAVY,width=max(4,int(8*s)))

def draw_people_icon(draw, x, y, scale=1.0):
    colors=['#7FCFFF','#A9DFFF','#5FAEE8']
    centers=[(x+45*scale,y+55*scale),(x+100*scale,y+35*scale),(x+155*scale,y+55*scale)]
    for i,(cx,cy) in enumerate(centers):
        r=28*scale
        draw.ellipse((cx-r,cy-r,cx+r,cy+r),fill=colors[i])
        rounded(draw,(cx-38*scale,cy+30*scale,cx+38*scale,cy+105*scale),20*scale,colors[i])

def category_icons(draw, category):
    y=750
    if category == '법인등기':
        draw_building_icon(draw, 390, y, .95); draw_doc_icon(draw, 585, y+8, .82)
    elif category == '부동산등기':
        draw_house_icon(draw, 385, y+18, .9); draw_doc_icon(draw, 590, y+8, .82)
    elif category == '상속재산분할':
        draw_people_icon(draw, 360, y+10, .9); draw_scale_icon(draw, 600, y+8, .9)
    elif category == '가사':
        draw_people_icon(draw, 365, y+10, .9); draw_scale_icon(draw, 600, y+8, .85)
    elif category == '상속포기·한정승인':
        draw_doc_icon(draw, 405, y+5, .82); draw_scale_icon(draw, 605, y+10, .9)
    else:
        draw_house_icon(draw, 390, y+18, .85); draw_doc_icon(draw, 590, y+8, .82)

def create_thumbnail(post, path):
    img = Image.new('RGB',(SIZE,SIZE),BG)
    d = ImageDraw.Draw(img)
    # outer sky-blue frame
    rounded(d,(18,18,SIZE-18,SIZE-18),34,WHITE,SKY,12)
    # subtle top wash
    d.rounded_rectangle((42,42,SIZE-42,185),radius=24,fill='#F0FAFF')

    # favicon / brand block
    fav = ROOT / 'favicon.png'
    if fav.exists():
        try:
            logo=Image.open(fav).convert('RGBA')
            logo.thumbnail((108,108),Image.Resampling.LANCZOS)
            img.paste(logo,(65,65),logo)
        except Exception:
            rounded(d,(65,65,173,173),22,BLUE)
    else:
        rounded(d,(65,65,173,173),22,BLUE)
    d.text((195,84),'등기로',font=font(42,True),fill=NAVY)
    d.text((196,133),post.get('category','법률정보'),font=font(24,False),fill=BLUE)

    title=clean_title(post.get('title',''))
    tf, lines = fit_title(d,title,860,4)
    line_h=int(tf.size*1.38) if hasattr(tf,'size') else 78
    total_h=line_h*len(lines)
    sy=max(265, 505-total_h//2)
    for i,line in enumerate(lines):
        bbox=d.textbbox((0,0),line,font=tf)
        tw=bbox[2]-bbox[0]
        d.text(((SIZE-tw)//2,sy+i*line_h),line,font=tf,fill=INK)

    # divider and category icons
    d.rounded_rectangle((420,700,660,706),radius=3,fill='#DCEBF5')
    category_icons(d,post.get('category',''))

    # footer label only, no phone number
    footer='현재두 법무사 사무소 · 인천'
    ff=font(24,False)
    tw=d.textbbox((0,0),footer,font=ff)[2]
    d.text(((SIZE-tw)//2,1000),footer,font=ff,fill=MUTED)
    img.save(path,'PNG',optimize=True)

def patch_article(slug, thumb_path):
    p=ROOT/'posts'/f'{slug}.html'
    if not p.exists():
        return False
    s=p.read_text(encoding='utf-8')
    rel='/' + thumb_path.as_posix().lstrip('/')
    absu='https://www.deunggiro.kr' + rel
    changed=False
    if re.search(r'<meta\s+name=["\']dg-thumbnail["\']',s,re.I):
        ns=re.sub(r'<meta\s+name=["\']dg-thumbnail["\']\s+content=["\'][^"\']*["\']\s*/?>',f'<meta name="dg-thumbnail" content="{rel}">',s,flags=re.I)
        changed |= ns!=s; s=ns
    else:
        marker='<meta name="dg-summary"'
        idx=s.find(marker)
        if idx!=-1:
            end=s.find('>',idx)
            s=s[:end+1]+f'<meta name="dg-thumbnail" content="{rel}">'+s[end+1:]
            changed=True
    if re.search(r'<meta\s+property=["\']og:image["\']',s,re.I):
        ns=re.sub(r'<meta\s+property=["\']og:image["\']\s+content=["\'][^"\']*["\']\s*/?>',f'<meta property="og:image" content="{absu}">',s,flags=re.I)
        changed |= ns!=s; s=ns
    else:
        pos=s.lower().find('</head>')
        if pos!=-1:
            s=s[:pos]+f'<meta property="og:image" content="{absu}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{absu}">'+s[pos:]
            changed=True
    if changed:
        p.write_text(s,encoding='utf-8')
    return changed

def main():
    posts=json.loads(POSTS_JSON.read_text(encoding='utf-8'))
    changed_count=0
    for post in posts:
        slug=post.get('slug','').strip()
        if not slug:
            continue
        out=OUT_DIR/f'{slug}-thumbnail.png'
        create_thumbnail(post,out)
        rel=f'/assets/posts/{slug}-thumbnail.png'
        if post.get('thumbnail')!=rel:
            post['thumbnail']=rel
            changed_count += 1
        patch_article(slug, Path(rel))
    POSTS_JSON.write_text(json.dumps(posts,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'generated={len(posts)}, updated_json={changed_count}')

if __name__=='__main__':
    main()
