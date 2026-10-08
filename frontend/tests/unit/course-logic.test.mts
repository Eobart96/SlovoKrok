import assert from "node:assert/strict";
import test from "node:test";
import { canUpdateCourseAnswer, courseAnswerMaxLength } from "../../app/data/courseAnswerBounds.ts";
import { taskMistakeKind, taskMistakeSource } from "../../app/data/taskMistakes.ts";

test("detached backup reviews keep their kind without a source task to open", () => {
  for (const kind of ["exercise", "homework"] as const) {
    const detached = `detached:${kind}:${"a".repeat(64)}`;
    assert.equal(taskMistakeKind(detached), kind);
    assert.equal(taskMistakeSource(detached), null);
    assert.deepEqual(taskMistakeSource(`${kind}:2`), { kind, id: 2 });
    assert.equal(taskMistakeKind(`${kind}:2`), kind);
  }
  assert.equal(taskMistakeKind("lesson-practice"), null);
  assert.equal(taskMistakeKind("detached:homework:2"), null);
});

test("saved practice answers bound new input and allow repairing oversized legacy answers", () => {
  const full = "a".repeat(courseAnswerMaxLength);
  assert.equal(canUpdateCourseAnswer("", full), true);
  assert.equal(canUpdateCourseAnswer("", full + "a"), false);
  assert.equal(canUpdateCourseAnswer(full, full + "á"), false);
  assert.equal(canUpdateCourseAnswer(full, full.slice(0, -1) + "á"), true);
  const legacy = full + "extra";
  assert.equal(canUpdateCourseAnswer(legacy, legacy.slice(0, -1)), true);
  assert.equal(canUpdateCourseAnswer(legacy, full), true);
  assert.equal(canUpdateCourseAnswer(legacy, legacy + "a"), false);
  assert.equal(canUpdateCourseAnswer(legacy, "b".repeat(legacy.length)), false);
});
import { createLazyCourseLoader } from "../../app/data/lazyCourseLoader.ts";

test("lazy course loader shares imports and caches success", async () => {
  let calls = 0;
  const catalog = { level: "A2" };
  const load = createLazyCourseLoader(async () => { calls += 1; return catalog; });
  const first = load();
  assert.equal(load(), first);
  assert.equal(await first, catalog);
  assert.equal(await load(), catalog);
  assert.equal(calls, 1);
});

test("lazy course loader retries rejected and synchronously failed imports", async () => {
  let calls = 0;
  const load = createLazyCourseLoader(() => { calls += 1; if (calls === 1) throw new Error("chunk unavailable"); return Promise.resolve("A2"); });
  await assert.rejects(load(), /chunk unavailable/);
  assert.equal(await load(), "A2");
  assert.equal(calls, 2);
  let attempts = 0;
  const retry = createLazyCourseLoader(async () => { attempts += 1; if (attempts === 1) throw new Error("download failed"); return "ready"; });
  await assert.rejects(retry(), /download failed/);
  assert.equal(await retry(), "ready");
});

import { scoreLessonUnderstanding } from "../../app/data/courseScoring.ts";
import { recordFinalAttemptMistakes } from "../../app/data/courseProgress.ts";
import { courseModuleCompletionKey, isCourseFinalCompleted, reopenExpandedA2Final, normalizeFinalCompletedModules, resolveCoursePosition, switchCourseLevel } from "../../app/data/courseLevelState.ts";
import { homeworkAssignmentHints, homeworkModeInstructions, homeworkReferenceSections, rankHomeworkReferenceLessons } from "../../app/data/homeworkPlanning.ts";
import { buildCourseGenerationScope, completedCourseModules, completedCourseSections, isCourseGenerationScopeSlug } from "../../app/data/courseGenerationScope.ts";
import { mergeProgress } from "../../app/data/progressMerge.ts";
import { applySlovakAltShortcut } from "../../app/data/slovakKeyboard.ts";
import { editTranslationDraft, swapTranslationDraft } from "../../app/data/translationState.ts";
import { isSentenceVocabularyItem, translationVocabularySeed } from "../../app/data/translationVocabulary.ts";
import { ApiError, apiErrorMessage } from "../../app/lib/apiError.ts";

test("expanding A2 reopens its final without changing legacy A1 or saved answers", () => {
  const selections = { "a2-pilot-final": "answer" };
  assert.equal(isCourseFinalCompleted("A2", true, ["a2-pilot-final"], selections), true);
  assert.equal(isCourseFinalCompleted("A2", true, ["a2-pilot-final", "a2-new-final"], selections), false);
  assert.equal(isCourseFinalCompleted("A2", false, ["a2-pilot-final"], selections), false);
  assert.equal(isCourseFinalCompleted("A2", true, [], selections), false);
  assert.equal(isCourseFinalCompleted("A1", true, ["legacy-question"], {}), true);
  assert.deepEqual(selections, { "a2-pilot-final": "answer" });
  const flags = { "a1:2": true, "a2:2": true, "a2:3": true };
  const expandedIds = ["a2-pilot-final", "a2-new-final"];
  const reopened = reopenExpandedA2Final("A2", "a2:2", flags, expandedIds, selections);
  assert.deepEqual(reopened, { "a1:2": true, "a2:2": false, "a2:3": true });
  assert.equal(isCourseFinalCompleted("A2", reopened["a2:2"], expandedIds, { ...selections, "a2-new-final": "new" }), false);
  assert.equal(reopenExpandedA2Final("A1", "a1:2", flags, expandedIds, {}), flags);
  assert.equal(reopenExpandedA2Final("A2", "a2:2", flags, ["a2-pilot-final"], selections), flags);
  assert.equal(flags["a2:2"], true);
});

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

test("switching levels preserves A1 location, answers and qualified finals", () => {
  const a1 = [{ order: 1, lessons: [{ slug: "greetings" }] }, { order: 2, lessons: [{ slug: "a1-topic" }] }];
  const a2 = [{ order: 2, lessons: [{ slug: "a2-pilot" }] }];
  const original = { activeLevel: "A1" as "A1" | "A2", activeModule: 2, selectedSlug: "a1-topic", levelPositions: {}, progress: { "a1-topic": "completed" }, answers: { "a1-test": "áno" }, finalCompletedModules: { "a1:2": true } };
  const switched = switchCourseLevel(original, "A2", a2);
  assert.equal(switched.selectedSlug, "a2-pilot");
  assert.equal(switched.activeModule, 2);
  assert.strictEqual(switched.progress, original.progress);
  assert.strictEqual(switched.answers, original.answers);
  assert.strictEqual(switched.finalCompletedModules, original.finalCompletedModules);
  assert.deepEqual(switchCourseLevel(switched, "A1", a1), { ...original, levelPositions: { A1: { activeModule: 2, selectedSlug: "a1-topic" }, A2: { activeModule: 2, selectedSlug: "a2-pilot" } } });
  assert.deepEqual(resolveCoursePosition(a2, { activeModule: 1, selectedSlug: "greetings" }), { activeModule: 2, selectedSlug: "a2-pilot" });
  assert.deepEqual(resolveCoursePosition(a1, { selectedSlug: "a1-topic" }), { activeModule: 2, selectedSlug: "a1-topic" });
});

test("A2 global task scopes stay separate from legacy A1 tasks", () => {
  const modules = [{ slug: "a2-module-2", order: 2, title: "Pilot", level: "A2", description: "", lessons: [], topicGroups: [] }];
  assert.equal(buildCourseGenerationScope({ mode: "progress", modules, completedLessonSlugs: [] }).storageSlug, "course:a2:progress");
  assert.equal(buildCourseGenerationScope({ mode: "mistakes", modules, completedLessonSlugs: [] }).storageSlug, "course:a2:mistakes");
  assert.equal(isCourseGenerationScopeSlug(modules, "course-progress"), false);
  assert.equal(isCourseGenerationScopeSlug(modules, "course:a2:progress"), true);
  assert.equal(isCourseGenerationScopeSlug(modules, "module:module-2"), false);
  assert.equal(isCourseGenerationScopeSlug(modules, "module:a2-module-2"), true);
});

test("prepending A2 Module1 preserves Module2 positions and starts new learners at Module1", () => {
  const modules = [{ order: 1, lessons: [{ slug: "a2-readiness-for-a2" }] }, { order: 2, lessons: [{ slug: "a2-nominative-plural-things" }, { slug: "a2-case-triads" }] }];
  assert.deepEqual(resolveCoursePosition(modules), { activeModule: 1, selectedSlug: "a2-readiness-for-a2" });
  assert.deepEqual(resolveCoursePosition(modules, { activeModule: 2 }), { activeModule: 2, selectedSlug: "a2-nominative-plural-things" });
  assert.deepEqual(resolveCoursePosition(modules, { activeModule: 1, selectedSlug: "a2-case-triads" }), { activeModule: 2, selectedSlug: "a2-case-triads" });
  const original = { activeLevel: "A1" as "A1" | "A2", activeModule: 3, selectedSlug: "a1-topic", levelPositions: { A2: { activeModule: 2, selectedSlug: "a2-case-triads" } }, progress: { "a2-case-triads": "completed" }, answers: { "a2-m2-case-triads-step-1": "answer" }, finalCompletedModules: { "a1:1": true, "a2:2": true } };
  const switched = switchCourseLevel(original, "A2", modules);
  assert.equal(switched.activeModule, 2);
  assert.equal(switched.selectedSlug, "a2-case-triads");
  assert.strictEqual(switched.progress, original.progress);
  assert.strictEqual(switched.answers, original.answers);
  assert.strictEqual(switched.finalCompletedModules, original.finalCompletedModules);
});

test("A2 Module1 final stays separate from legacy A1 and completed Module2", () => {
  const flags = normalizeFinalCompletedModules({ "1": true, "a2:2": true });
  const selections = { "a2-m2-final": "answer" };
  assert.equal(courseModuleCompletionKey("A2", 1), "a2:1");
  assert.deepEqual(flags, { "a1:1": true, "a2:2": true });
  assert.equal(isCourseFinalCompleted("A2", Boolean(flags["a2:1"]), ["a2-m1-final"], selections), false);
  assert.equal(isCourseFinalCompleted("A2", flags["a2:2"], ["a2-m2-final"], selections), true);
  assert.equal(reopenExpandedA2Final("A2", "a2:1", flags, ["a2-m1-final"], selections), flags);
});

test("adding A2 Module3 preserves previous modules and restores its own position", () => {
  const modules = [{ order: 1, lessons: [{ slug: "a2-readiness-for-a2" }] }, { order: 2, lessons: [{ slug: "a2-case-triads" }] }, { order: 3, lessons: [{ slug: "a2-adjective-case-agreement" }, { slug: "a2-numerals-dates-quantity" }] }];
  for (const [activeModule, selectedSlug] of [[1, "a2-readiness-for-a2"], [2, "a2-case-triads"], [3, "a2-numerals-dates-quantity"]] as const) {
    assert.deepEqual(resolveCoursePosition(modules, { activeModule, selectedSlug }), { activeModule, selectedSlug });
  }
  const original = { activeLevel: "A1" as "A1" | "A2", activeModule: 8, selectedSlug: "a1-topic", levelPositions: { A2: { activeModule: 3, selectedSlug: "a2-numerals-dates-quantity" } }, progress: { "a2-case-triads": "completed" }, practiceAnswers: { "a2-m2-case-triads-step-1": "answer" }, finalCompletedModules: { "a1:1": true, "a2:1": true, "a2:2": true } };
  const restored = switchCourseLevel(original, "A2", modules);
  assert.equal(restored.activeModule, 3);
  assert.equal(restored.selectedSlug, "a2-numerals-dates-quantity");
  assert.strictEqual(restored.progress, original.progress);
  assert.strictEqual(restored.practiceAnswers, original.practiceAnswers);
  assert.strictEqual(restored.finalCompletedModules, original.finalCompletedModules);
});

test("A2 Module3 completion cannot be supplied by A1 or earlier A2 finals", () => {
  const flags = normalizeFinalCompletedModules({ "3": true, "a2:1": true, "a2:2": true });
  const answers = { "a2-m1-final": "answer", "a2-m2-final": "answer" };
  assert.equal(courseModuleCompletionKey("A2", 3), "a2:3");
  assert.deepEqual(flags, { "a1:3": true, "a2:1": true, "a2:2": true });
  assert.equal(isCourseFinalCompleted("A2", Boolean(flags["a2:3"]), ["a2-m3-final"], answers), false);
  assert.equal(isCourseFinalCompleted("A2", true, ["a2-m3-final"], answers), false);
  const completed = { ...flags, "a2:3": true };
  const allAnswers = { ...answers, "a2-m3-final": "answer" };
  assert.equal(isCourseFinalCompleted("A2", completed["a2:3"], ["a2-m3-final"], allAnswers), true);
  assert.strictEqual(reopenExpandedA2Final("A2", "a2:3", completed, ["a2-m3-final"], allAnswers), completed);
});

test("A2 Module4 restores without changing earlier answers or completion", () => {
  const modules = [1, 2, 3, 4].map((order) => ({ order, lessons: [{ slug: `a2-topic-${order}` }] }));
  for (const order of [1, 2, 3, 4]) assert.deepEqual(resolveCoursePosition(modules, { activeModule: order, selectedSlug: `a2-topic-${order}` }), { activeModule: order, selectedSlug: `a2-topic-${order}` });
  const original = { activeLevel: "A1" as "A1" | "A2", activeModule: 4, selectedSlug: "a1-topic", levelPositions: { A2: { activeModule: 4, selectedSlug: "a2-topic-4" } }, answers: { previous: "answer" }, progress: { previous: "completed" }, finalCompletedModules: { "a1:4": true, "a2:1": true, "a2:2": true, "a2:3": true } };
  const switched = switchCourseLevel(original, "A2", modules);
  assert.equal(switched.activeModule, 4);
  assert.equal(switched.selectedSlug, "a2-topic-4");
  assert.strictEqual(switched.answers, original.answers);
  assert.strictEqual(switched.progress, original.progress);
  assert.strictEqual(switched.finalCompletedModules, original.finalCompletedModules);
});

test("expanding A2 Module4 final reopens only its own flag and retains answers", () => {
  const flags = normalizeFinalCompletedModules({ "4": true, "a2:1": true, "a2:2": true, "a2:3": true, "a2:4": true });
  const answers = { "a2-m4-old": "answer" };
  assert.equal(courseModuleCompletionKey("A2", 4), "a2:4");
  const reopened = reopenExpandedA2Final("A2", "a2:4", flags, ["a2-m4-old", "a2-m4-new"], answers);
  assert.deepEqual(reopened, { ...flags, "a2:4": false });
  assert.equal(flags["a1:4"], true);
  assert.equal(flags["a2:4"], true);
  assert.deepEqual(answers, { "a2-m4-old": "answer" });
  assert.equal(isCourseFinalCompleted("A2", reopened["a2:4"], ["a2-m4-old", "a2-m4-new"], { ...answers, "a2-m4-new": "answer" }), false);
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
