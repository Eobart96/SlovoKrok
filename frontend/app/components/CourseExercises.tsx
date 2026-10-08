"use client";

import { useLastCourseTask } from "../hooks/useLastCourseTask";

import { FormEvent, useEffect, useMemo, useRef, useState } from "react";

import type { CourseModule } from "../data/courseTypes";
import { buildExerciseGenerationContext, buildProgressGenerationContext, nextExerciseFormat, type GenerationMistakeHint } from "../data/courseGeneration";
import { buildCourseGenerationScope, completedCourseModules, completedCourseSections, isCourseGenerationScopeSlug, type CourseGenerationMode } from "../data/courseGenerationScope";
import { learnedVocabularySeeds } from "../data/courseVocabulary";
import { type LearningMode } from "../data/learningMode";
import { answerCourseExercise, deleteCourseExercise, generateCourseExercise, getCourseExercises, type CourseExercise, type CourseExerciseAttempt } from "../lib/api";
import { generateSequentialBatch } from "../lib/batchGeneration";
import { CourseExercisePlayer } from "./CourseExercisePlayer";

import type { TaskMistakeInput, TaskOpenRequest } from "../data/taskMistakes";
import { CourseTaskMistakeButton } from "./CourseTaskMistakeButton";

type ExerciseMode = Exclude<CourseGenerationMode, "mistakes">;

function exerciseNoun(count: number): string {
  const lastTwo = count % 100;
  if (lastTwo >= 11 && lastTwo <= 14) return "упражнений";
  if (count % 10 === 1) return "упражнение";
  if (count % 10 >= 2 && count % 10 <= 4) return "упражнения";
  return "упражнений";
}

export function CourseExercises({ modules, completedLessonSlugs, mistakeHints, learningMode, recordedMistakeIds, mistakesDisabled, onRecordMistake, onTaskChecked, openRequest }: { modules: CourseModule[]; completedLessonSlugs: string[]; mistakeHints: GenerationMistakeHint[]; learningMode: LearningMode; recordedMistakeIds: string[]; mistakesDisabled: boolean; onRecordMistake: (mistake: TaskMistakeInput) => void; onTaskChecked: (id: string, correct: boolean) => void; openRequest: TaskOpenRequest | null }) {
  const answerRef = useRef<HTMLTextAreaElement>(null);
  const workspaceRef = useRef<HTMLFormElement>(null);
  const allLessons = useMemo(() => modules.flatMap((module) => module.lessons), [modules]);
  const completedLessons = allLessons.filter((item) => completedLessonSlugs.includes(item.slug));
  const [mode, setMode] = useState<ExerciseMode>("topic");
  const [lessonSlug, setLessonSlug] = useState(completedLessons[0]?.slug ?? "");
  const sectionOptions = completedCourseSections(modules, completedLessonSlugs);
  const [sectionKey, setSectionKey] = useState(sectionOptions[0]?.key ?? "");
  const moduleOptions = completedCourseModules(modules, completedLessonSlugs);
  const [moduleSlug, setModuleSlug] = useState(moduleOptions[0]?.module.slug ?? "");
  const [exercises, setExercises] = useState<CourseExercise[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const { lastId, remember } = useLastCourseTask("exercise", modules[0]?.level === "A2" ? "a2" : "a1");
  const handledRequest = useRef<number | null>(null);
  const [answer, setAnswer] = useState("");
  const [assessment, setAssessment] = useState<CourseExerciseAttempt | null>(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [batchCount, setBatchCount] = useState(1);
  const [generatedCount, setGeneratedCount] = useState(0);
  const [generationNotice, setGenerationNotice] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const lesson = completedLessons.find((item) => item.slug === lessonSlug) ?? completedLessons[0];
  const scope = buildCourseGenerationScope({ mode, modules, completedLessonSlugs, lessonSlug, sectionKey, moduleSlug });
  const storageSlug = scope.storageSlug;
  const visible = exercises.filter((item) => item.lesson_slug === storageSlug);
  const nextFormat = nextExerciseFormat(visible.length);
  const selected = visible.find((item) => item.id === selectedId) ?? visible[0];
  const lastTask = exercises.find((item) => item.id === lastId) ?? exercises[0];
  const selectedIndex = selected ? visible.findIndex((item) => item.id === selected.id) : -1;
  const nextExercise = selectedIndex >= 0 ? visible[selectedIndex + 1] : undefined;
  const learnedCount = useMemo(() => learnedVocabularySeeds(allLessons, completedLessonSlugs).length, [allLessons, completedLessonSlugs]);
  const scopeLessonSlugs = new Set(scope.lessons.map((item) => item.slug));
  const relevantMistakeCount = mistakeHints.filter((hint) => scopeLessonSlugs.has(hint.lessonSlug)).length;

  useEffect(() => {
    let cancelled = false;
    void getCourseExercises().then((items) => {
      if (cancelled) return;
      const available = items.filter((item) => isCourseGenerationScopeSlug(modules, item.lesson_slug));
      setExercises(available); setSelectedId(available[0]?.id ?? null);
    }).catch((cause) => { if (!cancelled) setError(cause instanceof Error ? cause.message : "Не удалось загрузить упражнения."); }).finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [modules]);
  useEffect(() => {
    if (!completedLessons.some((item) => item.slug === lessonSlug)) setLessonSlug(completedLessons[0]?.slug ?? "");
  }, [completedLessons, lessonSlug]);
  useEffect(() => {
    if (!moduleOptions.some(({ module }) => module.slug === moduleSlug)) setModuleSlug(moduleOptions[0]?.module.slug ?? "");
  }, [moduleOptions, moduleSlug]);
  useEffect(() => {
    if (!sectionOptions.some(({ key }) => key === sectionKey)) setSectionKey(sectionOptions[0]?.key ?? "");
  }, [sectionKey, sectionOptions]);

  useEffect(() => {
    if (!openRequest || handledRequest.current === openRequest.nonce) return;
    const task = exercises.find((item) => item.id === openRequest.id);
    if (!task) {
      if (!loading) { handledRequest.current = openRequest.nonce; setError("Исходное упражнение удалено или недоступно. Исправление сохранено в разделе ошибок."); }
      return;
    }
    handledRequest.current = openRequest.nonce;
    remember(task.id);
    const slug = task.lesson_slug;
    if (slug.startsWith("section:")) { setMode("section"); setSectionKey(slug.slice(8)); }
    else if (slug.startsWith("module:")) { setMode("module"); setModuleSlug(slug.slice(7)); }
    else if (slug === "course-progress" || slug === "course:a2:progress") setMode("progress");

    else { setMode("topic"); setLessonSlug(slug); }
    setSelectedId(task.id); setAssessment(task.latest_attempt); setAnswer("");
  }, [openRequest, exercises, loading]);

  const openExercise = (item: CourseExercise) => {
    remember(item.id);
    setSelectedId(item.id);
    setAssessment(item.latest_attempt);
    if (selected?.id !== item.id) setAnswer("");
    requestAnimationFrame(() => workspaceRef.current?.scrollIntoView({ behavior: "smooth", block: "start" }));
  };

  const returnToLastTask = () => {
    if (!lastTask) return;
    const slug = lastTask.lesson_slug;
    if (slug.startsWith("section:")) { setMode("section"); setSectionKey(slug.slice(8)); }
    else if (slug.startsWith("module:")) { setMode("module"); setModuleSlug(slug.slice(7)); }
    else if (slug === "course-progress" || slug === "course:a2:progress") setMode("progress");

    else { setMode("topic"); setLessonSlug(slug); }
    openExercise(lastTask);
  };

  const generate = async () => {
    if (generating || learningMode === "offline") return;
    const requestedCount = Math.min(100, Math.max(1, Math.trunc(batchCount)));
    setGenerating(true); setGeneratedCount(0); setGenerationNotice(""); setError(""); setAssessment(null); setAnswer("");
    try {
      if (!scope.lessons.length) return;
      const baseContext = buildProgressGenerationContext({ mode, selectedLesson: lesson, completedLessons, mistakeHints, scope });
      const batch = await generateSequentialBatch({ count: requestedCount, create: async (index, createdItems: readonly CourseExercise[]) => {
        const format = nextExerciseFormat(visible.length + index);
        const theory = buildExerciseGenerationContext({
          baseContext,
          format,
          sourceLessons: [...scope.lessons].reverse().slice(0, 4),
        });
        const knownIds = [...exercises, ...createdItems].map((item) => item.id);
        let lastError: unknown;
        for (let attempt = 0; attempt < 3; attempt += 1) {
          try {
            const attemptTheory = attempt === 0
              ? theory
              : `${theory}\n\nПовторная попытка ${attempt + 1}: прошлый ответ не был принят. Создай другое упражнение того же формата. Верни ровно один корректный JSON без текста до или после него и соблюдай указанный тип интерактива.`;
            return await generateCourseExercise({ lesson_slug: scope.storageSlug, lesson_title: scope.title, theory: attemptTheory }, knownIds);
          } catch (cause) {
            lastError = cause;
          }
        }
        throw lastError;
      }, onProgress: ({ attempted }) => setGeneratedCount(attempted) });
      if (batch.items.length) {
        setExercises((current) => [...batch.items.slice().reverse(), ...current]);
        setSelectedId(batch.items.at(-1)!.id);
        remember(batch.items.at(-1)!.id);
      }
      setGenerationNotice(batch.failed
        ? `Сохранено заданий: ${batch.created} из ${requestedCount}. Не удалось создать: ${batch.failed}.${batch.stoppedEarly ? " Генерация остановлена после трёх сбоев подряд." : ""}`
        : `Сохранено заданий: ${batch.created}. Их можно выполнить в офлайн-режиме.`);
      if (!batch.items.length) setError("Не удалось создать упражнения после нескольких попыток. Сохранённые ранее задания не потеряны.");
    } finally { setGenerating(false); }
  };

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    if (!selected || !answer.trim() || submitting) return;
    remember(selected.id);
    setSubmitting(true); setError("");
    try {
      const result = await answerCourseExercise(selected.id, answer.trim(), learningMode, selected.latest_attempt?.id);
      onTaskChecked(`exercise:${selected.id}`, result.is_correct);
      setAssessment(result);
      setExercises((current) => current.map((item) => item.id === selected.id ? { ...item, latest_attempt: result } : item));
    } catch (cause) { setError(cause instanceof Error ? cause.message : "Не удалось проверить ответ."); }
    finally { setSubmitting(false); }
  };

  const insertKey = (key: string) => {
    const textarea = answerRef.current;
    if (!textarea) return;
    const start = textarea.selectionStart ?? answer.length;
    const end = textarea.selectionEnd ?? start;
    setAnswer(`${answer.slice(0, start)}${key}${answer.slice(end)}`);
    requestAnimationFrame(() => { textarea.focus(); textarea.setSelectionRange(start + key.length, start + key.length); });
  };

  const remove = async (item: CourseExercise) => {
    if (!window.confirm(`Удалить упражнение «${item.question}» вместе с историей ответов?`)) return;
    setError("");
    try {
      await deleteCourseExercise(item.id);
      setExercises((current) => current.filter((exercise) => exercise.id !== item.id));
      if (selectedId === item.id) { setSelectedId(null); setAssessment(null); setAnswer(""); }
    } catch (cause) { setError(cause instanceof Error ? cause.message : "Не удалось удалить упражнение."); }
  };

  return <section className="course-exercises" aria-labelledby="course-exercises-title" data-report-task-type="exercise" data-report-task-id={selected?.id} data-report-task-title={selected ? selected.question : undefined} data-report-scope={scope.title}>
    <div className="course-section-heading"><div><span>Практика по прогрессу</span><h3 id="course-exercises-title">Упражнения</h3></div><div className={`course-learning-mode ${learningMode}`}><strong>{learningMode === "online" ? "Онлайн" : "Офлайн"}</strong><p>{learningMode === "online" ? "ИИ доступен для генерации и гибкой проверки." : "Новых запросов к ИИ нет; ответы проверяются по сохранённым эталонам."}</p></div></div>
    <div className="course-task-navigation">
    <div className="course-reading-modes" role="group" aria-label="Режим генерации упражнения">{([['topic', 'По теме'], ['section', 'По разделу'], ['module', 'По модулю'], ['progress', 'По общему прогрессу']] as const).map(([value, label]) => <button key={value} type="button" disabled={generating} className={mode === value ? "active" : ""} onClick={() => { setMode(value); setSelectedId(null); setAssessment(null); setAnswer(""); }}>{label}</button>)}</div>
    <button type="button" className="course-task-return" onClick={returnToLastTask} disabled={loading || generating || submitting || !lastTask}>Вернуться к последнему заданию</button>
    </div>
    <div className="course-exercise-toolbar">
      {mode === "topic" ? <div className="course-generation-selectors"><label><span>Завершённая тема</span><select value={lessonSlug} disabled={!completedLessons.length || generating} onChange={(event) => { setLessonSlug(event.target.value); setSelectedId(null); setAssessment(null); setAnswer(""); }}>{completedLessons.map((item) => <option key={item.slug} value={item.slug}>{item.title}</option>)}</select></label><small>{relevantMistakeCount} активных ошибок в выбранной теме</small></div> : mode === "section" ? <div className="course-generation-selectors"><label><span>Учебный раздел</span><select value={sectionOptions.find(({ key }) => key === sectionKey)?.key ?? ""} disabled={!sectionOptions.length || generating} onChange={(event) => { setSectionKey(event.target.value); setSelectedId(null); setAssessment(null); setAnswer(""); }}>{sectionOptions.map(({ key, module, section, lessons }) => <option key={key} value={key}>Модуль {module.order} · {section.title} · {lessons.length} тем</option>)}</select></label><small>Это раздел с экрана выбора тем; используются только завершённые темы внутри него.</small></div> : mode === "module" ? <div className="course-generation-selectors"><label><span>Модуль с завершёнными темами</span><select value={scope.module?.slug ?? ""} disabled={!moduleOptions.length || generating} onChange={(event) => { setModuleSlug(event.target.value); setSelectedId(null); setAssessment(null); setAnswer(""); }}>{moduleOptions.map(({ module, lessons }) => <option key={module.slug} value={module.slug}>Модуль {module.order}. {module.title} · {lessons.length} тем</option>)}</select></label><small>Генератор использует только завершённые темы выбранного модуля.</small></div> : <div className="course-reading-scope"><span>Доступный материал</span><strong>{completedLessons.length} завершённых тем · {learnedCount} слов и фраз</strong><small>{relevantMistakeCount ? `Учитывается активных ошибок: ${relevantMistakeCount}.` : "Активных ошибок в пройденном материале нет."}</small></div>}
      <div className="course-exercise-create">
        <small>Следующий формат: <b>{nextFormat.label}</b></small>
        <label className="course-exercise-count"><span>Количество заданий</span><input type="number" min={1} max={100} step={1} value={batchCount} disabled={generating || learningMode === "offline"} onChange={(event) => setBatchCount(Math.min(100, Math.max(1, Math.trunc(Number(event.target.value) || 1))))} /></label>
        <button type="button" onClick={() => void generate()} disabled={generating || !completedLessons.length || learningMode === "offline"}>{generating ? `Создаю ${generatedCount}/${batchCount}…` : batchCount === 1 ? "Создать упражнение" : `Создать ${batchCount} ${exerciseNoun(batchCount)}`}</button>
        {learningMode === "offline" && <small>Чтобы пополнить запас, включите онлайн-режим в настройках.</small>}
      </div>
    </div>
    {!completedLessons.length && <p className="course-empty">Завершите хотя бы одну тему, чтобы создавать упражнения.</p>}
    {generationNotice && <p className="course-generation-notice" role="status">{generationNotice}</p>}
    {error && <p className="course-persistence-error" role="alert">{error}</p>}
    {loading ? <p className="course-empty">Загружаю упражнения…</p> : <div className="course-exercise-grid">
      <aside className="course-exercise-list"><strong>Сохранённые задания · {visible.length}</strong>{visible.length === 0 ? <p>Созданных заданий пока нет.</p> : visible.map((item, index) => <article className={selected?.id === item.id ? "active" : ""} key={item.id}><button type="button" onClick={() => openExercise(item)}><span>Упражнение {visible.length - index}</span><b>{item.question}</b>{item.latest_attempt && <small>{item.latest_attempt.is_correct ? "✓ Выполнено" : `Последний результат: ${item.latest_attempt.score}/100`}</small>}</button><button type="button" className="delete" onClick={() => void remove(item)} aria-label={`Удалить упражнение: ${item.question}`}>Удалить</button></article>)}</aside>
      <form ref={workspaceRef} className="course-exercise-workspace" onSubmit={(event) => void submit(event)}>{selected ? <><span>{selected.lesson_title}</span><h4>{selected.question}</h4><p>{selected.instruction}</p><CourseExercisePlayer key={selected.id} exercise={selected} answer={answer} onAnswerChange={setAnswer} answerRef={answerRef} disabled={submitting} onInsertKey={insertKey} /><button type="submit" disabled={!answer.trim() || submitting}>{submitting ? "Проверяю…" : "Проверить ответ"}</button>{(assessment ?? selected.latest_attempt) && (() => { const result = assessment ?? selected.latest_attempt!; return <><article className={result.is_correct ? "correct" : "incorrect"}><strong>{result.is_correct ? "Верно" : "Нужно исправить"} · {result.score}/100</strong>{!result.is_correct && <p><b>Исправленный вариант:</b> {result.corrected_answer}</p>}<p>{result.explanation}</p><small>Следующий шаг: {result.next_exercise}</small></article>{!result.is_correct && <CourseTaskMistakeButton mistake={{ id: `exercise:${selected.id}`, lessonSlug: selected.lesson_slug, prompt: `${selected.lesson_title} · ${selected.question}\n${selected.instruction}\nВаш ответ: ${result.answer}\n${result.explanation}`.slice(0, 2000), answer: result.corrected_answer, reviewTask: { prompt: `${selected.question}\n${selected.instruction}`.slice(0, 4000), learnerAnswer: result.answer.slice(0, 4000), explanation: result.explanation, kind: selected.interaction_type ? "exact" : "open" } }} recorded={recordedMistakeIds.includes(`exercise:${selected.id}`)} disabled={mistakesDisabled} onRecord={onRecordMistake} />}<button type="button" className="course-task-next" disabled={!nextExercise} onClick={() => nextExercise && openExercise(nextExercise)}>{nextExercise ? "Следующее задание →" : "Это последнее задание"}</button></>; })()}</> : <div className="course-empty"><strong>Выберите или создайте упражнение</strong><p>Генератор использует только теорию выбранной темы.</p></div>}</form>
    </div>}
  </section>;
}
