#!/usr/bin/env python3
"""Fill the templates in docs/PROMPT-RULES-TEAM.md with prompts/specs.json.

Writes one ready-to-paste markdown file per asset under prompts/.
Run: python3 scripts/build_prompts.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RULES = (ROOT / "docs/PROMPT-RULES-TEAM.md").read_text(encoding="utf-8")
SPECS = json.loads((ROOT / "prompts/specs.json").read_text(encoding="utf-8"))
CLOSET = json.loads((ROOT / "prompts/closet/items.json").read_text(encoding="utf-8"))
OUT = ROOT / "prompts"

RIG_LINE = "Arms slightly away from the body, wisps not touching him, eyes open."


def block_after(marker):
    """First fenced code block after the line containing `marker`."""
    start = RULES.index(marker)
    m = re.search(r"```\n(.*?)\n```", RULES[start:], re.S)
    return m.group(1)


HUHU_MASTER = block_after("**MASTER**")
HUHU_NEGATIVE = block_after("**NEGATIVE**")
BG_TEMPLATE = block_after("**Mẫu (dán, điền 4 ô)")
ICON_TEMPLATE = block_after("**Thêm icon mới:**")
ITEM_MASTER = block_after("**ITEM MASTER**")
ITEM_NEGATIVE = block_after("**ITEM NEGATIVE**")
ITEM_SHEET = block_after("**ITEM SHEET**")
SHEET_SIZE = 4


def fence(text):
    return f"```\n{text}\n```"


def write(path, body):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    print("wrote", path.relative_to(ROOT))


def huhu(spec):
    prompt = (
        HUHU_MASTER.replace("[POSE]", spec["pose"])
        .replace("[EXPRESSION]", spec["expression"])
        .replace("[PROP or \"none\"]", spec["prop"])
        .replace("[ACCENT or \"none\"]", spec["accent"])
    )
    if spec.get("rig"):
        prompt += "\n" + RIG_LINE
    return f"""# Hǔhǔ · {spec['id']}

- Slot: {spec['slot']}
- Attach 4 refs in order: `benchmark/huhu-front.jpg` · `benchmark/huhu-eyes-closeup.png` · `approved/huhu-set1-combined.png` · `HÚ HÚ 4 ANGLES FLAT.JPG`
- Output: 1:1, 2K, white bg → post: remove bg, upscale 2× → `assets/char/approved/{spec['id']}.png` (keep `*-source.png`)
- New chat every 3–4 images · max 1–2 edits, otherwise restart from this prompt

## Prompt
{fence(prompt)}

## Negative (always paste)
{fence(HUHU_NEGATIVE)}

## Result
| Run | File | Verdict | Note |
|---|---|---|---|
| | | | |
"""


def bg(spec, layout, states):
    prompt = (
        BG_TEMPLATE.replace("[SCENE — what is in the picture, Vietnamese objects]", spec["scene"])
        .replace("[where, in percent, named as one dark object — a card or title sits there]", layout["calm"])
        .replace("[one flat empty surface, x to y percent wide, top at z percent high, a character stands/sits there]", layout["stage"])
        .replace("[where the details and creatures go]", layout["busy"])
        .replace("[MOOD — 3 to 5 words]", spec["mood"])
    )
    return f"""# Background · {spec['id']}

- Slot: {spec['slot']}
- Attach image 1: `ref/bg/explore/C0-crazy-v6-soft-sat15.png` (style only)
- Output: 1536×1024 → crop 16:10 for the 1180×820 frame, key art ≥8% from side edges
- Layout matches DESIGN.md: tabs top-left, title in calm top third, Hǔhǔ bottom-left on the stage, lantern CTA bottom-centre, status bar along the bottom

## 1 · Đã sáng (base render)
{fence(prompt)}
→ `assets/bg/da-sang/{spec['id']}.png`

## 2 · Chưa sáng (one in-place edit of the result above)
{fence(states['chua-sang'])}
→ `assets/bg/chua-sang/{spec['id']}.png`

## QA (rules §2)
- [ ] no star lantern / Chinese motif (🔴) · no text / people (🔴)
- [ ] calm zone dark enough for a cream card (🟠)
- [ ] stage present (🟠) · no 4-point sparkles (🟠)
- [ ] creatures not mint/white, only in busy zone (🟠)
- [ ] drop a Hǔhǔ cut-out on the stage + C1 title in the top third

## Result
| Run | File | Verdict | Note |
|---|---|---|---|
| | | | |
"""


def icons(items):
    lines = "\n".join(f"- {i}" for i in items)
    prompt = re.sub(r"- \[icon 1.*?\n- \[icon 2 …\]", lines, ICON_TEMPLATE, flags=re.S)
    prompt = prompt.replace("[N]", str(len(items)))
    return f"""# Icons · batch 1 (C2 cut paper)

- Attach images 1–2: `ref/icons/c2-sheet-1.webp`, `ref/icons/c2-sheet-2.webp`
- Already kept from review (HIFI-PREP G4): state-learned, state-review, state-locked, xp-star-solid
- Back / close / tab Kho Tàng Truyện (= the open book): build as vectors in Figma, not here
- Sư Phụ tab: out of scope
- Palette only: #2EC4B6 #6CC36F #8A6BE0 #F07C62 #F7C844 #F5C542 #FBF4E4 #1B2A6B

## Prompt
{fence(prompt)}

## QA (rules §4)
- [ ] no text in icons, no star lantern (🔴)
- [ ] same material as the set: no gloss, 3D or outline (🟠)
- [ ] readable at 32 px (🟠)

→ crop each cell to `assets/icons/<name>.png`, then vectorise for SVG
"""


def item_prompt(item):
    """Full prompt text (master + negative) for one Tủ đồ item."""
    slot = CLOSET["slots"][item["slot"]]
    prompt = (
        ITEM_MASTER.replace("[ITEM]", item["item"])
        .replace("[SLOT]", slot["en"])
        .replace("[COLOURS]", item["colours"])
        .replace("[FIT]", slot["fit"])
    )
    return prompt + "\n\n" + ITEM_NEGATIVE


def sheets():
    """Group the catalogue into ChatGPT sheets of up to 4 items, per wave, in catalogue order.

    Returns [(sheet_id, cols, rows, [items])]; split_sheet.py relies on the same order.
    """
    out = []
    for wave in CLOSET["waves"]:
        items = [i for i in CLOSET["items"] if i["wave"] == wave and i["status"] != "blocked"]
        for k in range(0, len(items), SHEET_SIZE):
            chunk = items[k:k + SHEET_SIZE]
            cols = 1 if len(chunk) == 1 else 2
            rows = (len(chunk) + cols - 1) // cols
            out.append((f"{wave}-{k // SHEET_SIZE + 1}", cols, rows, chunk))
    return out


def sheet_prompt(cols, rows, items):
    lines = "\n".join(f"{n}. {it['item']} ({CLOSET['slots'][it['slot']]['en']}). Colours: {it['colours']}."
                       for n, it in enumerate(items, 1))
    prompt = (
        ITEM_SHEET.replace("[N]", str(len(items)))
        .replace("[COLS]", str(cols))
        .replace("[ROWS]", str(rows))
        .replace("[ITEMS]", lines)
    )
    return prompt + "\n\n" + ITEM_NEGATIVE.replace("draw several items or a sheet; ", "")


def closet_all():
    all_sheets = sheets()
    parts = [f"""# Tủ đồ · toàn bộ kho cho ChatGPT ({sum(len(s[3]) for s in all_sheets)} món, {len(all_sheets)} sheet)

Không cần API key. Mỗi khối dưới đây = 1 ảnh có tối đa 4 món.

1. Mở ChatGPT, **chat mới mỗi 3 sheet**. Dán nguyên 1 khối, chờ ra ảnh.
2. Ảnh lỗi (thiếu món, món dính nhau, có chữ, có bóng navy) → bấm tạo lại, không sửa chồng quá 1–2 lần.
3. Tải ảnh về, đặt tên đúng mã sheet, ví dụ `w3-1.png`, bỏ hết vào `materials/chatgpt-designs/closet/` (hoặc gửi thẳng cho Claude).
4. Cắt + xoá nền + ướm lên Hǔhǔ, một lệnh cho cả thư mục:
   ```
   python3 scripts/split_sheet.py materials/chatgpt-designs/closet/
   ```
   → từng món ở `assets/closet/gen/<id>-v<n>.png`, ảnh ướm ở `assets/closet/fit/`.

File này sinh tự động từ `prompts/closet/items.json` (`python3 scripts/build_prompts.py`), đừng sửa tay.
"""]
    for sid, cols, rows, items in all_sheets:
        names = " · ".join(f"{n}. {it['name']} (`{it['id']}`)" for n, it in enumerate(items, 1))
        parts.append(f"## `{sid}` · {CLOSET['waves'][sid.rsplit('-', 1)[0]]}\n\n{names}\n\n{fence(sheet_prompt(cols, rows, items))}\n")
    return "\n".join(parts)


def closet_wave(wave, items):
    parts = [f"""# Tủ đồ · {CLOSET['waves'][wave]}

- Rules: `docs/PROMPT-RULES-TEAM.md` §7 · catalogue: `prompts/closet/items.json`
- One item per chat message; new chat every 3–4 images
- Output: 1:1, transparent → `assets/closet/gen/<id>-v1.png`; approved → `assets/closet/approved/<id>.png`
- Or run `python3 scripts/gen_closet.py --wave {wave}` (GPT API)
"""]
    for it in items:
        if it["status"] == "blocked":
            parts.append(f"## {it['name']} · `{it['id']}` · BLOCKED\n\n{it.get('note', '')}\n")
            continue
        meta = f"slot {it['slot']} · {it['price']} bánh cam · {it['status']}"
        if it.get("source"):
            meta += f" · from {it['source']}"
        if it.get("note"):
            meta += f" · {it['note']}"
        parts.append(f"## {it['name']} · `{it['id']}`\n\n{meta}\n\n{fence(item_prompt(it))}\n")
    parts.append("## Result\n| Item | Run | File | Verdict | Note |\n|---|---|---|---|---|\n| | | | | |\n")
    return "\n".join(parts)


def main():
    for s in SPECS["huhu"]:
        write(OUT / "huhu" / f"{s['id']}.md", huhu(s))
    for s in SPECS["bg"]:
        write(OUT / "bg" / f"{s['id']}.md", bg(s, SPECS["bg_layout"], SPECS["bg_states"]))
    write(OUT / "icons" / "batch1.md", icons(SPECS["icons_batch1"]))
    for wave in CLOSET["waves"]:
        items = [i for i in CLOSET["items"] if i["wave"] == wave]
        if items:
            write(OUT / "closet" / f"{wave}.md", closet_wave(wave, items))
    write(OUT / "closet" / "ALL-CHATGPT.md", closet_all())


if __name__ == "__main__":
    main()
