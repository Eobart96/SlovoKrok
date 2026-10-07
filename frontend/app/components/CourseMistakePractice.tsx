"use client";

import { useRef, useState } from "react";
import type { MistakeRecord } from "../data/courseProgress";
import type { CourseModule } from "../data/courseTypes";
import type { LearningMode } from "../data/learningMode";
import { buildReinforcementPractices } from "../data/coursePractice";
import { taskMistakeSource } from "../data/taskMistakes";
import { checkCourseMistake, type MistakeReviewAssessment } from "../lib/api";
import { SlovakKeyboard } from "./SlovakKeyboard";
import { applySlovakAltShortcut } from "../data/slovakKeyboard";

function reviewTask(mistake: MistakeRecord, modules: CourseModule[]) {
  if (mistake.reviewTask) return { ...mistake.reviewTask, acceptedAnswers: [] as string[] };
  const lesson = modules.flatMap((module) => module.lessons).find((item) => item.slug === mistake.lessonSlug);
  const practice = lesson && [...lesson.stepPractices, ...buildReinforcementPractices(lesson)].find((item) => item.id === mistake.id);
  const check = lesson && [...lesson.knowledgeChecks, ...lesson.finalChecks].find((item) => item.id === mistake.id);
  // Older manual records put the answer and explanation after this marker.
  const [prompt, previous = ""] = mistake.prompt.split("\nВаш ответ:");
  return { prompt, learnerAnswer: previous.split("\n")[0].trim(), explanation: practice?.explanation || check?.explanation || lesson?.theory.summary || "Сравните свой вариант с исправлением и обратите внимание на форму слов.", acceptedAnswers: practice?.acceptableAnswers ?? [], kind: taskMistakeSource(mistake.id)?.kind === "homework" ? "open" as const : "exact" as const };
}

export function CourseMistakePractice({ mistakes, modules, learningMode, disabled, onChecked, onActiveChange }: { mistakes: Record<string, MistakeRecord>; modules: CourseModule[]; learningMode: LearningMode; disabled: boolean; onChecked: (id: string, correct: boolean, independent?: boolean) => void; onActiveChange: (active: boolean) => void }) {
  const [queue, setQueue] = useState<string[]>([]);
  const [index, setIndex] = useState(0);
  const [stage, setStage] = useState<"understand" | "practice" | "result">("understand");
  const [answer, setAnswer] = useState("");
  const [result, setResult] = useState<MistakeReviewAssessment | null>(null);
  const [checking, setChecking] = useState(false);
  const [error, setError] = useState("");
  const field = useRef<HTMLTextAreaElement>(null);
  const busy = useRef(false);
  const hintShown = useRef(false);
  const current = mistakes[queue[index]];
  const task = current ? reviewTask(current, modules) : null;
  const active = Object.values(mistakes).filter((item) => !item.mastered);
  const isDue = (item: MistakeRecord) => !item.dueAt || Date.parse(item.dueAt) <= Date.now();
  const resetStep = (item?: MistakeRecord) => {
    hintShown.current = false;
    setAnswer(""); setResult(null); setError("");
    setStage(item && (item.reviewStage ?? 0) > 0 && isDue(item) ? "practice" : "understand");
  };
  const start = () => {
    const selected = [...active].sort((a, b) => Number(isDue(b)) - Number(isDue(a)) || b.attempts - a.attempts).slice(0, 5);
    setQueue(selected.map((item) => item.id)); setIndex(0); resetStep(selected[0]);
    onActiveChange(true);
  };
  const stop = () => { setQueue([]); onActiveChange(false); };
  const submit = async () => {
    if (!current || !task || !answer.trim() || disabled || busy.current) return;
    busy.current = true; setChecking(true); setError("");
    try {
      const source = taskMistakeSource(current.id);
      const assessment = await checkCourseMistake({ prompt: task.prompt, expected_answer: current.answer, accepted_answers: task.acceptedAnswers, answer: answer.trim(), kind: task.kind, source_exercise_id: source?.kind === "exercise" ? source.id : undefined, assessment_mode: learningMode });
      onChecked(current.id, assessment.is_correct, !hintShown.current); setResult(assessment); setStage("result");
    } catch (cause) { setError(cause instanceof Error ? cause.message : "Не удалось проверить ответ. Ваш ответ сохранён на экране."); }
    finally { busy.current = false; setChecking(false); }
  };
  const insert = (text: string) => {
    const start = field.current?.selectionStart ?? answer.length;
    const end = field.current?.selectionEnd ?? start;
    setAnswer(answer.slice(0, start) + text + answer.slice(end));
    requestAnimationFrame(() => { field.current?.focus(); field.current?.setSelectionRange(start + text.length, start + text.length); });
  };
  if (!queue.length) return <section className="course-mistake-practice" data-report-task-type="mistake" data-report-task-id={current?.id} data-report-stage={stage}><h3>Работа над ошибками</h3><p>Короткая тренировка: разобрать ошибку, ответить без подсказки и повторить по расписанию. До пяти заданий за один подход.</p><button type="button" onClick={start} disabled={disabled || !active.length}>Начать работу над ошибками</button>{!active.length && <p>Активных ошибок нет.</p>}</section>;
  if (index >= queue.length) return <section className="course-mistake-practice" role="status"><h3>Тренировка завершена</h3><p>Вы проработали {queue.length} ошибок. Следующие повторения появятся по расписанию.</p><button type="button" onClick={stop}>К списку ошибок</button></section>;
  if (!current || !task) return <section className="course-mistake-practice" data-report-task-type="mistake" data-report-task-id={current?.id} data-report-stage={stage}><p>Эта ошибка уже удалена.</p><button type="button" onClick={() => { const next = index + 1; setIndex(next); resetStep(mistakes[queue[next]]); }}>Продолжить</button></section>;
  return <section className="course-mistake-practice" data-report-task-type="mistake" data-report-task-id={current?.id} data-report-stage={stage}>
    <div className="course-section-heading"><div><span>Ошибка {index + 1} из {queue.length}</span><h3>{stage === "understand" ? "1. Разобраться" : stage === "practice" ? "2. Попробовать снова" : "3. Закрепить"}</h3></div><button type="button" disabled={checking} onClick={stop}>К списку ошибок</button></div>
    <p style={{ whiteSpace: "pre-wrap" }}>{task.prompt}</p>
    {stage === "understand" && <><article className="course-mistake-explanation">{task.learnerAnswer && <p><b>Ваш прежний ответ:</b> {task.learnerAnswer}</p>}<p><b>Правильный вариант:</b> {current.answer}</p><p>{task.explanation}</p></article><button type="button" disabled={disabled} onClick={() => { setStage("practice"); setAnswer(""); }}>Попробовать без подсказки →</button></>}
    {stage === "practice" && <form onSubmit={(event) => { event.preventDefault(); void submit(); }}><label htmlFor="mistake-review-answer">Ваш новый ответ</label><textarea id="mistake-review-answer" ref={field} rows={4} value={answer} disabled={checking || disabled} onChange={(event) => setAnswer(event.target.value)} onKeyDown={(event) => { if (!event.altKey || event.ctrlKey || event.metaKey) return; const changed = applySlovakAltShortcut(answer, event.code, event.shiftKey, event.currentTarget.selectionStart, event.currentTarget.selectionEnd); if (changed) { event.preventDefault(); setAnswer(changed.value); requestAnimationFrame(() => { field.current?.focus(); field.current?.setSelectionRange(changed.caret, changed.caret); }); } }} /><SlovakKeyboard onInsert={insert} disabled={checking || disabled} />{task.kind === "open" && learningMode === "offline" && <p>Офлайн сравнивается сохранённый образец. Для проверки других правильных формулировок нужен онлайн-режим.</p>}<button type="submit" disabled={checking || disabled || !answer.trim()}>{checking ? "Проверяю…" : "Проверить ответ"}</button><button type="button" disabled={checking} onClick={() => { hintShown.current = true; setStage("understand"); }}>Разобрать ещё раз</button></form>}
    {error && <p role="alert" className="course-persistence-error">{error}</p>}
    {stage === "result" && result && <div role="status"><h4>{result.is_correct ? "Правильно" : "Нужно исправить"} · {result.score}/100</h4><p>{result.explanation}</p>{!result.is_correct && <p><b>Исправленный вариант:</b> {result.corrected_answer}</p>}{result.is_correct ? <><p>{hintShown.current && (current.reviewStage ?? 0) > 0 ? "Ответ выполнен с подсказкой. Для закрепления нужно повторить без неё; срок не изменён." : current.mastered ? "Ошибка закреплена." : `Повторите ${current.dueAt ? new Date(current.dueAt).toLocaleDateString("ru-RU") : "через 3 дня"}. Раннее повторение не меняет срок закрепления.`}</p><button type="button" onClick={() => { const next = index + 1; setIndex(next); resetStep(mistakes[queue[next]]); }}>{index + 1 === queue.length ? "Завершить тренировку" : "Следующая ошибка →"}</button></> : <><button type="button" onClick={() => { hintShown.current = true; setStage("understand"); setResult(null); }}>Разобраться ещё раз</button><button type="button" onClick={() => { setStage("practice"); setResult(null); setAnswer(""); }}>Попробовать снова</button></>}</div>}
  </section>;
}
