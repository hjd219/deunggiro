import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
posts=json.loads((ROOT/'data'/'posts.json').read_text(encoding='utf-8'))
changed=0
for post in posts:
    if post.get('source')!='naver-blog':continue
    slug=str(post.get('slug','')).replace('.html',''); p=ROOT/'posts'/f'{slug}.html'
    if not p.exists():continue
    s=p.read_text(encoding='utf-8'); n=s
    n=re.sub(r'<figure[^>]+id=["\']dg-post-hero-image["\'][^>]*>.*?</figure>','',n,flags=re.I|re.S)
    n=re.sub(r'<style[^>]+id=["\']dg-post-hero-style["\'][^>]*>.*?</style>','',n,flags=re.I|re.S)
    if n!=s:p.write_text(n,encoding='utf-8');changed+=1
print('stripped naver article hero',changed)
