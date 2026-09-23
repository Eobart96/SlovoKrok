import { createHash } from "node:crypto";
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { fileURLToPath } from "node:url";

const sourceRoot = process.argv[2];
if (!sourceRoot) throw new Error("Pass the folder containing the reviewed Russian–Slovak TXT files.");

const frontendRoot = resolve(fileURLToPath(new URL(".", import.meta.url)), "..");
const outputPath = resolve(frontendRoot, "app/data/additionalVocabularyCatalog.json");
const sourceSpecs = [
  ["word", "Все слова 1 часть — Русско-Словацкий.txt"],
  ["word", "Все слова 2 часть — Русско-Словацкий.txt"],
  ["sentence", "Все предложения 1 часть — Русско-Словацкий.txt"],
  ["sentence", "Все предложения 2 часть — Русско-Словацкий.txt"],
];

const lessonSlugs = Array.from({ length: 8 }, (_, index) => {
  const source = readFileSync(resolve(frontendRoot, `app/data/modules/module${index + 1}/index.ts`), "utf8");
  return [...source.matchAll(/from "\.\/lessons\/([^"]+)"/g)].map((match) => match[1]);
}).flat();
if (lessonSlugs.length !== 83 || new Set(lessonSlugs).size !== 83 || lessonSlugs.indexOf("present-tense") !== 38) {
  throw new Error("The A1 lesson sequence no longer matches the reviewed import contract.");
}

const previousAssignments = new Map();
const previousSections = new Map();
const previousStorageSources = new Map();
let previousDistributionVersion = 0;
if (existsSync(outputPath)) {
  const previous = JSON.parse(readFileSync(outputPath, "utf8"));
  previousDistributionVersion = previous.distributionVersion ?? 0;
  for (const entry of previous.entries ?? []) {
    previousAssignments.set(entry.id, entry.unlockAfterLessonSlug);
    if (entry.sectionId) previousSections.set(entry.id, entry.sectionId);
    const pluralKind = entry.kind === "word" ? "words" : "sentences";
    previousStorageSources.set(entry.id, entry.storageSourceId ?? `expanded-${pluralKind}-${entry.unlockAfterLessonSlug}`);
  }
}

const sha256 = (value) => createHash("sha256").update(value).digest("hex");
const rows = [];
const sourceHashes = {};
const sourceCounts = { words: 0, sentences: 0 };
for (const [kind, filename] of sourceSpecs) {
  const path = resolve(sourceRoot, filename);
  const bytes = readFileSync(path);
  sourceHashes[filename] = sha256(bytes).toUpperCase();
  const lines = bytes.toString("utf8").replace(/^\ufeff/, "").split(/\r?\n/).filter((line) => line.trim());
  sourceCounts[kind === "word" ? "words" : "sentences"] += lines.length;
  for (const [lineIndex, line] of lines.entries()) {
    const separator = line.indexOf("→");
    if (separator < 1) throw new Error(`${filename}:${lineIndex + 1} has no translation arrow.`);
    const translation = line.slice(0, separator).trim();
    const word = line.slice(separator + 1).trim();
    if (!word || !translation) throw new Error(`${filename}:${lineIndex + 1} contains an empty side.`);
    const id = `${kind}-${sha256(`${kind}\0${word}\0${translation}`).slice(0, 16)}`;
    rows.push({ id, kind, word, translation });
  }
}

const unique = [];
const seenIds = new Set();
for (const row of rows) {
  if (seenIds.has(row.id)) continue;
  seenIds.add(row.id);
  unique.push(row);
}

const groupWords = new Map();
const groupCounts = new Map();
const entries = unique.map((row) => {
  const candidates = lessonSlugs;
  const previous = previousAssignments.get(row.id);
  const preservePreviousUnlock = row.kind === "word" || previousDistributionVersion >= 2;
  let index = preservePreviousUnlock && previous && candidates.includes(previous)
    ? candidates.indexOf(previous)
    : candidates.reduce((best, _slug, candidate) =>
        (groupCounts.get(`${row.kind}:${candidates[candidate]}`) ?? 0) < (groupCounts.get(`${row.kind}:${candidates[best]}`) ?? 0) ? candidate : best, 0);
  let attempts = 0;
  while ((groupWords.get(`${row.kind}:${candidates[index]}`) ?? new Set()).has(row.word) && attempts < candidates.length) {
    index = (index + 1) % candidates.length;
    attempts += 1;
  }
  if (attempts === candidates.length) throw new Error(`Cannot assign repeated headword: ${row.word}`);
  const unlockAfterLessonSlug = candidates[index];
  const groupKey = `${row.kind}:${unlockAfterLessonSlug}`;
  if (!groupWords.has(groupKey)) groupWords.set(groupKey, new Set());
  groupWords.get(groupKey).add(row.word);
  groupCounts.set(groupKey, (groupCounts.get(groupKey) ?? 0) + 1);
  const pluralKind = row.kind === "word" ? "words" : "sentences";
  const storageSourceId = previousStorageSources.get(row.id) ?? `expanded-${pluralKind}-${unlockAfterLessonSlug}`;
  return { ...row, unlockAfterLessonSlug, storageSourceId, sectionId: previousSections.get(row.id) ?? "unclassified" };
});

const catalog = {
  source: "Reviewed Russian–Slovak TXT files from the owner vocabulary workspace",
  distributionVersion: 2,
  sourceRowCount: rows.length,
  duplicateRowsOmitted: rows.length - entries.length,
  sourceCounts,
  sourceHashes,
  entries,
};
writeFileSync(outputPath, `${JSON.stringify(catalog, null, 2)}\n`, "utf8");
console.log(`IMPORTED: ${entries.length} unique cards from ${rows.length} reviewed rows`);
