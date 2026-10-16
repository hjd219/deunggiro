#!/usr/bin/env python3
"""Notify Naver IndexNow only about newly published legal post URLs.

Used after a successful GitHub Pages source push; does not rewrite pages.
IndexNow requests do not guarantee crawling or indexing.
"""
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "www.deunggiro.kr"
KEY = "990e9e4644dbc0b8f18028d2913bba5f"
KEY_FILE = ROOT / f"{KEY}.txt"
ENDPOINT = "https://searchadvisor.naver.com/indexnow"


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: ping_naver_indexnow.py /path/to/new-post-paths.txt")
    manifest = Path(sys.argv[1])
    if not manifest.exists():
        print("INDEXNOW_SKIP missing newly-imported-posts manifest")
        return 0
    if not KEY_FILE.is_file() or KEY_FILE.read_text(encoding="utf-8").strip() != KEY:
        raise SystemExit("IndexNow verification key file is missing or incorrect")

    slugs = set()
    for raw in manifest.read_text(encoding="utf-8").splitlines():
        path = raw.strip()
        if re.fullmatch(r"posts/[a-zA-Z0-9_-]+\.html", path):
            if (ROOT / path).is_file():
                slugs.add(path)
    if not slugs:
        print("INDEXNOW_SKIP no newly imported legal articles")
        return 0

    urls = [f"https://{DOMAIN}/{path}" for path in sorted(slugs)]

    # GitHub Pages deployment is asynchronous after the Git push. Do not
    # notify Naver until at least the first new page is publicly reachable.
    # A URL reported before deployment could still return HTTP 404.
    first_url = urls[0]
    deployed = False
    for attempt in range(9):
        try:
            check = urllib.request.Request(
                first_url,
                headers={"Cache-Control": "no-cache", "User-Agent": "Deunggiro-PublicationCheck/1.0"},
                method="HEAD",
            )
            with urllib.request.urlopen(check, timeout=8) as response:
                deployed = response.status == 200
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError):
            deployed = False
        if deployed:
            break
        if attempt < 8:
            time.sleep(10)
    if not deployed:
        print(f"INDEXNOW_SKIP new page not publicly deployed yet: {first_url}")
        return 1

    data = json.dumps({
        "host": DOMAIN,
        "key": KEY,
        "keyLocation": f"https://{DOMAIN}/{KEY}.txt",
        "urlList": urls,
    }).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "Deunggiro-IndexNow/1.0"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            code = response.status
        print(f"INDEXNOW_SENT urls={len(urls)} http={code}; indexing not guaranteed")
        return 0 if code in (200, 202) else 1
    except urllib.error.HTTPError as exc:
        print(f"INDEXNOW_FAILED http={exc.code} urls={len(urls)}")
        return 1
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        print(f"INDEXNOW_FAILED transport={type(exc).__name__} urls={len(urls)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
