from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, os

ROOT=Path(__file__).resolve().parents[1]
POSTS=ROOT/'data'/'posts.json'
FAV=ROOT/'favicon.png'
PRIMARY='#36a9e1'
INK='#20242b'
WHITE='#ffffff'

FONT_BOLD=[
 '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
 '/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc',
]

def font(size):
    for p in FONT_BOLD:
        if os.path.exists(p): return ImageFont.truetype(p,size=size,index=0)
    return ImageFont.load_default()

def main():
    if not FAV.exists() or not POSTS.exists(): return
    posts=json.loads(POSTS.read_text(encoding='utf-8'))
    fav=Image.open(FAV).convert('RGBA')
    fav.thumbnail((112,112),Image.Resampling.LANCZOS)
    for p in posts:
        thumb=ROOT/str(p.get('thumbnail','')).lstrip('/')
        if not thumb.exists(): continue
        im=Image.open(thumb).convert('RGBA')
        d=ImageDraw.Draw(im)
        # 기존 가짜 D 로고 영역을 지우고 실제 favicon을 그대로 배치
        d.rounded_rectangle((48,48,470,195),radius=18,fill=WHITE)
        x=66+(112-fav.width)//2
        y=66+(112-fav.height)//2
        im.alpha_composite(fav,(x,y))
        d=ImageDraw.Draw(im)
        d.text((196,70),'등기로',font=font(48),fill=PRIMARY)
        d.text((198,132),p.get('category') or '법률정보',font=font(25),fill=INK)
        im.convert('RGB').save(thumb,'PNG',optimize=True)
    print('real favicon applied to thumbnail headers:',len(posts))

if __name__=='__main__': main()
