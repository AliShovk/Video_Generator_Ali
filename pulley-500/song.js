// THE SONG — вся музыка синтезируется здесь из score.js.
const path = require('path');
const { SR, Bus, reverb, pingpong } = require('./engine/audio/dsp');
const I = require('./engine/audio/instruments');
const MIX = require('./engine/audio/mix');
const sc = require('./score');
const { T, BEAT, DURATION, m, ev, clock } = sc;

const N = Math.ceil(DURATION * SR);
const bus = () => new Bus(N);
const drums = bus(), bass = bus(), pad = bus(), keys = bus(), fx = bus();
const verb = bus(), dly = bus();

// ---------- барабаны: спокойный грув, без дропа ----------
const K = I.kick({ punch: 0.6, tail: 0.5 });
const SN = I.snare({ tone: 0.4, snap: 0.5, decay: 0.18 });
const HC = [I.hat(false, 21), I.hat(false, 22)];
const CR = I.crash(23);
const kicks = [];

clock.eachStep(1, 16, 16, (t, b, s) => {
  if (s % 8 === 0) { drums.addMono(K, t, 0.8); kicks.push(t); }
  if (s === 4 || s === 12) { drums.addMono(SN, t, 0.42); verb.addMono(SN, t, 0.16); }
  if (s % 2 === 0) drums.addMono(HC[s % 4 === 2 ? 1 : 0], t, s % 4 === 2 ? 0.16 : 0.10, s % 4 === 2 ? -0.25 : 0.25);
});
drums.addMono(CR, ev.answer, 0.26, 0.1);

// ---------- бас ----------
for (const n of sc.bassline) {
  if (n.t < T(1)) continue;
  bass.addMono(I.bass(n.midi, n.dur * 0.9, { bright: 0.25, sub: 0.7 }), n.t, 0.55);
}

// ---------- пэды ----------
for (const c of sc.chords) {
  for (const n of c.notes) {
    const { L, R } = I.padNote(n, Math.max(0.4, c.t1 - c.t0), { cutoff: 1400, attack: 0.35, release: 1.1 });
    pad.addStereo(L, R, c.t0, 0.085);
  }
}

// ---------- мелодия: маримба + щипок ----------
for (const n of sc.plucks) {
  const mb = I.marimba(n.midi, { decay: 0.5, thock: 0.2 });
  keys.addMono(mb, n.t, 0.42, ((n.midi - m('A4')) / 24) * 0.3);
  verb.addMono(mb, n.t, 0.18);
}
for (const n of sc.melody.filter((_, i) => i % 2 === 0)) {
  keys.addMono(I.pluck(n.midi - 12, { decay: 0.35, cutoff: 2200 }), n.t, 0.18);
}

// ---------- эффекты по событиям ----------
fx.addMono(I.noiseSweep(0.5, 300, 2600, { q: 1.2, pink: true }), 0.02, 0.16);
fx.addMono(I.thud(72, 0.10), ev.blockLand, 0.55);
for (const t of [ev.split, ev.half1, ev.half2]) fx.addMono(I.woodTick(320, 3), t, 0.5);
fx.addMono(I.noiseSweep(0.7, 200, 6000, { q: 0.9, pink: true }), ev.answer - 0.75, 0.28);
fx.addMono(I.subBoom(1.6, 90, 45), ev.answer, 0.5);
fx.addMono(I.ting(m('A5'), { gap: 0.09 }), ev.answer + 0.05, 0.22);
fx.addMono(I.pop(520), ev.recap, 0.22);

// ---------- микс ----------
MIX.sidechain([pad, bass], kicks);
const stems = {
  drums, bass, pad, keys, fx,
  verb: reverb(verb, { room: 0.8, damp: 0.35 }),
  dly: pingpong(dly, BEAT * 0.75, 0.3, 3200),
};
const GAIN = { drums: 0.45, bass: 0.75, pad: 2.2, keys: 1.0, fx: 0.8, verb: 0.9, dly: 0.7 };
const out = path.join(__dirname, 'out');
const mix = MIX.mixdown(stems, GAIN, { stemDir: process.env.STEMS ? out : null });
MIX.highpass(mix, 24);
MIX.fadeOut(mix, DURATION - 1.2, DURATION);
const M = MIX.master(mix, parseFloat(process.env.DRIVE || '0.8'), undefined,
  { lufs: process.env.LUFS ? parseFloat(process.env.LUFS) : -14 });
MIX.writeWav(path.join(out, 'music.wav'), mix);
console.log(`wrote out/music.wav (${DURATION.toFixed(2)}s, ${M.lufs.toFixed(1)} LUFS)`);
