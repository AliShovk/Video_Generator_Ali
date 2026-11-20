// THE SONG — музыка для закона Ома: лёгкий грув + озвучка.
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
const HC = [I.hat(false, 21), I.hat(false, 22)];
const CR = I.crash(23);
const kicks = [];

clock.eachStep(1, 16, 16, (t, b, s) => {
  if (s % 8 === 0) { drums.addMono(K, t, 0.8); kicks.push(t); }
  if (s === 4 || s === 12) { drums.addMono(SN, t, 0.4); verb.addMono(SN, t, 0.15); }
  if (s % 2 === 0) drums.addMono(HC[s % 4 === 2 ? 1 : 0], t, s % 4 === 2 ? 0.15 : 0.09, s % 4 === 2 ? -0.25 : 0.25);
});
drums.addMono(CR, ev.result, 0.24, 0.1);

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

// эффекты по событиям
fx.addMono(I.pop(420), ev.vBadge, 0.5);
fx.addMono(I.pop(520), ev.iBadge, 0.5);
fx.addMono(I.pop(620), ev.rBadge, 0.5);
fx.addMono(I.noiseSweep(0.5, 300, 2400, { q: 1.1, pink: true }), ev.wire - 0.4, 0.2);
fx.addMono(I.boing(), ev.volt, 0.5);
fx.addMono(I.pop(300), ev.ampere, 0.8);
fx.addMono(I.pop(180), ev.ohm, 0.9);
fx.addMono(I.subBoom(1.0, 110, 55), ev.ohm + 0.03, 0.55);
fx.addMono(I.thud(90, 0.1), ev.ohm + 0.5, 0.4);
fx.addMono(I.ting(m('C6'), { gap: 0.08 }), ev.formula, 0.2);
fx.addMono(I.pop(700), ev.result, 0.85);
fx.addMono(I.ting(m('E6'), { gap: 0.08 }), ev.result + 0.03, 0.4);
fx.addMono(I.woodTick(260, 5), ev.rule, 0.4);

// озвучка
const voice = MIX.loadAudio(path.join(__dirname, 'out/voice.wav'), { at: 0, gain: 1.0 });

// микс
MIX.sidechain([pad, bass], kicks);
MIX.duck([drums, bass, pad, keys], voice, { depth: 0.5, attack: 0.02, release: 0.35, threshold: 0.02 });
const stems = {
  drums, bass, pad, keys, fx, voice,
  verb: reverb(verb, { room: 0.8, damp: 0.35 }),
  dly: pingpong(dly, BEAT * 0.75, 0.3, 3200),
};
const GAIN = { drums: 0.45, bass: 0.75, pad: 2.2, keys: 1.0, fx: 0.8, voice: 1.9, verb: 0.9, dly: 0.7 };
const out = path.join(__dirname, 'out');
const mix = MIX.mixdown(stems, GAIN, { stemDir: process.env.STEMPS ? out : null });
MIX.highpass(mix, 24);
MIX.fadeOut(mix, DURATION - 1.2, DURATION);
const M = MIX.master(mix, parseFloat(process.env.DRIVE || '0.8'), undefined,
  { lufs: process.env.LUFS ? parseFloat(process.env.LUFS) : -14 });
MIX.writeWav(path.join(out, 'music.wav'), mix);
console.log(`wrote out/music.wav (${DURATION.toFixed(2)}s, ${M.lufs.toFixed(1)} LUFS)`);
