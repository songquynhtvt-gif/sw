#!/usr/bin/env python3
"""Tìm vùng trống (copy space) trên tranh sách pilot, chốt điểm neo đặt chữ, xuất JSON.

Nguồn: https://twc.mikademy.vn (thư viện pilot). Mỗi trang sách = 1 ảnh minh hoạ + text tách riêng,
nên việc cần làm là tìm chỗ trên tranh đủ "yên" để đè hanzi + pinyin lên mà không che nhân vật.

Cách làm (chỉ cần numpy + Pillow):
  1. Mỗi trang: làm mờ nhẹ, thu nhỏ, đo độ "bận" (gradient màu) trên lưới GRID x GRID ô.
     Ô có gradient thấp = trống (nền trắng / trời / mảng màu phẳng).
  2. Gom các trang cùng tỉ lệ khung thành một layout. Ô trống ở >= STABLE_FRAC số trang
     của layout = ô ổn định. Hình chữ nhật lớn nhất trên vùng ổn định = vùng neo cố định
     (identical giữa các trang) -> chữ đứng một chỗ khi lật trang.
  3. Mỗi trang chọn vùng: ưu tiên vùng ổn định còn trống ở trang đó và chứa vừa text;
     không thì vùng riêng của trang; không nữa thì panel nền (panel-onart) ở dải yên nhất.
  4. Xuất JSON toạ độ chuẩn hoá 0..1 (độc lập kích thước ảnh) + ảnh overlay để duyệt.

Dùng:
  python3 scripts/copyspace.py SW-266338                 # 1 cuốn -> out/copyspace/SW-266338.json
  python3 scripts/copyspace.py --status Approve --all    # chạy hàng loạt theo bộ lọc
"""
import argparse, json, math, os, re, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

BASE = "https://twc.mikademy.vn"
GRID = 24              # lưới phân tích GRID x GRID ô
EMPTY_T = 0.03         # gradient trung bình của ô dưới ngưỡng này = trống
BLANK_T = 0.008        # dưới ngưỡng này = gần như phẳng tuyệt đối (giấy trắng, mảng màu)
STABLE_FRAC = 0.8      # ô trống ở >= 80% số trang cùng layout = ô ổn định
MIN_W, MIN_H = 0.25, 0.10   # vùng tối thiểu (tỉ lệ khung ảnh)

# Khung tham chiếu: iPad 11" ngang, cỡ chữ reader trong docs/DESIGN.md
CANVAS = {"w": 1194, "h": 834, "hanzi_px": 44, "pinyin_px": 16, "pad_px": 16, "min_scale": 0.7}
LINE_PX = CANVAS["hanzi_px"] * 1.35 + CANVAS["pinyin_px"] * 1.3   # 1 dòng hanzi + pinyin ~ 80px
INK = {"dark": "#0E4A3A", "light": "#FDF9F0"}                      # forest / cream

CJK = re.compile(r"[㐀-鿿豈-﫿　-〿＀-￯]")


# ---------- tải dữ liệu ----------
def get(url, path=None):
    req = urllib.request.Request(url, headers={"User-Agent": "copyspace/1"})
    data = urllib.request.urlopen(req, timeout=60).read()
    if path:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "wb").write(data)
    return data


def load_book(book_id, cache):
    p = os.path.join(cache, book_id, "book.json")
    if not os.path.exists(p):
        get(f"{BASE}/v1/pilot/books/{book_id}", p)
    book = json.load(open(p))
    for pg in book["pages"]:
        if not pg.get("image"):
            continue
        ext = os.path.splitext(pg["image"])[1] or ".png"
        pg["_local"] = os.path.join(cache, book_id, "pages", f"{pg['n']:02d}{ext}")
        if not os.path.exists(pg["_local"]):
            get(BASE + pg["image"], pg["_local"])
    return book


# ---------- phân tích 1 ảnh ----------
def analyse(path):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    W = 96
    H = max(8, round(h * W / w))
    small = im.filter(ImageFilter.GaussianBlur(w / 100)).resize((W, H), Image.LANCZOS)
    a = np.asarray(small, dtype=np.float32) / 255
    g = np.zeros((H, W), np.float32)
    g[:, :-1] += np.abs(np.diff(a, axis=1)).max(2)
    g[:-1, :] += np.abs(np.diff(a, axis=0)).max(2)
    rs, cs = np.array_split(np.arange(H), GRID), np.array_split(np.arange(W), GRID)
    busy = np.array([[g[np.ix_(r, c)].mean() for c in cs] for r in rs])
    color = np.array([[a[np.ix_(r, c)].reshape(-1, 3).mean(0) for c in cs] for r in rs])
    return {"size": (w, h), "busy": busy, "color": color}


# ---------- tìm hình chữ nhật trống ----------
def rects(mask, min_w=MIN_W, min_h=MIN_H, k=3):
    """Các hình chữ nhật toàn ô True, lớn nhất trước, không chồng nhau. Toạ độ theo ô."""
    G = mask.shape[0]
    cands = []
    for top in range(G):
        col_ok = np.ones(G, bool)
        for bot in range(top, G):
            col_ok &= mask[bot]
            if not col_ok.any():
                break
            hgt = bot - top + 1
            if hgt / G < min_h:
                continue
            c = 0
            while c < G:          # các đoạn cột liên tiếp
                if not col_ok[c]:
                    c += 1
                    continue
                s = c
                while c < G and col_ok[c]:
                    c += 1
                wid = c - s
                if wid / G >= min_w:
                    cands.append((wid * hgt, top, s, hgt, wid))
    cands.sort(reverse=True)
    out, used = [], np.zeros_like(mask)
    for area, t, l, hh, ww in cands:
        if used[t:t + hh, l:l + ww].any():
            continue
        out.append((t, l, hh, ww))
        used[t:t + hh, l:l + ww] = True
        if len(out) == k:
            break
    return out


def luminance(rgb):
    def ch(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(float(x)) for x in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(l1, l2):
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def hex_lum(h):
    return luminance([int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)])


def position_name(x, y, w, h):
    cx, cy = x + w / 2, y + h / 2
    v = "top" if cy < 0.34 else "bottom" if cy > 0.66 else "middle"
    hz = "left" if cx < 0.34 else "right" if cx > 0.66 else "center"
    if v == "middle":
        return "center" if hz == "center" else hz
    return v if hz == "center" else f"{v}-{hz}"


def capacity(bbox, size):
    """Số chữ hanzi chứa được ở cỡ 44px trên khung tham chiếu."""
    w, h = size
    s = min(CANVAS["w"] / w, CANVAS["h"] / h)
    zw, zh = bbox[2] * w * s - 2 * CANVAS["pad_px"], bbox[3] * h * s - 2 * CANVAS["pad_px"]
    if zw <= 0 or zh <= 0:
        return 0, 0, 0
    per_line, lines = int(zw // CANVAS["hanzi_px"]), int(zh // LINE_PX)
    return per_line * lines, per_line, lines


def fit_scale(n_chars, bbox, size):
    """Hệ số thu cỡ chữ cần để text vừa vùng (1.0 = cỡ chuẩn). None nếu dưới min_scale."""
    if n_chars == 0:
        return 1.0
    for sc in np.arange(1.0, CANVAS["min_scale"] - 1e-6, -0.05):
        w, h = size
        s = min(CANVAS["w"] / w, CANVAS["h"] / h)
        zw = bbox[2] * w * s - 2 * CANVAS["pad_px"]
        zh = bbox[3] * h * s - 2 * CANVAS["pad_px"]
        if zw > 0 and zh > 0 and int(zw // (CANVAS["hanzi_px"] * sc)) * int(zh // (LINE_PX * sc)) >= n_chars:
            return round(float(sc), 2)
    return None


def zone(zid, cell_rect, a, stability=None):
    t, l, hh, ww = cell_rect
    x, y, w, h = l / GRID, t / GRID, ww / GRID, hh / GRID
    busy = float(a["busy"][t:t + hh, l:l + ww].mean())
    rgb = a["color"][t:t + hh, l:l + ww].reshape(-1, 3).mean(0)
    L = luminance(rgb)
    ink = "dark" if contrast(L, hex_lum(INK["dark"])) >= contrast(L, hex_lum(INK["light"])) else "light"
    cr = contrast(L, hex_lum(INK[ink]))
    cap, per_line, lines = capacity((x, y, w, h), a["size"])
    z = {
        "id": zid,
        "bbox": [round(x, 4), round(y, 4), round(w, 4), round(h, 4)],     # x, y, w, h (0..1, gốc trên-trái)
        "position": position_name(x, y, w, h),
        "anchor": {                                                        # gốc khối chữ (sau padding)
            "x": round(x + w / 2, 4) if 0.3 < x + w / 2 < 0.7 else round(x, 4),
            "y": round(y, 4),
            "align": "center" if 0.3 < x + w / 2 < 0.7 else ("left" if x + w / 2 <= 0.5 else "right"),
        },
        "bg": "blank" if busy < BLANK_T else "calm",
        "bg_rgb": [int(v * 255) for v in rgb],
        "busy": round(busy, 4),
        "ink": INK[ink],
        "contrast": round(cr, 2),
        "scrim": None if cr >= 4.5 and busy < BLANK_T * 2 else ("cream" if ink == "dark" else "forest"),
        "capacity_hanzi": cap,
        "lines": lines,
        "chars_per_line": per_line,
    }
    if z["anchor"]["align"] == "right":
        z["anchor"]["x"] = round(x + w, 4)
    if stability is not None:
        z["stability"] = round(stability, 3)
    return z


def band_fallback(a, n_chars):
    """Không có vùng trống đủ lớn: chọn dải trên/dưới yên nhất, đặt panel nền."""
    best = None
    for frac in (0.22, 0.3, 0.38):
        hh = max(1, round(frac * GRID))
        for t in (0, GRID - hh):
            b = a["busy"][t:t + hh].mean()
            if best is None or b < best[0]:
                best = (b, (t, 0, hh, GRID))
        if fit_scale(n_chars, (0, 0, 1, frac), a["size"]) is not None:
            break
    z = zone("panel", best[1], a)
    z["bg"] = "busy"
    z["scrim"] = "panel-onart"
    z["ink"] = INK["dark"]
    return z


def text_len(text, lang):
    if lang == "zh":
        return len(CJK.findall(text))
    return len(text.split())


# ---------- 1 cuốn ----------
COLUMN_FRAC = 0.4      # cột chữ chiếm 40% bề ngang khung khi tranh không đủ chỗ trống
OVERLAY_MIN_SCALE = 0.85   # đè chữ lên tranh chỉ khi cỡ chữ giữ được >= 85%
OVERLAY_SHARE = 0.8    # layout dùng chế độ đè chữ khi >= 80% trang vừa vùng ổn định


def art_rect(size, column_side=None):
    """Vị trí tranh trên khung tham chiếu (px). column_side: chừa cột chữ bên trái/phải."""
    cw, ch = CANVAS["w"], CANVAS["h"]
    aw = cw * (1 - COLUMN_FRAC) if column_side else cw
    w, h = size
    s = min(aw / w, ch / h)
    rw, rh = w * s, h * s
    x0 = (cw * COLUMN_FRAC if column_side == "left" else 0) + (aw - rw) / 2
    return [round(x0), round((ch - rh) / 2), round(rw), round(rh)]


def column_slot(side):
    cw, ch = CANVAS["w"], CANVAS["h"]
    x = 0 if side == "left" else cw * (1 - COLUMN_FRAC)
    return [round(x), 0, round(cw * COLUMN_FRAC), ch]


def column_fit(n_chars, rect):
    """Cỡ chữ cho cột (rect px trên khung)."""
    for sc in np.arange(1.0, CANVAS["min_scale"] - 1e-6, -0.05):
        zw, zh = rect[2] - 2 * CANVAS["pad_px"], rect[3] - 2 * CANVAS["pad_px"]
        if int(zw // (CANVAS["hanzi_px"] * sc)) * int(zh // (LINE_PX * sc)) >= n_chars:
            return round(float(sc), 2)
    return None


def to_canvas(bbox, ar):
    x, y, w, h = bbox
    return [round(ar[0] + x * ar[2]), round(ar[1] + y * ar[3]), round(w * ar[2]), round(h * ar[3])]


def run_book(book, out_dir, overlay=True):
    pages = [p for p in book["pages"] if p.get("_local")]
    for p in pages:
        p["_a"] = analyse(p["_local"])
        txt = p.get("text") or ""
        p["_n"] = text_len(txt, book["lang"])
        # tiếng Anh chưa chuyển ngữ: ước lượng ~1.4 hanzi / từ
        p["_nz"] = p["_n"] if book["lang"] == "zh" else round(p["_n"] * 1.4)
        p["_empty"] = p["_a"]["busy"] < EMPTY_T

    # gom layout theo tỉ lệ khung; bìa tách riêng
    groups = {}
    for p in pages:
        w, h = p["_a"]["size"]
        key = ("cover" if p["kind"] == "bìa" else "page", round(w / h, 2))
        groups.setdefault(key, []).append(p)

    layouts = []
    for i, ((kind, ratio), ps) in enumerate(sorted(groups.items(), key=lambda kv: (kv[0][0] == "cover", -len(kv[1])))):
        lid = f"L{i + 1}"
        freq = np.stack([p["_empty"] for p in ps]).mean(0)
        stable = freq >= (STABLE_FRAC if len(ps) >= 3 else 1.0)
        ref = {"size": ps[0]["_a"]["size"],
               "busy": np.mean([p["_a"]["busy"] for p in ps], 0),
               "color": np.mean([p["_a"]["color"] for p in ps], 0)}
        sz = [zone(f"{lid}-S{j + 1}", r, ref, float(freq[r[0]:r[0] + r[2], r[1]:r[1] + r[3]].mean()))
              for j, r in enumerate(rects(stable))]

        # vùng ổn định nào chứa được chữ của nhiều trang nhất (cỡ chữ >= 85%)?
        best, best_ok = None, -1
        for z in sz:
            ok = sum((fit_scale(p["_nz"], z["bbox"], p["_a"]["size"]) or 0) >= OVERLAY_MIN_SCALE for p in ps)
            if ok > best_ok:
                best, best_ok = z, ok
        lay = {"layout_id": lid, "kind": kind, "aspect": ratio, "size": list(ps[0]["_a"]["size"]),
               "pages": [p["n"] for p in ps], "stable_zones": sz}
        if best and best_ok >= OVERLAY_SHARE * len(ps):
            lay.update(mode="overlay", art_rect=art_rect(ref["size"]), text_zone_id=best["id"],
                       text_slot=to_canvas(best["bbox"], art_rect(ref["size"])))
        else:
            # cột chữ đặt phía nửa tranh trống hơn để chữ "đọc" liền với khoảng trống
            half = GRID // 2
            side = "left" if ref["busy"][:, :half].mean() < ref["busy"][:, half:].mean() else "right"
            lay.update(mode="column", column_side=side, art_rect=art_rect(ref["size"], side),
                       text_slot=column_slot(side))
        lay["edge_blank"] = bool(np.concatenate([ref["busy"][0], ref["busy"][-1], ref["busy"][:, 0],
                                                 ref["busy"][:, -1]]).mean() < BLANK_T)
        layouts.append(lay)
        for p in ps:
            p["_layout"] = lay

    out_pages = []
    for p in pages:
        a, lay, empty, nz = p["_a"], p["_layout"], p["_empty"], p["_nz"]
        page_z = [zone(f"P{p['n']}-Z{j + 1}", r, a) for j, r in enumerate(rects(empty))]
        ar = lay["art_rect"]
        if lay["mode"] == "overlay":
            z = next(z for z in lay["stable_zones"] if z["id"] == lay["text_zone_id"])
            t, l = round(z["bbox"][1] * GRID), round(z["bbox"][0] * GRID)
            hh, ww = round(z["bbox"][3] * GRID), round(z["bbox"][2] * GRID)
            sc = fit_scale(nz, z["bbox"], a["size"])
            if empty[t:t + hh, l:l + ww].mean() >= 0.9 and (sc or 0) >= OVERLAY_MIN_SCALE:
                chosen, src = zone(z["id"], (t, l, hh, ww), a, z.get("stability")), "stable"
            else:   # trang lệch khỏi khuôn: vùng riêng của trang, không nữa thì panel
                chosen = next((q for q in page_z if (fit_scale(nz, q["bbox"], a["size"]) or 0) >= OVERLAY_MIN_SCALE), None)
                src = "page" if chosen else "fallback_panel"
                chosen = chosen or band_fallback(a, nz)
                sc = fit_scale(nz, chosen["bbox"], a["size"])
            placement = {"mode": "overlay", "zone_id": chosen["id"], "source": src,
                         "bbox": chosen["bbox"], "anchor": chosen["anchor"],
                         "text_rect": to_canvas(chosen["bbox"], ar),
                         "ink": chosen["ink"], "scrim": chosen["scrim"]}
        else:
            sc = column_fit(nz, lay["text_slot"])
            placement = {"mode": "column", "zone_id": f"{lay['layout_id']}-COL", "source": "stable",
                         "side": lay["column_side"], "text_rect": lay["text_slot"],
                         "anchor": {"x": lay["text_slot"][0] + CANVAS["pad_px"], "y": CANVAS["pad_px"], "align": "left"},
                         "ink": INK["dark"], "scrim": None if lay["edge_blank"] else "paper"}
        placement.update(art_rect=ar, font_scale=sc if sc is not None else CANVAS["min_scale"], fits=sc is not None)
        if lay["mode"] == "column":   # phương án phụ: trang này có chỗ trống riêng đủ đè chữ không
            alt = next((q for q in page_z if (fit_scale(nz, q["bbox"], a["size"]) or 0) >= OVERLAY_MIN_SCALE), None)
            placement["alt_overlay"] = alt and {"zone_id": alt["id"], "bbox": alt["bbox"], "anchor": alt["anchor"],
                                                "ink": alt["ink"], "scrim": alt["scrim"]}
        out_pages.append({
            "n": p["n"], "kind": p["kind"], "image": BASE + p["image"], "size": list(a["size"]),
            "layout_id": lay["layout_id"],
            "text": p.get("text") or "", "text_len": p["_n"], "text_unit": "hanzi" if book["lang"] == "zh" else "words",
            "empty_ratio": round(float(empty.mean()), 3),
            "zones": page_z,
            "placement": placement,
        })
        if overlay:
            draw_overlay(p, lay, page_z, placement, os.path.join(out_dir, "overlay", book["id"], f"{p['n']:02d}.jpg"))

    res = {
        "schema": "copyspace/v1",
        "book": {k: book.get(k) for k in ("id", "title", "author", "source", "lang", "pool", "n_pages")},
        "params": {"grid": GRID, "empty_t": EMPTY_T, "blank_t": BLANK_T, "stable_frac": STABLE_FRAC,
                   "min_zone": [MIN_W, MIN_H], "column_frac": COLUMN_FRAC,
                   "overlay_min_scale": OVERLAY_MIN_SCALE, "overlay_share": OVERLAY_SHARE},
        "reference_canvas": CANVAS,
        "layouts": layouts,
        "pages": out_pages,
        "summary": {
            "pages": len(out_pages),
            "overlay_stable": sum(p["placement"]["mode"] == "overlay" and p["placement"]["source"] == "stable" for p in out_pages),
            "overlay_page": sum(p["placement"]["source"] == "page" for p in out_pages),
            "overlay_panel": sum(p["placement"]["source"] == "fallback_panel" for p in out_pages),
            "column": sum(p["placement"]["mode"] == "column" for p in out_pages),
            "not_fit": sum(not p["placement"]["fits"] for p in out_pages),
        },
    }
    os.makedirs(out_dir, exist_ok=True)
    json.dump(res, open(os.path.join(out_dir, f"{book['id']}.json"), "w"), ensure_ascii=False, indent=1)
    return res


def draw_overlay(p, lay, page_z, pl, path):
    """Ảnh duyệt: tranh đặt trên khung tham chiếu, ô bận tô đỏ, vùng ổn định xanh dương,
    vùng riêng trang vàng, chỗ đặt chữ xanh lá + chấm neo."""
    im = Image.open(p["_local"]).convert("RGB")
    cv = Image.new("RGB", (CANVAS["w"], CANVAS["h"]), (247, 243, 234))
    ar = pl["art_rect"]
    cv.paste(im.resize((ar[2], ar[3])), (ar[0], ar[1]))
    ov = Image.new("RGBA", cv.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    cw, ch = ar[2] / GRID, ar[3] / GRID
    busy = p["_a"]["busy"]
    for r in range(GRID):
        for c in range(GRID):
            if busy[r, c] >= EMPTY_T:
                x, y = ar[0] + c * cw, ar[1] + r * ch
                d.rectangle([x, y, x + cw, y + ch], fill=(220, 40, 40, 45))

    def box(rect, col, wd):
        d.rectangle([rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3]], outline=col, width=wd)

    for z in lay["stable_zones"]:
        box(to_canvas(z["bbox"], ar), (40, 120, 255, 255), 3)
    for z in page_z:
        box(to_canvas(z["bbox"], ar), (255, 190, 0, 230), 2)
    tr = pl["text_rect"]
    d.rectangle([tr[0], tr[1], tr[0] + tr[2], tr[1] + tr[3]], outline=(0, 170, 80, 255), width=6,
                fill=(0, 170, 80, 40) if pl["mode"] == "column" else None)
    if pl["mode"] == "overlay":
        ax, ay = ar[0] + pl["anchor"]["x"] * ar[2], ar[1] + pl["anchor"]["y"] * ar[3]
    else:
        ax, ay = pl["anchor"]["x"], pl["anchor"]["y"]
    d.ellipse([ax - 10, ay - 10, ax + 10, ay + 10], fill=(0, 170, 80, 255), outline=(255, 255, 255, 255), width=3)
    cv = Image.alpha_composite(cv.convert("RGBA"), ov).convert("RGB")
    cv.thumbnail((800, 800))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    cv.save(path, quality=78)


# ---------- CLI ----------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--status", help="lọc theo review.status (Approve, TBD, ...)")
    ap.add_argument("--lang")
    ap.add_argument("--all", action="store_true", help="chạy mọi cuốn khớp bộ lọc")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--cache", default="out/cache")
    ap.add_argument("--out", default="out/copyspace")
    ap.add_argument("--no-overlay", action="store_true")
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()

    ids = list(args.ids)
    if args.all or args.status or args.lang:
        lst = json.loads(get(f"{BASE}/v1/pilot/books"))["books"]
        lst = [b for b in lst if b["view"] == "pages"
               and (not args.status or b["review"]["status"] == args.status)
               and (not args.lang or b["lang"] == args.lang)]
        ids += [b["id"] for b in lst]
    if args.limit:
        ids = ids[:args.limit]
    if not ids:
        ap.error("cần id sách hoặc --all / --status")

    def one(bid):
        try:
            res = run_book(load_book(bid, args.cache), args.out, overlay=not args.no_overlay)
            return bid, res["summary"], None
        except Exception as e:
            return bid, None, repr(e)

    index = []
    with ThreadPoolExecutor(args.workers) as ex:
        for bid, s, err in ex.map(one, ids):
            print(bid, s if s else "LỖI " + err, flush=True)
            index.append({"id": bid, "summary": s, "error": err})
    if len(ids) > 1:
        json.dump(index, open(os.path.join(args.out, "_index.json"), "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
