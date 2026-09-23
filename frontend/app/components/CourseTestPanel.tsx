"use client";

import { useEffect, useState } from "react";
import { type CourseLesson } from "../data/courseTypes";
import { type CourseSession, type ProgressMap } from "../hooks/useCourseSession";
import { deleteAllCourseExercises } from "../lib/api";
import { courseStatusLabels } from "./CourseMaterialView";
import { CourseTranslationHistory } from "./CourseTranslationHistory";

export function CourseTestPanel({ session, lessons, lesson, openLesson, openStep, openFinal, resetLesson, resetModule, onExercisesDeleted, open, onOpenChange }: {
  session: CourseSession; lessons: CourseLesson[]; lesson: CourseLesson;
  openLesson: (lesson: CourseLesson) => void; openStep: (step: number) => void;
  openFinal: () => void; resetLesson: () => boolean; resetModule: () => boolean;
  onExercisesDeleted: () => void;
  open?: boolean; onOpenChange?: (open: boolean) => void;
}) {
  const [undo, setUndo] = useState<ProgressMap | null>(null);
  const [message, setMessage] = useState("");
  const [deletingExercises, setDeletingExercises] = useState(false);
  useEffect(() => { if (session.readOnly) { setUndo(null); setMessage(""); } }, [session.readOnly]);
  const complete = (targets: CourseLesson[]) => {
    if (session.readOnly) return;
    setUndo(Object.fromEntries(targets.map((target) => [target.slug, session.progress[target.slug] ?? "not_started"])));
    session.setProgress((current) => ({ ...current, ...Object.fromEntries(targets.map((target) => [target.slug, "completed" as const])) }));
    setMessage(`Отмечено завершёнными тем: ${targets.length}. Ответы и оценки не изменены.`);
  };
  const removeAllExercises = async () => {
    if (!window.confirm("Удалить все сохранённые упражнения и всю историю ответов? Темы, общий прогресс, домашние задания и словарь останутся без изменений.")) return;
    setDeletingExercises(true);
    setMessage("");
    try {
      const result = await deleteAllCourseExercises();
      onExercisesDeleted();
      setMessage(`Удалено упражнений: ${result.exercises_deleted}. История их ответов также удалена.`);
    } catch (cause) {
      setMessage(cause instanceof Error ? cause.message : "Не удалось удалить упражнения.");
    } finally {
      setDeletingExercises(false);
    }
  };
  return <details className="course-test-panel" open={open} onToggle={(event) => onOpenChange?.(event.currentTarget.open)}>
    <summary>Инструменты разработки</summary>
    <div className="course-test-grid course-test-grid-development">
      <fieldset>
        <legend>Переходы и прогресс</legend>
        <p>Для проверки курса вручную. Пропуск отмечает темы завершёнными и сохраняется в вашем прогрессе. Перед большой проверкой можно скачать резервную копию выше.</p>
        <label>Тема для проверки
          <select aria-label="Тема для проверки" value={lesson.slug} onChange={(event) => { const target = lessons.find((item) => item.slug === event.target.value); if (target) openLesson(target); }}>
            {lessons.map((item, index) => <option key={item.slug} value={item.slug}>{index + 1}. {item.title}</option>)}
          </select>
        </label>
        <p>Статус: {courseStatusLabels[session.progress[lesson.slug] ?? "not_started"]}</p>
        <label>Шаг темы
          <select aria-label="Шаг темы" value={Math.min(session.lessonSteps[lesson.slug] ?? 0, lesson.sections.length - (lesson.materialAssessmentStep === false ? 1 : 0))} onChange={(event) => openStep(Number(event.target.value))}>
            {lesson.sections.map((section, index) => <option key={index} value={index}>{index + 1}. {section.title}</option>)}
            {lesson.materialAssessmentStep !== false && <option value={lesson.sections.length}>Тест темы</option>}
          </select>
        </label>
        <div className="course-test-actions">
          <button className="course-test-open" type="button" onClick={() => openLesson(lesson)}>Посмотреть выбранный шаг</button>
          <button className="course-test-open" type="button" onClick={openFinal}>Открыть итоговый тест без прохождения тем</button>
          <button className="course-test-complete" type="button" onClick={() => { complete([lesson]); const next = lessons[lessons.indexOf(lesson) + 1]; if (next) openLesson(next); }}>Пропустить тему и перейти дальше</button>
          <button className="course-test-complete" type="button" onClick={() => complete(lessons)}>Отметить весь модуль завершённым</button>
          <button className="course-test-undo" type="button" disabled={!undo} onClick={() => { if (undo) session.setProgress((current) => ({ ...current, ...undo })); setUndo(null); setMessage("Последняя отметка завершения отменена."); }}>Отменить последнюю отметку</button>
          <button className="course-test-reset" type="button" onClick={() => { if (resetLesson()) { setUndo(null); setMessage("Прогресс выбранной темы сброшен."); } }}>Сбросить выбранную тему</button>
          <button className="course-test-reset" type="button" onClick={() => { if (resetModule()) { setUndo(null); setMessage("Прогресс выбранного модуля сброшен."); } }}>Сбросить выбранный модуль</button>
        </div>
        {message && <p role="status">{message}</p>}
      </fieldset>
      <fieldset>
        <legend>Сохранённые упражнения</legend>
        <p>Удаляет все сгенерированные упражнения и историю ответов к ним. Прогресс тем, чтение, слова и домашние задания не изменяются.</p>
        <div className="course-test-actions">
          <button className="course-test-reset" type="button" disabled={deletingExercises} onClick={() => void removeAllExercises()}>{deletingExercises ? "Удаляю упражнения…" : "Удалить все упражнения"}</button>
        </div>
      </fieldset>
      <CourseTranslationHistory />
    </div>
  </details>;
}
