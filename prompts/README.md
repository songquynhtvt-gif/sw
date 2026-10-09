# Prompts

Rules: `docs/PROMPT-RULES-TEAM.md` (team short version). Full log `ref/PROMPTS-MASTER.md`: not in repo yet.

**Do not edit the generated `.md` files by hand.** Edit `specs.json`, then run:
```
python3 scripts/build_prompts.py
```
The script pulls MASTER / NEGATIVE / background / icon templates straight from the rules doc, so a rules update flows into every prompt.

| Folder | Content | Refs to attach (team machine, not in repo) |
|---|---|---|
| `huhu/` | 7 missing stage-1 poses | 4 Hǔhǔ refs, rules §3 |
| `bg/` | C0, C1, C2 · đã sáng + chưa sáng edit | `C0-crazy-v6-soft-sat15.png` |
| `icons/batch1.md` | 7 new C2 cut-paper icons | `c2-sheet-1/2.webp` |
| map | use `docs/HIFI-PREP.md` §G3, output on white per rules §5 | |

Log every run in the Result table of its file (verdict 🟢🟡🟠🔴).
