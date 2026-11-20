// THE FILM — боберштыль: первобытная бензопила на четырёх бобрах.
(function () {
  const U = globalThis.U, G = globalThis.G, S = globalThis.SCORE, Studio = globalThis.Studio;
  const { clamp, lerp, ease } = U;
  const { ev } = S;
  const W = G.W, H = G.H;

  const C = {
    sky1: '#FFF4DC', sky2: '#FBE0B4', sun: '#FFC24A',
    green: '#6FA35A', green2: '#588C46', ground: '#C9A06B', ground2: '#B78C57',
    trunk: '#8A5A33', trunk2: '#6E4526', bark: '#A5713F',
    skin: '#E0A87C', skin2: '#C98C60', hair: '#3E2A1B', tunic: '#C9A15E', tunic2: '#B08A4C',
    beaver: '#8B5A34', beaver2: '#A06B40', strap: '#5E8C3E',
    ink: '#2A2118', cream: '#FFF8EA', accent: '#E07A2A',
  };
  const F = 'Inter';

  const GROUND = 1520;
  const TREE = { x: 910, w: 200, base: GROUND };
  const MAN = { x: 360 };
  const SAW = { x: 610, y: 1010 };

  const fade = (t, t0, d = 0.4) => clamp((t - t0) / d);
  const out = (t, t0, d = 0.3) => 1 - clamp((t - t0) / d);

  function text(ctx, str, x, y, o = {}) {
    G.text(ctx, str, x, y, {
      size: o.size || 48, fam: F, weight: o.weight || 800,
      color: o.color || C.ink, align: o.align || 'center', baseline: 'middle',
      stroke: o.stroke, strokeW: o.strokeW || 0,
    });
  }

  // ---------- фон ----------
  function bg(ctx, t) {
    const g = ctx.createLinearGradient(0, 0, 0, GROUND);
    g.addColorStop(0, C.sky1);
    g.addColorStop(1, C.sky2);
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, W, GROUND);

    // солнце и лучи
    ctx.save();
    for (let i = 0; i < 12; i++) {
      const a = (i / 12) * Math.PI * 2 + t * 0.04;
      G.line(ctx, [[560 + Math.cos(a) * 90, 240 + Math.sin(a) * 90], [560 + Math.cos(a) * 150, 240 + Math.sin(a) * 150]],
        { color: 'rgba(255,200,90,0.35)', lw: 10, seed: 1 + i });
    }
    G.ellipse(ctx, 560, 240, 84, 84, { fill: C.sun, seed: 20 });
    ctx.restore();

    // дальний лес
    for (let i = 0; i < 7; i++) {
      const x = 40 + i * 150;
      const h = 420 + ((i * 71) % 220);
      ctx.save();
      ctx.globalAlpha = 0.28;
      G.rrect(ctx, x, GROUND - h, 40, h, 12, { fill: C.trunk2, seed: 30 + i });
      G.ellipse(ctx, x + 20, GROUND - h - 40, 90, 70, { fill: C.green2, seed: 40 + i });
      ctx.restore();
    }

    // земля
    G.rrect(ctx, 0, GROUND - 40, W, 60, 0, { fill: C.green, seed: 60 });
    ctx.fillStyle = C.ground;
    ctx.fillRect(0, GROUND, W, H - GROUND);
    G.rrect(ctx, 0, GROUND, W, 22, 0, { fill: C.ground2, seed: 61 });
    for (let i = 0; i < 16; i++) {
      const x = 30 + i * 68, h = 22 + ((i * 37) % 34);
      G.line(ctx, [[x, GROUND - 34], [x + 10, GROUND - 34 - h]], { color: C.green2, lw: 7, seed: 70 + i });
    }
    // опилки на земле
    for (let i = 0; i < 18; i++) {
      const x = 700 + ((i * 53) % 340);
      const y = GROUND + 6 + ((i * 31) % 40);
      G.ellipse(ctx, x, y, 9, 4, { fill: '#E8D2A8', seed: 90 + i });
    }
  }

  // ---------- дерево ----------
  function tree(ctx, t) {
    const fallK = clamp((t - ev.fall) / 1.15);
    const ang = -ease.inCubic(fallK) * 0.95;
    const shake = t > ev.build && t < ev.fall ? Math.sin(t * 26) * 3 : 0;

    ctx.save();
    ctx.translate(TREE.x, TREE.base);
    ctx.rotate(ang);
    ctx.translate(-TREE.x, -TREE.base);

    // ствол
    G.poly(ctx, [[TREE.x - TREE.w / 2 + shake, 60], [TREE.x + TREE.w / 2 + shake, 60],
      [TREE.x + TREE.w / 2 + 40, TREE.base], [TREE.x - TREE.w / 2 - 40, TREE.base]],
      { fill: C.trunk, seed: 100 });
    // кора
    for (let i = 0; i < 7; i++) {
      const y = 180 + i * 170;
      G.rrect(ctx, TREE.x - TREE.w / 2 + 30 + shake, y, 22, 110, 8, { fill: C.bark, seed: 101 + i });
      G.rrect(ctx, TREE.x + TREE.w / 2 - 60 + shake, y + 40, 20, 90, 8, { fill: C.bark, seed: 111 + i });
    }
    // зарубка
    // пропил
    G.rrect(ctx, TREE.x - TREE.w / 2 - 6, 956, 30, 96, 8,
      { fill: '#E8D2A8', seed: 130, stroke: '#6B4526', strokeW: 4 });

    // ветки
    G.line(ctx, [[TREE.x + 20, 300], [TREE.x + 250, 190]], { color: C.trunk, lw: 34, seed: 131 });
    G.line(ctx, [[TREE.x - 40, 220], [TREE.x - 240, 120]], { color: C.trunk, lw: 28, seed: 132 });
    // листва
    G.ellipse(ctx, TREE.x + 40, 80, 240, 150, { fill: C.green, seed: 133 });
    G.ellipse(ctx, TREE.x - 150, 150, 180, 120, { fill: C.green2, seed: 134 });
    G.ellipse(ctx, TREE.x + 240, 160, 160, 110, { fill: C.green, seed: 135 });
    ctx.restore();
  }

  // ---------- бобёр ----------
  function beaver(ctx, x, y, s, t, i) {
    const wob = Math.sin(t * 12 + i) * 2;
    ctx.save();
    ctx.translate(x, y + wob);
    ctx.scale(s, s);
    // хвост
    G.ellipse(ctx, -46, 10, 34, 18, { fill: '#6B4526', seed: 140 + i });
    // тело
    G.ellipse(ctx, 0, 0, 46, 30, { fill: C.beaver, seed: 141 + i, stroke: '#5E3B1E', strokeW: 4 });
    // голова
    G.ellipse(ctx, 40, -12, 26, 24, { fill: C.beaver2, seed: 142 + i, stroke: '#5E3B1E', strokeW: 4 });
    // уши
    G.ellipse(ctx, 34, -30, 8, 8, { fill: C.beaver, seed: 143 + i });
    G.ellipse(ctx, 48, -32, 8, 8, { fill: C.beaver, seed: 144 + i });
    // глаз
    G.ellipse(ctx, 46, -18, 4, 4, { fill: C.ink, seed: 145 + i });
    // нос
    G.ellipse(ctx, 62, -8, 7, 5, { fill: '#3E2A1B', seed: 146 + i });
    // зубы
    G.rrect(ctx, 56, 0, 8, 12, 2, { fill: '#FFF6E2', seed: 147 + i });
    ctx.restore();
  }

  // ---------- боберштыль ----------
  function saw(ctx, t) {
    const vib = t > ev.beavers ? Math.sin(t * 34) * 4 : 0;
    const x = SAW.x + vib, y = SAW.y;

    // ручка
    G.line(ctx, [[x - 150, y - 40], [x - 190, y + 10], [x - 150, y + 60]], { color: '#6B4526', lw: 20, seed: 160 });
    // бревно-корпус
    G.rrect(ctx, x - 150, y - 46, 300, 92, 40, { fill: '#9A6A3C', seed: 161, stroke: '#5E3E22', strokeW: 5 });
    G.rrect(ctx, x - 140, y - 34, 280, 30, 15, { fill: '#B07E48', seed: 162 });
    // ремни
    for (const dx of [-80, 0, 80]) {
      G.rrect(ctx, x + dx - 8, y - 54, 16, 108, 6, { fill: C.strap, seed: 163 + dx });
    }
    // бобры
    beaver(ctx, x - 104, y - 78, 1.15, t, 1);
    beaver(ctx, x - 4, y - 88, 1.2, t, 2);
    beaver(ctx, x + 96, y - 80, 1.15, t, 3);

    // опилки летят
    if (t > ev.build) {
      for (let i = 0; i < 14; i++) {
        const ph = ((t * 2.6 + i * 0.17) % 1);
        const sx = x + 150;
        const sy = y - 10 + Math.sin(i * 3) * 20;
        const px = sx + ph * 190 + Math.sin(i) * 20;
        const py = sy - ph * 120 + ph * ph * 240;
        ctx.save();
        ctx.globalAlpha = 1 - ph;
        G.ellipse(ctx, px, py, 8, 4, { fill: '#EFD9AC', seed: 170 + i });
        ctx.restore();
      }
    }
  }

  // ---------- руки изобретателя ----------
  function hands(ctx, t) {
    const push = t > ev.build && t < ev.fall ? Math.sin(t * 8) * 6 : 0;
    const hy = SAW.y;
    const kx = SAW.x - 196 + push;

    // рукав у левого края
    G.rrect(ctx, -60, 980, 210, 190, 60, { fill: '#C9A15E', seed: 179 });
    G.rrect(ctx, 120, 1010, 40, 130, 16, { fill: '#B08A4C', seed: 178 });

    // верхняя рука
    G.line(ctx, [[90, 1040], [300, 1010], [kx - 10, hy - 34]], { color: C.skin, lw: 52, seed: 180 });
    // нижняя рука
    G.line(ctx, [[110, 1160], [330, 1110], [kx, hy + 46]], { color: C.skin2, lw: 50, seed: 181 });

    // кулаки
    G.ellipse(ctx, kx - 6, hy - 30, 32, 28, { fill: C.skin, seed: 182 });
    G.ellipse(ctx, kx + 2, hy + 44, 32, 28, { fill: C.skin2, seed: 183 });
    for (let i = 0; i < 3; i++) {
      G.rrect(ctx, kx + 4, hy + 32 - i * 15, 42, 11, 5, { fill: C.skin, seed: 184 + i });
    }
    G.rrect(ctx, kx - 40, hy - 48, 18, 36, 8, { fill: '#8B6A3F', seed: 188 });
  }

  // ---------- пыль от падения ----------
  function dust(ctx, t) {
    const k = clamp((t - ev.fall - 0.7) / 1.2);
    if (k <= 0) return;
    ctx.save();
    for (let i = 0; i < 10; i++) {
      const x = 420 + i * 62 + Math.sin(i * 2) * 20;
      const y = GROUND - 20 - k * (30 + (i % 3) * 40);
      ctx.globalAlpha = (1 - k) * 0.45;
      G.ellipse(ctx, x, y, 70 + k * 60, 26 + k * 26, { fill: '#E7D3B0', seed: 200 + i });
    }
    ctx.restore();
  }

  // ---------- надписи ----------
  function chips(ctx, t) {
    // подпись «4 бобра»
    if (t < ev.beavers || t > ev.build + 0.2) return;
    const a = fade(t, ev.beavers, 0.35) * out(t, ev.build - 0.1, 0.25);
    if (a <= 0.01) return;
    ctx.save();
    ctx.globalAlpha = a;
    G.rrect(ctx, 70, 180, 470, 122, 26, { fill: 'rgba(255,248,234,0.94)', seed: 210, stroke: C.ink, strokeW: 5 });
    text(ctx, '4 БОБРА', 105, 222, { size: 46, align: 'left' });
    text(ctx, 'вместо двигателя', 105, 272, { size: 30, align: 'left', weight: 700, color: '#6B563C' });
    ctx.restore();
  }

  function nameCard(ctx, t) {
    if (t < ev.name || t > ev.quiet + 0.1) return;
    const a = fade(t, ev.name, 0.4) * out(t, ev.quiet - 0.2, 0.3);
    if (a <= 0.01) return;
    const k = ease.outBack(clamp((t - ev.name) / 0.5), 1.8);
    ctx.save();
    ctx.globalAlpha = a * 0.55;
    ctx.fillStyle = '#1A1208';
    ctx.fillRect(0, 0, W, H);
    ctx.restore();
    ctx.save();
    ctx.globalAlpha = a;
    ctx.translate(W / 2, 760);
    ctx.scale(k, k);
    text(ctx, 'БОБЕРШТЫЛЬ', 0, 0, { size: 96, color: C.cream });
    text(ctx, 'ПИЛА ПЕРВОБЫТНАЯ, 4 Л.С.', 0, 92, { size: 30, color: '#E5C9A0', weight: 700 });
    ctx.restore();
  }

  function hookText(ctx, t) {
    if (t > ev.before + 0.2) return;
    const a = 1 - fade(t, ev.before - 0.2, 0.3);
    ctx.save();
    ctx.globalAlpha = a * 0.5;
    ctx.fillStyle = '#1A1208';
    ctx.fillRect(0, 0, W, H);
    ctx.restore();
    ctx.save();
    ctx.globalAlpha = a;
    text(ctx, 'БЕНЗОПИЛА', W / 2, 700, { size: 104, color: C.cream });
    text(ctx, 'изобретена до бензина', W / 2, 800, { size: 40, color: '#E5C9A0', weight: 700 });
    ctx.restore();
  }

  function quietText(ctx, t) {
    if (t < ev.quiet || t > ev.cta) return;
    const a = fade(t, ev.quiet, 0.3) * out(t, ev.cta - 0.1, 0.2);
    if (a <= 0.01) return;
    ctx.save();
    ctx.globalAlpha = a;
    G.rrect(ctx, 60, 150, 620, 92, 24, { fill: 'rgba(255,248,234,0.94)', seed: 220, stroke: C.ink, strokeW: 5 });
    text(ctx, 'ТИШЕ БЕНЗОПИЛЫ', 92, 196, { size: 40, align: 'left' });
    ctx.restore();
  }

  function cta(ctx, t) {
    if (t < ev.cta) return;
    const a = fade(t, ev.cta, 0.4);
    ctx.save();
    ctx.globalAlpha = 0.7 * a;
    ctx.fillStyle = '#140E08';
    ctx.fillRect(0, 0, W, H);
    ctx.restore();
    ctx.save();
    ctx.globalAlpha = a;
    text(ctx, 'ПОДПИШИСЬ', W / 2, 780, { size: 96, color: C.cream });
    text(ctx, 'если тоже инженер', W / 2, 880, { size: 42, color: '#E5C9A0', weight: 700 });
    G.rrect(ctx, W / 2 - 110, 930, 220, 8, 4, { fill: C.accent, seed: 230 });
    ctx.restore();
  }

  function draw(ctx, t) {
    // тряска на падении
    const sh = t > ev.fall + 0.9 && t < ev.fall + 1.5 ? (1 - (t - ev.fall - 0.9) / 0.6) : 0;
    ctx.save();
    if (sh > 0) ctx.translate(Math.sin(t * 90) * 16 * sh, Math.cos(t * 70) * 12 * sh);
    const zoom = 1 + 0.04 * clamp(t / 21);
    ctx.translate(W / 2, 960);
    ctx.scale(zoom, zoom);
    ctx.translate(-W / 2, -960);

    bg(ctx, t);
    tree(ctx, t);
    hands(ctx, t);
    saw(ctx, t);
    dust(ctx, t);
    ctx.restore();

    hookText(ctx, t);
    chips(ctx, t);
    nameCard(ctx, t);
    quietText(ctx, t);
    cta(ctx, t);
  }

  Studio.film({ draw, post: { paper: 0.14, vignette: 0.16, grain: 0.05 } });
})();
