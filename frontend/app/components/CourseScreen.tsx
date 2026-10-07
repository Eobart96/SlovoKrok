"use client";

import dynamic from "next/dynamic";
import { useEffect, useMemo, useRef, useState, type ReactNode } from "react";

import { a1CourseModules, allA1Lessons, getA1Module } from "../data/a1Course";
import { orderedModuleLessons as getOrderedModuleLessons } from "../data/courseEngine";
import { type CourseLesson } from "../data/courseTypes";
import { nextMistakeRecord } from "../data/courseProgress";
import { taskMistakeSource, type TaskMistakeInput, type TaskOpenRequest } from "../data/taskMistakes";
import { learningModeStorageKey, readLearningMode, type LearningMode } from "../data/learningMode";
import { useCourseProgressController } from "../hooks/useCourseProgressController";
import { useCourseSession } from "../hooks/useCourseSession";
import { CourseListening } from "./CourseListening";
import { CourseMaterialView } from "./CourseMaterialView";
import { CourseReinforcementView } from "./CourseReinforcementView";
import { CourseTopicsView } from "./CourseTopicsView";
import { CourseFinalView, CourseReviewView } from "./CourseProgressViews";
import { emptyLearnerProfile, getLearnerProfile } from "../lib/api";
import { personalizeModule } from "../data/personalizeCourse";
import { LearnerProfileSettings } from "./LearnerProfileSettings";

const CourseExercises = dynamic(() => import("./CourseExercises").then((module) => module.CourseExercises));
const CourseReading = dynamic(() => import("./CourseReading").then((module) => module.CourseReading));
const CourseVocabulary = dynamic(() => import("./CourseVocabulary").then((module) => module.CourseVocabulary));
const CourseHomework = dynamic(() => import("./CourseHomework").then((module) => module.CourseHomework));
const CourseCheatSheets = dynamic(() => import("./CourseCheatSheets").then((module) => module.CourseCheatSheets));
const CourseStatsPanel = dynamic(() => import("./CourseStatsPanel").then((module) => module.CourseStatsPanel));
const CourseBackupPanel = dynamic(() => import("./CourseBackupPanel").then((module) => module.CourseBackupPanel));
const CourseTasksManager = dynamic(() => import("./CourseTasksManager").then((module) => module.CourseTasksManager));
const CourseTestPanel = dynamic(() => import("./CourseTestPanel").then((module) => module.CourseTestPanel));
const CourseAppearanceControls = dynamic(() => import("./CourseAppearanceControls").then((module) => module.CourseAppearanceControls));
const AiSettingsPanel = dynamic(() => import("./AiSettingsPanel").then((module) => module.AiSettingsPanel));

type CourseView = "topics" | "material" | "listening" | "cheats" | "exercises" | "reading" | "vocabulary" | "homework" | "reinforcement" | "review" | "final" | "stats";
type ModuleArea = "learning" | "cheats" | "exercises" | "reading" | "vocabulary" | "homework" | "review";
const developmentModeStorageKey = "slovokrok-development-mode-v1";
const settingsSectionsStorageKey = "slovokrok-settings-sections-v1";
type SettingsSection = "appearance" | "tasks" | "backup" | "mistakes" | "ai" | "development";
const defaultSettingsSections: Record<SettingsSection, boolean> = { appearance: false, tasks: false, backup: false, mistakes: false, ai: true, development: false };

export function CourseScreen({ requestedArea = "learning", onAreaChange, settingsOpen = false, onSettingsClose = () => {}, themeControl }: { requestedArea?: ModuleArea; onAreaChange?: (area: ModuleArea) => void; settingsOpen?: boolean; onSettingsClose?: () => void; themeControl?: ReactNode }) {
  const [view, setView] = useState<CourseView>("topics");
  const [exerciseOpenRequest, setExerciseOpenRequest] = useState<TaskOpenRequest | null>(null);
  const [homeworkOpenRequest, setHomeworkOpenRequest] = useState<TaskOpenRequest | null>(null);
  const taskRequestNonce = useRef(0);
  const [topicGroup, setTopicGroup] = useState("root");
  const [manualPreview, setManualPreview] = useState<{ lessonSlug: string; step: number } | null>(null);
  const [developmentMode, setDevelopmentMode] = useState(false);
  const [learningMode, setLearningMode] = useState<LearningMode>("online");
  const [materialRevision, setMaterialRevision] = useState(0);
  const [settingsSections, setSettingsSections] = useState(defaultSettingsSections);
  const [settingsSectionsReady, setSettingsSectionsReady] = useState(false);
  const testDestination = useRef<CourseView | null>(null);
  const session = useCourseSession();
  const [learnerProfile, setLearnerProfile] = useState(emptyLearnerProfile);
  const [profileError, setProfileError] = useState("");
  const [profileReady, setProfileReady] = useState(false);
  useEffect(() => { let cancelled = false; void getLearnerProfile().then((profile) => { if (!cancelled) setLearnerProfile(profile); }).catch((cause) => { if (!cancelled) setProfileError(cause instanceof Error ? cause.message : "Не удалось загрузить профиль."); }).finally(() => { if (!cancelled) setProfileReady(true); }); return () => { cancelled = true; }; }, []);
  const { activeModule, selectedSlug, fontSize, progress, lessonSteps, checkSelections, practiceAnswers, practiceResults, mistakes, finalSelections, lessonSummaries, personalCheatSheets, setActiveModule, setSelectedSlug, setPersonalCheatSheets, persistenceError } = session;

  const activeCourseModule = useMemo(() => personalizeModule(getA1Module(activeModule), learnerProfile), [activeModule, learnerProfile]);
  const orderedModuleLessons = useMemo(() => getOrderedModuleLessons(activeCourseModule), [activeCourseModule]);
  const displayLessonNumber = (lesson: CourseLesson): number => orderedModuleLessons.findIndex((item) => item.slug === lesson.slug) + 1;
  const selectedLesson = useMemo(
    () => activeCourseModule.lessons.find((lesson) => lesson.slug === selectedSlug) ?? activeCourseModule.lessons[0],
    [activeCourseModule, selectedSlug],
  );
  const progressController = useCourseProgressController({ module: activeCourseModule, lesson: selectedLesson, session });
  const { completedCount, reinforcementPractices, activeLessonSlugs, activeMistakes, dueMistakes, totalPracticeCount, correctPracticeCount, accuracy, finalQuestions, finalCompleted, finalScore, finalPassed, currentSummary, finalPassingPercent } = progressController.selectors;
  const allLessonsCompleted = completedCount === activeCourseModule.lessons.length;
  const generatedMistakeHints = Object.values(mistakes).filter((mistake) => !mistake.mastered).map((mistake) => ({ lessonSlug: mistake.lessonSlug, text: `${mistake.prompt}: ${mistake.answer}` }));
  const mistakesDisabled = session.readOnly || Boolean(persistenceError);
  const recordedMistakeIds = Object.values(mistakes).filter((mistake) => !mistake.mastered).map((mistake) => mistake.id);
  const recordTaskMistake = (input: TaskMistakeInput) => {
    if (mistakesDisabled) return;
    session.setMistakes((current) => {
      if (current[input.id] && !current[input.id].mastered) return current;
      const record = nextMistakeRecord({ ...input, previous: current[input.id], correct: false, nowMs: Date.now() });
      return record ? { ...current, [input.id]: { ...record, ...(input.reviewTask ? { reviewTask: input.reviewTask } : {}) } } : current;
    });
  };
  const checkTaskMistake = (id: string, correct: boolean, independent = true) => {
    if (mistakesDisabled) return;
    session.setMistakes((current) => {
      const previous = current[id];
      if (!previous) return current;
      if (correct && !independent && (previous.reviewStage ?? 0) > 0) return current;
      const record = nextMistakeRecord({ ...previous, previous, correct, nowMs: Date.now() });
      return record ? { ...current, [id]: record } : current;
    });
  };
  const openTaskMistake = (id: string) => {
    const source = taskMistakeSource(id);
    if (!source) return;
    const request = { id: source.id, nonce: ++taskRequestNonce.current };
    const area = source.kind === "exercise" ? "exercises" : "homework";
    if (source.kind === "exercise") setExerciseOpenRequest(request);
    else setHomeworkOpenRequest(request);
    setView(area);
    onAreaChange?.(area);
  };

  useEffect(() => {
    setDevelopmentMode(window.localStorage.getItem(developmentModeStorageKey) === "enabled");
    setLearningMode(readLearningMode(window.localStorage.getItem(learningModeStorageKey)));
    try {
      const saved: unknown = JSON.parse(window.localStorage.getItem(settingsSectionsStorageKey) ?? "{}");
      if (saved && typeof saved === "object" && !Array.isArray(saved)) {
        setSettingsSections(Object.fromEntries(Object.entries(defaultSettingsSections).map(([section, fallback]) => [section, typeof (saved as Record<string, unknown>)[section] === "boolean" ? (saved as Record<string, boolean>)[section] : fallback])) as Record<SettingsSection, boolean>);
      }
    } catch { /* Invalid saved UI state falls back to the defaults. */ }
    setSettingsSectionsReady(true);
  }, []);

  useEffect(() => {
    if (!settingsSectionsReady) return;
    try { window.localStorage.setItem(settingsSectionsStorageKey, JSON.stringify(settingsSections)); }
    catch { /* Section state still applies until this tab is closed. */ }
  }, [settingsSections, settingsSectionsReady]);

  const changeSettingsSection = (section: SettingsSection, open: boolean) => {
    setSettingsSections((current) => current[section] === open ? current : { ...current, [section]: open });
  };

  const changeDevelopmentMode = (enabled: boolean) => {
    setDevelopmentMode(enabled);
    if (!enabled) {
      const bypassedCourseGate = manualPreview !== null || (view === "final" && !allLessonsCompleted);
      setManualPreview(null);
      testDestination.current = null;
      if (bypassedCourseGate) {
        setView("topics");
        onAreaChange?.("learning");
      }
    }
    try { window.localStorage.setItem(developmentModeStorageKey, enabled ? "enabled" : "disabled"); }
    catch { /* The setting still applies until this tab is closed. */ }
  };

  const changeLearningMode = (mode: LearningMode) => {
    setLearningMode(mode);
    try { window.localStorage.setItem(learningModeStorageKey, mode); }
    catch { /* The setting still applies until this tab is closed. */ }
  };

  useEffect(() => {
    if (requestedArea === "learning" && testDestination.current) {
      setView(testDestination.current);
      testDestination.current = null;
      return;
    }
    if (requestedArea === "learning") { setView("topics"); return; }
    setView(requestedArea === "cheats" ? "cheats" : requestedArea === "exercises" ? "exercises" : requestedArea === "reading" ? "reading" : requestedArea === "vocabulary" ? "vocabulary" : requestedArea === "homework" ? "homework" : "review");
  }, [requestedArea]);

  const openTestView = (destination: CourseView) => {
    if (requestedArea !== "learning" && onAreaChange) {
      testDestination.current = destination;
      onAreaChange("learning");
    }
    setView(destination);
  };

  const openMaterial = (lesson: CourseLesson) => {
    setManualPreview(null);
    setSelectedSlug(lesson.slug);
    progressController.actions.startLesson(lesson);
    setView("material");
  };
  const openManualPreview = (lesson: CourseLesson, step = 0) => {
    setSelectedSlug(lesson.slug);
    setManualPreview({ lessonSlug: lesson.slug, step });
    openTestView("material");
  };

  const selectModule = (moduleOrder: number) => {
    const nextModule = getA1Module(moduleOrder);
    setActiveModule(nextModule.order);
    setTopicGroup("root");
    setSelectedSlug(nextModule.lessons[0].slug);
    setView("topics");
  };

  const continueAfterSummary = () => {
    const nextLesson = orderedModuleLessons[displayLessonNumber(selectedLesson)];
    if (nextLesson) openMaterial(nextLesson);
    else setView("final");
  };
  return (
    <>
    {session.readOnly && <div role="status" className="course-persistence-error"><p>{persistenceError || "Курс занят другой вкладкой или сохраняет данные. Дождитесь завершения операции либо закройте другую вкладку курса."}</p>{persistenceError && (session.canDiscardLocalChanges ? <button type="button" onClick={() => { if (window.confirm("Удалить несохранённые изменения этой вкладки и загрузить более новую сохранённую версию?")) session.discardLocalChanges(); }}>Загрузить сохранённую версию</button> : <button type="button" onClick={() => window.location.reload()}>Перезагрузить страницу</button>)}</div>}
    <section className="course" inert={session.readOnly} data-font-size={fontSize} aria-labelledby="course-title" data-report-view={view} data-report-module={activeCourseModule.title} data-report-lesson={selectedLesson.title} data-report-step={view === "material" ? (manualPreview?.step ?? lessonSteps[selectedLesson.slug] ?? 0) + 1 : undefined}>
      <header className="course-hero">
        <div>
          <label className="course-module-switcher">
            <span>Учебный модуль</span>
            <select value={activeModule} onChange={(event) => selectModule(Number(event.target.value))} aria-label="Выберите учебный модуль">
              {a1CourseModules.map((module) => <option value={module.order} key={module.slug}>{module.title}</option>)}
            </select>
          </label>
          <span className="course-kicker">Интерактивный курс · {activeCourseModule.level}</span>
          <h2 id="course-title">{activeCourseModule.title}</h2>
          <p>{activeCourseModule.description}</p>
        </div>
        <div className="course-progress" aria-label={`Завершено ${completedCount} из ${activeCourseModule.lessons.length} тем`}>
          <strong>{completedCount}/{activeCourseModule.lessons.length}</strong>
          <span>тем завершено</span>
          <div><i style={{ width: `${(completedCount / activeCourseModule.lessons.length) * 100}%` }} /></div>
        </div>
      </header>
      {persistenceError && <p className="course-persistence-error" role="alert">Данные временно не синхронизированы с базой: {persistenceError}</p>}

      {requestedArea === "learning" && <nav className="course-breadcrumbs" aria-label={`Навигация обучения ${activeCourseModule.title}`}>
        <button type="button" className={view === "topics" ? "active" : ""} onClick={() => setView("topics")}>Темы</button>
        <span>›</span>
        <button type="button" className={view === "material" ? "active" : ""} disabled={view === "topics"} onClick={() => setView("material")}>Материал</button>
        <span>›</span>
        <button type="button" className={view === "reinforcement" ? "active" : ""} disabled={progress[selectedLesson.slug] === "not_started"} onClick={() => setView("reinforcement")}>Закрепление</button>
        <span>·</span>
        <button type="button" className={view === "final" ? "active" : ""} disabled={!allLessonsCompleted} onClick={() => setView("final")}>Итоговый тест</button>
        <span>·</span>
        <button type="button" className={view === "stats" ? "active" : ""} onClick={() => setView("stats")}>Статистика</button>
      </nav>}

      {view === "topics" && <CourseTopicsView
        model={{ module: activeCourseModule, lessons: orderedModuleLessons, selectedGroupId: topicGroup, progress, mistakeCount: Object.keys(mistakes).length, activeMistakeCount: activeMistakes.length, finalCompleted, finalPassed, finalScore, finalQuestionCount: finalQuestions.length, completedCount, accuracy, correctPracticeCount, totalPracticeCount }}
        actions={{
          selectGroup: setTopicGroup,
          openLesson: openMaterial,
          openReview: () => setView("review"),
          openFinal: () => setView("final"),
          openStats: () => setView("stats"),
        }}
      />}
      <div hidden={view !== "cheats"}><CourseCheatSheets
        completedLessonSlugs={allA1Lessons.filter((lesson) => progress[lesson.slug] === "completed").map((lesson) => lesson.slug)}
        personalCheatSheets={personalCheatSheets}
        setPersonalCheatSheets={setPersonalCheatSheets}
        openLesson={(moduleOrder, lesson) => { setActiveModule(moduleOrder); setSelectedSlug(lesson.slug); openTestView("material"); }}
      /></div>
      <div hidden={view !== "exercises"}><CourseExercises key={materialRevision} completedLessonSlugs={allA1Lessons.filter((lesson) => progress[lesson.slug] === "completed").map((lesson) => lesson.slug)} mistakeHints={generatedMistakeHints} learningMode={learningMode} recordedMistakeIds={recordedMistakeIds} mistakesDisabled={mistakesDisabled} onRecordMistake={recordTaskMistake} onTaskChecked={checkTaskMistake} openRequest={exerciseOpenRequest} /></div>
      <div hidden={view !== "reading"}><CourseReading active={view === "reading" && !settingsOpen} key={materialRevision} completedLessonSlugs={allA1Lessons.filter((lesson) => progress[lesson.slug] === "completed").map((lesson) => lesson.slug)} learningMode={learningMode} /></div>
      <div hidden={view !== "vocabulary"}><CourseVocabulary completedLessonSlugs={allA1Lessons.filter((lesson) => progress[lesson.slug] === "completed").map((lesson) => lesson.slug)} /></div>
      <div hidden={view !== "homework"}><CourseHomework key={materialRevision} completedLessonSlugs={allA1Lessons.filter((lesson) => progress[lesson.slug] === "completed").map((lesson) => lesson.slug)} mistakeHints={generatedMistakeHints} learningMode={learningMode} personalCheatSheets={personalCheatSheets} recordedMistakeIds={recordedMistakeIds} mistakesDisabled={mistakesDisabled} onRecordMistake={recordTaskMistake} onTaskChecked={checkTaskMistake} openRequest={homeworkOpenRequest} /></div>

      {view === "listening" && <CourseListening key={selectedLesson.slug} lesson={selectedLesson} back={() => setView("material")} />}
      {view === "material" && selectedLesson.listening?.length && <button type="button" className="course-listening-launch" onClick={() => setView("listening")}>Послушать сообщения</button>}
      {view === "material" && <CourseMaterialView
        model={{ activeModule: activeCourseModule, lessons: orderedModuleLessons, selectedLesson, progress, lessonStep: manualPreview?.lessonSlug === selectedLesson.slug ? manualPreview.step : lessonSteps[selectedLesson.slug] ?? 0, practiceAnswers, practiceResults, checkSelections, reinforcementPractices, manualPreview: manualPreview?.lessonSlug === selectedLesson.slug }}
        actions={{
          openLesson: (lesson) => manualPreview ? openManualPreview(lesson) : openMaterial(lesson),
          setStep: (step) => manualPreview?.lessonSlug === selectedLesson.slug ? setManualPreview({ lessonSlug: selectedLesson.slug, step }) : progressController.actions.setLessonStep(step),
          updatePractice: manualPreview ? () => {} : progressController.actions.updatePractice,
          checkPractice: manualPreview ? () => {} : progressController.actions.checkPractice,
          selectKnowledgeAnswer: manualPreview ? () => {} : progressController.actions.selectKnowledgeAnswer,
          checkAllReinforcement: manualPreview ? () => {} : progressController.actions.checkAllReinforcement,
          resetLesson: (lesson) => { if (progressController.actions.resetLesson(lesson)) setView("topics"); },
          backToTopics: () => { setManualPreview(null); setView("topics"); },
          openChat: () => setView("reinforcement"),
          finishInteractiveAssessment: () => { progressController.actions.finishReinforcement(); setView("reinforcement"); },
        }}
      />}
      <div hidden={view !== "review"}><CourseReviewView
        learningMode={learningMode} disabled={mistakesDisabled} onChecked={checkTaskMistake}
        model={{ mistakes, modules: a1CourseModules }}
        actions={{ openTask: openTaskMistake, openTheory: (targetModule, lesson) => { setManualPreview(null); setActiveModule(targetModule.order); setSelectedSlug(lesson.slug); session.setLessonSteps((current) => ({ ...current, [lesson.slug]: 0 })); setTopicGroup("root"); openTestView("material"); }, openMistake: (targetModule, lesson, mistake) => { setManualPreview(null); setActiveModule(targetModule.order); setTopicGroup("root"); progressController.actions.openMistake(lesson, mistake); openTestView("material"); }, back: () => { setView("topics"); onAreaChange?.("learning"); } }}
      /></div>
      {view === "final" && <CourseFinalView
        model={{ module: activeCourseModule, moduleCount: a1CourseModules.length, lessons: orderedModuleLessons, questions: finalQuestions, selections: finalSelections, completed: finalCompleted, passingPercent: finalPassingPercent }}
        actions={{
          selectAnswer: progressController.actions.selectFinalAnswer,
          submit: progressController.actions.submitFinal,
          startAttempt: progressController.actions.startFinalAttempt,
          back: () => setView("topics"),
          openLesson: openMaterial,
          nextModule: () => selectModule(activeModule + 1),
        }}
      />}
      {view === "stats" && <CourseStatsPanel
        modules={a1CourseModules}
        module={activeCourseModule}
        lessons={orderedModuleLessons}
        progress={progress}
        practiceResults={practiceResults}
        checkSelections={checkSelections}
        mistakes={mistakes}
        summaries={lessonSummaries}
        completedCount={completedCount}
        accuracy={accuracy}
        correctPracticeCount={correctPracticeCount}
        totalPracticeCount={totalPracticeCount}
        dueCount={dueMistakes.length}
        back={() => setView("topics")}
        reset={() => { if (progressController.actions.resetModule()) setView("topics"); }}
      />}
      {view === "reinforcement" && <CourseReinforcementView
        model={{ lesson: selectedLesson, lessonNumber: displayLessonNumber(selectedLesson), lessonCount: orderedModuleLessons.length, summary: currentSummary, practices: reinforcementPractices, practiceAnswers, practiceResults }}
        actions={{
          backToMaterial: () => setView("material"),
          updatePractice: progressController.actions.updatePractice,
          checkPractice: progressController.actions.checkPractice,
          checkAll: progressController.actions.checkAllReinforcement,
          finish: progressController.actions.finishReinforcement,
          continueAfterSummary,
        }}
      />}
    </section>
    {settingsOpen && <AiSettingsPanel
      open={settingsOpen}
      profile={profileReady ? <LearnerProfileSettings profile={learnerProfile} onSaved={setLearnerProfile} loadError={profileError} /> : <p>Загружаю профиль…</p>}
      onClose={onSettingsClose}
      developmentMode={developmentMode}
      onDevelopmentModeChange={changeDevelopmentMode}
      learningMode={learningMode}
      onLearningModeChange={changeLearningMode}
      settingsSections={{ appearance: settingsSections.appearance, tasks: settingsSections.tasks, mistakes: settingsSections.mistakes, ai: settingsSections.ai }}
      onSettingsSectionChange={changeSettingsSection}
      appearance={<div className="course-test-grid course-settings-appearance"><CourseAppearanceControls session={session} showTitle={false} themeControl={themeControl} /></div>}
      tasks={<CourseTasksManager onChanged={() => setMaterialRevision((current) => current + 1)} />}
      mistakes={<div className="course-mistake-settings"><p>Сохранено ошибок: {Object.keys(mistakes).length}. Удаление очистит активные и закреплённые ошибки и план повторения. Прогресс уроков, ответы и задания сохранятся.</p><button type="button" disabled={session.readOnly || Boolean(persistenceError) || !Object.keys(mistakes).length} onClick={() => { if (!session.readOnly && !persistenceError && window.confirm("Удалить все сохранённые ошибки и план повторения? Прогресс уроков и задания останутся. Отменить удаление можно только восстановлением резервной копии.")) session.setMistakes({}); }}>Удалить все ошибки</button>{persistenceError && <p role="alert">Сначала устраните ошибку сохранения курса.</p>}</div>}
      backup={<CourseBackupPanel session={session} onRestored={() => { setView("topics"); onAreaChange?.("learning"); }} open={settingsSections.backup} onOpenChange={(open) => changeSettingsSection("backup", open)} />}
      developmentTools={developmentMode ? <CourseTestPanel session={session} lessons={orderedModuleLessons} lesson={selectedLesson}
        open={settingsSections.development}
        onOpenChange={(open) => changeSettingsSection("development", open)}
        openLesson={(lesson) => { openManualPreview(lesson, lessonSteps[lesson.slug] ?? 0); onSettingsClose(); }}
        openStep={(step) => { openManualPreview(selectedLesson, step); onSettingsClose(); }}
        openFinal={() => { openTestView("final"); onSettingsClose(); }}
        resetLesson={() => { const reset = progressController.actions.resetLesson(selectedLesson); if (reset) setView("topics"); return reset; }}
        resetModule={() => { const reset = progressController.actions.resetModule(); if (reset) setView("topics"); return reset; }}
        onExercisesDeleted={() => setMaterialRevision((current) => current + 1)}
      /> : null}
    />}
    </>
  );
}
