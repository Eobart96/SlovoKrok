import { expect, test } from "@playwright/test";
import { allA1Lessons } from "../../app/data/a1Course";
import { lessonVocabulary } from "../../app/data/courseVocabulary";
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
  await expect(page.getByText("Здравствуйте", { exact: true })).not.toBeVisible();
  await page.getByRole("button", { name: "Показать перевод" }).click();
  await expect(page.locator(".course-vocabulary-due")).toContainText("Здравствуйте");
  await page.getByRole("button", { name: "Не вспомнил", exact: true }).click();
  await expect.poll(() => rating).toBe("again");
  await expect(page.getByText("Вернёмся к этой карточке через 10 минут.")).toBeVisible();
  await expect(page.locator(".course-vocabulary-due")).toHaveCount(0);
});

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
