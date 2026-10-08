import type { CourseLesson, CourseModule, CourseTopicGroup } from "./courseTypes.ts";

export type CourseGenerationMode = "topic" | "section" | "module" | "progress" | "mistakes";

export type CourseGenerationScope = {
  mode: CourseGenerationMode;
  storageSlug: string;
  title: string;
  lessons: CourseLesson[];
  lesson?: CourseLesson;
  section?: CourseTopicGroup;
  sectionModule?: CourseModule;
  module?: CourseModule;
};

export type CompletedCourseModule = {
  module: CourseModule;
  lessons: CourseLesson[];
};

export type CompletedCourseSection = {
  key: string;
  module: CourseModule;
  section: CourseTopicGroup;
  lessons: CourseLesson[];
};

export function completedCourseModules(modules: CourseModule[], completedLessonSlugs: string[]): CompletedCourseModule[] {
  const completed = new Set(completedLessonSlugs);
  return modules
    .map((module) => ({ module, lessons: module.lessons.filter((lesson) => completed.has(lesson.slug)) }))
    .filter(({ lessons }) => lessons.length > 0);
}

export function completedCourseSections(modules: CourseModule[], completedLessonSlugs: string[]): CompletedCourseSection[] {
  const completed = new Set(completedLessonSlugs);
  return modules.flatMap((module) => (module.topicGroups ?? []).map((section) => ({
    key: `${module.slug}:${section.id}`,
    module,
    section,
    lessons: module.lessons.filter((lesson) => section.lessonSlugs.includes(lesson.slug) && completed.has(lesson.slug)),
  }))).filter(({ lessons }) => lessons.length > 0);
}

export function isCourseGenerationScopeSlug(modules: CourseModule[], slug: string): boolean {
  const a2 = modules[0]?.level === "A2";
  if (slug === (a2 ? "course:a2:progress" : "course-progress") || slug === (a2 ? "course:a2:mistakes" : "course-mistakes")) return true;
  return modules.some((module) => module.lessons.some((lesson) => lesson.slug === slug)
    || slug === `module:${module.slug}`
    || module.topicGroups?.some((section) => slug === `section:${module.slug}:${section.id}`));
}

export function buildCourseGenerationScope({
  mode,
  modules,
  completedLessonSlugs,
  lessonSlug,
  sectionKey,
  moduleSlug,
}: {
  mode: CourseGenerationMode;
  modules: CourseModule[];
  completedLessonSlugs: string[];
  lessonSlug?: string;
  sectionKey?: string;
  moduleSlug?: string;
}): CourseGenerationScope {
  const completedSet = new Set(completedLessonSlugs);
  const lessons = modules.flatMap((module) => module.lessons).filter((lesson) => completedSet.has(lesson.slug));
  const lesson = lessons.find((item) => item.slug === lessonSlug) ?? lessons[0];
  const sectionOptions = completedCourseSections(modules, completedLessonSlugs);
  const selectedSection = sectionOptions.find(({ key }) => key === sectionKey) ?? sectionOptions[0];
  const moduleOptions = completedCourseModules(modules, completedLessonSlugs);
  const selectedModule = moduleOptions.find(({ module }) => module.slug === moduleSlug) ?? moduleOptions[0];

  if (mode === "section" && selectedSection) {
    return {
      mode,
      storageSlug: `section:${selectedSection.key}`,
      title: `${selectedSection.section.title} · Модуль ${selectedSection.module.order}`,
      lessons: selectedSection.lessons,
      section: selectedSection.section,
      sectionModule: selectedSection.module,
    };
  }

  if (mode === "module" && selectedModule) {
    return {
      mode,
      storageSlug: `module:${selectedModule.module.slug}`,
      title: `Модуль ${selectedModule.module.order}. ${selectedModule.module.title}`,
      lessons: selectedModule.lessons,
      module: selectedModule.module,
    };
  }

  const level = modules[0]?.level ?? "A1";
  if (mode === "mistakes") return { mode, storageSlug: level === "A2" ? "course:a2:mistakes" : "course-mistakes", title: "Работа над ошибками", lessons };
  if (mode === "progress") return { mode, storageSlug: level === "A2" ? "course:a2:progress" : "course-progress", title: `Общий прогресс Slovak ${level}`, lessons };
  return { mode: "topic", storageSlug: lesson?.slug ?? "", title: lesson?.title ?? "Завершённая тема", lessons: lesson ? [lesson] : [], lesson };
}
