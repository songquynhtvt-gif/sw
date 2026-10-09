# Hǔhǔ gen batch 1 — QA vs DESIGN.md (9 Oct)

All 5: transparent RGBA cut-outs ✓ · bipedal/upright ✓ · 2–3 mint wisps ✓ · sage outline, no black ✓ · flat 2D ✓ · ~800–910 px ✗ (hero needs source ≥1500 px → re-render/upscale before ship) · visible upscale/compression artefacts along outlines.

| File | Candidate slot | Notes | Verdict |
|---|---|---|---|
| huhu-front-idle | front idle (Companion pick) | Fangs ✓, wisps with eyes/no mouth ✓. Pupils sit dead-centre in the iris → bullseye (DESIGN.md: reject; PROMPT-RULES MASTER doesn't require off-centre). Re-render: `prompts/huhu/front-idle.md` | 🟠 per DESIGN.md |
| huhu-wave-greeting | 01-greeting-home | Iris off-centre ✓, fangs ✓, toe beans ✓. Orange "!" marks: fine as accent, but Home already uses lantern CTA — keep marks small. | 🟡 |
| huhu-jump-cheer | 02-levelup-pass / 07-correct | Closed happy eyes (eye spec N/A), fangs ✓. Feet off ground — OK for celebration, needs contact shadow rule exception. | 🟡 |
| huhu-thinking | 06-thinking | Iris off-centre ✓, paw-to-chin pose reads well at 150 pt. | 🟡 |
| huhu-happy-singing | karaoke / happy | Closed eyes, fangs ✓, orange music notes. | 🟡 |

Founder to confirm slot mapping + verdicts; approved ones move to `../approved/` with final names.

Re-checked 9 Oct against docs/PROMPT-RULES-TEAM.md §3: all 5 keep the purple mustache smile + 2 white fangs, wisps have eyes and no mouth, sage outline. Next step for approved poses: single-character re-render ≥1500 px on white (rules §3 step 2).
