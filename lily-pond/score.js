// THE SCORE — кувшинка удваивается каждый день: 29-й день выглядит как провал.
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

  const clock = makeClock({ bpm: 120, offset: 0 });
  const { T, BEAT } = clock;
  const DURATION = 33;

  const ev = {
    hook: 0.0,
    rule: 3.0,
    d20: 6.0,
    d25: 10.0,
    d27: 13.0,
    d28: 15.0,
    d29: 18.0,
    d30: 22.0,
    moral: 26.0,
    end: 30.5,
  };

  // ключевые дни: время -> день
  const DAYS = [
    [0.0, 10],
    [3.0, 14],
    [6.0, 20],
    [10.0, 25],
    [13.0, 27],
    [15.0, 28],
    [18.0, 29],
    [22.0, 30],
    [DURATION, 30],
  ];

  const { chords, chordAt } = makeChords(clock, {
    Am: { notes: ['A3', 'C4', 'E4'], bass: 'A2' },
    F: { notes: ['F3', 'A3', 'C4'], bass: 'F2' },
    C: { notes: ['C4', 'E4', 'G4'], bass: 'C3' },
    G: { notes: ['G3', 'B3', 'D4'], bass: 'G2' },
    Dm: { notes: ['D4', 'F4', 'A4'], bass: 'D3' },
  }, [
    [0, 0, 4, 'Am'], [1, 0, 4, 'F'], [2, 0, 4, 'C'], [3, 0, 4, 'G'],
    [4, 0, 4, 'Am'], [5, 0, 4, 'F'], [6, 0, 4, 'C'], [7, 0, 4, 'G'],
    [8, 0, 4, 'F'], [9, 0, 4, 'C'], [10, 0, 4, 'G'], [11, 0, 4, 'Am'],
    [12, 0, 4, 'F'], [13, 0, 4, 'C'], [14, 0, 4, 'G'], [15, 0, 4, 'Am'],
  ]);

  const HOOK = {
    1: [['C5', 0, 2], ['E5', 2, 2], ['D5', 4, 2], ['C5', 6, 2]],
    2: [['A4', 0, 2], ['C5', 2, 2], ['E5', 4, 4]],
    3: [['G4', 0, 2], ['B4', 2, 2], ['D5', 4, 4]],
    4: [['F5', 0, 2], ['E5', 2, 2], ['C5', 4, 4]],
    5: [['D5', 0, 4], ['A4', 4, 4]],
    6: [['C5', 0, 2], ['D5', 2, 2], ['E5', 4, 2], ['G5', 6, 2]],
    7: [['F5', 0, 4], ['E5', 4, 4]],
    8: [['E5', 0, 2], ['C5', 2, 2], ['A4', 4, 4]],
    9: [['F5', 0, 2], ['A5', 2, 2], ['G5', 4, 4]],
    10: [['E5', 0, 2], ['D5', 2, 2], ['C5', 4, 4]],
    11: [['A4', 0, 8]],
    12: [['C5', 0, 2], ['E5', 2, 2], ['G5', 4, 4]],
    13: [['A5', 0, 4], ['G5', 4, 4]],
    14: [['E5', 0, 4], ['C5', 4, 4]],
    15: [['A4', 0, 8]],
  };

  const melody = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    .flatMap((bar) => placeBar(clock, HOOK[bar], bar));

  const bassline = [];
  for (const c of chords) {
    bassline.push({ t: c.t0, dur: BEAT * 2.6, midi: c.bass });
  }

  const markers = {
    d29: ev.d29,
    d30: { t: ev.d30, sync: 'av' },
    moral: ev.moral,
  };

  const SCORE = {
    FPS, FORMAT, W, H, SAFE, WIDE, STYLE, DURATION, clock, T, BEAT, DAYS,
    m, chords, chordAt, ev, markers, melody, bassline,
  };
  if (node) module.exports = SCORE; else globalThis.SCORE = SCORE;
})();
