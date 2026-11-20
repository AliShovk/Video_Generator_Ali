// THE SONG — тихое начало, нарастание к 30-му дню, вспышка на «весь пруд».
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

// ---------- барабаны: входят тихо, к 30-му дню — полный грув ----------
const K = I.kick({ punch: 0.5, tail: 0.6 });
const SN = I.snare({ tone: 0.35, snap: 0.45, decay: 0.2 });
const HC = [I.hat(false, 41), I.hat(false, 42)];
const kicks = [];

clock.eachStep(2, 16, 16, (t, b, s) => {
  const full = t >= ev.d29;
  if (s % 8 === 0) { drums.addMono(K, t, full ? 0.85 : 0.55); kicks.push(t); if (!full) kicks.push(t); }
  if (full && (s === 4 || s === 12)) { drums.addMono(SN, t, 0.42); verb.addMono(SN, t, 0.2); }
  if (s % 4 === 0) drums.addMono(HC[s % 8 === 0 ? 0 : 1], t, full ? 0.14 : 0.08, 0.2);
});

// ---------- бас ----------
for (const n of sc.bassline) {
  if (n.t < T(1)) continue;
  const g = n.t >= ev.d29 ? 0.6 : 0.4;
  bass.addMono(I.bass(n.midi, n.dur * 0.92, { bright: 0.25, sub: 0.7 }), n.t, g);
}

// ---------- пэды ----------
for (const c of sc.chords) {
  const near = c.t0 >= ev.d29;
  for (const n of c.notes) {
    const { L, R } = I.padNote(n, Math.max(0.5, c.t1 - c.t0), { cutoff: near ? 2600 : 1200, attack: 0.5, release: 1.6 });
    pad.addStereo(L, R, c.t0, near ? 0.11 : 0.085);
  }
}

// ---------- мелодия: маримба + электропиано ----------
for (const n of sc.melody) {
  const mb = I.marimba(n.midi, { decay: 0.6, thock: 0.12 });
  keys.addMono(mb, n.t, 0.34, ((n.midi - m('A4')) / 24) * 0.3);
  verb.addMono(mb, n.t, 0.2);
  if (n.t >= ev.d29) {
    const ep = I.epiano(n.midi - 12, n.dur * 1.2, { index: 1.4, decay: 0.9 });
    keys.addMono(ep, n.t, 0.22);
  }
}

// ---------- эффекты ----------
fx.addMono(I.noiseSweep(1.2, 200, 6000, { q: 0.8, pink: true }), ev.d29 - 1.2, 0.35); // вдох перед 29-м
fx.addMono(I.subBoom(1.8, 100, 45), ev.d30, 0.55);
fx.addMono(I.crash(51), ev.d30, 0.3, 0.1);
fx.addMono(I.ting(m('E6'), { gap: 0.1 }), ev.d30 + 0.05, 0.28);
fx.addMono(I.pop(360), ev.moral, 0.25);

// ---------- озвучка ----------
const voice = MIX.loadAudio(path.join(__dirname, 'out/voice.wav'), { at: 0, gain: 1.0 });

MIX.sidechain([pad, bass], kicks);
MIX.duck([drums, bass, pad, keys], voice, { depth: 0.5, attack: 0.02, release: 0.35, threshold: 0.02 });
const stems = {
  drums, bass, pad, keys, fx, voice,
  verb: reverb(verb, { room: 0.86, damp: 0.4 }),
  dly: pingpong(dly, BEAT * 0.75, 0.32, 3000),
};
const GAIN = { drums: 0.5, bass: 0.8, pad: 2.4, keys: 1.05, fx: 0.8, voice: 1.9, verb: 1.0, dly: 0.7 };
const out = path.join(__dirname, 'out');
const mix = MIX.mixdown(stems, GAIN, { stemDir: process.env.STEMS ? out : null });
MIX.highpass(mix, 22);
MIX.fadeOut(mix, DURATION - 1.4, DURATION);
const M = MIX.master(mix, parseFloat(process.env.DRIVE || '0.8'), undefined,
  { lufs: process.env.LUFS ? parseFloat(process.env.LUFS) : -14 });
MIX.writeWav(path.join(out, 'music.wav'), mix);
console.log(`wrote out/music.wav (${DURATION.toFixed(2)}s, ${M.lufs.toFixed(1)} LUFS)`);
