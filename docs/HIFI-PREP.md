# TongHua Land · Hi-fi prep & step-by-step guide

v1 · 30 Sep 2026. Everything left between "brand locked" (Step 0) and "hi-fi stage 1 handed off". Work top to bottom; each step says **who** does it, **input**, **output**, and **done when**.

Sources: `PRODUCT.md`, `DESIGN.md`, `ref/PROMPTS-MASTER.md`, `ref/PROMPTS-MASTER.md`, Build Brief v13.4 §14 (screen inventory).
Launch gate for every asset and screen: **only 🟢 / 🟡 ship; 🟠 / 🔴 must be fixed.**

**Who:** 🧑 = you (founder/designer) · 🤖 = Claude · 🎨 = AI image tool (Higgsfield) · 👩‍🎨 = illustrator.

---

## Progress board

| Phase | What | Status |
|---|---|---|
| 0 | Brand lock (PRODUCT, DESIGN, fonts, CTA, shapes, Hǔhǔ rules, BG rules) | ✅ done |
| A | Decisions that block everything else | ✅ done 30/09 |
| B | Figma foundation (variables, text styles, components) | ⬜ |
| C | Asset matrix + generation queue | 🟡 Hǔhǔ poses chosen (sheet v2, 16 + designer listening); full-res renders wait for credits |
| D | Audit Stitch lo-fi against v13.4 | ⬜ |
| E | Copy deck | ⬜ |
| F | Build stage-1 screens with placeholders + all states | ⬜ |
| G | Produce assets (characters, backgrounds, map, icons, props) | ⏸ paused until Higgsfield top-up · placeholders ready in `char/placeholders/` |
| H | Swap assets in + QA pass | ⬜ |
| I | Motion + voice-over specs | ⬜ |
| J | Handoff package | ⬜ |

---

## Phase A · Decisions ✅ (answered 30/09)

| # | Decision |
|---|---|
| A0 | **Deadline 12/10/2026.** All screens except Sư Phụ. Reuse backgrounds and poses across screens (see `screen-mapping-rules.html` §6). |
| A1 | Hand-drawn (D) shapes in Figma = **4 different corner radii + 0.5–1° rotation**. Code keeps the real CSS elliptical radii from `design.json`. |
| A2 | **Home background = current land** (changes on level-up). No separate den. |
| A3 | Scope = **every MVP screen except Sư Phụ**. Parent area = **plain paper #F7F3EA**, no illustration. |
| A3b | Land backgrounds = **2 states: chưa sáng / đã sáng** (no day/dusk/night). |
| A4 | Old PASS image **dropped**; use `approved/02-levelup-pass`. |
| A5 | Tủ đồ stage-1 list (§G5) **approved as is**. |
| A6 | **AI produces and refines all art**, including 🟠 fixes (restyle passes). Launch gate unchanged. |
| A7 | Tab bar **top-left**; lantern button **always bottom-centre**; quiz **2–4 answers** by question type. |
| A9 | Quiz / test / placement background = current land + flat cream veil 75% (no blur). |
| A10 | Home switches to ĐÃ SÁNG **only on the level-up day**; next day it moves to the new land, chưa sáng. |
| A11 | Credits topped up **in batches** (~80 first). |
| A12 | **Sheet first, then singles:** one 12-pose review sheet for Hǔhǔ, one 4-land sheet per background batch; only approved cells get full-res renders. Sheets never ship. |
| A8 | Pass screen copy: title "**Bé vượt cấp rồi!**" + line "**{Tên vùng đất} đã sáng!**". |

## Phase B · Figma foundation

🧑 in Figma (or 🤖 via Figma plugin console if the file is editable; the Figma MCP is on the Starter rate limit).

**B1 · Variables** (source: `DESIGN.md` frontmatter + `.impeccable/design.json`)
1. Create collection `color`: forest, forest-ink2, lantern, cream, paper, card, gold, leaf, lotus, glow, night, mint-ghost. Add Hǔhǔ palette as a separate collection `char/huhu` (fur, belly, sage-dark, sage-stripe, iris, pupil, nose, cheek, mustache, mouth).
2. Collection `radius`: sm 12, md 16, lg 24, xl 28, pill 999 (hand-drawn radii live in the vector components, not here).
3. Collection `space`: 4, 8, 16, 24, 32, 48.

**B2 · Text styles**
| Style | Font | Size / line | Use |
|---|---|---|---|
| display | Grandstander 800 | 44 / 1.15 | land names, level-up |
| headline | Grandstander 800 | 32 / 1.15 | C1 on-art titles |
| title | Grandstander 700 | 24 / 1.2 | card titles, secondary buttons |
| button | Grandstander 800 | 22 / 1 | primary button |
| body | Lexend 400 | 18 / 1.5 | companion lines, instructions |
| body-strong | Lexend 600 | 18 / 1.5 | currency numbers (tabular) |
| label | Lexend 600 | 14 / 1.3 | chips, tabs, metadata |
| pinyin | Lexend 400 | 16 / 1.3 | reader |
| hanzi | Noto Sans SC 500 | 44 / 1.35 | reader |
| title-onart | Grandstander 800 | 30–44, cream fill, 6 px forest stroke **outside** | C1 |

Check: type `ẦU ỬA ỖI ẶNG` in display and headline; no clipping at 1.15.

**B3 · Components** (shape family in brackets, see DESIGN.md → Shapes)
1. Button / primary [D] · secondary [D] · icon-onart [D] — states: default, pressed, focus, disabled-as-locked.
2. Tab bar [D], 4 tabs with icon slot + Bí Kíp 🍡 due badge.
3. Chip [D]: learned, review, new, locked, level.
4. Currency pill [D]: XP, bánh cam.
5. Word bar [D, W2 gold].
6. Reward popup [D] with one primary button slot.
7. Book card [B]: default, new, locked.
8. Quiz answer [B]: default, selected, correct (leaf + ✓), missed-shows-right (glow, never red).
9. Name input [B]: empty, typing, max length.
10. Companion pick card [A]: default, selected.
11. Long-text panel [A], white 85% + blur 8.
12. On-art title (C1) text component.
13. Hǔhǔ slot: a frame per size in §C3 holding the placeholder image, so swapping art is one click.

**Done when:** every component has all states and uses only variables (no raw hex).

---

## Phase C · Asset matrix + generation queue

### C1 · Screens

Scope changed (A3): **all MVP screens except Sư Phụ** by 12/10. The 15 below are the build order; stage-2 list is now also in scope except Sư Phụ. Screen-by-screen background + pose rules: `screen-mapping-rules.html`.

#### Build order (golden path first)

| # | Screen | Code | Why in stage 1 |
|---|---|---|---|
| 1 | Consent (parent, before mic/placement) | OB | legal gate |
| 2 | Parent questionnaire (5 questions) | HS-05…09 | onboarding |
| 3 | Companion pick | Pt 06 / C1 | first meeting |
| 4 | Name your companion | C1 | |
| 5 | Placement intro + 1 question + result | PT-01/02/05 | |
| 6 | Map found | PT-07 | North Star moment |
| 7 | Home (Hang ổ) | KT | daily entry |
| 8 | Library | KT-02 | |
| 9 | Story cover / start | KT-05 | |
| 10 | Reader + tap-word popup | KT-06 | core |
| 11 | Quiz + quiz result | KT | core |
| 12 | Nuôi lớn (feeding) | FEED-01 | daily review |
| 13 | Level-up popup on Home → Level test → result | LV | progression |
| 14 | Phiêu Lưu Ký map + land popup | PL + PL-03 | world |
| 15 | Hộ Chiếu stamp | PL-07 | reward end |

Then: karaoke, evolution cutscene, Tủ đồ, Sân chơi games, Flashcard, Học ngữ âm, Sổ nhãn dán, parent dashboard, settings, report sheet, paywall. **Sư Phụ: out of scope.**

### C2 · Asset matrix (stage 1)

| Screen | Hǔhǔ pose | Background | Icons / props | Status |
|---|---|---|---|---|
| 3 Companion pick | front idle (need) | C0 Nhà Nhỏ Bên Đồi · chưa sáng | — | ⬜ |
| 4 Name | `01-greeting-home` | C0 · chưa sáng | — | placeholder ✅ |
| 5 Placement | `06-thinking` (during), `02-levelup-pass` (result) | plain paper | state icons | placeholder ✅ |
| 6 Map found | **found-the-map (need)** | **Bản đồ tổng · mờ** (need) | old map | ⬜ |
| 7 Home | `01-greeting-home` · `hả-back-after-gap` (need) | current land · đã sáng | XP star, bánh cam, tab icons ×4 | partial |
| 8 Library | small head+shoulders crop of `01` | C2 Rừng Ngàn Mắt or current land, dimmed | lock, new chip | partial |
| 10 Reader | listening (need) in corner | story art (see §G6) | audio, pinyin toggle | ⬜ |
| 11 Quiz | `06-thinking` / `07-correct` / `05-miss` | plain cream | ✓, glow | placeholder ✅ |
| 11 Quiz result | `02-levelup-pass` | current land | XP star, bánh cam | placeholder ✅ |
| 12 Feeding | **eating bánh cam (need)**, bowl-full (need) | current land · đã sáng | bánh cam ×2 (answer buttons), bowl | ⬜ |
| 13 Level-up popup | `03-hehe-before-test` | current land | word bar | placeholder ✅ |
| 13 Level test | `06-thinking` / `05-miss` ("Còn 1 từ nữa") | plain cream | — | placeholder ✅ |
| 13 Test result | `02-levelup-pass` | next land · đã sáng | stamp | placeholder ✅ |
| 14 Map + land popup | — | Bản đồ tổng (3 states) + land thumbnails | ink marks, land pins | ⬜ |
| 15 Passport stamp | `07-correct` | paper | stamp per land (need) | ⬜ |

### C3 · Sizes (design at 1280×800, export @2x)

| Slot | On screen (pt, height) | Export min (px) | Source min |
|---|---|---|---|
| Hero (Home, map found, result) | 420 | 840 | 1500 |
| Popup | 220 | 440 | 1000 |
| Reader corner / quiz | 150 | 300 | 1000 |
| Head + shoulders (library, tab) | 64 | 128 | 1000 |
| Background | 1280×800 | 2560×1600 | 2560 wide |
| Icons | 24–32 | SVG | vector |

### C4 · Generation queue (credits ≈ 2 per image, 2 variants each)

| Batch | Items | Images | Credits |
|---|---|---|---|
| Hǔhǔ missing poses | front idle, found-the-map, hả, listening, eating, bowl-full, sleeping | 14 | ~28 |
| Hǔhǔ re-renders of the 7 approved (to reach ≥1500 px) | 7 | 14 | ~28 |
| Backgrounds stage 1 | C0, C1, C2 (current land for new users) × chưa/đã sáng | 9 | ~18 |
| Map master | 3 states | 5 | ~10 |
| **Total stage 1** | | ~42 | **~84** |

Backgrounds C3–C12 are also in scope for 12/10 (~40 credits more). Full estimate incl. icons, store items and refine passes ≈ **200 credits** (balance ≈ 8). Top up before Phase G.

---

## Phase D · Audit Stitch lo-fi against v13.4

🤖 can run this if you export each Stitch project's screens as PNG into `layouts/` (Stitch pages need a login, so export is the reliable path).

For every frame, flag:
- [ ] mini-game after the quiz (removed in v13.4)
- [ ] "Level", "Lv", "Dou Dou", "DouDou" in any string
- [ ] stars used as a rating (⭐ 3-star) · star is only the XP icon
- [ ] red colour, "sai", "Wrong", hearts/lives, timers
- [ ] world-lock land names (Làng Nhà Mình, Phố Chợ Xưa, Bến Chợ Nổi, Rừng Thiêng…) → brief §09B names
- [ ] map/feeding shortcuts on Home (brief: none)
- [ ] reward order different from: quiz result → Home → level-up popup → test → result → evolution → stamp
- [ ] emoji used as UI icons
- [ ] Stitch fonts (Manrope, Epilogue, Plus Jakarta, Nunito)
- [ ] two orange buttons on one screen

**Output:** `ref/stitch-audit.md`, one row per frame: code · issue · fix. **Done when:** every stage-1 frame is checked.

---

## Phase E · Copy deck

🤖 drafts, 🧑 approves.
1. One table per stage-1 screen: element · Vietnamese copy · status (🔒 locked from brief / ✏️ draft) · max length.
2. Locked strings come only from `PRODUCT.md` → Locked copy. Everything else is draft and marked.
3. Length test: C1 titles must fit one line in Grandstander 44 at 1280 wide (≈ 28 characters with diacritics); longer → long-text panel.
4. Companion lines per moment from `PRODUCT.md` → Companion lines; use `{tên bạn}` in the deck, "Hǔhǔ" in frames.
5. Parent-area copy in a separate section (more formal "phụ huynh" voice).

**Output:** `ref/copy-deck.md`. **Done when:** no screen has lorem or English placeholder.

---

## Phase F · Build stage-1 screens with placeholders

🧑 in Figma, one page per flow: `01 Onboarding`, `02 Home+Read`, `03 Feed`, `04 Level`, `05 Map`.

1. Frame 1280×800 named with the screen code.
2. Use only Phase B components + Hǔhǔ slot frames with `approved/` placeholders. Name each image layer with the final file name from §C2 so swapping is automatic.
3. For every screen also build these **states** (tick the ones that apply):

| State | Screens |
|---|---|
| first time vs returning | Home, Library, Map |
| returning after a gap (Hǔhǔ "Hả?!") | Home |
| loading | Reader, Quiz, Placement |
| offline (OB-02 pattern) | any network screen |
| locked (dashed + unlock line) | Library, Map, Level test |
| not enough words ("Cho bạn ăn hôm nay để mở thử thách") | Level-up card |
| failed test ("Còn 1 từ nữa") | Level result |
| streak broken / Ngày Ngủ used | Home |
| not enough bánh cam | (stage 2: store, Sân chơi) |
| empty (no due words) | Feeding |

4. Check each screen: one lantern button, top third free on art screens, 60 pt targets, every nav item icon + label.
5. **iPad sizes:** duplicate Home and Reader at 1133×744 (mini), 1194×834 (11"), 1366×1024 (12.9"); set constraints so nothing clips; keep 20 pt clear of the home indicator.

**Done when:** all 15 screens + applicable states exist with placeholders and pass step 4.

---

## Phase G · Produce assets

### G1 · Hǔhǔ poses
Follow `ref/PROMPTS-MASTER.md` exactly (one pose per image, 4 refs, MASTER + NEGATIVE, 2–3 ghost wisps). Queue = §C4 row 1–2.
Then per image: QA §6 → 🧑 hand-fix cheek tufts + line weight → background removal → check edge on dark → save `char/approved/NN-name.png` → update DESIGN.md asset map.

### G2 · Land backgrounds
Follow `ref/PROMPTS-MASTER.md`. Stage 1: C0, C1, C2 (new users start there). Make `chưa sáng` first, `đã sáng` as an edit. Crop 16:10, drop a Hǔhǔ cut-out on top to test the character zone and the C1 title.

### G3 · Map master (Bản đồ tổng) · prompt

Refs: `ref/PROMPTS-MASTER.md` §2 refs 1 and 3, plus 2–3 approved land backgrounds for colour.

```
Create ONE illustration: an old hand-drawn paper map of a Vietnamese folk-tale world, seen from above, for a children's app. Flat graphical 2D, large simple shapes, few details, no gradients, no texture, no grain.

PAPER: aged cream paper #EFE3C4 with a slightly darker flat border #D9C9A0 and a few flat torn-edge notches. No stains, no burn marks.

LANDS: 13 small flat landmark icons placed along one winding dotted ink path from bottom-left (start) to top-right (end): a small house on a hill; a bamboo lane; a round-canopy forest; a river splitting into five streams; a bay with karst rocks and a moon; a tall bamboo grove; a stone-pillar forest; a mountain peak with wind ribbons; a valley of rounded boulders; a moonlit pool between cliffs; an open meadow; tiled rooftops; a round flower garden. Each landmark is a simple flat shape in 2-3 colours from its land palette, about the same size, with clear space around it.

INK: path and outlines in faded ink #4A5A52, hand-drawn dotted line.

STATE: [MỜ = all landmarks faded to 25% ink-only outlines, only the start house in colour | ĐANG MỞ = lands 1..N in colour, the rest faded, the path glows warm #FFD27A up to land N | ĐÃ SÁNG = all in colour, path fully warm]

COMPOSITION: landscape 16:9, generous margins, top 20% calm (title space), no compass rose clutter, no sea monsters, no text, no labels, no numbers.

Do NOT: add characters, animals, people, flags, Chinese or Japanese architecture, text, a compass with letters, 3D, painterly shading, glow halos.
```

Note: the map is the brand's most important image. If two AI rounds don't reach 🟢/🟡, give it to 👩‍🎨 with this prompt as the brief.

### G4 · Icons (vector, you or illustrator)
Stage 1 set: 4 tab icons (Kho Tàng Truyện, Bí Kíp, Phiêu Lưu Ký, Sư Phụ), XP star, bánh cam (3/4 sphere, #D9953B, cream sesame), audio, pinyin toggle, back, close, lock, ✓ learned, ↻ review, bowl, stamp frame. From the review: keep `state-learned`, `state-review`, `state-locked`, `xp-star-solid`; redraw bánh cam; replace Chinese lantern with đèn ông sao or a flat Hội An lantern; keep only one sparkle burst.

### G5 · Tủ đồ stage-1 list (15 items, prices 40 / 80 / 150)
| Type | Items |
|---|---|
| Phụ kiện (40) | nón lá · khăn rằn · nơ bướm · vòng hoa · khăn quàng lá |
| Phụ kiện (80) | áo bà ba mini · đèn ông sao · diều giấy · trống cơm · ba lô gỗ |
| Món khoái khẩu (40) | bánh cam · xôi gấc · chè · bánh bò |
| Giữ chuỗi | Ngày Ngủ (50) · Hồi Sinh Chuỗi (150) |
Remove from the AI item sheet: táo, đào, mochi, há cảo, mì, áo gile, huy chương, cúp, đá quý, vương miện, vé a/b/c, móc khóa đèn lồng.

### G6 · Story illustrations (flag only)
Reader needs one illustration per story page (~890 books for Cấp 0–9). This is a separate content pipeline, not hi-fi. For stage 1, use 1 sample story (5 pages) with art made under `ref/PROMPTS-MASTER.md` + Hǔhǔ rules.

---

## Phase H · Swap assets + QA

1. Replace placeholders by layer name.
2. Per screen run:
   - [ ] launch gate on every asset (0 🟠, 0 🔴)
   - [ ] C1 title readable on this background, both land states
   - [ ] Hǔhǔ in the character zone, not covering the title or the button
   - [ ] one lantern button
   - [ ] contrast AA (text 4.5:1, button edges 3:1)
   - [ ] iPad mini + 12.9" frames still clean
3. 🤖 can run `impeccable critique` + `audit` on an exported HTML/PNG of each flow.

**Done when:** all 15 screens pass.

---

## Phase I · Motion + voice-over specs

**I1 · Motion** (durations from `design.json`; every item needs a Reduce Motion fallback = 150 ms fade)
| Moment | Motion |
|---|---|
| Primary button press (map-paper CTA, founder 1 Oct) | Rest = flat orange giấy dó on its bamboo slat, no dog-ear. On touch-down (0 ms): paper sinks onto the slat (lip hides, translate y+4, 80 ms) + top-right corner folds down into a dog-ear (corner overlay rotates/scales from the corner, 160 ms ease-out) + soft page-turn sound (≤250 ms, −18 dB, respects mute) + haptic tick. On release: navigate after the fold finishes (≤200 ms total). Cancel (finger slides off): corner unfolds, 120 ms. Reduce Motion: no fold, 150 ms fade + sound only |
| Other paper buttons / tabs / tags | sink on the slat/twine y+2, 80 ms; tab switch = soft paper rustle (no page-turn, it belongs to the primary only) |
| Ghost wisps idle | slow float ±6 pt, 3–4 s loop, offset per wisp |
| Hǔhǔ enter | pop 0.9→1.0 + settle, 300 ms |
| XP / bánh cam gain | count-up 600 ms, icon hop once |
| Word bar fill | width ease-out 600 ms |
| Land chưa sáng → đã sáng | mist fades out, warm spots fade in, 900 ms |
| Passport stamp | stamp drops, 1 bounce, 500 ms |
| Evolution (stage 2) | flat rays rotate in, 1.5 s |
Never: shake, flashing > 3/s, confetti bursts.

**I2 · Voice-over script list**
- Tab names ×4, Bí Kíp items ×4 (for pre-readers).
- Hǔhǔ lines per moment (PRODUCT.md table) for stage-1 moments.
- Onboarding map lines, "Còn 1 từ nữa", "Cho bạn ăn hôm nay để mở thử thách", "{land} đã sáng!".
Output: `ref/vo-script.md` with file names (`vo_huhu_correct_01.mp3`).

---

## Phase J · Handoff

- [ ] Figma: 5 flow pages, components, variables, all states, iPad sizes
- [ ] `ref/` docs current: PRODUCT, DESIGN, rules ×2, copy deck, VO script, stitch audit
- [ ] `.impeccable/design.json` regenerated if tokens changed
- [ ] Asset folder: `char/approved/`, `bg/`, `map/`, `icons/` with the naming in §C2
- [ ] Open items listed (stage 2 scope, Wūwū/Dūdū adaptation, story art pipeline)

---

## Open items carried forward
- Wūwū and Dūdū: copy `HUHU-PROMPT-RULES.md` per character after stage 1 (need their benchmark files).
- Colours of Wūwū/Dūdū in DESIGN.md come from the old brand book; verify with the illustrator.
- Draft copy lines (map found, "đã sáng") need founder approval before ship.
- CN land names need the Chinese teacher's approval.
