import catalog from "./additionalVocabularyCatalog.json";
import { plannedA1Modules } from "./a1CourseRoadmap";
import { type VocabularySectionId } from "./vocabularySections";

export type AdditionalVocabularyEntry = {
  /** A single Slovak word or a complete Slovak sentence. */
  word: string;
  translation: string;
  example?: string | null;
  sectionId: VocabularySectionId;
  storageSourceId: string;
};

export type AdditionalVocabularyGroup = {
  id: string;
  title: string;
  unlockAfterLessonSlug: string;
  items: AdditionalVocabularyEntry[];
};

type CatalogEntry = {
  id: string;
  kind: "word" | "sentence";
  unlockAfterLessonSlug: string;
  word: string;
  translation: string;
  sectionId: VocabularySectionId;
  storageSourceId: string;
};
type AdditionalVocabularyCatalog = {
  entries: CatalogEntry[];
};

const module1LessonSlugs = [
  "slovak-alphabet-pronunciation",
  "long-short-vowels",
  "diphthongs",
  "soft-hard-consonants",
  "word-stress",
  "rhythmic-law",
  "greetings",
  "introductions",
  "numbers",
  "days-and-months",
  "personal-pronouns",
  "verb-byt",
  "question-words",
  "communication-repair",
];

export const additionalVocabularyUnlockSlugs = [
  ...module1LessonSlugs,
  ...plannedA1Modules.flatMap((module) => module.lessons.map((lesson) => lesson.slug)),
];

const importedCatalog = catalog as unknown as AdditionalVocabularyCatalog;

function catalogGroups(entries: CatalogEntry[]): AdditionalVocabularyGroup[] {
  const groups = new Map<string, AdditionalVocabularyGroup>();
  for (const entry of entries) {
    const key = `${entry.kind}:${entry.unlockAfterLessonSlug}`;
    const group = groups.get(key) ?? {
      id: `expanded-${entry.kind === "word" ? "words" : "sentences"}-${entry.unlockAfterLessonSlug}`,
      title: entry.kind === "word" ? "Дополнительные слова" : "Дополнительные фразы",
      unlockAfterLessonSlug: entry.unlockAfterLessonSlug,
      items: [],
    };
    group.items.push({ word: entry.word, translation: entry.translation, example: null, sectionId: entry.sectionId, storageSourceId: entry.storageSourceId });
    groups.set(key, group);
  }
  return [...groups.values()];
}

/**
 * The reviewed external catalog stays separate from lesson content. Words
 * and complete sentences both unlock as evenly as possible throughout all 83
 * lessons. Storage source ids remain independent from unlock redistribution.
 */
export const additionalVocabularyGroups: AdditionalVocabularyGroup[] = [
  ...catalogGroups(importedCatalog.entries),
];

export function additionalVocabularySourceSlug(groupId: string): string {
  return `additional-vocabulary:${groupId}`;
}

export function validateAdditionalVocabulary(groups: AdditionalVocabularyGroup[], knownLessonSlugs: ReadonlySet<string>): void {
  const ids = new Set<string>();
  const storageKeys = new Set<string>();
  for (const group of groups) {
    if (group.id.length > 70 || !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(group.id)) throw new Error(`Invalid additional vocabulary group id: ${group.id}`);
    if (ids.has(group.id)) throw new Error(`Duplicate additional vocabulary group id: ${group.id}`);
    if (!group.title.trim() || group.title.length > 255) throw new Error(`Additional vocabulary group ${group.id} has an invalid title`);
    if (!knownLessonSlugs.has(group.unlockAfterLessonSlug)) throw new Error(`Unknown unlock lesson for additional vocabulary group ${group.id}: ${group.unlockAfterLessonSlug}`);
    if (!group.items.length) throw new Error(`Additional vocabulary group ${group.id} has no cards`);
    const storageKind = group.id.startsWith("expanded-words-")
      ? "words"
      : group.id.startsWith("expanded-sentences-")
        ? "sentences"
        : null;
    if (!storageKind) throw new Error(`Additional vocabulary group ${group.id} has an invalid kind`);
    ids.add(group.id);
    const words = new Set<string>();
    for (const item of group.items) {
      if (!item.word.trim() || item.word.length > 255 || !item.translation.trim() || item.translation.length > 500 || (item.example?.length ?? 0) > 2_000) throw new Error(`Additional vocabulary group ${group.id} contains an invalid card`);
      if (!new RegExp(`^expanded-${storageKind}-[a-z0-9]+(?:-[a-z0-9]+)*$`).test(item.storageSourceId)) throw new Error(`Additional vocabulary group ${group.id} contains an invalid storage source`);
      if (words.has(item.word)) throw new Error(`Duplicate additional vocabulary card in ${group.id}: ${item.word}`);
      const storageKey = `${item.storageSourceId}\0${item.word}`;
      if (storageKeys.has(storageKey)) throw new Error(`Duplicate additional vocabulary storage key: ${item.word}`);
      words.add(item.word);
      storageKeys.add(storageKey);
    }
  }
}
