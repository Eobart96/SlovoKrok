import type { CourseLesson } from "../../../courseTypes";

export const homeLesson = {
  vocabulary: [
    {"word":"Bývam v malom byte.","translation":"Я живу в маленькой квартире.","example":"Bývam v malom byte."},
    {"word":"V kuchyni je veľký stôl.","translation":"На кухне большой стол.","example":"V kuchyni je veľký stôl."},
    {"word":"Knihy sú na poličke.","translation":"Книги на полке.","example":"Knihy sú na poličke."},
    {"word":"Večer upratujem izbu.","translation":"Вечером я убираю комнату.","example":"Večer upratujem izbu."},
    {"word":"Posteľ je vedľa okna.","translation":"Кровать находится рядом с окном.","example":"Posteľ je vedľa okna."},
    {"word":"Doma varím a umývam riad.","translation":"Дома я готовлю и мою посуду.","example":"Doma varím a umývam riad."},
    {"word":"byt","translation":"квартира","example":"byt"},
    {"word":"dom","translation":"дом","example":"dom"},
    {"word":"izba","translation":"комната","example":"izba"},
    {"word":"kuchyňa","translation":"кухня","example":"kuchyňa"},
    {"word":"kúpeľňa","translation":"ванная","example":"kúpeľňa"},
    {"word":"obývačka","translation":"гостиная","example":"obývačka"},
    {"word":"spálňa","translation":"спальня","example":"spálňa"},
    {"word":"chodba / balkón","translation":"коридор / балкон","example":"chodba / balkón"},
  ],
  slug: "home",
  order: 2,
  title: "Дом и быт",
  slovakTitle: "Domov a domácnosť",
  description: "Описывайте жильё, комнаты, расположение предметов и обычные домашние дела.",
  duration: "35–40 мин",
  goals: [
    "Называть тип жилья, основные комнаты и предметы быта",
    "Сообщать, что находится в комнате, с помощью je и sú",
    "Использовать готовые модели места с v, na, pri и vedľa",
    "Говорить о простых домашних делах в настоящем времени",
    "Составлять короткое связное описание жилья",
  ],
  theory: {
    summary: "Описание дома строится от общего к частному: где вы живёте, какие комнаты есть, что в них находится и что вы там обычно делаете. Для A1 достаточно знакомых названий, моделей je/sú и нескольких частотных глаголов.",
    rules: [
      "Тип жилья сообщается моделью bývať v: Bývam v byte. Bývame v dome. Формы doma и domov означают «дома» и «домой», но не заменяют v byte/v dome.",
      "Основные комнаты: izba, obývačka, spálňa, kuchyňa, kúpeľňa, chodba и balkón.",
      "Один предмет вводится через je, несколько — через sú: V izbe je stôl. V izbe sú dve stoličky.",
      "Место учите готовыми блоками: v kuchyni, v kúpeľni, na stole, na poličke, pri okne, vedľa postele.",
      "Домашние дела сообщаются в настоящем времени: varím, umývam riad, upratujem, vysávam, periem.",
      "В коротком описании соединяйте факты словами a, ale и potom: Byt je malý, ale svetlý. Večer varím a potom umývam riad.",
    ],
    examples: [
      { slovak: "Bývam v malom byte.", russian: "Я живу в маленькой квартире.", explanation: "После v используется готовая форма v malom byte." },
      { slovak: "V kuchyni je veľký stôl.", russian: "На кухне большой стол.", explanation: "Один stôl требует формы je." },
      { slovak: "Knihy sú na poličke.", russian: "Книги на полке.", explanation: "Несколько книг требуют sú; место — na poličke." },
      { slovak: "Večer upratujem izbu.", russian: "Вечером я убираю комнату.", explanation: "Upratujem — форма первого лица настоящего времени." },
      { slovak: "Posteľ je vedľa okna.", russian: "Кровать находится рядом с окном.", explanation: "Vedľa обозначает положение рядом с предметом." },
      { slovak: "Doma varím a umývam riad.", russian: "Дома я готовлю и мою посуду.", explanation: "Doma отвечает на вопрос «где?»." },
    ],
  },
  sections: [
    {
      title: "Жильё и комнаты",
      paragraphs: [
        "Сначала назовите тип жилья: byt — квартира, dom — дом. Затем перечислите только основные комнаты. Для сообщения о месте жительства используйте v byte или v dome.",
        "Doma означает «дома», а domov — направление «домой»: Som doma. Idem domov. Эти слова не называют тип жилья.",
      ],
      table: { headers: ["Словацкий", "Русский", "Готовая форма места"], rows: [
        ["byt", "квартира", "v byte"], ["dom", "дом", "v dome"], ["izba", "комната", "v izbe"],
        ["kuchyňa", "кухня", "v kuchyni"], ["kúpeľňa", "ванная", "v kúpeľni"], ["obývačka", "гостиная", "v obývačke"],
        ["spálňa", "спальня", "v spálni"], ["chodba / balkón", "коридор / балкон", "na chodbe / na balkóne"],
      ] },
      items: ["Bývam v byte.", "Bývame v malom dome.", "V byte je kuchyňa, kúpeľňa a obývačka."],
      note: "Kde bývate? — Bývam v byte. Kde ste? — Som doma. Kam idete? — Idem domov.",
    },
    {
      title: "Что есть в комнате: je и sú",
      paragraphs: [
        "Je используется с одним предметом, sú — с несколькими. Число определяет форму глагола: V izbe je posteľ. V izbe sú dve postele.",
        "Если сначала стоит место, порядок остаётся простым: V kuchyni je stôl. Na stole sú knihy. Вопросы строятся с Čo je ...? или Čo je/sú v ...?",
      ],
      table: { headers: ["Количество", "Модель", "Перевод"], rows: [
        ["один предмет", "V kuchyni je veľký stôl.", "На кухне большой стол."], ["один предмет", "V spálni je posteľ.", "В спальне кровать."],
        ["несколько", "V izbe sú dve stoličky.", "В комнате два стула."], ["несколько", "Na poličke sú knihy.", "На полке книги."],
        ["отсутствие", "V byte nie je balkón.", "В квартире нет балкона."],
      ] },
      items: ["Čo je v kuchyni? — V kuchyni je stôl.", "Čo je v izbe? — V izbe je posteľ. Je tam aj skriňa.", "Sú v kúpeľni dve skrine? — Nie."],
      note: "Не переносите русскую фразу без глагола: «В комнате стол» → V izbe je stôl.",
    },
    {
      title: "Предметы и их расположение",
      paragraphs: [
        "Называйте только те отношения, которые нужны для ориентации: внутри комнаты, на поверхности, рядом с окном или возле мебели. Форму существительного после предлога учите вместе со всем блоком.",
        "Частые предметы: stôl, stolička, posteľ, skriňa, polička, pohovka, chladnička, sporák и práčka.",
      ],
      table: { headers: ["Где", "Модель", "Перевод"], rows: [
        ["v", "Práčka je v kúpeľni.", "Стиральная машина в ванной."], ["na", "Kniha je na stole.", "Книга на столе."],
        ["pri", "Stôl je pri okne.", "Стол у окна."], ["vedľa", "Skriňa je vedľa postele.", "Шкаф рядом с кроватью."],
        ["medzi", "Stôl je medzi oknom a dverami.", "Стол между окном и дверью."],
      ] },
      items: ["Knihy sú na poličke.", "Pohovka je pri okne.", "Chladnička je v kuchyni."],
      note: "Не выбирайте v или na по русскому переводу: запоминайте v kuchyni, но na stole и na balkóne.",
    },
    {
      title: "Обычные домашние дела",
      paragraphs: [
        "Для быта нужны короткие глагольные модели. Лицо уже видно по форме глагола, поэтому ja можно опустить: Varím večeru. Upratujem izbu.",
        "Добавьте время или частотность: ráno, večer, každý deň, často, cez víkend. Несколько действий соединяйте через a или potom.",
      ],
      table: { headers: ["Глагол", "Готовая фраза", "Перевод"], rows: [
        ["upratovať", "Večer upratujem izbu.", "Вечером я убираю комнату."], ["variť", "V kuchyni varím večeru.", "На кухне я готовлю ужин."],
        ["umývať", "Po večeri umývam riad.", "После ужина я мою посуду."], ["vysávať", "Cez víkend vysávam.", "На выходных я пылесошу."],
        ["prať", "V sobotu periem.", "В субботу я стираю."],
      ] },
      items: ["Ráno ustieľam posteľ.", "Často upratujem kuchyňu.", "Najprv varím a potom umývam riad."],
      note: "Для описания привычки используйте настоящее время: každý deň upratujem, cez víkend periem.",
    },
    {
      title: "Описание дома и частые ошибки",
      paragraphs: [
        "Соберите описание по маршруту: тип жилья → комнаты → один предмет и его место → одно бытовое действие. Четырёх-пяти коротких фраз достаточно.",
        "Перед ответом проверьте doma/domov, форму je/sú, готовую форму места и личную форму глагола.",
      ],
      table: { headers: ["Ошибка", "Правильно", "Почему"], rows: [
        ["Bývam v byt.", "Bývam v byte.", "После v нужна готовая форма v byte."], ["V izbe sú stôl.", "V izbe je stôl.", "Stôl — один предмет."],
        ["Knihy sú v poličke.", "Knihy sú na poličke.", "Нормативная модель — na poličke."], ["Som domov.", "Som doma.", "Doma — где; domov — куда."],
        ["Večer upratuje izbu.", "Večer upratujem izbu.", "Говорящий использует первое лицо."],
      ] },
      items: ["Bývam v malom byte.", "V byte je kuchyňa a obývačka.", "V obývačke je pohovka pri okne.", "Večer upratujem a potom umývam riad."],
      note: "Не требуется описывать ремонт, площадь или технические характеристики жилья.",
    },
  ],
  stepPractices: [
    { id: "m6-home-step-1", sectionIndex: 0, type: "pairs", prompt: "Выберите готовую форму места.", answer: "Bývam v malom byte.; v dome; v kuchyni; v kúpeľni; na balkóne", pairs: [
      { prompt: "Я живу в маленькой квартире.", answer: "Bývam v malom byte.", options: ["Bývam v malom byte.", "Som malý byt."] }, { prompt: "в доме", answer: "v dome", options: ["v dom", "v dome"] },
      { prompt: "на кухне", answer: "v kuchyni", options: ["na kuchyni", "v kuchyni"] }, { prompt: "в ванной", answer: "v kúpeľni", options: ["v kúpeľni", "na kúpeľni"] },
      { prompt: "на балконе", answer: "na balkóne", options: ["v balkóne", "na balkóne"] },
    ], hint: "Выбирайте готовый блок, а не переводите предлог отдельно.", explanation: "Правильно: v malom byte, v dome, v kuchyni, v kúpeľni, na balkóne." },
    { id: "m6-home-step-2", sectionIndex: 1, type: "pairs", prompt: "Выберите je или sú.", answer: "V kuchyni je veľký stôl.; je; sú; sú; nie je", pairs: [
      { prompt: "На кухне большой стол.", answer: "V kuchyni je veľký stôl.", options: ["V kuchyni je veľký stôl.", "V kuchyni sú veľký stôl."] },
      { prompt: "V spálni ___ posteľ.", answer: "je", options: ["je", "sú"] }, { prompt: "V izbe ___ dve stoličky.", answer: "sú", options: ["je", "sú"] },
      { prompt: "Na poličke ___ knihy.", answer: "sú", options: ["je", "sú"] }, { prompt: "V byte ___ balkón. · нет", answer: "nie je", options: ["nie je", "nie sú"] },
    ], hint: "Один предмет — je, несколько — sú.", explanation: "Posteľ и stôl требуют je; dve stoličky и knihy — sú; один отсутствующий balkón — nie je." },
    { id: "m6-home-step-3", sectionIndex: 2, type: "pairs", prompt: "Выберите подходящее расположение предмета.", answer: "Knihy sú na poličke.; v; na; pri; vedľa", pairs: [
      { prompt: "Книги на полке.", answer: "Knihy sú na poličke.", options: ["Knihy sú v poličke.", "Knihy sú na poličke."] },
      { prompt: "Práčka je ___ kúpeľni.", answer: "v", options: ["v", "na", "pri", "vedľa"] }, { prompt: "Kniha je ___ stole.", answer: "na", options: ["v", "na", "pri", "vedľa"] },
      { prompt: "Stôl je ___ okne.", answer: "pri", options: ["v", "na", "pri", "vedľa"] }, { prompt: "Skriňa je ___ postele.", answer: "vedľa", options: ["v", "na", "pri", "vedľa"] },
    ], hint: "Сверьте модель места из таблицы.", explanation: "Práčka je v kúpeľni; kniha na stole; stôl pri okne; skriňa vedľa postele." },
    { id: "m6-home-step-4", sectionIndex: 3, type: "pairs", prompt: "Переведите бытовые действия.", answer: "Večer upratujem izbu.; V kuchyni varím večeru.; Umývam riad.; Cez víkend vysávam.", pairs: [
      { prompt: "Вечером я убираю комнату.", answer: "Večer upratujem izbu.", inputHint: "Введите перевод" }, { prompt: "На кухне я готовлю ужин.", answer: "V kuchyni varím večeru.", inputHint: "Введите перевод" },
      { prompt: "Я мою посуду.", answer: "Umývam riad.", inputHint: "Введите перевод" }, { prompt: "На выходных я пылесошу.", answer: "Cez víkend vysávam.", inputHint: "Введите перевод" },
    ], hint: "Используйте форму первого лица и сохраните диакритику.", explanation: "Опорные формы: upratujem, varím, umývam и vysávam." },
    { id: "m6-home-step-5", sectionIndex: 4, type: "pairs", prompt: "Исправьте каждую фразу.", answer: "V izbe je stôl a dve stoličky.; Bývam v byte.; Knihy sú na poličke.; Som doma.; Večer upratujem izbu.", pairs: [
      { prompt: "В комнате есть стол и два стула.", answer: "V izbe je stôl a dve stoličky.", inputHint: "Введите перевод" }, { prompt: "Bývam v byt.", answer: "Bývam v byte.", inputHint: "Введите исправленную фразу" },
      { prompt: "Knihy sú v poličke.", answer: "Knihy sú na poličke.", inputHint: "Введите исправленную фразу" }, { prompt: "Som domov.", answer: "Som doma.", inputHint: "Введите исправленную фразу" },
      { prompt: "Večer upratuje izbu. · я", answer: "Večer upratujem izbu.", inputHint: "Введите исправленную фразу" },
    ], hint: "Проверьте je/sú, форму места, doma/domov и лицо глагола.", explanation: "Нормативно: V izbe je stôl a dve stoličky; v byte; na poličke; doma; upratujem." },
  ],
  assessmentMode: "interactive",
  materialAssessmentStep: false,
  reinforcementLabel: "Финальный тест темы",
  reinforcementTitle: "Выполните шесть заданий темы 2",
  reinforcementPractices: [
    { id: "reinforcement:home:1", sectionIndex: 0, type: "pairs", prompt: "Определите: комната, предмет или действие.", answer: "комната; предмет; комната; предмет; действие", pairs: [
      { prompt: "kuchyňa", answer: "комната", options: ["комната", "предмет", "действие"] }, { prompt: "posteľ", answer: "предмет", options: ["комната", "предмет", "действие"] },
      { prompt: "kúpeľňa", answer: "комната", options: ["комната", "предмет", "действие"] }, { prompt: "polička", answer: "предмет", options: ["комната", "предмет", "действие"] },
      { prompt: "upratovať", answer: "действие", options: ["комната", "предмет", "действие"] },
    ], showSlovakKeyboard: false, hint: "Определите роль слова в описании дома.", explanation: "Kuchyňa и kúpeľňa — комнаты; posteľ и polička — предметы; upratovať — действие." },
    { id: "reinforcement:home:2", sectionIndex: 1, type: "pairs", prompt: "Выберите форму наличия для каждого предмета.", answer: "je; sú; je; sú; nie je", pairs: [
      { prompt: "V izbe ___ stôl.", answer: "je", options: ["je", "sú", "nie je", "nie sú"] }, { prompt: "V izbe ___ dve stoličky.", answer: "sú", options: ["je", "sú", "nie je", "nie sú"] },
      { prompt: "V kuchyni ___ chladnička.", answer: "je", options: ["je", "sú", "nie je", "nie sú"] }, { prompt: "Na stole ___ knihy.", answer: "sú", options: ["je", "sú", "nie je", "nie sú"] },
      { prompt: "V byte ___ balkón. · нет", answer: "nie je", options: ["je", "sú", "nie je", "nie sú"] },
    ], hint: "Смотрите на число и наличие или отсутствие.", explanation: "Один предмет — je/nie je; несколько предметов — sú/nie sú." },
    { id: "reinforcement:home:3", sectionIndex: 2, type: "pairs", prompt: "Вставьте предлог в готовую модель места.", answer: "v; na; pri; vedľa; na", pairs: [
      { prompt: "Práčka je ___ kúpeľni.", answer: "v", options: ["v", "na", "pri", "vedľa"] }, { prompt: "Knihy sú ___ poličke.", answer: "na", options: ["v", "na", "pri", "vedľa"] },
      { prompt: "Pohovka je ___ okne.", answer: "pri", options: ["v", "na", "pri", "vedľa"] }, { prompt: "Skriňa je ___ postele.", answer: "vedľa", options: ["v", "na", "pri", "vedľa"] },
      { prompt: "Stolička je ___ balkóne.", answer: "na", options: ["v", "na", "pri", "vedľa"] },
    ], hint: "Выберите блок, который изучен вместе с существительным.", explanation: "Правильно: v kúpeľni, na poličke, pri okne, vedľa postele, na balkóne." },
    { id: "reinforcement:home:4", sectionIndex: 4, type: "pairs", prompt: "Исправьте ошибки в описании жилья.", answer: "Bývam v malom byte.; V kuchyni je stôl.; Knihy sú na poličke.; Som doma.; Večer upratujem izbu.", pairs: [
      { prompt: "Bývam v malý byt.", answer: "Bývam v malom byte.", inputHint: "Введите исправленную фразу" }, { prompt: "V kuchyni sú stôl.", answer: "V kuchyni je stôl.", inputHint: "Введите исправленную фразу" },
      { prompt: "Knihy je na poličke.", answer: "Knihy sú na poličke.", inputHint: "Введите исправленную фразу" }, { prompt: "Som domov.", answer: "Som doma.", inputHint: "Введите исправленную фразу" },
      { prompt: "Večer upratuje izbu. · я", answer: "Večer upratujem izbu.", inputHint: "Введите исправленную фразу" },
    ], hint: "Исправьте всю фразу и сохраните диакритику.", explanation: "Проверьте согласование прилагательного, je/sú, doma/domov и форму первого лица." },
    { id: "reinforcement:home:5", sectionIndex: 3, type: "pairs", prompt: "Переведите на словацкий.", answer: "Bývam v malom byte.; V kuchyni je veľký stôl.; Knihy sú na poličke.; Večer upratujem izbu.; Som doma.", pairs: [
      { prompt: "Я живу в маленькой квартире.", answer: "Bývam v malom byte.", acceptableAnswers: ["Žijem v malom byte."], inputHint: "Введите перевод" },
      { prompt: "На кухне большой стол.", answer: "V kuchyni je veľký stôl.", inputHint: "Введите перевод" }, { prompt: "Книги на полке.", answer: "Knihy sú na poličke.", inputHint: "Введите перевод" },
      { prompt: "Вечером я убираю комнату.", answer: "Večer upratujem izbu.", inputHint: "Введите перевод" }, { prompt: "Я дома.", answer: "Som doma.", inputHint: "Введите перевод" },
    ], hint: "Используйте готовые модели и проверьте словацкую диакритику.", explanation: "Переводы используют bývam, je/sú, na poličke, upratujem и doma." },
    { id: "reinforcement:home:6", sectionIndex: 4, type: "pairs", prompt: "Соберите связное описание квартиры.", answer: "Bývam v malom byte.; V byte je kuchyňa a obývačka.; V obývačke je pohovka.; Pohovka je pri okne.; Večer upratujem izbu.", pairs: [
      { prompt: "1 · тип жилья", answer: "Bývam v malom byte.", options: ["Bývam v malom byte.", "Som malý byt.", "Idem v malom byte."] },
      { prompt: "2 · комнаты", answer: "V byte je kuchyňa a obývačka.", options: ["V byte sú kuchyňa.", "V byte je kuchyňa a obývačka.", "V byt je kuchyňa."] },
      { prompt: "3 · предмет", answer: "V obývačke je pohovka.", options: ["V obývačke je pohovka.", "V obývačke sú pohovka.", "Na obývačke je pohovka."] },
      { prompt: "4 · место", answer: "Pohovka je pri okne.", options: ["Pohovka pri okne.", "Pohovka je na okne.", "Pohovka je pri okne."] },
      { prompt: "5 · действие", answer: "Večer upratujem izbu.", options: ["Večer upratuje izbu.", "Večer upratujem izbu.", "Večer som upratujem izbu."] },
    ], hint: "Все пять строк образуют описание от первого лица.", explanation: "Описание называет тип жилья, комнаты, предмет, его место и одно бытовое действие." },
  ],
  knowledgeChecks: [
    { id: "m6-home-check-1", question: "Как сказать «Я живу в маленькой квартире»?", options: ["Bývam v malom byte.", "Som v malý byt.", "Idem v malom byte."], answer: "Bývam v malom byte.", explanation: "Тип жилья сообщается моделью bývať v; после v — v malom byte." },
    { id: "m6-home-check-2", question: "Как сказать «На кухне большой стол»?", options: ["V kuchyni je veľký stôl.", "Na kuchyni sú veľký stôl.", "V kuchyňa je veľký stôl."], answer: "V kuchyni je veľký stôl.", explanation: "Нормативный блок места — v kuchyni; один stôl требует je." },
    { id: "m6-home-check-3", question: "Как правильно различить «дома» и «домой»?", options: ["Som doma. Idem domov.", "Som domov. Idem doma.", "Som v domov. Idem do doma."], answer: "Som doma. Idem domov.", explanation: "Doma отвечает на «где?», domov — на «куда?»." },
  ],
  finalChecks: [
    { id: "m6-home-final-1", question: "Выберите нормативное описание комнаты.", options: ["V izbe je stôl a dve stoličky.", "V izba sú stôl a dve stolička.", "Na izbe je stôl a dva stoličky."], answer: "V izbe je stôl a dve stoličky.", explanation: "Нужны готовая форма v izbe, je перед перечислением и dve stoličky." },
  ],
  chatPrompt: "Опишите своё или вымышленное жильё пятью короткими фразами: тип жилья, две комнаты, один предмет и его место, одно бытовое действие.",
  chatSuggestions: ["Bývam v malom byte.", "V kuchyni je veľký stôl.", "Večer upratujem izbu."],
} satisfies CourseLesson;
