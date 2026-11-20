// THE SCORE — кузница: удары не ломают, а придают форму.
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

  // 15 ударов по секунде: 3.0 … 17.0
  const HITS = Array.from({ length: 15 }, (_, i) => 3.0 + i);
  // редкие добивающие удары
  const TAPS = [18.4, 19.4];

  const ev = {
    hook: 0.0,
    first: HITS[0],
    last: HITS[HITS.length - 1],
    quench: 20.4,
    blade: 22.4,
    moral: 26.0,
    end: 30.5,
  };

  const { chords, chordAt } = makeChords(clock, {
    Dm: { notes: ['D3', 'F3', 'A3'], bass: 'D2' },
    Bb: { notes: ['Bb2', 'D3', 'F3'], bass: 'Bb1' },
    F: { notes: ['F3', 'A3', 'C4'], bass: 'F2' },
    C: { notes: ['C3', 'E3', 'G3'], bass: 'C2' },
    Gm: { notes: ['G3', 'Bb3', 'D4'], bass: 'G2' },
  }, [
    [0, 0, 4, 'Dm'], [1, 0, 4, 'Dm'], [2, 0, 4, 'Bb'], [3, 0, 4, 'F'],
    [4, 0, 4, 'Dm'], [5, 0, 4, 'Bb'], [6, 0, 4, 'F'], [7, 0, 4, 'C'],
    [8, 0, 4, 'Bb'], [9, 0, 4, 'F'], [10, 0, 4, 'Gm'], [11, 0, 4, 'Dm'],
    [12, 0, 4, 'Bb'], [13, 0, 4, 'F'], [14, 0, 4, 'C'], [15, 0, 4, 'Dm'],
  ]);

  const HOOK = {
    2: [['D4', 0, 2], ['F4', 2, 2], ['A4', 4, 2], ['D5', 6, 2]],
    3: [['C5', 0, 2], ['A4', 2, 2], ['F4', 4, 4]],
    4: [['Bb4', 0, 2], ['D5', 2, 2], ['F5', 4, 2], ['D5', 6, 2]],
    5: [['C5', 0, 4], ['A4', 4, 4]],
    6: [['F4', 0, 2], ['A4', 2, 2], ['C5', 4, 4]],
    7: [['D5', 0, 4], ['C5', 4, 4]],
    8: [['Bb4', 0, 2], ['A4', 2, 2], ['G4', 4, 4]],
    9: [['F4', 0, 8]],
    10: [['D5', 0, 2], ['F5', 2, 2], ['A5', 4, 4]],
    11: [['G5', 0, 4], ['F5', 4, 4]],
    12: [['D5', 0, 4], ['A4', 4, 4]],
    13: [['Bb4', 0, 4], ['F4', 4, 4]],
    14: [['C5', 0, 4], ['E5', 4, 4]],
    15: [['D5', 0, 8]],
  };

  const melody = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    .flatMap((bar) => placeBar(clock, HOOK[bar], bar));

  const bassline = [];
  for (const c of chords) {
    bassline.push({ t: c.t0, dur: BEAT * 1.2, midi: c.bass });
    bassline.push({ t: c.t0 + BEAT * 2, dur: BEAT * 1.2, midi: c.bass });
  }

  const markers = {
    first: { t: ev.first, sync: 'a' },
    last: { t: ev.last, sync: 'a' },
    quench: { t: ev.quench, sync: 'v' },
    blade: ev.blade,
    moral: ev.moral,
  };

  const SCORE = {
    FPS, FORMAT, W, H, SAFE, WIDE, STYLE, DURATION, clock, T, BEAT, HITS, TAPS,
    m, chords, chordAt, ev, markers, melody, bassline,
  };
  if (node) module.exports = SCORE; else globalThis.SCORE = SCORE;
})();
