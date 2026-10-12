import { plannedA2Module7 } from "../../../a2CourseRoadmap";
import type { CourseLesson, KnowledgeCheck, StepPractice } from "../../../courseTypes";

type Content = Omit<CourseLesson, "slug" | "order" | "title" | "slovakTitle" | "description" | "stepPractices" | "knowledgeChecks" | "finalChecks"> & {
  stepPractices: Array<Omit<StepPractice, "id">>;
  knowledgeChecks: Array<Omit<KnowledgeCheck, "id">>;
  finalChecks: Array<Omit<KnowledgeCheck, "id">>;
};

export function defineA2Module7Lesson(slug: string, content: Content): CourseLesson {
  const index = plannedA2Module7.lessons.findIndex((lesson) => lesson.slug === slug);
  const planned = plannedA2Module7.lessons[index];
  if (!planned) throw new Error(`Unknown A2 Module 7 lesson: ${slug}`);
  const prefix = `a2-m7-${slug.replace(/^a2-/, "")}`;
  return {
    ...content, slug, order: index + 1, title: planned.title, slovakTitle: planned.slovakTitle, description: planned.outcome,
    stepPractices: content.stepPractices.map((practice, index) => ({ ...practice, id: `${prefix}-step-${index + 1}` })),
    knowledgeChecks: content.knowledgeChecks.map((check, index) => ({ ...check, id: `${prefix}-check-${index + 1}` })),
    finalChecks: content.finalChecks.map((check, index) => ({ ...check, id: `${prefix}-final-${index + 1}` })),
  };
}
