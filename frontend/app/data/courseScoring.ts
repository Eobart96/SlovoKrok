export function scoreLessonUnderstanding(results: boolean[], activeMistakeCount: number): number {
  const correct = results.filter(Boolean).length;
  const rawPercent = results.length ? correct / results.length * 100 : 0;
  const penalty = Math.min(15, Math.max(0, activeMistakeCount) * 3);
  return Math.max(0, Math.min(100, Math.round(rawPercent - penalty)));
}
