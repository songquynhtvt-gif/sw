# Mapping chữ vào tranh (copy space + điểm neo)

> **Phạm vi hiện tại: chỉ bìa truyện** (chốt 15/10). Script bìa: `scripts/covers.py`, mẫu 93 bìa đã Approve ở `mapping/covers/`. Phần trang ruột bên dưới giữ làm tham khảo, `covers.py` dùng lại bộ đo độ bận của `copyspace.py`.

## Bìa truyện

**Rule chính: tên không bao giờ đè lên hình vẽ hay hoạ tiết.** Bìa có hình ở đâu thì tìm chỗ trống khác để đặt tên; panel chỉ dùng để tăng tương phản trên chỗ đã trống, không dùng để che hình.

**File bàn giao cho designer: `mapping/covers/cover_slots.json`** (tạo bằng `python3 scripts/export_slots.py out/covers/covers.json mapping/covers/cover_slots.json`). Chỉ có vị trí khung tên, không có kiểu chữ:
- `templates[]`: vị trí chuẩn dùng chung theo khổ bìa (`<khổ>-top-center`, `-top-left`, `-top-right`, `-bottom-center`, `-bottom-left`, `-bottom-right`), `bbox` [x, y, w, h] tỉ lệ 0..1, gốc trên-trái (trung vị các bìa trong nhóm), `anchor` mép trên căn theo cạnh của vị trí. `covers` = danh sách bìa đặt ĐÚNG vị trí này (nhóm identical, căn một lần cho cả nhóm).
- `covers[]`: `placement` = `identical` (đúng một vị trí chuẩn, `template_id` cho biết vị trí nào) | `shifted` (mọi vị trí chuẩn đều đè hình, dời tới chỗ trống thật khác) | `replace` (bìa in sẵn tên tiếng Anh, khung = vùng tên cũ) | `no_room` (bìa kín hình, `bbox` = chỗ đè ít hình nhất, cần người xem); `bbox` = chỗ trống được dùng (đã nới ngang tới bề rộng khung chung khi vẫn trống), `bbox_px` (px ảnh gốc), `anchor`, `backing` (`none` | `panel`: chỗ trống nhưng màu nền làm chữ kem kém tương phản), `cover_text_flag`, `note` (lý do).

**Nối tên đã thiết kế với bìa** (`scripts/compose_titles.py`), khoá nối là mã sách `id`:
1. `python3 scripts/compose_titles.py sheet mapping/covers/cover_slots.json mapping/covers/title_sheet.csv`: bảng giao việc (mở bằng Excel/Sheets), mỗi bìa một dòng: `file_name` = `<id>.png`, `design_w × design_h` = cỡ tối đa ở khung 1180px, `lines`, `align`, `template_id` (cùng template thì làm theo lô), `check` (no_room / replace / 2_lines / small).
2. Designer xuất PNG nền trong suốt, tên file đúng `<id>.png`, bỏ chung một thư mục.
3. `python3 scripts/compose_titles.py compose mapping/covers/cover_slots.json <thư-mục-png> out/composed/`: đặt từng PNG vào khung của bìa cùng id (thu vừa khung, giữ tỉ lệ, canh theo `anchor.align`, mép trên) → `out/composed/<id>.jpg` + `title_map.json` (vị trí px đã đặt; danh sách bìa thiếu tên và file không khớp id).

```bash
python3 scripts/covers.py --status Approve     # -> out/covers/covers.json + overlay/
python3 scripts/covers.py --all                 # mọi sách dạng ảnh trang (3.311 cuốn)
```

1. Mỗi bìa đo độ bận trên lưới 24×24 như trang ruột (thang thô, đã làm mờ: thấy vật và nhân vật) và đo cạnh hoạ tiết ở thang mịn (ảnh co về rộng 1180px, không làm mờ: thấy cả hoạ tiết nhỏ).
2. Bìa gom theo khổ: `wide` (≈2.09, StoryWeaver), `square` (1.0, African Storybook), `landscape`, `portrait`; lệch quá 8% thành khổ riêng.
3. **Vị trí cố định của khổ** (`formats[].title_slot`), theo rule C1 trong `docs/DESIGN.md` ("centred in the calm top third"): dải trên cùng, cao 1 dòng C1 44px + pinyin + lề 32px, rộng đủ tên dài điển hình (bách phân vị 75) của khổ.
4. **Hộp chữ theo độ dài tên** (`box_sizes`, `length_check`): bề rộng = max(số chữ Hán × cỡ chữ, dòng tên tiếng Anh 16px đo bằng font thật). Thử C1 một dòng 44→30px, rồi panel một dòng 28→24px. Tên ≤ 6 chữ (`SHORT_MAX`) luôn 1 dòng, không bẻ đôi; tên dài hơn mới được chia đều 2 dòng 32→24px. `title_slot.length_check`: `ok` | `small` (1 dòng, < 30px) | `2_lines` | `too_long` (> 16 chữ hoặc 2 dòng vẫn không vừa: cần rút gọn / người xem). Khung tìm ở bước 6 luôn đủ rộng cho cả tên ở cỡ đã chọn.
5. **Chỗ trống** (`art_free`): hộp chữ đặt được khi ≥ 95% diện tích nằm trên ô thô trống (`CALM_MIN`) VÀ ≤ 5% điểm ảnh là cạnh hoạ tiết (gradient màu > 0.12, `EDGE_MAX`). Chữ in sẵn khác trên bìa (tác giả, logo, từ OCR) cũng tính là có hình.
6. **Thứ tự tìm chỗ**: vị trí cố định (giữa trên) → các vị trí chuẩn khác: trái trên, phải trên, giữa dưới, trái dưới, phải dưới (mỗi vị trí thử chữ to trước; `source: fixed | anchor`, `anchor_name`) → dò tự do toàn bìa, bước 12px: phần ba trên, rồi phần ba dưới, rồi dải giữa, chữ to trước, gần vị trí cố định trước (`source: shifted`, `shift_px`) → không còn chỗ trống: chỗ đè ít hình nhất, cỡ nhỏ nhất (`source: no_room`, `covers_art: true`, "cần người xem"). `room_bbox` = hộp nới ngang hai bên tới bề rộng khung chung khi vẫn trống.
7. **Tương phản** (`title_slot.legibility`) trên chỗ đã chọn: chữ kem viền rừng (C1) khi `luma_std` ≤ 0.18 và `pair_contrast_p5` ≥ 3 (ở 95% điểm nền, chữ kem hoặc viền rừng đạt ≥ 3:1); không đạt thì lót panel trắng 85% + blur 8px, chữ rừng. Vì chỗ đã trống nên panel không che hình. `reason` ghi lý do bằng tiếng Việt.
8. **Mapping tạm**: designer sẽ đặt chữ thật sau. Dưới tên Trung có một dòng tên tiếng Anh 16px (`title_en`) để biết truyện gì và tìm được. Nguồn `title_en_source`: `original` (sách tiếng Anh), `source_url` (lấy từ đường dẫn StoryWeaver), `ai_gloss` (đường dẫn chỉ là pinyin, dịch nháp trong `mapping/covers/title_en_gloss.json`), `missing`. Độ rộng chữ đo bằng font thật, nên tên tiếng Anh dài không tràn khung.
9. **Chữ in sẵn trên bìa** (cần `rapidocr-onnxruntime`; `--no-ocr` để bỏ): OCR đọc chữ trên ảnh bìa (`baked_text`). Mỗi dòng (độ tin ≥ 0.5) thuộc tên nếu nằm trong tên tiếng Anh (bỏ hoa thường, khoảng trắng) hoặc giống một đoạn tên ≥ 80%. Các dòng khớp phủ ≥ 60% chữ cái của tên → `cover_text_flag: "title"`, `title_slot.style: "replace"`: designer xoá chữ Anh, đặt tên Trung vào đúng vùng đó (cỡ to nhất vừa vùng, 1–3 dòng). Có chữ khác (tác giả, logo, tên cách điệu OCR đọc không ra) → `cover_text_flag: "text"`, chữ lớn không khớp tên thì `reason` ghi "cần người xem". Không thấy chữ → `"none"`.
10. Tên lấy theo thứ tự: chữ trên trang bìa → `translation.title_zh` → `title` nếu là chữ Hán → tên tiếng Anh (`title_source: title_en`, độ dài ước lượng 1.4 chữ/từ).

Ảnh duyệt trong `overlay/` vẽ tên tiếng Trung thật + pinyin (`title_pinyin`, từ gói `pypinyin`) đúng cỡ, màu, viền hoặc panel, để nhìn được chữ có chìm không.

Giới hạn: chưa nhận diện mặt nhân vật; vật rất mảnh trên nền phẳng (dây, cành nhỏ) có thể lọt qua ngưỡng 5% cạnh. Giới hạn: tên viết tay cách điệu (vd. "Lory Dory") OCR đọc không ra, chỉ được gắn cờ "text" để người xem.

## Trang ruột (tham khảo)

Mục tiêu: với mỗi cuốn trong thư viện pilot (`https://twc.mikademy.vn/pilot.html`), tìm vùng trống trên tranh, xác định vị trí lặp lại giống nhau giữa các trang, chốt điểm neo đặt chữ (hanzi + pinyin) và xuất JSON cố định để app reader dựng trang.

Script trang ruột: `scripts/copyspace.py` (chỉ cần numpy + Pillow).

## Chạy

```bash
python3 scripts/copyspace.py SW-266338                   # 1 cuốn
python3 scripts/copyspace.py --status Approve --all      # hàng loạt theo bộ lọc (chỉ sách dạng "pages")
python3 scripts/copyspace.py --status Approve --no-overlay --workers 8
```

Mặc định ghi vào `out/copyspace/<id>.json`, ảnh tải về cache ở `out/cache/` (đã gitignore). Chạy nhiều cuốn sẽ có thêm `_index.json` tóm tắt.

## Cách máy quyết định

1. **Độ bận**: mỗi ảnh được làm mờ nhẹ, thu nhỏ, đo gradient màu trên lưới 24×24. Ô có gradient < `0.03` là trống (`blank` nếu < `0.008`: giấy trắng / mảng màu phẳng; còn lại `calm`).
2. **Layout**: các trang cùng tỉ lệ khung gom thành một layout; bìa tách riêng.
3. **Vùng ổn định (identical)**: ô trống ở ≥ 80% số trang của layout. Hình chữ nhật lớn nhất trên vùng này (tối thiểu 25% rộng × 10% cao) là vị trí neo cố định.
4. **Chế độ của layout** (giống nhau cho mọi trang trong layout, nên chữ không nhảy chỗ khi lật trang):
   - `overlay`: có vùng ổn định chứa được chữ của ≥ 80% số trang ở cỡ ≥ 85% → đè chữ lên tranh tại đó.
   - `column`: không có → tranh thu vào 60% khung, cột chữ 40% đặt phía nửa tranh trống hơn.
5. Trang lệch khuôn trong layout `overlay` dùng vùng trống riêng của trang, không nữa thì panel nền (`panel-onart`). Trong layout `column`, `alt_overlay` ghi chỗ trống riêng của trang nếu đủ đè chữ, để sau này chọn.

Khung tham chiếu: iPad 11" ngang 1194×834, hanzi 44px (line-height 1.35) + pinyin 16px, padding 16px (theo `docs/DESIGN.md`). Sức chứa và `font_scale` (thấp nhất 0.7) tính trên khung này. Sách tiếng Anh chưa chuyển ngữ ước lượng ~1.4 chữ Hán / từ.

## Schema `copyspace/v1`

| Trường | Ý nghĩa |
|---|---|
| `book` | id, title, author, source, lang, pool, n_pages |
| `params` | ngưỡng đã dùng (để chạy lại ra cùng kết quả) |
| `reference_canvas` | khung tham chiếu và cỡ chữ |
| `layouts[]` | `layout_id`, `kind` (page/cover), `aspect`, `size`, `pages`, `stable_zones[]`, `mode`, `art_rect`, `text_slot` (px trên khung), `column_side`, `edge_blank` |
| `pages[]` | `n`, `kind`, `image` (URL), `size`, `layout_id`, `text`, `text_len`, `text_unit`, `empty_ratio`, `zones[]`, `placement` |
| zone | `id`, `bbox` [x,y,w,h] tỉ lệ 0..1 của ảnh (gốc trên-trái), `position` (top-left…bottom), `anchor` {x,y,align}, `bg` (blank/calm), `bg_rgb`, `busy`, `ink` (#0E4A3A forest / #FDF9F0 cream), `contrast`, `scrim` (null / cream / forest), `capacity_hanzi`, `lines`, `chars_per_line`, `stability` (chỉ vùng ổn định) |
| `placement` | `mode`, `zone_id`, `source` (stable/page/fallback_panel), `text_rect` + `art_rect` (px trên khung), `anchor`, `ink`, `scrim`, `font_scale`, `fits`, `alt_overlay` |

## Giới hạn hiện tại

- Chỉ chạy sách dạng `pages` (3.311/3.908 cuốn). Sách chỉ có PDF (Book Dash, GDL) đã in sẵn chữ vào trang, cần bước riêng.
- Độ bận là đo hình học, không nhận diện mặt/nhân vật; vùng nhỏ cạnh nhân vật có thể vẫn được coi là trống.
