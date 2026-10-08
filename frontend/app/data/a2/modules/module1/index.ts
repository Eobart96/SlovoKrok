import type { CourseModule, CourseTopicGroup } from "../../../courseTypes";
import { plannedA2Module1 } from "../../../a2CourseRoadmap";
import { a2ReadinessForA2Lesson } from "./lessons/readiness-for-a2";
import { a2VerbAspectLesson } from "./lessons/verb-aspect";
import { a2CliticsWordOrderLesson } from "./lessons/clitics-word-order";
import { a2WordFamiliesLesson } from "./lessons/word-families";
import { a2CaseMapGovernmentLesson } from "./lessons/case-map-government";
import { a2CoherenceFocusLesson } from "./lessons/coherence-focus";
import { a2ConnectedPronunciationLesson } from "./lessons/connected-pronunciation";

const lessons = [a2ReadinessForA2Lesson, a2VerbAspectLesson, a2CliticsWordOrderLesson, a2WordFamiliesLesson, a2CaseMapGovernmentLesson, a2CoherenceFocusLesson, a2ConnectedPronunciationLesson];
const topicGroups: CourseTopicGroup[] = [
  { id: "a2-m1-foundation-and-aspect", title: "Готовность и вид глагола", slovakTitle: "Pripravenosť a slovesný vid", description: "Точечное повторение A1 и различение процесса, повтора и результата.", lessonSlugs: lessons.slice(0, 2).map((lesson) => lesson.slug) },
  { id: "a2-m1-words-and-government", title: "Структура фразы и словарные связи", slovakTitle: "Stavba vety a slovné vzťahy", description: "Клитики, семьи слов и обзорная карта падежей.", lessonSlugs: lessons.slice(2, 5).map((lesson) => lesson.slug) },
  { id: "a2-m1-connected-speech", title: "Связность и произношение", slovakTitle: "Súdržnosť a výslovnosť", description: "Понятный смысловой акцент и самостоятельная тренировка связной речи.", lessonSlugs: lessons.slice(5, 7).map((lesson) => lesson.slug) },
];

export const a2Module1: CourseModule = {
  slug: plannedA2Module1.slug, order: 1, title: plannedA2Module1.title, level: "A2", description: plannedA2Module1.description,
  lessons, topicGroups,
  contentRequirements: { minSections: 5, minCoreSections: 5, minStepPractices: 5, minTheoryRules: 5, minTheoryExamples: 5, minKnowledgeChecks: 3, minFinalChecks: 2, requirePracticeForEverySection: true },
};
