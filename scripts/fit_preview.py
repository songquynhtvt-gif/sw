#!/usr/bin/env python3
"""Dress a companion in Tủ đồ items (layered, not pasted on top).

The pose is split into occluding parts so items read as worn:
  body (ears removed under big hats, head outline redrawn) → item shadow on the fur →
  neck items (bent to follow the jaw) → head front (chin, cheeks, fangs over the scarf's
  top edge) → head items (bent to hug the head) → ears front (small hats: ears poke
  through) → hand items → a drawn mitten paw closed over the grip
Geometry lives in prompts/closet/items.json -> anchors.<companion> ("layers": fractions of the
pose). Per item "fit": {"scale", "dx", "dy", "ears": "front" | "covered", "bend": fraction of H}.

Uses the approved file if there is one, else the newest gen file, unless --file is given.

Examples:
  python3 scripts/fit_preview.py --id mu-la
  python3 scripts/fit_preview.py --id mu-la khan-ran ong-nhom-tre     # full outfit
  python3 scripts/fit_preview.py --sheet                               # every item worn, one sheet
  python3 scripts/fit_preview.py --rig                                 # export the pose layers for the app
"""
import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
CLOSET = json.loads((ROOT / "prompts/closet/items.json").read_text(encoding="utf-8"))
OUT = ROOT / "assets/closet/fit"
RIG = ROOT / "assets/closet/rig"
LAYER = {"hand": 0, "neck": 1, "head": 2}
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def item_file(item_id):
    approved = ROOT / f"assets/closet/approved/{item_id}.png"
    if approved.exists():
        return approved
    gens = sorted((ROOT / "assets/closet/gen").glob(f"{item_id}-v*.png"),
                  key=lambda p: int(p.stem.rsplit("-v", 1)[1]))
    return gens[-1] if gens else None


def place(art, slot, anchor, tweak, W, H, pad, canvas):
    """The item on its own transparent canvas, positioned at its anchor."""
    art = art.crop(art.getbbox())  # trim transparent margin
    scale = tweak.get("scale", 1.0)
    if slot == "hand":
        h = anchor["h"] * H * scale
        w = art.width * h / art.height
    else:
        w = anchor["w"] * W * scale
        h = art.height * w / art.width
    art = art.resize((round(w), round(h)), Image.LANCZOS)
    depth = tweak.get("bend", {"head": 0.03, "neck": -0.028}.get(slot, 0)) * H
    art = bend(art, depth)
    h = art.height
    x = (anchor["x"] + tweak.get("dx", 0)) * W - w / 2
    y = (anchor["y"] + tweak.get("dy", 0)) * H
    if slot != "neck":  # head and hand: anchor is the item's bottom edge
        y -= h
    layer = Image.new("RGBA", canvas)
    layer.alpha_composite(art, (round(x) + pad, round(y) + pad))
    return layer


OUTLINE = (46, 83, 59)   # Hǔhǔ's line colour, sampled from the pose
FUR = (245, 244, 208)


def bend(art, depth):
    """Curve an item along the body: depth > 0 drops the sides (hat hugging the head),
    depth < 0 lifts them (scarf following the jaw). Parabolic per-column shift."""
    if not depth:
        return art
    import numpy as np
    a = np.asarray(art)
    h, w = a.shape[:2]
    d = abs(round(depth))
    out = np.zeros((h + d, w, 4), np.uint8)
    for x in range(w):
        t = (x - (w - 1) / 2) / ((w - 1) / 2)
        s = round(d * t * t)
        y0 = s if depth > 0 else d - s
        out[y0:y0 + h, x] = a[:, x]
    return Image.fromarray(out, "RGBA")


def ears_off(base, geo, W, H, pad):
    """The pose without ears: erase above the head curve and redraw the outline there,
    so a big hat sits on a round head instead of being propped up by the ears."""
    hd = geo["head"]
    cx, cy, rx, ry = hd["x"] * W + pad, hd["y"] * H + pad, hd["rx"] * W, hd["ry"] * H
    zone = Image.new("L", base.size)
    d = ImageDraw.Draw(zone)
    x0 = min(e["x"] - e["rx"] for e in geo["ears"]) * W + pad - 4
    x1 = max(e["x"] + e["rx"] for e in geo["ears"]) * W + pad + 4
    d.rectangle([x0, 0, x1, geo["ear_cut"] * H + pad], fill=255)
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=0)  # keep the head itself
    out = base.copy()
    out.putalpha(ImageChops.subtract(base.getchannel("A"), zone))
    k = 4  # supersampled outline arc
    arc = Image.new("RGBA", (base.width * k, base.height * k))
    lw = max(2, round(W * 0.009)) * k
    top = cy - ry
    ImageDraw.Draw(arc).arc([(cx - rx) * k, top * k, (cx + rx) * k, (cy + ry) * k], 180, 360,
                            fill=OUTLINE + (255,), width=lw)
    arc = arc.resize(base.size, Image.LANCZOS)
    clip = Image.new("L", base.size)
    ImageDraw.Draw(clip).rectangle([x0, 0, x1, geo["ear_cut"] * H + pad + 6], fill=255)
    arc.putalpha(ImageChops.multiply(arc.getchannel("A"), clip))
    out.alpha_composite(arc)
    return out


def paw(canvas, cx, cy, W, side=1):
    """A closed mitten paw in Hǔhǔ's style, drawn over a held item's grip."""
    k = 4
    rx, ry = W * 0.052, W * 0.046
    lw = max(2, round(W * 0.008))
    img = Image.new("RGBA", (round(rx * 2 + lw * 4) * k, round(ry * 2 + lw * 4) * k))
    d = ImageDraw.Draw(img)
    o = lw * 2 * k
    d.ellipse([o, o, o + rx * 2 * k, o + ry * 2 * k], fill=FUR + (255,), outline=OUTLINE + (255,), width=lw * k)
    for f in (0.36, 0.64):  # two finger creases on the side facing the item
        fy = o + ry * 2 * k * f
        fx = o + rx * 2 * k * (0.62 if side > 0 else 0.10)
        d.arc([fx, fy - ry * 0.35 * k, fx + rx * 0.55 * k, fy + ry * 0.35 * k],
              270 if side > 0 else 90, 90 if side > 0 else 270, fill=OUTLINE + (255,), width=round(lw * 0.8 * k))
    img = img.resize((img.width // k, img.height // k), Image.LANCZOS)
    layer = Image.new("RGBA", canvas)
    layer.alpha_composite(img, (round(cx - img.width / 2), round(cy - img.height / 2)))
    return layer


def part_masks(geo, W, H, pad, canvas):
    """Occluding parts of the pose as L masks on the padded canvas."""
    def pt(p):
        return (p[0] * W + pad, p[1] * H + pad)

    head = Image.new("L", canvas)
    chin = [pt(p) for p in geo["chin"]]  # left to right along the jaw
    ImageDraw.Draw(head).polygon([(0, 0), (canvas[0], 0), (canvas[0], chin[-1][1])] + chin[::-1] + [(0, chin[0][1])],
                                 fill=255)
    ears = Image.new("L", canvas)
    d = ImageDraw.Draw(ears)
    for e in geo["ears"]:
        cx, cy = pt((e["x"], e["y"]))
        rx, ry = e["rx"] * W, e["ry"] * H
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=255)
    d.rectangle([0, geo["ear_cut"] * H + pad, canvas[0], canvas[1]], fill=0)  # only above the head line
    paw = Image.new("L", canvas)
    p = geo["paw"]
    cx, cy = pt((p["x"], p["y"]))
    ImageDraw.Draw(paw).ellipse([cx - p["rx"] * W, cy - p["ry"] * H, cx + p["rx"] * W, cy + p["ry"] * H], fill=255)
    soft = ImageFilter.GaussianBlur(1.2)
    return {k: v.filter(soft) for k, v in (("head", head), ("ears", ears), ("paw", paw))}


def cut(pose, mask):
    part = pose.copy()
    part.putalpha(ImageChops.multiply(pose.getchannel("A"), mask))
    return part


def shadow(items, pose, H):
    """Soft contact shadow of the items, only where it falls on the fur."""
    a = Image.new("L", pose.size)
    for layer in items:
        a = ImageChops.lighter(a, layer.getchannel("A"))
    a = ImageChops.offset(a, 0, round(H * 0.008)).filter(ImageFilter.GaussianBlur(H * 0.006))
    a = ImageChops.multiply(a, pose.getchannel("A")).point(lambda v: v * 0.28)
    sh = Image.new("RGBA", pose.size, (59, 82, 61, 0))
    sh.putalpha(a)
    return sh


def setup(companion):
    anchors = CLOSET["anchors"][companion]
    pose = Image.open(ROOT / anchors["pose"]).convert("RGBA")
    W, H = pose.size
    pad = H // 2  # room for tall hats and long hand items
    canvas = (W + 2 * pad, H + 2 * pad)
    base = Image.new("RGBA", canvas)
    base.alpha_composite(pose, (pad, pad))
    return anchors, base, W, H, pad, canvas


def dress(ids, companion="huhu", files=None):
    """The companion wearing the items, as an RGBA image (cropped)."""
    by_id = {i["id"]: i for i in CLOSET["items"]}
    if files and len(files) != len(ids):
        raise ValueError("one file per id")
    anchors, base, W, H, pad, canvas = setup(companion)

    layers = {}
    for n, item_id in enumerate(ids):
        it = by_id.get(item_id)
        if not it or it["slot"] not in LAYER:
            raise ValueError(f"{item_id}: unknown id or not wearable")
        if it["slot"] in layers:
            raise ValueError("one item per slot")
        path = (ROOT / files[n]) if files else item_file(item_id)
        if not path or not path.exists():
            raise ValueError(f"{item_id}: no PNG yet (run gen_closet.py or split_sheet.py first)")
        tweak = it.get("fit", {})
        layers[it["slot"]] = (it, place(Image.open(path).convert("RGBA"), it["slot"], anchors[it["slot"]],
                                        tweak, W, H, pad, canvas))

    geo = anchors.get("layers")
    out = base.copy()
    if not geo:  # no part geometry for this companion: plain stacking
        for slot in ("hand", "neck", "head"):
            if slot in layers:
                out.alpha_composite(layers[slot][1])
        return out.crop(out.getbbox())

    masks = part_masks(geo, W, H, pad, canvas)
    if "head" in layers and layers["head"][0].get("fit", {}).get("ears", "front") == "covered" and "head" in geo:
        body = ears_off(base, geo, W, H, pad)  # the body itself changes: no ears under a big hat
        out = body.copy()
        base = body
    out.alpha_composite(shadow([layer for _, layer in layers.values()], base, H))
    if "neck" in layers:
        out.alpha_composite(layers["neck"][1])
        out.alpha_composite(cut(base, masks["head"]))
    if "head" in layers:
        it, layer = layers["head"]
        out.alpha_composite(layer)
        if it.get("fit", {}).get("ears", "front") == "front":
            out.alpha_composite(cut(base, masks["ears"]))
    if "hand" in layers:
        it, layer = layers["hand"]
        out.alpha_composite(layer)
        tw = it.get("fit", {})
        a = anchors["hand"]
        gx = (a["x"] + tw.get("dx", 0)) * W + pad
        gy = (a["y"] + tw.get("dy", 0)) * H + pad - W * 0.05  # the paw closes just above the grip end
        out.alpha_composite(paw(canvas, gx, gy, W, side=1))
    return out.crop(out.getbbox())


def try_on(ids, companion="huhu", files=None):
    """Dress and save; returns the output path."""
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / f"{companion}-{'+'.join(ids)}.png"
    dress(ids, companion, files).save(out)
    return out


def export_rig(companion="huhu"):
    """Pose layers + order for the app (same compositing as dress())."""
    anchors, base, W, H, pad, canvas = setup(companion)
    masks = part_masks(anchors["layers"], W, H, pad, canvas)
    box = (pad, pad, pad + W, pad + H)
    folder = RIG / f"{companion}-front"
    folder.mkdir(parents=True, exist_ok=True)
    base.crop(box).save(folder / "body.png")
    for k in ("head", "ears"):
        cut(base, masks[k]).crop(box).save(folder / f"{k}-front.png")
    ears_off(base, anchors["layers"], W, H, pad).crop(box).save(folder / "body-no-ears.png")
    a = anchors["hand"]
    paw(canvas, a["x"] * W + pad, a["y"] * H + pad - W * 0.05, W).crop(box).save(folder / "paw-holding.png")
    stale = folder / "paw-front.png"
    if stale.exists():
        stale.unlink()
    order = {
        "_note": "Draw back to front. All layers share the pose size; item anchors are fractions of it.",
        "order": ["body.png, or body-no-ears.png when the head item's fit.ears is 'covered'",
                  "item shadow (items' alpha, offset 0.8% H, blur 0.6% H, #3B523D 28%, clipped to body)",
                  "neck item, bent: sides lifted by 2.8% H (parabola) to follow the jaw",
                  "head-front.png (only when a neck item is worn)",
                  "head item, bent: sides dropped by 3% H (parabola) to hug the head",
                  "ears-front.png (only when the head item's fit.ears is 'front')",
                  "hand item", "paw-holding.png (only when a hand item is held; moves with the item's dx/dy)"],
        "anchors": {k: v for k, v in anchors.items() if k in ("head", "neck", "hand")},
        "items": {i["id"]: i.get("fit", {}) for i in CLOSET["items"] if i["slot"] in LAYER},
    }
    (folder / "rig.json").write_text(json.dumps(order, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return folder


def sheet(companion="huhu", cell=320, cols=6):
    """Every wearable item worn by the companion, labelled, plus a few full outfits."""
    wear = [i for i in CLOSET["items"] if i["slot"] in LAYER and item_file(i["id"])]
    outfits = [o for o in CLOSET.get("outfits", []) if all(item_file(x) for x in o["ids"])]
    cards = [(i["name"], [i["id"]]) for i in wear] + [(o["name"], o["ids"]) for o in outfits]
    try:
        font = ImageFont.truetype(FONT, 17)
    except OSError:
        font = ImageFont.load_default()
    rows = (len(cards) + cols - 1) // cols
    img = Image.new("RGB", (cols * cell, rows * (cell + 30)), (251, 244, 228))
    d = ImageDraw.Draw(img)
    for k, (name, ids) in enumerate(cards):
        x, y = (k % cols) * cell, (k // cols) * (cell + 30)
        dressed = dress(ids, companion)
        dressed.thumbnail((cell - 16, cell - 16))
        img.paste(dressed, (x + (cell - dressed.width) // 2, y + (cell - dressed.height) // 2), dressed)
        d.text((x + cell // 2, y + cell + 4), name, fill=(27, 42, 107), font=font, anchor="mt")
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / f"_sheet-{companion}-mac-do.png"
    img.save(out)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--id", nargs="+", help="item ids (one per slot)")
    ap.add_argument("--file", nargs="+", type=Path, help="explicit PNG per id, same order")
    ap.add_argument("--companion", default="huhu", choices=[k for k in CLOSET["anchors"] if not k.startswith("_")])
    ap.add_argument("--sheet", action="store_true", help="every item worn, one labelled sheet")
    ap.add_argument("--rig", action="store_true", help="export the pose layers + order for the app")
    args = ap.parse_args()
    if args.rig:
        print(export_rig(args.companion).relative_to(ROOT))
    if args.sheet:
        print(sheet(args.companion).relative_to(ROOT))
    if args.id:
        try:
            out = try_on(args.id, args.companion, args.file)
        except ValueError as e:
            sys.exit(str(e))
        print(out.relative_to(ROOT))
    if not (args.rig or args.sheet or args.id):
        ap.error("give --id, --sheet or --rig")


if __name__ == "__main__":
    main()
