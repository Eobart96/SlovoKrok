import type { CourseLesson } from "../../../courseTypes";
import { defineModule4Lesson } from "../lessonFactory";

const baseGenitiveDoLesson = defineModule4Lesson("genitive-do", 6, {
  summary: "Do + Genitív отвечает на Kam? и называет цель движения внутрь здания, города или контейнера.",
  model: "Kam? + do + Genitív: do školy, do hotela, do mesta, do tašky.",
  goals: ["Различать Kde? и Kam?", "Выражать направление с do", "Употреблять частотные формы Genitívu", "Говорить, куда кладём вещи"],
  rules: [
    "После do нужен Genitív: škola → do školy; obchod → do obchodu; mesto → do mesta.",
    "Учите пары места и цели: v škole → do školy; v hoteli → do hotela; v meste → do mesta.",
    "Города склоняются: do Bratislavy, do Prahy, do Viedne, do Košíc.",
    "Контейнеры используют ту же модель: do tašky, do vrecka, do chladničky, do auta.",
    "Idem domov означает «иду домой», а Vchádzam do domu — «вхожу внутрь здания».",
    "Kam? не означает автоматически do: для почты учите na pošte → na poštu.",
  ],
  examples: [
    { slovak: "Idem do školy.", russian: "Я иду в школу." },
    { slovak: "Vraciame sa do hotela.", russian: "Мы возвращаемся в отель." },
    { slovak: "Cestujem do Bratislavy.", russian: "Я еду в Братиславу." },
    { slovak: "Dávam knihu do tašky.", russian: "Я кладу книгу в сумку." },
    { slovak: "Nastupujem do auta.", russian: "Я сажусь в машину." },
  ],
  primaryTitle: "Места и города после do",
  primaryTable: { headers: ["Nominatív", "Genitív", "Сочетание"], rows: [
    ["škola / banka", "školy / banky", "do školy / banky"], ["práca / nemocnica", "práce / nemocnice", "do práce / nemocnice"],
    ["obchod / park", "obchodu / parku", "do obchodu / parku"], ["dom / hotel", "domu / hotela", "do domu / hotela"],
    ["mesto / kino", "mesta / kina", "do mesta / kina"], ["divadlo / centrum", "divadla / centra", "do divadla / centra"],
  ] },
  secondaryTitle: "Контейнеры и особые пары",
  secondaryTable: { headers: ["Исходная форма", "Направление", "Пример"], rows: [
    ["taška / vrecko", "do tašky / vrecka", "Dávam kľúče do vrecka."], ["chladnička / auto", "do chladničky / auta", "Dávam mlieko do chladničky."],
    ["Bratislava / Praha / Viedeň", "do Bratislavy / Prahy / Viedne", "Cestujeme do Prahy."], ["Košice / Tatry / Alpy", "do Košíc / Tatier / Álp", "Ideme do Tatier."],
    ["domov", "без do", "Idem domov."], ["dom", "do domu", "Vchádzam do domu."],
  ] },
  boundaryItems: ["Som v škole → Idem do školy.", "Som v hoteli → Idem do hotela.", "Som na pošte → Idem na poštu.", "v Košiciach → do Košíc; v Tatrách → do Tatier."],
  mistake: "Не оставляйте словарную форму после do и не переносите do на места с na: do školy, do hotela, но na poštu.",
  task: "Назовите четыре места с do и скажите, какую вещь кладёте внутрь сумки, кармана или холодильника.",
  productionPrompt: "Переведите: «Я еду в Братиславу».",
  productionAnswer: "Cestujem do Bratislavy.",
  productionHint: "После do название города получает форму Bratislavy.",
});

export const genitiveDoLesson = {
  vocabulary: [
    {"word":"Som v škole. — Idem do školy.","translation":"Я в школе. — Я иду в школу.","example":"Som v škole. — Idem do školy."},
    {"word":"Sme v meste. — Ideme do mesta.","translation":"Мы в городе. — Мы идём в город.","example":"Sme v meste. — Ideme do mesta."},
    {"word":"Cestujeme do Košíc.","translation":"Мы едем в Кошице.","example":"Cestujeme do Košíc."},
    {"word":"Dávam mlieko do chladničky.","translation":"Я ставлю молоко в холодильник.","example":"Dávam mlieko do chladničky."},
    {"word":"Vraciame sa do hotela.","translation":"Мы возвращаемся в отель.","example":"Vraciame sa do hotela."},
    {"word":"Idem domov.","translation":"Я иду домой.","example":"Idem domov."},
  ],
  ...baseGenitiveDoLesson,
  description: "Отвечайте на Kam?, различайте место и направление и используйте do + Genitív с местами, городами и контейнерами.",
  goals: ["Различать Kde? и Kam?", "Называть цель движения", "Запоминать формы после do", "Описывать помещение предмета внутрь"],
  theory: {
    summary: "Kam? значит «куда?». Сочетание do + Genitív называет цель: идём в магазин, едем в город, помещаем вещь внутрь. Хотя по-русски часто используется «в» с винительным, после словацкого do нужен Genitív.",
    rules: [
      "Kde? обозначает место, Kam? — направление: Som v škole → Idem do školy; Som v hoteli → Idem do hotela.",
      "Не выбирайте do только по глаголу движения: Idem do parku называет цель, но Behám v parku — место действия.",
      "Kam? не означает автоматически do: Idem na poštu. Предлог учат вместе с местом: na pošte → na poštu.",
      "После do существительное принимает Genitív: do školy, do obchodu, do hotela, do mesta. Мужские формы -u/-a нужно запоминать.",
      "Географические названия тоже склоняются: do Bratislavy, do Prahy, do Viedne; do Košíc, do Tatier, do Álp.",
      "В Dávam knihu do tašky два вопроса: Čo dávam? — knihu в Akuzatíve; Kam? — do tašky в Genitíve.",
      "Idem domov означает «иду домой» и употребляется без do; Som doma отвечает на Kde?; Vchádzam do domu обозначает вход в здание.",
    ],
    examples: [
      { slovak: "Som v škole. — Idem do školy.", russian: "Я в школе. — Я иду в школу.", explanation: "V + Lokál отвечает на Kde?, do + Genitív — на Kam?." },
      { slovak: "Sme v meste. — Ideme do mesta.", russian: "Мы в городе. — Мы идём в город.", explanation: "Место и цель требуют разных форм." },
      { slovak: "Cestujeme do Košíc.", russian: "Мы едем в Кошице.", explanation: "Košice имеет форму множественного числа; Genitív — Košíc." },
      { slovak: "Dávam mlieko do chladničky.", russian: "Я ставлю молоко в холодильник.", explanation: "Do chladničky называет направление внутрь." },
      { slovak: "Vraciame sa do hotela.", russian: "Мы возвращаемся в отель.", explanation: "Возвратный глагол сохраняет sa; hotel → hotela." },
      { slovak: "Idem domov.", russian: "Я иду домой.", explanation: "Domov употребляется без do." },
    ],
  },
  sections: [
    {
      title: "Куда направлено движение?",
      paragraphs: ["Do + Genitív отвечает на Kam? и называет цель движения или направление внутрь.", "Движение само по себе не выбирает падеж: Idem do parku, но Behám v parku."],
      table: { headers: ["Kde? · место", "Kam? · направление"], rows: [["Som v škole.", "Idem do školy."], ["Som v hoteli.", "Idem do hotela."], ["Sme v meste.", "Ideme do mesta."]] },
      items: ["Idem do banky. — Иду в банк.", "Cestujeme do Prahy. — Едем в Прагу.", "Vchádzam do izby. — Вхожу в комнату.", "Dávam pero do tašky. — Кладу ручку в сумку.", "Na pošte → na poštu: не каждое Kam? использует do."],
      note: "Здесь разбирается пространственное do. Значения времени и срока остаются за рамками урока.",
    },
    {
      title: "Места и города после do",
      paragraphs: ["Учите место сразу с направлением. Одного окончания для всех слов нет."],
      table: { headers: ["Место", "Куда? · do + G", "Подсказка"], rows: [
        ["škola / banka", "do školy / do banky", "-a → -y"], ["práca / nemocnica", "do práce / do nemocnice", "-a → -e"],
        ["obchod / park", "do obchodu / do parku", "формы на -u"], ["dom / hotel", "do domu / do hotela", "разные окончания"],
        ["mesto / kino", "do mesta / do kina", "-o → -a"], ["divadlo / centrum", "do divadla / do centra", "частотные формы на -a"],
        ["Bratislava / Praha / Viedeň", "do Bratislavy / do Prahy / do Viedne", "формы городов"], ["Košice / Tatry / Alpy", "do Košíc / do Tatier / do Álp", "G множественного числа"],
      ] },
      items: ["obchod → obchodu, но hotel → hotela.", "centrum → centra: часть -um заменяется на -a.", "v Bratislave → do Bratislavy.", "v Košiciach → do Košíc; v Tatrách → do Tatier."],
      note: "Košíc, Tatier и Álp лучше выучить как готовые сочетания.",
    },
    {
      title: "Внутрь сумки, комнаты, машины",
      paragraphs: ["Do относится к месту назначения и не меняет падеж прямого объекта: Dávam knihu do tašky."],
      table: { headers: ["Куда внутрь?", "Готовая фраза", "По-русски"], rows: [
        ["taška → do tašky", "Dávam zošit do tašky.", "Кладу тетрадь в сумку."], ["vrecko → do vrecka", "Dávam kľúče do vrecka.", "Кладу ключи в карман."],
        ["chladnička → do chladničky", "Dávam mlieko do chladničky.", "Ставлю молоко в холодильник."], ["izba → do izby", "Vchádzam do izby.", "Вхожу в комнату."], ["auto → do auta", "Nastupujem do auta.", "Сажусь в машину."],
      ] },
      items: ["Čo dávam? Knihu — Akuzatív.", "Kam? Do tašky — Genitív.", "Idem domov — иду домой; Som doma — я дома; Vchádzam do domu — вхожу в здание.", "Vraciame sa do hotela: не пропускайте sa."],
      note: "В упражнениях используйте настоящее dávam; форма dám относится к будущему результату.",
    },
    {
      title: "Двадцать фраз для практики",
      paragraphs: ["Читайте вслух, подчёркивайте do + Genitív и восстанавливайте словацкую фразу по переводу."],
      table: { headers: ["Slovensky", "По-русски"], rows: [
        ["Ráno idem do práce.", "Утром я иду на работу."], ["Potom idem do banky.", "Потом я иду в банк."], ["Ideme do obchodu.", "Мы идём в магазин."], ["Lucia ide do školy.", "Луция идёт в школу."],
        ["Peter ide do nemocnice.", "Петер идёт в больницу."], ["Večer ideme do kina.", "Вечером мы идём в кино."], ["Idú do divadla.", "Они идут в театр."], ["Ideme do centra.", "Мы идём в центр."],
        ["Vraciame sa do hotela.", "Мы возвращаемся в отель."], ["Idem do parku.", "Я иду в парк."], ["Cestujem do Bratislavy.", "Я еду в Братиславу."], ["Cestujeme do Prahy.", "Мы едем в Прагу."],
        ["Anna cestuje do Viedne.", "Анна едет в Вену."], ["Cestujeme do Košíc.", "Мы едем в Кошице."], ["Ideme do Tatier.", "Мы едем в Татры."], ["Dávam knihu do tašky.", "Я кладу книгу в сумку."],
        ["Dávam telefón do vrecka.", "Я кладу телефон в карман."], ["Dávam syr do chladničky.", "Я кладу сыр в холодильник."], ["Nastupujem do auta.", "Я сажусь в машину."], ["Vchádzam do izby.", "Я вхожу в комнату."],
      ] },
      items: ["Kam ideš? — Do obchodu. A ty?", "Idem domov."],
      note: "Глаголы маршрута: idem/ideme, cestujem/cestujeme, vraciam sa/vraciame sa.",
    },
    {
      title: "Ошибки и самопроверка",
      table: { headers: ["Ошибка", "Правильно", "Почему"], rows: [
        ["Cestujem do Praha.", "Cestujem do Prahy.", "После do нужен Genitív."], ["Dávam kniha do taška.", "Dávam knihu do tašky.", "Объект в A, направление в G."],
        ["Vraciame do hotela.", "Vraciame sa do hotela.", "Нужно сохранить sa."], ["Som do školy.", "Som v škole.", "Для места нужен ответ на Kde?."],
      ] },
      items: ["После do проверьте форму Genitívu.", "Спросите: Kde? или Kam?", "Для «домой» используйте domov без do.", "В фразе с dávam отдельно найдите объект в Akuzatíve."],
      note: "Четыре опоры: Kam? + do + G; v škole → do školy; hotel → hotela; knihu (A) → do tašky (G).",
    },
  ],
  stepPractices: [
    { id: "m4-genitive-do-step-1", sectionIndex: 0, type: "pairs", prompt: "Выберите правильный вариант.", answer: "školy; v meste; hotela; domov", pairs: [
      { prompt: "Idem do (škola)", answer: "školy", options: ["škola", "školy"] }, { prompt: "Sme…", answer: "v meste", options: ["v meste", "do mesta"] },
      { prompt: "Ideme do (hotel)", answer: "hotela", options: ["hotelu", "hotela"] }, { prompt: "Idem…", answer: "domov", options: ["domov", "do domov"] },
    ], hint: "Различите место, направление и domov.", explanation: "Правильно: do školy; v meste; do hotela; domov." },
    { id: "m4-genitive-do-step-2", sectionIndex: 1, type: "pairs", prompt: "Напишите сочетание с do.", answer: "do práce; do nemocnice; do centra; do Viedne; do Košíc; do Tatier", pairs: [
      { prompt: "práca", answer: "do práce", inputHint: "Введите сочетание" }, { prompt: "nemocnica", answer: "do nemocnice", inputHint: "Введите сочетание" }, { prompt: "centrum", answer: "do centra", inputHint: "Введите сочетание" },
      { prompt: "Viedeň", answer: "do Viedne", inputHint: "Введите сочетание" }, { prompt: "Košice", answer: "do Košíc", inputHint: "Введите сочетание" }, { prompt: "Tatry", answer: "do Tatier", inputHint: "Введите сочетание" },
    ], hint: "Введите do и форму Genitívu.", explanation: "Формы: do práce, nemocnice, centra, Viedne, Košíc, Tatier." },
    { id: "m4-genitive-do-step-3", sectionIndex: 2, type: "pairs", prompt: "Назовите направление внутрь.", answer: "do tašky; do vrecka; do chladničky; do izby; do auta", pairs: [
      { prompt: "taška", answer: "do tašky", inputHint: "Введите сочетание" }, { prompt: "vrecko", answer: "do vrecka", inputHint: "Введите сочетание" }, { prompt: "chladnička", answer: "do chladničky", inputHint: "Введите сочетание" },
      { prompt: "izba", answer: "do izby", inputHint: "Введите сочетание" }, { prompt: "auto", answer: "do auta", inputHint: "Введите сочетание" },
    ], hint: "После do поставьте название контейнера в Genitív.", explanation: "Формы: do tašky, vrecka, chladničky, izby, auta." },
    { id: "m4-genitive-do-step-4", sectionIndex: 3, type: "pairs", prompt: "Переведите на словацкий.", answer: "Ideme do obchodu.; Dávam mlieko do chladničky.; Vraciame sa do hotela.; Idem domov.", pairs: [
      { prompt: "Мы идём в магазин.", answer: "Ideme do obchodu.", acceptableAnswers: ["My ideme do obchodu."], inputHint: "Введите перевод" },
      { prompt: "Я кладу молоко в холодильник.", answer: "Dávam mlieko do chladničky.", acceptableAnswers: ["Ja dávam mlieko do chladničky."], inputHint: "Введите перевод" },
      { prompt: "Мы возвращаемся в отель.", answer: "Vraciame sa do hotela.", acceptableAnswers: ["My sa vraciame do hotela."], inputHint: "Введите перевод" },
      { prompt: "Я иду домой.", answer: "Idem domov.", acceptableAnswers: ["Ja idem domov."], inputHint: "Введите перевод" },
    ], hint: "Проверьте do + G, sa и domov.", explanation: "Модели: do obchodu, do chladničky, vraciame sa do hotela, idem domov." },
    { id: "m4-genitive-do-step-5", sectionIndex: 4, type: "pairs", prompt: "Исправьте ошибки.", answer: "Cestujem do Prahy.; Dávam knihu do tašky.; Vraciame sa do hotela.; Som v škole.", pairs: [
      { prompt: "Cestujem do Praha.", answer: "Cestujem do Prahy.", inputHint: "Введите исправленную фразу" }, { prompt: "Dávam kniha do taška.", answer: "Dávam knihu do tašky.", inputHint: "Введите исправленную фразу" },
      { prompt: "Vraciame do hotela.", answer: "Vraciame sa do hotela.", inputHint: "Введите исправленную фразу" }, { prompt: "Som do školy. — смысл: я в школе", answer: "Som v škole.", inputHint: "Введите исправленную фразу" },
    ], hint: "Проверьте падежи, sa и Kde/Kam.", explanation: "Правильно: do Prahy; knihu do tašky; vraciame sa; som v škole." },
  ],
  assessmentMode: "interactive",
  materialAssessmentStep: false,
  reinforcementLabel: "Финальный тест темы",
  reinforcementTitle: "Выполните шесть заданий темы 7",
  reinforcementPractices: [
    { id: "reinforcement:genitive-do:1", sectionIndex: 0, type: "pairs", prompt: "Выберите правильный вариант.", answer: "školy; v meste; hotela; domov", pairs: [
      { prompt: "Idem do (škola)", answer: "školy", options: ["škola", "školy"] }, { prompt: "Sme…", answer: "v meste", options: ["v meste", "do mesta"] }, { prompt: "Ideme do (hotel)", answer: "hotela", options: ["hotelu", "hotela"] }, { prompt: "Idem…", answer: "domov", options: ["domov", "do domov"] },
    ], hint: "Выберите форму по смыслу.", explanation: "Правильно: školy, v meste, hotela, domov." },
    { id: "reinforcement:genitive-do:2", sectionIndex: 1, type: "pairs", prompt: "Напишите сочетание с do.", answer: "do práce; do nemocnice; do centra; do Viedne; do Košíc; do Tatier", pairs: [
      { prompt: "práca", answer: "do práce", inputHint: "Введите сочетание" }, { prompt: "nemocnica", answer: "do nemocnice", inputHint: "Введите сочетание" }, { prompt: "centrum", answer: "do centra", inputHint: "Введите сочетание" },
      { prompt: "Viedeň", answer: "do Viedne", inputHint: "Введите сочетание" }, { prompt: "Košice", answer: "do Košíc", inputHint: "Введите сочетание" }, { prompt: "Tatry", answer: "do Tatier", inputHint: "Введите сочетание" },
    ], hint: "После do нужен Genitív.", explanation: "Формы: do práce, nemocnice, centra, Viedne, Košíc, Tatier." },
    { id: "reinforcement:genitive-do:3", sectionIndex: 1, type: "pairs", prompt: "Превратите «где?» в «куда?».", answer: "do banky; do hotela; do kina; do Bratislavy; na poštu", pairs: [
      { prompt: "v banke", answer: "do banky", inputHint: "Введите направление" }, { prompt: "v hoteli", answer: "do hotela", inputHint: "Введите направление" }, { prompt: "v kine", answer: "do kina", inputHint: "Введите направление" },
      { prompt: "v Bratislave", answer: "do Bratislavy", inputHint: "Введите направление" }, { prompt: "na pošte", answer: "na poštu", inputHint: "Введите направление" },
    ], hint: "Не каждое направление использует do.", explanation: "Правильно: do banky, hotela, kina, Bratislavy; na poštu." },
    { id: "reinforcement:genitive-do:4", sectionIndex: 4, type: "pairs", prompt: "Исправьте ошибки.", answer: "Cestujem do Prahy.; Dávam knihu do tašky.; Vraciame sa do hotela.; Som v škole.", pairs: [
      { prompt: "Cestujem do Praha.", answer: "Cestujem do Prahy.", inputHint: "Введите исправленную фразу" }, { prompt: "Dávam kniha do taška.", answer: "Dávam knihu do tašky.", inputHint: "Введите исправленную фразу" },
      { prompt: "Vraciame do hotela.", answer: "Vraciame sa do hotela.", inputHint: "Введите исправленную фразу" }, { prompt: "Som do školy. — смысл: я в школе", answer: "Som v škole.", inputHint: "Введите исправленную фразу" },
    ], hint: "Исправьте только нарушенную модель.", explanation: "Правильно: Cestujem do Prahy; Dávam knihu do tašky; Vraciame sa do hotela; Som v škole." },
    { id: "reinforcement:genitive-do:5", sectionIndex: 3, type: "pairs", prompt: "Переведите на словацкий.", answer: "Ideme do obchodu.; Dávam mlieko do chladničky.; Vraciame sa do hotela.; Idem domov.", pairs: [
      { prompt: "Мы идём в магазин.", answer: "Ideme do obchodu.", acceptableAnswers: ["My ideme do obchodu."], inputHint: "Введите перевод" },
      { prompt: "Я кладу молоко в холодильник.", answer: "Dávam mlieko do chladničky.", acceptableAnswers: ["Ja dávam mlieko do chladničky."], inputHint: "Введите перевод" },
      { prompt: "Мы возвращаемся в отель.", answer: "Vraciame sa do hotela.", acceptableAnswers: ["My sa vraciame do hotela."], inputHint: "Введите перевод" },
      { prompt: "Я иду домой.", answer: "Idem domov.", acceptableAnswers: ["Ja idem domov."], inputHint: "Введите перевод" },
    ], hint: "Проверьте формы после do.", explanation: "Модели: Ideme do obchodu; Dávam mlieko do chladničky; Vraciame sa do hotela; Idem domov." },
    { id: "reinforcement:genitive-do:6", sectionIndex: 3, type: "pairs", prompt: "Выберите пять фраз маршрута.", answer: "Ráno idem do práce.; Potom idem do banky.; Idem do obchodu.; Večer idem do kina.; Doma dávam mlieko do chladničky.", pairs: [
      { prompt: "утром — работа", answer: "Ráno idem do práce.", options: ["Ráno idem v práci.", "Ráno idem do práce.", "Ráno idem do práca."] },
      { prompt: "потом — банк", answer: "Potom idem do banky.", options: ["Potom idem do banka.", "Potom idem v banke.", "Potom idem do banky."] },
      { prompt: "магазин", answer: "Idem do obchodu.", options: ["Idem do obchodu.", "Idem do obchod.", "Som do obchodu."] },
      { prompt: "вечером — кино", answer: "Večer idem do kina.", options: ["Večer som do kina.", "Večer idem do kina.", "Večer idem v kine."] },
      { prompt: "молоко — холодильник", answer: "Doma dávam mlieko do chladničky.", options: ["Doma dávam mlieka do chladnička.", "Doma dávam mlieko v chladničke.", "Doma dávam mlieko do chladničky."] },
    ], hint: "Каждая строка закрепляет часть открытого маршрута.", explanation: "Выбран маршрут с четырьмя местами и одним контейнером." },
  ],
  knowledgeChecks: [
    { id: "m4-genitive-do-check-1", question: "Как правильно сказать «Я иду в школу»?", options: ["Idem v škole.", "Idem do školy.", "Idem do škola."], answer: "Idem do školy.", explanation: "Цель отвечает на Kam? и требует do + Genitív." },
    { id: "m4-genitive-do-check-2", question: "Какая пара различает место и цель?", options: ["v hoteli — do hotela", "v hotela — do hoteli", "do hoteli — v hotela"], answer: "v hoteli — do hotela", explanation: "Kde? v hoteli; Kam? do hotela." },
    { id: "m4-genitive-do-check-3", question: "Как разобрать Dávam knihu do tašky?", options: ["knihu — A; do tašky — G", "оба слова — G", "knihu — N; do tašky — A"], answer: "knihu — A; do tašky — G", explanation: "Что кладём — Akuzatív; куда — do + Genitív." },
  ],
  finalChecks: [
    { id: "m4-genitive-do-final-1", question: "Переведите: «Я еду в Братиславу».", options: ["Cestujem do Bratislavy.", "Cestujem v Bratislave.", "Cestujem do Bratislava."], answer: "Cestujem do Bratislavy.", explanation: "После do название города получает форму Bratislavy." },
  ],
  chatPrompt: "Опишите маршрут: четыре места с do и одна вещь, которую вы кладёте внутрь сумки, кармана или холодильника.",
  chatSuggestions: ["Ráno idem do práce. Potom idem do banky.", "Večer idem do kina.", "Doma dávam mlieko do chladničky."],
} satisfies CourseLesson;
