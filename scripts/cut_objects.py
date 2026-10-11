#!/usr/bin/env python3
"""Cut a ChatGPT object sheet (objects on plain white, no fixed grid) into sharp transparent PNGs.

Every object keeps its loose parts (sparkle dashes, flying leaves, jumping seeds, butterflies):
each shape goes to the grid cell its centre falls in. Nothing is redrawn:
the design stays as drawn, only upscaled (Real-ESRGAN anime, 4x) and cut out.

  python3 scripts/cut_objects.py SHEET OUT_DIR --grid 6x3 [--prefix s1] [--upscaled CACHE.png]
Output: OUT_DIR/<prefix>-NN.png (row by row, left to right) + OUT_DIR/<prefix>-contact.png
"""
import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
from import_item import regions, remove_white, tidy  # noqa: E402

S = 4  # find shapes on a 1/S size mask


def cut(img, cols, rows):
    """RGBA sheet laid out as a cols x rows grid -> list of RGBA objects in reading order.
    cols may be a list (objects per row) when rows hold different numbers of objects.
    Each drawn shape goes to the cell its centre falls in, so loose parts stay with their object."""
    W, H = img.size
    small = img.getchannel("A").resize((W // S, H // S)).point(lambda a: 255 if a > 32 else 0)
    ys0, xs0 = np.nonzero(np.asarray(small))
    x_lo, x_hi, y_lo, y_hi = xs0.min(), xs0.max() + 1, ys0.min(), ys0.max() + 1   # the grid spans the drawn area
    cells = {}
    for r in regions(np.asarray(small) > 0):
        ys, xs = np.nonzero(r)
        if not len(xs):
            continue
        rw = min(rows - 1, int((ys.mean() - y_lo) / (y_hi - y_lo) * rows))
        n = cols[rw] if isinstance(cols, list) else cols
        c = min(n - 1, int((xs.mean() - x_lo) / (x_hi - x_lo) * n))
        cells[(rw, c)] = cells[(rw, c)] | r if (rw, c) in cells else r
    alpha = img.getchannel("A")
    out = []
    for key in sorted(cells):
        m = Image.fromarray((cells[key] * 255).astype(np.uint8)).resize((W, H), Image.NEAREST)
        m = m.filter(ImageFilter.MaxFilter(2 * S + 1))  # the nearest-neighbour mask is blocky: keep soft edges
        pc = img.copy()
        pc.putalpha(ImageChops.multiply(alpha, m))
        pc = tidy(pc.crop(pc.getbbox()), speck=0)       # keep every sparkle: only fill pinholes
        out.append(pc.crop(pc.getbbox()))
    return out, sorted(cells)


def contact(objs, path, prefix):
    n = len(objs)
    cols = 6
    o = Image.new("RGB", (cols * 260, ((n + cols - 1) // cols) * 260), (255, 255, 255))
    d = ImageDraw.Draw(o)
    for k, pc in enumerate(objs):
        t = pc.copy()
        t.thumbnail((230, 230), Image.LANCZOS)
        bg = Image.new("RGBA", (260, 260), (236, 232, 245, 255))
        bg.alpha_composite(t, ((260 - t.width) // 2, (260 - t.height) // 2 + 8))
        o.paste(bg.convert("RGB"), ((k % cols) * 260, (k // cols) * 260))
        d.text(((k % cols) * 260 + 6, (k // cols) * 260 + 4), f"{prefix}-{k + 1:02d}  {pc.width}x{pc.height}", fill=(0, 0, 0))
    o.save(path)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sheet", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--grid", required=True, help="columns x rows, e.g. 6x3, or objects per row, e.g. 5,4,4")
    ap.add_argument("--prefix", default="item")
    ap.add_argument("--upscaled", type=Path, help="the sheet already upscaled (skips Real-ESRGAN)")
    ap.add_argument("--tolerance", type=int, default=14)
    a = ap.parse_args()
    if a.upscaled and a.upscaled.exists():
        big = Image.open(a.upscaled).convert("RGB")
    else:
        import upscale
        big = upscale.upscale(Image.open(a.sheet).convert("RGB"), 4)
        if a.upscaled:
            big.save(a.upscaled)
    if "," in a.grid:
        cols = [int(v) for v in a.grid.split(",")]
        rows = len(cols)
    else:
        cols, rows = (int(v) for v in a.grid.lower().split("x"))
    objs, cells = cut(remove_white(big, a.tolerance), cols, rows)
    a.out.mkdir(parents=True, exist_ok=True)
    for k, pc in enumerate(objs):
        pc.save(a.out / f"{a.prefix}-{k + 1:02d}.png", optimize=True)
    contact(objs, a.out / f"{a.prefix}-contact.png", a.prefix)
    print(a.sheet.name, len(objs), "objects")


if __name__ == "__main__":
    main()
