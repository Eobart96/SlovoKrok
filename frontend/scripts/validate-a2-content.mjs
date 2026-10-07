import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { fileURLToPath } from "node:url";

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
  if (entries.length !== 12) fail(`expected 12 Module 2 roadmap topics, found ${entries.length}`);
  if (new Set(entries.map((entry) => entry[1])).size !== entries.length) fail("duplicate A2 lesson slug");
  const requiredTitles = [
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

const mode = process.argv[2] ?? "--all";
if (mode === "--plan") validatePlan();
else if (mode === "--pilot") validatePilot();
else if (mode === "--all") { validatePlan(); validatePilot(); }
else fail(`unknown mode: ${mode}`);
