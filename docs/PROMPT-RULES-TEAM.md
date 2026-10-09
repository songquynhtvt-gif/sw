# TongHua Land · Luật prompt cho team (rút gọn)

Bản đầy đủ và mọi prompt đã chạy: `ref/PROMPTS-MASTER.md`. File này chỉ giữ luật và mẫu để tự viết prompt mới.
Công cụ: ChatGPT / Gemini Pro. Prompt viết **tiếng Anh**, dán nguyên khối, chỉ điền vào các ô `[...]`.

---

## 0 · Quy trình chung (mọi loại ảnh)

1. **Luôn đính kèm ảnh tham chiếu** (anchor) đúng thứ tự ghi ở từng mục. Không tả style bằng chữ khi đã có ảnh mẫu.
2. **Một prompt sạch, tối đa 1–2 lần sửa.** Sửa nhiều lần thì ảnh trôi màu, xám dần. Hỏng thì làm lại từ prompt gốc, không sửa chồng.
3. Mở **chat mới sau mỗi 3–4 ảnh** để AI không "nhớ" lỗi cũ.
4. AI chỉ làm **chất liệu** (nền, nhân vật, icon, vật thể). Màn hình, chữ, nút, tên vùng đất dựng trong Figma/code, **không bao giờ để AI vẽ cả màn hình**.
5. Hậu kỳ làm ở máy (dev/design lo): xoá logo Gemini ✦ góc phải dưới, chỉnh màu (+15% bão hoà, +5% tương phản, +2% sáng), upscale 2×, cắt nền trắng.
6. Chấm điểm trước khi dùng: 🟢 dùng ngay · 🟡 dùng, ghi chú · 🟠 làm lại · 🔴 cấm. **Chỉ 🟢 và 🟡 được ship.**

## 1 · Luật cấm chung (áp cho mọi ảnh)

**Thế giới là Việt Nam, không Trung Quốc:**
- Không đèn ông sao, không đèn lồng có tua, không mây xoắn 祥云, không rồng, không chùa mái cong nhiều tầng, không đỏ-vàng cung đình.
- Nguồn sáng ấm duy nhất là **đèn dầu** (bóng thuỷ tinh, ngọn lửa hổ phách).
- Đạo cụ nên dùng: tre, lá chuối, dương xỉ, mây tre, mái tranh, nhà sàn, thúng chai, chum, nón lá.

**Dấu hiệu "AI slop", cấm hết:**
- Sao 4 cánh lấp lánh ✦.
- Bóng loáng kiểu kẹo, kính, quầng mờ (blur halo).
- 3D đất sét.
- Mây hồng tím kiểu synthwave.
- Bản đồ có X đỏ, la bàn, cuộn giấy cuộn hai đầu.
- Chữ nằm trong hình.
- Chữ trắng trên nền cam.

**Logic ánh sáng:** phản chiếu nằm ngay dưới nguồn sáng, mặt được chiếu quay về phía đèn. Ánh đèn vẽ thành **một mảng phẳng sáng hơn**, không blur.

---

## 2 · Background (nền cảnh)

**Style:** "CRAZY night". Đêm, màu bão hoà mạnh, mảng phẳng có dải màu kiểu sơn (**không phải cut paper**).
**Ảnh 1 bắt buộc:** `ref/bg/explore/C0-crazy-v6-soft-sat15.png` (chỉ lấy style, không chép nhà, sông, đồi).

**4 luật bố cục, thiếu cái nào là hỏng:**
1. **Vùng yên (calm zone):** chỗ đặt chữ hoặc khung giấy, ghi rõ % (ví dụ "left 45 percent"). Vùng này phải **tối** (chàm, xanh rêu, navy) để khung giấy kem nổi lên. Không dùng tường nâu, cam trơn.
2. **Mặt phẳng sân khấu (stage):** đúng **một** mặt phẳng trống (chiếu, tảng đá, bờ, lối đi), ghi % rộng và chiều cao, để Hǔhǔ đứng hoặc ngồi. Không có stage thì nhân vật sẽ lơ lửng.
3. **Vùng bận (busy zone):** chi tiết và bé ma chỉ nằm trong vùng này.
4. Biến vùng trống thành **một vật cụ thể có tên** ("a giant dark leaf wall", "a calm indigo plank wall"). Viết "empty area" thì AI sẽ vẽ đầy vào.

**Bé ma (creatures):** chỉ ló mắt và đỉnh đầu, tối đa 3, mỗi con một màu đậm khác nhau (mận, xanh rêu đậm, đỏ san hô, chàm). **Không bao giờ màu bạc hà hay trắng**, vì đó là màu hồn ma của Hǔhǔ.

**Mẫu (dán, điền 4 ô):**
```
Use image 1 only as the style reference: same colours, same energy, same flat graphic look with soft painted colour bands, same kind of peeking creatures. Do NOT copy its house, river, hills or its star-shaped lantern.

One single wide 3:2 landscape (1536x1024), nighttime, graphic 2D flat illustration with bold simplified shapes and soft painted colour bands (not cut paper). Highly saturated, funky night palette: deep electric navy and indigo with acid green, turquoise, lime, coral, hot pink, lavender and butter yellow; colours behave unexpectedly (pink ferns, turquoise tree trunks, lime moss, violet shadows). Not realistic green, not a dark horror forest.

SCENE: [SCENE — what is in the picture, Vietnamese objects]

The only warm light source is a small Vietnamese glass oil lamp (đèn dầu): a clear glass chimney with a warm amber flame, its glow drawn as ONE flat lighter shape, no blur halo. No star-shaped lantern, no paper lantern, no tassels.

Friendly ghost/monster creatures only PEEK (eyes and top of head), each a different deep colour (plum, dark teal, coral red, indigo), never mint or white, max 3, only inside the busy zone named below.

LAYOUT (an app interface sits on top):
- Calm zone: [where, in percent, named as one dark object — a card or title sits there]
- Stage: [one flat empty surface, x to y percent wide, top at z percent high, a character stands/sits there]
- Busy zone: [where the details and creatures go]
- Keep creatures and key details at least 8 percent from the left and right edges.
- Reflections directly under their light. No four-point sparkles.

Keep it Vietnamese (bamboo, banana leaves, ferns, rattan, thatch). No text, no letters, no people, no tiger or animal characters, no Chinese motifs (no swirl clouds, pagodas, dragons, star lanterns, tasselled lanterns), no castles, no 3D, no Disney/Pixar look.
Mood: [MOOD — 3 to 5 words]
```

**QA nền:**

| Mức | Điều kiện |
|---|---|
| 🔴 | Có đèn ông sao hoặc motif Trung |
| 🔴 | Có chữ, có người |
| 🟠 | Vùng yên không đủ tối để đặt khung kem |
| 🟠 | Không có stage |
| 🟠 | Có sao 4 cánh |
| 🟠 | Bé ma màu bạc hà hoặc nằm ngoài vùng bận |
| 🟡 | Hơi khác tông so với các nền khác |

---

## 3 · Nhân vật Hǔhǔ

**Quy trình 2 bước:**
1. Làm **sheet** (nhiều pose) để duyệt. Sheet không bao giờ ship.
2. Mỗi pose được duyệt thì render lại **1 nhân vật / 1 ảnh**, ≥1500px, nền trắng.

**Đính kèm 4 ảnh, đúng thứ tự:**

| # | File | Vai trò |
|---|---|---|
| 1 | `benchmark/huhu-front.jpg` | Nhận diện: mặt, nanh, ria-cười |
| 2 | `benchmark/huhu-eyes-closeup.png` | Cấu tạo mắt |
| 3 | `approved/huhu-set1-combined.png` | Nét, độ sáng màu |
| 4 | `HÚ HÚ 4 ANGLES FLAT.JPG` | Đuôi, màu |

**Không bao giờ đổi:**
- Hổ con mũm mĩm đứng 2 chân, đầu to bằng thân.
- **Nét cười hình ria màu tím đậm luôn hiện**, kèm 2 răng nanh trắng.
- Mắt tròng cam, đồng tử xanh đen, hai mắt nhìn cùng hướng.
- Đuôi ngắn dày, 2–3 sọc sage, chóp tròn màu sage đậm.
- **Luôn có 2–3 hồn ma bạc hà** bay quanh, có mắt, không có miệng.
- Nét viền sage `#587E5C` (không dùng đen), tô màu phẳng, không bóng, không viền sticker trắng.

**Pose và cảm xúc phải khác nhau theo từng khoảnh khắc** (vẫy chào, nhảy mừng, tinh nghịch, suy nghĩ, buồn nhẹ, đi bộ, cầm đèn dầu…). Hǔhǔ luôn quay mặt về phía nội dung chính trên màn.

**Cách xưng hô (lời thoại, VO):** nói với bố mẹ thì xưng **"Con"**, nói với bé thì xưng **"Tui"**.

**MASTER** (dán nguyên, chỉ điền 4 ô cuối):
```
Draw ONE new illustration of Hǔhǔ, the exact tiger character in the reference images. Image 1 = identity, image 2 = eye construction, image 3 = line and colour style, image 4 = tail and colours. Ignore the thin vertical guide line in image 1.

IDENTITY (never change): chubby bipedal tiger cub, big round head about the same width as the body, short legs, mitten paws, stands and walks upright on two legs. Round sage ears with cream inner ear.

FACE (must match image 1 and 2 exactly):
- A wide thin DARK PURPLE mustache-shaped smile line (#3B2A5C) that sweeps across the lower face like a "W" moustache. It is always visible, even when the mouth is open. An open mouth is only a small opening UNDER this line, inside colour muted red #B8483E. Never a big round cartoon mouth replacing the line.
- Two small WHITE FANGS at both ends of the smile line, sweeping outward and slightly up toward the cheeks.
- Eyes: large, cream #F5F4D0 eye white, thin dark outline, big vivid ORANGE iris #FA6402, dark green pupil #1D291F, one small lash tick at the outer top. Both pupils look in the SAME direction. Front view: both eyes the same size. Three-quarter view: the eye nearer to the viewer is slightly BIGGER.
- Small orange nose #FF630A.
- Cheek tufts on both sides of the head: orange #F69934 fur with 2-3 sage stripes, same shape as image 1.

BODY: cream fur #F5F4D0, one big belly oval #E0DF96, thin wavy sage stripes #587E5C / #76A27E on head, back, arms and legs. Orange toe beans #FF630A on the soles and palms.

GHOST WISPS (always): 2-3 small mint-green ghost wisps #BDDBA7 float around him, each a soft teardrop with a curled tail and 2 small white oval eyes (no mouth), about one quarter of his head size, flat fill with a thin darker mint outline, near the head and shoulders, never covering his face, paws or the prop. Their mood follows his.

TAIL: thick and short, about half the body height, curving up behind him, cream base with 2-3 wide light-sage bands and a big ROUNDED dark sage #587E5C tip.

LINE + COLOUR: thin dark sage outline #587E5C, outer contour slightly thicker, inner lines thinner. Flat fills only, bright and clean like image 3.

POSE: [POSE]
EXPRESSION: [EXPRESSION]
PROP: [PROP or "none"]
ACCENT: [ACCENT or "none"]

OUTPUT: single character, full body, both feet visible, centred with 10% margin, plain pure white background, square 1:1, 2K, no text, no border, no frame, no drop shadow.
```
**NEGATIVE** (luôn dán kèm):
```
Do NOT: draw a sheet, grid or multiple characters; replace the mustache smile with a small cat "ω" mouth or a big round open mouth; drop the fangs; make the iris red or brown; make the eyes different sizes in a front view; point the pupils in different directions; wink; draw a flat paddle tail or camouflage blotches on the tail; add soft shading, gradients, glow, airbrush, texture, 3D, blur or drop shadows; add a white sticker border or a halo; use pure black lines; walk on four legs; add text or logos; add a background scene; draw him without his 2-3 mint ghost wisps; give the wisps mouths or a white/grey colour; use Chinese or Japanese props (Chinese lanterns, red seals, mochi, dumplings).
```
Muốn có chuyển động nhẹ (rig), thêm câu: *"Arms slightly away from the body, wisps not touching him, eyes open"* để dev tách lớp được.

---

## 4 · Icon (C2 cut paper)

**Khác nền:** icon là **giấy cắt dán thật**, 2–4 lớp phẳng, có lớp lót navy mỏng làm chiều sâu duy nhất. Không viền, không bóng, không chữ.
**Ảnh 1–2 bắt buộc:** `ref/icons/c2-sheet-1.webp`, `ref/icons/c2-sheet-2.webp`.
**Bảng màu duy nhất:**

| Màu | Mã |
|---|---|
| Turquoise | #2EC4B6 |
| Leaf | #6CC36F |
| Violet | #8A6BE0 |
| Coral | #F07C62 |
| Butter | #F7C844 |
| Gold | #F5C542 |
| Cream | #FBF4E4 |
| Navy | #1B2A6B |

**Thêm icon mới:** luôn dùng cách "thêm vào bộ có sẵn". Ô đầu tiên chép lại 1 icon cũ để AI tự cân chỉnh:
```
Images 1 and 2 are one finished icon set. Add [N] NEW icons to this set so they are indistinguishable from the existing ones: same cut-paper material, same paper texture, same layering and navy under-layer, same colours, same level of detail, same size.

To keep them consistent, draw a 4x2 grid on plain white. Top-left cell: copy the open book icon from image 1 exactly (as a reference). The other cells are the new icons:
- [icon 1 — what it is, main colour]
- [icon 2 …]
```

**QA icon:**

| Mức | Điều kiện |
|---|---|
| 🔴 | Có chữ trong icon (trừ khi được yêu cầu), đèn ông sao |
| 🟠 | Lệch chất liệu so với bộ (bóng, 3D, có viền) |
| 🟠 | Không đọc được ở 32px |

---

## 5 · Vật thể tách lớp (bản đồ, hộ chiếu, đạo cụ cho motion)

- Vẽ **riêng vật thể trên nền trắng tinh**, không đổ bóng, mép sạch để cắt. Nền cảnh làm riêng, **không vẽ vật thể đó vào nền** (ví dụ rương để trống, bản đồ là một lớp riêng).
- Vật thể có nhiều mục (13 vùng đất…): ghi rõ **thứ tự, hàng, chiều đi của đường**, và nói "mỗi ô khác nhau, không lặp".
- Cần sửa vài ô thì dùng **edit tại chỗ**: "Edit only … keep everything else exactly the same", ghi vị trí hàng/cột.
- Chữ, tên, số, ghim **luôn dựng bằng code**. Để chừa chỗ, AI chỉ vẽ ô trống.

---

## 6 · Lưu file

- Đặt tên theo mã màn hoặc mã cảnh, ví dụ `ref/bg/onboard/N7-v2.png`, `ref/char/gen/25-holding-oil-lamp.png`.
- Giữ bản gốc tải về (`*-source.png`). Dev xuất bản đã xử lý vào `hires/`.
- Ghi kết quả QA và prompt đã dùng vào `ref/PROMPTS-MASTER.md` để lần sau không lặp lỗi.

---

## 7 · Tủ đồ (phụ kiện, món ăn)

Catalogue: `prompts/closet/items.json`. Ý tưởng + review: `docs/TU-DO.md`.

- **Một file master cho mỗi món**, vẽ theo **nét của Hǔhǔ** (viền sage, màu phẳng), nền **trong suốt**. Cùng file đó dùng cho lớp đeo lên nhân vật (neo đầu/cổ) và thẻ cửa hàng (bóng đổ của thẻ dựng bằng code).
- **Không** vẽ nhân vật trong ảnh phụ kiện. **Không** bóng navy lệch kiểu sticker: bóng đó làm món đồ "dán" lên Hǔhǔ chứ không "mặc".
- Nhìn **thẳng chính diện**, đúng tư thế khi đeo. Mũ chừa chỗ cho 2 tai tròn.
- Đọc được ở **96 px** (ô thẻ cửa hàng): tối đa 2–3 màu + kem, hình khối đơn giản.
- Luật cấm §1 áp hết. Riêng tủ đồ còn cấm: vương miện, huy chương, cúp, đá quý, mũ quả dưa, ngọc bích tròn kiểu Trung, áo choàng có mây xoắn hoặc tua rua. Màu bạc hà `#BDDBA7` không làm màu chính (màu hồn ma của Hǔhǔ).

**ITEM MASTER** (script tự điền 4 ô):
```
Draw ONE wearable accessory or item for a cute chubby cartoon tiger cub. Draw ONLY the item, never the tiger or any part of it.

ITEM: [ITEM]
SLOT: [SLOT]
COLOURS: [COLOURS]
FIT: [FIT]

STYLE: thin dark sage outline #587E5C (never black), outer contour slightly thicker, inner lines thinner. Flat fills only, bright and clean, at most 2-3 colours plus cream #F5F4D0. Simple chunky shapes that still read at 96 px. Vietnamese materials and craft: bamboo, rattan, straw, banana and palm leaf, cotton, indigo cloth, wood, silver.

OUTPUT: the single item centred with 12% margin, fully transparent background, square 1:1, no character, no head, no mannequin, no text, no border, no drop shadow, no sticker outline.
```
**ITEM NEGATIVE** (luôn dán kèm):
```
Do NOT: draw the tiger, a head, ears or any body part; draw several items or a sheet; add a navy or coloured offset shadow, gloss, glow, gradients, 3D, blur or noisy texture; add four-point sparkles; use Chinese motifs (swirl clouds, dragons, tasselled lanterns, star lanterns, melon caps, round jade discs, red-and-gold imperial colours); draw maps with a red X, compasses or rolled scrolls; draw crowns, medals, trophies or gems; add text, letters or numbers; use mint green #BDDBA7 as the main colour.
```

**QA tủ đồ:**

| Mức | Điều kiện |
|---|---|
| 🔴 | Có motif Trung, chữ, vương miện / đá quý, hoặc vẽ cả nhân vật |
| 🟠 | Có bóng navy lệch, bóng loáng, 3D, viền đen |
| 🟠 | Nghiêng, không chính diện, mũ không chừa chỗ tai |
| 🟠 | Không đọc được ở 96 px |
| 🟡 | Lệch tông nhẹ so với các món đã duyệt |
