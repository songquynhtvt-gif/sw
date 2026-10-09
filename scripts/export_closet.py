#!/usr/bin/env python3
"""Export the whole Tủ đồ as one zip: sharp transparent PNGs (+ optional SVG), Hǔhǔ try-ons,
a catalogue CSV and a contact sheet.

Per item it takes assets/closet/approved/<id>.png, else the newest gen file.
PNG: upscaled so the longest side is --size px (default 2048), lightly sharpened.
SVG: traced with vtracer when installed (pip install vtracer); sharp at any size.

  python3 scripts/export_closet.py            # -> exports/tu-do-<date>.zip
  python3 scripts/export_closet.py --size 1024 --no-svg
  python3 scripts/export_closet.py --id mu-la khan-ran --out exports/two.zip
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
from fit_preview import LAYER, export_rig, item_file, sheet, try_on  # noqa: E402

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
    ap.add_argument("--id", nargs="+", help="only these items (default: every item with an image)")
    ap.add_argument("--part-mb", type=float, default=28, help="split into zips of at most this size")
    ap.add_argument("--out", type=Path, default=ROOT / f"exports/tu-do-{date.today():%Y%m%d}.zip")
    args = ap.parse_args()

    args.out = args.out.resolve()
    svg = not args.no_svg
    if svg:
        try:
            import vtracer  # noqa: F401
        except ImportError:
            print("vtracer not installed: PNG only (pip install vtracer for SVG)")
            svg = False

    rows, missing, groups = [], [], []  # groups: one list of (zip path, bytes) per item, kept together
    table = io.StringIO()
    w = csv.writer(table)
    w.writerow(["id", "name", "wave", "slot", "price", "status", "png", "source"])
    for it in CLOSET["items"]:
        if args.id and it["id"] not in args.id:
            continue
        src = item_file(it["id"])
        if src is None:
            missing.append(it["id"])
            continue
        raw = Image.open(src).convert("RGBA")
        img = sharpen(raw, args.size)
        buf = io.BytesIO()
        img.save(buf, "PNG", optimize=True)
        name = f"png/{it['wave']}/{it['id']}.png"
        group = [(name, buf.getvalue())]
        if svg:
            small = io.BytesIO()
            raw.crop(raw.getbbox()).save(small, "PNG")  # trace the source: fewer paths, same look
            group.append((f"svg/{it['wave']}/{it['id']}.svg", to_svg(small.getvalue()).encode()))
        if it["slot"] in LAYER:
            group.append((f"fit/huhu-{it['id']}.png", try_on([it["id"]]).read_bytes()))
        groups.append(group)
        w.writerow([it["id"], it["name"], it["wave"], it["slot"], it["price"], it["status"], name,
                    src.relative_to(ROOT)])
        rows.append((it, img))
        print(f"✓ {it['id']} {img.size[0]}×{img.size[1]}")

    head = [("catalogue.csv", ("\ufeff" + table.getvalue()).encode())]  # BOM so Excel reads Vietnamese
    if rows:
        buf = io.BytesIO()
        contact_sheet(rows).save(buf, "PNG")
        head.append(("contact-sheet.png", buf.getvalue()))
    if not args.id:  # whole catalogue: outfits, the dressed sheet and the app rig
        for o in CLOSET.get("outfits", []):
            if all(item_file(x) for x in o["ids"]):
                head.append((f"fit/outfit-{'+'.join(o['ids'])}.png", try_on(o["ids"]).read_bytes()))
        head.append(("huhu-mac-do.png", sheet().read_bytes()))
        for f in sorted(export_rig().iterdir()):
            head.append((f"rig/huhu-front/{f.name}", f.read_bytes()))

    # pack into zips under --part-mb each (chat uploads cap at 30 MB)
    limit = args.part_mb * 1024 * 1024
    parts, size = [[]], 0
    for group in [head] + groups:
        g = sum(len(b) for _, b in group)
        if parts[-1] and size + g > limit:
            parts.append([])
            size = 0
        parts[-1].extend(group)
        size += g
    args.out.parent.mkdir(parents=True, exist_ok=True)
    outs = [args.out] if len(parts) == 1 else \
        [args.out.with_name(f"{args.out.stem}-{k}of{len(parts)}.zip") for k in range(1, len(parts) + 1)]
    for out, entries in zip(outs, parts):
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
            for name, data in entries:
                z.writestr(name, data)
        print(f"→ {out.relative_to(ROOT)} ({out.stat().st_size / 1e6:.1f} MB, {len(entries)} files)")

    print(f"\n{len(rows)} items")
    if missing:
        print(f"no image yet ({len(missing)}): {' '.join(missing)}")


if __name__ == "__main__":
    main()
