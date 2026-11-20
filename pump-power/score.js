// THE SCORE — мощность насоса и высота подъёма воды.
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
  const DURATION = 36;

  // ступени: высота, давление, мощность, труба
  const STEPS = [
    { m: 5, bar: '0,5', hp: '0,25', pipe: '1"', label: 'ДАЧА' },
    { m: 10, bar: '1', hp: '0,5', pipe: '1"', label: 'ДОМ' },
    { m: 20, bar: '2', hp: '0,75', pipe: '1"', label: 'ПОЛИВ' },
    { m: 40, bar: '4', hp: '1,5', pipe: '1–1¼"', label: 'УЧАСТОК' },
    { m: 80, bar: '8', hp: '3', pipe: '1¼–1½"', label: 'ДАВЛЕНИЕ' },
  ];

  const ev = {
    hook: 0,
    steps: [3.0, 7.0, 11.0, 15.0, 19.0],
    rule: 23.0,
    table: 27.0,
    end: 34.0,
  };

  const S = {
    hook: [0, 3.0],
    s1: [3.0, 7.0],
    s2: [7.0, 11.0],
    s3: [11.0, 15.0],
    s4: [15.0, 19.0],
    s5: [19.0, 23.0],
    rule: [23.0, 27.0],
    table: [27.0, DURATION],
  };

  const { chords, chordAt } = makeChords(clock, {
    Dm: { notes: ['D4', 'F4', 'A4'], bass: 'D3' },
    Bb: { notes: ['Bb3', 'D4', 'F4'], bass: 'Bb2' },
    F: { notes: ['F3', 'A3', 'C4'], bass: 'F2' },
    C: { notes: ['C4', 'E4', 'G4'], bass: 'C3' },
    Gm: { notes: ['G3', 'Bb3', 'D4'], bass: 'G2' },
  }, [
    [0, 0, 4, 'Dm'], [1, 0, 4, 'Bb'], [2, 0, 4, 'F'], [3, 0, 4, 'C'],
    [4, 0, 4, 'Dm'], [5, 0, 4, 'Bb'], [6, 0, 4, 'F'], [7, 0, 4, 'C'],
    [8, 0, 4, 'Bb'], [9, 0, 4, 'F'], [10, 0, 4, 'C'], [11, 0, 4, 'Dm'],
    [12, 0, 4, 'Bb'], [13, 0, 4, 'F'], [14, 0, 4, 'C'], [15, 0, 4, 'Dm'],
    [16, 0, 4, 'Dm'], [17, 0, 4, 'Dm'],
  ]);

  const HOOK = {
    1: [['A4', 0, 2], ['D5', 2, 1], ['F5', 3, 1], ['E5', 4, 2], ['D5', 6, 2]],
    2: [['C5', 0, 3], ['A4', 3, 1], ['F4', 4, 2], ['A4', 6, 2]],
    3: [['Bb4', 0, 2], ['D5', 2, 2], ['F5', 4, 2], ['E5', 6, 2]],
    4: [['D5', 0, 4], ['A4', 4, 4]],
    5: [['F5', 0, 2], ['E5', 2, 2], ['D5', 4, 2], ['C5', 6, 2]],
    6: [['D5', 0, 3], ['C5', 3, 1], ['Bb4', 4, 2], ['A4', 6, 2]],
    7: [['F4', 0, 2], ['A4', 2, 2], ['C5', 4, 4]],
    8: [['D5', 0, 2], ['C5', 2, 2], ['A4', 4, 4]],
    9: [['Bb4', 0, 2], ['D5', 2, 2], ['F5', 4, 4]],
    10: [['E5', 0, 2], ['D5', 2, 2], ['C5', 4, 4]],
    11: [['A4', 0, 8]],
    12: [['D5', 0, 4], ['F5', 4, 4]],
    13: [['E5', 0, 2], ['D5', 2, 2], ['C5', 4, 4]],
    14: [['D5', 0, 8]],
    15: [['A4', 0, 8]],
  };

  const melody = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    .flatMap((bar) => placeBar(clock, HOOK[bar], bar));

  const bassline = [];
  for (const c of chords) {
    bassline.push({ t: c.t0, dur: BEAT * 1.4, midi: c.bass });
    bassline.push({ t: c.t0 + BEAT * 2, dur: BEAT * 1.2, midi: c.bass });
  }

  const markers = {
    s1: { t: ev.steps[0], sync: 'a' },
    s2: ev.steps[1],
    s3: ev.steps[2],
    s4: { t: ev.steps[3], sync: 'a' },
    s5: { t: ev.steps[4], sync: 'a' },
    rule: ev.rule,
    table: ev.table,
  };

  const SCORE = {
    FPS, FORMAT, W, H, SAFE, WIDE, STYLE, DURATION, clock, T, BEAT, S, STEPS,
    m, chords, chordAt, ev, markers, melody, bassline,
  };
  if (node) module.exports = SCORE; else globalThis.SCORE = SCORE;
})();
