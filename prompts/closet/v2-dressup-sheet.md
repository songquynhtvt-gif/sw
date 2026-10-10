# Tủ đồ v2 · Dress-up preview sheet (ChatGPT, paste-ready)

Nguồn món: `tudo-mythic-v2.md` §4.2–4.5. Attach: image 1 = `hires/huhu/00-idle-front.png`, image 2 = `hires/huhu/10-feeding-eating.png`.
Output là sheet xem trước. Lớp PNG trong suốt do pipeline (`split_sheet.py`, `fit_preview.py`, `export_closet_web.py`) làm, không xin ChatGPT.
Nếu ô quá nhỏ, mất "điều lạ": tách 2 lần, cells 1–22 rồi cells 23–28.

```
Create a DRESS-UP PREVIEW SHEET for Hǔhǔ, matching image 1 (base) and image 2 (held-item paws).

BASE: Hǔhǔ exactly as in image 1, standing, front-facing: chubby cream tiger cub, sage stripes, orange eyes, dark purple mustache smile with 2 white fangs, short banded tail on the right, 2–3 mint ghost wisps with 2 white oval eyes (no mouth) floating near the head. Same size and position in every cell. Keep every body part; only add the item.

SLOTS (one item per slot; slots combine). Each item has exactly ONE impossible detail; keep it visible:
1 HEAD
- Mũ Chín Tầng Gió: soft round cap of 9 thin stacked fabric layers getting smaller to the top, lavender and peach; 3 pale sky-blue wind ribbons stream UPWARD from the top, frozen mid-air. Sits snug between the ears.
- Mũ Trăng Khuyết: small cap shaped like a fat crescent moon lying on its back, silver with a cream inner curve; its two tips drip tiny flat gold drops that hang in the air. Tilted slightly, between the ears.
- Mũ Tán Bóng Bay: tiny tree canopy of 3 round puffy leaf balls in violet, indigo and lime, like balloons; it floats a finger-width ABOVE the head with a small flat oval shadow on the fur.
- Mũ Măng Bảy Đốt: tall jade bamboo-shoot hat with 7 separated nodes, each with a thin flat gold ring; the tip curls into one new green leaf. Ears poke out at the base.
- Hoa Hai Màu: one flower tucked behind his right ear, each petal split half coral, half turquoise, perfectly mirrored, on a short leaf stem.
- Vòng Đom Đóm: thin headband of twisted leaf-green vine across the forehead; 5 small fireflies orbit above it on a dotted path, indigo bodies, flat warm-gold tail dots.
2 NECK
- Khăn Năm Dòng Sông: neck scarf of 5 thin turquoise and cyan ribbons braided, wrapped once; the 5 loose ends ripple sideways like little rivers, one ending in a tiny coral fish shape.
- Mặt Dây Vòng Trăng: round silver pendant on a dark cord, on the chest; inside a still teal pool with 3 silver ripple rings spreading from a tiny gold moon reflection.
- Khăn Lá Biết Bay: short sage-green scarf knotted at the front; 3 leaves peel off its edge and fly away to the side like small butterflies.
- Nơ Cánh Bướm Đêm: bow tie centred under the chin, its loops are night-moth wings, indigo with cream dots and one tiny flat gold moon on each wing, mirrored.
- Chuỗi Đá Bay: cord necklace with 5 small flat terracotta stones that float with clear gaps, never touching, each with a small flat gold oval under it.
- Bình Mây Nhỏ: small round clear glass bottle with a cork hanging on the chest from a cord; a tiny cream cloud lives inside with 3 flat sky-blue rain dashes.
3 SHOULDERS
- Áo Choàng Vảy Đá: short cape over both shoulders of overlapping flat stone scales, ochre, rust and plum; one thin gold S-curve groove runs through it. Never at the waist.
4 CROSS-BODY
- Túi Mái Ngói: small satchel, strap across the chest, bag at the hip; its flap is a tiny terracotta tiled roof with one round attic window and a trail of tiny gold paw prints walking into it.
5 HELD, TWO PAWS (in front of the belly, both paws wrapping it, like image 2)
- Bánh bò: three small round honeycomb cakes, cream and pandan green; 3 tiny round cream steam puffs float up from the top cake.
- Bánh cam: exactly as in image 2, unchanged.
- Chè: layered yellow mung bean and green jelly in a small round CERAMIC bowl with a ceramic spoon (not glass, not plastic); a few tiny flat gold star-shaped jelly bits on top.
- Xôi gấc: red-orange sticky rice mound on a square of banana leaf; one small leaf has just sprouted from the rice.
- Trống Sấm Con: small round drum, indigo body, cream heads, on a neck strap, paws on the drum; a tiny flat cream cloud sits on top with one butter-yellow zigzag spark. No tassels, no red cords.
6 HELD, ONE PAW (beside the body)
- Diều Gió Chạy: leaf-shaped kite in lime and butter; he holds the string in one paw, the kite flies up-right; its tail is 3 long pale wind ribbons curling like moving air.
- Giỏ Hạt Mầm Nhảy: small round woven basket held by the handle; 3 seeds jump out mid-air, each sprouting a tiny two-leaf sprout.

RULES: nothing covers the eyes, nose or mouth; straps stay under the chin or beside the face. An item looks identical alone and in a combo. No national or folk costume of any country, no tassels, cloud swirls, lanterns, jade, locks, coins, gems, crowns, no eyes or faces on objects, no text. Magic light is flat warm gold #FFD27A shapes, never a blurry glow.

STYLE: flat 2D vector, thin sage outline #587E5C (outer contour slightly thicker), flat fills, no soft shading, no gradients, no glow, no sparkles. Plain cream #FBF4E4 background, soft flat oval ground shadow.

SHEET: 6 columns x 5 rows, no labels.
Cell 1 base · cells 2–22 each item alone in the order above · cells 23–28 combos:
Nhà du hành mây (Mũ Chín Tầng Gió + Bình Mây Nhỏ + Diều Gió Chạy) · Người canh trăng (Mũ Trăng Khuyết + Mặt Dây Vòng Trăng + Nơ Cánh Bướm Đêm) · Rừng thức dậy (Mũ Tán Bóng Bay + Khăn Lá Biết Bay + Giỏ Hạt Mầm Nhảy) · Thợ săn đom đóm (Vòng Đom Đóm + Chuỗi Đá Bay + Túi Mái Ngói) · Hiệp sĩ đá (Mũ Măng Bảy Đốt + Áo Choàng Vảy Đá + Trống Sấm Con) · Bến năm dòng (Hoa Hai Màu + Khăn Năm Dòng Sông)
Cells 29–30: leave empty cream.
```

## Thứ tự ô (để Claude gán tên khi cắt)
1 base · 2–7 đầu (theo thứ tự trên) · 8–13 cổ · 14 áo choàng · 15 túi · 16–20 giữ 2 tay · 21–22 giữ 1 tay · 23–28 bộ phối · 29–30 trống
