"use client";

import { useEffect, useState } from "react";

import {
  deleteAllCourseTasks,
  deleteCourseExercise,
  deleteCourseHomework,
  deleteCourseReading,
  getCourseExercises,
  getCourseHomework,
  getCourseReadings,
  type CourseExercise,
  type CourseHomework,
  type CourseReading,
} from "../lib/api";
import { CourseMaterialTransfer } from "./CourseMaterialTransfer";


export function CourseTasksManager({ onChanged }: { onChanged: () => void }) {
  const [exercises, setExercises] = useState<CourseExercise[]>([]);
  const [readings, setReadings] = useState<CourseReading[]>([]);
  const [homework, setHomework] = useState<CourseHomework[]>([]);
  const [loading, setLoading] = useState(true);
  const [deletingAll, setDeletingAll] = useState(false);
  const [confirmingDeleteAll, setConfirmingDeleteAll] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");

  const load = async () => {
    setLoading(true); setError("");
    try {
      const [nextExercises, nextReadings, nextHomework] = await Promise.all([
        getCourseExercises(), getCourseReadings(), getCourseHomework(),
      ]);
      setExercises(nextExercises); setReadings(nextReadings); setHomework(nextHomework);
    } catch (cause) { setError(cause instanceof Error ? cause.message : "Не удалось загрузить задания."); }
    finally { setLoading(false); }
  };

  useEffect(() => { void load(); }, []);

  const remove = async (kind: "exercise" | "reading" | "homework", id: number, title: string) => {
    if (!window.confirm(`Удалить «${title}» вместе с сохранёнными ответами?`)) return;
    setError("");
    try {
      if (kind === "exercise") { await deleteCourseExercise(id); setExercises((items) => items.filter((item) => item.id !== id)); }
      if (kind === "reading") { await deleteCourseReading(id); setReadings((items) => items.filter((item) => item.id !== id)); }
      if (kind === "homework") { await deleteCourseHomework(id); setHomework((items) => items.filter((item) => item.id !== id)); }
      onChanged();
    } catch (cause) { setError(cause instanceof Error ? cause.message : "Не удалось удалить задание."); }
  };

  const removeAll = async () => {
    setDeletingAll(true); setError(""); setNotice("");
    try {
      const result = await deleteAllCourseTasks();
      const deleted = result.exercises_deleted + result.readings_deleted + result.homework_deleted;
      setExercises([]); setReadings([]); setHomework([]); setConfirmingDeleteAll(false);
      setNotice(`Удалено заданий: ${deleted}. Сохранённый прогресс курса и словарь не изменены.`);
      onChanged();
    } catch (cause) { setError(cause instanceof Error ? cause.message : "Не удалось удалить все задания."); }
    finally { setDeletingAll(false); }
  };

  const total = exercises.length + readings.length + homework.length;
  return <div className="course-task-manager">
    <p>Все созданные упражнения, тексты и домашние задания хранятся в SQLite. Здесь их можно перенести одним файлом или удалить вместе с ответами.</p>
    <CourseMaterialTransfer onImported={async () => { await load(); onChanged(); }} />
    {error && <p className="course-persistence-error" role="alert">{error}</p>}
    {notice && <p className="course-persistence-success" role="status">{notice}</p>}
    {loading ? <p role="status">Загружаю задания…</p> : <>
      <div className="course-task-summary"><strong>Всего: {total}</strong><span>Упражнения: {exercises.length}</span><span>Чтение: {readings.length}</span><span>Домашние: {homework.length}</span></div>
      <div className="course-task-delete-all">
        {!confirmingDeleteAll ? <button type="button" disabled={!total || deletingAll} onClick={() => { setConfirmingDeleteAll(true); setNotice(""); }}>Удалить все задания</button> : <div role="alert"><strong>Удалить все {total} заданий?</strong><p>Будут безвозвратно удалены упражнения, тексты для чтения, домашние задания и все ответы на них. Прогресс курса и словарь останутся.</p><div><button type="button" disabled={deletingAll} onClick={() => void removeAll()}>{deletingAll ? "Удаляю…" : "Да, удалить всё"}</button><button type="button" disabled={deletingAll} onClick={() => setConfirmingDeleteAll(false)}>Отмена</button></div></div>}
      </div>
      <div className="course-task-groups">
        <section><h4>Упражнения</h4>{exercises.length ? exercises.map((item) => <article key={item.id}><div><span>{item.lesson_title}</span><strong>{item.question}</strong></div><button type="button" onClick={() => void remove("exercise", item.id, item.question)}>Удалить</button></article>) : <p>Нет сохранённых упражнений.</p>}</section>
        <section><h4>Чтение</h4>{readings.length ? readings.map((item) => <article key={item.id}><div><span>{item.lesson_title}</span><strong>{item.title}</strong><small>{item.offline_ready ? "Можно проверять офлайн" : "Только онлайн-проверка"}</small></div><button type="button" onClick={() => void remove("reading", item.id, item.title)}>Удалить</button></article>) : <p>Нет сохранённых текстов.</p>}</section>
        <section><h4>Домашние задания</h4>{homework.length ? homework.map((item) => <article key={item.id}><div><span>{item.lesson_title}</span><strong>{item.title}</strong><small>{item.offline_ready ? "Можно проверять офлайн" : "Только онлайн-проверка"}</small></div><button type="button" onClick={() => void remove("homework", item.id, item.title)}>Удалить</button></article>) : <p>Нет сохранённых домашних заданий.</p>}</section>
      </div>
    </>}
  </div>;
}
