from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import import_naver_blog as base
import import_naver_blog_full as full

MAX_IMPORT = 3


def main():
    posts = base.load_posts()
    existing_log_nos, existing_sources, _ = full._existing_state()
    items = full.fetch_all_blog_items_robust()

    added = 0
    checked = 0
    for item in items:
        if added >= MAX_IMPORT:
            break

        n = item.get('log_no') or full._log_no(item.get('link', ''))
        if not n:
            continue
        checked += 1

        source_url = base.canonical_blog_url(n)
        slug = f'naver-{n}'
        path = base.POSTS_DIR / f'{slug}.html'

        # 중복 판단은 제목이 아니라 네이버 글 고유번호와 source_url로만 한다.
        if n in existing_log_nos or source_url in existing_sources:
            continue
        if path.exists():
            existing_log_nos.add(n)
            existing_sources.add(source_url)
            continue

        title = str(item.get('title') or '').strip()
        if len(title) < 2:
            print(f'IMPORT_SKIP_NO_TITLE {n}', flush=True)
            continue

        try:
            body, text = base.clean_article(source_url, slug)
        except Exception as e:
            print(f'IMPORT_SKIP_FETCH {n} {e}', flush=True)
            continue
        if not body.strip():
            print(f'IMPORT_SKIP_EMPTY {n}', flush=True)
            continue

        today = datetime.now().strftime('%Y-%m-%d')
        post = {
            'slug': slug,
            'title': title,
            'summary': base.summary_from(text, title),
            'category': base.infer_category(title),
            'date': today,
            'source': 'naver-blog',
            'source_url': source_url,
            'website_date': today,
        }

        base.POSTS_DIR.mkdir(parents=True, exist_ok=True)
        path.write_text(base.build_html(post, body), encoding='utf-8')
        posts.insert(0, post)
        existing_log_nos.add(n)
        existing_sources.add(source_url)
        added += 1
        print(f'IMPORTED_NEW {n} {title[:100]}', flush=True)

    base.POSTS_JSON.write_text(
        json.dumps(posts, ensure_ascii=False, indent=2),
        encoding='utf-8',
    )
    print(f'IMPORT_SCAN checked={checked} imported={added}', flush=True)
    print('IMPORTED', added, flush=True)


if __name__ == '__main__':
    main()
