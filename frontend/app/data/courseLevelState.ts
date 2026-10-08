export type CourseLevel = "A1" | "A2";
export type CoursePosition = { activeModule: number; selectedSlug: string };
export type CoursePositions = Partial<Record<CourseLevel, CoursePosition>>;

// An expanded A2 module needs answers to its new questions; legacy A1 flags stay intact.
export function isCourseFinalCompleted(level: CourseLevel, storedCompleted: boolean, questionIds: string[], selections: Record<string, string>): boolean {
  return storedCompleted && (level === "A1" || (questionIds.length > 0 && questionIds.every((id) => Boolean(selections[id]))));
}

export function reopenExpandedA2Final(level: CourseLevel, key: string, completed: Record<string, boolean>, questionIds: string[], selections: Record<string, string>): Record<string, boolean> {
  return level === "A2" && completed[key] && !isCourseFinalCompleted(level, true, questionIds, selections)
    ? { ...completed, [key]: false } : completed;
}

export function resolveCoursePosition(
  modules: Array<{ order: number; lessons: Array<{ slug: string }> }>,
  position: Partial<CoursePosition> = {},
): CoursePosition {
  const module = modules.find((item) => item.lessons.some((lesson) => lesson.slug === position.selectedSlug))
    ?? modules.find((item) => item.order === position.activeModule) ?? modules[0];
  return { activeModule: module.order, selectedSlug: module.lessons.find((lesson) => lesson.slug === position.selectedSlug)?.slug ?? module.lessons[0].slug };
}

export function switchCourseLevel<T extends { activeLevel: CourseLevel; activeModule: number; selectedSlug: string; levelPositions: CoursePositions }>(
  state: T, level: CourseLevel, modules: Array<{ order: number; lessons: Array<{ slug: string }> }>,
): T {
  if (level === state.activeLevel) return state;
  const position = resolveCoursePosition(modules, state.levelPositions[level]);
  return { ...state, ...position, activeLevel: level, levelPositions: {
    ...state.levelPositions, [state.activeLevel]: { activeModule: state.activeModule, selectedSlug: state.selectedSlug }, [level]: position,
  } };
}

const qualifiedModuleKeyPattern = /^(a1|a2):([1-8])$/;
const legacyModuleKeyPattern = /^[1-8]$/;

export function courseModuleCompletionKey(level: CourseLevel, moduleOrder: number): string {
  if (!Number.isInteger(moduleOrder) || moduleOrder < 1 || moduleOrder > 8) {
    throw new RangeError(`Invalid course module order: ${moduleOrder}`);
  }
  return `${level.toLowerCase()}:${moduleOrder}`;
}

export function normalizeFinalCompletedModules(
  stored: Record<string, boolean> | undefined,
  legacyFinalCompleted = false,
): Record<string, boolean> {
  const source = { ...(legacyFinalCompleted ? { "1": true } : {}), ...(stored ?? {}) };
  const normalized: Record<string, boolean> = {};

  for (const [key, completed] of Object.entries(source)) {
    if (legacyModuleKeyPattern.test(key)) {
      normalized[`a1:${key}`] = completed;
      continue;
    }
    const qualified = qualifiedModuleKeyPattern.exec(key);
    if (qualified) normalized[`${qualified[1]}:${qualified[2]}`] = completed;
  }
  return normalized;
}
