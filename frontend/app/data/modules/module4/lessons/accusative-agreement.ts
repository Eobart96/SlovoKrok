import type { CourseLesson } from "../../../courseTypes";
import { defineModule4Lesson } from "../lessonFactory";

const baseAccusativeAgreementLesson = defineModule4Lesson("accusative-agreement", 2, {
  summary: "В Akuzatíve вся объектная группа согласуется по роду, числу и падежу, а понятный объект можно заменить личным местоимением.",
  model: "Tá nová taška → Hľadám tú novú tašku. Ten nový učiteľ → Vidím toho nového učiteľa. Hľadám tú tašku → Hľadám ju.",
  goals: ["Согласовывать прилагательное с объектом", "Изменять ten/tá и môj/moja", "Заменять объект формами ma/ťa/ho/ju/nás/vás/ich", "Выбирать порядок слов и форму после na"],
  rules: [
    "Три изменения для типа nový: nový → nového у мужского одушевлённого, nová → novú у женского, noví → nových у мужчин во множественном числе.",
    "Мужской предмет, средний род и остальные группы множественного числа в моделях урока сохраняют форму Nominatívu.",
    "Указательные и притяжательные слова меняются вместе с группой: ten → toho, tá → tú, môj → môjho, moja → moju, moji → mojich.",
    "Краткие объектные местоимения без предлога: ma, ťa, ho, ju, nás, vás, ich.",
    "После na нужны полные формы: na mňa, na teba, na neho, na ňu, na nás, na vás, na nich.",
    "В нейтральной фразе краткая форма следует за первым смысловым блоком: Vidím ho. Dnes ho vidím. Moja sestra ho pozná.",
  ],
  examples: [
    { slovak: "Čítam tú novú knihu.", russian: "Я читаю ту новую книгу." },
    { slovak: "Vidím nového kolegu.", russian: "Я вижу нового коллегу." },
    { slovak: "Poznám tých nových učiteľov.", russian: "Я знаю тех новых учителей." },
    { slovak: "Dnes ho nevidím.", russian: "Сегодня я его не вижу." },
    { slovak: "Čakám na ňu.", russian: "Я жду её." },
  ],
  primaryTitle: "Согласование всей группы",
  primaryTable: { headers: ["Группа", "Nominatív", "Akuzatív"], rows: [["мужской, одуш., ед. ч.", "nový učiteľ", "nového učiteľa"], ["мужской, предмет", "nový telefón", "nový telefón"], ["женский, ед. ч.", "nová taška", "novú tašku"], ["средний, ед. ч.", "nové auto", "nové auto"], ["мужчины, мн. ч.", "noví učitelia", "nových učiteľov"], ["остальные, мн. ч.", "nové tašky", "nové tašky"]] },
  secondaryTitle: "Указательные, притяжательные и личные формы",
  secondaryTable: { headers: ["Тип", "Nominatív → Akuzatív", "Пример"], rows: [["мужской, одуш.", "ten → toho; môj → môjho", "toho nového učiteľa"], ["женский", "tá → tú; moja → moju", "tú novú tašku"], ["мужчины, мн. ч.", "tí → tých; moji → mojich", "tých nových učiteľov"], ["личное без предлога", "on → ho; ona → ju", "Vidím ho. Poznám ju."], ["после na", "neho / ňu / nich", "Čakám na ňu."]] },
  boundaryItems: ["tvoj brat → tvojho brata", "naša učiteľka → našu učiteľku", "vaši priatelia → vašich priateľov", "Jej не склоняется в Hľadám jej novú tašku.", "Ju заменяет женщину; jej показывает принадлежность."],
  mistake: "Не меняйте только существительное и не ставьте краткую форму после предлога: tú novú tašku; na ňu, не na ju.",
  task: "Назовите человека или предмет с определением, затем замените всю группу местоимением ho, ju или ich.",
  productionPrompt: "Переведите: «Я читаю ту новую книгу».",
  productionAnswer: "Čítam tú novú knihu.",
  productionHint: "Женские формы tá/nová/kniha переходят в tú/novú/knihu.",
});

export const accusativeAgreementLesson = {
  vocabulary: [
    {"word":"Vidím nového učiteľa.","translation":"Я вижу нового учителя.","example":"Vidím nového učiteľa."},
    {"word":"Hľadám tú novú tašku.","translation":"Я ищу ту новую сумку.","example":"Hľadám tú novú tašku."},
    {"word":"Poznám tých nových učiteľov.","translation":"Я знаю тех новых учителей.","example":"Poznám tých nových učiteľov."},
    {"word":"Poznám Adama. Poznám ho.","translation":"Я знаю Адама. Я его знаю.","example":"Poznám Adama. Poznám ho."},
    {"word":"Dnes ho nevidím.","translation":"Сегодня я его не вижу.","example":"Dnes ho nevidím."},
    {"word":"Čakám na ňu.","translation":"Я жду её.","example":"Čakám na ňu."},
  ],
  ...baseAccusativeAgreementLesson,
  description: "Согласовывайте всю объектную группу и заменяйте понятный объект формами ho, ju или ich.",
  duration: "35–40 мин",
  goals: [
    "Подбирать прилагательное к объекту в Akuzatíve",
    "Использовать формы toho, tú, tvojho, moju и podobные",
    "Заменять понятный объект формами ma, ťa, ho, ju, nás, vás, ich",
    "Выбирать место краткой формы и полную форму после предлога na",
  ],
  theory: {
    summary: "В теме 2 вы изменяли существительное: Vidím učiteľa. Теперь вся объектная группа должна показать один род, число и падеж: Vidím nového učiteľa. Понятный объект можно заменить: Hľadám tú novú tašku. → Hľadám ju.",
    rules: [
      "Для типа nový запомните три изменения: мужской одушевлённый nový → nového, женский nová → novú, мужчины во множественном числе noví → nových.",
      "Проверяйте всю группу: učiteľ → učiteľa → nového učiteľa → Poznám nového učiteľa.",
      "Указательные формы: ten → toho у мужского одушевлённого, tá → tú у женского, tí → tých у мужчин во множественном числе; у остальных групп урока форма сохраняется.",
      "Притяжательные формы: môj → môjho, moja → moju, moji → mojich. Tvoj, náš и váš следуют той же логике; jeho, jej и ich в значении принадлежности не склоняются.",
      "Краткие личные формы без предлога: ma, ťa, ho, ju, nás, vás, ich. Выбирайте их по словацкому слову: zošit — мужской род, поэтому Mám ho.",
      "Краткая форма обычно следует за первым смысловым блоком: Vidím ho. Dnes ho vidím. Moja sestra ho pozná. Не начинайте нейтральную фразу с ma, ťa или ho.",
      "После na используйте полные формы: na mňa, na teba, na neho, na ňu, na nás, na vás, na nich. Краткие na ma, na ho, na ju неверны.",
    ],
    examples: [
      { slovak: "Vidím nového učiteľa.", russian: "Я вижу нового учителя.", explanation: "Мужское одушевлённое: nový учiteľ → nového učiteľa." },
      { slovak: "Hľadám tú novú tašku.", russian: "Я ищу ту новую сумку.", explanation: "В женской группе меняются tá, nová и taška." },
      { slovak: "Poznám tých nových učiteľov.", russian: "Я знаю тех новых учителей.", explanation: "Мужчины во множественном числе: tí noví učitelia → tých nových učiteľov." },
      { slovak: "Poznám Adama. Poznám ho.", russian: "Я знаю Адама. Я его знаю.", explanation: "Ho заменяет понятный объект мужского рода." },
      { slovak: "Dnes ho nevidím.", russian: "Сегодня я его не вижу.", explanation: "Краткая форма стоит после первого смыслового блока dnes." },
      { slovak: "Čakám na ňu.", russian: "Я жду её.", explanation: "После предлога na нужна полная форма ňu." },
    ],
  },
  sections: [
    {
      title: "Согласуем прилагательное",
      paragraphs: ["Прилагательное согласуется с существительным по роду, числу и падежу; у мужского рода важна одушевлённость. Согласование не означает, что каждое слово обязательно изменится."],
      table: { headers: ["Группа", "Nominatív", "Akuzatív"], rows: [
        ["мужской, одуш., ед. ч.", "nový učiteľ", "nového učiteľa"], ["мужской, неодуш., ед. ч.", "nový telefón", "nový telefón"],
        ["женский, ед. ч.", "nová taška", "novú tašku"], ["средний, ед. ч.", "nové auto", "nové auto"],
        ["люди мужского рода, мн. ч.", "noví učitelia", "nových učiteľov"], ["остальные группы урока, мн. ч.", "nové zošity / tašky / autá", "nové zošity / tašky / autá"],
      ] },
      items: ["новый → nového у мужского одушевлённого", "nová → novú у женского", "noví → nových у мужчин во множественном числе", "Mám nové auto: группа стоит в Akuzatíve, хотя форма совпадает с Nominatívom."],
      note: "Таблица показывает тип nový. У других типов прилагательных окончания могут отличаться.",
    },
    {
      title: "Тот, мой, твой: формы при имени",
      paragraphs: ["Ten/tá/to и môj/moja/moje выбираются по существительному. В Akuzatíve согласуйте каждое изменяемое слово полной группы."],
      table: { headers: ["Группа", "Указательное · N → A", "Притяжательное · N → A"], rows: [
        ["мужской одуш., ед. ч.", "ten → toho", "môj → môjho"], ["мужской неодуш., ед. ч.", "ten → ten", "môj → môj"],
        ["женский, ед. ч.", "tá → tú", "moja → moju"], ["средний, ед. ч.", "to → to", "moje → moje"],
        ["люди мужского рода, мн. ч.", "tí → tých", "moji → mojich"], ["остальные группы, мн. ч.", "tie → tie", "moje → moje"],
      ] },
      items: ["ten nový učiteľ → toho nového učiteľa", "tá nová taška → tú novú tašku", "tvoj brat → tvojho brata", "naša učiteľka → našu učiteľku", "vaši priatelia → vašich priateľov"],
      note: "Jeho, jej и ich в значении принадлежности не склоняются: Hľadám jej novú tašku. Для принадлежности самому действующему лицу обычно используют svoj: Čítam svoju knihu.",
    },
    {
      title: "Вместо имени: ho, ju, ich",
      paragraphs: ["Когда объект уже понятен, замените его личным местоимением. Выбирайте форму по словацкому слову и учитывайте первый смысловой блок и предлог."],
      table: { headers: ["Кого заменяем", "Обычная форма A", "По-русски", "Пример"], rows: [
        ["ja", "ma", "меня", "Vidíš ma?"], ["ty", "ťa", "тебя", "Počujem ťa."], ["on / ono", "ho", "его", "Hľadám ho."], ["ona", "ju", "её", "Poznám ju."],
        ["my", "nás", "нас", "Vidí nás."], ["vy", "vás", "вас", "Nevidím vás."], ["oni / ony", "ich", "их", "Hľadám ich."],
      ] },
      items: ["Vidím | ho.", "Dnes | ho | vidím.", "Moja sestra | ho | pozná.", "Полные формы после предлога: na neho, na ňu, na nich.", "Počujem ťa — нейтрально; Teba počujem — с акцентом на «тебя»."],
      note: "Ju заменяет женщину: Poznám ju. Jej сообщает принадлежность: Poznám jej brata. После na нельзя использовать краткие формы.",
    },
    {
      title: "Готовые фразы с переводом",
      paragraphs: ["В первых десяти примерах следите за согласованием, в остальных — за тем, кого или что заменяет местоимение."],
      table: { headers: ["Slovensky", "По-русски"], rows: [
        ["Čítam tú novú knihu.", "Я читаю ту новую книгу."], ["Vidím nového kolegu.", "Я вижу нового коллегу."],
        ["Kupujem ten malý zošit.", "Я покупаю ту маленькую тетрадь."], ["Hľadám tvoju novú tašku.", "Я ищу твою новую сумку."],
        ["Poznáš moju sestru?", "Ты знаешь мою сестру?"], ["Vidíš môjho brata?", "Ты видишь моего брата?"],
        ["Mám nové auto.", "У меня есть новая машина."], ["Poznám tých nových učiteľov.", "Я знаю тех новых учителей."],
        ["Kupujem tie malé tašky.", "Я покупаю те маленькие сумки."], ["Vidím jej nového kolegu.", "Я вижу её нового коллегу."],
        ["Poznám Adama. Poznám ho.", "Я знаю Адама. Я его знаю."], ["Vidím Evu. Vidím ju.", "Я вижу Еву. Я вижу её."],
        ["Mám auto. Mám ho.", "У меня есть машина. Она у меня."], ["Hľadám kľúče. Hľadám ich.", "Я ищу ключи. Я ищу их."],
        ["Dnes ho nevidím.", "Сегодня я его не вижу."], ["Počuješ ma?", "Ты меня слышишь?"],
        ["Áno, počujem ťa.", "Да, я тебя слышу."], ["Oni nás poznajú.", "Они нас знают."],
        ["Čakám na ňu.", "Я жду её."], ["Čakáme na vás.", "Мы ждём вас."],
      ] },
      items: ["Poznám ju: ju заменяет женщину.", "Poznám jej brata: jej сообщает, чей это брат; объект — jej brata."],
      note: "Сначала определите, заменяет ли форма объект целиком или сообщает принадлежность.",
    },
    {
      title: "Ошибки и самопроверка",
      table: { headers: ["Ошибка", "Правильно", "Почему"], rows: [
        ["nová knihu", "novú knihu", "Согласуйте признак."], ["ten nového učiteľa", "toho nového učiteľa", "Измените указательное слово."],
        ["na ju", "na ňu", "После предлога нужна полная форма."], ["Ho dnes vidím.", "Dnes ho vidím.", "Краткая форма следует за первым смысловым блоком."],
      ] },
      items: ["Проверьте каждое слово полной группы.", "При замене учитывайте словацкий род и число исходного объекта.", "Поставьте краткую форму после первого смыслового блока.", "После na выберите полную форму."],
      note: "Перед финальным тестом повторите четыре опоры: согласование всей группы → словацкий род при замене → положение местоимения → форма после предлога.",
    },
  ],
  stepPractices: [
    { id: "m4-accusative-agreement-step-1", sectionIndex: 0, type: "pairs", prompt: "Выберите форму прилагательного в Akuzatíve.", answer: "nového; novú; nové; nových", pairs: [
      { prompt: "Vidím ___ učiteľa.", answer: "nového", options: ["nový", "nového"] }, { prompt: "Čítam ___ knihu.", answer: "novú", options: ["nová", "novú"] },
      { prompt: "Mám ___ auto.", answer: "nové", options: ["nové", "novú"] }, { prompt: "Poznám ___ študentov.", answer: "nových", options: ["noví", "nových"] },
    ], hint: "Определите род, число и одушевлённость существительного.", explanation: "Правильно: nového, novú, nové, nových." },
    { id: "m4-accusative-agreement-step-2", sectionIndex: 1, type: "pairs", prompt: "Поставьте всю группу в Akuzatív, сохранив число.", answer: "ten malý zošit; tú novú tašku; môjho brata; tých nových učiteľov", pairs: [
      { prompt: "ten malý zošit", answer: "ten malý zošit", inputHint: "Введите всю группу в Akuzatíve" }, { prompt: "tá nová taška", answer: "tú novú tašku", inputHint: "Введите всю группу в Akuzatíve" },
      { prompt: "môj brat", answer: "môjho brata", inputHint: "Введите всю группу в Akuzatíve" }, { prompt: "tí noví učitelia", answer: "tých nových učiteľov", inputHint: "Введите всю группу в Akuzatíve" },
    ], hint: "Проверьте каждое изменяемое слово.", explanation: "Мужской предмет не меняется; женская и одушевлённые группы согласуются полностью." },
    { id: "m4-accusative-agreement-step-3", sectionIndex: 2, type: "pairs", prompt: "Замените объект местоимением, сохранив остальные слова.", answer: "Vidím ho.; Hľadám ju.; Dnes ich vidím.; Mám ho.", pairs: [
      { prompt: "Vidím Adama.", answer: "Vidím ho.", inputHint: "Введите фразу с местоимением" }, { prompt: "Hľadám tú novú tašku.", answer: "Hľadám ju.", inputHint: "Введите фразу с местоимением" },
      { prompt: "Dnes vidím učiteľov.", answer: "Dnes ich vidím.", inputHint: "Введите фразу с местоимением" }, { prompt: "Mám nový zošit.", answer: "Mám ho.", inputHint: "Введите фразу с местоимением" },
    ], hint: "Учитывайте словацкий род, число и первый смысловой блок.", explanation: "Adama и zošit заменяет ho, tašku — ju, učiteľov — ich." },
    { id: "m4-accusative-agreement-step-4", sectionIndex: 3, type: "choice", prompt: "Как правильно сказать «Сегодня я его не вижу»?", options: ["Ho dnes nevidím.", "Dnes ho nevidím.", "Dnes nevidím na ho."], answer: "Dnes ho nevidím.", hint: "Краткая форма следует за первым смысловым блоком.", explanation: "Нейтральный порядок: Dnes ho nevidím." },
    { id: "m4-accusative-agreement-step-5", sectionIndex: 4, type: "pairs", prompt: "Исправьте каждую фразу.", answer: "Čakám na neho.; Dnes ho vidím.; Poznám ju.", pairs: [
      { prompt: "Čakám na ho.", answer: "Čakám na neho.", acceptableAnswers: ["Čakám naňho."], inputHint: "Введите исправленную фразу" },
      { prompt: "Ho dnes vidím.", answer: "Dnes ho vidím.", inputHint: "Введите исправленную фразу" },
      { prompt: "Poznám ona.", answer: "Poznám ju.", inputHint: "Введите исправленную фразу" },
    ], hint: "Используйте обычные нейтральные формы без особого выделения.", explanation: "После na нужна neho/naňho; краткое ho следует за dnes; ona заменяется формой ju." },
  ],
  assessmentMode: "interactive",
  materialAssessmentStep: false,
  reinforcementLabel: "Финальный тест темы",
  reinforcementTitle: "Выполните шесть заданий темы 3",
  reinforcementPractices: [
    { id: "reinforcement:accusative-agreement:1", sectionIndex: 0, type: "pairs", prompt: "Выберите нужную форму прилагательного.", answer: "nového; novú; nové; nových", pairs: [
      { prompt: "Vidím ___ učiteľa.", answer: "nového", options: ["nový", "nového"] }, { prompt: "Čítam ___ knihu.", answer: "novú", options: ["nová", "novú"] },
      { prompt: "Mám ___ auto.", answer: "nové", options: ["nové", "novú"] }, { prompt: "Poznám ___ študentov.", answer: "nových", options: ["noví", "nových"] },
    ], hint: "Слева форма Nominatívu или совпадающая форма, справа изменённая форма Akuzatívu.", explanation: "Правильно: nového, novú, nové, nových." },
    { id: "reinforcement:accusative-agreement:2", sectionIndex: 1, type: "pairs", prompt: "Поставьте всю группу в Akuzatív; число сохраните.", answer: "ten malý zošit; tú novú tašku; môjho brata; tých nových učiteľov", pairs: [
      { prompt: "ten malý zošit", answer: "ten malý zošit", inputHint: "Введите всю группу" }, { prompt: "tá nová taška", answer: "tú novú tašku", inputHint: "Введите всю группу" },
      { prompt: "môj brat", answer: "môjho brata", inputHint: "Введите всю группу" }, { prompt: "tí noví učitelia", answer: "tých nových učiteľov", inputHint: "Введите всю группу" },
    ], hint: "Проверьте указательное или притяжательное слово, прилагательное и существительное.", explanation: "Каждая группа сохраняет исходное число и получает нормативные формы Akuzatívu." },
    { id: "reinforcement:accusative-agreement:3", sectionIndex: 2, type: "pairs", prompt: "Замените выделенную группу местоимением и сохраните остальные слова.", answer: "Vidím ho.; Hľadám ju.; Dnes ich vidím.; Mám ho.", pairs: [
      { prompt: "Vidím Adama.", answer: "Vidím ho.", inputHint: "Введите фразу с местоимением" }, { prompt: "Hľadám tú novú tašku.", answer: "Hľadám ju.", inputHint: "Введите фразу с местоимением" },
      { prompt: "Dnes vidím učiteľov.", answer: "Dnes ich vidím.", inputHint: "Введите фразу с местоимением" }, { prompt: "Mám nový zošit.", answer: "Mám ho.", inputHint: "Введите фразу с местоимением" },
    ], hint: "Выберите ho, ju или ich и проверьте порядок слов.", explanation: "Правильно: Vidím ho. Hľadám ju. Dnes ich vidím. Mám ho." },
    { id: "reinforcement:accusative-agreement:4", sectionIndex: 4, type: "pairs", prompt: "Исправьте каждую фразу.", answer: "Čakám na neho.; Dnes ho vidím.; Poznám ju.", pairs: [
      { prompt: "Čakám na ho.", answer: "Čakám na neho.", acceptableAnswers: ["Čakám naňho."], inputHint: "Введите исправленную фразу" },
      { prompt: "Ho dnes vidím.", answer: "Dnes ho vidím.", inputHint: "Введите исправленную фразу" },
      { prompt: "Poznám ona.", answer: "Poznám ju.", inputHint: "Введите исправленную фразу" },
    ], hint: "Проверьте предлог, форму местоимения и первый смысловой блок.", explanation: "Čakám na neho/naňho; Dnes ho vidím; Poznám ju." },
    { id: "reinforcement:accusative-agreement:5", sectionIndex: 3, type: "pairs", prompt: "Переведите на словацкий.", answer: "Poznáš moju sestru?; Vidím tvojho brata.; Dnes ich nevidím.; Čakám na ňu.", pairs: [
      { prompt: "Ты знаешь мою сестру?", answer: "Poznáš moju sestru?", inputHint: "Введите перевод по-словацки" },
      { prompt: "Я вижу твоего брата.", answer: "Vidím tvojho brata.", inputHint: "Введите перевод по-словацки" },
      { prompt: "Сегодня я их не вижу.", answer: "Dnes ich nevidím.", inputHint: "Введите перевод по-словацки" },
      { prompt: "Я жду её.", answer: "Čakám na ňu.", inputHint: "Введите перевод по-словацки" },
    ], hint: "Проверьте согласование, положение краткой формы и форму после na.", explanation: "Нормативные формы: moju sestru, tvojho brata, Dnes ich nevidím, na ňu." },
    { id: "reinforcement:accusative-agreement:6", sectionIndex: 3, type: "pairs", prompt: "Соберите три пары: полная группа и её замена местоимением.", answer: "Poznám nového kolegu.; Dnes ho vidím.; Čítam tú novú knihu.; Mám ju doma.; Hľadám tie malé tašky.; Nevidím ich.", pairs: [
      { prompt: "назовите нового коллегу", answer: "Poznám nového kolegu.", options: ["Poznám nový kolega.", "Poznám nového kolegu.", "Poznám nové kolegu."] },
      { prompt: "замените коллегу после dnes", answer: "Dnes ho vidím.", options: ["Ho dnes vidím.", "Dnes ho vidím.", "Dnes vidím na ho."] },
      { prompt: "назовите ту новую книгу", answer: "Čítam tú novú knihu.", options: ["Čítam tá nová kniha.", "Čítam tú novú knihu.", "Čítam to nové knihu."] },
      { prompt: "замените книгу", answer: "Mám ju doma.", options: ["Mám ho doma.", "Mám ju doma.", "Mám jej doma."] },
      { prompt: "назовите те маленькие сумки", answer: "Hľadám tie malé tašky.", options: ["Hľadám tí malí tašky.", "Hľadám tie malé tašky.", "Hľadám tú malú tašky."] },
      { prompt: "замените сумки", answer: "Nevidím ich.", options: ["Nevidím ju.", "Nevidím ich.", "Nevidím ho."] },
    ], hint: "В каждой паре второе предложение заменяет всю объектную группу.", explanation: "Три пары используют ho, ju и ich; первая замена начинается с dnes." },
  ],
  knowledgeChecks: [
    { id: "m4-accusative-agreement-check-1", question: "Как правильно сказать «Я вижу того нового учителя»?", options: ["Vidím ten nového učiteľa.", "Vidím toho nového učiteľa.", "Vidím toho nový učiteľ."], answer: "Vidím toho nového učiteľa.", explanation: "В мужской одушевлённой группе меняются указательное слово, прилагательное и существительное." },
    { id: "m4-accusative-agreement-check-2", question: "Какая форма заменяет taška как понятный объект?", options: ["ju", "ho", "jej"], answer: "ju", explanation: "Taška — женский род; ju заменяет объект, а jej сообщает принадлежность." },
    { id: "m4-accusative-agreement-check-3", question: "Какая нейтральная фраза имеет правильный порядок?", options: ["Dnes ho vidím.", "Ho dnes vidím.", "Dnes vidím ho."], answer: "Dnes ho vidím.", explanation: "Краткая форма следует за первым смысловым блоком dnes." },
  ],
  finalChecks: [
    { id: "m4-accusative-agreement-final-1", question: "Переведите: «Я читаю ту новую книгу».", options: ["Čítam tú novú knihu.", "Čítam tá nová kniha.", "Čítam toho nového knihu."], answer: "Čítam tú novú knihu.", explanation: "Женские формы tá/nová/kniha переходят в tú/novú/knihu." },
  ],
  chatPrompt: "Назовите три объекта с определением, затем замените их формами ho, ju и ich. Одну фразу начните с dnes.",
  chatSuggestions: ["Poznám nového kolegu. Dnes ho vidím.", "Čítam tú novú knihu. Mám ju doma.", "Hľadám tie malé tašky. Nevidím ich."],
} satisfies CourseLesson;
