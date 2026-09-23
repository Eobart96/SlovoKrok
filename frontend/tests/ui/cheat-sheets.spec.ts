import { expect, test } from "@playwright/test";

test.beforeEach(async ({ page }) => {
  let state = {
    selectedSlug: "greetings",
    progress: { greetings: "completed", "preposition-government": "completed", "long-short-vowels": "not_started" },
    fontSize: "large",
  };
  await page.route("**/api/v1/course/state", (route) => {
    if (route.request().method() === "PUT") state = route.request().postDataJSON();
    return route.fulfill({ json: { exists: true, schema_version: 1, state, updated_at: null } });
  });
  await page.goto("/");
  await page.getByRole("button", { name: "Шпаргалки", exact: true }).click();
});

test("cheat sheets include only completed topics with rules examples and an action plan", async ({ page }) => {
  await expect(page.getByRole("heading", { name: "Шпаргалки", exact: true })).toBeVisible();
  await expect(page.locator(".course-cheat-card")).toHaveCount(2);
  await expect(page.getByText("Долгие и краткие гласные", { exact: true })).toHaveCount(0);
  await expect(page.getByLabel("Модуль шпаргалок").locator("option")).toHaveText([
    "Все пройденные модули",
    "Module 1 — Foundations",
    "Module 4 — Cases and Prepositions",
  ]);

  await page.getByLabel("Модуль шпаргалок").selectOption("4");
  const card = page.locator(".course-cheat-card");
  await expect(card).toHaveCount(1);
  await card.locator("summary").click();
  await expect(card.getByText("Суть темы", { exact: true })).toBeVisible();
  await expect(card.getByRole("heading", { name: "Главные правила" })).toBeVisible();
  await expect(card.getByRole("heading", { name: "Примеры" })).toBeVisible();
  await expect(card.getByRole("heading", { name: "План действий" })).toBeVisible();
  await expect(card.locator(".course-cheat-examples article")).not.toHaveCount(0);
});

test("cheat sheet search and full-topic link work on mobile in dark mode", async ({ page }) => {
  await page.getByLabel("Найти тему").fill("предлоги");
  await expect(page.locator(".course-cheat-card")).toHaveCount(1);
  await page.locator(".course-cheat-card summary").click();
  await page.setViewportSize({ width: 390, height: 844 });
  await page.getByRole("button", { name: "Включить тёмную тему" }).click();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
  await page.getByRole("button", { name: "Открыть полную тему →" }).click();
  await expect(page.getByRole("button", { name: "Обучение", exact: true })).toHaveClass("active");
  await expect(page.getByRole("heading", { name: "Предлоги и управление падежами", exact: true })).toBeVisible();
});

test("personal cheat sheets can be created edited restored and deleted", async ({ page }) => {
  await page.getByRole("button", { name: /Мои шпаргалки/ }).click();
  await page.getByLabel("Название").fill("Моё правило");
  await page.getByLabel("Правило или памятка").fill("После do использую Genitív.");
  await page.getByRole("button", { name: "Добавить шпаргалку" }).click();
  await expect(page.getByRole("heading", { name: "Моё правило" })).toBeVisible();
  await expect.poll(() => page.evaluate(() => JSON.parse(localStorage.getItem("slovak-module-1-beta-session-v1")!).personalCheatSheets?.[0]?.title)).toBe("Моё правило");

  await page.reload();
  await page.getByRole("button", { name: "Шпаргалки", exact: true }).click();
  await page.getByRole("button", { name: /Мои шпаргалки/ }).click();
  await expect(page.getByText("После do использую Genitív.", { exact: true })).toBeVisible();
  await page.getByRole("button", { name: "Изменить" }).click();
  await page.getByLabel("Название").fill("Моё важное правило");
  await page.getByRole("button", { name: "Сохранить изменения" }).click();
  await expect(page.getByRole("heading", { name: "Моё важное правило" })).toBeVisible();

  page.once("dialog", (dialog) => dialog.accept());
  await page.getByRole("button", { name: "Удалить" }).click();
  await expect(page.getByText("Личных шпаргалок пока нет", { exact: true })).toBeVisible();
});
