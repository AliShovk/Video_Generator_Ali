// THE FILM — анекдот: два персонажа в кабинете, крупный план, мимика.
(function () {
  const U = globalThis.U, G = globalThis.G, S = globalThis.SCORE, Studio = globalThis.Studio;
  const { clamp, lerp, ease } = U;
  const { ev } = S;
  const W = G.W, H = G.H;

  const C = {
    wall: '#F5E2C4', wall2: '#EDD3AE', ink: '#2A2118', cream: '#FFF8EA',
    accent: '#E07A2A', coat: '#FCF8F0', coatShade: '#E9E1D2', skin: '#E9B98F',
    skin2: '#D9A276', hair: '#4A3524', grey: '#D8CBB8', sweater: '#4E7EA8',
    sky: '#BFE3F2',
  };
  const F = 'Inter';

  const PAT = { x: 300, y: 820, s: 1.0 };
  const DOC = { x: 790, y: 780, s: 1.02 };

  const fade = (t, t0, d = 0.4) => clamp((t - t0) / d);
  const out = (t, t0, d = 0.3) => 1 - clamp((t - t0) / d);

  function text(ctx, str, x, y, o = {}) {
    G.text(ctx, str, x, y, {
      size: o.size || 48, fam: F, weight: o.weight || 800,
      color: o.color || C.ink, align: o.align || 'center', baseline: 'middle',
    });
  }

  // ---------- фон ----------
  function room(ctx, t) {
    const g = ctx.createLinearGradient(0, 0, 0, H);
    g.addColorStop(0, C.wall);
    g.addColorStop(1, C.wall2);
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, W, H);

    // окно за спиной пациента
    G.rrect(ctx, 40, 230, 300, 380, 8, { fill: C.sky, seed: 3 });
    G.rrect(ctx, 40, 230, 300, 110, 8, { fill: '#D6EEF8', seed: 4 });
    ctx.save();
    ctx.strokeStyle = '#FFF8EA';
    ctx.lineWidth = 12;
    ctx.strokeRect(40, 230, 300, 380);
    ctx.beginPath();
    ctx.moveTo(190, 230); ctx.lineTo(190, 610);
    ctx.moveTo(40, 420); ctx.lineTo(340, 420);
    ctx.stroke();
    ctx.restore();

    // плакат за врачом
    G.rrect(ctx, 700, 250, 300, 330, 8, { fill: '#FBF3E3', seed: 12, stroke: '#D8C3A2', strokeW: 5 });
    G.ellipse(ctx, 850, 350, 40, 40, { fill: '#E9D7B8', seed: 13 });
    G.rrect(ctx, 740, 420, 220, 10, 5, { fill: '#D8C3A2', seed: 14 });
    G.rrect(ctx, 740, 452, 170, 10, 5, { fill: '#D8C3A2', seed: 15 });
    G.rrect(ctx, 740, 484, 190, 10, 5, { fill: '#D8C3A2', seed: 16 });
    // полка
    G.rrect(ctx, 640, 600, 380, 16, 6, { fill: '#D8B98E', seed: 17 });
    G.rrect(ctx, 690, 540, 60, 60, 8, { fill: '#DDE6E9', seed: 18 });
    G.rrect(ctx, 780, 552, 44, 48, 8, { fill: '#CFE0D8', seed: 19 });
  }

  // ---------- персонаж (по грудь) ----------
  function bust(ctx, o) {
    const { x, y, s = 1, facing = 1, t = 0 } = o;
    const skin = o.skin || C.skin;
    const cloth = o.cloth;

    ctx.save();
    ctx.translate(x, y);
    ctx.scale(facing * s, s);

    const br = 1 + Math.sin(t * 1.5 + (o.breathOff || 0)) * 0.005;
    ctx.save();
    ctx.scale(1, br);

    // плечи и корпус
    G.rrect(ctx, -236, 198, 472, 300, 116, { fill: cloth, seed: 20 });
    G.rrect(ctx, -206, 430, 412, 500, 54, { fill: cloth, seed: 98 });
    // руки
    G.rrect(ctx, -282, 320, 86, 520, 43, { fill: cloth, seed: 99 });
    G.rrect(ctx, 196, 320, 86, 520, 43, { fill: cloth, seed: 100 });
    ctx.save();
    ctx.globalAlpha = 0.07;
    G.rrect(ctx, -282, 320, 20, 520, 10, { fill: '#000000', seed: 101 });
    G.rrect(ctx, 262, 320, 20, 520, 10, { fill: '#000000', seed: 102 });
    G.rrect(ctx, -236, 198, 472, 26, 13, { fill: '#000000', seed: 103 });
    ctx.restore();
    // шея
    G.rrect(ctx, -52, 70, 104, 150, 26, { fill: C.skin2, seed: 21 });

    if (o.coat) {
      // рубашка и галстук
      G.poly(ctx, [[-52, 210], [52, 210], [112, 330], [-112, 330]], { fill: '#8FB6D2', seed: 22 });
      
      // лацканы халата
      G.poly(ctx, [[-52, 200], [-6, 200], [-70, 470], [-170, 400]], { fill: C.coat, seed: 24 });
      G.poly(ctx, [[52, 200], [6, 200], [70, 470], [170, 400]], { fill: C.coat, seed: 25 });
      // стетоскоп
      ctx.save();
      ctx.strokeStyle = '#3A3F44';
      ctx.lineWidth = 9;
      ctx.beginPath();
      ctx.moveTo(-64, 214);
      ctx.bezierCurveTo(-96, 380, -30, 430, 0, 470);
      ctx.bezierCurveTo(30, 430, 96, 380, 64, 214);
      ctx.stroke();
      ctx.restore();
      G.ellipse(ctx, 0, 486, 26, 26, { fill: '#A9B6BC', seed: 26, stroke: '#7E8C92', strokeW: 4 });
      // карман
      G.rrect(ctx, 96, 520, 96, 12, 5, { fill: 'rgba(0,0,0,0.08)', seed: 27 });
    } else {
      // ворот свитера
      G.ellipse(ctx, 0, 214, 104, 30, { fill: '#3E6A92', seed: 28 });
      // молния
      G.rrect(ctx, -5, 230, 10, 500, 5, { fill: 'rgba(0,0,0,0.12)', seed: 29 });
      // воротник-стойка
      G.rrect(ctx, -70, 190, 140, 26, 12, { fill: '#3E6A92', seed: 30 });
    }
    ctx.restore();

    // голова
    ctx.save();
    ctx.rotate(o.tilt || 0);

    G.ellipse(ctx, 0, 0, 126, 142, { fill: skin, seed: 31 });
    G.ellipse(ctx, -122, 12, 20, 32, { fill: C.skin2, seed: 32 });
    G.ellipse(ctx, 122, 12, 20, 32, { fill: C.skin2, seed: 33 });

    // волосы
    if (o.hairStyle === 'hair') {
      G.ellipse(ctx, 0, -114, 126, 64, { fill: C.hair, seed: 34 });
      G.ellipse(ctx, -110, -30, 24, 56, { fill: C.hair, seed: 35 });
      G.ellipse(ctx, 110, -30, 24, 56, { fill: C.hair, seed: 36 });
    } else {
      G.ellipse(ctx, 0, -52, 108, 62, { fill: '#EFDCC2', seed: 37 });
      G.ellipse(ctx, -112, -8, 22, 48, { fill: C.grey, seed: 38 });
      G.ellipse(ctx, 112, -8, 22, 48, { fill: C.grey, seed: 39 });
    }

    // брови
    const brow = o.brow || 0;
    G.line(ctx, [[-74, -52 + brow], [-30, -60 + brow]], { color: o.hairStyle === 'hair' ? C.hair : '#9B8B76', lw: 10, seed: 40 });
    G.line(ctx, [[30, -60 + brow], [74, -52 + brow]], { color: o.hairStyle === 'hair' ? C.hair : '#9B8B76', lw: 10, seed: 41 });

    // глаза: белок, зрачок, веки
    let blink = ((t + (o.blinkOff || 0)) % 3.4) < 0.12 ? 0.12 : 1;
    if (o.noBlink && t > ev.punch - 0.1) blink = 1;
    const rx = o.wide ? 24 : 21, ry = o.wide ? 20 : 17;
    for (const ex of [-52, 52]) {
      G.ellipse(ctx, ex, -4, rx, ry * blink, { fill: '#FFFFFF', seed: 42 });
      G.ellipse(ctx, ex, -2, 10, 12 * blink, { fill: C.ink, seed: 43 });
      G.ellipse(ctx, ex + 3, -6, 3.4, 3.4 * blink, { fill: '#FFFFFF', seed: 44 });
    }

    // нос
    G.line(ctx, [[4, 14], [14, 48], [-2, 54]], { color: C.skin2, lw: 8, seed: 45 });

    // рот
    const sp = o.speaking || 0;
    if (sp > 0.2) {
      const open = 14 + sp * (16 + Math.sin(t * 24) * 10);
      G.ellipse(ctx, 0, 96, 40, open, { fill: '#6E3B33', seed: 46 });
      G.rrect(ctx, -26, 96 - open + 4, 52, 8, 4, { fill: '#FFF6EC', seed: 47 });
    } else {
      G.line(ctx, [[-34, 96], [0, 102], [34, 96]], { color: '#8A4A3E', lw: 8, seed: 48 });
    }

    if (o.glasses) {
      ctx.save();
      ctx.strokeStyle = '#3A3F44';
      ctx.lineWidth = 6;
      ctx.beginPath();
      ctx.arc(-52, -4, 40, 0, Math.PI * 2);
      ctx.arc(52, -4, 40, 0, Math.PI * 2);
      ctx.moveTo(-12, -4); ctx.lineTo(12, -4);
      ctx.stroke();
      ctx.restore();
    }

    ctx.restore();
    ctx.restore();
  }

  // ---------- камера ----------
  function cam(t) {
    let s = 1.0 + 0.03 * clamp(t / 21);
    let fx = W / 2, fy = 900;

    const zin = ease.outCubic(clamp((t - ev.punch) / 0.75));
    const zout = ease.outCubic(clamp((t - ev.cta + 0.15) / 0.6));
    const z = zin * (1 - zout);
    if (z > 0) {
      s = lerp(s, 1.42, z);
      fx = lerp(fx, PAT.x + 30, z);
      fy = lerp(fy, PAT.y - 20, z);
    }
    return { s, fx, fy };
  }

  function applyCam(ctx, t) {
    const { s, fx, fy } = cam(t);
    ctx.translate(fx, fy);
    ctx.scale(s, s);
    ctx.translate(-fx, -fy);
  }

  // ---------- субтитры ----------
  function subtitle(ctx, t) {
    const rows = [
      [ev.intro, ev.line1, '— Следующий.'],
      [ev.line1, ev.line2, '— Доктор, у меня провалы в памяти.'],
      [ev.line2, ev.punch, '— И давно?'],
      [ev.punch, ev.cta, '— Что давно?'],
    ];
    for (const [t0, t1, str] of rows) {
      if (t < t0 || t > t1) continue;
      const a = fade(t, t0, 0.25) * out(t, t1 - 0.15, 0.2);
      if (a <= 0.01) continue;
      const punch = t0 === ev.punch;
      const fs = punch ? 64 : 44;
      const tw = G.measure(ctx, str, fs, F, 800);
      ctx.save();
      ctx.globalAlpha = a;
      G.rrect(ctx, W / 2 - tw / 2 - 36, 1610, tw + 72, fs + 52, 22, { fill: 'rgba(18,13,9,0.8)', seed: 70 });
      text(ctx, str, W / 2, 1610 + (fs + 52) / 2 + 2, { size: fs, color: punch ? '#FFC46B' : C.cream });
      ctx.restore();
    }
  }

  // ---------- хук ----------
  function hook(ctx, t) {
    if (t > ev.intro + 0.3) return;
    const a = 1 - fade(t, ev.intro - 0.3, 0.35);
    ctx.save();
    ctx.globalAlpha = a * 0.6;
    ctx.fillStyle = '#1A1208';
    ctx.fillRect(0, 0, W, H);
    ctx.restore();
    ctx.save();
    ctx.globalAlpha = a;
    text(ctx, 'АНЕКДОТ', W / 2, 720, { size: 146, color: C.cream });
    text(ctx, 'который всегда заходит', W / 2, 840, { size: 42, color: '#E5C9A0', weight: 700 });
    G.rrect(ctx, W / 2 - 70, 900, 140, 6, 3, { fill: C.accent, seed: 80 });
    ctx.restore();
  }

  // ---------- концовка ----------
  function cta(ctx, t) {
    if (t < ev.cta) return;
    const a = fade(t, ev.cta, 0.45);
    ctx.save();
    ctx.globalAlpha = 0.68 * a;
    ctx.fillStyle = '#140E08';
    ctx.fillRect(0, 0, W, H);
    ctx.restore();
    ctx.save();
    ctx.globalAlpha = a;
    text(ctx, 'ПОДПИШИСЬ', W / 2, 520, { size: 102, color: C.cream });
    text(ctx, 'анекдоты каждый день', W / 2, 620, { size: 42, color: '#E5C9A0', weight: 700 });
    G.rrect(ctx, W / 2 - 110, 672, 220, 8, 4, { fill: C.accent, seed: 81 });
    ctx.restore();
  }

  function draw(ctx, t) {
    ctx.save();
    applyCam(ctx, t);
    room(ctx, t);

    const docSpeak = (t >= ev.intro && t < ev.line1) || (t >= ev.line2 && t < ev.punch) ? 1 : 0;
    const patSpeak = (t >= ev.line1 && t < ev.line2) || (t >= ev.punch && t < ev.cta) ? 1 : 0;

    bust(ctx, {
      x: DOC.x, y: DOC.y, s: DOC.s, facing: -1, cloth: C.coat, coat: true,
      hairStyle: 'bald', glasses: true, speaking: docSpeak, t,
      tilt: docSpeak ? -0.03 : 0.01, brow: docSpeak ? -6 : 0, blinkOff: 0.6, breathOff: 1.1,
    });

    bust(ctx, {
      x: PAT.x, y: PAT.y, s: PAT.s, facing: 1, cloth: C.sweater,
      hairStyle: 'hair', speaking: patSpeak, t,
      tilt: patSpeak ? 0.04 : -0.02, brow: t > ev.punch ? -12 : 0,
      wide: t > ev.punch, noBlink: true, blinkOff: 2.1, breathOff: 0,
    });

    ctx.restore();

    subtitle(ctx, t);
    hook(ctx, t);
    cta(ctx, t);
  }

  Studio.film({ draw, post: { paper: 0.12, vignette: 0.2, grain: 0.05 } });
})();
