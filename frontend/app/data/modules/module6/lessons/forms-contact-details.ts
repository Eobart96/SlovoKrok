import type { CourseLesson } from "../../../courseTypes";

const identityFieldOptions = ["meno", "priezvisko", "dátum narodenia", "štátna príslušnosť", "podpis"];
const addressFieldOptions = ["ulica", "číslo domu", "PSČ", "mesto", "krajina"];
const sampleValueOptions = ["Anna", "Nová", "12. 5. 2000", "Košice", "040 01"];

export const formsContactDetailsLesson = {
  vocabulary: [
    {"word":"Meno: Anna","translation":"Имя: Анна","example":"Meno: Anna"},
    {"word":"Priezvisko: Nová","translation":"Фамилия: Нова","example":"Priezvisko: Nová"},
    {"word":"Dátum narodenia: 12. 5. 2000","translation":"Дата рождения: 12.05.2000","example":"Dátum narodenia: 12. 5. 2000"},
    {"word":"Adresa: Hlavná 15, Košice","translation":"Адрес: Главная, 15, Кошице","example":"Adresa: Hlavná 15, Košice"},
    {"word":"Moje telefónne číslo je 0900 123 456.","translation":"Мой номер телефона — 0900 123 456.","example":"Moje telefónne číslo je 0900 123 456."},
    {"word":"Môj e-mail je anna.nova@example.sk.","translation":"Мой e-mail — anna.nova@example.sk.","example":"Môj e-mail je anna.nova@example.sk."},
  ],
  slug: "forms-contact-details",
  order: 15,
  title: "Анкета и контактные данные",
  slovakTitle: "Formulár a kontaktné údaje",
  description: "Заполняйте простую анкету вымышленными личными и контактными данными.",
  duration: "35–40 мин",
  goals: [
    "Понимать основные поля словацкой анкеты",
    "Различать имя, фамилию, дату рождения и гражданство",
    "Записывать адрес по отдельным полям",
    "Сообщать телефон и адрес электронной почты",
    "Перепроверять анкету и не раскрывать реальные данные в учебной практике",
  ],
  theory: {
    summary: "Простая анкета A1 требует не длинных предложений, а точного понимания подписей полей. Сначала определите, какие данные нужны, затем перепишите вымышленный образец без перестановок и проверьте цифры, диакритику и формат.",
    rules: [
      "Личные данные: meno — имя, priezvisko — фамилия, dátum narodenia — дата рождения, štátna príslušnosť — гражданство, podpis — подпись.",
      "Адрес делится на поля ulica, číslo domu, PSČ, mesto и krajina. PSČ — почтовый индекс, а не номер телефона.",
      "Контакты: telefónne číslo и e-mailová adresa. В устной диктовке e-mail zavináč означает @, bodka — точку.",
      "На вопрос Ako sa voláte? отвечают Volám sa...; телефон сообщают через Moje telefónne číslo je...; e-mail — Môj e-mail je....",
      "В учебных заданиях используйте только вымышленные данные. Перед отправкой реальной анкеты проверьте адресата и необходимость каждого поля.",
    ],
    examples: [
      { slovak: "Meno: Anna", russian: "Имя: Анна", explanation: "Meno — личное имя." },
      { slovak: "Priezvisko: Nová", russian: "Фамилия: Нова", explanation: "Priezvisko — фамилия." },
      { slovak: "Dátum narodenia: 12. 5. 2000", russian: "Дата рождения: 12.05.2000", explanation: "В словацкой записи после дня и месяца ставятся точки." },
      { slovak: "Adresa: Hlavná 15, Košice", russian: "Адрес: Главная, 15, Кошице", explanation: "В одной строке можно указать улицу, номер дома и город." },
      { slovak: "Moje telefónne číslo je 0900 123 456.", russian: "Мой номер телефона — 0900 123 456.", explanation: "Цифры нужно переписать в исходном порядке." },
      { slovak: "Môj e-mail je anna.nova@example.sk.", russian: "Мой e-mail — anna.nova@example.sk.", explanation: "В адресе нельзя заменять или переставлять символы." },
    ],
  },
  sections: [
    {
      title: "Имя и основные личные данные",
      paragraphs: ["В форме сначала найдите подпись поля, а затем впишите только требуемое значение. Meno и priezvisko — разные поля.", "Dátum narodenia можно записать цифрами. Štátna príslušnosť обозначает гражданство, а podpis — подпись в конце формы."],
      table: { headers: ["Поле", "Значение", "Учебный пример"], rows: [
        ["meno", "имя", "Anna"], ["priezvisko", "фамилия", "Nová"], ["dátum narodenia", "дата рождения", "12. 5. 2000"],
        ["štátna príslušnosť", "гражданство", "slovenská"], ["podpis", "подпись", "Anna Nová"],
      ] },
      items: ["Ako sa voláte? — Как вас зовут?", "Volám sa Anna Nová. — Меня зовут Анна Нова.", "Prosím, podpíšte sa. — Пожалуйста, распишитесь."],
      note: "Не вписывайте фамилию в поле meno и имя в поле priezvisko.",
    },
    {
      title: "Адрес по отдельным полям",
      paragraphs: ["Словацкая форма может разбить адрес на пять строк. Переносите каждый элемент в своё поле.", "PSČ читается как poštové smerovacie číslo и обычно записывается пятью цифрами с пробелом: 040 01."],
      table: { headers: ["Поле", "Перевод", "Учебный пример"], rows: [
        ["ulica", "улица", "Hlavná"], ["číslo domu", "номер дома", "15"], ["PSČ", "почтовый индекс", "040 01"],
        ["mesto", "город", "Košice"], ["krajina", "страна", "Slovensko"],
      ] },
      items: ["Adresa — адрес", "Bydlisko — место жительства", "Bývam v Košiciach. — Я живу в Кошице."],
      note: "Телефон не относится к полю PSČ: это разные числовые данные.",
    },
    {
      title: "Телефон и электронная почта",
      paragraphs: ["Telefónne číslo переписывайте группами цифр. E-mailová adresa требует точного порядка букв и символов.", "При диктовке e-mail полезны слова zavináč для @ и bodka для точки."],
      table: { headers: ["Данные", "Фраза", "Учебный пример"], rows: [
        ["telefónne číslo", "Moje telefónne číslo je...", "0900 123 456"], ["e-mail", "Môj e-mail je...", "anna.nova@example.sk"],
        ["@", "zavináč", "anna zavináč example"], [".", "bodka", "example bodka sk"],
        ["контакт", "Kontakt", "telefón alebo e-mail"],
      ] },
      items: ["Aké je vaše telefónne číslo? — Какой у вас номер телефона?", "Aký je váš e-mail? — Какой у вас e-mail?", "Prosím, zopakujte to. — Пожалуйста, повторите."],
      note: "В письменной форме используйте символы @ и точку, а не слова zavináč и bodka.",
    },
    {
      title: "Заполнение анкеты по образцу",
      paragraphs: ["Прочитайте учебную карточку целиком, затем переносите по одному значению. Не додумывайте отсутствующие данные.", "Образец: Anna Nová, дата рождения 12. 5. 2000, Hlavná 15, 040 01 Košice, телефон 0900 123 456, e-mail anna.nova@example.sk."],
      table: { headers: ["Поле формы", "Точное значение"], rows: [
        ["Meno", "Anna"], ["Priezvisko", "Nová"], ["Dátum narodenia", "12. 5. 2000"], ["Ulica a číslo domu", "Hlavná 15"],
        ["PSČ a mesto", "040 01 Košice"], ["Telefón", "0900 123 456"], ["E-mail", "anna.nova@example.sk"],
      ] },
      items: ["1. Найдите подпись поля.", "2. Скопируйте соответствующее значение.", "3. Сравните каждую цифру и букву с образцом."],
      note: "Все данные в примере вымышлены и предназначены только для обучения.",
    },
    {
      title: "Уточнение, проверка и безопасность",
      paragraphs: ["Если вы не расслышали значение, попросите повторить: Prosím, zopakujte to. Можно уточнить имя или написание: Ako sa to píše?", "Перед завершением проверьте meno/priezvisko, дату, PSČ, телефон, e-mail и подпись. В учебной среде реальные персональные данные не нужны."],
      table: { headers: ["Ошибка", "Правильно", "Почему"], rows: [
        ["Meno: Nová", "Meno: Anna", "В поле meno нужно имя."], ["Priezvisko: Anna", "Priezvisko: Nová", "В поле priezvisko нужна фамилия."],
        ["PSČ: 0900 123 456", "PSČ: 040 01", "PSČ — почтовый индекс."], ["telefonne cislo", "telefónne číslo", "В подписи поля нужна словацкая диакритика."],
        ["anna.nova example.sk", "anna.nova@example.sk", "В e-mail необходим символ @."],
      ] },
      items: ["Prosím, zopakujte to. — Повторите, пожалуйста.", "Ako sa to píše? — Как это пишется?", "Je to správne? — Это правильно?"],
      note: "Не отправляйте реальные данные неизвестному адресату и не заполняйте лишние поля без необходимости.",
    },
  ],
  stepPractices: [
    { id: "m6-forms-contact-details-step-1", sectionIndex: 0, type: "pairs", prompt: "Выберите словацкое поле личных данных.", answer: "meno; priezvisko; dátum narodenia; štátna príslušnosť; podpis", pairs: [
      { prompt: "имя", answer: "meno", options: identityFieldOptions }, { prompt: "фамилия", answer: "priezvisko", options: identityFieldOptions },
      { prompt: "дата рождения", answer: "dátum narodenia", options: identityFieldOptions }, { prompt: "гражданство", answer: "štátna príslušnosť", options: identityFieldOptions },
      { prompt: "подпись", answer: "podpis", options: identityFieldOptions },
    ], hint: "Каждому русскому значению соответствует отдельная подпись поля.", explanation: "Эти пять полей относятся к основным личным данным." },
    { id: "m6-forms-contact-details-step-2", sectionIndex: 1, type: "pairs", prompt: "Выберите нужное поле адреса.", answer: "ulica; číslo domu; PSČ; mesto; krajina", pairs: [
      { prompt: "улица", answer: "ulica", options: addressFieldOptions }, { prompt: "номер дома", answer: "číslo domu", options: addressFieldOptions },
      { prompt: "почтовый индекс", answer: "PSČ", options: addressFieldOptions }, { prompt: "город", answer: "mesto", options: addressFieldOptions },
      { prompt: "страна", answer: "krajina", options: addressFieldOptions },
    ], hint: "Сопоставьте часть адреса с подписью поля.", explanation: "Адрес разбивается на улицу, дом, индекс, город и страну." },
    { id: "m6-forms-contact-details-step-3", sectionIndex: 2, type: "pairs", prompt: "Выберите контакт или символ.", answer: "telefónne číslo; e-mailová adresa; zavináč; bodka; zopakujte", pairs: [
      { prompt: "номер телефона", answer: "telefónne číslo", options: ["telefónne číslo", "e-mailová adresa", "zavináč", "bodka", "zopakujte"] },
      { prompt: "адрес электронной почты", answer: "e-mailová adresa", options: ["telefónne číslo", "e-mailová adresa", "zavináč", "bodka", "zopakujte"] },
      { prompt: "символ @", answer: "zavináč", options: ["telefónne číslo", "e-mailová adresa", "zavináč", "bodka", "zopakujte"] },
      { prompt: "точка", answer: "bodka", options: ["telefónne číslo", "e-mailová adresa", "zavináč", "bodka", "zopakujte"] },
      { prompt: "повторите", answer: "zopakujte", options: ["telefónne číslo", "e-mailová adresa", "zavináč", "bodka", "zopakujte"] },
    ], hint: "Различайте название контакта, символ и просьбу.", explanation: "Слова помогают записать телефон и e-mail без потери символов." },
    { id: "m6-forms-contact-details-step-4", sectionIndex: 3, type: "pairs", prompt: "Перенесите данные Анны Новой в правильные поля.", answer: "Anna; Nová; 12. 5. 2000; Košice; 040 01", pairs: [
      { prompt: "Meno", answer: "Anna", options: sampleValueOptions }, { prompt: "Priezvisko", answer: "Nová", options: sampleValueOptions },
      { prompt: "Dátum narodenia", answer: "12. 5. 2000", options: sampleValueOptions }, { prompt: "Mesto", answer: "Košice", options: sampleValueOptions },
      { prompt: "PSČ", answer: "040 01", options: sampleValueOptions },
    ], hint: "Одно значение образца соответствует одному полю.", explanation: "Точный перенос предотвращает смешение имени, даты, города и индекса." },
    { id: "m6-forms-contact-details-step-5", sectionIndex: 4, type: "pairs", prompt: "Исправьте ошибки в анкете.", answer: "Meno: Anna; Priezvisko: Nová; PSČ: 040 01; Telefónne číslo; anna.nova@example.sk", pairs: [
      { prompt: "Meno: Nová", answer: "Meno: Anna", inputHint: "Введите исправленную строку" }, { prompt: "Priezvisko: Anna", answer: "Priezvisko: Nová", inputHint: "Введите исправленную строку" },
      { prompt: "PSČ: 0900 123 456", answer: "PSČ: 040 01", inputHint: "Введите исправленную строку" }, { prompt: "Telefonne cislo", answer: "Telefónne číslo", inputHint: "Введите исправленную подпись" },
      { prompt: "anna.nova example.sk", answer: "anna.nova@example.sk", inputHint: "Введите исправленный адрес" },
    ], hint: "Проверьте тип данных, диакритику и символ @.", explanation: "Форма должна содержать нужное значение в нужном поле." },
  ],
  assessmentMode: "interactive",
  materialAssessmentStep: false,
  reinforcementLabel: "Финальный тест темы",
  reinforcementTitle: "Выполните шесть заданий темы 15",
  reinforcementPractices: [
    { id: "reinforcement:forms-contact-details:1", sectionIndex: 0, type: "pairs", prompt: "Выберите поле личных данных.", answer: "meno; priezvisko; dátum narodenia; štátna príslušnosť; podpis", pairs: [
      { prompt: "имя", answer: "meno", options: identityFieldOptions }, { prompt: "фамилия", answer: "priezvisko", options: identityFieldOptions },
      { prompt: "дата рождения", answer: "dátum narodenia", options: identityFieldOptions }, { prompt: "гражданство", answer: "štátna príslušnosť", options: identityFieldOptions },
      { prompt: "подпись", answer: "podpis", options: identityFieldOptions },
    ], hint: "Выберите точную подпись поля.", explanation: "Пять подписей покрывают основные личные данные простой анкеты." },
    { id: "reinforcement:forms-contact-details:2", sectionIndex: 1, type: "pairs", prompt: "Выберите поле адреса.", answer: "ulica; číslo domu; PSČ; mesto; krajina", pairs: [
      { prompt: "улица", answer: "ulica", options: addressFieldOptions }, { prompt: "номер дома", answer: "číslo domu", options: addressFieldOptions },
      { prompt: "почтовый индекс", answer: "PSČ", options: addressFieldOptions }, { prompt: "город", answer: "mesto", options: addressFieldOptions }, { prompt: "страна", answer: "krajina", options: addressFieldOptions },
    ], hint: "Не путайте PSČ с телефоном.", explanation: "Каждая часть адреса записывается отдельно." },
    { id: "reinforcement:forms-contact-details:3", sectionIndex: 3, type: "pairs", prompt: "Заполните поля точными значениями образца.", answer: "Anna; Nová; 12. 5. 2000; Košice; 040 01", pairs: [
      { prompt: "Meno", answer: "Anna", options: sampleValueOptions }, { prompt: "Priezvisko", answer: "Nová", options: sampleValueOptions },
      { prompt: "Dátum narodenia", answer: "12. 5. 2000", options: sampleValueOptions }, { prompt: "Mesto", answer: "Košice", options: sampleValueOptions }, { prompt: "PSČ", answer: "040 01", options: sampleValueOptions },
    ], hint: "Используйте каждое значение один раз.", explanation: "Задание проверяет точный перенос данных между карточкой и формой." },
    { id: "reinforcement:forms-contact-details:4", sectionIndex: 4, type: "pairs", prompt: "Исправьте строки учебной анкеты.", answer: "Meno: Anna; Priezvisko: Nová; PSČ: 040 01; Telefónne číslo; anna.nova@example.sk", pairs: [
      { prompt: "Meno: Nová", answer: "Meno: Anna", inputHint: "Введите исправленную строку" }, { prompt: "Priezvisko: Anna", answer: "Priezvisko: Nová", inputHint: "Введите исправленную строку" },
      { prompt: "PSČ: 0900 123 456", answer: "PSČ: 040 01", inputHint: "Введите исправленную строку" }, { prompt: "Telefonne cislo", answer: "Telefónne číslo", inputHint: "Введите исправленную подпись" },
      { prompt: "anna.nova example.sk", answer: "anna.nova@example.sk", inputHint: "Введите исправленный адрес" },
    ], hint: "Исправьте всю строку, а не только один символ.", explanation: "Проверяются назначение поля, диакритика и формат e-mail." },
    { id: "reinforcement:forms-contact-details:5", sectionIndex: 4, type: "pairs", prompt: "Переведите на словацкий.", answer: "Volám sa Anna Nová.; Môj dátum narodenia je 12. 5. 2000.; Moja adresa je Hlavná 15, Košice.; Moje telefónne číslo je 0900 123 456.; Môj e-mail je anna.nova@example.sk.", pairs: [
      { prompt: "Меня зовут Анна Нова.", answer: "Volám sa Anna Nová.", acceptableAnswers: ["Moje meno je Anna Nová."], inputHint: "Введите перевод" },
      { prompt: "Моя дата рождения — 12.05.2000.", answer: "Môj dátum narodenia je 12. 5. 2000.", inputHint: "Введите перевод" },
      { prompt: "Мой адрес — Главная, 15, Кошице.", answer: "Moja adresa je Hlavná 15, Košice.", inputHint: "Введите перевод" },
      { prompt: "Мой номер телефона — 0900 123 456.", answer: "Moje telefónne číslo je 0900 123 456.", inputHint: "Введите перевод" },
      { prompt: "Мой e-mail — anna.nova@example.sk.", answer: "Môj e-mail je anna.nova@example.sk.", inputHint: "Введите перевод" },
    ], hint: "Используйте вымышленные данные образца и сохраняйте словацкую диакритику.", explanation: "Переводы проверяют пять готовых моделей для сообщения данных." },
    { id: "reinforcement:forms-contact-details:6", sectionIndex: 4, type: "pairs", prompt: "Соберите короткое уточнение контактных данных.", answer: "Ako sa voláte?; Volám sa Anna Nová.; Aké je vaše telefónne číslo?; Moje telefónne číslo je 0900 123 456.; Aký je váš e-mail?; Môj e-mail je anna.nova@example.sk.", pairs: [
      { prompt: "1 · вопрос об имени", answer: "Ako sa voláte?", options: ["Ako sa voláte?", "Kde sa voláte?", "Koľko sa voláte?"] },
      { prompt: "2 · имя", answer: "Volám sa Anna Nová.", options: ["Volám sa Anna Nová.", "Som meno Anna Nová.", "Volá Anna Nová."] },
      { prompt: "3 · вопрос о телефоне", answer: "Aké je vaše telefónne číslo?", options: ["Aké je vaše telefónne číslo?", "Kde je vaše telefónne číslo?", "Kto je telefónne číslo?"] },
      { prompt: "4 · телефон", answer: "Moje telefónne číslo je 0900 123 456.", options: ["Moje telefónne číslo je 0900 123 456.", "Môj telefónne číslo som 0900 123 456.", "Moja telefón je 0900 123 456."] },
      { prompt: "5 · вопрос об e-mail", answer: "Aký je váš e-mail?", options: ["Aký je váš e-mail?", "Aké je vaša e-mail?", "Kto je váš e-mail?"] },
      { prompt: "6 · e-mail", answer: "Môj e-mail je anna.nova@example.sk.", options: ["Môj e-mail je anna.nova@example.sk.", "Moja e-mail som anna.nova@example.sk.", "Môj e-mail ma anna.nova@example.sk."] },
    ], hint: "Чередуйте вопрос и точный ответ.", explanation: "Диалог запрашивает только имя и два способа связи." },
  ],
  knowledgeChecks: [
    { id: "m6-forms-contact-details-check-1", question: "Какое поле означает «фамилия»?", options: ["priezvisko", "meno", "podpis"], answer: "priezvisko", explanation: "Priezvisko — фамилия, meno — имя." },
    { id: "m6-forms-contact-details-check-2", question: "Что нужно вписать в поле PSČ?", options: ["Почтовый индекс", "Номер телефона", "Дату рождения"], answer: "Почтовый индекс", explanation: "PSČ — poštové smerovacie číslo." },
    { id: "m6-forms-contact-details-check-3", question: "Какая практика безопасна в учебном задании?", options: ["Использовать вымышленные данные", "Публиковать реальный телефон", "Отправлять паспортные данные"], answer: "Использовать вымышленные данные", explanation: "Для языковой практики реальные персональные данные не нужны." },
  ],
  finalChecks: [
    { id: "m6-forms-contact-details-final-1", question: "Переведите: «Мой номер телефона — 0900 123 456».", options: ["Moje telefónne číslo je 0900 123 456.", "Môj telefónne číslo som 0900 123 456.", "Moja telefón je 0900 123 456."], answer: "Moje telefónne číslo je 0900 123 456.", explanation: "Используйте готовую модель Moje telefónne číslo je...." },
  ],
  chatPrompt: "Заполните вымышленную анкету: имя, фамилия, дата рождения, адрес, телефон и e-mail. Не используйте реальные данные.",
  chatSuggestions: ["Meno: Anna", "Priezvisko: Nová", "Telefón: 0900 123 456"],
} satisfies CourseLesson;
