import type { CourseLesson } from "../../../courseTypes";

const questionOptions = ["Kedy", "O koľkej", "Kde", "Môžeš", "Platí"];
const weekdayOptions = ["v pondelok", "v utorok", "v stredu", "vo štvrtok", "v piatok"];

export const meetingScheduleLesson = {
  vocabulary: [
    {"word":"Kedy sa stretneme?","translation":"Когда встретимся?","example":"Kedy sa stretneme?"},
    {"word":"V piatok o šiestej.","translation":"В пятницу в шесть.","example":"V piatok o šiestej."},
    {"word":"Stretneme sa pred kinom.","translation":"Встретимся перед кинотеатром.","example":"Stretneme sa pred kinom."},
    {"word":"Dobre, platí.","translation":"Хорошо, договорились.","example":"Dobre, platí."},
    {"word":"Stretneme sa zajtra o piatej.","translation":"Встретимся завтра в пять.","example":"Stretneme sa zajtra o piatej."},
    {"word":"Môžem až o siedmej.","translation":"Я могу только в семь.","example":"Môžem až o siedmej."},
  ],
  slug: "meeting-schedule",
  order: 10,
  title: "Встреча, дата и расписание",
  slovakTitle: "Stretnutie a rozvrh",
  description: "Договаривайтесь о дне, времени и месте встречи.",
  duration: "35–40 мин",
  goals: [
    "Предлагать встречу и спрашивать Kedy?",
    "Называть день недели и простую дату",
    "Уточнять время через O koľkej?",
    "Договариваться о месте встречи",
    "Предлагать альтернативу и подтверждать план",
  ],
  theory: {
    summary: "Чтобы договориться о встрече на уровне A1, последовательно уточните день или дату, время и место. Закончите разговор коротким подтверждением Dobre, platí или предложите один другой вариант.",
    rules: [
      "Начало договорённости: Kedy sa stretneme? — Когда встретимся? Можно предложить: Stretneme sa zajtra?",
      "Дни недели употребляются в готовых блоках: v pondelok, v utorok, v stredu, vo štvrtok, v piatok, v sobotu, v nedeľu.",
      "В письменной дате после числа ставится точка, месяц пишется со строчной буквы: 5. mája, 12. júna. Для A1 учите форму месяца вместе с датой.",
      "Время встречи уточняет O koľkej? Ответ строится с o: o piatej, o šiestej, o pol siedmej.",
      "Место уточняет Kde? Частотные модели: pred kinom, pri stanici, v kaviarni, na námestí. Учите их как готовые блоки.",
      "Если время не подходит: Vtedy nemôžem. Môžem o siedmej. Подтверждение полного плана: Dobre, platí. / Áno, dovidenia.",
    ],
    examples: [
      { slovak: "Kedy sa stretneme?", russian: "Когда встретимся?", explanation: "Kedy спрашивает о дне или дате." },
      { slovak: "V piatok o šiestej.", russian: "В пятницу в шесть.", explanation: "День и время образуют один короткий ответ." },
      { slovak: "Stretneme sa pred kinom.", russian: "Встретимся перед кинотеатром.", explanation: "Pred kinom — готовая модель места." },
      { slovak: "Dobre, platí.", russian: "Хорошо, договорились.", explanation: "Platí подтверждает согласованный план." },
      { slovak: "Stretneme sa zajtra o piatej.", russian: "Встретимся завтра в пять.", explanation: "Zajtra и o piatej называют день и время." },
      { slovak: "Môžem až o siedmej.", russian: "Я могу только в семь.", explanation: "Так предлагают более позднее время." },
    ],
  },
  sections: [
    {
      title: "Предложение и вопросы",
      paragraphs: ["Начните с предложения Stretneme sa...? или вопроса Kedy sa stretneme? Затем задайте только тот вопрос, для которого ещё нет ответа.", "Kedy спрашивает о дне или дате, O koľkej — о точном времени, Kde — о месте."],
      table: { headers: ["Задача", "Реплика", "Перевод"], rows: [
        ["предложить", "Stretneme sa zajtra?", "Встретимся завтра?"], ["день или дата", "Kedy sa stretneme?", "Когда встретимся?"],
        ["время", "O koľkej sa stretneme?", "Во сколько встретимся?"], ["место", "Kde sa stretneme?", "Где встретимся?"],
        ["возможность", "Môžeš v piatok?", "Ты можешь в пятницу?"],
      ] },
      items: ["Máš čas zajtra?", "Môžeme sa stretnúť?", "Kedy môžeš?"],
      note: "В вопросе sa stretneme частица sa обычно стоит после вопросительного слова: Kedy sa stretneme?",
    },
    {
      title: "День недели и дата",
      paragraphs: ["Назовите ближайший день словом dnes или zajtra либо используйте день недели.", "Цифровая дата пишется с точкой после порядкового числа, а название месяца — с маленькой буквы: 5. mája."],
      table: { headers: ["Когда", "Пример", "Перевод"], rows: [
        ["dnes", "Stretneme sa dnes.", "Встретимся сегодня."], ["zajtra", "Stretneme sa zajtra.", "Встретимся завтра."],
        ["v pondelok", "Môžem v pondelok.", "Я могу в понедельник."], ["vo štvrtok", "Nemôžem vo štvrtok.", "Я не могу в четверг."],
        ["5. mája", "Stretneme sa 5. mája.", "Встретимся 5 мая."], ["12. júna", "Kurz je 12. júna.", "Курс 12 июня."],
      ] },
      items: ["v utorok", "v stredu", "v piatok", "v sobotu", "v nedeľu"],
      note: "Особая форма с vo: vo štvrtok. Месяц в дате пишется со строчной буквы.",
    },
    {
      title: "Время и расписание",
      paragraphs: ["После дня уточните точное время вопросом O koľkej? Ответьте блоком o + форма часа.", "Если предложенное время не подходит, сначала откажитесь, затем сразу назовите доступное время."],
      table: { headers: ["Ситуация", "Реплика", "Перевод"], rows: [
        ["время", "O koľkej sa stretneme?", "Во сколько встретимся?"], ["точный ответ", "O šiestej.", "В шесть."],
        ["день и время", "V piatok o šiestej.", "В пятницу в шесть."], ["не подходит", "Vtedy nemôžem.", "Тогда я не могу."],
        ["альтернатива", "Môžem o siedmej.", "Я могу в семь."], ["расписание", "Kurz je od piatej do šiestej.", "Курс с пяти до шести."],
      ] },
      items: ["o piatej", "o pol šiestej", "od šiestej do siedmej"],
      note: "Не смешивайте Je šesť — сейчас шесть и o šiestej — в шесть.",
    },
    {
      title: "Место, альтернатива и подтверждение",
      paragraphs: ["Когда день и время известны, уточните Kde? Назовите короткую знакомую точку встречи.", "Подтверждайте только полный план. Если меняете время или место, дождитесь согласия собеседника."],
      table: { headers: ["Функция", "Реплика", "Перевод"], rows: [
        ["место", "Stretneme sa pred kinom.", "Встретимся перед кинотеатром."], ["другое место", "Môžeme pri stanici?", "Можем у вокзала?"],
        ["внутри", "Stretneme sa v kaviarni.", "Встретимся в кафе."], ["площадь", "Stretneme sa na námestí.", "Встретимся на площади."],
        ["подтверждение", "Dobre, platí.", "Хорошо, договорились."], ["завершение", "Teším sa. Dovidenia.", "Буду рад(а). До свидания."],
      ] },
      items: ["Áno, môžem.", "Nie, vtedy nemôžem.", "A čo v sobotu?"],
      note: "Для практического результата должны быть понятны день, время и место.",
    },
    {
      title: "Полная договорённость и частые ошибки",
      paragraphs: ["Соберите диалог в порядке: предложение → день или дата → время → место → подтверждение.", "Перед ответом проверьте положение sa, предлог дня, форму часа, точку в цифровой дате и словацкую диакритику."],
      table: { headers: ["Ошибка", "Правильно", "Почему"], rows: [
        ["Kedy stretneme sa?", "Kedy sa stretneme?", "Sa ставится после вопросительного слова."], ["v štvrtok", "vo štvrtok", "Нормативная форма — vo štvrtok."],
        ["5 mája", "5. mája", "После числа даты нужна точка."], ["o päť", "o piatej", "Для времени встречи нужна форма после o."],
        ["Stretneme sa pred kino.", "Stretneme sa pred kinom.", "Готовая модель места — pred kinom."],
      ] },
      items: ["Kedy sa stretneme?", "V piatok o šiestej.", "Stretneme sa pred kinom.", "Dobre, platí."],
      note: "Длительные переговоры и формальная деловая переписка не входят в A1.",
    },
  ],
  stepPractices: [
    { id: "m6-meeting-schedule-step-1", sectionIndex: 0, type: "pairs", prompt: "Выберите ключевое слово реплики.", answer: "Kedy; O koľkej; Kde; Môžeš; Platí", pairs: [
      { prompt: "___ sa stretneme? · когда", answer: "Kedy", options: questionOptions }, { prompt: "___ sa stretneme? · во сколько", answer: "O koľkej", options: questionOptions },
      { prompt: "___ sa stretneme? · где", answer: "Kde", options: questionOptions }, { prompt: "___ v piatok? · можешь", answer: "Môžeš", options: questionOptions }, { prompt: "Dobre, ___. · договорились", answer: "Platí", options: questionOptions },
    ], hint: "Определите, нужен день, время, место, возможность или подтверждение.", explanation: "Пять форм ведут договорённость от вопроса к подтверждению." },
    { id: "m6-meeting-schedule-step-2", sectionIndex: 1, type: "pairs", prompt: "Выберите день недели.", answer: "v pondelok; v utorok; v stredu; vo štvrtok; v piatok", pairs: [
      { prompt: "в понедельник", answer: "v pondelok", options: weekdayOptions }, { prompt: "во вторник", answer: "v utorok", options: weekdayOptions }, { prompt: "в среду", answer: "v stredu", options: weekdayOptions }, { prompt: "в четверг", answer: "vo štvrtok", options: weekdayOptions }, { prompt: "в пятницу", answer: "v piatok", options: weekdayOptions },
    ], hint: "Сопоставьте русский день с готовым словацким блоком.", explanation: "Обратите внимание на vo štvrtok." },
    { id: "m6-meeting-schedule-step-3", sectionIndex: 2, type: "pairs", prompt: "Выберите подходящую реплику времени.", answer: "O koľkej sa stretneme?; O šiestej.; Vtedy nemôžem.; Môžem o siedmej.; Od piatej do šiestej.", pairs: [
      { prompt: "Во сколько встретимся?", answer: "O koľkej sa stretneme?", options: ["O koľkej sa stretneme?", "O šiestej.", "Vtedy nemôžem.", "Môžem o siedmej.", "Od piatej do šiestej."] },
      { prompt: "В шесть.", answer: "O šiestej.", options: ["O koľkej sa stretneme?", "O šiestej.", "Vtedy nemôžem.", "Môžem o siedmej.", "Od piatej do šiestej."] },
      { prompt: "Тогда я не могу.", answer: "Vtedy nemôžem.", options: ["O koľkej sa stretneme?", "O šiestej.", "Vtedy nemôžem.", "Môžem o siedmej.", "Od piatej do šiestej."] },
      { prompt: "Я могу в семь.", answer: "Môžem o siedmej.", options: ["O koľkej sa stretneme?", "O šiestej.", "Vtedy nemôžem.", "Môžem o siedmej.", "Od piatej do šiestej."] },
      { prompt: "С пяти до шести.", answer: "Od piatej do šiestej.", options: ["O koľkej sa stretneme?", "O šiestej.", "Vtedy nemôžem.", "Môžem o siedmej.", "Od piatej do šiestej."] },
    ], hint: "Определите вопрос, ответ, отказ, альтернативу или интервал.", explanation: "O задаёт точку времени, od — do задаёт интервал." },
    { id: "m6-meeting-schedule-step-4", sectionIndex: 3, type: "pairs", prompt: "Выберите место или подтверждение.", answer: "pred kinom; pri stanici; v kaviarni; na námestí; Dobre, platí.", pairs: [
      { prompt: "перед кинотеатром", answer: "pred kinom", options: ["pred kinom", "pri stanici", "v kaviarni", "na námestí", "Dobre, platí."] }, { prompt: "у вокзала", answer: "pri stanici", options: ["pred kinom", "pri stanici", "v kaviarni", "na námestí", "Dobre, platí."] },
      { prompt: "в кафе", answer: "v kaviarni", options: ["pred kinom", "pri stanici", "v kaviarni", "na námestí", "Dobre, platí."] }, { prompt: "на площади", answer: "na námestí", options: ["pred kinom", "pri stanici", "v kaviarni", "na námestí", "Dobre, platí."] }, { prompt: "Хорошо, договорились.", answer: "Dobre, platí.", options: ["pred kinom", "pri stanici", "v kaviarni", "na námestí", "Dobre, platí."] },
    ], hint: "Четыре ответа — места, один — подтверждение.", explanation: "Готовые модели места завершаются подтверждением platí." },
    { id: "m6-meeting-schedule-step-5", sectionIndex: 4, type: "pairs", prompt: "Исправьте каждую реплику.", answer: "Kedy sa stretneme?; Vo štvrtok o šiestej.; Stretneme sa 5. mája.; Stretneme sa pred kinom.; Stretneme sa zajtra o piatej.", pairs: [
      { prompt: "Kedy stretneme sa?", answer: "Kedy sa stretneme?", inputHint: "Введите исправленную фразу" }, { prompt: "V štvrtok o šesť.", answer: "Vo štvrtok o šiestej.", inputHint: "Введите исправленную фразу" },
      { prompt: "Stretneme sa 5 mája.", answer: "Stretneme sa 5. mája.", inputHint: "Введите исправленную фразу" }, { prompt: "Stretneme sa pred kino.", answer: "Stretneme sa pred kinom.", inputHint: "Введите исправленную фразу" },
      { prompt: "Переведите: «Встретимся завтра в пять».", answer: "Stretneme sa zajtra o piatej.", inputHint: "Введите перевод" },
    ], hint: "Проверьте sa, день, час, дату и место.", explanation: "Нормативны Kedy sa stretneme, vo štvrtok, 5. mája, pred kinom и o piatej." },
  ],
  assessmentMode: "interactive",
  materialAssessmentStep: false,
  reinforcementLabel: "Финальный тест темы",
  reinforcementTitle: "Выполните шесть заданий темы 10",
  reinforcementPractices: [
    { id: "reinforcement:meeting-schedule:1", sectionIndex: 0, type: "pairs", prompt: "Выберите функцию для каждой реплики.", answer: "Kedy; O koľkej; Kde; Môžeš; Platí", pairs: [
      { prompt: "___ sa stretneme? · день", answer: "Kedy", options: questionOptions }, { prompt: "___ sa stretneme? · время", answer: "O koľkej", options: questionOptions }, { prompt: "___ sa stretneme? · место", answer: "Kde", options: questionOptions }, { prompt: "___ zajtra? · возможность", answer: "Môžeš", options: questionOptions }, { prompt: "Dobre, ___. · подтверждение", answer: "Platí", options: questionOptions },
    ], hint: "Выберите один из пяти элементов договорённости.", explanation: "Вопросы уточняют план, platí подтверждает его." },
    { id: "reinforcement:meeting-schedule:2", sectionIndex: 1, type: "pairs", prompt: "Выберите нормативный блок дня.", answer: "v pondelok; v utorok; v stredu; vo štvrtok; v piatok", pairs: [
      { prompt: "понедельник", answer: "v pondelok", options: weekdayOptions }, { prompt: "вторник", answer: "v utorok", options: weekdayOptions }, { prompt: "среда", answer: "v stredu", options: weekdayOptions }, { prompt: "четверг", answer: "vo štvrtok", options: weekdayOptions }, { prompt: "пятница", answer: "v piatok", options: weekdayOptions },
    ], hint: "Обратите внимание на предлог и форму дня.", explanation: "Для четверга употребляется vo štvrtok." },
    { id: "reinforcement:meeting-schedule:3", sectionIndex: 1, type: "pairs", prompt: "Выберите правильную письменную дату.", answer: "5. mája; 12. júna; 20. septembra; 3. októbra; 24. decembra", pairs: [
      { prompt: "5 мая", answer: "5. mája", options: ["5. mája", "12. júna", "20. septembra", "3. októbra", "24. decembra"] }, { prompt: "12 июня", answer: "12. júna", options: ["5. mája", "12. júna", "20. septembra", "3. októbra", "24. decembra"] },
      { prompt: "20 сентября", answer: "20. septembra", options: ["5. mája", "12. júna", "20. septembra", "3. októbra", "24. decembra"] }, { prompt: "3 октября", answer: "3. októbra", options: ["5. mája", "12. júna", "20. septembra", "3. októbra", "24. decembra"] }, { prompt: "24 декабря", answer: "24. decembra", options: ["5. mája", "12. júna", "20. septembra", "3. októbra", "24. decembra"] },
    ], showSlovakKeyboard: false, hint: "Ищите точку после числа и форму месяца со строчной буквы.", explanation: "Письменная дата использует порядковое число с точкой и форму месяца." },
    { id: "reinforcement:meeting-schedule:4", sectionIndex: 4, type: "pairs", prompt: "Исправьте ошибки в договорённости.", answer: "Kedy sa stretneme?; Vo štvrtok o šiestej.; Stretneme sa 5. mája.; Stretneme sa pred kinom.; Dobre, platí.", pairs: [
      { prompt: "Kedy stretneme sa?", answer: "Kedy sa stretneme?", inputHint: "Введите исправленную фразу" }, { prompt: "V štvrtok o šesť.", answer: "Vo štvrtok o šiestej.", inputHint: "Введите исправленную фразу" },
      { prompt: "Stretneme sa 5 mája.", answer: "Stretneme sa 5. mája.", inputHint: "Введите исправленную фразу" }, { prompt: "Stretneme sa pred kino.", answer: "Stretneme sa pred kinom.", inputHint: "Введите исправленную фразу" }, { prompt: "Dobre plati.", answer: "Dobre, platí.", inputHint: "Введите исправленную фразу" },
    ], hint: "Исправьте всю строку: порядок, предлог, дату, форму места и диакритику.", explanation: "Каждая строка проверяет отдельный элемент полного плана." },
    { id: "reinforcement:meeting-schedule:5", sectionIndex: 4, type: "pairs", prompt: "Переведите на словацкий.", answer: "Kedy sa stretneme?; V piatok o šiestej.; Stretneme sa pred kinom.; Vtedy nemôžem.; Stretneme sa zajtra o piatej.", pairs: [
      { prompt: "Когда встретимся?", answer: "Kedy sa stretneme?", inputHint: "Введите перевод" }, { prompt: "В пятницу в шесть.", answer: "V piatok o šiestej.", inputHint: "Введите перевод" },
      { prompt: "Встретимся перед кинотеатром.", answer: "Stretneme sa pred kinom.", acceptableAnswers: ["Pred kinom sa stretneme."], inputHint: "Введите перевод" },
      { prompt: "Тогда я не могу.", answer: "Vtedy nemôžem.", inputHint: "Введите перевод" }, { prompt: "Встретимся завтра в пять.", answer: "Stretneme sa zajtra o piatej.", acceptableAnswers: ["Zajtra o piatej sa stretneme."], inputHint: "Введите перевод" },
    ], hint: "Используйте модели урока и сохраните словацкую диакритику.", explanation: "Переводы проверяют вопрос, день, время, место, отказ и полный план." },
    { id: "reinforcement:meeting-schedule:6", sectionIndex: 4, type: "pairs", prompt: "Соберите диалог о встрече.", answer: "Kedy sa stretneme?; V piatok o šiestej.; Vtedy nemôžem. Môžem o siedmej.; Dobre. Kde sa stretneme?; Pred kinom.; Dobre, platí.", pairs: [
      { prompt: "1 · вопрос", answer: "Kedy sa stretneme?", options: ["Kedy sa stretneme?", "Kde je stretnúť?", "Kedy stretneme sa?"] }, { prompt: "2 · предложение", answer: "V piatok o šiestej.", options: ["V piatok o šiestej.", "Piatok na šesť.", "V piatok o šesť."] },
      { prompt: "3 · альтернатива", answer: "Vtedy nemôžem. Môžem o siedmej.", options: ["Vtedy nemôžem. Môžem o siedmej.", "Vtedy môžem nie. O sedem.", "Nemôžem nikdy siedmej."] },
      { prompt: "4 · место", answer: "Dobre. Kde sa stretneme?", options: ["Dobre. Kde sa stretneme?", "Dobre. Kedy je miesto?", "Dobre. Kde stretneme sa?"] }, { prompt: "5 · ответ", answer: "Pred kinom.", options: ["Pred kino.", "Pred kinom.", "V kino."] }, { prompt: "6 · подтверждение", answer: "Dobre, platí.", options: ["Dobre, platí.", "Dobre, plati.", "Dobrý, platím."] },
    ], hint: "Следуйте маршруту: день, время, альтернатива, место, подтверждение.", explanation: "Диалог заканчивается только после согласования всех практических деталей." },
  ],
  knowledgeChecks: [
    { id: "m6-meeting-schedule-check-1", question: "Как спросить «Когда встретимся»?", options: ["Kedy sa stretneme?", "Kde sa stretneme?", "O koľkej sa stretneme?"], answer: "Kedy sa stretneme?", explanation: "Kedy спрашивает о дне или дате." },
    { id: "m6-meeting-schedule-check-2", question: "Как ответить «В пятницу в шесть»?", options: ["V piatok o šiestej.", "Vo piatok na šesť.", "V piatok o šesť."], answer: "V piatok o šiestej.", explanation: "Нужны блоки v piatok и o šiestej." },
    { id: "m6-meeting-schedule-check-3", question: "Какая граница соответствует уровню A1?", options: ["Длительные переговоры и формальная деловая переписка не входят в A1.", "Нужно вести сложные деловые переговоры.", "Нужно согласовать расписание большой группы."], answer: "Длительные переговоры и формальная деловая переписка не входят в A1.", explanation: "На A1 достаточно дня, времени, места и короткого подтверждения." },
  ],
  finalChecks: [
    { id: "m6-meeting-schedule-final-1", question: "Переведите: «Встретимся завтра в пять».", options: ["Stretneme sa zajtra o piatej.", "Stretneme zajtra o päť.", "Zajtra sa stretnúť na piatej."], answer: "Stretneme sa zajtra o piatej.", explanation: "Используйте stretneme sa, zajtra и o piatej." },
  ],
  chatPrompt: "Согласуйте день, время и место встречи, предложив один альтернативный вариант.",
  chatSuggestions: ["Kedy sa stretneme?", "V piatok o šiestej.", "Stretneme sa pred kinom."],
} satisfies CourseLesson;
