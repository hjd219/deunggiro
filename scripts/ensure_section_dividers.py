from __future__ import annotations
import json,re
from pathlib import Path
from bs4 import BeautifulSoup,Tag

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'/'posts.json'
POSTS=ROOT/'posts'
MAJOR_RE=re.compile(r'^(?:[1-9]\ufe0f?\u20e3|🔟)\s*')

def main():
    posts=json.loads(DATA.read_text(encoding='utf-8'))
    changed=0
    inserted=0
    for p in posts:
        if p.get('source')!='naver-blog':
            continue
        slug=str(p.get('slug','')).replace('.html','')
        path=POSTS/f'{slug}.html'
        if not path.exists():
            continue
        soup=BeautifulSoup(path.read_text(encoding='utf-8',errors='replace'),'html.parser')
        body=soup.select_one('.article-body')
        if body is None:
            continue
        file_changed=False
        for node in list(body.find_all(['p','h2','h3'],recursive=False)):
            text=' '.join(node.stripped_strings).strip()
            if not MAJOR_RE.match(text):
                continue
            prev=node.find_previous_sibling()
            while prev is not None and (not isinstance(prev,Tag) or not ' '.join(prev.stripped_strings).strip() and prev.name!='hr'):
                prev=prev.find_previous_sibling()
            if isinstance(prev,Tag) and prev.name=='hr':
                continue
            hr=soup.new_tag('hr')
            hr['class']=['article-divider','naver-divider']
            node.insert_before(hr)
            inserted+=1
            file_changed=True
        if file_changed:
            path.write_text(str(soup),encoding='utf-8')
            changed+=1
    print('SECTION_DIVIDERS_CHANGED',changed,'INSERTED',inserted)

if __name__=='__main__':
    main()
