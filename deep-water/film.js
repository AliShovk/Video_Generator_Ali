// THE FILM — глубинный полив: труба доводит воду до корней.
(function () {
  const U = globalThis.U, G = globalThis.G, S = globalThis.SCORE, Studio = globalThis.Studio;
  const { clamp, lerp, ease } = U;
  const { ev } = S;
  const W = G.W, H = G.H;

  const C = {
    sky1: '#FFF6E4', sky2: '#FFDDAE', sun: '#FFC24A',
    grass: '#79AE63', grass2: '#689B54',
    soil: '#BE8A57', soil2: '#AE7A47', hole: '#6A472B',
    pipe: '#DCE6EA', pipeDark: '#9DAFB6', water: '#57B4DE',
    ink: '#33240F', cream: '#FFF8EA', accent: '#DE7A28', leaf: '#3E8A6A', leaf2: '#4FA07C',
    trunk: '#8B5A2B',
  };
  const F = 'Inter';

  const GROUND = 820;
  const HOLE = { x1: 300, x2: 760, depth: 900 };      // 60 см ≈ 900 px
  const TREE = { x: 420 };
  const PIPE = { x: 640, w: 76, y1: 740, y2: 1490 };  // 50 см ≈ 750 px

  const pop = (t, t0, dur = 0.35, k = 2.0) => (t < t0 ? 0 : ease.outBack(clamp((t - t0) / dur), k));
  const fade = (t, t0, dur = 0.4) => clamp((t - t0) / dur);

  function text(ctx, str, x, y, o = {}) {
    G.text(ctx, str, x, y, {
      size: o.size || 44, fam: F, weight: o.weight || 800,
      color: o.color || C.ink, align: o.align || 'center', baseline: 'middle',
      stroke: o.stroke, strokeW: o.strokeW || 0,
    });
  }

  // ---------- небо ----------
  function sky(ctx, t) {
    const g = ctx.createLinearGradient(0, 0, 0, GROUND);
    g.addColorStop(0, C.sky1);
    g.addColorStop(1, C.sky2);
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, W, GROUND);

    ctx.save();
    for (let i = 0; i < 14; i++) {
      const a = (i / 14) * Math.PI * 2 + t * 0.05;
      G.line(ctx, [[860 + Math.cos(a) * 92, 190 + Math.sin(a) * 92], [860 + Math.cos(a) * 126, 190 + Math.sin(a) * 126]],
        { color: 'rgba(255,190,70,0.5)', lw: 8, seed: 10 + i });
    }
    G.ellipse(ctx, 860, 190, 70, 70, { fill: C.sun, seed: 3 });
    ctx.restore();

    for (let i = 0; i < 3; i++) {
      const x = ((i * 460 + t * (14 + i * 6)) % (W + 320)) - 160;
      const y = 120 + i * 120;
      G.ellipse(ctx, x, y, 88, 32, { fill: 'rgba(255,252,245,0.8)', seed: 20 + i });
      G.ellipse(ctx, x + 62, y + 10, 58, 24, { fill: 'rgba(255,252,245,0.7)', seed: 23 + i });
      G.ellipse(ctx, x - 64, y + 12, 50, 20, { fill: 'rgba(255,252,245,0.65)', seed: 26 + i });
    }

    G.rrect(ctx, 0, GROUND - 24, W, 38, 0, { fill: C.grass, seed: 40 });
    for (let i = 0; i < 26; i++) {
      const x = 20 + i * 42, h = 14 + ((i * 37) % 20);
      G.line(ctx, [[x, GROUND - 22], [x + 8, GROUND - 22 - h]], { color: C.grass2, lw: 6, seed: 50 + i });
    }
  }

  // ---------- земля ----------
  function soil(ctx) {
    ctx.fillStyle = C.soil;
    ctx.fillRect(0, GROUND, W, H - GROUND);
    G.rrect(ctx, 0, GROUND, W, 26, 0, { fill: C.soil2, seed: 60 });
    for (let i = 0; i < 26; i++) {
      const y = GROUND + 60 + i * 40;
      const x = 20 + ((i * 137) % 940);
      G.ellipse(ctx, x, y, 10 + (i % 4) * 4, 5, { fill: 'rgba(120,80,45,0.2)', seed: 70 + i });
    }
    for (let i = 0; i < 18; i++) {
      const x = 40 + ((i * 211) % 980);
      const y = GROUND + 90 + ((i * 97) % 900);
      G.ellipse(ctx, x, y, 12, 8, { fill: 'rgba(150,110,70,0.4)', seed: 90 + i });
    }
  }

  // ---------- яма ----------
  function hole(ctx, t) {
    if (t < ev.dig) return;
    const k = ease.outCubic(clamp((t - ev.dig) / 2.2));
    const d = HOLE.depth * k;
    ctx.save();
    ctx.beginPath();
    ctx.rect(HOLE.x1, GROUND, HOLE.x2 - HOLE.x1, d);
    ctx.clip();
    ctx.fillStyle = C.hole;
    ctx.fillRect(HOLE.x1, GROUND, HOLE.x2 - HOLE.x1, d);
    ctx.fillStyle = 'rgba(140,96,56,0.5)';
    ctx.fillRect(HOLE.x1, GROUND, 16, d);
    ctx.fillRect(HOLE.x2 - 16, GROUND, 16, d);
    ctx.restore();

    const a = fade(t, ev.dig + 0.6, 0.5);
    if (a > 0.01) {
      ctx.save();
      ctx.globalAlpha = a;
      const x = HOLE.x1 - 46;
      G.line(ctx, [[x, GROUND + 6], [x, GROUND + HOLE.depth]], { color: C.accent, lw: 5, seed: 120 });
      G.poly(ctx, [[x - 12, GROUND + 24], [x, GROUND + 4], [x + 12, GROUND + 24]], { fill: C.accent, seed: 121 });
      G.poly(ctx, [[x - 12, GROUND + HOLE.depth - 18], [x, GROUND + HOLE.depth + 2], [x + 12, GROUND + HOLE.depth - 18]], { fill: C.accent, seed: 122 });
      text(ctx, '60', x - 22, GROUND + 400, { size: 64, color: C.accent, align: 'right' });
      text(ctx, 'СМ', x - 22, GROUND + 456, { size: 28, color: C.accent, align: 'right' });
      ctx.restore();
    }
  }

  // ---------- саженец ----------
  function tree(ctx, t) {
    const grow = ease.outCubic(clamp((t - ev.plant) / 1.4));
    if (grow <= 0) return;
    const baseY = GROUND + HOLE.depth - 200;
    const stemTop = lerp(GROUND + 60, GROUND - 300, grow);
    const x = TREE.x;

    // корневой ком: холмик
    G.ellipse(ctx, x, baseY + 10, 96 * grow, 46 * grow, { fill: '#6E4B29', seed: 130 });
    G.ellipse(ctx, x, baseY - 4, 84 * grow, 38 * grow, { fill: '#7F5A33', seed: 131 });

    // ствол: сужается кверху
    G.poly(ctx, [[x - 15, baseY], [x + 15, baseY], [x + 7, stemTop], [x - 7, stemTop]],
      { fill: '#8B5A2B', seed: 132 });
    // ветки
    G.line(ctx, [[x - 2, stemTop + 190], [x - 74, stemTop + 96]], { color: '#8B5A2B', lw: 12, seed: 136 });
    G.line(ctx, [[x + 2, stemTop + 260], [x + 80, stemTop + 150]], { color: '#8B5A2B', lw: 12, seed: 137 });
    G.line(ctx, [[x, stemTop + 120], [x + 52, stemTop + 40]], { color: '#8B5A2B', lw: 9, seed: 138 });

    // крона: пять кругов
    const s2 = grow;
    G.ellipse(ctx, x - 92 * s2, stemTop + 24 * s2, 70 * s2, 60 * s2, { fill: '#357B5C', seed: 133 });
    G.ellipse(ctx, x + 94 * s2, stemTop + 14 * s2, 72 * s2, 62 * s2, { fill: C.leaf2, seed: 134 });
    G.ellipse(ctx, x, stemTop - 58 * s2, 86 * s2, 70 * s2, { fill: C.leaf, seed: 135 });
    G.ellipse(ctx, x - 48 * s2, stemTop - 92 * s2, 60 * s2, 50 * s2, { fill: C.leaf2, seed: 139 });
    G.ellipse(ctx, x + 54 * s2, stemTop - 84 * s2, 58 * s2, 48 * s2, { fill: '#2F7255', seed: 141 });
  }

  // ---------- корни ----------
  function roots(ctx, t) {
    const k = ease.outCubic(clamp((t - ev.plant - 0.5) / 1.2));
    if (k <= 0) return;
    const baseY = GROUND + HOLE.depth - 200;
    const deep = clamp((t - ev.water + 0.8) / 2.2);
    const len = (70 + 90 * Math.max(k * 0.55, deep)) * k;
    const x = TREE.x;
    const rs = [[-1.05, 0.7], [-0.55, 0.95], [0, 1.05], [0.55, 1.0], [1.05, 0.75]];

    ctx.save();
    ctx.lineCap = 'round';
    rs.forEach(([dx, dy], i) => {
      const x2 = x + dx * len;
      const y2 = baseY + 26 + dy * len * 0.8;
      ctx.beginPath();
      ctx.moveTo(x, baseY + 10);
      ctx.bezierCurveTo(x + dx * len * 0.25, baseY + 26 + dy * len * 0.35,
                        x + dx * len * 0.6, baseY + 26 + dy * len * 0.6, x2, y2);
      ctx.strokeStyle = '#C9A96A';
      ctx.lineWidth = 11 - i;
      ctx.stroke();
      // ответвление
      ctx.beginPath();
      ctx.moveTo(x + dx * len * 0.55, baseY + 26 + dy * len * 0.62);
      ctx.bezierCurveTo(x + dx * len * 0.8, baseY + 26 + dy * len * 0.8,
                        x + dx * len * 0.95, baseY + 26 + dy * len * 0.95,
                        x2 + dx * 22, y2 + 30);
      ctx.lineWidth = 5;
      ctx.stroke();
    });
    ctx.restore();
  }

  // ---------- труба ----------
  function pipe(ctx, t) {
    if (t < ev.pipe) return;
    const k = pop(t, ev.pipe, 0.45);
    const y1 = lerp(PIPE.y1 - 150, PIPE.y1, k);
    const y2 = lerp(PIPE.y2 - 150, PIPE.y2, k);
    G.rrect(ctx, PIPE.x, y1, PIPE.w, y2 - y1, 12, { fill: C.pipe, seed: 160, stroke: '#2E2415', strokeW: 4 });
    G.rrect(ctx, PIPE.x, y1, PIPE.w, 26, 10, { fill: C.pipeDark, seed: 161, stroke: '#2E2415', strokeW: 4 });

    const holes = fade(t, ev.pipe + 0.5, 0.6);
    if (holes > 0) {
      ctx.save();
      ctx.globalAlpha = holes;
      const gt = gravelTop(t);
      for (let i = 0; i < 12; i++) {
        const y = y1 + 74 + i * 62;
        if (y > gt - 10) continue;
        G.ellipse(ctx, PIPE.x + PIPE.w / 2, y, 7, 7, { fill: '#2E2415', seed: 170 + i });
      }
      ctx.restore();
    }

    const a = fade(t, ev.pipe + 0.8, 0.5);
    if (a > 0.01) {
      ctx.save();
      ctx.globalAlpha = a;
      const x = PIPE.x - 40;
      G.line(ctx, [[x, PIPE.y1 + 8], [x, PIPE.y1 + 750]], { color: C.accent, lw: 5, seed: 180 });
      G.poly(ctx, [[x - 12, PIPE.y1 + 26], [x, PIPE.y1 + 4], [x + 12, PIPE.y1 + 26]], { fill: C.accent, seed: 181 });
      G.poly(ctx, [[x - 12, PIPE.y1 + 740], [x, PIPE.y1 + 752], [x + 12, PIPE.y1 + 740]], { fill: C.accent, seed: 182 });
      text(ctx, '50', x - 18, PIPE.y1 + 340, { size: 56, color: C.accent, align: 'right' });
      text(ctx, 'СМ', x - 18, PIPE.y1 + 392, { size: 26, color: C.accent, align: 'right' });
      ctx.restore();
    }
  }

  function gravelTop(t) {
    return lerp(PIPE.y2 - 50, PIPE.y1 + 30, fade(t, ev.gravel, 1.6));
  }

  // ---------- гравий ----------
  function gravelTop(t) {
    return lerp(PIPE.y2 - 50, PIPE.y1 + 30, fade(t, ev.gravel, 1.6));
  }

  function gravel(ctx, t) {
    const k = fade(t, ev.gravel, 1.6);
    if (k <= 0) return;
    const top = gravelTop(t);
    ctx.save();
    ctx.beginPath();
    ctx.rect(PIPE.x + 5, top, PIPE.w - 10, PIPE.y2 - top - 5);
    ctx.clip();
    G.rrect(ctx, PIPE.x + 5, top, PIPE.w - 10, PIPE.y2 - top - 5, 8, { fill: '#BDB6A6', seed: 205 });
    const rows = Math.floor((PIPE.y2 - top) / 30) + 2;
    const tones = ['#CFC9BA', '#B9B2A1', '#A7A08F', '#C4BCA9'];
    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < 3; c++) {
        const h1 = Math.abs(Math.sin((r * 7 + c * 13) * 12.9898) % 1);
        const h2 = Math.abs(Math.sin((r * 3 + c * 5) * 78.233) % 1);
        const x = PIPE.x + 16 + c * 18 + h1 * 10;
        const y = PIPE.y2 - 18 - r * 30 - h2 * 8;
        const rx = 9 + h1 * 6;
        const ry = 7 + h2 * 5;
        G.ellipse(ctx, x, y, rx, ry, { fill: tones[(r + c) % 4], seed: 300 + r * 4 + c, stroke: '#8A8374', strokeW: 2 });
      }
    }
    ctx.restore();
  }

  // ---------- вода ----------
  function water(ctx, t) {
    if (t < ev.water) return;
    const k = fade(t, ev.water, 0.5);
    const sx = PIPE.x + PIPE.w / 2;
    const gt = gravelTop(t);

    // лейка на земле справа
    const cx = 792, cy = 724;
    ctx.save();
    ctx.globalAlpha = k;
    G.rrect(ctx, cx, cy, 172, 92, 22, { fill: C.accent, seed: 210, stroke: '#2E2415', strokeW: 5 });
    G.line(ctx, [[cx + 52, cy], [cx + 44, cy - 40], [cx + 128, cy - 40], [cx + 120, cy]],
      { color: '#2E2415', lw: 11, seed: 212 });
    // носик к трубе
    G.poly(ctx, [[cx, cy + 70], [sx + 26, PIPE.y1 + 4], [sx + 26, PIPE.y1 - 18], [cx, cy + 40]],
      { fill: C.accent, seed: 211, stroke: '#2E2415', strokeW: 5 });
    ctx.restore();

    // струя падает в трубу
    const ph = ((t - ev.water) % 0.6) / 0.6;
    for (let i = 0; i < 5; i++) {
      const u = ((i / 5) + ph) % 1;
      const xx = lerp(sx + 26, sx, u);
      const yy = lerp(PIPE.y1 - 8, PIPE.y1 + 26, u);
      G.ellipse(ctx, xx, yy, 5, 8, { fill: C.water, seed: 220 + i });
    }
    // вода в горле трубы
    ctx.save();
    ctx.globalAlpha = 0.5;
    G.rrect(ctx, PIPE.x + 10, PIPE.y1 + 24, PIPE.w - 20, 150, 8, { fill: C.water, seed: 227 });
    ctx.restore();
    // всплеск и влага в гравии
    const spl = fade(t, ev.water + 0.5, 0.5);
    if (spl > 0) {
      ctx.save();
      ctx.globalAlpha = 0.75 * spl;
      G.ellipse(ctx, sx, gt + 10, 26 * spl, 9 * spl, { fill: '#57B4DE', seed: 228 });
      G.rrect(ctx, PIPE.x + 10, gt + 6, PIPE.w - 20, Math.min(160, PIPE.y2 - gt - 10), 8,
        { fill: 'rgba(87,180,222,0.30)', seed: 229 });
      ctx.restore();
    }
    // влага у корней
    const wet = clamp((t - ev.water - 1.2) / 1.8);
    if (wet > 0) {
      ctx.save();
      ctx.globalAlpha = 0.55 * wet;
      for (let i = 0; i < 7; i++) {
        const yy = GROUND + HOLE.depth - 210 + i * 26;
        G.ellipse(ctx, TREE.x + (i % 2 ? 58 : -54), yy, 34 - i * 3, 11, { fill: '#57B4DE', seed: 240 + i });
      }
      ctx.restore();
    }
  }

  // ---------- подписи ----------
  const STEPS = [
    { t: ev.dig, n: '01', label: 'ЯМА 60 СМ' },
    { t: ev.plant, n: '02', label: 'САЖЕНЕЦ' },
    { t: ev.pipe, n: '03', label: 'ТРУБА 50 СМ' },
    { t: ev.gravel, n: '04', label: 'ГРАВИЙ' },
    { t: ev.water, n: '05', label: 'ВОДА' },
  ];

  function stepLabel(ctx, t) {
    let cur = null;
    for (const s of STEPS) if (t >= s.t) cur = s;
    if (!cur || t > ev.moral) return;
    const a = fade(t, cur.t, 0.35) * (1 - fade(t, ev.moral - 0.2, 0.3));
    if (a <= 0.01) return;
    ctx.save();
    ctx.globalAlpha = a;
    G.rrect(ctx, 56, 92, 400, 70, 35, { fill: 'rgba(255,248,234,0.94)', seed: 260, stroke: '#2E2415', strokeW: 4 });
    text(ctx, cur.n, 106, 127, { size: 32, color: C.accent, align: 'left' });
    text(ctx, cur.label, 160, 127, { size: 30, align: 'left' });
    ctx.restore();
  }

  function hook(ctx, t) {
    if (t > ev.dig + 0.2) return;
    const a = 1 - fade(t, ev.dig - 0.2, 0.3);
    ctx.save();
    ctx.globalAlpha = a;
    text(ctx, 'ПОЛИВАЙ', W / 2, 210, { size: 76 });
    text(ctx, 'НЕ ПОД СТВОЛ,', W / 2, 300, { size: 76 });
    text(ctx, 'А В ТРУБУ.', W / 2, 400, { size: 88, color: C.accent });
    ctx.restore();
  }

  function moral(ctx, t) {
    if (t < ev.moral) return;
    const a = fade(t, ev.moral, 0.5);
    ctx.save();
    ctx.globalAlpha = 0.88 * a;
    ctx.fillStyle = '#150F08';
    ctx.fillRect(0, 0, W, H);
    ctx.restore();
    ctx.save();
    ctx.globalAlpha = a;
    text(ctx, 'Вода должна попасть', W / 2, 700, { size: 42, color: '#D9C7AE' });
    text(ctx, 'на 50 см ниже.', W / 2, 766, { size: 56, color: C.cream });
    text(ctx, 'Тогда корни', W / 2, 862, { size: 56, color: C.cream });
    text(ctx, 'уходят вглубь.', W / 2, 928, { size: 56, color: C.cream });
    text(ctx, 'И дерево переживает', W / 2, 1022, { size: 40, color: '#D9C7AE' });
    text(ctx, 'первую засуху.', W / 2, 1084, { size: 52, color: C.sun });
    ctx.restore();
  }

  function draw(ctx, t) {
    sky(ctx, t);
    soil(ctx);
    hole(ctx, t);
    roots(ctx, t);
    tree(ctx, t);
    pipe(ctx, t);
    gravel(ctx, t);
    water(ctx, t);
    stepLabel(ctx, t);
    hook(ctx, t);
    moral(ctx, t);
  }

  Studio.film({ draw, post: { paper: 0.18, vignette: 0.16, grain: 0.05 } });
})();
