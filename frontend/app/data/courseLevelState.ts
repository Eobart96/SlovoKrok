export type CourseLevel = "A1" | "A2";

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
