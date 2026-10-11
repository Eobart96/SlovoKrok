import { defineA2Module5Lesson } from "../lessonFactory";

export const a2PairedConjunctionsLesson = defineA2Module5Lesson("a2-paired-conjunctions", {
  duration: "45–55 мин",
  goals: ["Включать оба элемента с aj — aj", "Исключать оба с ani — ani", "Согласовывать отрицание, падеж и число", "Ставить запятую перед повторённым союзом"],
  theory: {
    summary: "Aj X, aj Y подчёркивает «и X, и Y». Ani X, ani Y исключает оба: «ни X, ни Y». В наших полных отрицательных фразах сказуемое тоже отрицательное. Части пары выполняют одинаковую функцию.",
    rules: [
      "Aj повторяется перед каждым включённым элементом: Kúpim aj ovocie, aj zeleninu.",
      "Ani повторяется перед исключёнными элементами: Nechcem ani čaj, ani kávu.",
      "Отрицание согласуется: Nemám ani čas, ani energiu; не Mám ani čas, ani energiu.",
      "Если соединяются два действия, отрицание есть у каждого: Ani nevarím, ani nepečiem.",
      "Обе части сохраняют нужный падеж: Pomáham aj bratovi, aj sestre.",
      "Повторяйте необходимый предлог: aj s kolegom, aj s kolegyňou; ani na šport, ani na oddych.",
      "В модели с двумя подлежащими перед сказуемым используйте множественное число: Aj Anna, aj Peter pracujú. Запятая перед вторым союзом, не сразу после первого."
    ],
    examples: [
      { slovak: "Aj Anna, aj Peter pracujú doma.", russian: "И Анна, и Петер работают дома.", explanation: "Два деятеля: pracujú." },
      { slovak: "Kúpila som aj chlieb, aj mlieko.", russian: "Я купила и хлеб, и молоко.", explanation: "Подчёркнуто включены оба продукта." },
      { slovak: "Kurz je aj praktický, aj zaujímavý.", russian: "Курс и практичный, и интересный.", explanation: "Два признака одного курса." },
      { slovak: "Nechcem ani čaj, ani kávu.", russian: "Я не хочу ни чая, ни кофе.", explanation: "Оба исключены; отрицательное nechcem." },
      { slovak: "Ani neprší, ani nesneží.", russian: "Не идёт ни дождь, ни снег.", explanation: "Каждый глагол с отрицанием." },
      { slovak: "Hovorím aj s kolegom, aj s kolegyňou.", russian: "Я разговариваю и с коллегой, и с коллегой-женщиной.", explanation: "Одинаковая функция: s + творительный падеж." },
      { slovak: "Neboli sme ani v múzeu, ani v galérii.", russian: "Мы не были ни в музее, ни в галерее.", explanation: "Отрицательное boli и две параллельные формы места." }
    ]
  },
  sections: [
    { title: "Aj и aj: оба варианта важны", importance: "core", paragraphs: ["Anna a Peter prišli — Анна и Петер пришли: простое перечисление. Aj Anna, aj Peter prišli — и Анна, и Петер пришли: подчёркиваем, что пришли оба. Kúpim aj ovocie, aj zeleninu — куплю и фрукты, и овощи.", "Парный союз подходит, когда собеседник думает только об одном варианте. Kurz je aj praktický, aj zaujímavý — курс и практичный, и интересный. Aj čítam knihy, aj počúvam podcasty — я и читаю книги, и слушаю подкасты."], items: ["люди: Aj Anna, aj Peter...", "признаки: aj praktický, aj zaujímavý", "время: aj v pondelok, aj v stredu"], note: "Одиночное aj может значить «тоже». Здесь учим именно повторённую пару." },
    { title: "Ani и ani: отрицание в сказуемом", importance: "core", paragraphs: ["Nemám ani čas, ani energiu — у меня нет ни времени, ни сил. Nechcem ani čaj, ani kávu — не хочу ни чая, ни кофе. Ani Anna, ani Peter dnes nepracujú — ни Анна, ни Петер сегодня не работают. Ani не заменяет отрицательную форму глагола.", "При двух действиях отрицаем каждое: Ani mi nezavolal, ani mi nenapísal — он мне не позвонил и не написал. Ani nevarím, ani nepečiem — я не готовлю и не пеку. Это согласованное отрицание, а не отмена одного отрицания другим."], items: ["mám → nemám", "pracujú → nepracujú", "boli sme → neboli sme", "prší / sneží → neprší / nesneží"], note: "Практическая модель относится к полным предложениям с глаголом; короткие ответы без сказуемого не требуют выдумывать глагол." },
    { title: "Параллельные формы: падеж и предлог", importance: "core", paragraphs: ["Pomáham aj bratovi, aj sestre — помогаю и брату, и сестре: оба адресата в Datív. Hovorím aj s Petrom, aj s Janou — разговариваю и с Петером, и с Яной: обе части s + Inštrumentál. Čítam aj o meste, aj o jeho histórii — читаю и о городе, и о его истории: o + Lokál.", "Ideme aj do banky, aj do obchodu — идём и в банк, и в магазин: do + Genitív. Nemám čas ani na šport, ani na oddych — у меня нет времени ни на спорт, ни на отдых: na + Akuzatív. Повторённый предлог помогает не потерять связь и форму второго элемента."], items: ["кому? aj bratovi, aj sestre", "с кем? aj s Petrom, aj s Janou", "куда? ani do kina, ani na koncert"], note: "Предлоги не обязаны быть одинаковыми, если места требуют разных предлогов. Главное — одинаковая функция обеих частей и верные формы." },
    { title: "Два деятеля и запятая перед повтором", importance: "core", paragraphs: ["Aj mama, aj otec prišli — и мама, и папа пришли. Ani mama, ani otec neprišli — ни мама, ни папа не пришли. Для двух названных деятелей перед глаголом надёжная модель A2 — множественное число.", "Запятая перед вторым и каждым следующим повтором: Navštívime aj hrad, aj múzeum, aj park — посетим и замок, и музей, и парк. Не ставим запятую непосредственно после первого aj: Aj Jana, aj Peter..., не Aj, Jana...."], items: ["Aj byt, aj záhrada sú veľké. — И квартира, и сад большие.", "Nekúpil ani chlieb, ani mlieko. — Он не купил ни хлеба, ни молока."], note: "Kurz je aj praktický, aj zaujímavý имеет один субъект kurz, поэтому je, не sú." },
    { title: "Исправляем отрицание и симметрию", importance: "core", paragraphs: ["Mám ani čas, ani peniaze → Nemám ani čas, ani peniaze: отрицание у mám. Hovorím aj s Petrom, aj Janu → Hovorím aj s Petrom, aj s Janou: второй собеседник тоже после s.", "Myslím aj na prácu, aj o dovolenke → Myslím aj na prácu, aj na dovolenku — думаю и о работе, и об отпуске; здесь myslieť na. Nejdeme ani do kina, ani na koncert — не идём ни в кино, ни на концерт: обе части называют направление, но предлоги разные."], items: ["пара включает оба или исключает оба?", "если исключает — отрицательный глагол", "оба элемента выполняют одну функцию", "число глагола зависит от подлежащего, не просто от числа союзов"] },
    { title: "Два курса и план поездки", importance: "core", paragraphs: ["Eva: Máš čas aj v utorok, aj vo štvrtok? Martin: Nemôžem ani v utorok, ani vo štvrtok. Eva: A čo pondelok a streda? Martin: To mi vyhovuje. Aj pondelok, aj streda sú voľné. — Есть время и во вторник, и в четверг? Нет, не могу ни во вторник, ни в четверг. А понедельник и среда? Подходит, оба дня свободны.", "Na výlet pôjdu aj kolegovia, aj priatelia. Navštívime aj staré mesto, aj hrad. Výlet nebude ani drahý, ani náročný. Teším sa aj na program, aj na spoločný večer. — На экскурсию поедут и коллеги, и друзья. Посетим и старый город, и замок. Экскурсия не будет ни дорогой, ни сложной. Радуюсь и программе, и совместному вечеру."], items: ["В чате напишите 5–7 предложений о курсе или поездке.", "Используйте два включения aj — aj и два исключения ani — ani.", "Добавьте одну пару с предлогами и проверьте падежи."], note: "Не заставляйте одну и ту же форму предлога подходить ко всем местам." }
  ],
  stepPractices: [
    { sectionIndex: 0, type: "text", prompt: "Подчеркните оба продукта. Вставьте один и тот же союз в два пропуска: Kúpim ___ ovocie, ___ zeleninu. Введите союз один раз.", answer: "aj", showSlovakKeyboard: true, hint: "И фрукты, и овощи.", explanation: "Kúpim aj ovocie, aj zeleninu." },
    { sectionIndex: 1, type: "pairs", prompt: "Сделайте указанные глаголы отрицательными; формы лица и числа сохраните.", pairs: [{ prompt: "mám", answer: "nemám" }, { prompt: "pracujú", answer: "nepracujú" }, { prompt: "prší", answer: "neprší" }], answer: "nemám; nepracujú; neprší", showSlovakKeyboard: true, hint: "Добавьте ne- к глаголу.", explanation: "Ani — ani в этих полных фразах сочетается с отрицательным сказуемым." },
    { sectionIndex: 2, type: "text", prompt: "Дополните только вторую группу с предлогом: Hovorím aj s Petrom, aj ___. Используйте имя Jana.", answer: "s Janou", showSlovakKeyboard: true, hint: "S + Inštrumentál.", explanation: "Оба элемента называют собеседников: s Petrom, s Janou." },
    { sectionIndex: 3, type: "choice", prompt: "Какая форма подходит к двум людям перед сказуемым?", options: ["Aj Anna, aj Peter pracujú doma.", "Aj Anna, aj Peter pracuje doma.", "Aj Anna, aj Peter pracujem doma."], answer: "Aj Anna, aj Peter pracujú doma.", hint: "Два человека — они.", explanation: "Подлежащее называет Анну и Петера, используем pracujú." },
    { sectionIndex: 3, type: "choice", prompt: "Где нужна запятая в Nekúpil ani chlieb ani mlieko?", options: ["Перед вторым ani", "Сразу после первого ani", "Перед Nekúpil"], answer: "Перед вторым ani", hint: "Перед повторённой частью.", explanation: "Nekúpil ani chlieb, ani mlieko. Проверяем правило словами: текущий ввод не различает запятые автоматически." },
    { sectionIndex: 4, type: "choice", prompt: "Выберите грамматически согласованное исключение обоих мест.", options: ["Neboli sme ani v múzeu, ani v galérii.", "Boli sme ani v múzeu, ani v galérii.", "Neboli sme ani v múzeu, ani galériu."], answer: "Neboli sme ani v múzeu, ani v galérii.", hint: "Отрицание и v + Lokál в обеих частях.", explanation: "Отрицаем посещение обоих мест, не теряем предлог." },
    { sectionIndex: 5, type: "order", prompt: "Соберите сообщение, начиная с Výlet: «Экскурсия не будет ни дорогой, ни сложной».", tokens: ["Výlet", "nebude", "ani", "drahý,", "ani", "náročný."], answer: "Výlet nebude ani drahý, ani náročný.", hint: "Один субъект, два исключённых признака.", explanation: "Nebude согласовано с výlet; ani повторяется перед признаками." },
    { sectionIndex: 5, type: "text", prompt: "Вставьте союз исключения: Nemôžem ___ v utorok, ___ vo štvrtok. Введите его один раз.", answer: "ani", showSlovakKeyboard: true, hint: "Не могу ни в один из двух дней.", explanation: "Nemôžem ani v utorok, ani vo štvrtok." }
  ],
  knowledgeChecks: [
    { question: "Чем aj — aj отличается от простого a?", options: ["Подчёркивает включение обоих элементов", "Всегда исключает оба", "Всегда обозначает выбор одного"], answer: "Подчёркивает включение обоих элементов", explanation: "Aj Anna, aj Peter пришли оба." },
    { question: "Что нужно в полной фразе Nemám ani čas, ani peniaze?", options: ["Отрицательное сказуемое nemám", "Положительное mám", "Убрать оба ani"], answer: "Отрицательное сказуемое nemám", explanation: "Словацкое отрицание согласуется." },
    { question: "Почему в Kurz je aj praktický, aj zaujímavý форма je?", options: ["Подлежащее одно — kurz", "Два aj всегда требуют je", "Практичный и интересный — два человека"], answer: "Подлежащее одно — kurz", explanation: "Число глагола определяется субъектом, не количеством признаков." }
  ],
  finalChecks: [
    { question: "Выберите «Ни Анна, ни Петер не пришли».", options: ["Ani Anna, ani Peter neprišli.", "Ani Anna, ani Peter prišli.", "Aj Anna, aj Peter prišli."], answer: "Ani Anna, ani Peter neprišli.", explanation: "Ani исключает обоих, neprišli — отрицательное множественное число." },
    { question: "Как сказать «Помогаю и брату, и сестре»?", options: ["Pomáham aj bratovi, aj sestre.", "Pomáham aj bratovi, aj sestru.", "Pomáham ani bratovi, ani sestre."], answer: "Pomáham aj bratovi, aj sestre.", explanation: "Оба адресата после pomáhať в Datív." }
  ],
  vocabulary: [
    { word: "aj — aj", translation: "и — и; как — так и" }, { word: "ani — ani", translation: "ни — ни" }, { word: "energia", translation: "энергия; силы" },
    { word: "chuť", translation: "желание; вкус" }, { word: "náročný", translation: "сложный; требовательный" }, { word: "vyhovovať", translation: "подходить; устраивать" },
    { word: "galéria", translation: "галерея" }, { word: "hrad", translation: "замок" }, { word: "oddych", translation: "отдых" },
    { word: "spoločný večer", translation: "совместный вечер" }, { word: "dospelí", translation: "взрослые" }, { word: "počúvať podcasty", translation: "слушать подкасты" }
  ],
  assessmentMode: "quiz",
  chatPrompt: "Попроси 5–7 предложений о поездке или курсе с двумя aj — aj, двумя ani — ani и парой с предлогами. Проверь отрицательные сказуемые, функцию и падеж обеих частей, запятую перед повтором и число подлежащего. Не требуй множественного глагола от пары признаков одного субъекта. Принимай разные подходящие предлоги для разных мест (do kina, na koncert). Свободные естественные варианты не сравнивай с одной заученной строкой.",
  chatSuggestions: ["Опишу поездку с aj и ani", "Проверь отрицание и падежи", "Почему Kurz je, но Anna a Peter sú?"]
});
