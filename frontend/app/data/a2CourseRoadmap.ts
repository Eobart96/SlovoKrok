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
  title: "A2 · Модуль 2 — Падежи и управление",
  shortTitle: "Падежи и управление",
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

export const plannedA2Modules: A2PlannedModule[] = [plannedA2Module2];

export const getPlannedA2Module = (order: number): A2PlannedModule | undefined =>
  plannedA2Modules.find((module) => module.order === order);
