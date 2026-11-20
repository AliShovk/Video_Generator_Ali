// THE FILM — кузница: удары не ломают, а придают форму.
(function () {
  const U = globalThis.U, G = globalThis.G, S = globalThis.SCORE, Studio = globalThis.Studio;
  const { clamp, lerp, ease } = U;
  const { ev, HITS, TAPS } = S;
  const W = G.W, H = G.H;

  const C = {
    bg: '#120D0A', ink: '#0A0706', cream: '#F6EBDD', muted: '#A08C78',
    steel: '#93A9BB', steelDark: '#5E7385', hot: '#FFB05A', hot2: '#FF6B2A', deep: '#B3350F',
    iron: '#2A211B', ironLight: '#3E322A', ember: '#FF7A2A', gold: '#E8B44A',
  };
  const F = 'Inter';

  const ANVIL = { cx: 520, top: 1160 };
  const PIVOT = { x: 700, y: 520 };
  const HAMMER_L = 600;
  const REST = 1.52, STRIKE = 1.97;

  const pop = (t, t0, dur = 0.3, k = 2.2) => (t < t0 ? 0 : ease.outBack(clamp((t - t0) / dur), k));
  const fade = (t, t0, dur = 0.4) => clamp((t - t0) / dur);

  function text(ctx, str, x, y, o = {}) {
    G.text(ctx, str, x, y, {
      size: o.size || 48, fam: o.fam || F, weight: o.weight || 800,
      color: o.color || C.cream, align: o.align || 'center', baseline: 'middle',
      stroke: o.stroke, strokeW: o.strokeW || 0, boil: 0,
    });
  }

  const hitIndex = (t) => HITS.filter((h) => t >= h).length;
  const progress = (t) => clamp(hitIndex(t) / HITS.length);

  // удар: 0 — молот поднят, 1 — удар
  function swing(t) {
    let best = 0;
    for (const h of HITS) {
      const u = (t - (h - 0.30)) / 0.30;
      if (u > 0 && u < 1) best = Math.max(best, ease.inQuad(u));
      const back = (t - h) / 0.22;
      if (back > 0 && back < 1) best = Math.max(best, 1 - ease.outQuad(back));
      if (t > h - 0.35 && t < h + 0.3) best = Math.max(best, 0);
    }
    // добивающие удары
    for (const h of TAPS) {
      const u = (t - (h - 0.25)) / 0.25;
      if (u > 0 && u < 1) best = Math.max(best, ease.inQuad(u));
      const back = (t - h) / 0.3;
      if (back > 0 && back < 1) best = Math.max(best, 1 - ease.outQuad(back));
    }
    return best;
  }

  function background(ctx, t) {
    const g = ctx.createLinearGradient(0, 0, 0, H);
    g.addColorStop(0, '#0B0806');
    g.addColorStop(0.55, '#15100C');
    g.addColorStop(1, '#241610');
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, W, H);
    // зарево горна
    const rg = ctx.createRadialGradient(180, 1500, 40, 180, 1500, 620);
    rg.addColorStop(0, 'rgba(255,120,40,0.45)');
    rg.addColorStop(1, 'rgba(255,120,40,0)');
    ctx.fillStyle = rg;
    ctx.fillRect(0, 800, W, H - 800);
    // горн
    G.rrect(ctx, 60, 1470, 260, 150, 12, { fill: '#2A211B', stroke: C.ink, lw: 4, seed: 11 });
    G.rrect(ctx, 78, 1448, 224, 34, 8, { fill: '#1B1512', seed: 12 });
    for (let i = 0; i < 12; i++) {
      const ph = (Math.sin(t * 3 + i * 1.7) + 1) / 2;
      G.ellipse(ctx, 100 + (i * 19) % 190, 1440 - (i % 4) * 10, 9 + ph * 6, 7 + ph * 5,
        { fill: i % 2 ? '#FF8A3C' : '#FFC069', seed: 10 + i });
    }
  }

  function anvil(ctx) {
    const x = ANVIL.cx, y = ANVIL.top;
    // подставка
    G.poly(ctx, [[x - 150, 1480], [x + 150, 1480], [x + 110, 1400], [x - 110, 1400]], { fill: C.iron, stroke: C.ink, lw: 4, seed: 21 });
    // нога
    G.poly(ctx, [[x - 70, 1400], [x + 70, 1400], [x + 52, 1250], [x - 52, 1250]], { fill: C.iron, stroke: C.ink, lw: 4, seed: 22 });
    // тело
    G.rrect(ctx, x - 200, y - 38, 400, 82, 10, { fill: C.ironLight, stroke: C.ink, lw: 5, seed: 23 });
    // рог
    G.poly(ctx, [[x - 198, y - 30], [x - 330, y - 2], [x - 322, y + 30], [x - 196, y + 38]], { fill: C.ironLight, stroke: C.ink, lw: 4, seed: 24 });
    // блик
    G.line(ctx, [[x - 150, y - 22], [x + 150, y - 22]], { color: 'rgba(255,190,130,0.18)', lw: 5, seed: 25 });
  }

  function workpiece(ctx, t) {
    const p = progress(t);
    const cool = clamp((t - ev.quench) / 1.6);
    const heat = clamp(1 - ((t - HITS[HITS.length - 1]) / 3));
    const baseHot = t < ev.quench ? (0.55 + 0.45 * (1 - heat)) : 0;
    // цвет металла: раскалённый -> остывающий -> сталь
    const col = cool > 0.02
      ? mix(C.deep, C.steel, cool)
      : mix(C.hot2, C.hot, baseHot);
    const x = 520;
    const len = 300 + 40 * p;
    const w = lerp(46, 20, p);

    ctx.save();
    ctx.translate(x, ANVIL.top - 24);
    // заготовка: клин с остриём слева, хвостовик справа
    const tip = -len / 2, tail = len / 2;
    const tw = (w / 2) * (1 - p); // остриё появляется постепенно
    const pts = [
      [tip, -tw], [tip + 90, -w / 2], [tail - 40, -w * 0.42], [tail, -w * 0.5],
      [tail, w * 0.5], [tail - 40, w * 0.42], [tip + 90, w / 2], [tip, tw],
    ];
    G.poly(ctx, pts, { fill: col, stroke: 'rgba(10,8,6,0.7)', lw: 3, seed: 31 });
    // горячая кромка
    if (t < ev.quench + 0.2) {
      ctx.save();
      ctx.globalAlpha = 0.55 + 0.45 * Math.sin(t * 8);
      G.line(ctx, [[tip + 6, 0], [tip + 90, -w / 2 + 2]], { color: '#FFD9A0', lw: 3, seed: 32 });
      ctx.restore();
    }
    // блик по спинке после закалки
    if (cool > 0.5) {
      const gl = (t - ev.blade) * 1.6;
      const gx = lerp(-len / 2, len / 2, clamp(gl));
      ctx.save();
      ctx.globalAlpha = 0.5 * (1 - Math.abs(clamp(gl) - 0.5) * 2);
      G.line(ctx, [[gx - 30, -w / 2], [gx + 40, w / 2]], { color: '#E8F4FF', lw: 6, seed: 33 });
      ctx.restore();
    }
    ctx.restore();
  }

  function mixHex(a, b, u) {
    const pa = [1, 3, 5].map((i) => parseInt(a.slice(i, i + 2), 16));
    const pb = [1, 3, 5].map((i) => parseInt(b.slice(i, i + 2), 16));
    const c = pa.map((v, i) => Math.round(lerp(v, pb[i], u)));
    return '#' + c.map((v) => v.toString(16).padStart(2, '0')).join('');
  }
  const mix = mixHex;

  function hammer(ctx, t) {
    const s = swing(t);
    const a = lerp(REST, STRIKE, s);
    const hx = PIVOT.x + Math.cos(a) * HAMMER_L;
    const hy = PIVOT.y + Math.sin(a) * HAMMER_L;
    // рукоять
    G.line(ctx, [[PIVOT.x, PIVOT.y], [hx, hy]], { color: '#6B4A2A', lw: 22, seed: 41 });
    G.line(ctx, [[PIVOT.x, PIVOT.y], [hx, hy]], { color: '#8A6238', lw: 8, seed: 42 });
    // голова
    ctx.save();
    ctx.translate(hx, hy);
    ctx.rotate(a + Math.PI / 2);
    G.rrect(ctx, -56, -44, 112, 88, 8, { fill: '#4A4038', stroke: C.ink, lw: 4, seed: 43 });
    G.rrect(ctx, -56, -44, 112, 26, 6, { fill: '#5C5046', seed: 44 });
    ctx.restore();
  }

  function sparks(ctx, t) {
    for (const h of HITS.concat(TAPS)) {
      const age = t - h;
      if (age < 0 || age > 0.75) continue;
      const u = age / 0.75;
      const rnd = U.mulberry32(Math.round(h * 100));
      for (let i = 0; i < 22; i++) {
        const ang = -Math.PI * 0.15 - rnd() * Math.PI * 0.7;
        const sp = 200 + rnd() * 520;
        const x = 520 + Math.cos(ang) * sp * u;
        const y = ANVIL.top - 40 + Math.sin(ang) * sp * u + 900 * u * u;
        const r = (3 + rnd() * 3) * (1 - u * 0.6);
        ctx.save();
        ctx.globalAlpha = (1 - u) * 0.95;
        G.ellipse(ctx, x, y, r, r, { fill: i % 3 ? '#FFC069' : '#FF7A2A', seed: 50 + i });
        ctx.restore();
      }
      // вспышка на самом ударе
      if (age < 0.09) {
        ctx.save();
        ctx.globalAlpha = (1 - age / 0.09) * 0.5;
        const g = ctx.createRadialGradient(520, ANVIL.top - 30, 0, 520, ANVIL.top - 30, 180);
        g.addColorStop(0, 'rgba(255,220,160,0.9)');
        g.addColorStop(1, 'rgba(255,120,40,0)');
        ctx.fillStyle = g;
        ctx.beginPath(); ctx.arc(520, ANVIL.top - 30, 180, 0, Math.PI * 2); ctx.fill();
        ctx.restore();
      }
    }
  }

  function quench(ctx, t) {
    if (t < ev.quench) return;
    const u = clamp((t - ev.quench) / 2.2);
    if (u > 1) return;
    ctx.save();
    for (let i = 0; i < 16; i++) {
      const rnd = U.mulberry32(700 + i);
      const rise = (u * 420 + rnd() * 90);
      const x = 520 + (rnd() - 0.5) * 260;
      const y = ANVIL.top - 60 - rise;
      ctx.globalAlpha = (1 - u) * (0.10 + rnd() * 0.10);
      G.ellipse(ctx, x, y, 34 + u * 60, 26 + u * 46, { fill: '#EAF4FB', seed: 60 + i });
    }
    ctx.restore();
    // вода
    if (u < 0.35) {
      ctx.save();
      ctx.globalAlpha = (1 - u / 0.35) * 0.35;
      ctx.fillStyle = '#7FC4E8';
      ctx.fillRect(320, ANVIL.top - 40, 420, 14);
      ctx.restore();
    }
  }

  function counter(ctx, t) {
    const n = hitIndex(t);
    const a = fade(t, ev.first, 0.3) * (1 - fade(t, ev.quench, 0.3));
    if (a <= 0.01) return;
    ctx.save();
    ctx.globalAlpha = a;
    text(ctx, `УДАР ${n} / ${HITS.length}`, W / 2, 250, { size: 38, color: C.muted });
    // полоска прогресса
    G.rrect(ctx, 240, 292, 600, 8, 4, { fill: 'rgba(255,255,255,0.12)', seed: 70 });
    G.rrect(ctx, 240, 292, 600 * progress(t), 8, 4, { fill: C.hot, seed: 71 });
    ctx.restore();
  }

  function hook(ctx, t) {
    if (t > ev.first + 0.3) return;
    const a = 1 - fade(t, ev.first - 0.1, 0.3);
    ctx.save();
    ctx.globalAlpha = a;
    text(ctx, 'ЭТО ВЫГЛЯДИТ', W / 2, 230, { size: 46, color: C.muted });
    text(ctx, 'КАК УДАРЫ.', W / 2, 320, { size: 82 });
    text(ctx, 'НА САМОМ ДЕЛЕ —', W / 2, 430, { size: 46, color: C.muted });
    text(ctx, 'ЭТО ФОРМА.', W / 2, 512, { size: 82, color: C.hot });
    ctx.restore();
  }

  function quenchTitle(ctx, t) {
    if (t < ev.quench || t > ev.blade + 0.6) return;
    const a = fade(t, ev.quench, 0.3) * (1 - fade(t, ev.blade, 0.4));
    ctx.save();
    ctx.globalAlpha = a;
    text(ctx, 'ЗАКАЛКА', W / 2, 330, { size: 54, color: '#BFD8E8' });
    text(ctx, 'хрупкое становится твёрдым', W / 2, 396, { size: 30, weight: 700, color: C.muted });
    ctx.restore();
  }

  function moral(ctx, t) {
    if (t < ev.moral) return;
    const a = fade(t, ev.moral, 0.5);
    ctx.save();
    ctx.globalAlpha = 0.7 * a;
    ctx.fillStyle = '#080605';
    ctx.fillRect(0, 0, W, H);
    ctx.restore();
    ctx.save();
    ctx.globalAlpha = a;
    text(ctx, 'Тебя не ломают.', W / 2, 830, { size: 62 });
    text(ctx, 'Тебя куют.', W / 2, 930, { size: 84, color: C.gold });
    text(ctx, 'Каждый удар убирает лишнее.', W / 2, 1030, { size: 34, weight: 700, color: C.muted });
    ctx.restore();
  }

  function draw(ctx, t) {
    background(ctx, t);
    anvil(ctx);
    workpiece(ctx, t);
    sparks(ctx, t);
    hammer(ctx, t);
    quench(ctx, t);
    counter(ctx, t);
    hook(ctx, t);
    quenchTitle(ctx, t);
    moral(ctx, t);
  }

  Studio.film({ draw, post: { paper: 0.16, vignette: 0.4, grain: 0.07 } });
})();
