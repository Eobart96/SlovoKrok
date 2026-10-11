import { defineA2Module5Lesson } from "../lessonFactory";

export const a2EmbeddedQuestionsLesson = defineA2Module5Lesson("a2-embedded-questions", {
  duration: "40–50 мин",
  goals: ["Встраивать вопрос в сообщение или просьбу", "Различать kto, čo, kde", "Отличать kto от который", "Сохранять порядок клитик и знак всего предложения"],
  theory: {
    summary: "Kto, čo, kde вводят неизвестную информацию внутри сообщения: Neviem, kto volal; Povedz, čo potrebuješ; Ukáž mi, kde je vchod. Знак в конце зависит от всей конструкции, не только от внутреннего вопросительного слова.",
    rules: [
      "Kto обозначает человека: Viem, kto tam pracuje — знаю, кто там работает.",
      "Čo обозначает предмет, содержание, событие или действие: Vysvetli, čo sa stalo.",
      "Kde обозначает место нахождения или действия: Neviem, kde sú moje kľúče.",
      "Косвенная часть отделяется запятой: Povedz mi, kto volal.",
      "Neviem, kde býva. — сообщение; Vieš, kde býva? — вопрос к собеседнику. Внутреннее kde не требует вопросительного знака само по себе.",
      "Обычный словацкий порядок и ранние клитики сохраняются: čo sa stalo, kde sa koná kurz, kde si môžem sadnúť.",
      "Kto вводит неизвестного человека без названного существительного; ktorý уточняет названного: Poznám človeka, ktorý tu pracuje."
    ],
    examples: [
      { slovak: "Viem, kto volal.", russian: "Знаю, кто звонил.", explanation: "Сообщение о знании, не прямой вопрос." },
      { slovak: "Neviem, čo potrebuješ.", russian: "Не знаю, что тебе нужно.", explanation: "Неизвестно содержание потребности." },
      { slovak: "Vysvetli, čo sa stalo.", russian: "Объясни, что случилось.", explanation: "Просьба с ранним sa." },
      { slovak: "Ukáž mi, kde je vchod.", russian: "Покажи мне, где вход.", explanation: "Просьба показать место." },
      { slovak: "Vieš, kde býva Eva?", russian: "Ты знаешь, где живёт Ева?", explanation: "Вся конструкция — вопрос к собеседнику." },
      { slovak: "Pamätám si, kde sme sa stretli.", russian: "Помню, где мы встретились.", explanation: "Группа sme sa внутри придаточного." },
      { slovak: "Zistím, kde sa koná kurz.", russian: "Выясню, где проходит курс.", explanation: "Статичное место проведения." }
    ]
  },
  sections: [
    { title: "Вопрос внутри сообщения или просьбы", importance: "core", paragraphs: ["Kto tam pracuje? — кто там работает? Viem, kto tam pracuje — знаю, кто там работает. Čo potrebuješ? → Neviem, čo potrebuješ — не знаю, что тебе нужно. Kde je vchod? → Ukáž mi, kde je vchod — покажи мне, где вход. Внутреннее слово сохраняет смысл неизвестной информации.", "Рамки: viem/neviem — знаю/не знаю, povedz mi — скажи мне, ukáž mi — покажи мне, pamätám si — помню, zistím — выясню. После рамки строим законченную придаточную часть, а не просто список слов."], items: ["человек → kto", "предмет/действие/содержание → čo", "место → kde"], note: "Это продолжение 5.3: утверждение передавали через že, неизвестную информацию — через вопросительное слово." },
    { title: "Kto или ktorý: неизвестный человек и уточнение", importance: "core", paragraphs: ["Neviem, kto otvoril okno — не знаю, кто открыл окно. Zistíme, kto príde — выясним, кто придёт. Kto само обозначает неизвестного человека; слово človek перед ним не требуется.", "Poznám človeka, ktorý tam pracuje — знаю человека, который там работает: уже назван человек, уточняем его. Viem, kto tam pracuje — знаю, кто там работает: знаю ответ на вопрос. В этих нейтральных моделях различаем viem + информацию и poznám + человека."], items: ["Viem, kto volal. — Знаю, кто звонил.", "Poznám muža, ktorý volal. — Знаю мужчину, который звонил."], note: "Не заменяйте kto на который только потому, что по-русски обе фразы говорят о человеке." },
    { title: "Čo: содержание и событие, не союз что", importance: "core", paragraphs: ["Povedz, čo sa stalo — скажи, что случилось. Vidím, čo robíš — вижу, что ты делаешь. Napíš, čo potrebuješ — напиши, что тебе нужно. Здесь čo спрашивает о неизвестном действии или содержании.", "Viem, že príde — знаю, что он придёт: задан факт прихода. Viem, čo prinesie — знаю, что он принесёт: известен ответ о предмете. Русское «что» в этих двух случаях выполняет разные функции; словацкий различает že и čo."], items: ["что произошло? → čo sa stalo", "что нужно? → čo potrebuješ", "что это? → čo je to"], note: "В модели čo sa stalo частица sa ранняя; не тренируем механическое stalo sa в конце придаточного." },
    { title: "Kde: место и обычный порядок слов", importance: "core", paragraphs: ["Neviem, kde sú moje kľúče — не знаю, где мои ключи. Ukáž mi, kde je recepcia — покажи, где ресепшен. Povedz mi, kde máme čakať — скажи, где нам ждать. Kde здесь отвечает на статичное «где», не на «куда» или «откуда».", "Pamätám si, kde sme sa stretli — помню, где встретились. Ukáž mi, kde si môžem sadnúť — покажи, где могу сесть. Kde sa koná kurz — где проходит курс. Учебная нейтральная опора — kde je stanica, kde býva Peter; другие порядки возможны для акцента, не называйте их автоматически ошибкой."], items: ["kde je vchod — где вход", "kde sa koná kurz — где проходит курс", "kde sme sa stretli — где мы встретились"], note: "Краткая группа строится внутри каждой придаточной части заново." },
    { title: "Запятая и знак всего предложения", importance: "core", paragraphs: ["Viem, kde býva. — знаю, где живёт: сообщение с точкой. Povedz mi, kde býva. — скажи, где живёт: нейтральная просьба с точкой. Vieš, kde býva? — ты знаешь, где живёт? Вопросительный знак здесь задаёт главная часть Vieš?.", "Pamätáš si, kde sme sa stretli? — помнишь, где встретились? Neviem, kto má kľúč. — не знаю, у кого ключ. Перед kto/čo/kde ставим запятую на границе частей. В чат-письме проверяем сами знаки, в автоматическом задании спрашиваем правило словами."], items: ["Neviem... → сообщение", "Povedz mi... → просьба", "Vieš...? / Pamätáš si...? → общий вопрос"], note: "Само внутреннее вопросительное слово не превращает всё высказывание в прямой вопрос." },
    { title: "Первый день на курсе: передаём информацию", importance: "core", paragraphs: ["Anna: Vieš, kto je náš lektor? Marek: Áno, pán Novák. Neviem však, kde je naša učebňa. Anna: Ukážem ti, kde je. Je na druhom poschodí. Marek: A vieš, čo dnes budeme robiť? — Знаешь нашего преподавателя? Да, господин Новак, но не знаю, где аудитория. Покажу, она на втором этаже. А знаешь, что будем делать сегодня?", "Neviem, kto je vedúci kurzu. Chcem zistiť, čo budeme robiť. Recepčná mi ukázala, kde je učebňa. Vieš, kto má zoznam účastníkov? Lektor vysvetlil, čo potrebujeme. — Не знаю, кто руководит курсом. Хочу выяснить, что будем делать. Сотрудница ресепшена показала аудиторию. Знаешь, у кого список участников? Преподаватель объяснил, что нам нужно."], items: ["В чате напишите 5–7 предложений о первом дне на курсе, работе или в отеле.", "Используйте kto, čo и kde хотя бы по одному разу.", "Добавьте один общий вопрос с Vieš или Pamätáš si."], note: "Ответы о реальной ситуации оцениваем по смыслу; не ограничиваем одной моделью источника." }
  ],
  stepPractices: [
    { sectionIndex: 0, type: "pairs", prompt: "Введите kto, čo или kde по указанному смыслу.", pairs: [{ prompt: "Неизвестен человек: Neviem, ___ volal.", answer: "kto" }, { prompt: "Неизвестен нужный предмет: Povedz, ___ potrebuješ.", answer: "čo" }, { prompt: "Неизвестно место: Ukáž mi, ___ je výťah.", answer: "kde" }], answer: "kto; čo; kde", showSlovakKeyboard: true, hint: "Человек, содержание, место.", explanation: "Слово отражает тип неизвестной информации." },
    { sectionIndex: 1, type: "choice", prompt: "Выберите «Я знаю человека, который здесь работает».", options: ["Poznám človeka, ktorý tu pracuje.", "Neviem, kto tu pracuje.", "Viem, čo tu robíš."], answer: "Poznám človeka, ktorý tu pracuje.", hint: "Человек назван до уточнения.", explanation: "Ktorý уточняет človeka; две другие фразы сообщают другую информацию." },
    { sectionIndex: 2, type: "text", prompt: "Неизвестно, что случилось. Вставьте слово: Vysvetli, ___ sa stalo.", answer: "čo", showSlovakKeyboard: true, hint: "Предмет вопроса — событие.", explanation: "Čo здесь обозначает неизвестное содержание, не že как связку утверждения." },
    { sectionIndex: 3, type: "order", prompt: "Соберите нейтральную учебную модель, начиная с Ukáž: «Покажи мне, где вход».", tokens: ["Ukáž", "mi,", "kde", "je", "vchod."], answer: "Ukáž mi, kde je vchod.", hint: "Рамка Ukáž mi, затем kde je...",
      explanation: "Обычная нейтральная модель; расположение слов при другом акценте может отличаться." },
    { sectionIndex: 3, type: "text", prompt: "Сохраните раннюю частицу: Zistím, kde ___ koná kurz. Введите частицу глагола konať sa.", answer: "sa", showSlovakKeyboard: true, hint: "Курс проходит — kurz sa koná.", explanation: "В придаточной модели sa сразу после kde." },
    { sectionIndex: 4, type: "choice", prompt: "Какой конечный знак нужен нейтральному сообщению Neviem, kde býva? Ответьте правилом.", options: ["Точка: сообщаю, что не знаю", "Вопросительный знак только из-за внутреннего kde", "Знак не нужен, потому что есть запятая"], answer: "Точка: сообщаю, что не знаю", hint: "Главная часть — сообщение.", explanation: "Neviem, kde býva. Вопрос собеседнику: Vieš, kde býva?" },
    { sectionIndex: 5, type: "choice", prompt: "Как спросить собеседника, помнит ли он место вашей встречи?", options: ["Pamätáš si, kde sme sa stretli?", "Pamätám si, kde sme sa stretli.", "Neviem, čo sa stalo."], answer: "Pamätáš si, kde sme sa stretli?", hint: "Ты помнишь? — Pamätáš si?", explanation: "Вопрос задаёт главная часть; kde обозначает место." },
    { sectionIndex: 5, type: "text", prompt: "Вставьте слово о содержании работы: Lektor vysvetlil, ___ potrebujeme na projekt.", answer: "čo", showSlovakKeyboard: true, hint: "Объяснил, что нам нужно.", explanation: "Čo — нужные предметы или содержание подготовки." }
  ],
  knowledgeChecks: [
    { question: "Чем отличаются Viem, že príde и Viem, čo prinesie?", options: ["Первое сообщает факт прихода, второе — что именно принесёт", "Že и čo всегда полностью одинаковы", "Первое всегда вопрос, второе всегда приказ"], answer: "Первое сообщает факт прихода, второе — что именно принесёт", explanation: "Не переводим русское что одной формой во всех случаях." },
    { question: "Где ставим запятую в Neviem kto volal?", options: ["Перед kto, на границе частей", "Между kto и volal", "После каждой буквы"], answer: "Перед kto, на границе частей", explanation: "Neviem, kto volal." },
    { question: "Какой смысл тренируем с kde?", options: ["Статичное место: где находится или происходит", "Направление куда во всех случаях", "Причину почему"], answer: "Статичное место: где находится или происходит", explanation: "Kde je učebňa — где аудитория." }
  ],
  finalChecks: [
    { question: "Выберите «Объясни, что случилось».", options: ["Vysvetli, čo sa stalo.", "Vysvetli, kto prišiel.", "Vysvetli, kde býva Eva."], answer: "Vysvetli, čo sa stalo.", explanation: "Čo обозначает событие, ранняя частица sa сохранена." },
    { question: "Как узнать у собеседника, где ресепшен?", options: ["Vieš, kde je recepcia?", "Viem, kde je recepcia.", "Vieš, kto je lektor?"], answer: "Vieš, kde je recepcia?", explanation: "Vieš? задаёт вопрос, kde вводит неизвестное место." }
  ],
  vocabulary: [
    { word: "kto", translation: "кто" }, { word: "čo", translation: "что — предмет или содержание" }, { word: "kde", translation: "где" }, { word: "vchod", translation: "вход" },
    { word: "výťah", translation: "лифт" }, { word: "učebňa", translation: "аудитория; учебный кабинет" }, { word: "lektor", translation: "преподаватель курса" }, { word: "zoznam účastníkov", translation: "список участников" },
    { word: "zistiť", translation: "выяснить" }, { word: "pamätať si", translation: "помнить" }, { word: "konať sa", translation: "проходить; состояться (о мероприятии)" }, { word: "na druhom poschodí", translation: "на втором этаже" }
  ],
  assessmentMode: "quiz",
  chatPrompt: "Попроси 5–7 предложений о первом дне на курсе, работе или в отеле, используя kto, čo, kde и общий вопрос с Vieš/Pamätáš si. Проверь неизвестную информацию против že как утверждения, kto против ktorý при названном существительном, ранние sa/sme sa/si, границу частей и конечный знак по всей конструкции. Не называй всякий иной порядок слов ошибкой: уточняй акцент. В этой теме kde статичное; не подменяй им kam/odkiaľ. Поясняй по-русски и принимай естественные варианты.",
  chatSuggestions: ["Опишу первый день на курсе", "Чем отличаются čo и že?", "Проверь kto и ktorý"]
});
