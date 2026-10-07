import { readFileSync } from "node:fs";

const root = ".codex/skills/slovak-a2-study-module";
const skill = readFileSync(`${root}/SKILL.md`, "utf8");
const series = readFileSync(`${root}/references/series-spec.md`, "utf8");
const ui = readFileSync(`${root}/agents/openai.yaml`, "utf8");

const requiredSkill = [
  "course-content/slovak-a2/learning/learning_roadmap.md",
  "PROJECT_CHECKPOINT.md",
  "references/series-spec.md",
  "Do not reteach an A1 table",
  "15-20 Slovak examples",
  "5-6 exercises",
  "6-8 pages",
  "output/pdf/A2/Module_XX/",
  "Render every final page",
  "cite the final PDF exactly once",
];
const requiredSeries = [
  "#7B245F",
  "#CE3C92",
  "Default seven-page architecture",
  "Exercise progression",
  "output/pdf/A2/Module_01/Slovak_A2_Tema_1_5_Karta_padezhey.pdf",
];

for (const value of requiredSkill) {
  if (!skill.includes(value)) throw new Error(`Skill contract misses: ${value}`);
}
for (const value of requiredSeries) {
  if (!series.includes(value)) throw new Error(`Series specification misses: ${value}`);
}
if (!ui.includes("$slovak-a2-study-module") || !ui.includes("#7B245F")) {
  throw new Error("Skill UI metadata is incomplete");
}
if (/TODO|PLACEHOLDER/u.test(skill + series + ui)) {
  throw new Error("Skill contains unfinished scaffold text");
}

console.log("A2 study skill contract verified");
