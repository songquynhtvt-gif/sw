#!/usr/bin/env python3
"""Try Tủ đồ items on a companion: composite item PNGs onto a pose at its anchors.

Uses the approved file if there is one, else the newest gen file, unless --file is given.
Anchors live in prompts/closet/items.json -> "anchors".
Output: assets/closet/fit/<companion>-<ids>.png

Examples:
  python3 scripts/fit_preview.py --id mu-la
  python3 scripts/fit_preview.py --id mu-la khan-ran ong-nhom-tre     # full outfit
  python3 scripts/fit_preview.py --id mu-la --file assets/closet/gen/mu-la-v2.png
"""
import argparse
import json
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
CLOSET = json.loads((ROOT / "prompts/closet/items.json").read_text(encoding="utf-8"))
OUT = ROOT / "assets/closet/fit"
LAYER = {"hand": 0, "neck": 1, "head": 2}  # drawn back to front


def item_file(item_id):
    approved = ROOT / f"assets/closet/approved/{item_id}.png"
    if approved.exists():
        return approved
    gens = sorted((ROOT / "assets/closet/gen").glob(f"{item_id}-v*.png"),
                  key=lambda p: int(p.stem.rsplit("-v", 1)[1]))
    return gens[-1] if gens else None


def place(base, art, slot, anchor, tweak, W, H, pad):
    """Anchors are fractions of the pose (W x H); the canvas is padded by `pad` px."""
    art = art.crop(art.getbbox())  # trim transparent margin
    scale = tweak.get("scale", 1.0)
    if slot == "hand":
        h = anchor["h"] * H * scale
        w = art.width * h / art.height
    else:
        w = anchor["w"] * W * scale
        h = art.height * w / art.width
    art = art.resize((round(w), round(h)), Image.LANCZOS)
    x = (anchor["x"] + tweak.get("dx", 0)) * W - w / 2
    y = (anchor["y"] + tweak.get("dy", 0)) * H
    if slot != "neck":  # head and hand: anchor is the item's bottom edge
        y -= h
    base.alpha_composite(art, (round(x) + pad, round(y) + pad))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--id", nargs="+", required=True, help="item ids (one per slot)")
    ap.add_argument("--file", nargs="+", type=Path, help="explicit PNG per id, same order")
    ap.add_argument("--companion", default="huhu", choices=[k for k in CLOSET["anchors"] if not k.startswith("_")])
    args = ap.parse_args()

    by_id = {i["id"]: i for i in CLOSET["items"]}
    anchors = CLOSET["anchors"][args.companion]
    if args.file and len(args.file) != len(args.id):
        sys.exit("--file needs one path per --id")

    layers = []
    for n, item_id in enumerate(args.id):
        it = by_id.get(item_id)
        if not it or it["slot"] not in LAYER:
            sys.exit(f"{item_id}: unknown id or not wearable")
        path = (ROOT / args.file[n]) if args.file else item_file(item_id)
        if not path or not path.exists():
            sys.exit(f"{item_id}: no PNG yet (run gen_closet.py first)")
        layers.append((LAYER[it["slot"]], it, path))

    slots = [it["slot"] for _, it, _ in layers]
    if len(slots) != len(set(slots)):
        sys.exit("one item per slot")

    pose = Image.open(ROOT / anchors["pose"]).convert("RGBA")
    W, H = pose.size
    pad = H // 2  # room for tall hats and long hand items
    base = Image.new("RGBA", (W + 2 * pad, H + 2 * pad))
    base.alpha_composite(pose, (pad, pad))
    for _, it, path in sorted(layers, key=lambda layer: layer[0]):
        place(base, Image.open(path).convert("RGBA"), it["slot"], anchors[it["slot"]], it.get("fit", {}), W, H, pad)
    base = base.crop(base.getbbox())

    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / f"{args.companion}-{'+'.join(args.id)}.png"
    base.save(out)
    print(out.relative_to(ROOT))


if __name__ == "__main__":
    main()
