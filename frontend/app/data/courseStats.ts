import { buildReinforcementPractices, isCorePractice } from "./coursePractice";
import { type LessonSummary, type MistakeRecord } from "./courseProgress";
import { type CourseLesson, type CourseModule, type LessonStatus } from "./courseTypes";
import { learnedVocabularySeeds } from "./courseVocabulary";

export type PersonalModuleStats = {
  order: number;
  title: string;
  completed: number;
  lessons: number;
  solved: number;
  activities: number;
  accuracy: number;
};

export type PersonalCourseStats = {
  completedLessons: number;
  totalLessons: number;
  completionPercent: number;
  accuracy: number;
  vocabularyCount: number;
  activeMistakes: number;
  masteredMistakes: number;
  dueMistakes: number;
  averageUnderstanding: number | null;
  nextAction: string;
  moduleStats: PersonalModuleStats[];
};

function moduleActivityStats(
  module: CourseModule,
  practiceResults: Record<string, boolean>,
  checkSelections: Record<string, string>,
  mistakes: Record<string, MistakeRecord>,
): Pick<PersonalModuleStats, "solved" | "activities" | "accuracy"> {
  const lessonSlugs = new Set(module.lessons.map((lesson) => lesson.slug));
  const optionalIds = new Set(module.lessons.flatMap((lesson) => lesson.stepPractices.filter((practice) => !isCorePractice(lesson, practice)).map((practice) => practice.id)));
  const activities = module.lessons.reduce((total, lesson) => total
    + lesson.stepPractices.filter((practice) => isCorePractice(lesson, practice)).length
    + (lesson.assessmentMode === "interactive" ? buildReinforcementPractices(lesson).length : lesson.knowledgeChecks.length), 0);
  const solved = module.lessons.reduce((total, lesson) => total
    + lesson.stepPractices.filter((practice) => isCorePractice(lesson, practice) && practiceResults[practice.id]).length
    + (lesson.assessmentMode === "interactive"
      ? buildReinforcementPractices(lesson).filter((practice) => practiceResults[practice.id]).length
      : lesson.knowledgeChecks.filter((check) => checkSelections[check.id] === check.answer).length), 0);
  const incorrectAttempts = Object.values(mistakes)
    .filter((mistake) => lessonSlugs.has(mistake.lessonSlug) && !optionalIds.has(mistake.id))
    .reduce((total, mistake) => total + mistake.attempts, 0);
  return { solved, activities, accuracy: solved + incorrectAttempts === 0 ? 0 : Math.round(solved / (solved + incorrectAttempts) * 100) };
}

function nextLesson(lessons: CourseLesson[], progress: Record<string, LessonStatus>): CourseLesson | undefined {
  return lessons.find((lesson) => progress[lesson.slug] === "in_progress")
    ?? lessons.find((lesson) => progress[lesson.slug] !== "completed");
}

export function buildPersonalCourseStats({
  modules,
  progress,
  practiceResults,
  checkSelections,
  mistakes,
  summaries,
  nowMs = Date.now(),
}: {
  modules: CourseModule[];
  progress: Record<string, LessonStatus>;
  practiceResults: Record<string, boolean>;
  checkSelections: Record<string, string>;
  mistakes: Record<string, MistakeRecord>;
  summaries: Record<string, LessonSummary>;
  nowMs?: number;
}): PersonalCourseStats {
  const lessons = modules.flatMap((module) => module.lessons);
  const optionalIds = new Set(lessons.flatMap((lesson) => lesson.stepPractices.filter((practice) => !isCorePractice(lesson, practice)).map((practice) => practice.id)));
  const completedSlugs = lessons.filter((lesson) => progress[lesson.slug] === "completed").map((lesson) => lesson.slug);
  const active = Object.values(mistakes).filter((mistake) => !mistake.mastered);
  const mastered = Object.values(mistakes).filter((mistake) => mistake.mastered);
  const due = active.filter((mistake) => !mistake.dueAt || Date.parse(mistake.dueAt) <= nowMs);
  const completedUnderstanding = completedSlugs.map((slug) => summaries[slug]?.understanding).filter((value): value is number => typeof value === "number");
  const moduleStats = modules.map((module) => {
    const activityStats = moduleActivityStats(module, practiceResults, checkSelections, mistakes);
    return {
      order: module.order,
      title: module.title,
      completed: module.lessons.filter((lesson) => progress[lesson.slug] === "completed").length,
      lessons: module.lessons.length,
      ...activityStats,
    };
  });
  const totalSolved = moduleStats.reduce((total, module) => total + module.solved, 0);
  const totalIncorrectAttempts = Object.values(mistakes).filter((mistake) => !optionalIds.has(mistake.id)).reduce((total, mistake) => total + mistake.attempts, 0);
  const upcomingLesson = nextLesson(lessons, progress);
  const nextAction = due.length
    ? due.length === 1 ? "Повторите 1 ошибку, доступную сейчас." : `Повторите ${due.length} ошибок, доступных сейчас.`
    : active.length
      ? "Продолжайте обучение: следующее повторение ошибок уже запланировано."
      : upcomingLesson
        ? `${progress[upcomingLesson.slug] === "in_progress" ? "Завершите" : "Начните"} тему «${upcomingLesson.title}».`
        : "Курс завершён — поддерживайте результат повторением слов и чтением.";

  return {
    completedLessons: completedSlugs.length,
    totalLessons: lessons.length,
    completionPercent: lessons.length ? Math.round(completedSlugs.length / lessons.length * 100) : 0,
    accuracy: totalSolved + totalIncorrectAttempts === 0 ? 0 : Math.round(totalSolved / (totalSolved + totalIncorrectAttempts) * 100),
    vocabularyCount: learnedVocabularySeeds(lessons, completedSlugs).length,
    activeMistakes: active.length,
    masteredMistakes: mastered.length,
    dueMistakes: due.length,
    averageUnderstanding: completedUnderstanding.length ? Math.round(completedUnderstanding.reduce((total, value) => total + value, 0) / completedUnderstanding.length) : null,
    nextAction,
    moduleStats,
  };
}
