import type { CourseLesson } from "../../../courseTypes";

const messagePartOptions = ["Ahoj, Nina!", "Dnes nemôžem prísť.", "Som chorá.", "Stretneme sa v piatok?", "Maj sa!"];
const detailOptions = ["dnes", "zajtra", "o piatej", "pred kinom", "desať minút"];
const requestOptions = ["napíš", "zavolaj", "počkajte", "odpíš", "daj"];

export const personalMessageLesson = {
  vocabulary: [
    {"word":"Ahoj, Nina!","translation":"Привет, Нина!","example":"Ahoj, Nina!"},
    {"word":"Dnes nemôžem prísť.","translation":"Сегодня я не могу прийти.","example":"Dnes nemôžem prísť."},
    {"word":"Prepáč, meškám desať minút.","translation":"Извини, я опаздываю на десять минут.","example":"Prepáč, meškám desať minút."},
    {"word":"Stretneme sa zajtra o piatej pred kinom?","translation":"Встретимся завтра в пять перед кинотеатром?","example":"Stretneme sa zajtra o piatej pred kinom?"},
    {"word":"Prosím, napíš mi.","translation":"Пожалуйста, напиши мне.","example":"Prosím, napíš mi."},
    {"word":"Ďakujem a maj sa!","translation":"Спасибо, пока!","example":"Ďakujem a maj sa!"},
  ],
  slug: "personal-message",
  order: 16,
  title: "Короткое личное сообщение",
  slovakTitle: "Krátka osobná správa",
  description: "Пишите короткое понятное сообщение с фактом, просьбой или приглашением.",
  duration: "35–40 мин",
  goals: [
    "Начинать и завершать неформальное личное сообщение",
    "Сообщать один ключевой факт и простую причину",
    "Предлагать встречу с точным временем и местом",
    "Писать короткую просьбу и понятный ответ",
    "Собирать сообщение из четырёх-пяти логичных строк",
  ],
  theory: {
    summary: "Короткое личное сообщение A1 должно быстро отвечать на четыре вопроса: кому вы пишете, что произошло, что должен знать или сделать адресат и как ответить. Используйте короткие знакомые фразы и добавляйте время или место, когда от них зависит действие.",
    rules: [
      "Неформальное начало: Ahoj, Nina! или Milá Anna! Завершение: Maj sa! / Ďakujem! Затем можно написать своё имя.",
      "Главный факт ставьте сразу после приветствия: Dnes nemôžem prísť. Meškám desať minút. Som chorý/chorá.",
      "Предложение встречи должно содержать нужные детали: Stretneme sa zajtra o piatej pred kinom?",
      "Короткая просьба знакомому использует форму на ty: Prosím, napíš mi. Zavolaj mi večer. Počkajte — форма на vy, её не смешивают с неформальным Ahoj.",
      "Одно сообщение — одна ясная цель. Формальное письмо, длинное объяснение и сложная аргументация не входят в эту тему A1.",
    ],
    examples: [
      { slovak: "Ahoj, Nina!", russian: "Привет, Нина!", explanation: "Неформальное обращение к знакомому человеку." },
      { slovak: "Dnes nemôžem prísť.", russian: "Сегодня я не могу прийти.", explanation: "Ключевой факт сообщается сразу." },
      { slovak: "Prepáč, meškám desať minút.", russian: "Извини, я опаздываю на десять минут.", explanation: "Извинение сопровождается точной практической деталью." },
      { slovak: "Stretneme sa zajtra o piatej pred kinom?", russian: "Встретимся завтра в пять перед кинотеатром?", explanation: "В вопросе есть день, время и место." },
      { slovak: "Prosím, napíš mi.", russian: "Пожалуйста, напиши мне.", explanation: "Короткая просьба показывает ожидаемое действие." },
      { slovak: "Ďakujem a maj sa!", russian: "Спасибо, пока!", explanation: "Дружелюбное завершение личного сообщения." },
    ],
  },
  sections: [
    {
      title: "Приветствие, обращение и завершение",
      paragraphs: ["Личное сообщение знакомому начните с Ahoj и имени. После обращения поставьте запятую, а завершить можно фразой Maj sa!", "Milý используется перед мужским именем, Milá — перед женским: Milý Peter! Milá Anna!"],
      table: { headers: ["Функция", "Фраза", "Перевод"], rows: [
        ["приветствие", "Ahoj, Nina!", "Привет, Нина!"], ["обращение к мужчине", "Milý Peter!", "Дорогой Петер!"],
        ["обращение к женщине", "Milá Anna!", "Дорогая Анна!"], ["завершение", "Maj sa!", "Пока! / Всего хорошего!"],
        ["благодарность", "Ďakujem!", "Спасибо!"],
      ] },
      items: ["Ahoj! — Привет!", "Vidíme sa zajtra. — Увидимся завтра.", "Anna — подпись отправителя"],
      note: "В коротком чате подпись часто не нужна, но в учебном сообщении она помогает увидеть структуру.",
    },
    {
      title: "Главный факт и простая причина",
      paragraphs: ["После приветствия сразу сообщите главное: вы не придёте, опаздываете или плохо себя чувствуете.", "Причину можно добавить через pretože: Nemôžem prísť, pretože som chorá. Выберите chorý для мужчины и chorá для женщины."],
      table: { headers: ["Ситуация", "Сообщение", "Перевод"], rows: [
        ["отмена", "Dnes nemôžem prísť.", "Сегодня я не могу прийти."], ["опоздание", "Meškám desať minút.", "Я опаздываю на десять минут."],
        ["мужчина", "Som chorý.", "Я болен."], ["женщина", "Som chorá.", "Я больна."],
        ["причина", "Nemôžem prísť, pretože pracujem.", "Я не могу прийти, потому что работаю."],
      ] },
      items: ["Prepáč. — Извини.", "Dnes pracujem dlho. — Сегодня я долго работаю.", "Je mi zle. — Мне плохо."],
      note: "Не перегружайте сообщение: одного факта и одной короткой причины достаточно.",
    },
    {
      title: "Предложение встречи: когда и где",
      paragraphs: ["Если встреча отменяется, предложите новый вариант. Адресату нужны день, время и при необходимости место.", "Вопрос Stretneme sa...? подходит для совместного решения; Môžeme sa stretnúť...? мягко спрашивает о возможности."],
      table: { headers: ["Деталь", "Пример", "Перевод"], rows: [
        ["день", "Stretneme sa zajtra?", "Встретимся завтра?"], ["время", "Stretneme sa o piatej?", "Встретимся в пять?"],
        ["место", "Stretneme sa pred kinom?", "Встретимся перед кинотеатром?"], ["полный вариант", "Stretneme sa zajtra o piatej pred kinom?", "Встретимся завтра в пять перед кинотеатром?"],
        ["альтернатива", "Môžeme sa stretnúť v piatok?", "Мы можем встретиться в пятницу?"],
      ] },
      items: ["Chceš ísť zajtra do kina? — Хочешь завтра пойти в кино?", "Áno, môžem. — Да, могу.", "Prepáč, nemôžem. — Извини, не могу."],
      note: "Проверяйте, достаточно ли деталей, чтобы адресат понял, когда и куда прийти.",
    },
    {
      title: "Просьба и короткий ответ",
      paragraphs: ["В конце основного текста скажите, какого ответа или действия вы ждёте: napíš mi, odpíš mi, zavolaj mi.", "С неформальным Ahoj используйте формы ty. Вежливая форма vy нужна в другом регистре: Napíšte mi, prosím."],
      table: { headers: ["Цель", "Неформально", "Перевод"], rows: [
        ["написать", "Prosím, napíš mi.", "Пожалуйста, напиши мне."], ["ответить", "Prosím, odpíš mi.", "Пожалуйста, ответь мне."],
        ["позвонить", "Zavolaj mi večer.", "Позвони мне вечером."], ["подождать", "Prosím, počkaj na mňa.", "Пожалуйста, подожди меня."],
        ["дать знать", "Daj mi vedieť.", "Дай мне знать."],
      ] },
      items: ["Dobre. — Хорошо.", "Platí. — Договорились.", "Áno, prídem. — Да, я приду."],
      note: "Просьба должна быть конкретной: написать, позвонить, подождать или подтвердить.",
    },
    {
      title: "Цельное сообщение и частые ошибки",
      paragraphs: ["Соберите сообщение в порядке: обращение → главный факт → причина или новая договорённость → просьба → завершение и имя.", "Перед отправкой проверьте адресата, цель, день, время, место, форму ty/vy и словацкую диакритику."],
      table: { headers: ["Ошибка", "Правильно", "Почему"], rows: [
        ["Ahoj Nina!", "Ahoj, Nina!", "После Ahoj перед именем нужна запятая."], ["Dnes nemozem prist.", "Dnes nemôžem prísť.", "Нужна словацкая диакритика."],
        ["Ahoj! Napíšte mi.", "Ahoj! Napíš mi.", "Ahoj и форма ty должны соответствовать друг другу."], ["Stretneme zajtra?", "Stretneme sa zajtra?", "Глаголу stretnúť sa нужна частица sa."],
        ["Stretneme sa o piatej.", "Stretneme sa o piatej?", "Предложение-вопрос отмечается вопросительным знаком."],
      ] },
      items: ["Ahoj, Nina!", "Dnes nemôžem prísť, pretože som chorá.", "Môžeme sa stretnúť v piatok o piatej?", "Prosím, napíš mi.", "Maj sa! Anna"],
      note: "Свободное личное сообщение может иметь разные правильные формулировки; проверяйте прежде всего ясность и необходимые детали.",
    },
  ],
  stepPractices: [
    { id: "m6-personal-message-step-1", sectionIndex: 0, type: "pairs", prompt: "Выберите подходящую часть личного сообщения.", answer: "Ahoj, Nina!; Milý Peter!; Milá Anna!; Maj sa!; Ďakujem!", pairs: [
      { prompt: "приветствие Нине", answer: "Ahoj, Nina!", options: ["Ahoj, Nina!", "Milý Peter!", "Milá Anna!", "Maj sa!", "Ďakujem!"] },
      { prompt: "обращение к Петеру", answer: "Milý Peter!", options: ["Ahoj, Nina!", "Milý Peter!", "Milá Anna!", "Maj sa!", "Ďakujem!"] },
      { prompt: "обращение к Анне", answer: "Milá Anna!", options: ["Ahoj, Nina!", "Milý Peter!", "Milá Anna!", "Maj sa!", "Ďakujem!"] },
      { prompt: "прощание", answer: "Maj sa!", options: ["Ahoj, Nina!", "Milý Peter!", "Milá Anna!", "Maj sa!", "Ďakujem!"] },
      { prompt: "благодарность", answer: "Ďakujem!", options: ["Ahoj, Nina!", "Milý Peter!", "Milá Anna!", "Maj sa!", "Ďakujem!"] },
    ], hint: "Определите функцию строки и пол адресата там, где это важно.", explanation: "Приветствие и завершение задают дружеский регистр сообщения." },
    { id: "m6-personal-message-step-2", sectionIndex: 1, type: "pairs", prompt: "Выберите фразу для ситуации.", answer: "Dnes nemôžem prísť.; Meškám desať minút.; Som chorý.; Som chorá.; Prepáč.", pairs: [
      { prompt: "сегодня не могу прийти", answer: "Dnes nemôžem prísť.", options: ["Dnes nemôžem prísť.", "Meškám desať minút.", "Som chorý.", "Som chorá.", "Prepáč."] },
      { prompt: "опаздываю на десять минут", answer: "Meškám desať minút.", options: ["Dnes nemôžem prísť.", "Meškám desať minút.", "Som chorý.", "Som chorá.", "Prepáč."] },
      { prompt: "я болен · мужчина", answer: "Som chorý.", options: ["Dnes nemôžem prísť.", "Meškám desať minút.", "Som chorý.", "Som chorá.", "Prepáč."] },
      { prompt: "я больна · женщина", answer: "Som chorá.", options: ["Dnes nemôžem prísť.", "Meškám desať minút.", "Som chorý.", "Som chorá.", "Prepáč."] },
      { prompt: "извини", answer: "Prepáč.", options: ["Dnes nemôžem prísť.", "Meškám desať minút.", "Som chorý.", "Som chorá.", "Prepáč."] },
    ], hint: "Выберите точный факт или короткое извинение.", explanation: "Главная информация должна быть понятна без длинного объяснения." },
    { id: "m6-personal-message-step-3", sectionIndex: 2, type: "pairs", prompt: "Выберите недостающую деталь встречи.", answer: "dnes; zajtra; o piatej; pred kinom; desať minút", pairs: [
      { prompt: "___ nemôžem prísť. · сегодня", answer: "dnes", options: detailOptions }, { prompt: "Stretneme sa ___. · завтра", answer: "zajtra", options: detailOptions },
      { prompt: "Stretneme sa ___. · в пять", answer: "o piatej", options: detailOptions }, { prompt: "Stretneme sa ___. · перед кинотеатром", answer: "pred kinom", options: detailOptions },
      { prompt: "Meškám ___. · на десять минут", answer: "desať minút", options: detailOptions },
    ], hint: "Различайте день, время, место и длительность опоздания.", explanation: "Практические детали позволяют адресату правильно действовать." },
    { id: "m6-personal-message-step-4", sectionIndex: 3, type: "pairs", prompt: "Выберите глагол просьбы.", answer: "napíš; zavolaj; počkajte; odpíš; daj", pairs: [
      { prompt: "Prosím, ___ mi. · напиши", answer: "napíš", options: requestOptions }, { prompt: "___ mi večer. · позвони", answer: "zavolaj", options: requestOptions },
      { prompt: "Prosím, ___. · подождите · vy", answer: "počkajte", options: requestOptions }, { prompt: "Prosím, ___ mi. · ответь", answer: "odpíš", options: requestOptions },
      { prompt: "___ mi vedieť. · дай", answer: "daj", options: requestOptions },
    ], hint: "Учитывайте действие и отмеченную форму ty или vy.", explanation: "Каждая просьба сообщает одно ожидаемое действие." },
    { id: "m6-personal-message-step-5", sectionIndex: 4, type: "pairs", prompt: "Исправьте ошибки в сообщениях.", answer: "Ahoj, Nina!; Dnes nemôžem prísť.; Ahoj! Napíš mi.; Stretneme sa zajtra?; Stretneme sa o piatej?", pairs: [
      { prompt: "Ahoj Nina!", answer: "Ahoj, Nina!", inputHint: "Введите исправленную строку" }, { prompt: "Dnes nemozem prist.", answer: "Dnes nemôžem prísť.", inputHint: "Введите исправленную строку" },
      { prompt: "Ahoj! Napíšte mi.", answer: "Ahoj! Napíš mi.", inputHint: "Введите исправленную строку" }, { prompt: "Stretneme zajtra?", answer: "Stretneme sa zajtra?", inputHint: "Введите исправленную строку" },
      { prompt: "Stretneme sa o piatej.", answer: "Stretneme sa o piatej?", inputHint: "Введите исправленную строку" },
    ], hint: "Проверьте запятую, диакритику, ty/vy, sa и вопросительный знак.", explanation: "Исправления делают сообщение нормативным и однозначным." },
  ],
  assessmentMode: "interactive",
  materialAssessmentStep: false,
  reinforcementLabel: "Финальный тест темы",
  reinforcementTitle: "Выполните шесть заданий темы 16",
  reinforcementPractices: [
    { id: "reinforcement:personal-message:1", sectionIndex: 0, type: "pairs", prompt: "Выберите часть сообщения по её функции.", answer: "Ahoj, Nina!; Milý Peter!; Milá Anna!; Maj sa!; Ďakujem!", pairs: [
      { prompt: "приветствие Нине", answer: "Ahoj, Nina!", options: ["Ahoj, Nina!", "Milý Peter!", "Milá Anna!", "Maj sa!", "Ďakujem!"] },
      { prompt: "обращение к Петеру", answer: "Milý Peter!", options: ["Ahoj, Nina!", "Milý Peter!", "Milá Anna!", "Maj sa!", "Ďakujem!"] },
      { prompt: "обращение к Анне", answer: "Milá Anna!", options: ["Ahoj, Nina!", "Milý Peter!", "Milá Anna!", "Maj sa!", "Ďakujem!"] },
      { prompt: "прощание", answer: "Maj sa!", options: ["Ahoj, Nina!", "Milý Peter!", "Milá Anna!", "Maj sa!", "Ďakujem!"] },
      { prompt: "благодарность", answer: "Ďakujem!", options: ["Ahoj, Nina!", "Milý Peter!", "Milá Anna!", "Maj sa!", "Ďakujem!"] },
    ], hint: "Сначала определите функцию строки.", explanation: "Формулы начала и завершения соответствуют личному сообщению." },
    { id: "reinforcement:personal-message:2", sectionIndex: 2, type: "pairs", prompt: "Добавьте нужную практическую деталь.", answer: "dnes; zajtra; o piatej; pred kinom; desať minút", pairs: [
      { prompt: "___ nemôžem prísť.", answer: "dnes", options: detailOptions }, { prompt: "Stretneme sa ___. · завтра", answer: "zajtra", options: detailOptions },
      { prompt: "Stretneme sa ___. · в пять", answer: "o piatej", options: detailOptions }, { prompt: "Stretneme sa ___. · перед кинотеатром", answer: "pred kinom", options: detailOptions },
      { prompt: "Meškám ___.", answer: "desať minút", options: detailOptions },
    ], hint: "Каждый вариант используется один раз.", explanation: "День, время, место и длительность отвечают на разные практические вопросы." },
    { id: "reinforcement:personal-message:3", sectionIndex: 4, type: "pairs", prompt: "Соберите сообщение об отмене встречи по строкам.", answer: "Ahoj, Nina!; Dnes nemôžem prísť.; Som chorá.; Stretneme sa v piatok?; Maj sa!", pairs: [
      { prompt: "1 · обращение", answer: "Ahoj, Nina!", options: messagePartOptions }, { prompt: "2 · главный факт", answer: "Dnes nemôžem prísť.", options: messagePartOptions },
      { prompt: "3 · причина", answer: "Som chorá.", options: messagePartOptions }, { prompt: "4 · новый вариант", answer: "Stretneme sa v piatok?", options: messagePartOptions },
      { prompt: "5 · завершение", answer: "Maj sa!", options: messagePartOptions },
    ], hint: "Следуйте порядку от обращения к завершению.", explanation: "Пять строк образуют ясное короткое сообщение с новой договорённостью." },
    { id: "reinforcement:personal-message:4", sectionIndex: 4, type: "pairs", prompt: "Исправьте ошибки в личных сообщениях.", answer: "Ahoj, Nina!; Dnes nemôžem prísť.; Ahoj! Napíš mi.; Stretneme sa zajtra?; Stretneme sa o piatej?", pairs: [
      { prompt: "Ahoj Nina!", answer: "Ahoj, Nina!", inputHint: "Введите исправленную строку" }, { prompt: "Dnes nemozem prist.", answer: "Dnes nemôžem prísť.", inputHint: "Введите исправленную строку" },
      { prompt: "Ahoj! Napíšte mi.", answer: "Ahoj! Napíš mi.", inputHint: "Введите исправленную строку" }, { prompt: "Stretneme zajtra?", answer: "Stretneme sa zajtra?", inputHint: "Введите исправленную строку" },
      { prompt: "Stretneme sa o piatej.", answer: "Stretneme sa o piatej?", inputHint: "Введите исправленную строку" },
    ], hint: "Исправьте всю строку.", explanation: "Проверяются пунктуация, диакритика, регистр общения и модель stretneme sa." },
    { id: "reinforcement:personal-message:5", sectionIndex: 4, type: "pairs", prompt: "Переведите на словацкий.", answer: "Ahoj, Nina!; Dnes nemôžem prísť.; Prepáč, meškám desať minút.; Stretneme sa zajtra o piatej pred kinom?; Ďakujem a maj sa!", pairs: [
      { prompt: "Привет, Нина!", answer: "Ahoj, Nina!", inputHint: "Введите перевод" },
      { prompt: "Сегодня я не могу прийти.", answer: "Dnes nemôžem prísť.", inputHint: "Введите перевод" },
      { prompt: "Извини, я опаздываю на десять минут.", answer: "Prepáč, meškám desať minút.", inputHint: "Введите перевод" },
      { prompt: "Встретимся завтра в пять перед кинотеатром?", answer: "Stretneme sa zajtra o piatej pred kinom?", acceptableAnswers: ["Zajtra o piatej sa stretneme pred kinom?"], inputHint: "Введите перевод" },
      { prompt: "Спасибо, пока!", answer: "Ďakujem a maj sa!", inputHint: "Введите перевод" },
    ], hint: "Используйте готовые фразы и сохраняйте словацкую диакритику.", explanation: "Переводы проверяют начало, факт, опоздание, договорённость и завершение." },
    { id: "reinforcement:personal-message:6", sectionIndex: 4, type: "pairs", prompt: "Выберите цельное сообщение для каждой ситуации.", answer: "Ahoj! Dnes nemôžem prísť. Prosím, napíš mi.; Prepáč, meškám desať minút. Počkaj na mňa.; Ahoj! Chceš ísť zajtra do kina?; Áno, môžem. Stretneme sa o piatej.; Ďakujem za správu. Maj sa!", pairs: [
      { prompt: "отменить и попросить ответ", answer: "Ahoj! Dnes nemôžem prísť. Prosím, napíš mi.", options: ["Ahoj! Dnes nemôžem prísť. Prosím, napíš mi.", "Ahoj! Kde je prísť?", "Maj sa! Dnes stretnutie."] },
      { prompt: "сообщить об опоздании", answer: "Prepáč, meškám desať minút. Počkaj na mňa.", options: ["Prepáč, meškám desať minút. Počkaj na mňa.", "Mešká desať. Počkajte ja.", "Ahoj, meškanie miesto."] },
      { prompt: "пригласить в кино", answer: "Ahoj! Chceš ísť zajtra do kina?", options: ["Ahoj! Chceš ísť zajtra do kina?", "Ahoj! Chcete kino ja?", "Zajtra kino je chceš."] },
      { prompt: "согласиться и назвать время", answer: "Áno, môžem. Stretneme sa o piatej.", options: ["Áno, môžem. Stretneme sa o piatej.", "Áno, môže. Stretneme piata.", "Môžem áno kde piatej."] },
      { prompt: "поблагодарить и попрощаться", answer: "Ďakujem za správu. Maj sa!", options: ["Ďakujem za správu. Maj sa!", "Ďakujem správa. Mám sa!", "Správa maj ďakovať."] },
    ], hint: "Выберите вариант, который полностью решает указанную задачу.", explanation: "У каждого короткого сообщения одна ясная коммуникативная цель." },
  ],
  knowledgeChecks: [
    { id: "m6-personal-message-check-1", question: "Как начать неформальное сообщение Нине?", options: ["Ahoj, Nina!", "Vážená pani Nina!", "Dobrý deň, úrad!"], answer: "Ahoj, Nina!", explanation: "Ahoj подходит для личного сообщения знакомому человеку." },
    { id: "m6-personal-message-check-2", question: "Как сообщить об опоздании на десять минут?", options: ["Meškám desať minút.", "Meškám o desiatej.", "Som desať minút."], answer: "Meškám desať minút.", explanation: "После meškám указывается длительность опоздания." },
    { id: "m6-personal-message-check-3", question: "Какая структура подходит короткому сообщению A1?", options: ["Обращение → факт → нужная деталь или просьба → завершение", "Длинное вступление → сложная аргументация", "Только приветствие без цели"], answer: "Обращение → факт → нужная деталь или просьба → завершение", explanation: "Короткая структура помогает адресату сразу понять цель." },
  ],
  finalChecks: [
    { id: "m6-personal-message-final-1", question: "Напишите: «Привет, Анна! Встретимся завтра?»", options: ["Ahoj, Anna! Stretneme sa zajtra?", "Ahoj Anna. Stretneme zajtra.", "Dobrý deň Anna, zajtra sa?"], answer: "Ahoj, Anna! Stretneme sa zajtra?", explanation: "Используйте неформальное Ahoj, частицу sa и вопросительный знак." },
  ],
  chatPrompt: "Напишите короткое сообщение знакомому: сообщите, что не можете прийти, предложите новое время и попросите ответить.",
  chatSuggestions: ["Ahoj, Nina!", "Dnes nemôžem prísť.", "Môžeme sa stretnúť v piatok?"],
} satisfies CourseLesson;
