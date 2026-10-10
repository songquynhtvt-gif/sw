#!/usr/bin/env python3
"""Build the dress-up page layers (Hǔhǔ, Wuwu, Dudu) from the v3 object sheet (assets/closet/v3/items/NN.png).

Every item becomes one pose-framed layer per companion with the body interaction baked in, so the
page only stacks layers by z (back < body < shadow < feet < shoulders < neck < head < hand):
  - placements are written for Hǔhǔ and carried to the others through slot frames
    (head: brim point + skull width, neck: chin centre + jaw width, back: torso centre + width)
  - hats sit between / in front of the ears; rings lose the part behind the head top
  - neck items are tucked under the chin (pixels over the head removed); scarves wrap the neck
  - worn items show only their outside: tops fill the torso and arms, gloves the hands,
    boots the feet, each inside the companion's own outline
  - held items sit in the paw: a drawn paw (Hǔhǔ) or the companion's own paws redrawn on top
Base poses: Hǔhǔ front idle; Wuwu / Dudu from scripts/prep_mascots.py.
Output: docs/hu-hu-thay-do/<companion>/layers/*.webp, thumbs/*.webp, data.json
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

# file, id, name, slot, placement. Placement (fractions of Hǔhǔ's pose): x = centre, w = width,
# and one of bottom / top / cy for the vertical edge. wrap: ring around the head.
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
GEN = fp.ROOT / "assets/char/gen"
# Per companion geometry, fractions of its own pose.
#   head / neck / back: slot frames (x, y, width) -> Hǔhǔ placements are scaled into them
#   chin: jaw line (left to right) - neck items are erased above it, tops start below it
#   skull: ellipse (x, y, rx, ry) for rings; grip: where held items are held
#   grip_mask: ellipses (x, y, rx, ry) of the companion's own paws, redrawn over held items
#   gloves: per hand, a seed inside it, its row / column range and which side the cuff is on
#   feet: foot centre x values; top garment: torso seed, bottom row, arm seeds and rows
MASCOTS = {
    "huhu": dict(name="Hǔhǔ", pose="assets/char/gen/huhu-front-idle.png", ink=(46, 83, 59),
                 head=(.495, .255, .606), neck=(.498, .548, .648), back=(.50, .47, .62),
                 chin=[(.174, .509), (.311, .536), (.498, .548), (.685, .536), (.822, .509)],
                 skull=(.492, .376, .311, .251), grip=(.215, .855), grip_kind="paw", hand_scale=1.0, fly=(.08, .40),
                 gloves=[dict(seed=(.205, .80), rows=(.70, .866), cols=(.15, .26), cuff="top"),
                         dict(seed=(.744, .80), rows=(.70, .866), cols=(.70, .78), cuff="top")],
                 feet=[.318, .645], foot_rows=(.85, .94),
                 torso=[(.50, .70)], torso_bottom=.865, drop_white=True,
                 arms=[((.205, .80), (.15, .26)), ((.744, .80), (.70, .78))], arm_rows=(.60, .866)),
    "wuwu": dict(name="Wuwu", pose="assets/char/gen/wuwu/wuwu-dressup-base.png", ink=(11, 34, 61),
                 head=(.50, .18, .50), neck=(.50, .478, .62), back=(.50, .58, .70),
                 chin=[(.19, .42), (.33, .462), (.50, .478), (.67, .462), (.81, .42)],
                 skull=(.50, .30, .31, .22), grip=(.50, .62), grip_kind="mask", hand_scale=1.3, fly=(.10, .26),
                 grip_mask=[(.455, .62, .052, .072), (.545, .62, .052, .072)],
                 gloves=[dict(seed=(.44, .63), rows=(.50, .72), cols=(.37, .505), cuff="left"),
                         dict(seed=(.56, .63), rows=(.50, .72), cols=(.495, .63), cuff="right")],
                 feet=[.31, .70], foot_rows=(.875, .96),
                 torso=[(.50, .50), (.50, .76)], torso_bottom=.84, drop_white=False,
                 arms=[((.25, .60), None), ((.75, .60), None)], arm_rows=(.44, .72)),
    "dudu": dict(name="Dudu", pose="assets/char/gen/dudu/dudu-dressup-base.png", ink=(91, 28, 3),
                 head=(.548, .225, .544), neck=(.55, .52, .51), back=(.55, .64, .55),
                 chin=[(.29, .44), (.36, .50), (.43, .565), (.50, .53), (.58, .515), (.68, .49), (.80, .44)],
                 skull=(.548, .36, .272, .24), grip=(.20, .60), grip_kind="mask", hand_scale=1.2, fly=(.08, .30),
                 grip_mask=[(.197, .603, .074, .08)],
                 gloves=[dict(seed=(.17, .60), rows=(.50, .70), cols=(.10, .272), cuff="right"),
                         dict(seed=(.82, .78), rows=(.715, .84), cols=(.74, .90), cuff="top")],
                 feet=[.405, .65], foot_rows=(.87, .94),
                 torso=[(.55, .70)], torso_bottom=.86, drop_white=False,
                 arms=[((.33, .64), (.27, .45)), ((.80, .62), (.72, .92))], arm_rows=(.48, .84),
                 own=[("dudu-own-hat", "non-la-dudu", "Nón Lá Của Dudu", "head"),
                      ("dudu-own-bamboo", "gay-tre", "Gậy Tre", "hand")]),
}
REF = "huhu"


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


def worn_gloves(pose, art, M, W, H, pad, canvas):
    """Gloves as worn: only the outside shows. Each hand (inside the companion's own outline) is
    filled with the glove; a cream cuff with a gold band is where the arm goes in."""
    green, cream, gold = palette(art)
    ink = M["ink"] + (255,)
    k = 4
    hi = Image.new("RGBA", (canvas[0] * k, canvas[1] * k))
    for g in M["gloves"]:
        hand = fill_region(pose, [g["seed"]], g["rows"][0], g["rows"][1], [g["cols"]])
        ys, xs = np.nonzero(hand)
        x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
        m = Image.fromarray(hand.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(3))
        m = m.resize((W * k, H * k), Image.LANCZOS).point(lambda v: v if v > 8 else 0)
        fill = Image.new("RGBA", (W * k, H * k), green + (255,))
        d = ImageDraw.Draw(fill)
        lw = .004 * H * k
        c1, c2 = .020 * H, .029 * H                    # cuff depth, gold band depth (from the open end)
        if g["cuff"] == "top":
            band = lambda a, b: [0, (y0 + a) * k, W * k, (y0 + b) * k]
            edge = [(0, y0 * k + lw / 2), (W * k, y0 * k + lw / 2)]
            bead = (xs.mean(), y0 + (c1 + c2) / 2)
        else:
            sx = x0 if g["cuff"] == "left" else x1
            sg = 1 if g["cuff"] == "left" else -1
            band = lambda a, b: [min(sx + sg * a, sx + sg * b) * k, 0, max(sx + sg * a, sx + sg * b) * k, H * k]
            edge = [(sx * k + sg * lw / 2, 0), (sx * k + sg * lw / 2, H * k)]
            bead = (sx + sg * (c1 + c2) / 2, ys.mean())
        d.rectangle(band(0, c1), fill=cream + (255,))
        d.rectangle(band(c1, c2), fill=gold + (255,))
        for a in (c1, c2):
            r = band(a, a)
            d.line([(r[0], r[1]), (r[2], r[3])] if g["cuff"] == "top" else [(r[0], 0), (r[0], H * k)], fill=ink, width=round(lw * .7))
        d.line(edge, fill=ink, width=round(lw))
        br = .011 * H * k
        bx, by = bead[0] * k, bead[1] * k
        d.ellipse([bx - br, by - br, bx + br, by + br], fill=gold + (255,), outline=ink, width=round(lw * .7))
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
        px, py = round(sx * W), round(sy * H)
        if not box[py, px]:                           # seed on a line: start from the nearest fur pixel
            yy, xx = np.nonzero(box[max(0, py - 40):py + 40, max(0, px - 40):px + 40])
            if not len(yy):
                continue
            n = np.argmin((yy - min(py, 40)) ** 2 + (xx - min(px, 40)) ** 2)
            px, py = max(0, px - 40) + xx[n], max(0, py - 40) + yy[n]
        work = Image.fromarray(box.astype(np.uint8) * 255).copy()
        ImageDraw.floodfill(work, (int(px), int(py)), 128, thresh=0)
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


def front_boot(region, art, W, H, pad, canvas, ink=fp.OUTLINE):
    """A front-view boot in the boot art's colours, drawn inside the foot's own outline:
    green shaft, cream toe cap, blue sole along the bottom contour, cream rim and gold bead on top."""
    a = np.asarray(art).reshape(-1, 4)
    px = a[a[:, 3] > 200][:, :3].astype(int)
    r, g, b = px.T
    pick = lambda m: tuple(int(v) for v in np.median(px[m], axis=0)) + (255,)
    green, cream = pick((g > r + 15) & (g < 170)), pick((r > 235) & (g > 225) & (b > 180))
    gold, blue = pick((r > 220) & (b < 140)), pick(b > r + 50)
    ink = ink + (255,)
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


def boot_worn(boot, ink=fp.OUTLINE):
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
    ImageDraw.Draw(line).line([(x * k, edge[x] * k + lw / 2) for x in range(boot.width)], fill=ink + (255,), width=lw)
    line = line.resize(boot.size, Image.LANCZOS)
    line.putalpha(ImageChops.multiply(line.getchannel("A"), boot.getchannel("A")))
    out.alpha_composite(line)
    return out.crop(out.getbbox())


def neck_band(art, chin, W, H, pad, canvas, body_a, ink=fp.OUTLINE, k_s=1.0):
    """A fabric band in the scarf's own colour, following the jaw line across the whole neck."""
    a = np.asarray(art)
    px = a[a[..., 3] > 200][:, :3].astype(int)
    sat = px.max(1) - px.min(1)
    colour = tuple(int(v) for v in np.median(px[sat >= np.percentile(sat, 60)], axis=0))
    k = 4
    band = Image.new("RGBA", (canvas[0] * k, canvas[1] * k))
    d = ImageDraw.Draw(band)
    u = 825 * k_s                                    # Hǔhǔ's pose height, scaled to this companion
    pts = [((x * W + pad) * k, (y * H + pad + 0.018 * u) * k) for x, y in chin]
    pts = [(pts[0][0] - 0.06 * u * k, pts[0][1] - 0.02 * u * k)] + pts + [(pts[-1][0] + 0.06 * u * k, pts[-1][1] - 0.02 * u * k)]
    d.line(pts, fill=ink + (255,), width=round(0.050 * u * k), joint="curve")
    d.line(pts, fill=colour + (255,), width=round(0.036 * u * k), joint="curve")
    band = band.resize(canvas, Image.LANCZOS)
    band.putalpha(ImageChops.multiply(band.getchannel("A"), body_a))
    return band


def load_pose(M):
    pose = Image.open(fp.ROOT / M["pose"]).convert("RGBA")
    W, H = pose.size
    pad = H // 2  # room for tall hats and long hand items
    canvas = (W + 2 * pad, H + 2 * pad)
    base = Image.new("RGBA", canvas)
    base.alpha_composite(pose, (pad, pad))
    return base, W, H, pad, canvas


class Frame:
    """Carries a Hǔhǔ placement into a companion's slot frame (same spot on the body, scaled)."""
    def __init__(self, M, slot, ref, RW, RH, W, H):
        fx, fy, fw = ref[slot]
        tx, ty, tw = M[slot]
        self.k = tw * W / (fw * RW)
        self.f, self.t, self.RW, self.RH, self.W, self.H = (fx, fy), (tx, ty), RW, RH, W, H

    def pt(self, x, y):  # Hǔhǔ fractions -> companion pose pixels
        return (self.t[0] * self.W + (x - self.f[0]) * self.RW * self.k,
                self.t[1] * self.H + (y - self.f[1]) * self.RH * self.k)


def put_px(canvas, art, X, Y, edge, w, pad):
    h = art.height * w / art.width
    art = art.resize((max(1, round(w)), max(1, round(h))), Image.LANCZOS)
    py = {"bottom": Y - h, "top": Y, "cy": Y - h / 2}[edge]
    layer = Image.new("RGBA", canvas)
    layer.alpha_composite(art, (round(X - w / 2 + pad), round(py + pad)))
    return layer


def ellipses(canvas, ells, W, H, pad):
    m = Image.new("L", canvas)
    d = ImageDraw.Draw(m)
    for x, y, rx, ry in ells:
        cx, cy = x * W + pad, y * H + pad
        d.ellipse([cx - rx * W, cy - ry * H, cx + rx * W, cy + ry * H], fill=255)
    return m.filter(ImageFilter.GaussianBlur(1.2))


def build(mid, RW, RH):
    M = MASCOTS[mid]
    ref = MASCOTS[REF]
    base, W, H, pad, canvas = load_pose(M)
    pose = np.asarray(base.crop((pad, pad, pad + W, pad + H)))
    ink = M["ink"]
    body_a = base.getchannel("A")
    # the ghost wisps float in front of everything: split them off the body (all but the largest blob)
    from import_item import regions
    torso = max(regions(np.asarray(body_a) > 128), key=lambda r: r.sum())
    torso_img = Image.fromarray(torso.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(5))
    torso_a = ImageChops.multiply(body_a, torso_img)
    wisps = base.copy()
    wisps.putalpha(ImageChops.multiply(body_a, ImageChops.subtract(body_a, torso_img)))
    chin_px = [(x * W + pad, y * H + pad) for x, y in M["chin"]]
    head_mask = Image.new("L", canvas)              # everything above the jaw line
    ImageDraw.Draw(head_mask).polygon([(0, 0), (canvas[0], 0), (canvas[0], chin_px[-1][1])] + chin_px[::-1] + [(0, chin_px[0][1])], fill=255)
    head_mask = head_mask.filter(ImageFilter.GaussianBlur(1.2))
    sx, sy, srx, sry = M["skull"]
    head_ell = Image.new("L", canvas)
    ImageDraw.Draw(head_ell).ellipse([(sx - srx) * W + pad, (sy - sry) * H + pad, (sx + srx) * W + pad, (sy + sry) * H + pad], fill=255)
    frames = {s: Frame(M, s, ref, RW, RH, W, H) for s in ("head", "neck", "back")}
    grip = M["grip"]
    gx_px, gy_px = grip[0] * W + pad, grip[1] * H + pad
    paws = ellipses(canvas, M.get("grip_mask", []), W, H, pad)

    def hold(layer):                                # the paw closes over what it holds
        if M["grip_kind"] == "paw":
            layer.alpha_composite(fp.paw(canvas, gx_px, gy_px, W))
        else:
            layer.alpha_composite(fp.cut(base, ImageChops.multiply(paws, torso_img)))
        return layer

    layers = {"body": base, "wisps": wisps}
    items = []
    catalog = list(CATALOG) + [(f, i, n, s, dict(own=f)) for f, i, n, s in M.get("own", [])]
    for files, iid, name, slot, p in catalog:
        thumb = None
        if p.get("own"):                            # the companion's own item, cut from its original pose
            own = Image.open(GEN / mid / f"{files}.png").convert("RGBA")
            layer = Image.new("RGBA", canvas)
            layer.alpha_composite(own, (pad, pad))
            if slot == "hand":
                hold(layer)
            thumb = own.crop(own.getbbox())
        elif p.get("pair") == "paws":
            l, r = load("18"), load("19")
            layer = worn_gloves(pose, l, M, W, H, pad, canvas)
            thumb = Image.new("RGBA", (l.width + r.width + 20, max(l.height, r.height)))
            thumb.alpha_composite(l, (0, 0)); thumb.alpha_composite(r, (l.width + 20, 0))
        elif p.get("pair") == "feet":
            boot = boot_worn(load("14-boot"), ink)    # the front boot is the only complete one
            layer = Image.new("RGBA", canvas)
            top, seed_y = M["foot_rows"]
            for fx in M["feet"]:                      # the boot takes the foot's own shape
                foot = fill_region(pose, [(fx, seed_y)], top, 1.0, [(fx - .13, fx + .13)])
                layer.alpha_composite(front_boot(foot, boot, W, H, pad, canvas, ink))
            thumb = load(files)
        else:
            art = load(files)
            thumb = art
            if p.get("worn") == "top":                # a top covers the torso and both arms
                cx, cy = zip(*M["chin"])
                chin = lambda x: (np.interp(x / W, cx, cy) + .012) * H
                body = fill_region(pose, M["torso"], chin, M["torso_bottom"], drop_white=M["drop_white"])
                arms = fill_region(pose, [a[0] for a in M["arms"]], M["arm_rows"][0], M["arm_rows"][1], [a[1] for a in M["arms"]])
                body &= np.asarray(torso_img.crop((pad, pad, pad + W, pad + H))) > 0
                layer = texture_into(body | arms, art, W, H, pad, canvas, (.02, .05, .02, .03))
            elif slot == "hand":
                h = p["h"] * RH * M["hand_scale"]
                art = art.resize((max(1, round(art.width * h / art.height)), max(1, round(h))), Image.LANCZOS)
                gx, gy = p["grip"]
                if p.get("mirror"):  # point long items away from the body
                    art, gx = art.transpose(Image.FLIP_LEFT_RIGHT), 1 - gx
                layer = Image.new("RGBA", canvas)
                if p.get("fly"):  # kite flies up beside the head; a string runs from the paw to it
                    kx, ky = M["fly"][0] * W + pad, M["fly"][1] * H + pad
                    k = 4
                    s = Image.new("RGBA", (canvas[0] * k, canvas[1] * k))
                    ImageDraw.Draw(s).line([gx_px * k, gy_px * k, kx * k, ky * k], fill=ink + (255,), width=3 * k)
                    layer.alpha_composite(s.resize(canvas, Image.LANCZOS))
                    layer.alpha_composite(art, (round(kx - gx * art.width), round(ky - gy * art.height)))
                else:
                    layer.alpha_composite(art, (round(gx_px - gx * art.width), round(gy_px - gy * art.height)))
                hold(layer)
            else:
                fr = frames["back" if slot in ("back", "shoulders") else slot]
                edge = "bottom" if "bottom" in p else "top" if "top" in p else "cy"
                if slot == "neck":
                    art = fp.bend(art, -0.028 * RH * fr.k)
                X, Y = fr.pt(p["x"], p[edge])
                layer = put_px(canvas, art, X, Y, edge, p["w"] * RW * fr.k, pad)
                if p.get("band"):  # the scarf goes all the way round the neck, knot on top
                    layer = Image.alpha_composite(neck_band(art, M["chin"], W, H, pad, canvas, torso_a, ink, fr.k * RH / 825), layer)
                if slot == "neck":
                    erase(layer, head_mask)          # tucked under the chin
                if slot == "head" and p.get("wrap"):
                    a = np.asarray(layer.getchannel("A")) > 0
                    ys = np.nonzero(a.any(1))[0]
                    mid_y = ys[0] + (ys[-1] - ys[0]) * p["wrap"]  # ring's back half sits above this line
                    behind = Image.new("L", canvas)
                    ImageDraw.Draw(behind).rectangle([0, 0, canvas[0], mid_y], fill=255)
                    erase(layer, ImageChops.multiply(ImageChops.multiply(behind, head_ell), body_a))
        layers[iid] = layer
        layers[iid + "-sh"] = fp.shadow([layer], base, H)
        items.append({"id": iid, "name": name, "slot": slot, "slotVi": SLOT_VI[slot], "z": Z[slot], "_thumb": thumb})

    box = None
    for img in layers.values():
        b = img.getchannel("A").point(lambda v: 255 if v > 6 else 0).getbbox()
        if b:
            box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3]))
    out = OUT / mid / "layers"
    out.mkdir(parents=True, exist_ok=True)
    for f in out.glob("*.webp"):
        f.unlink()
    size = (round((box[2] - box[0]) * 900 / (box[3] - box[1])), 900)
    for name, img in layers.items():
        img.crop(box).resize(size, Image.LANCZOS).save(out / f"{name}.webp", quality=88, method=6)
    thumbs = OUT / "thumbs"
    thumbs.mkdir(parents=True, exist_ok=True)
    for e in items:
        t = e.pop("_thumb")
        t.thumbnail((200, 200), Image.LANCZOS)
        t.save(thumbs / f"{e['id']}.webp", quality=90)
    print(mid, len(items), "items", size)
    return {"id": mid, "name": M["name"], "size": size, "items": items}


def main():
    RW, RH = Image.open(fp.ROOT / MASCOTS[REF]["pose"]).size
    only = sys.argv[1:]
    if not only:
        for f in (OUT / "thumbs").glob("*.webp"):
            f.unlink()
    for old in ("layers",):                         # the single-companion layout (before Wuwu and Dudu)
        for f in (OUT / old).glob("*.webp"):
            f.unlink()
        if (OUT / old).exists():
            (OUT / old).rmdir()
    done = {}
    if only and (OUT / "data.json").exists():       # rebuilding some companions: keep the others
        done = {m["id"]: m for m in json.loads((OUT / "data.json").read_text(encoding="utf-8"))["mascots"]}
    for m in MASCOTS:
        if not only or m in only:
            done[m] = build(m, RW, RH)
    mascots = [done[m] for m in MASCOTS if m in done]
    outfits = [
        {"name": "Nhà du hành gió", "ids": ["mu-chin-tang-gio", "khan-gio", "dieu-gio-chay"]},
        {"name": "Người canh trăng", "ids": ["vong-dom-dom", "mat-day-vong-trang", "canh-nho"]},
        {"name": "Rừng thức dậy", "ids": ["mu-tan-bong-bay", "khan-la-biet-bay", "gio-hat-mam", "giay-la"]},
        {"name": "Thợ săn đom đóm", "ids": ["vong-dom-dom", "chuoi-hat-go", "tui-la"]},
        {"name": "Hiệp sĩ măng", "ids": ["mu-mang-bay-dot", "ao-choang-la", "gang-tay-la", "giay-la"]},
        {"name": "Tiên nhỏ", "ids": ["hoa-hai-mau", "no-la", "canh-nho", "dua-la"]},
        {"name": "Dudu thường ngày", "ids": ["non-la-dudu", "gay-tre"]},
    ]
    (OUT / "data.json").write_text(json.dumps({"mascots": mascots, "outfits": outfits}, ensure_ascii=False),
                                   encoding="utf-8")


if __name__ == "__main__":
    main()
