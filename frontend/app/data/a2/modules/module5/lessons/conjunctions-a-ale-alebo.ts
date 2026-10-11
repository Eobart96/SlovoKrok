import { defineA2Module5Lesson } from "../lessonFactory";

export const a2ConjunctionsLesson = defineA2Module5Lesson("a2-conjunctions-a-ale-alebo", {
  duration: "40–50 мин",
  goals: ["Добавлять факт с a", "Показывать контраст с ale", "Предлагать выбор с alebo", "Соединять короткие фразы с подходящей пунктуацией"],
  theory: {
    summary: "Союз показывает связь мыслей: a добавляет, ale противопоставляет, alebo предлагает выбор. Сначала определите смысл, затем выберите союз: русское «а» не всегда равно ale.",
    rules: [
      "A соединяет совместимые слова, признаки, факты и действия: chlieb a mlieko.",
      "Нейтральное русское «а» часто соответствует a: Ja pracujem doma a sestra pracuje v kancelárii.",
      "Ale показывает контраст или ограничение ожидания: Chcem ísť, ale nemám čas.",
      "Перед одиночным ale ставим запятую, в том числе между признаками: pekný, ale drahý.",
      "Alebo предлагает альтернативу: dnes alebo zajtra; в простой нейтральной паре запятая не нужна.",
      "Перед a запятая не ставится автоматически. Для обычного перечисления: Kúpim chlieb a syr.",
      "У alebo бывает и смысл «иначе»: Ponáhľaj sa, alebo zmeškáme vlak. Не переносите правило простой пары на любой контекст."
    ],
    examples: [
      { slovak: "Kúpim chlieb a mlieko.", russian: "Куплю хлеб и молоко.", explanation: "Два предмета в списке." },
      { slovak: "Ráno pracujem a večer študujem.", russian: "Утром я работаю, а вечером учусь.", explanation: "Нейтральное сопоставление, не препятствие." },
      { slovak: "Chcem ísť, ale nemám čas.", russian: "Хочу пойти, но у меня нет времени.", explanation: "Вторая часть ограничивает желание." },
      { slovak: "Hotel je pekný, ale drahý.", russian: "Отель красивый, но дорогой.", explanation: "Контраст признаков с запятой." },
      { slovak: "Dáš si čaj alebo kávu?", russian: "Будешь чай или кофе?", explanation: "Простой выбор двух напитков." },
      { slovak: "Zavolaj mi alebo mi napíš správu.", russian: "Позвони мне или напиши сообщение.", explanation: "Два способа связаться." },
      { slovak: "Mám voľno a chcem ísť von, ale prší.", russian: "Я свободен и хочу выйти, но идёт дождь.", explanation: "Добавление и ограничение в одной фразе." }
    ]
  },
  sections: [
    { title: "Три связи: добавление, контраст, выбор", importance: "core", paragraphs: ["Kúpim chlieb a mlieko — куплю хлеб и молоко. Hotel je pekný, ale drahý — отель красивый, но дорогой. Dáš si čaj alebo kávu? — будешь чай или кофе? Союз не украшение: он сообщает, как связаны две части.", "Перед переводом задайте вопрос: добавляю факт, называю препятствие или предлагаю два варианта? Одно русское слово не всегда подсказывает правильный словацкий союз."], items: ["добавляю → a", "ограничиваю или противопоставляю → ale", "предлагаю альтернативу → alebo"] },
    { title: "A: совместимые факты и последовательность", importance: "core", paragraphs: ["Byt je malý a útulný — квартира маленькая и уютная. Otvoril okno a zavolal Petrovi — он открыл окно и позвонил Петеру. Najprv sa najeme a potom pôjdeme von — сначала поедим, а потом выйдем. A может связывать и слова, и действия, и полные предложения.", "Ja bývam v Bratislave a brat býva v Nitre — я живу в Братиславе, а брат в Нитре. В русском «а» здесь просто сопоставляет факты. Ale добавило бы оттенок противопоставления, которого нейтральное сообщение не требует."], items: ["Ráno cvičím a večer čítam. — Утром занимаюсь, а вечером читаю.", "Sadli sme si a objednali sme si kávu. — Мы сели и заказали кофе."], note: "Проверьте, можно ли добавить «и ещё», не меняя смысла." },
    { title: "Ale: ожидание и ограничение", importance: "core", paragraphs: ["Chcem pomôcť, ale neviem ako — хочу помочь, но не знаю как. Je leto, ale dnes je chladno — лето, но сегодня холодно. Veľa som sa učil, ale test bol ťažký — я много учился, но тест был трудным. Вторая часть меняет направление мысли.", "To je dobrý nápad, ale dnes to nestihnem — это хорошая идея, но сегодня я не успею. Сначала признаём хорошее, затем мягко называем ограничение. Запятая стоит перед ale, а не после него."], items: ["Rozumiem, ale nesúhlasím. — Понимаю, но не согласен.", "Izba je čistá, ale veľmi malá. — Комната чистая, но очень маленькая."], note: "Byt je malý a útulný перечисляет признаки; Byt je malý, ale útulný подчёркивает, что уют компенсирует размер. Возможны оба смысла." },
    { title: "Alebo: предмет, время и действие", importance: "core", paragraphs: ["Stretneme sa dnes alebo zajtra? — встретимся сегодня или завтра? Môžeme ísť pešo alebo cestovať autobusom — можем пойти пешком или поехать автобусом. Выбираем между вариантами, не требуем выполнить оба.", "Prídeš večer, alebo nie? — придёшь вечером или нет? Ponáhľaj sa, alebo zmeškáme vlak — поторопись, иначе опоздаем на поезд. В противопоставленных решениях и предупреждениях возможна запятая. Наша базовая модель без запятой — нейтральная пара: čaj alebo kávu."], items: ["варианты времени: dnes alebo zajtra", "варианты транспорта: vlakom alebo autobusom", "варианты действия: zostať doma alebo ísť do kina"], note: "Не учите «перед alebo никогда нет запятой»: это неверное обобщение." },
    { title: "Запятые и проверка логики", importance: "core", paragraphs: ["Kúpime chlieb a syr. Prídeš dnes alebo zajtra? Mám čas, ale som unavený. В простом перечислении не копируем русскую пунктуацию; перед ale отмечаем контраст запятой.", "Исправляем смысл: Chcem spať, ale musím pracovať — хочу спать, но должен работать. Dáš si polievku alebo šalát? — будешь суп или салат? Для нейтрального сопоставления: Ja bývam v Košiciach a brat býva v Žiline."], items: ["сначала логика, потом союз", "ale → запятая перед союзом", "одиночные a/alebo → не добавляем запятую автоматически"], note: "Парные и повторённые союзы разберём в 5.2 отдельно." },
    { title: "План на вечер: три союза в сообщении", importance: "core", paragraphs: ["Marta: Dnes mám voľno a chcela by som ísť von. Ivan: Môžeme ísť do kina alebo na koncert. Marta: Koncert je zaujímavý, ale lístky sú drahé. Ivan: Tak pôjdeme do kina a potom si dáme večeru. — Марта свободна и хотела бы выйти; Иван предлагает кино или концерт; концерт интересный, но билеты дорогие; они выбирают кино и ужин.", "V piatok končím o piatej a potom mám voľno. Môžeme sa stretnúť v centre alebo pri stanici. Centrum je bližšie, ale býva tam veľa ľudí. Napíš mi a dohodneme sa. — В пятницу заканчиваю в пять и потом свободен. Можем встретиться в центре или у вокзала. Центр ближе, но там обычно много людей. Напиши, и договоримся."], items: ["Напишите в чате 5–7 предложений о выходном.", "Используйте a дважды, ale для ограничения и alebo для выбора.", "Проверьте, что союз отражает задуманный смысл."], note: "Свободный текст проверяется в чате; автоматические задания ниже ограничивают конкретную форму." }
  ],
  stepPractices: [
    { sectionIndex: 0, type: "pairs", prompt: "Введите союз по указанной функции.", pairs: [{ prompt: "добавление", answer: "a" }, { prompt: "контраст", answer: "ale" }, { prompt: "выбор", answer: "alebo" }], answer: "a; ale; alebo", showSlovakKeyboard: true, hint: "И / но / или.", explanation: "Сначала выбираем связь между мыслями." },
    { sectionIndex: 1, type: "text", prompt: "Нейтрально сопоставьте факты: Ráno pracujem ___ večer študujem. Введите только союз.", answer: "a", showSlovakKeyboard: true, hint: "Противопоставление не задано.", explanation: "Русское нейтральное «а» здесь соответствует a." },
    { sectionIndex: 2, type: "choice", prompt: "Как показать препятствие: хочу пойти, но нет времени?", options: ["Chcem ísť, ale nemám čas.", "Chcem ísť alebo nemám čas.", "Chcem ísť a mám čas."], answer: "Chcem ísť, ale nemám čas.", hint: "Желание ограничено отсутствием времени.", explanation: "Ale обозначает контраст, перед ним запятая." },
    { sectionIndex: 3, type: "text", prompt: "Предложите выбор: Dáš si čaj ___ kávu? Введите союз.", answer: "alebo", showSlovakKeyboard: true, hint: "Один из двух напитков.", explanation: "В нейтральной паре nebo не используем: словацкий союз — alebo." },
    { sectionIndex: 4, type: "text", prompt: "Перед каким союзом нужна запятая в Mám čas ale som unavený? Введите только союз.", answer: "ale", showSlovakKeyboard: true, hint: "Перед союзом контраста.", explanation: "Mám čas, ale som unavený. Автопроверка принимает слово-союз; написание запятой проверяем по объяснению и в чате." },
    { sectionIndex: 4, type: "choice", prompt: "Нужна ли запятая перед одиночным a в нейтральном Kúpime chlieb a syr?", options: ["Нет, это обычное перечисление двух продуктов", "Да, перед любым союзом всегда запятая", "Да, потому что a обозначает выбор одного продукта"], answer: "Нет, это обычное перечисление двух продуктов", hint: "Покупаем оба предмета.", explanation: "Одиночное a в этом списке не требует запятой." },
    { sectionIndex: 5, type: "order", prompt: "Соберите сообщение, начиная с Mám: «Я свободен и хочу выйти, но идёт дождь».", tokens: ["Mám", "voľno", "a", "chcem", "ísť", "von,", "ale", "prší."], answer: "Mám voľno a chcem ísť von, ale prší.", hint: "Сначала совместимые мысли, потом препятствие.", explanation: "A добавляет желание, ale вводит дождь как ограничение." },
    { sectionIndex: 5, type: "choice", prompt: "Что значит Môžeme zostať doma alebo ísť do kina?", options: ["Можно выбрать: остаться дома или пойти в кино", "Нужно одновременно остаться дома и пойти в кино", "Мы хотим кино, но оно закрыто"], answer: "Можно выбрать: остаться дома или пойти в кино", hint: "Alebo связывает альтернативы.", explanation: "Предлагаются два возможных решения." }
  ],
  knowledgeChecks: [
    { question: "Как перевести нейтральное «я дома, а брат на работе»?", options: ["Ja som doma a brat je v práci.", "Ja som doma alebo brat je v práci.", "Ja som doma, lebo brat je v práci."], answer: "Ja som doma a brat je v práci.", explanation: "Нейтрально добавляем второй факт." },
    { question: "Где нужна запятая в Hotel je pekný ale drahý?", options: ["Перед ale", "После ale", "После Hotel"], answer: "Перед ale", explanation: "Hotel je pekný, ale drahý." },
    { question: "Верно ли «перед alebo никогда нет запятой»?", options: ["Нет: базовая пара без запятой не покрывает все значения", "Да, даже в значении иначе", "Да, потому что словацкий не использует запятые"], answer: "Нет: базовая пара без запятой не покрывает все значения", explanation: "В предупреждении Ponáhľaj sa, alebo zmeškáme vlak ставим запятую." }
  ],
  finalChecks: [
    { question: "Выберите «Квартира светлая, но дорогая».", options: ["Byt je svetlý, ale drahý.", "Byt je svetlý alebo drahý.", "Byt je svetlý, ale lacný."], answer: "Byt je svetlý, ale drahý.", explanation: "Светлая — плюс, дорогая — ограничение." },
    { question: "Предложите выбор времени без изменения смысла.", options: ["Stretneme sa dnes alebo zajtra?", "Stretneme sa dnes a zajtra.", "Stretneme sa dnes, ale nie zajtra."], answer: "Stretneme sa dnes alebo zajtra?", explanation: "Alebo предлагает альтернативу, a включило бы оба дня." }
  ],
  vocabulary: [
    { word: "a", translation: "и; а при нейтральном сопоставлении" }, { word: "ale", translation: "но; а при контрасте" }, { word: "alebo", translation: "или; в предупреждении — иначе" },
    { word: "útulný", translation: "уютный" }, { word: "drahý", translation: "дорогой" }, { word: "nesúhlasiť", translation: "не соглашаться" },
    { word: "mať voľno", translation: "быть свободным, иметь свободное время" }, { word: "nestihnúť", translation: "не успеть" }, { word: "pri pokladni", translation: "у кассы" },
    { word: "dohodnúť sa", translation: "договориться" }, { word: "zmeškať vlak", translation: "опоздать на поезд" }, { word: "napísať správu", translation: "написать сообщение" }
  ],
  assessmentMode: "quiz",
  chatPrompt: "Попроси 5–7 связанных предложений о выходном: a дважды, ale как ограничение, alebo как выбор. Проверь логику союзов и запятые, принимай естественные формулировки. Не переводи нейтральное русское а всегда как ale и не называй отсутствие запятой перед a/alebo абсолютным правилом. Дай исправления с русским объяснением и попроси переписать проблемную фразу.",
  chatSuggestions: ["Опишу план на выходной", "Проверь a, ale и alebo", "Когда русское а переводится как a?"]
});
