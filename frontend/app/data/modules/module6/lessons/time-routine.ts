import type { CourseLesson } from "../../../courseTypes";

const hourOptions = ["o šiestej", "o siedmej", "o ôsmej", "o deviatej", "o desiatej"];
const routineOptions = ["vstávam", "raňajkujem", "pracujem", "oddychujem", "spím"];

export const timeRoutineLesson = {
  vocabulary: [
    {"word":"Vstávam o siedmej.","translation":"Я встаю в семь.","example":"Vstávam o siedmej."},
    {"word":"O pol ôsmej raňajkujem.","translation":"В половине восьмого я завтракаю.","example":"O pol ôsmej raňajkujem."},
    {"word":"Potom idem do práce.","translation":"Потом я иду на работу.","example":"Potom idem do práce."},
    {"word":"Večer sa učím po slovensky.","translation":"Вечером я учу словацкий.","example":"Večer sa učím po slovensky."},
    {"word":"Najprv pracujem, potom oddychujem.","translation":"Сначала я работаю, потом отдыхаю.","example":"Najprv pracujem, potom oddychujem."},
    {"word":"O desiatej idem spať.","translation":"В десять я иду спать.","example":"O desiatej idem spať."},
  ],
  slug: "time-routine",
  order: 9,
  title: "Время и распорядок дня",
  slovakTitle: "Čas a denný režim",
  description: "Сообщайте время и описывайте ежедневную последовательность.",
  duration: "35–40 мин",
  goals: [
    "Спрашивать и сообщать время целого часа",
    "Называть частые действия ежедневного распорядка",
    "Понимать время с pol",
    "Связывать действия через najprv, potom и nakoniec",
    "Составлять короткий рассказ о своём дне",
  ],
  theory: {
    summary: "Распорядок дня уровня A1 строится из времени, знакомого действия и простого слова последовательности. Сначала научитесь отвечать на O koľkej?, затем соедините несколько коротких фраз от утра до вечера.",
    rules: [
      "Вопрос о времени действия: O koľkej vstávaš? Ответ: Vstávam o siedmej.",
      "Для целого часа после o используются формы o jednej, o druhej, o tretej, o štvrtej, o piatej, o šiestej, o siedmej, o ôsmej, o deviatej, o desiatej, o jedenástej, o dvanástej.",
      "Pol называет половину до следующего часа: o pol ôsmej — в половине восьмого, то есть в 7:30.",
      "Части дня учите целиком: ráno, dopoludnia, popoludní, večer, v noci.",
      "Последовательность: najprv — сначала, potom — потом, nakoniec — наконец. Запятая отделяет части: Najprv raňajkujem, potom idem do práce.",
      "Каждое действие ставьте в личной форме: vstávam, raňajkujem, pracujem. Не оставляйте инфинитив после слов времени или последовательности.",
    ],
    examples: [
      { slovak: "Vstávam o siedmej.", russian: "Я встаю в семь.", explanation: "O siedmej отвечает на вопрос O koľkej?" },
      { slovak: "O pol ôsmej raňajkujem.", russian: "В половине восьмого я завтракаю.", explanation: "Pol ôsmej означает 7:30." },
      { slovak: "Potom idem do práce.", russian: "Потом я иду на работу.", explanation: "Potom связывает следующее действие с предыдущим." },
      { slovak: "Večer sa učím po slovensky.", russian: "Вечером я учу словацкий.", explanation: "Večer употребляется без предлога." },
      { slovak: "Najprv pracujem, potom oddychujem.", russian: "Сначала я работаю, потом отдыхаю.", explanation: "Два действия соединены парой najprv — potom." },
      { slovak: "O desiatej idem spať.", russian: "В десять я иду спать.", explanation: "Idem spať — частотная модель завершения дня." },
    ],
  },
  sections: [
    {
      title: "Который час и во сколько",
      paragraphs: ["Koľko je hodín? спрашивает, который сейчас час. O koľkej? спрашивает, во сколько происходит действие.", "В распорядке используйте o + форму часа: o šiestej, o siedmej, o ôsmej. Учите эти формы как готовые блоки времени."],
      table: { headers: ["Вопрос или время", "Пример", "Перевод"], rows: [
        ["Koľko je hodín?", "Je sedem hodín.", "Который час? — Семь часов."],
        ["O koľkej?", "Vstávam o siedmej.", "Во сколько? — Я встаю в семь."],
        ["o šiestej", "O šiestej vstávam.", "Я встаю в шесть."],
        ["o ôsmej", "O ôsmej idem do práce.", "В восемь я иду на работу."],
        ["o desiatej", "O desiatej idem spať.", "В десять я иду спать."],
      ] },
      items: ["o jednej", "o druhej", "o tretej", "o štvrtej", "o piatej"],
      note: "Сравните: Je sedem. — Сейчас семь. Vstávam o siedmej. — Я встаю в семь.",
    },
    {
      title: "Части дня и действия",
      paragraphs: ["Для короткого распорядка достаточно частых глаголов в форме ja. Добавляйте время суток перед действием.", "Возвратную частицу сохраняйте: obliekam sa, učím sa. В нейтральной фразе она обычно стоит рядом с глаголом."],
      table: { headers: ["Когда", "Действие", "Перевод"], rows: [
        ["ráno", "vstávam", "утром я встаю"], ["ráno", "raňajkujem", "утром я завтракаю"],
        ["dopoludnia", "pracujem / študujem", "до полудня я работаю / учусь"], ["popoludní", "oddychujem", "после обеда я отдыхаю"],
        ["večer", "učím sa po slovensky", "вечером я учу словацкий"], ["v noci", "spím", "ночью я сплю"],
      ] },
      items: ["umývam sa", "obliekam sa", "idem do práce", "obedujem", "vraciam sa domov", "idem spať"],
      note: "Употребляйте готовые формы: ráno, dopoludnia, popoludní, večer, v noci.",
    },
    {
      title: "Половина часа",
      paragraphs: ["В словацком pol смотрит вперёд к следующему часу. Pol ôsmej — половина восьмого, то есть 7:30.", "Для расписания поставьте o перед всем блоком: o pol siedmej, o pol ôsmej, o pol deviatej."],
      table: { headers: ["Цифрами", "По-словацки", "Пример"], rows: [
        ["6:30", "o pol siedmej", "O pol siedmej vstávam."], ["7:30", "o pol ôsmej", "O pol ôsmej raňajkujem."],
        ["8:30", "o pol deviatej", "O pol deviatej idem do práce."], ["9:30", "o pol desiatej", "O pol desiatej pracujem."],
      ] },
      items: ["Je pol ôsmej. — Сейчас 7:30.", "Raňajkujem o pol ôsmej. — Я завтракаю в 7:30."],
      note: "Не переводите pol ôsmej как 8:30: это половина до восьми, то есть 7:30.",
    },
    {
      title: "Последовательность дня",
      paragraphs: ["Свяжите действия маршрутом najprv, potom, nakoniec. Дополнительно можно использовать ráno, popoludní и večer.", "После каждого связующего слова ставьте личную форму глагола. Для A1 достаточно трёх–пяти коротких действий."],
      table: { headers: ["Связка", "Пример", "Перевод"], rows: [
        ["najprv", "Najprv vstávam.", "Сначала я встаю."], ["potom", "Potom raňajkujem.", "Потом я завтракаю."],
        ["potom", "Potom idem do práce.", "Затем я иду на работу."], ["nakoniec", "Nakoniec idem spať.", "Наконец я иду спать."],
      ] },
      items: ["Najprv pracujem, potom oddychujem.", "Ráno vstávam o siedmej.", "Večer sa učím po slovensky."],
      note: "Запятая нужна между частями одной фразы: Najprv raňajkujem, potom idem do práce.",
    },
    {
      title: "Мой день и частые ошибки",
      paragraphs: ["Составьте профиль дня: время подъёма, утреннее действие, работа или учёба, отдых и завершение дня. Не нужно описывать каждую минуту.", "Перед ответом проверьте форму часа, значение pol, личную форму глагола, частицу sa и словацкую диакритику."],
      table: { headers: ["Ошибка", "Правильно", "Почему"], rows: [
        ["Vstávam o sedem.", "Vstávam o siedmej.", "После o нужна форма siedmej."], ["7:30 = o pol siedmej", "7:30 = o pol ôsmej", "Pol называет следующий час."],
        ["Večer učím sa.", "Večer sa učím.", "В нейтральной модели sa стоит перед глаголом."], ["Potom ísť do práce.", "Potom idem do práce.", "Нужна личная форма idem."],
        ["O pol osmej ranajkujem.", "O pol ôsmej raňajkujem.", "Нужна словацкая диакритика."],
      ] },
      items: ["Ráno vstávam o siedmej.", "O pol ôsmej raňajkujem.", "Potom idem do práce.", "Večer oddychujem.", "O desiatej idem spať."],
      note: "Точные стилистические варианты времени не систематизируются полностью.",
    },
  ],
  stepPractices: [
    { id: "m6-time-routine-step-1", sectionIndex: 0, type: "pairs", prompt: "Выберите правильную форму часа.", answer: "o šiestej; o siedmej; o ôsmej; o deviatej; o desiatej", pairs: [
      { prompt: "в шесть", answer: "o šiestej", options: hourOptions }, { prompt: "в семь", answer: "o siedmej", options: hourOptions }, { prompt: "в восемь", answer: "o ôsmej", options: hourOptions }, { prompt: "в девять", answer: "o deviatej", options: hourOptions }, { prompt: "в десять", answer: "o desiatej", options: hourOptions },
    ], showSlovakKeyboard: false, hint: "Сопоставьте числовое время с формой после o.", explanation: "После o используются формы šiestej, siedmej, ôsmej, deviatej и desiatej." },
    { id: "m6-time-routine-step-2", sectionIndex: 1, type: "pairs", prompt: "Выберите действие распорядка.", answer: "vstávam; raňajkujem; pracujem; oddychujem; spím", pairs: [
      { prompt: "Я встаю.", answer: "vstávam", options: routineOptions }, { prompt: "Я завтракаю.", answer: "raňajkujem", options: routineOptions }, { prompt: "Я работаю.", answer: "pracujem", options: routineOptions }, { prompt: "Я отдыхаю.", answer: "oddychujem", options: routineOptions }, { prompt: "Я сплю.", answer: "spím", options: routineOptions },
    ], hint: "Сопоставьте русское действие с формой ja.", explanation: "Все ответы — личные формы глаголов ежедневного распорядка." },
    { id: "m6-time-routine-step-3", sectionIndex: 2, type: "pairs", prompt: "Выберите время с pol.", answer: "o pol siedmej; o pol ôsmej; o pol deviatej; o pol desiatej", pairs: [
      { prompt: "6:30", answer: "o pol siedmej", options: ["o pol siedmej", "o pol ôsmej", "o pol deviatej", "o pol desiatej"] },
      { prompt: "7:30", answer: "o pol ôsmej", options: ["o pol siedmej", "o pol ôsmej", "o pol deviatej", "o pol desiatej"] },
      { prompt: "8:30", answer: "o pol deviatej", options: ["o pol siedmej", "o pol ôsmej", "o pol deviatej", "o pol desiatej"] },
      { prompt: "9:30", answer: "o pol desiatej", options: ["o pol siedmej", "o pol ôsmej", "o pol deviatej", "o pol desiatej"] },
    ], showSlovakKeyboard: false, hint: "Pol называет следующий час.", explanation: "Например, 7:30 — o pol ôsmej." },
    { id: "m6-time-routine-step-4", sectionIndex: 3, type: "pairs", prompt: "Выберите связку последовательности.", answer: "Najprv; Potom; Potom; Nakoniec", pairs: [
      { prompt: "___ vstávam. · сначала", answer: "Najprv", options: ["Najprv", "Potom", "Nakoniec"] }, { prompt: "___ raňajkujem. · потом", answer: "Potom", options: ["Najprv", "Potom", "Nakoniec"] },
      { prompt: "___ idem do práce. · затем", answer: "Potom", options: ["Najprv", "Potom", "Nakoniec"] }, { prompt: "___ idem spať. · наконец", answer: "Nakoniec", options: ["Najprv", "Potom", "Nakoniec"] },
    ], hint: "Определите первый, следующий и последний шаг.", explanation: "Najprv начинает последовательность, potom продолжает, nakoniec завершает." },
    { id: "m6-time-routine-step-5", sectionIndex: 4, type: "pairs", prompt: "Исправьте каждую фразу.", answer: "Vstávam o siedmej.; O pol ôsmej raňajkujem.; Večer sa učím po slovensky.; Potom idem do práce.; Najprv pracujem, potom oddychujem.", pairs: [
      { prompt: "Vstávam o sedem.", answer: "Vstávam o siedmej.", inputHint: "Введите исправленную фразу" }, { prompt: "O pol osmej ranajkujem.", answer: "O pol ôsmej raňajkujem.", inputHint: "Введите исправленную фразу" },
      { prompt: "Večer učím sa po slovensky.", answer: "Večer sa učím po slovensky.", inputHint: "Введите исправленную фразу" }, { prompt: "Potom ísť do práce.", answer: "Potom idem do práce.", inputHint: "Введите исправленную фразу" },
      { prompt: "Переведите: «Сначала работаю, потом отдыхаю».", answer: "Najprv pracujem, potom oddychujem.", inputHint: "Введите перевод" },
    ], hint: "Проверьте час, pol, sa, личную форму и диакритику.", explanation: "Нормативны o siedmej, o pol ôsmej, sa učím, idem и najprv — potom." },
  ],
  assessmentMode: "interactive",
  materialAssessmentStep: false,
  reinforcementLabel: "Финальный тест темы",
  reinforcementTitle: "Выполните шесть заданий темы 9",
  reinforcementPractices: [
    { id: "reinforcement:time-routine:1", sectionIndex: 0, type: "pairs", prompt: "Выберите форму времени для каждого часа.", answer: "o šiestej; o siedmej; o ôsmej; o deviatej; o desiatej", pairs: [
      { prompt: "6:00", answer: "o šiestej", options: hourOptions }, { prompt: "7:00", answer: "o siedmej", options: hourOptions }, { prompt: "8:00", answer: "o ôsmej", options: hourOptions }, { prompt: "9:00", answer: "o deviatej", options: hourOptions }, { prompt: "10:00", answer: "o desiatej", options: hourOptions },
    ], showSlovakKeyboard: false, hint: "Выберите форму часа после o.", explanation: "Каждая строка проверяет один целый час." },
    { id: "reinforcement:time-routine:2", sectionIndex: 1, type: "pairs", prompt: "Дополните распорядок подходящим действием.", answer: "vstávam; raňajkujem; pracujem; oddychujem; spím", pairs: [
      { prompt: "Ráno ___. · встаю", answer: "vstávam", options: routineOptions }, { prompt: "O pol ôsmej ___. · завтракаю", answer: "raňajkujem", options: routineOptions }, { prompt: "Dopoludnia ___. · работаю", answer: "pracujem", options: routineOptions }, { prompt: "Popoludní ___. · отдыхаю", answer: "oddychujem", options: routineOptions }, { prompt: "V noci ___. · сплю", answer: "spím", options: routineOptions },
    ], hint: "Смотрите на часть дня и русский глагол.", explanation: "Пять глаголов образуют простой распорядок от утра до ночи." },
    { id: "reinforcement:time-routine:3", sectionIndex: 2, type: "pairs", prompt: "Выберите точное время.", answer: "o šiestej; o pol siedmej; o siedmej; o pol ôsmej; o ôsmej", pairs: [
      { prompt: "6:00", answer: "o šiestej", options: ["o šiestej", "o pol siedmej", "o siedmej", "o pol ôsmej", "o ôsmej"] }, { prompt: "6:30", answer: "o pol siedmej", options: ["o šiestej", "o pol siedmej", "o siedmej", "o pol ôsmej", "o ôsmej"] },
      { prompt: "7:00", answer: "o siedmej", options: ["o šiestej", "o pol siedmej", "o siedmej", "o pol ôsmej", "o ôsmej"] }, { prompt: "7:30", answer: "o pol ôsmej", options: ["o šiestej", "o pol siedmej", "o siedmej", "o pol ôsmej", "o ôsmej"] },
      { prompt: "8:00", answer: "o ôsmej", options: ["o šiestej", "o pol siedmej", "o siedmej", "o pol ôsmej", "o ôsmej"] },
    ], showSlovakKeyboard: false, hint: "Отличайте целый час от половины до следующего часа.", explanation: "Pol всегда смотрит к следующему часу." },
    { id: "reinforcement:time-routine:4", sectionIndex: 4, type: "pairs", prompt: "Исправьте ошибки в распорядке.", answer: "Vstávam o siedmej.; O pol ôsmej raňajkujem.; Večer sa učím.; Potom idem do práce.; Nakoniec idem spať.", pairs: [
      { prompt: "Vstávam o sedem.", answer: "Vstávam o siedmej.", inputHint: "Введите исправленную фразу" }, { prompt: "O pol osmej ranajkujem.", answer: "O pol ôsmej raňajkujem.", inputHint: "Введите исправленную фразу" },
      { prompt: "Večer učím sa.", answer: "Večer sa učím.", inputHint: "Введите исправленную фразу" }, { prompt: "Potom ísť do práce.", answer: "Potom idem do práce.", inputHint: "Введите исправленную фразу" },
      { prompt: "Nakoniec idem spať", answer: "Nakoniec idem spať.", inputHint: "Введите исправленную фразу" },
    ], hint: "Исправьте всю строку: форму часа, порядок sa, глагол и написание.", explanation: "Распорядок требует формы после o и личных глагольных форм." },
    { id: "reinforcement:time-routine:5", sectionIndex: 4, type: "pairs", prompt: "Переведите на словацкий.", answer: "Vstávam o siedmej.; O pol ôsmej raňajkujem.; Potom idem do práce.; Večer sa učím po slovensky.; Najprv pracujem, potom oddychujem.", pairs: [
      { prompt: "Я встаю в семь.", answer: "Vstávam o siedmej.", acceptableAnswers: ["O siedmej vstávam."], inputHint: "Введите перевод" },
      { prompt: "В половине восьмого я завтракаю.", answer: "O pol ôsmej raňajkujem.", acceptableAnswers: ["Raňajkujem o pol ôsmej."], inputHint: "Введите перевод" },
      { prompt: "Потом я иду на работу.", answer: "Potom idem do práce.", inputHint: "Введите перевод" }, { prompt: "Вечером я учу словацкий.", answer: "Večer sa učím po slovensky.", inputHint: "Введите перевод" },
      { prompt: "Сначала я работаю, потом отдыхаю.", answer: "Najprv pracujem, potom oddychujem.", inputHint: "Введите перевод" },
    ], hint: "Используйте модели урока и сохраните словацкую диакритику.", explanation: "Переводы проверяют целый час, pol, последовательность и возвратную частицу." },
    { id: "reinforcement:time-routine:6", sectionIndex: 4, type: "pairs", prompt: "Соберите распорядок дня по порядку.", answer: "Ráno vstávam o siedmej.; O pol ôsmej raňajkujem.; Potom idem do práce.; Popoludní oddychujem.; Večer sa učím po slovensky.; O desiatej idem spať.", pairs: [
      { prompt: "1 · подъём", answer: "Ráno vstávam o siedmej.", options: ["Ráno vstávam o siedmej.", "Ráno vstávať o sedem.", "V noci vstávam o siedmej."] },
      { prompt: "2 · завтрак", answer: "O pol ôsmej raňajkujem.", options: ["O pol siedmej raňajkujem.", "O pol ôsmej raňajkujem.", "O pol osem raňajkujem."] },
      { prompt: "3 · дорога на работу", answer: "Potom idem do práce.", options: ["Potom idem do práce.", "Najprv ísť do práce.", "Potom idem v práca."] },
      { prompt: "4 · отдых", answer: "Popoludní oddychujem.", options: ["Popoludnie oddychovať.", "Popoludní oddychujem.", "V popoludní oddychujem."] },
      { prompt: "5 · словацкий", answer: "Večer sa učím po slovensky.", options: ["Večer učím sa slovensky.", "Večer sa učím po slovensky.", "Na večer sa učiť slovenský."] },
      { prompt: "6 · сон", answer: "O desiatej idem spať.", options: ["O desiatej idem spať.", "O desať idem spať.", "O desiatej idem spím."] },
    ], hint: "Следуйте маршруту от утра к вечеру.", explanation: "Цельный профиль соединяет время, личные формы и части дня." },
  ],
  knowledgeChecks: [
    { id: "m6-time-routine-check-1", question: "Как сказать «Я встаю в семь»?", options: ["Vstávam o siedmej.", "Vstávam o sedem.", "Vstávať siedmej."], answer: "Vstávam o siedmej.", explanation: "После o используется форма siedmej." },
    { id: "m6-time-routine-check-2", question: "Как сказать «В половине восьмого я завтракаю»?", options: ["O pol ôsmej raňajkujem.", "O pol siedmej raňajkujem.", "O ôsmej pol raňajkujem."], answer: "O pol ôsmej raňajkujem.", explanation: "Pol ôsmej означает 7:30." },
    { id: "m6-time-routine-check-3", question: "Какая граница соответствует уровню A1?", options: ["Точные стилистические варианты времени не систематизируются полностью.", "Нужно освоить все разговорные варианты времени.", "Нужно свободно описывать сложное расписание."], answer: "Точные стилистические варианты времени не систематизируются полностью.", explanation: "На A1 достаточно целого часа, pol и короткого распорядка." },
  ],
  finalChecks: [
    { id: "m6-time-routine-final-1", question: "Переведите: «Сначала работаю, потом отдыхаю».", options: ["Najprv pracujem, potom oddychujem.", "Najprv pracovať, potom oddychovať.", "Potom pracujem, najprv oddychujem."], answer: "Najprv pracujem, potom oddychujem.", explanation: "Последовательность передают najprv — potom, оба глагола стоят в личной форме." },
  ],
  chatPrompt: "Опишите свой день пятью короткими фразами: подъём, завтрак, работа или учёба, отдых и сон.",
  chatSuggestions: ["Vstávam o siedmej.", "O pol ôsmej raňajkujem.", "Potom idem do práce."],
} satisfies CourseLesson;
