import { type CourseLesson } from "./courseTypes";

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
