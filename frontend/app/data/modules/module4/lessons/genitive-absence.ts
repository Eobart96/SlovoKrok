import type { CourseLesson } from "../../../courseTypes";
import { defineModule4Lesson } from "../lessonFactory";

const baseGenitiveAbsenceLesson = defineModule4Lesson("genitive-absence", 5, {
  summary: "Niet — неизменяемая безличная форма отсутствия. После неё существительное стоит в Genitíve; личное отсутствие и отсутствие названного субъекта выражаются другими моделями.",
  model: "Niet + Genitív: Niet času. Но: Nemám čas — Akuzatív; Peter tu nie je — Nominatív.",
  goals: ["Строить niet + Genitív", "Употреблять частотные формы отсутствия", "Различать niet, nemať и nie je/nie sú", "Выбирать естественную модель"],
  rules: [
    "Niet не меняется по лицам и числам: Niet vody. Niet ľudí. Не добавляйте к нему je или sú.",
    "Слова doma, tu и nikde уточняют место, но не меняют падеж: Doma niet chleba. Tu niet miesta.",
    "Nemať сообщает, что у кого-то чего-то нет, и требует Akuzatív: Nemám čas. Nemáme vodu.",
    "Nie je/nie sú сочетаются с Nominatívom: Peter tu nie je. Deti tu nie sú.",
    "Фразы с niet могут звучать книжно; в повседневной речи часто используются nemám и nie je/nie sú.",
    "Русское «нет» не определяет словацкий падеж: сначала выберите конструкцию.",
  ],
  examples: [
    { slovak: "Niet času.", russian: "Нет времени." },
    { slovak: "Niet peňazí.", russian: "Нет денег." },
    { slovak: "Nemám knihu.", russian: "У меня нет книги." },
    { slovak: "Peter tu nie je.", russian: "Петера здесь нет." },
    { slovak: "Knihy tu nie sú.", russian: "Книг здесь нет." },
  ],
  primaryTitle: "Нужные формы Genitívu",
  primaryTable: { headers: ["Nominatív", "Genitív", "Готовая фраза"], rows: [["čas / cukor", "času / cukru", "Niet času. / Niet cukru."], ["voda / káva", "vody / kávy", "Niet vody. / Niet kávy."], ["mlieko / miesto", "mlieka / miesta", "Niet mlieka. / Niet miesta."], ["chlieb / práca", "chleba / práce", "Niet chleba. / Niet práce."], ["knihy / autá", "kníh / áut", "Niet kníh. / Niet áut."], ["ľudia / deti / peniaze", "ľudí / detí / peňazí", "Niet ľudí / detí / peňazí."]] },
  secondaryTitle: "Три способа сказать «нет»",
  secondaryTable: { headers: ["Смысл", "Модель", "Падеж", "Пример"], rows: [["нет вообще / в наличии", "niet + существительное", "Genitív", "Niet vody."], ["у кого-то нет", "nemať + объект", "Akuzatív", "Nemám vodu."], ["здесь кого-то/чего-то нет", "nie je / nie sú", "Nominatív", "Tu nie je voda."]] },
  boundaryItems: ["Niet vody — Genitív.", "Nemám vodu — Akuzatív.", "Tu nie je voda — Nominatív.", "Kniha tu nie je — Knihy tu nie sú: je/sú выбирается по числу."],
  mistake: "Не смешивайте модели: Niet času; Nemám čas; Peter tu nie je.",
  task: "Скажите, чего нет у вас, чего нет дома, кого нет дома и каких предметов здесь нет.",
  productionPrompt: "Переведите общее отсутствие: «Нет времени».",
  productionAnswer: "Niet času.",
  productionHint: "Для модели с niet используйте Genitív času.",
});

export const genitiveAbsenceLesson = {
  vocabulary: [
    {"word":"Niet vody.","translation":"Нет воды.","example":"Niet vody."},
    {"word":"Doma niet chleba.","translation":"Дома нет хлеба.","example":"Doma niet chleba."},
    {"word":"Nemám vodu.","translation":"У меня нет воды.","example":"Nemám vodu."},
    {"word":"Tu nie je voda.","translation":"Здесь нет воды.","example":"Tu nie je voda."},
    {"word":"Deti tu nie sú.","translation":"Детей здесь нет.","example":"Deti tu nie sú."},
    {"word":"Knihy tu nie sú.","translation":"Книг здесь нет.","example":"Knihy tu nie sú."},
  ],
  ...baseGenitiveAbsenceLesson,
  description: "Говорите, чего нет, и различайте niet + Genitív, nemať + Akuzatív и nie je/nie sú + Nominatív.",
  goals: ["Узнавать конструкцию niet", "Подставлять знакомые существительные в Genitív", "Различать три модели русского «нет»", "Сообщать, чего нет дома и у вас"],
  theory: {
    summary: "Genitív отвечает на koho? čoho?. В этой теме он используется после niet: сообщаем, что кого-то или чего-то нет. Конструкция безличная: в ней нет подлежащего в Nominatíve.",
    rules: [
      "Формула: niet + существительное в Genitíve. Частотные модели: Niet času. Niet vody. Niet peňazí.",
      "Niet не меняется по лицам и числам и не сочетается с je/sú: Niet vody. Niet ľudí.",
      "Место можно уточнить словами doma, tu, nikde: Doma niet chleba. Tu niet miesta. Nikde niet ľudí.",
      "Nemať означает «не иметь» и управляет Akuzatívom: Mám knihu → Nemám knihu. Отрицание само по себе не меняет падеж на Genitív.",
      "Nie je/nie sú требуют Nominatív и согласуются по числу: Peter tu nie je; Deti tu nie sú; Tu nie je voda.",
      "Tu niet vody и Tu nie je voda могут передавать один смысл, но грамматические модели различаются: vody в G, voda в N.",
      "Фразы с niet встречаются в текстах и устойчивых выражениях и иногда звучат книжно. Для повседневной речи нужны также nemám и nie je/nie sú.",
    ],
    examples: [
      { slovak: "Niet vody.", russian: "Нет воды.", explanation: "После niet используется Genitív vody." },
      { slovak: "Doma niet chleba.", russian: "Дома нет хлеба.", explanation: "Doma уточняет место; chleba остаётся в Genitíve." },
      { slovak: "Nemám vodu.", russian: "У меня нет воды.", explanation: "После nemať используется Akuzatív vodu." },
      { slovak: "Tu nie je voda.", russian: "Здесь нет воды.", explanation: "После nie je названный предмет стоит в Nominatíve." },
      { slovak: "Deti tu nie sú.", russian: "Детей здесь нет.", explanation: "Множественное число требует nie sú; deti остаётся в Nominatíve." },
      { slovak: "Knihy tu nie sú.", russian: "Книг здесь нет.", explanation: "Knihy — Nominatív множественного числа, несмотря на русский перевод." },
    ],
  },
  sections: [
    {
      title: "Нет кого? Нет чего?",
      paragraphs: ["Niet + Genitív сообщает об отсутствии: Niet času, Niet vody, Niet peňazí.", "Niet — одна неизменяемая форма настоящего времени. Не добавляйте je или sú."],
      table: { headers: ["Что отсутствует", "Slovensky", "По-русски"], rows: [["вода", "Niet vody.", "Нет воды."], ["молоко", "Niet mlieka.", "Нет молока."], ["место", "Niet miesta.", "Нет места."], ["люди", "Nikde niet ľudí.", "Нигде нет людей."]] },
      items: ["Doma niet chleba. — Дома нет хлеба.", "Tu niet miesta. — Здесь нет места.", "Málo času — мало времени; niet času — нет времени."],
      note: "Слова дома, здесь и нигде уточняют ситуацию, но после niet всё равно нужен Genitív.",
    },
    {
      title: "Нужные формы Genitívu",
      paragraphs: ["Учите пары целиком. У мужских слов встречаются -a и -u; правила «всегда -u» нет."],
      table: { headers: ["Число", "Nominatív", "Genitív после niet", "Значение"], rows: [
        ["ед.", "čas / cukor / chlieb", "času / cukru / chleba", "время / сахар / хлеб"],
        ["ед.", "voda / káva / práca", "vody / kávy / práce", "вода / кофе / работа"],
        ["ед.", "mlieko / miesto", "mlieka / miesta", "молоко / место"],
        ["мн.", "knihy / autá / študenti", "kníh / áut / študentov", "книги / машины / студенты"],
        ["мн.", "ľudia / deti / peniaze", "ľudí / detí / peňazí", "люди / дети / деньги"],
      ] },
      items: ["kniha → knihy: Genitív единственного числа — «одной книги».", "knihy → kníh: Genitív множественного числа — «книг».", "Для значения «нет книг» нужно Niet kníh.", "Сохраняйте диакритику: kníh, áut, ľudí, detí, peňazí."],
      note: "Niet knihy возможно со значением отсутствия одной книги; число выбирается по смыслу.",
    },
    {
      title: "Три способа сказать «нет»",
      paragraphs: ["Русское «нет» не указывает словацкий падеж. Сначала выберите смысловую конструкцию, затем форму существительного."],
      table: { headers: ["Ситуация", "Конструкция", "Падеж", "Пример"], rows: [["отсутствие", "niet + G", "vody", "Niet vody."], ["у кого-то нет", "nemať + A", "vodu", "Nemám vodu."], ["здесь нет", "nie je/nie sú + N", "voda", "Tu nie je voda."]] },
      items: ["У меня/у нас нет → nemám/nemáme + Akuzatív.", "Здесь нет → в обычной речи удобно nie je/nie sú + Nominatív.", "Если выбрали niet, поставьте существительное в Genitív.", "Peter tu nie je; Deti tu nie sú: форму глагола выбирает число."],
      note: "Tu niet vody и Tu nie je voda могут совпадать по смыслу; важно не смешивать их внутреннюю грамматику.",
    },
    {
      title: "Примеры для чтения вслух",
      paragraphs: ["Читайте фразу, закрывайте её и восстанавливайте по переводу. Отмечайте модель: niet → G, nemám → A, nie je/nie sú → N."],
      table: { headers: ["Slovensky", "По-русски"], rows: [
        ["Niet času.", "Нет времени."], ["Niet peňazí.", "Нет денег."], ["Niet práce.", "Нет работы."], ["Doma niet cukru.", "Дома нет сахара."],
        ["Tu niet miesta.", "Здесь нет места."], ["Niet kávy.", "Нет кофе."], ["Niet mlieka.", "Нет молока."], ["Nikde niet ľudí.", "Нигде нет людей."],
        ["Nemám knihu.", "У меня нет книги."], ["Nemám pero.", "У меня нет ручки."], ["Nemám auto.", "У меня нет машины."], ["Nemáme vodu.", "У нас нет воды."],
        ["Nemáš čas?", "У тебя нет времени?"], ["Nemám peniaze.", "У меня нет денег."], ["Peter nie je doma.", "Петра нет дома."], ["Deti tu nie sú.", "Детей здесь нет."],
        ["V obchode nie je mlieko.", "В магазине нет молока."], ["Kniha tu nie je.", "Книги здесь нет."], ["Knihy tu nie sú.", "Книг здесь нет."], ["Autá tu nie sú.", "Машин здесь нет."],
      ] },
      items: ["Máš kávu? — У тебя есть кофе?", "Nie, nemám kávu. Mám čaj. — Нет, у меня нет кофе. У меня есть чай."],
      note: "Сравните три формы одного слова: Niet vody; Nemám vodu; Tu nie je voda.",
    },
    {
      title: "Ошибки и самопроверка",
      table: { headers: ["Ошибка", "Правильно", "Почему"], rows: [["Niet je času.", "Niet času.", "После niet не ставится je."], ["Nemám kníh.", "Nemám knihu.", "Одна книга после nemám стоит в Akuzatíve."], ["Deti tu nie je.", "Deti tu nie sú.", "Deti — множественное число."], ["Tu nie je vody.", "Tu nie je voda.", "После nie je здесь нужен Nominatív."]] },
      items: ["Не смешивайте niet + G, nemať + A и nie je/nie sú + N.", "Проверяйте число: одна книга и несколько книг требуют разных форм.", "Не добавляйте je к niet.", "Сохраняйте словацкую диакритику."],
      note: "Четыре опоры: Niet vody; Nemám vodu; Tu nie je voda; русское «нет» не определяет падеж.",
    },
  ],
  stepPractices: [
    { id: "m4-genitive-absence-step-1", sectionIndex: 0, type: "pairs", prompt: "Выберите правильную форму.", answer: "vody; knihu; nie je; nie sú", pairs: [
      { prompt: "Niet (voda)", answer: "vody", options: ["voda", "vody"] }, { prompt: "Nemám (kniha)", answer: "knihu", options: ["knihu", "kníh"] },
      { prompt: "Peter tu…", answer: "nie je", options: ["nie je", "nie sú"] }, { prompt: "Deti tu…", answer: "nie sú", options: ["nie je", "nie sú"] },
    ], hint: "Сначала определите конструкцию и число.", explanation: "Правильно: Niet vody; Nemám knihu; Peter tu nie je; Deti tu nie sú." },
    { id: "m4-genitive-absence-step-2", sectionIndex: 1, type: "pairs", prompt: "Поставьте слово после niet.", answer: "času; mlieka; peňazí; ľudí; kníh; miesta", pairs: [
      { prompt: "čas", answer: "času", inputHint: "Введите форму после niet" }, { prompt: "mlieko", answer: "mlieka", inputHint: "Введите форму после niet" }, { prompt: "peniaze", answer: "peňazí", inputHint: "Введите форму после niet" },
      { prompt: "ľudia", answer: "ľudí", inputHint: "Введите форму после niet" }, { prompt: "knihy (мн. ч.)", answer: "kníh", inputHint: "Введите форму после niet" }, { prompt: "miesto", answer: "miesta", inputHint: "Введите форму после niet" },
    ], hint: "Введите только форму Genitívu.", explanation: "Формы: času, mlieka, peňazí, ľudí, kníh, miesta." },
    { id: "m4-genitive-absence-step-3", sectionIndex: 2, type: "pairs", prompt: "Определите падеж выделенной формы.", answer: "A; G; N; N", pairs: [
      { prompt: "Nemám vodu.", answer: "A", options: ["N", "G", "A"] }, { prompt: "Niet vody.", answer: "G", options: ["N", "G", "A"] },
      { prompt: "Tu nie je voda.", answer: "N", options: ["N", "G", "A"] }, { prompt: "Deti tu nie sú.", answer: "N", options: ["N", "G", "A"] },
    ], hint: "Свяжите падеж с конструкцией.", explanation: "Nemať → A; niet → G; nie je/nie sú → N." },
    { id: "m4-genitive-absence-step-4", sectionIndex: 3, type: "pairs", prompt: "Переведите по заданному началу.", answer: "Niet cukru.; Nemáme vodu.; Peter nie je doma.; Knihy tu nie sú.", pairs: [
      { prompt: "Нет сахара. (Niet…)", answer: "Niet cukru.", inputHint: "Введите полную фразу" }, { prompt: "У нас нет воды. (Nemáme…)", answer: "Nemáme vodu.", inputHint: "Введите полную фразу" },
      { prompt: "Петра нет дома. (Peter…)", answer: "Peter nie je doma.", inputHint: "Введите полную фразу" }, { prompt: "Здесь нет книг. (Knihy…)", answer: "Knihy tu nie sú.", inputHint: "Введите полную фразу" },
    ], hint: "Начало фразы указывает нужную конструкцию.", explanation: "Правильно: Niet cukru; Nemáme vodu; Peter nie je doma; Knihy tu nie sú." },
    { id: "m4-genitive-absence-step-5", sectionIndex: 4, type: "pairs", prompt: "Исправьте фразы по указанной модели.", answer: "Niet času.; Nemám knihu.; Deti tu nie sú.; Tu nie je voda.", pairs: [
      { prompt: "Niet je času. — сохранить niet", answer: "Niet času.", inputHint: "Введите исправленную фразу" }, { prompt: "Nemám kníh. — одна книга", answer: "Nemám knihu.", inputHint: "Введите исправленную фразу" },
      { prompt: "Deti tu nie je. — сохранить deti", answer: "Deti tu nie sú.", inputHint: "Введите исправленную фразу" }, { prompt: "Tu nie je vody. — сохранить nie je", answer: "Tu nie je voda.", inputHint: "Введите исправленную фразу" },
    ], hint: "Не меняйте указанную конструкцию.", explanation: "Каждая строка сохраняет заданную модель и исправляет только несовместимую часть." },
  ],
  assessmentMode: "interactive",
  materialAssessmentStep: false,
  reinforcementLabel: "Финальный тест темы",
  reinforcementTitle: "Выполните шесть заданий темы 6",
  reinforcementPractices: [
    { id: "reinforcement:genitive-absence:1", sectionIndex: 0, type: "pairs", prompt: "Выберите форму.", answer: "vody; knihu; nie je; nie sú", pairs: [
      { prompt: "Niet (voda)", answer: "vody", options: ["voda", "vody"] }, { prompt: "Nemám (kniha)", answer: "knihu", options: ["knihu", "kníh"] }, { prompt: "Peter tu…", answer: "nie je", options: ["nie je", "nie sú"] }, { prompt: "Deti tu…", answer: "nie sú", options: ["nie je", "nie sú"] },
    ], hint: "Выберите форму по конструкции.", explanation: "Правильно: vody, knihu, nie je, nie sú." },
    { id: "reinforcement:genitive-absence:2", sectionIndex: 1, type: "pairs", prompt: "Поставьте слово после niet.", answer: "času; mlieka; peňazí; ľudí; kníh; miesta", pairs: [
      { prompt: "čas", answer: "času", inputHint: "Введите форму" }, { prompt: "mlieko", answer: "mlieka", inputHint: "Введите форму" }, { prompt: "peniaze", answer: "peňazí", inputHint: "Введите форму" }, { prompt: "ľudia", answer: "ľudí", inputHint: "Введите форму" }, { prompt: "knihy (мн. ч.)", answer: "kníh", inputHint: "Введите форму" }, { prompt: "miesto", answer: "miesta", inputHint: "Введите форму" },
    ], hint: "После niet нужен Genitív.", explanation: "Формы: času, mlieka, peňazí, ľudí, kníh, miesta." },
    { id: "reinforcement:genitive-absence:3", sectionIndex: 2, type: "pairs", prompt: "Определите падеж выделенной формы.", answer: "A; G; N; N", pairs: [
      { prompt: "Nemám vodu.", answer: "A", options: ["N", "G", "A"] }, { prompt: "Niet vody.", answer: "G", options: ["N", "G", "A"] }, { prompt: "Tu nie je voda.", answer: "N", options: ["N", "G", "A"] }, { prompt: "Deti tu nie sú.", answer: "N", options: ["N", "G", "A"] },
    ], hint: "Сопоставьте конструкцию с падежом.", explanation: "Nemať → A; niet → G; nie je/nie sú → N." },
    { id: "reinforcement:genitive-absence:4", sectionIndex: 4, type: "pairs", prompt: "Исправьте по указанной модели.", answer: "Niet času.; Nemám knihu.; Deti tu nie sú.; Tu nie je voda.", pairs: [
      { prompt: "Niet je času. — сохранить niet", answer: "Niet času.", inputHint: "Введите исправленную фразу" }, { prompt: "Nemám kníh. — одна книга", answer: "Nemám knihu.", inputHint: "Введите исправленную фразу" },
      { prompt: "Deti tu nie je. — сохранить deti", answer: "Deti tu nie sú.", inputHint: "Введите исправленную фразу" }, { prompt: "Tu nie je vody. — сохранить nie je", answer: "Tu nie je voda.", inputHint: "Введите исправленную фразу" },
    ], hint: "Сохраните указанную модель.", explanation: "Правильно: Niet času; Nemám knihu; Deti tu nie sú; Tu nie je voda." },
    { id: "reinforcement:genitive-absence:5", sectionIndex: 3, type: "pairs", prompt: "Переведите по заданному началу.", answer: "Niet cukru.; Nemáme vodu.; Peter nie je doma.; Knihy tu nie sú.", pairs: [
      { prompt: "Нет сахара. (Niet…)", answer: "Niet cukru.", inputHint: "Введите перевод" },
      { prompt: "У нас нет воды. (Nemáme…)", answer: "Nemáme vodu.", acceptableAnswers: ["My nemáme vodu."], inputHint: "Введите перевод" },
      { prompt: "Петра нет дома. (Peter…)", answer: "Peter nie je doma.", inputHint: "Введите перевод" },
      { prompt: "Здесь нет книг. (Knihy…)", answer: "Knihy tu nie sú.", inputHint: "Введите перевод" },
    ], hint: "Начало указывает конструкцию и падеж.", explanation: "Нормативные модели: Niet cukru; Nemáme vodu; Peter nie je doma; Knihy tu nie sú." },
    { id: "reinforcement:genitive-absence:6", sectionIndex: 3, type: "pairs", prompt: "Выберите четыре фразы для заданных ситуаций.", answer: "Nemám auto.; Doma niet cukru.; Peter nie je doma.; Knihy tu nie sú.", pairs: [
      { prompt: "чего нет у вас", answer: "Nemám auto.", options: ["Niet auto.", "Nemám auto.", "Auto nie sú."] },
      { prompt: "чего нет дома, с niet", answer: "Doma niet cukru.", options: ["Doma niet cukor.", "Doma niet cukru.", "Doma niet je cukru."] },
      { prompt: "кого нет дома, с nie je", answer: "Peter nie je doma.", options: ["Petra nie je doma.", "Peter nie sú doma.", "Peter nie je doma."] },
      { prompt: "каких предметов здесь нет, с nie sú", answer: "Knihy tu nie sú.", options: ["Kníh tu nie sú.", "Knihy tu nie sú.", "Knihy tu nie je."] },
    ], hint: "Каждая строка закрепляет одну модель открытого задания источника.", explanation: "Четыре выбранные фразы используют nemať, niet, nie je и nie sú." },
  ],
  knowledgeChecks: [
    { id: "m4-genitive-absence-check-1", question: "Как правильно сказать «Нет времени» с niet?", options: ["Niet čas.", "Niet času.", "Niet je času."], answer: "Niet času.", explanation: "После niet нужен Genitív času; je не добавляется." },
    { id: "m4-genitive-absence-check-2", question: "Какая строка правильно различает три падежа?", options: ["Niet vody — G; Nemám vodu — A; Tu nie je voda — N", "Niet vodu — A; Nemám vody — G; Tu nie je voda — N", "Во всех трёх фразах нужен G"], answer: "Niet vody — G; Nemám vodu — A; Tu nie je voda — N", explanation: "Падеж выбирается конструкцией, а не русским словом «нет»." },
    { id: "m4-genitive-absence-check-3", question: "Как правильно сказать о нескольких детях?", options: ["Deti tu nie sú.", "Deti tu nie je.", "Detí tu nie sú."], answer: "Deti tu nie sú.", explanation: "Nie sú согласуется с множественным числом, а deti остаётся в Nominatíve." },
  ],
  finalChecks: [
    { id: "m4-genitive-absence-final-1", question: "Переведите с niet: «Нет времени».", options: ["Niet času.", "Niet čas.", "Niet je času."], answer: "Niet času.", explanation: "Niet требует Genitív času и не сочетается с je." },
  ],
  chatPrompt: "Сообщите, чего нет у вас, чего нет дома, кого нет дома и каких предметов здесь нет. Выберите подходящую конструкцию.",
  chatSuggestions: ["Nemám auto. Doma niet cukru.", "Peter nie je doma.", "Knihy tu nie sú."],
} satisfies CourseLesson;
