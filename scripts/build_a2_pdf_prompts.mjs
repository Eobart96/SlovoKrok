import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";

const roadmapPath = "course-content/slovak-a2/learning/learning_roadmap.md";
const outputPath = "output/txt/Slovak_A2_PDF_prompts.txt";
const roadmap = readFileSync(roadmapPath, "utf8");

const modulePattern = /^## Модуль (\d+) — (.+)$/gmu;
const modules = [...roadmap.matchAll(modulePattern)].map((match, index, all) => ({
  number: Number(match[1]),
  title: match[2].trim(),
  start: match.index,
  end: all[index + 1]?.index ?? roadmap.length,
}));

const topics = [];
for (const module of modules) {
  const section = roadmap.slice(module.start, module.end);
  const topicPattern = /^\d+\. \*\*PDF (\d+\.\d+) — (.+?)\*\*\r?\n   - Тип: (.+?)\r?\n   - Результат: (.+?)\r?\n   - Содержание: (.+?)$/gmu;
  for (const match of section.matchAll(topicPattern)) {
    topics.push({
      id: match[1],
      title: match[2].trim(),
      type: match[3].trim(),
      result: match[4].trim(),
      content: match[5].trim(),
      moduleNumber: module.number,
      moduleTitle: module.title,
    });
  }
}

if (topics.length !== 72) {
  throw new Error(`Expected 72 roadmap topics, found ${topics.length}`);
}

const header = `ПРОМТЫ ДЛЯ СОЗДАНИЯ 72 PDF КУРСА СЛОВАЦКОГО A2

Как пользоваться:
1. Найдите нужный номер PDF.
2. Скопируйте текст между строками «НАЧАЛО ПРОМТА» и «КОНЕЦ ПРОМТА».
3. Отправьте его Codex в рабочей папке SlovoKrok.
4. Навык $slovak-a2-study-module сам прочитает дорожную карту, правила серии,
   создаст PDF и выполнит все проверки.

Ничего дописывать не требуется. Постоянные правила больше не повторяются в
каждом запросе: они хранятся в проектном навыке SlovoKrok.

ПРОГРЕСС: PDF 1.1-1.7 и 2.1-2.8 готовы и полностью проверены.
СЛЕДУЮЩИЙ PDF: 2.9 «Lokál: место и тема разговора».
`;

const blocks = topics.map((topic, index) => {
  const number = String(index + 1).padStart(2, "0");
  return `
================================================================================
ПРОМТ ${number} ИЗ 72 — PDF ${topic.id}
МОДУЛЬ ${topic.moduleNumber}: ${topic.moduleTitle}
================================================================================
НАЧАЛО ПРОМТА

Используй навык $slovak-a2-study-module. Создай и полностью проверь PDF A2
${topic.id} «${topic.title}» по актуальной дорожной карте SlovoKrok. Не
возвращай план или черновик — открой и отдай готовый PDF.

КОНЕЦ ПРОМТА
`;
});

mkdirSync(dirname(outputPath), { recursive: true });
writeFileSync(outputPath, header + blocks.join(""), "utf8");
console.log(`Created ${topics.length} prompts at ${outputPath}`);
