import type { CourseLesson } from "../../../courseTypes";

export const irregularVerbsLesson = {
  vocabulary: [
    {"word":"Idem do obchodu.","translation":"Я иду в магазин.","example":"Idem do obchodu."},
    {"word":"Deti jedia polievku.","translation":"Дети едят суп.","example":"Deti jedia polievku."},
    {"word":"Pijete čaj alebo kávu?","translation":"Вы пьёте чай или кофе?","example":"Pijete čaj alebo kávu?"},
    {"word":"Chcem oddychovať.","translation":"Я хочу отдыхать.","example":"Chcem oddychovať."},
    {"word":"Viem hovoriť po slovensky.","translation":"Я умею говорить по-словацки.","example":"Viem hovoriť po slovensky."},
    {"word":"Dám si minerálku.","translation":"Я закажу минеральную воду.","example":"Dám si minerálku."},
  ],
  slug: "irregular-verbs",
  order: 2,
  title: "Частотные неправильные глаголы",
  slovakTitle: "Časté nepravidelné slovesá",
  description: "Используйте девять частотных особых глаголов для движения, еды, планов, возможности, обязанности и заказа.",
  duration: "40–45 мин",
  goals: ["Узнавать и использовать девять частотных особых глаголов", "Запоминать их по тройке infinitív — ja — oni", "Ставить инфинитив после chcieť, môcť, musieť и vedieť", "Различать viem и môžem, а также nemusím и nesmiem", "Говорить о планах и уверенно делать простой заказ"],
  theory: {
    summary: "У частотных особых глаголов основа меняется, поэтому форму нельзя надёжно угадать по инфинитиву. Учите тройку infinitív — ja — oni и сразу помещайте личную форму в короткую фразу.",
    rules: [
      "Опорные тройки движения и еды: ísť — idem — idú; jesť — jem — jedia; piť — pijem — pijú.",
      "Опорные тройки намерения и модальности: chcieť — chcem — chcú; môcť — môžem — môžu; musieť — musím — musia; vedieť — viem — vedia.",
      "Опорные тройки действия с предметом: dať — dám — dajú; brať — beriem — berú.",
      "После chcem, môžem, musím и viem второй глагол остаётся в инфинитиве: Chcem ísť. Musím pracovať. Viem variť.",
      "Viem означает знание или навык, môžem — возможность или разрешение. Nemusím значит «мне не нужно», nesmiem — «мне нельзя».",
      "Обычное отрицание присоединяется к личной форме: nejdem, nejem, nepijem, nechcem, nemôžem, neviem, nemusím; запрет выражается nesmiem.",
      "Dať — совершенный глагол; в форме dám он обычно называет предстоящее завершённое действие: Dám si čaj — «Я закажу чай».",
    ],
    examples: [
      { slovak: "Idem do obchodu.", russian: "Я иду в магазин.", explanation: "Ísť обозначает движение пешком или на транспорте; способ уточняет контекст." },
      { slovak: "Deti jedia polievku.", russian: "Дети едят суп.", explanation: "Jedia — особая форма для oni/ony." },
      { slovak: "Pijete čaj alebo kávu?", russian: "Вы пьёте чай или кофе?", explanation: "Pijete — форма для vy." },
      { slovak: "Chcem oddychovať.", russian: "Я хочу отдыхать.", explanation: "После chcem используется инфинитив." },
      { slovak: "Viem hovoriť po slovensky.", russian: "Я умею говорить по-словацки.", explanation: "Viem передаёт навык." },
      { slovak: "Dám si minerálku.", russian: "Я закажу минеральную воду.", explanation: "В кафе dať si — готовая модель заказа." },
    ],
  },
  sections: [
    {
      title: "Движение и еда: ísť, jesť, piť",
      paragraphs: ["У этих частотных глаголов основа меняется, поэтому форму учат целиком. Начните с тройки infinitív — ja — oni, затем сравните весь ряд."],
      table: { headers: ["Глагол", "ja", "ty", "on/ona", "my", "vy", "oni/ony"], rows: [
        ["ísť — идти, ехать", "idem", "ideš", "ide", "ideme", "idete", "idú"],
        ["jesť — есть", "jem", "ješ", "je", "jeme", "jete", "jedia"],
        ["piť — пить", "pijem", "piješ", "pije", "pijeme", "pijete", "pijú"],
      ] },
      items: ["Idem domov. — Я иду домой.", "Ideme do práce. — Мы идём / едем на работу.", "Jem polievku. — Я ем суп.", "Čo jete na raňajky? — Что вы едите на завтрак?", "Pijem vodu. — Я пью воду.", "Pijú kávu. — Они пьют кофе."],
      note: "Не переносите долготу из инфинитива механически: ísť — idem — idú; piť — pijem — pijú. Отрицание: nejdem, nejem, nepijem.",
    },
    {
      title: "Желание, возможность, обязанность и навык",
      paragraphs: ["Личную форму получает только первый глагол. Второй глагол отвечает на вопрос «что делать?» и остаётся в инфинитиве: Chcem ísť, не Chcem idem."],
      table: { headers: ["Глагол", "ja", "ty", "on/ona", "my", "vy", "oni/ony"], rows: [
        ["chcieť — хотеть", "chcem", "chceš", "chce", "chceme", "chcete", "chcú"],
        ["môcť — мочь", "môžem", "môžeš", "môže", "môžeme", "môžete", "môžu"],
        ["musieť — быть должным", "musím", "musíš", "musí", "musíme", "musíte", "musia"],
        ["vedieť — знать, уметь", "viem", "vieš", "vie", "vieme", "viete", "vedia"],
      ] },
      items: ["Chcem oddychovať. — Я хочу отдыхать.", "Môžem otvoriť okno? — Можно открыть окно?", "Musím pracovať. — Я должен работать.", "Viem variť. — Я умею готовить.", "Viem plávať. — Я умею плавать: навык есть.", "Môžem plávať. — Я могу плавать: есть возможность или разрешение.", "Nemusím ísť. — Мне не нужно идти.", "Nesmiem ísť. — Мне нельзя идти."],
      note: "Не путайте отсутствие обязанности и запрет: nemusím — не нужно, nesmiem — нельзя.",
    },
    {
      title: "Dať, brať и карта девяти глаголов",
      paragraphs: ["Dať и brať полезны в заказе, выборе и бытовых действиях. Запомните особые основы dám и beriem."],
      table: { headers: ["Группа", "Infinitív — ja — oni", "Опорная фраза"], rows: [
        ["движение", "ísť — idem — idú", "Idem domov."], ["еда", "jesť — jem — jedia", "Deti jedia polievku."],
        ["напитки", "piť — pijem — pijú", "Pijem vodu."], ["желание", "chcieť — chcem — chcú", "Chcem spať."],
        ["возможность", "môcť — môžem — môžu", "Môžem prísť."], ["обязанность", "musieť — musím — musia", "Musím ísť."],
        ["навык", "vedieť — viem — vedia", "Viem variť."], ["дать / заказать", "dať — dám — dajú", "Dám si čaj."],
        ["брать", "brať — beriem — berú", "Beriem si vodu."],
      ] },
      items: ["dať: dám — dáš — dá — dáme — dáte — dajú", "brať: beriem — berieš — berie — berieme — beriete — berú", "Dám si kávu. — Я возьму / закажу кофе.", "Čo si dáte? — Что будете заказывать?", "Beriem si vodu. — Я беру с собой воду.", "Berie lieky. — Он принимает лекарства.", "Berieme túto izbu. — Мы берём этот номер.", "Для способа передвижения проще: Idem autobusom."],
      note: "Dať — совершенный глагол: Dám si čaj естественно выражает предстоящий завершённый выбор.",
    },
    {
      title: "Готовые фразы для вашей речи",
      paragraphs: ["Назовите инфинитив выделенной личной формы, затем восстановите смысл фразы. Учите глагол вместе с ситуацией."],
      table: { headers: ["Ситуация", "Словацкий пример", "Перевод"], rows: [
        ["движение", "Idem do obchodu.", "Я иду в магазин."], ["движение", "Kam idú deti?", "Куда идут дети?"], ["движение", "Dnes nejdeme do práce.", "Сегодня мы не идём на работу."],
        ["еда", "Ráno jem chlieb.", "Утром я ем хлеб."], ["еда", "Deti jedia polievku.", "Дети едят суп."], ["напитки", "Pijete čaj alebo kávu?", "Вы пьёте чай или кофе?"],
        ["напитки", "Nepijem mlieko.", "Я не пью молоко."], ["желание", "Chcem oddychovať.", "Я хочу отдыхать."], ["желание", "Chcú cestovať.", "Они хотят путешествовать."],
        ["разрешение", "Môžem si sadnúť?", "Можно мне сесть?"], ["возможность", "Dnes nemôže prísť.", "Сегодня он не может прийти."], ["обязанность", "Musíme kúpiť lístok.", "Мы должны купить билет."],
        ["нет обязанности", "Zajtra nemusím vstávať skoro.", "Завтра мне не нужно рано вставать."], ["запрет", "Tu nesmieme fajčiť.", "Здесь нам нельзя курить."], ["навык", "Viem hovoriť po slovensky.", "Я умею говорить по-словацки."],
        ["знание", "Nevie, kde je stanica.", "Он не знает, где вокзал."], ["заказ", "Dám si minerálku.", "Я закажу минеральную воду."], ["заказ", "Čo si dáte na obed?", "Что вы закажете на обед?"],
        ["выбор", "Berieme túto izbu.", "Мы берём этот номер."], ["с собой", "Beriem si dáždnik.", "Я беру с собой зонт."],
      ] },
      items: ["В кафе: Čo si dáte? — Dám si polievku a čaj. — Chcete aj vodu? — Nie, ďakujem.", "О планах: Kam chceš ísť večer? — Chcem ísť do kina, ale musím pracovať. — Môžeme ísť zajtra."],
      note: "После chcem, môžem, musím и viem используйте инфинитив; вопрос и отрицание меняют только личную форму первого глагола.",
    },
    {
      title: "Частые ошибки и самопроверка",
      paragraphs: ["Проверьте особую основу, согласование с лицом, инфинитив после модального глагола и точный смысл отрицания."],
      table: { headers: ["Ошибка", "Правильно", "Почему"], rows: [
        ["Ja ídem domov.", "Ja idem domov.", "В форме idem нет долгого í."], ["Oni ide do práce.", "Oni idú do práce.", "Нужна форма oni."],
        ["Chcem idem domov.", "Chcem ísť domov.", "Второй глагол — инфинитив."], ["Nemusím = мне нельзя", "Nemusím = мне не нужно", "Запрет выражает nesmiem."],
        ["Dám kávu si.", "Dám si kávu.", "Короткое si стоит близко к глаголу."],
      ] },
      items: ["Форма согласуется с лицом?", "После chcieť / môcť / musieť / vedieť стоит инфинитив?", "Viem передаёт навык, а môžem — возможность?", "Nemusím означает отсутствие обязанности, а nesmiem — запрет?", "Si стоит рядом с dať или brať?"],
      note: "Произносите тройку и исправленную фразу целиком: ísť — idem — idú; Oni idú do práce.",
    },
  ],
  stepPractices: [
    { id: "m5-irregular-verbs-step-1", sectionIndex: 0, type: "pairs", prompt: "Выберите форму для каждого лица.", answer: "idem; jedia; pijete; nejdeme", pairs: [
      { prompt: "ja · ísť", answer: "idem", options: ["idem", "ide", "idú"] }, { prompt: "oni · jesť", answer: "jedia", options: ["jem", "je", "jedia"] },
      { prompt: "vy · piť", answer: "pijete", options: ["pijem", "pijete", "pijú"] }, { prompt: "my · neísť", answer: "nejdeme", options: ["nejdem", "nejdeme", "nejdú"] },
    ], hint: "Вспомните тройку и полный ряд нужного глагола.", explanation: "Правильно: ja idem, oni jedia, vy pijete, my nejdeme." },
    { id: "m5-irregular-verbs-step-2", sectionIndex: 1, type: "pairs", prompt: "Выберите точную модель для каждой ситуации.", answer: "Viem plávať.; Môžem si sadnúť?; Nemusím ísť.; Nesmiem vojsť.", pairs: [
      { prompt: "Я умею плавать.", answer: "Viem plávať.", options: ["Viem plávať.", "Môžem plávať."] }, { prompt: "Можно мне сесть?", answer: "Môžem si sadnúť?", options: ["Viem si sadnúť?", "Môžem si sadnúť?"] },
      { prompt: "Мне не нужно идти.", answer: "Nemusím ísť.", options: ["Nemusím ísť.", "Nesmiem ísť."] }, { prompt: "Мне нельзя войти.", answer: "Nesmiem vojsť.", options: ["Nemusím vojsť.", "Nesmiem vojsť."] },
    ], hint: "Различайте навык и возможность, отсутствие обязанности и запрет.", explanation: "Viem — умею; môžem — могу; nemusím — не нужно; nesmiem — нельзя." },
    { id: "m5-irregular-verbs-step-3", sectionIndex: 2, type: "pairs", prompt: "Сопоставьте глагол с опорной тройкой.", answer: "dám — dajú; beriem — berú; chcem — chcú; viem — vedia", pairs: [
      { prompt: "dať", answer: "dám — dajú", options: ["dám — dajú", "beriem — berú", "chcem — chcú"] }, { prompt: "brať", answer: "beriem — berú", options: ["dám — dajú", "beriem — berú", "chcem — chcú"] },
      { prompt: "chcieť", answer: "chcem — chcú", options: ["dám — dajú", "beriem — berú", "chcem — chcú"] }, { prompt: "vedieť", answer: "viem — vedia", options: ["viem — vedia", "môžem — môžu", "musím — musia"] },
    ], hint: "Выберите формы ja и oni одного глагола.", explanation: "Тройки: dať — dám — dajú; brať — beriem — berú; chcieť — chcem — chcú; vedieť — viem — vedia." },
    { id: "m5-irregular-verbs-step-4", sectionIndex: 3, type: "pairs", prompt: "Переведите готовые бытовые фразы.", answer: "Idem do obchodu.; Chcem oddychovať.; Musíme kúpiť lístok.; Dám si minerálku.", pairs: [
      { prompt: "Я иду в магазин.", answer: "Idem do obchodu.", inputHint: "Введите перевод" }, { prompt: "Я хочу отдыхать.", answer: "Chcem oddychovať.", inputHint: "Введите перевод" },
      { prompt: "Мы должны купить билет.", answer: "Musíme kúpiť lístok.", inputHint: "Введите перевод" }, { prompt: "Я закажу минеральную воду.", answer: "Dám si minerálku.", inputHint: "Введите перевод" },
    ], hint: "Воспроизведите особую личную форму и инфинитив, если он нужен.", explanation: "Каждая фраза использует глагол в частотной бытовой модели." },
    { id: "m5-irregular-verbs-step-5", sectionIndex: 4, type: "pairs", prompt: "Исправьте ошибки в целых фразах.", answer: "Ja idem domov.; Oni idú do práce.; Chcem ísť domov.; Nemusím ísť.; Dám si kávu.", pairs: [
      { prompt: "Ja ídem domov.", answer: "Ja idem domov.", acceptableAnswers: ["Idem domov."], inputHint: "Введите исправленную фразу" }, { prompt: "Oni ide do práce.", answer: "Oni idú do práce.", acceptableAnswers: ["Idú do práce."], inputHint: "Введите исправленную фразу" },
      { prompt: "Chcem idem domov.", answer: "Chcem ísť domov.", inputHint: "Введите исправленную фразу" }, { prompt: "Nemusím ísť. · значение: мне нельзя", answer: "Nemusím ísť.", inputHint: "Введите фразу со значением «мне не нужно идти»" },
      { prompt: "Dám kávu si.", answer: "Dám si kávu.", inputHint: "Введите исправленную фразу" },
    ], hint: "Проверьте долготу, лицо, инфинитив и положение si.", explanation: "Правильно: idem, idú, chcem ísť, nemusím ísť, dám si kávu." },
  ],
  assessmentMode: "interactive",
  materialAssessmentStep: false,
  reinforcementLabel: "Финальный тест темы",
  reinforcementTitle: "Выполните шесть заданий темы 2",
  reinforcementPractices: [
    { id: "reinforcement:irregular-verbs:1", sectionIndex: 0, type: "pairs", prompt: "Выберите правильную форму.", answer: "idem; pijú; chceš; môžeme; viete", pairs: [
      { prompt: "Ja (idem / ide) domov.", answer: "idem", options: ["idem", "ide"] }, { prompt: "Oni (pijú / pije) vodu.", answer: "pijú", options: ["pijú", "pije"] },
      { prompt: "Ty (chcem / chceš) spať.", answer: "chceš", options: ["chcem", "chceš"] }, { prompt: "My (môžeme / môžu) začať.", answer: "môžeme", options: ["môžeme", "môžu"] },
      { prompt: "Vy (viete / vedia) variť?", answer: "viete", options: ["viete", "vedia"] },
    ], hint: "Сопоставьте подлежащее с личной формой.", explanation: "Ответы: idem, pijú, chceš, môžeme, viete." },
    { id: "reinforcement:irregular-verbs:2", sectionIndex: 1, type: "pairs", prompt: "Поставьте глагол в нужную форму.", answer: "je; musíte; viem; idú; dáme", pairs: [
      { prompt: "Eva ___ polievku. · jesť", answer: "je", inputHint: "Введите форму" }, { prompt: "Vy ___ pracovať. · musieť", answer: "musíte", inputHint: "Введите форму" },
      { prompt: "Ja ___ hovoriť po slovensky. · vedieť", answer: "viem", inputHint: "Введите форму" }, { prompt: "Deti ___ domov. · ísť", answer: "idú", inputHint: "Введите форму" },
      { prompt: "My si ___ čaj. · dať", answer: "dáme", inputHint: "Введите форму" },
    ], hint: "Введите только личную форму глагола.", explanation: "Формы: Eva je, vy musíte, ja viem, deti idú, my si dáme." },
    { id: "reinforcement:irregular-verbs:3", sectionIndex: 1, type: "pairs", prompt: "Выберите точный смысл.", answer: "Viem plávať.; Môžem vojsť?; Nemusím ísť.; Nesmiem vojsť.", pairs: [
      { prompt: "Я умею плавать.", answer: "Viem plávať.", options: ["Viem plávať.", "Môžem plávať."] }, { prompt: "Можно мне войти?", answer: "Môžem vojsť?", options: ["Viem vojsť?", "Môžem vojsť?"] },
      { prompt: "Мне не нужно идти.", answer: "Nemusím ísť.", options: ["Nemusím ísť.", "Nesmiem ísť."] }, { prompt: "Мне нельзя войти.", answer: "Nesmiem vojsť.", options: ["Nemusím vojsť.", "Nesmiem vojsť."] },
    ], hint: "Сверьте навык, возможность, отсутствие обязанности и запрет.", explanation: "Viem — навык; môžem — возможность; nemusím — не нужно; nesmiem — нельзя." },
    { id: "reinforcement:irregular-verbs:4", sectionIndex: 4, type: "pairs", prompt: "Исправьте ошибки.", answer: "Oni jedia obed.; My chceme ísť domov.; Ja môžem prísť dnes.; Dám si kávu.; Ty piješ vodu.", pairs: [
      { prompt: "Oni jem obed.", answer: "Oni jedia obed.", acceptableAnswers: ["Jedia obed."], inputHint: "Введите исправленную фразу" }, { prompt: "My chce ísť domov.", answer: "My chceme ísť domov.", acceptableAnswers: ["Chceme ísť domov."], inputHint: "Введите исправленную фразу" },
      { prompt: "Ja môcť prísť dnes.", answer: "Ja môžem prísť dnes.", acceptableAnswers: ["Môžem prísť dnes."], inputHint: "Введите исправленную фразу" }, { prompt: "Dám kávu si.", answer: "Dám si kávu.", inputHint: "Введите исправленную фразу" },
      { prompt: "Ty pím vodu.", answer: "Ty piješ vodu.", acceptableAnswers: ["Piješ vodu."], inputHint: "Введите исправленную фразу" },
    ], hint: "Исправьте особую основу, лицо, инфинитив или положение si.", explanation: "Правильно: jedia, chceme ísť, môžem prísť, dám si, piješ." },
    { id: "reinforcement:irregular-verbs:5", sectionIndex: 3, type: "pairs", prompt: "Переведите на словацкий.", answer: "Chcem piť.; Musíme ísť.; Vieš variť?; Nemôžu prísť.; Dám si čaj.", pairs: [
      { prompt: "Я хочу пить.", answer: "Chcem piť.", inputHint: "Введите перевод" }, { prompt: "Мы должны идти.", answer: "Musíme ísť.", inputHint: "Введите перевод" },
      { prompt: "Ты умеешь готовить?", answer: "Vieš variť?", inputHint: "Введите перевод" }, { prompt: "Они не могут прийти.", answer: "Nemôžu prísť.", acceptableAnswers: ["Oni nemôžu prísť."], inputHint: "Введите перевод" },
      { prompt: "Я закажу чай.", answer: "Dám si čaj.", inputHint: "Введите перевод" },
    ], hint: "После первой личной формы оставьте второй глагол в инфинитиве.", explanation: "Фразы используют chcieť, musieť, vedieť, môcť и dať si." },
    { id: "reinforcement:irregular-verbs:6", sectionIndex: 3, type: "pairs", prompt: "Соберите мини-диалог о планах и заказе.", answer: "Kam chceš ísť večer?; Chcem ísť do kaviarne. A ty?; Dnes nemôžem. Musím pracovať.; Môžeme ísť zajtra.; Dobre. Dám si kávu.; A ja si dám čaj.", pairs: [
      { prompt: "1 · вопрос о плане", answer: "Kam chceš ísť večer?", options: ["Kam chceš ísť večer?", "Kam chcem ideš večer?", "Kam chce ísť večer?"] },
      { prompt: "2 · ответ и встречный вопрос", answer: "Chcem ísť do kaviarne. A ty?", options: ["Chcem idem do kaviarne. A ty?", "Chcem ísť do kaviarne. A ty?", "Chceš ísť do kaviarne. A ja?"] },
      { prompt: "3 · невозможность и обязанность", answer: "Dnes nemôžem. Musím pracovať.", options: ["Dnes neviem. Musím pracujem.", "Dnes nemôžem. Musím pracovať.", "Dnes nemusím. Môžem pracovať."] },
      { prompt: "4 · предложение на завтра", answer: "Môžeme ísť zajtra.", options: ["Môžu ísť zajtra.", "Môžeme ideme zajtra.", "Môžeme ísť zajtra."] },
      { prompt: "5 · заказ кофе", answer: "Dobre. Dám si kávu.", options: ["Dobre. Dám si kávu.", "Dobre. Dám kávu si.", "Dobre. Beriem káva."] },
      { prompt: "6 · заказ чая", answer: "A ja si dám čaj.", options: ["A ja si dám čaj.", "A ja dám čaj si.", "A ja dávam si čaj."] },
    ], hint: "Следите за лицом, инфинитивом после модального глагола и положением si.", explanation: "Диалог соединяет chcieť, môcť, musieť и dať si в шести связанных репликах." },
  ],
  knowledgeChecks: [
    { id: "m5-irregular-verbs-check-1", question: "Какая тройка для глагола ísť правильная?", options: ["ísť — idem — idú", "ísť — ídem — ídú", "ísť — isím — isia"], answer: "ísť — idem — idú", explanation: "Формы idem и idú нужно запомнить целиком." },
    { id: "m5-irregular-verbs-check-2", question: "Как сказать «Я умею плавать»?", options: ["Viem plávať.", "Môžem plávať.", "Musím plávať."], answer: "Viem plávať.", explanation: "Viem передаёт знание или навык." },
    { id: "m5-irregular-verbs-check-3", question: "Что означает Nemusím ísť?", options: ["Мне не нужно идти.", "Мне нельзя идти.", "Я не умею идти."], answer: "Мне не нужно идти.", explanation: "Nemusím — отсутствие обязанности; запрет выражает nesmiem." },
  ],
  finalChecks: [
    { id: "m5-irregular-verbs-final-1", question: "Выберите нормативную фразу «Они идут в школу».", options: ["Idú do školy.", "Ide do školy.", "Ídú do školy."], answer: "Idú do školy.", explanation: "Форма oni глагола ísť — idú без долгого í в начале." },
  ],
  chatPrompt: "Составьте короткий диалог о планах или заказе: используйте три глагола темы, один инфинитив после chcieť / môcť / musieť / vedieť, вопрос и отрицание.",
  chatSuggestions: ["Kam chceš ísť večer?", "Dnes nemôžem. Musím pracovať.", "Dám si kávu."],
} satisfies CourseLesson;
