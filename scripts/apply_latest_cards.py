from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TOP=['index.html','inheritance.html','renunciation.html','corporate.html','realestate.html','family.html']
CSS='<link rel="stylesheet" href="/assets/latest-posts.css">'
JS='<script src="/assets/latest-posts.js" defer></script>'

def patch(path:Path):
    if not path.exists(): return False
    s=path.read_text(encoding='utf-8')
    old=s
    if '/assets/latest-posts.css' not in s:
        pos=s.lower().find('</head>')
        if pos!=-1: s=s[:pos]+CSS+'\n'+s[pos:]
    if '/assets/latest-posts.js' not in s:
        pos=s.lower().rfind('</body>')
        if pos!=-1: s=s[:pos]+JS+'\n'+s[pos:]
        else: s+=JS+'\n'
    if s!=old:
        path.write_text(s,encoding='utf-8')
        return True
    return False

def main():
    changed=[]
    for name in TOP:
        p=ROOT/name
        if patch(p): changed.append(name)
    posts=ROOT/'posts'
    if posts.exists():
        for p in posts.glob('*.html'):
            if patch(p): changed.append(str(p.relative_to(ROOT)))
    print('latest-card patched',len(changed),'files')

if __name__=='__main__': main()
