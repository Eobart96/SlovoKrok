import type { CourseModule, CourseTopicGroup } from "../../../courseTypes";
import { plannedA2Module2 } from "../../../a2CourseRoadmap";
import { a2NominativePluralThingsLesson } from "./lessons/nominative-plural-things";

const lessons = [a2NominativePluralThingsLesson];

const topicGroups: CourseTopicGroup[] = [
  {
    id: "a2-m2-plural-and-accusative",
    title: "Множественное число и Akuzatív",
    slovakTitle: "Množné číslo a akuzatív",
    description: "Полное согласование групп предметов и дальнейшая работа с прямым объектом.",
    lessonSlugs: lessons.map((lesson) => lesson.slug),
  },
];

export const a2Module2: CourseModule = {
  slug: plannedA2Module2.slug,
  order: plannedA2Module2.order,
  title: plannedA2Module2.title,
  level: "A2",
  description: plannedA2Module2.description,
  lessons,
  topicGroups,
  contentRequirements: {
    minSections: 5,
    minCoreSections: 5,
    minStepPractices: 5,
    minTheoryRules: 5,
    minTheoryExamples: 5,
    minKnowledgeChecks: 3,
    minFinalChecks: 2,
    requirePracticeForEverySection: true,
  },
};

export const a2Module2Lessons = a2Module2.lessons;
