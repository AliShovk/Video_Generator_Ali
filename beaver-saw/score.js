// THE SCORE — боберштыль: первобытная бензопила.
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

  const clock = makeClock({ bpm: 104, offset: 0 });
  const { T, BEAT } = clock;
  const DURATION = 21;

  const ev = {
    hook: 0.50,
    before: 3.40,
    beavers: 5.60,
    build: 9.20,
    name: 12.40,
    quiet: 15.40,
    fall: 16.40,
    cta: 18.00,
    end: 20.30,
  };

  const { chords, chordAt } = makeChords(clock, {
    Dm: { notes: ['D4', 'F4', 'A4'], bass: 'D3' },
    Bb: { notes: ['Bb3', 'D4', 'F4'], bass: 'Bb2' },
    C: { notes: ['C4', 'E4', 'G4'], bass: 'C3' },
    Am: { notes: ['A3', 'C4', 'E4'], bass: 'A2' },
  }, [
    [0, 0, 4, 'Dm'], [1, 0, 4, 'Bb'], [2, 0, 4, 'C'], [3, 0, 4, 'Dm'],
    [4, 0, 4, 'Bb'], [5, 0, 4, 'C'], [6, 0, 4, 'Dm'], [7, 0, 4, 'Am'],
    [8, 0, 4, 'Dm'], [9, 0, 4, 'Bb'],
  ]);

  const HOOK = {
    1: [['D5', 0, 2], ['F5', 2, 2], ['E5', 4, 2], ['D5', 6, 2]],
    2: [['Bb4', 0, 3], ['D5', 3, 1], ['F5', 4, 4]],
    3: [['C5', 0, 2], ['E5', 2, 2], ['G5', 4, 2], ['E5', 6, 2]],
    4: [['D5', 0, 4], ['A4', 4, 4]],
    5: [['F5', 0, 2], ['E5', 2, 2], ['D5', 4, 2], ['C5', 6, 2]],
    6: [['D5', 0, 4], ['F5', 4, 2], ['E5', 6, 2]],
    7: [['D5', 0, 8]],
    8: [['A4', 0, 2], ['D5', 2, 2], ['F5', 4, 4]],
    9: [['D5', 0, 8]],
  };

  const melody = [1, 2, 3, 4, 5, 6, 7, 8, 9].flatMap((bar) => placeBar(clock, HOOK[bar], bar));

  const bassline = [];
  for (const c of chords) {
    bassline.push({ t: c.t0, dur: BEAT * 1.5, midi: c.bass });
    bassline.push({ t: c.t0 + BEAT * 2, dur: BEAT * 1.1, midi: c.bass });
  }

  const markers = {
    name: ev.name,
    fall: ev.fall,
  };

  const SCORE = {
    FPS, FORMAT, W, H, SAFE, WIDE, STYLE, DURATION, clock, T, BEAT,
    m, chords, chordAt, ev, markers, melody, bassline,
  };

  if (node) module.exports = SCORE;
  else globalThis.SCORE = SCORE;
})();
