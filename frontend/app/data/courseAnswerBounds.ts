// Matches the CourseState saved-answer bound. Never silently truncate input.
export const courseAnswerMaxLength = 2000;

export function canUpdateCourseAnswer(previous: string, next: string): boolean {
  return next.length <= courseAnswerMaxLength
    || (previous.length > courseAnswerMaxLength && next.length < previous.length);
}
