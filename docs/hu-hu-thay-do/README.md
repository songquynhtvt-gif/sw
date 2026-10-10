# Thay Đồ: Hǔhǔ, Wuwu, Dudu

Trang: https://claude.ai/artifact/4doA81XFEbPMKieNRZe9qp

Nguồn món: `materials/chatgpt-designs/closet-v3/objects-35.webp` → `assets/closet/v3/items/`.

Dáng gốc:
- Hǔhǔ: `assets/char/gen/huhu-front-idle.png`
- Wuwu: `assets/char/gen/wuwu/wuwu-front-idle.png`
- Dudu: `assets/char/gen/dudu/dudu-front-idle-bamboo.png`. Dudu luôn đội nón lá và cầm gậy tre, nên `scripts/prep_mascots.py` tách hai món này thành món riêng (`dudu-own-hat.png`, `dudu-own-bamboo.png`), rồi vẽ lại đỉnh đầu, tai và nắm tay → `dudu-dressup-base.png`.

Tạo lại:
1. `python3 scripts/prep_mascots.py`
2. `python3 scripts/build_dressup.py` (chỉ một bạn: thêm `wuwu`). Vị trí món viết theo Hǔhǔ trong `CATALOG`; mỗi bạn có khung đầu / cổ / lưng, đường cằm, tay, chân trong `MASCOTS`.
3. Ghép `index.src.html` + `data.json` → `hu-hu-thay-do.html`.
