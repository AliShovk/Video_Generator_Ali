// THE SONG — спокойный грув сада + озвучка.
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

const K = I.kick({ punch: 0.45, tail: 0.55 });
const SN = I.snare({ tone: 0.35, snap: 0.35, decay: 0.2 });
const HC = [I.hat(false, 61), I.hat(false, 62)];
const kicks = [];

clock.eachStep(1, 16, 16, (t, b, s) => {
  if (s % 8 === 0) { drums.addMono(K, t, 0.55); kicks.push(t); }
  if (s === 4 || s === 12) { drums.addMono(SN, t, 0.22); verb.addMono(SN, t, 0.1); }
  if (s % 2 === 0) drums.addMono(HC[s % 4 === 2 ? 1 : 0], t, s % 4 === 2 ? 0.1 : 0.06, s % 4 === 2 ? -0.25 : 0.25);
});

for (const n of sc.bassline) {
  if (n.t < T(1)) continue;
  bass.addMono(I.bass(n.midi, n.dur * 0.9, { bright: 0.22, sub: 0.6 }), n.t, 0.42);
}

for (const c of sc.chords) {
  for (const n of c.notes) {
    const { L, R } = I.padNote(n, Math.max(0.4, c.t1 - c.t0), { cutoff: 1500, attack: 0.35, release: 1.1 });
    pad.addStereo(L, R, c.t0, 0.065);
  }
}

for (const n of sc.melody) {
  const mb = I.marimba(n.midi, { decay: 0.45, thock: 0.14 });
  keys.addMono(mb, n.t, 0.34, ((n.midi - m('A4')) / 24) * 0.3);
  verb.addMono(mb, n.t, 0.14);
}

// капли воды
for (let t = ev.water; t < DURATION - 1.2; t += 1.1) {
  const j = (Math.round(t * 10) % 5) - 2;
  fx.addMono(I.pop(520 + j * 40, 220), t, 0.09, (j / 4) * 0.5);
  verb.addMono(I.pop(520 + j * 40, 220), t + 0.02, 0.05);
}

// мягкие «удары» на этапах
for (const t of [ev.dig, ev.plant, ev.pipe, ev.gravel]) {
  fx.addMono(I.woodTick(120, 6), t, 0.16);
}

const voice = MIX.loadAudio(path.join(__dirname, 'out/voice.wav'), { at: 0, gain: 1.0 });

MIX.sidechain([pad, bass], kicks);
MIX.duck([drums, bass, pad, keys], voice, { depth: 0.5, attack: 0.02, release: 0.35, threshold: 0.02 });
const stems = {
  drums, bass, pad, keys, fx, voice,
  verb: reverb(verb, { room: 0.82, damp: 0.35 }),
  dly: pingpong(dly, BEAT * 0.75, 0.3, 3200),
};
const GAIN = { drums: 0.45, bass: 0.8, pad: 2.0, keys: 0.95, fx: 0.7, voice: 1.9, verb: 0.85, dly: 0.65 };
const out = path.join(__dirname, 'out');
const mix = MIX.mixdown(stems, GAIN, { stemDir: process.env.STEMS ? out : null });
MIX.highpass(mix, 24);
MIX.fadeOut(mix, DURATION - 1.3, DURATION);
const M = MIX.master(mix, parseFloat(process.env.DRIVE || '0.8'), undefined,
  { lufs: process.env.LUFS ? parseFloat(process.env.LUFS) : -14 });
MIX.writeWav(path.join(out, 'music.wav'), mix);
console.log(`wrote out/music.wav (${DURATION.toFixed(2)}s, ${M.lufs.toFixed(1)} LUFS)`);
