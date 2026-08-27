from pathlib import Path
import re

VERSION='4'
CSS=f'<link rel="stylesheet" href="/assets/article-v2.css?v={VERSION}">'
JS=f'<script src="/assets/article-v2.js?v={VERSION}" defer></script>'


def inject_html(text: str) -> str:
    # 기존 버전이 있으면 v4로 교체하고, 없으면 새로 삽입
    text=re.sub(r'<link rel="stylesheet" href="/assets/article-v2\.css\?v=\d+">', CSS, text)
    text=re.sub(r'<script src="/assets/article-v2\.js\?v=\d+" defer></script>', JS, text)
    if '/assets/article-v2.css?' not in text:
        text=text.replace('</head>',CSS+'</head>',1)
    if '/assets/article-v2.js?' not in text:
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
    region=inject_html(region)
    new=text[:start]+region+text[end:]
    if new!=text:
        path.write_text(new,encoding='utf-8')
        print('updated admin.html')


if __name__=='__main__':
    update_posts()
    update_admin()
