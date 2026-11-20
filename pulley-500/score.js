// THE SCORE — единый таймлайн: и музыка, и картинка читают эти события.
(function () {
  const node = typeof require !== 'undefined';
  const U = node ? require('./engine/util') : globalThis.U;
  const MU = node ? require('./engine/music') : globalThis.MUSIC;
  const { m, makeClock, placeBar, makeChords } = MU;

  const FPS = 30;
  const FORMAT = U.pickFormat('9:16');
  const [W, H] = U.formatSize(FORMAT);
  const SAFE = U.safeArea(W, H);
  const WIDE = W / H > 1.2;
  const STYLE = 'flat';

  // 120 BPM: 1 бит = 0,5 с, 1 такт = 2 с
  const clock = makeClock({ bpm: 120, offset: 0 });
  const { T, BEAT } = clock;
  const DURATION = 34;

  const S = {
    hook: [0, T(1)],
    rig: [T(1), T(2)],
    split: [T(2), T(4)],
    half1: [T(4), T(6)],
    half2: [T(6), T(8)],
    force: [T(8), T(11)],
    answer: [T(11), T(13)],
    recap: [T(13), T(16)],
    end: [T(16), DURATION],
  };

  const ev = {
    blockDrop: 0.30,
    blockLand: 1.00,   // камень встал на место
    rig: T(1),         // появляется рама: балка и блоки
    split: T(2),       // 500 -> 250 + 250
    half1: T(4),       // 250 -> 125
    half2: T(6),       // 125 -> 62,5
    arrows: T(8),      // стрелки F у рабочих
    formula: T(9),     // строка формулы
    answer: T(11),     // карточка ответа
    recap: T(13),
    end: T(16),
  };

  const { chords, chordAt } = makeChords(clock, {
    Am: { notes: ['A3', 'C4', 'E4'], bass: 'A2' },
    F: { notes: ['F3', 'A3', 'C4'], bass: 'F2' },
    C: { notes: ['G3', 'C4', 'E4'], bass: 'C3' },
    G: { notes: ['G3', 'B3', 'D4'], bass: 'G2' },
    Dm: { notes: ['D4', 'F4', 'A4'], bass: 'D3' },
    E: { notes: ['E4', 'G#4', 'B4'], bass: 'E3' },
  }, [
    [0, 0, 4, 'Am'], [1, 0, 4, 'Am'], [2, 0, 4, 'F'], [3, 0, 4, 'C'],
    [4, 0, 4, 'F'], [5, 0, 4, 'C'], [6, 0, 4, 'G'], [7, 0, 4, 'Am'],
    [8, 0, 4, 'F'], [9, 0, 4, 'C'], [10, 0, 4, 'G'], [11, 0, 4, 'Am'],
    [12, 0, 4, 'Dm'], [13, 0, 4, 'E'], [14, 0, 4, 'Am'], [15, 0, 4, 'Am'],
    [16, 0, 4, 'Am'],
  ]);

  // мелодия: восьмые, у каждой доли свой звук — как счёт «раз-два-три»
  const HOOK = {
    2: [['E5', 0, 2], ['A4', 2, 1], ['C5', 3, 1], ['E5', 4, 2], ['D5', 6, 2]],
    3: [['C5', 0, 3], ['A4', 3, 1], ['G4', 4, 2], ['A4', 6, 2]],
    4: [['F5', 0, 2], ['E5', 2, 1], ['C5', 3, 1], ['A4', 4, 4]],
    5: [['G4', 0, 2], ['A4', 2, 2], ['C5', 4, 2], ['E5', 6, 2]],
    6: [['D5', 0, 2], ['C5', 2, 2], ['B4', 4, 2], ['G4', 6, 2]],
    7: [['A4', 0, 4], ['E5', 4, 4]],
    8: [['F5', 0, 2], ['E5', 2, 2], ['C5', 4, 2], ['A4', 6, 2]],
    9: [['C5', 0, 2], ['D5', 2, 2], ['E5', 4, 4]],
    10: [['D5', 0, 2], ['B4', 2, 2], ['G4', 4, 4]],
    11: [['A4', 0, 8]],
    12: [['D5', 0, 2], ['F5', 2, 2], ['A5', 4, 4]],
    13: [['G5', 0, 2], ['E5', 2, 2], ['B4', 4, 4]],
    14: [['A5', 0, 8]],
  };

  const melody = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    .flatMap((bar) => placeBar(clock, HOOK[bar], bar));
  const plucks = melody.map((n) => ({ ...n }));
  const bassline = [];
  for (const c of chords) {
    bassline.push({ t: c.t0, dur: BEAT * 1.6, midi: c.bass });
    bassline.push({ t: c.t0 + BEAT * 2, dur: BEAT * 1.4, midi: c.bass });
  }

  // маркеры: их меряет verify (±20 мс звук, ±1 кадр картинка)
  const markers = {
    land: { t: ev.blockLand, sync: 'a' },
    rig: ev.rig,
    split: { t: ev.split, sync: 'a' },
    half1: { t: ev.half1, sync: 'a' },
    half2: { t: ev.half2, sync: 'av' },
    arrows: ev.arrows,
    answer: { t: ev.answer, sync: 'av' },
    recap: ev.recap,
    end: ev.end,
  };

  // тексты на экране (рисует film.js; здесь — чтобы song.js мог дать «щелчок» на появление)
  const captions = [
    { t: 0.15, end: T(1) - 0.1, text: 'Сколько силы нужно?' },
    { t: ev.rig, end: ev.split - 0.1, text: 'Два подвижных блока с каждой стороны' },
    { t: ev.split, end: ev.half1 - 0.1, text: 'Вес делят пополам' },
    { t: ev.half1, end: ev.half2 - 0.1, text: 'Каждый блок — ещё вдвое' },
    { t: ev.half2, end: ev.arrows, text: 'И ещё раз вдвое' },
    { t: ev.arrows, end: ev.answer - 0.1, text: 'Тянем верёвку вниз с силой F' },
    { t: ev.answer, end: ev.recap, text: 'Ответ' },
    { t: ev.recap, end: DURATION - 0.2, text: 'F = 62,5 кг на каждую верёвку' },
  ];

  const SCORE = {
    FPS, FORMAT, W, H, SAFE, WIDE, STYLE, DURATION, clock, T, BEAT, S,
    m, chords, chordAt, ev, markers, melody, plucks, bassline, captions,
  };
  if (node) module.exports = SCORE; else globalThis.SCORE = SCORE;
})();
