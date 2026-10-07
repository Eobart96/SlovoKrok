"use client";

import { type Dispatch, type SetStateAction, useEffect, useRef, useState } from "react";

import { a1CourseModules, findA1Lesson, getA1Module } from "../data/a1Course";
import { buildInitialProgress } from "../data/courseEngine";
import { normalizeFinalCompletedModules } from "../data/courseLevelState";
import { type LessonSummary, type MistakeRecord } from "../data/courseProgress";
import { type LessonStatus } from "../data/courseTypes";
import { mergeProgress } from "../data/progressMerge";
import { type CourseState, type CourseStateSnapshot, type PersonalCheatSheet } from "../lib/api";
import { CoursePersistence } from "../lib/coursePersistence";

export type ProgressMap = Record<string, LessonStatus>;
export type ChatInteractionKind = "answer" | "clarification" | "continue";
export type ChatMessage = { id: number; role: "assistant" | "user"; text: string; task?: string; suggestions?: string[]; countsAsPractice?: boolean; createdAt?: string; interactionKind?: ChatInteractionKind; diagnostic?: Record<string, string | number | boolean | null> };
export type FontSize = "normal" | "large" | "extra-large";
export type { LessonSummary, MistakeRecord } from "../data/courseProgress";

type SessionSetter<Key extends keyof CourseSessionState> = Dispatch<SetStateAction<CourseSessionState[Key]>>;

export type CourseSessionState = {
  activeModule: number;
  selectedSlug: string;
  fontSize: FontSize;
  progress: ProgressMap;
  lessonSteps: Record<string, number>;
  checkSelections: Record<string, string>;
  practiceAnswers: Record<string, string>;
  practiceResults: Record<string, boolean>;
  mistakes: Record<string, MistakeRecord>;
  finalSelections: Record<string, string>;
  finalCompletedModules: Record<string, boolean>;
  chatHistories: Record<string, ChatMessage[]>;
  lessonSummaries: Record<string, LessonSummary>;
  personalCheatSheets: PersonalCheatSheet[];
};

export type CourseSessionActions = {
  setActiveModule: SessionSetter<"activeModule">;
  setSelectedSlug: SessionSetter<"selectedSlug">;
  setFontSize: SessionSetter<"fontSize">;
  setProgress: SessionSetter<"progress">;
  setLessonSteps: SessionSetter<"lessonSteps">;
  setCheckSelections: SessionSetter<"checkSelections">;
  setPracticeAnswers: SessionSetter<"practiceAnswers">;
  setPracticeResults: SessionSetter<"practiceResults">;
  setMistakes: SessionSetter<"mistakes">;
  setFinalSelections: SessionSetter<"finalSelections">;
  setFinalCompletedModules: SessionSetter<"finalCompletedModules">;
  setChatHistories: SessionSetter<"chatHistories">;
  setLessonSummaries: SessionSetter<"lessonSummaries">;
  setPersonalCheatSheets: SessionSetter<"personalCheatSheets">;
};

export type CourseSession = CourseSessionState & CourseSessionActions & { persistenceError: string; readOnly: boolean; canDiscardLocalChanges: boolean; maintenance: (operation: (revision: string | null) => Promise<CourseStateSnapshot | void>) => Promise<void>; discardLocalChanges: () => void };

type PersistedCourseSession = Partial<CourseSessionState> & { finalCompleted?: boolean; _sync?: { dirty?: boolean; revision?: string | null } };

// These legacy keys are a compatibility boundary until a dedicated migration is approved.
const progressStorageKey = "slovak-module-1-beta-progress";
const sessionStorageKey = "slovak-module-1-beta-session-v1";
const fontSizeStorageKey = "slovak-module-1-beta-font-size";

function initialProgress(): ProgressMap {
  return buildInitialProgress(a1CourseModules);
}

function readJsonObject(key: string): Record<string, unknown> {
  const raw = window.localStorage.getItem(key);
  if (!raw) return {};
  try {
    const parsed: unknown = JSON.parse(raw);
    return parsed && typeof parsed === "object" && !Array.isArray(parsed) ? parsed as Record<string, unknown> : {};
  } catch {
    return {};
  }
}

function readLegacySession(): PersistedCourseSession {
  const cached = readJsonObject(sessionStorageKey) as PersistedCourseSession;
  const storedFontSize = window.localStorage.getItem(fontSizeStorageKey);
  const fontSize: FontSize = storedFontSize === "normal" || storedFontSize === "large" || storedFontSize === "extra-large" ? storedFontSize : "large";
  return {
    ...cached,
    progress: mergeProgress(initialProgress(), readJsonObject(progressStorageKey) as ProgressMap, cached.progress ?? {}),
    fontSize: cached._sync ? cached.fontSize ?? fontSize : fontSize,
  };
}

function resolveSession(parsed: PersistedCourseSession): CourseSessionState {
  const restoredLesson = parsed.selectedSlug ? findA1Lesson(parsed.selectedSlug) : undefined;
  const restoredModule = restoredLesson ? a1CourseModules.find((module) => module.lessons.some((lesson) => lesson.slug === restoredLesson.slug)) : undefined;
  const activeModule = restoredModule?.order ?? (parsed.activeModule && a1CourseModules.some((module) => module.order === parsed.activeModule) ? parsed.activeModule : 1);
  return {
    activeModule,
    selectedSlug: restoredLesson?.slug ?? getA1Module(activeModule).lessons[0].slug,
    fontSize: parsed.fontSize ?? "large",
    progress: { ...initialProgress(), ...(parsed.progress ?? {}) },
    lessonSteps: parsed.lessonSteps ?? {},
    checkSelections: parsed.checkSelections ?? {},
    practiceAnswers: parsed.practiceAnswers ?? {},
    practiceResults: parsed.practiceResults ?? {},
    mistakes: parsed.mistakes ?? {},
    finalSelections: parsed.finalSelections ?? {},
    finalCompletedModules: normalizeFinalCompletedModules(parsed.finalCompletedModules, parsed.finalCompleted),
    chatHistories: parsed.chatHistories ?? {},
    lessonSummaries: parsed.lessonSummaries ?? {},
    personalCheatSheets: Array.isArray(parsed.personalCheatSheets) ? parsed.personalCheatSheets : [],
  };
}

function toCourseState(session: CourseSessionState): CourseState {
  return { ...session, activeLevel: "A1", finalCompleted: Boolean(session.finalCompletedModules["a1:1"]) };
}

function writeLegacySession(session: CourseSessionState, dirty: boolean, revision: string | null): void {
  window.localStorage.setItem(sessionStorageKey, JSON.stringify({ ...toCourseState(session), _sync: { dirty, revision } }));
  window.localStorage.setItem(progressStorageKey, JSON.stringify(session.progress));
  window.localStorage.setItem(fontSizeStorageKey, session.fontSize);
}

export function useCourseSession(): CourseSession {
  const [activeModule, setActiveModule] = useState(1);
  const [selectedSlug, setSelectedSlug] = useState(a1CourseModules[0].lessons[0].slug);
  const [fontSize, setFontSize] = useState<FontSize>("large");
  const [progress, setProgress] = useState<ProgressMap>(initialProgress);
  const [lessonSteps, setLessonSteps] = useState<Record<string, number>>({});
  const [checkSelections, setCheckSelections] = useState<Record<string, string>>({});
  const [practiceAnswers, setPracticeAnswers] = useState<Record<string, string>>({});
  const [practiceResults, setPracticeResults] = useState<Record<string, boolean>>({});
  const [mistakes, setMistakes] = useState<Record<string, MistakeRecord>>({});
  const [finalSelections, setFinalSelections] = useState<Record<string, string>>({});
  const [finalCompletedModules, setFinalCompletedModules] = useState<Record<string, boolean>>({});
  const [chatHistories, setChatHistories] = useState<Record<string, ChatMessage[]>>({});
  const [lessonSummaries, setLessonSummaries] = useState<Record<string, LessonSummary>>({});
  const [personalCheatSheets, setPersonalCheatSheets] = useState<PersonalCheatSheet[]>([]);
  const [storageReady, setStorageReady] = useState(false);
  const [readOnly, setReadOnly] = useState(true);
  const [canDiscardLocalChanges, setCanDiscardLocalChanges] = useState(false);
  const [persistenceError, setPersistenceError] = useState("");
  const persistenceRef = useRef<CoursePersistence | null>(null);

  const applySession = (session: CourseSessionState) => {
    setActiveModule(session.activeModule);
    setSelectedSlug(session.selectedSlug);
    setFontSize(session.fontSize);
    setProgress(session.progress);
    setLessonSteps(session.lessonSteps);
    setCheckSelections(session.checkSelections);
    setPracticeAnswers(session.practiceAnswers);
    setPracticeResults(session.practiceResults);
    setMistakes(session.mistakes);
    setFinalSelections(session.finalSelections);
    setFinalCompletedModules(session.finalCompletedModules);
    setChatHistories(session.chatHistories);
    setLessonSummaries(session.lessonSummaries);
    setPersonalCheatSheets(session.personalCheatSheets);
  };

  useEffect(() => {
    const abort = new AbortController();
    let release = () => {};
    const ownSession = async () => {
      if (abort.signal.aborted) return;
      const released = new Promise<void>((resolve) => { release = resolve; });
      try {
        const local = readLegacySession();
        const resolved = resolveSession(local);
        applySession(resolved);
        const persistence = new CoursePersistence(
          toCourseState(resolved), Boolean(local._sync?.dirty), local._sync?.revision ?? null,
          (state, dirty, revision) => writeLegacySession(resolveSession(state as PersistedCourseSession), dirty, revision),
          (state) => applySession(resolveSession(state as PersistedCourseSession)),
          setPersistenceError,
          () => { setReadOnly(true); setCanDiscardLocalChanges(true); },
        );
        persistenceRef.current = persistence;
        setStorageReady(true);
        setReadOnly(false);
        persistence.start();
        await released;
        persistence.stop();
      } catch {
        setPersistenceError("Не удалось прочитать локальный прогресс. Проверьте доступ браузера к хранилищу.");
      }
    };
    if (navigator.locks) {
      void navigator.locks.request("slovokrok-course-editor", { signal: abort.signal }, ownSession)
        .catch(() => { if (!abort.signal.aborted) setPersistenceError("Не удалось открыть сеанс курса."); });
    } else {
      setPersistenceError("Откройте курс через localhost в браузере с поддержкой Web Locks.");
    }
    return () => { abort.abort(); persistenceRef.current?.stop(); release(); };
  }, []);

  useEffect(() => {
    if (!storageReady || readOnly) return;
    persistenceRef.current?.update(toCourseState({ activeModule, selectedSlug, fontSize, progress, lessonSteps, checkSelections, practiceAnswers, practiceResults, mistakes, finalSelections, finalCompletedModules, chatHistories, lessonSummaries, personalCheatSheets }));
  }, [storageReady, readOnly, activeModule, selectedSlug, fontSize, progress, lessonSteps, checkSelections, practiceAnswers, practiceResults, mistakes, finalSelections, finalCompletedModules, chatHistories, lessonSummaries, personalCheatSheets]);

  const maintenance = async (operation: (revision: string | null) => Promise<CourseStateSnapshot | void>) => {
    if (!persistenceRef.current || readOnly) throw new Error("Сеанс курса ещё не готов.");
    setReadOnly(true);
    try { await persistenceRef.current.maintenance(operation); }
    finally { setReadOnly(persistenceRef.current.needsRecovery()); }
  };

  const discardLocalChanges = () => {
    const cached = readJsonObject(sessionStorageKey);
    const sync = cached._sync && typeof cached._sync === "object" && !Array.isArray(cached._sync)
      ? cached._sync as Record<string, unknown>
      : {};
    window.localStorage.setItem(sessionStorageKey, JSON.stringify({ ...cached, _sync: { ...sync, dirty: false } }));
    window.location.reload();
  };

  return { activeModule, selectedSlug, fontSize, progress, lessonSteps, checkSelections, practiceAnswers, practiceResults, mistakes, finalSelections, finalCompletedModules, chatHistories, lessonSummaries, personalCheatSheets, setActiveModule, setSelectedSlug, setFontSize, setProgress, setLessonSteps, setCheckSelections, setPracticeAnswers, setPracticeResults, setMistakes, setFinalSelections, setFinalCompletedModules, setChatHistories, setLessonSummaries, setPersonalCheatSheets, persistenceError, readOnly, canDiscardLocalChanges, maintenance, discardLocalChanges };
}
