import { readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";

const root = process.cwd();
const pdfRoot = join(root, "output", "pdf");
const roadmap = readFileSync(join(root, "course-content", "slovak-a2", "learning", "learning_roadmap.md"), "utf8");
const topics = [...roadmap.matchAll(/^\d+\. \*\*PDF (\d+)\.(\d+) — (.+?)\*\*/gmu)]
  .map((match) => ({ module: Number(match[1]), topic: Number(match[2]), id: `${match[1]}.${match[2]}` }));
if (topics.length !== 72) throw new Error(`Roadmap has ${topics.length} topics instead of 72`);

const flat = readdirSync(pdfRoot, { withFileTypes: true })
  .filter((entry) => entry.isFile() && /^Slovak_A2_Tema_\d+_\d+_.+\.pdf$/u.test(entry.name));
if (flat.length !== 0) throw new Error(`Flat A2 PDF duplicates remain: ${flat.map((entry) => entry.name).join(", ")}`);

const actual = new Map();
const counts = [];
for (let module = 1; module <= 8; module += 1) {
  const folder = `Module_${String(module).padStart(2, "0")}`;
  const dir = join(pdfRoot, "A2", folder);
  const files = readdirSync(dir, { withFileTypes: true })
    .filter((entry) => entry.isFile() && entry.name.endsWith(".pdf"));
  counts.push(files.length);
  for (const file of files) {
    const match = file.name.match(/^Slovak_A2_Tema_(\d+)_(\d+)_.+\.pdf$/u);
    if (!match) throw new Error(`Unexpected learner file in ${folder}: ${file.name}`);
    const id = `${Number(match[1])}.${Number(match[2])}`;
    if (Number(match[1]) !== module) throw new Error(`Wrong module folder for ${file.name}`);
    if (actual.has(id)) throw new Error(`Duplicate topic ${id}`);
    actual.set(id, join(dir, file.name));
  }
}

const expectedCounts = [7, 12, 9, 12, 8, 9, 8, 7];
if (counts.some((count, index) => count !== expectedCounts[index])) {
  throw new Error(`Wrong module counts: ${counts.join("/")}`);
}
for (const topic of topics) if (!actual.has(topic.id)) throw new Error(`Missing PDF ${topic.id}`);
if (actual.size !== 72) throw new Error(`Expected 72 unique PDFs, found ${actual.size}`);

for (const topic of topics) {
  const builder = join(root, "scripts", `build_a2_module_${topic.module}_${topic.topic}.py`);
  const text = readFileSync(builder, "utf8");
  const folder = `Module_${String(topic.module).padStart(2, "0")}`;
  if (!(text.includes(`/ \"A2\" / \"${folder}\" /`) || text.includes(`output/pdf/A2/${folder}/`))) {
    throw new Error(`Builder path was not migrated: ${builder}`);
  }
}

const scriptNames = readdirSync(join(root, "scripts"));

for (const name of scriptNames.filter((value) => /^verify-a2-pdf-.+\.py$/u.test(value))) {
  const text = readFileSync(join(root, "scripts", name), "utf8");
  if (/output(?:\/|\\)pdf(?:\/|\\)Slovak_A2_Tema_/u.test(text) || /"output" \/ "pdf" \/ "Slovak_A2_Tema_/u.test(text)) {
    throw new Error(`Verifier still points to the flat folder: ${name}`);
  }
}

console.log(`modules=${counts.join("/")}, total=${actual.size}`);
console.log("A2 PDF organization verified");
