"use client";

import { useMemo } from "react";

import { buildReinforcementPractices, isCorePractice } from "../data/coursePractice";
import { buildPersonalCourseStats } from "../data/courseStats";
import { type CourseLesson, type CourseModule } from "../data/courseTypes";
import { type LessonSummary, type MistakeRecord, type ProgressMap } from "../hooks/useCourseSession";
import { courseStatusLabels } from "./CourseMaterialView";

export type CourseStatsPanelProps = {
  modules: CourseModule[];
  module: CourseModule;
  lessons: CourseLesson[];
  progress: ProgressMap;
  practiceResults: Record<string, boolean>;
  checkSelections: Record<string, string>;
  mistakes: Record<string, MistakeRecord>;
  summaries: Record<string, LessonSummary>;
  completedCount: number;
  accuracy: number;
  correctPracticeCount: number;
  totalPracticeCount: number;
  dueCount: number;
  back: () => void;
  reset: () => void;
};

export function CourseStatsPanel({ modules, module, lessons, progress, practiceResults, checkSelections, mistakes, summaries, completedCount, accuracy, correctPracticeCount, totalPracticeCount, dueCount, back, reset }: CourseStatsPanelProps) {
  const personalStats = useMemo(
    () => buildPersonalCourseStats({ modules, progress, practiceResults, checkSelections, mistakes, summaries }),
    [modules, progress, practiceResults, checkSelections, mistakes, summaries],
  );

  return <section className="course-stats"><div className="course-section-heading"><div><span>Личная статистика · весь курс</span><h3>Мой прогресс</h3></div><p>Расчёт по вашим сохранённым ответам, словам и исправлениям.</p></div>
    <div className="course-personal-stat-grid" aria-label="Личная статистика по всему курсу">
      <article><strong>{personalStats.completedLessons}/{personalStats.totalLessons}</strong><span>тем завершено</span><small>{personalStats.completionPercent}% курса</small></article>
      <article><strong>{personalStats.accuracy}%</strong><span>общая точность</span><small>с учётом повторных ошибок</small></article>
      <article><strong>{personalStats.vocabularyCount}</strong><span>слов и фраз открыто</span><small>из завершённых тем</small></article>
      <article><strong>{personalStats.averageUnderstanding ?? "—"}{personalStats.averageUnderstanding === null ? "" : "%"}</strong><span>среднее понимание</span><small>по завершённым темам</small></article>
    </div>
    <article className="course-personal-next"><span>Ваш следующий шаг</span><strong>{personalStats.nextAction}</strong><small>Активных ошибок: {personalStats.activeMistakes} · закреплено: {personalStats.masteredMistakes} · повторить сейчас: {personalStats.dueMistakes}</small></article>
    <section className="course-module-stats" aria-labelledby="course-module-stats-title"><div><h4 id="course-module-stats-title">Прогресс по модулям</h4><span>Видно, где вы продвинулись дальше и где осталось больше практики.</span></div><div>{personalStats.moduleStats.map((item) => <article key={item.order}><header><b>Module {item.order}</b><span>{item.completed}/{item.lessons} тем</span></header><strong>{item.title}</strong><div><i style={{ width: `${item.lessons ? item.completed / item.lessons * 100 : 0}%` }} /></div><small>{item.solved}/{item.activities} заданий · точность {item.accuracy}%</small></article>)}</div></section>
    <section className="course-current-module-stats" aria-labelledby="course-current-module-stats-title"><div><span>Выбранный модуль</span><h4 id="course-current-module-stats-title">{module.title}</h4></div><div className="course-stat-grid"><article><strong>{completedCount}/{module.lessons.length}</strong><span>тем завершено</span></article><article><strong>{accuracy}%</strong><span>точность обязательных ответов</span></article><article><strong>{correctPracticeCount}/{totalPracticeCount}</strong><span>обязательных заданий решено</span></article><article><strong>{dueCount}</strong><span>повторений сейчас</span></article></div></section>
    <div className="course-topic-stats">{lessons.map((lesson, index) => { const corePractices = lesson.stepPractices.filter((practice) => isCorePractice(lesson, practice)); const assessmentPractices = lesson.assessmentMode === "interactive" ? buildReinforcementPractices(lesson) : []; const checks = lesson.assessmentMode === "interactive" ? [] : lesson.knowledgeChecks; const solved = corePractices.filter((practice) => practiceResults[practice.id]).length + assessmentPractices.filter((practice) => practiceResults[practice.id]).length + checks.filter((check) => checkSelections[check.id] === check.answer).length; const total = corePractices.length + assessmentPractices.length + checks.length; const summary = summaries[lesson.slug]; return <article key={lesson.slug}><div><b>{index + 1}. {lesson.title}</b><span>{courseStatusLabels[progress[lesson.slug] ?? "not_started"]}</span></div><div><i style={{ width: `${total ? solved / total * 100 : 0}%` }} /></div><small>{solved}/{total} обязательных заданий{summary ? ` · понимание ${summary.understanding}%` : ""}</small></article>; })}</div><div className="course-actions"><button type="button" className="secondary" onClick={back}>← К темам</button><button type="button" className="course-danger" onClick={reset}>Сбросить прогресс модуля</button></div></section>;
}
