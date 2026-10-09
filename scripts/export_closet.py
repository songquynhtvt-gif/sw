#!/usr/bin/env python3
"""Export the whole Tủ đồ as one zip: sharp transparent PNGs (+ optional SVG), Hǔhǔ try-ons,
a catalogue CSV and a contact sheet.

Per item it takes assets/closet/approved/<id>.png, else the newest gen file.
PNG: upscaled so the longest side is --size px (default 2048), lightly sharpened.
SVG: traced with vtracer when installed (pip install vtracer); sharp at any size.

  python3 scripts/export_closet.py            # -> exports/tu-do-<date>.zip
  python3 scripts/export_closet.py --size 1024 --no-svg
"""
import argparse
import csv
import io
import sys
import zipfile
from datetime import date
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_prompts import CLOSET, ROOT  # noqa: E402
from fit_preview import LAYER, item_file, try_on  # noqa: E402

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def sharpen(img, size):
    img = img.crop(img.getbbox())
    k = size / max(img.size)
    if k > 1:
        img = img.resize((round(img.width * k), round(img.height * k)), Image.LANCZOS)
        img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=70, threshold=2))
    pad = round(max(img.size) * 0.04)
    out = Image.new("RGBA", (img.width + 2 * pad, img.height + 2 * pad))
    out.alpha_composite(img, (pad, pad))
    return out


def to_svg(png_bytes):
    import vtracer
    return vtracer.convert_raw_image_to_svg(png_bytes, img_format="png", colormode="color",
                                            filter_speckle=8, color_precision=7, mode="spline")


def contact_sheet(rows, cell=240, cols=6):
    try:
        font = ImageFont.truetype(FONT, 18)
    except OSError:
        font = ImageFont.load_default()
    n = len(rows)
    sheet = Image.new("RGB", (cols * cell, ((n + cols - 1) // cols) * (cell + 34)), (251, 244, 228))
    d = ImageDraw.Draw(sheet)
    for k, (it, img) in enumerate(rows):
        x, y = (k % cols) * cell, (k // cols) * (cell + 34)
        thumb = img.copy()
        thumb.thumbnail((cell - 30, cell - 30))
        sheet.paste(thumb, (x + (cell - thumb.width) // 2, y + 10 + (cell - 30 - thumb.height) // 2), thumb)
        d.text((x + cell // 2, y + cell + 6), f"{it['name']} · {it['price']}", fill=(27, 42, 107), font=font, anchor="mt")
    return sheet


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--size", type=int, default=2048, help="longest side of each PNG")
    ap.add_argument("--no-svg", action="store_true")
    ap.add_argument("--out", type=Path, default=ROOT / f"exports/tu-do-{date.today():%Y%m%d}.zip")
    args = ap.parse_args()

    svg = not args.no_svg
    if svg:
        try:
            import vtracer  # noqa: F401
        except ImportError:
            print("vtracer not installed: PNG only (pip install vtracer for SVG)")
            svg = False

    rows, missing = [], []
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.out, "w", zipfile.ZIP_DEFLATED) as z:
        table = io.StringIO()
        w = csv.writer(table)
        w.writerow(["id", "name", "wave", "slot", "price", "status", "png", "source"])
        for it in CLOSET["items"]:
            src = item_file(it["id"])
            if src is None:
                missing.append(it["id"])
                continue
            raw = Image.open(src).convert("RGBA")
            img = sharpen(raw, args.size)
            buf = io.BytesIO()
            img.save(buf, "PNG", optimize=True)
            name = f"png/{it['wave']}/{it['id']}.png"
            z.writestr(name, buf.getvalue())
            if svg:
                small = io.BytesIO()
                raw.crop(raw.getbbox()).save(small, "PNG")  # trace the source: fewer paths, same look
                z.writestr(f"svg/{it['wave']}/{it['id']}.svg", to_svg(small.getvalue()))
            if it["slot"] in LAYER:
                z.write(try_on([it["id"]]), f"fit/huhu-{it['id']}.png")
            w.writerow([it["id"], it["name"], it["wave"], it["slot"], it["price"], it["status"], name,
                        src.relative_to(ROOT)])
            rows.append((it, img))
            print(f"✓ {it['id']} {img.size[0]}×{img.size[1]}")
        z.writestr("catalogue.csv", "﻿" + table.getvalue())  # BOM so Excel reads Vietnamese
        if rows:
            buf = io.BytesIO()
            contact_sheet(rows).save(buf, "PNG")
            z.writestr("contact-sheet.png", buf.getvalue())

    print(f"\n{len(rows)} items → {args.out.relative_to(ROOT)}")
    if missing:
        print(f"no image yet ({len(missing)}): {' '.join(missing)}")


if __name__ == "__main__":
    main()
