#!/usr/bin/env python3
"""Generate Tủ đồ items with the OpenAI Images API (GPT image).

Prompts come from scripts/build_prompts.py (rules §7 + prompts/closet/items.json).
Images land in assets/closet/gen/<id>-v<n>.png and each run is logged back
into items.json (status need -> gen).

Setup: put OPENAI_API_KEY in .env (see .env.example). Optional:
OPENAI_IMAGE_MODEL (default gpt-image-1).

Examples:
  python3 scripts/gen_closet.py --list
  python3 scripts/gen_closet.py --id mu-la --dry-run
  python3 scripts/gen_closet.py --wave w3 --n 2
  python3 scripts/gen_closet.py --id khan-ran --ref assets/closet/approved/mu-la.png
"""
import argparse
import base64
import json
import os
import sys
from datetime import date
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_prompts import CLOSET, ROOT, item_prompt  # noqa: E402

ITEMS_FILE = ROOT / "prompts/closet/items.json"
OUT = ROOT / "assets/closet/gen"
API = "https://api.openai.com/v1/images"
REF_LINE = (
    "The attached images are STYLE references only: match their outline, colours and "
    "level of detail exactly. Do not copy their content or draw the character.\n\n"
)


def load_env():
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            key, sep, value = line.partition("=")
            if sep and key.strip() and not key.startswith("#"):
                os.environ.setdefault(key.strip(), value.strip())


def pick(args):
    items = [i for i in CLOSET["items"] if i["status"] != "blocked"]
    if args.id:
        wanted = set(args.id)
        items = [i for i in items if i["id"] in wanted]
        missing = wanted - {i["id"] for i in items}
        if missing:
            sys.exit(f"unknown or blocked id: {', '.join(sorted(missing))}")
    if args.wave:
        items = [i for i in items if i["wave"] == args.wave]
    if args.status:
        items = [i for i in items if i["status"] == args.status]
    return items


def call(prompt, refs, args, key):
    headers = {"Authorization": f"Bearer {key}"}
    fields = {
        "model": args.model,
        "prompt": prompt,
        "n": args.n,
        "size": "1024x1024",
        "quality": args.quality,
        "background": "transparent",
        "output_format": "png",
    }
    if refs:
        files = [("image[]", (p.name, p.read_bytes(), "image/png")) for p in refs]
        data = {k: str(v) for k, v in fields.items()}
        r = requests.post(f"{API}/edits", headers=headers, data=data, files=files, timeout=300)
    else:
        r = requests.post(f"{API}/generations", headers=headers, json=fields, timeout=300)
    if r.status_code != 200:
        raise RuntimeError(f"{r.status_code}: {r.text[:500]}")
    return [base64.b64decode(d["b64_json"]) for d in r.json()["data"]]


def next_version(item_id):
    taken = [int(p.stem.rsplit("-v", 1)[1]) for p in OUT.glob(f"{item_id}-v*.png")
             if p.stem.rsplit("-v", 1)[1].isdigit()]
    return max(taken, default=0) + 1


def log_run(item_id, files, model):
    """Append the run to items.json and move the item from need to gen."""
    data = json.loads(ITEMS_FILE.read_text(encoding="utf-8"))
    for it in data["items"]:
        if it["id"] == item_id:
            it.setdefault("runs", []).append(
                {"date": date.today().isoformat(), "model": model, "files": files, "verdict": ""}
            )
            if it["status"] in ("idea", "need"):
                it["status"] = "gen"
    ITEMS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--id", nargs="+", help="item ids")
    ap.add_argument("--wave", choices=list(CLOSET["waves"]), help="all items of one wave")
    ap.add_argument("--status", help="filter by status, e.g. need")
    ap.add_argument("--n", type=int, default=2, help="variants per item (rules: 2)")
    ap.add_argument("--quality", default="medium", choices=["low", "medium", "high"])
    ap.add_argument("--ref", nargs="+", type=Path, default=[], help="style reference PNGs (approved items)")
    ap.add_argument("--model", default=None)
    ap.add_argument("--list", action="store_true", help="print the catalogue and exit")
    ap.add_argument("--dry-run", action="store_true", help="print prompts, call nothing")
    args = ap.parse_args()

    if args.list:
        for it in CLOSET["items"]:
            print(f"{it['wave']:8} {it['id']:20} {it['slot']:7} {it['price']:>4}  {it['status']:8} {it['name']}")
        return

    items = pick(args)
    if not items or not (args.id or args.wave or args.status):
        sys.exit("pick items with --id, --wave or --status (see --list)")

    load_env()
    args.model = args.model or os.environ.get("OPENAI_IMAGE_MODEL", "gpt-image-1")
    refs = [ROOT / r if not r.is_absolute() else r for r in args.ref]
    for r in refs:
        if not r.exists():
            sys.exit(f"ref not found: {r}")

    print(f"{len(items)} items × {args.n} variants = {len(items) * args.n} images ({args.model}, {args.quality})")
    if args.dry_run:
        for it in items:
            print(f"\n=== {it['id']} ===\n{(REF_LINE if refs else '') + item_prompt(it)}")
        return

    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        sys.exit("OPENAI_API_KEY missing: add it to .env")

    OUT.mkdir(parents=True, exist_ok=True)
    for it in items:
        prompt = (REF_LINE if refs else "") + item_prompt(it)
        try:
            images = call(prompt, refs, args, key)
        except Exception as e:  # keep going: one bad item should not stop the wave
            print(f"✗ {it['id']}: {e}")
            continue
        v = next_version(it["id"])
        files = []
        for i, png in enumerate(images):
            path = OUT / f"{it['id']}-v{v + i}.png"
            path.write_bytes(png)
            files.append(str(path.relative_to(ROOT)))
        log_run(it["id"], files, args.model)
        print(f"✓ {it['id']}: {', '.join(files)}")


if __name__ == "__main__":
    main()
