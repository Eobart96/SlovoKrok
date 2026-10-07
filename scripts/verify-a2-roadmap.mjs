import { readFileSync } from "node:fs";

const roadmapPath = "course-content/slovak-a2/learning/learning_roadmap.md";
const text = readFileSync(roadmapPath, "utf8");

const count = (pattern) => [...text.matchAll(pattern)].length;
const modules = count(/^## Модуль /gmu);
const topics = count(/^\d+\. \*\*PDF /gmu);
const types = count(/^   - Тип:/gmu);
const results = count(/^   - Результат:/gmu);
const contents = count(/^   - Содержание:/gmu);

const requiredSections = [
  "## Логика новой структуры",
  "## Граница с A1",
  "## Карта официальных областей A2",
];
const requiredGrammar = [
  "nominatív",
  "genitív",
  "datív",
  "akuzatív",
  "lokál",
  "inštrumentál",
  "vokatív",
  "настоящее время",
  "прошедшее время",
  "аналитическое будущее",
  "синтетическое будущее",
  "вид глагола",
  "императив",
  "кондиционал",
  "сложные предложения",
];
const requiredCommunicativeAreas = [
  "Пространство вокруг нас",
  "Жизнь онлайн",
  "Работа и карьера",
  "Магазины и покупки",
  "Путешествия и отпуск",
  "Словакия и моя страна",
  "Семья, друзья и отношения",
  "Здоровье, образ жизни и спорт",
];
const requiredModes = [
  "рецепц",
  "продукц",
  "взаимодейств",
  "медиац",
];
const replacementTopic = "PDF 1.4 — Семьи слов: как расширять словарный запас";
const rejectedTopic = "PDF 1.4 — Существительные: род, число и модели основ";

if (
  requiredSections.some((heading) => !text.includes(heading)) ||
  modules !== 8 ||
  topics !== 72 ||
  types !== topics ||
  results !== topics ||
  contents !== topics
) {
  throw new Error(
    `A2 roadmap structure is incomplete: modules=${modules}, topics=${topics}, types=${types}, results=${results}, contents=${contents}`,
  );
}

if (!text.includes(replacementTopic) || text.includes(rejectedTopic)) {
  throw new Error("A2 roadmap item 1.4 was not replaced cleanly");
}

console.log("A2 roadmap structure verified");

const lowerText = text.toLocaleLowerCase("ru");

if (requiredGrammar.some((term) => !lowerText.includes(term.toLocaleLowerCase("ru")))) {
  throw new Error("A2 grammar spine is incomplete");
}

console.log("A2 grammar spine verified");

if (
  requiredCommunicativeAreas.some((term) => !text.includes(term)) ||
  requiredModes.some((term) => !lowerText.includes(term))
) {
  throw new Error("A2 communicative coverage is incomplete");
}

console.log("A2 communicative coverage verified");
console.log("A2 roadmap verification passed");
