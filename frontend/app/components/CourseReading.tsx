"use client";

import { ReadingDictation } from "./ReadingDictation";
import { useLastCourseTask } from "../hooks/useLastCourseTask";

import { FormEvent, useEffect, useRef, useState } from "react";

import { a1CourseModules, allA1Lessons } from "../data/a1Course";
import { buildProgressGenerationContext } from "../data/courseGeneration";
import { buildCourseGenerationScope, completedCourseModules, completedCourseSections, type CourseGenerationMode } from "../data/courseGenerationScope";
import { learnedVocabularyContext, learnedVocabularySeeds } from "../data/courseVocabulary";
import { type LearningMode } from "../data/learningMode";
import { checkCourseReading, deleteCourseReading, generateCourseReading, getCourseReadings, type CourseReading as Reading, type CourseReadingAttempt } from "../lib/api";
import { generateSequentialBatch } from "../lib/batchGeneration";

type ReadingMode = Exclude<CourseGenerationMode, "mistakes">;

function readingNoun(count: number): string {
  const lastTwo = count % 100;
  if (lastTwo >= 11 && lastTwo <= 14) return "текстов";
  if (count % 10 === 1) return "текст";
  if (count % 10 >= 2 && count % 10 <= 4) return "текста";
  return "текстов";
}

export function CourseReading({ completedLessonSlugs, learningMode, active = true }: { completedLessonSlugs: string[]; learningMode: LearningMode; active?: boolean }) {
  const workspaceRef = useRef<HTMLFormElement>(null);
  const completedLessons = allA1Lessons.filter((item) => completedLessonSlugs.includes(item.slug));
  const [mode, setMode] = useState<ReadingMode>("topic");
  const [lessonSlug, setLessonSlug] = useState(completedLessons[0]?.slug ?? "");
  const sectionOptions = completedCourseSections(a1CourseModules, completedLessonSlugs);
  const [sectionKey, setSectionKey] = useState(sectionOptions[0]?.key ?? "");
  const moduleOptions = completedCourseModules(a1CourseModules, completedLessonSlugs);
  const [moduleSlug, setModuleSlug] = useState(moduleOptions[0]?.module.slug ?? "");
  const [items, setItems] = useState<Reading[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const { lastId, remember } = useLastCourseTask("reading");
  const [retelling, setRetelling] = useState("");
  const [result, setResult] = useState<CourseReadingAttempt | null>(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [batchCount, setBatchCount] = useState(1);
  const [generatedCount, setGeneratedCount] = useState(0);
  const [generationNotice, setGenerationNotice] = useState("");
  const [checking, setChecking] = useState(false);
  const [error, setError] = useState("");
  const lesson = completedLessons.find((item) => item.slug === lessonSlug) ?? completedLessons[0];
  const scope = buildCourseGenerationScope({ mode, modules: a1CourseModules, completedLessonSlugs, lessonSlug, sectionKey, moduleSlug });
  const storageSlug = scope.storageSlug;
  const visible = items.filter((item) => item.lesson_slug === storageSlug);
  const selected = visible.find((item) => item.id === selectedId) ?? visible[0];
  const lastTask = items.find((item) => item.id === lastId) ?? items[0];
  const selectedIndex = selected ? visible.findIndex((item) => item.id === selected.id) : -1;
  const nextReading = selectedIndex >= 0 ? visible[selectedIndex + 1] : undefined;
  const scopeLessonSlugs = scope.lessons.map((item) => item.slug);
  const vocabularyContext = learnedVocabularyContext(scope.lessons, scopeLessonSlugs);
  const vocabularyCount = learnedVocabularySeeds(scope.lessons, scopeLessonSlugs).length;

  useEffect(() => { void getCourseReadings().then((readings) => { setItems(readings); setSelectedId(readings[0]?.id ?? null); }).catch((cause) => setError(cause instanceof Error ? cause.message : "Не удалось загрузить тексты.")).finally(() => setLoading(false)); }, []);
  useEffect(() => {
    if (!completedLessons.some((item) => item.slug === lessonSlug)) setLessonSlug(completedLessons[0]?.slug ?? "");
  }, [completedLessons, lessonSlug]);
  useEffect(() => {
    if (!moduleOptions.some(({ module }) => module.slug === moduleSlug)) setModuleSlug(moduleOptions[0]?.module.slug ?? "");
  }, [moduleOptions, moduleSlug]);
  useEffect(() => {
    if (!sectionOptions.some(({ key }) => key === sectionKey)) setSectionKey(sectionOptions[0]?.key ?? "");
  }, [sectionKey, sectionOptions]);

  const openReading = (item: Reading) => {
    remember(item.id);
    setSelectedId(item.id);
    setResult(item.latest_attempt);
    if (selected?.id !== item.id) setRetelling("");
    requestAnimationFrame(() => workspaceRef.current?.scrollIntoView({ behavior: "smooth", block: "start" }));
  };

  const returnToLastTask = () => {
    if (!lastTask) return;
    const slug = lastTask.lesson_slug;
    if (slug.startsWith("section:")) { setMode("section"); setSectionKey(slug.slice(8)); }
    else if (slug.startsWith("module:")) { setMode("module"); setModuleSlug(slug.slice(7)); }
    else if (slug === "course-progress") setMode("progress");

    else { setMode("topic"); setLessonSlug(slug); }
    openReading(lastTask);
  };

  const generate = async () => {
    if (generating || learningMode === "offline") return;
    const requestedCount = Math.min(20, Math.max(1, Math.trunc(batchCount)));
    setGenerating(true); setGeneratedCount(0); setGenerationNotice(""); setError(""); setResult(null); setRetelling("");
    try {
      if (!scope.lessons.length) return;
      const theory = buildProgressGenerationContext({ mode, selectedLesson: lesson, completedLessons, mistakeHints: [], scope });
      const payload = { lesson_slug: scope.storageSlug, lesson_title: scope.title, theory, completed_theory: vocabularyContext };
      const batch = await generateSequentialBatch({ count: requestedCount, create: async (index, createdItems: readonly Reading[]) => {
        const knownIds = [...items, ...createdItems].map((item) => item.id);
        return generateCourseReading({ ...payload, batch_index: index + 1, batch_total: requestedCount }, knownIds);
      }, onProgress: ({ attempted }) => setGeneratedCount(attempted) });
      if (batch.items.length) {
        setItems((current) => [...batch.items.slice().reverse(), ...current]);
        setSelectedId(batch.items.at(-1)!.id);
        remember(batch.items.at(-1)!.id);
      }
      setGenerationNotice(batch.failed
        ? `Сохранено текстов: ${batch.created} из ${requestedCount}. Не удалось создать: ${batch.failed}.${batch.stoppedEarly ? " Генерация остановлена после трёх сбоев подряд." : ""}`
        : `Сохранено текстов: ${batch.created}.`);
      if (!batch.items.length) setError("Не удалось создать тексты после нескольких попыток. Сохранённые ранее тексты не потеряны.");
    } finally { setGenerating(false); }
  };

  const submit = async (event: FormEvent) => {
    event.preventDefault(); if (!selected || !retelling.trim()) return;
    remember(selected.id);
    setChecking(true); setError("");
    try { const checked = await checkCourseReading(selected.id, retelling.trim(), learningMode, selected.latest_attempt?.id); setResult(checked); setItems((current) => current.map((item) => item.id === selected.id ? { ...item, latest_attempt: checked } : item)); }
    catch (cause) { setError(cause instanceof Error ? cause.message : "Не удалось проверить пересказ."); }
    finally { setChecking(false); }
  };

  const remove = async (item: Reading) => {
    if (!window.confirm(`Удалить текст «${item.title}» вместе с пересказами?`)) return;
    setError("");
    try {
      await deleteCourseReading(item.id);
      setItems((current) => current.filter((reading) => reading.id !== item.id));
      if (selectedId === item.id) { setSelectedId(null); setResult(null); setRetelling(""); }
    } catch (cause) { setError(cause instanceof Error ? cause.message : "Не удалось удалить текст."); }
  };

  return <section className="course-exercises course-reading" aria-labelledby="course-reading-title" data-report-task-type="reading" data-report-task-id={selected?.id} data-report-task-title={selected ? selected.title : undefined} data-report-scope={scope.title}>
    <div className="course-section-heading"><div><span>Практика понимания</span><h3 id="course-reading-title">Чтение</h3></div><div className={`course-learning-mode ${learningMode}`}><strong>{learningMode === "online" ? "Онлайн" : "Офлайн"}</strong><p>{learningMode === "online" ? "ИИ создаёт тексты и гибко проверяет пересказ." : "Сохранённые тексты проверяются по эталону без обращения к ИИ."}</p></div></div>
    <div className="course-task-navigation">
    <div className="course-reading-modes" role="group" aria-label="Режим генерации текста">{([['topic', 'По теме'], ['section', 'По разделу'], ['module', 'По модулю'], ['progress', 'По общему прогрессу']] as const).map(([value, label]) => <button key={value} type="button" disabled={generating} className={mode === value ? "active" : ""} onClick={() => { setMode(value); setSelectedId(null); setResult(null); setRetelling(""); }}>{label}</button>)}</div>
    <button type="button" className="course-task-return" onClick={returnToLastTask} disabled={loading || generating || checking || !lastTask}>Вернуться к последнему заданию</button>
    </div>
    <div className="course-exercise-toolbar">{mode === "topic" ? <div className="course-generation-selectors"><label><span>Завершённая тема</span><select value={lessonSlug} disabled={!completedLessons.length || generating} onChange={(event) => { setLessonSlug(event.target.value); setSelectedId(null); setResult(null); setRetelling(""); }}>{completedLessons.map((item) => <option value={item.slug} key={item.slug}>{item.title}</option>)}</select></label><small>{vocabularyCount} открытых слов и фраз в выбранной теме.</small></div> : mode === "section" ? <div className="course-generation-selectors"><label><span>Учебный раздел</span><select value={sectionOptions.find(({ key }) => key === sectionKey)?.key ?? ""} disabled={!sectionOptions.length || generating} onChange={(event) => { setSectionKey(event.target.value); setSelectedId(null); setResult(null); setRetelling(""); }}>{sectionOptions.map(({ key, module, section, lessons }) => <option key={key} value={key}>Модуль {module.order} · {section.title} · {lessons.length} тем</option>)}</select></label><small>{vocabularyCount} открытых слов и фраз · только завершённые темы этого раздела.</small></div> : mode === "module" ? <div className="course-generation-selectors"><label><span>Модуль с завершёнными темами</span><select value={scope.module?.slug ?? ""} disabled={!moduleOptions.length || generating} onChange={(event) => { setModuleSlug(event.target.value); setSelectedId(null); setResult(null); setRetelling(""); }}>{moduleOptions.map(({ module, lessons }) => <option key={module.slug} value={module.slug}>Модуль {module.order}. {module.title} · {lessons.length} тем</option>)}</select></label><small>{vocabularyCount} открытых слов и фраз · только завершённые темы модуля.</small></div> : <div className="course-reading-scope"><span>Доступный материал</span><strong>{completedLessons.length} завершённых тем · {vocabularyCount} слов и фраз</strong><small>Используются только завершённые темы.</small></div>}<div className="course-exercise-create"><label className="course-exercise-count"><span>Количество текстов</span><input type="number" min={1} max={20} step={1} value={batchCount} disabled={generating || learningMode === "offline"} onChange={(event) => setBatchCount(Math.min(20, Math.max(1, Math.trunc(Number(event.target.value) || 1))))} /></label><button type="button" onClick={() => void generate()} disabled={generating || !scope.lessons.length || learningMode === "offline"}>{generating ? `Создаю ${generatedCount}/${batchCount}…` : batchCount === 1 ? "Новый текст" : `Создать ${batchCount} ${readingNoun(batchCount)}`}</button>{learningMode === "offline" && <small>Новые тексты создаются только онлайн.</small>}</div></div>
    {!completedLessons.length && <p className="course-empty">Завершите хотя бы одну тему, чтобы создавать тексты.</p>}
    {generationNotice && <p className="course-generation-notice" role="status">{generationNotice}</p>}
    {error && <p className="course-persistence-error" role="alert">{error}</p>}
    {loading ? <p>Загружаю тексты…</p> : <div className="course-exercise-grid"><aside className="course-exercise-list"><strong>Сохранённые тексты</strong>{visible.length ? visible.map((item) => <article className={selected?.id === item.id ? "active" : ""} key={item.id}><button type="button" onClick={() => openReading(item)}><span>{item.lesson_title}</span><b>{item.title}</b>{item.latest_attempt && <small>Пересказ: {item.latest_attempt.score}/100</small>}</button><button type="button" className="delete" onClick={() => void remove(item)} aria-label={`Удалить текст: ${item.title}`}>Удалить</button></article>) : <p>Текстов по этой теме пока нет.</p>}</aside><form ref={workspaceRef} className="course-exercise-workspace" onSubmit={(event) => void submit(event)}>{selected ? <><span>{selected.lesson_title}</span><h4>{selected.title}</h4><p className="course-reading-text" lang="sk">{selected.text}</p><small>{selected.instruction}</small><ReadingDictation key={selected.id} active={active && !generating} disabled={checking} onText={(text) => setRetelling((current) => current + (current && !/\s$/.test(current) ? " " : "") + text)} /><textarea rows={6} value={retelling} onChange={(event) => setRetelling(event.target.value)} placeholder="Напишите по-русски, о чём этот текст…" disabled={checking} /><button type="submit" disabled={!retelling.trim() || checking || (learningMode === "offline" && !selected.offline_ready)}>{checking ? "Проверяю…" : learningMode === "offline" ? "Проверить офлайн" : "Проверить пересказ"}</button>{learningMode === "offline" && !selected.offline_ready && <small>У старого текста нет эталона. Для него нужна онлайн-проверка.</small>}{(result ?? selected.latest_attempt) && (() => { const checked = result ?? selected.latest_attempt!; return <><article className={checked.score >= 70 ? "correct" : "incorrect"}><strong>Результат: {checked.score}/100</strong><p>{checked.feedback}</p><p><b>Хороший вариант:</b> {checked.corrected_retelling}</p></article><button type="button" className="course-task-next" disabled={!nextReading} onClick={() => nextReading && openReading(nextReading)}>{nextReading ? "Следующий текст →" : "Это последний текст"}</button></>; })()}</> : <div className="course-empty"><strong>Выберите или создайте текст</strong><p>Текст будет ограничен грамматикой выбранной и предыдущих тем.</p></div>}</form></div>}
  </section>;
}
