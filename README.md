# sw — App build: Figma layout + GPT visual assets

Project gom 2 luồng làm việc song song:

| Luồng | Mục tiêu | Thư mục |
|---|---|---|
| **1. Figma layout** | Dựng layout / screen trong Figma, adapt từ visual design ChatGPT đã generate | `figma/`, `materials/chatgpt-designs/` |
| **2. GPT visual assets** | Prompt GPT tạo background, items, icon cho app | `prompts/`, `assets/` |

Hai luồng gặp nhau ở `app/` — code app dùng layout từ Figma và asset từ GPT.

## Cấu trúc

```
materials/            # Input gốc bạn gửi (chưa xử lý)
  chatgpt-designs/    # Ảnh design ChatGPT đã generate
  references/         # Moodboard, brief, spec, ghi chú
figma/                # Link file Figma, node IDs, design tokens export
  figma.md
prompts/              # Prompt GPT cho từng loại asset
  backgrounds/
  items/
  ui/
  _template.md
assets/               # Asset đã generate & chọn (output cuối)
  backgrounds/ items/ icons/ ui/
  manifest.json       # Danh sách asset: tên, prompt nguồn, kích thước, trạng thái
docs/                 # Brief, style guide, quyết định thiết kế
app/                  # Source code app (stack chốt sau khi có material)
```

## Quy trình

1. Bỏ material vào `materials/` (design ChatGPT, brief, reference).
2. **Figma**: điền link file vào `figma/figma.md` → dựng/adapt layout trong Figma → export tokens (màu, font, spacing).
3. **Assets**: viết prompt theo `prompts/_template.md` → generate bằng GPT → lưu vào `assets/` và ghi vào `assets/manifest.json`.
4. Upload asset vào Figma để ráp vào layout, rồi implement vào `app/`.

## Trạng thái

- [ ] Nhận đủ material
- [ ] Chốt platform & stack cho `app/`
- [ ] Style guide (`docs/style-guide.md`)
- [ ] Figma file + screen list
- [ ] Asset list + prompt
