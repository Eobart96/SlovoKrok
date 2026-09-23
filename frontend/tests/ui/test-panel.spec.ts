import { expect, type Locator, test } from "@playwright/test";

async function ensureDetailsOpen(details: Locator) {
  if (await details.getAttribute("open") === null) await details.locator("summary").click();
}

async function openDevelopmentTools(page: import("@playwright/test").Page) {
  await page.getByRole("button", { name: "Открыть настройки" }).click();
  const dialog = page.getByRole("dialog", { name: "Настройки" });
  const toggle = dialog.getByRole("switch", { name: "Режим разработки" });
  if (await toggle.getAttribute("aria-checked") === "false") await toggle.click();
  await ensureDetailsOpen(dialog.locator(".course-test-panel"));
  return dialog;
}

test.beforeEach(async ({ page }) => {
  let state = { selectedSlug: "greetings", progress: { greetings: "not_started", foreign: "completed" }, practiceAnswers: { foreign: "keep" }, fontSize: "large" };
  await page.route("**/api/v1/course/state", (route) => {
    if (route.request().method() === "PUT") state = route.request().postDataJSON();
    return route.fulfill({ json: { exists: true, schema_version: 1, state, updated_at: null } });
  });
  await page.route("**/api/v1/tutor/settings", (route) => route.fulfill({ json: {
    provider: "codex", codex_installed: true, codex_authenticated: true, codex_message: "Codex подключён.",
    openai_api_key_configured: false, openai_model: "gpt-5", polza_api_key_configured: false,
    polza_model: "openai/gpt-4o-mini", polza_base_url: "https://polza.ai/api/v1",
  } }));
  await page.goto("/");
  await expect(page.locator(".course-backup")).toHaveCount(0);
  await expect(page.locator(".course-test-panel")).toHaveCount(0);
  await openDevelopmentTools(page);
});

test("manual completion persists, can be undone, and reset preserves unrelated progress", async ({ page }) => {
  const panel = page.locator(".course-test-panel");
  await expect.poll(() => panel.locator(".course-test-grid").evaluate((element) => getComputedStyle(element).gridTemplateColumns.split(" ").length)).toBe(1);
  await panel.getByRole("button", { name: "Отметить весь модуль завершённым", exact: true }).click();
  await expect(page.locator(".course-progress strong")).toHaveText("14/14");
  await panel.getByRole("button", { name: "Отменить последнюю отметку" }).click();
  await expect(page.locator(".course-progress strong")).toHaveText("0/14");
  await panel.getByRole("button", { name: "Пропустить тему и перейти дальше" }).click();
  await openDevelopmentTools(page);
  await expect(panel.getByLabel("Тема для проверки")).not.toHaveValue("greetings");
  await expect.poll(() => page.evaluate(() => JSON.parse(localStorage.getItem("slovak-module-1-beta-session-v1")!)._sync.dirty)).toBe(false);
  await page.reload();
  await openDevelopmentTools(page);
  await expect(page.locator(".course-progress strong")).toHaveText("1/14");
  await panel.getByLabel("Тема для проверки").selectOption("greetings");
  await openDevelopmentTools(page);
  page.once("dialog", (dialog) => dialog.dismiss());
  await panel.getByRole("button", { name: "Сбросить выбранную тему", exact: true }).click();
  await expect(page.locator(".course-progress strong")).toHaveText("1/14");
  page.once("dialog", (dialog) => dialog.accept());
  await panel.getByRole("button", { name: "Сбросить выбранную тему", exact: true }).click();
  await expect(page.locator(".course-progress strong")).toHaveText("0/14");
  const stored = await page.evaluate(() => JSON.parse(localStorage.getItem("slovak-module-1-beta-session-v1")!));
  expect(stored.progress.foreign).toBe("completed");
  expect(stored.practiceAnswers).toEqual({ foreign: "keep" });
});

test("development tools delete every generated exercise after confirmation", async ({ page }) => {
  let deleteRequests = 0;
  let requestBody: unknown = null;
  await page.route("**/api/v1/course/exercises", async (route) => {
    if (route.request().method() !== "DELETE") return route.fallback();
    deleteRequests += 1;
    requestBody = route.request().postDataJSON();
    return route.fulfill({ json: { deleted: true, exercises_deleted: 7, attempts_deleted: 4 } });
  });

  const panel = page.locator(".course-test-panel");
  page.once("dialog", (dialog) => dialog.dismiss());
  await panel.getByRole("button", { name: "Удалить все упражнения", exact: true }).click();
  expect(deleteRequests).toBe(0);

  page.once("dialog", (dialog) => dialog.accept());
  await panel.getByRole("button", { name: "Удалить все упражнения", exact: true }).click();
  await expect.poll(() => deleteRequests).toBe(1);
  expect(requestBody).toEqual({ confirmation: "delete-all-exercises" });
  await expect(panel.getByRole("status")).toContainText("Удалено упражнений: 7");
});

test("manual navigation bypasses gates without completing the module", async ({ page }) => {
  const panel = page.locator(".course-test-panel");
  await panel.getByLabel("Шаг темы", { exact: true }).selectOption("2");
  await expect(page.locator(".course-material-layout")).toBeVisible();
  await expect(page.getByText("Режим просмотра: можно переходить между шагами без выполнения практики. Прогресс и ответы не изменяются.")).toBeVisible();
  await expect(page.getByRole("button", { name: "Следующий шаг →" })).toBeEnabled();
  await expect(page.locator(".course-progress strong")).toHaveText("0/14");
  await openDevelopmentTools(page);
  await panel.getByRole("button", { name: "Открыть итоговый тест без прохождения тем" }).click();
  await expect(page.locator(".course-material-layout")).toHaveCount(0);
  await expect(page.locator(".course-progress strong")).toHaveText("0/14");
  await expect(page.getByRole("heading", { name: /Итоговый тест/ })).toBeVisible();
  await page.getByRole("button", { name: "Ошибки", exact: true }).click();
  await openDevelopmentTools(page);
  await panel.getByRole("button", { name: "Посмотреть выбранный шаг", exact: true }).click();
  await expect(page.locator(".course-material-layout")).toBeVisible();
  await expect(page.getByRole("button", { name: "Обучение", exact: true })).toHaveClass("active");
});

test("turning development mode off closes an active bypass and stays off after reload", async ({ page }) => {
  const panel = page.locator(".course-test-panel");
  await panel.getByRole("button", { name: "Открыть итоговый тест без прохождения тем" }).click();
  await expect(page.getByRole("heading", { name: /Итоговый тест/ })).toBeVisible();

  await page.getByRole("button", { name: "Открыть настройки" }).click();
  let dialog = page.getByRole("dialog", { name: "Настройки" });
  await dialog.getByRole("switch", { name: "Режим разработки" }).click();
  await dialog.getByRole("button", { name: "Закрыть", exact: true }).click();
  await expect(page.getByRole("heading", { name: "Выберите раздел" })).toBeVisible();
  await expect(page.getByRole("heading", { name: /Итоговый тест/ })).toHaveCount(0);

  await page.reload();
  await page.getByRole("button", { name: "Открыть настройки" }).click();
  dialog = page.getByRole("dialog", { name: "Настройки" });
  await expect(dialog.getByRole("switch", { name: "Режим разработки" })).toHaveAttribute("aria-checked", "false");
  await expect(dialog.locator(".course-test-panel")).toHaveCount(0);
});

test("appearance applies, survives reload, resets and fits mobile in dark mode", async ({ page }) => {
  const panel = page.locator(".course-test-panel");
  let dialog = page.getByRole("dialog", { name: "Настройки" });
  await ensureDetailsOpen(dialog.locator(".settings-appearance"));
  await dialog.getByLabel("Шрифт", { exact: true }).selectOption("serif");
  await dialog.getByLabel("Тени", { exact: true }).selectOption("none");
  await dialog.getByLabel("Скругление карточек").selectOption("square");
  await dialog.getByLabel("Межстрочный интервал").selectOption("relaxed");
  await expect(page.locator(".course-route-shell")).toHaveCSS("font-family", /Georgia/);
  await expect(page.locator(".course")).toHaveCSS("box-shadow", "none");
  await expect(page.locator(".course")).toHaveCSS("border-radius", "0px");
  await page.reload();
  dialog = await openDevelopmentTools(page);
  await ensureDetailsOpen(dialog.locator(".settings-appearance"));
  await expect(dialog.getByLabel("Шрифт", { exact: true })).toHaveValue("serif");
  await page.setViewportSize({ width: 390, height: 844 });
  await dialog.getByRole("button", { name: "Закрыть", exact: true }).click();
  if (await page.getByRole("button", { name: "Включить тёмную тему" }).count()) await page.getByRole("button", { name: "Включить тёмную тему" }).click();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
  dialog = await openDevelopmentTools(page);
  await ensureDetailsOpen(dialog.locator(".settings-appearance"));
  await dialog.getByRole("button", { name: "Вернуть исходное оформление" }).click();
  await expect(dialog.getByLabel("Шрифт", { exact: true })).toHaveValue("default");
  await expect(panel).toHaveCSS("border-radius", "18px");
});

test("settings remember which sections are expanded after reload", async ({ page }) => {
  let dialog = page.getByRole("dialog", { name: "Настройки" });
  const appearance = dialog.locator(".settings-appearance");
  const backup = dialog.locator(".course-backup");
  const ai = dialog.locator(".settings-ai");
  await ensureDetailsOpen(appearance);
  await ensureDetailsOpen(backup);
  await ai.locator("summary").click();
  await dialog.getByRole("button", { name: "Закрыть", exact: true }).click();

  await page.reload();
  await page.getByRole("button", { name: "Открыть настройки" }).click();
  dialog = page.getByRole("dialog", { name: "Настройки" });
  await expect(dialog.locator(".settings-appearance")).toHaveAttribute("open", "");
  await expect(dialog.locator(".course-backup")).toHaveAttribute("open", "");
  await expect(dialog.locator(".settings-ai")).not.toHaveAttribute("open", "");
  await expect(dialog.locator(".course-test-panel")).toHaveAttribute("open", "");
});
