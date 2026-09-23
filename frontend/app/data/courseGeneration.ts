import type { CourseLesson } from "./courseTypes";
import { learnedVocabularyContext } from "./courseVocabulary";

export type GenerationMode = "topic" | "progress";
export type GenerationMistakeHint = { lessonSlug: string; text: string };

const contextLimit = 12_000;

export const exerciseFormats = [
  { label: "Перевод на словацкий", interactionType: "text", instruction: "Дай короткую русскую фразу для перевода на словацкий." },
  { label: "Заполни пропуск", interactionType: "choice", instruction: "Дай словацкую фразу с одним пропуском и 3–5 коротких вариантов для него." },
  { label: "Найди правильную фразу", interactionType: "choice", instruction: "Дай 3–4 похожие словацкие фразы, среди которых только одна нормативна." },
  { label: "Собери фразу", interactionType: "order", instruction: "Дай слова одной короткой словацкой фразы в перемешанном порядке." },
  { label: "Соедини пары", interactionType: "match", instruction: "Дай 3–5 пар из коротких словацких слов или фраз и их русских соответствий." },
  { label: "Ответь в ситуации", interactionType: "choice", instruction: "Опиши по-русски простую бытовую ситуацию и дай 3–4 варианта словацкой реплики." },
  { label: "Преобразуй фразу", interactionType: "text", instruction: "Дай одну короткую словацкую фразу и попроси изменить только один признак, доступный в пройденном материале: лицо, число, отрицание или вопрос." },
] as const;

export type ExerciseFormat = (typeof exerciseFormats)[number];

function detailedTheory(lesson: CourseLesson): string {
  return [
    lesson.theory.summary,
    ...lesson.theory.rules,
    ...lesson.theory.examples.map((example) => `${example.slovak} — ${example.russian}. ${example.explanation}`),
  ].join("\n");
}

function compactTheory(lesson: CourseLesson): string {
  return [`Тема: ${lesson.title}`, lesson.theory.summary, ...lesson.theory.rules].join("\n");
}

function trimAtLine(value: string, maxLength: number): string {
  if (value.length <= maxLength) return value;
  const shortened = value.slice(0, maxLength);
  const lastLine = shortened.lastIndexOf("\n");
  return (lastLine > maxLength / 2 ? shortened.slice(0, lastLine) : shortened).trimEnd();
}

function mistakeContext(hints: GenerationMistakeHint[]): string {
  if (!hints.length) return "Сохранённых ошибок в этом материале нет.";
  return trimAtLine(`Сохранённые ошибки ученика, которые полезно отработать:\n${hints.slice(0, 20).map((hint) => `- ${hint.text}`).join("\n")}`, 2_500);
}

function appendWithinLimit(parts: string[], candidate: string, limit = contextLimit): boolean {
  const separatorLength = parts.length ? 2 : 0;
  if (parts.join("\n\n").length + separatorLength + candidate.length > limit) return false;
  parts.push(candidate);
  return true;
}

function lessonExerciseExamples(lesson: CourseLesson): string[] {
  const practices = lesson.stepPractices.flatMap((practice) => practice.pairs?.length
    ? practice.pairs.map((pair) => `${pair.prompt} → ${pair.answer}`)
    : [`${practice.prompt} → ${practice.answer}`]);
  const checks = [...lesson.knowledgeChecks, ...lesson.finalChecks].map((check) => `${check.question} → ${check.answer}`);
  return [...checks, ...practices].slice(0, 4);
}

export function nextExerciseFormat(existingCount: number): ExerciseFormat {
  return exerciseFormats[Math.max(0, existingCount) % exerciseFormats.length];
}

export function buildExerciseGenerationContext({
  baseContext,
  format,
  sourceLessons,
}: {
  baseContext: string;
  format: ExerciseFormat;
  sourceLessons: CourseLesson[];
}): string {
  const examples = sourceLessons.flatMap((lesson) => lessonExerciseExamples(lesson).slice(0, 2).map((example) => `- ${lesson.title}: ${example}`)).slice(0, 6);
  const formatContext = [
    `Формат нового упражнения: ${format.label}.`,
    `Тип интерактива: ${format.interactionType}.`,
    format.instruction,
    "Сохрани этот формат. Создай новый пример, а не копию приведённой проверки. Нужен один короткий ответ на словацком без вариантов выбора.",
    examples.length ? `Ориентиры из упражнений и тестов пройденных тем:\n${examples.join("\n")}` : "Ориентиров из тестов пока нет; придумай простой пример строго по материалу.",
  ].join("\n");
  const availableForBase = Math.max(0, contextLimit - formatContext.length - 2);
  return `${trimAtLine(baseContext, availableForBase)}\n\n${formatContext}`.trim();
}

export function buildProgressGenerationContext({
  mode,
  selectedLesson,
  completedLessons,
  mistakeHints,
}: {
  mode: GenerationMode;
  selectedLesson?: CourseLesson;
  completedLessons: CourseLesson[];
  mistakeHints: GenerationMistakeHint[];
}): string {
  const completedSlugs = completedLessons.map((lesson) => lesson.slug);
  const relevantHints = mode === "topic" && selectedLesson
    ? mistakeHints.filter((hint) => hint.lessonSlug === selectedLesson.slug)
    : mistakeHints.filter((hint) => completedSlugs.includes(hint.lessonSlug));
  const vocabulary = learnedVocabularyContext(
    completedLessons,
    completedSlugs,
    undefined,
    mode === "topic" ? 3_000 : 4_500,
  );

  if (mode === "topic" && selectedLesson) {
    return [
      `Рабочая область: только завершённая тема «${selectedLesson.title}».`,
      `Материал темы:\n${trimAtLine(detailedTheory(selectedLesson), 6_000)}`,
      mistakeContext(relevantHints),
      vocabulary,
    ].filter(Boolean).join("\n\n");
  }

  const parts = [
    `Рабочая область: общий прогресс из ${completedLessons.length} завершённых тем. Не используй незавершённые темы.`,
  ];
  if (vocabulary) appendWithinLimit(parts, vocabulary);
  appendWithinLimit(parts, mistakeContext(relevantHints));
  appendWithinLimit(parts, "Материал последних завершённых тем (сначала самые новые):");
  for (const lesson of [...completedLessons].reverse()) {
    if (!appendWithinLimit(parts, compactTheory(lesson))) break;
  }
  return parts.join("\n\n");
}
