#!/usr/bin/env python3
"""Build real 1:1 JPEG thumbnails for the six Naver ItemList carousels.
Original hero/OG images are untouched. Run once; idempotent.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote, urlparse
from PIL import Image, ImageOps, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
PAGES = (
    "index.html", "inheritance.html", "renunciation.html",
    "corporate.html", "realestate.html", "family.html",
)
IMAGE_URL_BASE = "https://www.deunggiro.kr/images/"
SCRIPT_RX = re.compile(
    r'(<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)',
    re.I | re.S,
)
IMAGE_RX = re.compile(r'("image"\s*:\s*")([^"]+)(")')
OUTPUT_SIZE = 1200


def make_thumbnail(source: Path, target: Path) -> None:
    with Image.open(source) as original:
        im = ImageOps.exif_transpose(original).convert("RGB")
        w, h = im.size
        if source.name == "og-home.jpg":
            # Preserve text and logo in the wide office-brand image.
            background = ImageOps.fit(im, (OUTPUT_SIZE, OUTPUT_SIZE),
                                      method=Image.Resampling.LANCZOS)
            background = background.filter(ImageFilter.GaussianBlur(36))
            foreground = im.copy()
            foreground.thumbnail((OUTPUT_SIZE, OUTPUT_SIZE),
                                 Image.Resampling.LANCZOS)
            background.paste(foreground,
                             ((OUTPUT_SIZE - foreground.width) // 2,
                              (OUTPUT_SIZE - foreground.height) // 2))
            square = background
        elif abs(w - h) <= max(w, h) * 0.02:
            square = im.resize((OUTPUT_SIZE, OUTPUT_SIZE),
                               Image.Resampling.LANCZOS)
        else:
            square = ImageOps.fit(im, (OUTPUT_SIZE, OUTPUT_SIZE),
                                  method=Image.Resampling.LANCZOS,
                                  centering=(0.5, 0.5))
        target.parent.mkdir(parents=True, exist_ok=True)
        square.save(target, format="JPEG", quality=87, optimize=True,
                    progressive=True, subsampling=0)
    with Image.open(target) as verified:
        assert verified.size == (OUTPUT_SIZE, OUTPUT_SIZE), target


def main() -> None:
    outputs = {}
    originals = set()
    for page in PAGES:
        source = (ROOT / page).read_text("utf-8")
        changed_scripts = 0

        def replace_script(match: re.Match) -> str:
            nonlocal changed_scripts
            prefix, script_text, suffix = match.groups()
            try:
                parsed = json.loads(script_text)
            except json.JSONDecodeError:
                return match.group(0)
            if parsed.get("@type") != "ItemList":
                return match.group(0)
            if len(parsed.get("itemListElement", [])) < 2:
                return match.group(0)

            def change_image(image_match: re.Match) -> str:
                begin, url, end = image_match.groups()
                if not url.startswith(IMAGE_URL_BASE):
                    return image_match.group(0)
                relative = unquote(url[len(IMAGE_URL_BASE):])
                if relative.endswith("-carousel-square.jpg"):
                    return image_match.group(0)
                original_path = ROOT / "images" / relative
                if not original_path.is_file():
                    raise FileNotFoundError(f"{page}: carousel image not found: {original_path}")
                if not original_path.resolve().is_relative_to((ROOT / "images").resolve()):
                    raise ValueError(f"Bad image path: {relative}")
                originals.add(relative)
                square_relative = original_path.stem + "-carousel-square.jpg"
                square_path = ROOT / "images" / square_relative
                if square_relative not in outputs:
                    make_thumbnail(original_path, square_path)
                    outputs[square_relative] = relative
                return begin + IMAGE_URL_BASE + square_relative + end

            updated, count = IMAGE_RX.subn(change_image, script_text)
            if count:
                json.loads(updated)
                changed_scripts += 1
            return prefix + updated + suffix

        replaced = SCRIPT_RX.sub(replace_script, source)
        if changed_scripts != 1:
            raise RuntimeError(f"{page}: expected exactly one ItemList, got {changed_scripts}")
        if replaced != source:
            (ROOT / page).write_text(replaced, encoding="utf-8")
        print(f"{page}: ItemList square images ready; HTML changed={replaced != source}")

    for square, original in sorted(outputs.items()):
        print(f"  images/{original}  => images/{square} (1200x1200)")
    print(f"Done: {len(outputs)} distinct square thumbnails, {len(PAGES)} carousel pages; originals unchanged")


if __name__ == "__main__":
    main()
