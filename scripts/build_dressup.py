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
from PIL import Image, ImageChops, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fit_preview as fp  # noqa: E402

ITEMS = fp.ROOT / "assets/closet/v3/items"
OUT = fp.ROOT / "docs/hu-hu-thay-do"
Z = {"back": 0, "feet": 3, "shoulders": 4, "neck": 5, "head": 6, "hand": 7}
SLOT_VI = {"head": "Đầu", "neck": "Cổ", "shoulders": "Vai", "back": "Lưng", "hand": "Tay", "feet": "Chân"}

# file, id, name, slot, placement. Placement (fractions of the pose): x = centre, w = width,
# and one of bottom / top / cy for the vertical edge. ears: front | covered. wrap: ring around the head.
CATALOG = [
    ("00", "mu-chin-tang-gio", "Mũ Chín Tầng Gió", "head", dict(x=.495, w=.50, bottom=.255, ears="behind")),
    ("02", "mu-tan-bong-bay", "Mũ Tán Bóng Bay", "head", dict(x=.495, w=.54, bottom=.26, ears="behind")),
    ("03", "mu-mang-bay-dot", "Mũ Măng Bảy Đốt", "head", dict(x=.495, w=.46, bottom=.255, ears="behind")),
    ("04", "hoa-hai-mau", "Hoa Hai Màu", "head", dict(x=.24, w=.20, cy=.21, ears="front")),
    ("05", "vong-dom-dom", "Vòng Đom Đóm", "head", dict(x=.50, w=.62, bottom=.31, ears="front", wrap=.66)),
    ("26", "cai-la", "Cài Lá", "head", dict(x=.76, w=.20, cy=.21, ears="front")),
    ("07", "khan-nam-dong-song", "Khăn Năm Dòng Sông", "neck", dict(x=.51, w=.46, top=.50, band=True)),
    ("08", "mat-day-vong-trang", "Mặt Dây Vòng Trăng", "neck", dict(x=.50, w=.30, top=.45)),
    ("09", "khan-la-biet-bay", "Khăn Lá Biết Bay", "neck", dict(x=.50, w=.44, top=.50, band=True)),
    ("15", "khan-gio", "Khăn Gió", "neck", dict(x=.52, w=.50, top=.50, band=True)),
    ("17", "khan-la-soc", "Khăn Lá Sọc", "neck", dict(x=.50, w=.60, top=.50, band=True)),
        ("32", "chuoi-hat-go", "Chuỗi Hạt Gỗ", "neck", dict(x=.50, w=.40, top=.44)),
    ("33", "no-la", "Nơ Lá", "neck", dict(x=.50, w=.42, top=.47)),
    ("10", "ao-choang-la", "Áo Choàng Lá", "shoulders", dict(worn="top")),
    ("16b", "canh-nho", "Cánh Nhỏ", "back", dict(x=.50, w=1.10, cy=.47)),
    ("13", "gio-hat-mam", "Giỏ Hạt Mầm", "hand", dict(h=.24, grip=(.50, .05))),
    ("23", "binh-ngoc-xanh", "Bình Ngọc Xanh", "hand", dict(h=.21, grip=(.52, .06))),
    ("12", "tui-la", "Túi Lá", "hand", dict(h=.23, grip=(.81, .07))),
    ("21", "dieu-gio-chay", "Diều Gió Chạy", "hand", dict(h=.34, grip=(.05, .33), mirror=True, fly=(.08, .40))),
    ("22", "dua-la", "Đũa Lá", "hand", dict(h=.42, grip=(.14, .80), mirror=True)),
    ("18+19", "gang-tay-la", "Găng Tay Lá", "hand", dict(pair="paws", top=.70)),
    ("14", "giay-la", "Giày Lá", "feet", dict(pair="feet", top=.85)),
]
PAWS = [(.215, .855), (.787, .855)]       # left / right paw centres (fists tucked at the sides)
ARMS = [(.205, .80, .15, .26), (.744, .80, .70, .78)]  # a point inside each forearm strip, its x range
FEET = [(.318, .997), (.645, .997)]       # foot centres x, sole y (feet are ~.25 W wide, ~.14 H tall)


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


def palette(art):
    """Main colours of the glove art: (body green, cuff cream, band gold)."""
    a = np.asarray(art).reshape(-1, 4)
    px = a[a[:, 3] > 200][:, :3].astype(int)
    r, g, b = px.T
    pick = lambda m: tuple(int(v) for v in np.median(px[m], axis=0))
    return pick((g > r + 15) & (g < 170)), pick((r > 235) & (g > 225) & (b > 180)), pick((r > 220) & (b < 140))


def worn_gloves(pose_a, pose_rgb, art, W, H, pad, canvas, top):
    """Gloves as worn: only the outside shows. Each forearm strip below `top` (inside the body's
    own outline) is filled with the glove; a cream cuff with a gold band is where the arm goes in."""
    green, cream, gold = palette(art)
    lum = pose_rgb.astype(int) @ np.array([299, 587, 114]) // 1000
    inside = (pose_a > 200) & (lum > 100)            # fur and stripes, not the outline
    inside[: round(top * H)] = False
    inside[round(.866 * H):] = False                  # the hand ends where the foot starts
    k = 4
    hi = Image.new("RGBA", (canvas[0] * k, canvas[1] * k))
    for sx, sy, xa, xb in ARMS:
        box = inside.copy()
        box[:, : round(xa * W)] = False
        box[:, round(xb * W):] = False
        work = Image.fromarray(box.astype(np.uint8) * 255).copy()
        ImageDraw.floodfill(work, (round(sx * W), round(sy * H)), 128, thresh=0)
        strip = np.asarray(work) == 128
        ys, xs = np.nonzero(strip)
        y0, y1 = ys.min(), ys.max()
        m = Image.fromarray(strip.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(3))
        m = m.resize((W * k, H * k), Image.LANCZOS).point(lambda v: v if v > 8 else 0)
        fill = Image.new("RGBA", (W * k, H * k))
        d = ImageDraw.Draw(fill)
        d.rectangle([0, 0, W * k, H * k], fill=green + (255,))
        c0, c1, c2 = y0 * k, (y0 + .020 * H) * k, (y0 + .029 * H) * k
        d.rectangle([0, c0, W * k, c1], fill=cream + (255,))
        d.rectangle([0, c1, W * k, c2], fill=gold + (255,))
        lw = .004 * H * k
        for y in (c1, c2):
            d.line([(0, y), (W * k, y)], fill=fp.OUTLINE + (255,), width=round(lw * .7))
        d.line([(0, c0 + lw / 2), (W * k, c0 + lw / 2)], fill=fp.OUTLINE + (255,), width=round(lw))
        bx, by, br = xs.mean() * k, (c1 + c2) / 2, .011 * H * k
        d.ellipse([bx - br, by - br, bx + br, by + br], fill=gold + (255,), outline=fp.OUTLINE + (255,), width=round(lw * .7))
        fill.putalpha(ImageChops.multiply(fill.getchannel("A"), m))
        hi.alpha_composite(fill, (pad * k, pad * k))
    return hi.resize(canvas, Image.LANCZOS)


def fill_region(pose, seeds, y0, y1, x_ranges=None, drop_white=False):
    """Fur area of the pose (inside its outlines) reachable from the seeds between rows y0..y1."""
    a = pose.astype(int)
    W, H = pose.shape[1], pose.shape[0]
    lum = a[..., :3] @ np.array([299, 587, 114]) // 1000
    inside = (a[..., 3] > 200) & (lum > 100)
    if drop_white:                                    # the white cheek tufts belong to the head
        inside &= ~((a[..., 0] > 240) & (a[..., 1] > 240) & (a[..., 2] > 235))
    ys = np.arange(H)[:, None]
    lo = y0(np.arange(W))[None, :] if callable(y0) else y0 * H
    inside &= (ys >= lo) & (ys < y1 * H)
    out = np.zeros_like(inside)
    for n, (sx, sy) in enumerate(seeds):
        box = inside.copy()
        if x_ranges and x_ranges[n]:
            xa, xb = x_ranges[n]
            box[:, : round(xa * W)] = False
            box[:, round(xb * W):] = False
        work = Image.fromarray(box.astype(np.uint8) * 255).copy()
        ImageDraw.floodfill(work, (round(sx * W), round(sy * H)), 128, thresh=0)
        got = np.asarray(work) == 128
        shut = Image.fromarray(got.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.MinFilter(9))
        out |= got | ((np.asarray(shut) > 0) & (a[..., 3] > 200) & (lum > 60))   # close thin creases (toe lines)
    return out


def texture_into(region, art, W, H, pad, canvas, grow=(0, 0, 0, 0)):
    """Stretch the art over the region's box (grown by fractions l, t, r, b) and keep it inside the region."""
    ys, xs = np.nonzero(region)
    x0, x1, y0, y1 = xs.min() - grow[0] * W, xs.max() + grow[2] * W, ys.min() - grow[1] * H, ys.max() + grow[3] * H
    tex = art.resize((round(x1 - x0), round(y1 - y0)), Image.LANCZOS)
    m = Image.fromarray(region.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(3))
    layer = Image.new("RGBA", (W, H))
    layer.alpha_composite(tex, (round(x0), round(y0)))
    layer.putalpha(ImageChops.multiply(layer.getchannel("A"), m))
    out = Image.new("RGBA", canvas)
    out.alpha_composite(layer, (pad, pad))
    return out


def front_boot(region, art, W, H, pad, canvas):
    """A front-view boot in the boot art's colours, drawn inside the foot's own outline:
    green shaft, cream toe cap, blue sole along the bottom contour, cream rim and gold bead on top."""
    a = np.asarray(art).reshape(-1, 4)
    px = a[a[:, 3] > 200][:, :3].astype(int)
    r, g, b = px.T
    pick = lambda m: tuple(int(v) for v in np.median(px[m], axis=0)) + (255,)
    green, cream = pick((g > r + 15) & (g < 170)), pick((r > 235) & (g > 225) & (b > 180))
    gold, blue = pick((r > 220) & (b < 140)), pick(b > r + 50)
    ink = fp.OUTLINE + (255,)
    ys, xs = np.nonzero(region)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    k = 4
    big = lambda m: Image.fromarray(m.astype(np.uint8) * 255).resize((W * k, H * k), Image.LANCZOS)
    img = Image.new("RGBA", (W * k, H * k))
    d = ImageDraw.Draw(img)
    d.rectangle([x0 * k, y0 * k, x1 * k, y1 * k], fill=green)
    lw = .006 * H * k
    toe = y0 + (y1 - y0) * .42                      # cream toe cap, rounded top
    d.ellipse([(x0 - .03 * W) * k, toe * k, (x1 + .03 * W) * k, (y1 + (y1 - y0) * .9) * k], fill=cream, outline=ink, width=round(lw))
    sole_t = round(.022 * H)                        # sole: a band following the bottom contour
    up = np.zeros_like(region)
    up[:-sole_t] = region[sole_t:]
    sole = region & ~up
    soft = big(sole)
    blue_l = Image.new("RGBA", img.size, blue)
    blue_l.putalpha(soft)
    img.alpha_composite(blue_l)
    line = big(np.roll(sole, -2, axis=0) & ~sole & region)
    ink_l = Image.new("RGBA", img.size, ink)
    ink_l.putalpha(line.filter(ImageFilter.MaxFilter(5)))
    img.alpha_composite(ink_l)
    rim = .016 * H                                  # front rim where the leg goes in
    d.rectangle([x0 * k, y0 * k, x1 * k, (y0 + rim) * k], fill=cream)
    d.line([(x0 * k, (y0 + rim) * k), (x1 * k, (y0 + rim) * k)], fill=ink, width=round(lw * .8))
    d.line([(x0 * k, y0 * k + lw / 2), (x1 * k, y0 * k + lw / 2)], fill=ink, width=round(lw))
    cxm = (x0 + x1) / 2
    d.line([(cxm * k, (y0 + rim) * k), (cxm * k, toe * k)], fill=gold, width=round(.012 * H * k))
    br = .016 * H
    by = y0 + rim + br * .9
    d.ellipse([(cxm - br) * k, (by - br) * k, (cxm + br) * k, (by + br) * k], fill=gold, outline=ink, width=round(lw * .8))
    m = big(region).filter(ImageFilter.MaxFilter(5))
    img.putalpha(ImageChops.multiply(img.getchannel("A"), m))
    out = Image.new("RGBA", canvas)
    out.alpha_composite(img.resize((W, H), Image.LANCZOS), (pad, pad))
    return out


def boot_worn(boot):
    """Cut the boot opening and the back of its rim: on a foot the leg fills the opening, so only
    the front rim shows, with the leg going in behind it."""
    from import_item import regions
    a = np.asarray(boot).astype(int)
    r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    hole = (al > 200) & (g > r + 10) & (r + g + b < 420)
    hole[round(boot.height * .3):] = False             # the opening is in the top part only
    thin = np.asarray(Image.fromarray(hole.astype(np.uint8) * 255).filter(ImageFilter.MinFilter(7))) > 0
    blobs = [m for m in regions(thin) if m.sum() > hole.size * .005]   # eroded: the rim splits them
    top = min(blobs, key=lambda m: np.nonzero(m)[0].mean())    # the topmost green area
    hole &= np.asarray(Image.fromarray(top.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(9))) > 0
    ys, xs = np.nonzero(hole)
    x0, x1 = xs.min(), xs.max()
    cols = np.unique(xs)
    low = np.array([ys[xs == x].max() for x in cols], float)
    fit = np.poly1d(np.polyfit(cols, low, 2))          # smooth front lip of the opening
    edge = fit(np.clip(np.arange(boot.width), x0, x1))
    keep = (np.clip(np.arange(boot.height)[:, None] - edge[None, :], 0, 1) * 255).astype(np.uint8)  # soft edge
    out = boot.copy()
    out.putalpha(ImageChops.multiply(boot.getchannel("A"), Image.fromarray(keep)))
    k = 4
    line = Image.new("RGBA", (boot.width * k, boot.height * k))
    lw = max(2, round(boot.height * .025)) * k
    ImageDraw.Draw(line).line([(x * k, edge[x] * k + lw / 2) for x in range(boot.width)], fill=fp.OUTLINE + (255,), width=lw)
    line = line.resize(boot.size, Image.LANCZOS)
    line.putalpha(ImageChops.multiply(line.getchannel("A"), boot.getchannel("A")))
    out.alpha_composite(line)
    return out.crop(out.getbbox())


def neck_band(art, geo, W, H, pad, canvas, body_a):
    """A fabric band in the scarf's own colour, following the jaw line across the whole neck."""
    a = np.asarray(art)
    px = a[a[..., 3] > 200][:, :3].astype(int)
    sat = px.max(1) - px.min(1)
    colour = tuple(int(v) for v in np.median(px[sat >= np.percentile(sat, 60)], axis=0))
    k = 4
    band = Image.new("RGBA", (canvas[0] * k, canvas[1] * k))
    d = ImageDraw.Draw(band)
    pts = [((x * W + pad) * k, (y * H + pad + 0.018 * H) * k) for x, y in geo["chin"]]
    pts = [(pts[0][0] - 0.06 * W * k, pts[0][1] - 0.02 * H * k)] + pts + [(pts[-1][0] + 0.06 * W * k, pts[-1][1] - 0.02 * H * k)]
    d.line(pts, fill=fp.OUTLINE + (255,), width=round(0.050 * H * k), joint="curve")
    d.line(pts, fill=colour + (255,), width=round(0.036 * H * k), joint="curve")
    band = band.resize(canvas, Image.LANCZOS)
    band.putalpha(ImageChops.multiply(band.getchannel("A"), body_a))
    return band


def main():
    anchors, base, W, H, pad, canvas = fp.setup("huhu")
    geo = anchors["layers"]
    masks = fp.part_masks(geo, W, H, pad, canvas)
    # round skull for big hats: this ellipse meets the real head contour at .275, so no ear stubs stay
    skull = dict(geo, head=dict(geo["head"], x=.50, rx=.303), ear_cut=.275)
    noears = fp.ears_off(base, skull, W, H, pad)
    body_a = base.getchannel("A")
    # the ghost wisps float in front of everything: split them off the body (all but the largest blob)
    from import_item import regions
    blobs = regions(np.asarray(body_a) > 128)
    torso = max(blobs, key=lambda r: r.sum())
    torso_img = Image.fromarray(torso.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(5))
    wisp_mask = ImageChops.subtract(body_a, torso_img)
    torso_a = ImageChops.multiply(body_a, torso_img)
    hd = geo["head"]
    head_ell = Image.new("L", canvas)
    cx, cy, rx, ry = hd["x"] * W + pad, hd["y"] * H + pad, hd["rx"] * W, hd["ry"] * H
    ImageDraw.Draw(head_ell).ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=255)

    wisps = base.copy()
    wisps.putalpha(ImageChops.multiply(base.getchannel("A"), wisp_mask))
    layers = {"body": base, "body-noears": noears, "wisps": wisps}
    items = []
    for files, iid, name, slot, p in CATALOG:
        if p.get("pair") == "paws":
            l, r = load("18"), load("19")
            pose = np.asarray(base.crop((pad, pad, pad + W, pad + H)))
            layer = worn_gloves(pose[..., 3], pose[..., :3], l, W, H, pad, canvas, p["top"])
            thumb = Image.new("RGBA", (l.width + r.width + 20, max(l.height, r.height)))
            thumb.alpha_composite(l, (0, 0)); thumb.alpha_composite(r, (l.width + 20, 0))
        elif p.get("pair") == "feet":
            pair = load(files)
            r = boot_worn(load("14-boot"))                 # the front boot is the only complete one
            l = r.transpose(Image.FLIP_LEFT_RIGHT)
            pose = np.asarray(base.crop((pad, pad, pad + W, pad + H)))
            layer = Image.new("RGBA", canvas)
            for art, (fx, fy) in zip((l, r), FEET):          # the boot takes the foot's own shape
                foot = fill_region(pose, [(fx, .94)], p["top"], 1.0, [(fx - .16, fx + .16)])
                layer.alpha_composite(front_boot(foot, art, W, H, pad, canvas))
            thumb = pair
        else:
            art = load(files)
            thumb = art
            if p.get("cut_below"):  # keep only the part above this fraction (hood lining would hide the face)
                art = art.crop((0, 0, art.width, round(art.height * p["cut_below"])))
                art = art.crop(art.getbbox())
            if p.get("worn") == "top":                   # a top covers the torso and both arms
                pose = np.asarray(base.crop((pad, pad, pad + W, pad + H)))
                cx, cy = zip(*geo["chin"])
                chin = lambda x: (np.interp(x / W, cx, cy) + .012) * H
                torso = fill_region(pose, [(.50, .70)], chin, .865, drop_white=True)
                arms = fill_region(pose, [a[:2] for a in ARMS], .60, .866, [a[2:] for a in ARMS])
                torso &= np.asarray(torso_img.crop((pad, pad, pad + W, pad + H))) > 0
                layer = texture_into(torso | arms, art, W, H, pad, canvas, (.02, .05, .02, .03))
            elif slot == "hand":
                px, py = PAWS[0]
                h = p["h"] * H
                art = art.resize((max(1, round(art.width * h / art.height)), max(1, round(h))), Image.LANCZOS)
                gx, gy = p["grip"]
                if p.get("mirror"):  # point long items away from the body
                    art, gx = art.transpose(Image.FLIP_LEFT_RIGHT), 1 - gx
                layer = Image.new("RGBA", canvas)
                if p.get("fly"):  # kite flies up beside the head; a string runs from the paw to it
                    fx, fy = p["fly"]
                    kx, ky = fx * W + pad, fy * H + pad
                    k = 4
                    s = Image.new("RGBA", (canvas[0] * k, canvas[1] * k))
                    ImageDraw.Draw(s).line([(px * W + pad) * k, (py * H + pad) * k, kx * k, ky * k],
                                           fill=fp.OUTLINE + (255,), width=3 * k)
                    layer.alpha_composite(s.resize(canvas, Image.LANCZOS))
                    layer.alpha_composite(art, (round(kx - gx * art.width), round(ky - gy * art.height)))
                else:
                    layer.alpha_composite(art, (round(px * W + pad - gx * art.width), round(py * H + pad - gy * art.height)))
                layer.alpha_composite(fp.paw(canvas, px * W + pad, py * H + pad, W))   # paw closes on the grip
            else:
                edge = "bottom" if "bottom" in p else "top" if "top" in p else "cy"
                if slot == "neck":
                    art = fp.bend(art, -0.028 * H)
                layer = put(canvas, art, p["x"], p[edge], edge, W, H, pad, width=p["w"])
                if p.get("band"):  # the scarf goes all the way round the neck, knot on top
                    layer = Image.alpha_composite(neck_band(art, geo, W, H, pad, canvas, torso_a), layer)
                if slot in ("neck", "shoulders"):
                    erase(layer, masks["head"])          # tucked under the chin
                if slot == "head" and p.get("wrap"):
                    a = np.asarray(layer.getchannel("A")) > 0
                    ys = np.nonzero(a.any(1))[0]
                    mid = ys[0] + (ys[-1] - ys[0]) * p["wrap"]  # ring's back half sits above this line
                    behind = Image.new("L", canvas)
                    ImageDraw.Draw(behind).rectangle([0, 0, canvas[0], mid], fill=255)
                    erase(layer, ImageChops.multiply(ImageChops.multiply(behind, head_ell), body_a))
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
