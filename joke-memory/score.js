// THE SCORE — анекдот про провалы в памяти.
(function () {
  const node = typeof require !== 'undefined';
  const U = node ? require('./engine/util') : globalThis.U;
  const MU = node ? require('./engine/music') : globalThis.MUSIC;
  const { m, makeClock, makeChords, placeBar } = MU;

  const FPS = 30;
  const FORMAT = U.pickFormat('9:16');
  const [W, H] = U.formatSize(FORMAT);
  const SAFE = U.safeArea(W, H);
  const WIDE = W / H > 1.2;
  const STYLE = 'flat';

  const clock = makeClock({ bpm: 90, offset: 0 });
  const { T, BEAT } = clock;
  const DURATION = 21;

  const ev = {
    hook: 0.55,
    intro: 3.60,
    line1: 6.10,
    line2: 10.40,
    punch: 13.20,
    cta: 17.20,
    end: 20.20,
  };

  const { chords, chordAt } = makeChords(clock, {
    Am: { notes: ['A3', 'C4', 'E4'], bass: 'A2' },
    F: { notes: ['F3', 'A3', 'C4'], bass: 'F2' },
    C: { notes: ['C4', 'E4', 'G4'], bass: 'C3' },
    G: { notes: ['G3', 'B3', 'D4'], bass: 'G2' },
  }, [
    [0, 0, 4, 'Am'], [1, 0, 4, 'F'], [2, 0, 4, 'C'], [3, 0, 4, 'G'],
    [4, 0, 4, 'Am'], [5, 0, 4, 'F'], [6, 0, 4, 'C'], [7, 0, 4, 'G'],
    [8, 0, 4, 'Am'], [9, 0, 4, 'F'],
  ]);

  const HOOK = {
    1: [['E5', 0, 3], ['C5', 3, 1], ['A4', 4, 4]],
    2: [['F5', 0, 2], ['E5', 2, 2], ['C5', 4, 4]],
    3: [['G4', 0, 2], ['C5', 2, 2], ['E5', 4, 4]],
    4: [['E5', 0, 2], ['D5', 2, 2], ['C5', 4, 2], ['A4', 6, 2]],
    5: [['C5', 0, 3], ['A4', 3, 1], ['F4', 4, 4]],
    6: [['G4', 0, 2], ['A4', 2, 2], ['C5', 4, 4]],
    7: [['E5', 0, 4], ['D5', 4, 4]],
    8: [['C5', 0, 8]],
  };

  const melody = [1, 2, 3, 4, 5, 6, 7, 8].flatMap((bar) => placeBar(clock, HOOK[bar], bar));

  const bassline = [];
  for (const c of chords) {
    bassline.push({ t: c.t0, dur: BEAT * 1.8, midi: c.bass });
  }

  const markers = {
    line1: ev.line1,
    punch: { t: ev.punch, sync: 'a' },
  };

  const SCORE = {
    FPS, FORMAT, W, H, SAFE, WIDE, STYLE, DURATION, clock, T, BEAT,
    m, chords, chordAt, ev, markers, melody, bassline,
  };

  if (node) module.exports = SCORE;
  else globalThis.SCORE = SCORE;
})();
