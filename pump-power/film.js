// THE FILM — чем выше вода, тем больше нужна мощность.
(function () {
  const U = globalThis.U, G = globalThis.G, S = globalThis.SCORE, Studio = globalThis.Studio;
  const { clamp, lerp, ease, pulse } = U;
  const { ev, BEAT, STEPS } = S;
  const W = G.W, H = G.H;

  const C = {
    bg: '#EAF2F7', ink: '#16232E', cream: '#FFFDF6', muted: '#5B6B78',
    blue: '#1F5FA8', blueDark: '#123E70', steel: '#B9C6D0', water: '#2E9BD6',
    tank: '#1B1B1B', ok: '#15803D', accent: '#C8102E',
  };
  const F = 'Inter';

  const GROUND = 1560;
  const PX_PER_M = 14.0;
  const PIPE_X = 420;
  const PUMP = { x: 330, y: 1440, w: 190, h: 120 };
  const CARD = { x: 620, y: 470, w: 400, h: 360 };

  const pop = (t, t0, dur = 0.32, k = 2.1) => (t < t0 ? 0 : ease.outBack(clamp((t - t0) / dur), k));
  const fade = (t, t0, dur = 0.4) => clamp((t - t0) / dur);

  function text(ctx, str, x, y, o = {}) {
    G.text(ctx, str, x, y, {
      size: o.size || 48, fam: o.fam || F, weight: o.weight || 800,
      color: o.color || C.ink, align: o.align || 'center', baseline: 'middle',
      stroke: o.stroke, strokeW: o.strokeW || 0, boil: 0,
    });
  }

  // текущая ступень: 0..4 и сглаженный подъём между ними
  function stepState(t) {
    let i = -1;
    for (let k = 0; k < ev.steps.length; k++) if (t >= ev.steps[k]) i = k;
    if (i < 0) return { i: -1, h: 0, prev: 0 };
    const t0 = ev.steps[i];
    const prev = i > 0 ? STEPS[i - 1].m : 0;
    const u = ease.inOutCubic(clamp((t - t0) / 0.9));
    return { i, h: lerp(prev, STEPS[i].m, u), prev };
  }

  function tankHeightPx(m) { return m * PX_PER_M; }

  function drawTank(ctx, cx, bottomY, w, h, fill) {
    // бак: цилиндр с крышкой
    G.rrect(ctx, cx - w / 2, bottomY - h, w, h, 18, { fill: C.tank, stroke: C.ink, lw: 5, seed: 11 });
    G.ellipse(ctx, cx, bottomY - h, w / 2, 16, { fill: '#2A2A2A', stroke: C.ink, lw: 4, seed: 12 });
    // уровень воды
    if (fill > 0.02) {
      const fh = (h - 18) * fill;
      ctx.save();
      ctx.beginPath();
      ctx.rect(cx - w / 2 + 5, bottomY - 5 - fh, w - 10, fh);
      ctx.clip();
      ctx.fillStyle = C.water;
      ctx.fillRect(cx - w / 2 + 5, bottomY - 5 - fh, w - 10, fh);
      ctx.restore();
      G.line(ctx, [[cx - w / 2 + 8, bottomY - 5 - fh], [cx + w / 2 - 8, bottomY - 5 - fh]],
        { color: 'rgba(255,255,255,0.55)', lw: 3, seed: 13 });
    }
    // обручи
    for (const k of [0.28, 0.62]) {
      G.line(ctx, [[cx - w / 2 + 3, bottomY - h * k], [cx + w / 2 - 3, bottomY - h * k]],
        { color: 'rgba(255,255,255,0.18)', lw: 4, seed: 14 });
    }
  }

  function pump(ctx, t) {
    const { x, y, w, h } = PUMP;
    // опора
    G.rrect(ctx, x - 24, GROUND - 18, w + 48, 22, 6, { fill: C.blueDark, stroke: C.ink, lw: 4, seed: 21 });
    // корпус насоса
    G.rrect(ctx, x, y, w, h, 14, { fill: C.blue, stroke: C.ink, lw: 5, seed: 22 });
    // мотор
    G.rrect(ctx, x + w - 64, y + 22, 58, h - 44, 10, { fill: '#2D6FB5', stroke: C.ink, lw: 4, seed: 23 });
    for (let i = 0; i < 4; i++) {
      G.line(ctx, [[x + w - 54, y + 34 + i * 16], [x + w - 20, y + 34 + i * 16]], { color: 'rgba(255,255,255,0.25)', lw: 3, seed: 24 + i });
    }
    // улитка
    G.ellipse(ctx, x + 58, y + h / 2, 52, 52, { fill: '#3E86C4', stroke: C.ink, lw: 5, seed: 28 });
    G.ellipse(ctx, x + 58, y + h / 2, 18, 18, { fill: C.steel, stroke: C.ink, lw: 3, seed: 29 });
    // выходная труба
    G.rrect(ctx, x + 92, y + h / 2 - 18, 62, 36, 8, { fill: C.steel, stroke: C.ink, lw: 4, seed: 30 });
    // вода из патрубка
    const wob = Math.sin(t * 9) * 3;
    ctx.save();
    ctx.strokeStyle = C.water;
    ctx.lineWidth = 12;
    ctx.lineCap = 'round';
    ctx.beginPath();
    ctx.moveTo(x + 154, y + h / 2 + 4);
    ctx.bezierCurveTo(x + 210, y + h / 2 + 2, x + 226, GROUND - 60 + wob, x + 262, GROUND - 40);
    ctx.stroke();
    ctx.restore();
    // брызги
    for (let i = 0; i < 5; i++) {
      const ph = (t * 1.6 + i / 5) % 1;
      G.ellipse(ctx, x + 262 + ph * 26, GROUND - 40 - Math.sin(ph * Math.PI) * 18,
        4, 4, { fill: C.water, seed: 31 + i });
    }
  }

  function riser(ctx, tankBottomY) {
    // вертикальная труба от насоса к баку
    const top = tankBottomY + 6;
    G.rrect(ctx, PIPE_X - 16, top, 32, GROUND - 20 - top, 6, { fill: C.steel, stroke: C.ink, lw: 5, seed: 41 });
    // фланцы
    for (const yy of [top + 30, GROUND - 120]) {
      G.rrect(ctx, PIPE_X - 24, yy, 48, 16, 4, { fill: '#9FB0BC', stroke: C.ink, lw: 3, seed: 42 });
    }
  }

  function ruler(ctx, t, hM) {
    const a = fade(t, ev.steps[0] - 0.4, 0.5);
    if (a <= 0) return;
    const x = 150;
    ctx.save();
    ctx.globalAlpha = 0.9 * a;
    G.line(ctx, [[x, PUMP.y], [x, PUMP.y - 40 - 80 * PX_PER_M]], { color: 'rgba(22,35,46,0.35)', lw: 4, seed: 51 });
    for (let m = 10; m <= 80; m += 10) {
      const y = PUMP.y - m * PX_PER_M;
      const big = m % 20 === 0;
      G.line(ctx, [[x - (big ? 22 : 12), y], [x, y]], { color: 'rgba(22,35,46,0.45)', lw: big ? 4 : 3, seed: 52 + m });
      if (big) text(ctx, `${m}`, x - 42, y, { size: 30, weight: 700, color: C.muted });
    }
    // текущая высота
    const y = PUMP.y - hM * PX_PER_M;
    G.line(ctx, [[x, y], [PIPE_X - 30, y]], { color: C.accent, lw: 4, seed: 60 });
    text(ctx, `${Math.round(hM)} м`, 250, y - 26, { size: 40, color: C.accent });
    ctx.restore();
  }

  function card(ctx, t, st) {
    if (st.i < 0) return;
    const a = fade(t, ev.steps[0], 0.35);
    if (a <= 0) return;
    const s = STEPS[st.i];
    const t0 = ev.steps[st.i];
    const p = pop(t, t0, 0.4, 1.9);
    ctx.save();
    ctx.globalAlpha = a;
    G.rrect(ctx, CARD.x, CARD.y, CARD.w, CARD.h, 22, { fill: C.cream, stroke: C.ink, lw: 5, seed: 71 });
    ctx.translate(CARD.x + CARD.w / 2, CARD.y + CARD.h / 2);
    ctx.scale(lerp(0.92, 1, p), lerp(0.92, 1, p));
    ctx.translate(-(CARD.x + CARD.w / 2), -(CARD.y + CARD.h / 2));

    text(ctx, 'ВЫСОТА', CARD.x + CARD.w / 2, CARD.y + 46, { size: 26, weight: 700, color: C.muted });
    text(ctx, `${s.m} м`, CARD.x + CARD.w / 2, CARD.y + 100, { size: 72, color: C.blue });
    G.line(ctx, [[CARD.x + 40, CARD.y + 146], [CARD.x + CARD.w - 40, CARD.y + 146]], { color: 'rgba(22,35,46,0.15)', lw: 3, seed: 72 });
    text(ctx, 'ДАВЛЕНИЕ', CARD.x + 30, CARD.y + 186, { size: 21, weight: 700, color: C.muted, align: 'left' });
    text(ctx, `${s.bar} бар`, CARD.x + CARD.w - 30, CARD.y + 186, { size: 34, align: 'right', color: C.ink });
    text(ctx, 'МОЩНОСТЬ', CARD.x + 30, CARD.y + 244, { size: 21, weight: 700, color: C.muted, align: 'left' });
    text(ctx, `${s.hp} л.с.`, CARD.x + CARD.w - 30, CARD.y + 244, { size: 34, align: 'right', color: C.ink });
    text(ctx, 'ТРУБА', CARD.x + 30, CARD.y + 300, { size: 21, weight: 700, color: C.muted, align: 'left' });
    text(ctx, s.pipe, CARD.x + CARD.w - 30, CARD.y + 300, { size: 32, align: 'right', color: C.ink });
    ctx.restore();
  }

  function hookTitle(ctx, t) {
    if (t > ev.steps[0] - 0.2) return;
    const a = 1 - fade(t, ev.steps[0] - 0.6, 0.4);
    ctx.save();
    ctx.globalAlpha = a;
    text(ctx, 'Сколько мощности', W / 2, 250, { size: 62 });
    text(ctx, 'нужно насосу?', W / 2, 320, { size: 62 });
    ctx.restore();
  }

  function ruleCard(ctx, t) {
    if (t < ev.rule) return;
    const a = fade(t, ev.rule, 0.35);
    const p = pop(t, ev.rule, 0.4, 1.9);
    ctx.save();
    ctx.globalAlpha = a;
    ctx.translate(W / 2, 900);
    ctx.scale(lerp(0.9, 1, p), lerp(0.9, 1, p));
    G.rrect(ctx, -440, -220, 880, 400, 26, { fill: C.cream, stroke: C.ink, lw: 6, seed: 81 });
    text(ctx, '10 метров воды', 0, -140, { size: 46, color: C.muted });
    text(ctx, '≈ 1 бар', 0, -50, { size: 96, color: C.ok });
    text(ctx, 'Каждые 10 м столба дают +1 бар', 0, 60, { size: 32, weight: 700, color: C.muted });
    text(ctx, 'и требуют больше мощности', 0, 106, { size: 32, weight: 700, color: C.muted });
    ctx.restore();
  }

  function table(ctx, t) {
    if (t < ev.table) return;
    const a = fade(t, ev.table, 0.4);
    ctx.save();
    ctx.globalAlpha = a;
    G.rrect(ctx, 80, 590, W - 160, 660, 24, { fill: C.cream, stroke: C.ink, lw: 6, seed: 91 });
    text(ctx, 'ПОДБОР НАСОСА', W / 2, 640, { size: 34, color: C.muted });
    const cols = [200, 420, 640, 860];
    const head = ['высота', 'давление', 'мощность', 'труба'];
    for (let i = 0; i < 4; i++) {
      text(ctx, head[i], cols[i], 660, { size: 24, weight: 700, color: C.muted });
    }
    G.line(ctx, [[110, 690], [W - 110, 690]], { color: 'rgba(22,35,46,0.2)', lw: 3, seed: 92 });
    STEPS.forEach((s, i) => {
      const y = 742 + i * 98;
      const p = pop(t, ev.table + 0.15 + i * 0.12, 0.35, 1.8);
      ctx.save();
      ctx.globalAlpha = a * clamp(p);
      text(ctx, `${s.m} м`, cols[0], y, { size: 40, color: C.blue });
      text(ctx, `${s.bar}`, cols[1], y, { size: 40 });
      text(ctx, `${s.hp}`, cols[2], y, { size: 40 });
      text(ctx, s.pipe, cols[3], y, { size: 34, color: C.muted });
      ctx.restore();
      if (i < 4) G.line(ctx, [[110, y + 48], [W - 110, y + 48]], { color: 'rgba(22,35,46,0.10)', lw: 2, seed: 93 + i });
    });
    text(ctx, 'при расходе 30–60 л/мин', W / 2, 1215, { size: 28, weight: 700, color: C.muted });
    ctx.restore();
  }

  function draw(ctx, t) {
    ctx.fillStyle = C.bg;
    ctx.fillRect(0, 0, W, H);
    const g = ctx.createLinearGradient(0, 0, 0, 600);
    g.addColorStop(0, 'rgba(160,205,235,0.55)');
    g.addColorStop(1, 'rgba(160,205,235,0)');
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, W, 600);

    // земля
    G.rrect(ctx, 0, GROUND - 8, W, H - GROUND + 8, 0, { fill: '#D8C9A6', stroke: C.ink, lw: 5, seed: 3 });

    const st = stepState(t);
    const hPx = tankHeightPx(st.h);
    const tankBottom = PUMP.y - 6 - hPx;

    if (t < ev.table) {
      hookTitle(ctx, t);
      if (st.i >= 0) {
        riser(ctx, tankBottom);
        drawTank(ctx, PIPE_X, tankBottom, 190, 118, clamp((t - ev.steps[st.i]) / 1.6));
        pump(ctx, t);
        ruler(ctx, t, st.h);
        card(ctx, t, st);
      }
    }
    ruleCard(ctx, t);
    table(ctx, t);
  }

  Studio.film({ draw, post: { paper: 0.22, vignette: 0.14, grain: 0.05 } });
})();
