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

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_prompts import CLOSET, ROOT  # noqa: E402
from gen_closet import OUT, log_run, next_version  # noqa: E402


CLOSET_BY_ID = {i["id"]: i for i in CLOSET["items"]}


def keeps_shadow(item):
    """Navy / indigo items: shadow removal would eat their own edge, so leave them alone."""
    return any(w in item["colours"].lower() for w in ("navy", "indigo"))


def remove_white(img, tolerance):
    """Plain white background -> transparent, with soft de-matted edges (no white fringe)."""
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
    bg = np.all(np.asarray(rgb) == key, axis=2)
    bg |= enclosed_holes(rgb, bg, tolerance)

    src = np.asarray(img.convert("RGB")).astype(np.float32)
    return Image.fromarray(dematte(src, ~bg), "RGBA")


def enclosed_holes(rgb, bg, tolerance, strict=8, min_share=0.0008):
    """Big white areas the edge flood cannot reach: inside a handle, a necklace, a ring.

    A hole starts from a pure-white pixel (within `strict` of 255) and spreads like the
    background (within `tolerance`); only regions larger than `min_share` of the image count,
    so white flower centres, sesame seeds and highlights stay.
    """
    work = rgb.copy()
    arr = np.asarray(work)
    white = (arr.min(axis=2) >= 255 - strict) & ~bg
    holes = np.zeros(bg.shape, bool)
    min_area = min_share * bg.size
    tmp = (1, 2, 3)
    ys, xs = np.nonzero(white[::6, ::6])
    for y, x in zip(ys * 6, xs * 6):
        if work.getpixel((int(x), int(y))) in (tmp, (4, 5, 6), (7, 8, 9)):
            continue
        ImageDraw.floodfill(work, (int(x), int(y)), tmp, thresh=tolerance)
        region = np.all(np.asarray(work) == tmp, axis=2)
        mark = (7, 8, 9) if region.sum() >= min_area else (4, 5, 6)
        if mark == (7, 8, 9):
            holes |= region
        ImageDraw.floodfill(work, (int(x), int(y)), mark, thresh=0)
    return holes


def grow(mask, px=1):
    """Binary dilation by px pixels."""
    m = Image.fromarray(mask.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(2 * px + 1))
    return np.asarray(m) > 0


def interior_colour(src, solid, band):
    """For each band pixel, the colour of a solid pixel 3 px further inside (8 directions)."""
    out = np.full_like(src, 255.0)
    found = np.zeros(band.shape, bool)
    for dx, dy in ((3, 0), (-3, 0), (0, 3), (0, -3), (3, 3), (-3, -3), (3, -3), (-3, 3)):
        s_src = np.roll(src, (dy, dx), axis=(0, 1))
        s_ok = np.roll(solid, (dy, dx), axis=(0, 1))
        take = band & ~found & s_ok
        out[take] = s_src[take]
        found |= take
    return out


def dematte(src, item):
    """RGBA array: item pixels opaque, the 2 px edge band un-blended from white (no white fringe)."""
    alpha = np.where(item, 255.0, 0.0)
    band = item & grow(~item, 2)
    solid = item & ~band
    inner = interior_colour(src, solid, band)
    # pixel = a * inner + (1 - a) * white  ->  a from the channel with the most contrast to white
    room = 255.0 - inner
    a = np.where(room.max(axis=2) > 30,
                 ((255.0 - src) * (room > 30)).max(axis=2) / np.maximum(room.max(axis=2), 1),
                 1.0)  # cream on white cannot be separated: keep it opaque
    a = np.clip(a, 0.0, 1.0)
    alpha[band] = a[band] * 255.0
    safe = np.maximum(a, 1e-3)[..., None]
    unblended = np.clip(255.0 - (255.0 - src) / safe, 0, 255)
    src = src.copy()
    src[band] = unblended[band]
    return np.dstack([src, alpha]).astype(np.uint8)


def strip_shadow(img):
    """Remove a flat blue offset shadow (ChatGPT sticker look) that touches the transparent outside.

    Grows from the outside through blue pixels only, so blue inside the item survives. Do not use
    on navy / indigo items: their own edge would be eaten.
    """
    arr = np.asarray(img).astype(np.float32)
    r, g, b, a = arr[..., 0], arr[..., 1], arr[..., 2], arr[..., 3]
    blue = (b > r + 45) & (b > g + 30) & (b > 90) & (a > 0)
    outside = a < 128
    region = np.zeros(blue.shape, bool)
    for _ in range(200):
        nxt = blue & grow(outside | region)
        if (nxt == region).all():
            break
        region = nxt
    # shadow pockets with no white around them (under a hat brim, inside a ring): the shadow's own
    # colour is a strong navy-blue with little red, which violet (#8A6BE0) and turquoise are not
    region |= (r < 90) & (b > r + 80) & (b > g + 50) & (a > 0)
    region |= grow(region, 1) & (b > r + 20) & (a > 0)  # blended blue fringe
    item = (a >= 128) & ~region
    return Image.fromarray(dematte(arr[..., :3], item), "RGBA")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("id")
    ap.add_argument("image", type=Path)
    ap.add_argument("--tolerance", type=int, default=24, help="how far from pure white still counts as background")
    args = ap.parse_args()

    if args.id not in {i["id"] for i in CLOSET["items"]}:
        sys.exit(f"unknown id: {args.id} (see gen_closet.py --list)")
    img = remove_white(Image.open(args.image), args.tolerance)
    if not keeps_shadow(CLOSET_BY_ID[args.id]):
        img = strip_shadow(img)
    img = img.crop(img.getbbox())

    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{args.id}-v{next_version(args.id)}.png"
    img.save(path)
    rel = str(path.relative_to(ROOT))
    log_run(args.id, [rel], "chatgpt (manual)")
    print(rel)


if __name__ == "__main__":
    main()
