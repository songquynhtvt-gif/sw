# Tủ đồ · toàn bộ kho cho ChatGPT (42 món, 12 sheet)

Không cần API key. Mỗi khối dưới đây = 1 ảnh có tối đa 4 món.

1. Mở ChatGPT, **chat mới mỗi 3 sheet**. Dán nguyên 1 khối, chờ ra ảnh.
2. Ảnh lỗi (thiếu món, món dính nhau, có chữ, có bóng navy) → bấm tạo lại, không sửa chồng quá 1–2 lần.
3. Tải ảnh về, đặt tên đúng mã sheet, ví dụ `w3-1.png`, bỏ hết vào `materials/chatgpt-designs/closet/` (hoặc gửi thẳng cho Claude).
4. Cắt + xoá nền + ướm lên Hǔhǔ, một lệnh cho cả thư mục:
   ```
   python3 scripts/split_sheet.py materials/chatgpt-designs/closet/
   ```
   → từng món ở `assets/closet/gen/<id>-v<n>.png`, ảnh ướm ở `assets/closet/fit/`.

File này sinh tự động từ `prompts/closet/items.json` (`python3 scripts/build_prompts.py`), đừng sửa tay.

## `stage1-1` · Stage 1 (HIFI-PREP G5, đã duyệt)

1. Nón lá (`non-la`) · 2. Khăn rằn (`khan-ran`) · 3. Nơ bướm (`no-buom`) · 4. Vòng hoa (`vong-hoa`)

```
Draw 4 DIFFERENT accessories for a cute chubby cartoon tiger cub, laid out as an invisible grid of 2 columns and 2 rows on a plain pure white background. Each item sits alone in the centre of its own cell, all items drawn at a similar size, with wide white gaps between cells; nothing touches or crosses into another cell. Draw ONLY the items, never the tiger or any part of it. Order left to right, then top to bottom:

1. a small Vietnamese conical palm-leaf hat (nón lá), pale straw with thin concentric rib lines, a coral chin ribbon tied in a small bow (worn on the head). Colours: straw #E8D9A8, coral #F07C62 ribbon, cream.
2. a Southern Vietnamese checkered scarf (khăn rằn) in small navy and cream checks, folded into a triangle and tied in a knot at the front-left, two short ends sticking out (worn around the neck and chest). Colours: navy #1B2A6B and cream checks.
3. a chunky butterfly bow tie on a thin band, two rounded loops and a small knot (worn around the neck and chest). Colours: coral #F07C62, butter #F7C844 polka dots.
4. a flower crown ring of small five-petal flowers and leaves, worn flat around the top of the head (worn on the head). Colours: butter #F7C844 and coral #F07C62 flowers, leaf #6CC36F leaves.

Every item: straight front view, exactly as it is worn or held. Head items leave gaps where two round ears poke through. Neck items have a gentle smile-shaped top edge and hang on the chest. Held items stand upright with the grip at the bottom-centre. Food and icons: one simple object.

STYLE: thin dark sage outline #587E5C (never black), outer contour slightly thicker, inner lines thinner. Flat fills only, bright and clean, at most 2-3 colours plus cream #F5F4D0 per item. Simple chunky shapes that still read at 96 px. Vietnamese materials and craft: bamboo, rattan, straw, banana and palm leaf, cotton, indigo cloth, wood, silver.

OUTPUT: square 1:1, plain pure white background, no grid lines, no labels, no numbers, no text, no border, no drop shadow, no sticker outline.

Do NOT: draw the tiger, a head, ears or any body part; add a navy or coloured offset shadow, gloss, glow, gradients, 3D, blur or noisy texture; add four-point sparkles; use Chinese motifs (swirl clouds, dragons, tasselled lanterns, star lanterns, melon caps, round jade discs, red-and-gold imperial colours); draw maps with a red X, compasses or rolled scrolls; draw crowns, medals, trophies or gems; add text, letters or numbers; use mint green #BDDBA7 as the main colour.
```

## `stage1-2` · Stage 1 (HIFI-PREP G5, đã duyệt)

1. Khăn quàng lá (`khan-quang-la`) · 2. Diều giấy (`dieu-giay`) · 3. Trống cơm (`trong-com`) · 4. Giỏ xách mây (`gio-xach-may`)

```
Draw 4 DIFFERENT accessories for a cute chubby cartoon tiger cub, laid out as an invisible grid of 2 columns and 2 rows on a plain pure white background. Each item sits alone in the centre of its own cell, all items drawn at a similar size, with wide white gaps between cells; nothing touches or crosses into another cell. Draw ONLY the items, never the tiger or any part of it. Order left to right, then top to bottom:

1. a scarf made of overlapping big green leaves with visible centre veins, wrapped once around the neck, two leaf tips hanging at the front (worn around the neck and chest). Colours: leaf #6CC36F and dark leaf #3E8E4F, cream veins.
2. a small diamond-shaped Vietnamese paper kite on a bamboo cross frame, held up on a short bamboo stick, with a short ribbon tail of three bows (held in one paw). Colours: butter #F7C844 and coral #F07C62 panels, bamboo frame.
3. a small Vietnamese barrel drum (trống cơm) lying sideways on the chest, hung from a woven strap around the neck, laced with criss-cross cords (worn around the neck and chest). Colours: warm wood #C98A4B body, cream drum heads, coral #F07C62 cords.
4. a small woven rattan handbag basket with a round arched handle and a wooden toggle on the lid, held by the handle (held in one paw). Colours: rattan #D9B577, wood #8B5A2B toggle.

Every item: straight front view, exactly as it is worn or held. Head items leave gaps where two round ears poke through. Neck items have a gentle smile-shaped top edge and hang on the chest. Held items stand upright with the grip at the bottom-centre. Food and icons: one simple object.

STYLE: thin dark sage outline #587E5C (never black), outer contour slightly thicker, inner lines thinner. Flat fills only, bright and clean, at most 2-3 colours plus cream #F5F4D0 per item. Simple chunky shapes that still read at 96 px. Vietnamese materials and craft: bamboo, rattan, straw, banana and palm leaf, cotton, indigo cloth, wood, silver.

OUTPUT: square 1:1, plain pure white background, no grid lines, no labels, no numbers, no text, no border, no drop shadow, no sticker outline.

Do NOT: draw the tiger, a head, ears or any body part; add a navy or coloured offset shadow, gloss, glow, gradients, 3D, blur or noisy texture; add four-point sparkles; use Chinese motifs (swirl clouds, dragons, tasselled lanterns, star lanterns, melon caps, round jade discs, red-and-gold imperial colours); draw maps with a red X, compasses or rolled scrolls; draw crowns, medals, trophies or gems; add text, letters or numbers; use mint green #BDDBA7 as the main colour.
```

## `stage1-3` · Stage 1 (HIFI-PREP G5, đã duyệt)

1. Bánh cam (`banh-cam`) · 2. Xôi gấc (`xoi-gac`) · 3. Chè (`che`) · 4. Bánh bò (`banh-bo`)

```
Draw 4 DIFFERENT accessories for a cute chubby cartoon tiger cub, laid out as an invisible grid of 2 columns and 2 rows on a plain pure white background. Each item sits alone in the centre of its own cell, all items drawn at a similar size, with wide white gaps between cells; nothing touches or crosses into another cell. Draw ONLY the items, never the tiger or any part of it. Order left to right, then top to bottom:

1. one bánh cam: a round golden fried sesame ball with tiny cream sesame dots, must read as a Vietnamese sesame ball, not a coin or a cookie (a treat the tiger eats). Colours: golden #D9953B, cream sesame dots.
2. a small mound of red-orange gấc sticky rice on a piece of banana leaf, rounded dome shape with a few visible rice grain bumps (a treat the tiger eats). Colours: gấc red-orange #E0573A, leaf #6CC36F.
3. a small clear glass of Vietnamese layered chè dessert: green, yellow mung bean and white coconut layers, a little spoon (a treat the tiger eats). Colours: leaf green, butter yellow, cream layers.
4. one small round puffy Vietnamese steamed rice cake (bánh bò), soft dome with a honeycomb top, pandan green (a treat the tiger eats). Colours: pandan green #8BC97A, cream.

Every item: straight front view, exactly as it is worn or held. Head items leave gaps where two round ears poke through. Neck items have a gentle smile-shaped top edge and hang on the chest. Held items stand upright with the grip at the bottom-centre. Food and icons: one simple object.

STYLE: thin dark sage outline #587E5C (never black), outer contour slightly thicker, inner lines thinner. Flat fills only, bright and clean, at most 2-3 colours plus cream #F5F4D0 per item. Simple chunky shapes that still read at 96 px. Vietnamese materials and craft: bamboo, rattan, straw, banana and palm leaf, cotton, indigo cloth, wood, silver.

OUTPUT: square 1:1, plain pure white background, no grid lines, no labels, no numbers, no text, no border, no drop shadow, no sticker outline.

Do NOT: draw the tiger, a head, ears or any body part; add a navy or coloured offset shadow, gloss, glow, gradients, 3D, blur or noisy texture; add four-point sparkles; use Chinese motifs (swirl clouds, dragons, tasselled lanterns, star lanterns, melon caps, round jade discs, red-and-gold imperial colours); draw maps with a red X, compasses or rolled scrolls; draw crowns, medals, trophies or gems; add text, letters or numbers; use mint green #BDDBA7 as the main colour.
```

## `stage1-4` · Stage 1 (HIFI-PREP G5, đã duyệt)

1. Ngày Ngủ (`ngay-ngu`) · 2. Hồi Sinh Chuỗi (`hoi-sinh-chuoi`)

```
Draw 2 DIFFERENT accessories for a cute chubby cartoon tiger cub, laid out as an invisible grid of 2 columns and 1 rows on a plain pure white background. Each item sits alone in the centre of its own cell, all items drawn at a similar size, with wide white gaps between cells; nothing touches or crosses into another cell. Draw ONLY the items, never the tiger or any part of it. Order left to right, then top to bottom:

1. a small soft sleeping cap with a round pom-pom resting on a little rattan pillow (a small reward icon). Colours: violet #8A6BE0, cream pom-pom, rattan pillow.
2. a young bamboo shoot sprouting two fresh leaves out of a small round clay pot (a small reward icon). Colours: leaf #6CC36F, warm clay #C98A4B.

Every item: straight front view, exactly as it is worn or held. Head items leave gaps where two round ears poke through. Neck items have a gentle smile-shaped top edge and hang on the chest. Held items stand upright with the grip at the bottom-centre. Food and icons: one simple object.

STYLE: thin dark sage outline #587E5C (never black), outer contour slightly thicker, inner lines thinner. Flat fills only, bright and clean, at most 2-3 colours plus cream #F5F4D0 per item. Simple chunky shapes that still read at 96 px. Vietnamese materials and craft: bamboo, rattan, straw, banana and palm leaf, cotton, indigo cloth, wood, silver.

OUTPUT: square 1:1, plain pure white background, no grid lines, no labels, no numbers, no text, no border, no drop shadow, no sticker outline.

Do NOT: draw the tiger, a head, ears or any body part; add a navy or coloured offset shadow, gloss, glow, gradients, 3D, blur or noisy texture; add four-point sparkles; use Chinese motifs (swirl clouds, dragons, tasselled lanterns, star lanterns, melon caps, round jade discs, red-and-gold imperial colours); draw maps with a red X, compasses or rolled scrolls; draw crowns, medals, trophies or gems; add text, letters or numbers; use mint green #BDDBA7 as the main colour.
```

## `w3-1` · Tuần 3 · Rừng lá

1. Mũ lá (`mu-la`) · 2. Vòng hạt rừng (`vong-hat-rung`) · 3. Áo tơi lá (`ao-toi-la`) · 4. Mũ chóp lá (`mu-chop-la`)

```
Draw 4 DIFFERENT accessories for a cute chubby cartoon tiger cub, laid out as an invisible grid of 2 columns and 2 rows on a plain pure white background. Each item sits alone in the centre of its own cell, all items drawn at a similar size, with wide white gaps between cells; nothing touches or crosses into another cell. Draw ONLY the items, never the tiger or any part of it. Order left to right, then top to bottom:

1. a soft cap made of overlapping green leaves with visible veins, two small leaves sprouting on top (worn on the head). Colours: leaf #6CC36F, dark leaf #3E8E4F, cream veins.
2. a necklace of round wooden and green seed beads on a twisted brown cord, a round wooden medallion carved with a two-leaf sprout, one small leaf beside it (worn around the neck and chest). Colours: wood #C98A4B, leaf #6CC36F beads, cream beads.
3. a short shoulder cape like a Vietnamese palm-leaf raincoat (áo tơi): layered rows of long dry palm leaves tied at the neck with a cord (worn around the neck and chest). Colours: dry leaf #C9B26A, darker leaf lines #8F7A3A.
4. a soft pointed hat made of folded green leaves, the tip bending over, a band of tied bamboo strip around the base, a tiny leaf twig tucked in (worn on the head). Colours: leaf #6CC36F, bamboo #E8D9A8 band.

Every item: straight front view, exactly as it is worn or held. Head items leave gaps where two round ears poke through. Neck items have a gentle smile-shaped top edge and hang on the chest. Held items stand upright with the grip at the bottom-centre. Food and icons: one simple object.

STYLE: thin dark sage outline #587E5C (never black), outer contour slightly thicker, inner lines thinner. Flat fills only, bright and clean, at most 2-3 colours plus cream #F5F4D0 per item. Simple chunky shapes that still read at 96 px. Vietnamese materials and craft: bamboo, rattan, straw, banana and palm leaf, cotton, indigo cloth, wood, silver.

OUTPUT: square 1:1, plain pure white background, no grid lines, no labels, no numbers, no text, no border, no drop shadow, no sticker outline.

Do NOT: draw the tiger, a head, ears or any body part; add a navy or coloured offset shadow, gloss, glow, gradients, 3D, blur or noisy texture; add four-point sparkles; use Chinese motifs (swirl clouds, dragons, tasselled lanterns, star lanterns, melon caps, round jade discs, red-and-gold imperial colours); draw maps with a red X, compasses or rolled scrolls; draw crowns, medals, trophies or gems; add text, letters or numbers; use mint green #BDDBA7 as the main colour.
```

## `w5-1` · Tuần 5 · Thám hiểm

1. Mũ cối kính bay (`mu-coi-kinh`) · 2. Ống nhòm tre (`ong-nhom-tre`) · 3. Túi cói (`tui-coi`) · 4. Ống tre đựng nước (`ong-tre-nuoc`)

```
Draw 4 DIFFERENT accessories for a cute chubby cartoon tiger cub, laid out as an invisible grid of 2 columns and 2 rows on a plain pure white background. Each item sits alone in the centre of its own cell, all items drawn at a similar size, with wide white gaps between cells; nothing touches or crosses into another cell. Draw ONLY the items, never the tiger or any part of it. Order left to right, then top to bottom:

1. a small Vietnamese pith helmet (mũ cối) with a brown band and a pair of round aviator goggles resting on the front (worn on the head). Colours: khaki cream #E8D9A8, brown #8B5A2B band, turquoise #2EC4B6 lenses.
2. a short spyglass made of a bamboo tube with two rattan bands and a round lens, held upright (held in one paw). Colours: bamboo #D9C27A, rattan bands, turquoise lens.
3. a small woven sedge (cói) satchel on a long strap worn across the chest, the bag sits at the front-right with a leaf-shaped button (worn around the neck and chest). Colours: sedge #D9B577, leaf #6CC36F button.
4. a bamboo-tube water flask with a wooden stopper hanging at the chest from a cord around the neck (worn around the neck and chest). Colours: bamboo green #8BC97A, wood stopper.

Every item: straight front view, exactly as it is worn or held. Head items leave gaps where two round ears poke through. Neck items have a gentle smile-shaped top edge and hang on the chest. Held items stand upright with the grip at the bottom-centre. Food and icons: one simple object.

STYLE: thin dark sage outline #587E5C (never black), outer contour slightly thicker, inner lines thinner. Flat fills only, bright and clean, at most 2-3 colours plus cream #F5F4D0 per item. Simple chunky shapes that still read at 96 px. Vietnamese materials and craft: bamboo, rattan, straw, banana and palm leaf, cotton, indigo cloth, wood, silver.

OUTPUT: square 1:1, plain pure white background, no grid lines, no labels, no numbers, no text, no border, no drop shadow, no sticker outline.

Do NOT: draw the tiger, a head, ears or any body part; add a navy or coloured offset shadow, gloss, glow, gradients, 3D, blur or noisy texture; add four-point sparkles; use Chinese motifs (swirl clouds, dragons, tasselled lanterns, star lanterns, melon caps, round jade discs, red-and-gold imperial colours); draw maps with a red X, compasses or rolled scrolls; draw crowns, medals, trophies or gems; add text, letters or numbers; use mint green #BDDBA7 as the main colour.
```

## `w7-1` · Tuần 7 · Sông nước

1. Mũ thuyền giấy (`mu-thuyen-giay`) · 2. Vòng hoa súng (`vong-hoa-sung`) · 3. Nơ lá dừa (`no-la-dua`) · 4. Cần câu tre (`can-cau-tre`)

```
Draw 4 DIFFERENT accessories for a cute chubby cartoon tiger cub, laid out as an invisible grid of 2 columns and 2 rows on a plain pure white background. Each item sits alone in the centre of its own cell, all items drawn at a similar size, with wide white gaps between cells; nothing touches or crosses into another cell. Draw ONLY the items, never the tiger or any part of it. Order left to right, then top to bottom:

1. a folded newspaper-style paper boat hat, plain cream paper with crisp fold lines and one turquoise folded edge (worn on the head). Colours: cream paper, turquoise #2EC4B6 edge.
2. a crown ring of three water lily flowers (hoa súng) on round lily pads (worn on the head). Colours: violet #8A6BE0 flowers, turquoise #2EC4B6 pads, butter centres.
3. a bow woven from strips of coconut leaf, like a Mekong child's coconut-leaf toy, on a thin green band (worn around the neck and chest). Colours: coconut leaf green #6CC36F, pale leaf #CFE39A.
4. a short bamboo fishing rod held upright, a thin line hanging from the tip with a small red-and-cream float (held in one paw). Colours: bamboo #D9C27A, coral #F07C62 float.

Every item: straight front view, exactly as it is worn or held. Head items leave gaps where two round ears poke through. Neck items have a gentle smile-shaped top edge and hang on the chest. Held items stand upright with the grip at the bottom-centre. Food and icons: one simple object.

STYLE: thin dark sage outline #587E5C (never black), outer contour slightly thicker, inner lines thinner. Flat fills only, bright and clean, at most 2-3 colours plus cream #F5F4D0 per item. Simple chunky shapes that still read at 96 px. Vietnamese materials and craft: bamboo, rattan, straw, banana and palm leaf, cotton, indigo cloth, wood, silver.

OUTPUT: square 1:1, plain pure white background, no grid lines, no labels, no numbers, no text, no border, no drop shadow, no sticker outline.

Do NOT: draw the tiger, a head, ears or any body part; add a navy or coloured offset shadow, gloss, glow, gradients, 3D, blur or noisy texture; add four-point sparkles; use Chinese motifs (swirl clouds, dragons, tasselled lanterns, star lanterns, melon caps, round jade discs, red-and-gold imperial colours); draw maps with a red X, compasses or rolled scrolls; draw crowns, medals, trophies or gems; add text, letters or numbers; use mint green #BDDBA7 as the main colour.
```

## `w9-1` · Tuần 9 · Đồng quê

1. Mũ trùm sừng trâu (`mu-trum-trau`) · 2. Mõ trâu (`mo-trau`) · 3. Mũ rơm (`mu-rom`) · 4. Sáo trúc (`sao-truc`)

```
Draw 4 DIFFERENT accessories for a cute chubby cartoon tiger cub, laid out as an invisible grid of 2 columns and 2 rows on a plain pure white background. Each item sits alone in the centre of its own cell, all items drawn at a similar size, with wide white gaps between cells; nothing touches or crosses into another cell. Draw ONLY the items, never the tiger or any part of it. Order left to right, then top to bottom:

1. a cosy cream hood with two short curved brown buffalo horns, two small green leaves at the sides and two round pom-pom ties (worn on the head). Colours: cream, brown #8B5A2B horns, leaf #6CC36F.
2. a wooden buffalo bell (mõ trâu): a small carved wooden block bell with a clapper, hung from a rope around the neck (worn around the neck and chest). Colours: wood #C98A4B, rope #8B5A2B.
3. a round woven straw hat with a wide brim and a leaf-green band, one small yellow rice-flower tucked in the band (worn on the head). Colours: straw #E8C46A, leaf #6CC36F band.
4. a short bamboo flute (sáo trúc) with round finger holes and a small coral cord tied near the end, held upright (held in one paw). Colours: bamboo #D9C27A, coral cord.

Every item: straight front view, exactly as it is worn or held. Head items leave gaps where two round ears poke through. Neck items have a gentle smile-shaped top edge and hang on the chest. Held items stand upright with the grip at the bottom-centre. Food and icons: one simple object.

STYLE: thin dark sage outline #587E5C (never black), outer contour slightly thicker, inner lines thinner. Flat fills only, bright and clean, at most 2-3 colours plus cream #F5F4D0 per item. Simple chunky shapes that still read at 96 px. Vietnamese materials and craft: bamboo, rattan, straw, banana and palm leaf, cotton, indigo cloth, wood, silver.

OUTPUT: square 1:1, plain pure white background, no grid lines, no labels, no numbers, no text, no border, no drop shadow, no sticker outline.

Do NOT: draw the tiger, a head, ears or any body part; add a navy or coloured offset shadow, gloss, glow, gradients, 3D, blur or noisy texture; add four-point sparkles; use Chinese motifs (swirl clouds, dragons, tasselled lanterns, star lanterns, melon caps, round jade discs, red-and-gold imperial colours); draw maps with a red X, compasses or rolled scrolls; draw crowns, medals, trophies or gems; add text, letters or numbers; use mint green #BDDBA7 as the main colour.
```

## `w11-1` · Tuần 11 · Đêm đom đóm

1. Băng đô trăng khuyết (`bang-do-trang`) · 2. Hũ đom đóm (`hu-dom-dom`) · 3. Áo choàng chàm (`ao-choang-cham`) · 4. Băng đô chuồn chuồn (`bang-do-chuon-chuon`)

```
Draw 4 DIFFERENT accessories for a cute chubby cartoon tiger cub, laid out as an invisible grid of 2 columns and 2 rows on a plain pure white background. Each item sits alone in the centre of its own cell, all items drawn at a similar size, with wide white gaps between cells; nothing touches or crosses into another cell. Draw ONLY the items, never the tiger or any part of it. Order left to right, then top to bottom:

1. a headband with a butter-yellow crescent moon in the centre, flanked by cream petals and green leaves, one small round bead hanging below (worn on the head). Colours: butter #F7C844 moon, cream petals, leaf #6CC36F.
2. a small glass jar with a cloth lid tied with string, three tiny fireflies inside drawn as small butter-yellow dots with ONE flat lighter shape around them, no blur (held in one paw). Colours: clear glass with turquoise tint, butter #F7C844 fireflies.
3. a short indigo shoulder cape with a cream scalloped hem, scattered small round butter dots like stars (round dots only), fastened with a wooden toggle (worn around the neck and chest). Colours: indigo #3B4BA8, cream hem, butter dots.
4. a thin headband with a small dragonfly perched on top in the centre, two pairs of long rounded wings spread wide with a simple vein pattern (worn on the head). Colours: pale turquoise #A8E6DF wings, violet #8A6BE0 body and veins, leaf band.

Every item: straight front view, exactly as it is worn or held. Head items leave gaps where two round ears poke through. Neck items have a gentle smile-shaped top edge and hang on the chest. Held items stand upright with the grip at the bottom-centre. Food and icons: one simple object.

STYLE: thin dark sage outline #587E5C (never black), outer contour slightly thicker, inner lines thinner. Flat fills only, bright and clean, at most 2-3 colours plus cream #F5F4D0 per item. Simple chunky shapes that still read at 96 px. Vietnamese materials and craft: bamboo, rattan, straw, banana and palm leaf, cotton, indigo cloth, wood, silver.

OUTPUT: square 1:1, plain pure white background, no grid lines, no labels, no numbers, no text, no border, no drop shadow, no sticker outline.

Do NOT: draw the tiger, a head, ears or any body part; add a navy or coloured offset shadow, gloss, glow, gradients, 3D, blur or noisy texture; add four-point sparkles; use Chinese motifs (swirl clouds, dragons, tasselled lanterns, star lanterns, melon caps, round jade discs, red-and-gold imperial colours); draw maps with a red X, compasses or rolled scrolls; draw crowns, medals, trophies or gems; add text, letters or numbers; use mint green #BDDBA7 as the main colour.
```

## `w13-1` · Tuần 13 · Tết

1. Khăn đóng (`khan-dong`) · 2. Cành mai cài (`canh-mai`) · 3. Khánh bạc (`khanh-bac`) · 4. Túi gấm (`tui-gam`)

```
Draw 4 DIFFERENT accessories for a cute chubby cartoon tiger cub, laid out as an invisible grid of 2 columns and 2 rows on a plain pure white background. Each item sits alone in the centre of its own cell, all items drawn at a similar size, with wide white gaps between cells; nothing touches or crosses into another cell. Draw ONLY the items, never the tiger or any part of it. Order left to right, then top to bottom:

1. a traditional Vietnamese khăn đóng: a round wrapped headband turban with neat diagonal fold lines, flat top open (worn on the head). Colours: navy #1B2A6B, a thin butter #F7C844 edge.
2. a small sprig of yellow apricot blossom (hoa mai) with five-petal flowers and buds, tucked on one side of the head (worn on the head). Colours: butter #F7C844 flowers, brown twig, leaf buds.
3. a Vietnamese baby silver khánh pendant: a flat curved silver plate shaped like a lotus-edged crescent, hanging from a thin coral cord, two tiny silver bells (worn around the neck and chest). Colours: silver #C9D1D9 with a cream highlight shape, coral #F07C62 cord.
4. a small drawstring pouch of patterned cloth with a simple diamond weave, hanging at the chest (worn around the neck and chest). Colours: coral #F07C62, butter pattern.

Every item: straight front view, exactly as it is worn or held. Head items leave gaps where two round ears poke through. Neck items have a gentle smile-shaped top edge and hang on the chest. Held items stand upright with the grip at the bottom-centre. Food and icons: one simple object.

STYLE: thin dark sage outline #587E5C (never black), outer contour slightly thicker, inner lines thinner. Flat fills only, bright and clean, at most 2-3 colours plus cream #F5F4D0 per item. Simple chunky shapes that still read at 96 px. Vietnamese materials and craft: bamboo, rattan, straw, banana and palm leaf, cotton, indigo cloth, wood, silver.

OUTPUT: square 1:1, plain pure white background, no grid lines, no labels, no numbers, no text, no border, no drop shadow, no sticker outline.

Do NOT: draw the tiger, a head, ears or any body part; add a navy or coloured offset shadow, gloss, glow, gradients, 3D, blur or noisy texture; add four-point sparkles; use Chinese motifs (swirl clouds, dragons, tasselled lanterns, star lanterns, melon caps, round jade discs, red-and-gold imperial colours); draw maps with a red X, compasses or rolled scrolls; draw crowns, medals, trophies or gems; add text, letters or numbers; use mint green #BDDBA7 as the main colour.
```

## `long-1` · Để dành (150)

1. Nón quai thao (`non-quai-thao`) · 2. Cánh diều sáo (`canh-dieu-sao`) · 3. Áo choàng thổ cẩm (`ao-choang-tho-cam`)

```
Draw 3 DIFFERENT accessories for a cute chubby cartoon tiger cub, laid out as an invisible grid of 2 columns and 2 rows on a plain pure white background. Each item sits alone in the centre of its own cell, all items drawn at a similar size, with wide white gaps between cells; nothing touches or crosses into another cell. Draw ONLY the items, never the tiger or any part of it. Order left to right, then top to bottom:

1. a Northern Vietnamese nón quai thao: a big flat round palm-leaf hat with a shallow rim and two long cream silk chin straps (worn on the head). Colours: straw #E8D9A8, cream straps, a coral inner band.
2. a Vietnamese flute kite (diều sáo): a flat wing-shaped kite on a bamboo frame with a row of small bamboo flutes along its centre, held up on a short bamboo stick (held in one paw). Colours: cream paper, bamboo frame, turquoise trim.
3. a short shoulder cape of Vietnamese highland brocade (thổ cẩm): horizontal bands of simple diamond and zigzag woven patterns, fastened with a wooden toggle (worn around the neck and chest). Colours: indigo #3B4BA8, coral, butter, cream bands.

Every item: straight front view, exactly as it is worn or held. Head items leave gaps where two round ears poke through. Neck items have a gentle smile-shaped top edge and hang on the chest. Held items stand upright with the grip at the bottom-centre. Food and icons: one simple object.

STYLE: thin dark sage outline #587E5C (never black), outer contour slightly thicker, inner lines thinner. Flat fills only, bright and clean, at most 2-3 colours plus cream #F5F4D0 per item. Simple chunky shapes that still read at 96 px. Vietnamese materials and craft: bamboo, rattan, straw, banana and palm leaf, cotton, indigo cloth, wood, silver.

OUTPUT: square 1:1, plain pure white background, no grid lines, no labels, no numbers, no text, no border, no drop shadow, no sticker outline.

Do NOT: draw the tiger, a head, ears or any body part; add a navy or coloured offset shadow, gloss, glow, gradients, 3D, blur or noisy texture; add four-point sparkles; use Chinese motifs (swirl clouds, dragons, tasselled lanterns, star lanterns, melon caps, round jade discs, red-and-gold imperial colours); draw maps with a red X, compasses or rolled scrolls; draw crowns, medals, trophies or gems; add text, letters or numbers; use mint green #BDDBA7 as the main colour.
```

## `backlog-1` · Dự phòng

1. Băng đô mây (`bang-do-may`)

```
Draw 1 DIFFERENT accessories for a cute chubby cartoon tiger cub, laid out as an invisible grid of 1 columns and 1 rows on a plain pure white background. Each item sits alone in the centre of its own cell, all items drawn at a similar size, with wide white gaps between cells; nothing touches or crosses into another cell. Draw ONLY the items, never the tiger or any part of it. Order left to right, then top to bottom:

1. a sky-blue headband topped with four round puffy clouds (simple round bumps, no spirals or curls), two small round butter-yellow beads hanging at the ends (worn on the head). Colours: sky blue #8DC6EE band, cream clouds, butter beads.

Every item: straight front view, exactly as it is worn or held. Head items leave gaps where two round ears poke through. Neck items have a gentle smile-shaped top edge and hang on the chest. Held items stand upright with the grip at the bottom-centre. Food and icons: one simple object.

STYLE: thin dark sage outline #587E5C (never black), outer contour slightly thicker, inner lines thinner. Flat fills only, bright and clean, at most 2-3 colours plus cream #F5F4D0 per item. Simple chunky shapes that still read at 96 px. Vietnamese materials and craft: bamboo, rattan, straw, banana and palm leaf, cotton, indigo cloth, wood, silver.

OUTPUT: square 1:1, plain pure white background, no grid lines, no labels, no numbers, no text, no border, no drop shadow, no sticker outline.

Do NOT: draw the tiger, a head, ears or any body part; add a navy or coloured offset shadow, gloss, glow, gradients, 3D, blur or noisy texture; add four-point sparkles; use Chinese motifs (swirl clouds, dragons, tasselled lanterns, star lanterns, melon caps, round jade discs, red-and-gold imperial colours); draw maps with a red X, compasses or rolled scrolls; draw crowns, medals, trophies or gems; add text, letters or numbers; use mint green #BDDBA7 as the main colour.
```
