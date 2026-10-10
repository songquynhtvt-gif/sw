# Tủ đồ v2 · bộ prompt đầy đủ (ChatGPT)

Nguồn: `tudo-mythic-v2.md` (founder 10/10). 17 món mới + 4 món ăn + 6 bộ phối.
Quy trình: **Bước A** vẽ món đồ riêng (không có Hǔhǔ) → Claude tách nền làm lớp PNG. **Bước B** Hǔhǔ mặc từng món (thẻ bình chọn, màn TD-04). **Bước C** bộ phối.

Luật chung:
- Đính kèm: **ảnh 1** `hires/huhu/00-idle-front.png` · **ảnh 2** `hires/huhu/10-feeding-eating.png` · bước B/C thêm **ảnh 3 (4, 5)** = món đã duyệt ở bước A.
- Mỗi khối = 1 lần dán. **Chat mới** cho mỗi khối bước A; bước B mở chat mới mỗi 3–4 món.
- Hỏng thì tạo lại từ khối gốc, không sửa chồng quá 1–2 lần.
- Tải **PNG gốc** (nút tải về), đặt tên theo mã: `A1.png`, `B-mu-trang-khuyet.png`… rồi gửi Claude.
- QA: 🔴 trang phục dân tộc · chữ · mắt/mặt trên đồ · mây xoắn · tua rua · không thấy "điều lạ" ở 48 px. 🟠 hơn 1 điều lạ · glow mờ · Hǔhǔ mất hồn ma / lệch mặt · áo choàng ở hông · mũ bay không có bóng.

---

## Bước A · Vẽ món đồ (3 khối)

### A1 · Đầu (6) + Cổ (2)
Ô: 1. Mũ Chín Tầng Gió · 2. Mũ Trăng Khuyết · 3. Mũ Tán Bóng Bay · 4. Mũ Măng Bảy Đốt · 5. Hoa Hai Màu · 6. Vòng Đom Đóm · 7. Khăn Năm Dòng Sông · 8. Mặt Dây Vòng Trăng
```
Images 1 and 2 show Hǔhǔ, a finished cartoon character. Design NEW accessory objects for him in exactly his art style: flat 2D vector, clean dark outline (thicker outer contour, thinner inner lines), flat colour fills, at most one flat highlight shape per object, no gradients, no 3D, no glow halos, no texture noise.

OUTPUT: a 4x2 grid on plain white, 8 cells, thin gutters, one object per cell, front view, centred, same visual size, readable at 48 px. Objects only: no character, no hands, no people, no text, no labels, no numbers.

Every object is an ordinary thing touched by quiet folk-tale magic: it has exactly ONE impossible detail (described per item). Everything else stays simple. Mythic and surprising, never scary: no skulls, teeth, blood, weapons, fire.

Palette: forest #0E4A3A, sage #587E5C, cream #FBF4E4, turquoise #2EC4B6, leaf #6CC36F, violet #8A6BE0, indigo #3B3F9E, coral #F07C62, butter #F7C844, silver #C9D3DC, ochre #C9893A. Magic light = flat warm gold #FFD27A shapes, never a blurry glow.

BANNED: national or folk costume of any country (no conical hats, turbans, checked scarves, straw capes, áo dài, kimono, hanbok, sombrero), star lanterns, red paper lanterns, cloud swirls, tassels, jade, longevity locks, coins, gems, crowns, trophies, eyes or faces on objects.

Cells, left to right, top to bottom:
1. Mũ Chín Tầng Gió — a soft round cap built of 9 thin stacked fabric layers getting smaller to the top, lavender and peach; impossible detail: 3 pale sky-blue wind ribbons stream UPWARD from the top layer, frozen mid-air.
2. Mũ Trăng Khuyết — a small cap shaped like a fat crescent moon lying on its back, silver with a cream inner curve; impossible detail: the crescent's tips drip two tiny flat gold water drops that hang in the air without falling.
3. Mũ Tán Bóng Bay — a tiny tree canopy made of 3 round puffy leaf balls in violet, indigo and lime, like balloons; impossible detail: it floats a clear finger-width ABOVE where a head would be, with a small flat oval shadow under it.
4. Mũ Măng Bảy Đốt — a tall jade bamboo-shoot hat with 7 clearly separated nodes; impossible detail: each node has a thin flat gold ring, and the tip curls into a single new green leaf.
5. Hoa Hai Màu — one flower to tuck behind an ear, each petal split cleanly half coral, half turquoise, on a short leaf stem; impossible detail: the two halves are perfectly mirrored, like the flower is its own reflection.
6. Vòng Đom Đóm — a thin round headband of twisted leaf-green vine; impossible detail: 5 small fireflies orbit above it on a dotted flight path, bodies indigo, tails flat warm-gold dots.
7. Khăn Năm Dòng Sông — a soft neck scarf made of 5 thin turquoise and cyan ribbons braided together; impossible detail: the 5 loose ends fan out and ripple like five little rivers, one ending in a tiny coral fish shape.
8. Mặt Dây Vòng Trăng — a simple round silver pendant on a dark cord; inside it a still teal pool; impossible detail: 3 concentric silver ripple rings spread across the pool from a tiny gold moon reflection.
```

### A2 · Cổ / vai / túi (6) + Tay (2)
Ô: 1. Khăn Lá Biết Bay · 2. Nơ Cánh Bướm Đêm · 3. Áo Choàng Vảy Đá · 4. Bình Mây Nhỏ · 5. Túi Mái Ngói · 6. Chuỗi Đá Bay · 7. Diều Gió Chạy · 8. Giỏ Hạt Mầm Nhảy
```
Images 1 and 2 show Hǔhǔ, a finished cartoon character. Design NEW accessory objects for him in exactly his art style: flat 2D vector, clean dark outline (thicker outer contour, thinner inner lines), flat colour fills, at most one flat highlight shape per object, no gradients, no 3D, no glow halos, no texture noise.

OUTPUT: a 4x2 grid on plain white, 8 cells, thin gutters, one object per cell, front view, centred, same visual size, readable at 48 px. Objects only: no character, no hands, no people, no text, no labels, no numbers.

Every object is an ordinary thing touched by quiet folk-tale magic: it has exactly ONE impossible detail (described per item). Everything else stays simple. Mythic and surprising, never scary: no skulls, teeth, blood, weapons, fire.

Palette: forest #0E4A3A, sage #587E5C, cream #FBF4E4, turquoise #2EC4B6, leaf #6CC36F, violet #8A6BE0, indigo #3B3F9E, coral #F07C62, butter #F7C844, silver #C9D3DC, ochre #C9893A. Magic light = flat warm gold #FFD27A shapes, never a blurry glow.

BANNED: national or folk costume of any country (no conical hats, turbans, checked scarves, straw capes, áo dài, kimono, hanbok, sombrero), star lanterns, red paper lanterns, cloud swirls, tassels, jade, longevity locks, coins, gems, crowns, trophies, eyes or faces on objects.

Cells, left to right, top to bottom:
1. Khăn Lá Biết Bay — a short sage-green scarf tied in one knot; impossible detail: 3 leaves are peeling off its edge and flying away like small butterflies.
2. Nơ Cánh Bướm Đêm — a bow tie whose two loops are a night-moth's wings, indigo with cream dots; impossible detail: one tiny flat gold moon pattern hidden on each wing, mirrored.
3. Áo Choàng Vảy Đá — a short shoulder cape made of overlapping flat stone scales, ochre, rust and plum; impossible detail: one thin gold groove runs through the scales in an S-curve like a glowing path. Must sit on the shoulders, NOT around the waist.
4. Bình Mây Nhỏ — a small round clear glass bottle with a cork, hanging on a cord; impossible detail: a tiny fluffy cream cloud lives inside, with 3 flat sky-blue rain dashes falling from it.
5. Túi Mái Ngói — a small cross-body satchel whose flap is a tiny terracotta tiled roof with one round attic window; impossible detail: a trail of tiny warm-gold paw prints walks across the roof tiles into the window.
6. Chuỗi Đá Bay — a cord necklace with 5 small flat terracotta stones; impossible detail: the stones float with clear gaps on the cord, never touching, each with a small flat gold oval under it.
7. Diều Gió Chạy — a leaf-shaped kite in lime and butter on a thin string; impossible detail: its tail is 3 long pale wind ribbons instead of bows, curling like moving air. No cloud swirls anywhere.
8. Giỏ Hạt Mầm Nhảy — a small round woven basket with a handle; impossible detail: 3 seeds are jumping out of it mid-air, each sprouting a tiny two-leaf sprout as it jumps.
```

### A3 · Trống + món ăn (5, để trống ô 6)
Ô: 1. Trống Sấm Con · 2. Bánh bò · 3. Chè · 4. Xôi gấc · 5. Bánh cam
```
Images 1 and 2 show Hǔhǔ, a finished cartoon character. Design NEW accessory objects for him in exactly his art style: flat 2D vector, clean dark outline (thicker outer contour, thinner inner lines), flat colour fills, at most one flat highlight shape per object, no gradients, no 3D, no glow halos, no texture noise.

OUTPUT: a 3x2 grid on plain white, 6 (leave cell 6 empty white) cells, thin gutters, one object per cell, front view, centred, same visual size, readable at 48 px. Objects only: no character, no hands, no people, no text, no labels, no numbers.

Every object is an ordinary thing touched by quiet folk-tale magic: it has exactly ONE impossible detail (described per item). Everything else stays simple. Mythic and surprising, never scary: no skulls, teeth, blood, weapons, fire.

Palette: forest #0E4A3A, sage #587E5C, cream #FBF4E4, turquoise #2EC4B6, leaf #6CC36F, violet #8A6BE0, indigo #3B3F9E, coral #F07C62, butter #F7C844, silver #C9D3DC, ochre #C9893A. Magic light = flat warm gold #FFD27A shapes, never a blurry glow.

BANNED: national or folk costume of any country (no conical hats, turbans, checked scarves, straw capes, áo dài, kimono, hanbok, sombrero), star lanterns, red paper lanterns, cloud swirls, tassels, jade, longevity locks, coins, gems, crowns, trophies, eyes or faces on objects.

Cells, left to right, top to bottom:
1. Trống Sấm Con — a small round drum on a neck strap, indigo body, cream drum heads; impossible detail: a tiny flat cream cloud sits on top of the drum with one small butter-yellow zigzag spark. No tassels, no red cords.
2. Bánh bò — three small round honeycomb cakes, cream and pandan green; impossible detail: the top cake's honeycomb holes let out 3 tiny round cream steam puffs shaped like little clouds floating up.
3. Chè — layered sweet soup in a small round CERAMIC bowl (not a glass, not a plastic cup), yellow mung bean and green jelly layers, a ceramic spoon; impossible detail: a few tiny flat gold star-shaped jelly bits float on top.
4. Xôi gấc — a red-orange sticky rice mound on a square of banana leaf; impossible detail: one small leaf on top has just sprouted from the rice.
5. Bánh cam — copy the bánh cam from image 2 exactly, unchanged (calibration only).
```

---

## Bước B · Hǔhǔ mặc từng món (1 khối / món, kèm ảnh 1 + ảnh 3)

### B01 · Mũ Chín Tầng Gió · `mu-chin-tang-gio`
```
Image 1 = Hǔhǔ base pose. Image 3 = the approved accessory. Redraw Hǔhǔ EXACTLY as in image 1 — same pose, proportions, face, sage stripes, dark purple mustache line, white fangs, orange iris, 2–3 mint ghost wisps with 2 white oval eyes (no mouth), short banded tail — now wearing the accessory from image 3 at head.
Fit: sits snug between the ears, ribbons rise above. The accessory keeps its exact shape, colours and its one impossible detail. Nothing covers his eyes, nose or mouth. Hǔhǔ's ears stay visible (unless the hat covers them). Plain cream #FBF4E4 background, soft flat oval ground shadow, no text, no extra props, no scenery, no sparkles.
```

### B02 · Mũ Trăng Khuyết · `mu-trang-khuyet`
```
Image 1 = Hǔhǔ base pose. Image 3 = the approved accessory. Redraw Hǔhǔ EXACTLY as in image 1 — same pose, proportions, face, sage stripes, dark purple mustache line, white fangs, orange iris, 2–3 mint ghost wisps with 2 white oval eyes (no mouth), short banded tail — now wearing the accessory from image 3 at head.
Fit: tilted slightly, resting on top between the ears. The accessory keeps its exact shape, colours and its one impossible detail. Nothing covers his eyes, nose or mouth. Hǔhǔ's ears stay visible (unless the hat covers them). Plain cream #FBF4E4 background, soft flat oval ground shadow, no text, no extra props, no scenery, no sparkles.
```

### B03 · Mũ Tán Bóng Bay · `mu-tan-bong-bay`
```
Image 1 = Hǔhǔ base pose. Image 3 = the approved accessory. Redraw Hǔhǔ EXACTLY as in image 1 — same pose, proportions, face, sage stripes, dark purple mustache line, white fangs, orange iris, 2–3 mint ghost wisps with 2 white oval eyes (no mouth), short banded tail — now wearing the accessory from image 3 at head.
Fit: floats a finger-width above the head, a small flat oval shadow visible on the fur. The accessory keeps its exact shape, colours and its one impossible detail. Nothing covers his eyes, nose or mouth. Hǔhǔ's ears stay visible (unless the hat covers them). Plain cream #FBF4E4 background, soft flat oval ground shadow, no text, no extra props, no scenery, no sparkles.
```

### B04 · Mũ Măng Bảy Đốt · `mu-mang-bay-dot`
```
Image 1 = Hǔhǔ base pose. Image 3 = the approved accessory. Redraw Hǔhǔ EXACTLY as in image 1 — same pose, proportions, face, sage stripes, dark purple mustache line, white fangs, orange iris, 2–3 mint ghost wisps with 2 white oval eyes (no mouth), short banded tail — now wearing the accessory from image 3 at head.
Fit: sits on top, ears poke out at the base. The accessory keeps its exact shape, colours and its one impossible detail. Nothing covers his eyes, nose or mouth. Hǔhǔ's ears stay visible (unless the hat covers them). Plain cream #FBF4E4 background, soft flat oval ground shadow, no text, no extra props, no scenery, no sparkles.
```

### B05 · Hoa Hai Màu · `hoa-hai-mau`
```
Image 1 = Hǔhǔ base pose. Image 3 = the approved accessory. Redraw Hǔhǔ EXACTLY as in image 1 — same pose, proportions, face, sage stripes, dark purple mustache line, white fangs, orange iris, 2–3 mint ghost wisps with 2 white oval eyes (no mouth), short banded tail — now wearing the accessory from image 3 at head.
Fit: tucked behind his right ear. The accessory keeps its exact shape, colours and its one impossible detail. Nothing covers his eyes, nose or mouth. Hǔhǔ's ears stay visible (unless the hat covers them). Plain cream #FBF4E4 background, soft flat oval ground shadow, no text, no extra props, no scenery, no sparkles.
```

### B06 · Vòng Đom Đóm · `vong-dom-dom`
```
Image 1 = Hǔhǔ base pose. Image 3 = the approved accessory. Redraw Hǔhǔ EXACTLY as in image 1 — same pose, proportions, face, sage stripes, dark purple mustache line, white fangs, orange iris, 2–3 mint ghost wisps with 2 white oval eyes (no mouth), short banded tail — now wearing the accessory from image 3 at head.
Fit: headband across the forehead, fireflies above. The accessory keeps its exact shape, colours and its one impossible detail. Nothing covers his eyes, nose or mouth. Hǔhǔ's ears stay visible (unless the hat covers them). Plain cream #FBF4E4 background, soft flat oval ground shadow, no text, no extra props, no scenery, no sparkles.
```

### B07 · Khăn Năm Dòng Sông · `khan-nam-dong-song`
```
Image 1 = Hǔhǔ base pose. Image 3 = the approved accessory. Redraw Hǔhǔ EXACTLY as in image 1 — same pose, proportions, face, sage stripes, dark purple mustache line, white fangs, orange iris, 2–3 mint ghost wisps with 2 white oval eyes (no mouth), short banded tail — now wearing the accessory from image 3 at neck.
Fit: wrapped once, 5 ends ripple sideways. The accessory keeps its exact shape, colours and its one impossible detail. Nothing covers his eyes, nose or mouth. Hǔhǔ's ears stay visible. Plain cream #FBF4E4 background, soft flat oval ground shadow, no text, no extra props, no scenery, no sparkles.
```

### B08 · Mặt Dây Vòng Trăng · `mat-day-vong-trang`
```
Image 1 = Hǔhǔ base pose. Image 3 = the approved accessory. Redraw Hǔhǔ EXACTLY as in image 1 — same pose, proportions, face, sage stripes, dark purple mustache line, white fangs, orange iris, 2–3 mint ghost wisps with 2 white oval eyes (no mouth), short banded tail — now wearing the accessory from image 3 at neck.
Fit: cord around the neck, pendant on the chest. The accessory keeps its exact shape, colours and its one impossible detail. Nothing covers his eyes, nose or mouth. Hǔhǔ's ears stay visible. Plain cream #FBF4E4 background, soft flat oval ground shadow, no text, no extra props, no scenery, no sparkles.
```

### B09 · Khăn Lá Biết Bay · `khan-la-biet-bay`
```
Image 1 = Hǔhǔ base pose. Image 3 = the approved accessory. Redraw Hǔhǔ EXACTLY as in image 1 — same pose, proportions, face, sage stripes, dark purple mustache line, white fangs, orange iris, 2–3 mint ghost wisps with 2 white oval eyes (no mouth), short banded tail — now wearing the accessory from image 3 at neck.
Fit: knotted at the front, leaves fly off to the side. The accessory keeps its exact shape, colours and its one impossible detail. Nothing covers his eyes, nose or mouth. Hǔhǔ's ears stay visible. Plain cream #FBF4E4 background, soft flat oval ground shadow, no text, no extra props, no scenery, no sparkles.
```

### B10 · Nơ Cánh Bướm Đêm · `no-canh-buom-dem`
```
Image 1 = Hǔhǔ base pose. Image 3 = the approved accessory. Redraw Hǔhǔ EXACTLY as in image 1 — same pose, proportions, face, sage stripes, dark purple mustache line, white fangs, orange iris, 2–3 mint ghost wisps with 2 white oval eyes (no mouth), short banded tail — now wearing the accessory from image 3 at neck.
Fit: centred under the chin. The accessory keeps its exact shape, colours and its one impossible detail. Nothing covers his eyes, nose or mouth. Hǔhǔ's ears stay visible. Plain cream #FBF4E4 background, soft flat oval ground shadow, no text, no extra props, no scenery, no sparkles.
```

### B11 · Áo Choàng Vảy Đá · `ao-choang-vay-da`
```
Image 1 = Hǔhǔ base pose. Image 3 = the approved accessory. Redraw Hǔhǔ EXACTLY as in image 1 — same pose, proportions, face, sage stripes, dark purple mustache line, white fangs, orange iris, 2–3 mint ghost wisps with 2 white oval eyes (no mouth), short banded tail — now wearing the accessory from image 3 at shoulders.
Fit: cape over both shoulders down to mid-back, NOT a skirt, NOT at the waist. The accessory keeps its exact shape, colours and its one impossible detail. Nothing covers his eyes, nose or mouth. Hǔhǔ's ears stay visible. Plain cream #FBF4E4 background, soft flat oval ground shadow, no text, no extra props, no scenery, no sparkles.
```

### B12 · Bình Mây Nhỏ · `binh-may-nho`
```
Image 1 = Hǔhǔ base pose. Image 3 = the approved accessory. Redraw Hǔhǔ EXACTLY as in image 1 — same pose, proportions, face, sage stripes, dark purple mustache line, white fangs, orange iris, 2–3 mint ghost wisps with 2 white oval eyes (no mouth), short banded tail — now wearing the accessory from image 3 at neck.
Fit: bottle hangs on the chest from a cord. The accessory keeps its exact shape, colours and its one impossible detail. Nothing covers his eyes, nose or mouth. Hǔhǔ's ears stay visible. Plain cream #FBF4E4 background, soft flat oval ground shadow, no text, no extra props, no scenery, no sparkles.
```

### B13 · Túi Mái Ngói · `tui-mai-ngoi`
```
Image 1 = Hǔhǔ base pose. Image 3 = the approved accessory. Redraw Hǔhǔ EXACTLY as in image 1 — same pose, proportions, face, sage stripes, dark purple mustache line, white fangs, orange iris, 2–3 mint ghost wisps with 2 white oval eyes (no mouth), short banded tail — now wearing the accessory from image 3 at a cross-body strap.
Fit: strap across the chest, bag at the hip. The accessory keeps its exact shape, colours and its one impossible detail. Nothing covers his eyes, nose or mouth. Hǔhǔ's ears stay visible. Plain cream #FBF4E4 background, soft flat oval ground shadow, no text, no extra props, no scenery, no sparkles.
```

### B14 · Chuỗi Đá Bay · `chuoi-da-bay`
```
Image 1 = Hǔhǔ base pose. Image 3 = the approved accessory. Redraw Hǔhǔ EXACTLY as in image 1 — same pose, proportions, face, sage stripes, dark purple mustache line, white fangs, orange iris, 2–3 mint ghost wisps with 2 white oval eyes (no mouth), short banded tail — now wearing the accessory from image 3 at neck.
Fit: necklace around the neck, stones float with gaps. The accessory keeps its exact shape, colours and its one impossible detail. Nothing covers his eyes, nose or mouth. Hǔhǔ's ears stay visible. Plain cream #FBF4E4 background, soft flat oval ground shadow, no text, no extra props, no scenery, no sparkles.
```

### B15 · Diều Gió Chạy · `dieu-gio-chay`
```
Image 1 = Hǔhǔ base pose. Image 3 = the approved accessory. Redraw Hǔhǔ EXACTLY as in image 1 — same pose, proportions, face, sage stripes, dark purple mustache line, white fangs, orange iris, 2–3 mint ghost wisps with 2 white oval eyes (no mouth), short banded tail — now wearing the accessory from image 3 at one paw (held beside his body).
Fit: holds the string in one paw, the kite flies up and to the right. The accessory keeps its exact shape, colours and its one impossible detail. Nothing covers his eyes, nose or mouth. Hǔhǔ's ears stay visible. Plain cream #FBF4E4 background, soft flat oval ground shadow, no text, no extra props, no scenery, no sparkles.
```

### B16 · Giỏ Hạt Mầm Nhảy · `gio-hat-mam-nhay`
```
Image 1 = Hǔhǔ base pose. Image 3 = the approved accessory. Redraw Hǔhǔ EXACTLY as in image 1 — same pose, proportions, face, sage stripes, dark purple mustache line, white fangs, orange iris, 2–3 mint ghost wisps with 2 white oval eyes (no mouth), short banded tail — now wearing the accessory from image 3 at one paw (held beside his body).
Fit: holds the handle beside his body, seeds jump out. The accessory keeps its exact shape, colours and its one impossible detail. Nothing covers his eyes, nose or mouth. Hǔhǔ's ears stay visible. Plain cream #FBF4E4 background, soft flat oval ground shadow, no text, no extra props, no scenery, no sparkles.
```

### B17 · Trống Sấm Con · `trong-sam-con`
```
Image 1 = Hǔhǔ base pose. Image 3 = the approved accessory. Redraw Hǔhǔ EXACTLY as in image 1 — same pose, proportions, face, sage stripes, dark purple mustache line, white fangs, orange iris, 2–3 mint ghost wisps with 2 white oval eyes (no mouth), short banded tail — now wearing the accessory from image 3 at both paws (held in front of his belly).
Fit: drum hangs at the belly on a strap, both paws on the drum. The accessory keeps its exact shape, colours and its one impossible detail. Nothing covers his eyes, nose or mouth. Hǔhǔ's ears stay visible. Plain cream #FBF4E4 background, soft flat oval ground shadow, no text, no extra props, no scenery, no sparkles.
```

### B18 · Bánh bò · `banh-bo`
```
Image 1 = Hǔhǔ base pose. Image 3 = the approved accessory. Redraw Hǔhǔ EXACTLY as in image 1 — same pose, proportions, face, sage stripes, dark purple mustache line, white fangs, orange iris, 2–3 mint ghost wisps with 2 white oval eyes (no mouth), short banded tail — now wearing the accessory from image 3 at both paws (held in front of his belly).
Fit: holds the food in front of the chest with both paws, as in image 2. The accessory keeps its exact shape, colours and its one impossible detail. Nothing covers his eyes, nose or mouth. Hǔhǔ's ears stay visible. Plain cream #FBF4E4 background, soft flat oval ground shadow, no text, no extra props, no scenery, no sparkles.
```

### B19 · Chè · `che`
```
Image 1 = Hǔhǔ base pose. Image 3 = the approved accessory. Redraw Hǔhǔ EXACTLY as in image 1 — same pose, proportions, face, sage stripes, dark purple mustache line, white fangs, orange iris, 2–3 mint ghost wisps with 2 white oval eyes (no mouth), short banded tail — now wearing the accessory from image 3 at both paws (held in front of his belly).
Fit: holds the bowl in front of the chest with both paws, as in image 2. The accessory keeps its exact shape, colours and its one impossible detail. Nothing covers his eyes, nose or mouth. Hǔhǔ's ears stay visible. Plain cream #FBF4E4 background, soft flat oval ground shadow, no text, no extra props, no scenery, no sparkles.
```

### B20 · Xôi gấc · `xoi-gac`
```
Image 1 = Hǔhǔ base pose. Image 3 = the approved accessory. Redraw Hǔhǔ EXACTLY as in image 1 — same pose, proportions, face, sage stripes, dark purple mustache line, white fangs, orange iris, 2–3 mint ghost wisps with 2 white oval eyes (no mouth), short banded tail — now wearing the accessory from image 3 at both paws (held in front of his belly).
Fit: holds it in front of the chest with both paws, as in image 2. The accessory keeps its exact shape, colours and its one impossible detail. Nothing covers his eyes, nose or mouth. Hǔhǔ's ears stay visible. Plain cream #FBF4E4 background, soft flat oval ground shadow, no text, no extra props, no scenery, no sparkles.
```

### B21 · Bánh cam · `banh-cam`
```
Image 1 = Hǔhǔ base pose. Image 3 = the approved accessory. Redraw Hǔhǔ EXACTLY as in image 1 — same pose, proportions, face, sage stripes, dark purple mustache line, white fangs, orange iris, 2–3 mint ghost wisps with 2 white oval eyes (no mouth), short banded tail — now wearing the accessory from image 3 at both paws (held in front of his belly).
Fit: holds it in front of the chest with both paws, exactly as in image 2. The accessory keeps its exact shape, colours and its one impossible detail. Nothing covers his eyes, nose or mouth. Hǔhǔ's ears stay visible. Plain cream #FBF4E4 background, soft flat oval ground shadow, no text, no extra props, no scenery, no sparkles.
```

---

## Bước C · Bộ phối (kèm ảnh 1 + ảnh các món đã duyệt)

### Nhà du hành mây
```
Image 1 = Hǔhǔ base pose. Images 3, 4, 5 = the approved accessories. Redraw Hǔhǔ EXACTLY as in image 1 — same pose, proportions, face, sage stripes, dark purple mustache line, white fangs, orange iris, 2–3 mint ghost wisps with 2 white oval eyes (no mouth), short banded tail — now wearing ALL of them together: Mũ Chín Tầng Gió (sits snug between the ears, ribbons rise above); Bình Mây Nhỏ (bottle hangs on the chest from a cord); Diều Gió Chạy (holds the string in one paw, the kite flies up and to the right).
Each accessory keeps its exact shape, colours and its one impossible detail, and looks identical to how it looks worn alone. Nothing overlaps or clips; nothing covers his eyes, nose or mouth. Plain cream #FBF4E4 background, soft flat oval ground shadow, no text, no extra props, no scenery, no sparkles.
```

### Người canh trăng
```
Image 1 = Hǔhǔ base pose. Images 3, 4, 5 = the approved accessories. Redraw Hǔhǔ EXACTLY as in image 1 — same pose, proportions, face, sage stripes, dark purple mustache line, white fangs, orange iris, 2–3 mint ghost wisps with 2 white oval eyes (no mouth), short banded tail — now wearing ALL of them together: Mũ Trăng Khuyết (tilted slightly, resting on top between the ears); Mặt Dây Vòng Trăng (cord around the neck, pendant on the chest); Nơ Cánh Bướm Đêm (centred under the chin).
Each accessory keeps its exact shape, colours and its one impossible detail, and looks identical to how it looks worn alone. Nothing overlaps or clips; nothing covers his eyes, nose or mouth. Plain cream #FBF4E4 background, soft flat oval ground shadow, no text, no extra props, no scenery, no sparkles.
```

### Rừng thức dậy
```
Image 1 = Hǔhǔ base pose. Images 3, 4, 5 = the approved accessories. Redraw Hǔhǔ EXACTLY as in image 1 — same pose, proportions, face, sage stripes, dark purple mustache line, white fangs, orange iris, 2–3 mint ghost wisps with 2 white oval eyes (no mouth), short banded tail — now wearing ALL of them together: Mũ Tán Bóng Bay (floats a finger-width above the head, a small flat oval shadow visible on the fur); Khăn Lá Biết Bay (knotted at the front, leaves fly off to the side); Giỏ Hạt Mầm Nhảy (holds the handle beside his body, seeds jump out).
Each accessory keeps its exact shape, colours and its one impossible detail, and looks identical to how it looks worn alone. Nothing overlaps or clips; nothing covers his eyes, nose or mouth. Plain cream #FBF4E4 background, soft flat oval ground shadow, no text, no extra props, no scenery, no sparkles.
```

### Thợ săn đom đóm
```
Image 1 = Hǔhǔ base pose. Images 3, 4, 5 = the approved accessories. Redraw Hǔhǔ EXACTLY as in image 1 — same pose, proportions, face, sage stripes, dark purple mustache line, white fangs, orange iris, 2–3 mint ghost wisps with 2 white oval eyes (no mouth), short banded tail — now wearing ALL of them together: Vòng Đom Đóm (headband across the forehead, fireflies above); Chuỗi Đá Bay (necklace around the neck, stones float with gaps); Túi Mái Ngói (strap across the chest, bag at the hip).
Each accessory keeps its exact shape, colours and its one impossible detail, and looks identical to how it looks worn alone. Nothing overlaps or clips; nothing covers his eyes, nose or mouth. Plain cream #FBF4E4 background, soft flat oval ground shadow, no text, no extra props, no scenery, no sparkles.
```

### Hiệp sĩ đá
```
Image 1 = Hǔhǔ base pose. Images 3, 4, 5 = the approved accessories. Redraw Hǔhǔ EXACTLY as in image 1 — same pose, proportions, face, sage stripes, dark purple mustache line, white fangs, orange iris, 2–3 mint ghost wisps with 2 white oval eyes (no mouth), short banded tail — now wearing ALL of them together: Mũ Măng Bảy Đốt (sits on top, ears poke out at the base); Áo Choàng Vảy Đá (cape over both shoulders down to mid-back, NOT a skirt, NOT at the waist); Trống Sấm Con (drum hangs at the belly on a strap, both paws on the drum).
Each accessory keeps its exact shape, colours and its one impossible detail, and looks identical to how it looks worn alone. Nothing overlaps or clips; nothing covers his eyes, nose or mouth. Plain cream #FBF4E4 background, soft flat oval ground shadow, no text, no extra props, no scenery, no sparkles.
```

### Bến năm dòng
```
Image 1 = Hǔhǔ base pose. Images 3, 4 = the approved accessories. Redraw Hǔhǔ EXACTLY as in image 1 — same pose, proportions, face, sage stripes, dark purple mustache line, white fangs, orange iris, 2–3 mint ghost wisps with 2 white oval eyes (no mouth), short banded tail — now wearing ALL of them together: Hoa Hai Màu (tucked behind his right ear); Khăn Năm Dòng Sông (wrapped once, 5 ends ripple sideways).
Each accessory keeps its exact shape, colours and its one impossible detail, and looks identical to how it looks worn alone. Nothing overlaps or clips; nothing covers his eyes, nose or mouth. Plain cream #FBF4E4 background, soft flat oval ground shadow, no text, no extra props, no scenery, no sparkles.
```

---

## Đặt tên file gửi Claude
`A1.png` `A2.png` `A3.png` · `B-<mã>.png` (vd `B-mu-trang-khuyet.png`) · `C-<tên bộ không dấu>.png`
Claude sẽ: tách nền + phóng nét bước A thành lớp món đồ; dùng ảnh B/C cho trang bình chọn và làm chuẩn vị trí đeo.
