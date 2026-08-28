import json
import re
import subprocess
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
POSTS_JSON = ROOT / 'data' / 'posts.json'
POSTS_DIR = ROOT / 'posts'
TODAY = datetime.now(ZoneInfo('Asia/Seoul')).strftime('%Y-%m-%d')


def first_git_date(path: Path) -> str:
    """해당 상세페이지가 Git에 처음 추가된 날짜를 홈페이지 최초 작성일로 사용한다."""
    try:
        rel = path.relative_to(ROOT).as_posix()
        out = subprocess.check_output(
            [
                'git', 'log', '--diff-filter=A', '--format=%ad', '--date=short',
                '--reverse', '--', rel,
            ],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        if out:
            date = out.splitlines()[0].strip()
            if re.fullmatch(r'\d{4}-\d{2}-\d{2}', date):
                return date
    except Exception:
        pass
    return ''


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
    restored = 0

    for post in posts:
        if post.get('source') != 'naver-blog':
            continue

        slug = str(post.get('slug') or '').replace('.html', '')
        page = POSTS_DIR / f'{slug}.html' if slug else None

        # 기존 수집글은 Git 커밋 기록상 상세페이지가 최초 생성된 날짜를 복원한다.
        # 새로 수집되어 아직 커밋되지 않은 글은 오늘 날짜를 최초 작성일로 고정한다.
        git_date = first_git_date(page) if page else ''
        current_website_date = str(post.get('website_date') or '').strip()
        website_date = git_date or current_website_date or TODAY

        if git_date and current_website_date != git_date:
            restored += 1

        if post.get('website_date') != website_date:
            post['website_date'] = website_date
            changed += 1
        if post.get('date') != website_date:
            post['date'] = website_date
            changed += 1

        if page:
            patch_html(page, website_date)

    POSTS_JSON.write_text(json.dumps(posts, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'naver website dates fixed: changed={changed}, restored_from_git={restored}, today={TODAY}')


if __name__ == '__main__':
    main()
