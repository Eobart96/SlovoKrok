const fs = require('node:fs');
const path = require('node:path');
const Module = require('node:module');
const root = path.resolve(__dirname, '..');
const ts = require(path.join(root, 'frontend/node_modules/typescript'));
Module._extensions['.ts'] = (module, filename) => module._compile(ts.transpileModule(fs.readFileSync(filename, 'utf8'), { compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2022 } }).outputText, filename);
const { a1CourseModules } = require(path.join(root, 'frontend/app/data/a1Course.ts'));
const lessons = a1CourseModules.flatMap(module => module.lessons.map(lesson => ({ ...lesson, module: module.order })));
fs.mkdirSync(path.join(root, 'tmp/basic-task-pack'), { recursive: true });
for (const range of [[1, 4], [5, 8]]) {
  const data = lessons.filter(lesson => lesson.module >= range[0] && lesson.module <= range[1]).map(({ slug, title, module, theory, vocabulary }) => ({ slug, title, module, theory, vocabulary }));
  fs.writeFileSync(path.join(root, `tmp/basic-task-pack/lessons-${range[0]}-${range[1]}.json`), JSON.stringify(data, null, 2));
}

const personal = /(?<![\p{L}])(?:Boris|Marina|Марина|Horváth|Nováková|Novák|Ari|Ари|Eva|Eve|Evu|Evou|Peter|Petra|Petrovi|Petrom|Martin|Martina|Jana|Ján|Jan|Anna|Annu|Anny|Lucia|Luciu|Lucie|Lucii|Luciou|Katk(?:a|u|e|ou)|Mári(?:a|u|e|i|ou)|Tomáš|Zuzana|Andrej|Michal|Juraj|Lukáš|Adam(?:a|ovi|om)?|Nin(?:a|u|e|ou)|Em(?:a|u|e|ou)|Marek|Marka|Ivan(?:a|ovi|om)?|Адам[ау]?|Нин[ауы]|Иван[ау]?|Анн[ауы]|Ев[ауе]|Петр|Пётр|Мартин[ау]?|Луци[яюией]+|Мария|Иван|Алексей|IT|ИТ)(?![\p{L}])|[\w.+-]+@[\w.-]+\.[a-z]{2,}|\+421[\d\s-]{6,}/iu;
function neutral(value) {
  if (typeof value === 'string') return !personal.test(value);
  if (Array.isArray(value)) return value.every(neutral);
  if (value && typeof value === 'object') return Object.entries(value).every(([key, item]) => key === 'lesson_slug' || neutral(item));
  return true;
}
function convert(practice) {
  if (!neutral(practice)) return null;
  const base = { interaction_type: 'text', options: [], tokens: [], pairs: [], accepted_answers: [...new Set([practice.answer, ...(practice.acceptableAnswers ?? [])])].slice(0, 5) };
  if (!practice.answer || practice.type !== 'pairs' && base.accepted_answers.some(answer => answer.length > 500)) return null;
  if (practice.type === 'choice') {
    if (!practice.options || practice.options.length < 2 || practice.options.length > 6 || practice.options.some(option => option.length > 200) || !practice.options.includes(practice.answer)) return null;
    base.interaction_type = 'choice'; base.options = practice.options; base.accepted_answers = [practice.answer];
  }
  if (practice.type === 'order' && practice.tokenSeparator !== '') {
    const normalize = value => value.normalize('NFKC').toLowerCase().trim().replace(/\s+/g, ' ').replace(/\s+([,.;:!?])/g, '$1').replace(/^[ .!?…]+|[ .!?…]+$/g, '');
    const tokens = practice.tokens ?? [];
    if (tokens.length >= 2 && tokens.length <= 12 && tokens.every(token => token.length <= 100 && !normalize(token).includes(' ')) && JSON.stringify(tokens.map(normalize).sort()) === JSON.stringify(normalize(practice.answer).split(' ').sort())) {
      base.interaction_type = 'order'; base.tokens = tokens; base.accepted_answers = [practice.answer];
    } else return null;
  }
  if (practice.type === 'pairs') {
    const pairs = (practice.pairs ?? []).map(({ prompt, answer }) => ({ prompt, answer }));
    if (pairs.some(pair => /[;→\n]/u.test(pair.prompt + pair.answer))) return null;
    if (pairs.length < 2 || pairs.length > 5 || pairs.some(pair => pair.prompt.length > 200 || pair.answer.length > 200) || new Set(pairs.map(pair => pair.prompt)).size !== pairs.length || new Set(pairs.map(pair => pair.answer)).size !== pairs.length) return null;
    base.interaction_type = 'match'; base.pairs = pairs; base.accepted_answers = [];
  }
  return { question: practice.prompt, instruction: base.interaction_type === 'text' ? 'Запишите короткий ответ на задание. Используйте словацкие знаки, где они нужны.' : base.interaction_type === 'choice' ? 'Выберите один правильный вариант.' : base.interaction_type === 'order' ? 'Соберите фразу из предложенных слов.' : 'Соедините слова или фразы с правильными соответствиями.', interaction: base };
}
function exercisePool(lesson) {
  const source = [...lesson.stepPractices, ...(lesson.reinforcementPractices ?? [])];
  if (lesson.slug === 'simple-mediation') source.push(
    { type: 'text', prompt: 'Передайте по-словацки: «Преподаватель пишет, что занятие завтра».', answer: 'Učiteľ píše, že kurz je zajtra.' },
    { type: 'text', prompt: 'Передайте по-словацки: «Встреча в понедельник в девять».', answer: 'Stretnutie je v pondelok o deviatej.' },
    { type: 'text', prompt: 'Передайте по-словацки: «Нам нужно принести книгу».', answer: 'Máme priniesť knihu.' },
    { type: 'text', prompt: 'Передайте по-словацки: «Билет стоит двенадцать евро».', answer: 'Lístok stojí dvanásť eur.' },
  );
  const individualPairs = source.flatMap(practice => (practice.pairs ?? []).map(pair => ({ ...pair, prompt: `${practice.prompt}\n${pair.prompt}`, type: pair.options?.length >= 2 ? 'choice' : 'text' })));
  const pool = [...source, ...individualPairs, ...lesson.knowledgeChecks.map(check => ({ ...check, prompt: check.question, type: 'choice' })), ...lesson.finalChecks.map(check => ({ ...check, prompt: check.question, type: 'choice' }))].map(convert).filter(Boolean);
  const unique = [...new Map(pool.map(item => [JSON.stringify([item.question, item.interaction]), item])).values()];
  return unique;
}
const timestamp = '2026-10-07T00:00:00Z';
const pack = { format: 'slovokrok-course-materials', version: 1, exported_at: timestamp, exercises: [], readings: [], homework: [] };
for (const [lessonIndex, lesson] of lessons.entries()) {
  const pool = exercisePool(lesson);
  const queues = ['choice', 'text', 'order', 'match'].map(type => pool.filter(item => item.interaction.interaction_type === type));
  const chosen = [];
  while (chosen.length < 20 && queues.some(queue => queue.length)) {
    for (const queue of queues) if (queue.length && chosen.length < 20) chosen.push(queue.shift());
  }
  if (chosen.length !== 20) throw new Error(`Need 20 unique neutral exercises for ${lesson.slug}, got ${chosen.length}`);
  const theory = [`Тема: ${lesson.title}`, ...lesson.theory.rules.filter(neutral).slice(0, 3)].join('\n');
  chosen.forEach((item, index) => {
    const interaction = { ...item.interaction };
    if (interaction.options.length) {
      const shift = (lessonIndex + index) % interaction.options.length;
      interaction.options = [...interaction.options.slice(shift), ...interaction.options.slice(0, shift)];
    }
    pack.exercises.push({ lesson_slug: lesson.slug, lesson_title: lesson.title, question: `[Базовый пакет · ${String(index + 1).padStart(2, '0')}/20]\n${item.question}`, instruction: item.instruction, theory_snapshot: 'slovokrok-exercise:v1:' + JSON.stringify({ theory, ...interaction }), created_at: timestamp });
  });
}
if (process.argv.includes('--exercises-only')) {
  fs.writeFileSync(path.join(root, 'tmp/basic-task-pack/exercises.json'), JSON.stringify(pack, null, 2));
  console.log(`EXERCISES_READY topics=${lessons.length} exercises=${pack.exercises.length}`);
} else {
  const content = Object.assign({}, ...['texts-1-4.json', 'texts-5-8.json'].map(name => JSON.parse(fs.readFileSync(path.join(root, 'course-content/basic-task-pack', name), 'utf8'))));
  if (Object.keys(content).length !== lessons.length || Object.keys(content).some(slug => !lessons.some(lesson => lesson.slug === slug))) throw new Error('Text content does not match course roster');
  for (const lesson of lessons) {
    const items = content[lesson.slug];
    if (items.readings?.length !== 2 || items.homework?.length !== 2) throw new Error(`Need 2 readings and 2 homework for ${lesson.slug}`);
    items.readings.forEach(item => pack.readings.push({ lesson_slug: lesson.slug, lesson_title: lesson.title, ...item, created_at: timestamp }));
    const theory = [`Тема: ${lesson.title}`, ...lesson.theory.rules.filter(neutral).slice(0, 3)].join('\n');
    items.homework.forEach(item => pack.homework.push({ lesson_slug: lesson.slug, lesson_title: lesson.title, ...item, theory_snapshot: theory, created_at: timestamp }));
  }
  if (!neutral(pack)) throw new Error('Personal name, IT profile, or contact found in pack');
  for (const kind of ['readings', 'homework']) {
    const bodies = pack[kind].map(item => item.text ?? item.description);
    if (new Set(bodies).size !== bodies.length) throw new Error(`Duplicate ${kind} bodies`);
  }
  const destination = path.join(root, 'frontend/public/task-packs/slovokrok-a1-basic-v1.json');
  fs.mkdirSync(path.dirname(destination), { recursive: true });
  fs.writeFileSync(destination, JSON.stringify(pack, null, 2) + '\n');
  console.log(`BASIC_TASK_PACK_READY topics=${lessons.length} exercises=${pack.exercises.length} readings=${pack.readings.length} homework=${pack.homework.length} bytes=${fs.statSync(destination).size}`);
}
