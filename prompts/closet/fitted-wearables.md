# Đồ mặc vừa người · prompt ChatGPT (Hǔhǔ, Wuwu, Dudu)

Áo, giày cần vẽ riêng cho từng bạn: mỗi bạn một dáng người khác (Wuwu thân bè, tay khoanh; Dudu đứng nghiêng, một tay nắm). Kéo giãn hình chung hoặc vẽ bằng code đều xấu, nên mỗi món mặc cần một hình vẽ đúng dáng người đó.

Đính kèm theo thứ tự:
- **ảnh 1** = dáng của bạn đó:
  - Hǔhǔ: `assets/char/gen/huhu-front-idle.png`
  - Wuwu: `assets/char/gen/wuwu/wuwu-dressup-base.png`
  - Dudu: `assets/char/gen/dudu/dudu-dressup-base.png`
- **ảnh 2** = hình món gốc:
  - Áo Choàng Lá: `assets/closet/v3/items/10.png`
  - Giày Lá: `assets/closet/v3/items/14-boot.png`
- **ảnh 3** = style mẫu `materials/references/closet/style-ref-v2.png`

Mỗi khối = 1 chat mới. Tải PNG gốc, đặt tên đúng chỗ rồi chạy `python3 scripts/build_dressup.py`. Pipeline tự đặt hình vào người (áo: rộng bằng thân + tay, mép trên dưới cằm; giày: rộng bằng bàn chân, đế chạm đất).

| Món | Lưu vào |
|---|---|
| Áo của Hǔhǔ | `assets/closet/v3/fitted/huhu/ao-choang-la.png` |
| Áo của Wuwu | `assets/closet/v3/fitted/wuwu/ao-choang-la.png` |
| Áo của Dudu | `assets/closet/v3/fitted/dudu/ao-choang-la.png` |
| Giày (chân phải) | `assets/closet/v3/fitted/<huhu / wuwu / dudu>/giay-la.png` |

---

## Áo Choàng Lá mặc vừa người (thay `<NAME>` và mô tả dáng)

Dáng:
- Hǔhǔ: *two arms hang straight down at his sides*
- Wuwu: *very wide round body, both arms folded across the chest, paws meeting in the middle*
- Dudu: *left arm held out to the side with a closed fist, right arm hanging down*

```
Image 1 is <NAME>, a finished cartoon character, standing front-facing. Image 2 is the Leaf Cape item. Image 3 is the STYLE REFERENCE (line weight and colour, flat fills, one small flat highlight, chunky rounded shapes); copy the style only, none of its items.

Redraw the Leaf Cape from image 2 as a TOP WORN BY <NAME> in exactly his pose: <POSE>. Same design (overlapping green leaves, cream inner leaves, the gold bead at the collar), now shaped to his body: it covers his chest, belly and shoulders and has sleeves that follow his arms exactly as they are posed and stop at the wrist, so his paws stay bare. The collar sits right under his chin.

Draw ONLY the garment, exactly as it would look on him from the front: only its outside is visible (no inner lining, no opening, no back side). Same size and position as on image 1, so it can be laid straight over him. Do NOT draw the character, his head, paws, legs, tail or ghost wisps. Plain white background, nothing else in the picture. Flat 2D, no gradients, no glow, no text.
```

## Giày Lá mặc vừa chân (một chiếc, chân phải)

```
Image 1 is <NAME>, a finished cartoon character, standing front-facing. Image 2 is the Leaf Boot item. Image 3 is the STYLE REFERENCE; copy the style only.

Redraw ONE Leaf Boot from image 2 as it looks WORN on <NAME>'s right foot, seen from the front like in image 1: the same width as his foot, the sole flat on the ground, toe facing the viewer. Only its outside is visible: no opening or inner lining at the top, his leg goes into it. Same design (green shaft, cream toe with cloud scallops, blue sole, gold bead), no text.

Draw ONLY the boot: no foot, no leg, no character. Plain white background. Flat 2D, no gradients, no glow.
```

Gửi hình về, Claude tách nền và đặt vào. Chưa có hình thì trang dùng áo choàng gốc (không có tay áo) và giày vẽ theo bàn chân.
