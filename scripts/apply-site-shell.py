from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CSS='<link rel="stylesheet" href="/assets/site-shell.css">'
ANALYTICS='<script src="/assets/analytics.js" defer></script>'
JS='<script src="/assets/site-shell.js" defer></script>'
PUBLIC_ROOT=[
 'index.html','inheritance.html','renunciation.html','corporate.html','realestate.html','family.html',
 'posts.html','acquisition-calculator.html','corporate-calculator.html','divorce-calculator.html'
]

def inject(text:str)->str:
    if '/assets/site-shell.css' not in text:
        text=text.replace('</head>',CSS+'\n</head>',1)
    if '/assets/analytics.js' not in text:
        text=text.replace('</head>',ANALYTICS+'\n</head>',1)
    if '/assets/site-shell.js' not in text:
        text=text.replace('</body>',JS+'\n</body>',1)
    return text

def update_file(path:Path):
    if not path.exists(): return False
    old=path.read_text(encoding='utf-8')
    new=inject(old)
    if new!=old:
        path.write_text(new,encoding='utf-8')
        print('updated',path.relative_to(ROOT))
        return True
    return False

def update_admin_template():
    path=ROOT/'admin.html'
    text=path.read_text(encoding='utf-8')
    start=text.find('function makeArticle(p,body){return `')
    if start<0:
        print('makeArticle template not found; skipped admin template')
        return False
    end=text.find('`;\n}',start)
    if end<0:
        print('makeArticle template end not found; skipped admin template')
        return False
    region=text[start:end]
    new_region=inject(region)
    if new_region!=region:
        path.write_text(text[:start]+new_region+text[end:],encoding='utf-8')
        print('updated admin.html article template')
        return True
    return False

def main():
    for name in PUBLIC_ROOT:
        update_file(ROOT/name)
    for path in sorted((ROOT/'posts').glob('*.html')):
        update_file(path)
    update_admin_template()

if __name__=='__main__': main()
