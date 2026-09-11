import type { CourseLesson } from "../../../courseTypes";

const textTypeOptions = ["otváracie hodiny", "oznam", "menu", "cestovný poriadok", "zákaz"];
const openingValueOptions = ["9:00", "18:00", "12:00–13:00", "pondelok–piatok", "nedeľa"];
const menuValueOptions = ["paradajková", "kuracie mäso s ryžou", "voda", "7,90 €", "denné menu"];
const timetableValueOptions = ["R 603", "8:15", "9:05", "2", "10 minút"];

export const noticesMenusTimetablesLesson = {
  vocabulary: [
    {"word":"Otvorené: 9:00–18:00","translation":"Открыто: 9:00–18:00","example":"Otvorené: 9:00–18:00"},
    {"word":"Dnes zatvorené.","translation":"Сегодня закрыто.","example":"Dnes zatvorené."},
    {"word":"Denné menu: 7,90 €","translation":"Дневное меню: 7,90 евро","example":"Denné menu: 7,90 €"},
    {"word":"Vlak mešká 10 minút.","translation":"Поезд опаздывает на 10 минут.","example":"Vlak mešká 10 minút."},
    {"word":"Odchod: 8:15, nástupište: 2","translation":"Отправление: 8:15, платформа: 2","example":"Odchod: 8:15, nástupište: 2"},
    {"word":"Vstup zakázaný.","translation":"Вход запрещён.","example":"Vstup zakázaný."},
  ],
  slug: "notices-menus-timetables",
  order: 17,
  title: "Объявления, меню и расписания",
  slovakTitle: "Oznamy, menu a cestovné poriadky",
  description: "Извлекайте время, цену, место и нужное действие из коротких практических текстов.",
  duration: "35–40 мин",
  goals: [
    "Определять тип короткого текста по заголовку и ключевым словам",
    "Понимать часы работы, выходной и перерыв",
    "Находить блюдо, напиток и цену в простом меню",
    "Читать время отправления, прибытия, платформу и опоздание",
    "Извлекать нужный факт без полного перевода текста",
  ],
  theory: {
    summary: "Объявление, меню и расписание удобно читать не по словам, а по задаче. Сначала определите тип текста, затем найдите подпись нужного поля, цифры и единицы. После этого проверьте, относится ли найденный факт к нужному дню, блюду или рейсу.",
    rules: [
      "Сигнальные слова: oznam — объявление, otvorené/zatvorené — открыто/закрыто, zákaz — запрет, menu — меню, cestovný poriadok — расписание транспорта.",
      "Часы работы читаются через od–do или диапазон: Otvorené od 9:00 do 18:00. Prestávka означает перерыв.",
      "В меню ищите разделы polievka, hlavné jedlo, nápoj и cena. Десятичная цена в Словакии обычно пишется через запятую: 7,90 €.",
      "В расписании ключевые подписи — odchod, príchod, nástupište, zastávka и meškanie. Vlak mešká 10 minút сообщает задержку.",
      "Не делайте вывод по одному незнакомому слову: сопоставьте заголовок, подпись, число, единицу и нужную строку.",
    ],
    examples: [
      { slovak: "Otvorené: 9:00–18:00", russian: "Открыто: 9:00–18:00", explanation: "Диапазон показывает начало и конец работы." },
      { slovak: "Dnes zatvorené.", russian: "Сегодня закрыто.", explanation: "Zatvorené отменяет обычные часы работы на сегодня." },
      { slovak: "Denné menu: 7,90 €", russian: "Дневное меню: 7,90 евро", explanation: "Цена относится ко всему дневному меню." },
      { slovak: "Vlak mešká 10 minút.", russian: "Поезд опаздывает на 10 минут.", explanation: "Число после mešká показывает длительность задержки." },
      { slovak: "Odchod: 8:15, nástupište: 2", russian: "Отправление: 8:15, платформа: 2", explanation: "В одной строке указаны время и место посадки." },
      { slovak: "Vstup zakázaný.", russian: "Вход запрещён.", explanation: "Короткий запрет сообщает требуемое действие." },
    ],
  },
  sections: [
    {
      title: "Тип текста и сигнальные слова",
      paragraphs: ["Сначала посмотрите на заголовок, оформление и повторяющиеся подписи. Так можно понять задачу ещё до чтения всех слов.", "После определения типа задайте практический вопрос: когда открыто, сколько стоит, откуда отправляется или что запрещено?"],
      table: { headers: ["Сигнал", "Тип", "Что искать"], rows: [
        ["Otvorené / zatvorené", "otváracie hodiny", "день и время"], ["Oznam", "oznam", "изменение или действие"],
        ["Polievka / cena", "menu", "блюдо и цену"], ["Odchod / príchod", "cestovný poriadok", "рейс и время"],
        ["Zakázaný / zákaz", "zákaz", "что нельзя делать"],
      ] },
      items: ["Pozor! — Внимание!", "Informácia — информация", "Vstup — вход", "Výstup — выход"],
      note: "Цель — быстро найти нужный факт, а не перевести текст полностью.",
    },
    {
      title: "Часы работы и короткое объявление",
      paragraphs: ["В часах работы найдите день, начало, конец и возможный перерыв. Pondelok–piatok означает период с понедельника по пятницу.", "Строка Dnes zatvorené важнее обычного расписания: сегодня место не работает."],
      table: { headers: ["Строка", "Факт", "Перевод"], rows: [
        ["Pondelok–piatok: 9:00–18:00", "рабочие дни", "Пн–Пт: 9:00–18:00"], ["Prestávka: 12:00–13:00", "перерыв", "Перерыв: 12:00–13:00"],
        ["Sobota: 9:00–12:00", "короткий день", "Суббота: 9:00–12:00"], ["Nedeľa: zatvorené", "выходной", "Воскресенье: закрыто"],
        ["Dnes zatvorené.", "изменение сегодня", "Сегодня закрыто."],
      ] },
      items: ["Otvorené od deviatej do osemnástej. — Открыто с девяти до восемнадцати.", "Kedy je otvorené? — Когда открыто?", "Kedy je prestávka? — Когда перерыв?"],
      note: "Проверяйте конкретный день: часы в будни могут отличаться от субботы и воскресенья.",
    },
    {
      title: "Меню: раздел, блюдо и цена",
      paragraphs: ["В меню сначала найдите название раздела, затем конкретную строку и цену справа от неё.", "Учебный образец: Denné menu — paradajková polievka, kuracie mäso s ryžou, voda; cena 7,90 €."],
      table: { headers: ["Раздел", "Учебный образец", "Перевод"], rows: [
        ["Polievka", "paradajková", "томатный суп"], ["Hlavné jedlo", "kuracie mäso s ryžou", "куриное мясо с рисом"],
        ["Nápoj", "voda", "вода"], ["Cena", "7,90 €", "7,90 евро"], ["Denné menu", "polievka + jedlo + nápoj", "дневное меню"],
      ] },
      items: ["Čo je v dennom menu? — Что входит в дневное меню?", "Koľko stojí menu? — Сколько стоит меню?", "Bez nápoja — без напитка"],
      note: "Убедитесь, относится ли цена к одному блюду или ко всему dennému menu.",
    },
    {
      title: "Расписание и задержка транспорта",
      paragraphs: ["В расписании выберите нужный рейс и читайте его строку слева направо. Не переносите время с соседней строки.", "Образец: Vlak R 603 — odchod 8:15, príchod 9:05, nástupište 2, meškanie 10 minút."],
      table: { headers: ["Подпись", "Значение", "Перевод"], rows: [
        ["Vlak", "R 603", "поезд R 603"], ["Odchod", "8:15", "отправление в 8:15"], ["Príchod", "9:05", "прибытие в 9:05"],
        ["Nástupište", "2", "платформа 2"], ["Meškanie", "10 minút", "задержка 10 минут"],
      ] },
      items: ["Autobus číslo 50 — автобус номер 50", "Zastávka Centrum — остановка «Центр»", "Vlak mešká. — Поезд опаздывает."],
      note: "Odchod — когда транспорт уезжает; príchod — когда приезжает.",
    },
    {
      title: "Алгоритм чтения и частые ошибки",
      paragraphs: ["Работайте по шагам: определите тип текста → прочитайте вопрос → найдите подпись → проверьте цифру и единицу → сравните с нужным днём или рейсом.", "Диакритика помогает различать нормативные слова: otvorené, denné, mešká, nástupište. В цене не заменяйте десятичную запятую точкой."],
      table: { headers: ["Ошибка", "Правильно", "Что проверить"], rows: [
        ["Otvorene: 9:00–18:00", "Otvorené: 9:00–18:00", "долготу в otvorené"], ["Denne menu: 7.90 €", "Denné menu: 7,90 €", "долготу и десятичную запятую"],
        ["Vlak meška 10 minút.", "Vlak mešká 10 minút.", "долготу в mešká"], ["Nastupiste: 2", "Nástupište: 2", "словацкую диакритику"],
        ["Odchod 9:05", "Príchod: 9:05", "значение подписи в образце"],
      ] },
      items: ["Какой это текст?", "Какой факт спрашивают?", "Какая подпись стоит рядом с числом?", "К какой строке относится значение?"],
      note: "Незнакомое слово можно пропустить, если заголовок и нужная строка уже дают точный ответ.",
    },
  ],
  stepPractices: [
    { id: "m6-notices-menus-timetables-step-1", sectionIndex: 0, type: "pairs", prompt: "Определите тип практического текста.", answer: "otváracie hodiny; oznam; menu; cestovný poriadok; zákaz", pairs: [
      { prompt: "Otvorené / zatvorené", answer: "otváracie hodiny", options: textTypeOptions }, { prompt: "Dnes nefunguje výťah.", answer: "oznam", options: textTypeOptions },
      { prompt: "Polievka / hlavné jedlo / cena", answer: "menu", options: textTypeOptions }, { prompt: "Odchod / príchod", answer: "cestovný poriadok", options: textTypeOptions },
      { prompt: "Vstup zakázaný", answer: "zákaz", options: textTypeOptions },
    ], hint: "Ищите заголовок или повторяющиеся подписи.", explanation: "Тип текста подсказывает, какой факт искать дальше." },
    { id: "m6-notices-menus-timetables-step-2", sectionIndex: 1, type: "pairs", prompt: "Извлеките значение из часов работы.", answer: "9:00; 18:00; 12:00–13:00; pondelok–piatok; nedeľa", pairs: [
      { prompt: "начало работы в будни", answer: "9:00", options: openingValueOptions }, { prompt: "конец работы в будни", answer: "18:00", options: openingValueOptions },
      { prompt: "перерыв", answer: "12:00–13:00", options: openingValueOptions }, { prompt: "обычные рабочие дни", answer: "pondelok–piatok", options: openingValueOptions },
      { prompt: "закрыто", answer: "nedeľa", options: openingValueOptions },
    ], hint: "Сверяйте день и функцию времени.", explanation: "Одно расписание содержит начало, конец, перерыв и выходной." },
    { id: "m6-notices-menus-timetables-step-3", sectionIndex: 2, type: "pairs", prompt: "Найдите данные учебного меню.", answer: "paradajková; kuracie mäso s ryžou; voda; 7,90 €; denné menu", pairs: [
      { prompt: "polievka", answer: "paradajková", options: menuValueOptions }, { prompt: "hlavné jedlo", answer: "kuracie mäso s ryžou", options: menuValueOptions },
      { prompt: "nápoj", answer: "voda", options: menuValueOptions }, { prompt: "cena", answer: "7,90 €", options: menuValueOptions }, { prompt: "тип предложения", answer: "denné menu", options: menuValueOptions },
    ], hint: "Читайте подпись слева и значение справа.", explanation: "Меню сообщает суп, главное блюдо, напиток и общую цену." },
    { id: "m6-notices-menus-timetables-step-4", sectionIndex: 3, type: "pairs", prompt: "Извлеките данные поезда R 603.", answer: "R 603; 8:15; 9:05; 2; 10 minút", pairs: [
      { prompt: "vlak", answer: "R 603", options: timetableValueOptions }, { prompt: "odchod", answer: "8:15", options: timetableValueOptions },
      { prompt: "príchod", answer: "9:05", options: timetableValueOptions }, { prompt: "nástupište", answer: "2", options: timetableValueOptions }, { prompt: "meškanie", answer: "10 minút", options: timetableValueOptions },
    ], hint: "Не переносите значение из соседней подписи.", explanation: "Строка рейса даёт номер, два времени, платформу и задержку." },
    { id: "m6-notices-menus-timetables-step-5", sectionIndex: 4, type: "pairs", prompt: "Исправьте подписи и значения.", answer: "Otvorené: 9:00–18:00; Denné menu: 7,90 €; Vlak mešká 10 minút.; Nástupište: 2; Príchod: 9:05", pairs: [
      { prompt: "Otvorene: 9:00–18:00", answer: "Otvorené: 9:00–18:00", inputHint: "Введите исправленную строку" }, { prompt: "Denne menu: 7.90 €", answer: "Denné menu: 7,90 €", inputHint: "Введите исправленную строку" },
      { prompt: "Vlak meška 10 minút.", answer: "Vlak mešká 10 minút.", inputHint: "Введите исправленную строку" }, { prompt: "Nastupiste: 2", answer: "Nástupište: 2", inputHint: "Введите исправленную строку" },
      { prompt: "Odchod 9:05 · по образцу", answer: "Príchod: 9:05", inputHint: "Введите правильную подпись и время" },
    ], hint: "Проверьте диакритику, цену и значение подписи.", explanation: "Нормативная запись помогает точно извлечь практический факт." },
  ],
  assessmentMode: "interactive",
  materialAssessmentStep: false,
  reinforcementLabel: "Финальный тест темы",
  reinforcementTitle: "Выполните шесть заданий темы 17",
  reinforcementPractices: [
    { id: "reinforcement:notices-menus-timetables:1", sectionIndex: 0, type: "pairs", prompt: "Определите тип каждого текста.", answer: "otváracie hodiny; oznam; menu; cestovný poriadok; zákaz", pairs: [
      { prompt: "Otvorené / zatvorené", answer: "otváracie hodiny", options: textTypeOptions }, { prompt: "Dnes nefunguje výťah.", answer: "oznam", options: textTypeOptions },
      { prompt: "Polievka / cena", answer: "menu", options: textTypeOptions }, { prompt: "Odchod / nástupište", answer: "cestovný poriadok", options: textTypeOptions }, { prompt: "Vstup zakázaný", answer: "zákaz", options: textTypeOptions },
    ], hint: "Используйте сигнальные слова.", explanation: "Тип текста определяет дальнейшую стратегию чтения." },
    { id: "reinforcement:notices-menus-timetables:2", sectionIndex: 1, type: "pairs", prompt: "Прочитайте часы работы и выберите факт.", answer: "9:00; 18:00; 12:00–13:00; pondelok–piatok; nedeľa", pairs: [
      { prompt: "открывается в будни", answer: "9:00", options: openingValueOptions }, { prompt: "закрывается в будни", answer: "18:00", options: openingValueOptions },
      { prompt: "перерыв", answer: "12:00–13:00", options: openingValueOptions }, { prompt: "период обычной работы", answer: "pondelok–piatok", options: openingValueOptions }, { prompt: "день, когда закрыто", answer: "nedeľa", options: openingValueOptions },
    ], hint: "Сопоставьте вопрос с конкретной строкой расписания.", explanation: "Пять ответов извлекаются из одного объявления о часах работы." },
    { id: "reinforcement:notices-menus-timetables:3", sectionIndex: 2, type: "pairs", prompt: "Прочитайте учебное меню и выберите значение.", answer: "paradajková; kuracie mäso s ryžou; voda; 7,90 €; denné menu", pairs: [
      { prompt: "суп", answer: "paradajková", options: menuValueOptions }, { prompt: "главное блюдо", answer: "kuracie mäso s ryžou", options: menuValueOptions },
      { prompt: "напиток", answer: "voda", options: menuValueOptions }, { prompt: "цена", answer: "7,90 €", options: menuValueOptions }, { prompt: "вид предложения", answer: "denné menu", options: menuValueOptions },
    ], hint: "Каждое значение стоит рядом со своей подписью.", explanation: "Задание проверяет выбор блюда, напитка, цены и типа меню." },
    { id: "reinforcement:notices-menus-timetables:4", sectionIndex: 3, type: "pairs", prompt: "Прочитайте расписание поезда R 603.", answer: "R 603; 8:15; 9:05; 2; 10 minút", pairs: [
      { prompt: "номер поезда", answer: "R 603", options: timetableValueOptions }, { prompt: "отправление", answer: "8:15", options: timetableValueOptions },
      { prompt: "прибытие", answer: "9:05", options: timetableValueOptions }, { prompt: "платформа", answer: "2", options: timetableValueOptions }, { prompt: "задержка", answer: "10 minút", options: timetableValueOptions },
    ], hint: "Читайте одну строку рейса и различайте odchod/príchod.", explanation: "Все пять фактов относятся к одному поезду." },
    { id: "reinforcement:notices-menus-timetables:5", sectionIndex: 4, type: "pairs", prompt: "Переведите короткие практические тексты.", answer: "Dnes zatvorené.; Otvorené od deviatej do osemnástej.; Denné menu stojí 7,90 €.; Vlak mešká 10 minút.; Vstup zakázaný.", pairs: [
      { prompt: "Сегодня закрыто.", answer: "Dnes zatvorené.", inputHint: "Введите перевод" },
      { prompt: "Открыто с девяти до восемнадцати.", answer: "Otvorené od deviatej do osemnástej.", acceptableAnswers: ["Od deviatej do osemnástej je otvorené."], inputHint: "Введите перевод" },
      { prompt: "Дневное меню стоит 7,90 евро.", answer: "Denné menu stojí 7,90 €.", inputHint: "Введите перевод" },
      { prompt: "Поезд опаздывает на 10 минут.", answer: "Vlak mešká 10 minút.", inputHint: "Введите перевод" },
      { prompt: "Вход запрещён.", answer: "Vstup zakázaný.", inputHint: "Введите перевод" },
    ], hint: "Используйте готовые модели и сохраняйте словацкую диакритику.", explanation: "Переводы проверяют часы работы, цену, задержку и запрет." },
    { id: "reinforcement:notices-menus-timetables:6", sectionIndex: 4, type: "pairs", prompt: "Выберите вывод из каждого короткого текста.", answer: "Сегодня войти нельзя.; Магазин закрывается в 18:00.; Меню стоит 7,90 €.; Поезд отправляется в 8:15.; Поезд опаздывает на 10 минут.", pairs: [
      { prompt: "Dnes vstup zakázaný.", answer: "Сегодня войти нельзя.", options: ["Сегодня войти нельзя.", "Сегодня вход бесплатный.", "Сегодня открыто дольше."] },
      { prompt: "Otvorené: 9:00–18:00", answer: "Магазин закрывается в 18:00.", options: ["Магазин закрывается в 18:00.", "Магазин открывается в 18:00.", "Перерыв начинается в 18:00."] },
      { prompt: "Denné menu: 7,90 €", answer: "Меню стоит 7,90 €.", options: ["Меню стоит 7,90 €.", "Напиток стоит 7,90 €.", "Меню готово в 7:90."] },
      { prompt: "Odchod: 8:15", answer: "Поезд отправляется в 8:15.", options: ["Поезд отправляется в 8:15.", "Поезд прибывает в 8:15.", "Поезд опаздывает на 8 минут."] },
      { prompt: "Meškanie: 10 minút", answer: "Поезд опаздывает на 10 минут.", options: ["Поезд опаздывает на 10 минут.", "Поезд едет 10 минут.", "Поезд на платформе 10."] },
    ], hint: "Выберите только тот вывод, который прямо подтверждается текстом.", explanation: "Практическое чтение требует точного факта без домысливания." },
  ],
  knowledgeChecks: [
    { id: "m6-notices-menus-timetables-check-1", question: "Что означает Dnes zatvorené?", options: ["Сегодня закрыто", "Сегодня открыто", "Сегодня перерыв"], answer: "Сегодня закрыто", explanation: "Zatvorené означает «закрыто»." },
    { id: "m6-notices-menus-timetables-check-2", question: "Какая подпись означает время отправления?", options: ["odchod", "príchod", "meškanie"], answer: "odchod", explanation: "Odchod — отправление, príchod — прибытие." },
    { id: "m6-notices-menus-timetables-check-3", question: "Как правильно читать короткий практический текст?", options: ["Найти тип текста, подпись и нужное значение", "Обязательно перевести каждое слово", "Угадать по одному незнакомому слову"], answer: "Найти тип текста, подпись и нужное значение", explanation: "Так извлекается нужный факт без лишней нагрузки." },
  ],
  finalChecks: [
    { id: "m6-notices-menus-timetables-final-1", question: "Что означает Otvorené od 9:00 do 18:00?", options: ["Открыто с 9:00 до 18:00", "Закрыто в 9:00", "Перерыв с 9:00 до 18:00"], answer: "Открыто с 9:00 до 18:00", explanation: "Od–do задаёт начало и конец диапазона." },
  ],
  chatPrompt: "Прочитайте короткое объявление, учебное меню и расписание; назовите тип каждого текста и извлеките один нужный факт.",
  chatSuggestions: ["Dnes zatvorené.", "Denné menu stojí 7,90 €.", "Vlak mešká 10 minút."],
} satisfies CourseLesson;
