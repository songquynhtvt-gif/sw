// TongHua Builder — builds the stage-1 screens on page "01 Screens" from the
// components on "00 Foundation". Runs locally in Figma desktop, so it does not
// count against the Figma MCP rate limit.
//
// Figma desktop → Plugins → Development → Import plugin from manifest…
// → pick figma/plugin/manifest.json → run "TongHua Builder".
// Re-running deletes and rebuilds only the sections it created (name "TH · …").

const W = 1180;
const H = 820;
const GAP = 120;

const R = {
  'hand-lg': [30, 22, 28, 24],
  'hand-md': [24, 18, 22, 20],
  'hand-sm': [18, 12, 16, 13],
};

let V = {};
let TS = {};
let SETS = {};
let SINGLES = {};

async function init() {
  for (const v of await figma.variables.getLocalVariablesAsync('COLOR')) V[v.name] = v;
  for (const s of await figma.getLocalTextStylesAsync()) {
    TS[s.name] = s;
    await figma.loadFontAsync(s.fontName);
  }
  const foundation = figma.root.children.find((p) => p.name === '00 Foundation');
  if (!foundation) throw new Error('Page "00 Foundation" not found');
  await foundation.loadAsync();
  for (const n of foundation.children) {
    if (n.type === 'COMPONENT_SET') SETS[n.name] = n;
    if (n.type === 'COMPONENT') SINGLES[n.name] = n;
  }
}

// ---------- primitives ----------
function paint(k, opacity = 1) {
  if (!V[k]) throw new Error('Missing color variable ' + k);
  return figma.variables.setBoundVariableForPaint(
    { type: 'SOLID', color: { r: 0, g: 0, b: 0 }, opacity },
    'color',
    V[k]
  );
}
function fill(n, k, o = 1) { n.fills = [paint(k, o)]; }
function stroke(n, k, w = 2, dash) {
  n.strokes = [paint(k)];
  n.strokeWeight = w;
  n.strokeAlign = 'INSIDE';
  if (dash) n.dashPattern = dash;
}
function radii(n, [tl, tr, br, bl]) {
  n.topLeftRadius = tl; n.topRightRadius = tr; n.bottomRightRadius = br; n.bottomLeftRadius = bl;
}

async function text(parent, chars, style, color = 'forest', x = 0, y = 0, width) {
  const t = figma.createText();
  await t.setTextStyleIdAsync(TS[style].id);
  t.characters = chars;
  fill(t, color);
  if (width) { t.textAutoResize = 'HEIGHT'; t.resize(width, t.height); }
  parent.appendChild(t);
  t.x = x; t.y = y;
  return t;
}

function rect(parent, name, x, y, w, h, color, opacity = 1) {
  const r = figma.createRectangle();
  r.name = name; r.resize(w, h); fill(r, color, opacity);
  parent.appendChild(r); r.x = x; r.y = y;
  return r;
}

function hstack(parent, name, x, y, gap = 16) {
  const f = figma.createFrame();
  f.name = name; f.layoutMode = 'HORIZONTAL';
  f.primaryAxisSizingMode = 'AUTO'; f.counterAxisSizingMode = 'AUTO';
  f.itemSpacing = gap; f.fills = []; f.counterAxisAlignItems = 'CENTER';
  parent.appendChild(f); f.x = x; f.y = y;
  return f;
}

// Instance of a variant ("Button/Primary", {State: 'Default'}) or a single component.
function inst(name, props = {}) {
  if (SINGLES[name]) return SINGLES[name].createInstance();
  const set = SETS[name];
  if (!set) throw new Error('Component not found: ' + name);
  const want = Object.entries(props).map(([k, v]) => k + '=' + v);
  const variant = set.children.find((c) => want.every((p) => c.name.split(', ').includes(p))) || set.defaultVariant;
  return variant.createInstance();
}

// Replace the n-th text inside an instance.
function setText(node, value, index = 0) {
  const ts = node.findAll((n) => n.type === 'TEXT');
  if (ts[index]) ts[index].characters = value;
  return node;
}

function place(parent, node, x, y) {
  parent.appendChild(node); node.x = x; node.y = y; return node;
}

// ---------- screen chrome ----------
function screen(section, code, title, col, row) {
  const f = figma.createFrame();
  f.name = code + ' · ' + title;
  f.resize(W, H);
  f.clipsContent = true;
  section.appendChild(f);
  f.x = 80 + col * (W + GAP);
  f.y = 120 + row * (H + GAP);
  return f;
}

// Full-bleed land art placeholder. Swap the fill with assets/bg/<state>/<id>.png.
function landBg(f, id, state = 'da-sang') {
  const r = rect(f, 'bg/' + state + '/' + id, 0, 0, W, H, 'night');
  // calm top third + stage hint so layout can be judged before art lands
  rect(f, 'guide/calm-top-third (delete with art)', 0, 0, W, Math.round(H * 0.3), 'forest', 0.35);
  rect(f, 'guide/stage (delete with art)', Math.round(W * 0.06), Math.round(H * 0.62), Math.round(W * 0.3), 8, 'leaf', 0.5);
  return r;
}
function paperBg(f) { return rect(f, 'bg/paper', 0, 0, W, H, 'paper'); }
function veil(f) { return rect(f, 'veil/cream-75', 0, 0, W, H, 'cream', 0.75); }

function huhu(f, size, x, y, name) {
  const s = inst('Slot/Huhu', { Size: size });
  s.name = 'huhu/' + name;
  return place(f, s, x, y);
}

function primary(f, label, y = H - 88 - 60) {
  const b = setText(inst('Button/Primary', { State: 'Default' }), label);
  place(f, b, 0, y);
  b.x = Math.round((W - b.width) / 2);
  return b;
}

function backButton(f) { return place(f, inst('IconButton/OnArt', { Icon: 'Back' }), 32, 24); }

function title(f, chars, y = 72) {
  const t = setText(inst('Title/OnArt'), chars);
  place(f, t, 0, y);
  t.x = Math.round((W - t.width) / 2);
  return t;
}

function panel(f, chars, x, y) { return place(f, setText(inst('Panel/LongText'), chars), x, y); }

function tabBar(f, active = 0) {
  const t = place(f, inst('TabBar'), 32, 24);
  // the component ships with tab 0 active; mark the intended one in the layer name
  t.name = 'TabBar (active: ' + ['Kho Tàng Truyện', 'Bí Kíp', 'Phiêu Lưu Ký', 'Sư Phụ'][active] + ')';
  return t;
}

async function topRight(f) {
  const g = hstack(f, 'top-right', 0, 28, 12);
  const search = figma.createFrame();
  search.name = 'search-strip'; search.resize(180, 44); fill(search, 'card'); stroke(search, 'forest', 2); radii(search, R['hand-md']);
  g.appendChild(search);
  const toggle = figma.createFrame();
  toggle.name = 'toggle VIE/CN'; toggle.resize(96, 44); fill(toggle, 'cream'); stroke(toggle, 'forest', 2); radii(toggle, R['hand-md']);
  g.appendChild(toggle);
  await text(toggle, 'VIE · CN', 'label', 'forest', 18, 12);
  const disc = figma.createEllipse();
  disc.name = 'settings-disc'; disc.resize(44, 44); fill(disc, 'cream'); stroke(disc, 'forest', 2);
  g.appendChild(disc);
  g.x = W - 32 - g.width;
  return g;
}

// Bottom paper status bar (layout lock 1 Oct): avatar + name · Cấp + XP bar · bánh cam · từ đã học
async function statusBar(f) {
  const bar = figma.createFrame();
  bar.name = 'status-bar';
  bar.resize(W, 64); fill(bar, 'paper'); stroke(bar, 'forest', 2);
  bar.layoutMode = 'HORIZONTAL'; bar.primaryAxisSizingMode = 'FIXED'; bar.counterAxisSizingMode = 'FIXED';
  bar.paddingLeft = bar.paddingRight = 32; bar.itemSpacing = 24; bar.counterAxisAlignItems = 'CENTER';
  f.appendChild(bar); bar.x = 0; bar.y = H - 64;
  const av = figma.createEllipse(); av.name = 'avatar'; av.resize(40, 40); fill(av, 'mint-ghost'); stroke(av, 'forest', 2); bar.appendChild(av);
  const items = ['Bé: An', '•', 'Cấp 2', null, '•', '45 bánh cam', '•', '28 từ đã học'];
  for (const it of items) {
    if (it === null) {
      const track = figma.createFrame(); track.name = 'xp-bar (bamboo)'; track.resize(180, 14);
      fill(track, 'card'); stroke(track, 'forest', 2); track.cornerRadius = 7; track.clipsContent = true;
      const fl = figma.createRectangle(); fl.resize(126, 14); fill(fl, 'gold'); track.appendChild(fl);
      bar.appendChild(track);
      continue;
    }
    const t = figma.createText(); await t.setTextStyleIdAsync(TS[it === '•' ? 'label' : 'body-strong'].id);
    t.characters = it; fill(t, it === '•' ? 'forest-ink2' : 'forest'); bar.appendChild(t);
  }
  return bar;
}

async function kidChrome(f, active = 0) {
  tabBar(f, active);
  await topRight(f);
  await statusBar(f);
}

// ---------- screens ----------
const FLOWS = [
  ['01 Onboarding', [
    ['OB', 'Consent', async (f) => {
      paperBg(f);
      await text(f, 'Trước khi bắt đầu', 'headline', 'forest', 96, 96);
      await text(f, 'Phụ huynh vui lòng đọc và đồng ý', 'title', 'forest-ink2', 96, 148);
      const card = rect(f, 'consent-card', 96, 210, 988, 360, 'card'); card.cornerRadius = 24;
      await text(f, '• Giọng đọc của bé chỉ dùng để chấm phát âm, không lưu để huấn luyện.\n• Bài xếp lớp giúp chọn cấp phù hợp. Cấp không bao giờ tụt.\n• Không quảng cáo, không bán xu bằng tiền thật.', 'body', 'forest', 128, 242, 900);
      place(f, setText(inst('Button/Secondary', { State: 'Default' }), 'Để sau'), 96, H - 120);
      primary(f, 'Đồng ý và tiếp tục', H - 128);
    }],
    ['HS-05', 'Parent questionnaire 1/5', async (f) => {
      paperBg(f);
      backButton(f);
      await text(f, 'Câu 1 / 5', 'label', 'forest-ink2', 96, 96);
      await text(f, 'Bé đã học tiếng Trung bao lâu rồi?', 'headline', 'forest', 96, 124, 900);
      const opts = ['Chưa học bao giờ', 'Dưới 6 tháng', '6 tháng – 1 năm', 'Trên 1 năm'];
      for (let i = 0; i < opts.length; i++) {
        const a = setText(inst('QuizAnswer', { State: i === 1 ? 'Selected' : 'Default' }), '', 0);
        setText(a, opts[i], 1);
        a.findAll((n) => n.type === 'TEXT')[0].visible = false;
        place(f, a, 96 + (i % 2) * 500, 240 + Math.floor(i / 2) * 96);
      }
      primary(f, 'Tiếp tục', H - 128);
    }],
    ['C1-pick', 'Companion pick', async (f) => {
      landBg(f, 'C0-nha-nho-ben-doi', 'chua-sang');
      title(f, 'Chọn bạn đồng hành nha!');
      const names = ['Hǔhǔ 虎虎', 'Wūwū 呜呜', 'Dūdū 嘟嘟'];
      const row = hstack(f, 'cards', 0, 200, 32);
      for (let i = 0; i < 3; i++) row.appendChild(setText(inst('Card/CompanionPick', { State: i === 0 ? 'Selected' : 'Default' }), names[i]));
      row.x = Math.round((W - row.width) / 2);
      primary(f, 'Chọn bạn này', H - 128);
    }],
    ['C1-name', 'Name your companion', async (f) => {
      landBg(f, 'C0-nha-nho-ben-doi', 'chua-sang');
      backButton(f);
      huhu(f, 'Hero', 60, H - 420 - 40, '01-greeting-home');
      panel(f, 'Bé muốn gọi tui là gì? Đặt cho tui một cái tên thật xinh nha!', 480, 160);
      place(f, inst('Input/Name', { State: 'Typing' }), 520, 330);
      primary(f, 'Xong rồi!', H - 128);
    }],
    ['PT-02', 'Placement question', async (f) => {
      landBg(f, 'C0-nha-nho-ben-doi', 'chua-sang');
      veil(f);
      await text(f, 'Câu 5', 'label', 'forest-ink2', 96, 40);
      await text(f, 'Chữ nào là “con mèo”?', 'headline', 'forest', 96, 72);
      const hz = ['猫', '狗', '鸟', '鱼'];
      for (let i = 0; i < 4; i++) {
        const a = setText(inst('QuizAnswer', { State: 'Default' }), hz[i], 0);
        a.findAll((n) => n.type === 'TEXT')[1].visible = false;
        place(f, a, 260 + (i % 2) * 360, 220 + Math.floor(i / 2) * 110);
      }
      huhu(f, 'Corner', 40, H - 150, '06-thinking');
      primary(f, 'Tiếp tục', H - 128);
    }],
    ['PT-07', 'Map found', async (f) => {
      rect(f, 'bg/map-mo (Bản đồ tổng · mờ)', 0, 0, W, H, 'night');
      title(f, 'Tìm thấy bản đồ!');
      huhu(f, 'Hero', 60, H - 420 - 40, 'found-the-map');
      panel(f, 'Bản đồ của ông bà cố nè! Tên các nơi đã mờ hết rồi. Bé cùng tui đi tìm lại nhé?', 480, 200);
      primary(f, 'Bắt đầu', H - 128);
    }],
  ]],
  ['02 Home + Read', [
    ['KT', 'Home (Hang ổ)', async (f) => {
      landBg(f, 'C2-rung-ngan-mat', 'da-sang');
      await kidChrome(f, 0);
      huhu(f, 'Hero', 60, H - 64 - 420 - 8, '01-greeting-home');
      panel(f, 'Tui nhớ bé quá! Hôm nay mình đọc truyện gì đây?', 520, 220);
      primary(f, 'Truyện tiếp theo', H - 64 - 24 - 60);
    }],
    ['KT-02', 'Library', async (f) => {
      landBg(f, 'C2-rung-ngan-mat', 'da-sang');
      rect(f, 'dim', 0, 0, W, H, 'night', 0.45);
      await kidChrome(f, 0);
      const grid = figma.createFrame();
      grid.name = 'book-grid (5 cols, 16 gap)'; grid.fills = [];
      grid.layoutMode = 'HORIZONTAL'; grid.layoutWrap = 'WRAP';
      grid.itemSpacing = 16; grid.counterAxisSpacing = 16;
      f.appendChild(grid); grid.resize(W - 64, 100); grid.x = 32; grid.y = 100;
      grid.primaryAxisSizingMode = 'FIXED'; grid.counterAxisSizingMode = 'AUTO';
      const states = ['New', 'Default', 'Default', 'Default', 'Locked', 'Default', 'Default', 'Locked', 'Locked', 'Locked'];
      for (const s of states) {
        const b = inst('Card/Book', { State: s });
        grid.appendChild(b);
        b.rescale(0.88);
      }
      huhu(f, 'HeadShoulders', W - 100, H - 64 - 72, '01-greeting-home (head+shoulders)');
    }],
    ['KT-05', 'Story cover', async (f) => {
      rect(f, 'bg/story-cover-art', 0, 0, W, H, 'night');
      backButton(f);
      title(f, 'Hổ con đi chợ');
      place(f, inst('Chip', { Type: 'Level' }), 548, 140).rotation = 1;
      primary(f, 'Đọc truyện', H - 128);
    }],
    ['KT-06', 'Reader + tap-word', async (f) => {
      paperBg(f);
      backButton(f);
      place(f, inst('IconButton/OnArt', { Icon: 'Audio' }), W - 80, 24);
      const art = rect(f, 'story-art (page 3)', 96, 88, W - 192, 360, 'mint-ghost'); art.cornerRadius = 24;
      await text(f, 'xiǎo  māo    zài    chī    yú', 'pinyin', 'forest-ink2', 300, 476);
      const hl = rect(f, 'word-highlight (glow)', 334, 500, 120, 64, 'glow'); hl.cornerRadius = 12;
      await text(f, '小猫在吃鱼。', 'hanzi', 'forest', 300, 500);
      const sheet = figma.createFrame();
      sheet.name = 'tap-word sheet'; sheet.resize(300, 150); fill(sheet, 'card'); stroke(sheet, 'forest', 2); radii(sheet, R['hand-md']);
      f.appendChild(sheet); sheet.x = 720; sheet.y = 470;
      await text(sheet, '猫  māo', 'title', 'forest', 20, 16);
      await text(sheet, 'con mèo', 'body', 'forest', 20, 56);
      place(sheet, setText(inst('Button/Secondary', { State: 'Default' }), '+ Bí Kíp'), 20, 92);
      await text(f, 'Trang 3 / 12', 'label', 'forest-ink2', 96, H - 60);
      huhu(f, 'Corner', 0, H - 150, 'listening').x = 0;
      primary(f, 'Trang tiếp', H - 100);
    }],
    ['KT-quiz', 'Quiz', async (f) => {
      landBg(f, 'C2-rung-ngan-mat', 'da-sang');
      veil(f);
      backButton(f);
      await text(f, 'Câu 2 / 4', 'label', 'forest-ink2', 96, 92);
      await text(f, 'Bạn mèo đang ăn gì?', 'headline', 'forest', 96, 120);
      const st = ['Default', 'Selected', 'Default', 'Default'];
      const opts = [['鱼', 'con cá'], ['米饭', 'cơm'], ['苹果', 'quả táo'], ['面包', 'bánh mì']];
      for (let i = 0; i < 4; i++) {
        const a = inst('QuizAnswer', { State: st[i] });
        setText(a, opts[i][0], 0); setText(a, opts[i][1], 1);
        place(f, a, 260 + (i % 2) * 360, 230 + Math.floor(i / 2) * 110);
      }
      huhu(f, 'Corner', 40, H - 150, '06-thinking');
      primary(f, 'Kiểm tra', H - 128);
    }],
    ['KT-result', 'Quiz result', async (f) => {
      landBg(f, 'C2-rung-ngan-mat', 'da-sang');
      rect(f, 'dim', 0, 0, W, H, 'night', 0.35);
      const p = inst('Popup/Reward');
      setText(p, '3 từ mới! +30 XP', 0); setText(p, '+10 bánh cam vì đọc xong truyện mới', 1); setText(p, 'Về nhà', 2);
      place(f, p, 0, 120); p.x = Math.round((W - p.width) / 2);
      const chips = hstack(f, 'chips', 0, 640, 12);
      const c1 = inst('Chip', { Type: 'Learned' }); chips.appendChild(c1); c1.rotation = -1.2;
      const c2 = inst('Chip', { Type: 'Review' }); chips.appendChild(c2); c2.rotation = 1;
      chips.x = Math.round((W - chips.width) / 2);
    }],
  ]],
  ['03 Feed', [
    ['FEED-01', 'Nuôi lớn', async (f) => {
      landBg(f, 'C2-rung-ngan-mat', 'da-sang');
      await kidChrome(f, 1);
      huhu(f, 'Hero', 60, H - 64 - 420 - 8, 'eating-banh-cam');
      panel(f, 'Nghe nè! Bánh nào là “con mèo”?', 520, 120);
      place(f, inst('IconButton/OnArt', { Icon: 'Audio' }), 560, 210);
      for (let i = 0; i < 2; i++) {
        const b = figma.createEllipse();
        b.name = 'answer/banh-cam-' + (i + 1) + ' (tap target ≥ 120)'; b.resize(150, 150);
        fill(b, 'gold'); stroke(b, 'forest', 3); f.appendChild(b); b.x = 560 + i * 220; b.y = 300;
        await text(f, i ? '狗' : '猫', 'hanzi', 'forest', 610 + i * 220, 345);
      }
      const bowl = place(f, inst('WordBar'), 560, 500);
      setText(bowl, 'Bát: 4 / 15', 0);
    }],
  ]],
  ['04 Level', [
    ['LV-popup', 'Level-up popup on Home', async (f) => {
      landBg(f, 'C2-rung-ngan-mat', 'da-sang');
      await kidChrome(f, 0);
      rect(f, 'dim', 0, 0, W, H - 64, 'night', 0.35);
      const p = inst('Popup/Reward');
      setText(p, 'Thanh từ đầy rồi!', 0); setText(p, 'Làm thử thách 5 câu để tới vùng đất mới nha.', 1); setText(p, 'Làm thử thách', 2);
      place(f, p, 0, 110); p.x = Math.round((W - p.width) / 2);
    }],
    ['LV-test', 'Level test', async (f) => {
      landBg(f, 'C2-rung-ngan-mat', 'da-sang');
      veil(f);
      await text(f, 'Thử thách · Câu 2 / 5', 'label', 'forest-ink2', 96, 92);
      await text(f, 'Chữ nào là “ngày mai”?', 'headline', 'forest', 96, 120);
      const hz = ['明天', '今天', '昨天', '星期'];
      for (let i = 0; i < 4; i++) {
        const a = inst('QuizAnswer', { State: i === 0 ? 'MissedShowsRight' : 'Default' });
        setText(a, hz[i], 0); a.findAll((n) => n.type === 'TEXT')[1].visible = false;
        place(f, a, 260 + (i % 2) * 360, 230 + Math.floor(i / 2) * 110);
      }
      huhu(f, 'Corner', 40, H - 150, '05-miss');
      panel(f, 'Còn 1 từ nữa thôi!', 700, 500);
      primary(f, 'Tiếp tục', H - 128);
    }],
    ['LV-result', 'Test result', async (f) => {
      landBg(f, 'C3-ben-nam-dong', 'da-sang');
      const p = inst('Popup/Reward');
      setText(p, 'Bé vượt cấp rồi!', 0); setText(p, 'Bến Năm Dòng đã sáng! +50 bánh cam', 1); setText(p, 'Đóng dấu hộ chiếu', 2);
      place(f, p, 0, 110); p.x = Math.round((W - p.width) / 2);
    }],
  ]],
  ['05 Map', [
    ['PL', 'Phiêu Lưu Ký map + land popup', async (f) => {
      rect(f, 'bg/map-dang-mo (Bản đồ tổng)', 0, 0, W, H, 'night');
      await kidChrome(f, 2);
      for (let i = 0; i < 13; i++) {
        const pin = figma.createEllipse(); pin.name = 'land-pin/C' + i; pin.resize(36, 36);
        fill(pin, i <= 2 ? 'gold' : 'cream', i <= 2 ? 1 : 0.4); stroke(pin, 'forest', 2);
        f.appendChild(pin); pin.x = 120 + i * 72; pin.y = 560 - Math.round(Math.sin(i / 2) * 120) - i * 22;
      }
      const pop = figma.createFrame();
      pop.name = 'PL-03 land popup'; pop.resize(420, 330); fill(pop, 'card'); stroke(pop, 'forest', 2); radii(pop, R['hand-md']);
      f.appendChild(pop); pop.x = W - 420 - 48; pop.y = 110;
      await text(pop, 'Rừng Ngàn Mắt', 'title', 'forest', 24, 20);
      await text(pop, 'Keeper Hổ Tinh: “Ở rừng này, ngàn con mắt luôn dõi theo người lạc đường…”', 'body', 'forest', 24, 60, 372);
      place(pop, inst('WordBar'), 24, 170);
      place(pop, setText(inst('Button/Secondary', { State: 'Default' }), 'Chơi'), 24, 258);
    }],
    ['PL-07', 'Hộ Chiếu stamp', async (f) => {
      paperBg(f);
      backButton(f);
      await text(f, 'Hộ Chiếu Phiêu Lưu', 'display', 'forest', 96, 80);
      const stamp = figma.createEllipse(); stamp.name = 'stamp/C2 (drops + 1 bounce, 500ms)'; stamp.resize(260, 260);
      stamp.fills = []; stroke(stamp, 'lotus', 6); f.appendChild(stamp); stamp.x = 460; stamp.y = 200; stamp.rotation = -8;
      await text(f, 'Rừng Ngàn Mắt', 'title', 'lotus', 505, 310);
      huhu(f, 'Popup', 120, H - 260, '07-correct');
      primary(f, 'Tiếp tục', H - 128);
    }],
  ]],
];

async function run() {
  await init();
  const page = figma.root.children.find((p) => p.name === '01 Screens');
  if (!page) throw new Error('Page "01 Screens" not found');
  await figma.setCurrentPageAsync(page);
  for (const n of [...page.children]) if (n.name.startsWith('TH · ')) n.remove();

  let y = 0;
  const report = [];
  for (const [flow, screens] of FLOWS) {
    const sec = figma.createSection();
    sec.name = 'TH · ' + flow;
    page.appendChild(sec);
    sec.x = 0; sec.y = y;
    sec.resizeWithoutConstraints(80 + screens.length * (W + GAP), 120 + H + 120);
    for (let i = 0; i < screens.length; i++) {
      const [code, name, build] = screens[i];
      const f = screen(sec, code, name, i, 0);
      try { await build(f); report.push('✓ ' + code); }
      catch (e) { report.push('✗ ' + code + ': ' + e.message); }
    }
    y += sec.height + 200;
  }
  figma.viewport.scrollAndZoomIntoView(page.children);
  return report;
}

run()
  .then((r) => figma.closePlugin(r.filter((x) => x.startsWith('✗')).length ? r.join(' · ') : 'Built ' + r.length + ' screens'))
  .catch((e) => figma.closePlugin('Error: ' + e.message));
