export type LearningMode = "online" | "offline";

export const learningModeStorageKey = "slovokrok-learning-mode-v1";

export function readLearningMode(value: string | null): LearningMode {
  return value === "offline" ? "offline" : "online";
}
