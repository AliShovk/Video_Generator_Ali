// THE SONG — музыка для ролика о мощности насоса + озвучка.
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
const HC = [I.hat(false, 31), I.hat(false, 32)];
const CR = I.crash(33);
const kicks = [];

clock.eachStep(1, 17, 16, (t, b, s) => {
  if (s % 8 === 0) { drums.addMono(K, t, 0.8); kicks.push(t); }
  if (s === 4 || s === 12) { drums.addMono(SN, t, 0.4); verb.addMono(SN, t, 0.15); }
  if (s % 2 === 0) drums.addMono(HC[s % 4 === 2 ? 1 : 0], t, s % 4 === 2 ? 0.15 : 0.09, s % 4 === 2 ? -0.25 : 0.25);
});
drums.addMono(CR, ev.table, 0.26, 0.1);

for (const n of sc.bassline) {
  if (n.t < T(1)) continue;
  bass.addMono(I.bass(n.midi, n.dur * 0.9, { bright: 0.3, sub: 0.7 }), n.t, 0.55);
}

for (const c of sc.chords) {
  for (const n of c.notes) {
    const { L, R } = I.padNote(n, Math.max(0.4, c.t1 - c.t0), { cutoff: 1500, attack: 0.3, release: 1.0 });
    pad.addStereo(L, R, c.t0, 0.08);
  }
}

for (const n of sc.melody) {
  const mb = I.marimba(n.midi, { decay: 0.45, thock: 0.15 });
  keys.addMono(mb, n.t, 0.4, ((n.midi - m('A4')) / 24) * 0.3);
  verb.addMono(mb, n.t, 0.16);
}

// вода и ступени
for (let i = 0; i < ev.steps.length; i++) {
  fx.addMono(I.pop(260 + i * 60), ev.steps[i], 0.8);
  fx.addMono(I.noiseSweep(0.45, 500, 2200, { q: 1.1, pink: true }), ev.steps[i] - 0.1, 0.28);
}
fx.addMono(I.ting(m('D6'), { gap: 0.09 }), ev.rule, 0.3);
fx.addMono(I.ting(m('A5'), { gap: 0.09 }), ev.table, 0.3);

// озвучка
const voice = MIX.loadAudio(path.join(__dirname, 'out/voice.wav'), { at: 0, gain: 1.0 });

MIX.sidechain([pad, bass], kicks);
MIX.duck([drums, bass, pad, keys], voice, { depth: 0.5, attack: 0.02, release: 0.35, threshold: 0.02 });
const stems = {
  drums, bass, pad, keys, fx, voice,
  verb: reverb(verb, { room: 0.8, damp: 0.35 }),
  dly: pingpong(dly, BEAT * 0.75, 0.3, 3200),
};
const GAIN = { drums: 0.45, bass: 0.75, pad: 2.2, keys: 1.0, fx: 0.85, voice: 1.9, verb: 0.9, dly: 0.7 };
const out = path.join(__dirname, 'out');
const mix = MIX.mixdown(stems, GAIN, { stemDir: process.env.STEMS ? out : null });
MIX.highpass(mix, 24);
MIX.fadeOut(mix, DURATION - 1.2, DURATION);
const M = MIX.master(mix, parseFloat(process.env.DRIVE || '0.8'), undefined,
  { lufs: process.env.LUFS ? parseFloat(process.env.LUFS) : -14 });
MIX.writeWav(path.join(out, 'music.wav'), mix);
console.log(`wrote out/music.wav (${DURATION.toFixed(2)}s, ${M.lufs.toFixed(1)} LUFS)`);
