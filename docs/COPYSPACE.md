# Mapping chữ vào tranh (copy space + điểm neo)

> **Phạm vi hiện tại: chỉ bìa truyện** (chốt 15/10). Script bìa: `scripts/covers.py`, mẫu 93 bìa đã Approve ở `mapping/covers/`. Phần trang ruột bên dưới giữ làm tham khảo, `covers.py` dùng lại bộ đo độ bận của `copyspace.py`.

## Bìa truyện

```bash
python3 scripts/covers.py --status Approve     # -> out/covers/covers.json + overlay/
python3 scripts/covers.py --all                 # mọi sách dạng ảnh trang (3.311 cuốn)
```

1. Mỗi bìa đo độ bận trên lưới 24×24 như trang ruột.
2. Bìa gom theo khổ: `wide` (≈2.09, StoryWeaver), `square` (1.0, African Storybook), `landscape`, `portrait`; lệch quá 8% thành khổ riêng.
3. **Vị trí tên cố định của khổ** (`formats[].title_slot`): thử mọi dải trên/dưới và cột trái/phải đủ chứa tên dài điển hình (bách phân vị 75 độ dài tên trong khổ) ở chữ Hán 56px + pinyin 20px khi bìa rộng 1194px; lấy dải trống ở nhiều bìa nhất (hoà thì ưu tiên giữa).
4. Từng bìa (`covers[].title_slot`): luôn đặt ở vị trí cố định của khổ. `calm` = tỉ lệ ô trống của bìa đó tại vị trí ấy; `scrim` = `null` (≥90% trống, tương phản ≥4.5), `cream`/`forest` nền mờ (≥50%), `panel-onart` (còn lại). `alt_slot` = chỗ trống riêng của bìa đủ đặt tên, nếu có.
5. Tên lấy theo thứ tự: chữ trên trang bìa → `translation.title_zh` → `title` nếu là chữ Hán → tên tiếng Anh (`title_source: title_en`, độ dài ước lượng 1.4 chữ/từ).

Giới hạn: bìa đã in sẵn tên trong tranh (vd. "Lory Dory", "The Moon and The Cap") chưa được nhận ra; cần lọc tay hoặc thêm OCR.

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
