import { expect, test, type Page } from "@playwright/test";

import { a1CourseModules, allA1Lessons, getA1Module } from "../../app/data/a1Course";
import { a1CefrCoverage } from "../../app/data/a1CefrCoverage";
import { getPlannedModule } from "../../app/data/a1CourseRoadmap";
import { buildInitialProgress, filterKnownLessonSlugs, orderedModuleLessons, topicGroupLessons } from "../../app/data/courseEngine";
import type { CourseLesson } from "../../app/data/courseTypes";
import { validateCourseModules } from "../../app/data/courseValidation";
import type { CourseState } from "../../app/lib/api";
import { defineLessonsFromPlannedContent, definePlannedModule } from "../../app/data/modules/moduleFactory";
import { buildModuleFinalQuestions, buildReinforcementPractices } from "../../app/data/coursePractice";
import { buildCourseResetScope, buildLessonSummary, nextMistakeRecord, removeActivityScope, removeLessonScope, removeMistakeScope, resetProgressScope } from "../../app/data/courseProgress";
import { contentVocabulary } from "../../app/components/CourseVocabulary";

const module1 = getA1Module(1);
const module2 = getA1Module(2);
const module3 = getA1Module(3);
const module4 = getA1Module(4);
const module5 = getA1Module(5);
const module6 = getA1Module(6);
const module7 = getA1Module(7);
const module8 = getA1Module(8);

async function openModule7Lesson(page: Page, lesson: CourseLesson) {
  const group = module7.topicGroups?.find((candidate) => candidate.lessonSlugs.includes(lesson.slug));
  if (!group) throw new Error(`Module 7 group is missing for ${lesson.slug}`);
  await page.getByRole("button").filter({ hasText: group.title }).first().click();
  await page.getByRole("button").filter({ hasText: lesson.title }).first().click();
}

async function openModule8Lesson(page: Page, lesson: CourseLesson) {
  const group = module8.topicGroups?.find((candidate) => candidate.lessonSlugs.includes(lesson.slug));
  if (!group) throw new Error(`Module 8 group is missing for ${lesson.slug}`);
  await page.getByRole("button").filter({ hasText: group.title }).first().click();
  await page.getByRole("button").filter({ hasText: lesson.title }).first().click();
}

test("course structure has stable unique identifiers and data-driven ordering", () => {
  const lessonSlugs = allA1Lessons.map((lesson) => lesson.slug);
  const activityIds = allA1Lessons.flatMap((lesson) => [
    ...lesson.stepPractices.map((practice) => practice.id),
    ...(lesson.reinforcementPractices ?? []).map((practice) => practice.id),
    ...lesson.knowledgeChecks.map((check) => check.id),
    ...lesson.finalChecks.map((check) => check.id),
  ]);

  expect(new Set(a1CourseModules.map((module) => module.slug)).size).toBe(a1CourseModules.length);
  expect(new Set(lessonSlugs).size).toBe(lessonSlugs.length);
  expect(new Set(activityIds).size).toBe(activityIds.length);
  expect(orderedModuleLessons(module1).map((lesson) => lesson.slug)).toEqual(
    module1.topicGroups?.flatMap((group) => group.lessonSlugs),
  );
  for (const group of module1.topicGroups ?? []) {
    expect(topicGroupLessons(module1, group.id).map((lesson) => lesson.slug)).toEqual(group.lessonSlugs);
  }
  expect(module7.topicGroups?.map((group) => group.lessonSlugs)).toEqual([
    ["past-regular", "past-frequent"],
    ["future-budem", "future-questions-negation"],
    ["yesterday", "yesterday-today-tomorrow"],
    ["invitation-arrangement"],
  ]);
  expect(module8.topicGroups?.map((group) => group.lessonSlugs)).toEqual([
    ["social-etiquette", "supported-dialogue", "repair-strategies"],
    ["understand-message", "voice-description", "written-profile"],
    ["everyday-task", "simple-mediation"],
    ["a1-scenarios"],
  ]);
});

test("module registry rejects incomplete or unplanned content", () => {
  const planned = getPlannedModule(2);
  if (!planned) throw new Error("Module 2 roadmap is missing");
  expect(() => definePlannedModule({ planned, lessons: module2.lessons.slice(1) })).toThrow(/Missing Module 2 lesson file/);
  expect(() => definePlannedModule({ planned, lessons: [module2.lessons[0], module2.lessons[0]] })).toThrow(/Duplicate registered lesson/);
  expect(() => defineLessonsFromPlannedContent(planned, [{ slug: "unplanned-topic" }], () => module2.lessons[0])).toThrow(/Unplanned lesson content/);
});

test("course validation rejects malformed answer options", () => {
  const invalidModules = structuredClone(a1CourseModules);
  const practice = invalidModules[0].lessons[0].stepPractices.find((item) => item.type === "choice");
  if (!practice) throw new Error("Choice practice is missing");
  practice.options = [practice.answer, practice.answer];
  expect(() => validateCourseModules(invalidModules, a1CefrCoverage)).toThrow(/Неверные варианты выбора/);
});

test("progress and vocabulary ignore unknown or duplicate lesson slugs", () => {
  const knownSlug = allA1Lessons[0].slug;
  expect(Object.keys(buildInitialProgress(a1CourseModules))).toEqual(allA1Lessons.map((lesson) => lesson.slug));
  expect(filterKnownLessonSlugs(a1CourseModules, [knownSlug, "removed-lesson", knownSlug])).toEqual([knownSlug]);
  expect(contentVocabulary([knownSlug, "removed-lesson"]).every((item) => item.lesson_slug === knownSlug)).toBe(true);
  expect(contentVocabulary([knownSlug])).not.toHaveLength(0);
});

test("mistake scheduling advances through deterministic 3-day and 7-day review stages", () => {
  const nowMs = Date.parse("2026-08-30T12:00:00.000Z");
  const base = { id: "practice-1", lessonSlug: "greetings", prompt: "Pozdrav", answer: "Dobrý deň", nowMs };
  expect(nextMistakeRecord({ ...base, correct: true })).toBeNull();
  const failed = nextMistakeRecord({ ...base, correct: false });
  expect(failed).toMatchObject({ attempts: 1, mastered: false, reviewStage: 0, dueAt: "2026-08-30T12:00:00.000Z" });
  const firstReview = nextMistakeRecord({ ...base, previous: failed!, correct: true });
  expect(firstReview).toMatchObject({ attempts: 1, mastered: false, reviewStage: 1, dueAt: "2026-09-02T12:00:00.000Z" });
  expect(nextMistakeRecord({ ...base, previous: firstReview!, correct: true })).toEqual(firstReview);
  const mastered = nextMistakeRecord({ ...base, nowMs: Date.parse("2026-09-02T12:00:00.000Z"), previous: firstReview!, correct: true });
  expect(mastered).toMatchObject({ attempts: 1, mastered: true, reviewStage: 2, dueAt: "2026-09-09T12:00:00.000Z" });
});

test("lesson summary derives complete evidence from an immutable progress snapshot", () => {
  const lesson = module1.lessons[0];
  const reinforcementPractices = buildReinforcementPractices(lesson);
  const corePractices = lesson.stepPractices.filter((practice) => practice.sectionIndex < lesson.sections.length);
  const practiceResults = Object.fromEntries([...corePractices, ...reinforcementPractices].map((practice) => [practice.id, true]));
  const checkSelections = Object.fromEntries(lesson.knowledgeChecks.map((check) => [check.id, check.answer]));
  const summary = buildLessonSummary({ lesson, reinforcementPractices, practiceResults, checkSelections, mistakes: {}, userTurns: reinforcementPractices.length });
  expect(summary.understanding).toBe(100);
  expect(summary.level).toBe("Уверенное понимание");
  expect(summary.evidence?.coreCorrect).toBe(summary.evidence?.coreTotal);
  expect(summary.userTurns).toBe(reinforcementPractices.length);
  expect(summary.mistakes).toEqual([]);
});

test("course reset transforms clean only the selected lesson scope", () => {
  const target = module1.lessons[0];
  const external = module2.lessons[0];
  const scope = buildCourseResetScope([target]);
  const targetPracticeId = target.stepPractices[0].id;
  const targetReinforcementId = buildReinforcementPractices(target)[0].id;
  const externalPracticeId = external.stepPractices[0].id;
  expect(scope.activityIds).toContain(targetPracticeId);
  expect(scope.activityIds).toContain(targetReinforcementId);
  expect(scope.activityIds).not.toContain(externalPracticeId);
  expect(removeActivityScope({ [targetPracticeId]: "remove", [targetReinforcementId]: "remove", [externalPracticeId]: "keep", unknown: "keep" }, scope)).toEqual({ [externalPracticeId]: "keep", unknown: "keep" });
  expect(removeLessonScope({ [target.slug]: "remove", [external.slug]: "keep", unknown: "keep" }, scope)).toEqual({ [external.slug]: "keep", unknown: "keep" });
  expect(removeMistakeScope({ target: { id: "target", lessonSlug: target.slug, prompt: "p", answer: "a", attempts: 1, mastered: false }, external: { id: "external", lessonSlug: external.slug, prompt: "p", answer: "a", attempts: 1, mastered: false } }, scope)).toEqual({ external: { id: "external", lessonSlug: external.slug, prompt: "p", answer: "a", attempts: 1, mastered: false } });
  expect(resetProgressScope({ [target.slug]: "completed", [external.slug]: "in_progress", unknown: "completed" }, scope)).toEqual({ [target.slug]: "not_started", [external.slug]: "in_progress", unknown: "completed" });
});

test("every Module 1 reinforcement set has six different answers", () => {
  for (const lesson of module1.lessons) {
    const practices = buildReinforcementPractices(lesson);
    const answers = practices.map((practice) => practice.answer.normalize("NFC").toLocaleLowerCase("sk").replace(/\p{P}+/gu, " ").replace(/\s+/g, " ").trim());
    expect(practices, lesson.slug).toHaveLength(6);
    expect(new Set(answers).size, lesson.slug).toBe(6);
    if (lesson.reinforcementPractices?.length) continue;
    for (const [index, answer] of answers.entries()) {
      const answerTokens = new Set(answer.split(" "));
      for (const other of answers.slice(index + 1)) {
        const otherTokens = new Set(other.split(" "));
        const smaller = answerTokens.size <= otherTokens.size ? answerTokens : otherTokens;
        const larger = answerTokens.size <= otherTokens.size ? otherTokens : answerTokens;
        expect([...smaller].every((token) => larger.has(token)), `${lesson.slug}: ${answer} / ${other}`).toBe(false);
      }
    }
  }
});

test("every topic assessment and module final varies correct option positions", () => {
  for (const lesson of allA1Lessons) {
    const choicePositionsBySize = new Map<number, number[]>();
    for (const practice of buildReinforcementPractices(lesson)) {
      if (practice.type === "choice" && practice.options?.length) {
        const position = practice.options.indexOf(practice.answer);
        expect(position, `${lesson.slug}: ${practice.prompt}`).toBeGreaterThanOrEqual(0);
        choicePositionsBySize.set(practice.options.length, [...(choicePositionsBySize.get(practice.options.length) ?? []), position]);
      }
      const rowPositionsBySize = new Map<number, number[]>();
      for (const pair of practice.pairs ?? []) {
        if (!pair.options?.length) continue;
        const position = pair.options.indexOf(pair.answer);
        expect(position, `${lesson.slug}: ${practice.prompt}`).toBeGreaterThanOrEqual(0);
        rowPositionsBySize.set(pair.options.length, [...(rowPositionsBySize.get(pair.options.length) ?? []), position]);
      }
      for (const positions of rowPositionsBySize.values()) {
        if (positions.length >= 2) expect(new Set(positions).size, `${lesson.slug}: ${practice.prompt}`).toBeGreaterThan(1);
      }
    }
    for (const positions of choicePositionsBySize.values()) {
      if (positions.length >= 2) expect(new Set(positions).size, lesson.slug).toBeGreaterThan(1);
    }
  }

  for (const module of a1CourseModules) {
    const questions = buildModuleFinalQuestions(module.lessons);
    const positionsBySize = new Map<number, number[]>();
    for (const question of questions) {
      const position = question.options.indexOf(question.answer);
      expect(position, `${module.slug}: ${question.id}`).toBeGreaterThanOrEqual(0);
      positionsBySize.set(question.options.length, [...(positionsBySize.get(question.options.length) ?? []), position]);
    }
    for (const positions of positionsBySize.values()) {
      if (positions.length >= 2) expect(new Set(positions).size, module.slug).toBeGreaterThan(1);
    }
  }
});

test("Module 1 final test does not repeat normative answers", () => {
  const questions = buildModuleFinalQuestions(module1.lessons);
  const answers = questions.map((question) => question.answer.normalize("NFC").toLocaleLowerCase("sk").replace(/\p{P}+/gu, " ").replace(/\s+/g, " ").trim());
  expect(new Set(answers).size).toBe(answers.length);
  expect(questions.filter((question) => question.lessonSlug === "soft-hard-consonants").map((question) => question.answer)).not.toContain("žena");
});

test("Module 2 matches the expanded content contract", () => {
  expect(module2.lessons.map((lesson) => lesson.slug)).toEqual([
    "masculine-nouns",
    "feminine-nouns",
    "neuter-nouns",
    "noun-number",
    "noun-endings",
    "who-what-is-it",
    "presence-absence",
  ]);
  expect(orderedModuleLessons(module2).map((lesson) => lesson.slug)).toEqual(
    module2.topicGroups?.flatMap((group) => group.lessonSlugs),
  );
  for (const lesson of module2.lessons) {
    expect(lesson.sections.length, lesson.slug).toBeGreaterThanOrEqual(5);
    expect(lesson.stepPractices.length, lesson.slug).toBeGreaterThanOrEqual(5);
    expect(lesson.theory.rules.length, lesson.slug).toBeGreaterThanOrEqual(3);
    expect(new Set(lesson.stepPractices.map((practice) => practice.sectionIndex)).size, lesson.slug).toBe(lesson.sections.length);
    expect(lesson.stepPractices.every((practice) => practice.id.startsWith(`m2-${lesson.slug}-`)), lesson.slug).toBe(true);
  }
  const finalQuestions = buildModuleFinalQuestions(module2.lessons);
  expect(new Set(finalQuestions.map((question) => question.lessonSlug))).toEqual(new Set(module2.lessons.map((lesson) => lesson.slug)));
  expect(new Set(finalQuestions.map((question) => question.answer)).size).toBe(finalQuestions.length);
  const vocabulary = contentVocabulary(module2.lessons.map((lesson) => lesson.slug));
  expect(vocabulary.length).toBeGreaterThanOrEqual(module2.lessons.length * 4);
  expect(new Set(vocabulary.map((item) => item.lesson_slug))).toEqual(new Set(module2.lessons.map((lesson) => lesson.slug)));
});

test("Module 3 matches the expanded content contract", () => {
  expect(module3.lessons.map((lesson) => lesson.slug)).toEqual([
    "adjective-gender",
    "adjective-plural",
    "demonstratives-possessives",
    "basic-description",
    "choice-contrast",
    "basic-connectors",
  ]);
  expect(orderedModuleLessons(module3).map((lesson) => lesson.slug)).toEqual(
    module3.topicGroups?.flatMap((group) => group.lessonSlugs),
  );
  for (const lesson of module3.lessons) {
    expect(lesson.sections.length, lesson.slug).toBeGreaterThanOrEqual(5);
    expect(lesson.stepPractices.length, lesson.slug).toBeGreaterThanOrEqual(5);
    expect(lesson.theory.rules.length, lesson.slug).toBeGreaterThanOrEqual(3);
    expect(new Set(lesson.stepPractices.map((practice) => practice.sectionIndex)).size, lesson.slug).toBe(lesson.sections.length);
    expect(lesson.stepPractices.every((practice) => practice.id.startsWith(`m3-${lesson.slug}-`)), lesson.slug).toBe(true);
  }
  const finalQuestions = buildModuleFinalQuestions(module3.lessons);
  expect(new Set(finalQuestions.map((question) => question.lessonSlug))).toEqual(new Set(module3.lessons.map((lesson) => lesson.slug)));
  expect(new Set(finalQuestions.map((question) => question.answer)).size).toBe(finalQuestions.length);
  const vocabulary = contentVocabulary(module3.lessons.map((lesson) => lesson.slug));
  expect(vocabulary.length).toBeGreaterThanOrEqual(module3.lessons.length * 4);
  expect(new Set(vocabulary.map((item) => item.lesson_slug))).toEqual(new Set(module3.lessons.map((lesson) => lesson.slug)));

  const sourceGroundedText = JSON.stringify(module3.lessons);
  for (const fragment of [
    "aký dom?, aká kniha?, aké auto?",
    "cudzí turisti, но cudzie mestá",
    "Jeho, jej, ich не изменяются",
    "fialový",
    "Nie červené, ale modré.",
    "Mám aj brata, aj sestru.",
    "Najprv raňajkujem, potom pracujem a nakoniec oddychujem.",
  ]) {
    expect(sourceGroundedText, fragment).toContain(fragment);
  }
});

test("Module 4 matches the expanded content contract", () => {
  expect(module4.lessons.map((lesson) => lesson.slug)).toEqual([
    "nominative", "accusative-nouns", "accusative-agreement", "locative-v-na", "genitive-quantity", "genitive-absence",
    "genitive-do", "preposition-government", "where-direction-origin", "dative-instrumental-models", "simple-route",
  ]);
  expect(orderedModuleLessons(module4).map((lesson) => lesson.slug)).toEqual(module4.topicGroups?.flatMap((group) => group.lessonSlugs));
  for (const lesson of module4.lessons) {
    expect(lesson.sections.length, lesson.slug).toBeGreaterThanOrEqual(5);
    expect(lesson.stepPractices.length, lesson.slug).toBeGreaterThanOrEqual(5);
    expect(new Set(lesson.stepPractices.map((practice) => practice.sectionIndex)).size, lesson.slug).toBe(lesson.sections.length);
    expect(lesson.stepPractices.every((practice) => practice.id.startsWith(`m4-${lesson.slug}-`)), lesson.slug).toBe(true);
  }
  const finalQuestions = buildModuleFinalQuestions(module4.lessons);
  expect(new Set(finalQuestions.map((question) => question.lessonSlug))).toEqual(new Set(module4.lessons.map((lesson) => lesson.slug)));
  expect(new Set(finalQuestions.map((question) => question.answer)).size).toBe(finalQuestions.length);
  const vocabulary = contentVocabulary(module4.lessons.map((lesson) => lesson.slug));
  expect(vocabulary.length).toBeGreaterThanOrEqual(module4.lessons.length * 4);
  expect(new Set(vocabulary.map((item) => item.lesson_slug))).toEqual(new Set(module4.lessons.map((lesson) => lesson.slug)));

  const sourceGroundedText = JSON.stringify(module4.lessons);
  for (const fragment of [
    "študenti → študentov",
    "na neho, na ňu, na nich",
    "v obchodoch, v školách, na uliciach",
    "dve knihy, tri knihy, štyri autá",
    "Niet času. Niet vody. Niet peňazí.",
    "Idem domov означает",
    "na stole — Kde? + Lokál",
    "u lekára, k lekárovi, od lekára",
    "so mnou, s tebou, s ním, s ňou",
    "naľavo/napravo — где",
    "doľava/doprava — куда",
  ]) {
    expect(sourceGroundedText.includes(fragment), `Module 4 content must include: ${fragment}`).toBe(true);
  }
});

test("Module 5 matches the expanded content contract", () => {
  expect(module5.lessons.map((lesson) => lesson.slug)).toEqual([
    "present-tense", "irregular-verbs", "reflexive-sa-si", "verb-negation-questions", "chciet-infinitive", "moct-infinitive",
    "musiet-infinitive", "vediet-infinitive", "modal-questions-negation", "polite-requests", "basic-imperative",
  ]);
  expect(orderedModuleLessons(module5).map((lesson) => lesson.slug)).toEqual(module5.topicGroups?.flatMap((group) => group.lessonSlugs));
  for (const lesson of module5.lessons) {
    expect(lesson.sections.length, lesson.slug).toBeGreaterThanOrEqual(5);
    expect(lesson.stepPractices.length, lesson.slug).toBeGreaterThanOrEqual(5);
    expect(new Set(lesson.stepPractices.map((practice) => practice.sectionIndex)).size, lesson.slug).toBe(lesson.sections.length);
    expect(lesson.stepPractices.every((practice) => practice.id.startsWith(`m5-${lesson.slug}-`)), lesson.slug).toBe(true);
  }
  const finalQuestions = buildModuleFinalQuestions(module5.lessons);
  expect(new Set(finalQuestions.map((question) => question.lessonSlug))).toEqual(new Set(module5.lessons.map((lesson) => lesson.slug)));
  expect(new Set(finalQuestions.map((question) => question.answer)).size).toBe(finalQuestions.length);
  const vocabulary = contentVocabulary(module5.lessons.map((lesson) => lesson.slug));
  expect(vocabulary.length).toBeGreaterThanOrEqual(module5.lessons.length * 4);
  expect(new Set(vocabulary.map((item) => item.lesson_slug))).toEqual(new Set(module5.lessons.map((lesson) => lesson.slug)));
});

test("Module 6 matches the expanded content contract", () => {
  expect(module6.lessons).toHaveLength(18);
  expect(orderedModuleLessons(module6).map((lesson) => lesson.slug)).toEqual(module6.topicGroups?.flatMap((group) => group.lessonSlugs));
  for (const lesson of module6.lessons) {
    expect(lesson.sections.length, lesson.slug).toBeGreaterThanOrEqual(5);
    expect(lesson.stepPractices.length, lesson.slug).toBeGreaterThanOrEqual(5);
    expect(new Set(lesson.stepPractices.map((practice) => practice.sectionIndex)).size, lesson.slug).toBe(lesson.sections.length);
    expect(lesson.stepPractices.every((practice) => practice.id.startsWith(`m6-${lesson.slug}-`)), lesson.slug).toBe(true);
  }
  const finals = buildModuleFinalQuestions(module6.lessons);
  expect(new Set(finals.map((question) => question.lessonSlug))).toEqual(new Set(module6.lessons.map((lesson) => lesson.slug)));
  expect(new Set(finals.map((question) => question.answer)).size).toBe(finals.length);
  const vocabulary = contentVocabulary(module6.lessons.map((lesson) => lesson.slug));
  expect(new Set(vocabulary.map((item) => item.lesson_slug))).toEqual(new Set(module6.lessons.map((lesson) => lesson.slug)));
});

function createState(overrides: Partial<CourseState> = {}): CourseState {
  return {
    activeModule: 1,
    selectedSlug: module1.lessons[0].slug,
    fontSize: "large",
    progress: Object.fromEntries(module1.lessons.map((lesson) => [lesson.slug, "not_started"])),
    lessonSteps: {},
    checkSelections: {},
    practiceAnswers: {},
    practiceResults: {},
    mistakes: {},
    finalSelections: {},
    finalCompleted: false,
    finalCompletedModules: {},
    chatHistories: {},
    lessonSummaries: {},
    ...overrides,
  };
}

async function mockStateApi(page: Page, initialState: CourseState): Promise<void> {
  let state = structuredClone(initialState);
  await page.route("**/api/v1/course/state", async (route) => {
    if (route.request().method() === "PUT") {
      state = route.request().postDataJSON() as CourseState;
    }
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({ exists: true, schema_version: 1, state, updated_at: null }),
    });
  });
}

async function openCourse(page: Page): Promise<void> {
  const restored = page.waitForResponse((response) =>
    response.url().includes("/api/v1/course/state") && response.request().method() === "GET",
  );
  await page.goto("/");
  await restored;
  await expect(page.getByRole("heading", { name: module1.title })).toBeVisible();
  await expect(page.locator(".course-persistence-error")).toHaveCount(0);
}

async function openLesson(page: Page, lesson: CourseLesson): Promise<void> {
  const groupTitle = module1.topicGroups?.find((group) => group.lessonSlugs.includes(lesson.slug))?.title;
  if (!groupTitle) throw new Error(`Lesson ${lesson.slug} is not assigned to a topic group`);
  await page.locator(".course-group-card").filter({ hasText: groupTitle }).click();
  await page.getByRole("button", { name: new RegExp(lesson.title) }).first().click();
  await expect(page.locator(".course-material-heading h3")).toHaveText(lesson.title);
}

test("review combines mistakes from every module and opens the affected topic", async ({ page }) => {
  const firstLesson = module1.lessons[0];
  const priorityLesson = module2.lessons[0];
  const firstPractice = firstLesson.stepPractices[0];
  const priorityPractice = priorityLesson.stepPractices[0];
  await mockStateApi(page, createState({
    mistakes: {
      [firstPractice.id]: { id: firstPractice.id, lessonSlug: firstLesson.slug, prompt: firstPractice.prompt, answer: firstPractice.answer, attempts: 1, mastered: false },
      [priorityPractice.id]: { id: priorityPractice.id, lessonSlug: priorityLesson.slug, prompt: priorityPractice.prompt, answer: priorityPractice.answer, attempts: 3, mastered: false },
    },
  }));

  await openCourse(page);
  await page.getByRole("button", { name: "Ошибки", exact: true }).click();

  await expect(page.getByRole("heading", { name: "Где нужно подтянуть знания" })).toBeVisible();
  const overview = page.getByLabel("Сводка ошибок по курсу");
  await expect(overview.getByText("2", { exact: true })).toHaveCount(3);
  await expect(overview.getByText("1", { exact: true })).toHaveCount(1);
  await expect(page.locator(".course-review-list").first()).toContainText(firstLesson.title);
  await expect(page.locator(".course-review-list").first()).toContainText(priorityLesson.title);
  await expect(page.locator(".course-gap-priorities button").first()).toContainText(priorityLesson.title);

  await page.locator(".course-gap-priorities button").first().click();
  await expect(page.getByRole("heading", { name: module2.title })).toBeVisible();
  await expect(page.locator(".course-material-heading h3")).toHaveText(priorityLesson.title);
  await expect(page.getByRole("button", { name: "Обучение", exact: true })).toHaveClass("active");
});

test("incorrect final-test answers join the course-wide mistake review", async ({ page }) => {
  const finalQuestions = buildModuleFinalQuestions(module1.lessons);
  await mockStateApi(page, createState({
    progress: Object.fromEntries(module1.lessons.map((lesson) => [lesson.slug, "completed"])),
  }));

  await openCourse(page);
  await page.getByRole("button", { name: "Итоговый тест", exact: true }).click();
  const fields = page.locator(".course-final .course-check-list fieldset");
  await expect(fields).toHaveCount(finalQuestions.length);
  for (const [index, question] of finalQuestions.entries()) {
    const wrongOption = question.options.find((option) => option !== question.answer);
    if (!wrongOption) throw new Error(`Final question ${question.id} has no wrong option`);
    await fields.nth(index).getByRole("button", { name: wrongOption, exact: true }).click();
  }
  await page.getByRole("button", { name: "Проверить итоговый тест", exact: true }).click();
  await page.getByRole("button", { name: "Ошибки", exact: true }).click();

  await expect(page.getByRole("heading", { name: "Где нужно подтянуть знания" })).toBeVisible();
  await expect(page.locator(".course-review-list").first().locator("article")).toHaveCount(finalQuestions.length);
  await expect(page.getByText(finalQuestions[0].question, { exact: true })).toBeVisible();
});

test("AI settings switch provider without receiving saved secrets", async ({ page }) => {
  await mockStateApi(page, createState());
  let provider = "codex";
  let savedPayload: Record<string, unknown> | null = null;
  await page.route("**/api/v1/tutor/settings", async (route) => {
    if (route.request().method() === "PUT") {
      savedPayload = route.request().postDataJSON() as Record<string, unknown>;
      provider = String(savedPayload.provider);
    }
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        provider,
        codex_installed: true,
        codex_authenticated: true,
        codex_message: "Codex подключён.",
        openai_api_key_configured: false,
        openai_model: "gpt-5",
        polza_api_key_configured: provider === "polza",
        polza_model: "openai/gpt-4o-mini",
        polza_base_url: "https://polza.ai/api/v1",
      }),
    });
  });

  await openCourse(page);
  await page.getByRole("button", { name: "Открыть настройки" }).click();
  const dialog = page.getByRole("dialog", { name: "Настройки" });
  await expect(dialog).toBeVisible();
  await dialog.getByText("Polza API", { exact: true }).click();
  await dialog.getByLabel("API-ключ Polza").fill("temporary-test-key");
  await dialog.getByRole("button", { name: "Сохранить настройки ИИ" }).click();
  await expect(dialog.getByRole("status")).toContainText("Настройки сохранены");
  expect(savedPayload).toMatchObject({ provider: "polza", polza_api_key: "temporary-test-key" });
  await dialog.getByRole("button", { name: "Закрыть настройки" }).click();
  await expect(dialog).toBeHidden();
});

test("tablet header keeps navigation and settings inside the viewport", async ({ page }) => {
  await page.setViewportSize({ width: 768, height: 1024 });
  await mockStateApi(page, createState());
  await openCourse(page);

  await expect(page.getByRole("button", { name: "Открыть настройки" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Включить тёмную тему" })).toBeVisible();
  const dimensions = await page.evaluate(() => {
    const header = document.querySelector<HTMLElement>(".course-route-header");
    const settings = document.querySelector<HTMLElement>('[aria-label="Открыть настройки"]');
    return {
      clientWidth: document.documentElement.clientWidth,
      scrollWidth: document.documentElement.scrollWidth,
      headerRight: header?.getBoundingClientRect().right ?? 0,
      settingsRight: settings?.getBoundingClientRect().right ?? 0,
    };
  });
  expect(dimensions.scrollWidth).toBeLessThanOrEqual(dimensions.clientWidth);
  expect(dimensions.headerRight).toBeLessThanOrEqual(dimensions.clientWidth);
  expect(dimensions.settingsRight).toBeLessThanOrEqual(dimensions.clientWidth);
});

test("module switcher keeps a visible gap before the course badge", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await mockStateApi(page, createState());
  await openCourse(page);

  const spacing = await page.evaluate(() => {
    const switcher = document.querySelector<HTMLElement>(".course-module-switcher");
    const badge = document.querySelector<HTMLElement>(".course-kicker");
    const switcherBox = switcher?.getBoundingClientRect();
    const badgeBox = badge?.getBoundingClientRect();
    return {
      horizontalGap: (badgeBox?.left ?? 0) - (switcherBox?.right ?? 0),
      marginRight: switcher ? Number.parseFloat(getComputedStyle(switcher).marginRight) : 0,
    };
  });

  expect(spacing.marginRight).toBe(12);
  expect(spacing.horizontalGap).toBeGreaterThanOrEqual(12);
});

test("mobile material uses a compact lesson picker before the article", async ({ page }) => {
  const lesson = module1.lessons[0];
  await page.setViewportSize({ width: 390, height: 844 });
  await mockStateApi(page, createState({
    selectedSlug: lesson.slug,
    fontSize: "extra-large",
    progress: { [lesson.slug]: "in_progress" },
  }));
  await openCourse(page);
  await openLesson(page, lesson);

  const picker = page.getByLabel(`Выберите тему ${module1.title}`);
  await expect(picker).toBeVisible();
  await expect(picker).toHaveValue(lesson.slug);
  await expect(page.locator(".course-lesson-list")).toBeHidden();
  const dimensions = await page.evaluate(() => {
    const pickerElement = document.querySelector<HTMLElement>(".course-lesson-picker");
    const article = document.querySelector<HTMLElement>(".course-material");
    return {
      clientWidth: document.documentElement.clientWidth,
      scrollWidth: document.documentElement.scrollWidth,
      gap: (article?.getBoundingClientRect().top ?? 0) - (pickerElement?.getBoundingClientRect().bottom ?? 0),
    };
  });
  expect(dimensions.scrollWidth).toBeLessThanOrEqual(dimensions.clientWidth);
  expect(dimensions.gap).toBeLessThanOrEqual(20);

  await picker.selectOption(module1.lessons[1].slug);
  await expect(page.locator(".course-material-heading h3")).toHaveText(module1.lessons[1].title);
});

test("cached progress survives backend outage and reconnects without reload", async ({ page }) => {
  const completedProgress = Object.fromEntries(module1.lessons.map((lesson) => [lesson.slug, "completed"]));
  const serverState = createState({ progress: completedProgress });
  let backendAvailable = true;
  let getRequests = 0;
  let savedState: CourseState | null = null;
  await page.route("**/api/v1/course/state", async (route) => {
    if (route.request().method() === "GET") getRequests += 1;
    if (!backendAvailable) {
      await route.fulfill({ status: 503, contentType: "application/json", body: JSON.stringify({ detail: "Backend unavailable" }) });
      return;
    }
    if (route.request().method() === "PUT") savedState = route.request().postDataJSON() as CourseState;
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({ exists: true, schema_version: 1, state: serverState, updated_at: null }),
    });
  });

  await page.goto("/");
  await expect(page.locator(".course-progress strong")).toHaveText("14/14");
  await expect(page.locator(".course-persistence-error")).toHaveCount(0);

  backendAvailable = false;
  await page.reload();
  await expect(page.locator(".course-progress strong")).toHaveText("14/14");
  await expect(page.locator(".course-persistence-error")).toBeVisible();
  await page.getByRole("button", { name: "Обычный размер текста" }).click();

  backendAvailable = true;
  await expect(page.locator(".course-persistence-error")).toHaveCount(0, { timeout: 5_000 });
  await expect(page.locator(".course-progress strong")).toHaveText("14/14");
  await expect(page.getByRole("button", { name: "Обычный размер текста" })).toHaveAttribute("aria-pressed", "true");
  await expect.poll(() => savedState?.fontSize).toBe("normal");
  expect(getRequests).toBeGreaterThanOrEqual(3);
});

test("alphabet section groups the first six lessons as cards", async ({ page }) => {
  await mockStateApi(page, createState());
  await openCourse(page);

  const alphabetCard = page.locator(".course-group-card");
  await expect(alphabetCard).toHaveCount(4);
  await expect(page.getByText("Знакомство и общение", { exact: true })).toBeVisible();
  await expect(page.getByText("Числа и календарь", { exact: true })).toBeVisible();
  await expect(page.getByText("Базовая грамматика", { exact: true })).toBeVisible();
  await expect(page.getByRole("button", { name: new RegExp(module1.lessons[0].title) })).toHaveCount(0);
  await alphabetCard.filter({ hasText: "Алфавит" }).click();

  await expect(page.getByRole("heading", { name: "Алфавит" })).toBeVisible();
  await expect(page.locator(".course-topic-grid .course-topic-card")).toHaveCount(6);
  await expect(page.locator(".course-topic-number")).toHaveText(["01", "02", "03", "04", "05", "06"]);
  for (const lesson of module1.lessons.slice(0, 6)) await expect(page.getByRole("button", { name: new RegExp(lesson.title) })).toBeVisible();
  await page.getByRole("button", { name: "← К разделам" }).click();
  await expect(alphabetCard).toHaveCount(4);
  for (const [title, count, numbers] of [["Знакомство и общение", 3, ["07", "08", "09"]], ["Числа и календарь", 2, ["10", "11"]], ["Базовая грамматика", 3, ["12", "13", "14"]]] as const) {
    await page.locator(".course-group-card").filter({ hasText: title }).click();
    await expect(page.getByRole("heading", { name: title })).toBeVisible();
    await expect(page.locator(".course-topic-grid .course-topic-card")).toHaveCount(count);
    await expect(page.locator(".course-topic-number")).toHaveText(numbers);
    await page.getByRole("button", { name: "← К разделам" }).click();
  }
});

test("Theme 2 ends after five material steps and moves six exercises to its final test", async ({ page }) => {
  const lesson = module1.lessons.find((item) => item.slug === "long-short-vowels");
  if (!lesson) throw new Error("Long and short vowels lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.sectionIndex === 4);
  if (!lastPractice) throw new Error("Theme 2 step 5 practice is missing");
  await mockStateApi(page, createState({
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));

  await openCourse(page);
  await openLesson(page, lesson);
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Частые ошибки");
  await expect(page.getByRole("button", { name: "Открыть шаг 6" })).toHaveCount(0);
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы");
  await expect(page.getByText("Финальный тест темы", { exact: true })).toHaveCount(0);
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const matchingTask = page.locator(".course-reinforcement fieldset").nth(5);
  const matchingPractice = buildReinforcementPractices(lesson)[5];
  for (const [index, pair] of (matchingPractice.pairs ?? []).entries()) await matchingTask.locator(".course-pair-row").nth(index).getByRole("button", { name: pair.answer, exact: true }).click();
  await matchingTask.getByRole("button", { name: "Проверить" }).click();
  await expect(matchingTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(matchingTask).toHaveClass(/correct/);
});

test("Theme 11 follows the PDF sequence and uses a six-task interactive final test", async ({ page }) => {
  const lesson = module1.lessons.find((item) => item.slug === "days-and-months");
  if (!lesson) throw new Error("Days and months lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "days-step-6");
  if (!lastPractice) throw new Error("Theme 11 step 6 practice is missing");
  await mockStateApi(page, createState({
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 5 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));

  await openCourse(page);
  await openLesson(page, lesson);
  await expect(page.locator(".course-stepper")).toContainText("Шаг 6 из 6");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Частые ошибки");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 11");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const formsTask = page.locator(".course-reinforcement fieldset").nth(1);
  await expect(formsTask.locator(".course-pair-row")).toHaveCount(4);
  const formsPractice = buildReinforcementPractices(lesson)[1];
  for (const [index, pair] of (formsPractice.pairs ?? []).entries()) {
    const wrongOption = pair.options?.find((option) => option !== pair.answer);
    if (!wrongOption) throw new Error(`No wrong option for ${pair.prompt}`);
    await formsTask.locator(".course-pair-row").nth(index).getByRole("button", { name: wrongOption, exact: true }).click();
  }
  await formsTask.getByRole("button", { name: "Проверить" }).click();
  await expect(formsTask.locator(".course-pair-row.incorrect")).toHaveCount(4);
  await expect(formsTask.locator(".course-pair-row").first()).toContainText("Правильно: v pondelok");
  for (const [index, pair] of (formsPractice.pairs ?? []).entries()) {
    await formsTask.locator(".course-pair-row").nth(index).getByRole("button", { name: pair.answer, exact: true }).click();
  }
  await formsTask.getByRole("button", { name: "Проверить" }).click();
  await expect(formsTask.locator(".course-pair-row.correct")).toHaveCount(4);
});

test("Theme 12 follows the pronouns PDF and checks translations row by row", async ({ page }) => {
  const lesson = module1.lessons.find((item) => item.slug === "personal-pronouns");
  if (!lesson) throw new Error("Personal pronouns lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "pronouns-step-5");
  if (!lastPractice) throw new Error("Theme 12 step 5 practice is missing");
  await mockStateApi(page, createState({
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));

  await openCourse(page);
  await openLesson(page, lesson);
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Частые ошибки");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 12");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const rows = translationTask.locator(".course-pair-row");
  await expect(rows).toHaveCount(4);
  const checkButton = translationTask.getByRole("button", { name: "Проверить" });
  await expect(checkButton).toBeDisabled();
  await rows.nth(0).getByRole("textbox").fill("On je lekár");
  await rows.nth(1).getByRole("textbox").fill("My sme priateľ.");
  await rows.nth(2).getByRole("textbox").fill("Vy ste zo Slovenska.");
  await rows.nth(3).getByRole("textbox").fill("Oni sú tu.");
  await expect(checkButton).toBeEnabled();
  await checkButton.click();
  await expect(translationTask.locator(".course-pair-row.correct")).toHaveCount(3);
  await expect(rows.nth(1)).toHaveClass(/incorrect/);
  await expect(rows.nth(1)).toContainText("Правильно: My sme priatelia.");
  await rows.nth(1).getByRole("textbox").fill("My sme priatelia.");
  await checkButton.click();
  await expect(translationTask.locator(".course-pair-row.correct")).toHaveCount(4);
});

test("Theme 13 follows the byť PDF and accepts both natural question variants", async ({ page }) => {
  const lesson = module1.lessons.find((item) => item.slug === "verb-byt");
  if (!lesson) throw new Error("Verb byť lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "byt-step-5");
  if (!lastPractice) throw new Error("Theme 13 step 5 practice is missing");
  await mockStateApi(page, createState({
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));

  await openCourse(page);
  await openLesson(page, lesson);
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Частые ошибки");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 13");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const questionTask = page.locator(".course-reinforcement fieldset").nth(2);
  const rows = questionTask.locator(".course-pair-row");
  await expect(rows).toHaveCount(3);
  const checkButton = questionTask.getByRole("button", { name: "Проверить" });
  await expect(checkButton).toBeDisabled();
  await rows.nth(0).getByRole("textbox").fill("Si unavený");
  await rows.nth(1).getByRole("textbox").fill("Ste Ruska?");
  await rows.nth(2).getByRole("textbox").fill("Sú v škole?");
  await expect(checkButton).toBeEnabled();
  await checkButton.click();
  await expect(questionTask.locator(".course-pair-row.correct")).toHaveCount(2);
  await expect(rows.nth(1)).toHaveClass(/incorrect/);
  await expect(rows.nth(1)).toContainText("Правильно: Ste z Ruska?");
  await rows.nth(1).getByRole("textbox").fill("Ste z Ruska?");
  await checkButton.click();
  await expect(questionTask.locator(".course-pair-row.correct")).toHaveCount(3);
});

test("Theme 14 follows the question-word PDF and uses normative agreement", async ({ page }) => {
  const lesson = module1.lessons.find((item) => item.slug === "question-words");
  if (!lesson) throw new Error("Question words lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m1-question-words-step-5");
  if (!lastPractice) throw new Error("Theme 14 step 5 practice is missing");
  await mockStateApi(page, createState({
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));

  await openCourse(page);
  await openLesson(page, lesson);
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Частые ошибки");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 14");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const agreementTask = page.locator(".course-reinforcement fieldset").nth(3);
  const rows = agreementTask.locator(".course-pair-row");
  await expect(rows).toHaveCount(3);
  await rows.nth(0).getByRole("button", { name: "aký kniha", exact: true }).click();
  await rows.nth(1).getByRole("button", { name: "ktorá autobus", exact: true }).click();
  await rows.nth(2).getByRole("button", { name: "čia auto", exact: true }).click();
  await agreementTask.getByRole("button", { name: "Проверить" }).click();
  await expect(agreementTask.locator(".course-pair-row.incorrect")).toHaveCount(3);
  await expect(rows.nth(2)).toContainText("Правильно: čie auto");
  for (const [index, answer] of ["aká kniha", "ktorý autobus", "čie auto"].entries()) {
    await rows.nth(index).getByRole("button", { name: answer, exact: true }).click();
  }
  await agreementTask.getByRole("button", { name: "Проверить" }).click();
  await expect(agreementTask.locator(".course-pair-row.correct")).toHaveCount(3);
});

test("Theme 3 final task uses closed diphthong choices instead of unknown grammar", async ({ page }) => {
  const lesson = module1.lessons.find((item) => item.slug === "diphthongs");
  if (!lesson) throw new Error("Diphthongs lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.sectionIndex === 4);
  if (!lastPractice) throw new Error("Theme 3 step 5 practice is missing");
  await mockStateApi(page, createState({
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));

  await openCourse(page);
  await openLesson(page, lesson);
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  const task = page.locator(".course-reinforcement fieldset").nth(5);
  await expect(task.getByText("Вставьте недостающий дифтонг в каждое слово.")).toBeVisible();
  await expect(task.locator(".course-pair-row")).toHaveCount(4);
  const practice = buildReinforcementPractices(lesson)[5];
  for (const [index, pair] of (practice.pairs ?? []).entries()) {
    await task.locator(".course-pair-row").nth(index).getByRole("button", { name: pair.answer, exact: true }).click();
  }
  await task.getByRole("button", { name: "Проверить" }).click();
  await expect(task.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(task).toHaveClass(/correct/);
});

test("Theme 4 uses clear closed tasks for hidden softness and final review", async ({ page }) => {
  const lesson = module1.lessons.find((item) => item.slug === "soft-hard-consonants");
  if (!lesson) throw new Error("Soft and hard consonants lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.sectionIndex === 4);
  if (!lastPractice) throw new Error("Theme 4 step 5 practice is missing");
  await mockStateApi(page, createState({
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));

  await openCourse(page);
  await openLesson(page, lesson);
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  const practices = buildReinforcementPractices(lesson);
  const hiddenSoftnessTask = page.locator(".course-reinforcement fieldset").nth(1);
  await expect(hiddenSoftnessTask.getByText("Выберите мягкие звуки, которые слышны в каждом слове.")).toBeVisible();
  await expect(hiddenSoftnessTask.locator("input")).toHaveCount(0);
  for (const [index, pair] of (practices[1].pairs ?? []).entries()) {
    await hiddenSoftnessTask.locator(".course-pair-row").nth(index).getByRole("button", { name: pair.answer, exact: true }).click();
  }
  await hiddenSoftnessTask.getByRole("button", { name: "Проверить" }).click();
  await expect(hiddenSoftnessTask.locator(".course-pair-row.correct")).toHaveCount(5);

  const reviewTask = page.locator(".course-reinforcement fieldset").nth(5);
  await expect(reviewTask.getByText("Определите, как обозначена мягкость в каждом слове.")).toBeVisible();
  await expect(reviewTask.locator("input")).toHaveCount(0);
  for (const [index, pair] of (practices[5].pairs ?? []).entries()) {
    const row = reviewTask.locator(".course-pair-row").nth(index);
    await expect(row.getByRole("button")).toHaveText(["явная", "скрытая"]);
    await row.getByRole("button", { name: pair.answer, exact: true }).click();
  }
  await reviewTask.getByRole("button", { name: "Проверить" }).click();
  await expect(reviewTask.locator(".course-pair-row.correct")).toHaveCount(6);
});

test("Theme 5 ends after five steps and uses a closed six-task final test", async ({ page }) => {
  const lesson = module1.lessons.find((item) => item.slug === "word-stress");
  if (!lesson) throw new Error("Word stress lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.sectionIndex === 4);
  if (!lastPractice) throw new Error("Theme 5 step 5 practice is missing");
  await mockStateApi(page, createState({
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));

  await openCourse(page);
  await openLesson(page, lesson);
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Частые ошибки");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 5");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const practices = buildReinforcementPractices(lesson);

  const stressTask = page.locator(".course-reinforcement fieldset").nth(0);
  await expect(stressTask.getByText("Выберите вариант, где ударный слог выделен прописными буквами.")).toBeVisible();
  await expect(stressTask.locator(".course-pair-row").nth(1).getByRole("button")).toHaveText(["RO-di-na", "ro-DI-na", "ro-di-NA"]);

  const prepositionTask = page.locator(".course-reinforcement fieldset").nth(3);
  await expect(prepositionTask.getByText("Определите, читать ли сочетание слитно или с паузой.")).toBeVisible();
  for (const [index, pair] of (practices[3].pairs ?? []).entries()) {
    const row = prepositionTask.locator(".course-pair-row").nth(index);
    await expect(row.getByRole("button")).toHaveText(["слитно", "с паузой"]);
    await row.getByRole("button", { name: pair.answer, exact: true }).click();
  }
  await prepositionTask.getByRole("button", { name: "Проверить" }).click();
  await expect(prepositionTask.locator(".course-pair-row.correct")).toHaveCount(4);

  const reviewTask = page.locator(".course-reinforcement fieldset").nth(5);
  await expect(reviewTask.getByText("Определите главный фокус чтения в каждом примере.")).toBeVisible();
  await expect(reviewTask.locator("input")).toHaveCount(0);
  for (const [index, pair] of (practices[5].pairs ?? []).entries()) {
    const row = reviewTask.locator(".course-pair-row").nth(index);
    await expect(row.getByRole("button")).toHaveText(["Долгота", "Первый слог", "Ритмическая группа"]);
    await row.getByRole("button", { name: pair.answer, exact: true }).click();
  }
  await reviewTask.getByRole("button", { name: "Проверить" }).click();
  await expect(reviewTask.locator(".course-pair-row.correct")).toHaveCount(6);
});

test("Theme 6 follows the rhythmic-law source and uses a closed six-task final test", async ({ page }) => {
  const lesson = module1.lessons.find((item) => item.slug === "rhythmic-law");
  if (!lesson) throw new Error("Rhythmic law lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.sectionIndex === 4);
  if (!lastPractice) throw new Error("Theme 6 step 5 practice is missing");
  expect(lesson.sections.map((section) => section.title)).toEqual([
    "Что говорит ритмический закон",
    "Что считается долгим слогом",
    "Полезные модели A1",
    "Банк примеров и исключения",
    "Частые ошибки",
  ]);
  expect(lesson.stepPractices).toHaveLength(5);

  await mockStateApi(page, createState({
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));

  await openCourse(page);
  await openLesson(page, lesson);
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Частые ошибки");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 6");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const practices = buildReinforcementPractices(lesson);
  const syllableTask = page.locator(".course-reinforcement fieldset").nth(0);
  const syllableColumns = [
    ["krás", "ny"],
    ["bie", "ly"],
    ["pia", "ty"],
    ["spie", "vam"],
    ["chvá", "lim"],
  ];
  const syllableColumnPositions: number[][] = [];
  for (const [index, columns] of syllableColumns.entries()) {
    const row = syllableTask.locator(".course-pair-row").nth(index);
    await expect(row.getByRole("button")).toHaveText(columns);
    syllableColumnPositions.push(await row.getByRole("button").evaluateAll((buttons) => buttons.map((button) => Math.round(button.getBoundingClientRect().x))));
  }
  expect(syllableColumnPositions.every((positions) => positions.length === 2 && positions.every((position, index) => position === syllableColumnPositions[0][index]))).toBe(true);
  const reviewTask = page.locator(".course-reinforcement fieldset").nth(5);
  await expect(reviewTask.getByText("Определите, что запускает сокращение в каждом слове.")).toBeVisible();
  await expect(reviewTask.locator("input")).toHaveCount(0);
  const triggerColumns = ["долгая гласная á", "дифтонг ie", "дифтонг ia", "долгого слога перед окончанием нет"];
  const triggerColumnPositions: number[][] = [];
  for (const [index, pair] of (practices[5].pairs ?? []).entries()) {
    const row = reviewTask.locator(".course-pair-row").nth(index);
    await expect(row.getByRole("button")).toHaveText(triggerColumns);
    triggerColumnPositions.push(await row.getByRole("button").evaluateAll((buttons) => buttons.map((button) => Math.round(button.getBoundingClientRect().x))));
    await row.getByRole("button", { name: pair.answer, exact: true }).click();
  }
  expect(triggerColumnPositions.every((positions) => positions.length === 4 && positions.every((position, index) => position === triggerColumnPositions[0][index]))).toBe(true);
  await reviewTask.getByRole("button", { name: "Проверить" }).click();
  await expect(reviewTask.locator(".course-pair-row.correct")).toHaveCount(5);

  await page.setViewportSize({ width: 600, height: 900 });
  const narrowTriggerPositions = await reviewTask.locator(".course-pair-row").evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button")).map((button) => Math.round(button.getBoundingClientRect().x))));
  expect(narrowTriggerPositions.every((positions) => positions.length === 4 && positions[0] === positions[2] && positions[1] === positions[3])).toBe(true);
});

test("Theme 6 renders its pair practice inside the material step", async ({ page }) => {
  const lesson = module1.lessons.find((item) => item.slug === "rhythmic-law");
  if (!lesson) throw new Error("Rhythmic law lesson is missing");
  const practice = lesson.stepPractices.find((item) => item.sectionIndex === 1);
  if (!practice) throw new Error("Theme 6 step 2 practice is missing");
  await mockStateApi(page, createState({
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 1 },
  }));

  await openCourse(page);
  await openLesson(page, lesson);
  await expect(page.locator(".course-stepper")).toContainText("Шаг 2 из 5");
  const task = page.locator(".course-practice");
  await expect(task.getByText("Определите тип долготы в каждом слове.")).toBeVisible();
  await expect(task.locator(".course-pair-row")).toHaveCount(3);
  const check = task.getByRole("button", { name: "Проверить ответ" });
  await expect(check).toBeDisabled();

  const pairs = practice.pairs ?? [];
  for (let index = 0; index < pairs.length; index += 1) {
    await expect(task.locator(".course-pair-row").nth(index).getByRole("button")).toHaveText(["дифтонг", "долгая гласная"]);
  }
  await task.locator(".course-pair-row").nth(0).getByRole("button", { name: pairs[0].answer, exact: true }).click();
  await expect(check).toBeDisabled();
  for (let index = 1; index < pairs.length; index += 1) {
    await task.locator(".course-pair-row").nth(index).getByRole("button", { name: pairs[index].answer, exact: true }).click();
  }
  await expect(check).toBeEnabled();
  await check.click();
  await expect(task.locator(".course-pair-row.correct")).toHaveCount(3);
  await expect(page.getByRole("button", { name: "Следующий шаг →" })).toBeEnabled();
});

test("Theme 7 follows the greetings source and preserves its six progress steps", async ({ page }) => {
  const lesson = module1.lessons.find((item) => item.slug === "greetings");
  if (!lesson) throw new Error("Greetings lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "greetings-step-6");
  if (!lastPractice) throw new Error("Theme 7 step 6 practice is missing");
  expect(lesson.sections.map((section) => section.title)).toEqual([
    "Формально или неформально",
    "Как спросить «как дела?»",
    "Первая встреча",
    "Как попрощаться",
    "Три готовых мини-диалога",
    "Частые ошибки",
  ]);
  expect(lesson.stepPractices.map((practice) => practice.id)).toEqual([
    "greetings-step-1",
    "greetings-step-2",
    "greetings-step-3",
    "greetings-step-4",
    "greetings-step-5",
    "greetings-step-6",
  ]);

  await mockStateApi(page, createState({
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 5 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));

  await openCourse(page);
  await openLesson(page, lesson);
  await expect(page.locator(".course-stepper")).toContainText("Шаг 6 из 6");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Частые ошибки");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 7");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const practices = buildReinforcementPractices(lesson);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  await expect(translationTask.getByText("Переведите реплики формального диалога.")).toBeVisible();
  await expect(translationTask.locator("input")).toHaveCount(4);
  for (const [index, pair] of (practices[4].pairs ?? []).entries()) {
    await translationTask.locator(".course-pair-row").nth(index).locator("input").fill(pair.answer);
  }
  await translationTask.getByRole("button", { name: "Проверить" }).click();
  await expect(translationTask.locator(".course-pair-row.correct")).toHaveCount(4);

  const dialogueTask = page.locator(".course-reinforcement fieldset").nth(5);
  await expect(dialogueTask.getByText("Соберите диалог первой встречи.")).toBeVisible();
  const orderedTokens = [...(practices[5].tokens ?? [])].sort((left, right) => practices[5].answer.indexOf(left) - practices[5].answer.indexOf(right));
  for (const token of orderedTokens) await dialogueTask.getByRole("button", { name: token, exact: true }).click();
  await dialogueTask.getByRole("button", { name: "Проверить" }).click();
  await expect(dialogueTask).toHaveClass(/correct/);
});

test("Theme 8 follows the self-introduction source and uses a six-task final test", async ({ page }) => {
  const lesson = module1.lessons.find((item) => item.slug === "introductions");
  if (!lesson) throw new Error("Introductions lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "intro-step-6");
  if (!lastPractice) throw new Error("Theme 8 step 6 practice is missing");
  expect(lesson.sections.map((section) => section.title)).toEqual([
    "Имя и знакомство",
    "Откуда вы и где живёте",
    "Занятие и статус",
    "Языки и возраст",
    "Готовая самопрезентация",
    "Частые ошибки",
  ]);
  expect(lesson.stepPractices.map((practice) => practice.id)).toEqual([
    "intro-step-1",
    "intro-step-2",
    "intro-step-3",
    "intro-step-4",
    "intro-step-5",
    "intro-step-6",
  ]);

  await mockStateApi(page, createState({
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 5 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));

  await openCourse(page);
  await openLesson(page, lesson);
  await expect(page.locator(".course-stepper")).toContainText("Шаг 6 из 6");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Частые ошибки");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 8");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const insertionTask = page.locator(".course-reinforcement fieldset").nth(1);
  await expect(insertionTask.getByText("Вставьте недостающую часть каждой модели.")).toBeVisible();
  await expect(insertionTask.locator("input")).toHaveCount(0);

  const practices = buildReinforcementPractices(lesson);
  const insertionPairs = practices[1].pairs ?? [];
  for (const [index, pair] of insertionPairs.entries()) {
    const row = insertionTask.locator(".course-pair-row").nth(index);
    const selected = index === 0 ? pair.options?.find((option) => option !== pair.answer) : pair.answer;
    if (!selected) throw new Error(`Theme 8 pair ${index + 1} has no selectable answer`);
    await row.getByRole("button", { name: selected, exact: true }).click();
  }
  await insertionTask.getByRole("button", { name: "Проверить" }).click();
  await expect(insertionTask.locator(".course-pair-row.incorrect")).toHaveCount(1);
  await expect(insertionTask.locator(".course-pair-row").first()).toContainText("Правильно: sa");

  await insertionTask.locator(".course-pair-row").first().getByRole("button", { name: "sa", exact: true }).click();
  await insertionTask.getByRole("button", { name: "Проверить" }).click();
  await expect(insertionTask.locator(".course-pair-row.correct")).toHaveCount(4);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  await expect(translationTask.locator("input")).toHaveCount(4);
});

test("Theme 9 follows the communication-repair source and uses a six-task final test", async ({ page }) => {
  const lesson = module1.lessons.find((item) => item.slug === "communication-repair");
  if (!lesson) throw new Error("Communication-repair lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m1-communication-repair-step-5");
  if (!lastPractice) throw new Error("Theme 9 step 5 practice is missing");
  expect(lesson.sections.map((section) => section.title)).toEqual([
    "Скажите, что не поняли",
    "Попросите помочь с пониманием",
    "Уточните слово или информацию",
    "Готовые мини-диалоги",
    "Частые ошибки",
  ]);
  expect(lesson.stepPractices.map((practice) => practice.id)).toEqual([
    "m1-communication-repair-step-1",
    "m1-communication-repair-step-2",
    "m1-communication-repair-step-3",
    "m1-communication-repair-step-4",
    "m1-communication-repair-step-5",
  ]);

  await mockStateApi(page, createState({
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));

  await openCourse(page);
  await openLesson(page, lesson);
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Частые ошибки");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 9");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const practices = buildReinforcementPractices(lesson);
  const insertionTask = page.locator(".course-reinforcement fieldset").nth(1);
  await expect(insertionTask.getByText("Вставьте недостающие слова.")).toBeVisible();
  await expect(insertionTask.locator("input")).toHaveCount(3);
  const insertionPairs = practices[1].pairs ?? [];
  for (const [index, pair] of insertionPairs.entries()) {
    await insertionTask.locator(".course-pair-row").nth(index).locator("input").fill(index === 0 ? "zopakovat" : pair.answer);
  }
  await insertionTask.getByRole("button", { name: "Проверить" }).click();
  await expect(insertionTask.locator(".course-pair-row.incorrect")).toHaveCount(1);
  await expect(insertionTask.locator(".course-pair-row").first()).toContainText("Правильно: zopakovať");

  await insertionTask.locator(".course-pair-row").first().locator("input").fill("zopakovať");
  await insertionTask.getByRole("button", { name: "Проверить" }).click();
  await expect(insertionTask.locator(".course-pair-row.correct")).toHaveCount(3);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  await expect(translationTask.locator("input")).toHaveCount(3);
  const dialogueTask = page.locator(".course-reinforcement fieldset").nth(5);
  const orderedTokens = [...(practices[5].tokens ?? [])].sort((left, right) => practices[5].answer.indexOf(left) - practices[5].answer.indexOf(right));
  for (const token of orderedTokens) await dialogueTask.getByRole("button", { name: token, exact: true }).click();
  await dialogueTask.getByRole("button", { name: "Проверить" }).click();
  await expect(dialogueTask).toHaveClass(/correct/);
});

test("Theme 10 follows the numbers source and uses a six-task final test", async ({ page }) => {
  const lesson = module1.lessons.find((item) => item.slug === "numbers");
  if (!lesson) throw new Error("Numbers lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "numbers-step-6");
  if (!lastPractice) throw new Error("Theme 10 step 6 practice is missing");
  expect(lesson.sections.map((section) => section.title)).toEqual([
    "Числа от 0 до 10",
    "От 11 до 20 и десятки",
    "Возраст и телефон",
    "Цены",
    "Банк чисел и полезных фраз",
    "Частые ошибки",
  ]);
  expect(lesson.stepPractices.map((practice) => practice.id)).toEqual([
    "numbers-step-1",
    "numbers-step-2",
    "numbers-step-3",
    "numbers-step-4",
    "numbers-step-5",
    "numbers-step-6",
  ]);

  await mockStateApi(page, createState({
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 5 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));

  await openCourse(page);
  await openLesson(page, lesson);
  await expect(page.locator(".course-stepper")).toContainText("Шаг 6 из 6");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Частые ошибки");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 10");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const practices = buildReinforcementPractices(lesson);
  const spellingTask = page.locator(".course-reinforcement fieldset").first();
  await expect(spellingTask.getByText("Запишите цифры словами.")).toBeVisible();
  await expect(spellingTask.locator("input")).toHaveCount(5);
  const spellingPairs = practices[0].pairs ?? [];
  for (const [index, pair] of spellingPairs.entries()) {
    await spellingTask.locator(".course-pair-row").nth(index).locator("input").fill(index === 1 ? "styri" : pair.answer);
  }
  await spellingTask.getByRole("button", { name: "Проверить" }).click();
  await expect(spellingTask.locator(".course-pair-row.incorrect")).toHaveCount(1);
  await expect(spellingTask.locator(".course-pair-row").nth(1)).toContainText("Правильно: štyri");

  await spellingTask.locator(".course-pair-row").nth(1).locator("input").fill("štyri");
  await spellingTask.getByRole("button", { name: "Проверить" }).click();
  await expect(spellingTask.locator(".course-pair-row.correct")).toHaveCount(5);

  const digitsTask = page.locator(".course-reinforcement fieldset").nth(3);
  await expect(digitsTask.locator("input")).toHaveCount(5);
  await expect(digitsTask.locator(".course-slovak-keyboard")).toHaveCount(0);
  const situationsTask = page.locator(".course-reinforcement fieldset").nth(5);
  await expect(situationsTask.locator("input")).toHaveCount(0);
  for (const [index, pair] of (practices[5].pairs ?? []).entries()) {
    await situationsTask.locator(".course-pair-row").nth(index).getByRole("button", { name: pair.answer, exact: true }).click();
  }
  await situationsTask.getByRole("button", { name: "Проверить" }).click();
  await expect(situationsTask.locator(".course-pair-row.correct")).toHaveCount(3);
});

test("Module 2 opens as three topic groups and keeps the expanded lessons", async ({ page }) => {
  await mockStateApi(page, createState());
  await openCourse(page);

  await page.getByLabel("Выберите учебный модуль").selectOption("2");
  await expect(page.getByRole("heading", { name: module2.title })).toBeVisible();
  await expect(page.locator(".course-group-card")).toHaveCount(3);
  await expect(page.getByText("Род существительных", { exact: true })).toBeVisible();
  await expect(page.getByText("Число и словарная форма", { exact: true })).toBeVisible();
  await expect(page.getByText("Называние и наличие", { exact: true })).toBeVisible();

  await page.locator(".course-group-card").filter({ hasText: "Род существительных" }).click();
  await expect(page.locator(".course-topic-grid .course-topic-card")).toHaveCount(3);
  await page.getByRole("button", { name: new RegExp(module2.lessons[0].title) }).first().click();
  await expect(page.locator(".course-material-heading h3")).toHaveText(module2.lessons[0].title);
  await expect(page.locator(".course-practice")).toBeVisible();
  const personObjectRows = page.locator(".course-practice .course-pair-row");
  await expect(personObjectRows).toHaveCount(4);
  const columnPositions: number[][] = [];
  for (const index of [0, 1, 2, 3]) {
    const row = personObjectRows.nth(index);
    await expect(row.getByRole("button")).toHaveText(["človek", "predmet"]);
    columnPositions.push(await row.getByRole("button").evaluateAll((buttons) => buttons.map((button) => Math.round(button.getBoundingClientRect().x))));
  }
  expect(columnPositions.every((positions) => positions.length === 2 && positions.every((position, index) => position === columnPositions[0][index]))).toBe(true);
});

test("Module 2 theme 2 keeps feminine and masculine prompts in fixed columns", async ({ page }) => {
  await mockStateApi(page, createState());
  await openCourse(page);

  await page.getByLabel("Выберите учебный модуль").selectOption("2");
  await page.locator(".course-group-card").filter({ hasText: "Род существительных" }).click();
  await page.getByRole("button", { name: /Женский род существительных/ }).first().click();

  const rows = page.locator(".course-practice .course-pair-row");
  const expectedColumns = [["tá žena", "ten žena"], ["tá kolega", "ten kolega"], ["tá noc", "ten noc"], ["tá dom", "ten dom"]];
  await expect(rows).toHaveCount(expectedColumns.length);
  const columnPositions: number[][] = [];
  for (const [index, columns] of expectedColumns.entries()) {
    const row = rows.nth(index);
    await expect(row.getByRole("button")).toHaveText(columns);
    columnPositions.push(await row.getByRole("button").evaluateAll((buttons) => buttons.map((button) => Math.round(button.getBoundingClientRect().x))));
  }
  expect(columnPositions.every((positions) => positions.length === 2 && positions.every((position, index) => position === columnPositions[0][index]))).toBe(true);
});

test("Module 2 theme 1 follows the PDF route and checks its six-task final row by row", async ({ page }) => {
  const lesson = module2.lessons.find((item) => item.slug === "masculine-nouns");
  if (!lesson) throw new Error("Masculine nouns lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m2-masculine-nouns-step-5");
  if (!lastPractice) throw new Error("Module 2 theme 1 step 5 practice is missing");
  await mockStateApi(page, createState({
    activeModule: 2,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));

  const restored = page.waitForResponse((response) =>
    response.url().includes("/api/v1/course/state") && response.request().method() === "GET",
  );
  await page.goto("/");
  await restored;
  await expect(page.getByRole("heading", { name: module2.title })).toBeVisible();
  await page.locator(".course-group-card").filter({ hasText: "Род существительных" }).click();
  await page.getByRole("button", { name: new RegExp(lesson.title) }).first().click();

  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Частые ошибки");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 1");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const correctionTask = page.locator(".course-reinforcement fieldset").nth(3);
  const rows = correctionTask.locator(".course-pair-row");
  await expect(rows).toHaveCount(4);
  const checkButton = correctionTask.getByRole("button", { name: "Проверить" });
  await expect(checkButton).toBeDisabled();
  await rows.nth(0).getByRole("textbox").fill("Tí dobrí učitelia sú tu");
  await rows.nth(1).getByRole("textbox").fill("Tie nový domy sú veľké.");
  await rows.nth(2).getByRole("textbox").fill("Dvaja študenti sú z Bratislavy.");
  await rows.nth(3).getByRole("textbox").fill("Vidím toho nového kolegu.");
  await expect(checkButton).toBeEnabled();
  await checkButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(3);
  await expect(rows.nth(1)).toHaveClass(/incorrect/);
  await expect(rows.nth(1)).toContainText("Правильно: Tie nové domy sú veľké.");
  await rows.nth(1).getByRole("textbox").fill("Tie nové domy sú veľké.");
  await checkButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(4);
});

test("Module 2 theme 2 follows the PDF route and checks feminine agreement row by row", async ({ page }) => {
  const lesson = module2.lessons.find((item) => item.slug === "feminine-nouns");
  if (!lesson) throw new Error("Feminine nouns lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m2-feminine-nouns-step-5");
  if (!lastPractice) throw new Error("Module 2 theme 2 step 5 practice is missing");
  await mockStateApi(page, createState({
    activeModule: 2,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));

  const restored = page.waitForResponse((response) =>
    response.url().includes("/api/v1/course/state") && response.request().method() === "GET",
  );
  await page.goto("/");
  await restored;
  await expect(page.getByRole("heading", { name: module2.title })).toBeVisible();
  await page.locator(".course-group-card").filter({ hasText: "Род существительных" }).click();
  await page.getByRole("button", { name: new RegExp(lesson.title) }).first().click();

  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Частые ошибки");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 2");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const demonstrativeTask = page.locator(".course-reinforcement fieldset").first();
  const demonstrativeRows = demonstrativeTask.locator(".course-pair-row");
  await expect(demonstrativeRows).toHaveCount(5);
  const demonstrativeColumns: number[][] = [];
  for (const index of [0, 1, 2, 3, 4]) {
    const row = demonstrativeRows.nth(index);
    await expect(row.getByRole("button")).toHaveText(["tá", "tie"]);
    demonstrativeColumns.push(await row.getByRole("button").evaluateAll((buttons) => buttons.map((button) => Math.round(button.getBoundingClientRect().x))));
  }
  expect(demonstrativeColumns.every((positions) => positions.length === 2 && positions.every((position, index) => position === demonstrativeColumns[0][index]))).toBe(true);
  const adjectiveTask = page.locator(".course-reinforcement fieldset").nth(2);
  const adjectiveRows = adjectiveTask.locator(".course-pair-row");
  const adjectiveColumns = [["nová", "nové", "nový"], ["dobrá", "dobré", "dobrí"], ["malá", "malé", "malí"], ["dlhá", "dlhé", "dlhí"], ["nová", "nové", "nový"]];
  await expect(adjectiveRows).toHaveCount(adjectiveColumns.length);
  const adjectivePositions: number[][] = [];
  for (const [index, columns] of adjectiveColumns.entries()) {
    const row = adjectiveRows.nth(index);
    await expect(row.getByRole("button")).toHaveText(columns);
    adjectivePositions.push(await row.getByRole("button").evaluateAll((buttons) => buttons.map((button) => Math.round(button.getBoundingClientRect().x))));
  }
  expect(adjectivePositions.every((positions) => positions.length === 3 && positions.every((position, index) => position === adjectivePositions[0][index]))).toBe(true);
  const correctionTask = page.locator(".course-reinforcement fieldset").nth(3);
  const rows = correctionTask.locator(".course-pair-row");
  await expect(rows).toHaveCount(4);
  const checkButton = correctionTask.getByRole("button", { name: "Проверить" });
  await expect(checkButton).toBeDisabled();
  await rows.nth(0).getByRole("textbox").fill("Tá škola je veľká");
  await rows.nth(1).getByRole("textbox").fill("Tie nová knihy sú tu.");
  await rows.nth(2).getByRole("textbox").fill("Dve ženy sú učiteľky.");
  await rows.nth(3).getByRole("textbox").fill("Vidím tú novú ulicu.");
  await expect(checkButton).toBeEnabled();
  await checkButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(3);
  await expect(rows.nth(1)).toHaveClass(/incorrect/);
  await expect(rows.nth(1)).toContainText("Правильно: Tie nové knihy sú tu.");
  await rows.nth(1).getByRole("textbox").fill("Tie nové knihy sú tu.");
  await checkButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(4);
});

test("Module 2 theme 3 keeps adjective options in fixed form columns", () => {
  const lesson = module2.lessons.find((item) => item.slug === "neuter-nouns");
  const practice = lesson?.reinforcementPractices?.[2];
  expect(practice?.pairs?.map((pair) => pair.options)).toEqual([
    ["nová", "nové", "nový"], ["pekná", "pekné", "pekní"], ["veľká", "veľké", "veľký"], ["slovenská", "slovenské", "slovenskí"], ["malá", "malé", "malý"],
  ]);
});

test("Module 2 theme 3 follows the PDF route and checks neuter agreement row by row", async ({ page }) => {
  const lesson = module2.lessons.find((item) => item.slug === "neuter-nouns");
  if (!lesson) throw new Error("Neuter nouns lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m2-neuter-nouns-step-5");
  if (!lastPractice) throw new Error("Module 2 theme 3 step 5 practice is missing");
  await mockStateApi(page, createState({
    activeModule: 2,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));

  const restored = page.waitForResponse((response) =>
    response.url().includes("/api/v1/course/state") && response.request().method() === "GET",
  );
  await page.goto("/");
  await restored;
  await expect(page.getByRole("heading", { name: module2.title })).toBeVisible();
  await page.locator(".course-group-card").filter({ hasText: "Род существительных" }).click();
  await page.getByRole("button", { name: new RegExp(lesson.title) }).first().click();

  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Частые ошибки");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 3");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const correctionTask = page.locator(".course-reinforcement fieldset").nth(3);
  const rows = correctionTask.locator(".course-pair-row");
  await expect(rows).toHaveCount(4);
  const checkButton = correctionTask.getByRole("button", { name: "Проверить" });
  await expect(checkButton).toBeDisabled();
  await rows.nth(0).getByRole("textbox").fill("To auto je nové");
  await rows.nth(1).getByRole("textbox").fill("To pekná mesto je malé.");
  await rows.nth(2).getByRole("textbox").fill("Dve okná sú otvorené.");
  await rows.nth(3).getByRole("textbox").fill("Tie nové srdcia sú zdravé.");
  await expect(checkButton).toBeEnabled();
  await checkButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(3);
  await expect(rows.nth(1)).toHaveClass(/incorrect/);
  await expect(rows.nth(1)).toContainText("Правильно: To pekné mesto je malé.");
  await rows.nth(1).getByRole("textbox").fill("To pekné mesto je malé.");
  await checkButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(4);
});

test("Module 2 theme 4 follows the PDF route and checks number agreement row by row", async ({ page }) => {
  const lesson = module2.lessons.find((item) => item.slug === "noun-number");
  if (!lesson) throw new Error("Noun number lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m2-noun-number-step-5");
  if (!lastPractice) throw new Error("Module 2 theme 4 step 5 practice is missing");
  await mockStateApi(page, createState({
    activeModule: 2,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));

  const restored = page.waitForResponse((response) =>
    response.url().includes("/api/v1/course/state") && response.request().method() === "GET",
  );
  await page.goto("/");
  await restored;
  await expect(page.getByRole("heading", { name: module2.title })).toBeVisible();
  await page.locator(".course-group-card").filter({ hasText: "Число и словарная форма" }).click();
  await page.getByRole("button", { name: new RegExp(lesson.title) }).first().click();

  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 4");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const correctionTask = page.locator(".course-reinforcement fieldset").nth(4);
  const rows = correctionTask.locator(".course-pair-row");
  await expect(rows).toHaveCount(4);
  const checkButton = correctionTask.getByRole("button", { name: "Проверить" });
  await expect(checkButton).toBeDisabled();
  await rows.nth(0).getByRole("textbox").fill("Tí dobrí študenti sú tu");
  await rows.nth(1).getByRole("textbox").fill("Tí nové domy sú veľké.");
  await rows.nth(2).getByRole("textbox").fill("Dve ženy majú tri knihy.");
  await rows.nth(3).getByRole("textbox").fill("Dve autá sú nové.");
  await expect(checkButton).toBeEnabled();
  await checkButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(3);
  await expect(rows.nth(1)).toHaveClass(/incorrect/);
  await expect(rows.nth(1)).toContainText("Правильно: Tie nové domy sú veľké.");
  await rows.nth(1).getByRole("textbox").fill("Tie nové domy sú veľké.");
  await checkButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(4);
});

test("Module 2 theme 5 follows the PDF route and checks noun endings row by row", async ({ page }) => {
  const lesson = module2.lessons.find((item) => item.slug === "noun-endings");
  if (!lesson) throw new Error("Noun endings lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m2-noun-endings-step-5");
  if (!lastPractice) throw new Error("Module 2 theme 5 step 5 practice is missing");
  await mockStateApi(page, createState({
    activeModule: 2,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));

  const restored = page.waitForResponse((response) =>
    response.url().includes("/api/v1/course/state") && response.request().method() === "GET",
  );
  await page.goto("/");
  await restored;
  await expect(page.getByRole("heading", { name: module2.title })).toBeVisible();
  await page.locator(".course-group-card").filter({ hasText: "Число и словарная форма" }).click();
  await page.getByRole("button", { name: new RegExp(lesson.title) }).first().click();

  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 5");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const correctionTask = page.locator(".course-reinforcement fieldset").nth(4);
  const rows = correctionTask.locator(".course-pair-row");
  await expect(rows).toHaveCount(5);
  const checkButton = correctionTask.getByRole("button", { name: "Проверить" });
  await expect(checkButton).toBeDisabled();
  await rows.nth(0).getByRole("textbox").fill("Vidím ženu");
  await rows.nth(1).getByRole("textbox").fill("Som v hoteli.");
  await rows.nth(2).getByRole("textbox").fill("Idem do mesto.");
  await rows.nth(3).getByRole("textbox").fill("Hovorím o učiteľovi.");
  await rows.nth(4).getByRole("textbox").fill("Idem s kamarátom.");
  await expect(checkButton).toBeEnabled();
  await checkButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(rows.nth(2)).toHaveClass(/incorrect/);
  await expect(rows.nth(2)).toContainText("Правильно: Idem do mesta.");
  await rows.nth(2).getByRole("textbox").fill("Idem do mesta.");
  await checkButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(5);
});

test("Module 2 theme 6 follows the PDF route and checks full answers row by row", async ({ page }) => {
  const lesson = module2.lessons.find((item) => item.slug === "who-what-is-it");
  if (!lesson) throw new Error("Who what is it lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m2-who-what-is-it-step-5");
  if (!lastPractice) throw new Error("Module 2 theme 6 step 5 practice is missing");
  await mockStateApi(page, createState({
    activeModule: 2,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));

  const restored = page.waitForResponse((response) =>
    response.url().includes("/api/v1/course/state") && response.request().method() === "GET",
  );
  await page.goto("/");
  await restored;
  await expect(page.getByRole("heading", { name: module2.title })).toBeVisible();
  await page.locator(".course-group-card").filter({ hasText: "Называние и наличие" }).click();
  await page.getByRole("button", { name: /Кто это\? Что это\?/ }).first().click();

  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 6");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const questionWordTask = page.locator(".course-reinforcement fieldset").nth(0);
  const verbTask = page.locator(".course-reinforcement fieldset").nth(1);
  expect(await questionWordTask.locator(".course-pair-options").evaluateAll((groups) => groups.map((group) => Array.from(group.querySelectorAll("button"), (button) => button.textContent)))).toEqual(Array(5).fill(["Kto", "Čo"]));
  expect(await verbTask.locator(".course-pair-options").evaluateAll((groups) => groups.map((group) => Array.from(group.querySelectorAll("button"), (button) => button.textContent)))).toEqual(Array(5).fill(["je", "sú"]));
  const answerTask = page.locator(".course-reinforcement fieldset").nth(2);
  const rows = answerTask.locator(".course-pair-row");
  await expect(rows).toHaveCount(4);
  const checkButton = answerTask.getByRole("button", { name: "Проверить" });
  await expect(checkButton).toBeDisabled();
  await rows.nth(0).getByRole("textbox").fill("To je moja učiteľka");
  await rows.nth(1).getByRole("textbox").fill("To sú slovník.");
  await rows.nth(2).getByRole("textbox").fill("To sú študenti.");
  await rows.nth(3).getByRole("textbox").fill("To sú kľúče.");
  await expect(checkButton).toBeEnabled();
  await checkButton.click();
  await expect(answerTask.locator(".course-pair-row.correct")).toHaveCount(3);
  await expect(rows.nth(1)).toHaveClass(/incorrect/);
  await expect(rows.nth(1)).toContainText("Правильно: To je slovník.");
  await rows.nth(1).getByRole("textbox").fill("To je slovník.");
  await checkButton.click();
  await expect(answerTask.locator(".course-pair-row.correct")).toHaveCount(4);
});

test("Module 2 theme 7 follows the PDF route and checks presence forms row by row", async ({ page }) => {
  const lesson = module2.lessons.find((item) => item.slug === "presence-absence");
  if (!lesson) throw new Error("Presence absence lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m2-presence-absence-step-5");
  if (!lastPractice) throw new Error("Module 2 theme 7 step 5 practice is missing");
  await mockStateApi(page, createState({
    activeModule: 2,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));

  const restored = page.waitForResponse((response) =>
    response.url().includes("/api/v1/course/state") && response.request().method() === "GET",
  );
  await page.goto("/");
  await restored;
  await expect(page.getByRole("heading", { name: module2.title })).toBeVisible();
  await page.locator(".course-group-card").filter({ hasText: "Называние и наличие" }).click();
  await page.getByRole("button", { name: new RegExp(lesson.title) }).first().click();

  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 7");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const correctionTask = page.locator(".course-reinforcement fieldset").nth(4);
  const rows = correctionTask.locator(".course-pair-row");
  await expect(rows).toHaveCount(5);
  const checkButton = correctionTask.getByRole("button", { name: "Проверить" });
  await expect(checkButton).toBeDisabled();
  await rows.nth(0).getByRole("textbox").fill("Na stole sú dve knihy");
  await rows.nth(1).getByRole("textbox").fill("V izbe nie sú posteľ.");
  await rows.nth(2).getByRole("textbox").fill("Peter nie je v práci.");
  await rows.nth(3).getByRole("textbox").fill("V škole nie je učiteľ.");
  await rows.nth(4).getByRole("textbox").fill("Mám nový telefón.");
  await expect(checkButton).toBeEnabled();
  await checkButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(rows.nth(1)).toHaveClass(/incorrect/);
  await expect(rows.nth(1)).toContainText("Правильно: V izbe nie je posteľ.");
  await rows.nth(1).getByRole("textbox").fill("V izbe nie je posteľ.");
  await checkButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(5);
});

test("saved Module 2 lesson and progress are restored from the shared state", async ({ page }) => {
  const lesson = module2.lessons[3];
  await mockStateApi(page, createState({
    activeModule: 2,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 1 },
  }));

  const restored = page.waitForResponse((response) =>
    response.url().includes("/api/v1/course/state") && response.request().method() === "GET",
  );
  await page.goto("/");
  await restored;

  await expect(page.getByRole("heading", { name: module2.title })).toBeVisible();
  await expect(page.getByLabel("Выберите учебный модуль")).toHaveValue("2");
  const group = module2.topicGroups?.find((item) => item.lessonSlugs.includes(lesson.slug));
  if (!group) throw new Error(`Lesson ${lesson.slug} is not assigned to a Module 2 topic group`);
  await page.locator(".course-group-card").filter({ hasText: group.title }).click();
  await expect(page.getByRole("button", { name: new RegExp(lesson.title) }).first()).toContainText("В процессе");
});

test("Module 3 theme 1 follows the PDF route and checks adjective gender row by row", async ({ page }) => {
  const lesson = module3.lessons.find((item) => item.slug === "adjective-gender");
  if (!lesson) throw new Error("Adjective gender lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m3-adjective-gender-step-5");
  if (!lastPractice) throw new Error("Module 3 theme 1 step 5 practice is missing");
  await mockStateApi(page, createState({
    activeModule: 3,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));

  const restored = page.waitForResponse((response) =>
    response.url().includes("/api/v1/course/state") && response.request().method() === "GET",
  );
  await page.goto("/");
  await restored;
  await expect(page.getByRole("heading", { name: module3.title })).toBeVisible();
  await page.locator(".course-group-card").filter({ hasText: "Согласование" }).click();
  await page.getByRole("button", { name: new RegExp(lesson.title) }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 1");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const correctionTask = page.locator(".course-reinforcement fieldset").nth(2);
  const rows = correctionTask.locator(".course-pair-row");
  await expect(rows).toHaveCount(5);
  const checkButton = correctionTask.getByRole("button", { name: "Проверить" });
  await expect(checkButton).toBeDisabled();
  await rows.nth(0).getByRole("textbox").fill("Nová kniha.");
  await rows.nth(1).getByRole("textbox").fill("malý park");
  await rows.nth(2).getByRole("textbox").fill("dobré jedlo");
  await rows.nth(3).getByRole("textbox").fill("stará žena");
  await expect(checkButton).toBeDisabled();
  await rows.nth(4).getByRole("textbox").fill("pekná námestie");
  await checkButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(rows.nth(4)).toHaveClass(/incorrect/);
  await expect(rows.nth(4)).toContainText("Правильно: pekné námestie");
  await rows.nth(4).getByRole("textbox").fill("pekne namestie");
  await checkButton.click();
  await expect(rows.nth(4)).toHaveClass(/incorrect/);
  await rows.nth(4).getByRole("textbox").fill("pekné námestie");
  await checkButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(5);

  for (const [index, practice] of buildReinforcementPractices(lesson).entries()) {
    if (index === 2) continue;
    const task = page.locator(".course-reinforcement fieldset").nth(index);
    for (const [rowIndex, pair] of (practice.pairs ?? []).entries()) {
      const row = task.locator(".course-pair-row").nth(rowIndex);
      if (pair.options?.length) await row.getByRole("button", { name: pair.answer, exact: true }).click();
      else await row.getByRole("textbox").fill(pair.answer);
    }
    await task.getByRole("button", { name: "Проверить", exact: true }).click();
    await expect(task).toHaveClass(/correct/);
  }
  await expect(page.locator(".course-reinforcement fieldset.correct")).toHaveCount(6);
});

test("Module 3 theme 2 checks plural groups, soft endings and singular question contrast", async ({ page }) => {
  const lesson = module3.lessons.find((item) => item.slug === "adjective-plural");
  if (!lesson) throw new Error("Adjective plural lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m3-adjective-plural-step-5");
  if (!lastPractice) throw new Error("Module 3 theme 2 step 5 practice is missing");
  await mockStateApi(page, createState({
    activeModule: 3,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));

  const restored = page.waitForResponse((response) =>
    response.url().includes("/api/v1/course/state") && response.request().method() === "GET",
  );
  await page.goto("/");
  await restored;
  await page.locator(".course-group-card").filter({ hasText: "Согласование" }).click();
  await page.getByRole("button", { name: new RegExp(lesson.title) }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();
  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 2");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);

  const correctionTask = page.locator(".course-reinforcement fieldset").nth(2);
  const rows = correctionTask.locator(".course-pair-row");
  await expect(rows).toHaveCount(5);
  const checkButton = correctionTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(checkButton).toBeDisabled();
  await rows.nth(0).getByRole("textbox").fill("Dobrí muži.");
  await rows.nth(1).getByRole("textbox").fill("nové autá");
  await rows.nth(2).getByRole("textbox").fill("pekné ulice");
  await rows.nth(3).getByRole("textbox").fill("veľké okná");
  await expect(checkButton).toBeDisabled();
  await rows.nth(4).getByRole("textbox").fill("cudzé slová");
  await checkButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(rows.nth(4)).toContainText("Правильно: cudzie slová");
  await rows.nth(4).getByRole("textbox").fill("cudzie slova");
  await checkButton.click();
  await expect(rows.nth(4)).toHaveClass(/incorrect/);
  await rows.nth(4).getByRole("textbox").fill("cudzie slová");
  await checkButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(5);

  const questionTask = page.locator(".course-reinforcement fieldset").nth(3);
  const questionAnswers = ["Akí sú učitelia?", "Aké sú domy?", "Aké sú auto?", "Aké sú ženy?"];
  for (const [index, answer] of questionAnswers.entries()) {
    await questionTask.locator(".course-pair-row").nth(index).getByRole("button", { name: answer, exact: true }).click();
  }
  await questionTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(questionTask.locator(".course-pair-row.correct")).toHaveCount(3);
  await expect(questionTask.locator(".course-pair-row").nth(2)).toContainText("Правильно: Aké je auto?");

  for (const [index, practice] of buildReinforcementPractices(lesson).entries()) {
    if (index === 2) continue;
    const task = page.locator(".course-reinforcement fieldset").nth(index);
    for (const [rowIndex, pair] of (practice.pairs ?? []).entries()) {
      const row = task.locator(".course-pair-row").nth(rowIndex);
      if (pair.options?.length) await row.getByRole("button", { name: pair.answer, exact: true }).click();
      else await row.getByRole("textbox").fill(pair.answer);
    }
    await task.getByRole("button", { name: "Проверить", exact: true }).click();
    await expect(task).toHaveClass(/correct/);
  }
  await expect(page.locator(".course-reinforcement fieldset.correct")).toHaveCount(6);
});

test("Module 3 theme 3 checks demonstratives, possessive forms and unchanged jej", async ({ page }) => {
  const lesson = module3.lessons.find((item) => item.slug === "demonstratives-possessives");
  if (!lesson) throw new Error("Demonstratives possessives lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m3-demonstratives-possessives-step-5");
  if (!lastPractice) throw new Error("Module 3 theme 3 step 5 practice is missing");
  await mockStateApi(page, createState({
    activeModule: 3,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));

  const restored = page.waitForResponse((response) =>
    response.url().includes("/api/v1/course/state") && response.request().method() === "GET",
  );
  await page.goto("/");
  await restored;
  await page.locator(".course-group-card").filter({ hasText: "Указание и описание" }).click();
  await page.getByRole("button", { name: new RegExp(lesson.title) }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Порядок слов и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();
  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 3");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);

  const correctionTask = page.locator(".course-reinforcement fieldset").nth(3);
  const rows = correctionTask.locator(".course-pair-row");
  await expect(rows).toHaveCount(5);
  const checkButton = correctionTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(checkButton).toBeDisabled();
  await rows.nth(0).getByRole("textbox").fill("Tá žena.");
  await rows.nth(1).getByRole("textbox").fill("tí chlapci");
  await rows.nth(2).getByRole("textbox").fill("tvoje auto");
  await rows.nth(3).getByRole("textbox").fill("naše knihy");
  await expect(checkButton).toBeDisabled();
  await rows.nth(4).getByRole("textbox").fill("jeje rodina");
  await checkButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(rows.nth(4)).toHaveClass(/incorrect/);
  await expect(rows.nth(4)).toContainText("Правильно: jej rodina");
  await rows.nth(4).getByRole("textbox").fill("jej rodina");
  await checkButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(5);

  const possessiveTask = page.locator(".course-reinforcement fieldset").nth(1);
  for (const [index, answer] of ["moj", "moja", "moje", "mojí", "moje"].entries()) {
    await possessiveTask.locator(".course-pair-row").nth(index).getByRole("textbox").fill(answer);
  }
  await possessiveTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(possessiveTask.locator(".course-pair-row.correct")).toHaveCount(3);
  await expect(possessiveTask.locator(".course-pair-row").nth(0)).toContainText("Правильно: môj");
  await expect(possessiveTask.locator(".course-pair-row").nth(3)).toContainText("Правильно: moji");

  for (const [index, practice] of buildReinforcementPractices(lesson).entries()) {
    if (index === 3) continue;
    const task = page.locator(".course-reinforcement fieldset").nth(index);
    for (const [rowIndex, pair] of (practice.pairs ?? []).entries()) {
      const row = task.locator(".course-pair-row").nth(rowIndex);
      if (pair.options?.length) await row.getByRole("button", { name: pair.answer, exact: true }).click();
      else await row.getByRole("textbox").fill(pair.answer);
    }
    await task.getByRole("button", { name: "Проверить", exact: true }).click();
    await expect(task).toHaveClass(/correct/);
  }
  await expect(page.locator(".course-reinforcement fieldset.correct")).toHaveCount(6);
});

test("Module 3 theme 4 checks descriptions, adjective order and colour endings", async ({ page }) => {
  const lesson = module3.lessons.find((item) => item.slug === "basic-description");
  if (!lesson) throw new Error("Basic description lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m3-basic-description-step-5");
  if (!lastPractice) throw new Error("Module 3 theme 4 step 5 practice is missing");
  await mockStateApi(page, createState({
    activeModule: 3,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));

  const restored = page.waitForResponse((response) =>
    response.url().includes("/api/v1/course/state") && response.request().method() === "GET",
  );
  await page.goto("/");
  await restored;
  await page.locator(".course-group-card").filter({ hasText: "Указание и описание" }).click();
  await page.getByRole("button", { name: new RegExp(lesson.title) }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Несколько признаков");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();
  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 4");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const rows = translationTask.locator(".course-pair-row");
  await expect(rows).toHaveCount(5);
  const checkButton = translationTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(checkButton).toBeDisabled();
  await rows.nth(0).getByRole("textbox").fill("Biely veľký dom.");
  await rows.nth(1).getByRole("textbox").fill("červená malá taška");
  await rows.nth(2).getByRole("textbox").fill("modré nové auto");
  await rows.nth(3).getByRole("textbox").fill("mladé učitelia");
  await expect(checkButton).toBeDisabled();
  await rows.nth(4).getByRole("textbox").fill("stará zaujímavá kniha");
  await checkButton.click();
  await expect(translationTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(rows.nth(3)).toHaveClass(/incorrect/);
  await expect(rows.nth(3)).toContainText("Правильно: mladí učitelia");
  await rows.nth(3).getByRole("textbox").fill("mladi ucitelia");
  await checkButton.click();
  await expect(rows.nth(3)).toHaveClass(/incorrect/);
  await rows.nth(3).getByRole("textbox").fill("mladí učitelia");
  await checkButton.click();
  await expect(translationTask.locator(".course-pair-row.correct")).toHaveCount(5);

  const formsTask = page.locator(".course-reinforcement fieldset").nth(1);
  for (const [index, answer] of ["bielá", "vysoká", "nové", "pekné", "mladí"].entries()) {
    await formsTask.locator(".course-pair-row").nth(index).getByRole("textbox").fill(answer);
  }
  await formsTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(formsTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(formsTask.locator(".course-pair-row").first()).toContainText("Правильно: biela");

  for (const [index, practice] of buildReinforcementPractices(lesson).entries()) {
    if (index === 4) continue;
    const task = page.locator(".course-reinforcement fieldset").nth(index);
    for (const [rowIndex, pair] of (practice.pairs ?? []).entries()) {
      const row = task.locator(".course-pair-row").nth(rowIndex);
      if (pair.options?.length) await row.getByRole("button", { name: pair.answer, exact: true }).click();
      else await row.getByRole("textbox").fill(pair.answer);
    }
    await task.getByRole("button", { name: "Проверить", exact: true }).click();
    await expect(task).toHaveClass(/correct/);
  }
  await expect(page.locator(".course-reinforcement fieldset.correct")).toHaveCount(6);
});

test("Module 3 theme 5 checks contrast, negative agreement and comma placement", async ({ page }) => {
  const lesson = module3.lessons.find((item) => item.slug === "choice-contrast");
  if (!lesson) throw new Error("Choice contrast lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m3-choice-contrast-step-5");
  if (!lastPractice) throw new Error("Module 3 theme 5 step 5 practice is missing");
  await mockStateApi(page, createState({
    activeModule: 3,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));

  const restored = page.waitForResponse((response) =>
    response.url().includes("/api/v1/course/state") && response.request().method() === "GET",
  );
  await page.goto("/");
  await restored;
  await page.locator(".course-group-card").filter({ hasText: "Выбор и связная фраза" }).click();
  await page.getByRole("button", { name: new RegExp(lesson.title) }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Выбираем смысл и проверяем форму");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();
  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 5");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);

  const correctionTask = page.locator(".course-reinforcement fieldset").nth(2);
  const rows = correctionTask.locator(".course-pair-row");
  await expect(rows).toHaveCount(4);
  const checkButton = correctionTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(checkButton).toBeDisabled();
  await rows.nth(0).getByRole("textbox").fill("Izba je malá, ale čistá");
  await rows.nth(1).getByRole("textbox").fill("Auto nie je nové, ale je staré.");
  await rows.nth(2).getByRole("textbox").fill("Knihy nie je drahé.");
  await expect(checkButton).toBeDisabled();
  await rows.nth(3).getByRole("button", { name: "запятая не нужна", exact: true }).click();
  await checkButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(2);
  await expect(rows.nth(2)).toHaveClass(/incorrect/);
  await expect(rows.nth(2)).toContainText("Правильно: Knihy nie sú drahé.");
  await expect(rows.nth(3)).toHaveClass(/incorrect/);
  await expect(rows.nth(3)).toContainText("Правильно: перед ale");
  await rows.nth(2).getByRole("textbox").fill("Knihy nie su drahe.");
  await rows.nth(3).getByRole("button", { name: "перед ale", exact: true }).click();
  await checkButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(3);
  await expect(rows.nth(2)).toHaveClass(/incorrect/);
  await rows.nth(2).getByRole("textbox").fill("Knihy nie sú drahé.");
  await checkButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(4);

  for (const [index, practice] of buildReinforcementPractices(lesson).entries()) {
    if (index === 2) continue;
    const task = page.locator(".course-reinforcement fieldset").nth(index);
    for (const [rowIndex, pair] of (practice.pairs ?? []).entries()) {
      const row = task.locator(".course-pair-row").nth(rowIndex);
      if (pair.options?.length) await row.getByRole("button", { name: pair.answer, exact: true }).click();
      else await row.getByRole("textbox").fill(pair.acceptableAnswers?.[0] ?? pair.answer);
    }
    await task.getByRole("button", { name: "Проверить", exact: true }).click();
    await expect(task).toHaveClass(/correct/);
  }
  await expect(page.locator(".course-reinforcement fieldset.correct")).toHaveCount(6);
});

test("Module 3 theme 6 checks aj focus, punctuation and connected daily stories", async ({ page }) => {
  const lesson = module3.lessons.find((item) => item.slug === "basic-connectors");
  if (!lesson) throw new Error("Basic connectors lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m3-basic-connectors-step-5");
  if (!lastPractice) throw new Error("Module 3 theme 6 step 5 practice is missing");
  await mockStateApi(page, createState({
    activeModule: 3,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));

  const restored = page.waitForResponse((response) =>
    response.url().includes("/api/v1/course/state") && response.request().method() === "GET",
  );
  await page.goto("/");
  await restored;
  await page.locator(".course-group-card").filter({ hasText: "Выбор и связная фраза" }).click();
  await page.getByRole("button", { name: new RegExp(lesson.title) }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("От отдельных фраз к короткому рассказу");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();
  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 6");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);

  const focusTask = page.locator(".course-reinforcement fieldset").nth(1);
  const rows = focusTask.locator(".course-pair-row");
  await expect(rows).toHaveCount(3);
  const checkButton = focusTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(checkButton).toBeDisabled();
  await rows.nth(0).getByRole("textbox").fill("aj Peter ide");
  await rows.nth(1).getByRole("textbox").fill("Aj mám knihu.");
  await expect(checkButton).toBeDisabled();
  await rows.nth(2).getByRole("textbox").fill("Aj pracujem, aj študujem.");
  await checkButton.click();
  await expect(focusTask.locator(".course-pair-row.correct")).toHaveCount(2);
  await expect(rows.nth(1)).toHaveClass(/incorrect/);
  await expect(rows.nth(1)).toContainText("Правильно: Mám aj knihu.");
  await rows.nth(1).getByRole("textbox").fill("Mam aj knihu.");
  await checkButton.click();
  await expect(rows.nth(1)).toHaveClass(/incorrect/);
  await rows.nth(1).getByRole("textbox").fill("Mám aj knihu.");
  await checkButton.click();
  await expect(focusTask.locator(".course-pair-row.correct")).toHaveCount(3);

  const correctionTask = page.locator(".course-reinforcement fieldset").nth(2);
  const correctionRows = correctionTask.locator(".course-pair-row");
  await correctionRows.nth(1).getByRole("textbox").fill("Mám aj sestru.");
  await correctionRows.nth(2).getByRole("textbox").fill("Mám aj čaj, aj kávu.");
  await expect(correctionTask.getByRole("button", { name: "Проверить", exact: true })).toBeDisabled();
  await correctionRows.nth(0).getByRole("button", { name: "после ale", exact: true }).click();
  await correctionTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(2);
  await expect(correctionRows.nth(0)).toContainText("Правильно: перед ale");

  for (const [index, practice] of buildReinforcementPractices(lesson).entries()) {
    if (index === 1) continue;
    const task = page.locator(".course-reinforcement fieldset").nth(index);
    for (const [rowIndex, pair] of (practice.pairs ?? []).entries()) {
      const row = task.locator(".course-pair-row").nth(rowIndex);
      if (pair.options?.length) await row.getByRole("button", { name: pair.answer, exact: true }).click();
      else await row.getByRole("textbox").fill(pair.answer);
    }
    await task.getByRole("button", { name: "Проверить", exact: true }).click();
    await expect(task).toHaveClass(/correct/);
  }
  await expect(page.locator(".course-reinforcement fieldset.correct")).toHaveCount(6);
});

test("Module 3 opens as three topic groups and restores saved progress", async ({ page }) => {
  const lesson = module3.lessons[2];
  await mockStateApi(page, createState({
    activeModule: 3,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 1 },
  }));

  const restored = page.waitForResponse((response) =>
    response.url().includes("/api/v1/course/state") && response.request().method() === "GET",
  );
  await page.goto("/");
  await restored;

  await expect(page.getByRole("heading", { name: module3.title })).toBeVisible();
  await expect(page.getByLabel("Выберите учебный модуль")).toHaveValue("3");
  await expect(page.locator(".course-group-card")).toHaveCount(3);
  await expect(page.getByText("Согласование", { exact: true })).toBeVisible();
  await expect(page.getByText("Указание и описание", { exact: true })).toBeVisible();
  await expect(page.getByText("Выбор и связная фраза", { exact: true })).toBeVisible();

  const group = module3.topicGroups?.find((item) => item.lessonSlugs.includes(lesson.slug));
  if (!group) throw new Error(`Lesson ${lesson.slug} is not assigned to a Module 3 topic group`);
  await page.locator(".course-group-card").filter({ hasText: group.title }).click();
  const lessonButton = page.getByRole("button", { name: new RegExp(lesson.title) }).first();
  await expect(lessonButton).toContainText("В процессе");
  await lessonButton.click();
  await expect(page.locator(".course-material-heading h3")).toHaveText(lesson.title);
  await expect(page.locator(".course-practice")).toBeVisible();
});

test("Module 4 theme 1 follows the Nominatív source and checks corrections row by row", async ({ page }) => {
  const lesson = module4.lessons.find((item) => item.slug === "nominative");
  if (!lesson) throw new Error("Nominative lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m4-nominative-step-5");
  if (!lastPractice) throw new Error("Module 4 theme 1 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("ten študent — tí študenti");
  expect(JSON.stringify(lesson)).toContain("To je okno, где to вводит название");

  await mockStateApi(page, createState({
    activeModule: 4,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Субъект и прямой объект" }).click();
  await page.getByRole("button", { name: new RegExp(lesson.title) }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 1");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const correctionTask = page.locator(".course-reinforcement fieldset").nth(3);
  const rows = correctionTask.locator(".course-pair-row");
  await expect(rows).toHaveCount(4);
  const checkButton = correctionTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(checkButton).toBeDisabled();
  await rows.nth(0).getByRole("textbox").fill("Tá taška je nová.");
  await rows.nth(1).getByRole("textbox").fill("Tie zošity sú nové.");
  await rows.nth(2).getByRole("textbox").fill("To su novi ucitelia.");
  await expect(checkButton).toBeDisabled();
  await rows.nth(3).getByRole("textbox").fill("Lucia je študentka.");
  await checkButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(3);
  await expect(rows.nth(2)).toHaveClass(/incorrect/);
  await expect(rows.nth(2)).toContainText("Правильно: To sú noví učitelia.");
  await rows.nth(2).getByRole("textbox").fill("To sú noví učitelia.");
  await checkButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(4);
});

test("Module 4 theme 2 follows the Akuzatív source and checks noun forms row by row", async ({ page }) => {
  const lesson = module4.lessons.find((item) => item.slug === "accusative-nouns");
  if (!lesson) throw new Error("Accusative nouns lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m4-accusative-nouns-step-5");
  if (!lastPractice) throw new Error("Module 4 theme 2 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("Adam číta knihu");
  expect(JSON.stringify(lesson)).toContain("kolegovia → kolegov; priatelia → priateľov");

  await mockStateApi(page, createState({
    activeModule: 4,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Субъект и прямой объект" }).click();
  await page.getByRole("button", { name: new RegExp(lesson.title) }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 2");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const formTask = page.locator(".course-reinforcement fieldset").nth(0);
  const optionPositions = await formTask.locator(".course-pair-row").evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(optionPositions.every((positions) => positions.length === 2 && positions.every((position, index) => position === optionPositions[0][index]))).toBe(true);

  const correctionTask = page.locator(".course-reinforcement fieldset").nth(3);
  const rows = correctionTask.locator(".course-pair-row");
  await expect(rows).toHaveCount(4);
  const checkButton = correctionTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(checkButton).toBeDisabled();
  await rows.nth(0).getByRole("textbox").fill("Čítam knihu.");
  await rows.nth(1).getByRole("textbox").fill("Vidím auto.");
  await rows.nth(2).getByRole("textbox").fill("Nemam tasku.");
  await expect(checkButton).toBeDisabled();
  await rows.nth(3).getByRole("textbox").fill("Poznám kolegov.");
  await checkButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(3);
  await expect(rows.nth(2)).toHaveClass(/incorrect/);
  await expect(rows.nth(2)).toContainText("Правильно: Nemám tašku.");
  await rows.nth(2).getByRole("textbox").fill("Nemám tašku.");
  await checkButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(4);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  await translationRows.nth(0).getByRole("textbox").fill("Ja hľadám učiteľa.");
  await translationRows.nth(1).getByRole("textbox").fill("Kupujem jablká.");
  await translationRows.nth(2).getByRole("textbox").fill("Nemám knihu.");
  await translationRows.nth(3).getByRole("textbox").fill("Nevidím deti.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 4 theme 3 follows the agreement source and checks pronouns row by row", async ({ page }) => {
  const lesson = module4.lessons.find((item) => item.slug === "accusative-agreement");
  if (!lesson) throw new Error("Accusative agreement lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m4-accusative-agreement-step-5");
  if (!lastPractice) throw new Error("Module 4 theme 3 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("tá nová taška → tú novú tašku");
  expect(JSON.stringify(lesson)).toContain("Ju заменяет женщину");

  await mockStateApi(page, createState({
    activeModule: 4,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Субъект и прямой объект" }).click();
  await page.getByRole("button", { name: new RegExp(lesson.title) }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 3");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const formTask = page.locator(".course-reinforcement fieldset").nth(0);
  const optionPositions = await formTask.locator(".course-pair-row").evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(optionPositions.every((positions) => positions.length === 2 && positions.every((position, index) => position === optionPositions[0][index]))).toBe(true);

  const correctionTask = page.locator(".course-reinforcement fieldset").nth(3);
  const correctionRows = correctionTask.locator(".course-pair-row");
  await expect(correctionRows).toHaveCount(3);
  const correctionButton = correctionTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(correctionButton).toBeDisabled();
  await correctionRows.nth(0).getByRole("textbox").fill("Čakám naňho.");
  await correctionRows.nth(1).getByRole("textbox").fill("Ho dnes vidím.");
  await expect(correctionButton).toBeDisabled();
  await correctionRows.nth(2).getByRole("textbox").fill("Poznám ju.");
  await correctionButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(2);
  await expect(correctionRows.nth(1)).toHaveClass(/incorrect/);
  await expect(correctionRows.nth(1)).toContainText("Правильно: Dnes ho vidím.");
  await correctionRows.nth(1).getByRole("textbox").fill("Dnes ho vidím.");
  await correctionButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(3);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  await translationRows.nth(0).getByRole("textbox").fill("Poznas moju sestru?");
  await translationRows.nth(1).getByRole("textbox").fill("Vidím tvojho brata.");
  await translationRows.nth(2).getByRole("textbox").fill("Dnes ich nevidím.");
  await translationRows.nth(3).getByRole("textbox").fill("Čakám na ňu.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask.locator(".course-pair-row.correct")).toHaveCount(3);
  await expect(translationRows.nth(0)).toHaveClass(/incorrect/);
  await expect(translationRows.nth(0)).toContainText("Правильно: Poznáš moju sestru?");
  await translationRows.nth(0).getByRole("textbox").fill("Poznáš moju sestru?");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask.locator(".course-pair-row.correct")).toHaveCount(4);
});

test("Module 4 theme 4 follows the Lokál source and checks location forms row by row", async ({ page }) => {
  const lesson = module4.lessons.find((item) => item.slug === "locative-v-na");
  if (!lesson) throw new Error("Locative v/na lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m4-locative-v-na-step-5");
  if (!lastPractice) throw new Error("Module 4 theme 4 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("Som na pošte — Kde? + Lokál");
  expect(JSON.stringify(lesson)).toContain("v obchodoch, v školách, na uliciach");

  await mockStateApi(page, createState({
    activeModule: 4,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Место и направление" }).click();
  await page.getByRole("button", { name: new RegExp(lesson.title) }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 4");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const prepositionTask = page.locator(".course-reinforcement fieldset").nth(0);
  const optionPositions = await prepositionTask.locator(".course-pair-row").evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(optionPositions.every((positions) => positions.length === 3 && positions.every((position, index) => position === optionPositions[0][index]))).toBe(true);

  const correctionTask = page.locator(".course-reinforcement fieldset").nth(3);
  const correctionRows = correctionTask.locator(".course-pair-row");
  await expect(correctionRows).toHaveCount(4);
  const correctionButton = correctionTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(correctionButton).toBeDisabled();
  await correctionRows.nth(0).getByRole("textbox").fill("Som na poste.");
  await correctionRows.nth(1).getByRole("textbox").fill("Kľúče sú na stole.");
  await correctionRows.nth(2).getByRole("textbox").fill("Sedím vo vlaku.");
  await expect(correctionButton).toBeDisabled();
  await correctionRows.nth(3).getByRole("textbox").fill("Bývam v Bratislave.");
  await correctionButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(3);
  await expect(correctionRows.nth(0)).toHaveClass(/incorrect/);
  await expect(correctionRows.nth(0)).toContainText("Правильно: Som na pošte.");
  await correctionRows.nth(0).getByRole("textbox").fill("Som na pošte.");
  await correctionButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(4);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  await translationRows.nth(0).getByRole("textbox").fill("Ja pracujem v obchode.");
  await translationRows.nth(1).getByRole("textbox").fill("Sme na námestí.");
  await translationRows.nth(2).getByRole("textbox").fill("Telefón je v aute.");
  await translationRows.nth(3).getByRole("textbox").fill("Priatelia bývajú v Košiciach.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 4 theme 5 follows the quantity source and checks Genitív forms row by row", async ({ page }) => {
  const lesson = module4.lessons.find((item) => item.slug === "genitive-quantity");
  if (!lesson) throw new Error("Genitive quantity lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m4-genitive-quantity-step-5");
  if (!lastPractice) throw new Error("Module 4 theme 5 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("Nemám vodu —");
  expect(JSON.stringify(lesson)).toContain("dva litre vody, päť litrov vody");

  await mockStateApi(page, createState({
    activeModule: 4,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Количество и отсутствие" }).click();
  await page.getByRole("button", { name: new RegExp(lesson.title) }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 5");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const formTask = page.locator(".course-reinforcement fieldset").nth(0);
  const optionPositions = await formTask.locator(".course-pair-row").evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(optionPositions.every((positions) => positions.length === 2 && positions.every((position, index) => position === optionPositions[0][index]))).toBe(true);

  const numberTask = page.locator(".course-reinforcement fieldset").nth(3);
  const numberRows = numberTask.locator(".course-pair-row");
  await expect(numberRows).toHaveCount(6);
  const numberButton = numberTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(numberButton).toBeDisabled();
  await numberRows.nth(0).getByRole("textbox").fill("dve knihy");
  await numberRows.nth(1).getByRole("textbox").fill("pat knih");
  await numberRows.nth(2).getByRole("textbox").fill("štyri autá");
  await numberRows.nth(3).getByRole("textbox").fill("šesť áut");
  await numberRows.nth(4).getByRole("textbox").fill("dva litre vody");
  await expect(numberButton).toBeDisabled();
  await numberRows.nth(5).getByRole("textbox").fill("päť litrov vody");
  await numberButton.click();
  await expect(numberTask.locator(".course-pair-row.correct")).toHaveCount(5);
  await expect(numberRows.nth(1)).toHaveClass(/incorrect/);
  await expect(numberRows.nth(1)).toContainText("Правильно: päť kníh");
  await numberRows.nth(1).getByRole("textbox").fill("päť kníh");
  await numberButton.click();
  await expect(numberTask.locator(".course-pair-row.correct")).toHaveCount(6);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  await translationRows.nth(0).getByRole("textbox").fill("Mám málo času.");
  await translationRows.nth(1).getByRole("textbox").fill("Ja chcem trochu kávy.");
  await translationRows.nth(2).getByRole("textbox").fill("Kupujem fľašu vody.");
  await translationRows.nth(3).getByRole("textbox").fill("Mám desať eur.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 4 theme 6 follows the absence source and checks three negative models row by row", async ({ page }) => {
  const lesson = module4.lessons.find((item) => item.slug === "genitive-absence");
  if (!lesson) throw new Error("Genitive absence lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m4-genitive-absence-step-5");
  if (!lastPractice) throw new Error("Module 4 theme 6 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("Niet času. Niet vody. Niet peňazí.");
  expect(JSON.stringify(lesson)).toContain("Tu niet vody и Tu nie je voda");

  await mockStateApi(page, createState({
    activeModule: 4,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Количество и отсутствие" }).click();
  await page.getByRole("button", { name: new RegExp(lesson.title) }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 6");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const formTask = page.locator(".course-reinforcement fieldset").nth(0);
  const optionPositions = await formTask.locator(".course-pair-row").evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(optionPositions.every((positions) => positions.length === 2 && positions.every((position, index) => position === optionPositions[0][index]))).toBe(true);

  const correctionTask = page.locator(".course-reinforcement fieldset").nth(3);
  const correctionRows = correctionTask.locator(".course-pair-row");
  await expect(correctionRows).toHaveCount(4);
  const correctionButton = correctionTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(correctionButton).toBeDisabled();
  await correctionRows.nth(0).getByRole("textbox").fill("Niet času.");
  await correctionRows.nth(1).getByRole("textbox").fill("Nemám knihu.");
  await correctionRows.nth(2).getByRole("textbox").fill("Deti tu nie su.");
  await expect(correctionButton).toBeDisabled();
  await correctionRows.nth(3).getByRole("textbox").fill("Tu nie je voda.");
  await correctionButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(3);
  await expect(correctionRows.nth(2)).toHaveClass(/incorrect/);
  await expect(correctionRows.nth(2)).toContainText("Правильно: Deti tu nie sú.");
  await correctionRows.nth(2).getByRole("textbox").fill("Deti tu nie sú.");
  await correctionButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(4);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  await translationRows.nth(0).getByRole("textbox").fill("Niet cukru.");
  await translationRows.nth(1).getByRole("textbox").fill("My nemáme vodu.");
  await translationRows.nth(2).getByRole("textbox").fill("Peter nie je doma.");
  await translationRows.nth(3).getByRole("textbox").fill("Knihy tu nie sú.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 4 theme 7 follows the do source and checks direction forms row by row", async ({ page }) => {
  const lesson = module4.lessons.find((item) => item.slug === "genitive-do");
  if (!lesson) throw new Error("Genitive with do lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m4-genitive-do-step-5");
  if (!lastPractice) throw new Error("Module 4 theme 7 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("Idem domov означает");
  expect(JSON.stringify(lesson)).toContain("v Košiciach → do Košíc; v Tatrách → do Tatier.");

  await mockStateApi(page, createState({
    activeModule: 4,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Место и направление" }).click();
  await page.getByRole("button", { name: new RegExp(lesson.title) }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 7");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const formTask = page.locator(".course-reinforcement fieldset").nth(0);
  const optionPositions = await formTask.locator(".course-pair-row").evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(optionPositions.every((positions) => positions.length === 2 && positions.every((position, index) => position === optionPositions[0][index]))).toBe(true);

  const correctionTask = page.locator(".course-reinforcement fieldset").nth(3);
  const correctionRows = correctionTask.locator(".course-pair-row");
  await expect(correctionRows).toHaveCount(4);
  const correctionButton = correctionTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(correctionButton).toBeDisabled();
  await correctionRows.nth(0).getByRole("textbox").fill("Cestujem do Prahy.");
  await correctionRows.nth(1).getByRole("textbox").fill("Dávam knihu do tašky.");
  await correctionRows.nth(2).getByRole("textbox").fill("Vraciame sa do hotela.");
  await expect(correctionButton).toBeDisabled();
  await correctionRows.nth(3).getByRole("textbox").fill("Som v skole.");
  await correctionButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(3);
  await expect(correctionRows.nth(3)).toHaveClass(/incorrect/);
  await expect(correctionRows.nth(3)).toContainText("Правильно: Som v škole.");
  await correctionRows.nth(3).getByRole("textbox").fill("Som v škole.");
  await correctionButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(4);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  await translationRows.nth(0).getByRole("textbox").fill("My ideme do obchodu.");
  await translationRows.nth(1).getByRole("textbox").fill("Dávam mlieko do chladničky.");
  await translationRows.nth(2).getByRole("textbox").fill("Vraciame sa do hotela.");
  await translationRows.nth(3).getByRole("textbox").fill("Idem domov.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 4 theme 8 follows the preposition source and checks five cases row by row", async ({ page }) => {
  const lesson = module4.lessons.find((item) => item.slug === "preposition-government");
  if (!lesson) throw new Error("Preposition government lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m4-preposition-government-step-5");
  if (!lastPractice) throw new Error("Module 4 theme 8 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("Kam? → do školy (G), na poštu (A), k mame (D).");
  expect(JSON.stringify(lesson)).toContain("k lekárovi — к одному врачу; k lekárom — к врачам.");

  await mockStateApi(page, createState({
    activeModule: 4,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Управление и готовые модели" }).click();
  await page.getByRole("button", { name: new RegExp(lesson.title) }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 8");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const caseTask = page.locator(".course-reinforcement fieldset").nth(0);
  await expect(caseTask.locator(".course-pair-row")).toHaveCount(5);
  const optionPositions = await caseTask.locator(".course-pair-row").evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(optionPositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === optionPositions[0][index]))).toBe(true);

  const trioTask = page.locator(".course-reinforcement fieldset").nth(2);
  await expect(trioTask.locator(".course-pair-row")).toHaveCount(9);
  await expect(trioTask.getByRole("button", { name: "Проверить", exact: true })).toBeDisabled();

  const correctionTask = page.locator(".course-reinforcement fieldset").nth(3);
  const correctionRows = correctionTask.locator(".course-pair-row");
  await expect(correctionRows).toHaveCount(4);
  const correctionButton = correctionTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(correctionButton).toBeDisabled();
  await correctionRows.nth(0).getByRole("textbox").fill("Som v škole.");
  await correctionRows.nth(1).getByRole("textbox").fill("Káva je bez cukru.");
  await correctionRows.nth(2).getByRole("textbox").fill("Idem zo sestrou.");
  await expect(correctionButton).toBeDisabled();
  await correctionRows.nth(3).getByRole("textbox").fill("Idem k lekárovi.");
  await correctionButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(3);
  await expect(correctionRows.nth(2)).toHaveClass(/incorrect/);
  await expect(correctionRows.nth(2)).toContainText("Правильно: Idem so sestrou.");
  await correctionRows.nth(2).getByRole("textbox").fill("Idem so sestrou.");
  await correctionButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(4);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  await translationRows.nth(0).getByRole("textbox").fill("My sa vraciame z mesta.");
  await translationRows.nth(1).getByRole("textbox").fill("Darček je pre mamu.");
  await translationRows.nth(2).getByRole("textbox").fill("Hovorime o práci.");
  await translationRows.nth(3).getByRole("textbox").fill("Čakám pred domom.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask.locator(".course-pair-row.correct")).toHaveCount(3);
  await expect(translationRows.nth(2)).toHaveClass(/incorrect/);
  await expect(translationRows.nth(2)).toContainText("Правильно: Hovoríme o práci.");
  await translationRows.nth(2).getByRole("textbox").fill("Hovoríme o práci.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 4 theme 9 follows the place route source and checks spatial triples row by row", async ({ page }) => {
  const lesson = module4.lessons.find((item) => item.slug === "where-direction-origin");
  if (!lesson) throw new Error("Where direction origin lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m4-where-direction-origin-step-5");
  if (!lastPractice) throw new Error("Module 4 theme 9 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("u lekára, k lekárovi, od lekára.");
  expect(JSON.stringify(lesson)).toContain("doma → domov → z domu");

  await mockStateApi(page, createState({
    activeModule: 4,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Место и направление" }).click();
  await page.getByRole("button").filter({ hasText: lesson.title }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 9");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const questionTask = page.locator(".course-reinforcement fieldset").nth(0);
  await expect(questionTask.locator(".course-pair-row")).toHaveCount(5);
  const optionPositions = await questionTask.locator(".course-pair-row").evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(optionPositions.every((positions) => positions.length === 3 && positions.every((position, index) => position === optionPositions[0][index]))).toBe(true);

  const trioTask = page.locator(".course-reinforcement fieldset").nth(2);
  await expect(trioTask.locator(".course-pair-row")).toHaveCount(12);
  await expect(trioTask.getByRole("button", { name: "Проверить", exact: true })).toBeDisabled();

  const correctionTask = page.locator(".course-reinforcement fieldset").nth(3);
  const correctionRows = correctionTask.locator(".course-pair-row");
  await expect(correctionRows).toHaveCount(4);
  const correctionButton = correctionTask.getByRole("button", { name: "Проверить", exact: true });
  await correctionRows.nth(0).getByRole("textbox").fill("Som v hoteli.");
  await correctionRows.nth(1).getByRole("textbox").fill("Idem zo stanice.");
  await correctionRows.nth(2).getByRole("textbox").fill("Idem k mame.");
  await expect(correctionButton).toBeDisabled();
  await correctionRows.nth(3).getByRole("textbox").fill("Som domov.");
  await correctionButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(3);
  await expect(correctionRows.nth(3)).toHaveClass(/incorrect/);
  await expect(correctionRows.nth(3)).toContainText("Правильно: Som doma.");
  await correctionRows.nth(3).getByRole("textbox").fill("Som doma.");
  await correctionButton.click();
  await expect(correctionTask).toHaveClass(/correct/);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  await expect(translationRows).toHaveCount(6);
  await translationRows.nth(0).getByRole("textbox").fill("Kde si teraz?");
  await translationRows.nth(1).getByRole("textbox").fill("Ja som v centre.");
  await translationRows.nth(2).getByRole("textbox").fill("Kam ideš?");
  await translationRows.nth(3).getByRole("textbox").fill("Idem na poštu.");
  await translationRows.nth(4).getByRole("textbox").fill("Odkial ideš?");
  await translationRows.nth(5).getByRole("textbox").fill("Idem z banky.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask.locator(".course-pair-row.correct")).toHaveCount(5);
  await expect(translationRows.nth(4)).toHaveClass(/incorrect/);
  await expect(translationRows.nth(4)).toContainText("Правильно: Odkiaľ ideš?");
  await translationRows.nth(4).getByRole("textbox").fill("Odkiaľ ideš?");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 4 theme 10 follows the dative instrumental source and checks both cases row by row", async ({ page }) => {
  const lesson = module4.lessons.find((item) => item.slug === "dative-instrumental-models");
  if (!lesson) throw new Error("Dative instrumental lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m4-dative-instrumental-models-step-5");
  if (!lastPractice) throw new Error("Module 4 theme 10 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("so mnou, s tebou, s ním, s ňou");
  expect(JSON.stringify(lesson)).toContain("Dám sestre knihu");

  await mockStateApi(page, createState({
    activeModule: 4,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Управление и готовые модели" }).click();
  await page.getByRole("button").filter({ hasText: lesson.title }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 10");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const caseTask = page.locator(".course-reinforcement fieldset").nth(0);
  await expect(caseTask.locator(".course-pair-row")).toHaveCount(5);
  const optionPositions = await caseTask.locator(".course-pair-row").evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(optionPositions.every((positions) => positions.length === 2 && positions.every((position, index) => position === optionPositions[0][index]))).toBe(true);

  const pronounTask = page.locator(".course-reinforcement fieldset").nth(2);
  await expect(pronounTask.locator(".course-pair-row")).toHaveCount(5);
  await expect(pronounTask.getByRole("button", { name: "Проверить", exact: true })).toBeDisabled();

  const correctionTask = page.locator(".course-reinforcement fieldset").nth(3);
  const correctionRows = correctionTask.locator(".course-pair-row");
  await expect(correctionRows).toHaveCount(4);
  const correctionButton = correctionTask.getByRole("button", { name: "Проверить", exact: true });
  await correctionRows.nth(0).getByRole("textbox").fill("Idem k lekárovi.");
  await correctionRows.nth(1).getByRole("textbox").fill("Som so sestrou.");
  await correctionRows.nth(2).getByRole("textbox").fill("Ideme s vlakom.");
  await expect(correctionButton).toBeDisabled();
  await correctionRows.nth(3).getByRole("textbox").fill("Táto kniha sa mi páči.");
  await correctionButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(3);
  await expect(correctionRows.nth(2)).toHaveClass(/incorrect/);
  await expect(correctionRows.nth(2)).toContainText("Правильно: Ideme vlakom.");
  await correctionRows.nth(2).getByRole("textbox").fill("Ideme vlakom.");
  await correctionButton.click();
  await expect(correctionTask).toHaveClass(/correct/);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  await translationRows.nth(0).getByRole("textbox").fill("Ja pisem kamarátovi.");
  await translationRows.nth(1).getByRole("textbox").fill("Platím kartou.");
  await translationRows.nth(2).getByRole("textbox").fill("Kaviareň je za bankou.");
  await translationRows.nth(3).getByRole("textbox").fill("Páči sa mi táto hudba.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask.locator(".course-pair-row.correct")).toHaveCount(3);
  await expect(translationRows.nth(0)).toHaveClass(/incorrect/);
  await expect(translationRows.nth(0)).toContainText("Правильно: Píšem kamarátovi.");
  await translationRows.nth(0).getByRole("textbox").fill("Ja píšem kamarátovi.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 4 theme 11 follows the route source and checks directions row by row", async ({ page }) => {
  const lesson = module4.lessons.find((item) => item.slug === "simple-route");
  if (!lesson) throw new Error("Simple route lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m4-simple-route-step-5");
  if (!lastPractice) throw new Error("Module 4 theme 11 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("naľavo/napravo — где");
  expect(JSON.stringify(lesson)).toContain("doľava/doprava — куда");
  expect(JSON.stringify(lesson)).toContain("Pošta je naľavo, vedľa banky.");

  await mockStateApi(page, createState({
    activeModule: 4,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Место и направление" }).click();
  await page.getByRole("button").filter({ hasText: lesson.title }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 11");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const wordTask = page.locator(".course-reinforcement fieldset").nth(0);
  await expect(wordTask.locator(".course-pair-row")).toHaveCount(4);
  const optionPositions = await wordTask.locator(".course-pair-row").evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(optionPositions.every((positions) => positions.length === 2 && positions.every((position, index) => position === optionPositions[0][index]))).toBe(true);

  const correctionTask = page.locator(".course-reinforcement fieldset").nth(3);
  const correctionRows = correctionTask.locator(".course-pair-row");
  await expect(correctionRows).toHaveCount(4);
  const correctionButton = correctionTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(correctionButton).toBeDisabled();
  await correctionRows.nth(0).getByRole("textbox").fill("Choďte rovno.");
  await correctionRows.nth(1).getByRole("textbox").fill("Lekaren je vedľa banky.");
  await correctionRows.nth(2).getByRole("textbox").fill("Hotel je oproti pošte.");
  await expect(correctionButton).toBeDisabled();
  await correctionRows.nth(3).getByRole("textbox").fill("Kaviareň je medzi bankou a hotelom.");
  await correctionButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(3);
  await expect(correctionRows.nth(1)).toHaveClass(/incorrect/);
  await expect(correctionRows.nth(1)).toContainText("Правильно: Lekáreň je vedľa banky.");
  await correctionRows.nth(1).getByRole("textbox").fill("Lekáreň je vedľa banky.");
  await correctionButton.click();
  await expect(correctionTask).toHaveClass(/correct/);

  const sentenceTask = page.locator(".course-reinforcement fieldset").nth(2);
  const sentenceRows = sentenceTask.locator(".course-pair-row");
  await sentenceRows.nth(0).getByRole("textbox").fill("Odbočte doprava na križovatke.");
  await sentenceRows.nth(1).getByRole("textbox").fill("Potom pokračujte po tejto ulici.");
  await sentenceRows.nth(2).getByRole("textbox").fill("Vedľa banky je pošta.");
  await sentenceTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(sentenceTask).toHaveClass(/correct/);

  const routeTask = page.locator(".course-reinforcement fieldset").nth(5);
  await expect(routeTask.locator(".course-pair-row")).toHaveCount(5);
  await expect(routeTask).toContainText("Pošta je naľavo, vedľa banky.");
});

test("Module 4 opens as four topic groups and restores saved progress", async ({ page }) => {
  const lesson = module4.lessons[7];
  await mockStateApi(page, createState({ activeModule: 4, selectedSlug: lesson.slug, progress: { [lesson.slug]: "in_progress" }, lessonSteps: { [lesson.slug]: 2 } }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await expect(page.getByRole("heading", { name: module4.title })).toBeVisible();
  await expect(page.getByLabel("Выберите учебный модуль")).toHaveValue("4");
  await expect(page.locator(".course-group-card")).toHaveCount(4);
  for (const title of ["Субъект и прямой объект", "Место и направление", "Количество и отсутствие", "Управление и готовые модели"]) {
    await expect(page.getByText(title, { exact: true })).toBeVisible();
  }
  const group = module4.topicGroups?.find((item) => item.lessonSlugs.includes(lesson.slug));
  if (!group) throw new Error(`Lesson ${lesson.slug} is not assigned to a Module 4 topic group`);
  await page.locator(".course-group-card").filter({ hasText: group.title }).click();
  const lessonButton = page.getByRole("button", { name: new RegExp(lesson.title) }).first();
  await expect(lessonButton).toContainText("В процессе");
  await lessonButton.click();
  await expect(page.locator(".course-material-heading h3")).toHaveText(lesson.title);
  await expect(page.locator(".course-practice")).toBeVisible();
});

test("Module 5 theme 1 follows the present tense source and checks personal forms row by row", async ({ page }) => {
  const lesson = module5.lessons.find((item) => item.slug === "present-tense");
  if (!lesson) throw new Error("Present tense lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m5-present-tense-step-5");
  if (!lastPractice) throw new Error("Module 5 theme 1 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("robiť — robím");
  expect(JSON.stringify(lesson)).toContain("Nie som doma.");
  expect(JSON.stringify(lesson)).toContain("Dnes sa učíme doma.");

  await mockStateApi(page, createState({
    activeModule: 5,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Настоящее время" }).click();
  await page.getByRole("button").filter({ hasText: lesson.title }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Частые ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 1");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const formTask = page.locator(".course-reinforcement fieldset").nth(0);
  await expect(formTask.locator(".course-pair-row")).toHaveCount(5);
  const optionPositions = await formTask.locator(".course-pair-row").evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(optionPositions.every((positions) => positions.length === 2 && positions.every((position, index) => position === optionPositions[0][index]))).toBe(true);

  const conjugationTask = page.locator(".course-reinforcement fieldset").nth(1);
  const conjugationRows = conjugationTask.locator(".course-pair-row");
  const conjugationButton = conjugationTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(conjugationButton).toBeDisabled();
  await conjugationRows.nth(0).getByRole("textbox").fill("pracuje");
  await conjugationRows.nth(1).getByRole("textbox").fill("bývame");
  await conjugationRows.nth(2).getByRole("textbox").fill("máte");
  await conjugationRows.nth(3).getByRole("textbox").fill("hovorim");
  await expect(conjugationButton).toBeDisabled();
  await conjugationRows.nth(4).getByRole("textbox").fill("varia");
  await conjugationButton.click();
  await expect(conjugationTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(conjugationRows.nth(3)).toHaveClass(/incorrect/);
  await expect(conjugationRows.nth(3)).toContainText("Правильно: hovorím");
  await conjugationRows.nth(3).getByRole("textbox").fill("hovorím");
  await conjugationButton.click();
  await expect(conjugationTask).toHaveClass(/correct/);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  await translationRows.nth(0).getByRole("textbox").fill("Bývam v Bratislave.");
  await translationRows.nth(1).getByRole("textbox").fill("Pracujeme teraz.");
  await translationRows.nth(2).getByRole("textbox").fill("Ucis sa slovencinu?");
  await translationRows.nth(3).getByRole("textbox").fill("Nemám čas.");
  await translationRows.nth(4).getByRole("textbox").fill("Kde bývate?");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(translationRows.nth(2)).toHaveClass(/incorrect/);
  await expect(translationRows.nth(2)).toContainText("Правильно: Učíš sa slovenčinu?");
  await translationRows.nth(2).getByRole("textbox").fill("Učíš sa slovenčinu?");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 5 theme 2 follows the irregular verbs source and checks semantic contrasts row by row", async ({ page }) => {
  const lesson = module5.lessons.find((item) => item.slug === "irregular-verbs");
  if (!lesson) throw new Error("Irregular verbs lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m5-irregular-verbs-step-5");
  if (!lastPractice) throw new Error("Module 5 theme 2 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("ísť — idem — idú");
  expect(JSON.stringify(lesson)).toContain("dať — dám — dajú");
  expect(JSON.stringify(lesson)).toContain("Nemusím ísť. — Мне не нужно идти.");

  await mockStateApi(page, createState({
    activeModule: 5,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Настоящее время" }).click();
  await page.getByRole("button").filter({ hasText: lesson.title }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Частые ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 2");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const formTask = page.locator(".course-reinforcement fieldset").nth(0);
  await expect(formTask.locator(".course-pair-row")).toHaveCount(5);
  const optionPositions = await formTask.locator(".course-pair-row").evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(optionPositions.every((positions) => positions.length === 2 && positions.every((position, index) => position === optionPositions[0][index]))).toBe(true);

  const meaningTask = page.locator(".course-reinforcement fieldset").nth(2);
  await expect(meaningTask.locator(".course-pair-row")).toHaveCount(4);
  await expect(meaningTask).toContainText("Nemusím ísť.");
  await expect(meaningTask).toContainText("Nesmiem vojsť.");

  const correctionTask = page.locator(".course-reinforcement fieldset").nth(3);
  const correctionRows = correctionTask.locator(".course-pair-row");
  const correctionButton = correctionTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(correctionButton).toBeDisabled();
  await correctionRows.nth(0).getByRole("textbox").fill("Oni jedia obed.");
  await correctionRows.nth(1).getByRole("textbox").fill("Chceme ísť domov.");
  await correctionRows.nth(2).getByRole("textbox").fill("Môžem prísť dnes.");
  await correctionRows.nth(3).getByRole("textbox").fill("Dám si kávu.");
  await expect(correctionButton).toBeDisabled();
  await correctionRows.nth(4).getByRole("textbox").fill("Ty pijes vodu.");
  await correctionButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(correctionRows.nth(4)).toHaveClass(/incorrect/);
  await expect(correctionRows.nth(4)).toContainText("Правильно: Ty piješ vodu.");
  await correctionRows.nth(4).getByRole("textbox").fill("Ty piješ vodu.");
  await correctionButton.click();
  await expect(correctionTask).toHaveClass(/correct/);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  await translationRows.nth(0).getByRole("textbox").fill("Chcem piť.");
  await translationRows.nth(1).getByRole("textbox").fill("Musíme ísť.");
  await translationRows.nth(2).getByRole("textbox").fill("Vies varit?");
  await translationRows.nth(3).getByRole("textbox").fill("Oni nemôžu prísť.");
  await translationRows.nth(4).getByRole("textbox").fill("Dám si čaj.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(translationRows.nth(2)).toHaveClass(/incorrect/);
  await expect(translationRows.nth(2)).toContainText("Правильно: Vieš variť?");
  await translationRows.nth(2).getByRole("textbox").fill("Vieš variť?");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 5 theme 3 follows the sa and si source and checks clitic placement row by row", async ({ page }) => {
  const lesson = module5.lessons.find((item) => item.slug === "reflexive-sa-si");
  if (!lesson) throw new Error("Reflexive sa and si lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m5-reflexive-sa-si-step-5");
  if (!lastPractice) throw new Error("Module 5 theme 3 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("Umývam sa. — Я моюсь.");
  expect(JSON.stringify(lesson)).toContain("Umývam si ruky. — Я мою руки.");
  expect(JSON.stringify(lesson)).toContain("Chcem sa učiť.");

  await mockStateApi(page, createState({
    activeModule: 5,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Возвратность, отрицание и вопрос" }).click();
  await page.getByRole("button").filter({ hasText: lesson.title }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Частые ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 3");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const particleTask = page.locator(".course-reinforcement fieldset").nth(0);
  await expect(particleTask.locator(".course-pair-row")).toHaveCount(6);
  const optionPositions = await particleTask.locator(".course-pair-row").evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(optionPositions.every((positions) => positions.length === 2 && positions.every((position, index) => position === optionPositions[0][index]))).toBe(true);

  const orderTask = page.locator(".course-reinforcement fieldset").nth(2);
  const orderRows = orderTask.locator(".course-pair-row");
  const orderButton = orderTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(orderButton).toBeDisabled();
  await orderRows.nth(0).getByRole("textbox").fill("Dnes sa učím doma.");
  await orderRows.nth(1).getByRole("textbox").fill("Ráno si umývam zuby.");
  await orderRows.nth(2).getByRole("textbox").fill("Volám sa Ari.");
  await expect(orderButton).toBeDisabled();
  await orderRows.nth(3).getByRole("textbox").fill("Môžeme sa stretnúť zajtra?");
  await orderButton.click();
  await expect(orderTask).toHaveClass(/correct/);

  const correctionTask = page.locator(".course-reinforcement fieldset").nth(3);
  const correctionRows = correctionTask.locator(".course-pair-row");
  const correctionButton = correctionTask.getByRole("button", { name: "Проверить", exact: true });
  await correctionRows.nth(0).getByRole("textbox").fill("Dávam si kávu.");
  await correctionRows.nth(1).getByRole("textbox").fill("Učím sa slovenčinu.");
  await correctionRows.nth(2).getByRole("textbox").fill("Chcem si oddýchnuť.");
  await correctionRows.nth(3).getByRole("textbox").fill("Neučím sa dnes.");
  await expect(correctionButton).toBeDisabled();
  await correctionRows.nth(4).getByRole("textbox").fill("Umyvam si zuby.");
  await correctionButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(correctionRows.nth(4)).toHaveClass(/incorrect/);
  await expect(correctionRows.nth(4)).toContainText("Правильно: Umývam si zuby.");
  await correctionRows.nth(4).getByRole("textbox").fill("Umývam si zuby.");
  await correctionButton.click();
  await expect(correctionTask).toHaveClass(/correct/);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  await translationRows.nth(0).getByRole("textbox").fill("Volám sa Ari.");
  await translationRows.nth(1).getByRole("textbox").fill("Stretávame sa večer.");
  await translationRows.nth(2).getByRole("textbox").fill("Umývam si zuby.");
  await translationRows.nth(3).getByRole("textbox").fill("Čo si dáte?");
  await translationRows.nth(4).getByRole("textbox").fill("Chcem sa učiť slovenčinu.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 5 theme 4 follows the negation and questions source", async ({ page }) => {
  const lesson = module5.lessons.find((item) => item.slug === "verb-negation-questions");
  if (!lesson) throw new Error("Verb negation and questions lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m5-verb-negation-questions-step-5");
  if (!lastPractice) throw new Error("Module 5 theme 4 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("Nikto nepracuje.");
  expect(JSON.stringify(lesson)).toContain("Nie, nie sme.");
  expect(JSON.stringify(lesson)).toContain("Prečo sa učíš slovenčinu?");

  await mockStateApi(page, createState({
    activeModule: 5,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Возвратность, отрицание и вопрос" }).click();
  await page.getByRole("button").filter({ hasText: lesson.title }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Готовые фразы, ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 4");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const questionWordTask = page.locator(".course-reinforcement fieldset").nth(2);
  await expect(questionWordTask.locator(".course-pair-row")).toHaveCount(6);
  const optionPositions = await questionWordTask.locator(".course-pair-row").evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(optionPositions.every((positions) => positions.length === 6 && positions.every((position, index) => position === optionPositions[0][index]))).toBe(true);

  const shortAnswerTask = page.locator(".course-reinforcement fieldset").nth(3);
  await expect(shortAnswerTask).toContainText("Дайте полный ответ с глаголом.");
  const shortAnswerRows = shortAnswerTask.locator(".course-pair-row");
  const shortAnswerButton = shortAnswerTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(shortAnswerButton).toBeDisabled();
  await shortAnswerRows.nth(0).getByRole("textbox").fill("Áno, pracujem.");
  await shortAnswerRows.nth(1).getByRole("textbox").fill("Nie, nie sme.");
  await shortAnswerRows.nth(2).getByRole("textbox").fill("Nie, nemôže.");
  await expect(shortAnswerButton).toBeDisabled();
  await shortAnswerRows.nth(3).getByRole("textbox").fill("Áno, učíme sa.");
  await shortAnswerButton.click();
  await expect(shortAnswerTask).toHaveClass(/correct/);

  const correctionTask = page.locator(".course-reinforcement fieldset").nth(4);
  const correctionRows = correctionTask.locator(".course-pair-row");
  const correctionButton = correctionTask.getByRole("button", { name: "Проверить", exact: true });
  await correctionRows.nth(0).getByRole("textbox").fill("Nemám čas.");
  await correctionRows.nth(1).getByRole("textbox").fill("Nikdy nepijem kávu.");
  await correctionRows.nth(2).getByRole("textbox").fill("Preco sa ucis?");
  await correctionRows.nth(3).getByRole("textbox").fill("Nikto dnes nepracuje.");
  await correctionRows.nth(4).getByRole("textbox").fill("Kam ideš?");
  await correctionButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(correctionRows.nth(2)).toHaveClass(/incorrect/);
  await expect(correctionRows.nth(2)).toContainText("Правильно: Prečo sa učíš?");
  await correctionRows.nth(2).getByRole("textbox").fill("Prečo sa učíš?");
  await correctionButton.click();
  await expect(correctionTask).toHaveClass(/correct/);
});

test("Module 5 theme 5 follows the chciet plus infinitive source", async ({ page }) => {
  const lesson = module5.lessons.find((item) => item.slug === "chciet-infinitive");
  if (!lesson) throw new Error("Chciet plus infinitive lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m5-chciet-infinitive-step-5");
  if (!lastPractice) throw new Error("Module 5 theme 5 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("chcem, chceš, chce, chceme, chcete, chcú");
  expect(JSON.stringify(lesson)).toContain("Chcem si oddýchnuť.");
  expect(JSON.stringify(lesson)).toContain("Čo chcete robiť?");

  await mockStateApi(page, createState({
    activeModule: 5,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Желание, возможность и необходимость" }).click();
  await page.getByRole("button").filter({ hasText: lesson.title }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Готовые фразы, ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 5");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const conjugationTask = page.locator(".course-reinforcement fieldset").nth(0);
  await expect(conjugationTask.locator(".course-pair-row")).toHaveCount(6);
  const optionPositions = await conjugationTask.locator(".course-pair-row").evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(optionPositions.every((positions) => positions.length === 6 && positions.every((position, index) => position === optionPositions[0][index]))).toBe(true);

  const orderTask = page.locator(".course-reinforcement fieldset").nth(2);
  const orderRows = orderTask.locator(".course-pair-row");
  await orderRows.nth(0).getByRole("textbox").fill("Chcem dnes pracovať doma.");
  await orderRows.nth(1).getByRole("textbox").fill("Chcem sa učiť slovenčinu.");
  await orderRows.nth(2).getByRole("textbox").fill("Chcem si kúpiť lístok.");
  await orderRows.nth(3).getByRole("textbox").fill("Cez víkend nechcem pracovať.");
  await orderTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(orderTask).toHaveClass(/correct/);

  const shortAnswerTask = page.locator(".course-reinforcement fieldset").nth(3);
  const shortAnswerRows = shortAnswerTask.locator(".course-pair-row");
  const shortAnswerButton = shortAnswerTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(shortAnswerButton).toBeDisabled();
  await shortAnswerRows.nth(0).getByRole("textbox").fill("Áno, chcem.");
  await shortAnswerRows.nth(1).getByRole("textbox").fill("Áno, chceme.");
  await shortAnswerRows.nth(2).getByRole("textbox").fill("Nie, nechce.");
  await expect(shortAnswerButton).toBeDisabled();
  await shortAnswerRows.nth(3).getByRole("textbox").fill("Áno, chcem.");
  await shortAnswerButton.click();
  await expect(shortAnswerTask).toHaveClass(/correct/);

  const correctionTask = page.locator(".course-reinforcement fieldset").nth(4);
  const correctionRows = correctionTask.locator(".course-pair-row");
  const correctionButton = correctionTask.getByRole("button", { name: "Проверить", exact: true });
  await correctionRows.nth(0).getByRole("textbox").fill("Nechcem čakať.");
  await correctionRows.nth(1).getByRole("textbox").fill("Chcem si oddýchnuť.");
  await correctionRows.nth(2).getByRole("textbox").fill("Chceme cestovať.");
  await correctionRows.nth(3).getByRole("textbox").fill("Chceš ísť do kina?");
  await correctionRows.nth(4).getByRole("textbox").fill("Co chcete robit?");
  await correctionButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(correctionRows.nth(4)).toHaveClass(/incorrect/);
  await expect(correctionRows.nth(4)).toContainText("Правильно: Čo chcete robiť?");
  await correctionRows.nth(4).getByRole("textbox").fill("Čo chcete robiť?");
  await correctionButton.click();
  await expect(correctionTask).toHaveClass(/correct/);
});

test("Module 5 theme 6 follows the moct plus infinitive source", async ({ page }) => {
  const lesson = module5.lessons.find((item) => item.slug === "moct-infinitive");
  if (!lesson) throw new Error("Moct plus infinitive lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m5-moct-infinitive-step-5");
  if (!lastPractice) throw new Error("Module 5 theme 6 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("môžem, môžeš, môže, môžeme, môžete, môžu");
  expect(JSON.stringify(lesson)).toContain("Môžem sa opýtať?");
  expect(JSON.stringify(lesson)).toContain("Viem plávať.");
  expect(lesson.stepPractices.find((practice) => practice.id === "m5-moct-infinitive-step-3")?.prompt).toBe(
    "Ответьте вежливо, обращаясь к собеседнику на «вы»: Môžem otvoriť okno?",
  );
  expect(JSON.stringify(lesson.reinforcementPractices)).toContain("да, вежливо на «вы»");

  await mockStateApi(page, createState({
    activeModule: 5,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Желание, возможность и необходимость" }).click();
  await page.getByRole("button").filter({ hasText: lesson.title }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Готовые фразы, ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 6");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const conjugationTask = page.locator(".course-reinforcement fieldset").nth(0);
  await expect(conjugationTask.locator(".course-pair-row")).toHaveCount(6);
  const conjugationPositions = await conjugationTask.locator(".course-pair-row").evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(conjugationPositions.every((positions) => positions.length === 6 && positions.every((position, index) => position === conjugationPositions[0][index]))).toBe(true);

  const verbTask = page.locator(".course-reinforcement fieldset").nth(2);
  const verbRows = verbTask.locator(".course-pair-row");
  await expect(verbRows).toHaveCount(5);
  const verbPositions = await verbRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(verbPositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === verbPositions[0][index]))).toBe(true);
  for (const [index, answer] of ["môžem", "viem", "nesmiem", "vie", "nemôžem"].entries()) {
    await verbRows.nth(index).getByRole("button", { name: answer, exact: true }).click();
  }
  await verbTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(verbTask).toHaveClass(/correct/);

  const orderTask = page.locator(".course-reinforcement fieldset").nth(3);
  const orderRows = orderTask.locator(".course-pair-row");
  await orderRows.nth(0).getByRole("textbox").fill("Môžeme sa dnes stretnúť.");
  await orderRows.nth(1).getByRole("textbox").fill("Môžem si objednať čaj?");
  await orderRows.nth(2).getByRole("textbox").fill("Cez víkend nemôžu prísť.");
  await orderRows.nth(3).getByRole("textbox").fill("Kedy môžete začať?");
  await orderTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(orderTask).toHaveClass(/correct/);

  const responseTask = page.locator(".course-reinforcement fieldset").nth(4);
  await expect(responseTask).toContainText("Дайте полный ответ на вопросы или переведите предложения.");
  await expect(responseTask.getByPlaceholder("Введите полный ответ")).toHaveCount(2);
  const responseRows = responseTask.locator(".course-pair-row");
  const responseButton = responseTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(responseButton).toBeDisabled();
  await responseRows.nth(0).getByRole("textbox").fill("Áno, môžete.");
  await responseRows.nth(1).getByRole("textbox").fill("Nie, nemôže.");
  await responseRows.nth(2).getByRole("textbox").fill("Nemôžeme čakať.");
  await responseRows.nth(3).getByRole("textbox").fill("Môžete mi pomôcť?");
  await expect(responseButton).toBeDisabled();
  await responseRows.nth(4).getByRole("textbox").fill("Kedy mozes prist?");
  await responseButton.click();
  await expect(responseTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(responseRows.nth(4)).toHaveClass(/incorrect/);
  await expect(responseRows.nth(4)).toContainText("Правильно: Kedy môžeš prísť?");
  await responseRows.nth(4).getByRole("textbox").fill("Kedy môžeš prísť?");
  await responseButton.click();
  await expect(responseTask).toHaveClass(/correct/);
});

test("Module 5 theme 7 follows the musiet plus infinitive source", async ({ page }) => {
  const lesson = module5.lessons.find((item) => item.slug === "musiet-infinitive");
  if (!lesson) throw new Error("Musiet plus infinitive lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m5-musiet-infinitive-step-5");
  if (!lastPractice) throw new Error("Module 5 theme 7 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("musím, musíš, musí, musíme, musíte, musia");
  expect(JSON.stringify(lesson)).toContain("Nemusíš tu čakať.");
  expect(JSON.stringify(lesson)).toContain("Nesmiete tu parkovať.");

  await mockStateApi(page, createState({
    activeModule: 5,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Желание, возможность и необходимость" }).click();
  await page.getByRole("button").filter({ hasText: lesson.title }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Готовые фразы, ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 7");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const conjugationTask = page.locator(".course-reinforcement fieldset").nth(0);
  await expect(conjugationTask.locator(".course-pair-row")).toHaveCount(6);
  const conjugationPositions = await conjugationTask.locator(".course-pair-row").evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(conjugationPositions.every((positions) => positions.length === 6 && positions.every((position, index) => position === conjugationPositions[0][index]))).toBe(true);

  const modalTask = page.locator(".course-reinforcement fieldset").nth(2);
  const modalRows = modalTask.locator(".course-pair-row");
  const modalPositions = await modalRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(modalPositions.every((positions) => positions.length === 4 && positions.every((position, index) => position === modalPositions[0][index]))).toBe(true);
  for (const [index, answer] of ["musím", "chcem", "môžem", "musíme", "môžem"].entries()) {
    await modalRows.nth(index).getByRole("button", { name: answer, exact: true }).click();
  }
  await modalTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(modalTask).toHaveClass(/correct/);

  const obligationTask = page.locator(".course-reinforcement fieldset").nth(3);
  const obligationRows = obligationTask.locator(".course-pair-row");
  const obligationPositions = await obligationRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(obligationPositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === obligationPositions[0][index]))).toBe(true);
  for (const [index, answer] of ["nemusím", "nesmiete", "nemusia", "nesmiete"].entries()) {
    await obligationRows.nth(index).getByRole("button", { name: answer, exact: true }).click();
  }
  await obligationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(obligationTask).toHaveClass(/correct/);

  const responseTask = page.locator(".course-reinforcement fieldset").nth(4);
  const responseRows = responseTask.locator(".course-pair-row");
  const responseButton = responseTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(responseButton).toBeDisabled();
  await responseRows.nth(0).getByRole("textbox").fill("Áno, musím.");
  await responseRows.nth(1).getByRole("textbox").fill("Nie, nemusíme.");
  await responseRows.nth(2).getByRole("textbox").fill("Musíme kúpiť lístky.");
  await responseRows.nth(3).getByRole("textbox").fill("Nesmiete tu fajčiť.");
  await expect(responseButton).toBeDisabled();
  await responseRows.nth(4).getByRole("textbox").fill("Kedy musite prist?");
  await responseButton.click();
  await expect(responseTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(responseRows.nth(4)).toHaveClass(/incorrect/);
  await expect(responseRows.nth(4)).toContainText("Правильно: Kedy musíte prísť?");
  await responseRows.nth(4).getByRole("textbox").fill("Kedy musíte prísť?");
  await responseButton.click();
  await expect(responseTask).toHaveClass(/correct/);
});

test("Module 5 theme 8 follows the vediet plus infinitive source", async ({ page }) => {
  const lesson = module5.lessons.find((item) => item.slug === "vediet-infinitive");
  if (!lesson) throw new Error("Vediet plus infinitive lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m5-vediet-infinitive-step-5");
  if (!lastPractice) throw new Error("Module 5 theme 8 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("viem, vieš, vie, vieme, viete, vedia");
  expect(JSON.stringify(lesson)).toContain("Ešte neviem šoférovať.");
  expect(JSON.stringify(lesson)).toContain("Dnes nemôžem plávať.");

  await mockStateApi(page, createState({
    activeModule: 5,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Желание, возможность и необходимость" }).click();
  await page.getByRole("button").filter({ hasText: lesson.title }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Готовые фразы, ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 8");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const conjugationTask = page.locator(".course-reinforcement fieldset").nth(0);
  await expect(conjugationTask.locator(".course-pair-row")).toHaveCount(6);
  const conjugationPositions = await conjugationTask.locator(".course-pair-row").evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(conjugationPositions.every((positions) => positions.length === 6 && positions.every((position, index) => position === conjugationPositions[0][index]))).toBe(true);

  const modalTask = page.locator(".course-reinforcement fieldset").nth(2);
  const modalRows = modalTask.locator(".course-pair-row");
  const modalPositions = await modalRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(modalPositions.every((positions) => positions.length === 4 && positions.every((position, index) => position === modalPositions[0][index]))).toBe(true);
  for (const [index, answer] of ["viem", "môžem", "môžem", "vie", "nemôžem"].entries()) {
    await modalRows.nth(index).getByRole("button", { name: answer, exact: true }).click();
  }
  await modalTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(modalTask).toHaveClass(/correct/);

  const wordOrderTask = page.locator(".course-reinforcement fieldset").nth(3);
  const wordOrderRows = wordOrderTask.locator(".course-pair-row");
  for (const [index, answer] of ["Viem sa predstaviť.", "Vieš si objednať jedlo?", "Ešte dobre nevieme písať.", "Ako dobre viete hovoriť po slovensky?"].entries()) {
    await wordOrderRows.nth(index).getByRole("textbox").fill(answer);
  }
  await wordOrderTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(wordOrderTask).toHaveClass(/correct/);

  const responseTask = page.locator(".course-reinforcement fieldset").nth(4);
  const responseRows = responseTask.locator(".course-pair-row");
  const responseButton = responseTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(responseButton).toBeDisabled();
  await responseRows.nth(0).getByRole("textbox").fill("Áno, viem.");
  await responseRows.nth(1).getByRole("textbox").fill("Nie, nevieme.");
  await responseRows.nth(2).getByRole("textbox").fill("On nevie šoférovať.");
  await responseRows.nth(3).getByRole("textbox").fill("Už vieme čítať po slovensky.");
  await expect(responseButton).toBeDisabled();
  await responseRows.nth(4).getByRole("textbox").fill("Co vies uvarit?");
  await responseButton.click();
  await expect(responseTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(responseRows.nth(4)).toHaveClass(/incorrect/);
  await expect(responseRows.nth(4)).toContainText("Правильно: Čo vieš uvariť?");
  await responseRows.nth(4).getByRole("textbox").fill("Čo vieš uvariť?");
  await responseButton.click();
  await expect(responseTask).toHaveClass(/correct/);
});

test("Module 5 theme 9 follows the modal questions and negation source", async ({ page }) => {
  const lesson = module5.lessons.find((item) => item.slug === "modal-questions-negation");
  if (!lesson) throw new Error("Modal questions and negation lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m5-modal-questions-negation-step-5");
  if (!lastPractice) throw new Error("Module 5 theme 9 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("nechcem, nemôžem, nemusím, neviem");
  expect(JSON.stringify(lesson)).toContain("Kedy sa môžeme stretnúť?");
  expect(JSON.stringify(lesson)).toContain("Nesmiete tu parkovať.");

  await mockStateApi(page, createState({
    activeModule: 5,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Желание, возможность и необходимость" }).click();
  await page.getByRole("button").filter({ hasText: lesson.title }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Готовые вопросы, ошибки и диалог");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 9");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const modalTask = page.locator(".course-reinforcement fieldset").nth(0);
  const modalRows = modalTask.locator(".course-pair-row");
  await expect(modalRows).toHaveCount(6);
  const modalPositions = await modalRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(modalPositions.every((positions) => positions.length === 6 && positions.every((position, index) => position === modalPositions[0][index]))).toBe(true);
  for (const [index, answer] of ["chcem", "môžem", "musím", "viem", "nesmiete", "nemusím"].entries()) {
    await modalRows.nth(index).getByRole("button", { name: answer, exact: true }).click();
  }
  await modalTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(modalTask).toHaveClass(/correct/);

  const questionTask = page.locator(".course-reinforcement fieldset").nth(2);
  const questionRows = questionTask.locator(".course-pair-row");
  const questionPositions = await questionRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(questionPositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === questionPositions[0][index]))).toBe(true);
  for (const [index, answer] of ["Čo", "Kedy", "Prečo", "Kto", "Koľko"].entries()) {
    await questionRows.nth(index).getByRole("button", { name: answer, exact: true }).click();
  }
  await questionTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(questionTask).toHaveClass(/correct/);

  const negationTask = page.locator(".course-reinforcement fieldset").nth(3);
  const negationRows = negationTask.locator(".course-pair-row");
  const negationButton = negationTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(negationButton).toBeDisabled();
  for (const [index, answer] of ["Nechcem pracovať.", "Nemôžem prísť.", "Nemusím čakať.", "Neviem šoférovať."].entries()) {
    await negationRows.nth(index).getByRole("textbox").fill(answer);
  }
  await expect(negationButton).toBeDisabled();
  await negationRows.nth(4).getByRole("textbox").fill("Nesmiete tu parkovať.");
  await negationButton.click();
  await expect(negationTask).toHaveClass(/correct/);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  const translationButton = translationTask.getByRole("button", { name: "Проверить", exact: true });
  for (const [index, answer] of ["Chceš kávu?", "Kedy sa môžeme stretnúť?", "Dnes nemusím pracovať.", "Nemôžem prísť."].entries()) {
    await translationRows.nth(index).getByRole("textbox").fill(answer);
  }
  await translationRows.nth(4).getByRole("textbox").fill("Vies sa predstavit?");
  await translationButton.click();
  await expect(translationTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(translationRows.nth(4)).toHaveClass(/incorrect/);
  await expect(translationRows.nth(4)).toContainText("Правильно: Vieš sa predstaviť?");
  await translationRows.nth(4).getByRole("textbox").fill("Vieš sa predstaviť?");
  await translationButton.click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 5 theme 10 follows the polite requests source", async ({ page }) => {
  const lesson = module5.lessons.find((item) => item.slug === "polite-requests");
  if (!lesson) throw new Error("Polite requests lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m5-polite-requests-step-5");
  if (!lastPractice) throw new Error("Module 5 theme 10 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("chcel by som");
  expect(JSON.stringify(lesson)).toContain("chcela by som");
  expect(JSON.stringify(lesson)).toContain("Mohli by ste to zopakovať?");

  await mockStateApi(page, createState({
    activeModule: 5,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Просьбы и инструкции" }).click();
  await page.getByRole("button").filter({ hasText: lesson.title }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Готовые фразы, ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 10");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const genderTask = page.locator(".course-reinforcement fieldset").nth(0);
  const genderRows = genderTask.locator(".course-pair-row");
  await expect(genderRows).toHaveCount(6);
  const genderPositions = await genderRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(genderPositions.every((positions) => positions.length === 2 && positions.every((position, index) => position === genderPositions[0][index]))).toBe(true);
  for (const [index, answer] of ["chcel", "chcela", "chcel", "chcela", "chcel", "chcela"].entries()) {
    await genderRows.nth(index).getByRole("button", { name: answer, exact: true }).click();
  }
  await genderTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(genderTask).toHaveClass(/correct/);

  const orderTask = page.locator(".course-reinforcement fieldset").nth(3);
  const orderRows = orderTask.locator(".course-pair-row");
  const orderButton = orderTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(orderButton).toBeDisabled();
  for (const [index, answer] of ["Chcel by som sa opýtať.", "Chcela by som si objednať obed.", "Chcel by som účet, prosím.", "Dnes by som chcela zaplatiť."].entries()) {
    await orderRows.nth(index).getByRole("textbox").fill(answer);
  }
  await orderButton.click();
  await expect(orderTask).toHaveClass(/correct/);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  const translationButton = translationTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(translationButton).toBeDisabled();
  for (const [index, answer] of ["Chcel by som kávu.", "Chcela by som rezervovať izbu.", "Chcel by som sa opýtať.", "Chcela by som si kúpiť lístok."].entries()) {
    await translationRows.nth(index).getByRole("textbox").fill(answer);
  }
  await translationRows.nth(4).getByRole("textbox").fill("Mohli by ste to zopakovat?");
  await translationButton.click();
  await expect(translationTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(translationRows.nth(4)).toHaveClass(/incorrect/);
  await expect(translationRows.nth(4)).toContainText("Правильно: Mohli by ste to zopakovať?");
  await translationRows.nth(4).getByRole("textbox").fill("Mohli by ste to zopakovať?");
  await translationButton.click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 5 theme 11 follows the basic imperative source", async ({ page }) => {
  const lesson = module5.lessons.find((item) => item.slug === "basic-imperative");
  if (!lesson) throw new Error("Basic imperative lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m5-basic-imperative-step-5");
  if (!lastPractice) throw new Error("Module 5 theme 11 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("choď, príď, buď, vezmi");
  expect(JSON.stringify(lesson)).toContain("Nechoď tam.");
  expect(JSON.stringify(lesson)).toContain("Nakoniec skontrolujte odpovede.");

  await mockStateApi(page, createState({
    activeModule: 5,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Просьбы и инструкции" }).click();
  await page.getByRole("button").filter({ hasText: lesson.title }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Последовательность, ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 11");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const recipientTask = page.locator(".course-reinforcement fieldset").nth(0);
  const recipientRows = recipientTask.locator(".course-pair-row");
  await expect(recipientRows).toHaveCount(6);
  const recipientPositions = await recipientRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(recipientPositions.every((positions) => positions.length === 2 && positions.every((position, index) => position === recipientPositions[0][index]))).toBe(true);
  for (const [index, answer] of ["Počkaj", "Povedzte", "Čítajte", "Nechoď", "Sadnite si", "Zavolaj"].entries()) {
    await recipientRows.nth(index).getByRole("button", { name: answer, exact: true }).click();
  }
  await recipientTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(recipientTask).toHaveClass(/correct/);

  const orderTask = page.locator(".course-reinforcement fieldset").nth(3);
  const orderRows = orderTask.locator(".course-pair-row");
  const orderButton = orderTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(orderButton).toBeDisabled();
  for (const [index, answer] of ["Prosím, sadnite si.", "Pozrite sa sem.", "Daj si vodu.", "Nebojte sa."].entries()) {
    await orderRows.nth(index).getByRole("textbox").fill(answer);
  }
  await orderButton.click();
  await expect(orderTask).toHaveClass(/correct/);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  const translationButton = translationTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(translationButton).toBeDisabled();
  await translationRows.nth(0).getByRole("textbox").fill("Choďte rovno.");
  await translationRows.nth(1).getByRole("textbox").fill("Napíšte svoje meno.");
  await translationRows.nth(2).getByRole("textbox").fill("Neotvorte okno.");
  await translationRows.nth(3).getByRole("textbox").fill("Pockajte chvilu, prosim.");
  await translationRows.nth(4).getByRole("textbox").fill("Pozrite sa sem.");
  await translationButton.click();
  await expect(translationTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(translationRows.nth(3)).toHaveClass(/incorrect/);
  await expect(translationRows.nth(3)).toContainText("Правильно: Počkajte chvíľu, prosím.");
  await translationRows.nth(3).getByRole("textbox").fill("Prosím, počkajte chvíľu.");
  await translationButton.click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 5 opens as four topic groups and restores saved progress", async ({ page }) => {
  const lesson = module5.lessons[8];
  await mockStateApi(page, createState({ activeModule: 5, selectedSlug: lesson.slug, progress: { [lesson.slug]: "in_progress" }, lessonSteps: { [lesson.slug]: 3 } }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await expect(page.getByRole("heading", { name: module5.title })).toBeVisible();
  await expect(page.getByLabel("Выберите учебный модуль")).toHaveValue("5");
  await expect(page.locator(".course-group-card")).toHaveCount(4);
  for (const title of ["Настоящее время", "Возвратность, отрицание и вопрос", "Желание, возможность и необходимость", "Просьбы и инструкции"]) {
    await expect(page.getByText(title, { exact: true })).toBeVisible();
  }
  const group = module5.topicGroups?.find((item) => item.lessonSlugs.includes(lesson.slug));
  if (!group) throw new Error(`Lesson ${lesson.slug} is not assigned to a Module 5 topic group`);
  await page.locator(".course-group-card").filter({ hasText: group.title }).click();
  const lessonButton = page.getByRole("button", { name: new RegExp(lesson.title) }).first();
  await expect(lessonButton).toContainText("В процессе");
  await lessonButton.click();
  await expect(page.locator(".course-material-heading h3")).toHaveText(lesson.title);
  await expect(page.locator(".course-practice")).toBeVisible();
});

test("Module 6 theme 1 teaches a family profile and checks each answer row", async ({ page }) => {
  const lesson = module6.lessons.find((item) => item.slug === "family");
  if (!lesson) throw new Error("Family lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m6-family-step-5");
  if (!lastPractice) throw new Error("Module 6 theme 1 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("môj otec, moja sestra, moje dieťa, moji rodičia");
  expect(JSON.stringify(lesson)).toContain("Má tridsať rokov.");
  expect(JSON.stringify(lesson)).toContain("Moji rodičia bývajú v Košiciach.");

  await mockStateApi(page, createState({
    activeModule: 6,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Люди и дом" }).click();
  await page.getByRole("button").filter({ hasText: lesson.title }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Связное представление и частые ошибки");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 1");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const possessiveTask = page.locator(".course-reinforcement fieldset").nth(1);
  await expect(possessiveTask.locator(".course-pair-row")).toHaveCount(5);
  const optionPositions = await possessiveTask.locator(".course-pair-row").evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(optionPositions.every((positions) => positions.length === 4 && positions.every((position, index) => position === optionPositions[0][index]))).toBe(true);

  const formTask = page.locator(".course-reinforcement fieldset").nth(2);
  const formRows = formTask.locator(".course-pair-row");
  const formButton = formTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(formButton).toBeDisabled();
  for (const [index, answer] of ["brata", "sestru", "deti", "roky"].entries()) {
    await formRows.nth(index).getByRole("textbox").fill(answer);
  }
  await expect(formButton).toBeDisabled();
  await formRows.nth(4).getByRole("textbox").fill("rokov");
  await formButton.click();
  await expect(formTask).toHaveClass(/correct/);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  await translationRows.nth(0).getByRole("textbox").fill("To je moja sestra Anna.");
  await translationRows.nth(1).getByRole("textbox").fill("Mám jedného brata.");
  await translationRows.nth(2).getByRole("textbox").fill("Moji rodicia maju patdesiat rokov.");
  await translationRows.nth(3).getByRole("textbox").fill("Moja dcéra býva v Žiline.");
  await translationRows.nth(4).getByRole("textbox").fill("Otec pracuje v škole.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(translationRows.nth(2)).toHaveClass(/incorrect/);
  await expect(translationRows.nth(2)).toContainText("Правильно: Moji rodičia majú päťdesiat rokov.");
  await translationRows.nth(2).getByRole("textbox").fill("Moji rodičia majú päťdesiat rokov.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 7 theme 1 teaches regular past forms and checks each answer row", async ({ page }) => {
  const lesson = module7.lessons.find((item) => item.slug === "past-regular");
  if (!lesson) throw new Error("Module 7 regular past lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m7-past-regular-step-5");
  if (!lastPractice) throw new Error("Module 7 theme 1 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("pracoval som / pracovala som");
  expect(JSON.stringify(lesson)).toContain("В 3-м лице");
  expect(JSON.stringify(lesson)).toContain("Deti sa hrali v parku.");

  await mockStateApi(page, createState({
    activeModule: 7,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await expect(page.getByRole("heading", { name: module7.title })).toBeVisible();
  await openModule7Lesson(page, lesson);
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Частые ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 1");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);

  const auxiliaryTask = page.locator(".course-reinforcement fieldset").nth(2);
  const optionPositions = await auxiliaryTask.locator(".course-pair-row").evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(optionPositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === optionPositions[0][index]))).toBe(true);

  const formTask = page.locator(".course-reinforcement fieldset").nth(1);
  const formRows = formTask.locator(".course-pair-row");
  const formButton = formTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(formButton).toBeDisabled();
  for (const [index, answer] of ["pocuval", "upratovala", "robilo", "bývali"].entries()) {
    await formRows.nth(index).getByRole("textbox").fill(answer);
  }
  await expect(formButton).toBeDisabled();
  await formRows.nth(4).getByRole("textbox").fill("telefonovali");
  await formButton.click();
  await expect(formTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(formRows.nth(0)).toHaveClass(/incorrect/);
  await expect(formRows.nth(0)).toContainText("Правильно: počúval");
  await formRows.nth(0).getByRole("textbox").fill("počúval");
  await formButton.click();
  await expect(formTask).toHaveClass(/correct/);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  for (const [index, answer] of ["Včera som pracovala.", "Večer sme varili večeru.", "Anna nečítala.", "Kde ste bývali?", "Deti sa hrali v parku."].entries()) {
    await translationRows.nth(index).getByRole("textbox").fill(answer);
  }
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 7 theme 2 teaches frequent past forms and checks each answer row", async ({ page }) => {
  const lesson = module7.lessons.find((item) => item.slug === "past-frequent");
  if (!lesson) throw new Error("Module 7 frequent past lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m7-past-frequent-step-5");
  if (!lastPractice) throw new Error("Module 7 theme 2 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("byť — bol/bola/boli");
  expect(JSON.stringify(lesson)).toContain("Nemohol som prísť. ≠ Nemusel som prísť.");
  expect(JSON.stringify(lesson)).toContain("Deti jedli a pili.");

  await mockStateApi(page, createState({
    activeModule: 7,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await expect(page.getByRole("heading", { name: module7.title })).toBeVisible();
  await openModule7Lesson(page, lesson);
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Частые ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 2");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);

  const wordTask = page.locator(".course-reinforcement fieldset").nth(2);
  const optionPositions = await wordTask.locator(".course-pair-row").evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(optionPositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === optionPositions[0][index]))).toBe(true);

  const formTask = page.locator(".course-reinforcement fieldset").nth(1);
  const formRows = formTask.locator(".course-pair-row");
  const formButton = formTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(formButton).toBeDisabled();
  for (const [index, answer] of ["bol", "isla", "mohli", "jedol", "videla"].entries()) {
    await formRows.nth(index).getByRole("textbox").fill(answer);
  }
  await expect(formButton).toBeDisabled();
  await formRows.nth(5).getByRole("textbox").fill("vzali");
  await formButton.click();
  await expect(formTask.locator(".course-pair-row.correct")).toHaveCount(5);
  await expect(formRows.nth(1)).toHaveClass(/incorrect/);
  await expect(formRows.nth(1)).toContainText("Правильно: išla");
  await formRows.nth(1).getByRole("textbox").fill("išla");
  await formButton.click();
  await expect(formTask).toHaveClass(/correct/);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  for (const [index, answer] of ["Včera som bola doma.", "Chceli sme ísť do kina.", "Nemohla prísť.", "Čo povedal?", "Deti jedli a pili."].entries()) {
    await translationRows.nth(index).getByRole("textbox").fill(answer);
  }
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 7 theme 3 builds a coherent yesterday story and checks each answer row", async ({ page }) => {
  const lesson = module7.lessons.find((item) => item.slug === "yesterday");
  if (!lesson) throw new Error("Module 7 yesterday lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m7-yesterday-step-5");
  if (!lastPractice) throw new Error("Module 7 theme 3 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("najprv — сначала, potom — потом");
  expect(JSON.stringify(lesson)).toContain("Preto = результат; lebo = причина.");
  expect(JSON.stringify(lesson)).toContain("Bol to pokojný deň.");

  await mockStateApi(page, createState({
    activeModule: 7,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await expect(page.getByRole("heading", { name: module7.title })).toBeVisible();
  await openModule7Lesson(page, lesson);
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Частые ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 3");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);

  const connectorTask = page.locator(".course-reinforcement fieldset").nth(0);
  const optionPositions = await connectorTask.locator(".course-pair-row").evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(optionPositions.every((positions) => positions.length === 4 && positions.every((position, index) => position === optionPositions[0][index]))).toBe(true);

  const formTask = page.locator(".course-reinforcement fieldset").nth(2);
  const formRows = formTask.locator(".course-pair-row");
  const formButton = formTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(formButton).toBeDisabled();
  for (const [index, answer] of ["vstala", "isiel", "jedli"].entries()) {
    await formRows.nth(index).getByRole("textbox").fill(answer);
  }
  await expect(formButton).toBeDisabled();
  await formRows.nth(3).getByRole("textbox").fill("prišli");
  await formButton.click();
  await expect(formTask.locator(".course-pair-row.correct")).toHaveCount(3);
  await expect(formRows.nth(1)).toHaveClass(/incorrect/);
  await expect(formRows.nth(1)).toContainText("Правильно: išiel");
  await formRows.nth(1).getByRole("textbox").fill("išiel");
  await formButton.click();
  await expect(formTask).toHaveClass(/correct/);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  for (const [index, answer] of ["Včera som mala bežný deň.", "Najprv som raňajkovala.", "Potom sme išli do práce.", "Večer pršalo, preto som zostala doma."].entries()) {
    await translationRows.nth(index).getByRole("textbox").fill(answer);
  }
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 7 theme 4 teaches budem plus infinitive and checks each answer row", async ({ page }) => {
  const lesson = module7.lessons.find((item) => item.slug === "future-budem");
  if (!lesson) throw new Error("Module 7 future budem lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m7-future-budem-step-5");
  if (!lastPractice) throw new Error("Module 7 theme 4 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("budem, budeš, bude, budeme, budete или budú + инфинитив");
  expect(JSON.stringify(lesson)).toContain("Nebudeme dlho čakať.");
  expect(JSON.stringify(lesson)).toContain("Poobede sa budem učiť slovenčinu.");

  await mockStateApi(page, createState({
    activeModule: 7,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await expect(page.getByRole("heading", { name: module7.title })).toBeVisible();
  await openModule7Lesson(page, lesson);
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Частые ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 4");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);

  const personTask = page.locator(".course-reinforcement fieldset").nth(0);
  const optionPositions = await personTask.locator(".course-pair-row").evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(optionPositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === optionPositions[0][index]))).toBe(true);

  const negationTask = page.locator(".course-reinforcement fieldset").nth(2);
  const negationRows = negationTask.locator(".course-pair-row");
  const negationButton = negationTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(negationButton).toBeDisabled();
  for (const [index, answer] of ["Nebudem čakať.", "Nebudeš pracovať.", "Nebudeme variť."].entries()) {
    await negationRows.nth(index).getByRole("textbox").fill(answer);
  }
  await expect(negationButton).toBeDisabled();
  await negationRows.nth(3).getByRole("textbox").fill("Nebudu byvat v Nitre.");
  await negationButton.click();
  await expect(negationTask.locator(".course-pair-row.correct")).toHaveCount(3);
  await expect(negationRows.nth(3)).toHaveClass(/incorrect/);
  await expect(negationRows.nth(3)).toContainText("Правильно: Nebudú bývať v Nitre.");
  await negationRows.nth(3).getByRole("textbox").fill("Nebudú bývať v Nitre.");
  await negationButton.click();
  await expect(negationTask).toHaveClass(/correct/);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  for (const [index, answer] of ["Zajtra budem pracovať.", "Nebudeme dlho čakať.", "Kde budete byvat?", "Deti sa budú hrať vonku.", "Budeš večer čítať?"].entries()) {
    await translationRows.nth(index).getByRole("textbox").fill(answer);
  }
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(translationRows.nth(2)).toHaveClass(/incorrect/);
  await expect(translationRows.nth(2)).toContainText("Правильно: Kde budete bývať?");
  await translationRows.nth(2).getByRole("textbox").fill("Kde budete bývať?");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 7 theme 5 asks about future plans and checks each answer row", async ({ page }) => {
  const lesson = module7.lessons.find((item) => item.slug === "future-questions-negation");
  if (!lesson) throw new Error("Module 7 future questions lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m7-future-questions-negation-step-5");
  if (!lastPractice) throw new Error("Module 7 theme 5 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("Budete pracovať? — Áno, budem / budeme.");
  expect(JSON.stringify(lesson)).toContain("Kde? — место; Kam? — направление.");
  expect(JSON.stringify(lesson)).toContain("Ešte neviem. Možno budem pracovať.");

  await mockStateApi(page, createState({
    activeModule: 7,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await expect(page.getByRole("heading", { name: module7.title })).toBeVisible();
  await openModule7Lesson(page, lesson);
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Частые ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 5");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);

  const shortAnswerTask = page.locator(".course-reinforcement fieldset").nth(1);
  const optionPositions = await shortAnswerTask.locator(".course-pair-row").evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(optionPositions.every((positions) => positions.length === 4 && positions.every((position, index) => position === optionPositions[0][index]))).toBe(true);

  const negationTask = page.locator(".course-reinforcement fieldset").nth(2);
  const negationRows = negationTask.locator(".course-pair-row");
  const negationButton = negationTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(negationButton).toBeDisabled();
  for (const [index, answer] of ["Nebudem mať čas.", "Nebudeš cestovať.", "Nebudeme čakať."].entries()) {
    await negationRows.nth(index).getByRole("textbox").fill(answer);
  }
  await expect(negationButton).toBeDisabled();
  await negationRows.nth(3).getByRole("textbox").fill("Nebudu sa ucit.");
  await negationButton.click();
  await expect(negationTask.locator(".course-pair-row.correct")).toHaveCount(3);
  await expect(negationRows.nth(3)).toHaveClass(/incorrect/);
  await expect(negationRows.nth(3)).toContainText("Правильно: Nebudú sa učiť.");
  await negationRows.nth(3).getByRole("textbox").fill("Nebudú sa učiť.");
  await negationButton.click();
  await expect(negationTask).toHaveClass(/correct/);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  for (const [index, answer] of ["Čo budeš zajtra robiť?", "Kde sa budeme stretávať?", "Nebudem pracovať večer.", "Možno budú cestovať.", "Ešte neviem."].entries()) {
    await translationRows.nth(index).getByRole("textbox").fill(answer);
  }
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 7 theme 6 contrasts yesterday today and tomorrow row by row", async ({ page }) => {
  const lesson = module7.lessons.find((item) => item.slug === "yesterday-today-tomorrow");
  if (!lesson) throw new Error("Module 7 three times lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m7-yesterday-today-tomorrow-step-5");
  if (!lastPractice) throw new Error("Module 7 theme 6 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("pracoval som — pracujem — budem pracovať");
  expect(JSON.stringify(lesson)).toContain("Včera som sa učila. Dnes sa učím. Zajtra sa budem učiť.");
  expect(JSON.stringify(lesson)).toContain("a — и; ale — но; tiež — тоже; preto — поэтому");

  await mockStateApi(page, createState({
    activeModule: 7,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await expect(page.getByRole("heading", { name: module7.title })).toBeVisible();
  await openModule7Lesson(page, lesson);
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Частые ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 6");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);

  const tenseTask = page.locator(".course-reinforcement fieldset").nth(0);
  const optionPositions = await tenseTask.locator(".course-pair-row").evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(optionPositions.every((positions) => positions.length === 3 && positions.every((position, index) => position === optionPositions[0][index]))).toBe(true);

  const tripleTask = page.locator(".course-reinforcement fieldset").nth(2);
  const tripleRows = tripleTask.locator(".course-pair-row");
  const tripleButton = tripleTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(tripleButton).toBeDisabled();
  for (const [index, answer] of ["Včera som pracoval.", "Dnes pracujem.", "Zajtra budem pracovať.", "Včera som sa ucila.", "Dnes sa učím."].entries()) {
    await tripleRows.nth(index).getByRole("textbox").fill(answer);
  }
  await expect(tripleButton).toBeDisabled();
  await tripleRows.nth(5).getByRole("textbox").fill("Zajtra sa budem učiť.");
  await tripleButton.click();
  await expect(tripleTask.locator(".course-pair-row.correct")).toHaveCount(5);
  await expect(tripleRows.nth(3)).toHaveClass(/incorrect/);
  await expect(tripleRows.nth(3)).toContainText("Правильно: Včera som sa učila.");
  await tripleRows.nth(3).getByRole("textbox").fill("Včera som sa učila.");
  await tripleButton.click();
  await expect(tripleTask).toHaveClass(/correct/);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  for (const [index, answer] of ["Včera som pracovala.", "Dnes oddychujem.", "Zajtra sa budem učiť slovenčinu.", "Včera som nemala čas, ale dnes mám čas."].entries()) {
    await translationRows.nth(index).getByRole("textbox").fill(answer);
  }
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 7 theme 7 builds a complete invitation and checks each answer row", async ({ page }) => {
  const lesson = module7.lessons.find((item) => item.slug === "invitation-arrangement");
  if (!lesson) throw new Error("Module 7 invitation lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m7-invitation-arrangement-step-5");
  if (!lastPractice) throw new Error("Module 7 theme 7 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("приглашение → ответ → когда? → где? → подтверждение");
  expect(JSON.stringify(lesson)).toContain("Ďakujem, ale v sobotu nemôžem. A čo v nedeľu?");
  expect(JSON.stringify(lesson)).toContain("Takže v sobotu o štvrtej pred kinom?");

  await mockStateApi(page, createState({
    activeModule: 7,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await expect(page.getByRole("heading", { name: module7.title })).toBeVisible();
  await openModule7Lesson(page, lesson);
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Частые ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 7");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);

  const replyTask = page.locator(".course-reinforcement fieldset").nth(0);
  const optionPositions = await replyTask.locator(".course-pair-row").evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(optionPositions.every((positions) => positions.length === 4 && positions.every((position, index) => position === optionPositions[0][index]))).toBe(true);

  const invitationTask = page.locator(".course-reinforcement fieldset").nth(1);
  const invitationRows = invitationTask.locator(".course-pair-row");
  const invitationButton = invitationTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(invitationButton).toBeDisabled();
  for (const [index, answer] of ["Chceš ísť do kina?", "Môžeme sa stretnúť zajtra?", "Máš čas v sobotu?"].entries()) {
    await invitationRows.nth(index).getByRole("textbox").fill(answer);
  }
  await expect(invitationButton).toBeDisabled();
  await invitationRows.nth(3).getByRole("textbox").fill("Podme na prechadzku.");
  await invitationButton.click();
  await expect(invitationTask.locator(".course-pair-row.correct")).toHaveCount(3);
  await expect(invitationRows.nth(3)).toHaveClass(/incorrect/);
  await expect(invitationRows.nth(3)).toContainText("Правильно: Poďme na prechádzku.");
  await invitationRows.nth(3).getByRole("textbox").fill("Poďme na prechádzku.");
  await invitationButton.click();
  await expect(invitationTask).toHaveClass(/correct/);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  for (const [index, answer] of ["Máš čas v piatok?", "Nechceš ísť do kina?", "Bohužiaľ, nemôžem.", "Kde sa stretneme?", "Dobre, platí."].entries()) {
    await translationRows.nth(index).getByRole("textbox").fill(answer);
  }
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 8 theme 1 teaches ty and vy etiquette with a separate six-task test", async ({ page }) => {
  const lesson = module8.lessons.find((item) => item.slug === "social-etiquette");
  if (!lesson) throw new Error("Module 8 social etiquette lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m8-social-etiquette-step-5");
  if (!lastPractice) throw new Error("Module 8 theme 1 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("Môžeme si tykať?");
  expect(JSON.stringify(lesson)).toContain("Prepáčte, môžete… → Prepáč, môžeš…");
  expect(JSON.stringify(lesson)).toContain("Dobrý deň. Ako sa voláte? Odkiaľ ste? Hovoríte po slovensky?");

  await mockStateApi(page, createState({
    activeModule: 8,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await expect(page.getByRole("heading", { name: module8.title })).toBeVisible();
  await openModule8Lesson(page, lesson);
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Типичные ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 1");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);

  const situationTask = page.locator(".course-reinforcement fieldset").nth(0);
  const optionPositions = await situationTask.locator(".course-pair-row").evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(optionPositions.every((positions) => positions.length === 2 && positions.every((position, index) => position === optionPositions[0][index]))).toBe(true);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(3);
  const translationRows = translationTask.locator(".course-pair-row");
  const translationButton = translationTask.getByRole("button", { name: "Проверить", exact: true });
  await translationRows.nth(0).getByRole("textbox").fill("Hovorite po anglicky?");
  await translationRows.nth(1).getByRole("textbox").fill("Vieš, kde je stanica?");
  await expect(translationButton).toBeDisabled();
  await translationRows.nth(2).getByRole("textbox").fill("Prepáčte, môžete to zopakovať?");
  await translationButton.click();
  await expect(translationTask.locator(".course-pair-row.correct")).toHaveCount(2);
  await expect(translationRows.nth(0)).toHaveClass(/incorrect/);
  await expect(translationRows.nth(0)).toContainText("Правильно: Hovoríte po anglicky?");
  await translationRows.nth(0).getByRole("textbox").fill("Hovoríte po anglicky?");
  await translationButton.click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 8 theme 2 builds a supported introduction and checks dialogue rows", async ({ page }) => {
  const lesson = module8.lessons.find((item) => item.slug === "supported-dialogue");
  if (!lesson) throw new Error("Module 8 supported dialogue lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m8-supported-dialogue-step-5");
  if (!lastPractice) throw new Error("Module 8 theme 2 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("вопрос → ответ с маленькой деталью → реакция → встречный вопрос");
  expect(JSON.stringify(lesson)).toContain("Aha. Páči sa vám Bratislava?");
  expect(JSON.stringify(lesson)).toContain("Som zo Slovenska, z Nitry. A vy?");

  await mockStateApi(page, createState({
    activeModule: 8,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await expect(page.getByRole("heading", { name: module8.title })).toBeVisible();
  await openModule8Lesson(page, lesson);
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Типичные ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 2");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);

  const replyTask = page.locator(".course-reinforcement fieldset").nth(0);
  const optionPositions = await replyTask.locator(".course-pair-row").evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(optionPositions.every((positions) => positions.length === 2 && positions.every((position, index) => position === optionPositions[0][index]))).toBe(true);

  const correctionTask = page.locator(".course-reinforcement fieldset").nth(3);
  const correctionRows = correctionTask.locator(".course-pair-row");
  for (const [index, answer] of ["Ja som Boris.", "Odkiaľ ste?", "Som zo Slovenska.", "Čo robíte?"].entries()) {
    await correctionRows.nth(index).getByRole("textbox").fill(answer);
  }
  await correctionTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(correctionTask).toHaveClass(/correct/);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  const translationButton = translationTask.getByRole("button", { name: "Проверить", exact: true });
  await translationRows.nth(0).getByRole("textbox").fill("Teší ma.");
  await translationRows.nth(1).getByRole("textbox").fill("Kde bývate?");
  await translationRows.nth(2).getByRole("textbox").fill("Trochu hovorim po slovensky.");
  await expect(translationButton).toBeDisabled();
  await translationRows.nth(3).getByRole("textbox").fill("To je zaujímavé. A vy?");
  await translationButton.click();
  await expect(translationTask.locator(".course-pair-row.correct")).toHaveCount(3);
  await expect(translationRows.nth(2)).toHaveClass(/incorrect/);
  await expect(translationRows.nth(2)).toContainText("Правильно: Trochu hovorím po slovensky.");
  await translationRows.nth(2).getByRole("textbox").fill("Trochu hovorím po slovensky.");
  await translationButton.click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 8 theme 3 completes an everyday task and checks each result row", async ({ page }) => {
  const lesson = module8.lessons.find((item) => item.slug === "everyday-task");
  if (!lesson) throw new Error("Module 8 everyday task lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m8-everyday-task-step-5");
  if (!lastPractice) throw new Error("Module 8 theme 3 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("цель → просьба → уточнение → подтверждение");
  expect(JSON.stringify(lesson)).toContain("V byte nefunguje teplá voda.");
  expect(JSON.stringify(lesson)).toContain("Dobre, to mi vyhovuje. Ďakujem.");

  await mockStateApi(page, createState({
    activeModule: 8,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await expect(page.getByRole("heading", { name: module8.title })).toBeVisible();
  await openModule8Lesson(page, lesson);
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Типичные ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 3");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);

  const questionTask = page.locator(".course-reinforcement fieldset").nth(1);
  const optionPositions = await questionTask.locator(".course-pair-row").evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(optionPositions.every((positions) => positions.length === 4 && positions.every((position, index) => position === optionPositions[0][index]))).toBe(true);

  const correctionTask = page.locator(".course-reinforcement fieldset").nth(3);
  const correctionRows = correctionTask.locator(".course-pair-row");
  for (const [index, answer] of ["Potrebujem lístok.", "Prosím vás, môžete mi pomôcť?", "Koľko to stojí?", "Kedy môže technik prísť?"].entries()) {
    await correctionRows.nth(index).getByRole("textbox").fill(answer);
  }
  await correctionTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(correctionTask).toHaveClass(/correct/);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  const translationButton = translationTask.getByRole("button", { name: "Проверить", exact: true });
  await translationRows.nth(0).getByRole("textbox").fill("Potrebujem pomoc.");
  await translationRows.nth(1).getByRole("textbox").fill("Kde mozem zaplatiť?");
  await translationRows.nth(2).getByRole("textbox").fill("Kedy ide najbližší vlak?");
  await expect(translationButton).toBeDisabled();
  await translationRows.nth(3).getByRole("textbox").fill("Dobre, to mi vyhovuje.");
  await translationButton.click();
  await expect(translationTask.locator(".course-pair-row.correct")).toHaveCount(3);
  await expect(translationRows.nth(1)).toHaveClass(/incorrect/);
  await expect(translationRows.nth(1)).toContainText("Правильно: Kde môžem zaplatiť?");
  await translationRows.nth(1).getByRole("textbox").fill("Kde môžem zaplatiť?");
  await translationButton.click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 8 theme 4 extracts message details and checks negation row by row", async ({ page }) => {
  const lesson = module8.lessons.find((item) => item.slug === "understand-message");
  if (!lesson) throw new Error("Module 8 message comprehension lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m8-understand-message-step-5");
  if (!lastPractice) throw new Error("Module 8 theme 4 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("кто пишет → зачем → когда и где → что нужно сделать");
  expect(JSON.stringify(lesson)).toContain("Dnes neprídem na kurz.");
  expect(JSON.stringify(lesson)).toContain("Piatok o 17:30 mi vyhovuje.");

  await mockStateApi(page, createState({
    activeModule: 8,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await expect(page.getByRole("heading", { name: module8.title })).toBeVisible();
  await openModule8Lesson(page, lesson);
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Типичные ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 4");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);

  const purposeTask = page.locator(".course-reinforcement fieldset").nth(0);
  const optionPositions = await purposeTask.locator(".course-pair-row").evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(optionPositions.every((positions) => positions.length === 3 && positions.every((position, index) => position === optionPositions[0][index]))).toBe(true);

  const truthTask = page.locator(".course-reinforcement fieldset").nth(2);
  const truthRows = truthTask.locator(".course-pair-row");
  const truthButton = truthTask.getByRole("button", { name: "Проверить", exact: true });
  await truthRows.nth(0).getByRole("button", { name: "Верно", exact: true }).click();
  await truthRows.nth(1).getByRole("button", { name: "Верно", exact: true }).click();
  await expect(truthButton).toBeDisabled();
  await truthRows.nth(2).getByRole("button", { name: "Верно", exact: true }).click();
  await truthButton.click();
  await expect(truthTask.locator(".course-pair-row.correct")).toHaveCount(2);
  await expect(truthRows.nth(0)).toHaveClass(/incorrect/);
  await expect(truthRows.nth(0)).toContainText("Правильно: Неверно");
  await truthRows.nth(0).getByRole("button", { name: "Неверно", exact: true }).click();
  await truthButton.click();
  await expect(truthTask).toHaveClass(/correct/);

  const finalMessageTask = page.locator(".course-reinforcement fieldset").nth(5);
  await expect(finalMessageTask.locator(".course-pair-row")).toHaveCount(6);
  await finalMessageTask.getByRole("button", { name: "завтра курса нет", exact: true }).click();
  await finalMessageTask.getByRole("button", { name: "в пятницу", exact: true }).click();
  await finalMessageTask.getByRole("button", { name: "в 17:30", exact: true }).click();
  await finalMessageTask.getByRole("button", { name: "в школе", exact: true }).click();
  await finalMessageTask.getByRole("button", { name: "сообщить, можете ли вы прийти", exact: true }).click();
  await finalMessageTask.getByRole("button", { name: "Ahoj! Áno, môžem prísť. Piatok o 17:30 mi vyhovuje. Ďakujem.", exact: true }).click();
  await finalMessageTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(finalMessageTask).toHaveClass(/correct/);
});

test("Module 8 theme 5 structures a voice message and checks description agreement row by row", async ({ page }) => {
  const lesson = module8.lessons.find((item) => item.slug === "voice-description");
  if (!lesson) throw new Error("Module 8 voice description lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m8-voice-description-step-5");
  if (!lastPractice) throw new Error("Module 8 theme 5 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("кто → зачем → детали → просьба → конец");
  expect(JSON.stringify(lesson)).toContain("кто или что → где → какой → что происходит");
  expect(JSON.stringify(lesson)).toContain("Ahoj, Peter, tu je Ari.");

  await mockStateApi(page, createState({
    activeModule: 8,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await expect(page.getByRole("heading", { name: module8.title })).toBeVisible();
  await openModule8Lesson(page, lesson);
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Типичные ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 5");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);

  const orderTask = page.locator(".course-reinforcement fieldset").nth(1);
  const optionPositions = await orderTask.locator(".course-pair-row").evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(optionPositions.every((positions) => positions.length === 4 && positions.every((position, index) => position === optionPositions[0][index]))).toBe(true);

  const agreementTask = page.locator(".course-reinforcement fieldset").nth(3);
  const agreementRows = agreementTask.locator(".course-pair-row");
  const agreementButton = agreementTask.getByRole("button", { name: "Проверить", exact: true });
  await agreementRows.nth(0).getByRole("textbox").fill("Moja izba je malá.");
  await agreementRows.nth(1).getByRole("textbox").fill("To je modrá taška.");
  await agreementRows.nth(2).getByRole("textbox").fill("Hľadám čierny batoh.");
  await expect(agreementButton).toBeDisabled();
  await agreementRows.nth(3).getByRole("textbox").fill("Auto je nove.");
  await agreementButton.click();
  await expect(agreementTask.locator(".course-pair-row.correct")).toHaveCount(3);
  await expect(agreementRows.nth(3)).toHaveClass(/incorrect/);
  await expect(agreementRows.nth(3)).toContainText("Правильно: Auto je nové.");
  await agreementRows.nth(3).getByRole("textbox").fill("Auto je nové.");
  await agreementButton.click();
  await expect(agreementTask).toHaveClass(/correct/);

  const recordingTask = page.locator(".course-reinforcement fieldset").nth(5);
  await expect(recordingTask.locator(".course-pair-row")).toHaveCount(5);
  for (const answer of [
    "Ahoj, Peter, tu je Ari.",
    "Meškám asi desať minút.",
    "Budem pri stanici o 18:10.",
    "Počkaj na mňa, prosím.",
    "Ďakujem, ahoj.",
  ]) {
    await recordingTask.getByRole("button", { name: answer, exact: true }).click();
  }
  await recordingTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(recordingTask).toHaveClass(/correct/);
});

test("Module 8 theme 6 builds a written profile and checks first-person forms row by row", async ({ page }) => {
  const lesson = module8.lessons.find((item) => item.slug === "written-profile");
  if (!lesson) throw new Error("Module 8 written profile lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m8-written-profile-step-5");
  if (!lastPractice) throw new Error("Module 8 theme 6 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("имя → откуда и где живёте → работа или учёба → языки → интересы → цель");
  expect(JSON.stringify(lesson)).toContain("Som zo Slovenska.");
  expect(JSON.stringify(lesson)).toContain("Chcem lepšie hovoriť po slovensky.");

  await mockStateApi(page, createState({
    activeModule: 8,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await expect(page.getByRole("heading", { name: module8.title })).toBeVisible();
  await openModule8Lesson(page, lesson);
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Типичные ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 6");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);

  const orderTask = page.locator(".course-reinforcement fieldset").nth(2);
  const optionPositions = await orderTask.locator(".course-pair-row").evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(optionPositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === optionPositions[0][index]))).toBe(true);

  const correctionTask = page.locator(".course-reinforcement fieldset").nth(3);
  const correctionRows = correctionTask.locator(".course-pair-row");
  const correctionButton = correctionTask.getByRole("button", { name: "Проверить", exact: true });
  for (const [index, answer] of ["Volám sa Eva.", "Som zo Slovenska.", "Pracujem v škole.", "Hovorím po anglicky."].entries()) {
    await correctionRows.nth(index).getByRole("textbox").fill(answer);
  }
  await expect(correctionButton).toBeDisabled();
  await correctionRows.nth(4).getByRole("textbox").fill("Rad citam.");
  await correctionButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(correctionRows.nth(4)).toHaveClass(/incorrect/);
  await expect(correctionRows.nth(4)).toContainText("Правильно: Rád čítam.");
  await correctionRows.nth(4).getByRole("textbox").fill("Rada čítam.");
  await correctionButton.click();
  await expect(correctionTask).toHaveClass(/correct/);

  const profileTask = page.locator(".course-reinforcement fieldset").nth(5);
  await expect(profileTask.locator(".course-pair-row")).toHaveCount(6);
  for (const answer of [
    "Volám sa Ari.",
    "Som z Ruska, ale teraz bývam v Bratislave.",
    "Pracujem v IT.",
    "Hovorím po rusky a po anglicky.",
    "Vo voľnom čase rada čítam a chodím na prechádzky.",
    "Chcem lepšie hovoriť po slovensky.",
  ]) {
    await profileTask.getByRole("button", { name: answer, exact: true }).click();
  }
  await profileTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(profileTask).toHaveClass(/correct/);
});

test("Module 8 theme 7 relays exact details and checks third-person forms row by row", async ({ page }) => {
  const lesson = module8.lessons.find((item) => item.slug === "simple-mediation");
  if (!lesson) throw new Error("Module 8 simple mediation lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m8-simple-mediation-step-5");
  if (!lastPractice) throw new Error("Module 8 theme 7 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("кто сообщил → что произошло → когда и где → что нужно сделать");
  expect(JSON.stringify(lesson)).toContain("Eva zajtra nepríde.");
  expect(JSON.stringify(lesson)).toContain("Lístok stojí 18 eur.");

  await mockStateApi(page, createState({
    activeModule: 8,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await expect(page.getByRole("heading", { name: module8.title })).toBeVisible();
  await openModule8Lesson(page, lesson);
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Типичные ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 7");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);

  const detailsTask = page.locator(".course-reinforcement fieldset").nth(2);
  const optionPositions = await detailsTask.locator(".course-pair-row").evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(optionPositions.every((positions) => positions.length === 4 && positions.every((position, index) => position === optionPositions[0][index]))).toBe(true);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  const translationButton = translationTask.getByRole("button", { name: "Проверить", exact: true });
  for (const [index, answer] of [
    "Peter píše, že stretnutie je zajtra.",
    "Eva príde o siedmej.",
    "Máme priniesť doklady.",
  ].entries()) {
    await translationRows.nth(index).getByRole("textbox").fill(answer);
  }
  await expect(translationButton).toBeDisabled();
  await translationRows.nth(3).getByRole("textbox").fill("Rozumiem spravne: miestnost 12?");
  await translationButton.click();
  await expect(translationTask.locator(".course-pair-row.correct")).toHaveCount(3);
  await expect(translationRows.nth(3)).toHaveClass(/incorrect/);
  await expect(translationRows.nth(3)).toContainText("Правильно: Rozumiem správne: miestnosť 12?");
  await translationRows.nth(3).getByRole("textbox").fill("Rozumiem správne: miestnosť 12?");
  await translationButton.click();
  await expect(translationTask).toHaveClass(/correct/);

  const relayTask = page.locator(".course-reinforcement fieldset").nth(5);
  await expect(relayTask.locator(".course-pair-row")).toHaveCount(3);
  for (const answer of [
    "Anna hovorí, že obchod je dnes zatvorený.",
    "Zajtra je otvorený od deviatej do šiestej.",
    "Máme prísť zajtra ráno.",
  ]) {
    await relayTask.getByRole("button", { name: answer, exact: true }).click();
  }
  await relayTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(relayTask).toHaveClass(/correct/);
});

test("Module 8 theme 8 repairs misunderstanding and keeps ty-vy requests consistent", async ({ page }) => {
  const lesson = module8.lessons.find((item) => item.slug === "repair-strategies");
  if (!lesson) throw new Error("Module 8 repair strategies lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m8-repair-strategies-step-5");
  if (!lastPractice) throw new Error("Module 8 theme 8 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("сигнал → просьба → точное уточнение → подтверждение");
  expect(JSON.stringify(lesson)).toContain("Neviem — не знаю ответа или факта");
  expect(JSON.stringify(lesson)).toContain("Pätnásť alebo päťdesiat?");

  await mockStateApi(page, createState({
    activeModule: 8,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await expect(page.getByRole("heading", { name: module8.title })).toBeVisible();
  await openModule8Lesson(page, lesson);
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Типичные ошибки и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 8");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);

  const registerTask = page.locator(".course-reinforcement fieldset").nth(2);
  const optionPositions = await registerTask.locator(".course-pair-row").evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(optionPositions.every((positions) => positions.length === 2 && positions.every((position, index) => position === optionPositions[0][index]))).toBe(true);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  const translationButton = translationTask.getByRole("button", { name: "Проверить", exact: true });
  for (const [index, answer] of [
    "Môžete to zopakovať pomalšie?",
    "Čo znamená toto slovo?",
    "Rozumiem správne: vlak ide o šiestej?",
  ].entries()) {
    await translationRows.nth(index).getByRole("textbox").fill(answer);
  }
  await expect(translationButton).toBeDisabled();
  await translationRows.nth(3).getByRole("textbox").fill("Uz rozumiem, dakujem.");
  await translationButton.click();
  await expect(translationTask.locator(".course-pair-row.correct")).toHaveCount(3);
  await expect(translationRows.nth(3)).toHaveClass(/incorrect/);
  await expect(translationRows.nth(3)).toContainText("Правильно: Už rozumiem, ďakujem.");
  await translationRows.nth(3).getByRole("textbox").fill("Už rozumiem, ďakujem.");
  await translationButton.click();
  await expect(translationTask).toHaveClass(/correct/);

  const dialogueTask = page.locator(".course-reinforcement fieldset").nth(5);
  await expect(dialogueTask.locator(".course-pair-row")).toHaveCount(6);
  for (const answer of [
    "Choďte rovno a potom doprava.",
    "Prepáčte, nerozumiem. Môžete hovoriť pomalšie?",
    "Áno. Najprv rovno, potom doprava.",
    "Rozumiem správne: najprv rovno a potom doprava?",
    "Áno, presne tak.",
    "Dobre, už rozumiem. Ďakujem.",
  ]) {
    await dialogueTask.getByRole("button", { name: answer, exact: true }).click();
  }
  await dialogueTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(dialogueTask).toHaveClass(/correct/);
});

test("Module 8 theme 9 completes A1 scenarios and preserves exact details", async ({ page }) => {
  const lesson = module8.lessons.find((item) => item.slug === "a1-scenarios");
  if (!lesson) throw new Error("Module 8 final scenarios lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m8-a1-scenarios-step-5");
  if (!lastPractice) throw new Error("Module 8 theme 9 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("контакт → цель → детали → уточнение → результат → завершение");
  expect(JSON.stringify(lesson)).toContain("Dnes kurz nie je.");
  expect(JSON.stringify(lesson)).toContain("Rozumiem správne: o 15:20?");

  await mockStateApi(page, createState({
    activeModule: 8,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await expect(page.getByRole("heading", { name: module8.title })).toBeVisible();
  await openModule8Lesson(page, lesson);
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Финальные опоры и самопроверка");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть итоговых заданий A1");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);

  const detailsTask = page.locator(".course-reinforcement fieldset").nth(2);
  const optionPositions = await detailsTask.locator(".course-pair-row").evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(optionPositions.every((positions) => positions.length === 4 && positions.every((position, index) => position === optionPositions[0][index]))).toBe(true);

  const correctionTask = page.locator(".course-reinforcement fieldset").nth(3);
  const correctionRows = correctionTask.locator(".course-pair-row");
  const correctionButton = correctionTask.getByRole("button", { name: "Проверить", exact: true });
  for (const [index, answer] of [
    "Vy máte čas?",
    "Môžete mi pomôcť, prosím vás?",
    "Eva príde o piatej.",
  ].entries()) {
    await correctionRows.nth(index).getByRole("textbox").fill(answer);
  }
  await expect(correctionButton).toBeDisabled();
  await correctionRows.nth(3).getByRole("textbox").fill("Potrebujem listok.");
  await correctionButton.click();
  await expect(correctionTask.locator(".course-pair-row.correct")).toHaveCount(3);
  await expect(correctionRows.nth(3)).toHaveClass(/incorrect/);
  await expect(correctionRows.nth(3)).toContainText("Правильно: Potrebujem lístok.");
  await correctionRows.nth(3).getByRole("textbox").fill("Ja potrebujem lístok.");
  await correctionButton.click();
  await expect(correctionTask).toHaveClass(/correct/);

  const scenarioTask = page.locator(".course-reinforcement fieldset").nth(5);
  await expect(scenarioTask.locator(".course-pair-row")).toHaveCount(9);
  for (const [index, answer] of [
    "Dobrý deň. Chcela by som lístok do Nitry.",
    "Jednosmerný alebo spiatočný?",
    "Prepáčte, nerozumiem. Môžete to zopakovať pomalšie?",
    "Jednosmerný alebo spiatočný?",
    "Jednosmerný. Kedy ide najbližší vlak?",
    "O pätnástej dvadsať.",
    "Rozumiem správne: o 15:20?",
    "Áno. Stojí deväť eur.",
    "Dobre, vezmem si ho. Ďakujem.",
  ].entries()) {
    await scenarioTask.locator(".course-pair-row").nth(index).getByRole("button", { name: answer, exact: true }).click();
  }
  await scenarioTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(scenarioTask).toHaveClass(/correct/);
});

test("Module 6 theme 2 teaches home descriptions and checks location models row by row", async ({ page }) => {
  const lesson = module6.lessons.find((item) => item.slug === "home");
  if (!lesson) throw new Error("Home lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m6-home-step-5");
  if (!lastPractice) throw new Error("Module 6 theme 2 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("Bývam v malom byte.");
  expect(JSON.stringify(lesson)).toContain("Knihy sú na poličke.");
  expect(JSON.stringify(lesson)).toContain("Som doma. Idem domov.");

  await mockStateApi(page, createState({
    activeModule: 6,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Люди и дом" }).click();
  await page.getByRole("button").filter({ hasText: lesson.title }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Описание дома и частые ошибки");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 2");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const categoryTask = page.locator(".course-reinforcement fieldset").nth(0);
  const categoryRows = categoryTask.locator(".course-pair-row");
  await expect(categoryRows).toHaveCount(5);
  const categoryPositions = await categoryRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(categoryPositions.every((positions) => positions.length === 3 && positions.every((position, index) => position === categoryPositions[0][index]))).toBe(true);

  const locationTask = page.locator(".course-reinforcement fieldset").nth(2);
  const locationRows = locationTask.locator(".course-pair-row");
  const locationButton = locationTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(locationButton).toBeDisabled();
  for (const [index, answer] of ["v", "na", "pri", "vedľa"].entries()) {
    await locationRows.nth(index).getByRole("button", { name: answer, exact: true }).click();
  }
  await expect(locationButton).toBeDisabled();
  await locationRows.nth(4).getByRole("button", { name: "na", exact: true }).click();
  await locationButton.click();
  await expect(locationTask).toHaveClass(/correct/);
  const locationPositions = await locationRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(locationPositions.every((positions) => positions.length === 4 && positions.every((position, index) => position === locationPositions[0][index]))).toBe(true);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  await translationRows.nth(0).getByRole("textbox").fill("Žijem v malom byte.");
  await translationRows.nth(1).getByRole("textbox").fill("V kuchyni je veľký stôl.");
  await translationRows.nth(2).getByRole("textbox").fill("Knihy su na policke.");
  await translationRows.nth(3).getByRole("textbox").fill("Večer upratujem izbu.");
  await translationRows.nth(4).getByRole("textbox").fill("Som doma.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(translationRows.nth(2)).toHaveClass(/incorrect/);
  await expect(translationRows.nth(2)).toContainText("Правильно: Knihy sú na poličke.");
  await translationRows.nth(2).getByRole("textbox").fill("Knihy sú na poličke.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 6 theme 3 teaches a shopping dialogue and checks quantities row by row", async ({ page }) => {
  const lesson = module6.lessons.find((item) => item.slug === "shopping");
  if (!lesson) throw new Error("Shopping lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m6-shopping-step-5");
  if (!lastPractice) throw new Error("Module 6 theme 3 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("Prosím si dve jablká.");
  expect(JSON.stringify(lesson)).toContain("Koľko stojí toto tričko?");
  expect(JSON.stringify(lesson)).toContain("Môžem platiť kartou?");

  await mockStateApi(page, createState({
    activeModule: 6,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Покупки и еда" }).click();
  await page.getByRole("button").filter({ hasText: lesson.title }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Диалог покупки и частые ошибки");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 3");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const functionTask = page.locator(".course-reinforcement fieldset").nth(0);
  const functionRows = functionTask.locator(".course-pair-row");
  await expect(functionRows).toHaveCount(5);
  const functionPositions = await functionRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(functionPositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === functionPositions[0][index]))).toBe(true);

  const quantityTask = page.locator(".course-reinforcement fieldset").nth(2);
  const quantityRows = quantityTask.locator(".course-pair-row");
  const quantityButton = quantityTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(quantityButton).toBeDisabled();
  for (const [index, answer] of ["jeden", "jednu", "dva", "dve"].entries()) {
    await quantityRows.nth(index).getByRole("button", { name: answer, exact: true }).click();
  }
  await expect(quantityButton).toBeDisabled();
  await quantityRows.nth(4).getByRole("button", { name: "päť", exact: true }).click();
  await quantityButton.click();
  await expect(quantityTask).toHaveClass(/correct/);
  const quantityPositions = await quantityRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(quantityPositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === quantityPositions[0][index]))).toBe(true);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  await translationRows.nth(0).getByRole("textbox").fill("Máte čerstvý chlieb?");
  await translationRows.nth(1).getByRole("textbox").fill("Dve jablká, prosím.");
  await translationRows.nth(2).getByRole("textbox").fill("Kolko stoji toto tricko?");
  await translationRows.nth(3).getByRole("textbox").fill("Môžem zaplatiť kartou?");
  await translationRows.nth(4).getByRole("textbox").fill("Ďakujem.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(translationRows.nth(2)).toHaveClass(/incorrect/);
  await expect(translationRows.nth(2)).toContainText("Правильно: Koľko stojí toto tričko?");
  await translationRows.nth(2).getByRole("textbox").fill("Koľko stojí toto tričko?");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 6 theme 4 teaches food preferences and checks key forms row by row", async ({ page }) => {
  const lesson = module6.lessons.find((item) => item.slug === "food");
  if (!lesson) throw new Error("Food lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m6-food-step-5");
  if (!lastPractice) throw new Error("Module 6 theme 4 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("Mám rád zeleninu.");
  expect(JSON.stringify(lesson)).toContain("Chutí mi táto polievka.");
  expect(JSON.stringify(lesson)).toContain("Na raňajky jem chlieb a syr.");
  expect(JSON.stringify(lesson)).toContain("Nepijem mlieko.");

  await mockStateApi(page, createState({
    activeModule: 6,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Покупки и еда" }).click();
  await page.getByRole("button").filter({ hasText: lesson.title }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Короткий рассказ и частые ошибки");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 4");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const categoryTask = page.locator(".course-reinforcement fieldset").nth(0);
  const categoryRows = categoryTask.locator(".course-pair-row");
  await expect(categoryRows).toHaveCount(5);
  const categoryPositions = await categoryRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(categoryPositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === categoryPositions[0][index]))).toBe(true);

  const formTask = page.locator(".course-reinforcement fieldset").nth(2);
  const formRows = formTask.locator(".course-pair-row");
  const formButton = formTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(formButton).toBeDisabled();
  for (const [index, answer] of ["rád", "rada", "chutí", "nechutí"].entries()) {
    await formRows.nth(index).getByRole("button", { name: answer, exact: true }).click();
  }
  await expect(formButton).toBeDisabled();
  await formRows.nth(4).getByRole("button", { name: "nepijem", exact: true }).click();
  await formButton.click();
  await expect(formTask).toHaveClass(/correct/);
  const formPositions = await formRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(formPositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === formPositions[0][index]))).toBe(true);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  await translationRows.nth(0).getByRole("textbox").fill("Na raňajky jem chlieb a syr.");
  await translationRows.nth(1).getByRole("textbox").fill("Zeleninu mám rád.");
  await translationRows.nth(2).getByRole("textbox").fill("Chuti mi tato polievka.");
  await translationRows.nth(3).getByRole("textbox").fill("Mlieko nepijem.");
  await translationRows.nth(4).getByRole("textbox").fill("Mám rada kávu.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(translationRows.nth(2)).toHaveClass(/incorrect/);
  await expect(translationRows.nth(2)).toContainText("Правильно: Chutí mi táto polievka.");
  await translationRows.nth(2).getByRole("textbox").fill("Chutí mi táto polievka.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 6 theme 5 teaches a restaurant dialogue and checks polite forms row by row", async ({ page }) => {
  const lesson = module6.lessons.find((item) => item.slug === "restaurant");
  if (!lesson) throw new Error("Restaurant lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m6-restaurant-step-5");
  if (!lastPractice) throw new Error("Module 6 theme 5 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("Prosím si denné menu.");
  expect(JSON.stringify(lesson)).toContain("Čo obsahuje táto polievka?");
  expect(JSON.stringify(lesson)).toContain("Kávu bez cukru, prosím.");
  expect(JSON.stringify(lesson)).toContain("Môžeme dostať účet?");

  await mockStateApi(page, createState({
    activeModule: 6,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Покупки и еда" }).click();
  await page.getByRole("button").filter({ hasText: lesson.title }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Счёт, оплата и частые ошибки");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 5");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const menuTask = page.locator(".course-reinforcement fieldset").nth(0);
  const menuRows = menuTask.locator(".course-pair-row");
  await expect(menuRows).toHaveCount(5);
  const menuPositions = await menuRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(menuPositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === menuPositions[0][index]))).toBe(true);

  const formTask = page.locator(".course-reinforcement fieldset").nth(2);
  const formRows = formTask.locator(".course-pair-row");
  const formButton = formTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(formButton).toBeDisabled();
  for (const [index, answer] of ["Prosím si", "Chcel", "Chcela", "Môžeme"].entries()) {
    await formRows.nth(index).getByRole("button", { name: answer, exact: true }).click();
  }
  await expect(formButton).toBeDisabled();
  await formRows.nth(4).getByRole("button", { name: "Zaplatím", exact: true }).click();
  await formButton.click();
  await expect(formTask).toHaveClass(/correct/);
  const formPositions = await formRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(formPositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === formPositions[0][index]))).toBe(true);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  await translationRows.nth(0).getByRole("textbox").fill("Prosím si denné menu.");
  await translationRows.nth(1).getByRole("textbox").fill("Co obsahuje tato polievka?");
  await translationRows.nth(2).getByRole("textbox").fill("Prosím si kávu bez cukru.");
  await translationRows.nth(3).getByRole("textbox").fill("Účet, prosím.");
  await translationRows.nth(4).getByRole("textbox").fill("Zaplatím kartou.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(translationRows.nth(1)).toHaveClass(/incorrect/);
  await expect(translationRows.nth(1)).toContainText("Правильно: Čo obsahuje táto polievka?");
  await translationRows.nth(1).getByRole("textbox").fill("Čo obsahuje táto polievka?");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 6 theme 6 teaches a transport dialogue and checks route models row by row", async ({ page }) => {
  const lesson = module6.lessons.find((item) => item.slug === "transport");
  if (!lesson) throw new Error("Transport lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m6-transport-step-5");
  if (!lastPractice) throw new Error("Module 6 theme 6 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("Kedy ide vlak do Žiliny?");
  expect(JSON.stringify(lesson)).toContain("Jeden lístok do Trnavy, prosím.");
  expect(JSON.stringify(lesson)).toContain("Autobus odchádza o 8:15.");
  expect(JSON.stringify(lesson)).toContain("Kde je zastávka?");

  await mockStateApi(page, createState({
    activeModule: 6,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Движение, город и расписание" }).click();
  await page.getByRole("button").filter({ hasText: lesson.title }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Диалог поездки и частые ошибки");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 6");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const vocabularyTask = page.locator(".course-reinforcement fieldset").nth(0);
  const vocabularyRows = vocabularyTask.locator(".course-pair-row");
  await expect(vocabularyRows).toHaveCount(5);
  const vocabularyPositions = await vocabularyRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(vocabularyPositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === vocabularyPositions[0][index]))).toBe(true);

  const routeTask = page.locator(".course-reinforcement fieldset").nth(1);
  const routeRows = routeTask.locator(".course-pair-row");
  const routeButton = routeTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(routeButton).toBeDisabled();
  for (const [index, answer] of ["do", "na", "z", "zo"].entries()) {
    await routeRows.nth(index).getByRole("button", { name: answer, exact: true }).click();
  }
  await expect(routeButton).toBeDisabled();
  await routeRows.nth(4).getByRole("button", { name: "pri", exact: true }).click();
  await routeButton.click();
  await expect(routeTask).toHaveClass(/correct/);
  const routePositions = await routeRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(routePositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === routePositions[0][index]))).toBe(true);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  await translationRows.nth(0).getByRole("textbox").fill("Prosím si jeden lístok do Bratislavy.");
  await translationRows.nth(1).getByRole("textbox").fill("Kedy ide vlak do Žiliny?");
  await translationRows.nth(2).getByRole("textbox").fill("Autobus odchádza o 8:15.");
  await translationRows.nth(3).getByRole("textbox").fill("Kde je zastavka?");
  await translationRows.nth(4).getByRole("textbox").fill("Musím prestúpiť?");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(translationRows.nth(3)).toHaveClass(/incorrect/);
  await expect(translationRows.nth(3)).toContainText("Правильно: Kde je zastávka?");
  await translationRows.nth(3).getByRole("textbox").fill("Kde je zastávka?");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 6 theme 7 teaches work and study profiles and checks verbs row by row", async ({ page }) => {
  const lesson = module6.lessons.find((item) => item.slug === "work-study");
  if (!lesson) throw new Error("Work-study lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m6-work-study-step-5");
  if (!lastPractice) throw new Error("Module 6 theme 7 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("Som učiteľka.");
  expect(JSON.stringify(lesson)).toContain("Pracujem v kancelárii.");
  expect(JSON.stringify(lesson)).toContain("Študujem slovenčinu.");
  expect(JSON.stringify(lesson)).toContain("O koľkej začínaš pracovať?");

  await mockStateApi(page, createState({
    activeModule: 6,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Работа, досуг и самочувствие" }).click();
  await page.getByRole("button").filter({ hasText: lesson.title }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Короткий профиль и частые ошибки");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 7");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const professionTask = page.locator(".course-reinforcement fieldset").nth(0);
  const professionRows = professionTask.locator(".course-pair-row");
  await expect(professionRows).toHaveCount(5);
  const professionPositions = await professionRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(professionPositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === professionPositions[0][index]))).toBe(true);

  const verbTask = page.locator(".course-reinforcement fieldset").nth(2);
  const verbRows = verbTask.locator(".course-pair-row");
  const verbButton = verbTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(verbButton).toBeDisabled();
  for (const [index, answer] of ["učím", "píšem", "pracujem", "študujem"].entries()) {
    await verbRows.nth(index).getByRole("button", { name: answer, exact: true }).click();
  }
  await expect(verbButton).toBeDisabled();
  await verbRows.nth(4).getByRole("button", { name: "začínam", exact: true }).click();
  await verbButton.click();
  await expect(verbTask).toHaveClass(/correct/);
  const verbPositions = await verbRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(verbPositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === verbPositions[0][index]))).toBe(true);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  await translationRows.nth(0).getByRole("textbox").fill("Som učiteľka.");
  await translationRows.nth(1).getByRole("textbox").fill("V kancelárii pracujem.");
  await translationRows.nth(2).getByRole("textbox").fill("Studujem slovencinu.");
  await translationRows.nth(3).getByRole("textbox").fill("O koľkej začínaš pracovať?");
  await translationRows.nth(4).getByRole("textbox").fill("V škole pracujem.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(translationRows.nth(2)).toHaveClass(/incorrect/);
  await expect(translationRows.nth(2)).toContainText("Правильно: Študujem slovenčinu.");
  await translationRows.nth(2).getByRole("textbox").fill("Študujem slovenčinu.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 6 theme 8 teaches hobbies and checks dialogue forms row by row", async ({ page }) => {
  const lesson = module6.lessons.find((item) => item.slug === "hobbies");
  if (!lesson) throw new Error("Hobbies lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m6-hobbies-step-5");
  if (!lastPractice) throw new Error("Module 6 theme 8 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("Vo voľnom čase čítam.");
  expect(JSON.stringify(lesson)).toContain("Rada počúvam hudbu.");
  expect(JSON.stringify(lesson)).toContain("Dvakrát týždenne športujem.");
  expect(JSON.stringify(lesson)).toContain("Chceš ísť do kina?");

  await mockStateApi(page, createState({
    activeModule: 6,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Работа, досуг и самочувствие" }).click();
  await page.getByRole("button").filter({ hasText: lesson.title }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Короткий диалог и частые ошибки");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 8");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const actionTask = page.locator(".course-reinforcement fieldset").nth(0);
  const actionRows = actionTask.locator(".course-pair-row");
  await expect(actionRows).toHaveCount(5);
  const actionPositions = await actionRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(actionPositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === actionPositions[0][index]))).toBe(true);

  const dialogueTask = page.locator(".course-reinforcement fieldset").nth(2);
  const dialogueRows = dialogueTask.locator(".course-pair-row");
  const dialogueButton = dialogueTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(dialogueButton).toBeDisabled();
  for (const [index, answer] of ["Chceš", "Môžeme", "Áno", "Kedy"].entries()) {
    await dialogueRows.nth(index).getByRole("button", { name: answer, exact: true }).click();
  }
  await expect(dialogueButton).toBeDisabled();
  await dialogueRows.nth(4).getByRole("button", { name: "Prepáč", exact: true }).click();
  await dialogueButton.click();
  await expect(dialogueTask).toHaveClass(/correct/);
  const dialoguePositions = await dialogueRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(dialoguePositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === dialoguePositions[0][index]))).toBe(true);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  await translationRows.nth(0).getByRole("textbox").fill("Vo voľnom čase čítam.");
  await translationRows.nth(1).getByRole("textbox").fill("Hudbu počúvam rada.");
  await translationRows.nth(2).getByRole("textbox").fill("Dvakrat tyzdenne sportujem.");
  await translationRows.nth(3).getByRole("textbox").fill("Chceš ísť do kina?");
  await translationRows.nth(4).getByRole("textbox").fill("Prepáč, nemôžem.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(translationRows.nth(2)).toHaveClass(/incorrect/);
  await expect(translationRows.nth(2)).toContainText("Правильно: Dvakrát týždenne športujem.");
  await translationRows.nth(2).getByRole("textbox").fill("Športujem dvakrát týždenne.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 6 theme 9 teaches time and routine and checks clock forms row by row", async ({ page }) => {
  const lesson = module6.lessons.find((item) => item.slug === "time-routine");
  if (!lesson) throw new Error("Time-routine lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m6-time-routine-step-5");
  if (!lastPractice) throw new Error("Module 6 theme 9 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("Vstávam o siedmej.");
  expect(JSON.stringify(lesson)).toContain("O pol ôsmej raňajkujem.");
  expect(JSON.stringify(lesson)).toContain("Potom idem do práce.");
  expect(JSON.stringify(lesson)).toContain("Večer sa učím po slovensky.");

  await mockStateApi(page, createState({
    activeModule: 6,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Движение, город и расписание" }).click();
  await page.getByRole("button").filter({ hasText: lesson.title }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Мой день и частые ошибки");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 9");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const hourTask = page.locator(".course-reinforcement fieldset").nth(0);
  const hourRows = hourTask.locator(".course-pair-row");
  await expect(hourRows).toHaveCount(5);
  const hourPositions = await hourRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(hourPositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === hourPositions[0][index]))).toBe(true);

  const clockTask = page.locator(".course-reinforcement fieldset").nth(2);
  const clockRows = clockTask.locator(".course-pair-row");
  const clockButton = clockTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(clockButton).toBeDisabled();
  for (const [index, answer] of ["o šiestej", "o pol siedmej", "o siedmej", "o pol ôsmej"].entries()) {
    await clockRows.nth(index).getByRole("button", { name: answer, exact: true }).click();
  }
  await expect(clockButton).toBeDisabled();
  await clockRows.nth(4).getByRole("button", { name: "o ôsmej", exact: true }).click();
  await clockButton.click();
  await expect(clockTask).toHaveClass(/correct/);
  const clockPositions = await clockRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(clockPositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === clockPositions[0][index]))).toBe(true);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  await translationRows.nth(0).getByRole("textbox").fill("O siedmej vstávam.");
  await translationRows.nth(1).getByRole("textbox").fill("O pol osmej ranajkujem.");
  await translationRows.nth(2).getByRole("textbox").fill("Potom idem do práce.");
  await translationRows.nth(3).getByRole("textbox").fill("Večer sa učím po slovensky.");
  await translationRows.nth(4).getByRole("textbox").fill("Najprv pracujem, potom oddychujem.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(translationRows.nth(1)).toHaveClass(/incorrect/);
  await expect(translationRows.nth(1)).toContainText("Правильно: O pol ôsmej raňajkujem.");
  await translationRows.nth(1).getByRole("textbox").fill("Raňajkujem o pol ôsmej.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 6 theme 10 teaches meeting schedules and checks dates row by row", async ({ page }) => {
  const lesson = module6.lessons.find((item) => item.slug === "meeting-schedule");
  if (!lesson) throw new Error("Meeting-schedule lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m6-meeting-schedule-step-5");
  if (!lastPractice) throw new Error("Module 6 theme 10 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("Kedy sa stretneme?");
  expect(JSON.stringify(lesson)).toContain("V piatok o šiestej.");
  expect(JSON.stringify(lesson)).toContain("Stretneme sa pred kinom.");
  expect(JSON.stringify(lesson)).toContain("Dobre, platí.");

  await mockStateApi(page, createState({
    activeModule: 6,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Движение, город и расписание" }).click();
  await page.getByRole("button").filter({ hasText: lesson.title }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Полная договорённость и частые ошибки");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 10");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const functionTask = page.locator(".course-reinforcement fieldset").nth(0);
  const functionRows = functionTask.locator(".course-pair-row");
  const functionButton = functionTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(functionRows).toHaveCount(5);
  await expect(functionButton).toBeDisabled();
  for (const [index, answer] of ["Kedy", "O koľkej", "Kde", "Môžeš"].entries()) {
    await functionRows.nth(index).getByRole("button", { name: answer, exact: true }).click();
  }
  await expect(functionButton).toBeDisabled();
  await functionRows.nth(4).getByRole("button", { name: "Platí", exact: true }).click();
  await functionButton.click();
  await expect(functionTask).toHaveClass(/correct/);
  const functionPositions = await functionRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(functionPositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === functionPositions[0][index]))).toBe(true);

  const dateTask = page.locator(".course-reinforcement fieldset").nth(2);
  const dateRows = dateTask.locator(".course-pair-row");
  await expect(dateRows).toHaveCount(5);
  const datePositions = await dateRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(datePositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === datePositions[0][index]))).toBe(true);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  await translationRows.nth(0).getByRole("textbox").fill("Kedy sa stretneme?");
  await translationRows.nth(1).getByRole("textbox").fill("V piatok o siestej.");
  await translationRows.nth(2).getByRole("textbox").fill("Pred kinom sa stretneme.");
  await translationRows.nth(3).getByRole("textbox").fill("Vtedy nemôžem.");
  await translationRows.nth(4).getByRole("textbox").fill("Zajtra o piatej sa stretneme.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(translationRows.nth(1)).toHaveClass(/incorrect/);
  await expect(translationRows.nth(1)).toContainText("Правильно: V piatok o šiestej.");
  await translationRows.nth(1).getByRole("textbox").fill("V piatok o šiestej.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 6 theme 11 teaches neutral people descriptions and checks agreement row by row", async ({ page }) => {
  const lesson = module6.lessons.find((item) => item.slug === "people-description");
  if (!lesson) throw new Error("People-description lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m6-people-description-step-5");
  if (!lastPractice) throw new Error("Module 6 theme 11 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("Je vysoký a má krátke vlasy.");
  expect(JSON.stringify(lesson)).toContain("Má modré oči.");
  expect(JSON.stringify(lesson)).toContain("Nosí okuliare.");
  expect(JSON.stringify(lesson)).toContain("Je milá a pokojná.");

  await mockStateApi(page, createState({
    activeModule: 6,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Люди и дом" }).click();
  await page.getByRole("button").filter({ hasText: lesson.title }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Короткий профиль и частые ошибки");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 11");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const masculineTask = page.locator(".course-reinforcement fieldset").nth(0);
  const masculineRows = masculineTask.locator(".course-pair-row");
  await expect(masculineRows).toHaveCount(5);
  const masculinePositions = await masculineRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(masculinePositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === masculinePositions[0][index]))).toBe(true);

  const verbTask = page.locator(".course-reinforcement fieldset").nth(2);
  const verbRows = verbTask.locator(".course-pair-row");
  const verbButton = verbTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(verbButton).toBeDisabled();
  for (const [index, answer] of ["je", "má", "má", "nosí"].entries()) {
    await verbRows.nth(index).getByRole("button", { name: answer, exact: true }).click();
  }
  await expect(verbButton).toBeDisabled();
  await verbRows.nth(4).getByRole("button", { name: "nenosí", exact: true }).click();
  await verbButton.click();
  await expect(verbTask).toHaveClass(/correct/);
  const verbPositions = await verbRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(verbPositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === verbPositions[0][index]))).toBe(true);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  await translationRows.nth(0).getByRole("textbox").fill("Má krátke vlasy a je vysoký.");
  await translationRows.nth(1).getByRole("textbox").fill("Ma modre oci.");
  await translationRows.nth(2).getByRole("textbox").fill("Nosí okuliare.");
  await translationRows.nth(3).getByRole("textbox").fill("Je pokojná a milá.");
  await translationRows.nth(4).getByRole("textbox").fill("Je mladá a veľmi milá.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(translationRows.nth(1)).toHaveClass(/incorrect/);
  await expect(translationRows.nth(1)).toContainText("Правильно: Má modré oči.");
  await translationRows.nth(1).getByRole("textbox").fill("Má modré oči.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 6 theme 12 teaches city places and checks short routes row by row", async ({ page }) => {
  const lesson = module6.lessons.find((item) => item.slug === "city-places");
  if (!lesson) throw new Error("City-places lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m6-city-places-step-5");
  if (!lastPractice) throw new Error("Module 6 theme 12 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("Kde je najbližšia lekáreň?");
  expect(JSON.stringify(lesson)).toContain("Ako sa dostanem na námestie?");
  expect(JSON.stringify(lesson)).toContain("Pošta je vedľa banky.");
  expect(JSON.stringify(lesson)).toContain("Choďte rovno a potom vľavo.");

  await mockStateApi(page, createState({
    activeModule: 6,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Движение, город и расписание" }).click();
  await page.getByRole("button").filter({ hasText: lesson.title }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Диалог о дороге и частые ошибки");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 12");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const placeTask = page.locator(".course-reinforcement fieldset").nth(0);
  const placeRows = placeTask.locator(".course-pair-row");
  await expect(placeRows).toHaveCount(5);
  const placePositions = await placeRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(placePositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === placePositions[0][index]))).toBe(true);

  const routeTask = page.locator(".course-reinforcement fieldset").nth(2);
  const routeRows = routeTask.locator(".course-pair-row");
  const routeButton = routeTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(routeButton).toBeDisabled();
  for (const [index, answer] of ["rovno", "vľavo", "vpravo", "cez"].entries()) {
    await routeRows.nth(index).getByRole("button", { name: answer, exact: true }).click();
  }
  await expect(routeButton).toBeDisabled();
  await routeRows.nth(4).getByRole("button", { name: "pri", exact: true }).click();
  await routeButton.click();
  await expect(routeTask).toHaveClass(/correct/);
  const routePositions = await routeRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(routePositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === routePositions[0][index]))).toBe(true);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  await translationRows.nth(0).getByRole("textbox").fill("Kde je najbližšia lekáreň?");
  await translationRows.nth(1).getByRole("textbox").fill("Ako sa dostanem na namestie?");
  await translationRows.nth(2).getByRole("textbox").fill("Vedľa banky je pošta.");
  await translationRows.nth(3).getByRole("textbox").fill("Choďte rovno, potom vľavo.");
  await translationRows.nth(4).getByRole("textbox").fill("Oproti banke je lekáreň.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(translationRows.nth(1)).toHaveClass(/incorrect/);
  await expect(translationRows.nth(1)).toContainText("Правильно: Ako sa dostanem na námestie?");
  await translationRows.nth(1).getByRole("textbox").fill("Ako sa dostanem na námestie?");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 6 theme 13 teaches health communication and checks advice row by row", async ({ page }) => {
  const lesson = module6.lessons.find((item) => item.slug === "health");
  if (!lesson) throw new Error("Health lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m6-health-step-5");
  if (!lastPractice) throw new Error("Module 6 theme 13 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("Bolí ma hlava.");
  expect(JSON.stringify(lesson)).toContain("Mám teplotu.");
  expect(JSON.stringify(lesson)).toContain("Je mi zle.");
  expect(JSON.stringify(lesson)).toContain("Musíte veľa piť a oddychovať.");

  await mockStateApi(page, createState({
    activeModule: 6,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Работа, досуг и самочувствие" }).click();
  await page.getByRole("button").filter({ hasText: lesson.title }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Диалог с врачом и частые ошибки");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 13");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const bodyTask = page.locator(".course-reinforcement fieldset").nth(0);
  const bodyRows = bodyTask.locator(".course-pair-row");
  await expect(bodyRows).toHaveCount(5);
  const bodyPositions = await bodyRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(bodyPositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === bodyPositions[0][index]))).toBe(true);

  const adviceTask = page.locator(".course-reinforcement fieldset").nth(2);
  const adviceRows = adviceTask.locator(".course-pair-row");
  const adviceButton = adviceTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(adviceButton).toBeDisabled();
  for (const [index, answer] of ["oddychujte", "pite", "choďte", "zostaňte"].entries()) {
    await adviceRows.nth(index).getByRole("button", { name: answer, exact: true }).click();
  }
  await expect(adviceButton).toBeDisabled();
  await adviceRows.nth(4).getByRole("button", { name: "zavolajte", exact: true }).click();
  await adviceButton.click();
  await expect(adviceTask).toHaveClass(/correct/);
  const advicePositions = await adviceRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(advicePositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === advicePositions[0][index]))).toBe(true);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  await translationRows.nth(0).getByRole("textbox").fill("Hlava ma bolí.");
  await translationRows.nth(1).getByRole("textbox").fill("Mám teplotu.");
  await translationRows.nth(2).getByRole("textbox").fill("Je mi zle.");
  await translationRows.nth(3).getByRole("textbox").fill("Hrdlo ma bolí už dva dni.");
  await translationRows.nth(4).getByRole("textbox").fill("Musite vela pit a oddychovat.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(translationRows.nth(4)).toHaveClass(/incorrect/);
  await expect(translationRows.nth(4)).toContainText("Правильно: Musíte veľa piť a oddychovať.");
  await translationRows.nth(4).getByRole("textbox").fill("Musíte veľa piť a oddychovať.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 6 theme 14 teaches weather and clothes and checks choices row by row", async ({ page }) => {
  const lesson = module6.lessons.find((item) => item.slug === "weather-clothes");
  if (!lesson) throw new Error("Weather and clothes lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m6-weather-clothes-step-5");
  if (!lastPractice) throw new Error("Module 6 theme 14 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("Dnes prší.");
  expect(JSON.stringify(lesson)).toContain("Je desať stupňov.");
  expect(JSON.stringify(lesson)).toContain("Mám na sebe modré nohavice.");
  expect(JSON.stringify(lesson)).toContain("Je mi zima, preto potrebujem bundu.");

  await mockStateApi(page, createState({
    activeModule: 6,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Работа, досуг и самочувствие" }).click();
  await page.getByRole("button").filter({ hasText: lesson.title }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Прогноз, план и частые ошибки");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 14");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const weatherTask = page.locator(".course-reinforcement fieldset").nth(0);
  const weatherRows = weatherTask.locator(".course-pair-row");
  await expect(weatherRows).toHaveCount(5);
  const weatherPositions = await weatherRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(weatherPositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === weatherPositions[0][index]))).toBe(true);

  const choiceTask = page.locator(".course-reinforcement fieldset").nth(2);
  const choiceRows = choiceTask.locator(".course-pair-row");
  const choiceButton = choiceTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(choiceButton).toBeDisabled();
  for (const [index, answer] of ["dáždnik", "bundu", "kabát", "okuliare"].entries()) {
    await choiceRows.nth(index).getByRole("button", { name: answer, exact: true }).click();
  }
  await expect(choiceButton).toBeDisabled();
  await choiceRows.nth(4).getByRole("button", { name: "tričko", exact: true }).click();
  await choiceButton.click();
  await expect(choiceTask).toHaveClass(/correct/);
  const choicePositions = await choiceRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(choicePositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === choicePositions[0][index]))).toBe(true);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  await translationRows.nth(0).getByRole("textbox").fill("Dnes je slnečno a teplo.");
  await translationRows.nth(1).getByRole("textbox").fill("Prsi a fuka vietor.");
  await translationRows.nth(2).getByRole("textbox").fill("Je 10 stupňov.");
  await translationRows.nth(3).getByRole("textbox").fill("Mám na sebe modré nohavice.");
  await translationRows.nth(4).getByRole("textbox").fill("Je mi zima, preto potrebujem bundu.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(translationRows.nth(1)).toHaveClass(/incorrect/);
  await expect(translationRows.nth(1)).toContainText("Правильно: Prší a fúka vietor.");
  await translationRows.nth(1).getByRole("textbox").fill("Prší a fúka vietor.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 6 theme 15 teaches forms and checks contact data row by row", async ({ page }) => {
  const lesson = module6.lessons.find((item) => item.slug === "forms-contact-details");
  if (!lesson) throw new Error("Forms and contact details lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m6-forms-contact-details-step-5");
  if (!lastPractice) throw new Error("Module 6 theme 15 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("Dátum narodenia: 12. 5. 2000");
  expect(JSON.stringify(lesson)).toContain("Adresa: Hlavná 15, Košice");
  expect(JSON.stringify(lesson)).toContain("Moje telefónne číslo je 0900 123 456.");
  expect(JSON.stringify(lesson)).toContain("Môj e-mail je anna.nova@example.sk.");

  await mockStateApi(page, createState({
    activeModule: 6,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Практические тексты и сообщения" }).click();
  await page.getByRole("button").filter({ hasText: lesson.title }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Уточнение, проверка и безопасность");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 15");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const identityTask = page.locator(".course-reinforcement fieldset").nth(0);
  const identityRows = identityTask.locator(".course-pair-row");
  await expect(identityRows).toHaveCount(5);
  const identityPositions = await identityRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(identityPositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === identityPositions[0][index]))).toBe(true);

  const sampleTask = page.locator(".course-reinforcement fieldset").nth(2);
  const sampleRows = sampleTask.locator(".course-pair-row");
  const sampleButton = sampleTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(sampleButton).toBeDisabled();
  for (const [index, answer] of ["Anna", "Nová", "12. 5. 2000", "Košice"].entries()) {
    await sampleRows.nth(index).getByRole("button", { name: answer, exact: true }).click();
  }
  await expect(sampleButton).toBeDisabled();
  await sampleRows.nth(4).getByRole("button", { name: "040 01", exact: true }).click();
  await sampleButton.click();
  await expect(sampleTask).toHaveClass(/correct/);
  const samplePositions = await sampleRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(samplePositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === samplePositions[0][index]))).toBe(true);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  await translationRows.nth(0).getByRole("textbox").fill("Moje meno je Anna Nová.");
  await translationRows.nth(1).getByRole("textbox").fill("Môj dátum narodenia je 12. 5. 2000.");
  await translationRows.nth(2).getByRole("textbox").fill("Moja adresa je Hlavná 15, Košice.");
  await translationRows.nth(3).getByRole("textbox").fill("Moje telefonne cislo je 0900 123 456.");
  await translationRows.nth(4).getByRole("textbox").fill("Môj e-mail je anna.nova@example.sk.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(translationRows.nth(3)).toHaveClass(/incorrect/);
  await expect(translationRows.nth(3)).toContainText("Правильно: Moje telefónne číslo je 0900 123 456.");
  await translationRows.nth(3).getByRole("textbox").fill("Moje telefónne číslo je 0900 123 456.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 6 theme 16 teaches personal messages and checks structure row by row", async ({ page }) => {
  const lesson = module6.lessons.find((item) => item.slug === "personal-message");
  if (!lesson) throw new Error("Personal message lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m6-personal-message-step-5");
  if (!lastPractice) throw new Error("Module 6 theme 16 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("Ahoj, Nina!");
  expect(JSON.stringify(lesson)).toContain("Dnes nemôžem prísť.");
  expect(JSON.stringify(lesson)).toContain("Prepáč, meškám desať minút.");
  expect(JSON.stringify(lesson)).toContain("Stretneme sa zajtra o piatej pred kinom?");

  await mockStateApi(page, createState({
    activeModule: 6,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Практические тексты и сообщения" }).click();
  await page.getByRole("button").filter({ hasText: lesson.title }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Цельное сообщение и частые ошибки");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 16");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const greetingTask = page.locator(".course-reinforcement fieldset").nth(0);
  const greetingRows = greetingTask.locator(".course-pair-row");
  await expect(greetingRows).toHaveCount(5);
  const greetingPositions = await greetingRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(greetingPositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === greetingPositions[0][index]))).toBe(true);

  const structureTask = page.locator(".course-reinforcement fieldset").nth(2);
  const structureRows = structureTask.locator(".course-pair-row");
  const structureButton = structureTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(structureButton).toBeDisabled();
  for (const [index, answer] of ["Ahoj, Nina!", "Dnes nemôžem prísť.", "Som chorá.", "Stretneme sa v piatok?"].entries()) {
    await structureRows.nth(index).getByRole("button", { name: answer, exact: true }).click();
  }
  await expect(structureButton).toBeDisabled();
  await structureRows.nth(4).getByRole("button", { name: "Maj sa!", exact: true }).click();
  await structureButton.click();
  await expect(structureTask).toHaveClass(/correct/);
  const structurePositions = await structureRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(structurePositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === structurePositions[0][index]))).toBe(true);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  await translationRows.nth(0).getByRole("textbox").fill("Ahoj, Nina!");
  await translationRows.nth(1).getByRole("textbox").fill("Dnes nemozem prist.");
  await translationRows.nth(2).getByRole("textbox").fill("Prepáč, meškám desať minút.");
  await translationRows.nth(3).getByRole("textbox").fill("Zajtra o piatej sa stretneme pred kinom?");
  await translationRows.nth(4).getByRole("textbox").fill("Ďakujem a maj sa!");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(translationRows.nth(1)).toHaveClass(/incorrect/);
  await expect(translationRows.nth(1)).toContainText("Правильно: Dnes nemôžem prísť.");
  await translationRows.nth(1).getByRole("textbox").fill("Dnes nemôžem prísť.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 6 theme 17 teaches practical texts and checks timetable facts row by row", async ({ page }) => {
  const lesson = module6.lessons.find((item) => item.slug === "notices-menus-timetables");
  if (!lesson) throw new Error("Notices, menus, and timetables lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m6-notices-menus-timetables-step-5");
  if (!lastPractice) throw new Error("Module 6 theme 17 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("Otvorené: 9:00–18:00");
  expect(JSON.stringify(lesson)).toContain("Dnes zatvorené.");
  expect(JSON.stringify(lesson)).toContain("Denné menu: 7,90 €");
  expect(JSON.stringify(lesson)).toContain("Vlak mešká 10 minút.");

  await mockStateApi(page, createState({
    activeModule: 6,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Практические тексты и сообщения" }).click();
  await page.getByRole("button").filter({ hasText: lesson.title }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Алгоритм чтения и частые ошибки");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 17");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const typeTask = page.locator(".course-reinforcement fieldset").nth(0);
  const typeRows = typeTask.locator(".course-pair-row");
  await expect(typeRows).toHaveCount(5);
  const typePositions = await typeRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(typePositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === typePositions[0][index]))).toBe(true);

  const timetableTask = page.locator(".course-reinforcement fieldset").nth(3);
  const timetableRows = timetableTask.locator(".course-pair-row");
  const timetableButton = timetableTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(timetableButton).toBeDisabled();
  for (const [index, answer] of ["R 603", "8:15", "9:05", "2"].entries()) {
    await timetableRows.nth(index).getByRole("button", { name: answer, exact: true }).click();
  }
  await expect(timetableButton).toBeDisabled();
  await timetableRows.nth(4).getByRole("button", { name: "10 minút", exact: true }).click();
  await timetableButton.click();
  await expect(timetableTask).toHaveClass(/correct/);
  const timetablePositions = await timetableRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(timetablePositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === timetablePositions[0][index]))).toBe(true);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  await translationRows.nth(0).getByRole("textbox").fill("Dnes zatvorené.");
  await translationRows.nth(1).getByRole("textbox").fill("Od deviatej do osemnástej je otvorené.");
  await translationRows.nth(2).getByRole("textbox").fill("Denne menu stoji 7,90 €.");
  await translationRows.nth(3).getByRole("textbox").fill("Vlak mešká 10 minút.");
  await translationRows.nth(4).getByRole("textbox").fill("Vstup zakázaný.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(translationRows.nth(2)).toHaveClass(/incorrect/);
  await expect(translationRows.nth(2)).toContainText("Правильно: Denné menu stojí 7,90 €.");
  await translationRows.nth(2).getByRole("textbox").fill("Denné menu stojí 7,90 €.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 6 theme 18 teaches short spoken messages and checks key facts row by row", async ({ page }) => {
  const lesson = module6.lessons.find((item) => item.slug === "short-listening");
  if (!lesson) throw new Error("Short spoken messages lesson is missing");
  const lastPractice = lesson.stepPractices.find((practice) => practice.id === "m6-short-listening-step-5");
  if (!lastPractice) throw new Error("Module 6 theme 18 step 5 practice is missing");
  expect(lesson.sections).toHaveLength(5);
  expect(lesson.stepPractices).toHaveLength(5);
  expect(lesson.reinforcementPractices).toHaveLength(6);
  expect(JSON.stringify(lesson)).toContain("Autobus číslo päť príde o desať minút.");
  expect(JSON.stringify(lesson)).toContain("Lekáreň je dnes otvorená do šiestej.");
  expect(JSON.stringify(lesson)).toContain("Stretneme sa na stanici.");
  expect(JSON.stringify(lesson)).toContain("Prosím, čakajte pri dverách.");

  await mockStateApi(page, createState({
    activeModule: 6,
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: 4 },
    practiceAnswers: { [lastPractice.id]: lastPractice.answer },
    practiceResults: { [lastPractice.id]: true },
  }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;

  await page.locator(".course-group-card").filter({ hasText: "Практические тексты и сообщения" }).click();
  await page.getByRole("button").filter({ hasText: lesson.title }).first().click();
  await expect(page.locator(".course-stepper")).toContainText("Шаг 5 из 5");
  await expect(page.locator(".course-content-heading h4")).toHaveText("Повторное слушание и частые ошибки");
  await page.getByRole("button", { name: "Перейти к финальному тесту →" }).click();

  await expect(page.locator(".course-current-task")).toContainText("Выполните шесть заданий темы 18");
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  const situationTask = page.locator(".course-reinforcement fieldset").nth(0);
  const situationRows = situationTask.locator(".course-pair-row");
  await expect(situationRows).toHaveCount(5);
  const situationPositions = await situationRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(situationPositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === situationPositions[0][index]))).toBe(true);

  const actionTask = page.locator(".course-reinforcement fieldset").nth(3);
  const actionRows = actionTask.locator(".course-pair-row");
  const actionButton = actionTask.getByRole("button", { name: "Проверить", exact: true });
  await expect(actionButton).toBeDisabled();
  for (const [index, answer] of ["príde", "čakajte", "odchádza", "stretneme sa"].entries()) {
    await actionRows.nth(index).getByRole("button", { name: answer, exact: true }).click();
  }
  await expect(actionButton).toBeDisabled();
  await actionRows.nth(4).getByRole("button", { name: "zopakujte", exact: true }).click();
  await actionButton.click();
  await expect(actionTask).toHaveClass(/correct/);
  const actionPositions = await actionRows.evaluateAll((rows) => rows.map((row) => Array.from(row.querySelectorAll("button"), (button) => Math.round(button.getBoundingClientRect().x))));
  expect(actionPositions.every((positions) => positions.length === 5 && positions.every((position, index) => position === actionPositions[0][index]))).toBe(true);

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  const translationRows = translationTask.locator(".course-pair-row");
  await translationRows.nth(0).getByRole("textbox").fill("O desať minút príde autobus číslo päť.");
  await translationRows.nth(1).getByRole("textbox").fill("Lekaren je dnes otvorena do siestej.");
  await translationRows.nth(2).getByRole("textbox").fill("Stretneme sa na stanici.");
  await translationRows.nth(3).getByRole("textbox").fill("Prosím, čakajte pri dverách.");
  await translationRows.nth(4).getByRole("textbox").fill("Vlak odchádza o ôsmej.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask.locator(".course-pair-row.correct")).toHaveCount(4);
  await expect(translationRows.nth(1)).toHaveClass(/incorrect/);
  await expect(translationRows.nth(1)).toContainText("Правильно: Lekáreň je dnes otvorená do šiestej.");
  await translationRows.nth(1).getByRole("textbox").fill("Lekáreň je dnes otvorená do šiestej.");
  await translationTask.getByRole("button", { name: "Проверить", exact: true }).click();
  await expect(translationTask).toHaveClass(/correct/);
});

test("Module 6 opens as five topic groups and restores saved progress", async ({ page }) => {
  const lesson = module6.lessons[14];
  await mockStateApi(page, createState({ activeModule: 6, selectedSlug: lesson.slug, progress: { [lesson.slug]: "in_progress" }, lessonSteps: { [lesson.slug]: 2 } }));
  const restored = page.waitForResponse((response) => response.url().includes("/api/v1/course/state") && response.request().method() === "GET");
  await page.goto("/");
  await restored;
  await expect(page.getByRole("heading", { name: module6.title })).toBeVisible();
  await expect(page.getByLabel("Выберите учебный модуль")).toHaveValue("6");
  await expect(page.locator(".course-group-card")).toHaveCount(5);
  const group = module6.topicGroups?.find((item) => item.lessonSlugs.includes(lesson.slug));
  if (!group) throw new Error(`Lesson ${lesson.slug} is not assigned to Module 6`);
  await page.locator(".course-group-card").filter({ hasText: group.title }).click();
  const lessonButton = page.getByRole("button", { name: new RegExp(lesson.title) }).first();
  await expect(lessonButton).toContainText("В процессе");
  await lessonButton.click();
  await expect(page.locator(".course-practice")).toBeVisible();
});

test("lesson reinforcement is deterministic and does not call AI", async ({ page }) => {
  const lesson = module1.lessons[0];
  await mockStateApi(page, createState({
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: lesson.sections.length },
    checkSelections: Object.fromEntries(lesson.knowledgeChecks.map((check) => [check.id, check.answer])),
  }));

  let aiCalls = 0;
  await page.route("**/api/v1/tutor/module1-chat", async (route) => {
    aiCalls += 1;
    await route.abort();
  });

  await openCourse(page);
  await openLesson(page, lesson);

  const finish = page.getByRole("button", { name: "Завершить задания и получить итог →" });
  const checkAll = page.getByRole("button", { name: "Проверить всё" });
  await expect(page.locator(".course-current-task")).toBeHidden();
  await expect(page.locator(".course-reinforcement fieldset")).toHaveCount(6);
  await expect(page.locator(".course-reinforcement fieldset").nth(2).locator(".course-pair-row")).toHaveCount(4);
  await expect(page.locator(".course-reinforcement fieldset").nth(4).locator(".course-pair-row")).toHaveCount(6);
  await expect(page.locator(".course-reinforcement fieldset").nth(4).getByLabel("чай", { exact: true })).toBeVisible();
  const reinforcementTasks = buildReinforcementPractices(lesson);
  const normalizedAnswers = reinforcementTasks.map((practice) => practice.answer.normalize("NFC").toLocaleLowerCase("sk").replace(/\p{P}+/gu, " ").replace(/\s+/g, " ").trim());
  expect(new Set(normalizedAnswers).size).toBe(6);
  for (const [taskIndex, practice] of reinforcementTasks.entries()) {
    if (practice.type === "order") await expect(page.locator(".course-reinforcement fieldset").nth(taskIndex).locator(".course-check-options button")).not.toHaveCount(1);
  }
  await expect(finish).toBeDisabled();
  await expect(checkAll).toBeDisabled();

  const fieldset = page.locator(".course-reinforcement fieldset").first();
  await fieldset.getByRole("button", { name: "dom", exact: true }).click();
  await fieldset.getByRole("button", { name: "Проверить" }).click();
  await expect(fieldset.getByText(/Пока неверно|Почти/)).toBeVisible();
  await fieldset.getByRole("button", { name: "Очистить" }).click();
  await expect(finish).toBeDisabled();

  const transcriptionTask = page.locator(".course-reinforcement fieldset").nth(2);
  const transcriptionPractice = reinforcementTasks[2];
  for (const pair of transcriptionPractice.pairs ?? []) {
    if (!pair.prompt.startsWith("ja ")) await transcriptionTask.getByLabel(pair.prompt, { exact: true }).fill(pair.answer);
  }
  await expect(transcriptionTask.getByLabel("Словацкие буквы")).toHaveCount(0);
  for (const acceptedJa of ["я", "йа", "я(йа)"]) {
    await transcriptionTask.getByLabel("ja — было «жа»", { exact: true }).fill(acceptedJa);
    await transcriptionTask.getByRole("button", { name: "Проверить" }).click();
    await expect(transcriptionTask).toHaveClass(/correct/);
  }

  const translationTask = page.locator(".course-reinforcement fieldset").nth(4);
  for (const pair of reinforcementTasks[4].pairs ?? []) {
    await translationTask.getByLabel(pair.prompt, { exact: true }).fill(pair.prompt === "чай" ? "caj" : pair.answer);
  }
  await translationTask.getByRole("button", { name: "Проверить" }).click();
  await expect(translationTask.locator(".course-pair-row").first()).toHaveClass(/incorrect/);
  await expect(translationTask.locator(".course-pair-row").first()).toContainText("Правильно: čaj");

  for (const [index, practice] of reinforcementTasks.entries()) {
    const answer = practice.answer;
    const task = page.locator(".course-reinforcement fieldset").nth(index);
    if (practice.type === "choice") {
      const option = task.getByRole("button", { name: answer, exact: true });
      await option.click();
      await expect(option).toHaveClass(/selected/);
    }
    if (practice.type === "text") {
      const input = task.getByPlaceholder("Введите ответ");
      await input.fill(answer);
      await expect(input).toHaveValue(answer);
    }
    if (practice.type === "order") {
      const normalizedAnswer = answer.toLocaleLowerCase("sk").replace(/\p{P}+/gu, " ");
      const orderedTokens = [...(practice.tokens ?? [])]
        .filter((token) => normalizedAnswer.includes(token.toLocaleLowerCase("sk").replace(/\p{P}+/gu, "")))
        .sort((left, right) => normalizedAnswer.indexOf(left.toLocaleLowerCase("sk").replace(/\p{P}+/gu, "")) - normalizedAnswer.indexOf(right.toLocaleLowerCase("sk").replace(/\p{P}+/gu, "")));
      for (const token of orderedTokens) await task.getByRole("button", { name: token, exact: true }).first().click();
    }
    if (practice.type === "pairs") {
      for (const pair of practice.pairs ?? []) {
        if (pair.options?.length) await task.getByRole("button", { name: pair.answer, exact: true }).click();
        else await task.getByLabel(pair.prompt, { exact: true }).fill(pair.answer);
      }
    }
  }
  await expect(checkAll).toBeEnabled();
  await checkAll.click();
  await expect(page.locator(".course-reinforcement fieldset.correct")).toHaveCount(6);
  await expect(finish).toBeEnabled();
  await finish.click();

  await expect(page.getByRole("heading", { name: /понимание|основа|повторение/i })).toBeVisible();
  await expect(page.getByText("закрепление: 6/6", { exact: false })).toBeVisible();
  expect(aiCalls).toBe(0);
});

test("reinforcement Slovak keyboard inserts at the caret and replaces a selection", async ({ page }) => {
  const lesson = module1.lessons[0];
  await mockStateApi(page, createState({
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "in_progress" },
    lessonSteps: { [lesson.slug]: lesson.sections.length },
    checkSelections: Object.fromEntries(lesson.knowledgeChecks.map((check) => [check.id, check.answer])),
  }));

  await openCourse(page);
  await openLesson(page, lesson);
  const textTask = page.locator(".course-reinforcement-text").first();
  const input = textTask.getByPlaceholder("Введите ответ");
  await input.fill("caj");
  await input.evaluate((element: HTMLInputElement) => element.setSelectionRange(1, 1));
  const keyboard = textTask.getByLabel("Словацкие буквы");
  await expect(keyboard).toBeVisible();
  await keyboard.getByRole("button", { name: "č", exact: true }).click();
  await expect(input).toHaveValue("cčaj");
  await expect(input).toBeFocused();
  await input.evaluate((element: HTMLInputElement) => element.setSelectionRange(1, 3));
  await keyboard.getByRole("button", { name: "á", exact: true }).click();
  await expect(input).toHaveValue("cáj");

  const pairTask = page.locator(".course-pair-practice").filter({ has: page.locator("input") }).filter({ has: page.getByLabel("Словацкие буквы") }).first();
  const pairInput = pairTask.locator("input").first();
  await pairInput.fill("caj");
  await pairInput.evaluate((element: HTMLInputElement) => element.setSelectionRange(1, 1));
  await pairTask.getByLabel("Словацкие буквы").getByRole("button", { name: "á", exact: true }).click();
  await expect(pairInput).toHaveValue("cáaj");
});

test("saved duplicate mistakes render once without React key errors", async ({ page }) => {
  const lesson = module1.lessons.find((item) => item.slug === "verb-byt");
  if (!lesson) throw new Error("Verb byť lesson is missing");
  const duplicate = "Соберите «Вчера я был дома». → нормативно: Včera som bol doma.";
  const consoleErrors: string[] = [];
  page.on("console", (message) => { if (message.type() === "error") consoleErrors.push(message.text()); });
  await mockStateApi(page, createState({
    selectedSlug: lesson.slug,
    progress: { [lesson.slug]: "completed" },
    lessonSummaries: { [lesson.slug]: { understanding: 90, level: "Уверенное понимание", strengths: ["Задания выполнены"], mistakes: [duplicate, duplicate], review: ["Повторить формы"], userTurns: 6 } },
  }));

  await openCourse(page);
  await openLesson(page, lesson);
  await page.getByRole("button", { name: "Закрепление" }).click();
  await expect(page.getByText(duplicate, { exact: true })).toHaveCount(1);
  expect(consoleErrors.filter((message) => message.includes("same key"))).toEqual([]);
});

test("missing Slovak diacritics does not complete a required answer", async ({ page }) => {
  const lesson = module1.lessons.find((item) => item.slug === "slovak-alphabet-pronunciation");
  if (!lesson) throw new Error("Alphabet lesson is missing");
  await mockStateApi(page, createState({
    selectedSlug: lesson.slug,
    lessonSteps: { [lesson.slug]: 1 },
  }));

  await openCourse(page);
  await openLesson(page, lesson);

  const answer = page.getByPlaceholder("Введите ответ по-словацки");
  const next = page.getByRole("button", { name: "Следующий шаг →" });
  await answer.fill("skola");
  await page.getByRole("button", { name: "Проверить ответ" }).click();
  await expect(page.getByText("Почти — проверьте диакритику")).toBeVisible();
  await expect(page.getByText("Нормативный ответ: škola")).toBeVisible();
  await expect(next).toBeDisabled();

  await answer.fill("škola");
  await page.getByRole("button", { name: "Проверить ответ" }).click();
  await expect(page.getByText("Верно — можно идти дальше")).toBeVisible();
  await expect(next).toBeEnabled();
});

test("optional section can be skipped while a required section gates progress", async ({ page }) => {
  const lesson = module1.lessons.find((item) => item.slug === "long-short-vowels");
  if (!lesson) throw new Error("Vowel lesson is missing");
  const optionalIndex = lesson.sections.findIndex((section) => section.importance === "extra");
  if (optionalIndex < 0) throw new Error("Optional section is missing");
  await mockStateApi(page, createState({
    selectedSlug: lesson.slug,
    lessonSteps: { [lesson.slug]: optionalIndex },
  }));

  await openCourse(page);
  await openLesson(page, lesson);
  await expect(page.getByText("Дополнительное углубление")).toBeVisible();
  await expect(page.getByText("Этот раздел можно пропустить", { exact: false })).toBeVisible();
  await expect(page.getByRole("button", { name: "Пропустить дополнительный шаг →" })).toBeEnabled();

  await page.getByRole("button", { name: "Открыть шаг 2" }).click();
  await expect(page.getByText("Обязательная практика")).toBeVisible();
  await expect(page.getByRole("button", { name: "Следующий шаг →" })).toBeDisabled();
  await expect(page.getByText("Выполните обязательную практику шага, чтобы продолжить.")).toBeVisible();
});

test("final test shows review topics below 70 percent and passes after corrections", async ({ page }) => {
  const finalQuestions = buildModuleFinalQuestions(module1.lessons);
  await mockStateApi(page, createState({
    progress: Object.fromEntries(module1.lessons.map((lesson) => [lesson.slug, "completed"])),
    finalSelections: Object.fromEntries(finalQuestions.map((question) => [question.id, "__wrong__"])),
    finalCompleted: true,
    finalCompletedModules: { "1": true },
  }));

  await openCourse(page);
  await page.getByRole("button", { name: /Итоговый тест модуля/ }).click();
  await expect(page.getByText("Порог пока не достигнут")).toBeVisible();
  await expect(page.getByText("Что повторить перед новой попыткой")).toBeVisible();
  await expect(page.getByText("Для сдачи нужно не менее 70%", { exact: false })).toBeVisible();

  for (const question of finalQuestions) {
    const fieldset = page.locator(".course-final fieldset").filter({ hasText: question.lessonTitle }).filter({ hasText: question.question });
    await fieldset.getByRole("button", { name: question.answer, exact: true }).click();
  }
  await page.getByRole("button", { name: "Проверить итоговый тест" }).click();
  await expect(page.getByText("Модуль сдан")).toBeVisible();
  await expect(page.getByText("100%")).toBeVisible();
  await expect(page.getByRole("button", { name: "Перейти к Module 2 →" })).toBeVisible();
});
