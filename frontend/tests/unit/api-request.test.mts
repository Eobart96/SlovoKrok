import assert from "node:assert/strict";
import test from "node:test";

import { ApiError, ApiRequestError } from "../../app/lib/apiError.ts";
import { aiRequestTimeoutMs, defaultRequestTimeoutMs, requestJson } from "../../app/lib/request.ts";

const originalFetch = globalThis.fetch;

test.afterEach(() => {
  globalThis.fetch = originalFetch;
});

test("request policy keeps AI timeout beyond the backend maximum", () => {
  assert.equal(defaultRequestTimeoutMs, 30_000);
  assert.equal(aiRequestTimeoutMs, 310_000);
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
