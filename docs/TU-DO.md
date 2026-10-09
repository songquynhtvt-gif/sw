# Tủ đồ · ý tưởng, list items, pipeline GPT

Nguồn: brief v13.4 (phụ kiện = PNG trong suốt gắn điểm neo · founder 9/10: **neo đầu, cổ, tay** · giá 40 / 80 / 150 · 4 món mới 80 mỗi 2 tuần từ tuần 3 · cần món 150 để dành), HIFI-PREP G5 (list stage 1 đã duyệt), PROMPT-RULES §1 + §7.
Catalogue máy đọc được: `prompts/closet/items.json` (42 món). Prompt từng đợt: `prompts/closet/<wave>.md`.

---

## 1 · Review 2 sheet đã prompt

Ảnh gốc: `materials/references/closet/sheet-1-forest.webp`, `sheet-2-explorer.webp`.

**Style:** đẹp, nhưng **bóng navy lệch + texture màu nước** là style icon/sticker. Đeo lên Hǔhǔ (viền sage, màu phẳng) sẽ thành "dán" chứ không "mặc". → Vẽ lại mỗi món theo nét Hǔhǔ, nền trong suốt; **một file dùng cho cả lớp đeo lẫn thẻ cửa hàng** (bóng thẻ làm bằng code). Rẻ gấp đôi so với làm 2 bộ.

**Nội dung** (đối chiếu luật §1: không motif Trung, không ✦, không X đỏ / la bàn / cuộn giấy):

| Sheet · # | Món | Kết luận | Thành item |
|---|---|---|---|
| 1 · 1 | Mũ lá | 🟢 giữ | `mu-la` |
| 1 · 2 | Băng đô mây + sao | 🟠 mây xoắn 祥云 → mây tròn trơn, bỏ sao | `bang-do-may` (dự phòng) |
| 1 · 3 | Khăn bandana đỏ | 🟠 mây xoắn → đổi thành khăn rằn | `khan-ran` |
| 1 · 4 | Vòng hạt + mề đay mầm | 🟢 giữ | `vong-hat-rung` |
| 1 · 5 | Mũ phù thuỷ lá | 🟡 dáng Tây → lá gấp + đai tre | `mu-chop-la` |
| 1 · 6 | Băng đô trăng khuyết | 🟡 bỏ viên đá quý → hạt tròn | `bang-do-trang` |
| 1 · 7 | Áo choàng sao xanh | 🟠 sao 4 cánh + mây xoắn + tua → chấm tròn, viền vỏ sò | `ao-choang-cham` |
| 1 · 8 | Mũ trùm sừng + mây | 🟡 bỏ mây; sừng thành sừng trâu | `mu-trum-trau` |
| 1 · 9 | Mặt ngọc bích tròn | 🔴 ngọc bội kiểu Trung → khánh bạc Việt | `khanh-bac` |
| 1 · 10 | Vương miện vàng | 🔴 vương miện + đá quý (G5 đã gạch) | bỏ |
| 2 · 1 | Mũ thám hiểm + kính | 🟢 thành mũ cối (rất Việt) | `mu-coi-kinh` |
| 2 · 2 | Mũ quả dưa mây xanh | 🔴 mũ Trung + mây xoắn | bỏ |
| 2 · 3 | Mũ thuyền giấy | 🟡 bỏ mặt trời đỏ + xoắn | `mu-thuyen-giay` |
| 2 · 4 | Cổ áo đồng hồ cát | 🔴 không Việt, không đọc được ở 96 px | bỏ |
| 2 · 5–7 | Áo choàng đỏ / xanh / đen | 🟠 mây xoắn, tua → thay bằng áo tơi lá, áo choàng chàm | `ao-toi-la` |
| 2 · 8 | Áo choàng bản đồ X đỏ | 🔴 X đỏ | bỏ |
| 2 · 9 | Đèn lồng có tua | 🔴 đèn lồng tua | bỏ (xem `hu-dom-dom`) |
| 2 · 10 | Ống nhòm + la bàn | 🟡 bỏ la bàn, thân tre | `ong-nhom-tre` |
| 2 · 11 | Bó cuộn giấy | 🔴 cuộn giấy | bỏ |
| 2 · 12 | Cánh thiên thần | 🟡 → chuồn chuồn đậu trên băng đô (không có neo lưng) | `bang-do-chuon-chuon` |

---

## 2 · List items (42)

Đầy đủ mô tả, màu, nguồn: `prompts/closet/items.json`. Xem nhanh: `python3 scripts/gen_closet.py --list`.

**Stage 1 (G5, chỉnh theo quyết định 9/10)**
- Phụ kiện 40: Nón lá · Khăn rằn · Nơ bướm · Vòng hoa · Khăn quàng lá
- Phụ kiện 80: Diều giấy ✋ (cầm que) · Trống cơm · Giỏ xách mây ✋ (thay ba lô gỗ)
- Đã bỏ: Đèn ông sao (founder 9/10), Áo bà ba mini (không có neo thân)
- Món khoái khẩu 40: Bánh cam · Xôi gấc · Chè · Bánh bò
- Giữ chuỗi: Ngày Ngủ (50) · Hồi Sinh Chuỗi (150)

**Đợt mới, 4 món × 80, mỗi 2 tuần** (mỗi đợt 1 chủ đề, mỗi đợt có ≥1 mũ + ≥1 món cổ)

| Đợt | Chủ đề | Món |
|---|---|---|
| Tuần 3 | Rừng lá | Mũ lá · Vòng hạt rừng · Áo tơi lá · Mũ chóp lá |
| Tuần 5 | Thám hiểm | Mũ cối kính bay · Ống nhòm tre ✋ · Túi cói · Ống tre đựng nước |
| Tuần 7 | Sông nước | Mũ thuyền giấy · Vòng hoa súng · Nơ lá dừa · Cần câu tre ✋ |
| Tuần 9 | Đồng quê | Mũ trùm sừng trâu · Mõ trâu · Mũ rơm · Sáo trúc ✋ |
| Tuần 11 | Đêm đom đóm | Băng đô trăng khuyết · Hũ đom đóm ✋ · Áo choàng chàm · Băng đô chuồn chuồn |
| Tuần 13 | Tết | Khăn đóng · Cành mai cài · Khánh bạc · Túi gấm |

**Để dành 150:** Nón quai thao · Cánh diều sáo ✋ (cầm que) · Áo choàng thổ cẩm
**Dự phòng:** Băng đô mây

✋ neo tay

---

## 3 · Quyết định (founder 9/10)

1. **Neo: đầu, cổ, tay.** Không có neo lưng / thân. Món lưng đổi sang cầm tay (diều, diều sáo cầm que; giỏ xách mây, cần câu tre) hoặc lên đầu (băng đô chuồn chuồn). Áo bà ba bỏ.
2. **Đèn ông sao: bỏ** khỏi Tủ đồ. Hũ đom đóm vẫn ở đợt tuần 11.
3. **Thử trên Hǔhǔ trước.** Neo đo trên `assets/char/gen/huhu-front-idle.png`, nằm trong `items.json` → `anchors.huhu`. Dūdū / Wūwū thêm sau, cùng cấu trúc.

### Ướm đồ lên Hǔhǔ
```
python3 scripts/fit_preview.py --id mu-la                         # 1 món
python3 scripts/fit_preview.py --id non-la khan-ran ong-nhom-tre  # đủ bộ đầu + cổ + tay
```
→ `assets/closet/fit/huhu-<ids>.png`. Lấy file approved nếu có, không thì bản gen mới nhất.
Món lệch: thêm `"fit": {"scale": 1.1, "dx": 0, "dy": -0.02}` vào món đó trong `items.json` (đơn vị = tỉ lệ ảnh pose). Số `fit` này là số dev dùng để gắn neo trong app.

---

## 4 · Pipeline GPT

1. Thêm key vào `.env` (đã có trong `.gitignore`):
   ```
   OPENAI_API_KEY=sk-...
   OPENAI_IMAGE_MODEL=gpt-image-1
   ```
2. Chạy thử 3 món (đầu + cổ + tay), ướm lên Hǔhǔ để chốt style:
   ```
   python3 scripts/gen_closet.py --id mu-la khan-ran ong-nhom-tre --dry-run   # xem prompt
   python3 scripts/gen_closet.py --id mu-la khan-ran ong-nhom-tre             # 2 biến thể / món
   python3 scripts/fit_preview.py --id mu-la khan-ran ong-nhom-tre
   ```
3. Chấm theo QA §7. Món 🟢 copy sang `assets/closet/approved/<id>.png`, sửa `status` thành `approved` trong `items.json`.
4. Từ đó luôn đính kèm món đã duyệt làm style ref để cả kho đồng bộ:
   ```
   python3 scripts/gen_closet.py --wave stage1 --ref assets/closet/approved/mu-la.png assets/closet/approved/khan-ran.png
   ```
5. Mỗi lần chạy được ghi vào `runs` của món trong `items.json`, file ra `assets/closet/gen/<id>-v<n>.png` (nền trong suốt sẵn, không cần cắt nền).

**Không có API key (cách đang dùng): làm hàng loạt bằng sheet**
1. Mở `prompts/closet/ALL-CHATGPT.md`: 12 sheet, mỗi sheet tối đa 4 món, phủ hết kho.
2. Dán từng khối vào ChatGPT (chat mới mỗi 3 sheet), tải ảnh về, đặt tên theo mã sheet (`w3-1.png`…), bỏ vào `materials/chatgpt-designs/closet/`.
3. Một lệnh cắt cả thư mục: xoá nền trắng, tách từng món, lưu `assets/closet/gen/`, ghi `items.json`, ướm lên Hǔhǔ ở `assets/closet/fit/`:
   ```
   python3 scripts/split_sheet.py materials/chatgpt-designs/closet/
   ```
   Một món lẻ làm riêng: `python3 scripts/import_item.py <id> <ảnh>`.
4. Xuất cả kho thành 1 file zip:
   ```
   pip3 install -r requirements.txt
   python3 scripts/export_closet.py
   ```
   → `exports/tu-do-<ngày>.zip`: `png/<đợt>/<id>.png` (nền trong suốt, cạnh dài 2048 px, viền đã khử lem trắng) · `svg/<đợt>/<id>.svg` (vector, phóng bao nhiêu cũng nét) · `fit/huhu-<id>.png` · `catalogue.csv` · `contact-sheet.png` (xem nhanh cả kho).

Thêm món mới: thêm 1 object vào `items.json` → `python3 scripts/build_prompts.py`.

Chi phí ước tính: 42 món × 2 biến thể ≈ 84 ảnh mỗi vòng (`--quality medium`).
