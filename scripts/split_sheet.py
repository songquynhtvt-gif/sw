#!/usr/bin/env python3
"""Cut ChatGPT item sheets (prompts/closet/ALL-CHATGPT.md) into single Tủ đồ items.

For each sheet: remove the white background, find every drawn shape, give each
shape to the grid cell its centre falls in (so an item that spills over a cell
edge stays whole), then save assets/closet/gen/<id>-v<n>.png per item, log the
run in items.json and make a try-on image on Hǔhǔ for each wearable item.

Examples:
  python3 scripts/split_sheet.py materials/chatgpt-designs/closet/      # every <sheet-id>.png in the folder
  python3 scripts/split_sheet.py w3-1 ~/Downloads/ChatGPT-Image.png     # one sheet
  python3 scripts/split_sheet.py --list                                 # sheet ids and their items
"""
import argparse
import sys
from collections import deque
from pathlib import Path

from PIL import Image, ImageChops, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_prompts import ROOT, sheets  # noqa: E402
from fit_preview import LAYER, try_on  # noqa: E402
from gen_closet import OUT, log_run, next_version  # noqa: E402
from import_item import keeps_shadow, remove_white, strip_shadow, tidy  # noqa: E402
import upscale  # noqa: E402

SCALE = 4          # find shapes on a 1/4 size mask, fast enough in pure Python
MIN_SHARE = 0.0005  # shapes smaller than this share of the sheet are specks
EXTS = (".png", ".jpg", ".jpeg", ".webp")


def components(mask):
    """Connected shapes of a small 1-bit mask -> list of sets of (x, y)."""
    w, h = mask.size
    px = mask.load()
    seen = set()
    out = []
    for y in range(h):
        for x in range(w):
            if px[x, y] and (x, y) not in seen:
                comp, queue = set(), deque([(x, y)])
                seen.add((x, y))
                while queue:
                    cx, cy = queue.popleft()
                    comp.add((cx, cy))
                    for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                        if 0 <= nx < w and 0 <= ny < h and px[nx, ny] and (nx, ny) not in seen:
                            seen.add((nx, ny))
                            queue.append((nx, ny))
                out.append(comp)
    return out


CACHE = ROOT / "tools/cache/sheets"


def load_sheet(sheet_path, ai):
    """The sheet, AI-upscaled 2x when the Real-ESRGAN models are installed (cached)."""
    img = Image.open(sheet_path)
    if not ai or not upscale.available():
        return img
    cached = CACHE / f"{sheet_path.stem}-x2.png"
    if cached.exists() and cached.stat().st_mtime > sheet_path.stat().st_mtime:
        return Image.open(cached)
    print(f"  AI upscale {sheet_path.name} (2-3 min on CPU)…", flush=True)
    big = upscale.upscale(img, 2)
    CACHE.mkdir(parents=True, exist_ok=True)
    big.save(cached)
    return big


def split(sheet_path, cols, rows, n, tolerance, ai=True):
    img = remove_white(load_sheet(sheet_path, ai), tolerance)
    W, H = img.size
    small = img.getchannel("A").resize((W // SCALE, H // SCALE))
    small = small.point(lambda a: 255 if a > 32 else 0).filter(ImageFilter.MaxFilter(5))  # join beads, strings
    cells = [[] for _ in range(n)]
    for comp in components(small.convert("1")):
        if len(comp) < MIN_SHARE * small.width * small.height:
            continue
        cx = sum(p[0] for p in comp) / len(comp) * SCALE
        cy = sum(p[1] for p in comp) / len(comp) * SCALE
        idx = min(int(cy * rows / H), rows - 1) * cols + min(int(cx * cols / W), cols - 1)
        if idx < n:
            cells[idx].append(comp)
    pieces = []
    for comps in cells:
        if not comps:
            pieces.append(None)
            continue
        keep = Image.new("L", small.size, 0)
        kp = keep.load()
        for comp in comps:
            for p in comp:
                kp[p] = 255
        keep = keep.resize((W, H), Image.NEAREST)
        item = img.copy()
        item.putalpha(ImageChops.multiply(img.getchannel("A"), keep))
        pieces.append(item.crop(item.getbbox()))
    return pieces


def run(sheet_id, path, table, tolerance, ai=True):
    if sheet_id not in table:
        print(f"✗ {path.name}: no sheet called {sheet_id} (see --list)")
        return
    cols, rows, items = table[sheet_id]
    pieces = split(path, cols, rows, len(items), tolerance, ai)
    for it, piece in zip(items, pieces):
        if piece is None:
            print(f"✗ {sheet_id} · {it['id']}: nothing found in its cell, regenerate the sheet")
            continue
        if not keeps_shadow(it):
            piece = strip_shadow(piece)
        piece = tidy(piece)
        piece = piece.crop(piece.getbbox())
        out = OUT / f"{it['id']}-v{next_version(it['id'])}.png"
        OUT.mkdir(parents=True, exist_ok=True)
        piece.save(out)
        rel = str(out.relative_to(ROOT))
        log_run(it["id"], [rel], f"chatgpt sheet {sheet_id}")
        line = f"✓ {sheet_id} · {it['id']}: {rel}"
        if it["slot"] in LAYER:
            line += f" · try-on {try_on([it['id']], files=[rel]).relative_to(ROOT)}"
        print(line)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", nargs="?", help="a folder of <sheet-id>.png files, or a sheet id")
    ap.add_argument("image", nargs="?", type=Path, help="the sheet image when target is a sheet id")
    ap.add_argument("--tolerance", type=int, default=24)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--no-ai", action="store_true", help="skip the Real-ESRGAN upscale")
    args = ap.parse_args()

    table = {sid: (cols, rows, items) for sid, cols, rows, items in sheets()}
    if args.list:
        for sid, (_, _, items) in table.items():
            print(f"{sid:12} " + " · ".join(i["id"] for i in items))
        return
    if not args.target:
        sys.exit("give a folder, or a sheet id + image (see --help)")

    folder = Path(args.target)
    if args.image is None and folder.is_dir():
        files = sorted(p for p in folder.iterdir() if p.suffix.lower() in EXTS)
        if not files:
            sys.exit(f"no images in {folder}")
        for p in files:
            run(p.stem, p, table, args.tolerance, not args.no_ai)
    elif args.image:
        run(args.target, args.image, table, args.tolerance, not args.no_ai)
    else:
        sys.exit(f"{args.target} is not a folder; for one sheet pass: <sheet-id> <image>")


if __name__ == "__main__":
    main()
