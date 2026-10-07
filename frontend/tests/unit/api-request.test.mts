import assert from "node:assert/strict";
import test from "node:test";

import { ApiError, ApiRequestError } from "../../app/lib/apiError.ts";
import {
  answerCourseExercise,
  checkCourseReading,
  deleteAllCourseTasks,
  deleteCourseExercise,
  deleteCourseHomework,
  deleteCourseReading,
  findRecoveredHomeworkAttempt,
  generateCourseExercise,
  generateCourseHomework,
  generateCourseReading,
  isAmbiguousMutationError,
  submitCourseHomework,
  type CourseHomework,
} from "../../app/lib/api.ts";
import { generateSequentialBatch } from "../../app/lib/batchGeneration.ts";
import { aiRequestTimeoutMs, apiRequestUrl, backupRequestTimeoutMs, defaultRequestTimeoutMs, requestJson } from "../../app/lib/request.ts";

const originalFetch = globalThis.fetch;

test.afterEach(() => {
  globalThis.fetch = originalFetch;
});

test("request policy keeps AI timeout beyond the backend maximum", () => {
  assert.equal(defaultRequestTimeoutMs, 30_000);
  assert.equal(aiRequestTimeoutMs, 310_000);
  assert.equal(backupRequestTimeoutMs, 310_000);
});

test("browser requests bypass the Next proxy while Node requests stay relative", () => {
  assert.equal(apiRequestUrl("/course/readings", true), "http://127.0.0.1:8000/api/v1/course/readings");
  assert.equal(apiRequestUrl("/course/readings", false), "/api/v1/course/readings");
});

test("batch generation keeps successes after one failure and stops after three consecutive failures", async () => {
  const progress: Array<{ attempted: number; created: number; failed: number }> = [];
  const result = await generateSequentialBatch({
    count: 8,
    create: async (index) => {
      if ([1, 4, 5, 6].includes(index)) throw new Error(`failure ${index}`);
      return index;
    },
    onProgress: (value) => progress.push(value),
  });

  assert.deepEqual(result.items, [0, 2, 3]);
  assert.equal(result.attempted, 7);
  assert.equal(result.failed, 4);
  assert.equal(result.stoppedEarly, true);
  assert.deepEqual(progress.at(-1), { attempted: 7, created: 3, failed: 4 });
});

test("network failures are reported once without automatic retry", async () => {
  let calls = 0;
  globalThis.fetch = (async () => {
    calls += 1;
    throw new TypeError("connection refused");
  }) as typeof fetch;

  await assert.rejects(requestJson("/course/state", { timeoutMs: 50 }), (error: unknown) => {
    assert.ok(error instanceof ApiRequestError);
    assert.equal(error.kind, "network");
    return true;
  });
  assert.equal(calls, 1);
});

test("request timeout aborts the in-flight fetch with a stable error", async () => {
  globalThis.fetch = ((_input, init) => new Promise((_resolve, reject) => {
    init?.signal?.addEventListener("abort", () => reject(new DOMException("aborted", "AbortError")), { once: true });
  })) as typeof fetch;

  await assert.rejects(requestJson("/course/state", { timeoutMs: 5 }), (error: unknown) => {
    assert.ok(error instanceof ApiRequestError);
    assert.equal(error.kind, "timeout");
    assert.match(error.message, /не ответил вовремя/);
    return true;
  });
});

test("caller cancellation stays distinct from timeout", async () => {
  const controller = new AbortController();
  globalThis.fetch = ((_input, init) => new Promise((_resolve, reject) => {
    init?.signal?.addEventListener("abort", () => reject(new DOMException("aborted", "AbortError")), { once: true });
  })) as typeof fetch;

  const pending = requestJson("/course/state", { signal: controller.signal, timeoutMs: 1_000 });
  controller.abort();
  await assert.rejects(pending, (error: unknown) => {
    assert.ok(error instanceof ApiRequestError);
    assert.equal(error.kind, "cancelled");
    assert.equal(error.message, "Запрос отменён.");
    return true;
  });
});

test("HTTP detail remains an ApiError and is not remapped as a network failure", async () => {
  globalThis.fetch = (async () => new Response(JSON.stringify({ detail: "Конфликт revision" }), {
    status: 409,
    headers: { "Content-Type": "application/json" },
  })) as typeof fetch;

  await assert.rejects(requestJson("/course/state", { timeoutMs: 50 }), (error: unknown) => {
    assert.ok(error instanceof ApiError);
    assert.equal(error.status, 409);
    assert.equal(error.message, "Конфликт revision");
    return true;
  });
});

test("invalid success JSON is distinct from a connection failure", async () => {
  globalThis.fetch = (async () => new Response("not-json", { status: 200 })) as typeof fetch;

  await assert.rejects(requestJson("/course/state", { timeoutMs: 50 }), (error: unknown) => {
    assert.ok(error instanceof ApiRequestError);
    assert.equal(error.kind, "invalid-response");
    return true;
  });
});

test("homework submit recovers a result saved before a transient 500 without repeating POST", async () => {
  const attempt = { id: 12, answer: "Dobrý deň.", is_correct: true, score: 100, corrected_answer: "Dobrý deň.", explanation: "Верно.", next_exercise: "Продолжайте.", created_at: "2026-10-05T00:00:00Z" };
  const homework = [{ id: 7, lesson_slug: "greetings", lesson_title: "Приветствия", title: "Диалог", description: "Поздоровайтесь.", focus_category: "приветствие", created_at: "2026-10-05T00:00:00Z", offline_ready: true, latest_attempt: attempt }] satisfies CourseHomework[];
  const calls: Array<{ url: string; method: string }> = [];
  globalThis.fetch = (async (input, init) => {
    calls.push({ url: String(input), method: init?.method ?? "GET" });
    return calls.length === 1
      ? new Response(null, { status: 500 })
      : new Response(JSON.stringify(homework), { status: 200, headers: { "Content-Type": "application/json" } });
  }) as typeof fetch;

  assert.deepEqual(await submitCourseHomework(7, attempt.answer, "online", 11), attempt);
  assert.deepEqual(calls, [
    { url: "/api/v1/course/homework/7/submit", method: "POST" },
    { url: "/api/v1/course/homework", method: "GET" },
  ]);
});

test("homework recovery ignores the attempt that was already visible before submit", () => {
  const oldAttempt = { id: 11, answer: "Dobrý deň.", is_correct: true, score: 100, corrected_answer: "Dobrý deň.", explanation: "Верно.", next_exercise: "Продолжайте.", created_at: "2026-10-05T00:00:00Z" };
  const homework = [{ id: 7, lesson_slug: "greetings", lesson_title: "Приветствия", title: "Диалог", description: "Поздоровайтесь.", focus_category: "приветствие", created_at: "2026-10-05T00:00:00Z", offline_ready: true, latest_attempt: oldAttempt }] satisfies CourseHomework[];
  assert.equal(findRecoveredHomeworkAttempt(homework, 7, oldAttempt.answer, oldAttempt.id), null);
});

test("only proxy 500 and connection failures trigger mutation recovery", () => {
  assert.equal(isAmbiguousMutationError(new ApiError("proxy failed", 500)), true);
  assert.equal(isAmbiguousMutationError(new ApiError("bad provider output", 502)), false);
  assert.equal(isAmbiguousMutationError(new ApiError("provider unavailable", 503)), false);
  assert.equal(isAmbiguousMutationError(new ApiError("provider timeout", 504)), false);
  assert.equal(isAmbiguousMutationError(new ApiRequestError("socket closed", "network")), true);
  assert.equal(isAmbiguousMutationError(new ApiRequestError("cancelled", "cancelled")), false);
});

test("all generated material types recover a saved item after transient 500", async (context) => {
  const cases = [
    {
      name: "exercise",
      create: () => generateCourseExercise({ lesson_slug: "greetings", lesson_title: "Приветствия", theory: "Dobrý deň." }, [1]),
      item: { id: 2, lesson_slug: "greetings", lesson_title: "Приветствия", question: "Ответьте.", instruction: "Напишите фразу.", created_at: "2026-10-05T00:00:00Z", latest_attempt: null },
      postUrl: "/api/v1/course/exercises",
      getUrl: "/api/v1/course/exercises",
    },
    {
      name: "reading",
      create: () => generateCourseReading({ lesson_slug: "greetings", lesson_title: "Приветствия", theory: "Dobrý deň.", completed_theory: "" }, [1]),
      item: { id: 2, lesson_slug: "greetings", lesson_title: "Приветствия", title: "Текст", text: "Dobrý deň.", instruction: "Перескажите.", created_at: "2026-10-05T00:00:00Z", offline_ready: true, latest_attempt: null },
      postUrl: "/api/v1/course/readings",
      getUrl: "/api/v1/course/readings",
    },
    {
      name: "homework",
      create: () => generateCourseHomework({ lesson_slug: "greetings", lesson_title: "Приветствия", theory: "Dobrý deň.", known_mistakes: [] }, [1]),
      item: { id: 2, lesson_slug: "greetings", lesson_title: "Приветствия", title: "Диалог", description: "Поздоровайтесь.", focus_category: "приветствие", created_at: "2026-10-05T00:00:00Z", offline_ready: true, latest_attempt: null },
      postUrl: "/api/v1/course/homework",
      getUrl: "/api/v1/course/homework",
    },
  ];

  for (const scenario of cases) await context.test(scenario.name, async () => {
    const calls: Array<{ url: string; method: string }> = [];
    globalThis.fetch = (async (input, init) => {
      calls.push({ url: String(input), method: init?.method ?? "GET" });
      return calls.length === 1
        ? new Response(null, { status: 500 })
        : new Response(JSON.stringify([scenario.item]), { status: 200, headers: { "Content-Type": "application/json" } });
    }) as typeof fetch;
    assert.deepEqual(await scenario.create(), scenario.item);
    assert.deepEqual(calls, [{ url: scenario.postUrl, method: "POST" }, { url: scenario.getUrl, method: "GET" }]);
  });
});

test("exercise and reading checks recover attempts saved before transient 500", async (context) => {
  const exerciseAttempt = { id: 12, answer: "Dobrý deň.", is_correct: true, score: 100, corrected_answer: "Dobrý deň.", explanation: "Верно.", next_exercise: "Продолжайте.", created_at: "2026-10-05T00:00:00Z" };
  const readingAttempt = { id: 13, retelling: "Человек поздоровался.", score: 100, feedback: "Верно.", corrected_retelling: "Человек поздоровался.", created_at: "2026-10-05T00:00:00Z" };
  const cases = [
    { name: "exercise", submit: () => answerCourseExercise(7, exerciseAttempt.answer, "online", 11), item: { id: 7, latest_attempt: exerciseAttempt }, postUrl: "/api/v1/course/exercises/7/answer", getUrl: "/api/v1/course/exercises", attempt: exerciseAttempt },
    { name: "reading", submit: () => checkCourseReading(8, readingAttempt.retelling, "online", 12), item: { id: 8, latest_attempt: readingAttempt }, postUrl: "/api/v1/course/readings/8/check", getUrl: "/api/v1/course/readings", attempt: readingAttempt },
  ];
  for (const scenario of cases) await context.test(scenario.name, async () => {
    const calls: Array<{ url: string; method: string }> = [];
    globalThis.fetch = (async (input, init) => {
      calls.push({ url: String(input), method: init?.method ?? "GET" });
      return calls.length === 1
        ? new Response(null, { status: 500 })
        : new Response(JSON.stringify([scenario.item]), { status: 200, headers: { "Content-Type": "application/json" } });
    }) as typeof fetch;
    assert.deepEqual(await scenario.submit(), scenario.attempt);
    assert.deepEqual(calls, [{ url: scenario.postUrl, method: "POST" }, { url: scenario.getUrl, method: "GET" }]);
  });
});

test("all single-item deletions recover when the item is already absent", async (context) => {
  const cases = [
    { name: "exercise", remove: () => deleteCourseExercise(7), deleteUrl: "/api/v1/course/exercises/7", getUrl: "/api/v1/course/exercises" },
    { name: "reading", remove: () => deleteCourseReading(8), deleteUrl: "/api/v1/course/readings/8", getUrl: "/api/v1/course/readings" },
    { name: "homework", remove: () => deleteCourseHomework(9), deleteUrl: "/api/v1/course/homework/9", getUrl: "/api/v1/course/homework" },
  ];
  for (const scenario of cases) await context.test(scenario.name, async () => {
    const calls: Array<{ url: string; method: string }> = [];
    globalThis.fetch = (async (input, init) => {
      calls.push({ url: String(input), method: init?.method ?? "GET" });
      return calls.length === 1
        ? new Response(null, { status: 500 })
        : new Response("[]", { status: 200, headers: { "Content-Type": "application/json" } });
    }) as typeof fetch;
    assert.deepEqual(await scenario.remove(), { deleted: true });
    assert.deepEqual(calls, [{ url: scenario.deleteUrl, method: "DELETE" }, { url: scenario.getUrl, method: "GET" }]);
  });
});

test("delete all course tasks sends the protected confirmation phrase", async () => {
  const calls: Array<{ url: string; method: string; body: string }> = [];
  globalThis.fetch = (async (input, init) => {
    calls.push({ url: String(input), method: init?.method ?? "GET", body: String(init?.body ?? "") });
    const body = init?.method === "DELETE"
      ? { deleted: true, exercises_deleted: 1, exercise_attempts_deleted: 1, readings_deleted: 1, reading_attempts_deleted: 1, homework_deleted: 1, homework_attempts_deleted: 1 }
      : [];
    return new Response(JSON.stringify(body), { status: 200, headers: { "Content-Type": "application/json" } });
  }) as typeof fetch;

  await deleteAllCourseTasks();
  assert.deepEqual(calls.at(-1), { url: "/api/v1/course/materials", method: "DELETE", body: JSON.stringify({ confirmation: "delete-all-course-tasks" }) });
});
