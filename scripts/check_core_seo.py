#!/usr/bin/env python3
"""Read-only SEO regression check for Deunggiro's 19 priority pages.

No files are written; fail the import job if a core search landing page
loses its self-canonical, title/H1, structured data, or sitemap entry.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://www.deunggiro.kr"
PAGES = (
    "index.html",
    "inheritance.html",
    "inheritance-missing-heir.html",
    "inheritance-minor-heir.html",
    "inheritance-overseas-heir.html",
    "inheritance-substitute-succession.html",
    "inheritance-division.html",
    "renunciation.html",
    "renunciation-after-procedure.html",
    "renunciation-limited-acceptance-liquidation.html",
    "renunciation-deceased-deposit.html",
    "renunciation-death-insurance.html",
    "corporate.html",
    "realestate.html",
    "family.html",
    "posts.html",
    "acquisition-calculator.html",
    "corporate-calculator.html",
    "renunciation-calculator.html",
)

LINK_TAG = re.compile(r"<link\b[^>]*>", re.I)
META_TAG = re.compile(r"<meta\b[^>]*>", re.I)
LD_JSON = re.compile(
    r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>([\s\S]*?)</script>',
    re.I,
)


def attribute(tag: str, name: str) -> str:
    m = re.search(r"\b" + re.escape(name) + r'\s*=\s*["\']([^"\']*)["\']', tag, re.I)
    return m.group(1) if m else ""


def main() -> int:
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    problems = []
    for relative in PAGES:
        path = ROOT / relative
        if not path.is_file():
            problems.append(f"{relative}: missing file")
            continue
        html = path.read_text(encoding="utf-8")
        url = BASE + ("/" if relative == "index.html" else "/" + relative)
        canonicals = [
            attribute(tag.group(), "href")
            for tag in LINK_TAG.finditer(html)
            if attribute(tag.group(), "rel").lower() == "canonical"
        ]
        if canonicals != [url]:
            problems.append(f"{relative}: canonical incorrect or duplicated: {canonicals}")
        if len(re.findall(r"<title\b[^>]*>[^<]+</title>", html, re.I)) != 1:
            problems.append(f"{relative}: missing or duplicated title")
        if len(re.findall(r"<h1\b", html, re.I)) != 1:
            problems.append(f"{relative}: missing or duplicated H1")
        for tag in META_TAG.finditer(html):
            if attribute(tag.group(), "name").lower() == "robots":
                if "noindex" in attribute(tag.group(), "content").lower():
                    problems.append(f"{relative}: robots noindex")
        schemas = list(LD_JSON.finditer(html))
        if not schemas:
            problems.append(f"{relative}: JSON-LD missing")
        else:
            for i, tag in enumerate(schemas, start=1):
                try:
                    json.loads(tag.group(1))
                except json.JSONDecodeError as exc:
                    problems.append(f"{relative}: JSON-LD {i} invalid: {exc.msg}")
        if f"<loc>{url}</loc>" not in sitemap:
            problems.append(f"{relative}: missing from sitemap")

    print("CORE_SEO_CHECK", "pages", len(PAGES), "problems", len(problems))
    for issue in problems:
        print("CORE_SEO_ERROR", issue)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
