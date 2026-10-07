import { plannedA2Module2 } from "../../../a2CourseRoadmap";
import type { CourseLesson, KnowledgeCheck, StepPractice } from "../../../courseTypes";

type PracticeSeed = Omit<StepPractice, "id">;
type CheckSeed = Omit<KnowledgeCheck, "id">;

export type A2Module2LessonContent = Omit<
  CourseLesson,
  "slug" | "order" | "title" | "slovakTitle" | "description" | "stepPractices" | "knowledgeChecks" | "finalChecks"
> & {
  stepPractices: PracticeSeed[];
  knowledgeChecks: CheckSeed[];
  finalChecks: CheckSeed[];
};

export function defineA2Module2Lesson(slug: string, content: A2Module2LessonContent): CourseLesson {
  const orderIndex = plannedA2Module2.lessons.findIndex((lesson) => lesson.slug === slug);
  const planned = plannedA2Module2.lessons[orderIndex];
  if (!planned || orderIndex < 0) throw new Error(`Unknown A2 Module 2 lesson: ${slug}`);
  const activityPrefix = `a2-m2-${slug.replace(/^a2-/, "")}`;

  return {
    ...content,
    slug,
    order: orderIndex + 1,
    title: planned.title,
    slovakTitle: planned.slovakTitle,
    description: planned.outcome,
    stepPractices: content.stepPractices.map((practice, index) => ({
      ...practice,
      id: `${activityPrefix}-step-${index + 1}`,
    })),
    knowledgeChecks: content.knowledgeChecks.map((check, index) => ({
      ...check,
      id: `${activityPrefix}-check-${index + 1}`,
    })),
    finalChecks: content.finalChecks.map((check, index) => ({
      ...check,
      id: `${activityPrefix}-final-${index + 1}`,
    })),
  };
}
