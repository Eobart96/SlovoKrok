export type HomeworkGenerationMode = "topic" | "section" | "module" | "progress" | "mistakes";

const HIDDEN_HOMEWORK_REFERENCE_SECTION_TITLES = new Set([
  "финальные опоры и самопроверка",
]);

export function homeworkReferenceSections<T extends { title: string }>(sections: T[]): T[] {
  return sections.filter((section) => !HIDDEN_HOMEWORK_REFERENCE_SECTION_TITLES.has(section.title.trim().toLocaleLowerCase("ru")));
}

export function homeworkModeInstructions(mode: HomeworkGenerationMode): string[] {
  if (mode !== "mistakes") return [];
  return [
    "Рабочая область: только активные ошибки из завершённых тем. Не добавляй новое правило.",
    "Формат: короткая домашняя работа на 5–10 минут из трёх связанных частей: вспомнить правило, применить его в новой фразе, самостоятельно написать одну короткую фразу.",
  ];
}

type HomeworkHintLesson = {
  title: string;
  theory: {
    summary: string;
    rules: string[];
    examples: Array<{ slovak: string; russian: string; explanation: string }>;
  };
};

function hintTokens(value: string): string[] {
  const ignored = new Set(["короткий", "короткую", "коротких", "словацком", "задание", "задания", "тема", "темы", "реплик", "напишите", "используйте", "содержание"]);
  return [...new Set(value.toLocaleLowerCase("ru").match(/[\p{L}\p{N}]+/gu)?.filter((token) => token.length >= 4 && !ignored.has(token)) ?? [])];
}

const homeworkSemanticGroups = [
  ["формал", "вежлив", "официал", "môžete", "voláte", "máte", "ste"],
  ["представ", "знаком", "volám", "voláte", "teší ma"],
  ["непони", "непонят", "повтор", "уточн", "nerozumiem", "zopakovať", "pomalšie"],
  ["поздоров", "привет", "dobrý deň", "ahoj"],
  ["прощ", "dovidenia", "maj sa"],
] as const;

function normalized(value: string): string {
  return value.toLocaleLowerCase("ru");
}

function tokenRoot(token: string): string {
  return token.length >= 7 ? token.slice(0, 6) : token;
}

function assignmentTextScore(candidate: string, { title, description, focusCategory }: { title: string; description: string; focusCategory: string }): number {
  const material = normalized(candidate);
  const tokenScore = [
    ...hintTokens(title).map((token) => ({ token, weight: 4 })),
    ...hintTokens(focusCategory).map((token) => ({ token, weight: 5 })),
    ...hintTokens(description).map((token) => ({ token, weight: 1 })),
  ].reduce((score, { token, weight }) => score + (material.includes(tokenRoot(token)) ? weight : 0), 0);
  const assignment = normalized(`${title} ${description} ${focusCategory}`);
  const semanticScore = homeworkSemanticGroups.reduce((score, group) => {
    const assignmentMatches = group.some((marker) => assignment.includes(marker));
    const candidateMatches = group.some((marker) => material.includes(marker));
    return score + (assignmentMatches && candidateMatches ? 8 : 0);
  }, 0);
  return tokenScore + semanticScore;
}

function lessonMaterial(lesson: HomeworkHintLesson): string {
  return [
    lesson.title,
    lesson.theory.summary,
    ...lesson.theory.rules,
    ...lesson.theory.examples.flatMap((example) => [example.slovak, example.russian, example.explanation]),
  ].join(" ");
}

export function rankHomeworkReferenceLessons<T extends HomeworkHintLesson>(assignment: { title: string; description: string; focusCategory: string }, lessons: T[]): T[] {
  return lessons
    .map((lesson, index) => ({ lesson, index, score: assignmentTextScore(lessonMaterial(lesson), assignment) }))
    .sort((left, right) => right.score - left.score || left.index - right.index)
    .map(({ lesson }) => lesson);
}

export function selectHomeworkReferenceLessons<T extends HomeworkHintLesson>(assignment: { title: string; description: string; focusCategory: string }, lessons: T[], limit = 3): T[] {
  const scored = lessons
    .map((lesson, index) => ({ lesson, index, score: assignmentTextScore(lessonMaterial(lesson), assignment) }))
    .sort((left, right) => right.score - left.score || left.index - right.index);
  const cutoff = Math.max(1, (scored[0]?.score ?? 0) * 0.35);
  return scored.filter(({ score }) => score >= cutoff).slice(0, limit).map(({ lesson }) => lesson);
}

export function homeworkAssignmentHints({
  title,
  description,
  focusCategory,
  lessons,
}: {
  title: string;
  description: string;
  focusCategory: string;
  lessons: HomeworkHintLesson[];
}): string[] {
  if (!lessons.length) return [`Разберите условие «${title}» по шагам и проверьте правило «${focusCategory}» в завершённой теме.`];
  const assignment = { title, description, focusCategory };
  const relevantLessons = selectHomeworkReferenceLessons(assignment, lessons);
  const selectedLessons = relevantLessons.length ? relevantLessons : rankHomeworkReferenceLessons(assignment, lessons).slice(0, 1);
  return selectedLessons.map((lesson) => {
    const rule = [...lesson.theory.rules].sort((left, right) => assignmentTextScore(right, assignment) - assignmentTextScore(left, assignment))[0] ?? lesson.theory.summary;
    const example = [...lesson.theory.examples].sort((left, right) => assignmentTextScore(`${right.slovak} ${right.russian} ${right.explanation}`, assignment) - assignmentTextScore(`${left.slovak} ${left.russian} ${left.explanation}`, assignment))[0];
    return example
      ? `Тема «${lesson.title}»: ${rule} Модель: ${example.slovak} — ${example.russian}.`
      : `Тема «${lesson.title}»: ${rule}`;
  });
}
