---
name: TongHua Land
description: Gamified Chinese graded-reading iPad app for Vietnamese kids 5–12. Forest storybook world, one warm lantern button.
colors:
  forest: "#0E4A3A"
  forest-ink2: "#4A675E"
  lantern: "#FF8F45"
  cream: "#FDF9F0"
  paper: "#F7F3EA"
  card: "#FFFFFF"
  gold: "#F5C542"
  leaf: "#CDEBC0"
  lotus: "#BE3F67"
  glow: "#FFD27A"
  night: "#10261F"
  mint-ghost: "#BDDBA7"
typography:
  display:
    fontFamily: "Grandstander, ui-rounded, system-ui, sans-serif"
    fontSize: "44px"
    fontWeight: 800
    lineHeight: 1.15
  headline:
    fontFamily: "Grandstander, ui-rounded, system-ui, sans-serif"
    fontSize: "32px"
    fontWeight: 800
    lineHeight: 1.15
  title:
    fontFamily: "Grandstander, ui-rounded, system-ui, sans-serif"
    fontSize: "24px"
    fontWeight: 700
    lineHeight: 1.2
  body:
    fontFamily: "Lexend, system-ui, sans-serif"
    fontSize: "18px"
    fontWeight: 400
    lineHeight: 1.5
  body-strong:
    fontFamily: "Lexend, system-ui, sans-serif"
    fontSize: "18px"
    fontWeight: 600
    lineHeight: 1.5
  label:
    fontFamily: "Lexend, system-ui, sans-serif"
    fontSize: "14px"
    fontWeight: 600
    lineHeight: 1.3
  pinyin:
    fontFamily: "Lexend, system-ui, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.3
  hanzi-reader:
    fontFamily: "Noto Sans SC, PingFang SC, Hiragino Sans GB, sans-serif"
    fontSize: "44px"
    fontWeight: 500
    lineHeight: 1.35
rounded:
  sm: "12px"
  md: "16px"
  lg: "24px"
  xl: "28px"
  pill: "999px"
  hand-lg: "30px 22px 28px 24px / 24px 30px 22px 28px"
  hand-md: "24px 18px 22px 20px / 20px 24px 18px 22px"
  hand-sm: "18px 12px 16px 13px / 13px 18px 12px 16px"
  hand-round: "52% 48% 50% 46% / 48% 52% 46% 50%"
  hand-modal: "28px 20px 26px 22px / 22px 28px 20px 26px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "32px"
  xxl: "48px"
components:
  button-primary:
    backgroundColor: "{colors.lantern}"
    textColor: "{colors.forest}"
    typography: "{typography.headline}"
    rounded: "{rounded.hand-lg}"
    padding: "0 32px"
    height: "60px"
  button-secondary:
    backgroundColor: "{colors.cream}"
    textColor: "{colors.forest}"
    typography: "{typography.title}"
    rounded: "{rounded.hand-md}"
    padding: "0 24px"
    height: "48px"
  icon-button-onart:
    backgroundColor: "{colors.cream}"
    textColor: "{colors.forest}"
    rounded: "{rounded.hand-round}"
    size: "48px"
  title-onart:
    textColor: "{colors.cream}"
    typography: "{typography.headline}"
  panel-onart:
    backgroundColor: "{colors.card}"
    textColor: "{colors.forest}"
    typography: "{typography.body}"
    rounded: "{rounded.lg}"
    padding: "16px 24px"
  card-book:
    backgroundColor: "{colors.card}"
    textColor: "{colors.forest}"
    rounded: "{rounded.lg}"
    padding: "12px"
  card-selected:
    backgroundColor: "{colors.forest}"
    textColor: "{colors.cream}"
    rounded: "{rounded.lg}"
    padding: "16px"
  tab-active:
    backgroundColor: "{colors.forest}"
    textColor: "{colors.cream}"
    typography: "{typography.label}"
    rounded: "{rounded.hand-md}"
    height: "44px"
  chip-learned:
    backgroundColor: "{colors.leaf}"
    textColor: "{colors.forest}"
    typography: "{typography.label}"
    rounded: "{rounded.hand-sm}"
    height: "36px"
  chip-review:
    backgroundColor: "{colors.card}"
    textColor: "{colors.forest}"
    typography: "{typography.label}"
    rounded: "{rounded.hand-sm}"
    height: "36px"
  chip-new:
    backgroundColor: "{colors.lotus}"
    textColor: "{colors.card}"
    typography: "{typography.label}"
    rounded: "{rounded.hand-sm}"
    height: "36px"
  currency-pill:
    backgroundColor: "{colors.card}"
    textColor: "{colors.forest}"
    typography: "{typography.body-strong}"
    rounded: "{rounded.hand-md}"
    height: "44px"
  modal-reward:
    backgroundColor: "{colors.card}"
    textColor: "{colors.forest}"
    rounded: "{rounded.hand-modal}"
    padding: "24px"
  input-name:
    backgroundColor: "{colors.card}"
    textColor: "{colors.forest}"
    typography: "{typography.title}"
    rounded: "{rounded.md}"
    height: "56px"
  quiz-answer:
    backgroundColor: "{colors.card}"
    textColor: "{colors.forest}"
    rounded: "{rounded.md}"
    height: "56px"
  quiz-answer-selected:
    backgroundColor: "{colors.cream}"
    textColor: "{colors.forest}"
    rounded: "{rounded.md}"
    height: "56px"
  word-highlight:
    backgroundColor: "{colors.glow}"
    textColor: "{colors.forest}"
    rounded: "{rounded.sm}"
---

<!-- LOCKED 29 Sep 2026 (Step 0, v13.4 hi-fi pipeline). Decisions by Yennie: SQ hi-fi direction (forest world), Grandstander + Lexend, CTA "C" (lantern = the one action, forest = structure), C1 title on art for short lines, 85% white panel for long lines, graphical flat 2D, custom icons (drawn XP star + bánh cam). Supersedes: Lantern & Mist brand book names, old indigo/lime files, Tò He Pop, Fredoka/Baloo 2 type spec, SQ's Stitch fonts (Manrope/Epilogue/Plus Jakarta/Nunito). Comparison page: ref/font-cta-compare.html. Shape language picked per element 29 Sep in ref/shape-compare.html: D hand-drawn (primary, secondary, icon button, tabs, chips, reward popup, currency pill) · B sticker (book card, name input, quiz answer) · A soft (companion pick card, long-text panel). -->

# Design System: TongHua Land

## Overview

**Creative North Star: "The Lost Story Map"**

Bé opens great-grandparents' old map and walks into a hand-drawn forest storybook. Every screen is a page of that map: the illustrated land fills the frame, and the interface sits lightly on top of it like ink notes on paper, never like a software panel dropped over a picture. The world is Vietnamese; Chinese is the language bé reads.

One warm light guides the child. The lantern-orange button is the only warm call to action on any screen, so a five-year-old who can't read yet learns one rule: *warm means tap here*. Deep forest green holds everything else together (navigation, selected states, outlines, text), borrowing the tone of the art so the chrome recedes and the story stays in front. Cream and white carry words.

The system is flat and graphical: flat fills, clean coloured outlines, no gradients, no 3D. Things bé presses look hand-drawn: corners that are each a little different, a slight tilt, a hard offset shadow, like the Grandstander letters and Hǔhǔ's own line. Things bé reads look like sturdy stickers (book cards, answers, name field). Only two soft surfaces exist, the companion pick card and the long-text panel, so they feel like a quiet layer over the art.

**Key Characteristics:**
- Illustrated land as the ground of every child screen; UI floats on it.
- One lantern button per screen. Forest green for all structure.
- Short lines sit directly on the art (C1); long lines sit in a light 85% white panel.
- Grandstander (hand-drawn, warm) for voice; Lexend (built for early readers) for reading.
- Graphical flat 2D everywhere: characters, scenes, icons, UI.
- Drawn icons only. The XP star and the bánh cam are illustrated objects, not emoji.

## Colors

A forest-and-lantern palette: deep green structure, one warm action colour, cream for words, and three small state colours that always travel with an icon or text.

### Primary
- **Đèn Lồng · Lantern** (#FF8F45): the one primary action per screen ("Tiếp tục", "Truyện tiếp theo", "Bắt đầu"). Always forest text, 2px forest outline, hard forest shadow. Never text colour, never a background area, never on two buttons at once. Contrast: forest on lantern 4.50:1 (AA; label is large bold text).

### Secondary
- **Rừng Đậm · Forest** (#0E4A3A): all text on light grounds, icons, outlines, active tab, selected card fill, header strips, the stroke around on-art titles. Forest on paper 9.21:1, cream on forest 9.70:1.
- **Rêu Nhạt · Forest Ink 2** (#4A675E): secondary text, captions, locked-state labels. 5.59:1 on paper, 6.19:1 on white.

### Tertiary (state + reward, always paired with an icon or word)
- **Vàng · Gold** (#F5C542): the XP star and the bánh cam coin fill, level milestones. Always an illustrated object with a forest outline. Never a button, never a fill behind text blocks.
- **Lá · Leaf** (#CDEBC0): learned / correct / mastered. Always with ✓. Forest on leaf 7.89:1.
- **Sen · Lotus** (#BE3F67): rare attention chip ("Mới", "Đến hạn hôm nay"). White text 5.13:1. Max one per screen.
- **Ánh Đèn · Glow** (#FFD27A): new-word highlight in the reader, a companion's warm aura in celebrations. Forest on glow 7.16:1.
- **Hồn Bạc Hà · Mint Ghost** (#BDDBA7): the small mint wisps that float around every companion (2–3 each). Illustration only.

### Neutral
- **Kem · Cream** (#FDF9F0): fill of on-art titles, secondary button and on-art icon buttons. The "paper" of the map.
- **Giấy · Paper** (#F7F3EA): page ground only where there is no illustration (parent area, settings, long forms).
- **Mây · Card** (#FFFFFF): cards, sheets, long-text panel (at 85% on art).
- **Đêm · Night** (#10261F): ground for night lands (Vịnh Nuốt Trăng, Vực Ngân Nguyệt) and bedtime. Cream on night 15.15:1, lantern on night 7.03:1.

### Named Rules
**The One Lantern Rule.** Exactly one lantern-orange element per screen, and it is the primary action. If a screen seems to need two, one of them is secondary (cream + forest outline).

**The Warm Means Tap Rule.** Warm colour on an interactive element means "tap here". Gold is reward, not action: it never appears on a button.

**The No-Red Rule.** No red anywhere in the kid UI. A miss is never coloured as failure; it is a white "Ôn lại sau" chip with text.

**The Art-Stays-Art Rule.** Land palettes (the illustrated worlds) live only inside illustrations. They never colour buttons, text or chips. Land backgrounds follow `ref/PROMPTS-MASTER.md` (2 states per land: chưa sáng / đã sáng).

## Typography

**Display Font:** Grandstander (with ui-rounded, system-ui)
**Body Font:** Lexend (with system-ui)
**Hanzi Font:** Noto Sans SC (with PingFang SC on iPad)

**Character:** Grandstander is hand-drawn and slightly uneven, like a title lettered onto a storybook map. Lexend was designed to reduce reading strain for early readers, and stays calm and wide under Vietnamese diacritics. Both render ẩ ễ ộ ừ ỡ ặ cleanly at tight line-height (checked in ref/font-cta-compare.html).

### Hierarchy
- **Display** (Grandstander 800, 44px, 1.15): land names, level-up and stamp moments ("Rừng Ngàn Mắt"), big XP numbers.
- **Headline** (Grandstander 800, 32px, 1.15): on-art screen titles (C1), primary button label (22–24px on the button).
- **Title** (Grandstander 700, 24px, 1.2): card titles, book titles, sheet titles, secondary button label.
- **Body** (Lexend 400, 18px, 1.5): companion lines in the long-text panel, instructions, descriptions. Max ~55ch. 18px is the floor for child-facing reading text.
- **Body Strong** (Lexend 600, 18px): emphasis inside body, currency numbers (tabular figures).
- **Label** (Lexend 600, 14px, 1.3): chips, tab labels, small metadata ("Cấp 3", "Trang 3 / 12"). Never smaller than 14px on child screens.
- **Pinyin** (Lexend 400, 16px): above hanzi in the reader, forest-ink2.
- **Hanzi reader** (Noto Sans SC 500, 44px, 1.35): story text. Tapped/new word gets the glow highlight.

### Named Rules
**The Two-Voice Rule.** Grandstander speaks (titles, buttons, celebrations); Lexend explains (anything longer than one line). Never set a paragraph in Grandstander. Never set a button in Lexend.

**The Stitch-Font Ban.** Manrope, Epilogue, Plus Jakarta Sans, Nunito, Quicksand, Inter, Fredoka never appear. Any Stitch/Figma frame carrying them is re-set before hand-off.

## Layout

### Screen layout lock (founder lo-fi, 1 Oct)
- **Top-left:** tab row (4 giấy dó tokens hanging from one bamboo pole, labels under; active = forest token, Bí Kíp due = lotus wax seal).
- **Top-right:** search strip · VIE/CN toggle · settings paper disc.
- **Bottom:** full-width paper status bar: avatar + "Bé: {tên}" · Cấp + bamboo XP bar (gold fill) · bánh cam · từ đã học. Stats are written on the paper (icon + number + word, ink-dot divider); no boxes inside the bar.
- **Primary CTA:** bottom-centre, just above the status bar.
- **Companion:** bottom-left on open ground, ~260 pt tall at 820.
- Reference builds: `Claude outputs/key-screens-v5-ipad/`.

### UI kit = "Lost Story Map" (giấy dó + bamboo), founder 1 Oct
Pieces: `ref/ui-kit/pieces/` (prompts + history: `ref/PROMPTS-MASTER.md`). Every piece casts a flat navy shadow (#10143A 43 %, x3 y5, blur 0). Lantern orange appears only on the primary CTA; the background's star lantern stays golden yellow. XP fill stays gold #F5C542 (turquoise tested and rejected). Primary CTA press = corner folds into a dog-ear + page-turn sound (HIFI-PREP I1).

### Icons = C2 cut-paper (founder lock, 1 Oct)
Flat layered cut-paper, no outline, thin deep-navy under-layer as depth, scene palette. Ref `ref/icons/explore/style-C2.webp`; prompts `ref/PROMPTS-MASTER.md` §14. Old v1 icons kept in `ref/icons/_approved-v1-old/` as placeholders only.

### Backgrounds = CRAZY style (founder lock, 1 Oct)
Anchor `ref/bg/explore/C0-crazy-v6-soft-sat15.png`; prompts `ref/PROMPTS-MASTER.md`. Saturated night palette, cut-paper shapes, peeking blob creatures (deep colours, never mint/white = Hǔhǔ's wisps). Supersedes the earlier flat-night style in `ref/PROMPTS-MASTER.md` (land table, magic elements and safe zones there still apply).


iPad landscape, **1180×820 design frame** (iPad / iPad Air points; founder 1 Oct). Backgrounds are generated 3:2 (1536×1024) and centre-cropped; keep key art 8 % from the side edges. Safe margin 32px on child screens, 24px minimum.

Child screens are built in three layers: **art** (full-bleed illustrated land) → **content** (cards, panels, on-art titles) → **action** (one lantern button, usually bottom-centre, 32px above the bottom edge). The top third of every illustration stays calm (sky, canopy, mist) so C1 titles have somewhere to sit; the AI prompt blocks enforce this.

Spacing runs on a 4px base: 4 / 8 / 16 / 24 / 32 / 48. Card grids use 16px gaps (library: 5 columns at 1180). Touch targets: primary kid actions ≥60px tall, everything else ≥44px, with ≥8px between neighbours.

The parent area (PIN) is the only place that drops the art ground for paper #F7F3EA and a denser, list-based layout.

## Elevation & Depth

Flat by default. Depth comes from layering art → panel → button and from **hard offset shadows** (no blur) on things bé presses. Two named exceptions carry a soft shadow: the companion pick card and the long-text panel.

### Shadow Vocabulary
- **Hand press** (`box-shadow: 2px 4px 0 #0E4A3A`): primary button, reward popup (3px 5px), book-free hand-drawn elements. Offset slightly right as well as down, like a hand-inked shadow. On press: translate(2px,4px), shadow 0.
- **Hand small** (`box-shadow: 1px 3px 0 #0E4A3A`): secondary button; `1px 2px 0` on icon buttons.
- **Sticker** (`box-shadow: 0 6px 0 #0E4A3A`): book card; `0 4px 0` on the selected quiz answer.
- **Soft lift** (`box-shadow: 0 10px 30px rgba(0,0,0,.18)`): companion pick card only.
- **Soft panel** (`box-shadow: 0 8px 24px rgba(0,0,0,.12)` + `backdrop-filter: blur(8px)`): long-text panel only.
- **Selected ring** (`box-shadow: 0 0 0 3px #FFD27A`): selected companion card / answer, added on top of its own shadow.

### Named Rules
**The Two Soft Things Rule.** Blur and soft shadows exist on exactly two components: the companion pick card and the long-text panel. Everything else uses a hard, unblurred shadow or none. No gradients anywhere.

## Shapes

Three shape families, each with one job:

- **Hand-drawn (D)** for everything bé presses to act or that celebrates: primary/secondary/icon buttons, tab bar, chips, reward popup, currency pill. Each corner has its own radius (`hand-lg` 30/22/28/24 over 24/30/22/28, `hand-md`, `hand-sm`, `hand-round`, `hand-modal`), 2px forest outline, hard offset shadow. Chips tilt ±1°, the popup is allowed −0.5°. Never pill-perfect circles.
- **Sticker (B)** for content bé chooses or reads: book cards (20px), name input (16px), quiz answers (16px). 2.5px forest outline, straight (no tilt), hard vertical shadow.
- **Soft (A)** for the two quiet surfaces: companion pick card (24px, thumbnail 16px) and long-text panel (24px). No outline.

Small inner elements (word highlight, thumbnails) 12px. Outlines are coloured, never black. Locked items use a **dashed** outline plus one line saying what unlocks them.

### Named Rules
**The Hand-Drawn Action Rule.** If bé taps it to do something, it looks hand-drawn (D). If bé taps it to choose content, it's a sticker (B). If it only sits there to hold words or show a friend, it's soft (A). Never mix two families on one element.

## Components

### Buttons
Chunky, tactile, one warm voice.
- **Shape:** hand-drawn (D). Primary `hand-lg`, secondary `hand-md`, icon `hand-round`.
- **Primary (lantern):** lantern fill, forest Grandstander 800 label 22–24px, 2px forest outline, hand press shadow `2px 4px 0 #0E4A3A`, height 60px, padding 0 32px. One per screen.
- **Press:** translate(2px, 4px), shadow 0, 90–120ms ease-out. Haptic tick on iPad.
- **Map-paper CTA (UI kit v2, 1 Oct):** rests flat (no dog-ear); on press the top-right corner folds into a dog-ear + soft page-turn sound. The page-turn sound is reserved for the primary CTA. Spec: HIFI-PREP I1.
- **Focus-visible:** 3px glow (#FFD27A) ring, 2px offset.
- **Secondary:** cream fill, forest text, 2px forest outline, `1px 3px 0` forest shadow, height 48px ("Quay lại", "Để sau").
- **On-art icon button:** 48×48 hand-round blob, cream at 92%, forest glyph, 2px forest outline, `1px 2px 0` shadow. Back (‹), audio, close. Always top-left for back.
- **Disabled:** never greyed as punishment. Use the locked pattern (dashed outline + unlock line) or hide.

### On-art titles (C1): short lines
- **Use when:** one line, ≤ ~7 words ("Bé chọn bạn đồng hành rồi!", "Rừng Ngàn Mắt đã sáng!").
- **Style:** Grandstander 800, 30–44px, cream fill with a 6px forest stroke painted behind the fill (`-webkit-text-stroke: 6px #0E4A3A; paint-order: stroke fill`), centred in the calm top third.
- **Rule:** if the line wraps to two lines on iPad, it is a long line: use the panel.

### Long-text panel: long lines
- **Use when:** two lines or more: companion explanations, keeper story captions, instructions ("Tên các nơi đã mờ. Bé cùng bạn tìm lại nhé?").
- **Style (soft, A):** white at 85% opacity (`rgba(255,255,255,.85)`), `backdrop-filter: blur(8px)`, soft panel shadow, no outline, 24px radius, 16px 24px padding, forest Lexend 18px/1.5, max ~55ch. Optional small companion head+shoulders (never head-only) at the panel's leading edge when the companion is speaking.
- **Placement:** top or middle third, never covering the companion's face or the lantern button.

### Cards / Containers
- **Book card (sticker, B):** white, 2.5px forest outline, 20px radius, `0 6px 0` forest shadow, 12px padding, cover 16px radius inside. Locked = dashed outline + unlock line, cover at 35%.
- **Companion pick card (soft, A):** 24px radius, no outline, soft lift shadow. Default white; selected = forest fill, cream text, selected ring. Thumbnail 16px radius.
- **Reward popup (hand-drawn, D):** white, 2px forest outline, `hand-modal` radius, `3px 5px 0` forest shadow, 24px padding, may tilt −0.5°. Holds one lantern button.

### Name input (sticker, B)
- White, 2.5px forest outline, 16px radius, 56px tall, Grandstander 700 24px value, Lexend counter ("6 / 12") right-aligned in forest-ink2. Focus: glow ring 3px. Max 12 characters, word filter.

### Quiz answer (sticker, B)
- White, 2.5px forest outline, 16px radius, ≥56px tall, hanzi 24px + Lexend meaning. Selected = cream fill + `0 4px 0` forest shadow + selected ring. After answering: right = leaf + ✓; a miss never turns red, the right answer glows instead.

### Word bar (level progress)
- **Shape:** hand-drawn (D) track, 2px forest outline, 20px tall inside a cream holder.
- **Fill (W2, locked 29 Sep):** gold #F5C542 on a white track with 2px forest outline; gold here = "level milestone". Forest on gold 6.29:1. Holder: cream, `hand-md`, `1px 3px 0` forest shadow. Label "Cấp 2 · 28 / 40 từ" in Lexend 600, forest.

### Chips (status)
- **Shape:** hand-drawn `hand-sm`, 2px forest outline, tilt alternates −1.2° / +1°.
- **Learned:** leaf fill, forest text, ✓ icon. "✓ Đã thuộc"
- **Review later:** white fill, 1.5px forest-ink2 outline, forest text, ↻ icon. "↻ Ôn lại sau"
- **New / due:** lotus fill, white text. "Mới". Max one per screen.
- **Locked:** paper fill, 1.5px dashed forest-ink2, lock icon + unlock line. "🔒 Đọc xong Rừng Ngàn Mắt để mở" (lock is a drawn icon).
- **Level:** paper fill, forest text, "Cấp 3". Never "Level".

### Currency pill
- **Style:** white, `hand-md`, 2px forest outline, 44px tall, drawn icon (24px) + Lexend 600 tabular number. XP uses the drawn gold star; bánh cam uses the drawn bánh cam. Always top-right cluster, XP first.
- **Gain:** number counts up, icon does one small hop. No confetti bursts, no screen shake.

### Navigation (4 tabs)
- **Style:** top-left segmented bar, `hand-md` cream track with 2px forest outline; active tab = forest pill with cream label + icon; inactive = forest-ink2 label + icon on transparent.
- **Tabs:** Kho Tàng Truyện · Bí Kíp · Phiêu Lưu Ký · Sư Phụ. Every tab has a drawn icon and plays its name as audio on first tap for pre-readers.

### Reader word highlight
- **Style:** glow fill behind the tapped/new hanzi, 12px radius, 2px lantern underline inset. Tap → pinyin + meaning + audio sheet.

### Companion (signature)
- **Hǔhǔ 虎虎 (tiger, default guide art):** bipedal, upright. Identity = designer files in `ref/char/benchmark/`; line + brightness = approved set `ref/char/approved/huhu-set1-combined.png` (30 Sep). Colours (bright flat set, founder 30 Sep): fur #F5F4D0 · belly #E0DF96 · dark sage #587E5C (outline, ears, tail tip, dark stripes) · stripe sage #76A27E · iris orange #FA6402 · pupil dark green #1D291F · nose + toe beans #FF630A · cheek tufts #F69934 · mustache smile #3B2A5C · open-mouth inside #B8483E. Thin sage outline, inner lines thinner. **All new images follow `ref/PROMPTS-MASTER.md`.** **Launch gate: only 🟢/🟡 ship; 🟠/🔴 must be fixed** (section 6 of the rules).
- **Eyes (the most-missed feature; check first):** NOT concentric. Thin dark eye outline (#17342A-ish, same dark line as the mouth), cream #F0F1DB eye white, a big orange #DB6729 iris pushed off-centre toward the inner/lower edge so it touches the outline and leaves a cream crescent on the outer side, a dark #17342A pupil also off-centre inside the iris, one or two small lash ticks on the outer edge. Lids (sassy/half-closed) = flat dark sage #697D5D upper lid only. Reference close-up: `ref/char/benchmark/huhu-eyes-closeup.png`. Reject any bullseye (centred ring-in-ring) eye.
- **Signature features (must appear in every pose):** (1) **two small white fangs (nanh)** poking up from the corners of the wide thin mustache smile; (2) **cheek tufts on both sides of the head**, layered orange #F69934 + sage stripes, same shape as the turnaround; (3) large flat round eyes: cream ring, orange iris filling most of the eye, dark pupil, small lash ticks; (4) wavy sage stripes (horizontal waves on the back); (5) round sage ears; (6) thick sage tail with bands; (7) mitten paws with orange toe beans.
- **Wūwū 呜呜 (Sấu Năm Chèo):** teal body #5A9A9E, back #2D6E7E, belly #EDE4C8, outline #1F4F5A, tail spots #D98A5A in random sizes, extra arm (năm chèo) kept. Verify against the illustrator's file.
- **Dūdū 嘟嘟 (Chó Đội Nón):** white fur #FAFAF5, outline + ears/tail/paws burnt orange #C8703F, straw hat #D9B26A, bamboo tube #C9955A. Verify against the illustrator's file.
- **Shared rules:** same eye spec on all three; 2–3 mint ghost wisps (#BDDBA7) float around each; coloured outlines never black; all stand and walk on two legs; only Hǔhǔ is green-striped. Never crop head-only in UI (head + shoulders minimum). Expressions per moment: `companion-cast.md`.
- **Personality:** Hǔhǔ is a little sassy and mischievous; the designer's half-lidded "Not yet" face is on-model and approved (founder, 29 Sep).
- **Rejected outputs:** off-model meme faces (wink, frown), adult-tiger proportions, generic chibi kitten, four-legged walking, 3D/gradient renders.


### Hǔhǔ staging (founder, 1 Oct · option B)
Layout stays as lo-fi: Hǔhǔ in the **left** character zone. The background adapts, not the layout.
1. Hǔhǔ never covers the land's landmark or its warm light (the eye's second stop). If the landmark sits in the left 380 px, **mirror the background** (no text in backgrounds, so flipping is free).
2. Feet on ground (grass or path), never on water, sky or dense bush. Flat contact shadow under the feet: ellipse, forest #0E4A3A at 25–35 %, no blur.
3. Size: 380–420 pt tall in the foreground. Smaller mid-ground only for intro / map scenes.
4. Body and gaze turn toward the content or CTA (right).
5. Paper screens (reader, quiz on veil): Hǔhǔ rises from the bottom edge, cropped at the hips; never floats on paper.
Comparison: `ref/review/huhu-staging-compare.png`.

### Hǔhǔ asset map (stage 1)
| Moment | Asset in `ref/char/` | Status |
|---|---|---|
| Model sheet / on-model reference | `Hú Hú 4 angles in colour.jpeg`, `HÚ HÚ 4 ANGLES FLAT.JPG` | OK |
| Listening (reader, test) | `clean/huhu-listening-clean.png` | Cleaned (toolbar + "OG" removed). Still a screenshot: feet cropped, 704px. Ask designer for source |
| Walking / Home idle / map travel | `Hú Hú walking.jpg` | OK, low-res (375px): needs source file |
| Before a test ("Hehe!") | `gen/v3-hehe-fix.png` (proposed) | v3: benchmark outline + palette, green upper lid, orange iris, peach nose. Needs founder OK + background removal |
| Pass / level-up | `HÚ HÚ PASS.JPG` | Fix: sign says English "PASS" and he holds a round gold coin. Replace the sign with a Vietnamese/no-text sign and the coin with a bánh cam |
| Evolution (Cấp 3, 5) | `gen/huhu-evo-flat-b.png` | Approved pose; still v1 colours: restyle to benchmark palette. Tail slightly translucent |
| Bé fails a test / encouragement ("you can do it") | `Hú Hú you can do it.JPG` (designer) · flat redraw `gen/huhu-youcandoit-flat-b.png` | Designer's pose is for the fail moment, not "before a test". Flat redraw pending approval |
| Missed item / "Còn 1 từ nữa" | `HÚ HÚ NOT YET.JPG` | Approved (sassy personality). Pair with a kind line ("Để tui nghĩ…", "Còn 1 từ nữa thôi!"), never with "Quá dễ!" |
| Return after a gap ("Hả?!") | `gen/v3-surprised.png` (proposed) | v3: GPT pose (founder pick) restyled to benchmark outline + palette |
| Feeding (eating bánh cam) | `gen/v3-eating-b.png` + `gen/v3-eating-c.png` (founder picked both) | v3: restyled to benchmark outline + palette |
| Happy / "Tui biết rồi nha~" | `gen/huhu-proud-a.png` | Approved pose; still v1 colours: restyle to benchmark palette + outline |

Generated 29 Sep with Nano Banana (Higgsfield) from the approved turnaround + cleaned listening image; review page `ref/char/gen/index.html`. Paths above are relative to `ref/char/`. All new poses: generated or drawn from the approved turnaround, bipedal, flat 2D, transparent PNG cut-outs (no white box), head + shoulders minimum.

### Icons
- Custom drawn set: flat fill, 2px forest outline, rounded terminals, 24px grid (32px for tabs). Same line as the characters.
- **XP star:** chunky 5-point star, gold fill, forest outline, small cream highlight dot (flat, not a gradient).
- **Bánh cam:** round golden sesame ball, gold fill with tiny cream sesame dots, forest outline. Must read as bánh cam, not a coin.
- No emoji anywhere in shipped UI (emoji in this spec are shorthand only).

## Do's and Don'ts

### Do:
- **Do** put exactly one lantern button on every child screen, bottom-centre, ≥60px tall.
- **Do** use C1 on-art titles (cream + 6px forest stroke) for one-line titles, and the 85% white panel for anything longer.
- **Do** keep the illustration's top third calm so titles have space.
- **Do** pair every state colour with an icon or word (✓ Đã thuộc, ↻ Ôn lại sau).
- **Do** draw every icon, including the XP star and bánh cam, in the same flat outlined style as the characters.
- **Do** give every nav item an icon and spoken audio for pre-readers.
- **Do** write "Cấp n", "{tên bạn}", "TongHua Land" exactly.
- **Do** keep lantern on night grounds (7.03:1) and a lantern or warm light in frame on every night scene.
- **Do** respect Reduce Motion; no flashing faster than 3 per second.

### Don't:
- **Don't** use emoji as UI icons (SQ's 🍪 📖 🐻 chips get redrawn).
- **Don't** use Manrope, Epilogue, Plus Jakarta Sans, Nunito, Quicksand, Inter or Fredoka.
- **Don't** use soft blurred shadows or glass blur outside the companion pick card and long-text panel; never gradients, grain or 3D.
- **Don't** make buttons or chips perfect pills with even radius (that is the AI default); use the hand-drawn radii.
- **Don't** put white text on lantern (2.27:1), and don't put gold on a button.
- **Don't** use red, "sai", hearts/lives, or a 3-star rating. The star exists only as the XP icon.
- **Don't** default to a flat cream page for child screens; cream/paper is only for the parent area and forms.
- **Don't** put more than one lotus "Mới" chip on a screen.
- **Don't** colour UI with land palettes, and don't place long text straight on the art without the panel.
- **Don't** crop a companion to head-only, show it on four legs, or draw it with teeth, claws or red eyes.
- **Don't** show "Dou Dou", "DouDou" or "Level" in any user-facing string.
