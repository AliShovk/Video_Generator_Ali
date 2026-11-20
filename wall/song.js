// THE SONG — рабочий грув стройки + озвучка.
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

const K = I.kick({ punch: 0.6, tail: 0.5 });
const SN = I.snare({ tone: 0.4, snap: 0.5, decay: 0.18 });
const HC = [I.hat(false, 61), I.hat(false, 62)];
const kicks = [];

clock.eachStep(1, 16, 16, (t, b, s) => {
  if (s % 8 === 0) { drums.addMono(K, t, 0.8); kicks.push(t); }
  if (s === 4 || s === 12) { drums.addMono(SN, t, 0.4); verb.addMono(SN, t, 0.15); }
  if (s % 2 === 0) drums.addMono(HC[s % 4 === 2 ? 1 : 0], t, s % 4 === 2 ? 0.14 : 0.08, s % 4 === 2 ? -0.25 : 0.25);
});

for (const n of sc.bassline) {
  if (n.t < T(1)) continue;
  bass.addMono(I.bass(n.midi, n.dur * 0.9, { bright: 0.3, sub: 0.65 }), n.t, 0.55);
}

for (const c of sc.chords) {
  for (const n of c.notes) {
    const { L, R } = I.padNote(n, Math.max(0.4, c.t1 - c.t0), { cutoff: 1600, attack: 0.3, release: 1.0 });
    pad.addStereo(L, R, c.t0, 0.075);
  }
}

for (const n of sc.melody) {
  const mb = I.marimba(n.midi, { decay: 0.42, thock: 0.18 });
  keys.addMono(mb, n.t, 0.38, ((n.midi - m('A4')) / 24) * 0.3);
  verb.addMono(mb, n.t, 0.15);
}

// кладка: тихий стук кирпича на каждую восьмую в фазе стройки
for (let t = ev.build; t < ev.full; t += 0.5) {
  fx.addMono(I.woodTick(180 + (Math.round(t * 2) % 4) * 30, 5), t, 0.18, Math.sin(t * 2) * 0.4);
}
fx.addMono(I.noiseSweep(0.6, 300, 2400, { q: 1.1, pink: true }), ev.crane - 0.3, 0.25);
fx.addMono(I.pop(300), ev.crane, 0.5);
fx.addMono(I.subBoom(1.6, 100, 45), ev.full, 0.5);
fx.addMono(I.ting(m('C6'), { gap: 0.08 }), ev.done, 0.3);

const voice = MIX.loadAudio(path.join(__dirname, 'out/voice.wav'), { at: 0, gain: 1.0 });

MIX.sidechain([pad, bass], kicks);
MIX.duck([drums, bass, pad, keys], voice, { depth: 0.5, attack: 0.02, release: 0.35, threshold: 0.02 });
const stems = {
  drums, bass, pad, keys, fx, voice,
  verb: reverb(verb, { room: 0.82, damp: 0.35 }),
  dly: pingpong(dly, BEAT * 0.75, 0.3, 3200),
};
const GAIN = { drums: 0.5, bass: 0.8, pad: 2.1, keys: 1.0, fx: 0.75, voice: 1.9, verb: 0.9, dly: 0.7 };
const out = path.join(__dirname, 'out');
const mix = MIX.mixdown(stems, GAIN, { stemDir: process.env.STEMS ? out : null });
MIX.highpass(mix, 24);
MIX.fadeOut(mix, DURATION - 1.3, DURATION);
const M = MIX.master(mix, parseFloat(process.env.DRIVE || '0.8'), undefined,
  { lufs: process.env.LUFS ? parseFloat(process.env.LUFS) : -14 });
MIX.writeWav(path.join(out, 'music.wav'), mix);
console.log(`wrote out/music.wav (${DURATION.toFixed(2)}s, ${M.lufs.toFixed(1)} LUFS)`);
