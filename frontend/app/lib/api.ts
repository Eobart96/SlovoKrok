import { ApiError, ApiRequestError } from "./apiError.ts";
import { aiRequestTimeoutMs, backupRequestTimeoutMs, requestJson } from "./request.ts";
import type { CourseLevel } from "../data/courseLevelState.ts";
import type { ReportLocation } from "./reportLocation";

export { ApiError, ApiRequestError } from "./apiError.ts";

const request = requestJson;

export type LearnerProfile = { name: string; slovak_name: string; occupation: string; occupation_sentence_sk: string; city: string; interests: string; goal: string; share_with_ai: boolean };
export const emptyLearnerProfile: LearnerProfile = { name: "", slovak_name: "", occupation: "", occupation_sentence_sk: "", city: "", interests: "", goal: "", share_with_ai: false };
export function getLearnerProfile(): Promise<LearnerProfile> { return request("/profile"); }
export function saveLearnerProfile(profile: LearnerProfile): Promise<LearnerProfile> { return request("/profile", { method: "PUT", body: JSON.stringify(profile) }); }

export type IssueReportSection = "learning" | "cheats" | "exercises" | "homework" | "reading" | "review" | "vocabulary";
export type ReportScreenshot = { name: string; mime: "image/png" | "image/jpeg" | "image/webp"; data: string };
export type IssueReport = { id: string; section: IssueReportSection; description: string; created_at: string; location?: ReportLocation | null; screenshots: ReportScreenshot[] };
export function getIssueReports(): Promise<IssueReport[]> { return request("/reports"); }
export function saveIssueReport(section: IssueReportSection, description: string, location?: ReportLocation, screenshots: ReportScreenshot[] = []): Promise<IssueReport> { return request("/reports", { method: "POST", body: JSON.stringify({ section, description, location, screenshots }) }); }
export function exportIssueReports(): Promise<{ data: string }> { return request("/reports/export"); }
export function clearIssueReports(): Promise<{ deleted: boolean }> { return request("/reports", { method: "DELETE", body: JSON.stringify({ confirmation: "delete-all-reports" }) }); }
const aiRequest = <T>(path: string, init?: RequestInit): Promise<T> => request<T>(path, { ...init, timeoutMs: aiRequestTimeoutMs });
const backupRequest = <T>(path: string, init?: RequestInit): Promise<T> => request<T>(path, { ...init, timeoutMs: backupRequestTimeoutMs });

export type MistakeReviewAssessment = { is_correct: boolean; score: number; corrected_answer: string; explanation: string; next_exercise: string };
export function checkCourseMistake(payload: { prompt: string; expected_answer: string; accepted_answers?: string[]; answer: string; kind: "exact" | "open"; source_exercise_id?: number; assessment_mode: "online" | "offline" }): Promise<MistakeReviewAssessment> {
  return aiRequest("/course/mistakes/check", { method: "POST", body: JSON.stringify(payload) });
}

export type TutorReply = {
  provider: string;
  reply: string;
  correction: string | null;
  explanation: string | null;
  next_question: string | null;
  suggestions: string[];
  mistake_original: string | null;
  mistake_corrected: string | null;
};

export type TutorRequest = {
  lesson_slug: string;
  lesson_title: string;
  goals: string[];
  theory: string;
  known_mistakes: string[];
  history: Array<{ role: "user" | "assistant"; content: string }>;
  message: string;
  current_task?: string;
  interaction_kind?: "answer" | "clarification" | "continue";
  is_final_turn?: boolean;
};

export function askModule1Tutor(payload: TutorRequest): Promise<TutorReply> {
  return aiRequest<TutorReply>("/tutor/module1-chat", { method: "POST", body: JSON.stringify(payload) });
}

export type TranslationDirection = "ru-sk" | "sk-ru";
export type TutorTranslation = {
  history_id: number;
  provider: string;
  translation: string;
  alternatives: string[];
  note: string | null;
};

export function translateWithTutor(text: string, direction: TranslationDirection): Promise<TutorTranslation> {
  return aiRequest<TutorTranslation>("/tutor/translate", { method: "POST", body: JSON.stringify({ text, direction }) });
}

export type TutorTranslationQuestion = { history_id: number; provider: string; answer: string };

export function askTutorTranslationQuestion(payload: {
  history_id?: number;
  source_text: string;
  translation: string;
  direction: TranslationDirection;
  question: string;
}): Promise<TutorTranslationQuestion> {
  return aiRequest<TutorTranslationQuestion>("/tutor/translate-question", { method: "POST", body: JSON.stringify(payload) });
}

export type TutorTranslationHistoryQuestion = {
  id: number;
  question: string;
  answer: string;
  provider: string;
  created_at: string;
};

export type TutorTranslationHistoryEntry = {
  id: number;
  direction: TranslationDirection;
  source_text: string;
  translation: string;
  alternatives: string[];
  note: string | null;
  provider: string;
  created_at: string;
  questions: TutorTranslationHistoryQuestion[];
};

export function getTutorTranslationHistory(limit = 50, beforeId?: number): Promise<TutorTranslationHistoryEntry[]> {
  const cursor = beforeId ? `&before_id=${beforeId}` : "";
  return request<TutorTranslationHistoryEntry[]>(`/tutor/translation-history?limit=${limit}${cursor}`);
}

export function deleteTutorTranslationHistoryEntry(historyId: number): Promise<{ deleted: boolean }> {
  return request<{ deleted: boolean }>(`/tutor/translation-history/${historyId}`, { method: "DELETE" });
}

export function clearTutorTranslationHistory(): Promise<{ deleted: boolean; translations_deleted: number; questions_deleted: number }> {
  return request<{ deleted: boolean; translations_deleted: number; questions_deleted: number }>("/tutor/translation-history", {
    method: "DELETE",
    body: JSON.stringify({ confirmation: "delete-translation-history" }),
  });
}

export type TutorProviderName = "codex" | "openai" | "polza";
export type TutorSettings = {
  provider: TutorProviderName;
  codex_installed: boolean;
  codex_authenticated: boolean;
  codex_message: string;
  openai_api_key_configured: boolean;
  openai_model: string;
  polza_api_key_configured: boolean;
  polza_model: string;
  polza_base_url: string;
};
export type TutorSettingsUpdate = {
  provider: TutorProviderName;
  openai_api_key?: string;
  openai_model: string;
  polza_api_key?: string;
  polza_model: string;
  clear_openai_api_key?: boolean;
  clear_polza_api_key?: boolean;
};
export type CodexLoginStatus = { installed: boolean; authenticated: boolean; message: string };

export function getTutorSettings(): Promise<TutorSettings> { return request<TutorSettings>("/tutor/settings"); }
export function updateTutorSettings(payload: TutorSettingsUpdate): Promise<TutorSettings> { return request<TutorSettings>("/tutor/settings", { method: "PUT", body: JSON.stringify(payload) }); }
export function startCodexLogin(): Promise<CodexLoginStatus> { return request<CodexLoginStatus>("/tutor/codex-login", { method: "POST" }); }

export type PersonalCheatSheet = {
  id: string;
  title: string;
  content: string;
  createdAt: string;
  updatedAt: string;
};

export type CourseState = {
  activeLevel?: CourseLevel;
  levelPositions?: Partial<Record<CourseLevel, { activeModule: number; selectedSlug: string }>>;
  activeModule?: number;
  selectedSlug?: string;
  fontSize: "normal" | "large" | "extra-large";
  progress: Record<string, string>;
  lessonSteps: Record<string, number>;
  checkSelections: Record<string, string>;
  practiceAnswers: Record<string, string>;
  practiceResults: Record<string, boolean>;
  mistakes: Record<string, {
    id: string; lessonSlug: string; prompt: string; answer: string;
    attempts: number; mastered: boolean; reviewStage?: number | null; dueAt?: string | null;
  }>;
  finalSelections: Record<string, string>;
  finalCompleted: boolean;
  finalCompletedModules?: Record<string, boolean>;
  chatHistories: Record<string, Array<{
    id: number; role: "assistant" | "user"; text: string; task?: string | null;
    suggestions?: string[] | null; countsAsPractice?: boolean | null; createdAt?: string | null;
    interactionKind?: "answer" | "clarification" | "continue" | null;
    diagnostic?: Record<string, string | number | boolean | null> | null;
  }>>;
  lessonSummaries: Record<string, {
    understanding: number; level: string; strengths: string[]; mistakes?: string[] | null;
    review: string[]; userTurns: number;
    evidence?: { coreCorrect: number; coreTotal: number } | null;
  }>;
  personalCheatSheets?: PersonalCheatSheet[];
};

export type CourseStateResponse = { exists: boolean; schema_version: number; revision: string | null; state: CourseState | null; updated_at: string | null };
export function getCourseState(): Promise<CourseStateResponse> { return request<CourseStateResponse>("/course/state"); }
export function saveCourseState(state: CourseState, revision: string | null): Promise<CourseStateResponse> {
  return request<CourseStateResponse>("/course/state", {
    method: "PUT",
    headers: { "X-Course-State-Revision": revision ?? "none" },
    body: JSON.stringify(state),
  });
}

export type CourseBackupSummary = { exported_at: string; has_state: boolean; completed_topics: number; counts: Record<string, number> };
export function getCourseBackup(): Promise<unknown> { return backupRequest<unknown>("/course/backup"); }
export function validateCourseBackup(backup: string): Promise<CourseBackupSummary> { return backupRequest<CourseBackupSummary>("/course/backup/validate", { method: "POST", body: backup }); }
export type CourseStateSnapshot = { state: CourseState; revision: string | null };
export function restoreCourseBackup(backup: string, revision: string | null): Promise<{ restored: boolean; revision: string | null; state: CourseState | null }> {
  return backupRequest<{ restored: boolean; revision: string | null; state: CourseState | null }>("/course/backup/restore", {
    method: "POST",
    headers: { "X-Course-State-Revision": revision ?? "none" },
    body: backup,
  });
}

const mutationRecoveryDelaysMs = [0, 500, 1_500, 3_000, 5_000, 8_000] as const;

export function isAmbiguousMutationError(error: unknown): boolean {
  return (error instanceof ApiError && error.status === 500)
    || (error instanceof ApiRequestError && error.kind !== "cancelled");
}

async function recoverMutation<TLoaded, TRecovered>(load: () => Promise<TLoaded>, accept: (value: TLoaded) => TRecovered | null): Promise<TRecovered | null> {
  for (const delayMs of mutationRecoveryDelaysMs) {
    if (delayMs) await new Promise((resolve) => globalThis.setTimeout(resolve, delayMs));
    try {
      const loaded = await load();
      const recovered = accept(loaded);
      if (recovered !== null) return recovered;
    } catch {
      // The local development backend may still be restarting. Keep polling with read-only requests.
    }
  }
  return null;
}

async function recoverGeneratedItem<T extends { id: number; lesson_slug: string }>(load: () => Promise<T[]>, lessonSlug: string, knownIds: readonly number[]): Promise<T | null> {
  const known = new Set(knownIds);
  return recoverMutation(load, (items) => items.find((item) => item.lesson_slug === lessonSlug && !known.has(item.id)) ?? null);
}

async function recoverDeletedItem<T extends { id: number }>(load: () => Promise<T[]>, itemId: number): Promise<{ deleted: boolean } | null> {
  return recoverMutation(load, (items) => items.some((item) => item.id === itemId) ? null : { deleted: true });
}

export type CourseExerciseAttempt = { id: number; answer: string; is_correct: boolean; score: number; corrected_answer: string; explanation: string; next_exercise: string; created_at: string };
export type CourseExerciseInteraction = "text" | "choice" | "order" | "match";
export type CourseExercise = { id: number; lesson_slug: string; lesson_title: string; question: string; instruction: string; interaction_type?: CourseExerciseInteraction; options?: string[]; tokens?: string[]; pair_prompts?: string[]; pair_options?: string[]; created_at: string; latest_attempt: CourseExerciseAttempt | null };
export function getCourseExercises(lessonSlug?: string): Promise<CourseExercise[]> { const query = lessonSlug ? `?lesson_slug=${encodeURIComponent(lessonSlug)}` : ""; return request<CourseExercise[]>(`/course/exercises${query}`); }
export async function generateCourseExercise(payload: { lesson_slug: string; lesson_title: string; theory: string }, knownIds: readonly number[]): Promise<CourseExercise> { try { return await aiRequest<CourseExercise>("/course/exercises", { method: "POST", body: JSON.stringify(payload) }); } catch (error) { if (!isAmbiguousMutationError(error)) throw error; const recovered = await recoverGeneratedItem(getCourseExercises, payload.lesson_slug, knownIds); if (recovered) return recovered; throw error; } }
export async function answerCourseExercise(exerciseId: number, answer: string, assessmentMode: "online" | "offline" = "online", previousAttemptId?: number): Promise<CourseExerciseAttempt> { try { return await aiRequest<CourseExerciseAttempt>(`/course/exercises/${exerciseId}/answer`, { method: "POST", body: JSON.stringify({ answer, assessment_mode: assessmentMode }) }); } catch (error) { if (!isAmbiguousMutationError(error)) throw error; const recovered = await recoverMutation(getCourseExercises, (items) => { const attempt = items.find((item) => item.id === exerciseId)?.latest_attempt ?? null; return attempt && attempt.id !== previousAttemptId && attempt.answer === answer ? attempt : null; }); if (recovered) return recovered; throw error; } }
export async function deleteCourseExercise(exerciseId: number): Promise<{ deleted: boolean }> { try { return await request<{ deleted: boolean }>(`/course/exercises/${exerciseId}`, { method: "DELETE" }); } catch (error) { if (!isAmbiguousMutationError(error)) throw error; const recovered = await recoverDeletedItem(getCourseExercises, exerciseId); if (recovered) return recovered; throw error; } }
export function deleteAllCourseExercises(): Promise<{ deleted: boolean; exercises_deleted: number; attempts_deleted: number }> { return request<{ deleted: boolean; exercises_deleted: number; attempts_deleted: number }>("/course/exercises", { method: "DELETE", body: JSON.stringify({ confirmation: "delete-all-exercises" }) }); }

export type CourseReadingAttempt = { id: number; retelling: string; score: number; feedback: string; corrected_retelling: string; created_at: string };
export type CourseReading = { id: number; lesson_slug: string; lesson_title: string; title: string; text: string; instruction: string; created_at: string; offline_ready: boolean; latest_attempt: CourseReadingAttempt | null };
export type CourseMaterialCollection = {
  format: "slovokrok-course-materials";
  version: 1;
  exported_at: string;
  exercises: unknown[];
  readings: unknown[];
  homework: unknown[];
};
export type CourseMaterialImportBucket = { imported: number; skipped: number; total: number };
export type CourseMaterialImportResult = { exercises: CourseMaterialImportBucket; readings: CourseMaterialImportBucket; homework: CourseMaterialImportBucket };
export type CourseTasksDeleteResult = { deleted: true; exercises_deleted: number; exercise_attempts_deleted: number; readings_deleted: number; reading_attempts_deleted: number; homework_deleted: number; homework_attempts_deleted: number };
export function getCourseReadings(): Promise<CourseReading[]> { return request<CourseReading[]>("/course/readings"); }
export async function generateCourseReading(payload: { lesson_slug: string; lesson_title: string; theory: string; completed_theory: string; batch_index?: number; batch_total?: number }, knownIds: readonly number[]): Promise<CourseReading> { try { return await aiRequest<CourseReading>("/course/readings", { method: "POST", body: JSON.stringify(payload) }); } catch (error) { if (!isAmbiguousMutationError(error)) throw error; const recovered = await recoverGeneratedItem(getCourseReadings, payload.lesson_slug, knownIds); if (recovered) return recovered; throw error; } }
export async function checkCourseReading(readingId: number, retelling: string, assessmentMode: "online" | "offline" = "online", previousAttemptId?: number): Promise<CourseReadingAttempt> { try { return await aiRequest<CourseReadingAttempt>(`/course/readings/${readingId}/check`, { method: "POST", body: JSON.stringify({ retelling, assessment_mode: assessmentMode }) }); } catch (error) { if (!isAmbiguousMutationError(error)) throw error; const recovered = await recoverMutation(getCourseReadings, (items) => { const attempt = items.find((item) => item.id === readingId)?.latest_attempt ?? null; return attempt && attempt.id !== previousAttemptId && attempt.retelling === retelling ? attempt : null; }); if (recovered) return recovered; throw error; } }
export async function deleteCourseReading(readingId: number): Promise<{ deleted: boolean }> { try { return await request<{ deleted: boolean }>(`/course/readings/${readingId}`, { method: "DELETE" }); } catch (error) { if (!isAmbiguousMutationError(error)) throw error; const recovered = await recoverDeletedItem(getCourseReadings, readingId); if (recovered) return recovered; throw error; } }
export function exportCourseMaterials(): Promise<CourseMaterialCollection> { return request<CourseMaterialCollection>("/course/materials/export"); }
export function importCourseMaterials(collection: unknown): Promise<CourseMaterialImportResult> { return request<CourseMaterialImportResult>("/course/materials/import", { method: "POST", body: JSON.stringify(collection) }); }
export async function getBasicCourseMaterials(): Promise<unknown> {
  const response = await fetch("/task-packs/slovokrok-a1-basic-v1.json", { signal: AbortSignal.timeout(30_000) });
  if (!response.ok) throw new Error("Не удалось загрузить базовый пакет заданий.");
  return response.json();
}
export async function deleteAllCourseTasks(): Promise<CourseTasksDeleteResult> {
  const before = await Promise.all([getCourseExercises(), getCourseReadings(), getCourseHomework()]);
  try { return await request<CourseTasksDeleteResult>("/course/materials", { method: "DELETE", body: JSON.stringify({ confirmation: "delete-all-course-tasks" }) }); }
  catch (error) {
    if (!isAmbiguousMutationError(error)) throw error;
    const recovered = await recoverMutation(
      () => Promise.all([getCourseExercises(), getCourseReadings(), getCourseHomework()]),
      ([exercises, readings, homework]) => exercises.length || readings.length || homework.length ? null : true,
    );
    if (recovered) return {
      deleted: true,
      exercises_deleted: before[0].length,
      exercise_attempts_deleted: before[0].filter((item) => item.latest_attempt).length,
      readings_deleted: before[1].length,
      reading_attempts_deleted: before[1].filter((item) => item.latest_attempt).length,
      homework_deleted: before[2].length,
      homework_attempts_deleted: before[2].filter((item) => item.latest_attempt).length,
    };
    throw error;
  }
}

export type CourseVocabularyItem = { id: number; lesson_slug: string; lesson_title: string; word: string; translation: string; example: string | null; review_count: number; interval_days: number; next_review_at: string | null; is_due: boolean };
export type CourseVocabularySeed = Omit<CourseVocabularyItem, "id" | "review_count" | "interval_days" | "next_review_at" | "is_due">;
export async function syncCourseVocabulary(items: CourseVocabularySeed[]): Promise<CourseVocabularyItem[]> {
  const existing = await getCourseVocabulary();
  const existingByKey = new Map(existing.map((item) => [`${item.lesson_slug}\0${item.word}`, item]));
  const changed = items.filter((item) => {
    const stored = existingByKey.get(`${item.lesson_slug}\0${item.word}`);
    return !stored || stored.lesson_title !== item.lesson_title || stored.translation !== item.translation || stored.example !== item.example;
  });
  if (!changed.length) return existing;
  const batches = Array.from({ length: Math.ceil(changed.length / 400) }, (_, index) => changed.slice(index * 400, (index + 1) * 400));
  let stored = existing;
  for (const batch of batches) stored = await request<CourseVocabularyItem[]>("/course/vocabulary/sync", { method: "PUT", body: JSON.stringify({ items: batch }) });
  return stored;
}
export function getCourseVocabulary(): Promise<CourseVocabularyItem[]> { return request<CourseVocabularyItem[]>("/course/vocabulary"); }
export type VocabularyRating = "again" | "hard" | "easy";
export function reviewCourseVocabulary(itemId: number, rating?: VocabularyRating): Promise<CourseVocabularyItem> { return request<CourseVocabularyItem>(`/course/vocabulary/${itemId}/review`, { method: "POST", ...(rating ? { body: JSON.stringify({ rating }) } : {}) }); }

export type CourseHomeworkAttempt = { id: number; answer: string; is_correct: boolean; score: number; corrected_answer: string; explanation: string; next_exercise: string; created_at: string };
export type CourseHomework = { id: number; lesson_slug: string; lesson_title: string; title: string; description: string; focus_category: string; created_at: string; offline_ready: boolean; latest_attempt: CourseHomeworkAttempt | null };
export function getCourseHomework(): Promise<CourseHomework[]> { return request<CourseHomework[]>("/course/homework"); }
export async function generateCourseHomework(payload: { lesson_slug: string; lesson_title: string; theory: string; known_mistakes: string[]; batch_index?: number; batch_total?: number }, knownIds: readonly number[]): Promise<CourseHomework> { try { return await aiRequest<CourseHomework>("/course/homework", { method: "POST", body: JSON.stringify(payload) }); } catch (error) { if (!isAmbiguousMutationError(error)) throw error; const recovered = await recoverGeneratedItem(getCourseHomework, payload.lesson_slug, knownIds); if (recovered) return recovered; throw error; } }

export function findRecoveredHomeworkAttempt(homework: CourseHomework[], homeworkId: number, answer: string, previousAttemptId?: number): CourseHomeworkAttempt | null {
  const attempt = homework.find((item) => item.id === homeworkId)?.latest_attempt ?? null;
  return attempt && attempt.id !== previousAttemptId && attempt.answer === answer ? attempt : null;
}

async function recoverSubmittedHomeworkAttempt(homeworkId: number, answer: string, previousAttemptId?: number): Promise<CourseHomeworkAttempt | null> {
  return recoverMutation(getCourseHomework, (homework) => findRecoveredHomeworkAttempt(homework, homeworkId, answer, previousAttemptId));
}

export async function submitCourseHomework(homeworkId: number, answer: string, assessmentMode: "online" | "offline" = "online", previousAttemptId?: number): Promise<CourseHomeworkAttempt> {
  try {
    return await aiRequest<CourseHomeworkAttempt>(`/course/homework/${homeworkId}/submit`, { method: "POST", body: JSON.stringify({ answer, assessment_mode: assessmentMode }) });
  } catch (error) {
    if (!isAmbiguousMutationError(error)) throw error;
    const recovered = await recoverSubmittedHomeworkAttempt(homeworkId, answer, previousAttemptId);
    if (recovered) return recovered;
    throw error;
  }
}
export async function deleteCourseHomework(homeworkId: number): Promise<{ deleted: boolean }> { try { return await request<{ deleted: boolean }>(`/course/homework/${homeworkId}`, { method: "DELETE" }); } catch (error) { if (!isAmbiguousMutationError(error)) throw error; const recovered = await recoverDeletedItem(getCourseHomework, homeworkId); if (recovered) return recovered; throw error; } }
