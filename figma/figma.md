# Figma — TongHua Land

- File URL: _(chưa có — gửi link để Claude làm thẳng trên file)_
- Frame: **1180×820** iPad landscape (DESIGN.md 1 Oct). Thêm 1133×744, 1194×834, 1366×1024 cho Home + Reader.
- Tokens: `figma/tokens.json` → Phase B1 variables.

## Pages
Starter allows only 3 pages, so each flow is a **Section** on `01 Screens`:
- `00 Foundation`: variables, text styles, effect styles, components ✅ (built via MCP 9 Oct)
- `01 Screens`: sections `TH · 01 Onboarding` … `TH · 05 Map` (built by the local plugin)
- `99 Assets`: Hǔhǔ / Dūdū cut-outs, backgrounds

## Starter limits
- The Figma MCP call quota ran out after the foundation build. Screen work moves to the **local plugin** `figma/plugin/`, which has no quota.
- Run it: Figma **desktop** → Plugins → Development → *Import plugin from manifest…* → `figma/plugin/manifest.json` → run **TongHua Builder**. Re-running rebuilds only the `TH · …` sections.

## Built in 00 Foundation
- Variables: `color` (13), `char/huhu` (10), `radius` (5), `space` (6)
- Text styles: display, headline, title, button, body, body-strong, label, pinyin, hanzi (Grandstander / Lexend / Noto Sans SC)
- Effect styles: shadow/hand-press, hand-popup, hand-small, hand-icon, sticker, sticker-sm, soft-lift, soft-panel
- Components: Button/Primary, Button/Secondary, IconButton/OnArt, Chip ×5, CurrencyPill, WordBar, Panel/LongText, Title/OnArt, Card/Book, QuizAnswer ×4, Input/Name, Card/CompanionPick, TabBar, Popup/Reward, Slot/Huhu ×4
- Hand-drawn D = 4 different corner radii (A1). Rotate instances, not components.

## Screens stage 1

| # | Screen | Code | Page | Node ID | Status |
|---|---|---|---|---|---|
| 1 | Consent | OB | 01 | | ⬜ |
| 2 | Parent questionnaire | HS-05…09 | 01 | | ⬜ |
| 3 | Companion pick | Pt 06 / C1 | 01 | | ⬜ |
| 4 | Name your companion | C1 | 01 | | ⬜ |
| 5 | Placement intro / question / result | PT-01/02/05 | 01 | | ⬜ |
| 6 | Map found | PT-07 | 01 | | ⬜ |
| 7 | Home (Hang ổ) | KT | 02 | | ⬜ |
| 8 | Library | KT-02 | 02 | | ⬜ |
| 9 | Story cover | KT-05 | 02 | | ⬜ |
| 10 | Reader + tap-word | KT-06 | 02 | | ⬜ |
| 11 | Quiz + result | KT | 02 | | ⬜ |
| 12 | Nuôi lớn (feeding) | FEED-01 | 03 | | ⬜ |
| 13 | Level-up popup → test → result | LV | 04 | | ⬜ |
| 14 | Phiêu Lưu Ký map + land popup | PL / PL-03 | 05 | | ⬜ |
| 15 | Hộ Chiếu stamp | PL-07 | 05 | | ⬜ |

## Components (Phase B3)
Button primary/secondary/icon-onart [D] · Tab bar [D] · Chip ×5 [D] · Currency pill [D] · Word bar [D] · Reward popup [D] · Book card [B] · Quiz answer [B] · Name input [B] · Companion pick card [A] · Long-text panel [A] · On-art title C1 · Hǔhǔ slots (hero 420 / popup 220 / corner 150 / head 64)
