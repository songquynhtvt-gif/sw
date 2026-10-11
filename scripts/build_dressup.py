#!/usr/bin/env python3
"""Build the dress-up page layers (Hǔhǔ, Wuwu, Dudu) from the v3 object sheet (assets/closet/v3/items/NN.png).

Every item becomes one pose-framed layer per companion with the body interaction baked in, so the
page only stacks layers by z (back < body < shadow < feet < shoulders < neck < head < hand):
  - placements are written for Hǔhǔ and carried to the others through slot frames
    (head: brim point + skull width, neck: chin centre + jaw width, back: torso centre + width)
  - hats sit between / in front of the ears; rings lose the part behind the head top
  - neck items are tucked under the chin (pixels over the head removed); scarves wrap the neck
  - worn items show only their outside: tops fill the torso and arms, gloves the hands,
    boots the feet, each inside the companion's own outline
  - held items sit in the paw: a drawn paw (Hǔhǔ) or the companion's own paws redrawn on top
Base poses: Hǔhǔ front idle; Wuwu / Dudu from scripts/prep_mascots.py.
Output: docs/hu-hu-thay-do/<companion>/layers/*.webp, thumbs/*.webp, data.json
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fit_preview as fp  # noqa: E402

ITEMS = fp.ROOT / "assets/closet/v3/items"
OUT = fp.ROOT / "docs/hu-hu-thay-do"
Z = {"back": 0, "feet": 3, "shoulders": 4, "neck": 5, "head": 6, "hand": 7}
SLOT_VI = {"head": "Đầu", "neck": "Cổ", "shoulders": "Vai", "back": "Lưng", "hand": "Tay", "feet": "Chân"}

# file, id, name, slot, placement. Placement (fractions of Hǔhǔ's pose): x = centre, w = width,
# and one of bottom / top / cy for the vertical edge. wrap: ring around the head.
CATALOG = [
    ("v4:s2-05", "mu-chin-tang-gio", "Mũ Chín Tầng Gió", "head", dict(x=.495, w=.52, bottom=.262, ears="behind")),
    ("v4:s3-06", "mu-la-bon-mua", "Mũ Lá Đổi Màu", "head", dict(x=.495, w=.60, bottom=.262, ears="behind")),
    ("02", "mu-tan-bong-bay", "Mũ Tán Bóng Bay", "head", dict(x=.495, w=.54, bottom=.26, ears="behind")),
    ("03", "mu-mang-bay-dot", "Mũ Măng Bảy Đốt", "head", dict(x=.495, w=.46, bottom=.255, ears="behind")),
    ("v4:s3-05", "hoa-hai-mau", "Hoa Hai Màu", "head", dict(x=.25, w=.22, cy=.22, ears="front")),
    ("05", "vong-dom-dom", "Vòng Đom Đóm", "head", dict(x=.50, w=.62, bottom=.285, ears="front", wrap=.66)),
    ("26", "cai-la", "Cài Lá", "head", dict(x=.76, w=.20, cy=.21, ears="front")),
    ("07", "khan-nam-dong-song", "Khăn Năm Dòng Sông", "neck", dict(x=.51, w=.46, top=.50, band=True)),
    ("v4:s2-07", "mat-day-vong-trang", "Mặt Dây Vòng Trăng", "neck", dict(x=.50, w=.24, top=.525)),
    ("v4:s2-06", "chuoi-da-bay", "Chuỗi Đá Bay", "neck", dict(x=.50, w=.42, top=.50)),
    ("v4:s3-08", "binh-sam", "Bình Sấm Con", "neck", dict(x=.50, w=.24, top=.525)),
    ("09", "khan-la-biet-bay", "Khăn Lá Biết Bay", "neck", dict(x=.50, w=.44, top=.50, band=True)),
    ("15", "khan-gio", "Khăn Gió", "neck", dict(x=.52, w=.50, top=.50, band=True)),
    ("17", "khan-la-soc", "Khăn Lá Sọc", "neck", dict(x=.50, w=.60, top=.50, band=True)),
        ("32", "chuoi-hat-go", "Chuỗi Hạt Gỗ", "neck", dict(x=.50, w=.40, top=.44)),
    ("33", "no-la", "Nơ Lá", "neck", dict(x=.50, w=.42, top=.47)),
    ("10", "ao-choang-la", "Áo Choàng Lá", "shoulders", dict(worn="top")),
    ("v4:s3-03", "ao-choang-vay-da", "Áo Choàng Vảy Đá", "shoulders", dict(worn="top")),
    ("v4:s3-07", "ao-choang-buom-dem", "Áo Choàng Bướm Đêm", "shoulders", dict(worn="top")),
    ("16b", "canh-nho", "Cánh Nhỏ", "back", dict(x=.50, w=1.10, cy=.47)),
    ("13", "gio-hat-mam", "Giỏ Hạt Mầm", "hand", dict(h=.24, grip=(.50, .05))),
    ("v4:s3-01", "tui-hat-mam", "Túi Hạt Mầm", "hand", dict(h=.30, grip=(.50, .62))),
    ("v4:s2-01", "binh-dom-dom", "Bình Đom Đóm", "hand", dict(h=.20, grip=(.50, .12))),
    ("v4:s2-08", "tui-mai-ngoi", "Túi Mái Ngói", "hand", dict(h=.26, grip=(.55, .04))),
    ("v4:s2-02", "sach-buom-dem", "Sổ Bản Đồ Bướm", "hand", dict(h=.24, grip=(.42, .86))),
    ("v4:s2-03", "gay-gio", "Gậy Gió Núi", "hand", dict(h=.40, grip=(.30, .82), mirror=True)),
    ("v4:s3-02", "gay-trang", "Gậy Trăng Lặn", "hand", dict(h=.38, grip=(.20, .86), mirror=True)),
    ("v4:s2-04", "ong-tre", "Đốt Trúc Biết Bay", "hand", dict(h=.40, grip=(.45, .72), mirror=True)),
    ("v4:s3-04", "dieu-la", "Diều Gió Chạy", "hand", dict(h=.34, grip=(.42, .45), mirror=True, fly=(.08, .40))),
    ("23", "binh-ngoc-xanh", "Bình Ngọc Xanh", "hand", dict(h=.21, grip=(.52, .06))),
    ("12", "tui-la", "Túi Lá", "hand", dict(h=.23, grip=(.81, .07))),
    ("21", "dieu-gio-chay", "Diều Gió Chạy", "hand", dict(h=.34, grip=(.05, .33), mirror=True, fly=(.08, .40))),
    ("22", "dua-la", "Đũa Lá", "hand", dict(h=.42, grip=(.14, .80), mirror=True)),
    ("18+19", "gang-tay-la", "Găng Tay Lá", "hand", dict(pair="paws", top=.70)),
    ("14", "giay-la", "Giày Lá", "feet", dict(pair="feet", top=.85)),
]
# 🔴 in the v2 scoring (tudo-mythic-v2 §8): kept in CATALOG for reference, not built or shown
HIDDEN = {"binh-ngoc-xanh", "ao-choang-la", "khan-gio", "khan-la-soc", "no-la", "cai-la",
          "chuoi-hat-go", "gang-tay-la", "giay-la", "tui-la",
          "gio-hat-mam", "dieu-gio-chay",               # replaced by v4 art
          # not ok in the reviews: Christmas-tree hat, scarf without its flying leaves, angel wings,
          # faces on the fireflies / seeds (no eyes or faces on objects)
          "mu-mang-bay-dot", "khan-la-biet-bay", "canh-nho", "binh-dom-dom", "tui-hat-mam"}

# Every item comes from one of the 13 lands (Brief v13.4 §09B, founder 10/10).
REGION_OF = {
    "sach-buom-dem": "C0", "vong-dom-dom": "C1", "non-la-dudu": "C1", "gay-tre": "C1",
    "mu-tan-bong-bay": "C2", "ao-choang-buom-dem": "C2", "khan-nam-dong-song": "C3",
    "gay-trang": "C4", "ong-tre": "C5", "chuoi-da-bay": "C6",
    "mu-chin-tang-gio": "C7", "binh-sam": "C7", "gay-gio": "C7", "ao-choang-vay-da": "C8",
    "mat-day-vong-trang": "C9", "dieu-la": "C10", "dua-la": "C10", "tui-mai-ngoi": "C11",
    "hoa-hai-mau": "C12", "mu-la-bon-mua": "C12",
}
# What the item is, one line, tied to its land.
ABOUT = {
    "sach-buom-dem": "Sổ ông bà cố để lại: lật trang nào, bướm đêm bay ra trang đó.",
    "vong-dom-dom": "Đom đóm của xóm tre bay vòng quanh đầu, như những ngọn đèn nhỏ.",
    "non-la-dudu": "Chiếc nón quen thuộc mà Chó Đội Nón nhận ra ngay.",
    "gay-tre": "Gậy tre đi đường của Dudu, chặt từ con đường tre trong xóm.",
    "mu-tan-bong-bay": "Tán cây bé xíu lơ lửng trên đầu, nhặt được lúc chơi trốn tìm với Hổ Tinh.",
    "ao-choang-buom-dem": "Áo choàng màu đêm, bướm trắng đậu quanh gấu áo như những đôi mắt trong lá.",
    "khan-nam-dong-song": "Năm dải khăn chảy như năm nhánh sông, một đầu thành chú cá nhỏ.",
    "gay-trang": "Mảnh trăng Ngư Tinh trả lại sau khi lặn xuống rồi nổi lên.",
    "ong-tre": "Đốt trúc thứ bảy, đốt mà Hùng Tinh đếm cùng bé, tự nhảy lên khỏi thân.",
    "chuoi-da-bay": "Năm hòn đá nhỏ lơ lửng, không bao giờ chạm nhau, như Hầu Tinh nhảy đá.",
    "mu-chin-tang-gio": "Chín tầng vải như chín tầng gió, dải gió bay ngược lên trời.",
    "binh-sam": "Một tia sấm nhỏ trên đỉnh núi gió, nhốt trong bình.",
    "gay-gio": "Gió núi quấn quanh cây gậy, nơi Đại Bàng Tinh tập hạ cánh.",
    "ao-choang-vay-da": "Vảy đá xếp lớp, một đường vàng uốn lượn như dấu Chằn Tinh để lại.",
    "mat-day-vong-trang": "Vực nước nhỏ trong mặt dây, bóng trăng nằm yên giữa vòng sóng.",
    "dieu-la": "Diều lá chạy đua với gió trên đồng cỏ của Thỏ Tinh.",
    "dua-la": "Đũa lá vẫy gió, dải lụa bay theo như tai Thỏ Tinh.",
    "tui-mai-ngoi": "Nắp túi là mái ngói nhỏ, dấu chân vàng chạy vào ô cửa sổ như Chuột Tinh.",
    "hoa-hai-mau": "Mỗi cánh hoa hai màu, như hoa trong vườn ảo ảnh cứ đổi màu mãi.",
    "mu-la-bon-mua": "Bốn chiếc lá bốn màu: mưa, nắng, thu, xanh. Mũ đổi màu như vườn hoa ảo ảnh.",
}
# Brief v13.4 §09B: land, English name, keeper, story (bé's view).
REGIONS = {
    "C0": ("Nhà Nhỏ Bên Đồi", "Little House on the Hill", "", "Bé tìm thấy bản đồ cũ của ông bà cố trong nhà. Tấm bản đồ có những vùng đất lạ. Bé chọn bạn đồng hành và bắt đầu chuyến đi."),
    "C1": ("Xóm Tre Đèn Sáng", "Bamboo Lantern Hamlet", "🐕 Chó Đội Nón", "Bé đến một ngôi làng nhỏ. Chó nhận ra chiếc nón quen thuộc và dẫn bé đi qua con đường tre khi những chiếc đèn lần lượt sáng lên."),
    "C2": ("Rừng Ngàn Mắt", "Forest of a Thousand Eyes", "🐯 Hổ Tinh", "Trong khu rừng, bé nhìn thấy những đôi mắt sáng giữa tán lá. Hổ bật mí đó chỉ là những người bạn đang chơi trốn tìm."),
    "C3": ("Bến Năm Dòng", "Five-Stream Wharf", "🐊 Sấu Năm Chèo", "Bé đến một bến nước nơi dòng sông chia thành nhiều nhánh. Sấu xuất hiện và khoe điều đặc biệt nhất của mình: năm chiếc chân."),
    "C4": ("Vịnh Nuốt Trăng", "Moon-Swallowing Bay", "🐟 Ngư Tinh", "Bé đến biển vào một đêm trăng. Ngư Tinh xuất hiện dưới mặt nước và chơi đùa với bóng trăng trên lưng mình."),
    "C5": ("Rừng Thất Trúc", "Seven-Node Bamboo Forest", "🐻 Hùng Tinh", "Bé gặp Hùng Tinh giữa rừng trúc. Hùng Tinh rất yêu một cây trúc đặc biệt và cùng bé đếm đủ bảy đốt trên thân cây."),
    "C6": ("Rừng Đá Nhảy", "Jumping Stone Forest", "🐒 Hầu Tinh", "Bé nghe tiếng động trong rừng rồi gặp Hầu Tinh. Hầu Tinh đưa bé xem cách mình nhảy từ tảng đá này sang tảng đá khác."),
    "C7": ("Đỉnh Chín Tầng Gió", "Nine-Wind Peak", "🦅 Đại Bàng Tinh", "Bé leo lên một ngọn núi đầy gió và gặp Đại Bàng Tinh. Đại Bàng bay rất giỏi nhưng vẫn đang tập cách hạ cánh thật đẹp."),
    "C8": ("Thung Lũng Vảy Đá", "Stone-Scale Valley", "🐍 Chằn Tinh", "Bé nhìn thấy những dấu dài uốn quanh các tảng đá. Chằn Tinh xuất hiện và tiết lộ đó là dấu mình để lại."),
    "C9": ("Vực Ngân Nguyệt", "Silver Moon Gorge", "🐉 Thuồng Luồng", "Bé đến một vực nước sáng dưới ánh trăng. Thuồng Luồng nhút nhát xuất hiện và dẫn bé xem nơi mình thích bơi nhất."),
    "C10": ("Đồng Cỏ Gió Chạy", "Wind-Racing Meadow", "🐰 Thỏ Tinh", "Bé gặp Thỏ Tinh trên một đồng cỏ rộng. Thỏ chạy nhanh đến mức tưởng như đang chạy đua với gió."),
    "C11": ("Phố Mái Ngói", "Tiled-Roof Street", "🐭 Chuột Tinh", "Khi trời tối, bé nghe tiếng động trên những mái nhà. Chuột Tinh xuất hiện và chơi trò trốn tìm trên mái ngói."),
    "C12": ("Vườn Hoa Ảo Ảnh", "Mirage Flower Garden", "🦊 Cáo Quỷ", "Ở điểm cuối bản đồ, bé gặp Cáo Quỷ trong một khu vườn kỳ lạ. Những bông hoa liên tục đổi màu và hình dạng."),
}
GEN = fp.ROOT / "assets/char/gen"
FITTED = fp.ROOT / "assets/closet/v3/fitted"   # <companion>/<item id>.png: art drawn to fit that body (prompts/closet/fitted-wearables.md)
# Per companion geometry, fractions of its own pose.
#   head / neck / back: slot frames (x, y, width) -> Hǔhǔ placements are scaled into them
#   chin: jaw line (left to right) - neck items are erased above it, tops start below it
#   skull: ellipse (x, y, rx, ry) for rings; grip: where held items are held
#   grip_mask: ellipses (x, y, rx, ry) of the companion's own paws, redrawn over held items
#   gloves: per hand, a seed inside it, its row / column range and which side the cuff is on
#   feet: foot centre x values; top garment: torso seeds, bottom row, arm seeds and rows
#   shoulder / hip: tops span the body width at the shoulder row and end at the hips. Checked against the proportion guides (11 Oct, form 1, head top -> ground):
#     Hǔhǔ eyes .28 chin .43 shoulders .50 hips .77 knees .88 · Wuwu .18 .41 .45 .75 .88 ·
#     Dudu .18 .39 .42 .78 .87 (hat brims sit halfway between head top and eyes)
#   hand_scale: held items' size against Hǔhǔ's; fit: per item touch-ups (dx, dy, scale)
MASCOTS = {
    "huhu": dict(name="Hǔhǔ", hip=.80, shoulder=.60, pose="assets/char/gen/huhu-front-idle.png", ink=(46, 83, 59),
                 head=(.495, .255, .606), neck=(.498, .548, .648), back=(.50, .47, .62),
                 chin=[(.174, .509), (.311, .536), (.498, .548), (.685, .536), (.822, .509)],
                 skull=(.492, .376, .311, .251), grip=(.215, .855), grip_kind="paw", hand_scale=1.0, fly=(.08, .40),
                 gloves=[dict(seed=(.205, .80), rows=(.70, .866), cols=(.15, .26), cuff="top"),
                         dict(seed=(.744, .80), rows=(.70, .866), cols=(.70, .78), cuff="top")],
                 feet=[.318, .645], foot_rows=(.85, .94),
                 torso=[(.50, .70)], torso_bottom=.865, drop_white=True,
                 arms=[((.205, .80), (.15, .26)), ((.744, .80), (.70, .78))], arm_rows=(.60, .866)),
    "wuwu": dict(name="Wuwu", hip=.785, shoulder=.53, pose="assets/char/gen/wuwu/wuwu-dressup-base.png", ink=(11, 34, 61),
                 head=(.50, .19, .64), neck=(.50, .478, .72), back=(.50, .58, .80),
                 chin=[(.19, .42), (.33, .462), (.50, .478), (.67, .462), (.81, .42)],
                 skull=(.50, .30, .31, .22), grip=(.50, .62), grip_kind="mask", hand_scale=1.9, fly=(.10, .26),
                 grip_mask=[(.455, .62, .052, .072), (.545, .62, .052, .072)],
                 fit={"vong-dom-dom": dict(dy=-.035, scale=.9),   # long held items would cover the face
                      "gay-gio": dict(scale=.55), "gay-trang": dict(scale=.55), "ong-tre": dict(scale=.55),
                      "dua-la": dict(scale=.6), "sach-buom-dem": dict(scale=.7)}, paws_front=True,
                 gloves=[dict(seed=(.44, .63), rows=(.50, .72), cols=(.37, .505), cuff="left"),
                         dict(seed=(.56, .63), rows=(.50, .72), cols=(.495, .63), cuff="right")],
                 feet=[.31, .70], foot_rows=(.875, .96),
                 torso=[(.50, .50), (.50, .76)], torso_bottom=.80, drop_white=False,
                 arms=[((.25, .60), None), ((.75, .60), None)], arm_rows=(.44, .72)),
    "dudu": dict(name="Dudu", hip=.796, shoulder=.56, shoulder_span=(.30, .90), pose="assets/char/gen/dudu/dudu-dressup-base.png", ink=(91, 28, 3),
                 head=(.548, .25, .58), neck=(.55, .52, .58), back=(.55, .64, .62),
                 chin=[(.29, .44), (.36, .50), (.43, .565), (.50, .53), (.58, .515), (.68, .49), (.80, .44)],
                 skull=(.548, .36, .272, .24), grip=(.20, .60), grip_kind="mask", hand_scale=1.7, fly=(.08, .30),
                 grip_mask=[(.197, .603, .074, .08)],
                 fit={"vong-dom-dom": dict(dy=-.02), "hoa-hai-mau": dict(dx=.04, dy=.03), "cai-la": dict(dx=-.02, dy=.02)},
                 gloves=[dict(seed=(.17, .60), rows=(.50, .70), cols=(.10, .272), cuff="right"),
                         dict(seed=(.82, .78), rows=(.715, .84), cols=(.74, .90), cuff="top")],
                 feet=[.405, .65], foot_rows=(.87, .94),
                 torso=[(.55, .70)], torso_bottom=.80, drop_white=False,
                 arms=[((.33, .64), (.27, .45)), ((.80, .62), (.72, .92))], arm_rows=(.48, .84),
                 own=[("dudu-own-hat", "non-la-dudu", "Nón Lá Của Dudu", "head"),
                      ("dudu-own-bamboo", "gay-tre", "Gậy Tre", "hand")]),
}
REF = "huhu"


def load(name):
    src = (ITEMS.parent.parent / "v4/items" / f"{name[3:]}.png") if name.startswith("v4:") else ITEMS / f"{name}.png"
    im = Image.open(src).convert("RGBA")
    return im.crop(im.getbbox())


def split_pair(im):
    """Two objects side by side -> (left, right), cut at the widest empty column run."""
    cols = np.asarray(im.getchannel("A")).max(0) > 32
    best, run = (0, im.width // 2), None
    for x in range(im.width):
        if not cols[x]:
            run = x if run is None else run
        elif run is not None:
            if x - run > best[0]:
                best = (x - run, (run + x) // 2)
            run = None
    cut = best[1]
    l, r = im.crop((0, 0, cut, im.height)), im.crop((cut, 0, im.width, im.height))
    return l.crop(l.getbbox()), r.crop(r.getbbox())


def put(canvas, art, x, y_edge, edge, W, H, pad, width=None, height=None):
    if width is not None:
        w = width * W
        h = art.height * w / art.width
    else:
        h = height * H
        w = art.width * h / art.height
    art = art.resize((max(1, round(w)), max(1, round(h))), Image.LANCZOS)
    px = x * W + pad - w / 2
    py = {"bottom": y_edge * H - h, "top": y_edge * H, "cy": y_edge * H - h / 2}[edge] + pad
    layer = Image.new("RGBA", canvas)
    layer.alpha_composite(art, (round(px), round(py)))
    return layer


def erase(layer, mask):
    layer.putalpha(ImageChops.subtract(layer.getchannel("A"), mask))
    return layer


def palette(art):
    """Main colours of the glove art: (body green, cuff cream, band gold)."""
    a = np.asarray(art).reshape(-1, 4)
    px = a[a[:, 3] > 200][:, :3].astype(int)
    r, g, b = px.T
    pick = lambda m: tuple(int(v) for v in np.median(px[m], axis=0))
    return pick((g > r + 15) & (g < 170)), pick((r > 235) & (g > 225) & (b > 180)), pick((r > 220) & (b < 140))


def worn_gloves(pose, art, M, W, H, pad, canvas):
    """Gloves as worn: only the outside shows. Each hand (inside the companion's own outline) is
    filled with the glove; a cream cuff with a gold band is where the arm goes in."""
    green, cream, gold = palette(art)
    ink = M["ink"] + (255,)
    k = 4
    hi = Image.new("RGBA", (canvas[0] * k, canvas[1] * k))
    for g in M["gloves"]:
        hand = fill_region(pose, [g["seed"]], g["rows"][0], g["rows"][1], [g["cols"]])
        ys, xs = np.nonzero(hand)
        x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
        m = Image.fromarray(hand.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(3))
        m = m.resize((W * k, H * k), Image.LANCZOS).point(lambda v: v if v > 8 else 0)
        fill = Image.new("RGBA", (W * k, H * k), green + (255,))
        d = ImageDraw.Draw(fill)
        lw = .004 * H * k
        c1, c2 = .020 * H, .029 * H                    # cuff depth, gold band depth (from the open end)
        if g["cuff"] == "top":
            band = lambda a, b: [0, (y0 + a) * k, W * k, (y0 + b) * k]
            edge = [(0, y0 * k + lw / 2), (W * k, y0 * k + lw / 2)]
            bead = (xs.mean(), y0 + (c1 + c2) / 2)
        else:
            sx = x0 if g["cuff"] == "left" else x1
            sg = 1 if g["cuff"] == "left" else -1
            band = lambda a, b: [min(sx + sg * a, sx + sg * b) * k, 0, max(sx + sg * a, sx + sg * b) * k, H * k]
            edge = [(sx * k + sg * lw / 2, 0), (sx * k + sg * lw / 2, H * k)]
            bead = (sx + sg * (c1 + c2) / 2, ys.mean())
        d.rectangle(band(0, c1), fill=cream + (255,))
        d.rectangle(band(c1, c2), fill=gold + (255,))
        for a in (c1, c2):
            r = band(a, a)
            d.line([(r[0], r[1]), (r[2], r[3])] if g["cuff"] == "top" else [(r[0], 0), (r[0], H * k)], fill=ink, width=round(lw * .7))
        d.line(edge, fill=ink, width=round(lw))
        br = .011 * H * k
        bx, by = bead[0] * k, bead[1] * k
        d.ellipse([bx - br, by - br, bx + br, by + br], fill=gold + (255,), outline=ink, width=round(lw * .7))
        fill.putalpha(ImageChops.multiply(fill.getchannel("A"), m))
        hi.alpha_composite(fill, (pad * k, pad * k))
    return hi.resize(canvas, Image.LANCZOS)


def fill_region(pose, seeds, y0, y1, x_ranges=None, drop_white=False):
    """Fur area of the pose (inside its outlines) reachable from the seeds between rows y0..y1."""
    a = pose.astype(int)
    W, H = pose.shape[1], pose.shape[0]
    lum = a[..., :3] @ np.array([299, 587, 114]) // 1000
    inside = (a[..., 3] > 200) & (lum > 100)
    if drop_white:                                    # the white cheek tufts belong to the head
        inside &= ~((a[..., 0] > 240) & (a[..., 1] > 240) & (a[..., 2] > 235))
    ys = np.arange(H)[:, None]
    lo = y0(np.arange(W))[None, :] if callable(y0) else y0 * H
    inside &= (ys >= lo) & (ys < y1 * H)
    out = np.zeros_like(inside)
    for n, (sx, sy) in enumerate(seeds):
        box = inside.copy()
        if x_ranges and x_ranges[n]:
            xa, xb = x_ranges[n]
            box[:, : round(xa * W)] = False
            box[:, round(xb * W):] = False
        px, py = round(sx * W), round(sy * H)
        if not box[py, px]:                           # seed on a line: start from the nearest fur pixel
            yy, xx = np.nonzero(box[max(0, py - 40):py + 40, max(0, px - 40):px + 40])
            if not len(yy):
                continue
            n = np.argmin((yy - min(py, 40)) ** 2 + (xx - min(px, 40)) ** 2)
            px, py = max(0, px - 40) + xx[n], max(0, py - 40) + yy[n]
        work = Image.fromarray(box.astype(np.uint8) * 255).copy()
        ImageDraw.floodfill(work, (int(px), int(py)), 128, thresh=0)
        got = np.asarray(work) == 128
        shut = Image.fromarray(got.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.MinFilter(9))
        out |= got | ((np.asarray(shut) > 0) & (a[..., 3] > 200) & (lum > 60))   # close thin creases (toe lines)
    return out


def worn_art(art, fur_np, top_y, shoulder_y, bottom_y, W, H, pad, canvas, fur, span=(0, 1)):
    """A garment picture laid on the body, sized to the companion's own measurements
    (proportion guides, 11 Oct): as wide as the body at the shoulder line, from just under the
    chin down to the hips; trimmed to the silhouette so it never spills past the outline."""
    row = np.nonzero(fur_np[round(shoulder_y)])[0]
    row = row[(row >= span[0] * W) & (row <= span[1] * W)]   # an arm held out is not the shoulders
    x0, x1 = row.min(), row.max()
    w = (x1 - x0) * 1.10
    h = bottom_y - top_y
    if h / w > art.height / art.width * 1.35:      # keep the design's shape: at most a little stretch
        h = w * art.height / art.width * 1.35
    elif h / w < art.height / art.width / 1.35:
        h = w * art.height / art.width / 1.35
    art = art.resize((round(w), round(h)), Image.LANCZOS)
    layer = Image.new("RGBA", (W, H))
    layer.alpha_composite(art, (round((x0 + x1) / 2 - w / 2), round(top_y)))
    layer.putalpha(ImageChops.multiply(layer.getchannel("A"), fur))
    out = Image.new("RGBA", canvas)
    out.alpha_composite(layer, (pad, pad))
    return out


def front_boot(region, art, W, H, pad, canvas, ink=fp.OUTLINE):
    """A front-view boot in the boot art's colours, drawn inside the foot's own outline:
    green shaft, cream toe cap, blue sole along the bottom contour, cream rim and gold bead on top."""
    a = np.asarray(art).reshape(-1, 4)
    px = a[a[:, 3] > 200][:, :3].astype(int)
    r, g, b = px.T
    pick = lambda m: tuple(int(v) for v in np.median(px[m], axis=0)) + (255,)
    green, cream = pick((g > r + 15) & (g < 170)), pick((r > 235) & (g > 225) & (b > 180))
    gold, blue = pick((r > 220) & (b < 140)), pick(b > r + 50)
    ink = ink + (255,)
    ys, xs = np.nonzero(region)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    k = 4
    big = lambda m: Image.fromarray(m.astype(np.uint8) * 255).resize((W * k, H * k), Image.LANCZOS)
    img = Image.new("RGBA", (W * k, H * k))
    d = ImageDraw.Draw(img)
    d.rectangle([x0 * k, y0 * k, x1 * k, y1 * k], fill=green)
    lw = .006 * H * k
    toe = y0 + (y1 - y0) * .42                      # cream toe cap, rounded top
    d.ellipse([(x0 - .03 * W) * k, toe * k, (x1 + .03 * W) * k, (y1 + (y1 - y0) * .9) * k], fill=cream, outline=ink, width=round(lw))
    sole_t = round(.022 * H)                        # sole: a band following the bottom contour
    up = np.zeros_like(region)
    up[:-sole_t] = region[sole_t:]
    sole = region & ~up
    soft = big(sole)
    blue_l = Image.new("RGBA", img.size, blue)
    blue_l.putalpha(soft)
    img.alpha_composite(blue_l)
    line = big(np.roll(sole, -2, axis=0) & ~sole & region)
    ink_l = Image.new("RGBA", img.size, ink)
    ink_l.putalpha(line.filter(ImageFilter.MaxFilter(5)))
    img.alpha_composite(ink_l)
    rim = .016 * H                                  # front rim where the leg goes in
    d.rectangle([x0 * k, y0 * k, x1 * k, (y0 + rim) * k], fill=cream)
    d.line([(x0 * k, (y0 + rim) * k), (x1 * k, (y0 + rim) * k)], fill=ink, width=round(lw * .8))
    d.line([(x0 * k, y0 * k + lw / 2), (x1 * k, y0 * k + lw / 2)], fill=ink, width=round(lw))
    cxm = (x0 + x1) / 2
    d.line([(cxm * k, (y0 + rim) * k), (cxm * k, toe * k)], fill=gold, width=round(.012 * H * k))
    br = .016 * H
    by = y0 + rim + br * .9
    d.ellipse([(cxm - br) * k, (by - br) * k, (cxm + br) * k, (by + br) * k], fill=gold, outline=ink, width=round(lw * .8))
    m = big(region).filter(ImageFilter.MaxFilter(5))
    img.putalpha(ImageChops.multiply(img.getchannel("A"), m))
    out = Image.new("RGBA", canvas)
    out.alpha_composite(img.resize((W, H), Image.LANCZOS), (pad, pad))
    return out


def boot_worn(boot, ink=fp.OUTLINE):
    """Cut the boot opening and the back of its rim: on a foot the leg fills the opening, so only
    the front rim shows, with the leg going in behind it."""
    from import_item import regions
    a = np.asarray(boot).astype(int)
    r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    hole = (al > 200) & (g > r + 10) & (r + g + b < 420)
    hole[round(boot.height * .3):] = False             # the opening is in the top part only
    thin = np.asarray(Image.fromarray(hole.astype(np.uint8) * 255).filter(ImageFilter.MinFilter(7))) > 0
    blobs = [m for m in regions(thin) if m.sum() > hole.size * .005]   # eroded: the rim splits them
    top = min(blobs, key=lambda m: np.nonzero(m)[0].mean())    # the topmost green area
    hole &= np.asarray(Image.fromarray(top.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(9))) > 0
    ys, xs = np.nonzero(hole)
    x0, x1 = xs.min(), xs.max()
    cols = np.unique(xs)
    low = np.array([ys[xs == x].max() for x in cols], float)
    fit = np.poly1d(np.polyfit(cols, low, 2))          # smooth front lip of the opening
    edge = fit(np.clip(np.arange(boot.width), x0, x1))
    keep = (np.clip(np.arange(boot.height)[:, None] - edge[None, :], 0, 1) * 255).astype(np.uint8)  # soft edge
    out = boot.copy()
    out.putalpha(ImageChops.multiply(boot.getchannel("A"), Image.fromarray(keep)))
    k = 4
    line = Image.new("RGBA", (boot.width * k, boot.height * k))
    lw = max(2, round(boot.height * .025)) * k
    ImageDraw.Draw(line).line([(x * k, edge[x] * k + lw / 2) for x in range(boot.width)], fill=ink + (255,), width=lw)
    line = line.resize(boot.size, Image.LANCZOS)
    line.putalpha(ImageChops.multiply(line.getchannel("A"), boot.getchannel("A")))
    out.alpha_composite(line)
    return out.crop(out.getbbox())


def neck_band(art, chin, W, H, pad, canvas, body_a, ink=fp.OUTLINE, k_s=1.0):
    """A fabric band in the scarf's own colour, following the jaw line across the whole neck."""
    a = np.asarray(art)
    px = a[a[..., 3] > 200][:, :3].astype(int)
    sat = px.max(1) - px.min(1)
    colour = tuple(int(v) for v in np.median(px[sat >= np.percentile(sat, 60)], axis=0))
    k = 4
    band = Image.new("RGBA", (canvas[0] * k, canvas[1] * k))
    d = ImageDraw.Draw(band)
    u = 825 * k_s                                    # Hǔhǔ's pose height, scaled to this companion
    pts = [((x * W + pad) * k, (y * H + pad + 0.018 * u) * k) for x, y in chin]
    pts = [(pts[0][0] - 0.06 * u * k, pts[0][1] - 0.02 * u * k)] + pts + [(pts[-1][0] + 0.06 * u * k, pts[-1][1] - 0.02 * u * k)]
    d.line(pts, fill=ink + (255,), width=round(0.050 * u * k), joint="curve")
    d.line(pts, fill=colour + (255,), width=round(0.036 * u * k), joint="curve")
    band = band.resize(canvas, Image.LANCZOS)
    band.putalpha(ImageChops.multiply(band.getchannel("A"), body_a))
    return band


def load_pose(M):
    pose = Image.open(fp.ROOT / M["pose"]).convert("RGBA")
    W, H = pose.size
    pad = H // 2  # room for tall hats and long hand items
    canvas = (W + 2 * pad, H + 2 * pad)
    base = Image.new("RGBA", canvas)
    base.alpha_composite(pose, (pad, pad))
    return base, W, H, pad, canvas


class Frame:
    """Carries a Hǔhǔ placement into a companion's slot frame (same spot on the body, scaled)."""
    def __init__(self, M, slot, ref, RW, RH, W, H):
        fx, fy, fw = ref[slot]
        tx, ty, tw = M[slot]
        self.k = tw * W / (fw * RW)
        self.f, self.t, self.RW, self.RH, self.W, self.H = (fx, fy), (tx, ty), RW, RH, W, H

    def pt(self, x, y):  # Hǔhǔ fractions -> companion pose pixels
        return (self.t[0] * self.W + (x - self.f[0]) * self.RW * self.k,
                self.t[1] * self.H + (y - self.f[1]) * self.RH * self.k)


def put_px(canvas, art, X, Y, edge, w, pad):
    h = art.height * w / art.width
    art = art.resize((max(1, round(w)), max(1, round(h))), Image.LANCZOS)
    py = {"bottom": Y - h, "top": Y, "cy": Y - h / 2}[edge]
    layer = Image.new("RGBA", canvas)
    layer.alpha_composite(art, (round(X - w / 2 + pad), round(py + pad)))
    return layer


def ellipses(canvas, ells, W, H, pad):
    m = Image.new("L", canvas)
    d = ImageDraw.Draw(m)
    for x, y, rx, ry in ells:
        cx, cy = x * W + pad, y * H + pad
        d.ellipse([cx - rx * W, cy - ry * H, cx + rx * W, cy + ry * H], fill=255)
    return m.filter(ImageFilter.GaussianBlur(1.2))


def build(mid, RW, RH):
    M = MASCOTS[mid]
    ref = MASCOTS[REF]
    base, W, H, pad, canvas = load_pose(M)
    pose = np.asarray(base.crop((pad, pad, pad + W, pad + H)))
    ink = M["ink"]
    body_a = base.getchannel("A")
    # the ghost wisps float in front of everything: split them off the body (all but the largest blob)
    from import_item import regions
    torso = max(regions(np.asarray(body_a) > 128), key=lambda r: r.sum())
    torso_img = Image.fromarray(torso.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(5))
    torso_a = ImageChops.multiply(body_a, torso_img)
    wisps = base.copy()
    wisps.putalpha(ImageChops.multiply(body_a, ImageChops.subtract(body_a, torso_img)))
    chin_px = [(x * W + pad, y * H + pad) for x, y in M["chin"]]
    head_mask = Image.new("L", canvas)              # everything above the jaw line
    ImageDraw.Draw(head_mask).polygon([(0, 0), (canvas[0], 0), (canvas[0], chin_px[-1][1])] + chin_px[::-1] + [(0, chin_px[0][1])], fill=255)
    head_mask = head_mask.filter(ImageFilter.GaussianBlur(1.2))
    sx, sy, srx, sry = M["skull"]
    head_ell = Image.new("L", canvas)
    ImageDraw.Draw(head_ell).ellipse([(sx - srx) * W + pad, (sy - sry) * H + pad, (sx + srx) * W + pad, (sy + sry) * H + pad], fill=255)
    frames = {s: Frame(M, s, ref, RW, RH, W, H) for s in ("head", "neck", "back")}
    grip = M["grip"]
    gx_px, gy_px = grip[0] * W + pad, grip[1] * H + pad
    paws = ellipses(canvas, M.get("grip_mask", []), W, H, pad)

    def hold(layer):                                # the paw closes over what it holds
        if M["grip_kind"] == "paw":
            layer.alpha_composite(fp.paw(canvas, gx_px, gy_px, W))
        else:
            layer.alpha_composite(fp.cut(base, ImageChops.multiply(paws, torso_img)))
        return layer

    layers = {"body": base, "wisps": wisps}
    items = []
    catalog = [c for c in CATALOG if c[1] not in HIDDEN] + [(f, i, n, s, dict(own=f)) for f, i, n, s in M.get("own", [])]
    for files, iid, name, slot, p in catalog:
        thumb = None
        if p.get("own"):                            # the companion's own item, cut from its original pose
            own = Image.open(GEN / mid / f"{files}.png").convert("RGBA")
            layer = Image.new("RGBA", canvas)
            layer.alpha_composite(own, (pad, pad))
            if slot == "hand":
                hold(layer)
            thumb = own.crop(own.getbbox())
        elif p.get("pair") == "paws":
            l, r = load("18"), load("19")
            layer = worn_gloves(pose, l, M, W, H, pad, canvas)
            thumb = Image.new("RGBA", (l.width + r.width + 20, max(l.height, r.height)))
            thumb.alpha_composite(l, (0, 0)); thumb.alpha_composite(r, (l.width + 20, 0))
        elif p.get("pair") == "feet":
            boot = boot_worn(load("14-boot"), ink)    # the front boot is the only complete one
            fitted = FITTED / mid / f"{iid}.png"     # one boot (the right foot) drawn for this companion
            layer = Image.new("RGBA", canvas)
            top, seed_y = M["foot_rows"]
            for n, fx in enumerate(M["feet"]):        # the boot takes the foot's own shape
                foot = fill_region(pose, [(fx, seed_y)], top, 1.0, [(fx - .13, fx + .13)])
                if fitted.exists():
                    fb = Image.open(fitted).convert("RGBA")
                    fb = fb.crop(fb.getbbox())
                    if n == 0:
                        fb = fb.transpose(Image.FLIP_LEFT_RIGHT)
                    ys_, xs_ = np.nonzero(foot)
                    w = (xs_.max() - xs_.min()) * 1.08
                    fb = fb.resize((round(w), round(fb.height * w / fb.width)), Image.LANCZOS)
                    layer.alpha_composite(fb, (round(pad + (xs_.min() + xs_.max()) / 2 - w / 2), round(pad + ys_.max() + .006 * H - fb.height)))
                else:
                    layer.alpha_composite(front_boot(foot, boot, W, H, pad, canvas, ink))
            thumb = load(files)
        else:
            art = load(files)
            thumb = art
            if p.get("worn") == "top":                # a top over the torso (and the arms, if its art has sleeves)
                cx, cy = zip(*M["chin"])
                chin = lambda x: (np.interp(x / W, cx, cy) + .012) * H
                fur_np = np.asarray(torso_img.crop((pad, pad, pad + W, pad + H))) > 0
                body = fill_region(pose, M["torso"], chin, M["torso_bottom"], drop_white=M["drop_white"]) & fur_np
                arms = fill_region(pose, [a[0] for a in M["arms"]], M["arm_rows"][0], M["arm_rows"][1], [a[1] for a in M["arms"]])
                fitted = FITTED / mid / f"{iid}.png"     # art drawn for this companion's body, if there is one
                if fitted.exists():
                    art = Image.open(fitted).convert("RGBA")
                    art = art.crop(art.getbbox())
                fur = Image.fromarray(fur_np.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(5))
                y0 = np.interp(M["neck"][0], cx, cy) * H - .02 * H
                layer = worn_art(art, fur_np, y0, M["shoulder"] * H, (M["hip"] + .03) * H, W, H, pad, canvas, fur,
                                 M.get("shoulder_span", (0, 1)))
                erase(layer, head_mask)
                if M.get("paws_front"):              # folded arms stay in front of the top
                    hold(layer)
            elif slot == "hand":
                h = p["h"] * RH * M["hand_scale"] * M.get("fit", {}).get(iid, {}).get("scale", 1)
                art = art.resize((max(1, round(art.width * h / art.height)), max(1, round(h))), Image.LANCZOS)
                gx, gy = p["grip"]
                if p.get("mirror"):  # point long items away from the body
                    art, gx = art.transpose(Image.FLIP_LEFT_RIGHT), 1 - gx
                layer = Image.new("RGBA", canvas)
                if p.get("fly"):  # kite flies up beside the head; a string runs from the paw to it
                    kx, ky = M["fly"][0] * W + pad, M["fly"][1] * H + pad
                    k = 4
                    s = Image.new("RGBA", (canvas[0] * k, canvas[1] * k))
                    ImageDraw.Draw(s).line([gx_px * k, gy_px * k, kx * k, ky * k], fill=ink + (255,), width=3 * k)
                    layer.alpha_composite(s.resize(canvas, Image.LANCZOS))
                    layer.alpha_composite(art, (round(kx - gx * art.width), round(ky - gy * art.height)))
                else:
                    layer.alpha_composite(art, (round(gx_px - gx * art.width), round(gy_px - gy * art.height)))
                hold(layer)
            else:
                fr = frames["back" if slot in ("back", "shoulders") else slot]
                edge = "bottom" if "bottom" in p else "top" if "top" in p else "cy"
                if slot == "neck":
                    art = fp.bend(art, -0.028 * RH * fr.k)
                X, Y = fr.pt(p["x"], p[edge])
                f = M.get("fit", {}).get(iid, {})       # per companion touch-ups (fractions of its pose)
                X, Y = X + f.get("dx", 0) * W, Y + f.get("dy", 0) * H
                layer = put_px(canvas, art, X, Y, edge, p["w"] * RW * fr.k * f.get("scale", 1), pad)
                if p.get("band"):  # the scarf goes all the way round the neck, knot on top
                    layer = Image.alpha_composite(neck_band(art, M["chin"], W, H, pad, canvas, torso_a, ink, fr.k * RH / 825), layer)
                if slot == "neck":
                    erase(layer, head_mask)          # tucked under the chin
                if slot == "head" and p.get("wrap"):
                    a = np.asarray(layer.getchannel("A")) > 0
                    ys = np.nonzero(a.any(1))[0]
                    mid_y = ys[0] + (ys[-1] - ys[0]) * p["wrap"]  # ring's back half sits above this line
                    behind = Image.new("L", canvas)
                    ImageDraw.Draw(behind).rectangle([0, 0, canvas[0], mid_y], fill=255)
                    erase(layer, ImageChops.multiply(ImageChops.multiply(behind, head_ell), body_a))
        layers[iid] = layer
        layers[iid + "-sh"] = fp.shadow([layer], base, H)
        items.append({"id": iid, "name": name, "slot": slot, "slotVi": SLOT_VI[slot], "z": Z[slot],
                      "region": REGION_OF.get(iid), "about": ABOUT.get(iid, ""), "_thumb": thumb})

    box = None
    for img in layers.values():
        b = img.getchannel("A").point(lambda v: 255 if v > 6 else 0).getbbox()
        if b:
            box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3]))
    out = OUT / mid / "layers"
    out.mkdir(parents=True, exist_ok=True)
    for f in out.glob("*.webp"):
        f.unlink()
    size = (round((box[2] - box[0]) * 900 / (box[3] - box[1])), 900)
    for name, img in layers.items():
        img.crop(box).resize(size, Image.LANCZOS).save(out / f"{name}.webp", quality=88, method=6)
    thumbs = OUT / "thumbs"
    thumbs.mkdir(parents=True, exist_ok=True)
    for e in items:
        t = e.pop("_thumb")
        t.thumbnail((200, 200), Image.LANCZOS)
        t.save(thumbs / f"{e['id']}.webp", quality=90)
    print(mid, len(items), "items", size)
    return {"id": mid, "name": M["name"], "size": size, "items": items}


def main():
    RW, RH = Image.open(fp.ROOT / MASCOTS[REF]["pose"]).size
    only = sys.argv[1:]
    if not only:
        for f in (OUT / "thumbs").glob("*.webp"):
            f.unlink()
    for old in ("layers",):                         # the single-companion layout (before Wuwu and Dudu)
        for f in (OUT / old).glob("*.webp"):
            f.unlink()
        if (OUT / old).exists():
            (OUT / old).rmdir()
    done = {}
    if only and (OUT / "data.json").exists():       # rebuilding some companions: keep the others
        done = {m["id"]: m for m in json.loads((OUT / "data.json").read_text(encoding="utf-8"))["mascots"]}
    for m in MASCOTS:
        if not only or m in only:
            done[m] = build(m, RW, RH)
    mascots = [done[m] for m in MASCOTS if m in done]
    for m in mascots:
        m["items"] = [i for i in m["items"] if i["id"] not in HIDDEN]
    outfits = [
        {"name": "Nhà du hành gió", "ids": ["mu-chin-tang-gio", "binh-sam", "gay-gio"]},
        {"name": "Người canh trăng", "ids": ["vong-dom-dom", "mat-day-vong-trang", "gay-trang"]},
        {"name": "Rừng ngàn mắt", "ids": ["mu-tan-bong-bay", "ao-choang-buom-dem", "sach-buom-dem"]},
        {"name": "Hiệp sĩ đá", "ids": ["ao-choang-vay-da", "chuoi-da-bay", "ong-tre"]},
        {"name": "Bến năm dòng", "ids": ["hoa-hai-mau", "khan-nam-dong-song", "dieu-la"]},
        {"name": "Phố mái ngói", "ids": ["mu-la-bon-mua", "tui-mai-ngoi", "dua-la"]},
        {"name": "Dudu thường ngày", "ids": ["non-la-dudu", "gay-tre"]},
    ]
    outfits = [dict(o, ids=[i for i in o["ids"] if i not in HIDDEN]) for o in outfits]
    outfits = [o for o in outfits if len(o["ids"]) >= 2]
    regions = {k: dict(zip(("name", "en", "keeper", "story"), v)) for k, v in REGIONS.items()}
    for m in mascots:                              # names / lands may change without a rebuild of the layers
        by = {c[1]: c for c in CATALOG}
        for i in m["items"]:
            if i["id"] in by:
                i["name"] = by[i["id"]][2]
            i["region"], i["about"] = REGION_OF.get(i["id"]), ABOUT.get(i["id"], "")
    (OUT / "data.json").write_text(json.dumps({"mascots": mascots, "outfits": outfits, "regions": regions}, ensure_ascii=False),
                                   encoding="utf-8")


if __name__ == "__main__":
    main()
