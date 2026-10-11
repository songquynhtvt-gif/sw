# Thay Đồ: Hǔhǔ, Wuwu, Dudu

Trang: https://claude.ai/artifact/4doA81XFEbPMKieNRZe9qp

## Thêm món mới (nhanh)

1. **Cắt sheet:** lưu sheet vào `materials/chatgpt-designs/closet-v5/`, rồi chạy:
   `python3 scripts/cut_objects.py materials/chatgpt-designs/closet-v5/sheet-1.webp assets/closet/v5/items --grid 4x2 --prefix s1 --upscaled tools/cache/sheets/v5-sheet-1-x4.png`
   Bước này phóng to 4 lần, tách nền trắng và giữ chi tiết rời. Xem `assets/closet/v5/items/s1-contact.png` để biết số thứ tự từng món.
2. **Khai món** trong `scripts/build_dressup.py`:
   - Thêm 1 dòng vào `CATALOG`, dùng mẫu vị trí có sẵn `K[...]` theo loại: `hat` · `flower` · `ring` · `scarf` · `pendant` · `necklace` · `cape` · `wings` · `bag` · `bottle` · `book` · `stick` · `kite`.
   - Ví dụ: `("v5:s1-03", "mu-moi", "Mũ Mới", "head", K["hat"]),`
   - Gắn vùng ở `REGION_OF` (C0–C12), viết 1 câu ở `ABOUT`.
3. **Dựng chỉ các món mới**, khoảng 30 giây, cả 3 bạn:
   `python3 scripts/build_dressup.py --items mu-moi,tui-moi`
   Lệnh này tự ghép lại `hu-hu-thay-do.html`. Nếu món mới tràn ra ngoài khung cũ, lệnh tự chuyển sang dựng lại toàn bộ (khoảng 4 phút).
4. **Kiểm tra:** `python3 scripts/preview_dressup.py /tmp/pv.png mu-moi,tui-moi`, ra từng món trên cả 3 bạn.
5. **Đăng** `hu-hu-thay-do.html` cùng các file `*/layers/<id>*.webp` và `thumbs/<id>.webp` mới.

Áo vẽ riêng theo dáng từng bạn (có tay áo): `assets/closet/v3/fitted/<huhu|wuwu|dudu>/<id>.png`. Có file là tự dùng, prompt ở `prompts/closet/fitted-wearables.md`.

## Dáng gốc

- **Hǔhǔ:** `assets/char/gen/huhu-front-idle.png`
- **Wuwu:** `assets/char/gen/wuwu/wuwu-front-idle.png`
- **Dudu:** `assets/char/gen/dudu/dudu-front-idle-bamboo.png`. `scripts/prep_mascots.py` tách nón lá và gậy tre thành món riêng của Dudu, rồi vẽ lại đỉnh đầu, tai và nắm tay, ra `dudu-dressup-base.png`.

Khung từng bạn nằm trong `MASCOTS` (đầu, cổ, vai, hông, tay, chân), đã đối chiếu với bản đo tỉ lệ ngày 11/10.
