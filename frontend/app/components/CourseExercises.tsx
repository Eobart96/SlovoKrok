"use client";

import { FormEvent, useEffect, useMemo, useRef, useState } from "react";

import { allA1Lessons } from "../data/a1Course";
import { buildExerciseGenerationContext, buildProgressGenerationContext, nextExerciseFormat, type GenerationMistakeHint } from "../data/courseGeneration";
import { learnedVocabularySeeds } from "../data/courseVocabulary";
import { type LearningMode } from "../data/learningMode";
import { answerCourseExercise, deleteCourseExercise, generateCourseExercise, getCourseExercises, type CourseExercise, type CourseExerciseAttempt } from "../lib/api";
import { CourseExercisePlayer } from "./CourseExercisePlayer";

type ExerciseMode = "topic" | "progress";

function exerciseNoun(count: number): string {
  const lastTwo = count % 100;
  if (lastTwo >= 11 && lastTwo <= 14) return "упражнений";
  if (count % 10 === 1) return "упражнение";
  if (count % 10 >= 2 && count % 10 <= 4) return "упражнения";
  return "упражнений";
}

export function CourseExercises({ completedLessonSlugs, mistakeHints, learningMode }: { completedLessonSlugs: string[]; mistakeHints: GenerationMistakeHint[]; learningMode: LearningMode }) {
  const answerRef = useRef<HTMLTextAreaElement>(null);
  const completedLessons = allA1Lessons.filter((item) => completedLessonSlugs.includes(item.slug));
  const [mode, setMode] = useState<ExerciseMode>("topic");
  const [lessonSlug, setLessonSlug] = useState(completedLessons[0]?.slug ?? "");
  const [exercises, setExercises] = useState<CourseExercise[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
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
  const storageSlug = mode === "progress" ? "course-progress" : lessonSlug;
  const visible = exercises.filter((item) => item.lesson_slug === storageSlug);
  const nextFormat = nextExerciseFormat(visible.length);
  const selected = visible.find((item) => item.id === selectedId) ?? visible[0];
  const learnedCount = useMemo(() => learnedVocabularySeeds(allA1Lessons, completedLessonSlugs).length, [completedLessonSlugs]);
  const relevantMistakeCount = mistakeHints.filter((hint) => mode === "progress" ? completedLessonSlugs.includes(hint.lessonSlug) : hint.lessonSlug === lesson?.slug).length;

  useEffect(() => {
    void getCourseExercises().then((items) => { setExercises(items); setSelectedId(items[0]?.id ?? null); }).catch((cause) => setError(cause instanceof Error ? cause.message : "Не удалось загрузить упражнения.")).finally(() => setLoading(false));
  }, []);
  useEffect(() => {
    if (!completedLessons.some((item) => item.slug === lessonSlug)) setLessonSlug(completedLessons[0]?.slug ?? "");
  }, [completedLessons, lessonSlug]);

  const generate = async () => {
    if (generating || learningMode === "offline") return;
    const requestedCount = Math.min(20, Math.max(1, Math.trunc(batchCount)));
    const createdItems: CourseExercise[] = [];
    setGenerating(true); setGeneratedCount(0); setGenerationNotice(""); setError(""); setAssessment(null); setAnswer("");
    try {
      if (!completedLessons.length || (mode === "topic" && !lesson)) return;
      const baseContext = buildProgressGenerationContext({ mode, selectedLesson: lesson, completedLessons, mistakeHints });
      for (let index = 0; index < requestedCount; index += 1) {
        const format = nextExerciseFormat(visible.length + index);
        const theory = buildExerciseGenerationContext({
          baseContext,
          format,
          sourceLessons: mode === "topic" && lesson ? [lesson] : [...completedLessons].reverse().slice(0, 4),
        });
        const item = mode === "topic"
          ? await generateCourseExercise({ lesson_slug: lesson.slug, lesson_title: lesson.title, theory })
          : await generateCourseExercise({ lesson_slug: "course-progress", lesson_title: "Общий прогресс Slovak A1", theory });
        createdItems.push(item);
        setGeneratedCount(createdItems.length);
      }
    } catch (cause) { setError(cause instanceof Error ? cause.message : "Не удалось создать упражнение."); }
    finally {
      if (createdItems.length) {
        setExercises((current) => [...createdItems.slice().reverse(), ...current]);
        setSelectedId(createdItems.at(-1)!.id);
        setGenerationNotice(`Сохранено заданий: ${createdItems.length}. Их можно выполнить в офлайн-режиме.`);
      }
      setGenerating(false);
    }
  };

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    if (!selected || !answer.trim() || submitting) return;
    setSubmitting(true); setError("");
    try {
      const result = await answerCourseExercise(selected.id, answer.trim(), learningMode);
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

  return <section className="course-exercises" aria-labelledby="course-exercises-title">
    <div className="course-section-heading"><div><span>Практика по прогрессу</span><h3 id="course-exercises-title">Упражнения</h3></div><div className={`course-learning-mode ${learningMode}`}><strong>{learningMode === "online" ? "Онлайн" : "Офлайн"}</strong><p>{learningMode === "online" ? "ИИ доступен для генерации и гибкой проверки." : "Новых запросов к ИИ нет; ответы проверяются по сохранённым эталонам."}</p></div></div>
    <div className="course-reading-modes" role="group" aria-label="Режим генерации упражнения"><button type="button" disabled={generating} className={mode === "topic" ? "active" : ""} onClick={() => { setMode("topic"); setSelectedId(null); setAssessment(null); setAnswer(""); }}>По теме</button><button type="button" disabled={generating} className={mode === "progress" ? "active" : ""} onClick={() => { setMode("progress"); setSelectedId(null); setAssessment(null); setAnswer(""); }}>По общему прогрессу</button></div>
    <div className="course-exercise-toolbar">
      {mode === "topic" ? <label><span>Завершённая тема</span><select value={lessonSlug} disabled={!completedLessons.length || generating} onChange={(event) => { setLessonSlug(event.target.value); setSelectedId(null); setAssessment(null); setAnswer(""); }}>{completedLessons.map((item) => <option key={item.slug} value={item.slug}>{item.title}</option>)}</select><small>{learnedCount} открытых слов и фраз · {relevantMistakeCount} активных ошибок по теме</small></label> : <div className="course-reading-scope"><span>Доступный материал</span><strong>{completedLessons.length} завершённых тем · {learnedCount} слов и фраз</strong><small>{relevantMistakeCount ? `Учитывается активных ошибок: ${relevantMistakeCount}.` : "Активных ошибок в пройденном материале нет."}</small></div>}
      <div className="course-exercise-create">
        <small>Следующий формат: <b>{nextFormat.label}</b></small>
        <label className="course-exercise-count"><span>Количество заданий</span><input type="number" min={1} max={20} step={1} value={batchCount} disabled={generating || learningMode === "offline"} onChange={(event) => setBatchCount(Math.min(20, Math.max(1, Math.trunc(Number(event.target.value) || 1))))} /></label>
        <button type="button" onClick={() => void generate()} disabled={generating || !completedLessons.length || learningMode === "offline"}>{generating ? `Создаю ${generatedCount}/${batchCount}…` : batchCount === 1 ? "Создать упражнение" : `Создать ${batchCount} ${exerciseNoun(batchCount)}`}</button>
        {learningMode === "offline" && <small>Чтобы пополнить запас, включите онлайн-режим в настройках.</small>}
      </div>
    </div>
    {!completedLessons.length && <p className="course-empty">Завершите хотя бы одну тему, чтобы создавать упражнения.</p>}
    {generationNotice && <p className="course-generation-notice" role="status">{generationNotice}</p>}
    {error && <p className="course-persistence-error" role="alert">{error}</p>}
    {loading ? <p className="course-empty">Загружаю упражнения…</p> : <div className="course-exercise-grid">
      <aside className="course-exercise-list"><strong>Сохранённые задания · {visible.length}</strong>{visible.length === 0 ? <p>Созданных заданий пока нет.</p> : visible.map((item, index) => <article className={selected?.id === item.id ? "active" : ""} key={item.id}><button type="button" onClick={() => { setSelectedId(item.id); setAssessment(item.latest_attempt); setAnswer(""); }}><span>Упражнение {visible.length - index}</span><b>{item.question}</b>{item.latest_attempt && <small>{item.latest_attempt.is_correct ? "✓ Выполнено" : `Последний результат: ${item.latest_attempt.score}/100`}</small>}</button><button type="button" className="delete" onClick={() => void remove(item)} aria-label={`Удалить упражнение: ${item.question}`}>Удалить</button></article>)}</aside>
      <form className="course-exercise-workspace" onSubmit={(event) => void submit(event)}>{selected ? <><span>{selected.lesson_title}</span><h4>{selected.question}</h4><p>{selected.instruction}</p><CourseExercisePlayer key={selected.id} exercise={selected} answer={answer} onAnswerChange={setAnswer} answerRef={answerRef} disabled={submitting} onInsertKey={insertKey} /><button type="submit" disabled={!answer.trim() || submitting}>{submitting ? "Проверяю…" : "Проверить ответ"}</button>{(assessment ?? selected.latest_attempt) && (() => { const result = assessment ?? selected.latest_attempt!; return <article className={result.is_correct ? "correct" : "incorrect"}><strong>{result.is_correct ? "Верно" : "Нужно исправить"} · {result.score}/100</strong>{!result.is_correct && <p><b>Исправленный вариант:</b> {result.corrected_answer}</p>}<p>{result.explanation}</p><small>Следующий шаг: {result.next_exercise}</small></article>; })()}</> : <div className="course-empty"><strong>Выберите или создайте упражнение</strong><p>Генератор использует только теорию выбранной темы.</p></div>}</form>
    </div>}
  </section>;
}
