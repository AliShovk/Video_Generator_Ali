// THE FILM — стройка: стена растёт кирпич за кирпичом, у каждого своя работа.
(function () {
  const U = globalThis.U, G = globalThis.G, S = globalThis.SCORE, Studio = globalThis.Studio;
  const { clamp, lerp, ease } = U;
  const { ev } = S;
  const W = G.W, H = G.H;

  const C = {
    sky1: '#FFE9C9', sky2: '#F6CFA0', sun: '#FFC24A', ink: '#2A2118',
    ground: '#D9C49C', ground2: '#C9B189', brickA: '#C4693F', brickB: '#B85F38',
    brickC: '#D0764A', mortar: '#EADCC6', vest: '#F08A24', vest2: '#FFD34E',
    helmet: '#F5C531', skin: '#E7B48C', crane: '#E8B24A', craneDark: '#B98523',
    steel: '#9AA7B0', text: '#2A2118', cream: '#FFF9EE', ok: '#1F7A4D',
  };
  const F = 'Inter';

  const GROUND = 1520;
  const WALL = { x: 80, y: 1450, cols: 8, rows: 10, bw: 76, bh: 38, gap: 5 };

  const pop = (t, t0, dur = 0.3, k = 2.2) => (t < t0 ? 0 : ease.outBack(clamp((t - t0) / dur), k));
  const fade = (t, t0, dur = 0.4) => clamp((t - t0) / dur);

  function text(ctx, str, x, y, o = {}) {
    G.text(ctx, str, x, y, {
      size: o.size || 48, fam: o.fam || F, weight: o.weight || 800,
      color: o.color || C.text, align: o.align || 'center', baseline: 'middle',
      stroke: o.stroke, strokeW: o.strokeW || 0, boil: 0,
    });
  }

  // ---------- фон ----------
  function sky(ctx, t) {
    const g = ctx.createLinearGradient(0, 0, 0, GROUND);
    g.addColorStop(0, C.sky1);
    g.addColorStop(1, C.sky2);
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, W, GROUND);
    // солнце
    ctx.save();
    ctx.globalAlpha = 0.9;
    for (let i = 0; i < 12; i++) {
      const a = (i / 12) * Math.PI * 2 + t * 0.06;
      G.line(ctx, [[860 + Math.cos(a) * 84, 250 + Math.sin(a) * 84], [860 + Math.cos(a) * 118, 250 + Math.sin(a) * 118]],
        { color: 'rgba(255,190,70,0.55)', lw: 8, seed: 10 + i });
    }
    G.ellipse(ctx, 860, 250, 66, 66, { fill: C.sun, seed: 3 });
    ctx.restore();
    // облака
    for (let i = 0; i < 3; i++) {
      const x = ((i * 470 + t * (12 + i * 5)) % (W + 300)) - 150;
      const y = 180 + i * 120;
      G.ellipse(ctx, x, y, 86, 34, { fill: 'rgba(255,250,240,0.75)', seed: 20 + i });
      G.ellipse(ctx, x + 60, y + 10, 60, 26, { fill: 'rgba(255,250,240,0.7)', seed: 23 + i });
      G.ellipse(ctx, x - 62, y + 12, 52, 22, { fill: 'rgba(255,250,240,0.65)', seed: 26 + i });
    }
    // дальний город
    for (let i = 0; i < 8; i++) {
      const bx = 40 + i * 140, bh = 90 + ((i * 53) % 120);
      G.rrect(ctx, bx, GROUND - bh - 40, 96, bh, 4, { fill: 'rgba(190,160,120,0.45)', seed: 30 + i });
    }
    // земля
    G.rrect(ctx, 0, GROUND, W, H - GROUND, 0, { fill: C.ground, stroke: C.ink, lw: 5, seed: 40 });
  }

  // ---------- кирпичи ----------
  const TOTAL = WALL.cols * WALL.rows;

  function brickAt(i) {
    const row = Math.floor(i / WALL.cols);
    const col = i % WALL.cols;
    const x = WALL.x + col * (WALL.bw + WALL.gap) + (row % 2 ? 18 : 0);
    const y = WALL.y - (row + 1) * (WALL.bh + WALL.gap);
    return { x, y, row, col };
  }

  function wall(ctx, t) {
    const built = clamp((t - ev.build) / (ev.full - ev.build));
    const shown = Math.floor(built * TOTAL);
    for (let i = 0; i < shown; i++) {
      const b = brickAt(i);
      const t0 = ev.build + (i / TOTAL) * (ev.full - ev.build);
      const p = pop(t, t0, 0.22, 2.4);
      if (p <= 0.02) continue;
      ctx.save();
      ctx.translate(b.x + WALL.bw / 2, b.y + WALL.bh / 2);
      ctx.scale(p, p);
      const col = i % 7 === 0 ? C.brickC : i % 3 === 0 ? C.brickB : C.brickA;
      G.rrect(ctx, -WALL.bw / 2, -WALL.bh / 2, WALL.bw, WALL.bh, 4, { fill: col, stroke: 'rgba(60,30,15,0.45)', lw: 3, seed: 50 + i });
      G.line(ctx, [[-WALL.bw / 2 + 6, -4], [WALL.bw / 2 - 6, -4]], { color: 'rgba(255,255,255,0.18)', lw: 3, seed: 80 + i });
      ctx.restore();
    }
    // пыль от последнего кирпича
    if (shown > 0) {
      const b = brickAt(shown - 1);
      const t0 = ev.build + ((shown - 1) / TOTAL) * (ev.full - ev.build);
      const u = (t - t0) / 0.5;
      if (u > 0 && u < 1) {
        ctx.save();
        ctx.globalAlpha = (1 - u) * 0.4;
        for (let k = 0; k < 6; k++) {
          const a = (k / 6) * Math.PI * 2;
          G.ellipse(ctx, b.x + WALL.bw / 2 + Math.cos(a) * (20 + u * 40), b.y + 10 + Math.sin(a) * (10 + u * 20),
            8 + u * 12, 6 + u * 9, { fill: '#EFE0C8', seed: 90 + k });
        }
        ctx.restore();
      }
    }
  }

  // ---------- рабочий ----------
  function worker(ctx, x, feetY, o = {}) {
    const { s = 1, armL = 0.2, armR = 0.2, face = 1, walking = 0, vest = C.vest } = o;
    ctx.save();
    ctx.translate(x, feetY);
    ctx.scale(s * face, s);
    // тень
    G.ellipse(ctx, 0, 4, 52, 10, { fill: 'rgba(80,60,40,0.18)', seed: 100 });
    // ноги
    const swing = Math.sin(walking) * 26;
    G.line(ctx, [[-14, -110], [-16 - swing * 0.5, -6]], { color: '#3B4A5A', lw: 22, seed: 101 });
    G.line(ctx, [[16, -110], [18 + swing * 0.5, -6]], { color: '#3B4A5A', lw: 22, seed: 102 });
    G.rrect(ctx, -34 - swing * 0.5, -14, 36, 14, 4, { fill: '#2B2118', seed: 103 });
    G.rrect(ctx, 18 + swing * 0.5, -14, 36, 14, 4, { fill: '#2B2118', seed: 104 });
    // корпус-жилет
    G.rrect(ctx, -34, -268, 68, 168, 16, { fill: vest, stroke: C.ink, lw: 4, seed: 105 });
    G.rrect(ctx, -34, -232, 68, 10, 2, { fill: C.vest2, seed: 106 });
    G.rrect(ctx, -34, -180, 68, 10, 2, { fill: C.vest2, seed: 107 });
    // руки
    G.line(ctx, [[-32, -244], [-54 - armL * 26, -190 + armL * 60]], { color: vest, lw: 18, seed: 108 });
    G.line(ctx, [[32, -244], [54 + armR * 26, -190 + armR * 60]], { color: vest, lw: 18, seed: 109 });
    G.ellipse(ctx, -54 - armL * 26, -190 + armL * 60, 11, 11, { fill: C.skin, seed: 110 });
    G.ellipse(ctx, 54 + armR * 26, -190 + armR * 60, 11, 11, { fill: C.skin, seed: 111 });
    // голова
    G.ellipse(ctx, 0, -304, 30, 34, { fill: C.skin, stroke: C.ink, lw: 4, seed: 112 });
    // каска
    G.poly(ctx, [[-34, -318], [34, -318], [26, -352], [-26, -352]], { fill: C.helmet, stroke: C.ink, lw: 4, seed: 113 });
    G.rrect(ctx, -44, -322, 60, 9, 3, { fill: '#D9A81F', seed: 114 });
    G.ellipse(ctx, -10, -302, 3, 4, { fill: C.ink, seed: 115 });
    G.ellipse(ctx, 10, -302, 3, 4, { fill: C.ink, seed: 116 });
    G.line(ctx, [[-8, -284], [8, -284]], { color: C.ink, lw: 3, seed: 117 });
    ctx.restore();
  }

  // ---------- леса ----------
  function scaffold(ctx) {
    for (const x of [200, 330]) {
      G.rrect(ctx, x, 980, 12, GROUND - 980, 3, { fill: C.steel, stroke: C.ink, lw: 3, seed: 120 });
    }
    G.rrect(ctx, 180, 966, 190, 18, 4, { fill: '#C08B4A', stroke: C.ink, lw: 4, seed: 121 });
    G.line(ctx, [[200, 1120], [330, 1050]], { color: C.steel, lw: 6, seed: 122 });
    G.line(ctx, [[200, 1300], [330, 1230]], { color: C.steel, lw: 6, seed: 123 });
  }

  // ---------- кран ----------
  function crane(ctx, t) {
    const baseX = 880;
    // мачта
    G.rrect(ctx, baseX - 22, 330, 44, GROUND - 330, 4, { fill: C.crane, stroke: C.ink, lw: 4, seed: 130 });
    for (let y = 370; y < GROUND - 40; y += 90) {
      G.line(ctx, [[baseX - 22, y], [baseX + 22, y + 45]], { color: C.craneDark, lw: 5, seed: 131 + y });
      G.line(ctx, [[baseX + 22, y], [baseX - 22, y + 45]], { color: C.craneDark, lw: 5, seed: 141 + y });
    }
    // поворотная платформа
    G.rrect(ctx, baseX - 60, 296, 120, 40, 6, { fill: C.craneDark, stroke: C.ink, lw: 4, seed: 150 });
    // стрела
    const ang = -0.06 + Math.sin(t * 0.25) * 0.02;
    const len = 560;
    const tipX = baseX - Math.cos(ang) * len;
    const tipY = 316 + Math.sin(ang) * len;
    G.line(ctx, [[baseX, 316], [tipX, tipY]], { color: C.crane, lw: 26, seed: 151 });
    G.line(ctx, [[baseX, 316], [tipX, tipY]], { color: C.craneDark, lw: 6, seed: 152 });
    // трос и груз
    const loadT = clamp((t - ev.crane) / 4);
    const travel = clamp((t - ev.crane - 4) / 4);
    const hookX = lerp(baseX - 200, 360, travel);
    const palletY = lerp(GROUND - 40, 920, ease.outQuad(loadT));
    G.line(ctx, [[lerp(baseX, tipX, 0.35), lerp(316, tipY, 0.35)], [hookX, palletY - 40]], { color: C.ink, lw: 4, seed: 153 });
    if (t >= ev.crane && t < ev.done) {
      // поддон с кирпичами
      G.rrect(ctx, hookX - 70, palletY - 20, 140, 16, 3, { fill: '#8B5A2B', stroke: C.ink, lw: 3, seed: 154 });
      for (let i = 0; i < 8; i++) {
        G.rrect(ctx, hookX - 64 + (i % 4) * 34, palletY - 52 + Math.floor(i / 4) * 18, 30, 14, 2,
          { fill: i % 2 ? C.brickA : C.brickB, seed: 155 + i });
      }
    }
    // кабина
    G.rrect(ctx, baseX + 18, 340, 86, 74, 6, { fill: '#E9D6B4', stroke: C.ink, lw: 4, seed: 160 });
    G.rrect(ctx, baseX + 26, 348, 70, 40, 4, { fill: '#9CC9E8', seed: 161 });
  }

  // ---------- сцена ----------
  function people(ctx, t) {
    if (t < ev.build) return;
    // 1) на лесах кладёт кирпич
    const lay = 0.5 + 0.5 * Math.sin(t * 6.0);
    worker(ctx, 300, 966, { s: 0.92, armR: 0.9 - lay * 0.8, armL: 0.2, face: 1 });
    // кирпич в руке
    const hy = 966 - 244 + (0.9 - lay * 0.8) * 60;
    if (t < ev.full) {
      G.rrect(ctx, 356, hy - 10, 34, 16, 2, { fill: C.brickA, stroke: 'rgba(60,30,15,0.45)', lw: 2, seed: 170 });
    }
    // 2) носит кирпичи по земле
    const walk = t * 3.2;
    const wx = 640 - ((t * 90) % 320);
    worker(ctx, wx, GROUND, { s: 0.95, walking: walk, armR: 0.9, armL: 0.1 });
    G.rrect(ctx, wx + 40, GROUND - 250, 56, 22, 3, { fill: C.brickC, stroke: 'rgba(60,30,15,0.45)', lw: 2, seed: 171 });
    // 3) у крана тянет рычаг
    const pull = 0.5 + 0.5 * Math.sin(t * 2.4);
    worker(ctx, 780, GROUND, { s: 0.9, armR: 0.9 - pull * 0.5, armL: 0.5, face: -1 });
    // пульт с рычагом
    G.rrect(ctx, 700, GROUND - 96, 46, 96, 5, { fill: '#6B6255', stroke: C.ink, lw: 4, seed: 175 });
    G.line(ctx, [[723, GROUND - 96], [706 + pull * 22, GROUND - 150]], { color: '#C8102E', lw: 6, seed: 176 });
  }


  function flyingBricks(ctx, t) {
    if (t < ev.crane || t > ev.done) return;
    const built = clamp((t - ev.build) / (ev.full - ev.build));
    const n = Math.max(1, Math.floor(built * TOTAL));
    const b = brickAt(Math.min(TOTAL - 1, n - 1));
    for (let k = 0; k < 70; k++) {
      const t0 = ev.crane + k * 0.26;
      const u = (t - t0) / 0.62;
      if (u < 0 || u > 1) continue;
      const x0 = 360, y0 = 900;
      const x1 = b.x + WALL.bw / 2, y1 = b.y;
      const x = lerp(x0, x1, u);
      const y = lerp(y0, y1, u) - Math.sin(Math.PI * u) * 150;
      ctx.save();
      ctx.translate(x, y);
      ctx.rotate(u * 6 + k);
      G.rrect(ctx, -17, -8, 34, 16, 2, { fill: k % 2 ? C.brickA : C.brickC, stroke: 'rgba(60,30,15,0.5)', lw: 2, seed: 200 + k });
      ctx.restore();
    }
  }

  function barrow(ctx, t) {
    if (t < ev.build) return;
    const x = 1010 - ((t * 110) % 300);
    const y = GROUND;
    ctx.save();
    ctx.translate(x, y);
    // тачка
    G.poly(ctx, [[-70, -40], [70, -40], [50, -6], [-50, -6]], { fill: '#8B5A2B', stroke: C.ink, lw: 4, seed: 210 });
    G.ellipse(ctx, 44, -4, 18, 18, { fill: '#2B2118', stroke: C.ink, lw: 3, seed: 211 });
    G.line(ctx, [[-60, -40], [-90, -90]], { color: '#6B4A2A', lw: 8, seed: 212 });
    for (let i = 0; i < 4; i++) {
      G.rrect(ctx, -52 + i * 26, -62, 24, 18, 2, { fill: i % 2 ? C.brickA : C.brickB, seed: 213 + i });
    }
    ctx.restore();
    // человек за тачкой
    worker(ctx, x - 86, GROUND, { s: 0.9, armR: 1.1, armL: 0.8, walking: t * 6 });
  }

  function hookText(ctx, t) {
    if (t > ev.build + 0.3) return;
    const a = 1 - fade(t, ev.build - 0.15, 0.3);
    ctx.save();
    ctx.globalAlpha = a;
    text(ctx, 'ТЫ НЕ ВИДИШЬ РЕЗУЛЬТАТА.', W / 2, 250, { size: 42 });
    text(ctx, 'А ОН УЖЕ ЕСТЬ.', W / 2, 320, { size: 64, color: '#A8541F' });
    ctx.restore();
  }

  function counter(ctx, t) {
    const a = fade(t, ev.build, 0.4) * (1 - fade(t, ev.done, 0.4));
    if (a <= 0.01) return;
    const built = clamp((t - ev.build) / (ev.full - ev.build));
    const n = Math.floor(built * TOTAL);
    ctx.save();
    ctx.globalAlpha = a;
    text(ctx, `КИРПИЧ ${n} / ${TOTAL}`, W / 2, 250, { size: 34, color: '#7A5A3A' });
    G.rrect(ctx, 250, 288, 580, 8, 4, { fill: 'rgba(90,60,30,0.18)', seed: 180 });
    G.rrect(ctx, 250, 288, 580 * built, 8, 4, { fill: C.vest, seed: 181 });
    ctx.restore();
  }

  function moral(ctx, t) {
    if (t < ev.moral) return;
    const a = fade(t, ev.moral, 0.5);
    ctx.save();
    ctx.globalAlpha = 0.72 * a;
    ctx.fillStyle = '#150F0A';
    ctx.fillRect(0, 0, W, H);
    ctx.restore();
    ctx.save();
    ctx.globalAlpha = a;
    text(ctx, 'Стена не появляется сразу.', W / 2, 800, { size: 40, color: '#D9C7AE' });
    text(ctx, 'Она появляется', W / 2, 880, { size: 56, color: C.cream });
    text(ctx, 'из тысяч кирпичей.', W / 2, 960, { size: 70, color: C.helmet });
    text(ctx, 'Ты не строишь стену.', W / 2, 1080, { size: 40, color: '#D9C7AE' });
    text(ctx, 'Ты строишь то, что за ней.', W / 2, 1140, { size: 44, color: C.cream });
    ctx.restore();
  }

  function draw(ctx, t) {
    sky(ctx, t);
    wall(ctx, t);
    scaffold(ctx);
    crane(ctx, t);
    people(ctx, t);
    flyingBricks(ctx, t);
    barrow(ctx, t);
    hookText(ctx, t);
    counter(ctx, t);
    moral(ctx, t);
  }

  Studio.film({ draw, post: { paper: 0.2, vignette: 0.16, grain: 0.05 } });
})();
