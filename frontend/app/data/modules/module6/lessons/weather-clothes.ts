import type { CourseLesson } from "../../../courseTypes";

const weatherOptions = ["slnečno", "zamračené", "teplo", "chladno", "veterno"];
const precipitationOptions = ["prší", "sneží", "fúka", "mrzne", "svieti"];
const clothingOptions = ["bundu", "kabát", "tričko", "čiapku", "topánky"];

export const weatherClothesLesson = {
  vocabulary: [
    {"word":"Dnes je slnečno a teplo.","translation":"Сегодня солнечно и тепло.","example":"Dnes je slnečno a teplo."},
    {"word":"Prší a fúka vietor.","translation":"Идёт дождь и дует ветер.","example":"Prší a fúka vietor."},
    {"word":"Je desať stupňov.","translation":"Десять градусов.","example":"Je desať stupňov."},
    {"word":"Mám na sebe modré nohavice.","translation":"На мне синие брюки.","example":"Mám na sebe modré nohavice."},
    {"word":"Keď sneží, oblečiem si bundu a čiapku.","translation":"Когда идёт снег, я надену куртку и шапку.","example":"Keď sneží, oblečiem si bundu a čiapku."},
    {"word":"Je mi zima, preto potrebujem kabát.","translation":"Мне холодно, поэтому мне нужно пальто.","example":"Je mi zima, preto potrebujem kabát."},
  ],
  slug: "weather-clothes",
  order: 14,
  title: "Погода и одежда",
  slovakTitle: "Počasie a oblečenie",
  description: "Понимайте простой прогноз и выбирайте одежду по погоде.",
  duration: "35–40 мин",
  goals: [
    "Спрашивать о погоде и описывать её короткими фразами",
    "Понимать дождь, снег, ветер и простую температуру",
    "Называть основную одежду и говорить, что на вас надето",
    "Связывать погоду с подходящей одеждой",
    "Понимать короткий прогноз и избегать частых ошибок",
  ],
  theory: {
    summary: "На уровне A1 достаточно понять, какая сегодня или завтра погода, назвать температуру и сказать, какая одежда нужна. Используйте готовые безличные модели Je... / Prší. / Sneží. и короткие фразы с mám na sebe, oblečiem si и potrebujem.",
    rules: [
      "Вопрос о погоде: Aké je dnes počasie? Ответ: Je slnečno, zamračené, teplo, chladno или veterno.",
      "Осадки и ветер называют короткими предложениями: Prší. Sneží. Fúka vietor. О температуре: Je dvadsať stupňov.",
      "О том, что надето сейчас: Mám na sebe bundu a nohavice. О выборе одежды: Oblečiem si kabát.",
      "Связь с погодой: Keď prší, potrebujem dáždnik. Keď je zima, nosím teplý kabát.",
      "Je zima значит «холодно», а Je mi zima — «мне холодно». Не используйте Som zima.",
    ],
    examples: [
      { slovak: "Dnes je slnečno a teplo.", russian: "Сегодня солнечно и тепло.", explanation: "Два признака погоды соединяются союзом a." },
      { slovak: "Prší a fúka vietor.", russian: "Идёт дождь и дует ветер.", explanation: "Осадки и ветер описываются отдельными глаголами." },
      { slovak: "Je desať stupňov.", russian: "Десять градусов.", explanation: "Температуру называют через je + число + stupňov." },
      { slovak: "Mám na sebe modré nohavice.", russian: "На мне синие брюки.", explanation: "Mám na sebe сообщает, что надето сейчас." },
      { slovak: "Keď sneží, oblečiem si bundu a čiapku.", russian: "Когда идёт снег, я надену куртку и шапку.", explanation: "После oblečiem si называются выбранные предметы одежды." },
      { slovak: "Je mi zima, preto potrebujem kabát.", russian: "Мне холодно, поэтому мне нужно пальто.", explanation: "Je mi zima описывает ощущение человека." },
    ],
  },
  sections: [
    {
      title: "Какая сегодня погода",
      paragraphs: ["Спросите Aké je dnes počasie? В ответе обычно достаточно одной-двух характеристик после je.", "Слова slnečno, zamračené, teplo, chladno и veterno не изменяются по роду говорящего."],
      table: { headers: ["Погода", "Фраза", "Перевод"], rows: [
        ["slnko", "Je slnečno.", "Солнечно."], ["oblaky", "Je zamračené.", "Облачно."],
        ["teplo", "Je teplo.", "Тепло."], ["chlad", "Je chladno.", "Прохладно / холодно."], ["vietor", "Je veterno.", "Ветрено."],
      ] },
      items: ["Aké je dnes počasie? — Какая сегодня погода?", "Dnes je pekne. — Сегодня хорошая погода.", "Je slnečno, ale chladno. — Солнечно, но холодно."],
      note: "Je chladno описывает погоду; Je mi zima описывает ваше ощущение.",
    },
    {
      title: "Дождь, снег, ветер и температура",
      paragraphs: ["Для дождя и снега используйте глагол без подлежащего: Prší. Sneží. С ветром говорят Fúka vietor.", "Температуру спросите Koľko je stupňov? и назовите числом: Je päť stupňov. Je mínus päť stupňov."],
      table: { headers: ["Явление", "Фраза", "Перевод"], rows: [
        ["dážď", "Prší.", "Идёт дождь."], ["sneh", "Sneží.", "Идёт снег."],
        ["vietor", "Fúka vietor.", "Дует ветер."], ["mráz", "Mrzne.", "Мороз / подмораживает."],
        ["teplota", "Je dvadsať stupňov.", "Двадцать градусов."],
      ] },
      items: ["Koľko je stupňov? — Сколько градусов?", "Slnko svieti. — Светит солнце.", "Zajtra bude pršať. — Завтра будет дождь."],
      note: "После чисел от пяти в учебной модели используйте stupňov: päť stupňov, desať stupňov.",
    },
    {
      title: "Основная одежда",
      paragraphs: ["Запоминайте одежду сразу в короткой фразе. Так видна форма после mám na sebe или oblečiem si.", "Обувь topánky и брюки nohavice обычно употребляются во множественном числе."],
      table: { headers: ["Предмет", "Фраза", "Перевод"], rows: [
        ["bunda", "Mám na sebe bundu.", "На мне куртка."], ["kabát", "Oblečiem si kabát.", "Я надену пальто."],
        ["tričko", "Nosím tričko.", "Я ношу футболку."], ["nohavice", "Mám na sebe nohavice.", "На мне брюки."],
        ["čiapka", "Oblečiem si čiapku.", "Я надену шапку."], ["topánky", "Mám nové topánky.", "У меня новые туфли / ботинки."],
      ] },
      items: ["sveter — свитер", "šál — шарф", "šaty — платье", "sukňa — юбка", "dáždnik — зонт"],
      note: "Mám na sebe — уже надето; oblečiem si — я надену / выберу сейчас.",
    },
    {
      title: "Что надеть по погоде",
      paragraphs: ["Свяжите знакомое условие с практическим выбором через Keď...: Keď prší, potrebujem dáždnik.", "Для регулярной привычки используйте nosím, для конкретного выбора — oblečiem si или vezmem si."],
      table: { headers: ["Погода", "Выбор", "Перевод"], rows: [
        ["Keď prší,", "potrebujem dáždnik.", "Когда идёт дождь, мне нужен зонт."], ["Keď sneží,", "oblečiem si bundu.", "Когда идёт снег, я надену куртку."],
        ["Keď je zima,", "nosím teplý kabát.", "Когда холодно, я ношу тёплое пальто."], ["Keď je slnečno,", "vezmem si okuliare.", "Когда солнечно, я возьму очки."],
        ["Keď je teplo,", "nosím tričko.", "Когда тепло, я ношу футболку."],
      ] },
      items: ["Vezmi si dáždnik. — Возьми зонт.", "Obleč si bundu. — Надень куртку.", "Potrebujem teplé topánky. — Мне нужны тёплые ботинки."],
      note: "После keď в этих моделях стоит обычная форма: keď prší, keď sneží, keď je teplo.",
    },
    {
      title: "Прогноз, план и частые ошибки",
      paragraphs: ["В коротком прогнозе сначала найдите время dnes/zajtra, затем погоду и температуру. После этого выберите одежду.", "Проверяйте безличную модель, форму одежды после глагола и диакритику: prší, sneží, dáždnik, čiapku."],
      table: { headers: ["Ошибка", "Правильно", "Почему"], rows: [
        ["Dnes je prší.", "Dnes prší.", "С prší глагол je не нужен."], ["Som zima.", "Je mi zima.", "Ощущение холода передаёт je mi."],
        ["Oblečiem si bunda.", "Oblečiem si bundu.", "После oblečiem si нужна форма bundu."], ["Potrebujem dáždník.", "Potrebujem dáždnik.", "В слове dáždnik нет долготы над i."],
        ["Zajtra je pršať.", "Zajtra bude pršať.", "Простой прогноз на завтра: bude + инфинитив."],
      ] },
      items: ["Zajtra bude chladno a bude pršať.", "Bude desať stupňov.", "Vezmem si bundu a dáždnik."],
      note: "Для A1 достаточно понять и составить прогноз из двух-трёх коротких предложений.",
    },
  ],
  stepPractices: [
    { id: "m6-weather-clothes-step-1", sectionIndex: 0, type: "pairs", prompt: "Выберите описание погоды.", answer: "slnečno; zamračené; teplo; chladno; veterno", pairs: [
      { prompt: "Je ___. · солнечно", answer: "slnečno", options: weatherOptions }, { prompt: "Je ___. · облачно", answer: "zamračené", options: weatherOptions },
      { prompt: "Je ___. · тепло", answer: "teplo", options: weatherOptions }, { prompt: "Je ___. · холодно", answer: "chladno", options: weatherOptions },
      { prompt: "Je ___. · ветрено", answer: "veterno", options: weatherOptions },
    ], hint: "Все ответы стоят после Je.", explanation: "Пять неизменяемых слов кратко описывают погоду." },
    { id: "m6-weather-clothes-step-2", sectionIndex: 1, type: "pairs", prompt: "Выберите глагол погодного явления.", answer: "prší; sneží; fúka; mrzne; svieti", pairs: [
      { prompt: "___ . · идёт дождь", answer: "prší", options: precipitationOptions }, { prompt: "___ . · идёт снег", answer: "sneží", options: precipitationOptions },
      { prompt: "___ vietor. · дует", answer: "fúka", options: precipitationOptions }, { prompt: "___ . · морозит", answer: "mrzne", options: precipitationOptions },
      { prompt: "Slnko ___. · светит", answer: "svieti", options: precipitationOptions },
    ], hint: "Сопоставьте явление с глаголом.", explanation: "Prší и sneží употребляются без подлежащего; vietor и slnko названы отдельно." },
    { id: "m6-weather-clothes-step-3", sectionIndex: 2, type: "pairs", prompt: "Выберите предмет одежды в нужной форме.", answer: "bundu; kabát; tričko; čiapku; topánky", pairs: [
      { prompt: "Mám na sebe ___. · куртку", answer: "bundu", options: clothingOptions }, { prompt: "Oblečiem si ___. · пальто", answer: "kabát", options: clothingOptions },
      { prompt: "Nosím ___. · футболку", answer: "tričko", options: clothingOptions }, { prompt: "Oblečiem si ___. · шапку", answer: "čiapku", options: clothingOptions },
      { prompt: "Mám nové ___. · ботинки", answer: "topánky", options: clothingOptions },
    ], hint: "Учитывайте и предмет, и форму после глагола.", explanation: "Задание закрепляет частотную одежду в готовых фразах." },
    { id: "m6-weather-clothes-step-4", sectionIndex: 3, type: "pairs", prompt: "Подберите одежду или предмет к погоде.", answer: "dáždnik; bundu; kabát; okuliare; tričko", pairs: [
      { prompt: "Keď prší, potrebujem ___.", answer: "dáždnik", options: ["dáždnik", "čiapku", "tričko", "sandále", "šaty"] },
      { prompt: "Keď sneží, oblečiem si ___.", answer: "bundu", options: ["bundu", "plavky", "tričko", "sukňu", "sandále"] },
      { prompt: "Keď je zima, nosím teplý ___.", answer: "kabát", options: ["kabát", "dáždnik", "okuliare", "tričko", "šaty"] },
      { prompt: "Keď je slnečno, vezmem si ___.", answer: "okuliare", options: ["okuliare", "kabát", "šál", "rukavice", "čiapku"] },
      { prompt: "Keď je teplo, nosím ___.", answer: "tričko", options: ["tričko", "kabát", "šál", "rukavice", "čiapku"] },
    ], hint: "Выберите самый естественный вариант для указанной погоды.", explanation: "Модель keď связывает погодную ситуацию с практическим выбором." },
    { id: "m6-weather-clothes-step-5", sectionIndex: 4, type: "pairs", prompt: "Исправьте каждую фразу.", answer: "Dnes prší.; Je mi zima.; Oblečiem si bundu.; Potrebujem dáždnik.; Zajtra bude pršať.", pairs: [
      { prompt: "Dnes je prší.", answer: "Dnes prší.", inputHint: "Введите исправленную фразу" }, { prompt: "Som zima.", answer: "Je mi zima.", inputHint: "Введите исправленную фразу" },
      { prompt: "Oblečiem si bunda.", answer: "Oblečiem si bundu.", inputHint: "Введите исправленную фразу" }, { prompt: "Potrebujem dáždník.", answer: "Potrebujem dáždnik.", inputHint: "Введите исправленную фразу" },
      { prompt: "Zajtra je pršať.", answer: "Zajtra bude pršať.", inputHint: "Введите исправленную фразу" },
    ], hint: "Проверьте je, je mi, форму bundu, слово dáždnik и модель bude + инфинитив.", explanation: "Исправления закрепляют пять основных моделей урока." },
  ],
  assessmentMode: "interactive",
  materialAssessmentStep: false,
  reinforcementLabel: "Финальный тест темы",
  reinforcementTitle: "Выполните шесть заданий темы 14",
  reinforcementPractices: [
    { id: "reinforcement:weather-clothes:1", sectionIndex: 0, type: "pairs", prompt: "Опишите погоду одним словом после je.", answer: "slnečno; zamračené; teplo; chladno; veterno", pairs: [
      { prompt: "солнечно", answer: "slnečno", options: weatherOptions }, { prompt: "облачно", answer: "zamračené", options: weatherOptions },
      { prompt: "тепло", answer: "teplo", options: weatherOptions }, { prompt: "холодно", answer: "chladno", options: weatherOptions }, { prompt: "ветрено", answer: "veterno", options: weatherOptions },
    ], hint: "Каждый ответ можно поставить после Je.", explanation: "Задание проверяет пять основных характеристик погоды." },
    { id: "reinforcement:weather-clothes:2", sectionIndex: 1, type: "pairs", prompt: "Выберите погодное явление.", answer: "prší; sneží; fúka; mrzne; svieti", pairs: [
      { prompt: "идёт дождь", answer: "prší", options: precipitationOptions }, { prompt: "идёт снег", answer: "sneží", options: precipitationOptions },
      { prompt: "дует ветер", answer: "fúka", options: precipitationOptions }, { prompt: "морозит", answer: "mrzne", options: precipitationOptions }, { prompt: "светит солнце", answer: "svieti", options: precipitationOptions },
    ], hint: "Выберите глагол по русскому значению.", explanation: "Глаголы описывают осадки, ветер, мороз и солнце." },
    { id: "reinforcement:weather-clothes:3", sectionIndex: 3, type: "pairs", prompt: "Выберите подходящий предмет по погоде.", answer: "dáždnik; bundu; kabát; okuliare; tričko", pairs: [
      { prompt: "Prší: potrebujem ___.", answer: "dáždnik", options: ["dáždnik", "bundu", "kabát", "okuliare", "tričko"] },
      { prompt: "Sneží: oblečiem si ___.", answer: "bundu", options: ["dáždnik", "bundu", "kabát", "okuliare", "tričko"] },
      { prompt: "Je zima: nosím teplý ___.", answer: "kabát", options: ["dáždnik", "bundu", "kabát", "okuliare", "tričko"] },
      { prompt: "Je slnečno: vezmem si ___.", answer: "okuliare", options: ["dáždnik", "bundu", "kabát", "okuliare", "tričko"] },
      { prompt: "Je teplo: nosím ___.", answer: "tričko", options: ["dáždnik", "bundu", "kabát", "okuliare", "tričko"] },
    ], hint: "Каждый вариант используется один раз.", explanation: "Погода определяет практический выбор одежды или предмета." },
    { id: "reinforcement:weather-clothes:4", sectionIndex: 4, type: "pairs", prompt: "Исправьте ошибки в прогнозе и выборе одежды.", answer: "Dnes prší.; Je mi zima.; Oblečiem si bundu.; Potrebujem dáždnik.; Zajtra bude pršať.", pairs: [
      { prompt: "Dnes je prší.", answer: "Dnes prší.", inputHint: "Введите исправленную фразу" }, { prompt: "Som zima.", answer: "Je mi zima.", inputHint: "Введите исправленную фразу" },
      { prompt: "Oblečiem si bunda.", answer: "Oblečiem si bundu.", inputHint: "Введите исправленную фразу" }, { prompt: "Potrebujem dáždník.", answer: "Potrebujem dáždnik.", inputHint: "Введите исправленную фразу" },
      { prompt: "Zajtra je pršať.", answer: "Zajtra bude pršať.", inputHint: "Введите исправленную фразу" },
    ], hint: "Перепишите всю строку в нормативной форме.", explanation: "Задание различает погоду, ощущение человека, форму одежды и прогноз." },
    { id: "reinforcement:weather-clothes:5", sectionIndex: 4, type: "pairs", prompt: "Переведите на словацкий.", answer: "Dnes je slnečno a teplo.; Prší a fúka vietor.; Je desať stupňov.; Mám na sebe modré nohavice.; Je mi zima, preto potrebujem bundu.", pairs: [
      { prompt: "Сегодня солнечно и тепло.", answer: "Dnes je slnečno a teplo.", inputHint: "Введите перевод" },
      { prompt: "Идёт дождь и дует ветер.", answer: "Prší a fúka vietor.", inputHint: "Введите перевод" },
      { prompt: "Десять градусов.", answer: "Je desať stupňov.", acceptableAnswers: ["Je 10 stupňov."], inputHint: "Введите перевод" },
      { prompt: "На мне синие брюки.", answer: "Mám na sebe modré nohavice.", inputHint: "Введите перевод" },
      { prompt: "Мне холодно, поэтому мне нужна куртка.", answer: "Je mi zima, preto potrebujem bundu.", acceptableAnswers: ["Je mi zima, takže potrebujem bundu."], inputHint: "Введите перевод" },
    ], hint: "Используйте модели урока и сохраняйте словацкую диакритику.", explanation: "Переводы проверяют погоду, температуру, одежду и личное ощущение." },
    { id: "reinforcement:weather-clothes:6", sectionIndex: 4, type: "pairs", prompt: "Соберите короткий прогноз и решение.", answer: "Aké bude zajtra počasie?; Bude chladno.; Bude pršať a fúkať vietor.; Koľko bude stupňov?; Bude desať stupňov.; Vezmem si bundu a dáždnik.", pairs: [
      { prompt: "1 · вопрос", answer: "Aké bude zajtra počasie?", options: ["Aké bude zajtra počasie?", "Koľko je oblečenie?", "Kde bude bunda?"] },
      { prompt: "2 · погода", answer: "Bude chladno.", options: ["Bude chladno.", "Budem chladno.", "Bude chladný."] },
      { prompt: "3 · явления", answer: "Bude pršať a fúkať vietor.", options: ["Bude pršať a fúkať vietor.", "Bude prší a fúka vietor.", "Je pršať a vietor."] },
      { prompt: "4 · температура", answer: "Koľko bude stupňov?", options: ["Koľko bude stupňov?", "Aký bude stupne?", "Kde bude teplota?"] },
      { prompt: "5 · ответ", answer: "Bude desať stupňov.", options: ["Bude desať stupňov.", "Budem desať stupeň.", "Je desať stupňa."] },
      { prompt: "6 · решение", answer: "Vezmem si bundu a dáždnik.", options: ["Vezmem si bundu a dáždnik.", "Mám bundu prší.", "Som si bunda a dáždnik."] },
    ], hint: "Следуйте порядку: вопрос, прогноз, температура, выбор одежды.", explanation: "Диалог соединяет понимание прогноза с простым практическим решением." },
  ],
  knowledgeChecks: [
    { id: "m6-weather-clothes-check-1", question: "Как сказать «Сегодня идёт дождь»?", options: ["Dnes prší.", "Dnes je prší.", "Dnes pršať."], answer: "Dnes prší.", explanation: "Prší — самостоятельный безличный глагол; je не нужен." },
    { id: "m6-weather-clothes-check-2", question: "Как сказать «На мне куртка»?", options: ["Mám na sebe bundu.", "Som na sebe bunda.", "Mám na seba bunda."], answer: "Mám na sebe bundu.", explanation: "Используйте mám na sebe + форму bundu." },
    { id: "m6-weather-clothes-check-3", question: "Как правильно сказать «Мне холодно»?", options: ["Je mi zima.", "Som zima.", "Mám zima."], answer: "Je mi zima.", explanation: "Личное ощущение передаёт готовая модель je mi zima." },
  ],
  finalChecks: [
    { id: "m6-weather-clothes-final-1", question: "Переведите: «Холодно, поэтому мне нужна куртка».", options: ["Je zima, preto potrebujem bundu.", "Som zima, preto mám bunda.", "Je chladný, preto potrebujem bunda."], answer: "Je zima, preto potrebujem bundu.", explanation: "Погода — je zima; после potrebujem нужна форма bundu." },
  ],
  chatPrompt: "Опишите сегодняшнюю погоду, назовите температуру и скажите, что вы наденете или возьмёте.",
  chatSuggestions: ["Dnes je slnečno, ale chladno.", "Je desať stupňov.", "Oblečiem si bundu."],
} satisfies CourseLesson;
