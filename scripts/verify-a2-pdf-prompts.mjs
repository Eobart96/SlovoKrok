import { readFileSync } from "node:fs";

if (process.argv[2] !== "--compact") {
  throw new Error("Use --compact");
}

const roadmap = readFileSync("course-content/slovak-a2/learning/learning_roadmap.md", "utf8");
const text = readFileSync("output/txt/Slovak_A2_PDF_prompts.txt", "utf8");
const topics = [...roadmap.matchAll(
  /^\d+\. \*\*PDF (\d+\.\d+) — (.+?)\*\*/gmu,
)].map((match) => ({ id: match[1], title: match[2].trim() }));
const prompts = [...text.matchAll(
  /НАЧАЛО ПРОМТА\r?\n([\s\S]*?)\r?\nКОНЕЦ ПРОМТА/gmu,
)].map((match) => match[1].trim());

if (topics.length !== 72 || prompts.length !== 72) {
  throw new Error(`Expected 72 topics and prompts, got ${topics.length} and ${prompts.length}`);
}

for (const [index, topic] of topics.entries()) {
  const prompt = prompts[index];
  for (const required of [
    "$slovak-a2-study-module",
    `PDF A2\n${topic.id} «${topic.title}»`,
    "актуальной дорожной карте SlovoKrok",
    "готовый PDF",
  ]) {
    if (!prompt.includes(required)) {
      throw new Error(`Prompt ${topic.id} misses: ${required}`);
    }
  }
  if (prompt.length > 420) {
    throw new Error(`Prompt ${topic.id} is too long: ${prompt.length} chars`);
  }
  for (const repeated of ["15-20", "5-6 упражнений", "#7B245F", "Отрендери каждую"]) {
    if (prompt.includes(repeated)) {
      throw new Error(`Prompt ${topic.id} repeats skill detail: ${repeated}`);
    }
  }
}

if (new Set(prompts).size !== 72) {
  throw new Error("Compact prompts are not distinct");
}

console.log("A2 compact prompt file verified");
