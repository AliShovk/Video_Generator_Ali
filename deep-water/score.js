// THE SCORE — глубинный полив деревьев.
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

  const clock = makeClock({ bpm: 108, offset: 0 });
  const { T, BEAT } = clock;
  const DURATION = 33;

  const ev = {
    hook: 0.0,
    dig: 2.6,
    plant: 7.0,
    pipe: 11.2,
    gravel: 15.4,
    water: 19.6,
    grow: 23.4,
    moral: 27.0,
    end: 32.0,
  };

  const { chords, chordAt } = makeChords(clock, {
    C: { notes: ['C4', 'E4', 'G4'], bass: 'C3' },
    G: { notes: ['G3', 'B3', 'D4'], bass: 'G2' },
    Am: { notes: ['A3', 'C4', 'E4'], bass: 'A2' },
    F: { notes: ['F3', 'A3', 'C4'], bass: 'F2' },
    Dm: { notes: ['D4', 'F4', 'A4'], bass: 'D3' },
  }, [
    [0, 0, 4, 'C'], [1, 0, 4, 'G'], [2, 0, 4, 'Am'], [3, 0, 4, 'F'],
    [4, 0, 4, 'C'], [5, 0, 4, 'G'], [6, 0, 4, 'Am'], [7, 0, 4, 'F'],
    [8, 0, 4, 'Dm'], [9, 0, 4, 'C'], [10, 0, 4, 'F'], [11, 0, 4, 'G'],
    [12, 0, 4, 'C'], [13, 0, 4, 'F'], [14, 0, 4, 'G'], [15, 0, 4, 'C'],
  ]);

  const HOOK = {
    1: [['G4', 0, 2], ['C5', 2, 2], ['E5', 4, 2], ['D5', 6, 2]],
    2: [['E5', 0, 3], ['C5', 3, 1], ['A4', 4, 2], ['G4', 6, 2]],
    3: [['A4', 0, 2], ['C5', 2, 2], ['F5', 4, 2], ['E5', 6, 2]],
    4: [['D5', 0, 2], ['E5', 2, 2], ['G5', 4, 4]],
    5: [['E5', 0, 2], ['D5', 2, 2], ['B4', 4, 2], ['G4', 6, 2]],
    6: [['C5', 0, 3], ['E5', 3, 1], ['A5', 4, 4]],
    7: [['F5', 0, 2], ['E5', 2, 2], ['C5', 4, 4]],
    8: [['D5', 0, 2], ['F5', 2, 2], ['A5', 4, 4]],
    9: [['G5', 0, 2], ['E5', 2, 2], ['C5', 4, 4]],
    10: [['A4', 0, 2], ['C5', 2, 2], ['F5', 4, 4]],
    11: [['G4', 0, 2], ['B4', 2, 2], ['D5', 4, 2], ['G5', 6, 2]],
    12: [['C5', 0, 4], ['E5', 4, 4]],
    13: [['F5', 0, 2], ['A5', 2, 2], ['G5', 4, 4]],
    14: [['E5', 0, 2], ['D5', 2, 2], ['C5', 4, 4]],
    15: [['C5', 0, 8]],
  };

  const melody = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    .flatMap((bar) => placeBar(clock, HOOK[bar], bar));

  const bassline = [];
  for (const c of chords) {
    bassline.push({ t: c.t0, dur: BEAT * 1.6, midi: c.bass });
    bassline.push({ t: c.t0 + BEAT * 2, dur: BEAT * 1.2, midi: c.bass });
  }

  const markers = {
    dig: { t: ev.dig, sync: 'a' },
    pipe: ev.pipe,
    water: ev.water,
    moral: ev.moral,
  };

  const SCORE = {
    FPS, FORMAT, W, H, SAFE, WIDE, STYLE, DURATION, clock, T, BEAT,
    m, chords, chordAt, ev, markers, melody, bassline,
  };

  if (node) module.exports = SCORE;
  else globalThis.SCORE = SCORE;
})();
