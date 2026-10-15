#!/usr/bin/env python3
"""Mapping bìa truyện: vùng trống trên tranh bìa + điểm neo đặt tên truyện, xuất JSON.

Dùng lại bộ đo độ bận của scripts/copyspace.py. Khác với trang ruột:
  - Mỗi cuốn chỉ có 1 bìa, nên "vị trí giống nhau" được tìm GIỮA CÁC CUỐN: bìa gom theo khổ
    (tỉ lệ khung), ô trống ở >= STABLE_FRAC số bìa trong khổ = vùng ổn định của khổ đó.
  - Chữ đặt lên bìa là tên truyện. Theo docs/DESIGN.md: tên một dòng dùng kiểu C1 (chữ kem, viền
    rừng 6px, đặt giữa phần ba trên đang yên); tên xuống hai dòng, hoặc nền ở đó nhiều hoạ tiết /
    loang sáng tối khiến chữ chìm, thì dùng panel trắng 85% + blur 8px, chữ màu rừng.
  - Độ "trống" đo ở thang thô (đã làm mờ) để tìm chỗ đặt; độ đọc được đo lại ở thang mịn,
    đúng kích thước hiển thị, ngay trên hộp chữ thật, vì nền trông trống từ xa vẫn có thể đầy hoạ tiết nhỏ.

Dùng:
  python3 scripts/covers.py --status Approve            # -> out/covers/covers.json + overlay/
  python3 scripts/covers.py --all                        # mọi sách dạng ảnh trang
  python3 scripts/covers.py SW-266338 ASB-13623          # vài cuốn
"""
import argparse, json, os, sys
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import copyspace as cs  # noqa: E402

STABLE_FRAC = 0.5       # bìa khác nhau nhiều hơn trang ruột: ô trống ở >= nửa số bìa cùng khổ là ổn định
MIN_COVERS = 5          # khổ có ít hơn số bìa này thì không tính vùng ổn định
# docs/DESIGN.md: khung 1180×820, lề an toàn 32px, C1 30–44px viền rừng 6px, panel 85% trắng padding 16/24
FRAME_W, MARGIN = 1180, 32
C1 = {"max_px": 44, "min_px": 30, "pinyin_px": 16, "stroke_px": 6, "fill": "#FDF9F0", "stroke": "#0E4A3A"}
PANEL = {"px": 32, "min_px": 24, "pad": (16, 24), "white_alpha": 0.85, "blur_px": 8, "ink": "#0E4A3A", "max_lines": 2}
LINE_H = lambda px: px * 1.2 + C1["pinyin_px"] * 1.3      # 1 dòng chữ Hán + pinyin phía trên
# Ngưỡng đọc được cho C1 (đo trên hộp chữ, ảnh co về rộng FRAME_W):
CALM_MIN = 0.85    # >= 85% ô lưới thô dưới chữ phải trống (không đè lên vật, nhân vật)
EDGE_MAX = 0.05     # tỉ lệ điểm ảnh là cạnh hoạ tiết (gradient màu > EDGE_T)
EDGE_T = 0.12
LUMA_STD_MAX = 0.18 # độ lệch chuẩn độ sáng tương đối: nền loang sáng/tối mạnh thì chữ lúc nổi lúc chìm


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


def frame_scale(size):
    return FRAME_W / size[0]


def fixed_slot(freq, ref, its):
    """Vị trí tên cố định cho cả khổ bìa, theo rule C1: dải trong phần ba trên, ưu tiên giữa.
    Dải cao 1 dòng C1 cỡ lớn nhất, rộng đủ tên dài điển hình (bách phân vị 75) của khổ.
    Chỉ dời sang trái/phải khi giữa trống ở ít bìa hơn hẳn (kém hơn 0.15)."""
    G = cs.GRID
    w, h = ref["size"]
    s = frame_scale(ref["size"])
    n_typ = int(np.percentile([title_len(title_of(it["book"])[0]) for it in its], 75))
    need_w = (n_typ * C1["max_px"] + 2 * C1["stroke_px"] + 2 * MARGIN) / (w * s)
    need_h = (LINE_H(C1["max_px"]) + 2 * MARGIN) / (h * s)
    ww = min(G, max(4, int(np.ceil(need_w * G))))
    hh = min(G // 3, max(2, int(np.ceil(need_h * G))))
    top = 0
    def score(l):
        return float(freq[top:top + hh, l:l + ww].mean())
    centre = (G - ww) // 2
    best = max(range(0, G - ww + 1), key=score)
    l = centre if score(centre) >= score(best) - 0.15 else best
    z = cs.zone("slot", (top, l, hh, ww), ref)
    z["empty_freq"] = round(score(l), 3)
    z["typical_title_len"] = n_typ
    return z


def text_box(n, slot_bbox, size):
    """Hộp chữ thật cho một tên: thử C1 một dòng (44→30px) trong dải; không vừa thì panel 2 dòng.
    Trả về (kiểu, cỡ chữ, số dòng, bbox 0..1 của hộp chữ kể cả viền/padding), căn theo neo của dải."""
    w, h = size
    s = frame_scale(size)
    sx, sy, sw, sh = (v * d * s for v, d in zip(slot_bbox, (w, h, w, h)))
    avail = sw - 2 * MARGIN
    cx = sx + sw / 2
    for px in range(C1["max_px"], C1["min_px"] - 1, -2):
        tw = n * px + 2 * C1["stroke_px"]
        if tw <= avail:
            th = LINE_H(px) + 2 * C1["stroke_px"]
            return "c1", px, 1, _bbox(cx - tw / 2, sy + MARGIN, tw, th, w * s, h * s)
    for px in range(PANEL["px"], PANEL["min_px"] - 1, -2):
        per = max(1, int((avail - 2 * PANEL["pad"][1]) // px))
        lines = -(-n // per)
        if lines <= PANEL["max_lines"]:
            tw = min(n, per) * px + 2 * PANEL["pad"][1]
            th = lines * LINE_H(px) + 2 * PANEL["pad"][0]
            return "panel", px, lines, _bbox(cx - tw / 2, sy + MARGIN, tw, th, w * s, h * s)
    px = PANEL["min_px"]
    per = max(1, int((avail - 2 * PANEL["pad"][1]) // px))
    lines = -(-n // per)
    tw, th = min(n, per) * px + 2 * PANEL["pad"][1], lines * LINE_H(px) + 2 * PANEL["pad"][0]
    return "panel", px, lines, _bbox(cx - tw / 2, sy + MARGIN, tw, th, w * s, h * s)


def _bbox(x, y, bw, bh, W, H):
    x = min(max(x, MARGIN), W - MARGIN - bw)
    return [round(x / W, 4), round(y / H, 4), round(bw / W, 4), round(bh / H, 4)]


def display(path):
    """Ảnh bìa ở kích thước hiển thị (rộng FRAME_W), dạng mảng 0..1."""
    im = Image.open(path).convert("RGB")
    s = FRAME_W / im.size[0]
    im = im.resize((FRAME_W, max(1, round(im.size[1] * s))), Image.LANCZOS)
    return np.asarray(im, dtype=np.float32) / 255


def legibility(img, bbox, empty):
    """Đo nền ngay dưới hộp chữ, ở kích thước hiển thị, không làm mờ (hoạ tiết nhỏ vẫn còn)."""
    H, W = img.shape[:2]
    x0, y0 = int(bbox[0] * W), int(bbox[1] * H)
    x1, y1 = max(x0 + 2, int((bbox[0] + bbox[2]) * W)), max(y0 + 2, int((bbox[1] + bbox[3]) * H))
    a = img[y0:y1, x0:x1]
    g = np.zeros(a.shape[:2], np.float32)
    g[:, :-1] = np.maximum(g[:, :-1], np.abs(np.diff(a, axis=1)).max(2))
    g[:-1, :] = np.maximum(g[:-1, :], np.abs(np.diff(a, axis=0)).max(2))
    lin = np.where(a <= 0.03928, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
    L = lin @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    lf, lk = cs.hex_lum(C1["fill"]), cs.hex_lum(C1["stroke"])
    cf = (np.maximum(L, lf) + 0.05) / (np.minimum(L, lf) + 0.05)
    ck = (np.maximum(L, lk) + 0.05) / (np.minimum(L, lk) + 0.05)
    # panel: 85% trắng phủ lên nền đã blur -> độ sáng nền sau panel, tương phản chữ rừng
    lp = PANEL["white_alpha"] * 1.0 + (1 - PANEL["white_alpha"]) * L
    cp = (lp + 0.05) / (lk + 0.05)
    G = cs.GRID
    r0, r1 = int(bbox[1] * G), min(G, int(np.ceil((bbox[1] + bbox[3]) * G)))
    c0, c1 = int(bbox[0] * G), min(G, int(np.ceil((bbox[0] + bbox[2]) * G)))
    return {
        "calm_coarse": round(float(empty[r0:max(r1, r0 + 1), c0:max(c1, c0 + 1)].mean()), 2),  # thang thô: có vật/nhân vật không
        "edge_density": round(float((g > EDGE_T).mean()), 3),
        "luma_std": round(float(L.std()), 3),
        "luma_p5_p50_p95": [round(float(v), 3) for v in np.percentile(L, [5, 50, 95])],
        "fill_contrast_p5": round(float(np.percentile(cf, 5)), 2),     # chữ kem so với nền
        "stroke_contrast_p5": round(float(np.percentile(ck, 5)), 2),   # viền rừng so với nền
        "pair_contrast_p5": round(float(np.percentile(np.maximum(cf, ck), 5)), 2),  # ít nhất một trong hai
        "panel_contrast_min": round(float(cp.min()), 2),
    }


def shift_c1(img, tb, empty, step=24):
    """Trượt hộp chữ C1 trong phần ba trên (giữ lề an toàn), trả về chỗ gần vị trí cũ nhất mà
    decide() cho C1, kèm số đo. None nếu không có."""
    H, W = img.shape[:2]
    bw, bh = tb[2] * W, tb[3] * H
    x_old, y_old = tb[0] * W, tb[1] * H
    best = None
    for y in np.arange(MARGIN, H / 3 - bh + 1, step / 2):
        for x in np.arange(MARGIN, W - MARGIN - bw + 1, step):
            d = abs(x - x_old) + 2 * abs(y - y_old)       # ưu tiên giữ độ cao, rồi gần tâm cũ
            if best and d >= best[0]:
                continue
            bb = _bbox(x, y, bw, bh, W, H)
            leg = legibility(img, bb, empty)
            if decide("c1", 1, leg)[0] == "c1":
                best = (d, bb, leg)
    return best and (best[1], best[2])


def decide(kind, lines, leg):
    """Rule chọn kiểu chữ. C1 chỉ khi tên một dòng VÀ nền dưới chữ yên ở thang mịn."""
    if kind == "panel":
        return "panel", f"tên dài, xuống {lines} dòng: dùng panel theo rule C1"
    why = []
    if leg["calm_coarse"] < CALM_MIN:
        why.append(f"tranh có hình ngay chỗ chữ ({round((1 - leg['calm_coarse']) * 100)}% ô bận)")
    if leg["edge_density"] > EDGE_MAX:
        why.append(f"nền nhiều hoạ tiết ({round(leg['edge_density'] * 100)}% điểm là cạnh)")
    if leg["luma_std"] > LUMA_STD_MAX:
        why.append(f"nền loang sáng tối (lệch {leg['luma_std']})")
    if leg["pair_contrast_p5"] < 3:
        why.append("có chỗ cả chữ kem lẫn viền rừng đều dưới 3:1 với nền")
    if why:
        return "panel", "; ".join(why) + ": chữ C1 sẽ chìm, dùng panel"
    return "c1", "nền yên dưới chữ: chữ kem viền rừng đọc rõ"


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
        n = it["_n"] = title_len(title)
        it["_title"] = title
        it["_pinyin"] = pinyin_of(title) if cs.CJK.search(title) else None
        own = [cs.zone(f"Z{j + 1}", r, a) for j, r in enumerate(cs.rects(empty, min_w=0.25, min_h=0.15))]
        slot = it["fmt_slot"]
        img = display(it["cover"]["_local"])
        kind, px, lines, tb = text_box(n, slot["bbox"], a["size"])
        leg = legibility(img, tb, empty)
        style, reason = decide(kind, lines, leg)
        source, shift = "fixed", [0, 0]
        if kind == "c1" and style == "panel":
            # nền ở vị trí cố định làm chữ chìm: dò trong phần ba trên tìm chỗ gần nhất mà C1 đọc rõ
            near = shift_c1(img, tb, empty)
            if near:
                shift = [round((near[0][0] - tb[0]) * img.shape[1]), round((near[0][1] - tb[1]) * img.shape[0])]
                tb, leg = near
                style, reason = "c1", f"vị trí cố định bị chìm ({reason.split(':')[0]}); dời {shift[0]:+d}px ngang, {shift[1]:+d}px dọc tới chỗ nền yên"
                source = "shifted"
            else:   # không chỗ nào yên: panel bọc đúng dòng chữ ở vị trí cố định
                Wf, Hf = img.shape[1], img.shape[0]
                px = min(px, PANEL["px"])
                bw, bh = n * px + 2 * PANEL["pad"][1], LINE_H(px) + 2 * PANEL["pad"][0]
                tb = _bbox((tb[0] + tb[2] / 2) * Wf - bw / 2, tb[1] * Hf, bw, bh, Wf, Hf)
                leg = legibility(img, tb, empty)
        t, l = round(slot["bbox"][1] * cs.GRID), round(slot["bbox"][0] * cs.GRID)
        hh, ww = round(slot["bbox"][3] * cs.GRID), round(slot["bbox"][2] * cs.GRID)
        calm = float(empty[t:t + hh, l:l + ww].mean())
        c = it["cover"]
        covers.append({
            "id": book["id"], "source": book["source"], "lang": book["lang"],
            "image": cs.BASE + c["image"], "size": list(a["size"]), "format": it["fmt"],
            "title": title, "title_source": tsrc, "title_len": n, "title_pinyin": it["_pinyin"],
            "empty_ratio": round(float(empty.mean()), 3),
            "zones": own,
            "title_slot": {"slot_bbox": slot["bbox"], "calm_coarse": round(calm, 2),
                           "style": style, "source": source, "shift_px": shift, "reason": reason,
                           "text_box": tb, "anchor": {"x": round(tb[0] + tb[2] / 2, 4), "y": tb[1], "align": "center"},
                           "font_px": px, "lines": lines, "legibility": leg},
        })
        if not args.no_overlay:
            draw(it, slot, covers[-1]["title_slot"], None, os.path.join(args.out, "overlay", f"{book['id']}.jpg"))

    covers.sort(key=lambda c: c["id"])
    res = {
        "schema": "covers/v2",
        "params": {"grid": cs.GRID, "empty_t": cs.EMPTY_T, "blank_t": cs.BLANK_T,
                   "stable_frac": STABLE_FRAC, "min_covers": MIN_COVERS, "frame_w": FRAME_W, "margin": MARGIN,
                   "c1": C1, "panel": PANEL, "calm_min": CALM_MIN, "edge_t": EDGE_T, "edge_max": EDGE_MAX, "luma_std_max": LUMA_STD_MAX},
        "formats": fmt_out,
        "covers": covers,
        "errors": [{"id": it["id"], "error": it["error"]} for it in items if "error" in it],
        "summary": {
            "covers": len(covers),
            "c1": sum(c["title_slot"]["style"] == "c1" for c in covers),
            "panel_long": sum(c["title_slot"]["reason"].startswith("tên dài") for c in covers),
            "panel_busy": sum(c["title_slot"]["style"] == "panel" and not c["title_slot"]["reason"].startswith("tên dài") for c in covers),
            "c1_fixed": sum(c["title_slot"]["style"] == "c1" and c["title_slot"]["source"] == "fixed" for c in covers),
            "c1_shifted": sum(c["title_slot"]["source"] == "shifted" for c in covers),
            "no_zh_title": sum(c["title_source"] == "title_en" for c in covers),
        },
    }
    os.makedirs(args.out, exist_ok=True)
    json.dump(res, open(os.path.join(args.out, "covers.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(res["summary"], ensure_ascii=False))
    for f in fmt_out:
        print(f["format"], f["covers"], f["title_slot"]["position"], f["title_slot"]["bbox"], f["title_slot"]["empty_freq"])


FONT_FILES = ["/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"]


def font(px):
    """Font chữ Hán để vẽ ảnh duyệt (app dùng Noto Sans SC; máy chạy không có thì dùng WenQuanYi)."""
    from PIL import ImageFont
    for f in FONT_FILES:
        if os.path.exists(f):
            return ImageFont.truetype(f, int(px))
    return ImageFont.load_default()


def pinyin_of(title):
    """Pinyin có dấu cho từng chữ Hán (cần gói pypinyin; không có thì bỏ trống)."""
    try:
        from pypinyin import pinyin, Style
    except ImportError:
        return None
    chars = hanzi_chars(title)
    return [p[0] if ch.isalpha() else "" for ch, p in zip(chars, pinyin(chars, style=Style.TONE))]


def hanzi_chars(title):
    """Các ký tự sẽ đặt lên bìa (chữ Hán + dấu câu CJK), đúng với số đếm của title_len."""
    return cs.CJK.findall(title)


def draw(it, slot, ts, alt, path):
    """Ảnh duyệt ở kích thước hiển thị: ô bận đỏ nhạt, dải cố định xanh dương, hộp chữ xanh lá
    (C1) hoặc cam (panel), chỗ phụ vàng; mô phỏng luôn chữ để nhìn có chìm không."""
    im = Image.open(it["cover"]["_local"]).convert("RGB")
    s = FRAME_W / im.size[0]
    im = im.resize((FRAME_W, round(im.size[1] * s)), Image.LANCZOS)
    w, h = im.size
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    cw, ch = w / cs.GRID, h / cs.GRID
    for r in range(cs.GRID):
        for c in range(cs.GRID):
            if not it["empty"][r, c]:
                d.rectangle([c * cw, r * ch, (c + 1) * cw, (r + 1) * ch], fill=(220, 40, 40, 35))

    def rect(bb):
        return [bb[0] * w, bb[1] * h, (bb[0] + bb[2]) * w, (bb[1] + bb[3]) * h]

    d.rectangle(rect(slot["bbox"]), outline=(40, 120, 255, 255), width=3)
    if alt:
        d.rectangle(rect(alt["text_box"]), outline=(255, 190, 0, 255), width=4)
    im = Image.alpha_composite(im.convert("RGBA"), ov)
    # vẽ tên thật (chữ Hán + pinyin) đúng cỡ, màu, viền để nhìn chữ có chìm không
    sim = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(sim)
    x0, y0, x1, y1 = rect(ts["text_box"])
    px, py_px = ts["font_px"], C1["pinyin_px"]
    chars = hanzi_chars(it["_title"]) or [it["_title"]]
    pys = it["_pinyin"] or [""] * len(chars)
    f_h, f_p = font(px), font(py_px)
    forest, cream = (14, 74, 58, 255), (253, 249, 240, 255)
    if ts["style"] == "panel":
        panel_bg = im.crop((int(x0), int(y0), int(x1), int(y1))).filter(ImageFilter.GaussianBlur(PANEL["blur_px"]))
        white = Image.new("RGBA", panel_bg.size, (255, 255, 255, int(255 * PANEL["white_alpha"])))
        im.paste(Image.alpha_composite(panel_bg, white), (int(x0), int(y0)))
        pad = PANEL["pad"]
        ox, oy, ink, stroke = x0 + pad[1], y0 + pad[0], forest, 0
        per = max(1, int((x1 - x0 - 2 * pad[1]) // px))
    else:
        ox, oy, ink, stroke = x0 + C1["stroke_px"], y0 + C1["stroke_px"], cream, C1["stroke_px"]
        per = len(chars)
    for i, ch in enumerate(chars):
        li, k = divmod(i, per)
        cx = ox + k * px + px / 2
        top = oy + li * LINE_H(px)
        if pys[i] if i < len(pys) else "":
            d.text((cx, top), pys[i], font=f_p, anchor="ma", fill=ink if not stroke else cream,
                   stroke_width=max(2, stroke // 2) if stroke else 0, stroke_fill=forest)
        d.text((cx if len(chars) > 1 else ox, top + py_px * 1.3), ch, font=f_h, anchor="ma" if len(chars) > 1 else "la",
               fill=ink, stroke_width=stroke, stroke_fill=forest)
    if ts["style"] == "panel":
        d.rounded_rectangle([x0, y0, x1, y1], 24, outline=(230, 120, 40, 160), width=2)
    im = Image.alpha_composite(im, sim).convert("RGB")
    im.thumbnail((800, 800))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path, quality=80)


if __name__ == "__main__":
    main()
