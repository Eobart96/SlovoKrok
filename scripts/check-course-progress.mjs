import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

const roadmap = readFileSync("course-content/slovak-a1/learning/learning_roadmap.md", "utf8");
const checkpoint = readFileSync("PROJECT_CHECKPOINT.md", "utf8");
const readme = readFileSync("README.md", "utf8");
const green = "✅ Проверено и согласовано";
const blue = "🔵 Загружено — проверить";

function moduleTopics(order) {
  const start = roadmap.indexOf(`## Module ${order} —`);
  assert.notEqual(start, -1, `Module ${order} heading is missing`);
  const next = roadmap.indexOf(`## Module ${order + 1} —`, start + 1);
  const section = roadmap.slice(start, next === -1 ? roadmap.indexOf("## Статус наполнения", start) : next);
  return [...section.matchAll(/^\d+\. .+ — \*\*(.+)\*\*$/gm)].map((match) => match[1]);
}

const expectedCounts = [14, 7, 6, 11, 11, 18, 7, 9];
const modules = expectedCounts.map((expected, index) => {
  const topics = moduleTopics(index + 1);
  assert.equal(topics.length, expected, `Module ${index + 1} topic count changed`);
  return topics;
});

assert.equal(modules.flat().length, 83, "Course topic total changed");
assert.equal(modules.slice(0, 6).flat().filter((status) => status === green).length, 67, "Modules 1–6 must contain 67 approved topics");
assert.ok(modules.slice(0, 6).flat().every((status) => status === green), "Modules 1–6 must be fully approved");
assert.ok(modules[6].every((status) => status === blue), "Module 7 must remain awaiting review until the owner names completed topics");
assert.ok(modules[7].every((status) => status === blue), "Module 8 must remain awaiting review");
assert.match(roadmap, /Modules 1–6 полностью: 67 из 83 тем/);
assert.match(roadmap, /Module 7 сейчас проверяется владельцем/);
assert.match(checkpoint, /принял Modules 1–6: 67 уроков/);
assert.match(checkpoint, /Сейчас он проверяет Module 7/);
assert.match(readme, /Modules 1–6 \(67 уроков\) вручную проверены/);
assert.match(readme, /Module 7 проверяется сейчас/);

console.log("COURSE_PROGRESS_OK");
