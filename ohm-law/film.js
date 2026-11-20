// THE FILM — закон Ома в трёх героях: Вольт толкает, Ампер бежит, Ом мешает.
(function () {
  const U = globalThis.U, G = globalThis.G, S = globalThis.SCORE, Studio = globalThis.Studio;
  const { clamp, lerp, ease, pulse } = U;
  const { ev, BEAT } = S;
  const W = G.W, H = G.H;

  const C = {
    bg: '#F3E9D2', ink: '#221F1A', cream: '#FFFDF6', muted: '#6B6255',
    v: '#7EC8E3', vInk: '#2C6B84', i: '#F2E07A', iInk: '#8A7A12',
    r: '#F0A868', rInk: '#9C5218', wire: '#EFE3C6', wireInk: '#2B2620',
    accent: '#C8102E', ok: '#15803D',
  };
  const F = 'Inter';

  // ---------- геометрия ----------
  const TITLE_Y = 230;
  const BADGE_Y = 400, BADGE_R = 58;
  const WIRE = { x0: 50, x1: 1030, y: 620, h: 280 };
  const FORM = { x: 90, y: 1000, w: 900, h: 260 };
  const RECAP_Y = 1330;

  const pop = (t, t0, dur = 0.32, k = 2.1) => (t < t0 ? 0 : ease.outBack(clamp((t - t0) / dur), k));
  const fade = (t, t0, dur = 0.4) => clamp((t - t0) / dur);

  function text(ctx, str, x, y, o = {}) {
    G.text(ctx, str, x, y, {
      size: o.size || 48, fam: o.fam || F, weight: o.weight || 800,
      color: o.color || C.ink, align: o.align || 'center', baseline: 'middle',
      stroke: o.stroke, strokeW: o.strokeW || 0, boil: 0,
    });
  }

  function badge(ctx, x, y, letter, color, t, t0) {
    const p = pop(t, t0, 0.34, 2.2);
    if (p <= 0.01) return;
    ctx.save();
    ctx.translate(x, y);
    ctx.scale(p, p);
    G.ellipse(ctx, 0, 0, BADGE_R, BADGE_R, { fill: color, stroke: C.ink, lw: 5, seed: 7 });
    text(ctx, letter, 0, 2, { size: 66, color: C.ink });
    ctx.restore();
  }

  // ---------- персонажи ----------
  function eyes(ctx, x, y, look = 0, mood = 'normal') {
    const dx = look * 6;
    if (mood === 'squeeze') {
      G.line(ctx, [[x - 20, y - 6], [x - 8, y + 2]], { color: C.ink, lw: 4, seed: 11 });
      G.line(ctx, [[x + 8, y + 2], [x + 20, y - 6]], { color: C.ink, lw: 4, seed: 12 });
      G.line(ctx, [[x - 8, y + 14], [x + 8, y + 14]], { color: C.ink, lw: 4, seed: 13 });
      return;
    }
    G.ellipse(ctx, x - 14 + dx, y, 5, 7, { fill: C.ink, seed: 14 });
    G.ellipse(ctx, x + 14 + dx, y, 5, 7, { fill: C.ink, seed: 15 });
  }

  function volt(ctx, t) {
    const a = pop(t, ev.volt, 0.45, 1.7);
    if (a <= 0.01) return;
    const bob = Math.sin(t * 6) * 4;
    const push = t > ev.ampere ? 0.5 + 0.5 * Math.sin(t * 6) : 0;
    const x = 215, y = WIRE.y + 112 + bob;
    ctx.save();
    ctx.globalAlpha = clamp(a);
    ctx.translate(x, y);
    ctx.scale(1.36, 1.36);
    // тело
    G.ellipse(ctx, 0, 0, 78, 88, { fill: C.v, stroke: C.ink, lw: 6, seed: 21 });
    // ноги
    G.line(ctx, [[-26, 74], [-38, 118]], { color: C.v, lw: 18, seed: 22 });
    G.line(ctx, [[24, 74], [40, 116]], { color: C.v, lw: 18, seed: 23 });
    G.rrect(ctx, -52, 112, 34, 14, 6, { fill: C.ink, seed: 24 });
    G.rrect(ctx, 26, 110, 34, 14, 6, { fill: C.ink, seed: 25 });
    // руки толкают вправо
    const hx = 96 + push * 16;
    G.line(ctx, [[54, -10], [hx - 6, 6]], { color: C.v, lw: 18, seed: 26 });
    G.line(ctx, [[54, 26], [hx - 2, 34]], { color: C.v, lw: 18, seed: 27 });
    G.ellipse(ctx, hx + 4, 8, 15, 15, { fill: C.v, stroke: C.ink, lw: 4, seed: 28 });
    G.ellipse(ctx, hx + 6, 36, 14, 14, { fill: C.v, stroke: C.ink, lw: 4, seed: 29 });
    // лицо
    eyes(ctx, 0, -18, 0.6);
    G.line(ctx, [[-14, 26], [16, 24]], { color: C.ink, lw: 5, seed: 30 });
    ctx.restore();
  }

  function ampereSpeed(t) {
    if (t < ev.rule) return 1;
    return lerp(1, 0.28, ease.inOutCubic(clamp((t - ev.rule) / 2.5)));
  }

  function amperePos(t) {
    const t0 = ev.ampere;
    const span = 430;
    let s = 0;
    const dt = 0.05;
    for (let x = t0; x < t; x += dt) s += ampereSpeed(x) * 120 * dt;
    return 300 + (s % span);
  }

  function ampere(ctx, t) {
    const a = pop(t, ev.ampere, 0.4, 1.8);
    if (a <= 0.01) return;
    const x = amperePos(t);
    const run = Math.sin(t * 14) * 4;
    ctx.save();
    ctx.globalAlpha = clamp(a);
    ctx.translate(x, WIRE.y + 138 + run);
    ctx.scale(1.36, 1.36);
    // вытянутое тело
    G.ellipse(ctx, 0, 0, 72, 56, { fill: C.i, stroke: C.ink, lw: 6, seed: 41 });
    // лапы
    G.line(ctx, [[-30, 42], [-48, 74]], { color: C.i, lw: 15, seed: 42 });
    G.line(ctx, [[28, 42], [50, 72]], { color: C.i, lw: 15, seed: 43 });
    G.line(ctx, [[-34, -20], [-6, -34]], { color: C.i, lw: 14, seed: 44 });
    // хвост-искра
    G.line(ctx, [[-52, 0], [-84, -10]], { color: C.i, lw: 10, seed: 45 });
    // лицо: бежит, рот открыт
    G.ellipse(ctx, 14, -14, 5, 7, { fill: C.ink, seed: 46 });
    G.ellipse(ctx, 34, -14, 5, 7, { fill: C.ink, seed: 47 });
    G.ellipse(ctx, 26, 10, 12, 9, { fill: C.ink, seed: 48 });
    ctx.restore();
  }

  function ohm(ctx, t) {
    const a = pop(t, ev.ohm, 0.4, 1.9);
    if (a <= 0.01) return;
    // падает на провод и сжимает его
    const drop = clamp((t - ev.ohm) / 0.55);
    const yOff = (1 - ease.outBounce(drop)) * -260;
    const squeeze = t < ev.ohm + 0.55 ? 0.35 : lerp(0.35, 1, clamp((t - ev.ohm - 0.55) / 0.6));
    const x = 800, y = WIRE.y - 55 + yOff;
    ctx.save();
    ctx.globalAlpha = clamp(a);
    ctx.translate(x, y);
    // рога
    G.poly(ctx, [[-34, -46], [-20, -84], [-6, -50]], { fill: C.r, stroke: C.ink, lw: 4, seed: 51 });
    G.poly(ctx, [[34, -46], [20, -84], [6, -50]], { fill: C.r, stroke: C.ink, lw: 4, seed: 52 });
    // тело
    G.ellipse(ctx, 0, 0, 54, 58, { fill: C.r, stroke: C.ink, lw: 6, seed: 53 });
    // руки сжимают провод
    const hx = 62 * squeeze, hy = 92;
    G.line(ctx, [[-40, 20], [-hx, hy]], { color: C.r, lw: 15, seed: 54 });
    G.line(ctx, [[40, 20], [hx, hy]], { color: C.r, lw: 15, seed: 55 });
    G.ellipse(ctx, -hx, hy, 13, 11, { fill: C.r, stroke: C.ink, lw: 4, seed: 56 });
    G.ellipse(ctx, hx, hy, 13, 11, { fill: C.r, stroke: C.ink, lw: 4, seed: 57 });
    eyes(ctx, 0, -14, 0, 'squeeze');
    G.line(ctx, [[-16, 22], [16, 22]], { color: C.ink, lw: 5, seed: 58 });
    ctx.restore();
  }

  // ---------- провод ----------
  function wire(ctx, t) {
    const a = fade(t, ev.wire, 0.5);
    if (a <= 0) return;
    const squeeze = t < ev.ohm + 0.6 ? 0 : clamp((t - ev.ohm - 0.6) / 0.8);
    const extra = t >= ev.rule ? ease.inOutCubic(clamp((t - ev.rule) / 2.4)) : 0;
    const k = Math.max(squeeze, extra);
    const x0 = WIRE.x0, x1 = WIRE.x1, y = WIRE.y, h = WIRE.h;

    ctx.save();
    ctx.globalAlpha = a;
    // корпус провода: сверху и снизу выемка у x=800
    const notch = 72 * k;
    const pts = [
      [x0, y], [720, y], [800, y + notch], [880, y], [x1, y],
      [x1, y + h], [880, y + h], [800, y + h - notch], [720, y + h], [x0, y + h],
    ];
    G.poly(ctx, pts, { fill: C.wire, stroke: C.wireInk, lw: 9, seed: 61 });
    // обмотка
    for (let i = 0; i < 10; i++) {
      const xx = x0 + 30 + i * 96;
      if (xx > 700 && xx < 900) continue;
      G.line(ctx, [[xx, y + 14], [xx, y + h - 14]], { color: 'rgba(43,38,32,0.18)', lw: 4, seed: 62 + i });
    }
    ctx.restore();

    // бегущие заряды
    if (t >= ev.ampere) {
      const sp = ampereSpeed(t);
      for (let i = 0; i < 7; i++) {
        const phase = (t * 0.55 * sp + i / 7) % 1;
        const xx = lerp(300, 880, phase);
        const yy = y + h / 2 + Math.sin(phase * 6.28 + i) * 18;
        ctx.save();
        ctx.globalAlpha = 0.55 * a;
        G.ellipse(ctx, xx, yy, 7, 7, { fill: C.iInk, seed: 70 + i });
        ctx.restore();
      }
    }
  }

  // ---------- формулы ----------
  function formulaCard(ctx, t) {
    if (t < ev.wire + 0.4) return;
    const p = pop(t, ev.wire + 0.4, 0.4, 1.8);
    ctx.save();
    ctx.globalAlpha = clamp(p);
    G.rrect(ctx, FORM.x, FORM.y, FORM.w, FORM.h, 24, { fill: C.cream, stroke: C.ink, lw: 6, seed: 80 });

    // I = V / R
    const big = ev.numbers > t;
    if (big) {
      const on = { I: t >= ev.ampere, V: t >= ev.volt, R: t >= ev.ohm };
      const dim = '#D3C8B0';
      const words = [['I', 290], ['=', 385], ['V', 495], ['/', 585], ['R', 665]];
      for (const [ch, x] of words) {
        const col = ch === 'I' ? (on.I ? C.iInk : dim) : ch === 'V' ? (on.V ? C.vInk : dim)
          : ch === 'R' ? (on.R ? C.rInk : dim) : ch === '=' ? C.ink : C.muted;
        text(ctx, ch, x, FORM.y + 118, { size: 96, color: col });
      }
      text(ctx, 'ток = напряжение / сопротивление', W / 2, FORM.y + 206, { size: 30, weight: 700, color: C.muted });
    } else {
      // числа: I = 12 В / 4 Ом = 3 А
      text(ctx, 'I =', 210, FORM.y + 120, { size: 76, color: C.iInk });
      text(ctx, '12 В', 400, FORM.y + 92, { size: 62, color: C.vInk });
      G.line(ctx, [[316, FORM.y + 122], [500, FORM.y + 122]], { color: C.ink, lw: 5, seed: 82 });
      text(ctx, '4 Ом', 400, FORM.y + 172, { size: 62, color: C.rInk });
      if (t >= ev.result) {
        const q = pop(t, ev.result, 0.35, 2.2);
        ctx.save(); ctx.translate(700, FORM.y + 128); ctx.scale(q, q);
        text(ctx, '= 3 А', 0, 0, { size: 82, color: C.ok });
        ctx.restore();
      }
    }
    ctx.restore();
  }

  function ruleCard(ctx, t) {
    if (t < ev.rule) return;
    const a = fade(t, ev.rule, 0.35);
    ctx.save();
    ctx.globalAlpha = a;
    G.rrect(ctx, FORM.x, FORM.y, FORM.w, FORM.h, 24, { fill: C.cream, stroke: C.ink, lw: 6, seed: 90 });
    text(ctx, 'R ↑', 300, FORM.y + 96, { size: 82, color: C.rInk });
    text(ctx, '→', 500, FORM.y + 96, { size: 70, color: C.muted });
    text(ctx, 'I ↓', 700, FORM.y + 96, { size: 82, color: C.iInk });
    text(ctx, 'при том же напряжении V', W / 2, FORM.y + 190, { size: 34, weight: 700, color: C.muted });
    ctx.restore();
  }

  function recap(ctx, t) {
    if (t < ev.recap) return;
    const a = fade(t, ev.recap, 0.4);
    ctx.save();
    ctx.globalAlpha = a;
    text(ctx, 'I = V / R', W / 2, RECAP_Y, { size: 64, color: C.ink });
    text(ctx, 'V = I · R     R = V / I', W / 2, RECAP_Y + 66, { size: 36, weight: 700, color: C.muted });
    ctx.restore();
  }

  function labels(ctx, t) {
    if (t >= ev.volt) {
      const a = fade(t, ev.volt, 0.3) * (1 - fade(t, ev.recap, 0.3));
      if (a > 0.01) {
        ctx.save(); ctx.globalAlpha = a;
        text(ctx, 'ВОЛЬТ · V', 215, 958, { size: 38, color: C.vInk });
        ctx.restore();
      }
    }
    if (t >= ev.ampere) {
      const a = fade(t, ev.ampere, 0.3) * (1 - fade(t, ev.recap, 0.3));
      if (a > 0.01) {
        ctx.save(); ctx.globalAlpha = a;
        text(ctx, 'АМПЕР · I', 555, 958, { size: 38, color: C.iInk });
        ctx.restore();
      }
    }
    if (t >= ev.ohm) {
      const a = fade(t, ev.ohm, 0.3) * (1 - fade(t, ev.recap, 0.3));
      if (a > 0.01) {
        ctx.save(); ctx.globalAlpha = a;
        text(ctx, 'ОМ · R', 800, 470, { size: 38, color: C.rInk });
        ctx.restore();
      }
    }
  }

  function titles(ctx, t) {
    if (t < ev.wire + 0.5) {
      ctx.save();
      ctx.globalAlpha = 1 - fade(t, ev.wire, 0.3);
      text(ctx, 'ЗАКОН ОМА', W / 2, TITLE_Y, { size: 92, color: C.ink });
      text(ctx, 'три величины и одна формула', W / 2, TITLE_Y + 76, { size: 36, weight: 700, color: C.muted });
      ctx.restore();
    } else {
      ctx.save();
      ctx.globalAlpha = fade(t, ev.wire + 0.3, 0.4);
      text(ctx, 'ЗАКОН ОМА', W / 2, 240, { size: 46, color: C.muted });
      ctx.restore();
    }
    // бейджи V, I, R на старте
    const ba = 1 - fade(t, ev.ohm - 0.1, 0.35); // бейджи уходят, когда все трое вышли
    if (ba > 0.01) {
      ctx.save(); ctx.globalAlpha = ba;
      badge(ctx, 300, BADGE_Y, 'V', C.v, t, ev.vBadge);
      badge(ctx, 540, BADGE_Y, 'I', C.i, t, ev.iBadge);
      badge(ctx, 780, BADGE_Y, 'R', C.r, t, ev.rBadge);
      ctx.restore();
    }
  }

  function draw(ctx, t) {
    ctx.fillStyle = C.bg;
    ctx.fillRect(0, 0, W, H);
    const g = ctx.createLinearGradient(0, 0, 0, H * 0.5);
    g.addColorStop(0, 'rgba(255,214,150,0.32)');
    g.addColorStop(1, 'rgba(255,214,150,0)');
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, W, H * 0.5);

    titles(ctx, t);
    wire(ctx, t);
    volt(ctx, t);
    ampere(ctx, t);
    ohm(ctx, t);
    labels(ctx, t);
    formulaCard(ctx, t);
    if (t >= ev.rule) ruleCard(ctx, t);
    recap(ctx, t);

    // нижняя плашка-вывод
    if (t >= ev.rule && t < ev.recap) {
      const a = fade(t, ev.rule, 0.4) * (1 - fade(t, ev.recap - 0.2, 0.2));
      ctx.save();
      ctx.globalAlpha = a * 0.94;
      G.rrect(ctx, 80, 1390, W - 160, 86, 16, { fill: C.ink, seed: 100 });
      text(ctx, 'Больше сопротивление — меньше ток', W / 2, 1433, { size: 32, weight: 700, color: C.cream });
      ctx.restore();
    }
  }

  Studio.film({ draw, post: { paper: 0.22, vignette: 0.16, grain: 0.05 } });
})();
