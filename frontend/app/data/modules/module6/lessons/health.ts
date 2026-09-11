import type { CourseLesson } from "../../../courseTypes";

const symptomOptions = ["teplotu", "kašeľ", "nádchu", "zimnicu", "alergiu"];
const bodyOptions = ["hlava", "hrdlo", "brucho", "chrbát", "zub"];
const adviceOptions = ["oddychujte", "pite", "choďte", "zostaňte", "zavolajte"];

export const healthLesson = {
  vocabulary: [
    {"word":"Bolí ma hlava.","translation":"У меня болит голова.","example":"Bolí ma hlava."},
    {"word":"Mám teplotu.","translation":"У меня температура.","example":"Mám teplotu."},
    {"word":"Je mi zle.","translation":"Мне плохо.","example":"Je mi zle."},
    {"word":"Musíte veľa piť a oddychovať.","translation":"Вам нужно много пить и отдыхать.","example":"Musíte veľa piť a oddychovať."},
    {"word":"Už dva dni ma bolí hrdlo.","translation":"У меня уже два дня болит горло.","example":"Už dva dni ma bolí hrdlo."},
    {"word":"Potrebujem lekára.","translation":"Мне нужен врач.","example":"Potrebujem lekára."},
  ],
  slug: "health",
  order: 13,
  title: "Здоровье и самочувствие",
  slovakTitle: "Zdravie",
  description: "Сообщайте о недомогании и понимайте простую рекомендацию.",
  duration: "35–40 мин",
  goals: [
    "Отвечать на вопрос о самочувствии",
    "Называть боль через Bolí ma...",
    "Сообщать частые симптомы и их длительность",
    "Просить врача или аптеку о помощи",
    "Понимать простые рекомендации и экстренную инструкцию",
  ],
  theory: {
    summary: "На уровне A1 важно понятно сообщить, как вы себя чувствуете, что болит и как давно. Затем нужно понять короткую рекомендацию или попросить профессиональную помощь; урок не учит ставить диагноз.",
    rules: [
      "Самочувствие: Ako sa cítite? — Cítim sa dobre/zle. Коротко о недомогании: Je mi zle. Som unavený/unavená.",
      "Боль в одной части тела: Bolí ma hlava/hrdlo/brucho/chrbát/zub. После Bolí ma называется то, что болит.",
      "Другие симптомы строятся через mám: Mám teplotu, kašeľ, nádchu, zimnicu, alergiu.",
      "Длительность можно сообщить готовыми блоками: od včera, od rána, už dva dni, tri dni.",
      "Просьба о помощи: Potrebujem lekára. Kde je lekáreň? Что делать: Čo mám robiť?",
      "Простая рекомендация: Oddychujte. Pite veľa vody. Choďte k lekárovi. При экстренной ситуации: Zavolajte 112. Эти фразы нужно понимать, а не использовать для самостоятельной диагностики.",
    ],
    examples: [
      { slovak: "Bolí ma hlava.", russian: "У меня болит голова.", explanation: "Готовая модель боли — Bolí ma + часть тела." },
      { slovak: "Mám teplotu.", russian: "У меня температура.", explanation: "Симптом сообщается через mám." },
      { slovak: "Je mi zle.", russian: "Мне плохо.", explanation: "Короткая общая фраза о самочувствии." },
      { slovak: "Musíte veľa piť a oddychovať.", russian: "Вам нужно много пить и отдыхать.", explanation: "Musíte + инфинитив передаёт рекомендацию специалиста." },
      { slovak: "Už dva dni ma bolí hrdlo.", russian: "У меня уже два дня болит горло.", explanation: "Už dva dni сообщает длительность." },
      { slovak: "Potrebujem lekára.", russian: "Мне нужен врач.", explanation: "Прямая просьба о профессиональной помощи." },
    ],
  },
  sections: [
    {
      title: "Как вы себя чувствуете",
      paragraphs: ["Врач или знакомый может спросить Ako sa cítite? Вежливая форма cítite подходит незнакомому взрослому.", "Ответьте общей фразой, а затем назовите конкретный симптом: Je mi zle. Mám teplotu."],
      table: { headers: ["Состояние", "Мужчина", "Женщина"], rows: [
        ["хорошо", "Cítim sa dobre.", "Cítim sa dobre."], ["плохо", "Cítim sa zle.", "Cítim sa zle."],
        ["устал(а)", "Som unavený.", "Som unavená."], ["мне плохо", "Je mi zle.", "Je mi zle."],
      ] },
      items: ["Ako sa máte?", "Necítim sa dobre.", "Je mi lepšie. — Мне лучше."],
      note: "Je mi zle — общая фраза. После неё полезно назвать конкретный симптом.",
    },
    {
      title: "Что болит: Bolí ma...",
      paragraphs: ["Для одной части тела используйте Bolí ma... и назовите её в форме из таблицы.", "Не начинайте с ja: в этой модели ma уже показывает, что болит у говорящего."],
      table: { headers: ["Часть тела", "Фраза", "Перевод"], rows: [
        ["hlava", "Bolí ma hlava.", "У меня болит голова."], ["hrdlo", "Bolí ma hrdlo.", "У меня болит горло."],
        ["brucho", "Bolí ma brucho.", "У меня болит живот."], ["chrbát", "Bolí ma chrbát.", "У меня болит спина."], ["zub", "Bolí ma zub.", "У меня болит зуб."],
      ] },
      items: ["Kde vás to bolí? — Где у вас болит?", "Veľmi ma bolí hlava. — У меня сильно болит голова."],
      note: "После bolí ma часть тела обычно стоит в Nominatív: Bolí ma hlava.",
    },
    {
      title: "Симптомы и длительность",
      paragraphs: ["Температуру, кашель, насморк и другие знакомые симптомы сообщайте через mám.", "Добавьте один короткий ответ о времени: od včera, od rána или už dva dni."],
      table: { headers: ["Симптом", "Пример", "Перевод"], rows: [
        ["teplota", "Mám teplotu.", "У меня температура."], ["kašeľ", "Mám kašeľ.", "У меня кашель."], ["nádcha", "Mám nádchu.", "У меня насморк."],
        ["zimnica", "Mám zimnicu.", "У меня озноб."], ["alergia", "Mám alergiu.", "У меня аллергия."],
        ["длительность", "Už dva dni ma bolí hrdlo.", "У меня уже два дня болит горло."],
      ] },
      items: ["Od včera. — Со вчерашнего дня.", "Od rána. — С утра.", "Už tri dni. — Уже три дня."],
      note: "Сообщайте только наблюдаемый симптом и длительность; не называйте себе диагноз.",
    },
    {
      title: "Помощь и простая рекомендация",
      paragraphs: ["Спросите Čo mám robiť? и слушайте ключевой глагол рекомендации. В аптеке можно сказать Prosím si niečo na bolesť hrdla, но выбор средства оставьте специалисту.", "При серьёзной или экстренной ситуации нужна профессиональная помощь. Короткая инструкция Zavolajte 112 означает «Позвоните 112»."],
      table: { headers: ["Функция", "Реплика", "Перевод"], rows: [
        ["попросить врача", "Potrebujem lekára.", "Мне нужен врач."], ["спросить", "Čo mám robiť?", "Что мне делать?"],
        ["отдых", "Oddychujte.", "Отдыхайте."], ["вода", "Pite veľa vody.", "Пейте много воды."],
        ["врач", "Choďte k lekárovi.", "Идите к врачу."], ["экстренно", "Zavolajte 112.", "Позвоните 112."],
      ] },
      items: ["Zostaňte doma. — Оставайтесь дома.", "Musíte oddychovať. — Вам нужно отдыхать.", "Rozumiem. Ďakujem."],
      note: "Учебные рекомендации — языковые модели, а не персональная медицинская консультация.",
    },
    {
      title: "Диалог с врачом и частые ошибки",
      paragraphs: ["Соберите разговор: общее состояние → один-два симптома → длительность → вопрос Čo mám robiť? → рекомендация.", "Перед ответом проверьте bolí ma, форму симптома после mám, диакритику и вежливую форму рекомендации."],
      table: { headers: ["Ошибка", "Правильно", "Почему"], rows: [
        ["Ja bolí hlava.", "Bolí ma hlava.", "Нужна готовая модель bolí ma."], ["Mám teplota.", "Mám teplotu.", "После mám используется форма teplotu."],
        ["Boli ma hrdlo.", "Bolí ma hrdlo.", "В bolí нужна долгота."], ["Pite veľa voda.", "Pite veľa vody.", "Готовая модель — veľa vody."],
        ["Musíte veľa pijete.", "Musíte veľa piť.", "После musíte нужен инфинитив."],
      ] },
      items: ["Je mi zle.", "Bolí ma hlava a mám teplotu.", "Od včera.", "Čo mám robiť?", "Musíte veľa piť a oddychovať."],
      note: "Урок не заменяет медицинскую помощь и не обучает диагностике.",
    },
  ],
  stepPractices: [
    { id: "m6-health-step-1", sectionIndex: 0, type: "pairs", prompt: "Выберите подходящую фразу о самочувствии.", answer: "Cítim sa dobre.; Cítim sa zle.; Som unavený.; Som unavená.; Je mi zle.", pairs: [
      { prompt: "Я чувствую себя хорошо.", answer: "Cítim sa dobre.", options: ["Cítim sa dobre.", "Cítim sa zle."] }, { prompt: "Я чувствую себя плохо.", answer: "Cítim sa zle.", options: ["Cítim sa dobre.", "Cítim sa zle."] },
      { prompt: "Я устал. (мужчина)", answer: "Som unavený.", options: ["Som unavený.", "Som unavená."] }, { prompt: "Я устала. (женщина)", answer: "Som unavená.", options: ["Som unavený.", "Som unavená."] },
      { prompt: "Мне плохо.", answer: "Je mi zle.", options: ["Je mi zle.", "Som mi zle."] },
    ], hint: "Учитывайте значение и пол только в форме unavený/unavená.", explanation: "Фразы сообщают общее состояние без диагноза." },
    { id: "m6-health-step-2", sectionIndex: 1, type: "pairs", prompt: "Выберите часть тела.", answer: "hlava; hrdlo; brucho; chrbát; zub", pairs: [
      { prompt: "Bolí ma ___. · голова", answer: "hlava", options: bodyOptions }, { prompt: "Bolí ma ___. · горло", answer: "hrdlo", options: bodyOptions }, { prompt: "Bolí ma ___. · живот", answer: "brucho", options: bodyOptions }, { prompt: "Bolí ma ___. · спина", answer: "chrbát", options: bodyOptions }, { prompt: "Bolí ma ___. · зуб", answer: "zub", options: bodyOptions },
    ], hint: "Дополните одну и ту же модель частью тела.", explanation: "Bolí ma + часть тела сообщает локализацию боли." },
    { id: "m6-health-step-3", sectionIndex: 2, type: "pairs", prompt: "Выберите симптом после mám.", answer: "teplotu; kašeľ; nádchu; zimnicu; alergiu", pairs: [
      { prompt: "Mám ___. · температуру", answer: "teplotu", options: symptomOptions }, { prompt: "Mám ___. · кашель", answer: "kašeľ", options: symptomOptions }, { prompt: "Mám ___. · насморк", answer: "nádchu", options: symptomOptions }, { prompt: "Mám ___. · озноб", answer: "zimnicu", options: symptomOptions }, { prompt: "Mám ___. · аллергию", answer: "alergiu", options: symptomOptions },
    ], hint: "Сопоставьте русский симптом с формой после mám.", explanation: "Формы teplotu, nádchu, zimnicu и alergiu уже стоят после mám." },
    { id: "m6-health-step-4", sectionIndex: 3, type: "pairs", prompt: "Выберите ключевой глагол рекомендации.", answer: "oddychujte; pite; choďte; zostaňte; zavolajte", pairs: [
      { prompt: "___ doma. · отдыхайте", answer: "oddychujte", options: adviceOptions }, { prompt: "___ veľa vody. · пейте", answer: "pite", options: adviceOptions }, { prompt: "___ k lekárovi. · идите", answer: "choďte", options: adviceOptions }, { prompt: "___ doma. · оставайтесь", answer: "zostaňte", options: adviceOptions }, { prompt: "___ 112. · позвоните", answer: "zavolajte", options: adviceOptions },
    ], hint: "Выберите действие по русской подсказке.", explanation: "Формы обращения на vy помогают понять рекомендацию или инструкцию." },
    { id: "m6-health-step-5", sectionIndex: 4, type: "pairs", prompt: "Исправьте каждую фразу.", answer: "Bolí ma hlava.; Mám teplotu.; Je mi zle.; Pite veľa vody.; Musíte veľa piť a oddychovať.", pairs: [
      { prompt: "Ja bolí hlava.", answer: "Bolí ma hlava.", inputHint: "Введите исправленную фразу" }, { prompt: "Mám teplota.", answer: "Mám teplotu.", inputHint: "Введите исправленную фразу" },
      { prompt: "Som mi zle.", answer: "Je mi zle.", inputHint: "Введите исправленную фразу" }, { prompt: "Pite veľa voda.", answer: "Pite veľa vody.", inputHint: "Введите исправленную фразу" },
      { prompt: "Musíte veľa pijete a oddychujete.", answer: "Musíte veľa piť a oddychovať.", inputHint: "Введите исправленную фразу" },
    ], hint: "Проверьте модель боли, mám, je mi, количество и инфинитивы.", explanation: "Нормативны bolí ma, mám teplotu, je mi zle, veľa vody и musíte + инфинитив." },
  ],
  assessmentMode: "interactive",
  materialAssessmentStep: false,
  reinforcementLabel: "Финальный тест темы",
  reinforcementTitle: "Выполните шесть заданий темы 13",
  reinforcementPractices: [
    { id: "reinforcement:health:1", sectionIndex: 1, type: "pairs", prompt: "Дополните модель боли.", answer: "hlava; hrdlo; brucho; chrbát; zub", pairs: [
      { prompt: "голова", answer: "hlava", options: bodyOptions }, { prompt: "горло", answer: "hrdlo", options: bodyOptions }, { prompt: "живот", answer: "brucho", options: bodyOptions }, { prompt: "спина", answer: "chrbát", options: bodyOptions }, { prompt: "зуб", answer: "zub", options: bodyOptions },
    ], hint: "Выберите часть тела после Bolí ma.", explanation: "Каждый ответ завершает модель боли." },
    { id: "reinforcement:health:2", sectionIndex: 2, type: "pairs", prompt: "Выберите симптом после mám.", answer: "teplotu; kašeľ; nádchu; zimnicu; alergiu", pairs: [
      { prompt: "температура", answer: "teplotu", options: symptomOptions }, { prompt: "кашель", answer: "kašeľ", options: symptomOptions }, { prompt: "насморк", answer: "nádchu", options: symptomOptions }, { prompt: "озноб", answer: "zimnicu", options: symptomOptions }, { prompt: "аллергия", answer: "alergiu", options: symptomOptions },
    ], hint: "Выберите форму, совместимую с mám.", explanation: "Задание проверяет пять наблюдаемых симптомов." },
    { id: "reinforcement:health:3", sectionIndex: 3, type: "pairs", prompt: "Выберите действие рекомендации.", answer: "oddychujte; pite; choďte; zostaňte; zavolajte", pairs: [
      { prompt: "___ doma. · отдыхайте", answer: "oddychujte", options: adviceOptions }, { prompt: "___ veľa vody.", answer: "pite", options: adviceOptions }, { prompt: "___ k lekárovi.", answer: "choďte", options: adviceOptions }, { prompt: "___ doma. · оставайтесь", answer: "zostaňte", options: adviceOptions }, { prompt: "___ 112.", answer: "zavolajte", options: adviceOptions },
    ], hint: "Определите отдых, питьё, визит, пребывание дома или звонок.", explanation: "Формы на vy передают вежливую рекомендацию или экстренную инструкцию." },
    { id: "reinforcement:health:4", sectionIndex: 4, type: "pairs", prompt: "Исправьте ошибки в сообщении о здоровье.", answer: "Bolí ma hlava.; Mám teplotu.; Je mi zle.; Pite veľa vody.; Musíte veľa piť.", pairs: [
      { prompt: "Ja bolí hlava.", answer: "Bolí ma hlava.", inputHint: "Введите исправленную фразу" }, { prompt: "Mám teplota.", answer: "Mám teplotu.", inputHint: "Введите исправленную фразу" }, { prompt: "Som mi zle.", answer: "Je mi zle.", inputHint: "Введите исправленную фразу" },
      { prompt: "Pite veľa voda.", answer: "Pite veľa vody.", inputHint: "Введите исправленную фразу" }, { prompt: "Musíte veľa pijete.", answer: "Musíte veľa piť.", inputHint: "Введите исправленную фразу" },
    ], hint: "Исправьте всю строку: модель, форму после mám, количество или инфинитив.", explanation: "Каждая строка проверяет одну частотную медицинскую реплику A1." },
    { id: "reinforcement:health:5", sectionIndex: 4, type: "pairs", prompt: "Переведите на словацкий.", answer: "Bolí ma hlava.; Mám teplotu.; Je mi zle.; Už dva dni ma bolí hrdlo.; Musíte veľa piť a oddychovať.", pairs: [
      { prompt: "У меня болит голова.", answer: "Bolí ma hlava.", acceptableAnswers: ["Hlava ma bolí."], inputHint: "Введите перевод" }, { prompt: "У меня температура.", answer: "Mám teplotu.", inputHint: "Введите перевод" },
      { prompt: "Мне плохо.", answer: "Je mi zle.", inputHint: "Введите перевод" }, { prompt: "У меня уже два дня болит горло.", answer: "Už dva dni ma bolí hrdlo.", acceptableAnswers: ["Hrdlo ma bolí už dva dni."], inputHint: "Введите перевод" },
      { prompt: "Вам нужно много пить и отдыхать.", answer: "Musíte veľa piť a oddychovať.", inputHint: "Введите перевод" },
    ], hint: "Используйте модели урока и сохраните словацкую диакритику.", explanation: "Переводы проверяют боль, симптом, состояние, длительность и рекомендацию." },
    { id: "reinforcement:health:6", sectionIndex: 4, type: "pairs", prompt: "Соберите короткий диалог с врачом.", answer: "Ako sa cítite?; Je mi zle.; Bolí ma hlava a mám teplotu.; Ako dlho?; Od včera.; Musíte veľa piť a oddychovať.", pairs: [
      { prompt: "1 · вопрос", answer: "Ako sa cítite?", options: ["Ako sa cítite?", "Kde sa cítite?", "Ako cítim vás?"] }, { prompt: "2 · состояние", answer: "Je mi zle.", options: ["Je mi zle.", "Som mi zle.", "Mám zlá."] },
      { prompt: "3 · симптомы", answer: "Bolí ma hlava a mám teplotu.", options: ["Bolí ma hlava a mám teplotu.", "Ja bolí hlava a mám teplota.", "Je hlava a teplotu."] }, { prompt: "4 · длительность", answer: "Ako dlho?", options: ["Ako dlho?", "Koľko ďaleko?", "Kedy miesto?"] },
      { prompt: "5 · ответ", answer: "Od včera.", options: ["Od včera.", "Do včera.", "Na včerajší."] }, { prompt: "6 · рекомендация", answer: "Musíte veľa piť a oddychovať.", options: ["Musíte veľa piť a oddychovať.", "Musíte veľa pijete a oddychujete.", "Máte piť veľa oddych."] },
    ], hint: "Следуйте маршруту: состояние, симптомы, длительность, рекомендация.", explanation: "Диалог передаёт врачу наблюдаемые факты и не ставит диагноз." },
  ],
  knowledgeChecks: [
    { id: "m6-health-check-1", question: "Как сказать «У меня болит голова»?", options: ["Bolí ma hlava.", "Ja bolí hlava.", "Mám bolí hlavu."], answer: "Bolí ma hlava.", explanation: "Используется готовая модель Bolí ma + часть тела." },
    { id: "m6-health-check-2", question: "Как сказать «У меня температура»?", options: ["Mám teplotu.", "Je mi teplota.", "Mám teplota."], answer: "Mám teplotu.", explanation: "Симптом сообщается через mám teplotu." },
    { id: "m6-health-check-3", question: "Какая граница соответствует уровню A1?", options: ["Урок не заменяет медицинскую помощь и не обучает диагностике.", "Ученик должен самостоятельно определять диагноз.", "Нужно выбирать лекарства без специалиста."], answer: "Урок не заменяет медицинскую помощь и не обучает диагностике.", explanation: "Цель — сообщить факты и понять рекомендацию." },
  ],
  finalChecks: [
    { id: "m6-health-final-1", question: "Переведите: «У меня болит голова».", options: ["Bolí ma hlava.", "Ja bolí hlava.", "Mám bolí hlavu."], answer: "Bolí ma hlava.", explanation: "Используйте готовую модель Bolí ma…" },
  ],
  chatPrompt: "Сообщите врачу два симптома, их длительность и спросите, что нужно делать.",
  chatSuggestions: ["Bolí ma hlava.", "Mám teplotu od včera.", "Čo mám robiť?"],
} satisfies CourseLesson;
