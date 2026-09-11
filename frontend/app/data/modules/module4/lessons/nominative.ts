import type { CourseLesson } from "../../../courseTypes";
import { defineModule4Lesson } from "../lessonFactory";

const baseNominativeLesson = defineModule4Lesson("nominative", 0, {
  summary: "Nominatív называет человека или предмет и обычно оформляет подлежащее — участника, о котором что-то сообщается.",
  model: "Kto? относится к людям, Čo? — к предметам; To je вводит одно название, To sú — несколько: To je učiteľ. To sú učitelia.",
  goals: ["Узнавать Nominatív по роли слова", "Различать Kto? и Čo?", "Выбирать je и sú", "Согласовывать указательное слово и признак по роду и числу"],
  rules: [
    "У большинства существительных словарная форма — Nominatív единственного числа.",
    "В модели je + профессия или роль оба названия стоят в Nominatíve: Martin je učiteľ.",
    "Род запоминайте по-словацки вместе с опорой ten/tá/to.",
    "Nominatív бывает в единственном и множественном числе; единого окончания множественного числа нет.",
    "Прилагательное согласуется: nový telefón, nová taška, nové okno, noví učitelia, nové zošity.",
  ],
  examples: [
    { slovak: "To je Lucia.", russian: "Это Луция." },
    { slovak: "Martin je študent.", russian: "Мартин — студент." },
    { slovak: "To sú učitelia.", russian: "Это учителя." },
    { slovak: "Ten zošit je nový.", russian: "Та тетрадь новая." },
    { slovak: "Okná sú veľké.", russian: "Окна большие." },
  ],
  primaryTitle: "Кого или что мы называем",
  primaryTable: { headers: ["Задача", "Пример", "Как понять"], rows: [["назвать человека", "To je učiteľ.", "Kto je to?"], ["назвать предмет", "To je zošit.", "Čo je to?"], ["сообщить о действии", "Lucia číta.", "Kto číta?"], ["описать предмет", "Telefón je nový.", "Речь о telefón"]] },
  secondaryTitle: "Род, число и согласование",
  secondaryTable: { headers: ["Группа", "Опора", "Пример"], rows: [["мужской, ед. ч.", "ten / -ý", "ten nový telefón"], ["женский, ед. ч.", "tá / -á", "tá nová taška"], ["средний, ед. ч.", "to / -é", "to nové okno"], ["мужчины, мн. ч.", "tí / -í", "tí noví učitelia"], ["остальные, мн. ч.", "tie / -é", "tie nové zošity"]] },
  boundaryItems: ["Kniha je nová. — kniha называет субъект.", "Čítam knihu. — knihu уже обозначает объект.", "Lucia je študentka. — в словацкой полной фразе нужна связка je.", "To je okno. — to вводит название; To okno je malé. — to согласуется с существительным."],
  mistake: "Не переносите русский род и не смешивайте число: zošit — мужской род, To sú требует множественного числа.",
  task: "Представьте человека, назовите его роль, затем покажите один предмет и несколько предметов с согласованным признаком.",
  productionPrompt: "Ответьте полным предложением: Kto je doma? — «Моя сестра дома».",
  productionAnswer: "Moja sestra je doma.",
  productionHint: "Субъект остаётся в словарной форме, связка je обязательна.",
});

export const nominativeLesson = {
  vocabulary: [
    {"word":"Kto je to? — To je Lucia.","translation":"Кто это? — Это Луция.","example":"Kto je to? — To je Lucia."},
    {"word":"Lucia je učiteľka.","translation":"Луция — учительница.","example":"Lucia je učiteľka."},
    {"word":"To sú učitelia.","translation":"Это учителя.","example":"To sú učitelia."},
    {"word":"Ten zošit je nový.","translation":"Та тетрадь новая.","example":"Ten zošit je nový."},
    {"word":"Tie zošity sú nové.","translation":"Те тетради новые.","example":"Tie zošity sú nové."},
    {"word":"Dieťa je malé. Deti sú tu.","translation":"Ребёнок маленький. Дети здесь.","example":"Dieťa je malé. Deti sú tu."},
  ],
  ...baseNominativeLesson,
  description: "Узнавайте именительный падеж, спрашивайте kto?/čo? и согласовывайте слова в моделях To je / To sú.",
  duration: "35–40 мин",
  goals: [
    "Находить, кто или что является участником простой фразы",
    "Спрашивать Kto? / Čo? и отвечать через To je / To sú",
    "Учитывать словацкий род и число существительного",
    "Согласовывать указательное слово, связку и частотный признак",
  ],
  theory: {
    summary: "Nominatív (N) отвечает на вопросы kto? čo? и обычно называет подлежащее — человека или предмет, о котором что-то сообщается. У большинства существительных словарная форма — Nominatív единственного числа.",
    rules: [
      "Назвать человека или предмет: Kto je to? — To je učiteľ. Čo je to? — To je zošit.",
      "В модели профессии или роли оба названия остаются в Nominatíve: Martin je učiteľ. Название профессии пишется со строчной буквы.",
      "В полной словацкой фразе связку не опускают: Lucia je študentka. Для нескольких участников используется sú: Študentky sú tu.",
      "Падеж определяется ролью слова: Kniha je nová — субъект в Nominatíve; Čítam knihu — объект уже в Akuzatíve.",
      "Род учите по-словацки с ten/tá/to: ten zošit, tá taška, to okno. Окончание — подсказка, а не гарантия: ten kolega, tá noc, to dieťa.",
      "Для мужчин во множественном числе используйте tí, для предметов и остальных групп урока — tie: tí učitelia, tie zošity, tie tašky, tie okná.",
      "Признак согласуется с существительным: nový telefón, nová taška, nové okno, noví učitelia, nové zošity.",
    ],
    examples: [
      { slovak: "Kto je to? — To je Lucia.", russian: "Кто это? — Это Луция.", explanation: "Kto? спрашивает о человеке; одно имя вводится через To je." },
      { slovak: "Lucia je učiteľka.", russian: "Луция — учительница.", explanation: "Имя и профессия стоят в Nominatíve, связка je обязательна." },
      { slovak: "To sú učitelia.", russian: "Это учителя.", explanation: "Несколько людей требуют sú и формы множественного числа." },
      { slovak: "Ten zošit je nový.", russian: "Та тетрадь новая.", explanation: "Zošit по-словацки мужского рода: ten и nový." },
      { slovak: "Tie zošity sú nové.", russian: "Те тетради новые.", explanation: "Zošity — предметы во множественном числе, поэтому: tie zošity sú nové." },
      { slovak: "Dieťa je malé. Deti sú tu.", russian: "Ребёнок маленький. Дети здесь.", explanation: "Готовую пару dieťa — deti нужно запомнить целиком." },
    ],
  },
  sections: [
    {
      title: "Кого или что мы называем",
      paragraphs: [
        "Nominatív отвечает на вопросы kto? čo? и обычно оформляет подлежащее. Сначала найдите человека или предмет, о котором что-то сообщается.",
        "Для знакомства используйте модель je + название в Nominatíve: Martin je učiteľ. Эта модель не означает, что после любого употребления byť всегда нужен Nominatív.",
      ],
      table: { headers: ["Задача", "Пример", "Как понять"], rows: [
        ["назвать человека", "To je učiteľ. — Это учитель.", "Kto je to?"],
        ["назвать предмет", "To je zošit. — Это тетрадь.", "Čo je to?"],
        ["сообщить о действии", "Lucia číta. — Луция читает.", "Kto číta?"],
        ["описать предмет", "Telefón je nový. — Телефон новый.", "Речь о telefón"],
      ] },
      items: ["Lucia je študentka. — В полной словацкой фразе нужна связка je.", "Študentky sú tu. — Несколько участников требуют sú.", "Kniha je nová. — kniha в Nominatíve; Čítam knihu. — knihu уже в Akuzatíve."],
      note: "Падеж определяется ролью слова. В этой теме объектную форму достаточно только отличать; её окончания изучаются дальше.",
    },
    {
      title: "Род и число существительного",
      paragraphs: ["Род запоминайте по-словацки. Русская «тетрадь» женского рода, а zošit — мужского. Ten/tá/to помогают учить род, но не являются артиклями."],
      table: { headers: ["Род и опора", "Частая подсказка A1", "Примеры"], rows: [
        ["мужской — ten", "обычно согласная", "ten zošit; ten telefón"],
        ["женский — tá", "часто -a", "tá taška; tá škola"],
        ["средний — to", "часто -o или -e", "to okno; to more"],
      ] },
      items: [
        "ten študent — tí študenti; ten učiteľ — tí učitelia",
        "ten zošit — tie zošity; tá taška — tie tašky",
        "to okno — tie okná; to dieťa — tie deti",
      ],
      note: "Окончание — подсказка, а не гарантия: ten kolega, tá noc, to dieťa. Единого окончания множественного числа нет; учите пары целиком.",
    },
    {
      title: "Собираем простое описание",
      paragraphs: [
        "В модели «Это…» слово to сохраняется при любом роде и числе: To je študentka. To sú tašky. Меняются связка и название.",
        "Различайте To je okno, где to вводит название, и To okno je malé, где to стоит при существительном среднего рода. С женским родом: Tá taška je malá.",
      ],
      table: { headers: ["Группа в Nominatíve", "Форма", "Пример"], rows: [
        ["мужской, ед. ч.", "nový", "nový telefón"],
        ["женский, ед. ч.", "nová", "nová taška"],
        ["средний, ед. ч.", "nové", "nové okno"],
        ["мужчины, мн. ч.", "noví", "noví učitelia"],
        ["остальные группы урока, мн. ч.", "nové", "nové zošity / tašky / okná"],
      ] },
      items: ["Aký je telefón? — Je nový.", "Aká je taška? — Je malá.", "Aké je okno? — Je veľké.", "Nová taška → Taška je nová. Noví učitelia → Učitelia sú noví."],
      note: "Ту же модель используют malý и pekný. У других типов прилагательных могут быть иные окончания.",
    },
    {
      title: "Примеры для вашей речи",
      paragraphs: ["Прочитайте фразы вслух, затем закройте перевод и объясните смысл. Проверяйте род, число и форму связки."],
      table: { headers: ["Slovensky", "По-русски"], rows: [
        ["Kto je to?", "Кто это?"], ["To je Lucia.", "Это Луция."], ["Lucia je učiteľka.", "Луция — учительница."],
        ["Martin je študent.", "Мартин — студент."], ["To sú učitelia.", "Это учителя."], ["Tí učitelia sú milí.", "Те учителя приветливые."],
        ["Študentky sú veselé.", "Студентки весёлые."], ["Dieťa je malé.", "Ребёнок маленький."], ["Deti sú tu.", "Дети здесь."],
        ["Čo je to?", "Что это?"], ["To je zošit.", "Это тетрадь."], ["Ten zošit je nový.", "Та тетрадь новая."],
        ["To sú zošity.", "Это тетради."], ["Tie zošity sú nové.", "Те тетради новые."], ["Tá taška je pekná.", "Та сумка красивая."],
        ["To okno je veľké.", "То окно большое."], ["Okná sú veľké.", "Окна большие."], ["Telefón je malý.", "Телефон маленький."],
      ] },
      items: ["Čo je to? — To je taška.", "Aká je tá taška? — Je nová.", "Замените taška на zošit и согласуйте вопрос и ответ."],
      note: "Готовый мини-диалог: Čo je to? — To je taška. — Aká je tá taška? — Je nová.",
    },
    {
      title: "Ошибки и самопроверка",
      table: { headers: ["Ошибка", "Правильно", "Почему"], rows: [
        ["To sú taška.", "To je taška.", "Один предмет требует je."],
        ["Zošit je nová.", "Zošit je nový.", "Zošit по-словацки мужского рода."],
        ["Tí zošity sú nové.", "Tie zošity sú nové.", "Zošity — предметы."],
        ["Lucia študentka.", "Lucia je študentka.", "В полной фразе нужна связка je."],
      ] },
      items: ["Найдите существительное и определите его роль.", "Проверьте род и число по-словацки.", "Выберите je/sú и указательное слово.", "Проверьте окончание прилагательного."],
      note: "Если правило ещё не получается применить без таблицы, вернитесь к нужному шагу. Затем переходите к отдельному финальному тесту из шести заданий.",
    },
  ],
  stepPractices: [
    { id: "m4-nominative-step-1", sectionIndex: 0, type: "choice", prompt: "Выберите правильный вопрос и ответ о человеке.", options: ["Čo je to? — To je študentka.", "Kto je to? — To je študentka.", "Kto sú to? — To je študentka."], answer: "Kto je to? — To je študentka.", hint: "Сначала определите: человек или предмет, один или несколько.", explanation: "О человеке спрашиваем Kto?; один человек требует To je." },
    { id: "m4-nominative-step-2", sectionIndex: 1, type: "pairs", prompt: "Выберите словацкий род каждого существительного.", answer: "ten; tá; to; ten", pairs: [
      { prompt: "zošit", answer: "ten", options: ["ten", "tá", "to"] }, { prompt: "taška", answer: "tá", options: ["ten", "tá", "to"] },
      { prompt: "okno", answer: "to", options: ["ten", "tá", "to"] }, { prompt: "kolega", answer: "ten", options: ["ten", "tá", "to"] },
    ], hint: "Опирайтесь на словацкое слово, а не на русский перевод.", explanation: "Правильно: ten zošit, tá taška, to okno, ten kolega." },
    { id: "m4-nominative-step-3", sectionIndex: 2, type: "pairs", prompt: "Выберите je или sú.", answer: "je; sú; je; sú", pairs: [
      { prompt: "To ___ taška.", answer: "je", options: ["je", "sú"] }, { prompt: "To ___ zošity.", answer: "sú", options: ["je", "sú"] },
      { prompt: "Okno ___ veľké.", answer: "je", options: ["je", "sú"] }, { prompt: "Učitelia ___ noví.", answer: "sú", options: ["je", "sú"] },
    ], hint: "Определите число существительного.", explanation: "Единственное число требует je, множественное — sú." },
    { id: "m4-nominative-step-4", sectionIndex: 3, type: "choice", prompt: "Как по-словацки: «Те тетради новые»?", options: ["Tí zošity sú noví.", "To zošity je nové.", "Tie zošity sú nové."], answer: "Tie zošity sú nové.", hint: "Zošity — предметы во множественном числе.", explanation: "Для предметов нужны tie, sú и форма nové." },
    { id: "m4-nominative-step-5", sectionIndex: 4, type: "pairs", prompt: "Исправьте каждое предложение.", answer: "Tá taška je nová.; Tie zošity sú nové.; To sú noví učitelia.; Lucia je študentka.", pairs: [
      { prompt: "Tá taška je nový.", answer: "Tá taška je nová.", inputHint: "Введите исправленное предложение" },
      { prompt: "Tí zošity sú nové.", answer: "Tie zošity sú nové.", inputHint: "Введите исправленное предложение" },
      { prompt: "To sú nové učitelia.", answer: "To sú noví učitelia.", inputHint: "Введите исправленное предложение" },
      { prompt: "Lucia študentka.", answer: "Lucia je študentka.", inputHint: "Введите исправленное предложение" },
    ], hint: "Проверьте род, число, je/sú и окончание признака.", explanation: "Каждая строка исправляется отдельно: nová, tie, noví и обязательное je." },
  ],
  assessmentMode: "interactive",
  materialAssessmentStep: false,
  reinforcementLabel: "Финальный тест темы",
  reinforcementTitle: "Выполните шесть заданий темы 1",
  reinforcementPractices: [
    { id: "reinforcement:nominative:1", sectionIndex: 0, type: "pairs", prompt: "Выберите Kto или Čo.", answer: "Kto; Čo; Kto", pairs: [
      { prompt: "___ je to? — To je študentka.", answer: "Kto", options: ["Kto", "Čo"] }, { prompt: "___ je to? — To je telefón.", answer: "Čo", options: ["Kto", "Čo"] },
      { prompt: "___ sú to? — To sú učitelia.", answer: "Kto", options: ["Kto", "Čo"] },
    ], hint: "Люди отвечают на kto?, предметы — на čo?.", explanation: "Študentka и učitelia — люди; telefón — предмет." },
    { id: "reinforcement:nominative:2", sectionIndex: 2, type: "pairs", prompt: "Вставьте je или sú.", answer: "je; sú; je; sú", pairs: [
      { prompt: "To ___ taška.", answer: "je", options: ["je", "sú"] }, { prompt: "To ___ zošity.", answer: "sú", options: ["je", "sú"] },
      { prompt: "Lucia ___ učiteľka.", answer: "je", options: ["je", "sú"] }, { prompt: "Okná ___ veľké.", answer: "sú", options: ["je", "sú"] },
    ], hint: "Сверьте связку с числом существительного.", explanation: "Taška и Lucia — единственное число; zošity и okná — множественное." },
    { id: "reinforcement:nominative:3", sectionIndex: 1, type: "pairs", prompt: "Замените одного человека или один предмет на несколько. Перепишите фразу целиком.", answer: "To sú zošity.; To sú tašky.; To sú okná.; To sú učitelia.", pairs: [
      { prompt: "To je zošit.", answer: "To sú zošity.", inputHint: "Введите фразу во множественном числе" },
      { prompt: "To je taška.", answer: "To sú tašky.", inputHint: "Введите фразу во множественном числе" },
      { prompt: "To je okno.", answer: "To sú okná.", inputHint: "Введите фразу во множественном числе" },
      { prompt: "To je učiteľ.", answer: "To sú učitelia.", inputHint: "Введите фразу во множественном числе" },
    ], hint: "Поменяйте je на sú и вспомните готовую форму множественного числа.", explanation: "Правильные пары: zošit — zošity, taška — tašky, okno — okná, učiteľ — učitelia." },
    { id: "reinforcement:nominative:4", sectionIndex: 4, type: "pairs", prompt: "Исправьте каждое предложение.", answer: "Tá taška je nová.; Tie zošity sú nové.; To sú noví učitelia.; Lucia je študentka.", pairs: [
      { prompt: "Tá taška je nový.", answer: "Tá taška je nová.", inputHint: "Введите исправленное предложение" },
      { prompt: "Tí zošity sú nové.", answer: "Tie zošity sú nové.", inputHint: "Введите исправленное предложение" },
      { prompt: "To sú nové učitelia.", answer: "To sú noví učitelia.", inputHint: "Введите исправленное предложение" },
      { prompt: "Lucia študentka.", answer: "Lucia je študentka.", inputHint: "Введите исправленное предложение" },
    ], hint: "Ищите одну ошибку в роде, числе, указательном слове или связке.", explanation: "Нормативные формы проверяются отдельно в каждой строке." },
    { id: "reinforcement:nominative:5", sectionIndex: 3, type: "pairs", prompt: "Переведите на словацкий.", answer: "To je učiteľka.; Ten zošit je malý.; Okná sú nové.; Tí učitelia sú milí.", pairs: [
      { prompt: "Это учительница.", answer: "To je učiteľka.", inputHint: "Введите перевод по-словацки" },
      { prompt: "Та тетрадь маленькая.", answer: "Ten zošit je malý.", inputHint: "Введите перевод по-словацки" },
      { prompt: "Окна новые.", answer: "Okná sú nové.", inputHint: "Введите перевод по-словацки" },
      { prompt: "Те учителя приветливые.", answer: "Tí učitelia sú milí.", inputHint: "Введите перевод по-словацки" },
    ], hint: "Проверьте словацкий род, число и окончания с диакритикой.", explanation: "Zošit — мужской род; okná — множественное число; мужская группа людей требует tí и milí." },
    { id: "reinforcement:nominative:6", sectionIndex: 3, type: "pairs", prompt: "Выберите пять согласованных фраз для короткого рассказа.", answer: "To je Adam.; Adam je študent.; To je malý zošit.; To sú nové tašky.; Tašky sú pekné.", pairs: [
      { prompt: "представьте человека", answer: "To je Adam.", options: ["To je Adam.", "To sú Adam.", "To Adam je."] },
      { prompt: "назовите его роль", answer: "Adam je študent.", options: ["Adam sú študent.", "Adam študent.", "Adam je študent."] },
      { prompt: "покажите один маленький предмет", answer: "To je malý zošit.", options: ["To je malá zošit.", "To je malý zošit.", "To sú malý zošit."] },
      { prompt: "покажите несколько новых предметов", answer: "To sú nové tašky.", options: ["To sú nové tašky.", "To je nová tašky.", "To sú noví tašky."] },
      { prompt: "добавьте ещё один признак", answer: "Tašky sú pekné.", options: ["Tašky je pekná.", "Tašky sú pekné.", "Tašky sú pekní."] },
    ], hint: "Каждая строка должна быть самостоятельной нормативной фразой уровня A1.", explanation: "Пять выбранных фраз образуют связный мини-текст без проверки свободного ответа по одному образцу." },
  ],
  knowledgeChecks: [
    { id: "m4-nominative-check-1", question: "Какая модель правильно называет одного человека?", options: ["Čo je to? — To sú študentka.", "Kto je to? — To je študentka.", "Kto sú to? — To je študentka."], answer: "Kto je to? — To je študentka.", explanation: "О человеке спрашиваем Kto?, один человек требует je." },
    { id: "m4-nominative-check-2", question: "Как правильно сказать «Те тетради новые»?", options: ["Tie zošity sú nové.", "Tí zošity sú noví.", "Tá zošity je nová."], answer: "Tie zošity sú nové.", explanation: "Предметы во множественном числе требуют tie, sú и nové." },
    { id: "m4-nominative-check-3", question: "Почему в Kniha je nová слово kniha стоит в Nominatíve?", options: ["Оно называет субъект сообщения", "После je всегда нужен Nominatív", "Все слова на -a всегда стоят в Nominatíve"], answer: "Оно называет субъект сообщения", explanation: "Падеж определяется ролью слова, а не одним окончанием или наличием je." },
  ],
  finalChecks: [
    { id: "m4-nominative-final-1", question: "Ответьте полным предложением: Kto je doma? — «Моя сестра дома».", options: ["Moja sestra je doma.", "Moju sestru je doma.", "Moja sestra sú doma."], answer: "Moja sestra je doma.", explanation: "Субъект остаётся в словарной форме, связка je обязательна." },
  ],
  chatPrompt: "Представьте человека, назовите его роль, затем покажите один предмет и несколько предметов с согласованным признаком.",
  chatSuggestions: ["To je Lucia. Lucia je učiteľka.", "To je malý zošit.", "To sú nové tašky."],
} satisfies CourseLesson;
