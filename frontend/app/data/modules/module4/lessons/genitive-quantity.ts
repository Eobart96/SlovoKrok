import type { CourseLesson } from "../../../courseTypes";
import { defineModule4Lesson } from "../lessonFactory";

const baseGenitiveQuantityLesson = defineModule4Lesson("genitive-quantity", 4, {
  summary: "После veľa, málo, trochu, koľko и единицы измерения существительное обычно стоит в Genitíve. Число зависит от того, говорим ли мы о веществе или считаем отдельные предметы и людей.",
  model: "Слово количества или мера + Genitív: veľa vody, päť kníh, kilo jabĺk.",
  goals: ["Задавать Koľko?", "Использовать veľa, málo и trochu", "Различать формы после 2–4 и 5–10", "Называть меры продуктов"],
  rules: [
    "Вещество или общий объём обычно требуют Genitív единственного числа: veľa vody, málo času, trochu kávy.",
    "Отдельные предметы и люди обычно требуют Genitív множественного числа: veľa kníh, málo študentov.",
    "После 2–4 с предметами используется обычное множественное число: dve knihy, tri mestá, štyri autá.",
    "После 5–10 нужна форма Genitívu множественного числа: päť kníh, šesť áut, desať eur.",
    "Мера управляет названием содержимого: liter vody, šálka kávy, fľaša vody, kilo jabĺk.",
    "Учите частотные формы целиком и сохраняйте диакритику: kníh, ľudí, detí, jabĺk, peňazí.",
  ],
  examples: [
    { slovak: "Mám veľa práce.", russian: "У меня много работы." },
    { slovak: "Chcem trochu kávy.", russian: "Я хочу немного кофе." },
    { slovak: "Mám dve knihy.", russian: "У меня две книги." },
    { slovak: "Kupujem kilo jabĺk.", russian: "Я покупаю килограмм яблок." },
    { slovak: "Mám desať eur.", russian: "У меня десять евро." },
  ],
  primaryTitle: "Формы Genitívu",
  primaryTable: { headers: ["Тип", "Nominatív", "Genitív", "Модель"], rows: [
    ["вещество", "voda / káva", "vody / kávy", "veľa vody / trochu kávy"],
    ["объём", "čas / práca", "času / práce", "málo času / veľa práce"],
    ["предметы", "knihy / otázky", "kníh / otázok", "veľa kníh / päť otázok"],
    ["люди", "ľudia / deti", "ľudí / detí", "málo ľudí / veľa detí"],
    ["особые", "eurá / jablká", "eur / jabĺk", "desať eur / kilo jabĺk"],
  ] },
  secondaryTitle: "Числа и меры количества",
  secondaryTable: { headers: ["Количество", "Модель", "Примеры"], rows: [
    ["2–4", "обычное множественное", "dve knihy / štyri autá"],
    ["5–10", "Genitív множественного", "päť kníh / šesť áut"],
    ["liter / pohár", "+ Genitív", "liter vody / pohár vody"],
    ["šálka / fľaša / kilo", "+ Genitív", "šálka kávy / fľaša vody / kilo jabĺk"],
  ] },
  boundaryItems: ["Nemám vodu — объект в Akuzatíve.", "Nemám veľa vody — Genitív после veľa.", "Dva litre vody — päť litrov vody: меняется мера, но не vody.", "Kupujem fľašu vody: fľašu в Akuzatíve, воды в Genitíve."],
  mistake: "Не используйте одну форму после любого числа: tri knihy, но päť kníh; desať eur, не desať eurá.",
  task: "Назовите пять количеств: со словом количества, числом 2–4, числом 5–10, мерой и вопросом Koľko?.",
  productionPrompt: "Переведите: «пять книг».",
  productionAnswer: "päť kníh",
  productionHint: "После päť нужна форма Genitívu множественного числа kníh.",
});

export const genitiveQuantityLesson = {
  vocabulary: [
    {"word":"Koľko máš času? — Mám málo času.","translation":"Сколько у тебя времени? — У меня мало времени.","example":"Koľko máš času? — Mám málo času."},
    {"word":"Koľko chceš vody? — Chcem trochu vody.","translation":"Сколько воды ты хочешь? — Я хочу немного воды.","example":"Koľko chceš vody? — Chcem trochu vody."},
    {"word":"Mám dve knihy, ale Peter má päť kníh.","translation":"У меня две книги, а у Петера пять книг.","example":"Mám dve knihy, ale Peter má päť kníh."},
    {"word":"Kupujem fľašu vody.","translation":"Я покупаю бутылку воды.","example":"Kupujem fľašu vody."},
    {"word":"Mám málo peňazí.","translation":"У меня мало денег.","example":"Mám málo peňazí."},
    {"word":"Kilo jabĺk, prosím.","translation":"Килограмм яблок, пожалуйста.","example":"Kilo jabĺk, prosím."},
  ],
  ...baseGenitiveQuantityLesson,
  description: "Спрашивайте Koľko?, используйте veľa, málo и trochu, различайте dve knihy и päť kníh и называйте меры продуктов.",
  goals: ["Задавать вопрос Koľko?", "Различать Genitív единственного и множественного числа", "Выбирать формы после 2–4 и 5–10", "Просить нужную меру в магазине"],
  theory: {
    summary: "Genitív отвечает на koho? čoho? — «кого? чего?». О количестве спрашивают Koľko?. В сочетании Koľko vody? форма vody стоит в Genitíve. На A1 учите частотные сочетания целиком.",
    rules: [
      "Veľa — много, málo — мало, trochu — немного, koľko — сколько.",
      "Вещество или общий объём: Genitív единственного числа — veľa vody, málo času, trochu cukru.",
      "Отдельные предметы и люди: Genitív множественного числа — veľa kníh, málo ľudí, veľa detí.",
      "После 2–4 с предметами: dve knihy, tri knihy, štyri autá; после 5–10: päť kníh, šesť áut, desať eur.",
      "При простом назывании мужчин: dvaja/traja/štyria študenti; объектное Vidím dvoch študentov — отдельная модель Akuzatívu.",
      "После меры содержимое остаётся в Genitíve: liter vody, pohár vody, šálka kávy, fľaša vody, kilo jabĺk.",
      "Число меняет форму меры: dva litre vody, päť litrov vody. В Kupujem fľašu vody формы fľašu и vody относятся к разным падежам.",
    ],
    examples: [
      { slovak: "Koľko máš času? — Mám málo času.", russian: "Сколько у тебя времени? — У меня мало времени.", explanation: "Общий объём: času в Genitíve единственного числа." },
      { slovak: "Koľko chceš vody? — Chcem trochu vody.", russian: "Сколько воды ты хочешь? — Я хочу немного воды.", explanation: "Вещество после trochu стоит в Genitíve." },
      { slovak: "Mám dve knihy, ale Peter má päť kníh.", russian: "У меня две книги, а у Петера пять книг.", explanation: "После dve — knihy, после päť — kníh." },
      { slovak: "Kupujem fľašu vody.", russian: "Я покупаю бутылку воды.", explanation: "Fľašu — объект, vody — содержимое после меры." },
      { slovak: "Mám málo peňazí.", russian: "У меня мало денег.", explanation: "Genitív слова peniaze — peňazí." },
      { slovak: "Kilo jabĺk, prosím.", russian: "Килограмм яблок, пожалуйста.", explanation: "После kilo нужна форма jabĺk с долгим ĺ." },
    ],
  },
  sections: [
    {
      title: "Много, мало, немного",
      paragraphs: ["Veľa, málo, trochu и koľko обозначают количество. Veľa означает «много», а не обязательно «слишком много».", "Вещество или общий объём обычно требуют единственное число Genitívu; предметы и люди — множественное."],
      table: { headers: ["Слово", "Значение", "Сочетания"], rows: [["veľa", "много", "veľa vody; veľa kníh"], ["málo", "мало", "málo času; málo otázok"], ["trochu", "немного", "trochu kávy; trochu soli"], ["koľko", "сколько?", "Koľko mlieka?; Koľko kníh?"]] },
      items: ["Koľko máš času? — Mám málo času.", "Koľko chceš vody? — Chcem trochu vody.", "Nemám vodu — vodu в Akuzatíve.", "Nemám veľa vody — vody в Genitíve из-за veľa."],
      note: "Сначала определите: вещество/объём или отдельные предметы/люди. Затем выберите число формы Genitívu.",
    },
    {
      title: "Формы, которые пригодятся",
      paragraphs: ["Единого окончания Genitívu нет. Учите готовую пару, а не только последнюю букву."],
      table: { headers: ["Тип", "Nominatív", "Genitív", "Сочетание"], rows: [
        ["ед. · вещество", "voda / káva / mlieko", "vody / kávy / mlieka", "veľa vody / trochu kávy / málo mlieka"],
        ["ед. · объём", "cukor / soľ / čas / práca", "cukru / soli / času / práce", "trochu cukru / soli; málo času; veľa práce"],
        ["мн. · предметы", "knihy / otázky", "kníh / otázok", "veľa kníh / päť otázok"],
        ["мн. · люди", "študenti / ľudia / deti", "študentov / ľudí / detí", "veľa študentov / málo ľudí / veľa detí"],
        ["мн. · особые", "eurá / jablká / peniaze", "eur / jabĺk / peňazí", "desať eur / kilo jabĺk / málo peňazí"],
      ] },
      items: ["Jabĺk пишется с долгим ĺ.", "В kníh, ľudí и detí сохраняйте долгое í.", "Peniaze — множественное число; форму peňazí запомните отдельно."],
      note: "Словацкая диакритика — часть правильного написания: jabĺk и jablk не равны.",
    },
    {
      title: "Числа и меры количества",
      paragraphs: ["После 2–4 предмет стоит в обычной форме множественного числа; после 5–10 — в Genitíve множественного числа.", "Мера и содержимое меняются независимо: dva litre vody, но päť litrov vody."],
      table: { headers: ["Что считаем", "2–4", "5–10"], rows: [["книги", "dve knihy; tri knihy", "päť kníh"], ["машины", "štyri autá", "šesť áut"], ["евро", "dve eurá", "desať eur"], ["литры воды", "dva litre vody", "päť litrov vody"]] },
      items: ["dva zošity; dve knihy; dve autá", "dvaja študenti; traja študenti; štyria študenti", "liter vody; pohár vody; šálka kávy; fľaša vody; kilo jabĺk", "Kupujem fľašu vody: fľašu — Akuzatív, воды — Genitív."],
      note: "Таблица чисел относится к предметам. Формы людей мужского рода и их Akuzatív не смешивайте с этой моделью.",
    },
    {
      title: "Двадцать фраз о количестве",
      paragraphs: ["Читайте вслух, затем закройте перевод и восстановите сочетание количества. Формы глаголов используйте как готовые образцы."],
      table: { headers: ["Slovensky", "По-русски"], rows: [
        ["Mám veľa práce.", "У меня много работы."], ["Dnes mám málo času.", "Сегодня у меня мало времени."], ["Potrebujem veľa vody.", "Мне нужно много воды."],
        ["Chcem trochu kávy.", "Я хочу немного кофе."], ["Potrebujem trochu cukru.", "Мне нужно немного сахара."], ["Máme málo mlieka.", "У нас мало молока."],
        ["Potrebujem trochu soli.", "Мне нужно немного соли."], ["Mám veľa kníh.", "У меня много книг."], ["Poznám veľa ľudí.", "Я знаю много людей."],
        ["Mám málo peňazí.", "У меня мало денег."], ["Koľko vody chceš?", "Сколько воды ты хочешь?"], ["Koľko kníh máš?", "Сколько у тебя книг?"],
        ["Mám dve knihy.", "У меня две книги."], ["Mám päť otázok.", "У меня пять вопросов."], ["Kupujem šesť jabĺk.", "Я покупаю шесть яблок."],
        ["Mám desať eur.", "У меня десять евро."], ["Potrebujem liter mlieka.", "Мне нужен литр молока."], ["Kupujem kilo jabĺk.", "Я покупаю килограмм яблок."],
        ["Chcem pohár vody.", "Я хочу стакан воды."], ["Kupujem fľašu vody.", "Я покупаю бутылку воды."],
      ] },
      items: ["Koľko jabĺk chcete? — Kilo jabĺk, prosím.", "A koľko mlieka? — Dva litre mlieka, prosím."],
      note: "Мини-диалог использует kilo jabĺk и dva litre mlieka как готовые просьбы в магазине.",
    },
    {
      title: "Ошибки и самопроверка",
      table: { headers: ["Ошибка", "Правильно", "Почему"], rows: [["veľa voda", "veľa vody", "После количества нужен Genitív."], ["tri kníh", "tri knihy", "После 3 — обычное множественное число."], ["päť knihy", "päť kníh", "После 5 — Genitív множественного числа."], ["fľašu vodu", "fľašu vody", "Содержимое после меры стоит в Genitíve."]] },
      items: ["Подчеркните слово количества или меру.", "Определите вещество/объём или предметы/людей.", "Проверьте диапазон 2–4 или 5–10.", "В сочетании с мерой проверяйте каждое слово отдельно."],
      note: "Повторите четыре опоры: слово количества + Genitív; число формы; 2–4 против 5–10; мера + содержимое в Genitíve.",
    },
  ],
  stepPractices: [
    { id: "m4-genitive-quantity-step-1", sectionIndex: 0, type: "pairs", prompt: "Выберите правильную форму.", answer: "vody; času; mlieka; detí", pairs: [
      { prompt: "veľa (voda)", answer: "vody", options: ["voda", "vody"] }, { prompt: "málo (čas)", answer: "času", options: ["čas", "času"] },
      { prompt: "trochu (mlieko)", answer: "mlieka", options: ["mlieko", "mlieka"] }, { prompt: "veľa (deti)", answer: "detí", options: ["deti", "detí"] },
    ], hint: "Выберите форму Genitívu.", explanation: "Правильно: veľa vody, málo času, trochu mlieka, veľa detí." },
    { id: "m4-genitive-quantity-step-2", sectionIndex: 1, type: "pairs", prompt: "Поставьте слово в Genitív единственного числа.", answer: "kávy; práce; cukru; mlieka; soli", pairs: [
      { prompt: "trochu (káva)", answer: "kávy", inputHint: "Введите форму слова" }, { prompt: "veľa (práca)", answer: "práce", inputHint: "Введите форму слова" }, { prompt: "trochu (cukor)", answer: "cukru", inputHint: "Введите форму слова" },
      { prompt: "liter (mlieko)", answer: "mlieka", inputHint: "Введите форму слова" }, { prompt: "trochu (soľ)", answer: "soli", inputHint: "Введите форму слова" },
    ], hint: "Введите только требуемую форму.", explanation: "Формы: kávy, práce, cukru, mlieka, soli." },
    { id: "m4-genitive-quantity-step-3", sectionIndex: 2, type: "pairs", prompt: "Поставьте слово в Genitív множественного числа.", answer: "kníh; ľudí; študentov; eur; jabĺk", pairs: [
      { prompt: "veľa (knihy)", answer: "kníh", inputHint: "Введите форму слова" }, { prompt: "málo (ľudia)", answer: "ľudí", inputHint: "Введите форму слова" }, { prompt: "veľa (študenti)", answer: "študentov", inputHint: "Введите форму слова" },
      { prompt: "desať (eurá)", answer: "eur", inputHint: "Введите форму слова" }, { prompt: "kilo (jablká)", answer: "jabĺk", inputHint: "Введите форму слова" },
    ], hint: "Сохраните долготу в kníh, ľudí и jabĺk.", explanation: "Формы: kníh, ľudí, študentov, eur, jabĺk." },
    { id: "m4-genitive-quantity-step-4", sectionIndex: 3, type: "pairs", prompt: "Запишите сочетания; числа пишите словами.", answer: "dve knihy; päť kníh; štyri autá; šesť áut; dva litre vody; päť litrov vody", pairs: [
      { prompt: "2 (kniha)", answer: "dve knihy", inputHint: "Введите сочетание" }, { prompt: "5 (kniha)", answer: "päť kníh", inputHint: "Введите сочетание" }, { prompt: "4 (auto)", answer: "štyri autá", inputHint: "Введите сочетание" },
      { prompt: "6 (auto)", answer: "šesť áut", inputHint: "Введите сочетание" }, { prompt: "2 (liter) vody", answer: "dva litre vody", inputHint: "Введите сочетание" }, { prompt: "5 (liter) vody", answer: "päť litrov vody", inputHint: "Введите сочетание" },
    ], hint: "Выберите форму числа и предмета или меры.", explanation: "После 2–4 — обычное множественное число; после 5–10 — Genitív." },
    { id: "m4-genitive-quantity-step-5", sectionIndex: 4, type: "pairs", prompt: "Исправьте сочетания.", answer: "veľa vody; tri knihy; päť kníh; fľašu vody", pairs: [
      { prompt: "veľa voda", answer: "veľa vody", inputHint: "Введите исправленное сочетание" }, { prompt: "tri kníh", answer: "tri knihy", inputHint: "Введите исправленное сочетание" },
      { prompt: "päť knihy", answer: "päť kníh", inputHint: "Введите исправленное сочетание" }, { prompt: "fľašu vodu", answer: "fľašu vody", inputHint: "Введите исправленное сочетание" },
    ], hint: "Проверьте слово количества, число и меру.", explanation: "Правильно: veľa vody, tri knihy, päť kníh, fľašu vody." },
  ],
  assessmentMode: "interactive",
  materialAssessmentStep: false,
  reinforcementLabel: "Финальный тест темы",
  reinforcementTitle: "Выполните шесть заданий темы 5",
  reinforcementPractices: [
    { id: "reinforcement:genitive-quantity:1", sectionIndex: 0, type: "pairs", prompt: "Выберите правильную форму.", answer: "vody; času; mlieka; detí", pairs: [
      { prompt: "veľa (voda)", answer: "vody", options: ["voda", "vody"] }, { prompt: "málo (čas)", answer: "času", options: ["čas", "času"] }, { prompt: "trochu (mlieko)", answer: "mlieka", options: ["mlieko", "mlieka"] }, { prompt: "veľa (deti)", answer: "detí", options: ["deti", "detí"] },
    ], hint: "Выберите форму Genitívu.", explanation: "Правильно: vody, času, mlieka, detí." },
    { id: "reinforcement:genitive-quantity:2", sectionIndex: 1, type: "pairs", prompt: "Поставьте слово в Genitív единственного числа.", answer: "kávy; práce; cukru; mlieka; soli", pairs: [
      { prompt: "trochu (káva)", answer: "kávy", inputHint: "Введите форму слова" }, { prompt: "veľa (práca)", answer: "práce", inputHint: "Введите форму слова" }, { prompt: "trochu (cukor)", answer: "cukru", inputHint: "Введите форму слова" }, { prompt: "liter (mlieko)", answer: "mlieka", inputHint: "Введите форму слова" }, { prompt: "trochu (soľ)", answer: "soli", inputHint: "Введите форму слова" },
    ], hint: "Введите только форму существительного.", explanation: "Формы: kávy, práce, cukru, mlieka, soli." },
    { id: "reinforcement:genitive-quantity:3", sectionIndex: 1, type: "pairs", prompt: "Поставьте слово в Genitív множественного числа.", answer: "kníh; ľudí; študentov; eur; jabĺk", pairs: [
      { prompt: "veľa (knihy)", answer: "kníh", inputHint: "Введите форму слова" }, { prompt: "málo (ľudia)", answer: "ľudí", inputHint: "Введите форму слова" }, { prompt: "veľa (študenti)", answer: "študentov", inputHint: "Введите форму слова" }, { prompt: "desať (eurá)", answer: "eur", inputHint: "Введите форму слова" }, { prompt: "kilo (jablká)", answer: "jabĺk", inputHint: "Введите форму слова" },
    ], hint: "Не теряйте диакритику.", explanation: "Формы: kníh, ľudí, študentov, eur, jabĺk." },
    { id: "reinforcement:genitive-quantity:4", sectionIndex: 2, type: "pairs", prompt: "Запишите сочетания; числа пишите словами.", answer: "dve knihy; päť kníh; štyri autá; šesť áut; dva litre vody; päť litrov vody", pairs: [
      { prompt: "2 (kniha)", answer: "dve knihy", inputHint: "Введите сочетание" }, { prompt: "5 (kniha)", answer: "päť kníh", inputHint: "Введите сочетание" }, { prompt: "4 (auto)", answer: "štyri autá", inputHint: "Введите сочетание" }, { prompt: "6 (auto)", answer: "šesť áut", inputHint: "Введите сочетание" }, { prompt: "2 (liter) vody", answer: "dva litre vody", inputHint: "Введите сочетание" }, { prompt: "5 (liter) vody", answer: "päť litrov vody", inputHint: "Введите сочетание" },
    ], hint: "Проверьте каждое слово.", explanation: "Правильно: dve knihy, päť kníh, štyri autá, šesť áut, dva litre vody, päť litrov vody." },
    { id: "reinforcement:genitive-quantity:5", sectionIndex: 3, type: "pairs", prompt: "Переведите на словацкий.", answer: "Mám málo času.; Chcem trochu kávy.; Kupujem fľašu vody.; Mám desať eur.", pairs: [
      { prompt: "У меня мало времени.", answer: "Mám málo času.", acceptableAnswers: ["Ja mám málo času."], inputHint: "Введите перевод по-словацки" },
      { prompt: "Я хочу немного кофе.", answer: "Chcem trochu kávy.", acceptableAnswers: ["Ja chcem trochu kávy."], inputHint: "Введите перевод по-словацки" },
      { prompt: "Я покупаю бутылку воды.", answer: "Kupujem fľašu vody.", acceptableAnswers: ["Ja kupujem fľašu vody."], inputHint: "Введите перевод по-словацки" },
      { prompt: "У меня десять евро.", answer: "Mám desať eur.", acceptableAnswers: ["Ja mám desať eur."], inputHint: "Введите перевод по-словацки" },
    ], hint: "Проверьте сочетание количества.", explanation: "Модели: málo času, trochu kávy, fľašu vody, desať eur." },
    { id: "reinforcement:genitive-quantity:6", sectionIndex: 3, type: "pairs", prompt: "Выберите пять фраз с разными моделями количества.", answer: "Mám málo času.; Kupujem dve knihy.; Mám päť otázok.; Potrebujem liter mlieka.; Koľko vody chceš?", pairs: [
      { prompt: "veľa / málo / trochu", answer: "Mám málo času.", options: ["Mám málo čas.", "Mám málo času.", "Mám málo časy."] },
      { prompt: "число 2–4 с предметом", answer: "Kupujem dve knihy.", options: ["Kupujem dve knihy.", "Kupujem dve kníh.", "Kupujem dvoch knihy."] },
      { prompt: "число 5–10", answer: "Mám päť otázok.", options: ["Mám päť otázky.", "Mám päť otázok.", "Mám piati otázok."] },
      { prompt: "единица измерения", answer: "Potrebujem liter mlieka.", options: ["Potrebujem liter mlieko.", "Potrebujem litra mlieka.", "Potrebujem liter mlieka."] },
      { prompt: "вопрос с Koľko?", answer: "Koľko vody chceš?", options: ["Koľko voda chceš?", "Koľké vody chceš?", "Koľko vody chceš?"] },
    ], hint: "Каждая строка проверяет отдельную модель.", explanation: "Выбраны слово количества, числа 2–4 и 5–10, мера и вопрос Koľko?." },
  ],
  knowledgeChecks: [
    { id: "m4-genitive-quantity-check-1", question: "Как правильно сказать «немного кофе»?", options: ["trochu káva", "trochu kávy", "trochu kávu"], answer: "trochu kávy", explanation: "Вещество после trochu стоит в Genitíve." },
    { id: "m4-genitive-quantity-check-2", question: "Какая пара показывает различие после 2 и 5?", options: ["dve knihy — päť kníh", "dve kníh — päť knihy", "dve knihy — päť knihy"], answer: "dve knihy — päť kníh", explanation: "После dve — knihy, после päť — kníh." },
    { id: "m4-genitive-quantity-check-3", question: "Почему в Kupujem fľašu vody две разные формы?", options: ["Fľašu — объект, vody — содержимое после меры", "Оба слова стоят в Nominatíve", "После kupujem всегда нужен Genitív"], answer: "Fľašu — объект, vody — содержимое после меры", explanation: "Fľašu отвечает на что покупаю, vody — бутылка чего." },
  ],
  finalChecks: [
    { id: "m4-genitive-quantity-final-1", question: "Переведите: «пять книг».", options: ["päť kníh", "päť knihy", "piati kníh"], answer: "päť kníh", explanation: "После päť нужна форма Genitívu множественного числа kníh." },
  ],
  chatPrompt: "Назовите пять количеств: со словом veľa/málo/trochu, числом 2–4, числом 5–10, мерой и вопросом Koľko?.",
  chatSuggestions: ["Mám málo času. Kupujem dve knihy.", "Mám päť otázok. Potrebujem liter mlieka.", "Koľko vody chceš?"],
} satisfies CourseLesson;
