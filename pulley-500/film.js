// THE FILM — схема полиспаста: 500 кг, два подвижных блока с каждой стороны.
// Всё — чистая функция от t: звук и картинка читают один и тот же score.js.
(function () {
  const U = globalThis.U, G = globalThis.G, S = globalThis.SCORE, Studio = globalThis.Studio;
  const { clamp, lerp, ease, pulse } = U;
  const { ev, BEAT } = S;
  const W = G.W, H = G.H;

  // ---------- палитра ----------
  const C = {
    bg: '#F3E9D2', ink: '#221F1A', wood: '#B07A45', woodDark: '#7E5430',
    wheel: '#C58D52', wheelFace: '#F0DFC0', rope: '#8E6B3E',
    stone: '#6E6259', accent: '#C8102E', ok: '#15803D',
    cream: '#FFFDF6', muted: '#6B6255', shirt: '#7C8FA3', pants: '#3B4A5A',
  };
  const F = 'Inter';

  // ---------- геометрия (1080×1920) ----------
  const BEAM = { x0: 88, x1: 992, y: 520, h: 40 };
  const FIX = { y: 650, r: 52, lx: 170, rx: 910 };
  const MID = { y: 900, r: 48, lx: 400, rx: 680 };
  const BOT = { y: 1140, r: 44, lx: 470, rx: 610 };
  const BLOCK = { cx: 540, cy: 1290, w: 300, h: 180 };
  const FEET = 1560, HAND_Y = 1180, GROUND = 1548;
  const SAFE_TOP = 232;
  let LIFT = 0; // 0..1 — насколько блок уже поднят

  const pop = (t, t0, dur = 0.32, k = 2.1) => (t < t0 ? 0 : ease.outBack(clamp((t - t0) / dur), k));
  const fade = (t, t0, dur = 0.4) => clamp((t - t0) / dur);
  const ring = (t, t0, r0, r1) => {
    const u = clamp((t - t0) / 0.55);
    if (u <= 0 || u >= 1) return null;
    return { r: lerp(r0, r1, ease.outCubic(u)), a: 1 - u };
  };

  function arcPts(cx, cy, r, a0, a1, n = 16) {
    const out = [];
    for (let i = 0; i <= n; i++) {
      const a = lerp(a0, a1, i / n);
      out.push([cx + Math.cos(a) * r, cy + Math.sin(a) * r]);
    }
    return out;
  }

  function rope(ctx, pts, seed, alpha = 1, lw = 9) {
    if (alpha <= 0) return;
    ctx.save();
    ctx.globalAlpha = alpha;
    ctx.lineJoin = 'round';
    G.line(ctx, pts, { color: C.rope, lw, seed, amp: 0.5 });
    G.line(ctx, pts, { color: 'rgba(255,240,205,0.40)', lw: lw * 0.34, seed: seed + 1, amp: 0.4 });
    ctx.restore();
  }

  function pulley(ctx, x, y, r, opts = {}) {
    const { glow = 0, spin = 0, alpha = 1 } = opts;
    if (alpha <= 0) return;
    ctx.save();
    ctx.globalAlpha = alpha;
    if (glow > 0) {
      const g = ctx.createRadialGradient(x, y, r * 0.6, x, y, r * 2.5);
      g.addColorStop(0, `rgba(200,16,46,${0.32 * glow})`);
      g.addColorStop(1, 'rgba(200,16,46,0)');
      ctx.fillStyle = g;
      ctx.beginPath(); ctx.arc(x, y, r * 2.5, 0, Math.PI * 2); ctx.fill();
    }
    G.ellipse(ctx, x, y, r, r, { fill: C.wheel, stroke: C.ink, lw: 5, seed: 11 + Math.round(x) });
    G.ellipse(ctx, x, y, r * 0.76, r * 0.76, { fill: C.wheelFace, stroke: C.ink, lw: 4, seed: 21 + Math.round(x) });
    G.ellipse(ctx, x, y, r * 0.22, r * 0.22, { fill: C.ink, seed: 31 });
    for (let i = 0; i < 3; i++) {
      const a = spin + (i / 3) * Math.PI * 2;
      G.line(ctx, [
        [x + Math.cos(a) * r * 0.28, y + Math.sin(a) * r * 0.28],
        [x + Math.cos(a) * r * 0.7, y + Math.sin(a) * r * 0.7],
      ], { color: 'rgba(34,31,26,0.30)', lw: 4, seed: 40 + i });
    }
    ctx.restore();
  }

  function plate(ctx, x, y, w, h, seed) {
    G.rrect(ctx, x - w / 2, y - h / 2, w, h, 10, { fill: 'rgba(255,253,246,0.92)', stroke: 'rgba(34,31,26,0.35)', lw: 3, seed });
  }

  function arrowHead(ctx, x, y, color, size = 20) {
    G.poly(ctx, [[x - size, y - size], [x + size, y - size], [x, y + size * 0.5]], { fill: color, seed: 72 });
  }

  function weightLabel(ctx, text, x, y, t, t0, color, leaderTo) {
    const p = pop(t, t0, 0.34, 2.3);
    if (p <= 0.01) return;
    ctx.save();
    ctx.globalAlpha = clamp(p);
    if (leaderTo) {
      ctx.strokeStyle = 'rgba(34,31,26,0.28)';
      ctx.setLineDash([7, 7]);
      ctx.lineWidth = 3;
      ctx.beginPath();
      const dir = leaderTo[0] > x ? 1 : -1;
      ctx.moveTo(x + dir * 62, y);
      ctx.lineTo(leaderTo[0] - dir * 8, leaderTo[1]);
      ctx.stroke();
      ctx.setLineDash([]);
    }
    ctx.translate(x, y);
    ctx.scale(p, p);
    G.text(ctx, text, 0, 0, {
      size: 46, fam: F, weight: 800, color, align: 'center', baseline: 'middle',
      stroke: C.cream, strokeW: 10, boil: 0,
    });
    ctx.restore();
    const rr = ring(t, t0, 26, 92);
    if (rr) {
      ctx.save();
      ctx.globalAlpha = rr.a * 0.7;
      ctx.strokeStyle = color;
      ctx.lineWidth = 5;
      ctx.beginPath(); ctx.arc(x, y, rr.r, 0, Math.PI * 2); ctx.stroke();
      ctx.restore();
    }
  }

  function worker(ctx, x, hand, t, pull) {
    const ink = C.ink;
    const y = FEET;
    const lean = 0.10 * pull;
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(-lean * (x < W / 2 ? 1 : -1));
    G.ellipse(ctx, 4, 6, 66, 14, { fill: 'rgba(34,31,26,0.16)', seed: 5 });
    // ноги
    G.line(ctx, [[-16, -118], [-28, -8]], { color: C.pants, lw: 26, seed: 6 });
    G.line(ctx, [[18, -118], [32, -8]], { color: C.pants, lw: 26, seed: 7 });
    // ботинки
    G.rrect(ctx, -46, -18, 42, 20, 6, { fill: '#2B2118', seed: 8 });
    G.rrect(ctx, 14, -18, 46, 20, 6, { fill: '#2B2118', seed: 9 });
    // руки — к верёвке (руки подняты)
    const hx = hand[0] - x, hy = hand[1] - y;
    G.line(ctx, [[-32, -262], [hx * 0.55 - 6, hy + 60], [hx, hy + 14]], { color: C.shirt, lw: 20, seed: 12 });
    G.line(ctx, [[34, -262], [hx * 0.55 + 8, hy + 66], [hx, hy + 20]], { color: C.shirt, lw: 20, seed: 13 });
    // торс
    G.rrect(ctx, -38, -292, 76, 180, 18, { fill: C.shirt, stroke: ink, lw: 5, seed: 10 });
    // голова
    G.ellipse(ctx, 0, -326, 34, 38, { fill: '#E8B48A', stroke: ink, lw: 5, seed: 14 });
    // кепка
    G.poly(ctx, [[-34, -348], [34, -348], [26, -372], [-26, -372]], { fill: '#5B6B7A', stroke: ink, lw: 4, seed: 15 });
    G.rrect(ctx, -42, -352, 54, 12, 5, { fill: '#42505C', seed: 16 });
    // глаза и усы
    G.ellipse(ctx, -11, -330, 3.6, 4.4, { fill: ink, seed: 17 });
    G.ellipse(ctx, 11, -330, 3.6, 4.4, { fill: ink, seed: 18 });
    G.line(ctx, [[-13, -310], [13, -310]], { color: ink, lw: 4, seed: 19 });
    ctx.restore();
  }

  function background(ctx, t) {
    ctx.fillStyle = C.bg;
    ctx.fillRect(0, 0, W, H);
    const g = ctx.createLinearGradient(0, 0, 0, H * 0.5);
    g.addColorStop(0, 'rgba(255,214,150,0.35)');
    g.addColorStop(1, 'rgba(255,214,150,0)');
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, W, H * 0.5);
    G.poly(ctx, [[0, GROUND], [W, GROUND], [W, H], [0, H]], { fill: '#E2CFA6', stroke: C.ink, lw: 5, seed: 3 });
    for (let i = 0; i < 9; i++) {
      G.line(ctx, [[(i * 137) % W, GROUND + 44 + (i % 3) * 32], [(i * 137) % W + 90, GROUND + 44 + (i % 3) * 32]],
        { color: 'rgba(120,90,50,0.20)', lw: 4, seed: 50 + i });
    }
  }

  function rig(ctx, t) {
    const a = fade(t, ev.rig - 0.25, 0.5);
    if (a <= 0) return;
    ctx.save();
    ctx.globalAlpha = a;
    G.rrect(ctx, BEAM.x0, BEAM.y, BEAM.x1 - BEAM.x0, BEAM.h, 8, { fill: C.woodDark, stroke: C.ink, lw: 5, seed: 60 });
    G.line(ctx, [[BEAM.x0 + 14, BEAM.y + 13], [BEAM.x1 - 14, BEAM.y + 13]], { color: 'rgba(255,230,180,0.35)', lw: 5, seed: 61 });
    for (const x of [FIX.lx, FIX.rx]) G.rrect(ctx, x - 13, BEAM.y + BEAM.h - 8, 26, 30, 3, { fill: '#4A4A4A', seed: 62 });
    ctx.restore();
  }

  function ropes(ctx, t) {
    const a = fade(t, ev.rig, 0.7);
    if (a <= 0) return;
    const tail = fade(t, ev.arrows, 0.4); // хвост верёвки вниз, когда тянут
    const my = MID.y - 150 * LIFT;        // средние блоки поднимаются
    const by = BOT.y - 235 * LIFT;        // нижние блоки и груз — выше
    const hy = HAND_Y + 120 * LIFT;       // руки тянут вниз

    // ЛЕВАЯ сторона
    const lA = [
      [448, BEAM.y + BEAM.h],
      [448, my - MID.r * 0.9],
      ...arcPts(MID.lx, my, MID.r, 0, Math.PI, 14),        // под средним блоком
      [FIX.lx + FIX.r * 0.86, FIX.y + FIX.r * 0.46],
      ...arcPts(FIX.lx, FIX.y, FIX.r, 0.5, -Math.PI + 0.15, 14), // через верх неподвижного
      [118, hy],
    ];
    rope(ctx, lA, 81, a);
    if (tail > 0) rope(ctx, [[118, hy], [118, hy + 150]], 85, a * tail, 8);

    const lB = [
      [426, BEAM.y + BEAM.h],
      [426, by - BOT.r * 0.9],
      ...arcPts(BOT.lx, by, BOT.r, Math.PI, 0, 12),          // под нижним блоком
      [MID.lx + 6, my + MID.r + 10],
    ];
    rope(ctx, lB, 82, a);

    // ПРАВАЯ сторона (зеркально)
    const m = (x) => W - x;
    const rA = [
      [m(448), BEAM.y + BEAM.h],
      [m(448), my - MID.r * 0.9],
      ...arcPts(m(MID.lx), my, MID.r, Math.PI, 0, 14),
      [m(FIX.lx + FIX.r * 0.86), FIX.y + FIX.r * 0.46],
      ...arcPts(m(FIX.lx), FIX.y, FIX.r, Math.PI - 0.5, 0.15, 14),
      [W - 118, hy],
    ];
    rope(ctx, rA, 83, a);
    if (tail > 0) rope(ctx, [[W - 118, hy], [W - 118, hy + 150]], 86, a * tail, 8);

    const rB = [
      [m(426), BEAM.y + BEAM.h],
      [m(426), by - BOT.r * 0.9],
      ...arcPts(m(BOT.lx), by, BOT.r, 0, Math.PI, 12),
      [m(MID.lx + 6), my + MID.r + 10],
    ];
    rope(ctx, rB, 84, a);

    // узлы на балке
    for (const x of [448, 426, W - 448, W - 426]) {
      G.ellipse(ctx, x, BEAM.y + BEAM.h + 2, 12, 10, { fill: C.ink, seed: 87 });
    }
  }

  function block(ctx, t) {
    const dropT = ev.blockDrop, landT = ev.blockLand;
    if (t < dropT) return;
    let y = 0;
    if (t < landT) {
      const u = clamp((t - dropT) / (landT - dropT));
      y = lerp(-560, 0, ease.inQuad(u));
    } else {
      y = -10 * Math.exp(-(t - landT) * 9) * Math.cos((t - landT) * 22);
    }
    const squash = t < landT ? 0 : Math.exp(-(t - landT) * 8) * 0.08;
    // хук: камень крупнее, пока не появилась рама
    const zoom = 1 + 0.30 * (1 - fade(t, ev.rig - 0.35, 0.45));
    const hookShift = -150 * (1 - fade(t, ev.rig - 0.35, 0.45));

    // стропы от нижних блоков к камню
    if (t >= ev.rig) {
      const a = fade(t, ev.rig + 0.2, 0.4);
      const by = BOT.y - 235 * LIFT, bcy = BLOCK.cy + y - 235 * LIFT;
      rope(ctx, [[BOT.lx, by + BOT.r - 6], [BOT.lx + 4, bcy - 82]], 94, a, 10);
      rope(ctx, [[BOT.rx, by + BOT.r - 6], [BOT.rx - 4, bcy - 82]], 95, a, 10);
    }

    ctx.save();
    ctx.translate(BLOCK.cx, BLOCK.cy + y + hookShift - 235 * LIFT);
    ctx.scale((1 + squash) * zoom, (1 - squash) * zoom);
    const w = BLOCK.w, h = BLOCK.h;
    const pts = [
      [-w / 2, -h * 0.26], [-w * 0.30, -h * 0.50], [w * 0.28, -h * 0.54],
      [w / 2, -h * 0.18], [w * 0.47, h * 0.34], [w * 0.08, h * 0.50],
      [-w * 0.34, h * 0.45], [-w * 0.52, h * 0.02],
    ];
    G.poly(ctx, pts, {
      fill: C.stone, stroke: C.ink, lw: 6, seed: 91,
      hatch: { color: 'rgba(0,0,0,0.16)', gap: 11, angle: -0.6 },
    });
    G.line(ctx, [[-92, -58], [-18, -80], [58, -66]], { color: 'rgba(255,255,255,0.20)', lw: 7, seed: 92 });
    G.text(ctx, '500 кг', 0, 10, { size: 62, fam: F, weight: 800, color: C.cream, align: 'center', baseline: 'middle', stroke: 'rgba(0,0,0,0.35)', strokeW: 8, boil: 0 });
    ctx.restore();

    // постамент стоит на полу и не поднимается вместе с грузом
    G.rrect(ctx, BLOCK.cx - 126, BLOCK.cy + 90, 252, 26, 6, { fill: C.woodDark, stroke: C.ink, lw: 5, seed: 93 });

    if (t >= landT && t < landT + 0.9) {
      const u = (t - landT) / 0.9;
      ctx.save();
      ctx.globalAlpha = (1 - u) * 0.5;
      for (let i = 0; i < 14; i++) {
        const ang = (i / 14) * Math.PI * 2;
        const rr = 40 + u * 200;
        G.ellipse(ctx, BLOCK.cx + Math.cos(ang) * rr * 1.6, BLOCK.cy + 92 - Math.abs(Math.sin(ang)) * u * 40,
          16 + u * 22, 12 + u * 16, { fill: '#D8C39B', seed: 100 + i });
      }
      ctx.restore();
    }
  }

  function pulleys(ctx, t) {
    const a = fade(t, ev.rig, 0.6);
    if (a <= 0) return;
    const g1 = t >= ev.split ? pulse(t, ev.split, 5) * 0.9 : 0;
    const g2 = t >= ev.half1 ? pulse(t, ev.half1, 5) * 0.9 : 0;
    const g3 = t >= ev.half2 ? pulse(t, ev.half2, 5) * 0.9 : 0;
    const spin = t * 0.8 + LIFT * 7;
    const my = MID.y - 150 * LIFT, by = BOT.y - 235 * LIFT;
    pulley(ctx, FIX.lx, FIX.y, FIX.r, { alpha: a, glow: g3, spin });
    pulley(ctx, FIX.rx, FIX.y, FIX.r, { alpha: a, glow: g3, spin: -spin });
    pulley(ctx, MID.lx, my, MID.r, { alpha: a, glow: g2, spin: -spin * 1.1 });
    pulley(ctx, MID.rx, my, MID.r, { alpha: a, glow: g2, spin: spin * 1.1 });
    pulley(ctx, BOT.lx, by, BOT.r, { alpha: a, glow: g1, spin });
    pulley(ctx, BOT.rx, by, BOT.r, { alpha: a, glow: g1, spin: -spin });
  }

  function weights(ctx, t) {
    if (t >= ev.answer - 0.15) return;
    const hy = HAND_Y + 120 * LIFT;
    // при подъёме блоки уезжают — подписи-выноски убираем
    if (LIFT < 0.02) {
      const lxTop = FIX.lx + FIX.r + 138, rxTop = W - lxTop;
      const lxMid = 250, rxMid = W - lxMid;
      if (t >= ev.split) {
        weightLabel(ctx, '250 кг', lxMid, BOT.y, t, ev.split, C.ink, [BOT.lx - BOT.r - 6, BOT.y]);
        weightLabel(ctx, '250 кг', rxMid, BOT.y, t, ev.split + 0.12, C.ink, [BOT.rx + BOT.r + 6, BOT.y]);
      }
      if (t >= ev.half1) {
        weightLabel(ctx, '125 кг', lxMid, MID.y, t, ev.half1, C.ink, [MID.lx - MID.r - 6, MID.y]);
        weightLabel(ctx, '125 кг', rxMid, MID.y, t, ev.half1 + 0.12, C.ink, [MID.rx + MID.r + 6, MID.y]);
      }
      if (t >= ev.half2) {
        weightLabel(ctx, '62,5 кг', lxTop, FIX.y, t, ev.half2, C.accent, [FIX.lx + FIX.r + 8, FIX.y]);
        weightLabel(ctx, '62,5 кг', rxTop, FIX.y, t, ev.half2 + 0.12, C.accent, [FIX.rx - FIX.r - 8, FIX.y]);
      }
    }
    if (t >= ev.arrows) {
      const p = pop(t, ev.arrows, 0.3, 2.4);
      ctx.save();
      ctx.globalAlpha = clamp(p);
      arrowHead(ctx, 118, hy + 150, C.accent, 22);
      arrowHead(ctx, W - 118, hy + 150, C.accent, 22);
      G.text(ctx, 'F', 118 + 74, hy + 110, { size: 62, fam: F, weight: 800, color: C.accent, align: 'center', baseline: 'middle', stroke: C.cream, strokeW: 9, boil: 0 });
      G.text(ctx, 'F', W - 118 - 74, hy + 110, { size: 62, fam: F, weight: 800, color: C.accent, align: 'center', baseline: 'middle', stroke: C.cream, strokeW: 9, boil: 0 });
      ctx.restore();
    }
  }

  function people(ctx, t) {
    if (t < ev.rig) return;
    const a = fade(t, ev.rig + 0.1, 0.5);
    if (a <= 0) return;
    ctx.save();
    ctx.globalAlpha = a;
    const hy = HAND_Y + 120 * LIFT;
    const pull = t >= ev.arrows ? 0.5 + 0.5 * Math.max(0, Math.sin(Math.PI * ((t - ev.arrows) % BEAT) / BEAT)) : 0;
    const step = 12 * LIFT;
    worker(ctx, 66 - step, [118, hy], t, pull + 0.3 * LIFT);
    worker(ctx, 1014 + step, [W - 118, hy], t, pull + 0.3 * LIFT);
    // кисти на верёвке
    for (const x of [118, W - 118]) {
      G.ellipse(ctx, x, hy, 15, 17, { fill: '#E8B48A', stroke: C.ink, lw: 4, seed: 140 });
    }
    ctx.restore();
  }

  function titles(ctx, t) {
    if (t < ev.split) {
      const a1 = t < ev.rig ? 1 : 1 - fade(t, ev.rig, 0.3);
      if (a1 > 0.01) {
        ctx.save(); ctx.globalAlpha = a1;
        G.text(ctx, 'Какая сила нужна,', W / 2, SAFE_TOP + 34, { size: 60, fam: F, weight: 800, color: C.ink, align: 'center', baseline: 'middle', boil: 0 });
        G.text(ctx, 'чтобы поднять 500 кг?', W / 2, SAFE_TOP + 110, { size: 60, fam: F, weight: 800, color: C.ink, align: 'center', baseline: 'middle', boil: 0 });
        ctx.restore();
      }
    }
    for (const c of S.captions) {
      if (c.t < ev.rig) continue;
      if (t < c.t || t > c.end) continue;
      if (c.t >= ev.answer) continue; // на карточке ответа подпись не нужна
      const a = fade(t, c.t, 0.35) * (1 - fade(t, c.end - 0.2, 0.2));
      if (a <= 0.01) continue;
      ctx.save();
      ctx.globalAlpha = a;
      G.text(ctx, c.text, W / 2, SAFE_TOP + 40, { size: c.text.length > 26 ? 40 : 46, fam: F, weight: 700, color: C.muted, align: 'center', baseline: 'middle', boil: 0 });
      ctx.restore();
    }
  }

  function answerCard(ctx, t) {
    if (t < ev.answer) return;
    const p = ease.outBack(clamp((t - ev.answer) / 0.14), 1.6);
    ctx.save();
    ctx.globalAlpha = 0.6;
    ctx.fillStyle = C.bg;
    ctx.fillRect(0, 0, W, H);
    ctx.restore();

    const w = 880, h = 470, x = (W - w) / 2, y = 720;
    ctx.save();
    ctx.globalAlpha = 1;
    ctx.translate(W / 2, y + h / 2);
    ctx.scale(p, p);
    ctx.translate(-W / 2, -(y + h / 2));
    G.rrect(ctx, x, y, w, h, 26, { fill: C.cream, stroke: C.ink, lw: 6, seed: 120 });
    G.text(ctx, 'ОТВЕТ', W / 2, y + 70, { size: 38, fam: F, weight: 700, color: C.muted, align: 'center', baseline: 'middle', boil: 0 });
    G.text(ctx, 'F = 62,5 кг', W / 2, y + 192, { size: 118, fam: F, weight: 800, color: C.ok, align: 'center', baseline: 'middle', boil: 0 });
    G.text(ctx, '≈ 613 Н на каждую верёвку', W / 2, y + 288, { size: 46, fam: F, weight: 700, color: C.ink, align: 'center', baseline: 'middle', boil: 0 });
    G.text(ctx, '500 ÷ 2 ÷ 2 ÷ 2 = 62,5', W / 2, y + 368, { size: 44, fam: F, weight: 700, color: C.muted, align: 'center', baseline: 'middle', boil: 0 });
    ctx.restore();
  }

  function recap(ctx, t) {
    if (t < ev.recap) return;
    const a = fade(t, ev.recap, 0.4);
    ctx.save();
    ctx.globalAlpha = a * 0.94;
    G.rrect(ctx, 80, 1408, W - 160, 86, 16, { fill: C.ink, seed: 130 });
    G.text(ctx, 'Каждый подвижный блок делит силу вдвое', W / 2, 1451, { size: 33, fam: F, weight: 700, color: C.cream, align: 'center', baseline: 'middle', boil: 0 });
    ctx.restore();
  }

  function draw(ctx, t) {
    LIFT = ease.inOutCubic(clamp((t - 16.6) / 4.8)); // блок идёт вверх, пока тянут
    background(ctx, t);
    rig(ctx, t);
    ropes(ctx, t);
    pulleys(ctx, t);
    block(ctx, t);
    people(ctx, t);
    weights(ctx, t);
    titles(ctx, t);
    answerCard(ctx, t);
    recap(ctx, t);
  }

  Studio.film({ draw, post: { paper: 0.22, vignette: 0.16, grain: 0.05 } });
})();
