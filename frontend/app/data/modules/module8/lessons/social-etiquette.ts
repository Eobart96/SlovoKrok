import type { CourseLesson } from "../../../courseTypes";

export const socialEtiquetteContent = {
  vocabulary: [
    {"word":"Ahoj, ako sa máš?","translation":"Привет, как ты?","example":"Ahoj, ako sa máš?"},
    {"word":"Dobrý deň, ako sa máte?","translation":"Добрый день, как вы?","example":"Dobrý deň, ako sa máte?"},
    {"word":"Prosím vás, môžete mi pomôcť?","translation":"Скажите, пожалуйста, вы можете мне помочь?","example":"Prosím vás, môžete mi pomôcť?"},
    {"word":"Môžeme si tykať?","translation":"Мы можем перейти на ты?","example":"Môžeme si tykať?"},
    {"word":"Áno, rada. Ahoj!","translation":"Да, с удовольствием. Привет!","example":"Áno, rada. Ahoj!"},
    {"word":"Prepáčte, radšej by som zostal pri vykaní.","translation":"Извините, я бы предпочёл остаться на «вы».","example":"Prepáčte, radšej by som zostal pri vykaní."},
  ],
  slug: "social-etiquette",
  order: 1,
  title: "Социальный этикет: ty/vy",
  slovakTitle: "Spoločenská etiketa",
  description: "Выбирать уместное обращение и формулы вежливости.",
  duration: "35–40 мин",
  goals: [
    "Выбирать ty или vy по ситуации",
    "Согласовывать обращение с формой глагола",
    "Предлагать перейти на ty и естественно отвечать",
    "Не смешивать неофициальные и вежливые формулы",
  ],
  theory: {
    summary: "Главная формула: ty + 2-е лицо единственного числа — Ako sa máš?; vy + 2-е лицо множественного числа — Ako sa máte? Если ситуация официальная или взрослый собеседник незнаком, безопасно начать с vy.",
    rules: [
      "Ty — близкое неофициальное обращение к одному человеку; vy — вежливое обращение к одному человеку или обычное обращение к нескольким людям.",
      "После ty используйте форму 2-го лица единственного числа: si, máš, hovoríš, chceš, môžeš, vieš.",
      "После vy используйте форму 2-го лица множественного числа: ste, máte, hovoríte, chcete, môžete, viete.",
      "Местоимения ty и vy часто опускаются: форма глагола уже показывает обращение.",
      "Для перехода на неофициальное общение спросите Môžeme si tykať? и после согласия поменяйте всю связку обращения.",
      "В официальной ситуации сочетайте Dobrý deň, prosím vás и prepáčte; неофициально — ahoj, prosím ťa и prepáč.",
    ],
    examples: [
      { slovak: "Ahoj, ako sa máš?", russian: "Привет, как ты?", explanation: "Ty и máš образуют неофициальную связку." },
      { slovak: "Dobrý deň, ako sa máte?", russian: "Добрый день, как вы?", explanation: "Vy может обозначать одного человека, но глагол стоит во множественном числе." },
      { slovak: "Prosím vás, môžete mi pomôcť?", russian: "Скажите, пожалуйста, вы можете мне помочь?", explanation: "Prosím vás и môžete согласованы как вежливое обращение." },
      { slovak: "Môžeme si tykať?", russian: "Мы можем перейти на ты?", explanation: "Частотная A1-фраза для явного перехода на ty." },
      { slovak: "Áno, rada. Ahoj!", russian: "Да, с удовольствием. Привет!", explanation: "Rada говорит женщина; после согласия общение переходит на ty." },
      { slovak: "Prepáčte, radšej by som zostal pri vykaní.", russian: "Извините, я бы предпочёл остаться на «вы».", explanation: "Вежливый отказ мужчины от перехода на ty." },
    ],
  },
  sections: [
    {
      title: "Ty или vy: определяем дистанцию",
      paragraphs: [
        "Ty используют с другом, близким родственником и обычно со сверстником в неформальной группе. Vy выбирают при первом разговоре с незнакомым взрослым, с врачом, преподавателем или сотрудником учреждения.",
        "Vy также обращение к двум и более людям. Если сомневаетесь, начните с vy: перейти на ty можно позже.",
      ],
      table: { headers: ["Ситуация", "Обычно", "Пример"], rows: [
        ["друг, близкий родственник", "ty", "Ahoj, ako sa máš?"],
        ["ребёнок или сверстник", "ty", "Ako sa voláš?"],
        ["незнакомый взрослый", "vy", "Prosím vás, kde je stanica?"],
        ["врач, преподаватель, сотрудник", "vy", "Môžete mi pomôcť?"],
        ["два и более человека", "vy", "Odkiaľ ste?"],
      ] },
      note: "Безопасное правило A1: официальная ситуация или незнакомый взрослый → vy.",
    },
    {
      title: "Согласуем глагол",
      paragraphs: [
        "После ty нужен глагол во 2-м лице единственного числа. После вежливого vy — форма 2-го лица множественного числа, даже если перед вами один человек.",
        "Ty и vy можно опустить: Máte chvíľu? звучит естественно, потому что форма máte уже показывает обращение.",
      ],
      table: { headers: ["Значение", "ty", "vy / несколько людей"], rows: [
        ["быть", "si", "ste"], ["иметь", "máš", "máte"], ["говорить", "hovoríš", "hovoríte"],
        ["хотеть", "chceš", "chcete"], ["мочь", "môžeš", "môžete"], ["знать / уметь", "vieš", "viete"],
      ] },
      items: ["Kde bývaš? → Kde bývate?", "Rozumieš po slovensky? → Rozumiete po slovensky?", "Chceš kávu? → Chcete kávu?", "Môžeš to zopakovať? → Môžete to zopakovať?"],
      note: "В письме к конкретному человеку возможны уважительные Vy, Vám, Vás с большой буквы; устно различия нет.",
    },
    {
      title: "Как предложить перейти на ty",
      paragraphs: [
        "Если общение стало неформальным, переход лучше обозначить словами. Самая полезная фраза уровня A1 — Môžeme si tykať?",
        "При переходе меняется не одно слово, а вся связка: Prepáčte, môžete… → Prepáč, môžeš…",
      ],
      table: { headers: ["Фраза", "Естественный перевод"], rows: [
        ["Môžeme si tykať?", "Мы можем перейти на ты?"], ["Môžeme si potykať?", "Можем перейти на ты?"],
        ["Budeme si tykať?", "Будем на ты?"], ["Jasné, môžeme.", "Конечно, можем."],
        ["Áno, rada. / Áno, rád.", "Да, с удовольствием. (жен. / муж.)"],
        ["Prepáčte, radšej by som zostal pri vykaní.", "Извините, я бы предпочёл остаться на «вы»."],
      ] },
      items: [
        "На работе: Dobrý deň, ja som Martin. — Teší ma, ja som Anna. — Môžeme si tykať? — Áno, rada. Ahoj, Martin!",
        "На vy: Dobrý deň, pani Nováková. Ako sa máte? — Ďakujem, dobre. A vy? — Tiež dobre, ďakujem.",
      ],
      note: "Вежливо: pán, pani, prosím vás, prepáčte. Неофициально: ahoj, prosím ťa, prepáč.",
    },
    {
      title: "Банк готовых фраз",
      paragraphs: ["Читайте пары вслух: сначала вариант с ty, затем сразу тот же смысл с vy."],
      table: { headers: ["ty — неофициально", "vy — вежливо / мн. число"], rows: [
        ["Ahoj!", "Dobrý deň!"], ["Ako sa máš?", "Ako sa máte?"], ["Ako sa voláš?", "Ako sa voláte?"],
        ["Odkiaľ si?", "Odkiaľ ste?"], ["Kde pracuješ?", "Kde pracujete?"], ["Hovoríš po anglicky?", "Hovoríte po anglicky?"],
        ["Máš čas?", "Máte čas?"], ["Chceš si sadnúť?", "Chcete si sadnúť?"], ["Môžeš mi pomôcť?", "Môžete mi pomôcť?"],
        ["Vieš, kde je pošta?", "Viete, kde je pošta?"], ["Prosím ťa, zopakuj to.", "Prosím vás, zopakujte to."],
        ["Ďakujem ti.", "Ďakujem vám."], ["Prepáč.", "Prepáčte."], ["Maj sa!", "Dovidenia!"],
      ] },
      note: "Для автоматизма преобразуйте каждую фразу с ty в vy, затем сделайте обратное.",
    },
    {
      title: "Типичные ошибки и самопроверка",
      paragraphs: ["Проверяйте местоимение, окончание глагола, приветствие и всю формулу обращения."],
      table: { headers: ["Ошибка", "Правильно", "Почему"], rows: [
        ["Vy máš čas?", "Vy máte čas?", "После vy нужна форма множественного числа."],
        ["Ty ste z Bratislavy?", "Ty si z Bratislavy?", "После ty: si, не ste."],
        ["Prosím ťa, môžete…", "Prosím vás, môžete…", "Не смешиваем две связки."],
        ["Ahoj, pani doktorka.", "Dobrý deň, pani doktorka.", "В официальной ситуации безопаснее нейтральное приветствие."],
      ] },
      items: ["Я могу выбрать ty/vy в знакомой ситуации.", "Я могу задать один вопрос в обеих формах.", "Я могу предложить перейти на ty.", "Я не смешиваю prosím ťa и prosím vás."],
      note: "Четыре опоры: ty — близко; vy — вежливо или к нескольким; согласуйте глагол; сомневаетесь — начните с vy.",
    },
  ],
  stepPractices: [
    { id: "m8-social-etiquette-step-1", sectionIndex: 0, type: "choice", prompt: "Выберите безопасную фразу для незнакомого взрослого.", options: ["Ahoj, ako sa máš?", "Dobrý deň, ako sa máte?", "Čau, ako sa máš?"], answer: "Dobrý deň, ako sa máte?", hint: "Официальная ситуация требует vy.", explanation: "С незнакомым взрослым безопасно начать: Dobrý deň, ako sa máte?" },
    { id: "m8-social-etiquette-step-2", sectionIndex: 1, type: "text", prompt: "Переведите неофициально: «Привет, как ты?»", answer: "Ahoj, ako sa máš?", hint: "Используйте приветствие и форму máš.", explanation: "Верная фраза: Ahoj, ako sa máš?" },
    { id: "m8-social-etiquette-step-3", sectionIndex: 2, type: "text", prompt: "Переведите вежливо: «Пожалуйста, можете мне помочь?»", answer: "Prosím, môžete mi pomôcť?", acceptableAnswers: ["Prosím vás, môžete mi pomôcť?"], hint: "Согласуйте вежливую формулу с môžete.", explanation: "Верно: Prosím, môžete mi pomôcť? Также естественно: Prosím vás, môžete mi pomôcť?" },
    { id: "m8-social-etiquette-step-4", sectionIndex: 3, type: "pairs", prompt: "Выберите вежливую пару для каждой ty-фразы.", answer: "Ako sa máte?; Ako sa voláte?; Odkiaľ ste?; Hovoríte po anglicky?", pairs: [
      { prompt: "Ako sa máš?", answer: "Ako sa máte?", options: ["Ako sa máte?", "Ako sa máš?"] },
      { prompt: "Ako sa voláš?", answer: "Ako sa voláte?", options: ["Ako sa voláte?", "Ako sa voláš?"] },
      { prompt: "Odkiaľ si?", answer: "Odkiaľ ste?", options: ["Odkiaľ ste?", "Odkiaľ si?"] },
      { prompt: "Hovoríš po anglicky?", answer: "Hovoríte po anglicky?", options: ["Hovoríte po anglicky?", "Hovoríš po anglicky?"] },
    ], hint: "В форме vy меняется окончание глагола.", explanation: "Каждая строка преобразована из ty в vy." },
    { id: "m8-social-etiquette-step-5", sectionIndex: 4, type: "pairs", prompt: "Исправьте смешанные формы обращения.", answer: "Vy máte čas?; Ty si z Bratislavy?; Prosím vás, môžete to zopakovať?", pairs: [
      { prompt: "Vy máš čas?", answer: "Vy máte čas?", inputHint: "Введите исправленную фразу" },
      { prompt: "Ty ste z Bratislavy?", answer: "Ty si z Bratislavy?", inputHint: "Введите исправленную фразу" },
      { prompt: "Prosím ťa, môžete to zopakovať?", answer: "Prosím vás, môžete to zopakovať?", inputHint: "Введите исправленную фразу" },
    ], hint: "Согласуйте всю связку ty или vy.", explanation: "Ty требует si/máš и prosím ťa; vy требует ste/máte/môžete и prosím vás." },
  ],
  assessmentMode: "interactive",
  materialAssessmentStep: false,
  reinforcementLabel: "Финальный тест темы",
  reinforcementTitle: "Выполните шесть заданий темы 1",
  reinforcementPractices: [
    { id: "reinforcement:social-etiquette:1", sectionIndex: 0, type: "pairs", prompt: "Выберите форму по ситуации.", answer: "máte; si; chcete", pairs: [
      { prompt: "Pani Nováková, ako sa …?", answer: "máte", options: ["máš", "máte"] },
      { prompt: "Peter, odkiaľ …?", answer: "si", options: ["si", "ste"] },
      { prompt: "Deti, … čaj?", answer: "chcete", options: ["chceš", "chcete"] },
    ], hint: "Один знакомый — ty; вежливость или несколько людей — vy.", explanation: "Правильно: máte; si; chcete." },
    { id: "reinforcement:social-etiquette:2", sectionIndex: 1, type: "pairs", prompt: "Вставьте подходящее слово.", answer: "vás; ti; Ako", pairs: [
      { prompt: "Prosím …, môžete mi pomôcť?", answer: "vás", inputHint: "Введите одно слово" },
      { prompt: "Ďakujem …, Katka.", answer: "ti", inputHint: "Введите одно слово" },
      { prompt: "… sa voláte?", answer: "Ako", inputHint: "Введите одно слово" },
    ], hint: "Смотрите на форму глагола и имя собеседника.", explanation: "Правильно: Prosím vás; Ďakujem ti; Ako sa voláte?" },
    { id: "reinforcement:social-etiquette:3", sectionIndex: 2, type: "pairs", prompt: "Исправьте ошибки в обращении.", answer: "Dobrý deň, odkiaľ ste, pán Horváth?; Ahoj, Eva, máš čas?; Prosím vás, môžete to zopakovať?", pairs: [
      { prompt: "Dobrý deň, odkiaľ si, pán Horváth?", answer: "Dobrý deň, odkiaľ ste, pán Horváth?", inputHint: "Введите исправленную фразу" },
      { prompt: "Ahoj, Eva, máte čas?", answer: "Ahoj, Eva, máš čas?", inputHint: "Введите исправленную фразу" },
      { prompt: "Prosím ťa, môžete to zopakovať?", answer: "Prosím vás, môžete to zopakovať?", inputHint: "Введите исправленную фразу" },
    ], hint: "Не смешивайте ty- и vy-формы.", explanation: "Каждая исправленная фраза последовательно использует одну форму обращения." },
    { id: "reinforcement:social-etiquette:4", sectionIndex: 3, type: "pairs", prompt: "Переведите на словацкий.", answer: "Hovoríte po anglicky?; Vieš, kde je stanica?; Prepáčte, môžete to zopakovať?", pairs: [
      { prompt: "Вы говорите по-английски? (вежливо)", answer: "Hovoríte po anglicky?", inputHint: "Введите перевод" },
      { prompt: "Ты знаешь, где вокзал?", answer: "Vieš, kde je stanica?", inputHint: "Введите перевод" },
      { prompt: "Извините, вы можете повторить?", answer: "Prepáčte, môžete to zopakovať?", inputHint: "Введите перевод" },
    ], hint: "Сначала определите ty или vy, затем выберите форму глагола.", explanation: "В переводах согласованы Hovoríte, Vieš и связка Prepáčte, môžete." },
    { id: "reinforcement:social-etiquette:5", sectionIndex: 3, type: "pairs", prompt: "Преобразуйте ty-фразы в vy.", answer: "Dobrý deň.; Ako sa voláte?; Odkiaľ ste?; Hovoríte po slovensky?", pairs: [
      { prompt: "Ahoj.", answer: "Dobrý deň.", inputHint: "Введите вежливый вариант" },
      { prompt: "Ako sa voláš?", answer: "Ako sa voláte?", inputHint: "Введите вежливый вариант" },
      { prompt: "Odkiaľ si?", answer: "Odkiaľ ste?", inputHint: "Введите вежливый вариант" },
      { prompt: "Hovoríš po slovensky?", answer: "Hovoríte po slovensky?", inputHint: "Введите вежливый вариант" },
    ], hint: "Меняйте приветствие и каждую глагольную форму.", explanation: "Вежливая цепочка: Dobrý deň. Ako sa voláte? Odkiaľ ste? Hovoríte po slovensky?" },
    { id: "reinforcement:social-etiquette:6", sectionIndex: 4, type: "pairs", prompt: "Соберите знакомство со взрослой коллегой и переход на ty.", answer: "Dobrý deň, ja som Ari. Ako sa voláte?; Ja som Lucia. Teší ma.; Aj mňa teší. Odkiaľ ste?; Som z Bratislavy. Môžeme si tykať?; Áno, rada. Ahoj, Ari!", pairs: [
      { prompt: "1 · вежливо представиться и спросить имя", answer: "Dobrý deň, ja som Ari. Ako sa voláte?", options: ["Dobrý deň, ja som Ari. Ako sa voláte?", "Ahoj, ja som Ari. Ako sa voláš?"] },
      { prompt: "2 · представиться в ответ", answer: "Ja som Lucia. Teší ma.", options: ["Ja som Lucia. Teší ma.", "Lucia, máte čas?"] },
      { prompt: "3 · спросить, откуда собеседница", answer: "Aj mňa teší. Odkiaľ ste?", options: ["Aj mňa teší. Odkiaľ ste?", "Aj mňa teší. Odkiaľ si?"] },
      { prompt: "4 · ответить и предложить ty", answer: "Som z Bratislavy. Môžeme si tykať?", options: ["Som z Bratislavy. Môžeme si tykať?", "Som z Bratislavy. Máte čas?"] },
      { prompt: "5 · согласиться и перейти на ty", answer: "Áno, rada. Ahoj, Ari!", options: ["Áno, rada. Ahoj, Ari!", "Nie. Dovidenia!"] },
    ], hint: "Начните с vy; на ty переходите только после явного предложения и согласия.", explanation: "Диалог начинается вежливо и меняет обращение после Môžeme si tykať? — Áno, rada." },
  ],
  chatPrompt: "Разыграйте знакомство со взрослым коллегой: начните с vy, задайте один вопрос, предложите перейти на ty и после согласия продолжите неофициально.",
  chatSuggestions: ["Dobrý deň, ako sa voláte?", "Odkiaľ ste?", "Môžeme si tykať?", "Áno, rada. Ahoj!"],
  knowledgeChecks: [
    { id: "m8-social-etiquette-check-1", question: "Как по-словацки вежливо: «Добрый день, как вы?»", options: ["Dobrý deň, ako sa máte?", "Ahoj, ako sa máš?", "Dobrý deň, ako sa máš?"], answer: "Dobrý deň, ako sa máte?", explanation: "Правильная вежливая модель: Dobrý deň, ako sa máte?" },
    { id: "m8-social-etiquette-check-2", question: "Как по-словацки неофициально: «Привет, как ты?»", options: ["Ahoj, ako sa máš?", "Dobrý deň, ako sa máte?", "Ahoj, ako sa máte?"], answer: "Ahoj, ako sa máš?", explanation: "Правильная неофициальная модель: Ahoj, ako sa máš?" },
  ],
  finalChecks: [
    { id: "m8-social-etiquette-final-1", question: "Выберите перевод «Пожалуйста, можете мне помочь?»", options: ["Prosím, môžete mi pomôcť?", "Prosím, môžeš mi pomôcť?", "Ďakujem, môžete mi pomôcť?"], answer: "Prosím, môžete mi pomôcť?", explanation: "Правильный ответ: Prosím, môžete mi pomôcť?" },
  ],
} satisfies CourseLesson;
