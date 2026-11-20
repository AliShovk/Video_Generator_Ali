// THE SONG — минимальный бит под анекдот + озвучка.
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

const K = I.kick({ punch: 0.5, tail: 0.5 });
const SN = I.snare({ tone: 0.3, snap: 0.3, decay: 0.2 });
const HC = [I.hat(false, 61), I.hat(false, 62)];
const kicks = [];

clock.eachStep(1, 16, 16, (t, b, s) => {
  if (s % 8 === 0) { drums.addMono(K, t, 0.55); kicks.push(t); }
  if (s === 8) drums.addMono(SN, t, 0.18);
  if (s % 4 === 2) drums.addMono(HC[1], t, 0.07, 0.2);
  if (s % 2 === 0) drums.addMono(HC[0], t, 0.045, -0.2);
});

for (const n of sc.bassline) {
  if (n.t < T(1)) continue;
  bass.addMono(I.bass(n.midi, n.dur * 0.85, { bright: 0.2, sub: 0.7 }), n.t, 0.45);
}

for (const c of sc.chords) {
  for (const n of c.notes) {
    const { L, R } = I.padNote(n, Math.max(0.4, c.t1 - c.t0), { cutoff: 1200, attack: 0.5, release: 1.4 });
    pad.addStereo(L, R, c.t0, 0.05);
  }
}

// редкая маримба — только во второй половине
for (const n of sc.melody) {
  if (n.t < ev.line1 - 0.2) continue;
  const mb = I.marimba(n.midi, { decay: 0.5, thock: 0.12 });
  keys.addMono(mb, n.t, 0.22, ((n.midi - m('A4')) / 24) * 0.25);
  verb.addMono(mb, n.t, 0.1);
}

// тихий «клик» на каждой реплике
for (const t of [ev.intro, ev.line1, ev.line2]) {
  fx.addMono(I.woodTick(140, 5), t, 0.14);
}
// панч: клик + удар + звон
fx.addMono(I.woodTick(150, 6), ev.punch, 0.22);
fx.addMono(I.subBoom(0.9, 95, 42), ev.punch, 0.28);
fx.addMono(I.ting(m('E6'), { gap: 0.1 }), ev.punch + 0.02, 0.16);
verb.addMono(I.ting(m('E6'), { gap: 0.1 }), ev.punch + 0.03, 0.1);

const voice = MIX.loadAudio(path.join(__dirname, 'out/voice.wav'), { at: 0, gain: 1.0 });

MIX.sidechain([pad, bass], kicks);
MIX.duck([drums, bass, pad, keys], voice, { depth: 0.55, attack: 0.02, release: 0.3, threshold: 0.02 });

const stems = {
  drums, bass, pad, keys, fx, voice,
  verb: reverb(verb, { room: 0.8, damp: 0.4 }),
  dly: pingpong(dly, BEAT * 0.75, 0.25, 3000),
};
const GAIN = { drums: 0.35, bass: 0.6, pad: 1.5, keys: 0.7, fx: 0.8, voice: 2.0, verb: 0.8, dly: 0.5 };
const out = path.join(__dirname, 'out');
const mix = MIX.mixdown(stems, GAIN, { stemDir: process.env.STEMS ? out : null });
MIX.highpass(mix, 28);
MIX.fadeOut(mix, DURATION - 1.0, DURATION);
const M = MIX.master(mix, parseFloat(process.env.DRIVE || '0.75'), undefined,
  { lufs: process.env.LUFS ? parseFloat(process.env.LUFS) : -14 });
MIX.writeWav(path.join(out, 'music.wav'), mix);
console.log(`wrote out/music.wav (${DURATION.toFixed(2)}s, ${M.lufs.toFixed(1)} LUFS)`);
