import json, re
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import inject_internal_links as il
ROOT=Path(__file__).resolve().parents[1]
posts=json.loads((ROOT/'data/posts.json').read_text(encoding='utf-8'))
core=il.build_core_slugs(posts)
incoming={s:0 for s in core}
all_incoming={}
for p in posts:
    slug=str(p.get('slug','')).replace('.html','')
    path=ROOT/'posts'/f'{slug}.html'
    if not path.exists(): continue
    text=path.read_text(encoding='utf-8',errors='replace')
    m=re.search(r'<!-- SEO_RELATED_POSTS_START -->(.*?)<!-- SEO_RELATED_POSTS_END -->',text,re.S)
    if not m: continue
    for target in re.findall(r'href=["\\\']/posts/([^"\\\']+)\\.html',m.group(1)):
        all_incoming[target]=all_incoming.get(target,0)+1
        if target in incoming: incoming[target]+=1
meta={str(p.get('slug','')).replace('.html',''):p for p in posts}
rows=[]
for s,n in incoming.items():
    p=meta.get(s,{})
    rows.append({'slug':s,'category':p.get('category',''),'title':p.get('title',''),'incoming_related_links':n})
rows.sort(key=lambda x:(-x['incoming_related_links'],x['category'],x['title']))
summary={'core_count':len(core),'core_incoming_total':sum(incoming.values()),'core_zero':sum(1 for n in incoming.values() if n==0),'core_ge_10':sum(1 for n in incoming.values() if n>=10),'core_ge_5':sum(1 for n in incoming.values() if n>=5),'all_related_links':sum(all_incoming.values()),'rows':rows}
print(json.dumps(summary,ensure_ascii=False,indent=2))
