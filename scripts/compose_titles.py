#!/usr/bin/env python3
"""Nối tên truyện designer đã thiết kế với bìa, khoá nối là MÃ SÁCH (id, vd SW-266338).

1) Xuất bảng giao việc cho designer: mỗi dòng 1 bìa, tên file phải đặt, cỡ khung tối đa.
     python3 scripts/compose_titles.py sheet mapping/covers/cover_slots.json mapping/covers/title_sheet.csv
   Designer làm tên cho từng bìa, xuất PNG nền trong suốt, ĐẶT TÊN FILE = id (vd SW-266338.png),
   cỡ không vượt `design_w × design_h` (px ở khung hiển thị rộng 1180px). Bìa cùng template_id
   có cùng vị trí, có thể làm theo lô.

2) Ghép: đọc thư mục PNG, đặt từng file vào đúng khung của bìa có cùng id.
     python3 scripts/compose_titles.py compose mapping/covers/cover_slots.json titles/ out/composed/
   Ảnh được thu (giữ tỉ lệ, không phóng to quá khung) cho vừa khung, canh theo điểm neo
   (mép trên; trái / giữa / phải theo anchor.align). Ra out/composed/<id>.jpg + title_map.json
   (id -> file tên, ảnh bìa, vị trí px đã đặt) để app dùng; báo file thiếu / file thừa không khớp id.
"""
import csv, io, json, os, sys, urllib.request

from PIL import Image

FRAME_W = 1180


def sheet(slots, dst):
    d = json.load(open(slots))
    with open(dst, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["id", "file_name", "title_zh", "title_en", "cover_bucket", "needs_human", "template_id", "placement", "align",
                    "design_w", "design_h", "chars", "lines", "backing", "check", "note"])
        for c in d["covers"]:
            s = FRAME_W / c["image_size"][0]
            bw, bh = c["bbox"][2] * c["image_size"][0] * s, c["bbox"][3] * c["image_size"][1] * s
            L = c.get("length", {})
            flags = [x for x in (c["placement"] if c["placement"] in ("no_room", "replace") else "",
                                 L.get("check") if L.get("check") not in (None, "ok") else "") if x]
            w.writerow([c["id"], f"{c['id']}.png", c["title_zh"], c["title_en"], c.get("cover_bucket"),
                        "yes" if c.get("needs_human") else "", c["template_id"] or "riêng",
                        c["placement"], c["anchor"]["align"], round(bw), round(bh), L.get("chars"), L.get("lines"),
                        c["backing"], ",".join(flags), c["note"]])
    print(f"{len(d['covers'])} dòng -> {dst}")


def fetch(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return Image.open(io.BytesIO(r.read())).convert("RGBA")


def cover_image(c, cache="out/cache"):
    """Ảnh bìa đúng như lúc tính khung: ảnh trang bìa, trang hero, hoặc trang 1 PDF đã cắt (dùng lại covers.pdf_cover)."""
    if not c.get("image_page"):
        return fetch(c["image"])
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import covers
    base = covers.cs.BASE
    pg = covers.pdf_cover(cache, {"id": c["id"], "source": c["source"], "pdf": c["image"][len(base):]})
    return Image.open(pg["_local"]).convert("RGBA")


def compose(slots, titles, out):
    d = json.load(open(slots))
    os.makedirs(out, exist_ok=True)
    files = {os.path.splitext(f)[0]: os.path.join(titles, f) for f in os.listdir(titles)
             if f.lower().endswith((".png", ".webp"))}
    by_id = {c["id"]: c for c in d["covers"]}
    done, missing = {}, []
    for cid, c in by_id.items():
        if cid not in files:
            missing.append(cid)
            continue
        cover = cover_image(c)
        W, H = cover.size
        x, y, bw, bh = c["bbox"][0] * W, c["bbox"][1] * H, c["bbox"][2] * W, c["bbox"][3] * H
        t = Image.open(files[cid]).convert("RGBA")
        k = min(bw / t.width, bh / t.height)
        t = t.resize((max(1, round(t.width * k)), max(1, round(t.height * k))), Image.LANCZOS)
        align = c["anchor"]["align"].split("-")[1]
        px = {"left": x, "center": x + (bw - t.width) / 2, "right": x + bw - t.width}[align]
        pos = (round(px), round(y))
        cover.alpha_composite(t, pos)
        cover.convert("RGB").save(os.path.join(out, f"{cid}.jpg"), quality=90)
        done[cid] = {"title_file": os.path.basename(files[cid]), "cover_image": c["image"],
                     "placed_px": [pos[0], pos[1], t.width, t.height], "scale": round(k, 4), "fit": round(k * FRAME_W / W, 3),
                     "bbox": c["bbox"], "anchor": c["anchor"]}
    extra = sorted(set(files) - set(by_id))
    json.dump({"schema": "title-map/v1", "covers": done, "missing_title": missing, "unmatched_files": extra},
              open(os.path.join(out, "title_map.json"), "w"), ensure_ascii=False, indent=1)
    # fit = cỡ PNG sau khi đặt so với cỡ thiết kế ở khung 1180px; < 0.7 là PNG to hơn khung nhiều (sai số dòng / quá to)
    small = sorted(cid for cid, v in done.items() if v["fit"] < 0.7)
    flagged = sorted(cid for cid in done if by_id[cid]["placement"] in ("no_room", "replace"))
    lines = [f"# Ghép tên vào bìa", "",
             f"- Đã ghép: **{len(done)}** / {len(by_id)} bìa",
             f"- Còn thiếu tên: {len(missing)}",
             f"- File không khớp mã sách nào: {len(extra)}" + (f" ({', '.join(extra[:20])})" if extra else ""),
             f"- PNG phải thu nhỏ dưới 70% cỡ thiết kế (kiểm tra số dòng / design_w × design_h): {len(small)}" + (f" ({', '.join(small[:20])})" if small else ""),
             f"- Bìa cần người xem (kín hình / thay tên in sẵn): {len(flagged)}" + (f" ({', '.join(flagged[:20])})" if flagged else "")]
    open(os.path.join(out, "report.md"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    cmd, *a = sys.argv[1:]
    {"sheet": sheet, "compose": compose}[cmd](*a)
