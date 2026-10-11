import type { StepPractice } from "./courseTypes";
import type { MistakeReviewTask } from "./taskMistakes";

export function practiceReviewPrompt(practice: StepPractice): string {
  if (practice.type === "pairs" && practice.pairs?.length) {
    return [practice.prompt, ...practice.pairs.map((pair, index) => `${index + 1}. ${pair.prompt}${pair.options?.length ? `\nВарианты: ${pair.options.join(" / ")}` : ""}`), "Запишите ответы по порядку через точку с запятой (;)."].join("\n\n");
  }
  return [practice.prompt, practice.type === "order" && practice.tokens?.length ? `Слова: ${practice.tokens.join(" / ")}` : ""].filter(Boolean).join("\n\n");
}

export function readableMistakeAnswer(value: string): string {
  try {
    const parsed: unknown = JSON.parse(value);
    if (Array.isArray(parsed) && parsed.every((item) => typeof item === "string")) return parsed.map((item, index) => `${index + 1}. ${item || "Ответ не дан"}`).join("\n");
  } catch { /* Plain text and older semicolon-separated answers are already readable. */ }
  return value;
}

export function practiceMistakeReview(practice: StepPractice, learnerAnswer: string): MistakeReviewTask {
  return { prompt: practiceReviewPrompt(practice), learnerAnswer, explanation: [practice.hint, practice.explanation].filter(Boolean).join("\n"), kind: "exact" };
}
