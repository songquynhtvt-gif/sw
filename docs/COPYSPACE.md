# Mapping chữ vào tranh (copy space + điểm neo)

> **Phạm vi hiện tại: chỉ bìa truyện** (chốt 15/10). Script bìa: `scripts/covers.py`, mẫu 93 bìa đã Approve ở `mapping/covers/`. Phần trang ruột bên dưới giữ làm tham khảo, `covers.py` dùng lại bộ đo độ bận của `copyspace.py`.

## Bìa truyện

```bash
python3 scripts/covers.py --status Approve     # -> out/covers/covers.json + overlay/
python3 scripts/covers.py --all                 # mọi sách dạng ảnh trang (3.311 cuốn)
```

1. Mỗi bìa đo độ bận trên lưới 24×24 như trang ruột (thang thô, đã làm mờ: thấy vật và nhân vật).
2. Bìa gom theo khổ: `wide` (≈2.09, StoryWeaver), `square` (1.0, African Storybook), `landscape`, `portrait`; lệch quá 8% thành khổ riêng.
3. **Vị trí tên cố định của khổ** (`formats[].title_slot`), theo rule C1 trong `docs/DESIGN.md` ("centred in the calm top third"): dải trên cùng, cao 1 dòng C1 44px + pinyin + lề 32px, rộng đủ tên dài điển hình (bách phân vị 75) của khổ, ở khung 1180px. Đặt giữa; chỉ lệch trái/phải khi giữa trống ở ít bìa hơn hẳn (kém 0.15).
4. **Hộp chữ thật** cho từng tên: C1 một dòng, cỡ 44→30px. Không vừa một dòng thì theo rule là panel (tối đa 2 dòng, 32→24px).
5. **Kiểm tra chữ có chìm không** (`title_slot.legibility`), đo ngay dưới hộp chữ trên ảnh co về rộng 1180px, KHÔNG làm mờ, nên thấy cả hoạ tiết nhỏ ở chỗ nhìn xa tưởng trống. C1 chỉ được dùng khi đủ cả 4:
   - `calm_coarse` ≥ 0.85: ô lưới thô dưới chữ trống (không đè lên vật, nhân vật);
   - `edge_density` ≤ 0.05: tỉ lệ điểm ảnh là cạnh hoạ tiết (gradient màu > 0.12);
   - `luma_std` ≤ 0.18: nền không loang sáng/tối mạnh;
   - `pair_contrast_p5` ≥ 3: ở 95% điểm nền, chữ kem hoặc viền rừng đạt ≥ 3:1.
6. Trượt ở vị trí cố định → dò trong phần ba trên (bước 24px ngang, 12px dọc) tìm chỗ gần nhất đạt cả 4 (`source: shifted`, `shift_px`). Không có → panel trắng 85% + blur 8px, chữ rừng, bọc đúng dòng chữ tại vị trí cố định (`style: panel`). `reason` ghi lý do bằng tiếng Việt.
7. **Mapping tạm**: designer sẽ đặt chữ thật sau. Dưới tên Trung có một dòng tên tiếng Anh 16px (`title_en`) để biết truyện gì và tìm được. Nguồn `title_en_source`: `original` (sách tiếng Anh), `source_url` (lấy từ đường dẫn StoryWeaver), `ai_gloss` (đường dẫn chỉ là pinyin, dịch nháp trong `mapping/covers/title_en_gloss.json`), `missing`. Độ rộng chữ đo bằng font thật, nên tên tiếng Anh dài không tràn khung.
8. Tên lấy theo thứ tự: chữ trên trang bìa → `translation.title_zh` → `title` nếu là chữ Hán → tên tiếng Anh (`title_source: title_en`, độ dài ước lượng 1.4 chữ/từ).

Ảnh duyệt trong `overlay/` vẽ tên tiếng Trung thật + pinyin (`title_pinyin`, từ gói `pypinyin`) đúng cỡ, màu, viền hoặc panel, để nhìn được chữ có chìm không.

Giới hạn: chưa nhận diện mặt nhân vật, nên panel ở vị trí cố định có thể che đầu nhân vật nếu nhân vật chạm mép trên. Giới hạn: bìa đã in sẵn tên trong tranh (vd. "Lory Dory", "The Moon and The Cap") chưa được nhận ra; cần lọc tay hoặc thêm OCR.

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
