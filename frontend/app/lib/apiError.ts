export class ApiError extends Error {
  readonly status: number;
  readonly body: unknown;

  constructor(message: string, status: number, body?: unknown) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.body = body;
  }
}

export type ApiRequestFailureKind = "timeout" | "cancelled" | "network" | "invalid-response";

export class ApiRequestError extends Error {
  readonly kind: ApiRequestFailureKind;
  readonly cause: unknown;

  constructor(message: string, kind: ApiRequestFailureKind, cause?: unknown) {
    super(message);
    this.name = "ApiRequestError";
    this.kind = kind;
    this.cause = cause;
  }
}

export function apiErrorMessage(body: unknown, status: number): string {
  return typeof body === "object" && body !== null && "detail" in body
    ? String((body as { detail: unknown }).detail)
    : `Ошибка сервера (${status})`;
}
