#!/usr/bin/env python3
"""Build the Hǔhǔ dress-up page layers from the v3 object sheet (assets/closet/v3/items/NN.png).

Every item becomes one pose-framed layer with the body interaction baked in, so the page only
stacks layers by z (back < body < shadow < feet < shoulders < neck < head < hand):
  - rings (wreath, headbands) lose the part that sits behind the head top
  - small hats keep the ears in front (hat pixels over the ears are removed)
  - big hats ("covered") switch the body to the no-ears variant
  - neck / shoulder items are tucked under the chin (pixels over the head removed)
  - held items get a closed paw; gloves and boots are split per paw / foot
Output: docs/hu-hu-thay-do/{layers,thumbs}/*.webp + data.json
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fit_preview as fp  # noqa: E402

ITEMS = fp.ROOT / "assets/closet/v3/items"
OUT = fp.ROOT / "docs/hu-hu-thay-do"
Z = {"back": 0, "feet": 3, "shoulders": 4, "neck": 5, "head": 6, "hand": 7}
SLOT_VI = {"head": "Đầu", "neck": "Cổ", "shoulders": "Vai", "back": "Lưng", "hand": "Tay", "feet": "Chân"}

# file, id, name, slot, placement. Placement (fractions of the pose): x = centre, w = width,
# and one of bottom / top / cy for the vertical edge. ears: front | covered. wrap: ring around the head.
CATALOG = [
    ("00", "mu-chin-tang-gio", "Mũ Chín Tầng Gió", "head", dict(x=.50, w=.58, bottom=.275, ears="front")),
    ("02", "mu-tan-bong-bay", "Mũ Tán Bóng Bay", "head", dict(x=.50, w=.66, bottom=.285, ears="front")),
    ("03", "mu-mang-bay-dot", "Mũ Măng Bảy Đốt", "head", dict(x=.50, w=.52, bottom=.275, ears="front")),
    ("04", "hoa-hai-mau", "Hoa Hai Màu", "head", dict(x=.20, w=.20, cy=.20, ears="front", behind_ear=True)),
    ("05", "vong-dom-dom", "Vòng Đom Đóm", "head", dict(x=.50, w=.62, bottom=.31, ears="front", wrap=.66)),
    ("26", "cai-la", "Cài Lá", "head", dict(x=.79, w=.20, cy=.20, ears="front", behind_ear=True)),
    ("07", "khan-nam-dong-song", "Khăn Năm Dòng Sông", "neck", dict(x=.52, w=.66, top=.45)),
    ("08", "mat-day-vong-trang", "Mặt Dây Vòng Trăng", "neck", dict(x=.50, w=.30, top=.45)),
    ("09", "khan-la-biet-bay", "Khăn Lá Biết Bay", "neck", dict(x=.50, w=.44, top=.46)),
    ("15", "khan-gio", "Khăn Gió", "neck", dict(x=.52, w=.52, top=.45)),
    ("17", "khan-la-soc", "Khăn Lá Sọc", "neck", dict(x=.50, w=.62, top=.46)),
    ("23", "binh-ngoc-xanh", "Bình Ngọc Xanh", "neck", dict(x=.50, w=.20, top=.50)),
    ("32", "chuoi-hat-go", "Chuỗi Hạt Gỗ", "neck", dict(x=.50, w=.40, top=.44)),
    ("33", "no-la", "Nơ Lá", "neck", dict(x=.50, w=.42, top=.47)),
    ("10", "ao-choang-la", "Áo Choàng Lá", "shoulders", dict(x=.50, w=.64, top=.455)),
    ("16b", "canh-nho", "Cánh Nhỏ", "back", dict(x=.50, w=1.10, cy=.47)),
    ("13", "gio-hat-mam", "Giỏ Hạt Mầm", "hand", dict(h=.30)),
    ("12", "tui-la", "Túi Lá", "hand", dict(h=.26)),
    ("21", "dieu-gio-chay", "Diều Gió Chạy", "hand", dict(h=.44)),
    ("22", "dua-la", "Đũa Lá", "hand", dict(h=.40)),
    ("18+19", "gang-tay-la", "Găng Tay Lá", "hand", dict(pair="paws", w=.19)),
    ("14", "giay-la", "Giày Lá", "feet", dict(pair="feet", w=.29)),
]
PAWS = [(.237, .855), (.766, .855)]       # left / right paw centres on the pose
FEET = [(.311, .992), (.672, .992)]       # foot centres x, sole y


def load(name):
    im = Image.open(ITEMS / f"{name}.png").convert("RGBA")
    return im.crop(im.getbbox())


def split_pair(im):
    """Two objects side by side -> (left, right), cut at the widest empty column run."""
    cols = np.asarray(im.getchannel("A")).max(0) > 32
    best, run = (0, im.width // 2), None
    for x in range(im.width):
        if not cols[x]:
            run = x if run is None else run
        elif run is not None:
            if x - run > best[0]:
                best = (x - run, (run + x) // 2)
            run = None
    cut = best[1]
    l, r = im.crop((0, 0, cut, im.height)), im.crop((cut, 0, im.width, im.height))
    return l.crop(l.getbbox()), r.crop(r.getbbox())


def put(canvas, art, x, y_edge, edge, W, H, pad, width=None, height=None):
    if width is not None:
        w = width * W
        h = art.height * w / art.width
    else:
        h = height * H
        w = art.width * h / art.height
    art = art.resize((max(1, round(w)), max(1, round(h))), Image.LANCZOS)
    px = x * W + pad - w / 2
    py = {"bottom": y_edge * H - h, "top": y_edge * H, "cy": y_edge * H - h / 2}[edge] + pad
    layer = Image.new("RGBA", canvas)
    layer.alpha_composite(art, (round(px), round(py)))
    return layer


def erase(layer, mask):
    layer.putalpha(ImageChops.subtract(layer.getchannel("A"), mask))
    return layer


def main():
    anchors, base, W, H, pad, canvas = fp.setup("huhu")
    geo = anchors["layers"]
    masks = fp.part_masks(geo, W, H, pad, canvas)
    noears = fp.ears_off(base, geo, W, H, pad)
    body_a = base.getchannel("A")
    hd = geo["head"]
    head_ell = Image.new("L", canvas)
    cx, cy, rx, ry = hd["x"] * W + pad, hd["y"] * H + pad, hd["rx"] * W, hd["ry"] * H
    ImageDraw.Draw(head_ell).ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=255)

    layers = {"body": base, "body-noears": noears}
    items = []
    for files, iid, name, slot, p in CATALOG:
        if p.get("pair") == "paws":
            l, r = load("18"), load("19")
            layer = Image.new("RGBA", canvas)
            for art, (px, py) in zip((l, r), PAWS):
                layer.alpha_composite(put(canvas, art, px, py, "cy", W, H, pad, width=p["w"]))
            thumb = Image.new("RGBA", (l.width + r.width + 20, max(l.height, r.height)))
            thumb.alpha_composite(l, (0, 0)); thumb.alpha_composite(r, (l.width + 20, 0))
        elif p.get("pair") == "feet":
            pair = load(files)
            r = load("14-boot")                           # the front boot is the only complete one
            r = r.resize((r.width, round(r.height * 0.66)), Image.LANCZOS)  # chibi legs: short shaft
            l = r.transpose(Image.FLIP_LEFT_RIGHT)
            layer = Image.new("RGBA", canvas)
            for art, (fx, fy) in zip((l, r), FEET):
                layer.alpha_composite(put(canvas, art, fx, fy, "bottom", W, H, pad, width=p["w"]))
            thumb = pair
        else:
            art = load(files)
            thumb = art
            if p.get("cut_below"):  # keep only the part above this fraction (hood lining would hide the face)
                art = art.crop((0, 0, art.width, round(art.height * p["cut_below"])))
                art = art.crop(art.getbbox())
            if slot == "hand":
                a = anchors["hand"]
                layer = put(canvas, art, a["x"], a["y"], "bottom", W, H, pad, height=p["h"])
                layer.alpha_composite(fp.paw(canvas, a["x"] * W + pad, a["y"] * H + pad - W * 0.05, W))
            else:
                edge = "bottom" if "bottom" in p else "top" if "top" in p else "cy"
                if slot in ("neck", "shoulders"):
                    art = fp.bend(art, -0.028 * H)
                layer = put(canvas, art, p["x"], p[edge], edge, W, H, pad, width=p["w"])
                if slot in ("neck", "shoulders"):
                    erase(layer, masks["head"])          # tucked under the chin
                if slot == "head" and p.get("wrap"):
                    a = np.asarray(layer.getchannel("A")) > 0
                    ys = np.nonzero(a.any(1))[0]
                    mid = ys[0] + (ys[-1] - ys[0]) * p["wrap"]  # ring's back half sits above this line
                    behind = Image.new("L", canvas)
                    ImageDraw.Draw(behind).rectangle([0, 0, canvas[0], mid], fill=255)
                    erase(layer, ImageChops.multiply(ImageChops.multiply(behind, head_ell), body_a))
                if slot == "head" and p.get("ears") == "front":
                    erase(layer, masks["ears"])          # ears stay in front of small hats
                if slot == "head" and p.get("behind_ear"):
                    erase(layer, ImageChops.multiply(body_a, masks["ears"]))
        covered = slot == "head" and p.get("ears") == "covered"
        layers[iid] = layer
        layers[iid + "-sh"] = fp.shadow([layer], noears if covered else base, H)
        items.append({"id": iid, "name": name, "slot": slot, "slotVi": SLOT_VI[slot], "z": Z[slot],
                      "covered": covered, "_thumb": thumb})

    box = None
    for img in layers.values():
        b = img.getbbox()
        if b:
            box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3]))
    for d in ("layers", "thumbs"):
        (OUT / d).mkdir(parents=True, exist_ok=True)
        for f in (OUT / d).glob("*.webp"):
            f.unlink()
    scale = 900 / (box[3] - box[1])
    size = (round((box[2] - box[0]) * scale), 900)
    for name, img in layers.items():
        img.crop(box).resize(size, Image.LANCZOS).save(OUT / "layers" / f"{name}.webp", quality=88, method=6)
    for e in items:
        t = e.pop("_thumb")
        t.thumbnail((200, 200), Image.LANCZOS)
        t.save(OUT / "thumbs" / f"{e['id']}.webp", quality=90)
    outfits = [
        {"name": "Nhà du hành gió", "ids": ["mu-chin-tang-gio", "khan-gio", "dieu-gio-chay"]},
        {"name": "Người canh trăng", "ids": ["vong-dom-dom", "mat-day-vong-trang", "canh-nho"]},
        {"name": "Rừng thức dậy", "ids": ["mu-tan-bong-bay", "khan-la-biet-bay", "gio-hat-mam", "giay-la"]},
        {"name": "Thợ săn đom đóm", "ids": ["vong-dom-dom", "chuoi-hat-go", "tui-la"]},
        {"name": "Hiệp sĩ măng", "ids": ["mu-mang-bay-dot", "ao-choang-la", "gang-tay-la", "giay-la"]},
        {"name": "Tiên nhỏ", "ids": ["hoa-hai-mau", "no-la", "canh-nho", "dua-la"]},
    ]
    (OUT / "data.json").write_text(json.dumps({"size": size, "items": items, "outfits": outfits},
                                              ensure_ascii=False), encoding="utf-8")
    print(len(items), "items", size)


if __name__ == "__main__":
    main()
