#!/usr/bin/env python3
"""Import a Tủ đồ image made by hand in ChatGPT (no API key needed).

Removes a plain white background (flood fill from the edges, so white inside
the item stays), trims, and saves assets/closet/gen/<id>-v<n>.png, logged in
items.json like an API run.

Example:
  python3 scripts/import_item.py mu-la ~/Downloads/ChatGPT\\ Image.png
"""
import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_prompts import CLOSET, ROOT  # noqa: E402
from gen_closet import OUT, log_run, next_version  # noqa: E402


def remove_white(img, tolerance):
    img = img.convert("RGBA")
    if img.getextrema()[3][0] < 255:  # already has transparency
        return img
    rgb = img.convert("RGB")
    # mark the background magenta by flooding from every edge pixel that is near white
    key = (255, 0, 255)
    w, h = rgb.size
    edge = [(x, y) for x in range(0, w, 8) for y in (0, h - 1)] + [(x, y) for y in range(0, h, 8) for x in (0, w - 1)]
    for xy in edge:
        if min(rgb.getpixel(xy)) >= 255 - tolerance:
            ImageDraw.floodfill(rgb, xy, key, thresh=tolerance)
    mask = Image.new("L", (w, h), 255)
    px, mp = rgb.load(), mask.load()
    for y in range(h):
        for x in range(w):
            if px[x, y] == key:
                mp[x, y] = 0
    img.putalpha(mask)
    return img


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("id")
    ap.add_argument("image", type=Path)
    ap.add_argument("--tolerance", type=int, default=24, help="how far from pure white still counts as background")
    args = ap.parse_args()

    if args.id not in {i["id"] for i in CLOSET["items"]}:
        sys.exit(f"unknown id: {args.id} (see gen_closet.py --list)")
    img = remove_white(Image.open(args.image), args.tolerance)
    img = img.crop(img.getbbox())

    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{args.id}-v{next_version(args.id)}.png"
    img.save(path)
    rel = str(path.relative_to(ROOT))
    log_run(args.id, [rel], "chatgpt (manual)")
    print(rel)


if __name__ == "__main__":
    main()
