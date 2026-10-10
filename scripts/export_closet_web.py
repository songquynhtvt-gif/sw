#!/usr/bin/env python3
"""Export the layers for the Tủ đồ try-on web page (docs/tu-do-thu-do/).

Every layer shares one frame, so the page only stacks them (same order as fit_preview.dress):
  body | body-noears → item shadows → neck item → head-front (if a neck item) → head item →
  ears-front (if the hat's ears are "front") → hand item (with the holding paw baked in)
Writes layers/*.webp, thumbs/*.webp and items.json next to the page.
"""
import json
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fit_preview as fp  # noqa: E402

OUT = fp.ROOT / "docs/tu-do-thu-do"
SLOT_VI = {"head": "Đầu", "neck": "Cổ", "hand": "Tay"}


def main():
    anchors, base, W, H, pad, canvas = fp.setup("huhu")
    geo = anchors["layers"]
    masks = fp.part_masks(geo, W, H, pad, canvas)
    noears = fp.ears_off(base, geo, W, H, pad)

    layers = {"body": base, "body-noears": noears,
              "head-front": fp.cut(base, masks["head"]), "ears-front": fp.cut(base, masks["ears"])}
    items = []
    for it in fp.CLOSET["items"]:
        src = fp.item_file(it["id"])
        if it["slot"] not in fp.LAYER or not src:
            continue
        tw = it.get("fit", {})
        layer = fp.place(Image.open(src).convert("RGBA"), it["slot"], anchors[it["slot"]], tw, W, H, pad, canvas)
        covered = it["slot"] == "head" and tw.get("ears", "front") == "covered"
        if it["slot"] == "hand":
            a = anchors["hand"]
            layer.alpha_composite(fp.paw(canvas, (a["x"] + tw.get("dx", 0)) * W + pad,
                                         (a["y"] + tw.get("dy", 0)) * H + pad - W * 0.05, W))
        layers[it["id"]] = layer
        layers[it["id"] + "-sh"] = fp.shadow([layer], noears if covered else base, H)
        items.append({"id": it["id"], "name": it["name"], "slot": it["slot"], "slotVi": SLOT_VI[it["slot"]],
                      "price": it["price"], "covered": covered, "thumb": src})

    box = None
    for img in layers.values():
        b = img.getbbox()
        if b:
            box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3]))
    for d in ("layers", "thumbs"):
        (OUT / d).mkdir(parents=True, exist_ok=True)
    scale = 900 / (box[3] - box[1])  # page canvas height
    size = (round((box[2] - box[0]) * scale), 900)
    for name, img in layers.items():
        img.crop(box).resize(size, Image.LANCZOS).save(OUT / "layers" / f"{name}.webp", quality=88, method=6)
    for e in items:
        t = Image.open(e.pop("thumb")).convert("RGBA")
        t = t.crop(t.getbbox())
        t.thumbnail((180, 180), Image.LANCZOS)
        t.save(OUT / "thumbs" / f"{e['id']}.webp", quality=88)
    outfits = [o for o in fp.CLOSET.get("outfits", []) if all(any(e["id"] == x for e in items) for x in o["ids"])]
    (OUT / "items.json").write_text(json.dumps({"size": size, "items": items, "outfits": outfits},
                                               ensure_ascii=False), encoding="utf-8")
    print(len(items), "items", size, "→", OUT.relative_to(fp.ROOT))


if __name__ == "__main__":
    main()
