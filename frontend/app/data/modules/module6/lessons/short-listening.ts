import type { CourseLesson } from "../../../courseTypes";

const situationOptions = ["doprava", "otváracie hodiny", "stretnutie", "pokyn", "počasie"];
const timeOptions = ["päť", "desať minút", "do šiestej", "o ôsmej", "zajtra"];
const placeOptions = ["na stanici", "pri dverách", "pred kinom", "na zastávke", "v lekárni"];
const actionOptions = ["príde", "čakajte", "odchádza", "stretneme sa", "zopakujte"];

export const shortListeningLesson = {
  listening: [
    { id: "short-listening-audio-bus", audio: "/audio/short-listening/bus.mp3", transcript: "Autobus číslo päť príde o desať minút.", question: "Какой автобус и через сколько минут прибудет?", options: ["Автобус 10 через 5 минут", "Автобус 5 через 10 минут", "Автобус 5 в 10 часов"], answer: "Автобус 5 через 10 минут", explanation: "Číslo päť — номер 5; o desať minút — через 10 минут." },
    { id: "short-listening-audio-pharmacy", audio: "/audio/short-listening/pharmacy.mp3", transcript: "Lekáreň je dnes otvorená do šiestej.", question: "До которого часа сегодня открыта аптека?", options: ["До пяти", "До восьми", "До шести"], answer: "До шести", explanation: "Do šiestej обозначает границу времени: до шести." },
    { id: "short-listening-audio-meeting", audio: "/audio/short-listening/meeting.mp3", transcript: "Stretneme sa na stanici. Vlak odchádza o ôsmej.", question: "Где встреча и во сколько отправляется поезд?", options: ["На вокзале; в восемь", "На остановке; через восемь минут", "На вокзале; в шесть"], answer: "На вокзале; в восемь", explanation: "Na stanici — на вокзале; odchádza o ôsmej — отправляется в восемь." },
  ],
  vocabulary: [
    {"word":"Autobus číslo päť príde o desať minút.","translation":"Автобус номер пять прибудет через десять минут.","example":"Autobus číslo päť príde o desať minút."},
    {"word":"Lekáreň je dnes otvorená do šiestej.","translation":"Аптека сегодня открыта до шести.","example":"Lekáreň je dnes otvorená do šiestej."},
    {"word":"Stretneme sa na stanici.","translation":"Встретимся на вокзале.","example":"Stretneme sa na stanici."},
    {"word":"Prosím, čakajte pri dverách.","translation":"Пожалуйста, ждите у двери.","example":"Prosím, čakajte pri dverách."},
    {"word":"Vlak odchádza o ôsmej.","translation":"Поезд отправляется в восемь.","example":"Vlak odchádza o ôsmej."},
    {"word":"Prosím, zopakujte to.","translation":"Пожалуйста, повторите это.","example":"Prosím, zopakujte to."},
  ],
  slug: "short-listening",
  order: 18,
  title: "Короткие устные сообщения",
  slovakTitle: "Krátke hovorené správy",
  description: "Распознавайте ситуацию, числа, время, место и главное действие в короткой ясной реплике.",
  duration: "35–40 мин",
  goals: [
    "Определять знакомую ситуацию по нескольким опорным словам",
    "Распознавать номера, время и длительность",
    "Находить место встречи или ожидания",
    "Понимать главное действие или инструкцию",
    "Проверять один-два важных факта при повторе сообщения",
  ],
  theory: {
    summary: "При медленной ясной речи уровня A1 не нужно записывать каждое слово. Во время первого прослушивания определите ситуацию и главное действие; во время второго проверьте число, время или место. В уроке короткие реплики показаны текстом как учебные сценарии понимания, а не как аудиозаписи.",
    rules: [
      "Первый проход: определите тему по словам autobus/vlak, otvorená, stretneme sa, čakajte или počasie.",
      "Второй проход: зафиксируйте одно число или время — číslo päť, o desať minút, do šiestej, o ôsmej.",
      "Предлоги помогают найти место: na stanici, na zastávke, pred kinom, pri dverách, v lekárni.",
      "Главный глагол сообщает действие: príde, odchádza, stretneme sa, čakajte, zopakujte.",
      "Если важная деталь неясна, попросите: Prosím, zopakujte to. Полная дословная транскрипция для этой задачи не нужна.",
    ],
    examples: [
      { slovak: "Autobus číslo päť príde o desať minút.", russian: "Автобус номер пять прибудет через десять минут.", explanation: "Ключевые факты: autobus 5 и ожидание 10 минут." },
      { slovak: "Lekáreň je dnes otvorená do šiestej.", russian: "Аптека сегодня открыта до шести.", explanation: "Место — аптека, граница времени — до шести." },
      { slovak: "Stretneme sa na stanici.", russian: "Встретимся на вокзале.", explanation: "Действие и место слышны в stretneme sa + na stanici." },
      { slovak: "Prosím, čakajte pri dverách.", russian: "Пожалуйста, ждите у двери.", explanation: "Инструкция — ждать; место — у двери." },
      { slovak: "Vlak odchádza o ôsmej.", russian: "Поезд отправляется в восемь.", explanation: "Odchádza сообщает отправление, o ôsmej — время." },
      { slovak: "Prosím, zopakujte to.", russian: "Пожалуйста, повторите это.", explanation: "Фраза помогает уточнить непонятую деталь." },
    ],
  },
  sections: [
    {
      title: "Сначала определите ситуацию",
      paragraphs: ["Не начинайте с перевода каждого слова. Услышьте одно-два существительных и глагол: autobus + príde дают транспорт, lekáreň + otvorená — часы работы.", "Ситуация сужает возможный смысл остальных слов и помогает не потеряться из-за незнакомой детали."],
      table: { headers: ["Опорные слова", "Ситуация", "Что важно"], rows: [
        ["autobus, vlak, príde", "doprava", "номер и время"], ["lekáreň, otvorená", "otváracie hodiny", "до какого часа"],
        ["stretneme sa", "stretnutie", "где и когда"], ["prosím, čakajte", "pokyn", "что сделать и где"],
        ["prší, bude chladno", "počasie", "погода и решение"],
      ] },
      items: ["Kto alebo čo? — Кто или что?", "Aká je situácia? — Какая ситуация?", "Čo je dôležité? — Что важно?"],
      note: "Первый результат слушания — тема и главное действие, а не полный перевод.",
    },
    {
      title: "Числа, время и длительность",
      paragraphs: ["Числа могут обозначать номер маршрута, часы или длительность ожидания. Всегда связывайте число с соседним словом.", "Číslo päť — номер пять; o piatej — в пять часов; o desať minút — через десять минут."],
      table: { headers: ["Фрагмент", "Что означает", "Факт"], rows: [
        ["autobus číslo päť", "номер маршрута", "5"], ["o desať minút", "через сколько", "10 минут"],
        ["do šiestej", "до какого часа", "до 6"], ["o ôsmej", "во сколько", "в 8"],
        ["zajtra", "когда", "завтра"],
      ] },
      items: ["päť ≠ o piatej: номер и время имеют разную форму.", "minúta / minúty / minút — в готовой фразе o desať minút.", "Прослушайте число ещё раз, если от него зависит действие."],
      note: "Запишите число вместе с функцией: автобус 5, в 8, через 10 минут.",
    },
    {
      title: "Место и направление",
      paragraphs: ["После ключевого действия слушайте короткий блок с предлогом. Обычно весь блок можно запомнить как одну единицу.", "Na stanici и na zastávke — место; pred kinom — перед кинотеатром; pri dverách — у двери."],
      table: { headers: ["Блок", "Перевод", "Вопрос"], rows: [
        ["na stanici", "на вокзале", "где встречаемся?"], ["pri dverách", "у двери", "где ждать?"],
        ["pred kinom", "перед кинотеатром", "где встречаемся?"], ["na zastávke", "на остановке", "где ждать транспорт?"],
        ["v lekárni", "в аптеке", "где происходит ситуация?"],
      ] },
      items: ["Stretneme sa na stanici.", "Čakajte pri dverách.", "Autobus stojí na zastávke."],
      note: "Не отделяйте предлог от существительного: запоминайте na stanici, pri dverách целиком.",
    },
    {
      title: "Главное действие и инструкция",
      paragraphs: ["Глагол показывает, что произойдёт или что нужно сделать. В транспортном сообщении различайте príde и odchádza.", "Формы čakajte и zopakujte обращены вежливо к одному человеку или к нескольким людям."],
      table: { headers: ["Глагол", "Значение", "Пример"], rows: [
        ["príde", "прибудет", "Autobus príde."], ["odchádza", "отправляется", "Vlak odchádza."],
        ["stretneme sa", "встретимся", "Stretneme sa na stanici."], ["čakajte", "ждите", "Čakajte pri dverách."],
        ["zopakujte", "повторите", "Prosím, zopakujte to."],
      ] },
      items: ["Príďte o piatej. — Придите в пять.", "Choďte na nástupište dva. — Идите на платформу два.", "Počkajte desať minút. — Подождите десять минут."],
      note: "Сначала поймите действие, затем добавьте к нему время или место.",
    },
    {
      title: "Повторное слушание и частые ошибки",
      paragraphs: ["После первого прохода сформулируйте короткий ответ: кто/что + действие. После второго добавьте один-два факта: номер, время или место.", "Если факт всё ещё неясен, попросите повторить. Не заменяйте услышанное догадкой и не смешивайте данные двух сообщений."],
      table: { headers: ["Ошибка", "Правильно", "Что различать"], rows: [
        ["Autobus päť príde o piatej.", "Autobus číslo päť príde o desať minút.", "номер и длительность"], ["Lekáreň je otvorený.", "Lekáreň je otvorená.", "род слова lekáreň"],
        ["Stretneme na stanici.", "Stretneme sa na stanici.", "частицу sa"], ["Čakajte na dverách.", "Čakajte pri dverách.", "предлог места"],
        ["Vlak odchádza v ôsmej.", "Vlak odchádza o ôsmej.", "предлог времени"],
      ] },
      items: ["1. Какая ситуация?", "2. Какое главное действие?", "3. Какое число, время или место нужно проверить?", "4. Нужно ли попросить повторить?"],
      note: "Текстовые реплики этого урока моделируют содержание слушания; настоящую речь полезно дополнительно тренировать с преподавателем или аудиоматериалом.",
    },
  ],
  stepPractices: [
    { id: "m6-short-listening-step-1", sectionIndex: 0, type: "pairs", prompt: "Определите ситуацию по короткой реплике.", answer: "doprava; otváracie hodiny; stretnutie; pokyn; počasie", pairs: [
      { prompt: "Autobus číslo päť príde.", answer: "doprava", options: situationOptions }, { prompt: "Lekáreň je otvorená do šiestej.", answer: "otváracie hodiny", options: situationOptions },
      { prompt: "Stretneme sa na stanici.", answer: "stretnutie", options: situationOptions }, { prompt: "Prosím, čakajte pri dverách.", answer: "pokyn", options: situationOptions },
      { prompt: "Zajtra bude chladno.", answer: "počasie", options: situationOptions },
    ], hint: "Ищите существительное и главный глагол.", explanation: "Опорные слова позволяют определить ситуацию до понимания всех деталей." },
    { id: "m6-short-listening-step-2", sectionIndex: 1, type: "pairs", prompt: "Выберите услышанное число или время.", answer: "päť; desať minút; do šiestej; o ôsmej; zajtra", pairs: [
      { prompt: "Autobus číslo ___.", answer: "päť", options: timeOptions }, { prompt: "Príde o ___.", answer: "desať minút", options: timeOptions },
      { prompt: "Otvorená ___.", answer: "do šiestej", options: timeOptions }, { prompt: "Vlak odchádza ___.", answer: "o ôsmej", options: timeOptions },
      { prompt: "Stretneme sa ___.", answer: "zajtra", options: timeOptions },
    ], hint: "Свяжите число с номером, временем или длительностью.", explanation: "Одинаковая цифра может звучать по-разному в разных функциях." },
    { id: "m6-short-listening-step-3", sectionIndex: 2, type: "pairs", prompt: "Выберите место из реплики.", answer: "na stanici; pri dverách; pred kinom; na zastávke; v lekárni", pairs: [
      { prompt: "Stretneme sa ___.", answer: "na stanici", options: placeOptions }, { prompt: "Čakajte ___.", answer: "pri dverách", options: placeOptions },
      { prompt: "Stretneme sa ___. · перед кинотеатром", answer: "pred kinom", options: placeOptions }, { prompt: "Autobus stojí ___.", answer: "na zastávke", options: placeOptions },
      { prompt: "Liek kúpim ___.", answer: "v lekárni", options: placeOptions },
    ], hint: "Выбирайте предлог вместе с существительным.", explanation: "Цельный блок места легче распознать и запомнить." },
    { id: "m6-short-listening-step-4", sectionIndex: 3, type: "pairs", prompt: "Выберите главное действие.", answer: "príde; čakajte; odchádza; stretneme sa; zopakujte", pairs: [
      { prompt: "Autobus ___ o desať minút.", answer: "príde", options: actionOptions }, { prompt: "Prosím, ___ pri dverách.", answer: "čakajte", options: actionOptions },
      { prompt: "Vlak ___ o ôsmej.", answer: "odchádza", options: actionOptions }, { prompt: "Zajtra ___ na stanici.", answer: "stretneme sa", options: actionOptions },
      { prompt: "Prosím, ___ to.", answer: "zopakujte", options: actionOptions },
    ], hint: "Определите, что произойдёт или что просят сделать.", explanation: "Главный глагол несёт практическую цель устного сообщения." },
    { id: "m6-short-listening-step-5", sectionIndex: 4, type: "pairs", prompt: "Исправьте неточно переданную реплику.", answer: "Autobus číslo päť príde o desať minút.; Lekáreň je otvorená do šiestej.; Stretneme sa na stanici.; Čakajte pri dverách.; Vlak odchádza o ôsmej.", pairs: [
      { prompt: "Autobus päť príde o piatej.", answer: "Autobus číslo päť príde o desať minút.", inputHint: "Введите точную реплику" }, { prompt: "Lekáreň je otvorený do šiestej.", answer: "Lekáreň je otvorená do šiestej.", inputHint: "Введите точную реплику" },
      { prompt: "Stretneme na stanici.", answer: "Stretneme sa na stanici.", inputHint: "Введите точную реплику" }, { prompt: "Čakajte na dverách.", answer: "Čakajte pri dverách.", inputHint: "Введите точную реплику" },
      { prompt: "Vlak odchádza v ôsmej.", answer: "Vlak odchádza o ôsmej.", inputHint: "Введите точную реплику" },
    ], hint: "Проверьте номер, время, согласование, sa и предлог.", explanation: "Точная короткая запись сохраняет практический смысл услышанного." },
  ],
  assessmentMode: "interactive",
  materialAssessmentStep: false,
  reinforcementLabel: "Финальный тест темы",
  reinforcementTitle: "Выполните шесть заданий темы 18",
  reinforcementPractices: [
    { id: "reinforcement:short-listening:1", sectionIndex: 0, type: "pairs", prompt: "Определите ситуацию каждой реплики.", answer: "doprava; otváracie hodiny; stretnutie; pokyn; počasie", pairs: [
      { prompt: "Autobus príde o desať minút.", answer: "doprava", options: situationOptions }, { prompt: "Lekáreň je otvorená do šiestej.", answer: "otváracie hodiny", options: situationOptions },
      { prompt: "Stretneme sa na stanici.", answer: "stretnutie", options: situationOptions }, { prompt: "Čakajte pri dverách.", answer: "pokyn", options: situationOptions }, { prompt: "Zajtra bude pršať.", answer: "počasie", options: situationOptions },
    ], hint: "Найдите опорные существительные и глаголы.", explanation: "Первый проход определяет ситуацию и цель сообщения." },
    { id: "reinforcement:short-listening:2", sectionIndex: 1, type: "pairs", prompt: "Выберите ключевое число или время.", answer: "päť; desať minút; do šiestej; o ôsmej; zajtra", pairs: [
      { prompt: "номер автобуса", answer: "päť", options: timeOptions }, { prompt: "через сколько прибудет", answer: "desať minút", options: timeOptions },
      { prompt: "до какого часа открыта аптека", answer: "do šiestej", options: timeOptions }, { prompt: "когда отправляется поезд", answer: "o ôsmej", options: timeOptions }, { prompt: "день встречи", answer: "zajtra", options: timeOptions },
    ], hint: "Свяжите форму числа с её функцией.", explanation: "Номер, час, длительность и день отвечают на разные вопросы." },
    { id: "reinforcement:short-listening:3", sectionIndex: 2, type: "pairs", prompt: "Выберите место из сообщения.", answer: "na stanici; pri dverách; pred kinom; na zastávke; v lekárni", pairs: [
      { prompt: "место встречи", answer: "na stanici", options: placeOptions }, { prompt: "место ожидания", answer: "pri dverách", options: placeOptions },
      { prompt: "место встречи у кинотеатра", answer: "pred kinom", options: placeOptions }, { prompt: "место автобуса", answer: "na zastávke", options: placeOptions }, { prompt: "место покупки лекарства", answer: "v lekárni", options: placeOptions },
    ], hint: "Выбирайте полный предложный блок.", explanation: "Предлог и существительное вместе передают место." },
    { id: "reinforcement:short-listening:4", sectionIndex: 3, type: "pairs", prompt: "Выберите главное действие сообщения.", answer: "príde; čakajte; odchádza; stretneme sa; zopakujte", pairs: [
      { prompt: "автобус · прибудет", answer: "príde", options: actionOptions }, { prompt: "пожалуйста · ждите", answer: "čakajte", options: actionOptions },
      { prompt: "поезд · отправляется", answer: "odchádza", options: actionOptions }, { prompt: "мы · встретимся", answer: "stretneme sa", options: actionOptions }, { prompt: "пожалуйста · повторите", answer: "zopakujte", options: actionOptions },
    ], hint: "Определите действие по субъекту и русской подсказке.", explanation: "Глагол показывает событие или требуемое действие." },
    { id: "reinforcement:short-listening:5", sectionIndex: 4, type: "pairs", prompt: "Передайте ключевую информацию по-словацки.", answer: "Autobus číslo päť príde o desať minút.; Lekáreň je dnes otvorená do šiestej.; Stretneme sa na stanici.; Prosím, čakajte pri dverách.; Vlak odchádza o ôsmej.", pairs: [
      { prompt: "Автобус номер пять прибудет через десять минут.", answer: "Autobus číslo päť príde o desať minút.", acceptableAnswers: ["O desať minút príde autobus číslo päť."], inputHint: "Введите ключевую реплику" },
      { prompt: "Аптека сегодня открыта до шести.", answer: "Lekáreň je dnes otvorená do šiestej.", inputHint: "Введите ключевую реплику" },
      { prompt: "Встретимся на вокзале.", answer: "Stretneme sa na stanici.", inputHint: "Введите ключевую реплику" },
      { prompt: "Пожалуйста, ждите у двери.", answer: "Prosím, čakajte pri dverách.", inputHint: "Введите ключевую реплику" },
      { prompt: "Поезд отправляется в восемь.", answer: "Vlak odchádza o ôsmej.", inputHint: "Введите ключевую реплику" },
    ], hint: "Сохраните ключевые факты и словацкую диакритику.", explanation: "Короткая запись передаёт субъект, действие и нужную деталь." },
    { id: "reinforcement:short-listening:6", sectionIndex: 4, type: "pairs", prompt: "Выберите точный вывод из каждой реплики.", answer: "Нужно ждать автобус 10 минут.; Аптека закрывается в 6.; Встреча будет на вокзале.; Нужно ждать у двери.; Поезд отправляется в 8.", pairs: [
      { prompt: "Autobus číslo päť príde o desať minút.", answer: "Нужно ждать автобус 10 минут.", options: ["Нужно ждать автобус 10 минут.", "Автобус едет 5 минут.", "Автобус отправляется в 10."] },
      { prompt: "Lekáreň je otvorená do šiestej.", answer: "Аптека закрывается в 6.", options: ["Аптека закрывается в 6.", "Аптека открывается в 6.", "Аптека закрыта весь день."] },
      { prompt: "Stretneme sa na stanici.", answer: "Встреча будет на вокзале.", options: ["Встреча будет на вокзале.", "Поезд будет на остановке.", "Встреча будет у аптеки."] },
      { prompt: "Prosím, čakajte pri dverách.", answer: "Нужно ждать у двери.", options: ["Нужно ждать у двери.", "Нужно войти в дверь.", "Нужно ждать на вокзале."] },
      { prompt: "Vlak odchádza o ôsmej.", answer: "Поезд отправляется в 8.", options: ["Поезд отправляется в 8.", "Поезд прибывает через 8 минут.", "Поезд стоит на платформе 8."] },
    ], hint: "Выберите только прямо услышанный факт.", explanation: "Понимание проверяется действием, временем или местом без дословной транскрипции." },
  ],
  knowledgeChecks: [
    { id: "m6-short-listening-check-1", question: "Что лучше определить при первом прослушивании?", options: ["Ситуацию и главное действие", "Каждую букву сообщения", "Все грамматические окончания"], answer: "Ситуацию и главное действие", explanation: "Детали удобнее проверить при повторе." },
    { id: "m6-short-listening-check-2", question: "Что означает Vlak odchádza o ôsmej?", options: ["Поезд отправляется в восемь", "Поезд прибывает через восемь минут", "Поезд опаздывает на восемь минут"], answer: "Поезд отправляется в восемь", explanation: "Odchádza — отправляется, o ôsmej — в восемь." },
    { id: "m6-short-listening-check-3", question: "Что сказать, если важная деталь неясна?", options: ["Prosím, zopakujte to.", "Nerozumiem nikdy.", "Preložte každé slovo."], answer: "Prosím, zopakujte to.", explanation: "Вежливая просьба позволяет услышать деталь ещё раз." },
  ],
  finalChecks: [
    { id: "m6-short-listening-final-1", question: "Передайте ключевую информацию: «Поезд отправляется в восемь».", options: ["Vlak odchádza o ôsmej.", "Vlak prichádza o osem minút.", "Vlak mešká ôsmej."], answer: "Vlak odchádza o ôsmej.", explanation: "Субъект — vlak, действие — odchádza, время — o ôsmej." },
  ],
  chatPrompt: "Попросите собеседника произнести одну короткую реплику о транспорте, встрече или часах работы; назовите ситуацию, действие и одну важную деталь.",
  chatSuggestions: ["Prosím, zopakujte to.", "Autobus príde o desať minút.", "Stretneme sa na stanici."],
} satisfies CourseLesson;
