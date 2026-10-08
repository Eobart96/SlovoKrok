"use client";

import { type Dispatch, type SetStateAction, useEffect, useRef, useState } from "react";

import { a1CourseModules } from "../data/a1Course";
import { coursePositionCatalog as courseCatalog } from "../data/coursePositionCatalog";
import { buildInitialProgress } from "../data/courseEngine";
import { normalizeFinalCompletedModules, resolveCoursePosition, switchCourseLevel, type CourseLevel, type CoursePositions } from "../data/courseLevelState";
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
  activeLevel: CourseLevel;
  levelPositions: CoursePositions;
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
  selectLevel: (level: CourseLevel) => void;
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
  return buildInitialProgress([...courseCatalog.A1, ...courseCatalog.A2]);
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
  const activeLevel = parsed.activeLevel === "A2" ? "A2" : "A1";
  const position = resolveCoursePosition(courseCatalog[activeLevel], parsed);
  return {
    activeLevel,
    levelPositions: { A1: resolveCoursePosition(courseCatalog.A1, parsed.levelPositions?.A1), A2: resolveCoursePosition(courseCatalog.A2, parsed.levelPositions?.A2), [activeLevel]: position },
    ...position,
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
  return { ...session, levelPositions: { ...session.levelPositions, [session.activeLevel]: { activeModule: session.activeModule, selectedSlug: session.selectedSlug } }, finalCompleted: Boolean(session.finalCompletedModules["a1:1"]) };
}

function writeLegacySession(session: CourseSessionState, dirty: boolean, revision: string | null): void {
  window.localStorage.setItem(sessionStorageKey, JSON.stringify({ ...toCourseState(session), _sync: { dirty, revision } }));
  window.localStorage.setItem(progressStorageKey, JSON.stringify(session.progress));
  window.localStorage.setItem(fontSizeStorageKey, session.fontSize);
}

export function useCourseSession(): CourseSession {
  const [activeLevel, setActiveLevel] = useState<CourseLevel>("A1");
  const [levelPositions, setLevelPositions] = useState<CoursePositions>({});
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
    setActiveLevel(session.activeLevel);
    setLevelPositions(session.levelPositions);
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
    persistenceRef.current?.update(toCourseState({ activeLevel, levelPositions, activeModule, selectedSlug, fontSize, progress, lessonSteps, checkSelections, practiceAnswers, practiceResults, mistakes, finalSelections, finalCompletedModules, chatHistories, lessonSummaries, personalCheatSheets }));
  }, [storageReady, readOnly, activeLevel, levelPositions, activeModule, selectedSlug, fontSize, progress, lessonSteps, checkSelections, practiceAnswers, practiceResults, mistakes, finalSelections, finalCompletedModules, chatHistories, lessonSummaries, personalCheatSheets]);

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

  const selectLevel = (level: CourseLevel) => {
    if (readOnly || persistenceError) return;
    const next = switchCourseLevel({ activeLevel, levelPositions, activeModule, selectedSlug }, level, courseCatalog[level]);
    setLevelPositions(next.levelPositions); setActiveLevel(next.activeLevel); setActiveModule(next.activeModule); setSelectedSlug(next.selectedSlug);
  };
  return { activeLevel, levelPositions, selectLevel, activeModule, selectedSlug, fontSize, progress, lessonSteps, checkSelections, practiceAnswers, practiceResults, mistakes, finalSelections, finalCompletedModules, chatHistories, lessonSummaries, personalCheatSheets, setActiveModule, setSelectedSlug, setFontSize, setProgress, setLessonSteps, setCheckSelections, setPracticeAnswers, setPracticeResults, setMistakes, setFinalSelections, setFinalCompletedModules, setChatHistories, setLessonSummaries, setPersonalCheatSheets, persistenceError, readOnly, canDiscardLocalChanges, maintenance, discardLocalChanges };
}
