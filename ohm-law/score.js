// THE SCORE — закон Ома: три величины и одна формула.
(function () {
  const node = typeof require !== 'undefined';
  const U = node ? require('./engine/util') : globalThis.U;
  const MU = node ? require('./engine/music') : globalThis.MUSIC;
  const { m, makeClock, makeChords } = MU;

  const FPS = 30;
  const FORMAT = U.pickFormat('9:16');
  const [W, H] = U.formatSize(FORMAT);
  const SAFE = U.safeArea(W, H);
  const WIDE = W / H > 1.2;
  const STYLE = 'flat';

  const clock = makeClock({ bpm: 120, offset: 0 }); // 1 такт = 2 с
  const { T, BEAT } = clock;
  const DURATION = 33;

  const ev = {
    title: 0.15,
    vBadge: 0.75,
    iBadge: 1.25,
    rBadge: 1.75,
    wire: 3.9,
    volt: 4.30,
    ampere: 7.45,
    ohm: 10.40,
    formula: 13.80,
    numbers: 17.80,
    result: 20.10,
    rule: 21.20,
    recap: 24.80,
    end: 31.00,
  };

  const S = {
    intro: [0, 3.9],
    volt: [3.9, 7.4],
    ampere: [7.4, 10.4],
    ohm: [10.4, 13.8],
    formula: [13.8, 17.8],
    numbers: [17.8, 21.2],
    rule: [21.2, 24.8],
    recap: [24.8, DURATION],
  };

  const { chords, chordAt } = makeChords(clock, {
    C: { notes: ['C4', 'E4', 'G4'], bass: 'C3' },
    Am: { notes: ['A3', 'C4', 'E4'], bass: 'A2' },
    F: { notes: ['F3', 'A3', 'C4'], bass: 'F2' },
    G: { notes: ['G3', 'B3', 'D4'], bass: 'G2' },
  }, [
    [0, 0, 4, 'C'], [1, 0, 4, 'C'], [2, 0, 4, 'Am'], [3, 0, 4, 'F'],
    [4, 0, 4, 'C'], [5, 0, 4, 'G'], [6, 0, 4, 'Am'], [7, 0, 4, 'F'],
    [8, 0, 4, 'C'], [9, 0, 4, 'G'], [10, 0, 4, 'F'], [11, 0, 4, 'C'],
    [12, 0, 4, 'Am'], [13, 0, 4, 'F'], [14, 0, 4, 'G'], [15, 0, 4, 'C'],
    [16, 0, 4, 'C'],
  ]);

  const HOOK = {
    1: [['E5', 0, 2], ['G5', 2, 1], ['E5', 3, 1], ['C5', 4, 2], ['D5', 6, 2]],
    2: [['E5', 0, 3], ['C5', 3, 1], ['A4', 4, 2], ['C5', 6, 2]],
    3: [['F5', 0, 2], ['E5', 2, 1], ['C5', 3, 1], ['A4', 4, 4]],
    4: [['G4', 0, 2], ['C5', 2, 2], ['E5', 4, 2], ['G5', 6, 2]],
    5: [['F5', 0, 2], ['E5', 2, 2], ['D5', 4, 2], ['B4', 6, 2]],
    6: [['C5', 0, 4], ['E5', 4, 4]],
    7: [['A4', 0, 2], ['C5', 2, 2], ['F5', 4, 4]],
    8: [['E5', 0, 2], ['D5', 2, 2], ['C5', 4, 2], ['G4', 6, 2]],
    9: [['C5', 0, 2], ['E5', 2, 2], ['G5', 4, 4]],
    10: [['F5', 0, 2], ['A5', 2, 2], ['G5', 4, 2], ['E5', 6, 2]],
    11: [['C5', 0, 8]],
    12: [['A4', 0, 2], ['C5', 2, 2], ['E5', 4, 4]],
    13: [['F5', 0, 2], ['E5', 2, 2], ['C5', 4, 4]],
    14: [['G5', 0, 4], ['E5', 4, 4]],
    15: [['C5', 0, 8]],
  };

  const melody = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    .flatMap((bar) => MU.placeBar(clock, HOOK[bar], bar));
  const bassline = [];
  for (const c of chords) {
    bassline.push({ t: c.t0, dur: BEAT * 1.5, midi: c.bass });
    bassline.push({ t: c.t0 + BEAT * 2, dur: BEAT * 1.2, midi: c.bass });
  }

  const markers = {
    volt: { t: ev.volt, sync: 'a' },
    ampere: ev.ampere,
    ohm: ev.ohm,
    formula: ev.formula,
    result: ev.result,
    rule: ev.rule,
    recap: ev.recap,
  };

  const SCORE = {
    FPS, FORMAT, W, H, SAFE, WIDE, STYLE, DURATION, clock, T, BEAT, S,
    m, chords, chordAt, ev, markers, melody, bassline,
  };
  if (node) module.exports = SCORE; else globalThis.SCORE = SCORE;
})();
