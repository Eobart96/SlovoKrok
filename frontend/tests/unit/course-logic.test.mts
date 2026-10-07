import assert from "node:assert/strict";
import test from "node:test";

import { scoreLessonUnderstanding } from "../../app/data/courseScoring.ts";
import { recordFinalAttemptMistakes } from "../../app/data/courseProgress.ts";
import { courseModuleCompletionKey, normalizeFinalCompletedModules } from "../../app/data/courseLevelState.ts";
import { homeworkAssignmentHints, homeworkModeInstructions, homeworkReferenceSections, rankHomeworkReferenceLessons } from "../../app/data/homeworkPlanning.ts";
import { buildCourseGenerationScope, completedCourseModules, completedCourseSections } from "../../app/data/courseGenerationScope.ts";
import { mergeProgress } from "../../app/data/progressMerge.ts";
import { applySlovakAltShortcut } from "../../app/data/slovakKeyboard.ts";
import { editTranslationDraft, swapTranslationDraft } from "../../app/data/translationState.ts";
import { isSentenceVocabularyItem, translationVocabularySeed } from "../../app/data/translationVocabulary.ts";
import { ApiError, apiErrorMessage } from "../../app/lib/apiError.ts";

test("progress merge keeps defaults and lets cached session win over legacy storage", () => {
  assert.deepEqual(
    mergeProgress(
      { first: "not_started", second: "not_started" },
      { first: "in_progress" },
      { first: "completed" },
    ),
    { first: "completed", second: "not_started" },
  );
});

test("lesson scoring applies the capped active-mistake penalty", () => {
  assert.equal(scoreLessonUnderstanding([true, true, false, false], 2), 44);
  assert.equal(scoreLessonUnderstanding([true], 99), 85);
  assert.equal(scoreLessonUnderstanding([], 4), 0);
  assert.equal(scoreLessonUnderstanding([true], -2), 100);
});

test("editing and swapping a translation reset stale follow-up state", () => {
  const result = { translation: "dobrý deň" };
  const edited = editTranslationDraft({ direction: "ru-sk" as const, text: "привет", result }, "добрый день");
  assert.deepEqual(edited, {
    direction: "ru-sk", text: "добрый день", result: null, error: "", questionOpen: false, question: "", questionAnswer: "", questionError: "",
  });
  assert.deepEqual(swapTranslationDraft({ direction: "ru-sk" as const, text: "привет", result }), {
    direction: "sk-ru", text: "dobrý deň", result: null, error: "", questionOpen: false, question: "", questionAnswer: "", questionError: "",
  });
});

test("course level state keeps legacy A1 module results separate from A2", () => {
  assert.equal(courseModuleCompletionKey("A1", 2), "a1:2");
  assert.equal(courseModuleCompletionKey("A2", 2), "a2:2");
  assert.throws(() => courseModuleCompletionKey("A2", 9), RangeError);
  assert.deepEqual(
    normalizeFinalCompletedModules({ "2": true, "a2:2": false, invalid: true }, true),
    { "a1:1": true, "a1:2": true, "a2:2": false },
  );
  assert.deepEqual(normalizeFinalCompletedModules({ "1": false }, true), { "a1:1": false });
});

test("Alt shortcuts use the physical key and cycle Slovak variants", () => {
  const firstO = applySlovakAltShortcut("stl", "KeyO", false, 2, 2);
  assert.deepEqual(firstO, { value: "stól", caret: 3 });
  assert.deepEqual(applySlovakAltShortcut(firstO!.value, "KeyO", false, firstO!.caret, firstO!.caret), { value: "stôl", caret: 3 });
  assert.deepEqual(applySlovakAltShortcut("A", "KeyA", true, 1, 1), { value: "Á", caret: 1 });
  assert.equal(applySlovakAltShortcut("text", "KeyB", false), null);
});

test("translator vocabulary stores Slovak words and sentences in separate personal sources", () => {
  const word = translationVocabularySeed("молоко", "mlieko", "ru-sk");
  const sentence = translationVocabularySeed("Dnes pijem mlieko.", "Сегодня я пью молоко.", "sk-ru");
  assert.deepEqual(word, {
    lesson_slug: "translator:words", lesson_title: "Из переводчика · слова", word: "mlieko", translation: "молоко", example: "mlieko",
  });
  assert.equal(sentence?.lesson_slug, "translator:sentences");
  assert.equal(sentence ? isSentenceVocabularyItem(sentence) : false, true);
  assert.equal(translationVocabularySeed("x".repeat(256), "перевод", "sk-ru"), null);
});

test("submitting a final attempt records every wrong answer without requiring a second click", () => {
  const questions = [
    { id: "q1", lessonSlug: "lesson-1", question: "Первый вопрос", answer: "áno" },
    { id: "q2", lessonSlug: "lesson-2", question: "Второй вопрос", answer: "nie" },
  ];
  const recorded = recordFinalAttemptMistakes({}, questions, { q1: "нет", q2: "nie" }, Date.UTC(2026, 8, 25));
  assert.deepEqual(Object.keys(recorded), ["q1"]);
  assert.equal(recorded.q1.attempts, 1);
  assert.equal(recorded.q1.answer, "áno");
  assert.equal(recorded.q1.mastered, false);
});

test("mistake-focused homework is bounded to known errors and uses a three-step task", () => {
  const instructions = homeworkModeInstructions("mistakes").join("\n");
  assert.match(instructions, /только активные ошибки/u);
  assert.match(instructions, /трёх связанных частей/u);
  assert.deepEqual(homeworkModeInstructions("topic"), []);
});

test("homework help ranks every relevant theme above a coincidental phrase match", () => {
  const assignment = {
    title: "Первая встреча",
    description: "Напишите формальный диалог: поздоровайтесь, представьтесь, попросите повторить непонятное и попрощайтесь.",
    focusCategory: "формальный диалог и уточнение при непонимании",
  };
  const lessons = [
    { title: "Ресторан и кафе", theory: { summary: "Короткие реплики во время еды.", rules: ["Во время еды достаточно коротких реплик."], examples: [{ slovak: "Všetko je v poriadku.", russian: "Всё в порядке.", explanation: "Ответ в ресторане." }] } },
    { title: "Представление себя", theory: { summary: "Представьтесь и познакомьтесь.", rules: ["Не смешивайте формальные voláte, ste и неформальные voláš, si."], examples: [{ slovak: "Dobrý deň. Volám sa Ari. Teší ma.", russian: "Добрый день. Меня зовут Ари. Очень приятно.", explanation: "Формальное знакомство." }] } },
    { title: "Коммуникативное уточнение", theory: { summary: "Сообщите, что не поняли, и попросите повторить.", rules: ["Формально попросите: Môžete to zopakovať?"], examples: [{ slovak: "Prepáčte, nerozumiem. Ešte raz, prosím.", russian: "Извините, не понимаю. Ещё раз, пожалуйста.", explanation: "Уточнение при непонимании." }] } },
  ];
  const ranked = rankHomeworkReferenceLessons(assignment, lessons);
  const hints = homeworkAssignmentHints({ ...assignment, lessons });
  assert.equal(hints.length, 2);
  assert.deepEqual(new Set(ranked.slice(0, 2).map((lesson) => lesson.title)), new Set(["Представление себя", "Коммуникативное уточнение"]));
  assert.equal(ranked[2].title, "Ресторан и кафе");
  assert.match(hints.join(" "), /Volám sa Ari/u);
  assert.match(hints.join(" "), /nerozumiem/u);
  assert.doesNotMatch(hints.join(" "), /Všetko je v poriadku/u);
  assert.doesNotMatch(hints.join(" "), /правильный ответ/iu);
});

test("homework topic reference omits the final self-check section", () => {
  const sections = [
    { title: "Опорные фразы" },
    { title: "Финальные опоры и самопроверка" },
  ];
  assert.deepEqual(homeworkReferenceSections(sections), [{ title: "Опорные фразы" }]);
});

test("API errors preserve server detail and map invalid bodies to a stable fallback", () => {
  assert.equal(apiErrorMessage({ detail: "Недоступно" }, 503), "Недоступно");
  assert.equal(apiErrorMessage(null, 502), "Ошибка сервера (502)");
  const error = new ApiError("Недоступно", 503, { detail: "Недоступно" });
  assert.equal(error.name, "ApiError");
  assert.equal(error.status, 503);
  assert.deepEqual(error.body, { detail: "Недоступно" });
});

test("generation scopes keep sections and modules inside completed material", () => {
  const makeLesson = (slug: string, title: string) => ({ slug, title, sections: [{ title: "Первый раздел" }, { title: "Второй раздел" }] });
  const firstModule = { slug: "module-1", order: 1, title: "Основы", lessons: [makeLesson("lesson-1", "Первая тема"), makeLesson("lesson-2", "Вторая тема"), makeLesson("lesson-3", "Будущая тема")], topicGroups: [{ id: "alphabet", title: "Алфавит", slovakTitle: "Abeceda", description: "Буквы", lessonSlugs: ["lesson-1", "lesson-2", "lesson-3"] }] };
  const secondModule = { slug: "module-2", order: 2, title: "Дальше", lessons: [makeLesson("lesson-4", "Четвёртая тема")] };
  const modules = [firstModule, secondModule] as never;
  const completedSlugs = firstModule.lessons.slice(0, 2).map((lesson) => lesson.slug);
  const sectionScope = buildCourseGenerationScope({
    mode: "section",
    modules,
    completedLessonSlugs: completedSlugs,
    sectionKey: "module-1:alphabet",
  });
  assert.equal(sectionScope.storageSlug, "section:module-1:alphabet");
  assert.deepEqual(sectionScope.lessons.map((lesson) => lesson.slug), completedSlugs);
  assert.equal(sectionScope.section?.title, "Алфавит");
  assert.equal(completedCourseSections(modules, completedSlugs)[0].key, "module-1:alphabet");
  assert.equal(sectionScope.lessons.some((lesson) => lesson.slug === "lesson-3"), false);
  assert.ok(sectionScope.storageSlug.length <= 100);

  const moduleScope = buildCourseGenerationScope({
    mode: "module",
    modules,
    completedLessonSlugs: completedSlugs,
    moduleSlug: firstModule.slug,
  });
  assert.equal(moduleScope.storageSlug, `module:${firstModule.slug}`);
  assert.deepEqual(moduleScope.lessons.map((lesson) => lesson.slug), completedSlugs);
  assert.equal(completedCourseModules(modules, completedSlugs).length, 1);
  assert.equal(moduleScope.lessons.some((lesson) => lesson.slug === "lesson-3"), false);
});
