#!/usr/bin/env python3
"""Contact sheet of dress-up items on all three companions (one column per item), from the built
layers in docs/hu-hu-thay-do. Use it to check new items before publishing.

  python3 scripts/preview_dressup.py out.png mu-chin-tang-gio,tui-mai-ngoi [--h 230]
  python3 scripts/preview_dressup.py out.png all
"""
import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw

D = Path(__file__).resolve().parent.parent / "docs/hu-hu-thay-do"


def dressed(m, ids):
    by = {i["id"]: i for i in m["items"]}
    its = sorted((by[i] for i in ids if i in by), key=lambda i: i["z"])
    out = Image.new("RGBA", tuple(m["size"]), (232, 222, 200, 255))
    layer = lambda n: out.alpha_composite(Image.open(D / m["id"] / "layers" / f"{n}.webp").convert("RGBA"))
    for i in its:
        if i["z"] == 0:
            layer(i["id"])
    layer("body")
    for i in its:
        if i["z"] > 0:
            layer(i["id"] + "-sh")
    for i in its:
        if i["z"] > 0:
            layer(i["id"])
    layer("wisps")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("out", type=Path)
    ap.add_argument("ids", help="comma separated item ids (id+id wears them together), or 'all'")
    ap.add_argument("--h", type=int, default=230)
    a = ap.parse_args()
    data = json.loads((D / "data.json").read_text(encoding="utf-8"))
    mascots = data["mascots"]
    cols = ([[i["id"]] for i in mascots[0]["items"]] if a.ids == "all"
            else [c.split("+") for c in a.ids.split(",")])
    h = a.h
    cells = [[dressed(m, c) for c in cols] for m in mascots]
    cw = max(im.width * h // im.height for row in cells for im in row)
    o = Image.new("RGB", (cw * len(cols), h * len(mascots) + 14), (255, 255, 255))
    d = ImageDraw.Draw(o)
    for r, row in enumerate(cells):
        for c, im in enumerate(row):
            o.paste(im.resize((im.width * h // im.height, h)).convert("RGB"), (c * cw, 14 + r * h))
    for c, ids in enumerate(cols):
        d.text((c * cw + 3, 1), "+".join(ids)[:28], fill=(0, 0, 0))
    o.save(a.out)
    print(a.out, len(cols), "items x", len(mascots))


if __name__ == "__main__":
    main()
