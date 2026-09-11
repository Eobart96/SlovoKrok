import type { CourseLesson } from "../../../courseTypes";

const placeOptions = ["banka", "pošta", "lekáreň", "stanica", "námestie"];
const directionOptions = ["rovno", "vľavo", "vpravo", "cez", "pri"];

export const cityPlacesLesson = {
  vocabulary: [
    {"word":"Kde je najbližšia lekáreň?","translation":"Где ближайшая аптека?","example":"Kde je najbližšia lekáreň?"},
    {"word":"Ako sa dostanem na námestie?","translation":"Как мне добраться до площади?","example":"Ako sa dostanem na námestie?"},
    {"word":"Pošta je vedľa banky.","translation":"Почта рядом с банком.","example":"Pošta je vedľa banky."},
    {"word":"Choďte rovno a potom vľavo.","translation":"Идите прямо, затем налево.","example":"Choďte rovno a potom vľavo."},
    {"word":"Lekáreň je oproti banke.","translation":"Аптека находится напротив банка.","example":"Lekáreň je oproti banke."},
    {"word":"Je to asi päť minút pešo.","translation":"Это примерно пять минут пешком.","example":"Je to asi päť minút pešo."},
  ],
  slug: "city-places",
  order: 12,
  title: "Город и общественные места",
  slovakTitle: "Mesto a verejné miesta",
  description: "Находите городские места, спрашивайте дорогу и понимайте короткий маршрут.",
  duration: "35–40 мин",
  goals: [
    "Называть основные городские места",
    "Спрашивать Kde je...? и Ako sa dostanem...?",
    "Описывать положение через ориентир",
    "Понимать один–три шага короткого маршрута",
    "Проводить простой диалог о дороге",
  ],
  theory: {
    summary: "В незнакомом городе сначала назовите нужное место, затем спросите, где оно или как туда добраться. Ответ уровня A1 использует один понятный ориентир и несколько коротких команд.",
    rules: [
      "Городские места: banka, pošta, lekáreň, nemocnica, stanica, zastávka, námestie, park, obchod, múzeum.",
      "Местоположение спрашивает Kde je...?: Kde je najbližšia lekáreň? Направление спрашивает Ako sa dostanem...?: Ako sa dostanem na námestie?",
      "Согласуйте najbližší с местом: najbližšia lekáreň/pošta/stanica, najbližšie námestie/múzeum, najbližší obchod/park.",
      "Ориентир можно дать готовым блоком: vedľa banky, oproti banke, pri stanici, za hotelom, pred múzeom.",
      "Короткий вежливый маршрут: Choďte rovno. Odbočte vľavo/vpravo. Prejdite cez ulicu. Место назначения: na námestie, na stanicu, do lekárne.",
      "Завершите разговор проверкой или благодарностью: Je to ďaleko? / Ďakujem pekne. — Nemáte za čo.",
    ],
    examples: [
      { slovak: "Kde je najbližšia lekáreň?", russian: "Где ближайшая аптека?", explanation: "Najbližšia согласовано с lekáreň." },
      { slovak: "Ako sa dostanem na námestie?", russian: "Как мне добраться до площади?", explanation: "Na námestie отвечает на направление Kam?" },
      { slovak: "Pošta je vedľa banky.", russian: "Почта рядом с банком.", explanation: "Vedľa banky задаёт ориентир." },
      { slovak: "Choďte rovno a potom vľavo.", russian: "Идите прямо, затем налево.", explanation: "Две короткие команды образуют простой маршрут." },
      { slovak: "Lekáreň je oproti banke.", russian: "Аптека находится напротив банка.", explanation: "Oproti banke — готовая модель ориентира." },
      { slovak: "Je to asi päť minút pešo.", russian: "Это примерно пять минут пешком.", explanation: "Фраза сообщает простое расстояние." },
    ],
  },
  sections: [
    {
      title: "Места в городе",
      paragraphs: ["Запомните небольшой практический набор мест, которые часто нужны в городе. Сначала узнавайте их в вывеске или вопросе.", "Род слова помогает согласовать najbližší: tá lekáreň — najbližšia lekáreň, to námestie — najbližšie námestie."],
      table: { headers: ["Место", "Род", "Перевод"], rows: [
        ["banka", "tá", "банк"], ["pošta", "tá", "почта"], ["lekáreň", "tá", "аптека"], ["nemocnica", "tá", "больница"],
        ["stanica", "tá", "вокзал / станция"], ["zastávka", "tá", "остановка"], ["námestie", "to", "площадь"], ["múzeum", "to", "музей"], ["park", "ten", "парк"],
      ] },
      items: ["obchod — магазин", "reštaurácia — ресторан", "hotel — отель", "kino — кинотеатр"],
      note: "Согласуйте прилагательное с местом: najbližšia lekáreň, najbližšie námestie.",
    },
    {
      title: "Где находится и как добраться",
      paragraphs: ["Kde je...? просит назвать положение места. Ako sa dostanem...? просит объяснить путь к нему.", "После dostanem используйте уже знакомое направление: na námestie/stanicu/poštu, do banky/lekárne/nemocnice."],
      table: { headers: ["Цель", "Вопрос", "Перевод"], rows: [
        ["найти аптеку", "Kde je najbližšia lekáreň?", "Где ближайшая аптека?"], ["найти вокзал", "Kde je stanica?", "Где вокзал?"],
        ["путь на площадь", "Ako sa dostanem na námestie?", "Как добраться до площади?"], ["путь на почту", "Ako sa dostanem na poštu?", "Как добраться до почты?"],
        ["путь в больницу", "Ako sa dostanem do nemocnice?", "Как добраться до больницы?"],
      ] },
      items: ["Prosím vás, kde je...?", "Je to ďaleko?", "Môžem ísť pešo?"],
      note: "Учите направление целиком: na stanicu, na poštu, na námestie; do lekárne, do banky.",
    },
    {
      title: "Ориентиры и положение",
      paragraphs: ["Если путь очень короткий, достаточно назвать положение относительно известного места.", "Форму после предлога учите в готовой паре: vedľa banky, oproti banke, pri stanici, za hotelom, pred múzeom."],
      table: { headers: ["Ориентир", "Пример", "Перевод"], rows: [
        ["vedľa", "Pošta je vedľa banky.", "Почта рядом с банком."], ["oproti", "Lekáreň je oproti banke.", "Аптека напротив банка."],
        ["pri", "Zastávka je pri stanici.", "Остановка у вокзала."], ["za", "Park je za hotelom.", "Парк за отелем."],
        ["pred", "Banka je pred múzeom.", "Банк перед музеем."],
      ] },
      items: ["Je to blízko.", "Je to ďaleko.", "Je to asi päť minút pešo."],
      note: "Не заменяйте форму ориентира словарной: vedľa banky, не vedľa banka.",
    },
    {
      title: "Короткий маршрут",
      paragraphs: ["Маршрут уровня A1 состоит из одного–трёх шагов. Сначала задайте общее направление, затем поворот или переход улицы.", "Используйте вежливые команды на vy: Choďte, Odbočte, Prejdite. Эти формы подходят незнакомому человеку."],
      table: { headers: ["Шаг", "Команда", "Перевод"], rows: [
        ["прямо", "Choďte rovno.", "Идите прямо."], ["налево", "Odbočte vľavo.", "Поверните налево."], ["направо", "Odbočte vpravo.", "Поверните направо."],
        ["через улицу", "Prejdite cez ulicu.", "Перейдите улицу."], ["ориентир", "Lekáreň je pri zastávke.", "Аптека у остановки."],
      ] },
      items: ["Choďte rovno a potom vľavo.", "Prejdite cez ulicu a odbočte vpravo.", "Je to naľavo."],
      note: "Rovno — прямо; vľavo — налево; vpravo — направо. Сохраняйте ľ в vľavo.",
    },
    {
      title: "Диалог о дороге и частые ошибки",
      paragraphs: ["Соберите разговор: вежливое обращение → вопрос → ориентир или маршрут → проверка расстояния → благодарность.", "Перед ответом проверьте Kde/Ako, согласование najbližší, направление na/do, форму ориентира и словацкую диакритику."],
      table: { headers: ["Ошибка", "Правильно", "Почему"], rows: [
        ["najbližší lekáreň", "najbližšia lekáreň", "Lekáreň — женского рода."], ["Ako sa dostanem v námestie?", "Ako sa dostanem na námestie?", "Направление — na námestie."],
        ["Pošta je vedľa banka.", "Pošta je vedľa banky.", "После vedľa нужна форма banky."], ["Choďte rovno a potom vlavo.", "Choďte rovno a potom vľavo.", "В vľavo нужна буква ľ."],
        ["Lekáreň je oproti banka.", "Lekáreň je oproti banke.", "Готовая модель — oproti banke."],
      ] },
      items: ["Prosím vás, kde je najbližšia lekáreň?", "Choďte rovno a potom vľavo.", "Je pri zastávke.", "Ďakujem pekne."],
      note: "Сложная навигация и длинные маршруты ограничиваются ключевыми ориентирами.",
    },
  ],
  stepPractices: [
    { id: "m6-city-places-step-1", sectionIndex: 0, type: "pairs", prompt: "Выберите городское место.", answer: "banka; pošta; lekáreň; stanica; námestie", pairs: [
      { prompt: "банк", answer: "banka", options: placeOptions }, { prompt: "почта", answer: "pošta", options: placeOptions }, { prompt: "аптека", answer: "lekáreň", options: placeOptions }, { prompt: "вокзал", answer: "stanica", options: placeOptions }, { prompt: "площадь", answer: "námestie", options: placeOptions },
    ], hint: "Сопоставьте русское название с вывеской.", explanation: "Пять слов — основные общественные места." },
    { id: "m6-city-places-step-2", sectionIndex: 1, type: "pairs", prompt: "Выберите нормативный вопрос.", answer: "Kde je najbližšia lekáreň?; Kde je stanica?; Ako sa dostanem na námestie?; Ako sa dostanem na poštu?; Ako sa dostanem do nemocnice?", pairs: [
      { prompt: "Где ближайшая аптека?", answer: "Kde je najbližšia lekáreň?", options: ["Kde je najbližšia lekáreň?", "Ako je lekáreň?", "Kde sú najbližší lekáreň?"] },
      { prompt: "Где вокзал?", answer: "Kde je stanica?", options: ["Kde je stanica?", "Kam stanica je?", "Ako stanica?"] },
      { prompt: "Как добраться до площади?", answer: "Ako sa dostanem na námestie?", options: ["Ako sa dostanem na námestie?", "Kde sa dostanem v námestie?", "Ako idem do námestie?"] },
      { prompt: "Как добраться до почты?", answer: "Ako sa dostanem na poštu?", options: ["Ako sa dostanem na poštu?", "Ako sa dostanem v pošta?", "Kde dostanem do poštu?"] },
      { prompt: "Как добраться до больницы?", answer: "Ako sa dostanem do nemocnice?", options: ["Ako sa dostanem do nemocnice?", "Ako sa dostanem na nemocnica?", "Kde idem v nemocnicu?"] },
    ], hint: "Kde ищет место; Ako sa dostanem просит маршрут.", explanation: "Направление различает na námestie/poštu и do nemocnice." },
    { id: "m6-city-places-step-3", sectionIndex: 2, type: "pairs", prompt: "Выберите ориентир.", answer: "vedľa; oproti; pri; za; pred", pairs: [
      { prompt: "Pošta je ___ banky.", answer: "vedľa", options: ["vedľa", "oproti", "pri", "za", "pred"] }, { prompt: "Lekáreň je ___ banke.", answer: "oproti", options: ["vedľa", "oproti", "pri", "za", "pred"] },
      { prompt: "Zastávka je ___ stanici.", answer: "pri", options: ["vedľa", "oproti", "pri", "za", "pred"] }, { prompt: "Park je ___ hotelom.", answer: "za", options: ["vedľa", "oproti", "pri", "za", "pred"] }, { prompt: "Banka je ___ múzeom.", answer: "pred", options: ["vedľa", "oproti", "pri", "za", "pred"] },
    ], hint: "Смотрите на готовую форму ориентира после пропуска.", explanation: "Положение выражают vedľa, oproti, pri, za и pred." },
    { id: "m6-city-places-step-4", sectionIndex: 3, type: "pairs", prompt: "Выберите слово маршрута.", answer: "rovno; vľavo; vpravo; cez; pri", pairs: [
      { prompt: "Choďte ___. · прямо", answer: "rovno", options: directionOptions }, { prompt: "Odbočte ___. · налево", answer: "vľavo", options: directionOptions }, { prompt: "Odbočte ___. · направо", answer: "vpravo", options: directionOptions }, { prompt: "Prejdite ___ ulicu. · через", answer: "cez", options: directionOptions }, { prompt: "Lekáreň je ___ zastávke. · у", answer: "pri", options: directionOptions },
    ], hint: "Различайте движение и последний ориентир.", explanation: "Rovno, vľavo, vpravo и cez задают путь; pri задаёт положение." },
    { id: "m6-city-places-step-5", sectionIndex: 4, type: "pairs", prompt: "Исправьте каждую фразу.", answer: "Kde je najbližšia lekáreň?; Ako sa dostanem na námestie?; Pošta je vedľa banky.; Choďte rovno a potom vľavo.; Lekáreň je oproti banke.", pairs: [
      { prompt: "Kde je najbližší lekáreň?", answer: "Kde je najbližšia lekáreň?", inputHint: "Введите исправленную фразу" }, { prompt: "Ako sa dostanem v námestie?", answer: "Ako sa dostanem na námestie?", inputHint: "Введите исправленную фразу" },
      { prompt: "Pošta je vedľa banka.", answer: "Pošta je vedľa banky.", inputHint: "Введите исправленную фразу" }, { prompt: "Choďte rovno a potom vlavo.", answer: "Choďte rovno a potom vľavo.", inputHint: "Введите исправленную фразу" },
      { prompt: "Переведите: «Аптека находится напротив банка».", answer: "Lekáreň je oproti banke.", inputHint: "Введите перевод" },
    ], hint: "Проверьте согласование, направление, ориентир и диакритику.", explanation: "Нормативны najbližšia, na námestie, vedľa banky, vľavo и oproti banke." },
  ],
  assessmentMode: "interactive",
  materialAssessmentStep: false,
  reinforcementLabel: "Финальный тест темы",
  reinforcementTitle: "Выполните шесть заданий темы 12",
  reinforcementPractices: [
    { id: "reinforcement:city-places:1", sectionIndex: 0, type: "pairs", prompt: "Выберите нужное городское место.", answer: "banka; pošta; lekáreň; stanica; námestie", pairs: [
      { prompt: "банк", answer: "banka", options: placeOptions }, { prompt: "почта", answer: "pošta", options: placeOptions }, { prompt: "аптека", answer: "lekáreň", options: placeOptions }, { prompt: "вокзал", answer: "stanica", options: placeOptions }, { prompt: "площадь", answer: "námestie", options: placeOptions },
    ], hint: "Выберите одно из пяти мест.", explanation: "Задание проверяет базовую городскую лексику." },
    { id: "reinforcement:city-places:2", sectionIndex: 0, type: "pairs", prompt: "Выберите форму najbližší.", answer: "najbližšia; najbližšie; najbližší; najbližšia; najbližšie", pairs: [
      { prompt: "___ lekáreň", answer: "najbližšia", options: ["najbližší", "najbližšia", "najbližšie"] }, { prompt: "___ námestie", answer: "najbližšie", options: ["najbližší", "najbližšia", "najbližšie"] },
      { prompt: "___ park", answer: "najbližší", options: ["najbližší", "najbližšia", "najbližšie"] }, { prompt: "___ stanica", answer: "najbližšia", options: ["najbližší", "najbližšia", "najbližšie"] }, { prompt: "___ múzeum", answer: "najbližšie", options: ["najbližší", "najbližšia", "najbližšie"] },
    ], hint: "Согласуйте форму с родом места.", explanation: "Мужской род — najbližší, женский — najbližšia, средний — najbližšie." },
    { id: "reinforcement:city-places:3", sectionIndex: 3, type: "pairs", prompt: "Выберите элемент маршрута.", answer: "rovno; vľavo; vpravo; cez; pri", pairs: [
      { prompt: "Choďte ___.", answer: "rovno", options: directionOptions }, { prompt: "Odbočte ___. · налево", answer: "vľavo", options: directionOptions }, { prompt: "Odbočte ___. · направо", answer: "vpravo", options: directionOptions }, { prompt: "Prejdite ___ ulicu.", answer: "cez", options: directionOptions }, { prompt: "Je ___ zastávke.", answer: "pri", options: directionOptions },
    ], hint: "Определите прямое движение, поворот, переход или ориентир.", explanation: "Пять элементов образуют короткий городской маршрут." },
    { id: "reinforcement:city-places:4", sectionIndex: 4, type: "pairs", prompt: "Исправьте ошибки в вопросах и маршруте.", answer: "Kde je najbližšia lekáreň?; Ako sa dostanem na námestie?; Pošta je vedľa banky.; Choďte rovno a potom vľavo.; Lekáreň je oproti banke.", pairs: [
      { prompt: "Kde je najbližší lekáreň?", answer: "Kde je najbližšia lekáreň?", inputHint: "Введите исправленную фразу" }, { prompt: "Ako sa dostanem v námestie?", answer: "Ako sa dostanem na námestie?", inputHint: "Введите исправленную фразу" },
      { prompt: "Pošta je vedľa banka.", answer: "Pošta je vedľa banky.", inputHint: "Введите исправленную фразу" }, { prompt: "Choďte rovno a potom vlavo.", answer: "Choďte rovno a potom vľavo.", inputHint: "Введите исправленную фразу" }, { prompt: "Lekáreň je oproti banka.", answer: "Lekáreň je oproti banke.", inputHint: "Введите исправленную фразу" },
    ], hint: "Исправьте всю строку: согласование, направление, форму ориентира или диакритику.", explanation: "Каждая строка проверяет отдельный элемент городской ситуации." },
    { id: "reinforcement:city-places:5", sectionIndex: 4, type: "pairs", prompt: "Переведите на словацкий.", answer: "Kde je najbližšia lekáreň?; Ako sa dostanem na námestie?; Pošta je vedľa banky.; Choďte rovno a potom vľavo.; Lekáreň je oproti banke.", pairs: [
      { prompt: "Где ближайшая аптека?", answer: "Kde je najbližšia lekáreň?", inputHint: "Введите перевод" }, { prompt: "Как мне добраться до площади?", answer: "Ako sa dostanem na námestie?", inputHint: "Введите перевод" },
      { prompt: "Почта рядом с банком.", answer: "Pošta je vedľa banky.", acceptableAnswers: ["Vedľa banky je pošta."], inputHint: "Введите перевод" },
      { prompt: "Идите прямо, затем налево.", answer: "Choďte rovno a potom vľavo.", acceptableAnswers: ["Choďte rovno, potom vľavo."], inputHint: "Введите перевод" },
      { prompt: "Аптека находится напротив банка.", answer: "Lekáreň je oproti banke.", acceptableAnswers: ["Oproti banke je lekáreň."], inputHint: "Введите перевод" },
    ], hint: "Используйте модели урока и сохраните словацкую диакритику.", explanation: "Переводы проверяют вопрос, направление, ориентир и маршрут." },
    { id: "reinforcement:city-places:6", sectionIndex: 4, type: "pairs", prompt: "Соберите диалог о дороге к аптеке.", answer: "Prosím vás, kde je najbližšia lekáreň?; Choďte rovno.; Potom odbočte vľavo.; Lekáreň je pri zastávke.; Je to ďaleko?; Nie, asi päť minút pešo.", pairs: [
      { prompt: "1 · вопрос", answer: "Prosím vás, kde je najbližšia lekáreň?", options: ["Prosím vás, kde je najbližšia lekáreň?", "Prosím, ako lekáreň je?", "Kde sú najbližší lekáreň?"] },
      { prompt: "2 · прямо", answer: "Choďte rovno.", options: ["Choďte rovno.", "Choďte v rovný.", "Ísť rovno."] }, { prompt: "3 · поворот", answer: "Potom odbočte vľavo.", options: ["Potom odbočte vľavo.", "Potom odbočiť vlavo.", "Potom choďte ľavý."] },
      { prompt: "4 · ориентир", answer: "Lekáreň je pri zastávke.", options: ["Lekáreň je pri zastávke.", "Lekáreň je pri zastávka.", "Lekáreň sú na zastávke."] },
      { prompt: "5 · расстояние", answer: "Je to ďaleko?", options: ["Je to ďaleko?", "Je ďaleký to?", "Ako ďaleko sú?"] }, { prompt: "6 · ответ", answer: "Nie, asi päť minút pešo.", options: ["Nie, asi päť minút pešo.", "Nie, asi päť minúta peší.", "Nie, pešo päť ďaleko."] },
    ], hint: "Следуйте маршруту: вопрос, прямо, поворот, ориентир, расстояние.", explanation: "Диалог остаётся коротким и даёт достаточно информации, чтобы найти место." },
  ],
  knowledgeChecks: [
    { id: "m6-city-places-check-1", question: "Как спросить «Где ближайшая аптека»?", options: ["Kde je najbližšia lekáreň?", "Kde je najbližší lekáreň?", "Ako sú lekáreň?"], answer: "Kde je najbližšia lekáreň?", explanation: "Najbližšia согласовано с lekáreň." },
    { id: "m6-city-places-check-2", question: "Как спросить дорогу до площади?", options: ["Ako sa dostanem na námestie?", "Kde sa dostanem v námestie?", "Ako idem do námestie?"], answer: "Ako sa dostanem na námestie?", explanation: "Направление к площади — na námestie." },
    { id: "m6-city-places-check-3", question: "Какая граница соответствует уровню A1?", options: ["Сложная навигация и длинные маршруты ограничиваются ключевыми ориентирами.", "Нужно объяснять маршрут через весь город.", "Нужно понимать любую транспортную схему."], answer: "Сложная навигация и длинные маршруты ограничиваются ключевыми ориентирами.", explanation: "На A1 достаточно одного ориентира и нескольких команд." },
  ],
  finalChecks: [
    { id: "m6-city-places-final-1", question: "Переведите: «Аптека находится напротив банка».", options: ["Lekáreň je oproti banke.", "Lekáreň je oproti banka.", "Lekáreň sú pred banky."], answer: "Lekáreň je oproti banke.", explanation: "Готовая модель ориентира — oproti banke." },
  ],
  chatPrompt: "Спросите дорогу к двум городским местам и дайте короткий маршрут с двумя ориентирами.",
  chatSuggestions: ["Kde je najbližšia lekáreň?", "Ako sa dostanem na námestie?", "Choďte rovno a potom vľavo."],
} satisfies CourseLesson;
