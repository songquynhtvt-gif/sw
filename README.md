# TongHua Land — hi-fi build (Figma + GPT assets)

App iPad đọc truyện tiếng Trung cho trẻ Việt 5–12 tuổi. Repo này gom 2 luồng:

1. **Figma layout** — dựng design system + 15 screen stage 1, adapt từ visual ChatGPT / Stitch lo-fi → `figma/`
2. **GPT visual assets** — nhân vật (Hǔhǔ), background land, map, icon, UI kit → `prompts/`, `assets/`

**Deadline: 12/10/2026** (HIFI-PREP A0).

## Docs (nguồn chuẩn)
| File | Nội dung |
|---|---|
| `docs/DESIGN.md` | Design system đã lock: màu, font, shape D/B/A, component, Hǔhǔ rules |
| `docs/HIFI-PREP.md` | Kế hoạch Phase A→J, screen list, asset matrix, generation queue |
| `docs/TongHua-Land-Build-Brief-v13.4.html` | Product & engineering brief |

**Còn thiếu (docs có nhắc tới):** `PRODUCT.md` (locked copy, companion lines), `ref/PROMPTS-MASTER.md`, `screen-mapping-rules.html`, `.impeccable/design.json`, `companion-cast.md`.

## Cấu trúc
```
docs/            nguồn chuẩn
figma/           tokens.json (variables), figma.md (link, pages, screen tracker)
prompts/         prompt từng asset (theo PROMPTS-MASTER)
assets/
  char/          benchmark/ (file designer) · gen/ (đang thử) · approved/ · placeholders/
  bg/            chua-sang/ · da-sang/   (C0–C12)
  map/           Bản đồ tổng 3 state
  icons/         C2 cut-paper
  ui-kit/pieces/ giấy dó + bamboo
  story/         art truyện mẫu
  manifest.json  37 asset stage 1 + trạng thái
materials/       input thô: chatgpt-designs/, stitch-layouts/, references/
app/             code (sau hi-fi)
```

## Tiến độ (theo HIFI-PREP)
| Phase | | Status |
|---|---|---|
| 0, A | Brand lock + decisions | ✅ |
| B | Figma foundation (variables, text styles, components) | ⬜ |
| C | Asset matrix | 🟡 `assets/manifest.json` |
| D | Audit Stitch lo-fi | ⬜ cần PNG trong `materials/stitch-layouts/` |
| E | Copy deck | ⬜ cần PRODUCT.md |
| F | 15 screens + states | ⬜ |
| G | Produce assets | ⏸ |
| H–J | Swap, motion/VO, handoff | ⬜ |
