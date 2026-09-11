import type { CourseLesson } from "../../../courseTypes";
import { defineModule4Lesson } from "../lessonFactory";

const baseLocativeVNaLesson = defineModule4Lesson("locative-v-na", 3, {
  summary: "Lokál после v/vo и na отвечает на Kde? и описывает место человека, предмета или действия, а не направление.",
  model: "Kde? + v/vo или na + Lokál: Adam je v hoteli. Som na pošte. Sedím vo vlaku.",
  goals: ["Задавать Kde?", "Выбирать v/vo или na", "Употреблять частотные формы Lokálu", "Описывать место в единственном и множественном числе"],
  rules: [
    "V/vo обычно обозначает нахождение внутри, во многих помещениях, городах и странах: v škole, v meste.",
    "Na используется с поверхностями и рядом закреплённых мест: na stole, na pošte, na stanici, na Slovensku.",
    "Vo облегчает произношение перед некоторыми словами на v- и f-: vo vlaku, vo firme, vo fľaši.",
    "Форму нельзя надёжно угадать по последней букве: hotel → v hoteli, park → v parku, námestie → na námestí.",
    "Во множественном числе частотны -och, -ách и -iach: v obchodoch, v školách, na uliciach.",
    "Не выбирайте предлог по русскому переводу: v škole, но na univerzite и na Slovensku.",
  ],
  examples: [
    { slovak: "Adam je v škole.", russian: "Адам в школе." },
    { slovak: "Sedím vo vlaku.", russian: "Я сижу в поезде." },
    { slovak: "Mama je na pošte.", russian: "Мама на почте." },
    { slovak: "Kľúče sú na stole.", russian: "Ключи на столе." },
    { slovak: "Priatelia bývajú v Košiciach.", russian: "Друзья живут в Кошице." },
  ],
  primaryTitle: "Формы единственного числа",
  primaryTable: { headers: ["Модель", "Словарная форма", "Сочетание в Lokáli"], rows: [["женский: -e", "škola / banka / pošta", "v škole / v banke / na pošte"], ["женский: -i", "práca / ulica / stanica", "v práci / na ulici / na stanici"], ["мужской: -e", "obchod / stôl", "v obchode / na stole"], ["мужской: -i", "hotel", "v hoteli"], ["мужской: -u", "park / vlak", "v parku / vo vlaku"], ["средний: -e", "mesto / auto / centrum", "v meste / v aute / v centre"], ["средний: -í", "námestie", "na námestí"], ["страна", "Slovensko", "na Slovensku"]] },
  secondaryTitle: "Vo и множественное число",
  secondaryTable: { headers: ["Сигнал", "Форма", "Примеры"], rows: [["обычная форма", "v", "v škole, v práci, v banke"], ["удобное произношение", "vo", "vo vlaku, vo firme, vo fľaši"], ["мужской, мн. ч.", "-och", "v obchodoch, v hoteloch"], ["женский, мн. ч.", "-ách/-iach", "v školách, na uliciach"], ["средний, мн. ч.", "-ách", "v mestách, v autách"], ["Košice", "-iach", "v Košiciach"]] },
  boundaryItems: ["Som na pošte — Kde? + Lokál.", "Idem na poštu — Kam? + Akuzatív.", "Bežím v parku: движение происходит где-то, поэтому нужен Lokál.", "Čakám na stanici — место; Čakám na sestru — человек, которого ждут."],
  mistake: "Не оставляйте словарную форму и не смешивайте место с направлением: Som v škole, не v škola и не idem do školy.",
  task: "Опишите, где находятся люди и предметы; используйте v, vo, na и одну форму множественного числа.",
  productionPrompt: "Переведите: «Мы в школе».",
  productionAnswer: "Sme v škole.",
  productionHint: "Местонахождение отвечает на Kde? и использует сочетание v škole.",
});

export const locativeVNaLesson = {
  vocabulary: [
    {"word":"Adam je v škole.","translation":"Адам в школе.","example":"Adam je v škole."},
    {"word":"Sedím vo vlaku.","translation":"Я сижу в поезде.","example":"Sedím vo vlaku."},
    {"word":"Mama je na pošte.","translation":"Мама на почте.","example":"Mama je na pošte."},
    {"word":"Kľúče sú na stole.","translation":"Ключи на столе.","example":"Kľúče sú na stole."},
    {"word":"Turisti sú v hoteloch.","translation":"Туристы в отелях.","example":"Turisti sú v hoteloch."},
    {"word":"Priatelia bývajú v Košiciach.","translation":"Друзья живут в Кошице.","example":"Priatelia bývajú v Košiciach."},
  ],
  ...baseLocativeVNaLesson,
  description: "Отвечайте на Kde?, выбирайте устойчивое сочетание с v/vo или na и форму места в Lokáli.",
  duration: "35–40 мин",
  goals: [
    "Задавать вопрос Kde? о человеке или предмете",
    "Использовать привычные сочетания с v/vo и na",
    "Подбирать форму места в единственном и множественном числе",
    "Составлять короткие фразы о местонахождении",
  ],
  theory: {
    summary: "Lokál (L) — местный падеж, близкий по употреблению к русскому предложному. Он всегда используется с предлогом. В этой теме v/vo + Lokál и na + Lokál отвечают на kde? — «где?»: Kde je Adam? — Adam je v hoteli.",
    rules: [
      "V/vo обычно обозначает нахождение внутри, во многих помещениях, городах и странах; na используется с поверхностями и рядом учреждений, событий и названий мест.",
      "Учите место вместе с предлогом: v škole, v obchode, v Bratislave, но na univerzite, na pošte, na Slovensku.",
      "Kde? и Kam? различают место и цель: Som na pošte — Kde? + Lokál; Idem na poštu — Kam? + Akuzatív.",
      "У Lokálu нет одного окончания: škola → v škole, práca → v práci, hotel → v hoteli, park → v parku, mesto → v meste, námestie → na námestí.",
      "Vo — форма того же предлога v, удобная перед некоторыми словами на v- и f-: vo vlaku, vo firme, vo fľaši. Смысл и падеж не меняются.",
      "Во множественном числе учите готовые пары: obchody → v obchodoch, školy → v školách, ulice → na uliciach, mestá → v mestách.",
      "Сам предлог na не определяет падеж: Čakám na stanici отвечает на Kde? и использует Lokál; Čakám na sestru отвечает на Na koho? и использует Akuzatív.",
    ],
    examples: [
      { slovak: "Adam je v škole.", russian: "Адам в школе.", explanation: "Место внутри учреждения: v + Lokál." },
      { slovak: "Sedím vo vlaku.", russian: "Я сижу в поезде.", explanation: "Перед vlak используется удобная форма vo; падеж остаётся Lokál." },
      { slovak: "Mama je na pošte.", russian: "Мама на почте.", explanation: "Pošta употребляется в готовом сочетании na pošte." },
      { slovak: "Kľúče sú na stole.", russian: "Ключи на столе.", explanation: "Поверхность выражается сочетанием na stole; в основе меняется гласная." },
      { slovak: "Turisti sú v hoteloch.", russian: "Туристы в отелях.", explanation: "Множественная форма hotely → v hoteloch." },
      { slovak: "Priatelia bývajú v Košiciach.", russian: "Друзья живут в Кошице.", explanation: "Название одного города имеет форму множественного числа: Košice → v Košiciach." },
    ],
  },
  sections: [
    {
      title: "Где? Выбираем предлог",
      paragraphs: [
        "V/vo и na с Lokálom отвечают на Kde?. Русское «в» не выбирает словацкий предлог: сравните v škole и na univerzite.",
        "Движение тоже может происходить где-то: Bežím v parku. Здесь v parku обозначает место действия, а не направление.",
      ],
      table: { headers: ["Предлог", "Ориентир для A1", "Пример"], rows: [
        ["v / vo", "внутри; во многих помещениях, городах и странах", "Som v banke."],
        ["na", "на поверхности; с рядом учреждений, событий и мест", "Som na pošte."],
      ] },
      items: ["v škole; v obchode; v meste; v Bratislave; vo vlaku", "na univerzite; na pošte; na stanici; na Slovensku; na stole", "Som na pošte — Kde?; Idem na poštu — Kam?"],
      note: "У некоторых мест другой предлог возможен с иным оттенком значения. На A1 запоминайте обычные сочетания целиком.",
    },
    {
      title: "Формы единственного числа",
      paragraphs: ["Учите пару «словарная форма → сочетание места». Одной последней буквы недостаточно для выбора окончания."],
      table: { headers: ["Модель", "Словарная форма", "Готовое сочетание"], rows: [
        ["женский: -e", "škola; banka; pošta", "v škole; v banke; na pošte"], ["женский: -i", "práca; ulica; stanica", "v práci; na ulici; na stanici"],
        ["мужской: -e", "obchod; stôl", "v obchode; na stole"], ["мужской: -i", "hotel", "v hoteli"], ["мужской: -u", "park; vlak", "v parku; vo vlaku"],
        ["средний: -e", "mesto; auto; centrum", "v meste; v aute; v centre"], ["средний: -í", "námestie", "na námestí"], ["страна", "Slovensko", "na Slovensku"],
      ] },
      items: ["Stôl → na stole: меняется гласная основы.", "Centrum → v centre: -um не сохраняется.", "Na námestí пишется с долгим í.", "Som v centre. Bývam v meste. Pracujem v obchode. Študujem na univerzite."],
      note: "В фразах Adam je v práci и Deti sú v škole нужны je/sú, хотя русская связка обычно отсутствует.",
    },
    {
      title: "Vo и множественное число",
      paragraphs: [
        "V и vo — две формы одного предлога. Vo облегчает произношение перед некоторыми словами на v- и f-; не добавляйте o перед любой группой согласных.",
        "Не прибавляйте окончания к готовому множественному числу: hotely → hoteloch, не hotelyoch.",
      ],
      table: { headers: ["Nominatív, мн. ч.", "Lokál с предлогом", "Перевод"], rows: [
        ["obchody", "v obchodoch", "в магазинах"], ["hotely", "v hoteloch", "в отелях"], ["školy", "v školách", "в школах"],
        ["ulice", "na uliciach", "на улицах"], ["mestá", "v mestách", "в городах"], ["autá", "v autách", "в машинах"], ["Košice", "v Košiciach", "в Кошице"],
      ] },
      items: ["С v: v škole, v práci, v banke.", "С vo: vo vlaku, vo firme, vo fľaši.", "Частотная карта: v obchodoch, v školách, na uliciach.", "Čakám na stanici — место ожидания; Čakám na sestru — человек, которого ждут."],
      note: "Košice называют один город, но имеют форму множественного числа. Сочетание v Košiciach лучше запомнить целиком.",
    },
    {
      title: "Двадцать фраз о месте",
      paragraphs: ["Читайте вслух, затем закройте перевод и восстановите смысл. Каждое выделенное сочетание отвечает на Kde?."],
      table: { headers: ["Slovensky", "По-русски"], rows: [
        ["Adam je v škole.", "Адам в школе."], ["Lucia je v práci.", "Луция на работе."], ["Bývam v Bratislave.", "Я живу в Братиславе."],
        ["Pracujem v obchode.", "Я работаю в магазине."], ["Sme v hoteli.", "Мы в отеле."], ["Sedím vo vlaku.", "Я сижу в поезде."],
        ["Voda je vo fľaši.", "Вода в бутылке."], ["Sestra pracuje vo firme.", "Сестра работает в компании."], ["Deti sú v parku.", "Дети в парке."],
        ["Telefón je v aute.", "Телефон в машине."], ["Mama je na pošte.", "Мама на почте."], ["Čakám na stanici.", "Я жду на вокзале."],
        ["Študujem na univerzite.", "Я учусь в университете."], ["Teraz som na Slovensku.", "Сейчас я в Словакии."], ["Kľúče sú na stole.", "Ключи на столе."],
        ["Sme na námestí.", "Мы на площади."], ["Peter je na koncerte.", "Петер на концерте."], ["Autá sú na uliciach.", "Машины на улицах."],
        ["Turisti sú v hoteloch.", "Туристы в отелях."], ["Priatelia bývajú v Košiciach.", "Друзья живут в Кошице."],
      ] },
      items: ["Kde si? — Som v centre.", "A kde je Lucia? — Je na pošte."],
      note: "В вопросе Kde si? форма si относится к «ты». В ответе о себе используйте som.",
    },
    {
      title: "Ошибки и самопроверка",
      table: { headers: ["Ошибка", "Правильно", "Почему"], rows: [
        ["Som v škola.", "Som v škole.", "Нужна падежная форма."], ["Som v vlaku.", "Som vo vlaku.", "Здесь используется vo."],
        ["Som na poštu.", "Som na pošte.", "Местонахождение требует Lokál."], ["Kľúče sú v stole.", "Kľúče sú na stole.", "Ключи лежат на поверхности."],
      ] },
      items: ["Подчеркните предлог и форму места.", "Спросите: где или куда?", "Проверьте единственное или множественное число.", "Сверьте сочетание с таблицей."],
      note: "Перед финальным тестом повторите четыре опоры: Kde? → предлог вместе с местом → форма v/vo → число и окончание Lokálu.",
    },
  ],
  stepPractices: [
    { id: "m4-locative-v-na-step-1", sectionIndex: 0, type: "pairs", prompt: "Выберите v, vo или na.", answer: "v; na; vo; na; vo", pairs: [
      { prompt: "___ škole", answer: "v", options: ["v", "vo", "na"] }, { prompt: "___ pošte", answer: "na", options: ["v", "vo", "na"] },
      { prompt: "___ vlaku", answer: "vo", options: ["v", "vo", "na"] }, { prompt: "___ Slovensku", answer: "na", options: ["v", "vo", "na"] },
      { prompt: "___ firme", answer: "vo", options: ["v", "vo", "na"] },
    ], hint: "Вспомните готовое сочетание места.", explanation: "Правильно: v škole, na pošte, vo vlaku, na Slovensku, vo firme." },
    { id: "m4-locative-v-na-step-2", sectionIndex: 1, type: "pairs", prompt: "Поставьте слово в Lokál единственного числа.", answer: "v hoteli; v parku; na stanici; na námestí; v centre; na stole", pairs: [
      { prompt: "v (hotel)", answer: "v hoteli", inputHint: "Введите сочетание целиком" }, { prompt: "v (park)", answer: "v parku", inputHint: "Введите сочетание целиком" },
      { prompt: "na (stanica)", answer: "na stanici", inputHint: "Введите сочетание целиком" }, { prompt: "na (námestie)", answer: "na námestí", inputHint: "Введите сочетание целиком" },
      { prompt: "v (centrum)", answer: "v centre", inputHint: "Введите сочетание целиком" }, { prompt: "na (stôl)", answer: "na stole", inputHint: "Введите сочетание целиком" },
    ], hint: "Учите предлог и форму места одним блоком.", explanation: "Правильно: v hoteli, v parku, na stanici, na námestí, v centre, na stole." },
    { id: "m4-locative-v-na-step-3", sectionIndex: 2, type: "pairs", prompt: "Дополните формы Lokálu множественного числа.", answer: "v obchodoch; v mestách; na uliciach; v školách; v Košiciach", pairs: [
      { prompt: "v (obchody)", answer: "v obchodoch", inputHint: "Введите сочетание целиком" }, { prompt: "v (mestá)", answer: "v mestách", inputHint: "Введите сочетание целиком" },
      { prompt: "na (ulice)", answer: "na uliciach", inputHint: "Введите сочетание целиком" }, { prompt: "v (školy)", answer: "v školách", inputHint: "Введите сочетание целиком" },
      { prompt: "v (Košice)", answer: "v Košiciach", inputHint: "Введите сочетание целиком" },
    ], hint: "Число не меняйте; вспомните окончания -och, -ách и -iach.", explanation: "Правильно: v obchodoch, v mestách, na uliciach, v školách, v Košiciach." },
    { id: "m4-locative-v-na-step-4", sectionIndex: 3, type: "choice", prompt: "Как по-словацки: «Друзья живут в Кошице»?", options: ["Priatelia bývajú v Košice.", "Priatelia bývajú v Košiciach.", "Priatelia bývajú na Košiciach."], answer: "Priatelia bývajú v Košiciach.", hint: "Название Košice имеет форму множественного числа.", explanation: "Готовое сочетание места: v Košiciach." },
    { id: "m4-locative-v-na-step-5", sectionIndex: 4, type: "pairs", prompt: "Исправьте фразы по смыслу.", answer: "Som na pošte.; Kľúče sú na stole.; Sedím vo vlaku.; Bývam v Bratislave.", pairs: [
      { prompt: "Som na poštu.", answer: "Som na pošte.", inputHint: "Введите исправленную фразу" },
      { prompt: "Kľúče sú v stole.", answer: "Kľúče sú na stole.", inputHint: "Введите исправленную фразу" },
      { prompt: "Sedím v vlaku.", answer: "Sedím vo vlaku.", inputHint: "Введите исправленную фразу" },
      { prompt: "Bývam v Bratislava.", answer: "Bývam v Bratislave.", inputHint: "Введите исправленную фразу" },
    ], hint: "Проверьте вопрос Kde?, предлог и форму места.", explanation: "Правильно: na pošte, na stole, vo vlaku, v Bratislave." },
  ],
  assessmentMode: "interactive",
  materialAssessmentStep: false,
  reinforcementLabel: "Финальный тест темы",
  reinforcementTitle: "Выполните шесть заданий темы 4",
  reinforcementPractices: [
    { id: "reinforcement:locative-v-na:1", sectionIndex: 0, type: "pairs", prompt: "Вставьте v, vo или na.", answer: "v; na; vo; na; vo", pairs: [
      { prompt: "___ škole", answer: "v", options: ["v", "vo", "na"] }, { prompt: "___ pošte", answer: "na", options: ["v", "vo", "na"] },
      { prompt: "___ vlaku", answer: "vo", options: ["v", "vo", "na"] }, { prompt: "___ Slovensku", answer: "na", options: ["v", "vo", "na"] },
      { prompt: "___ firme", answer: "vo", options: ["v", "vo", "na"] },
    ], hint: "Выбирайте по готовому сочетанию места.", explanation: "Правильно: v škole, na pošte, vo vlaku, na Slovensku, vo firme." },
    { id: "reinforcement:locative-v-na:2", sectionIndex: 1, type: "pairs", prompt: "Поставьте слово в Lokál единственного числа.", answer: "v hoteli; v parku; na stanici; na námestí; v centre; na stole", pairs: [
      { prompt: "v (hotel)", answer: "v hoteli", inputHint: "Введите сочетание целиком" }, { prompt: "v (park)", answer: "v parku", inputHint: "Введите сочетание целиком" },
      { prompt: "na (stanica)", answer: "na stanici", inputHint: "Введите сочетание целиком" }, { prompt: "na (námestie)", answer: "na námestí", inputHint: "Введите сочетание целиком" },
      { prompt: "v (centrum)", answer: "v centre", inputHint: "Введите сочетание целиком" }, { prompt: "na (stôl)", answer: "na stole", inputHint: "Введите сочетание целиком" },
    ], hint: "Не угадывайте по одной последней букве; вспомните сочетание из таблицы.", explanation: "Правильно: v hoteli, v parku, na stanici, na námestí, v centre, na stole." },
    { id: "reinforcement:locative-v-na:3", sectionIndex: 2, type: "pairs", prompt: "Дополните формы Lokálu множественного числа.", answer: "v obchodoch; v mestách; na uliciach; v školách; v Košiciach", pairs: [
      { prompt: "v (obchody)", answer: "v obchodoch", inputHint: "Введите сочетание целиком" }, { prompt: "v (mestá)", answer: "v mestách", inputHint: "Введите сочетание целиком" },
      { prompt: "na (ulice)", answer: "na uliciach", inputHint: "Введите сочетание целиком" }, { prompt: "v (školy)", answer: "v školách", inputHint: "Введите сочетание целиком" },
      { prompt: "v (Košice)", answer: "v Košiciach", inputHint: "Введите сочетание целиком" },
    ], hint: "Сохраните множественное число.", explanation: "Формы: obchodoch, mestách, uliciach, školách, Košiciach." },
    { id: "reinforcement:locative-v-na:4", sectionIndex: 4, type: "pairs", prompt: "Исправьте фразы по смыслу.", answer: "Som na pošte.; Kľúče sú na stole.; Sedím vo vlaku.; Bývam v Bratislave.", pairs: [
      { prompt: "Som na poštu.", answer: "Som na pošte.", inputHint: "Введите исправленную фразу" },
      { prompt: "Kľúče sú v stole.", answer: "Kľúče sú na stole.", inputHint: "Введите исправленную фразу" },
      { prompt: "Sedím v vlaku.", answer: "Sedím vo vlaku.", inputHint: "Введите исправленную фразу" },
      { prompt: "Bývam v Bratislava.", answer: "Bývam v Bratislave.", inputHint: "Введите исправленную фразу" },
    ], hint: "Проверьте смысл, предлог и падежную форму.", explanation: "Каждая строка проверяется отдельно: na pošte, na stole, vo vlaku, v Bratislave." },
    { id: "reinforcement:locative-v-na:5", sectionIndex: 3, type: "pairs", prompt: "Переведите на словацкий.", answer: "Pracujem v obchode.; Sme na námestí.; Telefón je v aute.; Priatelia bývajú v Košiciach.", pairs: [
      { prompt: "Я работаю в магазине.", answer: "Pracujem v obchode.", acceptableAnswers: ["Ja pracujem v obchode."], inputHint: "Введите перевод по-словацки" },
      { prompt: "Мы на площади.", answer: "Sme na námestí.", inputHint: "Введите перевод по-словацки" },
      { prompt: "Телефон в машине.", answer: "Telefón je v aute.", inputHint: "Введите перевод по-словацки" },
      { prompt: "Друзья живут в Кошице.", answer: "Priatelia bývajú v Košiciach.", inputHint: "Введите перевод по-словацки" },
    ], hint: "Все фразы отвечают на Kde?.", explanation: "Нормативные сочетания: v obchode, na námestí, v aute, v Košiciach." },
    { id: "reinforcement:locative-v-na:6", sectionIndex: 3, type: "pairs", prompt: "Выберите пять фраз о местонахождении.", answer: "Som v hoteli.; Adam je vo vlaku.; Lucia je na pošte.; Kľúče sú na stole.; Turisti sú v hoteloch.", pairs: [
      { prompt: "вы в отеле", answer: "Som v hoteli.", options: ["Som do hotela.", "Som v hoteli.", "Som v hotel."] },
      { prompt: "Адам в поезде", answer: "Adam je vo vlaku.", options: ["Adam je v vlak.", "Adam je do vlaku.", "Adam je vo vlaku."] },
      { prompt: "Луция на почте", answer: "Lucia je na pošte.", options: ["Lucia je na pošte.", "Lucia je na poštu.", "Lucia je v pošte."] },
      { prompt: "ключи на столе", answer: "Kľúče sú na stole.", options: ["Kľúče sú v stole.", "Kľúče sú na stôl.", "Kľúče sú na stole."] },
      { prompt: "туристы в отелях", answer: "Turisti sú v hoteloch.", options: ["Turisti sú v hotely.", "Turisti sú v hoteloch.", "Turisti sú do hotelov."] },
    ], hint: "Каждая фраза должна отвечать на Kde? и вместе использовать v, vo, na и множественное число.", explanation: "Пять выбранных фраз образуют проверяемый рассказ о местонахождении." },
  ],
  knowledgeChecks: [
    { id: "m4-locative-v-na-check-1", question: "Как правильно сказать «Я на почте»?", options: ["Som na pošte.", "Som na poštu.", "Som v pošta."], answer: "Som na pošte.", explanation: "Местонахождение отвечает на Kde? и требует готовое сочетание na pošte." },
    { id: "m4-locative-v-na-check-2", question: "Какое сочетание использует форму vo?", options: ["vo vlaku", "vo škole", "vo pošte"], answer: "vo vlaku", explanation: "Vo облегчает произношение перед словом vlak." },
    { id: "m4-locative-v-na-check-3", question: "Почему в Bežím v parku используется Lokál?", options: ["Фраза отвечает на Kde?", "Любой глагол движения требует Lokál", "После v всегда обозначается направление"], answer: "Фраза отвечает на Kde?", explanation: "Движение происходит в парке; место действия отвечает на Kde?." },
  ],
  finalChecks: [
    { id: "m4-locative-v-na-final-1", question: "Переведите: «Мы в школе».", options: ["Sme v škole.", "Sme do školy.", "Sme v škola."], answer: "Sme v škole.", explanation: "Местонахождение отвечает на Kde? и использует сочетание v škole." },
  ],
  chatPrompt: "Опишите, где находятся люди и предметы. Используйте v, vo, na и одну форму Lokálu множественного числа.",
  chatSuggestions: ["Som v hoteli. Adam je vo vlaku.", "Lucia je na pošte. Kľúče sú na stole.", "Turisti sú v hoteloch."],
} satisfies CourseLesson;
