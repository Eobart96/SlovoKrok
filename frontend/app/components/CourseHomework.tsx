"use client";

import { useLastCourseTask } from "../hooks/useLastCourseTask";

import { FormEvent, type KeyboardEvent, useEffect, useMemo, useRef, useState } from "react";

import type { CourseModule } from "../data/courseTypes";
import { buildProgressGenerationContext, type GenerationMistakeHint } from "../data/courseGeneration";
import { buildCourseGenerationScope, completedCourseModules, completedCourseSections, isCourseGenerationScopeSlug, type CourseGenerationMode } from "../data/courseGenerationScope";
import { homeworkAssignmentHints, rankHomeworkReferenceLessons, selectHomeworkReferenceLessons } from "../data/homeworkPlanning";
import { type LearningMode } from "../data/learningMode";
import { applySlovakAltShortcut } from "../data/slovakKeyboard";
import { learnedVocabularySeeds } from "../data/courseVocabulary";
import { deleteCourseHomework, generateCourseHomework, getCourseHomework, submitCourseHomework, type CourseHomework as Homework, type CourseHomeworkAttempt, type PersonalCheatSheet } from "../lib/api";
import { generateSequentialBatch } from "../lib/batchGeneration";
import { CourseHomeworkReference } from "./CourseHomeworkReference";
import { SlovakKeyboard } from "./SlovakKeyboard";

import type { TaskMistakeInput, TaskOpenRequest } from "../data/taskMistakes";
import { CourseTaskMistakeButton } from "./CourseTaskMistakeButton";

type HomeworkMode = CourseGenerationMode;

function homeworkNoun(count: number): string {
  const lastTwo = count % 100;
  if (lastTwo >= 11 && lastTwo <= 14) return "домашних заданий";
  if (count % 10 === 1) return "домашнее задание";
  if (count % 10 >= 2 && count % 10 <= 4) return "домашних задания";
  return "домашних заданий";
}

export function CourseHomework({ modules, completedLessonSlugs, mistakeHints, learningMode, personalCheatSheets, recordedMistakeIds, mistakesDisabled, onRecordMistake, onTaskChecked, openRequest }: { modules: CourseModule[]; completedLessonSlugs: string[]; mistakeHints: GenerationMistakeHint[]; learningMode: LearningMode; personalCheatSheets: PersonalCheatSheet[]; recordedMistakeIds: string[]; mistakesDisabled: boolean; onRecordMistake: (mistake: TaskMistakeInput) => void; onTaskChecked: (id: string, correct: boolean) => void; openRequest: TaskOpenRequest | null }) {
  const allLessons = useMemo(() => modules.flatMap((module) => module.lessons), [modules]);
  const completedLessons = useMemo(() => allLessons.filter((item) => completedLessonSlugs.includes(item.slug)), [allLessons, completedLessonSlugs]);
  const [mode, setMode] = useState<HomeworkMode>("topic");
  const [lessonSlug, setLessonSlug] = useState(completedLessons[0]?.slug ?? "");
  const sectionOptions = completedCourseSections(modules, completedLessonSlugs);
  const [sectionKey, setSectionKey] = useState(sectionOptions[0]?.key ?? "");
  const moduleOptions = completedCourseModules(modules, completedLessonSlugs);
  const [moduleSlug, setModuleSlug] = useState(moduleOptions[0]?.module.slug ?? "");
  const [items, setItems] = useState<Homework[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const { lastId, remember } = useLastCourseTask("homework", modules[0]?.level === "A2" ? "a2" : "a1");
  const handledRequest = useRef<number | null>(null);
  const [answer, setAnswer] = useState("");
  const [result, setResult] = useState<CourseHomeworkAttempt | null>(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [batchCount, setBatchCount] = useState(1);
  const [generatedCount, setGeneratedCount] = useState(0);
  const [generationNotice, setGenerationNotice] = useState("");
  const [checking, setChecking] = useState(false);
  const [hintLevel, setHintLevel] = useState(0);
  const [error, setError] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const workspaceRef = useRef<HTMLFormElement>(null);
  const lesson = completedLessons.find((item) => item.slug === lessonSlug) ?? completedLessons[0];
  const scope = buildCourseGenerationScope({ mode, modules, completedLessonSlugs, lessonSlug, sectionKey, moduleSlug });
  const storageSlug = scope.storageSlug;
  const visible = items.filter((item) => item.lesson_slug === storageSlug);
  const selected = visible.find((item) => item.id === selectedId) ?? visible[0];
  const lastTask = items.find((item) => item.id === lastId) ?? items[0];
  const selectedIndex = selected ? visible.findIndex((item) => item.id === selected.id) : -1;
  const nextHomework = selectedIndex >= 0 ? visible[selectedIndex + 1] : undefined;
  const referenceLessons = useMemo(() => {
    if (!selected) return [];
    const directLesson = completedLessons.find((item) => item.slug === selected.lesson_slug);
    const candidateLessons = directLesson
      ? [directLesson]
      : selected.lesson_slug === "course-mistakes" || selected.lesson_slug === "course:a2:mistakes"
        ? completedLessons.filter((item) => mistakeHints.some((hint) => hint.lessonSlug === item.slug))
        : selected.lesson_slug === scope.storageSlug
          ? scope.lessons
          : completedLessons;
    const ranked = rankHomeworkReferenceLessons({ title: selected.title, description: selected.description, focusCategory: selected.focus_category }, candidateLessons);
    return directLesson ? [directLesson, ...completedLessons.filter((item) => item.slug !== directLesson.slug)] : ranked;
  }, [completedLessons, mistakeHints, scope.lessons, scope.storageSlug, selected]);
  const recommendedLessons = useMemo(() => {
    if (!selected) return [];
    const directLesson = completedLessons.find((item) => item.slug === selected.lesson_slug);
    return directLesson ? [directLesson] : selectHomeworkReferenceLessons({ title: selected.title, description: selected.description, focusCategory: selected.focus_category }, referenceLessons);
  }, [completedLessons, referenceLessons, selected]);
  const hints = useMemo(() => selected ? homeworkAssignmentHints({ title: selected.title, description: selected.description, focusCategory: selected.focus_category, lessons: recommendedLessons }) : [], [recommendedLessons, selected]);
  const learnedCount = useMemo(() => learnedVocabularySeeds(allLessons, completedLessonSlugs).length, [allLessons, completedLessonSlugs]);
  const scopeLessonSlugs = new Set(scope.lessons.map((item) => item.slug));
  const relevantMistakes = mistakeHints.filter((hint) => scopeLessonSlugs.has(hint.lessonSlug));

  useEffect(() => {
    let cancelled = false;
    void getCourseHomework().then((homework) => {
      if (cancelled) return;
      const available = homework.filter((item) => isCourseGenerationScopeSlug(modules, item.lesson_slug));
      setItems(available); setSelectedId(available[0]?.id ?? null);
    }).catch((cause) => { if (!cancelled) setError(cause instanceof Error ? cause.message : "Не удалось загрузить домашние задания."); }).finally(() => { if (!cancelled) setLoading(false); });
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
  useEffect(() => { setHintLevel(0); }, [selected?.id]);

  useEffect(() => {
    if (!openRequest || handledRequest.current === openRequest.nonce) return;
    const task = items.find((item) => item.id === openRequest.id);
    if (!task) {
      if (!loading) { handledRequest.current = openRequest.nonce; setError("Исходное домашнее задание удалено или недоступно. Исправление сохранено в разделе ошибок."); }
      return;
    }
    handledRequest.current = openRequest.nonce;
    remember(task.id);
    const slug = task.lesson_slug;
    if (slug.startsWith("section:")) { setMode("section"); setSectionKey(slug.slice(8)); }
    else if (slug.startsWith("module:")) { setMode("module"); setModuleSlug(slug.slice(7)); }
    else if (slug === "course-progress" || slug === "course:a2:progress") setMode("progress");
    else if (slug === "course-mistakes" || slug === "course:a2:mistakes") setMode("mistakes");
    else { setMode("topic"); setLessonSlug(slug); }
    setSelectedId(task.id); setResult(task.latest_attempt); setAnswer("");
  }, [openRequest, items, loading]);

  const openHomework = (item: Homework) => {
    remember(item.id);
    setSelectedId(item.id);
    setResult(item.latest_attempt);
    if (selected?.id !== item.id) setAnswer("");
    requestAnimationFrame(() => workspaceRef.current?.scrollIntoView({ behavior: "smooth", block: "start" }));
  };

  const returnToLastTask = () => {
    if (!lastTask) return;
    const slug = lastTask.lesson_slug;
    if (slug.startsWith("section:")) { setMode("section"); setSectionKey(slug.slice(8)); }
    else if (slug.startsWith("module:")) { setMode("module"); setModuleSlug(slug.slice(7)); }
    else if (slug === "course-progress" || slug === "course:a2:progress") setMode("progress");
    else if (slug === "course-mistakes" || slug === "course:a2:mistakes") setMode("mistakes");
    else { setMode("topic"); setLessonSlug(slug); }
    openHomework(lastTask);
  };

  const generate = async () => {
    if (generating || learningMode === "offline") return;
    const requestedCount = Math.min(20, Math.max(1, Math.trunc(batchCount)));
    setGenerating(true); setGeneratedCount(0); setGenerationNotice(""); setError(""); setAnswer(""); setResult(null);
    try {
      if (!scope.lessons.length) return;
      const theory = buildProgressGenerationContext({ mode, selectedLesson: lesson, completedLessons, mistakeHints, scope });
      const payload = { lesson_slug: scope.storageSlug, lesson_title: scope.title, theory, known_mistakes: relevantMistakes.slice(0, 20).map((hint) => hint.text) };
      const batch = await generateSequentialBatch({ count: requestedCount, create: async (index, createdItems: readonly Homework[]) => {
        const knownIds = [...items, ...createdItems].map((item) => item.id);
        return generateCourseHomework({ ...payload, batch_index: index + 1, batch_total: requestedCount }, knownIds);
      }, onProgress: ({ attempted }) => setGeneratedCount(attempted) });
      if (batch.items.length) {
        setItems((current) => [...batch.items.slice().reverse(), ...current]);
        setSelectedId(batch.items.at(-1)!.id);
        remember(batch.items.at(-1)!.id);
      }
      setGenerationNotice(batch.failed
        ? `Сохранено домашних заданий: ${batch.created} из ${requestedCount}. Не удалось создать: ${batch.failed}.${batch.stoppedEarly ? " Генерация остановлена после трёх сбоев подряд." : ""}`
        : `Сохранено домашних заданий: ${batch.created}.`);
      if (!batch.items.length) setError("Не удалось создать домашние задания после нескольких попыток. Сохранённые ранее задания не потеряны.");
    } finally { setGenerating(false); }
  };

  const submit = async (event: FormEvent) => {
    event.preventDefault(); if (!selected || !answer.trim()) return;
    remember(selected.id);
    setChecking(true); setError("");
    try { const checked = await submitCourseHomework(selected.id, answer.trim(), learningMode, selected.latest_attempt?.id); onTaskChecked(`homework:${selected.id}`, checked.is_correct); setResult(checked); setItems((current) => current.map((item) => item.id === selected.id ? { ...item, latest_attempt: checked } : item)); setAnswer(""); }
    catch (cause) { setError(cause instanceof Error ? cause.message : "Не удалось проверить домашнее задание."); }
    finally { setChecking(false); }
  };

  const insertKey = (key: string) => { const field = textareaRef.current; if (!field) return; const start = field.selectionStart ?? answer.length; const end = field.selectionEnd ?? start; setAnswer(`${answer.slice(0, start)}${key}${answer.slice(end)}`); requestAnimationFrame(() => { field.focus(); field.setSelectionRange(start + key.length, start + key.length); }); };
  const handleAltShortcut = (event: KeyboardEvent<HTMLTextAreaElement>) => { if (!event.altKey || event.ctrlKey || event.metaKey) return; const field = textareaRef.current; const inserted = applySlovakAltShortcut(answer, event.code, event.shiftKey, field?.selectionStart ?? answer.length, field?.selectionEnd ?? answer.length); if (!inserted) return; event.preventDefault(); setAnswer(inserted.value); requestAnimationFrame(() => { field?.focus(); field?.setSelectionRange(inserted.caret, inserted.caret); }); };
  const remove = async (item: Homework) => { if (!window.confirm(`Удалить задание «${item.title}» вместе с ответами?`)) return; setError(""); try { await deleteCourseHomework(item.id); setItems((current) => current.filter((entry) => entry.id !== item.id)); if (selectedId === item.id) { setSelectedId(null); setResult(null); setAnswer(""); } } catch (cause) { setError(cause instanceof Error ? cause.message : "Не удалось удалить задание."); } };
  const checked = result ?? selected?.latest_attempt;

  return <section className="course-exercises course-homework" aria-labelledby="course-homework-title" data-report-task-type="homework" data-report-task-id={selected?.id} data-report-task-title={selected ? selected.title : undefined} data-report-scope={scope.title}>
    <div className="course-section-heading"><div><span>Самостоятельная практика по прогрессу</span><h3 id="course-homework-title">Домашнее задание</h3></div><div className={`course-learning-mode ${learningMode}`}><strong>{learningMode === "online" ? "Онлайн" : "Офлайн"}</strong><p>{learningMode === "online" ? "ИИ создаёт задания и гибко проверяет ответы." : "Сохранённые задания проверяются по эталону без обращения к ИИ."}</p></div></div>
    <div className="course-task-navigation">
    <div className="course-reading-modes" role="group" aria-label="Режим генерации домашнего задания">{([['topic', 'По теме'], ['section', 'По разделу'], ['module', 'По модулю'], ['progress', 'По общему прогрессу']] as const).map(([value, label]) => <button key={value} type="button" disabled={generating} className={mode === value ? "active" : ""} onClick={() => { setMode(value); setSelectedId(null); setResult(null); setAnswer(""); }}>{label}</button>)}</div>
    <button type="button" className="course-task-return" onClick={returnToLastTask} disabled={loading || generating || checking || !lastTask}>Вернуться к последнему заданию</button>
    </div>
    <div className="course-exercise-toolbar">{mode === "topic" ? <div className="course-generation-selectors"><label><span>Завершённая тема</span><select value={lessonSlug} disabled={!completedLessons.length || generating} onChange={(event) => { setLessonSlug(event.target.value); setSelectedId(null); setResult(null); setAnswer(""); }}>{completedLessons.map((item) => <option value={item.slug} key={item.slug}>{item.title}</option>)}</select></label><small>{learnedCount} открытых слов и фраз · {relevantMistakes.length} активных ошибок в выбранной теме</small></div> : mode === "section" ? <div className="course-generation-selectors"><label><span>Учебный раздел</span><select value={sectionOptions.find(({ key }) => key === sectionKey)?.key ?? ""} disabled={!sectionOptions.length || generating} onChange={(event) => { setSectionKey(event.target.value); setSelectedId(null); setResult(null); setAnswer(""); }}>{sectionOptions.map(({ key, module, section, lessons }) => <option key={key} value={key}>Модуль {module.order} · {section.title} · {lessons.length} тем</option>)}</select></label><small>{scope.lessons.length} завершённых тем · {relevantMistakes.length} активных ошибок в разделе</small></div> : mode === "module" ? <div className="course-generation-selectors"><label><span>Модуль с завершёнными темами</span><select value={scope.module?.slug ?? ""} disabled={!moduleOptions.length || generating} onChange={(event) => { setModuleSlug(event.target.value); setSelectedId(null); setResult(null); setAnswer(""); }}>{moduleOptions.map(({ module, lessons }) => <option key={module.slug} value={module.slug}>Модуль {module.order}. {module.title} · {lessons.length} тем</option>)}</select></label><small>{scope.lessons.length} завершённых тем · {relevantMistakes.length} активных ошибок в модуле</small></div> : <div className="course-reading-scope"><span>{mode === "mistakes" ? "Фокус задания" : "Доступный материал"}</span><strong>{mode === "mistakes" ? `${relevantMistakes.length} активных ошибок из завершённых тем` : `${completedLessons.length} завершённых тем · ${learnedCount} слов и фраз`}</strong><small>{mode === "mistakes" ? "Три шага: вспомнить правило, применить его и написать свою фразу." : relevantMistakes.length ? `Учитывается активных ошибок: ${relevantMistakes.length}.` : "Активных ошибок в пройденном материале нет."}</small></div>}<div className="course-exercise-create"><label className="course-exercise-count"><span>Количество заданий</span><input type="number" min={1} max={20} step={1} value={batchCount} disabled={generating || learningMode === "offline"} onChange={(event) => setBatchCount(Math.min(20, Math.max(1, Math.trunc(Number(event.target.value) || 1))))} /></label><button type="button" onClick={() => void generate()} disabled={generating || !scope.lessons.length || learningMode === "offline" || (mode === "mistakes" && !relevantMistakes.length)}>{generating ? `Создаю ${generatedCount}/${batchCount}…` : batchCount === 1 ? "Создать задание" : `Создать ${batchCount} ${homeworkNoun(batchCount)}`}</button>{learningMode === "offline" && <small>Новые задания создаются только онлайн.</small>}</div></div>
    {mode === "mistakes" && !relevantMistakes.length && <p className="course-empty">Активных ошибок нет — выберите домашнее задание по теме или по общему прогрессу.</p>}
    {!completedLessons.length && <p className="course-empty">Завершите хотя бы одну тему, чтобы создавать домашние задания.</p>}
    {generationNotice && <p className="course-generation-notice" role="status">{generationNotice}</p>}
    {error && <p className="course-persistence-error" role="alert">{error}</p>}
    {loading ? <p>Загружаю задания…</p> : <div className="course-exercise-grid"><aside className="course-exercise-list"><strong>Сохранённые задания</strong>{visible.length ? visible.map((item) => <article className={selected?.id === item.id ? "active" : ""} key={item.id}><button type="button" onClick={() => openHomework(item)}><span>{item.lesson_title}</span><b>{item.title}</b><small>{item.latest_attempt ? `Результат: ${item.latest_attempt.score}/100` : item.focus_category}</small></button><button type="button" className="delete" onClick={() => void remove(item)} aria-label={`Удалить задание: ${item.title}`}>Удалить</button></article>) : <p>По этой теме заданий пока нет.</p>}</aside><form ref={workspaceRef} className="course-exercise-workspace" onSubmit={(event) => void submit(event)}>{selected ? <><span>{selected.lesson_title} · {selected.focus_category}</span><h4>{selected.title}</h4><p className="course-homework-description">{selected.description}</p><div className="course-homework-help"><button type="button" onClick={() => setHintLevel((current) => current >= hints.length ? 0 : current + 1)} aria-expanded={hintLevel > 0} aria-controls="course-homework-hints">{hintLevel === 0 ? "Подсказка по этому заданию" : hintLevel < hints.length ? "Ещё подходящая тема" : "Скрыть подсказку"}</button>{hintLevel > 0 && <div id="course-homework-hints" className="course-homework-hints" role="status" aria-live="polite"><strong>Подсказка к заданию «{selected.title}»:</strong><ol>{hints.slice(0, hintLevel).map((hint) => <li key={hint}>{hint}</li>)}</ol><small>Правила и примеры взяты из подходящих завершённых тем; готовый ответ не показывается.</small></div>}</div><CourseHomeworkReference lessons={referenceLessons} personalCheatSheets={personalCheatSheets} preferredLessonSlug={selected.lesson_slug} recommendedLessonSlugs={recommendedLessons.map((item) => item.slug)} /><textarea ref={textareaRef} rows={7} value={answer} onChange={(event) => setAnswer(event.target.value)} onKeyDown={handleAltShortcut} placeholder="Напишите ответ по-словацки…" disabled={checking} /><SlovakKeyboard onInsert={insertKey} disabled={checking} /><button type="submit" disabled={!answer.trim() || checking || (learningMode === "offline" && !selected.offline_ready)}>{checking ? "Проверяю…" : learningMode === "offline" ? "Проверить офлайн" : checked && !checked.is_correct ? "Отправить исправление" : "Отправить на проверку"}</button>{learningMode === "offline" && !selected.offline_ready && <small>У старого задания нет эталона. Для него нужна онлайн-проверка.</small>}{checked && <><article className={checked.is_correct ? "correct" : "incorrect"}><strong>{checked.is_correct ? "Выполнено правильно" : "Нужно исправить"} · {checked.score}/100</strong><p><b>Ваш ответ:</b> {checked.answer}</p><p><b>Исправленный вариант:</b> {checked.corrected_answer}</p><p><b>Объяснение:</b> {checked.explanation}</p><p><b>Что повторить:</b> {checked.next_exercise}</p></article>{!checked.is_correct && <CourseTaskMistakeButton mistake={{ id: `homework:${selected.id}`, lessonSlug: selected.lesson_slug, prompt: `${selected.lesson_title} · ${selected.title}\n${selected.description}\nВаш ответ: ${checked.answer}\n${checked.explanation}`.slice(0, 2000), answer: checked.corrected_answer, reviewTask: { prompt: selected.description, learnerAnswer: checked.answer.slice(0, 4000), explanation: checked.explanation, kind: "open" } }} recorded={recordedMistakeIds.includes(`homework:${selected.id}`)} disabled={mistakesDisabled} onRecord={onRecordMistake} />}<button type="button" className="course-task-next" disabled={!nextHomework} onClick={() => nextHomework && openHomework(nextHomework)}>{nextHomework ? "Следующее задание →" : "Это последнее задание"}</button></>}</> : <div className="course-empty"><strong>Выберите или создайте задание</strong><p>Оно сохранится в базе данных.</p></div>}</form></div>}
  </section>;
}
