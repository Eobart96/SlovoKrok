import assert from "node:assert/strict";
import test from "node:test";

import { scoreLessonUnderstanding } from "../../app/data/courseScoring.ts";
import { mergeProgress } from "../../app/data/progressMerge.ts";
import { editTranslationDraft, swapTranslationDraft } from "../../app/data/translationState.ts";
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

test("API errors preserve server detail and map invalid bodies to a stable fallback", () => {
  assert.equal(apiErrorMessage({ detail: "Недоступно" }, 503), "Недоступно");
  assert.equal(apiErrorMessage(null, 502), "Ошибка сервера (502)");
  const error = new ApiError("Недоступно", 503, { detail: "Недоступно" });
  assert.equal(error.name, "ApiError");
  assert.equal(error.status, 503);
  assert.deepEqual(error.body, { detail: "Недоступно" });
});
