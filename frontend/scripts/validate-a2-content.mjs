import { existsSync, readFileSync, readdirSync } from "node:fs";
import { dirname, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";
import { runInNewContext } from "node:vm";
import ts from "typescript";

const root = resolve(fileURLToPath(new URL(".", import.meta.url)), "..");
const read = (path) => readFileSync(resolve(root, path), "utf8");
const fail = (message) => { throw new Error(`A2 content validation failed: ${message}`); };

const roadmap = read("app/data/a2CourseRoadmap.ts");
const plan = read("../course-content/slovak-a2/learning/runtime_implementation_plan.md");
const factory = read("app/data/a2/modules/module2/lessonFactory.ts");
const moduleIndex = read("app/data/a2/modules/module2/index.ts");
const lesson = read("app/data/a2/modules/module2/lessons/nominative-plural-things.ts");

function validateRoadmap() {
  const entries = [...roadmap.matchAll(/item\("([^"]+)", "([^"]+)"/g)];
  if (entries.length !== 31) fail(`expected 7/12/9/3 ready Module 1/2/3/4 topics, found ${entries.length}`);
  if (new Set(entries.map((entry) => entry[1])).size !== entries.length) fail("duplicate A2 lesson slug");
  const requiredTitles = [
    "Вид в связном рассказе: фон и цепочка событий",
    "Видовые пары с приставками",
    "Видовые пары с суффиксами и изменением основы",
    "Прилагательные: согласование во всех изученных падежах",
    "Прилагательные во множественном числе",
    "Степени сравнения прилагательных",
    "Наречия и их сравнение",
    "Личные местоимения в косвенных падежах",
    "Притяжательные слова и местоимение svoj",
    "Притяжательные прилагательные",
    "Неопределённые, отрицательные и обобщающие местоимения",
    "Числительные, даты и количество",
    "Что нужно уметь перед A2",
    "Вид глагола: процесс, повтор и результат",
    "Клитики и порядок слов: вторая позиция",
    "Семьи слов: как расширять словарный запас",
    "Карта падежей и управление",
    "Связность: тема, новая информация и смысловой акцент",
    "Произношение A2: связная речь",
    "Nominatív множественного числа: предметы и понятия",
    "Nominatív множественного числа: люди",
    "Akuzatív единственного числа: полное согласование",
    "Akuzatív множественного числа",
    "Genitív единственного числа: отсутствие, происхождение и границы",
    "Genitív количества и меры",
    "Genitív множественного числа",
    "Datív: адресат, польза и причина",
    "Lokál: место и тема разговора",
    "Inštrumentál: средство, совместность и характеристика",
    "Где, куда и откуда: падежные триады",
    "Падежи в одной системе: управление и обращение",
  ];
  for (const title of requiredTitles) if (!roadmap.includes(title)) fail(`roadmap title missing: ${title}`);
}

function validatePlan() {
  validateRoadmap();
  const requiredFragments = [
    "## Этап 1. Каркас A2 и пилот 2.1",
    "## Этап 2. Разделение состояния A1 и A2",
    "## Этап 3. Подключение A2 к интерфейсу",
    "## Этап 4. Ручная приёмка пилота",
    "## Этап 5. Остальные темы Module 2",
    "## Этап 6. Полный Module 1",
    "## Этап 7. Полный Module 3",
    "## Этап 8. Module 4: рассказ и видовые пары",
    "A1 продолжает работать без изменения существующих slug",
    "2.11-2.12",
    "validate:a2",
    "UI/Playwright-тесты запускаются только по прямому запросу владельца",
  ];
  for (const fragment of requiredFragments) if (!plan.includes(fragment)) fail(`implementation plan fragment missing: ${fragment}`);
  console.log("A2 runtime plan valid");
}

function validatePilot() {
  validateRoadmap();
  if (!moduleIndex.includes('from "./lessons/nominative-plural-things"')) fail("lesson 2.1 is not registered");
  if (!moduleIndex.includes("minSections: 5") || !moduleIndex.includes("minStepPractices: 5")) fail("pilot content requirements are incomplete");
  if (!factory.includes("a2-m2-") || !factory.includes("replace(/^a2-/")) fail("qualified activity prefix is missing");
  const requiredLessonFragments = [
    'defineA2Module2Lesson("a2-nominative-plural-things"',
    "kniha → knihy",
    "ulica → ulice",
    "dlaň → dlane",
    "kosť → kosti",
    "mesto → mestá",
    "srdce → srdcia",
    "stretnutie → stretnutia",
    "Tieto dôležité informácie sú presné.",
    "Jej nové autá sú drahé.",
    "showSlovakKeyboard: true",
  ];
  for (const fragment of requiredLessonFragments) if (!lesson.includes(fragment)) fail(`pilot source coverage missing: ${fragment}`);
  if ((lesson.match(/sectionIndex:/g) ?? []).length !== 5) fail("pilot must contain exactly five step practices");
  if ((lesson.match(/title: "/g) ?? []).length < 5) fail("pilot must contain five titled sections");
  if ((lesson.match(/\{ word: /g) ?? []).length < 10) fail("pilot vocabulary is too small");
  if (/TODO|placeholder|заполнить позже/i.test(lesson)) fail("pilot contains placeholder text");
  console.log("A2 lesson 2.1 pilot valid");
}

// Evaluate repository-owned data modules in memory, without emitting files.
const dataRoot = resolve(root, "app/data");
const cache = new Map();
function loadData(path) {
  const resolved = [path, `${path}.ts`, resolve(path, "index.ts")].find((candidate) => existsSync(candidate) && candidate.endsWith(".ts"));
  if (!resolved || !resolved.startsWith(`${dataRoot}${sep}`)) fail(`invalid data import: ${path}`);
  if (cache.has(resolved)) return cache.get(resolved).exports;
  const module = { exports: {} };
  cache.set(resolved, module);
  const { outputText } = ts.transpileModule(readFileSync(resolved, "utf8"), { compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2022 } });
  runInNewContext(outputText, { module, exports: module.exports, require: (specifier) => {
    if (!specifier.startsWith(".")) fail(`non-data import: ${specifier}`);
    return loadData(resolve(dirname(resolved), specifier));
  } }, { filename: resolved });
  return module.exports;
}

function validateReadyLessons() {
  const { a2Module2 } = loadData(resolve(dataRoot, "a2/modules/module2/index.ts"));
  const { a2CourseModules } = loadData(resolve(dataRoot, "a2/a2Course.ts"));
  const { plannedA2Modules } = loadData(resolve(dataRoot, "a2CourseRoadmap.ts"));
  const { a2ReadyLessonSlugs, coursePositionCatalog } = loadData(resolve(dataRoot, "coursePositionCatalog.ts"));
  const readyLessons = a2CourseModules.flatMap((module) => module.lessons);
  if (JSON.stringify(a2ReadyLessonSlugs) !== JSON.stringify(readyLessons.map((lesson) => lesson.slug))) fail("A2 position catalog differs from ready lessons");
  const positions = a2CourseModules.map((module) => ({ order: module.order, lessons: module.lessons.map(({ slug }) => ({ slug })) }));
  if (JSON.stringify(positions) !== JSON.stringify(coursePositionCatalog.A2)) fail("A2 module positions differ from runtime catalog");
  if (a2CourseModules.length !== 4 || a2CourseModules.some((module, index) => module.order !== index + 1)) fail("ready A2 modules must be Module1/2/3/4 in order");
  const { validateCourseModules } = loadData(resolve(dataRoot, "courseValidation.ts"));
  const { getPracticeMatch, buildModuleFinalQuestions, buildReinforcementPractices } = loadData(resolve(dataRoot, "coursePractice.ts"));
  const { resolveCoursePosition, isCourseFinalCompleted } = loadData(resolve(dataRoot, "courseLevelState.ts"));
  for (const module of a2CourseModules) {
    for (const lesson of module.lessons) {
      const restored = resolveCoursePosition(coursePositionCatalog.A2, { activeModule: module.order, selectedSlug: lesson.slug });
      if (restored.selectedSlug !== lesson.slug || restored.activeModule !== module.order) fail(`A2 position cannot restore: ${lesson.slug}`);
    }
    const final = buildModuleFinalQuestions(module.lessons);
    for (const lesson of module.lessons) if (final.filter((question) => question.lessonSlug === lesson.slug).length !== 2) fail(`final lacks two questions for ${lesson.slug}`);
  }
  const expandedFinal = buildModuleFinalQuestions(a2Module2.lessons);
  for (const lesson of a2Module2.lessons) {
    if (expandedFinal.filter((question) => question.lessonSlug === lesson.slug).length !== 2) fail(`final lacks two questions for ${lesson.slug}`);
  }
  for (const size of [1, 4, 7, 10]) {
    const oldFinal = buildModuleFinalQuestions(a2Module2.lessons.slice(0, size));
    const oldAnswers = Object.fromEntries(oldFinal.map((question) => [question.id, question.answer]));
    if (isCourseFinalCompleted("A2", true, expandedFinal.map((question) => question.id), oldAnswers)) fail(`old ${size}-topic A2 final closes expanded final`);
    if (oldFinal.some((question) => !expandedFinal.some((item) => item.id === question.id && item.answer === question.answer))) fail(`existing ${size}-topic final questions changed`);
  }
  validateCourseModules(a2CourseModules, []);
  // Positive control: malformed content must be rejected by the shared oracle.
  let badContentRejected = false;
  try { validateCourseModules([{ ...a2CourseModules[0], lessons: [] }], []); } catch { badContentRejected = true; }
  if (!badContentRejected) fail("shared content validator accepted empty module control");
  const firstFinal = buildModuleFinalQuestions(a2CourseModules[0].lessons);
  const oldModule2Answers = Object.fromEntries(expandedFinal.map((question) => [question.id, question.answer]));
  if (!isCourseFinalCompleted("A2", true, expandedFinal.map((question) => question.id), oldModule2Answers)) fail("completed Module2 final was invalidated by Module1");
  if (isCourseFinalCompleted("A2", true, firstFinal.map((question) => question.id), oldModule2Answers)) fail("Module2 answers completed Module1 final");
  const module3Final = buildModuleFinalQuestions(a2CourseModules[2].lessons);
  const previousAnswers = { ...oldModule2Answers, ...Object.fromEntries(firstFinal.map((question) => [question.id, question.answer])) };
  if (module3Final.length !== 18 || isCourseFinalCompleted("A2", true, module3Final.map(({ id }) => id), previousAnswers)) fail("Module3 final incomplete or completed by previous modules");
  const module4Final = buildModuleFinalQuestions(a2CourseModules[3].lessons);
  const earlierAnswers = { ...previousAnswers, ...Object.fromEntries(module3Final.map(({ id, answer }) => [id, answer])) };
  if (module4Final.length !== 6 || isCourseFinalCompleted("A2", true, module4Final.map(({ id }) => id), earlierAnswers)) fail("Module4 final incomplete or completed by previous modules");
  const ownAnswers = Object.fromEntries(module4Final.map(({ id, answer }) => [id, answer]));
  if (!isCourseFinalCompleted("A2", true, module4Final.map(({ id }) => id), ownAnswers)) fail("Module4 submitted final cannot complete");
  if (isCourseFinalCompleted("A2", false, module4Final.map(({ id }) => id), ownAnswers)) fail("Module4 completes without submitting");
  const allEarlierFinals = a2CourseModules.slice(0, 3).flatMap(({ lessons }) => buildModuleFinalQuestions(lessons));
  const answersWithModule4 = { ...earlierAnswers, ...ownAnswers };
  for (const earlier of a2CourseModules.slice(0, 3)) {
    if (!isCourseFinalCompleted("A2", true, buildModuleFinalQuestions(earlier.lessons).map(({ id }) => id), answersWithModule4)) fail("Module4 invalidated earlier final");
  }
  if (new Set([...allEarlierFinals, ...module4Final].map(({ id }) => id)).size !== allEarlierFinals.length + module4Final.length) fail("Module4 final ID collision");
  for (const module of a2CourseModules) {
    if (!/^Module \d+ — /.test(module.title) || module.title.startsWith("A2")) fail(`module title is not concise English: ${module.slug}`);
  }
  for (const module of a2CourseModules) {
    const planned = plannedA2Modules.find((item) => item.order === module.order);
    const indexSource = read(`app/data/a2/modules/module${module.order}/index.ts`);
    const files = readdirSync(resolve(dataRoot, `a2/modules/module${module.order}/lessons`)).filter((name) => name.endsWith(".ts"));
    const imports = [...indexSource.matchAll(/from "\.\/lessons\/([^"]+)"/g)].map((match) => `${match[1]}.ts`);
    if (files.length !== imports.length || files.some((name) => !imports.includes(name))) fail(`unregistered A2 Module${module.order} lesson file`);
    if (!planned || module.slug !== planned.slug || module.title !== planned.title || module.level !== "A2" || module.lessons.length !== files.length || module.lessons.length !== planned.lessons.length) fail(`incomplete A2 Module${module.order}`);
    const groupSlugs = (module.topicGroups ?? []).flatMap((group) => group.lessonSlugs);
    if (module.topicGroups?.length !== (module.order === 4 ? 1 : module.order === 2 ? 4 : 3) || JSON.stringify(groupSlugs) !== JSON.stringify(module.lessons.map((lesson) => lesson.slug))) fail(`A2 Module${module.order} groups must cover all lessons once in roadmap order`);
  }
  const { allCourseModules } = loadData(resolve(dataRoot, "courseCatalog.ts"));
  const ids = new Set();
  const slugs = new Set();
  for (const lesson of allCourseModules.flatMap((module) => module.lessons)) {
    if (slugs.has(lesson.slug)) fail(`global duplicate slug: ${lesson.slug}`);
    slugs.add(lesson.slug);
    for (const activity of [...lesson.stepPractices, ...(lesson.reinforcementPractices ?? []), ...lesson.knowledgeChecks, ...lesson.finalChecks]) {
      if (ids.has(activity.id)) fail(`global duplicate activity: ${activity.id}`);
      ids.add(activity.id);
    }
  }
  for (const module of a2CourseModules) {
  for (const [index, lesson] of module.lessons.entries()) {
    const planned = plannedA2Modules.find((item) => item.order === module.order).lessons[index];
    if (lesson.slug !== planned?.slug || lesson.title !== planned.title || lesson.description !== planned.outcome) fail(`roadmap mismatch: ${lesson.slug}`);
    if ((lesson.vocabulary?.length ?? 0) < 10 || /TODO|placeholder|заполнить позже/i.test(JSON.stringify(lesson))) fail(`incomplete content: ${lesson.slug}`);
    const prefix = `a2-m${module.order}-${lesson.slug.replace(/^a2-/, "")}`;
    for (const [kind, activities] of [["step", lesson.stepPractices], ["check", lesson.knowledgeChecks], ["final", lesson.finalChecks]]) {
      activities.forEach((activity, index) => { if (activity.id !== `${prefix}-${kind}-${index + 1}`) fail(`unstable activity ID: ${activity.id}`); });
    }
    const reinforcement = buildReinforcementPractices(lesson);
    if (reinforcement.length !== 6) fail(`incomplete reinforcement: ${lesson.slug}`);
    for (const practice of [...lesson.stepPractices, ...reinforcement]) {
      if ((!practice.id.startsWith(`a2-m${module.order}-`) && !practice.id.startsWith(`reinforcement:${lesson.slug}:`)) || (practice.type === "text" && !practice.showSlovakKeyboard)) fail(`practice contract: ${practice.id}`);
      const answer = practice.type === "pairs" ? JSON.stringify(practice.pairs.map((pair) => pair.answer)) : practice.answer;
      if (getPracticeMatch(practice, answer) !== "correct") fail(`canonical answer rejected: ${practice.id}`);
      if (practice.type === "choice" && practice.options.some((option) => option !== practice.answer && getPracticeMatch(practice, option) === "correct")) fail(`wrong choice accepted: ${practice.id}`);
      for (const pair of practice.pairs ?? []) {
        if ((pair.options ?? []).some((option) => option !== pair.answer && getPracticeMatch({ ...practice, type: "choice", answer: pair.answer, acceptableAnswers: pair.acceptableAnswers }, option) === "correct")) fail(`wrong pair choice accepted: ${practice.id}`);
      }
      for (const alternative of practice.acceptableAnswers ?? []) if (getPracticeMatch(practice, alternative) !== "correct") fail(`alternative rejected: ${practice.id}`);
      if (practice.type === "order" && getPracticeMatch(practice, practice.tokens.join(practice.tokenSeparator ?? " ")) !== "correct") fail(`order tokens mismatch: ${practice.id}`);
    }
    for (const check of [...lesson.knowledgeChecks, ...lesson.finalChecks]) {
      if (check.options.some((option) => option !== check.answer && getPracticeMatch({ ...check, type: "choice" }, option) === "correct")) fail(`wrong check choice accepted: ${check.id}`);
    }
  }
  }
  for (const module of a2CourseModules) {
    const stats = module.lessons.reduce((result, lesson) => ({ sections: result.sections + lesson.sections.length, practices: result.practices + lesson.stepPractices.length, vocabulary: result.vocabulary + lesson.vocabulary.length }), { sections: 0, practices: 0, vocabulary: 0 });
    console.log(`A2 Module${module.order} measured: ${JSON.stringify(stats)}; ${buildModuleFinalQuestions(module.lessons).length} final questions`);
  }
  console.log(`A2 runtime package valid: ${a2CourseModules.length} modules, ${readyLessons.length} lessons; global slug/activity IDs unique; answers accepted`);
}

const mode = process.argv[2] ?? "--all";
if (mode === "--plan") validatePlan();
else if (mode === "--pilot") validatePilot();
else if (mode === "--all") { validatePlan(); validatePilot(); validateReadyLessons(); }
else fail(`unknown mode: ${mode}`);
