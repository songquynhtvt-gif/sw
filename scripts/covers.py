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
import argparse, difflib, functools, json, os, re, sys, threading
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
EN = {"px": 16, "line": 16 * 1.4, "char_w": 0.55}          # dòng tên tiếng Anh nhỏ bên dưới (để biết truyện gì)
en_width = lambda en: font(EN["px"]).getlength(en) + 4 if en else 0   # đo bằng font thật
# Ngưỡng đọc được cho C1 (đo trên hộp chữ, ảnh co về rộng FRAME_W):
CALM_MIN = 0.85    # >= 85% ô lưới thô dưới chữ phải trống (không đè lên vật, nhân vật)
EDGE_MAX = 0.05     # tỉ lệ điểm ảnh là cạnh hoạ tiết (gradient màu > EDGE_T)
EDGE_T = 0.12
LUMA_STD_MAX = 0.18 # độ lệch chuẩn độ sáng tương đối: nền loang sáng/tối mạnh thì chữ lúc nổi lúc chìm


def title_of(book):
    """Tên truyện bằng tiếng Trung nếu có, kèm nguồn của tên."""
    cover = next((p for p in book["pages"] if p["kind"] == "bìa"), None)
    if cover and cs.CJK.search(cover.get("text") or ""):
        # chữ trang bìa có thể kèm dòng tên tác giả, minh hoạ: chỉ giữ các dòng có chữ Hán
        return " ".join(l.strip() for l in cover["text"].splitlines() if cs.CJK.search(l)), "cover_text"
    tr = book.get("translation") or {}
    if tr.get("title_zh"):
        return tr["title_zh"], "translation"
    if cs.CJK.search(book.get("title") or ""):
        return book["title"], "title"
    return book.get("title") or "", "title_en"


GLOSS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "mapping", "covers", "title_en_gloss.json")
_GLOSS = None


def gloss():
    """Tên tiếng Anh dịch nháp (AI) cho sách tiếng Trung mà nguồn chỉ ghi pinyin: {id: tên}."""
    global _GLOSS
    if _GLOSS is None:
        _GLOSS = json.load(open(GLOSS_FILE)) if os.path.exists(GLOSS_FILE) else {}
    return _GLOSS


def title_en(book):
    """Tên tiếng Anh để biết truyện gì, kèm nguồn: sách tiếng Anh dùng tên gốc; sách tiếng Trung
    lấy từ đường dẫn nguồn (storyweaver.org.in/en/stories/266338-the-story-of-a-dancer); đường dẫn
    chỉ là pinyin thì dùng bản dịch nháp trong GLOSS_FILE, chưa có thì để trống."""
    if not cs.CJK.search(book.get("title") or ""):
        return book.get("title") or "", "original"
    url = ((book.get("fields") or {}).get("Source URL") or "").rstrip("/")
    slug = url.rsplit("/", 1)[-1]
    slug = slug.split("-", 1)[1] if "-" in slug and slug.split("-", 1)[0].isdigit() else slug
    t = slug.replace("-", " ").strip()
    if t and not cs.CJK.search(t) and "." not in t and not is_pinyin(t, book["title"]):
        return t[:1].upper() + t[1:], "source_url"
    if book["id"] in gloss():
        return gloss()[book["id"]], "ai_gloss"
    return "", "missing"


def is_pinyin(text, zh):
    """Đường dẫn có phải chỉ là pinyin của tên Trung không (vd. jintian-wo-shi)."""
    try:
        from pypinyin import lazy_pinyin
    except ImportError:
        return False
    a = re.sub(r"[^a-z]", "", text.lower())
    b = re.sub(r"[^a-z]", "", "".join(lazy_pinyin(zh)).replace("ü", "v"))
    return bool(a) and (a == b or (len(a) > 6 and (a in b or b in a)))


def title_len(title):
    """Độ dài tên tính theo "ô chữ Hán" (1 ô = 1 em). Tên tiếng Anh đo bằng font thật."""
    n = len(cs.CJK.findall(title))
    return n if n else int(np.ceil(font(100).getlength(title) / 100))


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


def text_box(n, slot_bbox, size, en=""):
    """Hộp chữ thật cho một tên: thử C1 một dòng (44→30px) trong dải; không vừa thì panel 2 dòng.
    Trả về (kiểu, cỡ chữ, số dòng, bbox 0..1 của hộp chữ kể cả viền/padding), căn theo neo của dải."""
    w, h = size
    s = frame_scale(size)
    sx, sy, sw, sh = (v * d * s for v, d in zip(slot_bbox, (w, h, w, h)))
    avail = sw - 2 * MARGIN
    cx = sx + sw / 2
    for px in range(C1["max_px"], C1["min_px"] - 1, -2):
        tw = max(n * px, en_width(en)) + 2 * C1["stroke_px"]
        if tw <= avail:
            th = LINE_H(px) + (EN["line"] if en else 0) + 2 * C1["stroke_px"]
            return "c1", px, 1, _bbox(cx - tw / 2, sy + MARGIN, tw, th, w * s, h * s)
    for px in range(PANEL["px"], PANEL["min_px"] - 1, -2):
        per = max(1, int((avail - 2 * PANEL["pad"][1]) // px))
        lines = -(-n // per)
        if lines <= PANEL["max_lines"]:
            tw = max(min(n, per) * px, min(en_width(en), avail - 2 * PANEL["pad"][1])) + 2 * PANEL["pad"][1]
            th = lines * LINE_H(px) + (EN["line"] if en else 0) + 2 * PANEL["pad"][0]
            return "panel", px, lines, _bbox(cx - tw / 2, sy + MARGIN, tw, th, w * s, h * s)
    px = PANEL["min_px"]
    per = max(1, int((avail - 2 * PANEL["pad"][1]) // px))
    lines = -(-n // per)
    tw = max(min(n, per) * px, min(en_width(en), avail - 2 * PANEL["pad"][1])) + 2 * PANEL["pad"][1]
    th = lines * LINE_H(px) + (EN["line"] if en else 0) + 2 * PANEL["pad"][0]
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


_ocr_local = threading.local()


def ocr(path):
    """Đọc chữ đã in sẵn trên bìa (cần gói rapidocr-onnxruntime; không có thì trả None).
    Trả về [{text, conf, bbox 0..1}]."""
    try:
        from rapidocr_onnxruntime import RapidOCR
    except ImportError:
        return None
    if not hasattr(_ocr_local, "eng"):
        _ocr_local.eng = RapidOCR()
    im = Image.open(path).convert("RGB")
    W, H = im.size
    res, _ = _ocr_local.eng(np.asarray(im))
    out = []
    for box, text, conf in res or []:
        xs, ys = [p[0] for p in box], [p[1] for p in box]
        out.append({"text": text, "conf": round(float(conf), 2),
                    "bbox": [round(min(xs) / W, 4), round(min(ys) / H, 4),
                             round((max(xs) - min(xs)) / W, 4), round((max(ys) - min(ys)) / H, 4)]})
    return out


def letters(t):
    return re.sub(r"[^a-z0-9]", "", (t or "").lower())


def baked_title(found, en):
    """Rule nhận ra tên tiếng Anh đã in sẵn trên bìa:
    - mỗi dòng OCR (độ tin >= 0.5) được tính là thuộc tên nếu chữ của nó nằm trong tên (bỏ dấu, khoảng trắng),
      hoặc giống một đoạn của tên >= 80%;
    - tổng số chữ cái khớp >= 60% số chữ cái của tên -> bìa có tên in sẵn, vùng tên = hộp bao các dòng khớp.
    Trả về (score, bbox, các dòng khớp, các dòng chữ khác)."""
    t = letters(en)
    if not found or len(t) < 3:
        return 0.0, None, [], [x for x in found or [] if x["conf"] >= 0.5]
    hit, other, covered = [], [], 0
    for x in found:
        w = letters(x["text"])
        if x["conf"] < 0.5 or len(w) < 2:
            continue
        ok = w in t or max((difflib.SequenceMatcher(None, w, t[i:i + len(w)]).ratio()
                            for i in range(0, max(1, len(t) - len(w) + 1))), default=0) >= 0.8
        if ok:
            hit.append(x)
            covered += len(w)
        else:
            other.append(x)
    score = min(1.0, covered / len(t))
    if not hit:
        return score, None, hit, other
    x0 = min(h["bbox"][0] for h in hit)
    y0 = min(h["bbox"][1] for h in hit)
    x1 = max(h["bbox"][0] + h["bbox"][2] for h in hit)
    y1 = max(h["bbox"][1] + h["bbox"][3] for h in hit)
    return round(score, 2), [round(x0, 4), round(y0, 4), round(x1 - x0, 4), round(y1 - y0, 4)], hit, other


def cover_flag(baked):
    """Cờ chữ in sẵn trên bìa: "title" (có tên tiếng Anh in sẵn), "text" (có chữ khác: tác giả,
    logo, hoặc tên viết cách điệu OCR đọc không ra), "none" (không thấy chữ), "unknown" (chưa chạy OCR)."""
    if not baked["ocr"]:
        return "unknown"
    if baked["title_bbox"] and baked["title_score"] >= 0.6:
        return "title"
    return "text" if baked["other_text"] or baked["title_lines"] else "none"


def replace_box(n, bbox, size, sub):
    """Tên Trung đặt vào đúng vùng tên Anh in sẵn: chọn số dòng (1–3) cho chữ to nhất vừa vùng."""
    W, H = size[0] * frame_scale(size), size[1] * frame_scale(size)
    pad = 0.15
    bw, bh = bbox[2] * W, bbox[3] * H
    x, y = bbox[0] * W - bw * pad / 2, bbox[1] * H - bh * pad / 2
    bw, bh = bw * (1 + pad), bh * (1 + pad)
    best = (0, 1)
    for lines in (1, 2, 3):
        per = -(-n // lines)
        px = min(bw / per, (bh - (EN["line"] if sub else 0)) / (lines * 1.2 + 0.4))
        if px > best[0]:
            best = (px, lines)
    px = int(max(16, min(96, best[0])))
    return px, best[1], [round(max(0, x) / W, 4), round(max(0, y) / H, 4), round(min(bw, W) / W, 4), round(min(bh, H) / H, 4)]


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
    """Chỉ tải JSON sách và ảnh bìa (không tải các trang ruột)."""
    p = os.path.join(cache, book_id, "book.json")
    if not os.path.exists(p):
        cs.get(f"{cs.BASE}/v1/pilot/books/{book_id}", p)
    book = json.load(open(p))
    cover = next((pg for pg in book["pages"] if pg["kind"] == "bìa" and pg.get("image")), None)
    if cover:
        ext = os.path.splitext(cover["image"])[1] or ".png"
        cover["_local"] = os.path.join(cache, book_id, "pages", f"{cover['n']:02d}{ext}")
        if not os.path.exists(cover["_local"]):
            cs.get(cs.BASE + cover["image"], cover["_local"])
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
    ap.add_argument("--no-ocr", action="store_true", help="bỏ bước dò chữ in sẵn trên bìa")
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
            return {"id": bid, "book": book, "cover": cover, "a": cs.analyse(cover["_local"]),
                    "ocr": None if args.no_ocr else ocr(cover["_local"])}
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
        en, en_src = title_en(book)
        sub = en if tsrc != "title_en" else ""          # tên chính đã là tiếng Anh thì không lặp lại
        it["_sub"] = sub
        kind, px, lines, tb = text_box(n, slot["bbox"], a["size"], sub)
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
                bw = max(n * px, en_width(sub)) + 2 * PANEL["pad"][1]
                bh = LINE_H(px) + (EN["line"] if sub else 0) + 2 * PANEL["pad"][0]
                tb = _bbox((tb[0] + tb[2] / 2) * Wf - bw / 2, tb[1] * Hf, bw, bh, Wf, Hf)
                leg = legibility(img, tb, empty)
        found = it.get("ocr")
        score, bt, hit, other = baked_title(found, en)
        baked = {"ocr": found is not None, "title_score": score, "title_bbox": bt,
                 "title_lines": [h["text"] for h in hit],
                 "other_text": [{"text": o["text"], "bbox": o["bbox"]} for o in other]}
        if bt and score >= 0.6:
            # bìa đã in sẵn tên tiếng Anh: tên Trung thay vào đúng chỗ đó, designer xoá chữ Anh
            px, lines, tb = replace_box(n, bt, a["size"], sub)
            leg = legibility(img, tb, empty)
            style, source, shift = "replace", "baked_title", [0, 0]
            reason = (f"bìa đã in sẵn tên tiếng Anh ({' / '.join(baked['title_lines'])}, khớp {round(score * 100)}%): "
                      "xoá chữ Anh trong tranh, đặt tên Trung vào đúng vùng đó")
        elif other and any(o["bbox"][3] >= 0.06 for o in other):
            reason += "; có chữ lớn in sẵn trên bìa nhưng không khớp tên, cần người xem"
        t, l = round(slot["bbox"][1] * cs.GRID), round(slot["bbox"][0] * cs.GRID)
        hh, ww = round(slot["bbox"][3] * cs.GRID), round(slot["bbox"][2] * cs.GRID)
        calm = float(empty[t:t + hh, l:l + ww].mean())
        c = it["cover"]
        covers.append({
            "id": book["id"], "source": book["source"], "lang": book["lang"],
            "image": cs.BASE + c["image"], "size": list(a["size"]), "format": it["fmt"],
            "title": title, "title_source": tsrc, "title_len": n, "title_pinyin": it["_pinyin"],
            "title_en": en, "title_en_source": en_src,
            "empty_ratio": round(float(empty.mean()), 3),
            "zones": own,
            "title_slot": {"slot_bbox": slot["bbox"], "calm_coarse": round(calm, 2),
                           "style": style, "source": source, "shift_px": shift, "reason": reason,
                           "text_box": tb, "anchor": {"x": round(tb[0] + tb[2] / 2, 4), "y": tb[1], "align": "center"},
                           "font_px": px, "lines": lines, "legibility": leg},
            "baked_text": baked,
            "cover_text_flag": cover_flag(baked),
        })
        if not args.no_overlay:
            draw(it, slot, covers[-1]["title_slot"], None, os.path.join(args.out, "overlay", f"{book['id']}.jpg"))

    covers.sort(key=lambda c: c["id"])
    res = {
        "schema": "covers/v2",
        "params": {"en": EN, "grid": cs.GRID, "empty_t": cs.EMPTY_T, "blank_t": cs.BLANK_T,
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
            "replace_baked_title": sum(c["title_slot"]["style"] == "replace" for c in covers),
            "text_needs_review": sum("cần người xem" in c["title_slot"]["reason"] for c in covers),
            "flag_title": sum(c["cover_text_flag"] == "title" for c in covers),
            "flag_text": sum(c["cover_text_flag"] == "text" for c in covers),
            "no_zh_title": sum(c["title_source"] == "title_en" for c in covers),
            "en_missing": sum(c["title_en_source"] == "missing" for c in covers),
            "en_ai_gloss": sum(c["title_en_source"] == "ai_gloss" for c in covers),
        },
    }
    os.makedirs(args.out, exist_ok=True)
    json.dump(res, open(os.path.join(args.out, "covers.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(res["summary"], ensure_ascii=False))
    for f in fmt_out:
        print(f["format"], f["covers"], f["title_slot"]["position"], f["title_slot"]["bbox"], f["title_slot"]["empty_freq"])


FONT_FILES = ["/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"]


@functools.lru_cache(maxsize=None)
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
    if ts["style"] == "replace":
        # chỉ khoanh vùng tên in sẵn, không vẽ đè lên tranh (designer tự xử lý chữ Anh)
        d.rectangle([x0, y0, x1, y1], outline=(230, 120, 40, 255), width=4)
        ox, oy, ink, stroke, per = x0, y0, cream, 0, 1
        chars, pys = [], []
    elif ts["style"] == "panel":
        panel_bg = im.crop((int(x0), int(y0), int(x1), int(y1))).filter(ImageFilter.GaussianBlur(PANEL["blur_px"]))
        white = Image.new("RGBA", panel_bg.size, (255, 255, 255, int(255 * PANEL["white_alpha"])))
        im.paste(Image.alpha_composite(panel_bg, white), (int(x0), int(y0)))
        pad = PANEL["pad"]
        ox, oy, ink, stroke = x0 + pad[1], y0 + pad[0], forest, 0
        per = -(-len(chars) // max(1, ts["lines"]))      # chia đều theo số dòng đã tính
    else:
        ox, oy, ink, stroke = x0 + C1["stroke_px"], y0 + C1["stroke_px"], cream, C1["stroke_px"]
        per = len(chars)
    if not hanzi_chars(it["_title"]) and ts["style"] != "replace":      # tên chính tiếng Anh: xuống dòng theo từ, đo bằng font thật
        maxw = (x1 - x0) - 2 * (PANEL["pad"][1] if ts["style"] == "panel" else C1["stroke_px"])
        rows, cur = [], ""
        for wd in it["_title"].split():
            t = (cur + " " + wd).strip()
            if cur and f_h.getlength(t) > maxw:
                rows.append(cur)
                cur = wd
            else:
                cur = t
        rows.append(cur)
        chars, per = rows, 1
        pys = [""] * len(rows)
    for i, ch in enumerate(chars):
        li, k = divmod(i, per)
        cx = ox + k * px + px / 2
        top = oy + li * LINE_H(px)
        if pys[i] if i < len(pys) else "":
            d.text((cx, top), pys[i], font=f_p, anchor="ma", fill=ink if not stroke else cream,
                   stroke_width=max(2, stroke // 2) if stroke else 0, stroke_fill=forest)
        if per == 1 and not hanzi_chars(it["_title"]):
            cx = (x0 + x1) / 2
        d.text((cx, top + py_px * 1.3), ch, font=f_h, anchor="ma",
               fill=ink, stroke_width=stroke, stroke_fill=forest)
    if it["_sub"] and ts["style"] != "replace":
        y_en = oy + (-(-len(chars) // per)) * LINE_H(px) + 2
        d.text(((x0 + x1) / 2, y_en), it["_sub"], font=font(EN["px"]), anchor="ma",
               fill=ink, stroke_width=3 if stroke else 0, stroke_fill=forest)
    if ts["style"] == "panel":
        d.rounded_rectangle([x0, y0, x1, y1], 24, outline=(230, 120, 40, 160), width=2)
    im = Image.alpha_composite(im, sim).convert("RGB")
    im.thumbnail((800, 800))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path, quality=80)


if __name__ == "__main__":
    main()
