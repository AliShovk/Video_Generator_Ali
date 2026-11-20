// THE SONG — кузнечный ритм: лязг на каждый удар, низкий горн, нарастание к закалке.
const path = require('path');
const { SR, Bus, reverb, pingpong } = require('./engine/audio/dsp');
const I = require('./engine/audio/instruments');
const MIX = require('./engine/audio/mix');
const sc = require('./score');
const { T, BEAT, DURATION, m, ev, clock, HITS, TAPS } = sc;

const N = Math.ceil(DURATION * SR);
const bus = () => new Bus(N);
const drums = bus(), bass = bus(), pad = bus(), keys = bus(), fx = bus();
const verb = bus(), dly = bus();

// ---------- лязг молота ----------
function clang(seed, pitch) {
  const bell = I.bell(pitch, 0.28, 1.6, 2.1);
  const tick = I.noiseSweep(0.05, 2600, 900, { q: 1.4 });
  const out = new Float32Array(Math.max(bell.length, tick.length));
  for (let i = 0; i < bell.length; i++) out[i] += bell[i] * 0.55;
  for (let i = 0; i < tick.length; i++) out[i] += tick[i] * 0.22;
  return out;
}

for (let i = 0; i < HITS.length; i++) {
  const t = HITS[i];
  const pitch = 520 + (i % 5) * 40;
  const c = clang(i, pitch);
  fx.addMono(c, t, 0.5, (i % 2 ? 0.2 : -0.2));
  verb.addMono(c, t, 0.25);
  if (i % 2 === 0) drums.addMono(I.kick({ punch: 0.5, tail: 0.5 }), t, 0.6);
}
for (const t of TAPS) {
  const c = clang(9, 700);
  fx.addMono(c, t, 0.45);
  verb.addMono(c, t, 0.3);
}

// ---------- низкий пульс ----------
const kicks = [];
clock.eachStep(1, 16, 16, (t, b, s) => {
  if (s % 8 === 0) { drums.addMono(I.kick({ punch: 0.7, tail: 0.7 }), t, 0.55); kicks.push(t); }
  if (s === 4 || s === 12) drums.addMono(I.snare({ tone: 0.3, snap: 0.4, decay: 0.25 }), t, 0.22, 0.1);
});

for (const n of sc.bassline) {
  if (n.t < T(1)) continue;
  bass.addMono(I.bass(n.midi, n.dur * 0.95, { bright: 0.2, sub: 0.85 }), n.t, 0.6);
}

for (const c of sc.chords) {
  const near = c.t0 >= ev.quench - 1;
  for (const n of c.notes) {
    const { L, R } = I.padNote(n, Math.max(0.5, c.t1 - c.t0), { cutoff: near ? 2400 : 900, attack: 0.6, release: 1.8 });
    pad.addStereo(L, R, c.t0, near ? 0.10 : 0.075);
  }
}

for (const n of sc.melody) {
  const mb = I.marimba(n.midi, { decay: 0.5, thock: 0.25 });
  keys.addMono(mb, n.t, 0.3, ((n.midi - m('A4')) / 24) * 0.3);
  verb.addMono(mb, n.t, 0.16);
}

// ---------- закалка ----------
fx.addMono(I.noiseSweep(0.9, 8000, 300, { q: 0.7, pink: true }), ev.quench - 0.05, 0.5); // ш-ш-ш
fx.addMono(I.subBoom(2.2, 90, 40), ev.quench + 0.05, 0.5);
fx.addMono(I.ting(m('D6'), { gap: 0.08 }), ev.blade, 0.28);
fx.addMono(I.ting(m('A5'), { gap: 0.08 }), ev.blade + 0.12, 0.22);

// ---------- озвучка ----------
const voice = MIX.loadAudio(path.join(__dirname, 'out/voice.wav'), { at: 0, gain: 1.0 });

MIX.sidechain([pad, bass], kicks);
MIX.duck([drums, bass, pad, keys], voice, { depth: 0.5, attack: 0.02, release: 0.35, threshold: 0.02 });
const stems = {
  drums, bass, pad, keys, fx, voice,
  verb: reverb(verb, { room: 0.9, damp: 0.35 }),
  dly: pingpong(dly, BEAT * 0.75, 0.28, 2800),
};
const GAIN = { drums: 0.6, bass: 0.85, pad: 2.3, keys: 0.95, fx: 0.9, voice: 1.9, verb: 1.0, dly: 0.6 };
const out = path.join(__dirname, 'out');
const mix = MIX.mixdown(stems, GAIN, { stemDir: process.env.STEMS ? out : null });
MIX.highpass(mix, 26);
MIX.fadeOut(mix, DURATION - 1.4, DURATION);
const M = MIX.master(mix, parseFloat(process.env.DRIVE || '0.8'), undefined,
  { lufs: process.env.LUFS ? parseFloat(process.env.LUFS) : -14 });
MIX.writeWav(path.join(out, 'music.wav'), mix);
console.log(`wrote out/music.wav (${DURATION.toFixed(2)}s, ${M.lufs.toFixed(1)} LUFS)`);
