export type MistakeReviewTask = { prompt: string; learnerAnswer: string; explanation: string; kind: "exact" | "open" };
export type TaskMistakeInput = { id: string; lessonSlug: string; prompt: string; answer: string; reviewTask?: MistakeReviewTask | null };
export type TaskOpenRequest = { id: number; nonce: number };
export function taskMistakeSource(id: string): { kind: "exercise" | "homework"; id: number } | null {
  const match = /^(exercise|homework):(\d+)$/.exec(id);
  return match ? { kind: match[1] as "exercise" | "homework", id: Number(match[2]) } : null;
}

// Detached backup reviews retain their task kind, but have no navigable ID.
export function taskMistakeKind(id: string): "exercise" | "homework" | null {
  const source = taskMistakeSource(id);
  if (source) return source.kind;
  const detached = /^detached:(exercise|homework):[0-9a-f]{64}$/.exec(id);
  return detached ? detached[1] as "exercise" | "homework" : null;
}
