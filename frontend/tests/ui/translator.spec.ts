import { expect, test } from "@playwright/test";

test("floating AI translator translates both ways and can be moved while learning", async ({ page }, testInfo) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.route("**/api/v1/course/state", async (route) => {
    if (route.request().method() === "GET") {
      await route.fulfill({ json: { exists: false, schema_version: 1, state: null, updated_at: null } });
      return;
    }
    await route.fulfill({ json: { exists: true, schema_version: 1, state: route.request().postDataJSON(), updated_at: "2026-09-15T12:00:00Z" } });
  });

  const requests: Array<{ text: string; direction: string }> = [];
  await page.route("**/api/v1/tutor/translate", async (route) => {
    const payload = route.request().postDataJSON() as { text: string; direction: string };
    requests.push(payload);
    await route.fulfill({
      json: payload.direction === "ru-sk"
        ? { provider: "codex", translation: "Ďakujem.", alternatives: ["Vďaka."], note: "Нейтральная форма благодарности." }
        : { provider: "codex", translation: "Спасибо.", alternatives: [], note: null },
    });
  });

  await page.goto("/");
  await expect(page.getByRole("heading", { name: "Module 1 — Foundations" })).toBeVisible();
  await page.getByRole("button", { name: "Переводчик" }).click();

  const translator = page.locator(".floating-translator");
  const source = translator.getByRole("textbox", { name: "Текст для перевода" });
  await source.fill("Спасибо.");
  await translator.getByRole("button", { name: "Перевести", exact: true }).click();
  await expect(translator.getByText("Ďakujem.", { exact: true })).toBeVisible();
  await expect(translator.getByText("Также: Vďaka.", { exact: true })).toBeVisible();
  expect(requests[0]).toEqual({ text: "Спасибо.", direction: "ru-sk" });

  await translator.getByRole("button", { name: "Поменять языки местами" }).click();
  await expect(source).toHaveValue("Ďakujem.");
  await translator.getByRole("button", { name: "Перевести", exact: true }).click();
  await expect(translator.getByText("Спасибо.", { exact: true })).toBeVisible();
  expect(requests[1]).toEqual({ text: "Ďakujem.", direction: "sk-ru" });

  const before = await translator.boundingBox();
  const handle = translator.getByRole("button", { name: "Перетащить переводчик" });
  const handleBox = await handle.boundingBox();
  if (!before || !handleBox) throw new Error("Translator should have a measurable position");
  await page.mouse.move(handleBox.x + 20, handleBox.y + 18);
  await page.mouse.down();
  await page.mouse.move(handleBox.x + 20, handleBox.y + 98, { steps: 4 });
  await page.mouse.up();
  const after = await translator.boundingBox();
  if (!after) throw new Error("Translator should remain visible after dragging");
  expect(after.y).toBeGreaterThan(before.y + 30);
  expect(after.x).toBeGreaterThanOrEqual(0);
  expect(after.x + after.width).toBeLessThanOrEqual(390);
  expect(after.y + after.height).toBeLessThanOrEqual(844);

  await translator.getByRole("button", { name: "Свернуть переводчик" }).click();
  await expect(source).toBeHidden();
  await translator.getByRole("button", { name: "Развернуть переводчик" }).click();
  await expect(source).toBeVisible();
  await translator.screenshot({ path: testInfo.outputPath("floating-translator-mobile.png") });
  await page.getByRole("button", { name: "Включить тёмную тему" }).click();
  await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
  await translator.screenshot({ path: testInfo.outputPath("floating-translator-mobile-dark.png") });
});
