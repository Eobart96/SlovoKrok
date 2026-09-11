import type { CourseLesson } from "../../../courseTypes";

const masculineOptions = ["vysoký", "nízky", "mladý", "milý", "pokojný"];
const feminineOptions = ["vysoká", "nízka", "mladá", "milá", "pokojná"];
const verbOptions = ["má", "nosí", "je", "nemá", "nenosí"];

export const peopleDescriptionLesson = {
  vocabulary: [
    {"word":"Je vysoký a má krátke vlasy.","translation":"Он высокий, и у него короткие волосы.","example":"Je vysoký a má krátke vlasy."},
    {"word":"Má modré oči.","translation":"У неё голубые глаза.","example":"Má modré oči."},
    {"word":"Nosí okuliare.","translation":"Он/она носит очки.","example":"Nosí okuliare."},
    {"word":"Je milá a pokojná.","translation":"Она милая и спокойная.","example":"Je milá a pokojná."},
    {"word":"Je mladá a veľmi milá.","translation":"Она молодая и очень милая.","example":"Je mladá a veľmi milá."},
    {"word":"Má dlhé tmavé vlasy.","translation":"У него/неё длинные тёмные волосы.","example":"Má dlhé tmavé vlasy."},
  ],
  slug: "people-description",
  order: 11,
  title: "Описание людей",
  slovakTitle: "Opis ľudí",
  description: "Нейтрально описывайте внешность и характер знакомого человека.",
  duration: "35–40 мин",
  goals: [
    "Согласовывать простые признаки с мужчиной и женщиной",
    "Называть рост и возрастную характеристику",
    "Описывать волосы и глаза через mať",
    "Говорить об очках и нейтральных чертах характера",
    "Составлять короткий уважительный профиль человека",
  ],
  theory: {
    summary: "Описание человека уровня A1 состоит из нескольких наблюдаемых и нейтральных признаков. Сначала назовите человека, затем добавьте внешность через je или má и одну простую характеристику характера.",
    rules: [
      "После muž/on употребляйте мужскую форму: vysoký, mladý, milý. После žena/ona — женскую: vysoká, mladá, milá.",
      "Рост и характер описываются через byť: Je vysoký. Je pokojná.",
      "Волосы и глаза описываются через mať: Má krátke vlasy. Má modré oči. Прилагательное согласуется со словом vlasy или oči, поэтому форма остаётся на -é.",
      "Очки описываются глаголом nosiť: Nosí okuliare. Отрицание: Nenosí okuliare.",
      "Несколько признаков соединяйте через a: Je mladá a veľmi milá. Он/она обычно не нужны, если человек уже понятен из контекста.",
      "Выбирайте нейтральные наблюдаемые признаки. Не делайте выводов о здоровье, происхождении, способностях или характере только по внешности.",
    ],
    examples: [
      { slovak: "Je vysoký a má krátke vlasy.", russian: "Он высокий, и у него короткие волосы.", explanation: "Vysoký относится к мужчине, krátke — к слову vlasy." },
      { slovak: "Má modré oči.", russian: "У неё голубые глаза.", explanation: "Для глаз используется mať, а не byť." },
      { slovak: "Nosí okuliare.", russian: "Он/она носит очки.", explanation: "Форма nosí одинакова для on и ona." },
      { slovak: "Je milá a pokojná.", russian: "Она милая и спокойная.", explanation: "Обе формы согласованы с женщиной." },
      { slovak: "Je mladá a veľmi milá.", russian: "Она молодая и очень милая.", explanation: "Veľmi усиливает второй нейтральный признак." },
      { slovak: "Má dlhé tmavé vlasy.", russian: "У него/неё длинные тёмные волосы.", explanation: "Оба определения согласуются с множественным vlasy." },
    ],
  },
  sections: [
    {
      title: "Кто это и согласование",
      paragraphs: ["Начните с To je... или уже известного on/ona. Форма прилагательного показывает, описывается мужчина или женщина.", "Для частых признаков мужская форма обычно оканчивается на -ý, женская — на -á: mladý — mladá."],
      table: { headers: ["Признак", "Мужчина", "Женщина"], rows: [
        ["высокий", "vysoký", "vysoká"], ["невысокий", "nízky", "nízka"], ["молодой", "mladý", "mladá"],
        ["милый", "milý", "milá"], ["спокойный", "pokojný", "pokojná"], ["тихий", "tichý", "tichá"],
      ] },
      items: ["To je Peter. Je vysoký.", "To je Anna. Je vysoká.", "On je mladý.", "Ona je mladá."],
      note: "Форма зависит от описываемого человека: Peter je milý, Anna je milá.",
    },
    {
      title: "Рост и общий внешний признак",
      paragraphs: ["Рост описывайте через je + прилагательное. Для осторожного возрастного контраста достаточно mladý/mladá и starší/staršia.", "Не превращайте описание в оценку привлекательности. На A1 важнее узнаваемый нейтральный признак."],
      table: { headers: ["Мужчина", "Женщина", "Перевод"], rows: [
        ["Je vysoký.", "Je vysoká.", "Он высокий. / Она высокая."], ["Je nízky.", "Je nízka.", "Он невысокий. / Она невысокая."],
        ["Je mladý.", "Je mladá.", "Он молодой. / Она молодая."], ["Je starší.", "Je staršia.", "Он старше. / Она старше."],
      ] },
      items: ["Je veľmi vysoký.", "Nie je vysoká, je nízka.", "Je mladý a tichý."],
      note: "Veľmi не изменяется: veľmi vysoký, veľmi vysoká.",
    },
    {
      title: "Волосы и глаза: má",
      paragraphs: ["У человека есть волосы и глаза, поэтому используйте má. Не говорите je modré oči или je dlhé vlasy.", "Прилагательные при vlasy и oči имеют форму множественного числа на -é: krátke, dlhé, svetlé, tmavé, modré, hnedé, zelené."],
      table: { headers: ["Что", "Пример", "Перевод"], rows: [
        ["короткие волосы", "Má krátke vlasy.", "У него/неё короткие волосы."], ["длинные волосы", "Má dlhé vlasy.", "У него/неё длинные волосы."],
        ["тёмные волосы", "Má tmavé vlasy.", "У него/неё тёмные волосы."], ["голубые глаза", "Má modré oči.", "У него/неё голубые глаза."],
        ["карие глаза", "Má hnedé oči.", "У него/неё карие глаза."], ["зелёные глаза", "Má zelené oči.", "У него/неё зелёные глаза."],
      ] },
      items: ["Má dlhé svetlé vlasy.", "Má krátke tmavé vlasy.", "Má modré oči."],
      note: "Для частей тела используется mať: má modré oči; не je modré oči.",
    },
    {
      title: "Очки и нейтральный характер",
      paragraphs: ["Об очках говорите nosí okuliare или nenosí okuliare. После этого добавьте одну известную нейтральную характеристику.", "Характер описывайте только тогда, когда вы действительно знаете человека, а не делаете вывод по фотографии."],
      table: { headers: ["Признак", "Мужчина", "Женщина"], rows: [
        ["очки", "Nosí okuliare.", "Nosí okuliare."], ["милый", "Je milý.", "Je milá."], ["спокойный", "Je pokojný.", "Je pokojná."],
        ["тихий", "Je tichý.", "Je tichá."], ["весёлый", "Je veselý.", "Je veselá."],
      ] },
      items: ["Je milá a pokojná.", "Je veselý a nosí okuliare.", "Nenosí okuliare."],
      note: "Nosí не показывает род; род виден в прилагательных milý/milá и pokojný/pokojná.",
    },
    {
      title: "Короткий профиль и частые ошибки",
      paragraphs: ["Профиль из четырёх фраз может назвать человека, рост, волосы или глаза, очки и одну характеристику. Не нужно угадывать скрытые качества.", "Перед ответом проверьте род прилагательного, je/má/nosí, форму -é при vlasy/oči и словацкую диакритику."],
      table: { headers: ["Ошибка", "Правильно", "Почему"], rows: [
        ["Женщина: Je vysoký.", "Je vysoká.", "Нужна женская форма."], ["Je modré oči.", "Má modré oči.", "Для глаз используется má."],
        ["Má krátky vlasy.", "Má krátke vlasy.", "Vlasy требуют формы krátke."], ["Ona je milý.", "Ona je milá.", "Признак согласуется с ona."],
        ["Nosi okuliare.", "Nosí okuliare.", "В форме nosí нужна долгота."],
      ] },
      items: ["To je Eva.", "Je vysoká a mladá.", "Má dlhé tmavé vlasy.", "Nosí okuliare.", "Je milá a pokojná."],
      note: "Избегайте чувствительных оценок и детальных медицинских характеристик.",
    },
  ],
  stepPractices: [
    { id: "m6-people-description-step-1", sectionIndex: 0, type: "pairs", prompt: "Выберите мужскую форму признака.", answer: "vysoký; nízky; mladý; milý; pokojný", pairs: [
      { prompt: "высокий", answer: "vysoký", options: masculineOptions }, { prompt: "невысокий", answer: "nízky", options: masculineOptions }, { prompt: "молодой", answer: "mladý", options: masculineOptions }, { prompt: "милый", answer: "milý", options: masculineOptions }, { prompt: "спокойный", answer: "pokojný", options: masculineOptions },
    ], hint: "Все ответы описывают мужчину.", explanation: "Мужские формы оканчиваются здесь на -ý." },
    { id: "m6-people-description-step-2", sectionIndex: 1, type: "pairs", prompt: "Выберите женскую форму признака.", answer: "vysoká; nízka; mladá; milá; pokojná", pairs: [
      { prompt: "высокая", answer: "vysoká", options: feminineOptions }, { prompt: "невысокая", answer: "nízka", options: feminineOptions }, { prompt: "молодая", answer: "mladá", options: feminineOptions }, { prompt: "милая", answer: "milá", options: feminineOptions }, { prompt: "спокойная", answer: "pokojná", options: feminineOptions },
    ], hint: "Все ответы описывают женщину.", explanation: "Женские формы оканчиваются здесь на -á." },
    { id: "m6-people-description-step-3", sectionIndex: 2, type: "pairs", prompt: "Выберите подходящий глагол.", answer: "má; nosí; je; má; nenosí", pairs: [
      { prompt: "___ modré oči.", answer: "má", options: verbOptions }, { prompt: "___ okuliare.", answer: "nosí", options: verbOptions }, { prompt: "___ vysoká.", answer: "je", options: verbOptions }, { prompt: "___ dlhé vlasy.", answer: "má", options: verbOptions }, { prompt: "___ okuliare. · не носит", answer: "nenosí", options: verbOptions },
    ], hint: "Различайте признак, наличие и ношение очков.", explanation: "Je описывает признак, má — волосы/глаза, nosí — очки." },
    { id: "m6-people-description-step-4", sectionIndex: 3, type: "pairs", prompt: "Выберите нормативное описание.", answer: "Je milý.; Je milá.; Je pokojný.; Je pokojná.; Nosí okuliare.", pairs: [
      { prompt: "мужчина · милый", answer: "Je milý.", options: ["Je milý.", "Je milá."] }, { prompt: "женщина · милая", answer: "Je milá.", options: ["Je milý.", "Je milá."] },
      { prompt: "мужчина · спокойный", answer: "Je pokojný.", options: ["Je pokojný.", "Je pokojná."] }, { prompt: "женщина · спокойная", answer: "Je pokojná.", options: ["Je pokojný.", "Je pokojná."] },
      { prompt: "он/она носит очки", answer: "Nosí okuliare.", options: ["Nosí okuliare.", "Je okuliare."] },
    ], hint: "Учитывайте род только там, где форма его показывает.", explanation: "Прилагательные согласуются по роду, nosí одинаково для on и ona." },
    { id: "m6-people-description-step-5", sectionIndex: 4, type: "pairs", prompt: "Исправьте каждую фразу.", answer: "Je vysoká.; Má modré oči.; Má krátke vlasy.; Ona je milá.; Je mladá a veľmi milá.", pairs: [
      { prompt: "Женщина: Je vysoký.", answer: "Je vysoká.", inputHint: "Введите исправленную фразу" }, { prompt: "Je modré oči.", answer: "Má modré oči.", inputHint: "Введите исправленную фразу" },
      { prompt: "Má krátky vlasy.", answer: "Má krátke vlasy.", inputHint: "Введите исправленную фразу" }, { prompt: "Ona je milý.", answer: "Ona je milá.", inputHint: "Введите исправленную фразу" },
      { prompt: "Переведите: «Она молодая и очень милая».", answer: "Je mladá a veľmi milá.", inputHint: "Введите перевод" },
    ], hint: "Проверьте род, je/má, форму при vlasy и диакритику.", explanation: "Нормативны vysoká, má oči, krátke vlasy, milá и veľmi milá." },
  ],
  assessmentMode: "interactive",
  materialAssessmentStep: false,
  reinforcementLabel: "Финальный тест темы",
  reinforcementTitle: "Выполните шесть заданий темы 11",
  reinforcementPractices: [
    { id: "reinforcement:people-description:1", sectionIndex: 0, type: "pairs", prompt: "Выберите мужскую форму.", answer: "vysoký; nízky; mladý; milý; pokojný", pairs: [
      { prompt: "высокий", answer: "vysoký", options: masculineOptions }, { prompt: "невысокий", answer: "nízky", options: masculineOptions }, { prompt: "молодой", answer: "mladý", options: masculineOptions }, { prompt: "милый", answer: "milý", options: masculineOptions }, { prompt: "спокойный", answer: "pokojný", options: masculineOptions },
    ], hint: "Выберите форму на -ý.", explanation: "Пять признаков описывают мужчину." },
    { id: "reinforcement:people-description:2", sectionIndex: 0, type: "pairs", prompt: "Выберите женскую форму.", answer: "vysoká; nízka; mladá; milá; pokojná", pairs: [
      { prompt: "высокая", answer: "vysoká", options: feminineOptions }, { prompt: "невысокая", answer: "nízka", options: feminineOptions }, { prompt: "молодая", answer: "mladá", options: feminineOptions }, { prompt: "милая", answer: "milá", options: feminineOptions }, { prompt: "спокойная", answer: "pokojná", options: feminineOptions },
    ], hint: "Выберите форму на -á.", explanation: "Пять признаков описывают женщину." },
    { id: "reinforcement:people-description:3", sectionIndex: 2, type: "pairs", prompt: "Выберите je, má или nosí.", answer: "je; má; má; nosí; nenosí", pairs: [
      { prompt: "___ vysoký.", answer: "je", options: verbOptions }, { prompt: "___ modré oči.", answer: "má", options: verbOptions }, { prompt: "___ krátke vlasy.", answer: "má", options: verbOptions }, { prompt: "___ okuliare.", answer: "nosí", options: verbOptions }, { prompt: "___ okuliare. · не носит", answer: "nenosí", options: verbOptions },
    ], hint: "Признак — je, волосы/глаза — má, очки — nosí.", explanation: "Глагол показывает тип описания." },
    { id: "reinforcement:people-description:4", sectionIndex: 4, type: "pairs", prompt: "Исправьте ошибки в описании.", answer: "Je vysoká.; Má modré oči.; Má krátke vlasy.; Ona je milá.; Nosí okuliare.", pairs: [
      { prompt: "Женщина: Je vysoký.", answer: "Je vysoká.", inputHint: "Введите исправленную фразу" }, { prompt: "Je modré oči.", answer: "Má modré oči.", inputHint: "Введите исправленную фразу" },
      { prompt: "Má krátky vlasy.", answer: "Má krátke vlasy.", inputHint: "Введите исправленную фразу" }, { prompt: "Ona je milý.", answer: "Ona je milá.", inputHint: "Введите исправленную фразу" }, { prompt: "Nosi okuliare.", answer: "Nosí okuliare.", inputHint: "Введите исправленную фразу" },
    ], hint: "Исправьте всю строку: род, глагол, согласование или диакритику.", explanation: "Каждая строка проверяет один частотный элемент описания." },
    { id: "reinforcement:people-description:5", sectionIndex: 4, type: "pairs", prompt: "Переведите на словацкий.", answer: "Je vysoký a má krátke vlasy.; Má modré oči.; Nosí okuliare.; Je milá a pokojná.; Je mladá a veľmi milá.", pairs: [
      { prompt: "Он высокий, и у него короткие волосы.", answer: "Je vysoký a má krátke vlasy.", acceptableAnswers: ["Má krátke vlasy a je vysoký."], inputHint: "Введите перевод" },
      { prompt: "У неё голубые глаза.", answer: "Má modré oči.", inputHint: "Введите перевод" }, { prompt: "Он/она носит очки.", answer: "Nosí okuliare.", inputHint: "Введите перевод" },
      { prompt: "Она милая и спокойная.", answer: "Je milá a pokojná.", acceptableAnswers: ["Je pokojná a milá."], inputHint: "Введите перевод" }, { prompt: "Она молодая и очень милая.", answer: "Je mladá a veľmi milá.", inputHint: "Введите перевод" },
    ], hint: "Используйте модели урока и сохраните словацкую диакритику.", explanation: "Переводы проверяют род, je/má/nosí и нейтральные признаки." },
    { id: "reinforcement:people-description:6", sectionIndex: 4, type: "pairs", prompt: "Соберите нейтральный профиль женщины.", answer: "To je Eva.; Je vysoká a mladá.; Má dlhé tmavé vlasy.; Má modré oči.; Nosí okuliare.; Je milá a pokojná.", pairs: [
      { prompt: "1 · кто", answer: "To je Eva.", options: ["To je Eva.", "Ona Eva byť.", "Toto Eva sú."] }, { prompt: "2 · рост и возраст", answer: "Je vysoká a mladá.", options: ["Je vysoký a mladý.", "Je vysoká a mladá.", "Má vysoká a mladá."] },
      { prompt: "3 · волосы", answer: "Má dlhé tmavé vlasy.", options: ["Má dlhé tmavé vlasy.", "Je dlhý tmavý vlasy.", "Má dlhá tmavá vlasy."] }, { prompt: "4 · глаза", answer: "Má modré oči.", options: ["Je modré oči.", "Má modré oči.", "Nosí modrá oči."] },
      { prompt: "5 · очки", answer: "Nosí okuliare.", options: ["Je okuliare.", "Má okuliare nosí.", "Nosí okuliare."] }, { prompt: "6 · характер", answer: "Je milá a pokojná.", options: ["Je milý a pokojný.", "Je milá a pokojná.", "Má milá a pokojná."] },
    ], hint: "Сохраняйте женский род и различайте je, má и nosí.", explanation: "Профиль использует только нейтральные, изученные и наблюдаемые признаки." },
  ],
  knowledgeChecks: [
    { id: "m6-people-description-check-1", question: "Как описать высокого мужчину с короткими волосами?", options: ["Je vysoký a má krátke vlasy.", "Je vysoká a má krátky vlasy.", "Má vysoký a je krátke vlasy."], answer: "Je vysoký a má krátke vlasy.", explanation: "Рост описывает je, волосы — má." },
    { id: "m6-people-description-check-2", question: "Как сказать «У неё голубые глаза»?", options: ["Má modré oči.", "Je modré oči.", "Nosí modré oči."], answer: "Má modré oči.", explanation: "Для глаз используется mať." },
    { id: "m6-people-description-check-3", question: "Какая граница соответствует уровню A1?", options: ["Избегайте чувствительных оценок и детальных медицинских характеристик.", "Нужно определять характер человека по фотографии.", "Нужно подробно описывать медицинское состояние."], answer: "Избегайте чувствительных оценок и детальных медицинских характеристик.", explanation: "A1-профиль остаётся коротким, нейтральным и уважительным." },
  ],
  finalChecks: [
    { id: "m6-people-description-final-1", question: "Переведите: «Она молодая и очень милая».", options: ["Je mladá a veľmi milá.", "Je mladý a veľmi milý.", "Má mladá a veľa milá."], answer: "Je mladá a veľmi milá.", explanation: "Обе формы женского рода; признаки соединены через a." },
  ],
  chatPrompt: "Опишите знакомого человека четырьмя нейтральными признаками, не называя его имени.",
  chatSuggestions: ["Je vysoký a má krátke vlasy.", "Nosí okuliare.", "Je milá a pokojná."],
} satisfies CourseLesson;
