#!/usr/bin/env python3
"""AI upscale (Real-ESRGAN anime, ncnn on CPU) for ChatGPT sheets and items.

Models are not in the repo: run once
  python3 scripts/upscale.py --setup        # downloads the official Real-ESRGAN ncnn release into tools/esrgan/
then
  python3 scripts/upscale.py in.png out.png --scale 2

split_sheet.py calls upscale() on every sheet before cutting when the models are present.
"""
import argparse
import io
import sys
import zipfile
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
MODELS = ROOT / "tools/esrgan/models"
RELEASE = ("https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/"
           "realesrgan-ncnn-vulkan-20220424-ubuntu.zip")
MODEL = "realesrgan-x4plus-anime"  # 4x, tuned for flat illustration
TILE, PAD = 192, 12

_net = None


def available():
    return (MODELS / f"{MODEL}.param").exists()


def setup():
    import requests
    print("downloading", RELEASE)
    data = requests.get(RELEASE, timeout=300).content
    MODELS.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for name in z.namelist():
            if name.startswith("models/") and name.endswith((".param", ".bin")):
                (MODELS / Path(name).name).write_bytes(z.read(name))
    print("models in", MODELS.relative_to(ROOT))


def net():
    global _net
    if _net is None:
        import ncnn
        _net = ncnn.Net()
        _net.opt.use_vulkan_compute = False
        _net.opt.num_threads = 4
        _net.load_param(str(MODELS / f"{MODEL}.param"))
        _net.load_model(str(MODELS / f"{MODEL}.bin"))
    return _net


def _run(tile):
    """tile: HxWx3 float32 0..1 -> 4H x 4W x 3."""
    import ncnn
    chw = np.ascontiguousarray(tile.transpose(2, 0, 1))  # keep alive: ncnn.Mat borrows this buffer
    mat = ncnn.Mat(chw)
    ex = net().create_extractor()
    ex.input("data", mat)
    _, out = ex.extract("output")
    return np.array(out).transpose(1, 2, 0).copy()


def upscale(img, scale=2):
    """PIL image -> AI-upscaled 4x, then resized to `scale`x (supersampled). Alpha: Lanczos."""
    rgba = img.convert("RGBA")
    src = np.asarray(rgba.convert("RGB")).astype(np.float32) / 255.0
    h, w, _ = src.shape
    out = np.zeros((h * 4, w * 4, 3), np.float32)
    padded = np.pad(src, ((PAD, PAD), (PAD, PAD), (0, 0)), mode="edge")
    for y in range(0, h, TILE):
        for x in range(0, w, TILE):
            th, tw = min(TILE, h - y), min(TILE, w - x)
            t = padded[y:y + th + 2 * PAD, x:x + tw + 2 * PAD]
            r = _run(t)
            out[y * 4:(y + th) * 4, x * 4:(x + tw) * 4] = r[PAD * 4:(PAD + th) * 4, PAD * 4:(PAD + tw) * 4]
    big = Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8), "RGB")
    size = (w * scale, h * scale)
    big = big.resize(size, Image.LANCZOS) if scale != 4 else big
    if rgba.getextrema()[3][0] < 255:
        big = big.convert("RGBA")
        big.putalpha(rgba.getchannel("A").resize(size, Image.LANCZOS))
    return big


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src", nargs="?", type=Path)
    ap.add_argument("dst", nargs="?", type=Path)
    ap.add_argument("--scale", type=int, default=2, choices=[2, 3, 4])
    ap.add_argument("--setup", action="store_true")
    args = ap.parse_args()
    if args.setup:
        setup()
        return
    if not available():
        sys.exit("models missing: run python3 scripts/upscale.py --setup")
    if not (args.src and args.dst):
        sys.exit("usage: upscale.py in.png out.png [--scale 2]")
    upscale(Image.open(args.src), args.scale).save(args.dst)
    print(args.dst)


if __name__ == "__main__":
    main()
