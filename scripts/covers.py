#!/usr/bin/env python3
"""Mapping bìa truyện: vùng trống trên tranh bìa + điểm neo đặt tên truyện, xuất JSON.

Dùng lại bộ đo độ bận của scripts/copyspace.py. Khác với trang ruột:
  - Mỗi cuốn chỉ có 1 bìa, nên "vị trí giống nhau" được tìm GIỮA CÁC CUỐN: bìa gom theo khổ
    (tỉ lệ khung), ô trống ở >= STABLE_FRAC số bìa trong khổ = vùng ổn định của khổ đó.
  - Chữ đặt lên bìa là tên truyện (hanzi lớn + pinyin), luôn đè lên tranh.
  - Mỗi bìa: dùng vùng ổn định của khổ nếu bìa đó trống ở đấy và chứa vừa tên;
    không thì vùng trống riêng của bìa; không nữa thì dải panel trên/dưới yên nhất.

Dùng:
  python3 scripts/covers.py --status Approve            # -> out/covers/covers.json + overlay/
  python3 scripts/covers.py --all                        # mọi sách dạng ảnh trang
  python3 scripts/covers.py SW-266338 ASB-13623          # vài cuốn
"""
import argparse, json, os, sys
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import copyspace as cs  # noqa: E402

STABLE_FRAC = 0.5       # bìa khác nhau nhiều hơn trang ruột: ô trống ở >= nửa số bìa cùng khổ là ổn định
MIN_COVERS = 5          # khổ có ít hơn số bìa này thì không tính vùng ổn định
TITLE = {"hanzi_px": 56, "pinyin_px": 20, "pad_px": 16, "min_scale": 0.6, "ref_w": 1194}
TITLE_LINE = TITLE["hanzi_px"] * 1.2 + TITLE["pinyin_px"] * 1.3


def title_of(book):
    """Tên truyện bằng tiếng Trung nếu có, kèm nguồn của tên."""
    cover = next((p for p in book["pages"] if p["kind"] == "bìa"), None)
    if cover and cs.CJK.search(cover.get("text") or ""):
        return cover["text"].strip(), "cover_text"
    tr = book.get("translation") or {}
    if tr.get("title_zh"):
        return tr["title_zh"], "translation"
    if cs.CJK.search(book.get("title") or ""):
        return book["title"], "title"
    return book.get("title") or "", "title_en"


def title_len(title):
    n = len(cs.CJK.findall(title))
    return n if n else round(len(title.split()) * 1.4)   # chưa có tên Trung: ước lượng


def title_scale(n, bbox, size):
    """Hệ số cỡ chữ để tên vừa vùng, ảnh bìa hiển thị rộng ref_w px. None nếu dưới min_scale."""
    w, h = size
    s = TITLE["ref_w"] / w
    zw = bbox[2] * w * s - 2 * TITLE["pad_px"]
    zh = bbox[3] * h * s - 2 * TITLE["pad_px"]
    for sc in np.arange(1.0, TITLE["min_scale"] - 1e-6, -0.05):
        if zw > 0 and zh > 0 and int(zw // (TITLE["hanzi_px"] * sc)) * int(zh // (TITLE_LINE * sc)) >= n:
            return round(float(sc), 2)
    return None


def fixed_slot(freq, ref, its):
    """Vị trí tên truyện cố định cho cả khổ bìa: trong các dải đủ chứa tên dài điển hình
    (dải trên/dưới, cột trái/phải), lấy dải trống ở nhiều bìa nhất."""
    G = cs.GRID
    w, h = ref["size"]
    s = TITLE["ref_w"] / w
    need_h = (TITLE_LINE + 2 * TITLE["pad_px"]) / (h * s)          # 1 dòng tên ở cỡ chuẩn
    n_typ = int(np.percentile([title_len(title_of(it["book"])[0]) for it in its], 75))
    need_w = (n_typ * TITLE["hanzi_px"] + 2 * TITLE["pad_px"]) / (w * s)
    hh = min(G, max(2, int(np.ceil(need_h * G))))
    ww = min(G, max(4, int(np.ceil(need_w * G))))
    cands = []
    for t in (0, G - hh):                                    # dải ngang trên / dưới
        for l in range(0, G - ww + 1):
            cands.append((t, l, hh, ww))
    vh = min(G, hh * 2)
    vw = min(G, max(4, int(np.ceil(need_w * G / 2))))      # cột dọc: tên xuống 2 dòng
    for l in (0, G - vw):
        for t in range(0, G - vh + 1):
            cands.append((t, l, vh, vw))
    t, l, hh_, ww_ = max(cands, key=lambda r: (freq[r[0]:r[0] + r[2], r[1]:r[1] + r[3]].mean(),
                                                -abs(r[1] + r[3] / 2 - G / 2)))   # hoà thì ưu tiên giữa
    z = cs.zone("slot", (t, l, hh_, ww_), ref)
    z["empty_freq"] = round(float(freq[t:t + hh_, l:l + ww_].mean()), 3)
    z["typical_title_len"] = n_typ
    return z


def fmt_key(size):
    """Khổ bìa: tỉ lệ khung làm tròn, gom các ảnh lệch vài px về cùng khổ."""
    r = size[0] / size[1]
    for name, ref in (("wide", 2.09), ("square", 1.0), ("landscape", 1.33), ("portrait", 0.75)):
        if abs(r - ref) / ref < 0.08:
            return name
    return f"r{r:.2f}"


def load(book_id, cache):
    book = cs.load_book(book_id, cache)
    cover = next((p for p in book["pages"] if p["kind"] == "bìa" and p.get("_local")), None)
    return book, cover


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--status")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--cache", default="out/cache")
    ap.add_argument("--out", default="out/covers")
    ap.add_argument("--no-overlay", action="store_true")
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()

    ids = list(args.ids)
    if args.all or args.status:
        lst = json.loads(cs.get(f"{cs.BASE}/v1/pilot/books"))["books"]
        ids += [b["id"] for b in lst if b["view"] == "pages"
                and (not args.status or b["review"]["status"] == args.status)]
    ids = ids[:args.limit] if args.limit else ids
    if not ids:
        ap.error("cần id sách hoặc --all / --status")

    def one(bid):
        try:
            book, cover = load(bid, args.cache)
            if not cover:
                return {"id": bid, "error": "không có ảnh bìa"}
            return {"id": bid, "book": book, "cover": cover, "a": cs.analyse(cover["_local"])}
        except Exception as e:
            return {"id": bid, "error": repr(e)}

    with ThreadPoolExecutor(args.workers) as ex:
        items = list(ex.map(one, ids))
    ok = [it for it in items if "a" in it]

    # khổ bìa + vùng ổn định giữa các cuốn
    formats = {}
    for it in ok:
        it["fmt"] = fmt_key(it["a"]["size"])
        it["empty"] = it["a"]["busy"] < cs.EMPTY_T
        formats.setdefault(it["fmt"], []).append(it)
    fmt_out = []
    for name, its in sorted(formats.items(), key=lambda kv: -len(kv[1])):
        freq = np.stack([it["empty"] for it in its]).mean(0)
        ref = {"size": its[0]["a"]["size"],
               "busy": np.mean([it["a"]["busy"] for it in its], 0),
               "color": np.mean([it["a"]["color"] for it in its], 0)}
        zones = []
        if len(its) >= MIN_COVERS:
            zones = [cs.zone(f"{name}-S{j + 1}", r, ref, float(freq[r[0]:r[0] + r[2], r[1]:r[1] + r[3]].mean()))
                     for j, r in enumerate(cs.rects(freq >= STABLE_FRAC, min_w=0.2, min_h=0.12))]
        slot = fixed_slot(freq, ref, its)
        fmt_out.append({"format": name, "aspect": round(ref["size"][0] / ref["size"][1], 2),
                        "covers": len(its), "title_slot": slot, "stable_zones": zones,
                        "empty_freq": [[round(float(v), 2) for v in row] for row in freq]})
        for it in its:
            it["fmt_zones"], it["fmt_slot"] = zones, slot

    covers = []
    for it in ok:
        a, book, empty = it["a"], it["book"], it["empty"]
        title, tsrc = title_of(book)
        n = title_len(title)
        own = [cs.zone(f"Z{j + 1}", r, a) for j, r in enumerate(cs.rects(empty, min_w=0.25, min_h=0.15))]
        slot = it["fmt_slot"]
        t, l = round(slot["bbox"][1] * cs.GRID), round(slot["bbox"][0] * cs.GRID)
        hh, ww = round(slot["bbox"][3] * cs.GRID), round(slot["bbox"][2] * cs.GRID)
        chosen = cs.zone(slot["id"], (t, l, hh, ww), a)
        calm = float(empty[t:t + hh, l:l + ww].mean())
        # tranh ở vị trí cố định có trống không: trống hẳn thì để chữ trần, lấn một phần thì nền mờ, bận thì panel
        chosen["scrim"] = None if calm >= 0.9 and chosen["contrast"] >= 4.5 else (
            ("cream" if chosen["ink"] == cs.INK["dark"] else "forest") if calm >= 0.5 else "panel-onart")
        if chosen["scrim"] == "panel-onart":
            chosen["ink"] = cs.INK["dark"]
        src = "fixed"
        sc = title_scale(n, chosen["bbox"], a["size"])
        alt = next((z for z in own if title_scale(n, z["bbox"], a["size"])), None)
        c = it["cover"]
        covers.append({
            "id": book["id"], "source": book["source"], "lang": book["lang"],
            "image": cs.BASE + c["image"], "size": list(a["size"]), "format": it["fmt"],
            "title": title, "title_source": tsrc, "title_len": n,
            "empty_ratio": round(float(empty.mean()), 3),
            "zones": own,
            "title_slot": {"zone_id": chosen["id"], "source": src, "calm": round(calm, 2), "bbox": chosen["bbox"],
                           "position": chosen["position"], "anchor": chosen["anchor"],
                           "ink": chosen["ink"], "contrast": chosen["contrast"], "scrim": chosen["scrim"],
                           "font_scale": sc if sc else TITLE["min_scale"], "fits": sc is not None},
            "alt_slot": alt and {"zone_id": alt["id"], "bbox": alt["bbox"], "position": alt["position"],
                                 "anchor": alt["anchor"], "ink": alt["ink"], "scrim": alt["scrim"],
                                 "font_scale": title_scale(n, alt["bbox"], a["size"])},
        })
        if not args.no_overlay:
            draw(it, chosen, alt, os.path.join(args.out, "overlay", f"{book['id']}.jpg"))

    covers.sort(key=lambda c: c["id"])
    res = {
        "schema": "covers/v1",
        "params": {"grid": cs.GRID, "empty_t": cs.EMPTY_T, "blank_t": cs.BLANK_T,
                   "stable_frac": STABLE_FRAC, "min_covers": MIN_COVERS, "title": TITLE},
        "formats": fmt_out,
        "covers": covers,
        "errors": [{"id": it["id"], "error": it["error"]} for it in items if "error" in it],
        "summary": {
            "covers": len(covers),
            "clean": sum(c["title_slot"]["scrim"] is None for c in covers),
            "soft_scrim": sum(c["title_slot"]["scrim"] in ("cream", "forest") for c in covers),
            "panel": sum(c["title_slot"]["scrim"] == "panel-onart" for c in covers),
            "has_alt_slot": sum(bool(c["alt_slot"]) for c in covers),
            "not_fit": sum(not c["title_slot"]["fits"] for c in covers),
            "no_zh_title": sum(c["title_source"] == "title_en" for c in covers),
        },
    }
    os.makedirs(args.out, exist_ok=True)
    json.dump(res, open(os.path.join(args.out, "covers.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(res["summary"], ensure_ascii=False))
    for f in fmt_out:
        print(f["format"], f["covers"], f["title_slot"]["position"], f["title_slot"]["bbox"], f["title_slot"]["empty_freq"])


def draw(it, chosen, alt, path):
    im = Image.open(it["cover"]["_local"]).convert("RGB")
    w, h = im.size
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    cw, ch = w / cs.GRID, h / cs.GRID
    for r in range(cs.GRID):
        for c in range(cs.GRID):
            if not it["empty"][r, c]:
                d.rectangle([c * cw, r * ch, (c + 1) * cw, (r + 1) * ch], fill=(220, 40, 40, 45))
    lw = max(2, w // 200)

    def box(bb, col, wd):
        d.rectangle([bb[0] * w, bb[1] * h, (bb[0] + bb[2]) * w, (bb[1] + bb[3]) * h], outline=col, width=wd)

    for z in it["fmt_zones"]:
        box(z["bbox"], (40, 120, 255, 255), lw * 2)
    if alt:
        box(alt["bbox"], (255, 190, 0, 255), lw * 2)
    box(chosen["bbox"], (0, 170, 80, 255), lw * 3)
    ax, ay, r = chosen["anchor"]["x"] * w, chosen["anchor"]["y"] * h, lw * 4
    d.ellipse([ax - r, ay - r, ax + r, ay + r], fill=(0, 170, 80, 255), outline=(255, 255, 255, 255), width=lw)
    im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
    im.thumbnail((800, 800))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path, quality=78)


if __name__ == "__main__":
    main()
