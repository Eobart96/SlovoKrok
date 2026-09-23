import { ApiError } from "./apiError";
import { aiRequestTimeoutMs, requestJson } from "./request";

export { ApiError, ApiRequestError } from "./apiError";

const request = requestJson;
const aiRequest = <T>(path: string, init?: RequestInit): Promise<T> => request<T>(path, { ...init, timeoutMs: aiRequestTimeoutMs });

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
export function getCourseBackup(): Promise<unknown> { return request<unknown>("/course/backup"); }
export function validateCourseBackup(backup: string): Promise<CourseBackupSummary> { return request<CourseBackupSummary>("/course/backup/validate", { method: "POST", body: backup }); }
export type CourseStateSnapshot = { state: CourseState; revision: string | null };
export function restoreCourseBackup(backup: string, revision: string | null): Promise<{ restored: boolean; revision: string | null; state: CourseState | null }> {
  return request<{ restored: boolean; revision: string | null; state: CourseState | null }>("/course/backup/restore", {
    method: "POST",
    headers: { "X-Course-State-Revision": revision ?? "none" },
    body: backup,
  });
}

export type CourseExerciseAttempt = { id: number; answer: string; is_correct: boolean; score: number; corrected_answer: string; explanation: string; next_exercise: string; created_at: string };
export type CourseExerciseInteraction = "text" | "choice" | "order" | "match";
export type CourseExercise = { id: number; lesson_slug: string; lesson_title: string; question: string; instruction: string; interaction_type?: CourseExerciseInteraction; options?: string[]; tokens?: string[]; pair_prompts?: string[]; pair_options?: string[]; created_at: string; latest_attempt: CourseExerciseAttempt | null };
export function getCourseExercises(lessonSlug?: string): Promise<CourseExercise[]> { const query = lessonSlug ? `?lesson_slug=${encodeURIComponent(lessonSlug)}` : ""; return request<CourseExercise[]>(`/course/exercises${query}`); }
export function generateCourseExercise(payload: { lesson_slug: string; lesson_title: string; theory: string }): Promise<CourseExercise> { return aiRequest<CourseExercise>("/course/exercises", { method: "POST", body: JSON.stringify(payload) }); }
export function answerCourseExercise(exerciseId: number, answer: string, assessmentMode: "online" | "offline" = "online"): Promise<CourseExerciseAttempt> { return aiRequest<CourseExerciseAttempt>(`/course/exercises/${exerciseId}/answer`, { method: "POST", body: JSON.stringify({ answer, assessment_mode: assessmentMode }) }); }
export function deleteCourseExercise(exerciseId: number): Promise<{ deleted: boolean }> { return request<{ deleted: boolean }>(`/course/exercises/${exerciseId}`, { method: "DELETE" }); }
export function deleteAllCourseExercises(): Promise<{ deleted: boolean; exercises_deleted: number; attempts_deleted: number }> { return request<{ deleted: boolean; exercises_deleted: number; attempts_deleted: number }>("/course/exercises", { method: "DELETE", body: JSON.stringify({ confirmation: "delete-all-exercises" }) }); }

export type CourseReadingAttempt = { id: number; retelling: string; score: number; feedback: string; corrected_retelling: string; created_at: string };
export type CourseReading = { id: number; lesson_slug: string; lesson_title: string; title: string; text: string; instruction: string; created_at: string; latest_attempt: CourseReadingAttempt | null };
export function getCourseReadings(): Promise<CourseReading[]> { return request<CourseReading[]>("/course/readings"); }
export function generateCourseReading(payload: { lesson_slug: string; lesson_title: string; theory: string; completed_theory: string }): Promise<CourseReading> { return aiRequest<CourseReading>("/course/readings", { method: "POST", body: JSON.stringify(payload) }); }
export function checkCourseReading(readingId: number, retelling: string): Promise<CourseReadingAttempt> { return aiRequest<CourseReadingAttempt>(`/course/readings/${readingId}/check`, { method: "POST", body: JSON.stringify({ retelling }) }); }
export function deleteCourseReading(readingId: number): Promise<{ deleted: boolean }> { return request<{ deleted: boolean }>(`/course/readings/${readingId}`, { method: "DELETE" }); }

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
export type CourseHomework = { id: number; lesson_slug: string; lesson_title: string; title: string; description: string; focus_category: string; created_at: string; latest_attempt: CourseHomeworkAttempt | null };
export function getCourseHomework(): Promise<CourseHomework[]> { return request<CourseHomework[]>("/course/homework"); }
export function generateCourseHomework(payload: { lesson_slug: string; lesson_title: string; theory: string; known_mistakes: string[] }): Promise<CourseHomework> { return aiRequest<CourseHomework>("/course/homework", { method: "POST", body: JSON.stringify(payload) }); }
export function submitCourseHomework(homeworkId: number, answer: string): Promise<CourseHomeworkAttempt> { return aiRequest<CourseHomeworkAttempt>(`/course/homework/${homeworkId}/submit`, { method: "POST", body: JSON.stringify({ answer }) }); }
export function deleteCourseHomework(homeworkId: number): Promise<{ deleted: boolean }> { return request<{ deleted: boolean }>(`/course/homework/${homeworkId}`, { method: "DELETE" }); }
