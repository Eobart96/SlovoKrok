import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { fileURLToPath } from "node:url";

const frontendRoot = resolve(fileURLToPath(new URL(".", import.meta.url)), "..");
const catalog = JSON.parse(readFileSync(resolve(frontendRoot, "app/data/additionalVocabularyCatalog.json"), "utf8"));
const courseSections = JSON.parse(readFileSync(resolve(frontendRoot, "app/data/courseVocabularySections.json"), "utf8"));
const allowedSections = new Set([
  "basics-communication", "family-people", "appearance-character", "home-household", "food-drink",
  "shopping-money", "clothing-accessories", "body-health", "feelings-emotions", "education-language",
  "countries-nationalities", "work-professions", "time-calendar", "numbers-quantity", "colors-shapes-materials",
  "nature-weather", "animals-plants", "city-services", "transport-travel", "location-directions",
  "technology-media", "leisure-sport-culture", "actions-movement", "qualities-states", "function-words",
]);
const moduleSlugs = Array.from({ length: 8 }, (_, index) => {
  const source = readFileSync(resolve(frontendRoot, `app/data/modules/module${index + 1}/index.ts`), "utf8");
  return [...source.matchAll(/from "\.\/lessons\/([^"]+)"/g)].map((match) => match[1]);
}).flat();

const fail = (message) => { throw new Error(`Additional vocabulary validation failed: ${message}`); };
if (catalog.sourceRowCount !== 2_050) fail(`expected 2050 source rows, got ${catalog.sourceRowCount}`);
if (catalog.sourceCounts?.words !== 1_278 || catalog.sourceCounts?.sentences !== 772) fail("expected 1278 word rows and 772 sentence rows");
if (catalog.duplicateRowsOmitted !== 18) fail(`expected 18 exact duplicate rows to be omitted, got ${catalog.duplicateRowsOmitted}`);
if (catalog.entries?.length !== 2_032) fail(`expected 2032 unique cards, got ${catalog.entries?.length}`);
if (catalog.distributionVersion !== 2) fail(`expected distribution version 2, got ${catalog.distributionVersion}`);
if (moduleSlugs.length !== 83 || new Set(moduleSlugs).size !== 83) fail(`expected 83 unique unlock points, got ${moduleSlugs.length}`);
if (moduleSlugs.indexOf("present-tense") !== 38) fail("expected the stable Module 5 boundary at lesson index 38");
if (Object.keys(catalog.sourceHashes ?? {}).length !== 4 || Object.values(catalog.sourceHashes).some((hash) => !/^[A-F0-9]{64}$/.test(hash))) fail("expected four SHA-256 source hashes");

const knownSlugs = new Set(moduleSlugs);
const ids = new Set();
const pairs = new Set();
const groupWords = new Set();
const storageKeys = new Set();
const wordUnlocks = new Set();
const sentenceUnlocks = new Set();
const wordUnlockCounts = new Map();
const sentenceUnlockCounts = new Map();
const usedSections = new Set();
let wordCount = 0;
let sentenceCount = 0;
for (const [index, entry] of catalog.entries.entries()) {
  if (!/^(?:word|sentence)-[a-f0-9]{16}$/.test(entry.id) || ids.has(entry.id)) fail(`entry ${index + 1} has an invalid or duplicate stable id`);
  const expectedId = `${entry.kind}-${createHash("sha256").update(`${entry.kind}\0${entry.word}\0${entry.translation}`).digest("hex").slice(0, 16)}`;
  if (entry.id !== expectedId) fail(`entry ${index + 1} stable id does not match its content`);
  if (entry.kind !== "word" && entry.kind !== "sentence") fail(`entry ${index + 1} has an invalid kind`);
  if (!knownSlugs.has(entry.unlockAfterLessonSlug)) fail(`entry ${entry.id} has an unknown unlock lesson`);
  if (!entry.word?.trim() || entry.word.length > 255 || /[А-Яа-яЁё]/.test(entry.word)) fail(`entry ${entry.id} has invalid Slovak text`);
  if (!entry.translation?.trim() || entry.translation.length > 500) fail(`entry ${entry.id} has invalid Russian text`);
  if (!allowedSections.has(entry.sectionId)) fail(`entry ${entry.id} has an unknown semantic section: ${entry.sectionId}`);
  const storageKind = entry.kind === "word" ? "words" : "sentences";
  if (!new RegExp(`^expanded-${storageKind}-[a-z0-9]+(?:-[a-z0-9]+)*$`).test(entry.storageSourceId)) fail(`entry ${entry.id} has an invalid storage source id`);
  const pairKey = `${entry.kind}\0${entry.word}\0${entry.translation}`;
  if (pairs.has(pairKey)) fail(`exact duplicate pair remains: ${entry.word} — ${entry.translation}`);
  const groupWordKey = `${entry.kind}\0${entry.unlockAfterLessonSlug}\0${entry.word}`;
  if (groupWords.has(groupWordKey)) fail(`storage-key collision remains in ${entry.unlockAfterLessonSlug}: ${entry.word}`);
  const storageKey = `${entry.storageSourceId}\0${entry.word}`;
  if (storageKeys.has(storageKey)) fail(`duplicate preserved storage identity: ${entry.word}`);
  ids.add(entry.id);
  pairs.add(pairKey);
  groupWords.add(groupWordKey);
  storageKeys.add(storageKey);
  usedSections.add(entry.sectionId);
  if (entry.kind === "word") {
    wordCount += 1; wordUnlocks.add(entry.unlockAfterLessonSlug);
    wordUnlockCounts.set(entry.unlockAfterLessonSlug, (wordUnlockCounts.get(entry.unlockAfterLessonSlug) ?? 0) + 1);
  } else {
    sentenceCount += 1; sentenceUnlocks.add(entry.unlockAfterLessonSlug);
    sentenceUnlockCounts.set(entry.unlockAfterLessonSlug, (sentenceUnlockCounts.get(entry.unlockAfterLessonSlug) ?? 0) + 1);
  }
}

if (wordCount !== 1_261 || sentenceCount !== 771) fail(`unexpected unique kind counts: ${wordCount} words, ${sentenceCount} sentences`);
if (wordUnlocks.size !== 83) fail(`words do not cover all 83 lessons: ${wordUnlocks.size}`);
if (sentenceUnlocks.size !== 83) fail(`sentences do not cover all 83 lessons: ${sentenceUnlocks.size}`);
const countFrequency = (counts) => [...counts.values()].reduce((frequency, count) => ({ ...frequency, [count]: (frequency[count] ?? 0) + 1 }), {});
const wordFrequency = countFrequency(wordUnlockCounts);
const sentenceFrequency = countFrequency(sentenceUnlockCounts);
if (wordFrequency[15] !== 67 || wordFrequency[16] !== 16 || Object.keys(wordFrequency).length !== 2) fail(`uneven word distribution: ${JSON.stringify(wordFrequency)}`);
if (sentenceFrequency[9] !== 59 || sentenceFrequency[10] !== 24 || Object.keys(sentenceFrequency).length !== 2) fail(`uneven sentence distribution: ${JSON.stringify(sentenceFrequency)}`);
if (usedSections.size !== allowedSections.size) fail(`expected all ${allowedSections.size} semantic sections in the imported catalog, got ${usedSections.size}`);

const semanticAnchors = [
  ["mama", "family-people"], ["otec", "family-people"], ["rodina", "family-people"],
  ["jedlo", "food-drink"], ["paprika", "food-drink"], ["mrkva", "food-drink"],
  ["cesnak", "food-drink"], ["chlieb", "food-drink"], ["autobus", "transport-travel"],
  ["vlak", "transport-travel"], ["lekár", "work-professions"], ["učiteľka", "work-professions"],
  ["Dobrý deň.", "basics-communication"], ["Nerozumiem.", "basics-communication"],
  ["krajina", "countries-nationalities"], ["počítač", "technology-media"], ["pes", "animals-plants"],
];
for (const [word, expectedSection] of semanticAnchors) {
  const matches = catalog.entries.filter((entry) => entry.word.toLocaleLowerCase("sk") === word.toLocaleLowerCase("sk"));
  if (!matches.length || matches.some((entry) => entry.sectionId !== expectedSection)) fail(`semantic anchor is not consistently classified: ${word} -> ${expectedSection}`);
}
if (Object.keys(courseSections).length !== 660) fail(`expected 660 built-in vocabulary section assignments, got ${Object.keys(courseSections).length}`);
for (const [key, sectionId] of Object.entries(courseSections)) {
  if (!key.includes("\0") || !allowedSections.has(sectionId)) fail(`invalid built-in vocabulary assignment: ${key}`);
}

console.log("ADDITIONAL VOCABULARY VALID: 2032 unique cards from 2050 source rows, 83 unlock points");
console.log("SEMANTIC SECTIONS VALID: 2032 cards");
console.log("FAMILY EXAMPLES VALID: mama, otec, rodina");
console.log(`SEMANTIC ANCHORS VALID: ${semanticAnchors.length} common words and phrases`);
console.log("WORD DISTRIBUTION VALID: 67x15 + 16x16 across 83 lessons");
console.log("SENTENCE DISTRIBUTION VALID: 59x9 + 24x10 across 83 lessons");
