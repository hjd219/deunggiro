import json
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
POSTS_JSON = ROOT / 'data' / 'posts.json'


def main():
    posts = json.loads(POSTS_JSON.read_text(encoding='utf-8'))
    changed = 0
    missing = []

    for post in posts:
        slug = (post.get('slug') or '').replace('.html', '').strip()
        category = (post.get('category') or '').strip()
        if not slug or not category:
            continue

        file = ROOT / 'posts' / f'{slug}.html'
        if not file.exists():
            missing.append(slug)
            continue

        original = file.read_text(encoding='utf-8')
        soup = BeautifulSoup(original, 'html.parser')
        meta = soup.find('meta', attrs={'name': 'dg-category'})
        if meta is None:
            meta = soup.new_tag('meta')
            meta['name'] = 'dg-category'
            meta['content'] = category
            if soup.head:
                soup.head.append(meta)
        else:
            meta['content'] = category

        next_html = str(soup)
        if next_html != original:
            file.write_text(next_html, encoding='utf-8')
            changed += 1

    if missing:
        raise SystemExit('post html missing: ' + ', '.join(missing[:20]))

    print(f'category meta synchronized: {changed}/{len(posts)}')


if __name__ == '__main__':
    main()
