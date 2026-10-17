#!/usr/bin/env python3
"""Xuất file vị trí khung tên cho designer từ kết quả scripts/covers.py.

Designer làm sẵn chữ tên truyện (ảnh/khối chữ), file này chỉ nói đặt vào ĐÂU trên từng bìa.
Rule chính: tên KHÔNG được đè lên hình vẽ hay hoạ tiết. Mỗi bìa được đặt vào chỗ trống thật
(>= 95% diện tích hộp trên nền trống ở thang thô, <= 5% điểm là cạnh hoạ tiết ở thang mịn).

  - templates[]: neo chuẩn theo khổ bìa (giữa-trên, trái-trên, phải-trên, giữa-dưới, ...). Các bìa đặt
    đúng một neo là nhóm IDENTICAL: designer căn 1 lần cho cả nhóm (danh sách id trong `covers`).
  - cover_bucket: A bìa sạch | B có chữ in sẵn (xoá bằng inpaint rồi như A) | C kín hình (nới canvas / dải tên,
    luôn cần người xem) | D không có trang bìa (dựng từ hero_page). Bìa sách PDF lấy từ trang 1 (pdf_crop:
    spread_right_half = nửa phải bìa trải đôi Book Dash, embedded_image = tranh chính của trang tên GDL).
  - covers[]: từng bìa, khung tên cuối cùng (bbox tỉ lệ 0..1 và px theo ảnh gốc):
      placement = "identical"  -> đúng một neo chuẩn của khổ, chỗ đó trống (template_id cho biết neo nào)
                  "shifted"    -> mọi neo chuẩn đều đè hình, dời tới chỗ trống thật gần vị trí cố định nhất
                                  (ưu tiên phần ba trên, rồi phần ba dưới, rồi dải giữa)
                  "replace"    -> bìa in sẵn tên tiếng Anh, khung = vùng tên cũ (designer xoá chữ Anh)
                  "no_room"    -> bìa kín hình, không chỗ nào trống đủ: bbox = chỗ đè ít hình nhất, cần người xem
      length   = rule độ dài tên: chars (số chữ Hán, hoặc độ rộng em với tên tiếng Anh), font_px, lines (cỡ chữ
                 khung chứa được), check = ok | small (1 dòng, < 30px) | 2_lines (tên > 6 chữ, chia đều 2 dòng)
                 | too_long (> 16 chữ hoặc 2 dòng vẫn không vừa: cần rút gọn / người xem). Tên <= 6 chữ luôn 1 dòng.
      bbox     = chỗ trống designer được dùng (đã nới ngang tới bề rộng khung chung nếu vẫn trống)
      backing  = "none" (đặt chữ trực tiếp) | "panel" (chỗ trống nhưng màu nền làm chữ kem kém tương phản,
                 lót panel nhẹ; không bao giờ dùng panel để che hình)

Dùng:
  python3 scripts/export_slots.py out/covers/covers.json mapping/covers/cover_slots.json
"""
import json, sys
from collections import defaultdict

import numpy as np


# 4 loại bìa (cover triage)
ACTION = {
    "A": "Bìa sạch: đặt tên vào khung",
    "B": "Có chữ in sẵn trong tranh: xoá chữ bằng inpaint (inpaint_bboxes), rồi đặt tên như loại A",
    "C": "Kín hình: nới canvas lên trên hoặc dùng dải tên đặc (title_band); luôn cần người xem",
    "D": "Không có trang bìa: dựng bìa từ trang hero_page, rồi đặt tên như loại A; cần người xem",
}


def px(bbox, size):
    return [round(bbox[0] * size[0]), round(bbox[1] * size[1]), round(bbox[2] * size[0]), round(bbox[3] * size[1])]


def anchor_of(bbox, name):
    """Điểm neo: mép trên, căn theo cạnh của neo (trái / giữa / phải)."""
    h = (name or "top-center").split("-")[1]
    x = {"left": bbox[0], "center": bbox[0] + bbox[2] / 2, "right": bbox[0] + bbox[2]}[h]
    return {"x": round(x, 4), "y": bbox[1], "align": f"top-{h}"}


def main(src, dst):
    d = json.load(open(src))
    aspect = {f["format"]: f["aspect"] for f in d["formats"]}
    members = defaultdict(list)
    covers = []
    for c in d["covers"]:
        ts = c["title_slot"]
        room = ts.get("room_bbox", ts["text_box"])   # chỗ trống thật đã kiểm tra: không đè hình
        name = ts.get("anchor_name")
        if ts["style"] == "replace":
            placement, bbox = "replace", ts["text_box"]
        elif ts["source"] == "no_room":
            placement, bbox = "no_room", ts["text_box"]
        elif ts["source"] == "shifted":
            placement, bbox = "shifted", room
        else:
            placement, bbox = "identical", room
        tid = f"{c['format']}-{name}" if placement == "identical" else None
        if tid:
            members[tid].append((c["id"], bbox))
        covers.append({
            "id": c["id"], "title_en": c["title_en"], "title_zh": c["title"] if c["title_source"] != "title_en" else "",
            "source": c["source"], "image": c["image"], "image_page": c.get("image_page"), "pdf_crop": c.get("pdf_crop"),
            "image_size": c["size"], "format": c["format"],
            "cover_bucket": c.get("cover_bucket"), "bucket_action": ACTION.get(c.get("cover_bucket")),
            "cover_from": c.get("cover_from"), "hero_page": c.get("hero_page"),
            "inpaint_bboxes": c.get("inpaint_bboxes") or [], "title_band": c.get("title_band"),
            "needs_human": c.get("needs_human", False),
            "template_id": tid, "placement": placement,
            "bbox": bbox, "bbox_px": px(bbox, c["size"]),
            "anchor": anchor_of(bbox, name if placement == "identical" else None),
            "backing": "panel" if ts["style"] == "panel" else "none",
            "length": {"chars": c["title_len"], "font_px": ts["font_px"], "lines": ts["lines"],
                       "check": ts.get("length_check", "ok")},
            "cover_text_flag": c.get("cover_text_flag", "unknown"),
            "note": ts["reason"],
        })
    out_t = []
    for tid, mem in members.items():
        fmt, name = tid.split("-", 1)
        b = np.median([m[1] for m in mem], 0)   # khung điển hình của nhóm; mỗi bìa vẫn có bbox riêng
        bbox = [round(float(v), 4) for v in b]
        out_t.append({"template_id": tid, "format": fmt, "aspect": aspect.get(fmt), "position": name,
                      "bbox": bbox, "anchor": anchor_of(bbox, name),
                      "identical_count": len(mem), "covers": [m[0] for m in mem]})
    out_t.sort(key=lambda t: -t["identical_count"])
    res = {
        "schema": "cover-slots/v2",
        "note": ("Vị trí khung tên truyện trên bìa để đặt chữ đã thiết kế, không đè lên hình vẽ. "
                 "bbox = [x, y, rộng, cao] theo tỉ lệ 0..1 của ảnh bìa, gốc trên-trái; bbox_px theo ảnh gốc."),
        "templates": out_t,
        "summary": {
            "covers": len(covers),
            "identical": sum(c["placement"] == "identical" for c in covers),
            "shifted": sum(c["placement"] == "shifted" for c in covers),
            "replace": sum(c["placement"] == "replace" for c in covers),
            "no_room": sum(c["placement"] == "no_room" for c in covers),
            **{f"bucket_{k}": sum(c["cover_bucket"] == k for c in covers) for k in "ABCD"},
            "needs_human": sum(c["needs_human"] for c in covers),
            "backing_panel": sum(c["backing"] == "panel" for c in covers),
            "length_2_lines": sum(c["length"]["check"] == "2_lines" for c in covers),
            "length_small": sum(c["length"]["check"] == "small" for c in covers),
            "length_too_long": sum(c["length"]["check"] == "too_long" for c in covers),
            "flag_title": sum(c["cover_text_flag"] == "title" for c in covers),
            "flag_text": sum(c["cover_text_flag"] == "text" for c in covers),
        },
        "covers": covers,
    }
    res["buckets"] = ACTION
    json.dump(res, open(dst, "w"), ensure_ascii=False, indent=1)
    print(json.dumps(res["summary"], ensure_ascii=False))
    for t in out_t:
        print(t["template_id"], t["bbox"], t["identical_count"])


if __name__ == "__main__":
    main(*sys.argv[1:3])
