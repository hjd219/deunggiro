import json, os, re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
POSTS_JSON = ROOT / 'data' / 'posts.json'
OUT_DIR = ROOT / 'assets' / 'posts'
OUT_DIR.mkdir(parents=True, exist_ok=True)
SIZE = 1080
SKY = '#7FD1FF'
BLUE = '#168BD8'
BLUE_DARK = '#2457A6'
NAVY = '#173B6B'
INK = '#20344A'
WHITE = '#FFFFFF'
BG = '#FFFFFF'
SOFT = '#F5FBFF'
MUTED = '#6F8190'

FONT_BOLD = [
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
    '/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc',
]
FONT_REG = [
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
]

def font(size, bold=True):
    for p in (FONT_BOLD if bold else FONT_REG):
        if os.path.exists(p):
            return ImageFont.truetype(p, size=size, index=0)
    return ImageFont.load_default()

def clean_title(title):
    t = re.sub(r'^\s*\[[^\]]+\]\s*', '', title or '').strip()
    t = re.sub(r'\s*\|\s*', ' · ', t)
    t = re.sub(r'\s+', ' ', t)
    return t

def short_title(title):
    t = clean_title(title)
    t = re.sub(r'\s*(총정리|완벽정리|한눈에 정리)\s*$', '', t)
    parts = re.split(r'\s*[·,]\s*', t)
    if len(t) > 34 and len(parts) > 1:
        t = ' · '.join(parts[:2])
    return t[:54].strip()

def pick_point(title):
    rules = [
        ('상속순위', '상속순위'), ('대습상속', '대습상속'), ('3개월', '3개월'),
        ('임기만료', '임기만료'), ('본점이전', '본점이전'), ('본점 이전', '본점 이전'),
        ('상속재산', '상속재산'), ('예금', '예금'), ('보험금', '보험금'),
        ('주주전원', '주주전원'), ('서면결의', '서면결의'), ('대표이사', '대표이사'),
        ('상속포기', '상속포기'), ('한정승인', '한정승인'), ('상속등기', '상속등기'),
        ('취득세', '취득세'), ('증자', '증자'), ('상호변경', '상호변경'),
        ('목적변경', '목적변경'), ('재산분할', '재산분할'), ('근저당', '근저당')
    ]
    for needle, label in rules:
        if needle in title:
            return label
    return ''

def wrap_text(draw, text, f, max_width, max_lines=3):
    words = re.split(r'(\s+|·|,|\?|!)', text)
    lines, cur = [], ''
    for token in words:
        if not token:
            continue
        test = cur + token
        if cur and draw.textbbox((0,0), test, font=f)[2] > max_width:
            lines.append(cur.strip(' ·,'))
            cur = token.lstrip()
        else:
            cur = test
    if cur.strip(): lines.append(cur.strip(' ·,'))
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip(' ·,') + '…'
    return lines

def fit_title(draw, text, max_width, max_lines=3):
    for size in range(76, 48, -2):
        f = font(size, True)
        lines = wrap_text(draw, text, f, max_width, max_lines)
        if len(lines) <= max_lines and all(draw.textbbox((0,0), line, font=f)[2] <= max_width for line in lines):
            return f, lines
    f = font(48, True)
    return f, wrap_text(draw, text, f, max_width, max_lines)

def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(tuple(int(v) for v in box), radius=int(radius), fill=fill, outline=outline, width=int(width))

def draw_logo(draw, category):
    # 현재 적용한 D 원형 로고 형태 + 등기로 + 업무분야
    draw.ellipse((66,66,174,174), fill=BLUE)
    df = font(68, True)
    db = draw.textbbox((0,0),'D',font=df)
    draw.text((120-(db[2]-db[0])/2, 111-(db[3]-db[1])/2-4),'D',font=df,fill=WHITE)
    draw.text((196,76),'등기로',font=font(42,True),fill=NAVY)
    cat = category or '법률정보'
    draw.text((198,130),cat,font=font(24,True),fill=BLUE)

def icon_shadow(draw, box, radius=24):
    x1,y1,x2,y2 = box
    rounded(draw,(x1+14,y1+18,x2+14,y2+18),radius,'#DCECF7')

def draw_hourglass(d,x,y):
    icon_shadow(d,(x,y,x+180,y+180),32)
    rounded(d,(x+20,y+8,x+160,y+35),13,BLUE_DARK)
    rounded(d,(x+20,y+145,x+160,y+172),13,BLUE_DARK)
    d.polygon([(x+45,y+35),(x+135,y+35),(x+104,y+86),(x+135,y+145),(x+45,y+145),(x+76,y+86)],fill='#DFF3FF')
    d.polygon([(x+63,y+48),(x+117,y+48),(x+92,y+85),(x+88,y+85)],fill=SKY)
    d.polygon([(x+67,y+132),(x+113,y+132),(x+92,y+98),(x+88,y+98)],fill=BLUE)

def draw_calendar(d,x,y):
    icon_shadow(d,(x,y,x+180,y+180),30)
    rounded(d,(x,y+12,x+180,y+172),28,SOFT,'#BDE4FA',4)
    rounded(d,(x,y+12,x+180,y+60),28,BLUE)
    for xx in (x+48,x+132): rounded(d,(xx-8,y,xx+8,y+34),8,NAVY)
    for r in range(2):
        for c in range(3):
            rounded(d,(x+34+c*45,y+83+r*39,x+56+c*45,y+105+r*39),6,SKY if (r+c)%2==0 else '#CFEAF8')

def draw_pin(d,x,y):
    icon_shadow(d,(x+10,y,x+170,y+180),40)
    d.ellipse((x+28,y+4,x+152,y+128),fill=BLUE)
    d.polygon([(x+48,y+93),(x+90,y+180),(x+132,y+93)],fill=BLUE)
    d.ellipse((x+66,y+42,x+114,y+90),fill=WHITE)

def draw_search(d,x,y):
    icon_shadow(d,(x,y,x+150,y+150),40)
    d.ellipse((x+8,y+8,x+120,y+120),fill=SOFT,outline=BLUE,width=18)
    d.line((x+105,y+108,x+170,y+170),fill=NAVY,width=24)
    d.ellipse((x+45,y+42,x+78,y+75),fill=SKY)

def draw_bank(d,x,y):
    icon_shadow(d,(x,y+15,x+190,y+170),24)
    d.polygon([(x+10,y+62),(x+95,y+5),(x+180,y+62)],fill=BLUE)
    rounded(d,(x+8,y+62,x+182,y+82),8,BLUE_DARK)
    for i in range(4): rounded(d,(x+24+i*42,y+80,x+49+i*42,y+145),7,'#DFF3FF',BLUE,2)
    rounded(d,(x+3,y+145,x+187,y+170),8,NAVY)

def draw_ballot(d,x,y):
    icon_shadow(d,(x+10,y+40,x+180,y+170),24)
    rounded(d,(x+12,y+62,x+178,y+172),24,BLUE)
    rounded(d,(x+45,y+82,x+145,y+97),7,WHITE)
    rounded(d,(x+52,y+4,x+142,y+105),14,WHITE,'#B8DEF6',4)
    d.line((x+75,y+53,x+91,y+69),fill=BLUE,width=9)
    d.line((x+91,y+69,x+121,y+35),fill=BLUE,width=9)

def draw_person(d,x,y):
    icon_shadow(d,(x+20,y,x+165,y+180),36)
    d.ellipse((x+58,y+4,x+132,y+78),fill='#A7E2FF')
    rounded(d,(x+34,y+75,x+156,y+176),42,BLUE)
    rounded(d,(x+73,y+96,x+117,y+145),8,WHITE)
    d.polygon([(x+86,y+100),(x+108,y+100),(x+100,y+130),(x+94,y+130)],fill=NAVY)

def draw_ladder(d,x,y):
    icon_shadow(d,(x+20,y,x+165,y+180),24)
    d.line((x+45,y+8,x+45,y+172),fill=BLUE_DARK,width=20)
    d.line((x+145,y+8,x+145,y+172),fill=BLUE_DARK,width=20)
    for yy in (35,75,115,155): d.line((x+48,y+yy,x+142,y+yy),fill=SKY,width=18)

def draw_house(d,x,y):
    icon_shadow(d,(x,y+20,x+190,y+175),26)
    d.polygon([(x+8,y+76),(x+95,y+8),(x+182,y+76)],fill=BLUE)
    rounded(d,(x+28,y+70,x+162,y+172),20,'#DFF3FF','#B6DFF7',3)
    rounded(d,(x+78,y+105,x+116,y+172),8,WHITE)

def draw_building(d,x,y):
    icon_shadow(d,(x+15,y,x+170,y+180),24)
    rounded(d,(x+20,y+5,x+168,y+178),22,BLUE)
    for r in range(4):
        for c in range(2): rounded(d,(x+48+c*55,y+30+r*34,x+74+c*55,y+48+r*34),5,WHITE)
    rounded(d,(x+80,y+142,x+112,y+178),6,WHITE)

def draw_shield(d,x,y):
    icon_shadow(d,(x+12,y,x+178,y+180),32)
    d.polygon([(x+95,y+4),(x+174,y+34),(x+158,y+128),(x+95,y+180),(x+32,y+128),(x+16,y+34)],fill=BLUE)
    d.line((x+58,y+90,x+84,y+116),fill=WHITE,width=16)
    d.line((x+84,y+116,x+132,y+62),fill=WHITE,width=16)

def pick_icon(title, category):
    t = title
    if any(k in t for k in ['상속순위','대습상속','상속인 순위']): return 'ladder'
    if any(k in t for k in ['3개월','기간','기한']): return 'hourglass'
    if any(k in t for k in ['임기','임기만료','날짜']): return 'calendar'
    if any(k in t for k in ['본점이전','본점 이전','주소변경','주소 변경']): return 'pin'
    if any(k in t for k in ['조회','찾기','확인']): return 'search'
    if any(k in t for k in ['예금','보험금','금융','퇴직금','주식']): return 'bank'
    if any(k in t for k in ['주주','서면결의','주주총회']): return 'ballot'
    if any(k in t for k in ['대표이사','임원','감사','이사']): return 'person'
    if category == '법인등기': return 'building'
    if category == '상속포기·한정승인': return 'shield'
    return 'house'

def draw_icon(d, kind, x=445, y=755):
    funcs={'ladder':draw_ladder,'hourglass':draw_hourglass,'calendar':draw_calendar,'pin':draw_pin,'search':draw_search,'bank':draw_bank,'ballot':draw_ballot,'person':draw_person,'house':draw_house,'building':draw_building,'shield':draw_shield}
    funcs.get(kind,draw_house)(d,x,y)

def draw_highlighted_line(d, line, f, y, point):
    total = d.textbbox((0,0),line,font=f)[2]
    x = (SIZE-total)//2
    if point and point in line:
        before, after = line.split(point,1)
        d.text((x,y),before,font=f,fill=INK)
        bw=d.textbbox((0,0),before,font=f)[2]
        d.text((x+bw,y),point,font=f,fill=BLUE)
        pw=d.textbbox((0,0),point,font=f)[2]
        d.text((x+bw+pw,y),after,font=f,fill=INK)
    else:
        d.text((x,y),line,font=f,fill=INK)

def create_thumbnail(post, path):
    img=Image.new('RGB',(SIZE,SIZE),BG)
    d=ImageDraw.Draw(img)
    rounded(d,(18,18,SIZE-18,SIZE-18),34,WHITE,SKY,12)
    draw_logo(d,post.get('category',''))

    title=short_title(post.get('title',''))
    point=pick_point(title)
    tf,lines=fit_title(d,title,860,3)
    line_h=int(tf.size*1.38) if hasattr(tf,'size') else 76
    total_h=line_h*len(lines)
    sy=max(300, 515-total_h//2)
    for i,line in enumerate(lines):
        draw_highlighted_line(d,line,tf,sy+i*line_h,point)

    draw_icon(d,pick_icon(title,post.get('category','')),445,755)
    img.save(path,'PNG',optimize=True)

def patch_article(slug, thumb_path):
    p=ROOT/'posts'/f'{slug}.html'
    if not p.exists(): return False
    s=p.read_text(encoding='utf-8')
    rel='/' + thumb_path.as_posix().lstrip('/')
    absu='https://www.deunggiro.kr'+rel
    changed=False
    if re.search(r'<meta\s+name=["\']dg-thumbnail["\']',s,re.I):
        ns=re.sub(r'<meta\s+name=["\']dg-thumbnail["\']\s+content=["\'][^"\']*["\']\s*/?>',f'<meta name="dg-thumbnail" content="{rel}">',s,flags=re.I); changed|=ns!=s; s=ns
    else:
        pos=s.lower().find('</head>')
        if pos!=-1: s=s[:pos]+f'<meta name="dg-thumbnail" content="{rel}">\n'+s[pos:]; changed=True
    if re.search(r'<meta\s+property=["\']og:image["\']',s,re.I):
        ns=re.sub(r'<meta\s+property=["\']og:image["\']\s+content=["\'][^"\']*["\']\s*/?>',f'<meta property="og:image" content="{absu}">',s,flags=re.I); changed|=ns!=s; s=ns
    else:
        pos=s.lower().find('</head>')
        if pos!=-1: s=s[:pos]+f'<meta property="og:image" content="{absu}">\n<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:image" content="{absu}">\n'+s[pos:]; changed=True
    if changed: p.write_text(s,encoding='utf-8')
    return changed

def main():
    posts=json.loads(POSTS_JSON.read_text(encoding='utf-8'))
    for post in posts:
        slug=(post.get('slug') or '').strip()
        if not slug: continue
        out=OUT_DIR/f'{slug}-thumbnail.png'
        create_thumbnail(post,out)
        rel=f'/assets/posts/{slug}-thumbnail.png'
        post['thumbnail']=rel
        patch_article(slug,Path(rel))
    POSTS_JSON.write_text(json.dumps(posts,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('generated',len(posts),'thumbnails')

if __name__=='__main__': main()
