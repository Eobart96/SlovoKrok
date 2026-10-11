export type A2PlannedLesson = {
  slug: string;
  title: string;
  slovakTitle: string;
  outcome: string;
};

export type A2PlannedModule = {
  order: number;
  slug: string;
  title: string;
  shortTitle: string;
  description: string;
  lessons: A2PlannedLesson[];
};

const item = (slug: string, title: string, slovakTitle: string, outcome: string): A2PlannedLesson => ({
  slug,
  title,
  slovakTitle,
  outcome,
});

export const plannedA2Module2: A2PlannedModule = {
  order: 2,
  slug: "a2-module-2-cases",
  title: "Module 2 — Cases and Government",
  shortTitle: "Cases and Government",
  description: "Полное согласование именной группы, падежные формы и управление в ситуациях уровня A2.",
  lessons: [
    item("a2-nominative-plural-things", "Nominatív множественного числа: предметы и понятия", "Nominatív množného čísla: veci a pojmy", "Называть и описывать несколько предметов с полным согласованием."),
    item("a2-nominative-plural-people", "Nominatív множественного числа: люди", "Nominatív množného čísla: osoby", "Говорить о группах людей, профессиях и национальностях."),
    item("a2-accusative-singular-agreement", "Akuzatív единственного числа: полное согласование", "Akuzatív jednotného čísla: úplná zhoda", "Правильно оформлять прямой объект вместе с определением и местоимением."),
    item("a2-accusative-plural", "Akuzatív множественного числа", "Akuzatív množného čísla", "Говорить, кого и что ученик видит, ищет, приглашает, покупает или выбирает."),
    item("a2-genitive-singular", "Genitív единственного числа: отсутствие, происхождение и границы", "Genitív jednotného čísla", "Выражать отсутствие, движение из или до места, происхождение и временной интервал."),
    item("a2-genitive-quantity", "Genitív количества и меры", "Genitív množstva a miery", "Заказать или описать точное и приблизительное количество."),
    item("a2-genitive-plural", "Genitív множественного числа", "Genitív množného čísla", "Использовать частотные формы после количества и отрицания."),
    item("a2-dative-recipient-benefit-cause", "Datív: адресат, польза и причина", "Datív: adresát, prospech a príčina", "Сказать, кому дают, пишут, звонят, помогают или благодаря кому что-то произошло."),
    item("a2-locative-place-topic", "Lokál: место и тема разговора", "Lokál: miesto a téma rozhovoru", "Описывать место и говорить, о ком или о чём идёт речь."),
    item("a2-instrumental-means-company-role", "Inštrumentál: средство, совместность и характеристика", "Inštrumentál: prostriedok, spoločnosť a charakteristika", "Сказать, чем выполняется действие, с кем оно происходит и кем человек работает."),
    item("a2-case-triads", "Где, куда и откуда: падежные триады", "Kde, kam a odkiaľ: pádové trojice", "Выбирать падеж и предлог при описании положения и движения."),
    item("a2-case-system-government-address", "Падежи в одной системе: управление и обращение", "Pády v jednom systéme: väzby a oslovenie", "Собрать падежные модели в одну карту и естественно обратиться к человеку."),
  ],
};

export const plannedA2Module1: A2PlannedModule = {
  order: 1,
  slug: "a2-module-1-transition",
  title: "Module 1 — Transition to A2",
  shortTitle: "Transition to A2",
  description: "Диагностика опор A1, вид глагола, порядок слов, словарные связи и связная речь.",
  lessons: [
    item("a2-readiness-for-a2", "Что нужно уметь перед A2", "Pripravenosť na A2", "Проверить опоры A1 и составить личный список пробелов без повторного прохождения курса."),
    item("a2-verb-aspect", "Вид глагола: процесс, повтор и результат", "Slovesný vid: priebeh, opakovanie a výsledok", "Выбирать вид по смыслу действия и различать процесс, повторяемость и результат."),
    item("a2-clitics-word-order", "Клитики и порядок слов: вторая позиция", "Príklonky a slovosled: druhá pozícia", "Размещать короткие безударные формы в главной и придаточной части предложения."),
    item("a2-word-families", "Семьи слов: как расширять словарный запас", "Slovné rodiny a rozširovanie slovnej zásoby", "Узнавать родственные слова и расширять словарь без механического угадывания форм."),
    item("a2-case-map-government", "Карта падежей и управление", "Mapa pádov a väzby", "Выбирать падеж по функции, вопросу, предлогу или управляющему слову."),
    item("a2-coherence-focus", "Связность: тема, новая информация и смысловой акцент", "Súdržnosť: téma, nová informácia a dôraz", "Связывать предложения и менять смысловой акцент без нарушения грамматики."),
    item("a2-connected-pronunciation", "Произношение A2: связная речь", "Výslovnosť A2: súvislá reč", "Разборчиво произносить длинные фразы, контролируя долготу, ударение и интонацию."),
  ],
};

export const plannedA2Module3: A2PlannedModule = {
  order: 3,
  slug: "a2-module-3-adjectives-pronouns-numerals",
  title: "Module 3 — Description and Quantity",
  shortTitle: "Description and Quantity",
  description: "Согласование, сравнение, местоимения, принадлежность, числа и даты.",
  lessons: [
    item("a2-adjective-case-agreement", "Прилагательные: согласование во всех изученных падежах", "Prídavné mená: zhoda v pádoch", "Согласовывать определение с существительным в единственном числе."),
    item("a2-adjectives-plural", "Прилагательные во множественном числе", "Prídavné mená v množnom čísle", "Описывать группы людей и предметов в разных падежах."),
    item("a2-adjective-comparison", "Степени сравнения прилагательных", "Stupňovanie prídavných mien", "Сравнивать людей, места, товары и варианты."),
    item("a2-adverb-comparison", "Наречия и их сравнение", "Príslovky a ich stupňovanie", "Сравнивать, как, где и насколько происходит действие."),
    item("a2-personal-pronoun-cases", "Личные местоимения в косвенных падежах", "Osobné zámená v nepriamych pádoch", "Выбирать краткую или полную форму личного местоимения и ставить её в предложении."),
    item("a2-possessives-svoj", "Притяжательные слова и местоимение svoj", "Privlastňovacie zámená a svoj", "Различать принадлежность субъекту и другому человеку."),
    item("a2-possessive-adjectives", "Притяжательные прилагательные", "Privlastňovacie prídavné mená", "Называть индивидуальную принадлежность человеку или члену семьи."),
    item("a2-indefinite-negative-pronouns", "Неопределённые, отрицательные и обобщающие местоимения", "Neurčité, záporné a zovšeobecňujúce zámená", "Говорить о неопределённом, отсутствующем или полном множестве."),
    item("a2-numerals-dates-quantity", "Числительные, даты и количество", "Číslovky, dátumy a množstvo", "Использовать числа с людьми и предметами, произносить даты и формы количества."),
  ],
};

export const plannedA2Module4: A2PlannedModule = {
  order: 4,
  slug: "a2-module-4-verbs",
  title: "Module 4 — Verb Aspect, Tense and Mood",
  shortTitle: "Verb Aspect, Tense and Mood",
  description: "Вид и время, движение, возвратность, инструкции, условные просьбы и результативные формы.",
  lessons: [
    item("a2-aspect-in-narrative", "Вид в связном рассказе: фон и цепочка событий", "Vid v súvislom rozprávaní", "Чередовать фон, незавершённый процесс и последовательность завершённых событий."),
    item("a2-aspect-prefix-pairs", "Видовые пары с приставками", "Vidové dvojice s predponami", "Узнавать частотные пары и различать результат и дополнительный смысл приставки."),
    item("a2-aspect-stem-pairs", "Видовые пары с суффиксами и изменением основы", "Vidové dvojice so zmenou kmeňa", "Использовать частотные пары с изменением основы вместе с управлением и частицами."),
    item("a2-aspect-present-past", "Вид в настоящем и прошедшем времени", "Vid v prítomnom a minulom čase", "Различать текущий процесс, привычку, прошлый факт и завершённый результат."),
    item("a2-imperfective-future", "Аналитическое будущее несовершенных глаголов", "Opisné futúrum nedokonavých slovies", "Строить budem + инфинитив, отрицания и вопросы, сохраняя раннюю позицию sa/si."),
    item("a2-perfective-future", "Синтетическое будущее совершенных глаголов", "Jednoduché futúrum dokonavých slovies", "Выбирать napíšem, zavolám, stretneme sa для будущего результата и сочетать их с процессом."),
    item("a2-motion-verbs", "Глаголы движения ísť и chodiť", "Smer, opakovanie a cestovanie", "Различать конкретное движение и обычный маршрут, описывать транспорт и пересадки."),
    item("a2-reflexive-sa-si", "Возвратные глаголы sa и si", "Zvratnosť, vzájomnosť a zmena významu", "Сохранять sa/si, различать их функции, согласование и управление всей конструкции."),
    item("a2-imperative-requests", "Императив: просьба, инструкция и запрет", "Rozkaz, návod, prosba a zákaz", "Выбирать ty/my/vy, строить команды, запреты и уместные вежливые просьбы."),
    item("a2-conditional-by", "Кондиционал с частицей by", "Podmieňovací spôsob s časticou by", "Строить условное наклонение, согласовывать род, использовать keby и короткие формы."),
    item("a2-conditional-modals", "Модальные глаголы в условных просьбах и советах", "Zdvorilá prosba, možnosť a jemná rada", "Различать chcel, mohol и mal by для желания, возможности, просьбы и мягкого совета."),
    item("a2-verbal-nouns-participles", "Отглагольные существительные и пассивные причастия", "Názov deja a výsledný stav", "Различать названия действий и результативные признаки, согласовывать формы и читать объявления."),
  ],
};

export const plannedA2Module5: A2PlannedModule = {
  order: 5,
  slug: "a2-module-5-sentences",
  title: "Module 5 — Connected Speech and Complex Sentences",
  shortTitle: "Connected Speech and Complex Sentences",
  description: "Союзы, сообщение и уточнение, косвенные вопросы, причина, время и условие, связный рассказ.",
  lessons: [
    item("a2-conjunctions-a-ale-alebo", "Соединяем мысли: a, ale, alebo", "Spájame myšlienky: a, ale, alebo", "Соединять факты, показывать контраст и предлагать выбор с подходящей пунктуацией."),
    item("a2-paired-conjunctions", "Парные союзы aj — aj и ani — ani", "Párové spojky aj — aj a ani — ani", "Подчёркивать включение или исключение обоих элементов, согласовывать формы и отрицание."),
    item("a2-reported-statements-ze", "Передаём сообщение с že", "Sprostredkujeme správu so spojkou že", "Пересказывать факт, мнение, надежду и инструкцию с новой точкой зрения и временем по смыслу."),
    item("a2-relative-clauses-ktory", "Относительные предложения с ktorý", "Vzťažné vety so zámenom ktorý", "Уточнять существительное с согласованием, падежом по роли внутри уточнения и нужным предлогом."),
    item("a2-embedded-questions", "Придаточные с kto, čo и kde", "Vedľajšie vety s kto, čo a kde", "Передавать неизвестного человека, содержание или место внутри сообщения, просьбы и общего вопроса."),
    item("a2-cause-and-consequence", "Причина и следствие", "Príčina a následok", "Объяснять причину с lebo/pretože и результат с preto, сохраняя направление связи."),
    item("a2-time-and-real-condition", "Время и реальное условие", "Čas a reálna podmienka", "Различать kedy/keď/ak, строить реальный план с подходящим временем и условием."),
    item("a2-connected-story-focus", "Связный рассказ и актуальное членение", "Súvislé rozprávanie a aktuálne členenie", "Строить рассказ с временными переходами, связью известного и нового и понятным смысловым акцентом."),
  ],
};

export const plannedA2Modules: A2PlannedModule[] = [plannedA2Module1, plannedA2Module2, plannedA2Module3, plannedA2Module4, plannedA2Module5];

export const getPlannedA2Module = (order: number): A2PlannedModule | undefined =>
  plannedA2Modules.find((module) => module.order === order);
