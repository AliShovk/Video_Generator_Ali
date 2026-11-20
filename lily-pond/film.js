// THE FILM — пруд сверху: лилия удваивается каждый день, 29-й выглядит как провал.
(function () {
  const U = globalThis.U, G = globalThis.G, S = globalThis.SCORE, Studio = globalThis.Studio;
  const { clamp, lerp, ease, pulse } = U;
  const { ev, DAYS } = S;
  const W = G.W, H = G.H;

  const C = {
    ink: '#0B1F1D', cream: '#F6F1E3', muted: '#8FA9A2',
    padA: '#2F7D5B', padB: '#3E9A6E', padC: '#256B4E', vein: 'rgba(10,40,32,0.35)',
    flower: '#F7F2E7', pollen: '#F2C14E', gold: '#E8B44A',
  };
  const F = 'Inter';

  const POND = { cx: 540, cy: 1010, rx: 470, ry: 700 };
  const N = 520;

  const pop = (t, t0, dur = 0.3, k = 2.2) => (t < t0 ? 0 : ease.outBack(clamp((t - t0) / dur), k));
  const fade = (t, t0, dur = 0.4) => clamp((t - t0) / dur);

  function text(ctx, str, x, y, o = {}) {
    G.text(ctx, str, x, y, {
      size: o.size || 48, fam: o.fam || F, weight: o.weight || 800,
      color: o.color || C.cream, align: o.align || 'center', baseline: 'middle',
      stroke: o.stroke, strokeW: o.strokeW || 0, boil: 0,
    });
  }

  // ---------- раскладка листьев: спираль от центра, сортировка по радиусу ----------
  const PADS = (() => {
    const rnd = U.mulberry32(7);
    const pts = [];
    const ga = Math.PI * (3 - Math.sqrt(5));
    for (let i = 0; i < N * 1.6; i++) {
      const r = Math.sqrt((i + 0.5) / (N * 1.6));
      const a = i * ga;
      const x = Math.cos(a) * r * POND.rx * 0.96;
      const y = Math.sin(a) * r * POND.ry * 0.96;
      if ((x / (POND.rx * 0.99)) ** 2 + (y / (POND.ry * 0.99)) ** 2 > 1) continue;
      pts.push({
        x: POND.cx + x, y: POND.cy + y,
        r: 24 + rnd() * 12,
        rot: rnd() * Math.PI * 2,
        tone: rnd(),
        notch: 0.5 + rnd() * 0.35,
      });
      if (pts.length >= N) break;
    }
    // приоритет появления: чуть раньше — ближе к центру, но листья расходятся по всему пруду
    for (const q of pts) {
      const dn = Math.sqrt(((q.x - POND.cx) / POND.rx) ** 2 + ((q.y - POND.cy) / POND.ry) ** 2);
      q.pri = rnd() * 0.82 + dn * 0.18;
    }
    pts.sort((a, b) => a.pri - b.pri);
    return pts;
  })();

  function dayAt(t) {
    for (let i = 0; i < DAYS.length - 1; i++) {
      const [t0, d0] = DAYS[i], [t1, d1] = DAYS[i + 1];
      if (t >= t0 && t <= t1) return lerp(d0, d1, (t - t0) / (t1 - t0));
    }
    return DAYS[DAYS.length - 1][1];
  }

  const fillAt = (t) => Math.pow(2, dayAt(t) - 30);

  function water(ctx, t, bright) {
    const g = ctx.createLinearGradient(0, 0, 0, H);
    g.addColorStop(0, bright ? '#17494A' : '#0D3333');
    g.addColorStop(1, bright ? '#0B2B2C' : '#061A1A');
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, W, H);
    // блики на воде
    ctx.save();
    for (let i = 0; i < 9; i++) {
      const ph = (t * 0.08 + i / 9) % 1;
      const y = POND.cy - POND.ry + ph * POND.ry * 2;
      ctx.globalAlpha = 0.05 * (1 - Math.abs(ph - 0.5) * 2);
      G.line(ctx, [[120 + i * 37, y], [W - 140 - i * 23, y + 18]], { color: '#BFE3DC', lw: 2, seed: 10 + i });
    }
    ctx.restore();
    // кромка пруда
    G.ellipse(ctx, POND.cx, POND.cy, POND.rx + 8, POND.ry + 8, { fill: 'rgba(6,26,25,0.55)', seed: 3 });
  }

  function pad(ctx, p, scale, flower) {
    if (scale <= 0.01) return;
    ctx.save();
    ctx.translate(p.x, p.y);
    ctx.rotate(p.rot);
    ctx.scale(scale, scale);
    const col = p.tone < 0.34 ? C.padA : p.tone < 0.68 ? C.padB : C.padC;
    // лист с вырезом
    const a0 = p.notch, a1 = Math.PI * 2 - p.notch;
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.arc(0, 0, p.r, a0, a1);
    ctx.closePath();
    ctx.fillStyle = col;
    ctx.fill();
    ctx.strokeStyle = 'rgba(8,35,28,0.55)';
    ctx.lineWidth = 2;
    ctx.stroke();
    // прожилки
    for (let k = 1; k <= 3; k++) {
      const a = a0 + (a1 - a0) * (k / 4);
      G.line(ctx, [[0, 0], [Math.cos(a) * p.r * 0.85, Math.sin(a) * p.r * 0.85]],
        { color: C.vein, lw: 1.6, seed: 20 + k });
    }
    if (flower) {
      for (let k = 0; k < 7; k++) {
        const a = (k / 7) * Math.PI * 2;
        G.ellipse(ctx, Math.cos(a) * 8, Math.sin(a) * 8, 6, 9, { fill: C.flower, stroke: 'rgba(20,60,50,0.35)', lw: 1, seed: 30 + k });
      }
      G.ellipse(ctx, 0, 0, 5, 5, { fill: C.pollen, seed: 40 });
    }
    ctx.restore();
  }

  function pond(ctx, t) {
    const f = fillAt(t);
    const bloom = t >= ev.d30 - 0.6;
    // первый лист — пока пруд почти пуст
    if (f < 0.004) {
      const s = 1 + 0.03 * Math.sin(t * 2.2);
      // круги на воде вокруг первого листа
      for (let k = 0; k < 3; k++) {
        const ph = ((t * 0.35 + k / 3) % 1);
        ctx.save();
        ctx.globalAlpha = 0.18 * (1 - ph);
        ctx.strokeStyle = '#9BD3C4';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.ellipse(POND.cx, POND.cy + 60, 90 + ph * 190, (90 + ph * 190) * 0.86, 0, 0, Math.PI * 2);
        ctx.stroke();
        ctx.restore();
      }
      pad(ctx, { x: POND.cx, y: POND.cy + 60, r: 74, rot: 0.6, tone: 0.2, notch: 0.62 }, s, false);
    }
    for (let i = 0; i < PADS.length; i++) {
      const p = PADS[i];
      if (p.pri > f) break;
      const local = clamp((f - p.pri) / Math.max(0.004, f * 0.08));
      const s = 0.55 + 0.45 * ease.outBack(local, 1.8);
      pad(ctx, p, Math.min(1, s), bloom && i % 5 === 0);
    }
  }

  function dayBadge(ctx, t) {
    const d = Math.floor(dayAt(t));
    const a = fade(t, 5.4, 0.5) * (1 - fade(t, ev.moral, 0.4));
    if (a <= 0.01) return;
    ctx.save();
    ctx.globalAlpha = a;
    text(ctx, `ДЕНЬ ${d}`, W / 2, 210, { size: 44, color: C.muted });
    const pct = Math.pow(2, d - 30) * 100;
    const label = pct >= 99.5 ? '100%' : pct >= 10 ? `${Math.round(pct)}%` : pct >= 0.5 ? `${pct.toFixed(1)}%` : '0,1%';
    text(ctx, label, W / 2, 262, { size: 34, weight: 700, color: C.gold });
    ctx.restore();
  }

  function hookText(ctx, t) {
    if (t > ev.rule + 0.2) return;
    const a = 1 - fade(t, ev.rule - 0.2, 0.35);
    ctx.save();
    ctx.globalAlpha = a;
    text(ctx, 'ЗА ДЕНЬ ДО РЕЗУЛЬТАТА', W / 2, 240, { size: 40, color: C.muted });
    text(ctx, 'ЭТО ВЫГЛЯДИТ', W / 2, 330, { size: 76 });
    text(ctx, 'КАК ПРОВАЛ', W / 2, 412, { size: 76, color: C.gold });
    ctx.restore();
  }

  function ruleText(ctx, t) {
    if (t < ev.rule || t > ev.d25 + 0.4) return;
    const a = fade(t, ev.rule, 0.35) * (1 - fade(t, ev.d25, 0.35));
    ctx.save();
    ctx.globalAlpha = a;
    text(ctx, 'каждый день — вдвое больше', W / 2, 300, { size: 40, color: C.cream });
    ctx.restore();
  }

  function moral(ctx, t) {
    if (t < ev.moral) return;
    const a = fade(t, ev.moral, 0.5);
    ctx.save();
    ctx.globalAlpha = 0.62 * a;
    ctx.fillStyle = '#04100F';
    ctx.fillRect(0, 0, W, H);
    ctx.restore();
    ctx.save();
    ctx.globalAlpha = 0.72 * a;
    G.rrect(ctx, 70, 742, W - 140, 320, 26, { fill: 'rgba(3,12,11,0.72)', seed: 77 });
    ctx.restore();
    ctx.save();
    ctx.globalAlpha = a;
    text(ctx, 'Ты не стоишь на месте.', W / 2, 820, { size: 56 });
    text(ctx, 'Ты на 29-м дне.', W / 2, 910, { size: 72, color: C.gold });
    text(ctx, 'Ещё один день — и весь пруд твой.', W / 2, 1000, { size: 36, weight: 700, color: C.muted });
    ctx.restore();
  }

  function draw(ctx, t) {
    const bright = t >= ev.d30;
    water(ctx, t, bright);
    pond(ctx, t);
    // вспышка на 30-й день
    if (t >= ev.d30 && t < ev.d30 + 0.5) {
      const u = (t - ev.d30) / 0.5;
      ctx.save();
      ctx.globalAlpha = (1 - u) * 0.35;
      ctx.fillStyle = '#CFEFE2';
      ctx.fillRect(0, 0, W, H);
      ctx.restore();
    }
    dayBadge(ctx, t);
    hookText(ctx, t);
    ruleText(ctx, t);
    moral(ctx, t);
  }

  Studio.film({ draw, post: { paper: 0.18, vignette: 0.28, grain: 0.05 } });
})();
