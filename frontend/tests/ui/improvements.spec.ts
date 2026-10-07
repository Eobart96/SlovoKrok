import { expect, test } from "@playwright/test";
import { allA1Lessons } from "../../app/data/a1Course";
import { buildProgressGenerationContext, exerciseFormats } from "../../app/data/courseGeneration";
import { learnedVocabularySeeds, lessonVocabulary } from "../../app/data/courseVocabulary";
import { buildReinforcementPractices, getPracticeMatch } from "../../app/data/coursePractice";

test("offline edits survive closing the tab and a stale server on the next launch", async ({ context, page }) => {
  let available = true;
  let saved: Record<string, unknown> | null = null;
  const stale = { fontSize: "large", selectedSlug: "greetings", progress: {} };
  await context.route("**/api/v1/course/state", async (route) => {
    if (!available) return route.fulfill({ status: 503, json: { detail: "offline" } });
    if (route.request().method() === "PUT") saved = route.request().postDataJSON();
    return route.fulfill({ json: { exists: true, schema_version: 1, state: stale, updated_at: null } });
  });
  await page.goto("/");
  await expect(page.getByRole("button", { name: "Крупный размер текста", exact: true })).toHaveAttribute("aria-pressed", "true");
  available = false;
  await page.getByRole("button", { name: "Обычный размер текста", exact: true }).click();
  await expect(page.locator(".course-persistence-error")).toBeVisible();
  await page.close();
  available = true;
  const reopened = await context.newPage();
  await reopened.goto("/");
  await expect(reopened.getByRole("button", { name: "Обычный размер текста", exact: true })).toHaveAttribute("aria-pressed", "true");
  await expect.poll(() => saved?.fontSize).toBe("normal");
});

test("only one tab edits the course and a waiting tab takes over safely", async ({ context, page }) => {
  let state = { fontSize: "large", selectedSlug: "greetings", progress: {} };
  await context.route("**/api/v1/course/state", async (route) => {
    if (route.request().method() === "PUT") state = route.request().postDataJSON();
    return route.fulfill({ json: { exists: true, schema_version: 1, state, updated_at: null } });
  });
  await page.goto("/");
  await page.getByRole("button", { name: "Обычный размер текста", exact: true }).click();
  await expect.poll(() => state.fontSize).toBe("normal");
  const waiting = await context.newPage();
  await waiting.goto("/");
  await expect(waiting.locator(".course[inert]")).toHaveCount(1);
  await expect(waiting.getByRole("status")).toContainText("другой вкладкой");
  await page.close();
  await expect(waiting.locator(".course[inert]")).toHaveCount(0);
  await expect(waiting.getByRole("button", { name: "Обычный размер текста", exact: true })).toHaveAttribute("aria-pressed", "true");
});

test("slow saves stay ordered and acknowledge only their own snapshot", async ({ page }) => {
  let hold = false;
  let release = () => {};
  let inFlight = 0;
  let peak = 0;
  let state = { fontSize: "large", selectedSlug: "greetings", progress: {} };
  const writes: string[] = [];
  await page.route("**/api/v1/course/state", async (route) => {
    if (route.request().method() === "PUT") {
      inFlight++; peak = Math.max(peak, inFlight);
      const incoming = route.request().postDataJSON();
      writes.push(incoming.fontSize);
      if (hold) { hold = false; await new Promise<void>((resolve) => { release = resolve; }); }
      state = incoming; inFlight--;
    }
    return route.fulfill({ json: { exists: true, schema_version: 1, state, updated_at: null } });
  });
  await page.goto("/");
  await expect(page.locator(".course[inert]")).toHaveCount(0);
  await expect.poll(() => state.fontSize).toBe("large");
  hold = true;
  await page.getByRole("button", { name: "Обычный размер текста", exact: true }).click();
  await expect.poll(() => writes.includes("normal")).toBe(true);
  await page.getByRole("button", { name: "Очень крупный размер текста", exact: true }).click();
  await expect.poll(() => page.evaluate(() => JSON.parse(localStorage.getItem("slovak-module-1-beta-session-v1")!).fontSize)).toBe("extra-large");
  release();
  await expect.poll(() => state.fontSize).toBe("extra-large");
  expect(peak).toBe(1);
  await expect.poll(() => page.evaluate(() => JSON.parse(localStorage.getItem("slovak-module-1-beta-session-v1")!)._sync.dirty)).toBe(false);
});

test("explicit vocabulary preserves every legacy card key and translation", () => {
  for (const lesson of allA1Lessons) {
    expect(lesson.vocabulary, lesson.slug).toBeDefined();
    expect(lessonVocabulary(lesson), lesson.slug).toEqual(lessonVocabulary({ ...lesson, vocabulary: undefined }));
    const reformatted = structuredClone(lesson);
    reformatted.theory.examples = [];
    reformatted.sections = [];
    expect(lessonVocabulary(reformatted)).toEqual(lesson.vocabulary);
  }
});

test("every course practice accepts its canonical answer and text alternatives", () => {
  for (const lesson of allA1Lessons) {
    for (const practice of [...lesson.stepPractices, ...buildReinforcementPractices(lesson)]) {
      if (practice.type === "pairs") {
        const rows = practice.pairs ?? [];
        expect(getPracticeMatch(practice, JSON.stringify(rows.map((row) => row.answer))), practice.id).toBe("correct");
        rows.forEach((row, index) => {
          for (const alternative of row.acceptableAnswers ?? []) {
            expect(getPracticeMatch(practice, JSON.stringify(rows.map((item, i) => i === index ? alternative : item.answer))), practice.id).toBe("correct");
          }
        });
        continue;
      }
      for (const answer of [practice.answer, ...(practice.acceptableAnswers ?? [])]) {
        expect(getPracticeMatch(practice, answer), `${lesson.slug}/${practice.id}: ${answer}`).toBe("correct");
      }
    }
  }
});

test("vocabulary hides translations until recall and records difficulty", async ({ page }) => {
  await page.route("**/api/v1/course/state", (route) => route.fulfill({ json: { exists: true, state: { selectedSlug: "greetings", progress: { greetings: "completed" } } } }));
  const card = { id: 1, lesson_slug: "greetings", lesson_title: "Приветствия", word: "Dobrý deň", translation: "Здравствуйте", example: null, review_count: 0, interval_days: 0, next_review_at: null, is_due: true };
  await page.route("**/api/v1/course/vocabulary/sync", (route) => route.fulfill({ json: [card] }));
  let rating = "";
  await page.route("**/api/v1/course/vocabulary/1/review", (route) => {
    rating = route.request().postDataJSON().rating;
    return route.fulfill({ json: { ...card, review_count: 1, next_review_at: new Date(Date.now() + 600_000).toISOString(), is_due: false } });
  });
  await page.goto("/");
  await page.getByRole("button", { name: "Слова", exact: true }).click();
  await expect(page.locator(".course-vocabulary-due").getByText("Здравствуйте", { exact: true })).toHaveCount(0);
  await page.getByRole("button", { name: "Показать перевод" }).click();
  await expect(page.locator(".course-vocabulary-due")).toContainText("Здравствуйте");
  await page.getByRole("button", { name: "Не вспомнил", exact: true }).click();
  await expect.poll(() => rating).toBe("again");
  await expect(page.getByText("Вернёмся к этой карточке через 10 минут.")).toBeVisible();
  await expect(page.locator(".course-vocabulary-due")).toHaveCount(0);
});

test("progress-aware exercises use learned vocabulary and relevant mistakes", async ({ page }) => {
  const greetings = allA1Lessons.find((lesson) => lesson.slug === "greetings")!;
  const numbers = allA1Lessons.find((lesson) => lesson.slug === "numbers")!;
  const introductions = allA1Lessons.find((lesson) => lesson.slug === "introductions")!;
  const fullProgressContext = buildProgressGenerationContext({ mode: "progress", completedLessons: allA1Lessons, mistakeHints: [] });
  expect(fullProgressContext.length).toBeLessThanOrEqual(12_000);
  expect(fullProgressContext).toContain(allA1Lessons.at(-1)!.title);
  const requests: Array<Record<string, string>> = [];
  await page.route("**/api/v1/course/state", (route) => route.fulfill({ json: { exists: true, state: {
    selectedSlug: "greetings",
    progress: { greetings: "completed", numbers: "completed", introductions: "in_progress" },
    mistakes: {
      "generated:greetings": { id: "generated:greetings", lessonSlug: "greetings", prompt: "Вежливое приветствие", answer: "Dobrý deň", attempts: 1, mastered: false },
      "generated:numbers": { id: "generated:numbers", lessonSlug: "numbers", prompt: "Число ноль", answer: "nula", attempts: 1, mastered: false },
      "generated:introductions": { id: "generated:introductions", lessonSlug: "introductions", prompt: "Будущая ошибка", answer: "Volám sa", attempts: 1, mastered: false },
    },
  } } }));
  await page.route("**/api/v1/course/exercises", async (route) => {
    if (route.request().method() === "GET") return route.fulfill({ json: [
      { id: 99, lesson_slug: "course-progress", lesson_title: "Общий прогресс Slovak A1", question: "Сохранённое общее упражнение", instruction: "Ответьте.", created_at: new Date().toISOString(), latest_attempt: null },
      { id: 98, lesson_slug: "greetings", lesson_title: greetings.title, question: "Сохранённое упражнение темы", instruction: "Ответьте.", created_at: new Date().toISOString(), latest_attempt: null },
    ] });
    const request = route.request().postDataJSON() as Record<string, string>;
    requests.push(request);
    return route.fulfill({ json: { id: requests.length, lesson_slug: request.lesson_slug, lesson_title: request.lesson_title, question: `Задание ${requests.length}`, instruction: "Ответьте по-словацки.", created_at: new Date().toISOString(), latest_attempt: null } });
  });
  await page.goto("/");
  await page.getByRole("button", { name: "Упражнения", exact: true }).click();
  await expect(page.locator(".course-exercise-workspace h4")).toHaveText("Сохранённое упражнение темы");
  await page.getByRole("button", { name: "Создать упражнение", exact: true }).click();
  await expect.poll(() => requests.length).toBe(1);
  expect(requests[0].lesson_slug).toBe("greetings");
  expect(requests[0].theory).toContain(`тема «${greetings.title}»`);
  expect(requests[0].theory).toContain(greetingVocabularyLine());
  expect(requests[0].theory).toContain("Вежливое приветствие: Dobrý deň");
  expect(requests[0].theory).not.toContain("Будущая ошибка");

  await page.getByRole("button", { name: "По общему прогрессу", exact: true }).click();
  await page.getByRole("button", { name: "Создать упражнение", exact: true }).click();
  await expect.poll(() => requests.length).toBe(2);
  expect(requests[1].lesson_slug).toBe("course-progress");
  expect(requests[1].theory).toContain(numbers.title);
  expect(requests[1].theory).toContain(`${numbers.vocabulary![0].word} = ${numbers.vocabulary![0].translation}`);
  expect(requests[1].theory).toContain("Число ноль: nula");
  expect(requests[1].theory).not.toContain(introductions.title);
  expect(requests[1].theory).not.toContain("Будущая ошибка");
});

test("varied exercise formats rotate and use topic test examples", async ({ page }) => {
  const greetings = allA1Lessons.find((lesson) => lesson.slug === "greetings")!;
  const numbers = allA1Lessons.find((lesson) => lesson.slug === "numbers")!;
  const requests: Array<Record<string, string>> = [];
  await page.route("**/api/v1/course/state", (route) => route.fulfill({ json: { exists: true, state: {
    selectedSlug: "greetings",
    progress: { greetings: "completed", numbers: "completed" },
  } } }));
  await page.route("**/api/v1/course/exercises", async (route) => {
    if (route.request().method() === "GET") return route.fulfill({ json: [] });
    const request = route.request().postDataJSON() as Record<string, string>;
    requests.push(request);
    return route.fulfill({ json: {
      id: requests.length,
      lesson_slug: request.lesson_slug,
      lesson_title: request.lesson_title,
      question: `Разнообразное задание ${requests.length}`,
      instruction: "Ответьте по-словацки.",
      created_at: new Date().toISOString(),
      latest_attempt: null,
    } });
  });

  await page.goto("/");
  await page.getByRole("button", { name: "Упражнения", exact: true }).click();
  for (const [index, format] of exerciseFormats.entries()) {
    await expect(page.locator(".course-exercise-create small")).toContainText(format.label);
    await page.getByRole("button", { name: "Создать упражнение", exact: true }).click();
    await expect.poll(() => requests.length).toBe(index + 1);
    expect(requests[index].theory).toContain(`Формат нового упражнения: ${format.label}.`);
    expect(requests[index].theory).toContain(`Тип интерактива: ${format.interactionType}.`);
    expect(requests[index].theory).toContain(greetings.knowledgeChecks[0].question);
    expect(requests[index].theory).toContain(greetings.knowledgeChecks[0].answer);
    expect(requests[index].theory).not.toContain(numbers.knowledgeChecks[0].question);
    expect(requests[index].theory.length).toBeLessThanOrEqual(12_000);
  }
  await expect(page.locator(".course-exercise-create small")).toContainText(exerciseFormats[0].label);
  expect(new Set(requests.map((request) => request.theory.match(/Формат нового упражнения: ([^.]+)\./)?.[1])).size).toBe(exerciseFormats.length);
});

test("interactive exercise mini-games submit choice order matching and text answers", async ({ page }) => {
  const answers: string[] = [];
  const createdAt = new Date().toISOString();
  await page.route("**/api/v1/course/state", (route) => route.fulfill({ json: { exists: true, state: { selectedSlug: "greetings", progress: { greetings: "completed" } } } }));
  await page.route("**/api/v1/course/exercises/*/answer", async (route) => {
    answers.push(route.request().postDataJSON().answer);
    return route.fulfill({ json: { id: answers.length, answer: answers.at(-1), is_correct: true, score: 100, corrected_answer: answers.at(-1), explanation: "Верно.", next_exercise: "Продолжайте.", created_at: createdAt } });
  });
  await page.route("**/api/v1/course/exercises", (route) => route.fulfill({ json: [
    { id: 4, lesson_slug: "greetings", lesson_title: "Приветствия", question: "Соедините пары", instruction: "Подберите перевод.", interaction_type: "match", pair_prompts: ["Dobrý deň", "Dovidenia"], pair_options: ["До свидания", "Здравствуйте"], options: [], tokens: [], created_at: createdAt, latest_attempt: null },
    { id: 3, lesson_slug: "greetings", lesson_title: "Приветствия", question: "Порядок слов", instruction: "Соберите приветствие.", interaction_type: "order", tokens: ["deň", "Dobrý"], options: [], pair_prompts: [], pair_options: [], created_at: createdAt, latest_attempt: null },
    { id: 2, lesson_slug: "greetings", lesson_title: "Приветствия", question: "Выберите приветствие", instruction: "Найдите формальную фразу.", interaction_type: "choice", options: ["Ahoj", "Dobrý deň", "Čau"], tokens: [], pair_prompts: [], pair_options: [], created_at: createdAt, latest_attempt: null },
    { id: 1, lesson_slug: "greetings", lesson_title: "Приветствия", question: "Переведите", instruction: "Напишите «До свидания».", interaction_type: "text", options: [], tokens: [], pair_prompts: [], pair_options: [], created_at: createdAt, latest_attempt: null },
  ] }));

  await page.goto("/");
  await page.getByRole("button", { name: "Упражнения", exact: true }).click();
  const workspace = page.locator(".course-exercise-workspace");
  await workspace.locator(".course-mini-match label").nth(0).locator("select").selectOption("Здравствуйте");
  await workspace.locator(".course-mini-match label").nth(1).locator("select").selectOption("До свидания");
  await workspace.getByRole("button", { name: "Проверить ответ" }).click();
  await expect.poll(() => answers.at(-1)).toBe("Dobrý deň → Здравствуйте; Dovidenia → До свидания");

  await page.locator(".course-exercise-list article").filter({ hasText: "Порядок слов" }).getByRole("button").first().click();
  await workspace.getByRole("button", { name: "Добавить Dobrý" }).click();
  await workspace.getByRole("button", { name: "Добавить deň" }).click();
  await workspace.getByRole("button", { name: "Проверить ответ" }).click();
  await expect.poll(() => answers.at(-1)).toBe("Dobrý deň");

  await page.locator(".course-exercise-list article").filter({ hasText: "Выберите приветствие" }).getByRole("button").first().click();
  await workspace.getByRole("button", { name: "Dobrý deň", exact: true }).click();
  await expect(workspace.getByRole("button", { name: "Dobrý deň", exact: true })).toHaveAttribute("aria-pressed", "true");
  await workspace.getByRole("button", { name: "Проверить ответ" }).click();
  await expect.poll(() => answers.at(-1)).toBe("Dobrý deň");

  await page.locator(".course-exercise-list article").filter({ hasText: "Переведите" }).getByRole("button").first().click();
  await workspace.getByPlaceholder("Напишите ответ по-словацки…").fill("Dovidenia");
  await workspace.getByRole("button", { name: "Проверить ответ" }).click();
  await expect.poll(() => answers.at(-1)).toBe("Dovidenia");
  expect(answers).toHaveLength(4);
});

test("offline exercise packs persist mode generate batch and check without AI", async ({ page }) => {
  const createdAt = new Date().toISOString();
  const generated: Array<Record<string, unknown>> = [];
  const generationRequests: Array<Record<string, string>> = [];
  let submitted: Record<string, string> | null = null;
  await page.route("**/api/v1/course/state", (route) => route.fulfill({ json: { exists: true, state: { selectedSlug: "greetings", progress: { greetings: "completed" } } } }));
  await page.route("**/api/v1/tutor/settings", (route) => route.fulfill({ json: {
    provider: "codex", codex_installed: true, codex_authenticated: true, codex_message: "Codex подключён.",
    openai_api_key_configured: false, openai_model: "gpt-5", polza_api_key_configured: false,
    polza_model: "google/gemini-2.5-flash-lite", polza_base_url: "https://polza.ai/api/v1",
  } }));
  await page.route("**/api/v1/course/exercises/*/answer", async (route) => {
    submitted = route.request().postDataJSON() as Record<string, string>;
    return route.fulfill({ json: { id: 1, answer: submitted.answer, is_correct: true, score: 100, corrected_answer: "Dobrý deň", explanation: "Ответ совпадает с сохранённым эталоном.", next_exercise: "Следующее задание.", created_at: createdAt } });
  });
  await page.route("**/api/v1/course/exercises", async (route) => {
    if (route.request().method() === "GET") return route.fulfill({ json: generated.slice().reverse() });
    const request = route.request().postDataJSON() as Record<string, string>;
    generationRequests.push(request);
    const item = { id: generated.length + 1, lesson_slug: request.lesson_slug, lesson_title: request.lesson_title, question: `Офлайн-задание ${generated.length + 1}`, instruction: "Напишите приветствие.", interaction_type: "text", options: [], tokens: [], pair_prompts: [], pair_options: [], created_at: createdAt, latest_attempt: null };
    generated.push(item);
    return route.fulfill({ json: item });
  });

  await page.goto("/");
  await page.getByRole("button", { name: "Упражнения", exact: true }).click();
  await page.getByLabel("Количество заданий").fill("3");
  await page.getByRole("button", { name: "Создать 3 упражнения", exact: true }).click();
  await expect.poll(() => generationRequests.length).toBe(3);
  await expect(page.getByRole("status")).toContainText("Сохранено заданий: 3");
  expect(generationRequests.map((request) => request.theory.match(/Тип интерактива: (\w+)/)?.[1])).toEqual(["text", "choice", "choice"]);

  await page.getByRole("button", { name: "Открыть настройки" }).click();
  const dialog = page.getByRole("dialog", { name: "Настройки" });
  const offlineSwitch = dialog.getByRole("switch", { name: "Офлайн-режим" });
  await offlineSwitch.click();
  await expect(offlineSwitch).toHaveAttribute("aria-checked", "true");
  await dialog.getByRole("button", { name: "Закрыть настройки" }).click();

  await page.reload();
  await page.getByRole("button", { name: "Упражнения", exact: true }).click();
  await expect(page.locator(".course-learning-mode")).toContainText("Офлайн");
  await expect(page.getByLabel("Количество заданий")).toBeDisabled();
  await expect(page.getByRole("button", { name: "Создать упражнение", exact: true })).toBeDisabled();
  await page.getByPlaceholder("Напишите ответ по-словацки…").fill("Dobrý deň");
  await page.getByRole("button", { name: "Проверить ответ" }).click();
  await expect.poll(() => submitted?.assessment_mode).toBe("offline");
  await expect(page.locator(".course-exercise-workspace article.correct")).toContainText("100/100");
});

test("personal statistics summarizes the whole course and recommends next action", async ({ page }) => {
  const greetings = allA1Lessons.find((lesson) => lesson.slug === "greetings")!;
  const family = allA1Lessons.find((lesson) => lesson.slug === "family")!;
  const completedSlugs = [greetings.slug, family.slug];
  await page.route("**/api/v1/course/state", (route) => route.fulfill({ json: { exists: true, state: {
    activeModule: 1,
    selectedSlug: greetings.slug,
    progress: { [greetings.slug]: "completed", [family.slug]: "completed", numbers: "in_progress" },
    practiceResults: { [greetings.stepPractices[0].id]: true, [family.stepPractices[0].id]: true },
    checkSelections: { [greetings.knowledgeChecks[0].id]: greetings.knowledgeChecks[0].answer },
    mistakes: {
      "stats-active": { id: "stats-active", lessonSlug: greetings.slug, prompt: "Исправьте приветствие", answer: "Dobrý deň", attempts: 2, mastered: false, dueAt: "2026-09-01T00:00:00.000Z" },
      "stats-mastered": { id: "stats-mastered", lessonSlug: family.slug, prompt: "Назовите родственника", answer: "sestra", attempts: 1, mastered: true },
    },
    lessonSummaries: {
      [greetings.slug]: { understanding: 90, level: "Уверенное понимание", strengths: [], review: [], userTurns: 6 },
      [family.slug]: { understanding: 70, level: "Хорошая основа", strengths: [], review: [], userTurns: 6 },
    },
  } } }));

  await page.goto("/");
  await page.getByRole("button", { name: "Статистика", exact: true }).click();
  await expect(page.getByRole("heading", { name: "Мой прогресс" })).toBeVisible();
  const overview = page.locator(".course-personal-stat-grid");
  await expect(overview.locator("article").nth(0)).toContainText(`2/${allA1Lessons.length}`);
  await expect(overview.locator("article").nth(1)).toContainText("40%");
  await expect(overview.locator("article").nth(2)).toContainText(`${learnedVocabularySeeds(allA1Lessons, completedSlugs).length}`);
  await expect(overview.locator("article").nth(3)).toContainText("80%");
  await expect(page.locator(".course-personal-next")).toContainText("Повторите 1 ошибку, доступную сейчас.");
  await expect(page.locator(".course-personal-next")).toContainText("Активных ошибок: 1 · закреплено: 1 · повторить сейчас: 1");
  await expect(page.locator(".course-module-stats article")).toHaveCount(8);
  await expect(page.locator(".course-module-stats")).toContainText("Module 1");
  await expect(page.locator(".course-module-stats")).toContainText("Module 6");
  await expect(page.getByRole("heading", { name: "Module 1 — Foundations", exact: true }).last()).toBeVisible();
  await expect(page.getByRole("button", { name: "Сбросить прогресс модуля" })).toBeVisible();
  await page.setViewportSize({ width: 390, height: 844 });
  await page.getByRole("button", { name: "Включить тёмную тему" }).click();
  await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
});

test("progress-aware homework uses learned vocabulary and relevant mistakes", async ({ page }) => {
  const numbers = allA1Lessons.find((lesson) => lesson.slug === "numbers")!;
  const introductions = allA1Lessons.find((lesson) => lesson.slug === "introductions")!;
  const requests: Array<{ lesson_slug: string; lesson_title: string; theory: string; known_mistakes: string[] }> = [];
  await page.route("**/api/v1/course/state", (route) => route.fulfill({ json: { exists: true, state: {
    selectedSlug: "greetings",
    progress: { greetings: "completed", numbers: "completed", introductions: "in_progress" },
    mistakes: {
      "generated:greetings": { id: "generated:greetings", lessonSlug: "greetings", prompt: "Вежливое приветствие", answer: "Dobrý deň", attempts: 1, mastered: false },
      "generated:numbers": { id: "generated:numbers", lessonSlug: "numbers", prompt: "Число ноль", answer: "nula", attempts: 1, mastered: false },
      "generated:introductions": { id: "generated:introductions", lessonSlug: "introductions", prompt: "Будущая ошибка", answer: "Volám sa", attempts: 1, mastered: false },
    },
  } } }));
  await page.route("**/api/v1/course/homework", async (route) => {
    if (route.request().method() === "GET") return route.fulfill({ json: [
      { id: 99, lesson_slug: "course-progress", lesson_title: "Общий прогресс Slovak A1", title: "Сохранённое общее задание", description: "Ответьте.", focus_category: "Общее", created_at: new Date().toISOString(), latest_attempt: null },
      { id: 98, lesson_slug: "greetings", lesson_title: "Приветствия", title: "Сохранённое задание темы", description: "Ответьте.", focus_category: "Тема", created_at: new Date().toISOString(), latest_attempt: null },
    ] });
    const request = route.request().postDataJSON() as typeof requests[number];
    requests.push(request);
    return route.fulfill({ json: { id: requests.length, lesson_slug: request.lesson_slug, lesson_title: request.lesson_title, title: `Домашнее задание ${requests.length}`, description: "Напишите короткий ответ.", focus_category: "Прогресс", created_at: new Date().toISOString(), latest_attempt: null } });
  });
  await page.goto("/");
  await page.getByRole("button", { name: "Домашнее задание", exact: true }).click();
  await expect(page.locator(".course-exercise-workspace h4")).toHaveText("Сохранённое задание темы");
  await page.getByRole("button", { name: "Создать задание", exact: true }).click();
  await expect.poll(() => requests.length).toBe(1);
  expect(requests[0].lesson_slug).toBe("greetings");
  expect(requests[0].theory).toContain(greetingVocabularyLine());
  expect(requests[0].known_mistakes).toEqual(["Вежливое приветствие: Dobrý deň"]);

  await page.getByRole("button", { name: "По общему прогрессу", exact: true }).click();
  await page.getByRole("button", { name: "Создать задание", exact: true }).click();
  await expect.poll(() => requests.length).toBe(2);
  expect(requests[1].lesson_slug).toBe("course-progress");
  expect(requests[1].theory).toContain(numbers.title);
  expect(requests[1].theory).toContain(`${numbers.vocabulary![0].word} = ${numbers.vocabulary![0].translation}`);
  expect(requests[1].known_mistakes).toEqual(["Вежливое приветствие: Dobrý deň", "Число ноль: nula"]);
  expect(requests[1].theory).not.toContain(introductions.title);
  expect(requests[1].known_mistakes).not.toContain("Будущая ошибка: Volám sa");
});

function greetingVocabularyLine(): string {
  const item = allA1Lessons.find((lesson) => lesson.slug === "greetings")!.vocabulary![0];
  return `${item.word} = ${item.translation}`;
}

test("backup preview precedes restore and autosave never overwrites restored progress", async ({ page }) => {
  let state = { selectedSlug: "greetings", fontSize: "large", progress: {} };
  let restores = 0;
  await page.route("**/api/v1/course/state", (route) => {
    if (route.request().method() === "PUT") state = route.request().postDataJSON();
    return route.fulfill({ json: { exists: true, schema_version: 1, state } });
  });
  await page.route("**/api/v1/course/backup", (route) => route.fulfill({ json: { format: "slovokrok-course-backup", version: 1, state } }));
  await page.route("**/api/v1/course/backup/validate", (route) => route.fulfill({ json: { exported_at: "2026-09-11T10:00:00Z", has_state: true, completed_topics: 1, counts: { vocabulary: 2, exercises: 1 } } }));
  await page.route("**/api/v1/course/backup/restore", (route) => {
    restores++;
    state = { selectedSlug: "greetings", fontSize: "extra-large", progress: { greetings: "completed" } };
    return route.fulfill({ json: { restored: true, state } });
  });
  await page.goto("/");
  await page.getByRole("button", { name: "Открыть настройки" }).click();
  await page.locator(".course-backup summary").click();
  const download = page.waitForEvent("download");
  await page.getByRole("button", { name: "Скачать резервную копию" }).click();
  expect((await download).suggestedFilename()).toMatch(/^slovokrok-backup-/);
  await page.locator(".course-backup input").setInputFiles({ name: "backup.json", mimeType: "application/json", buffer: Buffer.from("{}") });
  await expect(page.locator(".course-backup-preview")).toContainText("Завершено тем: 1");
  expect(restores).toBe(0);
  page.once("dialog", (dialog) => dialog.accept());
  const previousBackup = page.waitForEvent("download");
  await page.getByRole("button", { name: "Восстановить выбранную копию" }).click();
  expect((await previousBackup).suggestedFilename()).toMatch(/^slovokrok-before-restore-/);
  await expect(page.getByText("Копия восстановлена.", { exact: true })).toBeVisible();
  await expect(page.locator(".course-progress strong")).toHaveText("1/14");
  await page.getByRole("button", { name: "Закрыть", exact: true }).click();
  await page.getByRole("button", { name: "Обычный размер текста", exact: true }).click();
  await expect.poll(() => state.fontSize).toBe("normal");
  expect(state.progress).toMatchObject({ greetings: "completed" });
});

for (const width of [390, 1280]) test(`listening pilot plays local MP3 and reveals text after an attempt at ${width}px`, async ({ page }, testInfo) => {
  await page.setViewportSize({ width, height: 900 });
  await page.route("**/api/v1/course/state", (route) => route.fulfill({ json: { exists: true, state: { activeModule: 6, selectedSlug: "short-listening", fontSize: "extra-large", progress: { "short-listening": "in_progress" } } } }));
  await page.goto("/");
  if (width === 390) await page.getByRole("button", { name: "Включить тёмную тему" }).click();
  await page.locator(".course-group-card").filter({ hasText: "Практические тексты и сообщения" }).click();
  await page.getByRole("button").filter({ hasText: "Короткие устные сообщения" }).first().click();
  await page.getByRole("button", { name: "Послушать сообщения", exact: true }).click();
  await expect(page.locator(".course-material")).toHaveCount(0);
  const clips = allA1Lessons.find((lesson) => lesson.slug === "short-listening")!.listening!;
  for (const [index, clip] of clips.entries()) {
    const field = page.locator(".course-listening fieldset").nth(index);
    await expect(field.getByText(clip.transcript, { exact: true })).toHaveCount(0);
    await expect(field.getByRole("button", { name: "Проверить ответ" })).toBeDisabled();
    const audio = field.locator("audio");
    await expect.poll(() => audio.evaluate((element: HTMLAudioElement) => element.duration)).toBeGreaterThan(1);
    await audio.evaluate((element: HTMLAudioElement) => element.play());
    await expect.poll(() => audio.evaluate((element: HTMLAudioElement) => element.currentTime)).toBeGreaterThan(0);
    await field.getByRole("button", { name: clip.answer, exact: true }).click();
    await field.getByRole("button", { name: "Проверить ответ" }).click();
    await expect(field.getByText(clip.transcript, { exact: true })).toBeVisible();
  }
  const size = await page.evaluate(() => ({ content: document.documentElement.scrollWidth, viewport: innerWidth }));
  expect(size.content).toBeLessThanOrEqual(size.viewport);
  await page.screenshot({ path: testInfo.outputPath(`listening-${width}.png`), fullPage: true });
});
