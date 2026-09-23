import { ApiError, ApiRequestError, apiErrorMessage } from "./apiError.ts";

export const defaultRequestTimeoutMs = 30_000;
export const aiRequestTimeoutMs = 310_000;

export type ApiRequestInit = RequestInit & { timeoutMs?: number };

export async function requestJson<T>(path: string, init: ApiRequestInit = {}): Promise<T> {
  const { timeoutMs = defaultRequestTimeoutMs, signal: callerSignal, ...fetchInit } = init;
  const controller = new AbortController();
  let timedOut = false;
  const cancelFromCaller = () => controller.abort(callerSignal?.reason);

  if (callerSignal?.aborted) cancelFromCaller();
  else callerSignal?.addEventListener("abort", cancelFromCaller, { once: true });

  const timeout = globalThis.setTimeout(() => {
    timedOut = true;
    controller.abort();
  }, timeoutMs);

  try {
    let response: Response;
    try {
      response = await fetch(`/api/v1${path}`, {
        ...fetchInit,
        headers: { "Content-Type": "application/json", ...fetchInit.headers },
        signal: controller.signal,
      });
    } catch (error) {
      if (timedOut) throw new ApiRequestError("Сервер не ответил вовремя. Попробуйте ещё раз.", "timeout", error);
      if (callerSignal?.aborted) throw new ApiRequestError("Запрос отменён.", "cancelled", error);
      throw new ApiRequestError("Не удалось связаться с локальным сервером.", "network", error);
    }
    if (!response.ok) {
      const body: unknown = await response.json().catch(() => null);
      throw new ApiError(apiErrorMessage(body, response.status), response.status, body);
    }
    try {
      return await response.json() as T;
    } catch (error) {
      if (timedOut) throw new ApiRequestError("Сервер не ответил вовремя. Попробуйте ещё раз.", "timeout", error);
      if (callerSignal?.aborted) throw new ApiRequestError("Запрос отменён.", "cancelled", error);
      throw new ApiRequestError("Локальный сервер вернул некорректный ответ.", "invalid-response", error);
    }
  } finally {
    globalThis.clearTimeout(timeout);
    callerSignal?.removeEventListener("abort", cancelFromCaller);
  }
}
