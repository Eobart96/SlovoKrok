import type { CourseModule } from "../../../courseTypes";
import { plannedA2Module4 } from "../../../a2CourseRoadmap";
import { a2AspectInNarrativeLesson } from "./lessons/aspect-in-narrative";
import { a2AspectPrefixPairsLesson } from "./lessons/aspect-prefix-pairs";
import { a2AspectStemPairsLesson } from "./lessons/aspect-stem-pairs";

const lessons = [a2AspectInNarrativeLesson, a2AspectPrefixPairsLesson, a2AspectStemPairsLesson];

export const a2Module4: CourseModule = {
  slug: plannedA2Module4.slug, order: 4, title: plannedA2Module4.title,
  level: "A2", description: plannedA2Module4.description, lessons,
  topicGroups: [{ id: "a2-m4-narrative-and-pairs", title: "Рассказ и видовые пары", slovakTitle: "Rozprávanie a vidové dvojice", description: "Фон и событие, приставки, суффиксы и смена основы.", lessonSlugs: lessons.map(({ slug }) => slug) }],
  contentRequirements: { minSections: 5, minCoreSections: 5, minStepPractices: 7, minTheoryRules: 5, minTheoryExamples: 5, minKnowledgeChecks: 3, minFinalChecks: 2, requirePracticeForEverySection: true },
};
