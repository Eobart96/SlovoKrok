import { type CourseLesson } from "./courseTypes";
import courseVocabularySections from "./courseVocabularySections.json";
import {
  additionalVocabularyGroups,
  additionalVocabularySourceSlug,
  type AdditionalVocabularyGroup,
} from "./additionalVocabulary";
import { vocabularySectionTitle, type VocabularySectionId } from "./vocabularySections";

const builtInSectionByKey = courseVocabularySections as Record<string, VocabularySectionId>;

function builtInSection(lessonSlug: string, word: string): VocabularySectionId {
  return builtInSectionByKey[`${lessonSlug}\0${word}`] ?? "basics-communication";
}

export type VocabularySeed = {
  lesson_slug: string;
  lesson_title: string;
  word: string;
  translation: string;
  example: string | null;
};

export type VocabularySource = {
  id: string;
  title: string;
  items: VocabularySeed[];
};

export function lessonVocabulary(lesson: CourseLesson) {
  if (lesson.vocabulary !== undefined) return lesson.vocabulary;
  const words = lesson.theory.examples.map((example) => ({ word: example.slovak, translation: example.russian, example: example.slovak }));
  for (const section of lesson.sections) {
    if (!section.table) continue;
    const slovak = section.table.headers.findIndex((header) => header.toLocaleLowerCase("ru").includes("словац"));
    const russian = section.table.headers.findIndex((header) => header.toLocaleLowerCase("ru").includes("рус"));
    if (slovak < 0 || russian < 0) continue;
    for (const row of section.table.rows) {
      if (row[slovak] && row[russian]) words.push({ word: row[slovak], translation: row[russian], example: row[slovak] });
    }
  }
  return [...new Map(words.map((word) => [word.word, word])).values()];
}

export function learnedVocabularySources(
  lessons: CourseLesson[],
  completedLessonSlugs: string[],
  additionalGroups: AdditionalVocabularyGroup[] = additionalVocabularyGroups,
): VocabularySource[] {
  const completed = new Set(completedLessonSlugs);
  const groupsByUnlockLesson = new Map<string, AdditionalVocabularyGroup[]>();
  for (const group of additionalGroups) {
    const current = groupsByUnlockLesson.get(group.unlockAfterLessonSlug) ?? [];
    current.push(group);
    groupsByUnlockLesson.set(group.unlockAfterLessonSlug, current);
  }

  const sources: VocabularySource[] = [];
  for (const lesson of lessons) {
    if (!completed.has(lesson.slug)) continue;
    sources.push({
      id: lesson.slug,
      title: lesson.title,
      items: lessonVocabulary(lesson).map((item) => ({
        lesson_slug: lesson.slug,
        lesson_title: vocabularySectionTitle(builtInSection(lesson.slug, item.word)),
        word: item.word,
        translation: item.translation,
        example: item.example ?? null,
      })),
    });
    for (const group of groupsByUnlockLesson.get(lesson.slug) ?? []) {
      sources.push({
        id: additionalVocabularySourceSlug(group.id),
        title: lesson.title,
        items: group.items.map((item) => ({
          lesson_slug: additionalVocabularySourceSlug(item.storageSourceId),
          lesson_title: vocabularySectionTitle(item.sectionId),
          word: item.word,
          translation: item.translation,
          example: item.example ?? null,
        })),
      });
    }
  }
  return sources;
}

export function learnedVocabularySeeds(
  lessons: CourseLesson[],
  completedLessonSlugs: string[],
  additionalGroups: AdditionalVocabularyGroup[] = additionalVocabularyGroups,
): VocabularySeed[] {
  const items = learnedVocabularySources(lessons, completedLessonSlugs, additionalGroups).flatMap((source) => source.items);
  return [...new Map(items.map((item) => [`${item.lesson_slug}:${item.word}`, item])).values()];
}

function oneLine(value: string): string {
  return value.replace(/[\t\r\n]+/g, " ").trim();
}

export function ankiVocabularyText(items: Array<Pick<VocabularySeed, "word" | "translation">>): string {
  return items.map((item) => `${oneLine(item.word)}\t${oneLine(item.translation)}`).join("\r\n");
}

export type VocabularyExportFormat = "anki" | "text" | "csv" | "json";
export type VocabularyExportDirection = "slovak-russian" | "russian-slovak";

type VocabularyExportItem = Pick<VocabularySeed, "word" | "translation" | "lesson_title">;

function csvCell(value: string): string {
  return `"${oneLine(value).replaceAll('"', '""')}"`;
}

export function vocabularyExportContent(
  items: VocabularyExportItem[],
  format: VocabularyExportFormat,
  direction: VocabularyExportDirection,
): { content: string; extension: "txt" | "csv" | "json"; mimeType: string } {
  const russianFirst = direction === "russian-slovak";
  if (format === "anki") {
    const content = items.map((item) => russianFirst
      ? `${oneLine(item.translation)}\t${oneLine(item.word)}`
      : `${oneLine(item.word)}\t${oneLine(item.translation)}`).join("\r\n");
    return { content, extension: "txt", mimeType: "text/plain;charset=utf-8" };
  }
  if (format === "text") {
    const content = items.map((item) => russianFirst
      ? `${oneLine(item.translation)} → ${oneLine(item.word)}`
      : `${oneLine(item.word)} → ${oneLine(item.translation)}`).join("\r\n");
    return { content, extension: "txt", mimeType: "text/plain;charset=utf-8" };
  }
  if (format === "csv") {
    const headers = russianFirst ? ["Русский", "Словацкий", "Раздел"] : ["Словацкий", "Русский", "Раздел"];
    const rows = items.map((item) => {
      const pair = russianFirst ? [item.translation, item.word] : [item.word, item.translation];
      return [...pair, item.lesson_title].map(csvCell).join(";");
    });
    return { content: [headers.map(csvCell).join(";"), ...rows].join("\r\n"), extension: "csv", mimeType: "text/csv;charset=utf-8" };
  }
  const content = JSON.stringify(items.map((item) => russianFirst
    ? { russian: oneLine(item.translation), slovak: oneLine(item.word), section: item.lesson_title }
    : { slovak: oneLine(item.word), russian: oneLine(item.translation), section: item.lesson_title }), null, 2);
  return { content, extension: "json", mimeType: "application/json;charset=utf-8" };
}

export function learnedVocabularyContext(
  lessons: CourseLesson[],
  completedLessonSlugs: string[],
  additionalGroups: AdditionalVocabularyGroup[] = additionalVocabularyGroups,
  maxLength = 29_500,
): string {
  const sources = learnedVocabularySources(lessons, completedLessonSlugs, additionalGroups);
  const prioritized = [
    ...sources.filter((source) => source.id.startsWith("additional-vocabulary:")).reverse(),
    ...sources.filter((source) => !source.id.startsWith("additional-vocabulary:")).reverse(),
  ];
  const lines = prioritized.flatMap((source) => source.items.map((item) => `${oneLine(item.word)} = ${oneLine(item.translation)}`));
  if (!lines.length) return "";
  const heading = "Изученные слова и фразы (их можно использовать в тексте):";
  const included: string[] = [];
  let length = heading.length;
  for (const line of lines) {
    if (length + line.length + 1 > maxLength) break;
    included.push(line);
    length += line.length + 1;
  }
  return `${heading}\n${included.join("\n")}`;
}
