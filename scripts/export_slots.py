#!/usr/bin/env python3
"""Xuất file vị trí khung tên cho designer từ kết quả scripts/covers.py.

Designer làm sẵn chữ tên truyện (ảnh/khối chữ), file này chỉ nói đặt vào ĐÂU trên từng bìa:
  - templates[]: mỗi khổ bìa có 1 khung tên cố định. Các bìa dùng đúng khung đó là nhóm IDENTICAL,
    chỉ cần thiết kế/căn 1 lần cho cả nhóm (danh sách id trong `covers`).
  - covers[]: từng bìa, khung tên cuối cùng (bbox tỉ lệ 0..1 và px theo ảnh gốc), lý do nếu lệch khỏi khung chung:
      placement = "identical"  -> đúng khung chung của khổ
                  "shifted"    -> cùng cỡ khung chung nhưng dời chỗ vì nền ở khung chung làm chữ chìm
                  "replace"    -> bìa in sẵn tên tiếng Anh, khung = vùng tên cũ (designer xoá chữ Anh)
      backing  = "none" (nền yên, đặt chữ trực tiếp) | "panel" (nền nhiều hoạ tiết, cần nền lót dưới chữ)

Dùng:
  python3 scripts/export_slots.py out/covers/covers.json mapping/covers/cover_slots.json
"""
import json, sys
from collections import defaultdict

MARGIN = 32  # px trên khung 1180, như covers.py


def inset(bbox, size, frame_w=1180):
    """Khung tên = dải cố định trừ lề an toàn 32px (theo khung hiển thị rộng 1180px)."""
    s = frame_w / size[0]
    W, H = size[0] * s, size[1] * s
    mx, my = MARGIN / W, MARGIN / H
    x, y, w, h = bbox
    return [round(x + mx, 4), round(y + my, 4), round(max(0.01, w - 2 * mx), 4), round(max(0.01, h - my), 4)]


def px(bbox, size):
    return [round(bbox[0] * size[0]), round(bbox[1] * size[1]), round(bbox[2] * size[0]), round(bbox[3] * size[1])]


def main(src, dst):
    d = json.load(open(src))
    templates, members = {}, defaultdict(list)
    for f in d["formats"]:
        slot = f["title_slot"]
        templates[f["format"]] = {"template_id": f"{f['format']}-title", "format": f["format"], "aspect": f["aspect"],
                                  "position": slot["position"], "bbox_raw": slot["bbox"]}
    covers = []
    for c in d["covers"]:
        t = templates[c["format"]]
        ts = c["title_slot"]
        area = inset(ts["slot_bbox"], c["size"])
        if ts["style"] == "replace":
            placement, bbox = "replace", ts["text_box"]
        elif ts["source"] == "shifted":
            tb = ts["text_box"]   # hộp chữ đã kiểm tra đọc rõ; khung cùng cỡ khung chung, căn giữa theo hộp đó
            placement = "shifted"
            x = tb[0] + tb[2] / 2 - area[2] / 2
            bbox = [round(min(max(0, x), 1 - area[2]), 4), round(min(max(0, tb[1]), 1 - area[3]), 4), area[2], area[3]]
        else:
            placement, bbox = "identical", area
        if placement == "identical":
            members[t["template_id"]].append(c["id"])
        covers.append({
            "id": c["id"], "title_en": c["title_en"], "title_zh": c["title"] if c["title_source"] != "title_en" else "",
            "image": c["image"], "image_size": c["size"], "format": c["format"],
            "template_id": t["template_id"], "placement": placement,
            "bbox": bbox, "bbox_px": px(bbox, c["size"]),
            "anchor": {"x": round(bbox[0] + bbox[2] / 2, 4), "y": bbox[1], "align": "top-center"},
            "backing": "panel" if ts["style"] == "panel" else "none",
            "cover_text_flag": c.get("cover_text_flag", "unknown"),
            "note": ts["reason"],
        })
    out_t = []
    for t in templates.values():
        ids = members[t["template_id"]]
        any_c = next((c for c in d["covers"] if c["format"] == t["format"]), None)
        bbox = inset(t.pop("bbox_raw"), any_c["size"])
        out_t.append({**t, "bbox": bbox, "anchor": {"x": round(bbox[0] + bbox[2] / 2, 4), "y": bbox[1], "align": "top-center"},
                      "identical_count": len(ids), "covers": ids})
    out_t.sort(key=lambda t: -t["identical_count"])
    res = {
        "schema": "cover-slots/v1",
        "note": "Vị trí khung tên truyện trên bìa để đặt chữ đã thiết kế. bbox = [x, y, rộng, cao] theo tỉ lệ 0..1 của ảnh bìa, gốc trên-trái; bbox_px theo ảnh gốc.",
        "templates": out_t,
        "summary": {
            "covers": len(covers),
            "identical": sum(c["placement"] == "identical" for c in covers),
            "shifted": sum(c["placement"] == "shifted" for c in covers),
            "replace": sum(c["placement"] == "replace" for c in covers),
            "backing_panel": sum(c["backing"] == "panel" for c in covers),
            "flag_title": sum(c["cover_text_flag"] == "title" for c in covers),
            "flag_text": sum(c["cover_text_flag"] == "text" for c in covers),
        },
        "covers": covers,
    }
    json.dump(res, open(dst, "w"), ensure_ascii=False, indent=1)
    print(json.dumps(res["summary"], ensure_ascii=False))
    for t in out_t:
        print(t["template_id"], t["position"], t["bbox"], t["identical_count"])


if __name__ == "__main__":
    main(*sys.argv[1:3])
