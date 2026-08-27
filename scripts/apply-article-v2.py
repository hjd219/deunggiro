from pathlib import Path

CSS='<link rel="stylesheet" href="/assets/article-v2.css?v=2">'
JS='<script src="/assets/article-v2.js?v=2" defer></script>'


def inject_html(text: str) -> str:
    if CSS not in text:
        text=text.replace('</head>',CSS+'</head>',1)
    if JS not in text:
        text=text.replace('</body>',JS+'</body>',1)
    return text


def update_posts():
    for path in sorted(Path('posts').glob('*.html')):
        old=path.read_text(encoding='utf-8')
        new=inject_html(old)
        if new!=old:
            path.write_text(new,encoding='utf-8')
            print('updated',path)


def update_admin():
    path=Path('admin.html')
    text=path.read_text(encoding='utf-8')
    start=text.find('function makeArticle(p,body){return `')
    if start<0:
        raise RuntimeError('makeArticle template not found')
    end=text.find('`;\n}',start)
    if end<0:
        raise RuntimeError('makeArticle template end not found')
    region=text[start:end]
    if CSS not in region:
        region=region.replace('</head><body>',CSS+'</head><body>',1)
    if JS not in region:
        pos=region.rfind('</body></html>')
        if pos<0:
            raise RuntimeError('article template closing tags not found')
        region=region[:pos]+JS+region[pos:]
    new=text[:start]+region+text[end:]
    if new!=text:
        path.write_text(new,encoding='utf-8')
        print('updated admin.html')


if __name__=='__main__':
    update_posts()
    update_admin()
