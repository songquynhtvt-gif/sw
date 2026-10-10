#!/usr/bin/env python3
"""Dress-up base poses for the other companions.

Wuwu: the front idle pose is used as is.
Dudu: his front pose always wears the nón lá and holds a bamboo stick, so both come off:
  - the white background trapped between the stick, arm and head is cleared
  - the bamboo is cut out above and below the fist (the fist stays closed, ready to grip)
  - the hat is cut out and the head top is redrawn: a round fur dome and two floppy ears
    behind what is left of the head
  - the hat and the stick are kept as his own items (pose-framed, they go back exactly)
Output: assets/char/gen/<companion>/<companion>-dressup-base.png (+ dudu-own-hat.png, dudu-own-bamboo.png)
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
GEN = ROOT / "assets/char/gen"


def grow(mask, px):
    m = Image.fromarray(mask.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(px * 2 + 1))
    return np.asarray(m) > 0


def flood(mask, seed):
    work = Image.fromarray(mask.astype(np.uint8) * 255).copy()
    ImageDraw.floodfill(work, seed, 128, thresh=0)
    return np.asarray(work) == 128


def keep(img, mask):
    out = img.copy()
    out.putalpha(ImageChops.multiply(img.getchannel("A"), Image.fromarray(mask.astype(np.uint8) * 255)))
    return out


def ellipse_layer(size, box, fill, ink, lw, angle=0, k=4):
    """A filled, outlined ellipse (optionally rotated about its centre), supersampled."""
    W, H = size
    x0, y0, x1, y1 = box
    cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y1 - y0) / 2
    t = np.linspace(0, 2 * np.pi, 180)
    a = np.radians(angle)
    pts = [((cx + rx * np.cos(s) * np.cos(a) - ry * np.sin(s) * np.sin(a)) * k,
            (cy + rx * np.cos(s) * np.sin(a) + ry * np.sin(s) * np.cos(a)) * k) for s in t]
    img = Image.new("RGBA", (W * k, H * k))
    ImageDraw.Draw(img).polygon(pts, fill=fill + (255,), outline=ink + (255,), width=round(lw * k))
    return img.resize(size, Image.LANCZOS)


def dudu():
    src = Image.open(GEN / "dudu/dudu-front-idle-bamboo.png").convert("RGBA")
    W, H = src.size
    a = np.asarray(src).astype(int)
    r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    op = al > 128
    ys, xs = np.mgrid[0:H, 0:W]
    ink = (91, 28, 3)
    dark = op & (r + g + b < 170)
    sys.path.insert(0, str(ROOT / "scripts"))
    from import_item import regions
    main = max(regions(op), key=lambda m: m.sum())   # body + hat + stick; the ghost wisps are apart
    green = main & (g > r + 10) & (g >= b)

    white = flood(op & (r > 236) & (g > 236) & (b > 236), (round(.29 * W), round(.47 * H)))
    lum = (r * 299 + g * 587 + b * 114) // 1000
    white |= grow(white, 4) & (lum > 120) & ~((r > 200) & (g < 175))   # its anti-aliased rim

    stick = green & (ys > .365 * H) & (xs < .31 * W)
    outside_fist = (ys < .523 * H) | (ys > .684 * H)
    orange = (r > 200) & (g < 175) & (b < 130)        # the ear behind the stick stays
    bamboo = grow(stick, 15) & main & outside_fist & (xs < .30 * W) & ~(orange & ~grow(stick, 2)) & ~white

    sys.path.insert(0, str(ROOT / "scripts"))
    cap = green & (ys < .37 * H)
    hat = cap | (grow(cap, 13) & dark & (ys < .40 * H))
    hat = grow(hat, 1) & (cap | dark | grow(cap, 3))

    fur = tuple(int(v) for v in np.median(a[op & (ys > .27 * H) & (ys < .33 * H) & (xs > .33 * W) & (xs < .40 * W)][:, :3], axis=0))
    ear = tuple(int(v) for v in np.median(a[op & (ys > .37 * H) & (ys < .42 * H) & (xs > .86 * W) & (xs < .90 * W)][:, :3], axis=0))

    # what the hat brim left on the face and ears: its shadow band, cut brows, specks -> dome fur shows
    def rect(x0, y0, x1, y1):
        return (xs > x0 * W) & (xs < x1 * W) & (ys > y0 * H) & (ys < y1 * H)
    brim = rect(.28, .10, .82, .252) & (lum < 175)
    brim |= rect(.27, .10, .83, .33) & (r > 165) & (r < 242) & (g > 65) & (g < 125) & (b < 85)  # hat shadow
    brim |= (rect(.27, .23, .365, .31) | rect(.76, .23, .83, .31)) & (lum < 150)   # old head outline under the brim
    dome = ((xs / W - .548) / .272) ** 2 + ((ys / H - .36) / .24) ** 2 < 1
    # the old ears were half under the brim and half behind the stick: drop them, new ears go behind
    brim |= (rect(.12, .24, .30, .523) | rect(.76, .22, .97, .48)) & ~dome
    brim |= rect(.12, .50, .30, .70) & green
    brow = tuple(int(v) for v in np.median(a[rect(.48, .235, .51, .26) & op][:, :3], axis=0))
    brim &= main
    body = keep(src, op & ~white & ~bamboo & ~hat & ~brim)
    lw = .011 * W
    base = Image.new("RGBA", src.size)
    for cx, ang in ((.865, -28), (.245, 28)):     # floppy ears hanging from the head sides
        base.alpha_composite(ellipse_layer(src.size, ((cx - .062) * W, .275 * H, (cx + .062) * W, .465 * H), ear, ink, lw, ang))
    dome_l = ellipse_layer(src.size, (.276 * W, .12 * H, .82 * W, .60 * H), fur, ink, lw)  # head dome
    top = Image.fromarray((np.clip((.335 * H - ys) / 3, 0, 1) * 255).astype(np.uint8))  # only above the face
    dome_l.putalpha(ImageChops.multiply(dome_l.getchannel("A"), top))
    base.alpha_composite(dome_l)
    fist = Image.new("RGBA", (W * 4, H * 4))           # closes the fist outline where the stick crossed it
    ImageDraw.Draw(fist).rounded_rectangle([.128 * W * 4, .53 * H * 4, .268 * W * 4, .684 * H * 4], radius=.045 * W * 4,
                                           fill=fur + (255,), outline=ink + (255,), width=round(lw * 4))
    base.alpha_composite(fist.resize(src.size, Image.LANCZOS))
    base.alpha_composite(body)
    for x0 in (.462, .607):                       # brows, redrawn whole (the brim had cut their tops)
        base.alpha_composite(ellipse_layer(src.size, (x0 * W, .222 * H, (x0 + .062) * W, .268 * H), brow, brow, 1))
    out = GEN / "dudu"
    base.save(out / "dudu-dressup-base.png")
    keep(src, hat & op).save(out / "dudu-own-hat.png")
    keep(src, bamboo & op).save(out / "dudu-own-bamboo.png")
    print("dudu", src.size, "fur", fur, "ear", ear)


def wuwu():
    src = Image.open(GEN / "wuwu/wuwu-front-idle.png").convert("RGBA")
    src.save(GEN / "wuwu/wuwu-dressup-base.png")
    print("wuwu", src.size)


if __name__ == "__main__":
    for name in sys.argv[1:] or ["wuwu", "dudu"]:
        globals()[name]()
