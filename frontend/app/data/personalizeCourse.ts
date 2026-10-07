import type { LearnerProfile } from "../lib/api";
import type { CourseModule } from "./courseTypes";

export function personalizeText(text: string, profile: LearnerProfile): string {
  let value = text;
  if (profile.name && profile.slovak_name) {
    value = value.replace(/(?<!\p{L})Ари(?!\p{L})/gu, () => profile.name);
    value = value.replace(/\bAri\b/g, () => profile.slovak_name);
  }
  if (profile.occupation && profile.occupation_sentence_sk) value = value.replace(/Pracujem v IT\./g, () => profile.occupation_sentence_sk.replace(/[.!?]+$/, "") + ".");
  if (profile.occupation && profile.occupation_sentence_sk) value = value.replace(/Я работаю в (?:IT|ИТ)\./g, () => profile.occupation.replace(/[.!?]+$/, "") + ".");
  return value;
}

function transform<T>(value: T, profile: LearnerProfile, key = ""): T {
  if (["id", "slug", "audio", "lessonSlugs"].includes(key)) return value;
  if (typeof value === "string") return personalizeText(value, profile) as T;
  if (Array.isArray(value)) return value.map((item) => transform(item, profile)) as T;
  if (value && typeof value === "object") return Object.fromEntries(Object.entries(value).map(([name, item]) => [name, transform(item, profile, name)])) as T;
  return value;
}

export function personalizeModule(module: CourseModule, profile: LearnerProfile): CourseModule {
  return { ...module, lessons: module.lessons.map((lesson) => {
    const personalized = transform(lesson, profile);
    // Fixed tests keep their authored text and answer contract across profile changes.
    return { ...personalized, knowledgeChecks: lesson.knowledgeChecks, finalChecks: lesson.finalChecks, stepPractices: lesson.stepPractices, reinforcementPractices: lesson.reinforcementPractices, listening: lesson.listening };
  }) };
}
