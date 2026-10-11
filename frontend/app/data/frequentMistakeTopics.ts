import type { MistakeRecord } from "./courseProgress";

export type FrequentMistakeTopic = { lessonSlug: string; attempts: number; active: number; corrected: number; repeated: number };
export const topicRuleReviewThreshold = 3;

export function needsTopicRuleReview(mistakes: Record<string, MistakeRecord>, lessonSlug: string): boolean {
  const newAttempts = Object.values(mistakes).reduce((total, mistake) => total + (mistake.lessonSlug === lessonSlug ? Math.max(0, mistake.attempts - (mistake.rulesReviewedAttempts ?? 0)) : 0), 0);
  return newAttempts >= topicRuleReviewThreshold;
}

export function markTopicRulesReviewed(mistakes: Record<string, MistakeRecord>, lessonSlug: string): Record<string, MistakeRecord> {
  return Object.fromEntries(Object.entries(mistakes).map(([id, mistake]) => [id, mistake.lessonSlug === lessonSlug ? { ...mistake, rulesReviewedAttempts: mistake.attempts } : mistake]));
}

// Use only explicit lesson links. A task covering a module or the whole course
// does not prove that every topic in that scope caused a mistake.
export function frequentMistakeTopics(mistakes: Record<string, MistakeRecord>, lessonSlugs: ReadonlySet<string>): FrequentMistakeTopic[] {
  const topics = new Map<string, FrequentMistakeTopic>();
  for (const mistake of Object.values(mistakes)) {
    if (!lessonSlugs.has(mistake.lessonSlug)) continue;
    const topic = topics.get(mistake.lessonSlug) ?? { lessonSlug: mistake.lessonSlug, attempts: 0, active: 0, corrected: 0, repeated: 0 };
    topic.attempts += mistake.attempts;
    topic.repeated += Math.max(0, mistake.attempts - 1);
    if (mistake.mastered) topic.corrected++;
    else topic.active++;
    topics.set(mistake.lessonSlug, topic);
  }
  return [...topics.values()].filter((topic) => needsTopicRuleReview(mistakes, topic.lessonSlug))
    .sort((left, right) => right.attempts - left.attempts || right.repeated - left.repeated || right.active - left.active || left.lessonSlug.localeCompare(right.lessonSlug));
}
