import type { CourseLesson } from "../../../courseTypes";

export const verbNegationQuestionsLesson = {
  vocabulary: [
    {"word":"Dnes nepracujem.","translation":"Сегодня я не работаю.","example":"Dnes nepracujem."},
    {"word":"Nie som unavený.","translation":"Я не устал.","example":"Nie som unavený."},
    {"word":"Nikto nevolá.","translation":"Никто не звонит.","example":"Nikto nevolá."},
    {"word":"Pracuješ dnes?","translation":"Ты сегодня работаешь?","example":"Pracuješ dnes?"},
    {"word":"Kde bývaš?","translation":"Где ты живёшь?","example":"Kde bývaš?"},
    {"word":"Nie, dnes nemôžem.","translation":"Нет, сегодня я не могу.","example":"Nie, dnes nemôžem."},
  ],
  slug: "verb-negation-questions",
  order: 4,
  title: "Отрицание и вопросы с глаголом",
  slovakTitle: "Zápor a otázky",
  description: "Говорите «нет», уточняйте информацию и отвечайте полными короткими фразами.",
  duration: "35–40 мин",
  goals: ["Выбирать между слитным ne- и формами nie som / nie je", "Строить фразы с nikto, nič, nikdy и nikde", "Задавать общие и специальные вопросы без вспомогательного глагола", "Менять лицо глагола при ответе собеседнику", "Поддерживать диалог коротким ответом и одной новой деталью"],
  theory: {
    summary: "У большинства глаголов отрицание образуется слитным ne- перед готовой личной формой. Глагол byť использует отдельное nie. Общий вопрос часто сохраняет порядок слов, а специальный начинается с вопросительного слова.",
    rules: [
      "Обычный глагол: ne- + готовая личная форма — pracujem → nepracujem, mám → nemám, chcem → nechcem.",
      "Особые формы тоже учите парами: idem — nejdem, viem — neviem, môžem — nemôžem.",
      "С byť используется отдельное nie: nie som, nie si, nie je, nie sme, nie ste, nie sú.",
      "Nie в начале ответа означает самостоятельное «нет», после него всё равно нужна полная отрицательная форма: Nie, nepracujem. Nie, nie som doma.",
      "Nikto, nič, nikdy и nikde поддерживаются отрицательной формой глагола: Nikto nepracuje. Nič neviem.",
      "Sa/si остаётся отдельным словом, а ne- присоединяется к глаголу: Neučím sa; Dnes sa neučím; Nedám si kávu.",
      "Общий вопрос не требует вспомогательного глагола: Pracuješ dnes? Специальный начинается с kto, čo, kde, kam, kedy, prečo, ako или koľko.",
      "В ответе меняйте перспективу: Pracuješ dnes? — Áno, pracujem. Bývate tu? — Áno, bývame.",
    ],
    examples: [
      { slovak: "Dnes nepracujem.", russian: "Сегодня я не работаю.", explanation: "Ne- пишется слитно с готовой формой pracujem." },
      { slovak: "Nie som unavený.", russian: "Я не устал.", explanation: "С byť используется отдельное nie." },
      { slovak: "Nikto nevolá.", russian: "Никто не звонит.", explanation: "Отрицательное слово сопровождается отрицательным глаголом." },
      { slovak: "Pracuješ dnes?", russian: "Ты сегодня работаешь?", explanation: "Общий вопрос сохраняет порядок слов." },
      { slovak: "Kde bývaš?", russian: "Где ты живёшь?", explanation: "Специальный вопрос начинается с вопросительного слова." },
      { slovak: "Nie, dnes nemôžem.", russian: "Нет, сегодня я не могу.", explanation: "Nie — ответ «нет», nemôžem — отрицательная личная форма." },
    ],
  },
  sections: [
    {
      title: "Отрицание: ne- и nie",
      paragraphs: ["Поставьте ne- перед уже готовой личной формой: лицо и окончание не меняются. Особые формы запоминайте целиком."],
      table: { headers: ["Утверждение", "Отрицание", "Перевод"], rows: [
        ["pracujem", "nepracujem", "я не работаю"], ["mám", "nemám", "у меня нет"], ["chcem", "nechcem", "я не хочу"],
        ["môžem", "nemôžem", "я не могу"], ["viem", "neviem", "я не знаю / не умею"], ["idem", "nejdem", "я не иду / не еду"],
      ] },
      items: ["byť: nie som — nie si — nie je — nie sme — nie ste — nie sú", "Pracuješ dnes? — Áno, pracujem. / Nie, nepracujem.", "Ste doma? — Áno, sme. / Nie, nie sme.", "Je Peter doma? — Áno, je. / Nie, nie je.", "Môžu prísť? — Áno, môžu. / Nie, nemôžu."],
      note: "Обычный глагол — ne- слитно; byť — отдельное nie; ответ «нет» — Nie, + полная отрицательная форма.",
    },
    {
      title: "Отрицательные слова и разные смыслы",
      paragraphs: ["Одного nikto, nič, nikdy или nikde недостаточно: отрицательное слово поддерживается отрицательной формой глагола."],
      table: { headers: ["Слово", "Значение", "Пример"], rows: [
        ["nikto", "никто", "Nikto nepracuje."], ["nič", "ничего", "Nič neviem."], ["nikdy", "никогда", "Nikdy nepijem kávu."], ["nikde", "нигде", "Nikde nepracujem."],
      ] },
      items: ["Возможны оба порядка: Nič neviem и Neviem nič.", "Učím sa. → Neučím sa. → Dnes sa neučím.", "Dám si kávu. → Nedám si kávu. → Dnes si nedám kávu.", "Chcem sa učiť. → Nechcem sa učiť.", "nemôžem — не могу сейчас; neviem — не знаю / не умею", "nemusím — мне не нужно; nesmiem — мне нельзя", "Ešte nepracujem. — Я ещё не работаю; Už nepracujem. — Я уже не работаю."],
      note: "Не путайте отсутствие обязанности и запрет: Nemusím ísť — не нужно; Nesmiem ísť — нельзя.",
    },
    {
      title: "Общий вопрос и перспектива ответа",
      paragraphs: ["Для вопроса с ответом «да / нет» часто достаточно вопросительной интонации и знака вопроса. Порядок слов можно сохранить; отдельное слово со значением русского «ли» не требуется."],
      table: { headers: ["Сообщение", "Вопрос", "Короткий ответ"], rows: [
        ["Pracuješ dnes.", "Pracuješ dnes?", "Áno, pracujem."], ["Máte čas.", "Máte čas?", "Nie, nemáme."],
        ["Peter môže prísť.", "Môže Peter prísť?", "Nie, nemôže."], ["Učíš sa doma.", "Učíš sa doma?", "Áno, učím sa."],
      ] },
      items: ["Pracuješ dnes? — ty → ja: Áno, pracujem.", "Bývate tu? — vy → my: Áno, bývame.", "Je Nina doma? — Nina → ona: Nie, nie je doma.", "Форма vy может обозначать группу или вежливое обращение к одному человеку; контекст определяет форму ответа."],
      note: "Не копируйте лицо из вопроса автоматически: собеседник спрашивает ty, а вы отвечаете от ja.",
    },
    {
      title: "Специальные вопросы и живой ответ",
      paragraphs: ["Специальный вопрос начинается с вопросительного слова. После него используйте знакомую личную форму; sa/si обычно располагается перед глаголом."],
      table: { headers: ["Слово", "Значение", "Пример"], rows: [
        ["kto", "кто", "Kto pracuje?"], ["čo", "что", "Čo robíš?"], ["kde", "где", "Kde bývate?"], ["kam", "куда", "Kam ideš?"],
        ["kedy", "когда", "Kedy pracujete?"], ["prečo", "почему", "Prečo sa učíš?"], ["ako", "как", "Ako sa voláte?"], ["koľko", "сколько", "Koľko to stojí?"],
      ] },
      items: ["После otázkového slova: Ako sa voláš? Čo si dáte? Kedy sa stretneme?", "Вежливо: Môžete mi pomôcť? Kde bývate?", "Хороший ответ повторяет глагол и добавляет одну деталь: Kedy pracujete? — Pracujem od ôsmej.", "Pracuješ dnes? — Nie, nepracujem. — Prečo nepracuješ? — Nie som doma."],
      note: "Одного áno или nie часто мало для живого диалога: повторите глагол в нужном лице и добавьте деталь.",
    },
    {
      title: "Готовые фразы, ошибки и самопроверка",
      paragraphs: ["Для отрицания восстановите положительную форму. Для вопроса дайте короткий личный ответ и добавьте одну новую деталь."],
      table: { headers: ["Ситуация", "Словацкий пример", "Перевод"], rows: [
        ["работа", "Dnes nepracujem.", "Сегодня я не работаю."], ["время", "Nemám čas.", "У меня нет времени."], ["желание", "Nechcem čakať.", "Я не хочу ждать."],
        ["возможность", "Nemôžem prísť.", "Я не могу прийти."], ["навык", "Neviem variť.", "Я не умею готовить."], ["движение", "Nejdem domov.", "Я не иду домой."],
        ["byť", "Nie som unavený.", "Я не устал."], ["byť", "Nie sú doma.", "Они не дома."], ["никто", "Nikto nevolá.", "Никто не звонит."],
        ["ничего", "Nič neviem.", "Я ничего не знаю."], ["никогда", "Nikdy nepijem kávu.", "Я никогда не пью кофе."], ["ещё не", "Ešte nepracujem.", "Я ещё не работаю."],
        ["sa", "Dnes sa neučím.", "Сегодня я не учусь."], ["si", "Nedám si polievku.", "Я не буду заказывать суп."], ["да / нет", "Pracuješ dnes?", "Ты сегодня работаешь?"],
        ["да / нет", "Máte čas?", "У вас есть время?"], ["место", "Kde bývaš?", "Где ты живёшь?"], ["направление", "Kam ideš?", "Куда ты идёшь?"],
        ["время", "Kedy sa stretneme?", "Когда мы встретимся?"], ["причина", "Prečo sa učíš slovenčinu?", "Почему ты учишь словацкий?"],
      ] },
      items: ["Ne som doma. → Nie som doma.", "Nie pracujem. → Nepracujem.", "Nikto pracuje. → Nikto nepracuje.", "Pracuješ? Áno, pracuješ. → Pracuješ? Áno, pracujem.", "Čo dáte si? → Čo si dáte?"],
      note: "Проверьте ne-/nie, двойное отрицание, вопросительное слово и лицо глагола в каждом ответе.",
    },
  ],
  stepPractices: [
    { id: "m5-verb-negation-questions-step-1", sectionIndex: 0, type: "pairs", prompt: "Сделайте отрицание.", answer: "Nepracujem.; Nie som doma.; Nemáme čas.; Nechce prísť.", pairs: [
      { prompt: "Pracujem.", answer: "Nepracujem.", inputHint: "Введите отрицание" }, { prompt: "Som doma.", answer: "Nie som doma.", inputHint: "Введите отрицание" },
      { prompt: "Máme čas.", answer: "Nemáme čas.", inputHint: "Введите отрицание" }, { prompt: "Chce prísť.", answer: "Nechce prísť.", inputHint: "Введите отрицание" },
    ], hint: "Обычный глагол получает слитное ne-, а byť — отдельное nie.", explanation: "Правильно: nepracujem, nie som, nemáme, nechce." },
    { id: "m5-verb-negation-questions-step-2", sectionIndex: 1, type: "pairs", prompt: "Выберите точную отрицательную модель.", answer: "Nikto nepracuje.; Nič neviem.; Nikdy nepijem kávu.; Nemusím ísť.; Nesmiem vojsť.", pairs: [
      { prompt: "Никто не работает.", answer: "Nikto nepracuje.", options: ["Nikto nepracuje.", "Nikto pracuje."] }, { prompt: "Я ничего не знаю.", answer: "Nič neviem.", options: ["Nič viem.", "Nič neviem."] },
      { prompt: "Я никогда не пью кофе.", answer: "Nikdy nepijem kávu.", options: ["Nikdy pijem kávu.", "Nikdy nepijem kávu."] }, { prompt: "Мне не нужно идти.", answer: "Nemusím ísť.", options: ["Nemusím ísť.", "Nesmiem ísť."] },
      { prompt: "Мне нельзя войти.", answer: "Nesmiem vojsť.", options: ["Nemusím vojsť.", "Nesmiem vojsť."] },
    ], hint: "Проверьте двойное отрицание и смысл nemusím/nesmiem.", explanation: "Отрицательное слово требует отрицательного глагола; nemusím — не нужно, nesmiem — нельзя." },
    { id: "m5-verb-negation-questions-step-3", sectionIndex: 2, type: "pairs", prompt: "Ответьте коротко и измените перспективу.", answer: "Áno, pracujem.; Nie, nie sme doma.; Nie, nemôže.; Áno, učíme sa slovenčinu.", pairs: [
      { prompt: "Pracuješ dnes? · да", answer: "Áno, pracujem.", inputHint: "Введите ответ" }, { prompt: "Ste doma? · нет", answer: "Nie, nie sme doma.", acceptableAnswers: ["Nie, nie sme."], inputHint: "Введите ответ" },
      { prompt: "Môže Peter prísť? · нет", answer: "Nie, nemôže.", inputHint: "Введите ответ" }, { prompt: "Učíte sa slovenčinu? · да, отвечают двое", answer: "Áno, učíme sa slovenčinu.", acceptableAnswers: ["Áno, učíme sa."], inputHint: "Введите ответ" },
    ], hint: "Повторите глагол от лица отвечающего.", explanation: "В ответах ty меняется на ja, vy — на my; третье лицо сохраняется." },
    { id: "m5-verb-negation-questions-step-4", sectionIndex: 3, type: "pairs", prompt: "Выберите вопросительное слово.", answer: "Ako; Kde; Kam; Kedy; Prečo; Koľko", pairs: [
      { prompt: "___ sa voláš?", answer: "Ako", options: ["Ako", "Kde", "Kam", "Kedy", "Prečo", "Koľko"] }, { prompt: "___ bývaš?", answer: "Kde", options: ["Ako", "Kde", "Kam", "Kedy", "Prečo", "Koľko"] },
      { prompt: "___ ideš?", answer: "Kam", options: ["Ako", "Kde", "Kam", "Kedy", "Prečo", "Koľko"] }, { prompt: "___ pracujete?", answer: "Kedy", options: ["Ako", "Kde", "Kam", "Kedy", "Prečo", "Koľko"] },
      { prompt: "___ sa učíš slovenčinu?", answer: "Prečo", options: ["Ako", "Kde", "Kam", "Kedy", "Prečo", "Koľko"] }, { prompt: "___ to stojí?", answer: "Koľko", options: ["Ako", "Kde", "Kam", "Kedy", "Prečo", "Koľko"] },
    ], hint: "Определите, спрашивают ли о способе, месте, направлении, времени, причине или количестве.", explanation: "Ответы: ako, kde, kam, kedy, prečo, koľko." },
    { id: "m5-verb-negation-questions-step-5", sectionIndex: 4, type: "pairs", prompt: "Исправьте ошибки.", answer: "Nie som doma.; Nepracujem.; Nikto nepracuje.; Pracuješ? Áno, pracujem.; Čo si dáte?", pairs: [
      { prompt: "Ne som doma.", answer: "Nie som doma.", inputHint: "Введите исправленную фразу" }, { prompt: "Nie pracujem.", answer: "Nepracujem.", inputHint: "Введите исправленную фразу" },
      { prompt: "Nikto pracuje.", answer: "Nikto nepracuje.", inputHint: "Введите исправленную фразу" }, { prompt: "Pracuješ? Áno, pracuješ.", answer: "Pracuješ? Áno, pracujem.", inputHint: "Введите исправленный обмен" },
      { prompt: "Čo dáte si?", answer: "Čo si dáte?", inputHint: "Введите исправленный вопрос" },
    ], hint: "Проверьте ne-/nie, двойное отрицание, лицо ответа и место si.", explanation: "Исправления соответствуют пяти основным правилам темы." },
  ],
  assessmentMode: "interactive",
  materialAssessmentStep: false,
  reinforcementLabel: "Финальный тест темы",
  reinforcementTitle: "Выполните шесть заданий темы 4",
  reinforcementPractices: [
    { id: "reinforcement:verb-negation-questions:1", sectionIndex: 0, type: "pairs", prompt: "Сделайте отрицание.", answer: "Nepracujem.; Nie som doma.; Nemáme čas.; Nechce prísť.; Neučím sa dnes.; Nedám si kávu.", pairs: [
      { prompt: "Pracujem.", answer: "Nepracujem.", inputHint: "Введите отрицание" }, { prompt: "Som doma.", answer: "Nie som doma.", inputHint: "Введите отрицание" },
      { prompt: "Máme čas.", answer: "Nemáme čas.", inputHint: "Введите отрицание" }, { prompt: "Chce prísť.", answer: "Nechce prísť.", inputHint: "Введите отрицание" },
      { prompt: "Učím sa dnes.", answer: "Neučím sa dnes.", acceptableAnswers: ["Dnes sa neučím."], inputHint: "Введите отрицание" }, { prompt: "Dám si kávu.", answer: "Nedám si kávu.", acceptableAnswers: ["Dnes si nedám kávu."], inputHint: "Введите отрицание" },
    ], hint: "Сохраните лицо и sa/si; выберите слитное ne- или отдельное nie.", explanation: "Шесть фраз проверяют обычный глагол, byť, особую форму и частицы sa/si." },
    { id: "reinforcement:verb-negation-questions:2", sectionIndex: 1, type: "pairs", prompt: "Вставьте отрицательное слово.", answer: "Nikto; Nič; Nikdy; Nikde; nič", pairs: [
      { prompt: "___ nepracuje. · никто", answer: "Nikto", inputHint: "Введите слово" }, { prompt: "___ neviem. · ничего", answer: "Nič", inputHint: "Введите слово" },
      { prompt: "___ nepijem kávu. · никогда", answer: "Nikdy", inputHint: "Введите слово" }, { prompt: "___ nepracujem. · нигде", answer: "Nikde", inputHint: "Введите слово" },
      { prompt: "Nemám ___. · ничего", answer: "nič", inputHint: "Введите слово" },
    ], hint: "Выберите nikto, nič, nikdy или nikde; глагол уже стоит в отрицании.", explanation: "Ответы: Nikto, Nič, Nikdy, Nikde, nič." },
    { id: "reinforcement:verb-negation-questions:3", sectionIndex: 3, type: "pairs", prompt: "Вставьте вопросительное слово.", answer: "Ako; Kde; Kam; Kedy; Prečo; Koľko", pairs: [
      { prompt: "___ sa voláš?", answer: "Ako", options: ["Ako", "Kde", "Kam", "Kedy", "Prečo", "Koľko"] }, { prompt: "___ bývaš?", answer: "Kde", options: ["Ako", "Kde", "Kam", "Kedy", "Prečo", "Koľko"] },
      { prompt: "___ ideš?", answer: "Kam", options: ["Ako", "Kde", "Kam", "Kedy", "Prečo", "Koľko"] }, { prompt: "___ pracujete?", answer: "Kedy", options: ["Ako", "Kde", "Kam", "Kedy", "Prečo", "Koľko"] },
      { prompt: "___ sa učíš slovenčinu?", answer: "Prečo", options: ["Ako", "Kde", "Kam", "Kedy", "Prečo", "Koľko"] }, { prompt: "___ to stojí?", answer: "Koľko", options: ["Ako", "Kde", "Kam", "Kedy", "Prečo", "Koľko"] },
    ], hint: "Определите тип недостающей информации.", explanation: "Ответы: Ako, Kde, Kam, Kedy, Prečo, Koľko." },
    { id: "reinforcement:verb-negation-questions:4", sectionIndex: 2, type: "pairs", prompt: "Дайте короткий ответ.", answer: "Áno, pracujem.; Nie, nie sme doma.; Nie, nemôže.; Áno, učíme sa slovenčinu.", pairs: [
      { prompt: "Pracuješ dnes? · да", answer: "Áno, pracujem.", inputHint: "Введите ответ" }, { prompt: "Ste doma? · нет", answer: "Nie, nie sme doma.", acceptableAnswers: ["Nie, nie sme."], inputHint: "Введите ответ" },
      { prompt: "Môže Peter prísť? · нет", answer: "Nie, nemôže.", inputHint: "Введите ответ" }, { prompt: "Učíte sa slovenčinu? · да, отвечают двое", answer: "Áno, učíme sa slovenčinu.", acceptableAnswers: ["Áno, učíme sa."], inputHint: "Введите ответ" },
    ], hint: "Измените перспективу глагола и не ограничивайтесь одним áno/nie.", explanation: "Ответы используют формы ja, my и третьего лица по ситуации." },
    { id: "reinforcement:verb-negation-questions:5", sectionIndex: 4, type: "pairs", prompt: "Исправьте или переведите.", answer: "Nemám čas.; Nikdy nepijem kávu.; Prečo sa učíš?; Dnes nikto nepracuje.; Kam ideš?", pairs: [
      { prompt: "Nie mám čas.", answer: "Nemám čas.", inputHint: "Введите исправленную фразу" }, { prompt: "Nikdy pijem kávu.", answer: "Nikdy nepijem kávu.", inputHint: "Введите исправленную фразу" },
      { prompt: "Почему ты учишься?", answer: "Prečo sa učíš?", inputHint: "Введите перевод" }, { prompt: "Сегодня никто не работает.", answer: "Dnes nikto nepracuje.", acceptableAnswers: ["Nikto dnes nepracuje."], inputHint: "Введите перевод" },
      { prompt: "Куда ты идёшь?", answer: "Kam ideš?", inputHint: "Введите перевод" },
    ], hint: "Проверьте слитное ne-, двойное отрицание, вопросительное слово и диакритику.", explanation: "Пять строк объединяют исправление отрицания и перевод вопросов." },
    { id: "reinforcement:verb-negation-questions:6", sectionIndex: 3, type: "pairs", prompt: "Соберите мини-диалог о планах.", answer: "Pracuješ dnes?; Nie, nepracujem.; Prečo nepracuješ?; Nie som doma. Som v Bratislave.; Môžeme sa stretnúť večer?; Nie, dnes nemôžem. Môžeme sa stretnúť zajtra.", pairs: [
      { prompt: "1 · общий вопрос", answer: "Pracuješ dnes?", options: ["Pracuješ dnes?", "Pracujem dnes?", "Dnes pracuješ."] },
      { prompt: "2 · короткий отрицательный ответ", answer: "Nie, nepracujem.", options: ["Nie, nepracujem.", "Nie, nepracuješ.", "Nie pracujem."] },
      { prompt: "3 · вопрос о причине", answer: "Prečo nepracuješ?", options: ["Kde nepracuješ?", "Prečo nepracuješ?", "Prečo nepracujem?"] },
      { prompt: "4 · отрицание byť и деталь", answer: "Nie som doma. Som v Bratislave.", options: ["Ne som doma. Som v Bratislave.", "Nie som doma. Som v Bratislave.", "Nie, som doma. Nie v Bratislave."] },
      { prompt: "5 · предложение встречи", answer: "Môžeme sa stretnúť večer?", options: ["Môžeme sa stretnúť večer?", "Môžeme stretnúť sa večer?", "Môžem sa stretnúť večer?"] },
      { prompt: "6 · невозможность и новая деталь", answer: "Nie, dnes nemôžem. Môžeme sa stretnúť zajtra.", options: ["Nie, dnes neviem. Môžeme sa stretnúť zajtra.", "Nie, dnes nemôžem. Môžeme sa stretnúť zajtra.", "Nie dnes môžem. Môžeme stretnúť sa zajtra."] },
    ], hint: "Проверьте лицо, ne-/nie, вопросительное слово и положение sa.", explanation: "Диалог содержит общий вопрос, специальный вопрос, краткие ответы, отрицание и конструкцию с sa." },
  ],
  knowledgeChecks: [
    { id: "m5-verb-negation-questions-check-1", question: "Какая отрицательная модель правильна?", options: ["Nepracujem.", "Nie pracujem.", "Ne pracujem."], answer: "Nepracujem.", explanation: "С обычным глаголом ne- пишется слитно." },
    { id: "m5-verb-negation-questions-check-2", question: "Как правильно ответить отрицательно на Ste doma?", options: ["Nie, nie sme.", "Nie, ne sme.", "Nie, nie ste."], answer: "Nie, nie sme.", explanation: "В ответе vy меняется на my, а byť использует отдельное nie." },
    { id: "m5-verb-negation-questions-check-3", question: "Какая фраза означает «Никто не работает»?", options: ["Nikto nepracuje.", "Nikto pracuje.", "Nie kto pracuje."], answer: "Nikto nepracuje.", explanation: "Nikto требует отрицательной формы глагола." },
  ],
  finalChecks: [
    { id: "m5-verb-negation-questions-final-1", question: "Выберите правильный вопрос «Почему ты учишь словацкий?»", options: ["Prečo sa učíš slovenčinu?", "Prečo učíš sa slovenčinu?", "Prečo sa učím slovenčinu?"], answer: "Prečo sa učíš slovenčinu?", explanation: "Prečo стоит в начале, sa занимает раннюю позицию, а učíš согласуется с ty." },
  ],
  chatPrompt: "Скажите, чего сегодня не делаете, где не находитесь и что вам не нужно делать. Затем задайте общий вопрос, вопрос с kam и вопрос с prečo и ответьте полными короткими фразами.",
  chatSuggestions: ["Dnes nepracujem.", "Kam ideš?", "Prečo sa učíš slovenčinu?"],
} satisfies CourseLesson;
