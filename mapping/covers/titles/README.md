# Tên truyện đã thiết kế

Bỏ PNG nền trong suốt vào thư mục này, **tên file = mã sách** (vd `SW-266338.png`), cỡ theo cột `design_w × design_h`
và số dòng theo cột `lines` trong `../title_sheet.csv`.

Mỗi lần có PNG mới được đẩy lên, GitHub Actions (`.github/workflows/compose-titles.yml`) tự:
1. ghép từng PNG vào đúng khung của bìa cùng mã (`scripts/compose_titles.py compose`);
2. cập nhật `../title_map.json` (vị trí đã đặt, app dùng file này) và `../compose_report.md`;
3. đính kèm ảnh bìa đã ghép để xem trong mục Artifacts của lần chạy, kèm báo cáo trong Summary.
