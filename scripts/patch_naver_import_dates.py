import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
POSTS_JSON = ROOT / 'data' / 'posts.json'
POSTS_DIR = ROOT / 'posts'
TODAY = datetime.now(ZoneInfo('Asia/Seoul')).strftime('%Y-%m-%d')


def patch_html(path: Path, date: str):
    if not path.exists():
        return
    s = path.read_text(encoding='utf-8')
    s = re.sub(
        r'(<meta\s+name=["\']dg-date["\']\s+content=["\'])[^"\']*(["\']\s*/?>)',
        rf'\g<1>{date}\g<2>',
        s,
        count=1,
        flags=re.I,
    )
    s = re.sub(
        r'(<div\s+class=["\']post-meta["\'][^>]*>\s*<span\s+class=["\']badge["\'][^>]*>.*?</span>\s*)\d{4}-\d{2}-\d{2}',
        rf'\g<1>{date}',
        s,
        count=1,
        flags=re.I | re.S,
    )
    path.write_text(s, encoding='utf-8')


def main():
    posts = json.loads(POSTS_JSON.read_text(encoding='utf-8'))
    changed = 0
    for post in posts:
        if post.get('source') != 'naver-blog':
            continue
        # 최초 홈페이지 수집일을 한 번만 기록하고 이후 재수집 때는 날짜를 유지한다.
        website_date = str(post.get('website_date') or '').strip()
        if not website_date:
            website_date = TODAY
            post['website_date'] = website_date
        if post.get('date') != website_date:
            post['date'] = website_date
            changed += 1
        slug = str(post.get('slug') or '').replace('.html', '')
        if slug:
            patch_html(POSTS_DIR / f'{slug}.html', website_date)

    POSTS_JSON.write_text(json.dumps(posts, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'naver website dates fixed: {changed}, today={TODAY}')


if __name__ == '__main__':
    main()
