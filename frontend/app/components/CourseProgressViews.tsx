"use client";

import { useState } from "react";
import type { LearningMode } from "../data/learningMode";
import { CourseMistakePractice } from "./CourseMistakePractice";

import { buildReinforcementPractices, type ModuleFinalQuestion } from "../data/coursePractice";
import { type CourseLesson, type CourseModule } from "../data/courseTypes";
import { type MistakeRecord } from "../hooks/useCourseSession";
import { taskMistakeKind, taskMistakeSource } from "../data/taskMistakes";

export type CourseReviewViewModel = { mistakes: Record<string, MistakeRecord>; modules: CourseModule[] };
export type CourseReviewActions = { openMistake: (module: CourseModule, lesson: CourseLesson, mistake: MistakeRecord) => void; openTask: (id: string) => void; openTheory: (module: CourseModule, lesson: CourseLesson) => void; back: () => void };

export function CourseReviewView({ model: { mistakes, modules }, actions, learningMode, disabled, onChecked }: { model: CourseReviewViewModel; actions: CourseReviewActions; learningMode: LearningMode; disabled: boolean; onChecked: (id: string, correct: boolean, independent?: boolean) => void }) {
  const [trainingActive, setTrainingActive] = useState(false);
  const taskMistakes = Object.values(mistakes).filter((mistake) => taskMistakeKind(mistake.id));
  const activeTaskMistakes = taskMistakes.filter((mistake) => !mistake.mastered);
  const lessonLocations = new Map(modules.flatMap((module) => module.lessons.map((lesson) => [lesson.slug, { module, lesson }] as const)));
  const allMistakes = Object.values(mistakes).flatMap((mistake) => {
    if (taskMistakeKind(mistake.id)) return [];
    const location = lessonLocations.get(mistake.lessonSlug);
    return location ? [{ mistake, ...location }] : [];
  });
  const activeMistakes = allMistakes.filter(({ mistake }) => !mistake.mastered);
  const masteredMistakes = allMistakes.filter(({ mistake }) => mistake.mastered);
  const isDue = (mistake: MistakeRecord) => !mistake.dueAt || new Date(mistake.dueAt).getTime() <= Date.now();
  const dueCount = activeMistakes.filter(({ mistake }) => isDue(mistake)).length + activeTaskMistakes.filter(isDue).length;
  const repeatedCount = activeMistakes.filter(({ mistake }) => mistake.attempts > 1).length + activeTaskMistakes.filter((mistake) => mistake.attempts > 1).length;
  const gaps = [...activeMistakes.reduce((byLesson, item) => {
    const current = byLesson.get(item.lesson.slug) ?? { module: item.module, lesson: item.lesson, mistakes: 0, attempts: 0, due: 0 };
    current.mistakes += 1;
    current.attempts += item.mistake.attempts;
    current.due += isDue(item.mistake) ? 1 : 0;
    byLesson.set(item.lesson.slug, current);
    return byLesson;
  }, new Map<string, { module: CourseModule; lesson: CourseLesson; mistakes: number; attempts: number; due: number }>()).values()]
    .sort((left, right) => Number(right.due > 0) - Number(left.due > 0) || right.attempts - left.attempts || right.mistakes - left.mistakes || left.module.order - right.module.order);
  const sortedActiveMistakes = [...activeMistakes].sort((left, right) => right.mistake.attempts - left.mistake.attempts || Number(isDue(right.mistake)) - Number(isDue(left.mistake)));
  const reviewPlan = gaps.flatMap((gap) => {
    const lessonMistakes = sortedActiveMistakes.filter((item) => item.lesson.slug === gap.lesson.slug);
    const dueMistakes = lessonMistakes.filter((item) => isDue(item.mistake));
    const focus = dueMistakes.length ? dueMistakes : lessonMistakes;
    return [{ ...gap, focus: focus.slice(0, 3), allCount: lessonMistakes.length }];
  });
  const renderMistake = ({ mistake, module, lesson }: typeof allMistakes[number]) => {
    const practice = [...lesson.stepPractices, ...buildReinforcementPractices(lesson)].find((item) => item.id === mistake.id);
    const check = [...lesson.knowledgeChecks, ...lesson.finalChecks].find((item) => item.id === mistake.id);
    return <article key={mistake.id} className={mistake.mastered ? "mastered" : ""}>
      <span>{module.title} · {lesson.title} · {mistake.attempts} ошиб.</span>
      <h4>{mistake.prompt}</h4>
      <p>Правильный ответ: <b>{mistake.answer}</b></p>
      {(practice?.explanation || check?.explanation) && <p><b>Почему:</b> {practice?.explanation || check?.explanation}</p>}
      <small>{mistake.mastered ? "Закреплено" : isDue(mistake) ? "Можно повторить сейчас" : `Следующее повторение: ${new Date(mistake.dueAt!).toLocaleDateString("ru-RU")}`}</small>
      <button type="button" onClick={() => actions.openMistake(module, lesson, mistake)}>{mistake.mastered ? "Повторить ещё раз" : "Открыть практику →"}</button>
    </article>;
  };
  return <section className="course-review course-exercises" aria-labelledby="course-review-title">
    <div className="course-section-heading"><div><span>Практика и закрепление</span><h3 id="course-review-title">Ошибки</h3></div><p>Разберите ошибку, попробуйте снова и закрепите результат.</p></div>
    <CourseMistakePractice mistakes={mistakes} modules={modules} learningMode={learningMode} disabled={disabled} onChecked={onChecked} onActiveChange={setTrainingActive} />
    <div hidden={trainingActive}>
    {taskMistakes.length > 0 && <section className="course-gap-priorities"><h3>Ошибки из упражнений и домашнего задания</h3><div className="course-review-list">{taskMistakes.map((mistake) => <article key={mistake.id} className={mistake.mastered ? "mastered" : ""}><span>{taskMistakeKind(mistake.id) === "exercise" ? "Упражнение" : "Домашнее задание"} · {mistake.mastered ? "Закреплено" : "Нужно повторить"}</span><p style={{ whiteSpace: "pre-wrap" }}>{mistake.prompt}</p><p>Правильный ответ: <b>{mistake.answer}</b></p>{mistake.dueAt && <small>Повторение: {new Date(mistake.dueAt).toLocaleDateString("ru-RU")}</small>}{taskMistakeSource(mistake.id) ? <button type="button" onClick={() => actions.openTask(mistake.id)}>Открыть задание для повторения →</button> : <small>Исходное задание недоступно. Повторите сохранённую ошибку через «Начать работу над ошибками».</small>}</article>)}</div><p>После правильного ответа повторите задание через 3 дня. Два успешных повторения по расписанию закрепляют ошибку.</p></section>}
    <div className="course-section-heading"><div><span>Весь курс Slovak A1</span><h3>Где нужно подтянуть знания</h3></div><p>{dueCount ? `Можно проработать сейчас: ${dueCount}` : (activeMistakes.length + activeTaskMistakes.length) ? "Следующее повторение уже запланировано" : "Активных ошибок сейчас нет."}</p></div>
    <div className="course-review-overview" aria-label="Сводка ошибок по курсу">
      <article><strong>{activeMistakes.length + activeTaskMistakes.length}</strong><span>активных ошибок</span></article>
      <article><strong>{gaps.length}</strong><span>тем с пробелами</span></article>
      <article><strong>{repeatedCount}</strong><span>повторных промахов</span></article>
      <article><strong>{dueCount}</strong><span>можно повторить сейчас</span></article>
    </div>
    {!activeMistakes.length ? <div className="course-empty"><strong>{masteredMistakes.length ? "Все сохранённые ошибки закреплены" : taskMistakes.length ? "В темах курса активных ошибок нет" : "Ошибок по курсу пока нет"}</strong><p>Неверные ответы из тем и итоговых тестов автоматически появятся здесь.</p></div> : <>
      <section className="course-gap-priorities" aria-labelledby="course-gap-priorities-title">
        <div><strong id="course-gap-priorities-title">План повторения по темам</strong><span>Порядок учитывает число ошибок и повторных промахов. Сначала темы, которые уже пора повторить.</span></div>
        <ol>{reviewPlan.map((item, index) => <li key={item.lesson.slug}>
          <button type="button" onClick={() => actions.openMistake(item.module, item.lesson, item.focus[0].mistake)}>
            <span>{index + 1}</span><b>{item.lesson.title}</b><small>{item.module.title} · {item.allCount} активн. ошибок · {item.attempts} промахов</small><i>{item.due ? `${item.due} сейчас` : "по расписанию позже"}</i>
          </button>
          <div className="course-review-topic-plan">
            <p><b>Почему эта тема:</b> {item.attempts > item.allCount ? `есть повторяющиеся ошибки: ${item.attempts - item.allCount} повторных промахов.` : "есть ошибки, которые ещё нужно закрепить."}</p>
            <p><b>1. Вспомнить правило.</b> {item.lesson.theory.summary}</p>
            <button type="button" onClick={() => actions.openTheory(item.module, item.lesson)}>Открыть объяснение темы →</button>
            <p><b>2. Применить без подсказки.</b> Начните с {item.focus.length} {item.focus.length === 1 ? "задания" : "заданий"}: {item.focus.map(({ mistake }) => `«${mistake.prompt}»`).join("; ")}. Затем разберите остальные ошибки этой темы.</p>
            <p><b>3. Закрепить.</b> После правильного ответа повторите задание через 3 дня. Два успешных повторения по расписанию переводят ошибку в закреплённые. Ранняя тренировка не меняет срок повторения.</p>
            {!item.due && <p>Следующая проверка памяти: {new Date(Math.min(...sortedActiveMistakes.filter((entry) => entry.lesson.slug === item.lesson.slug).map(({ mistake }) => Date.parse(mistake.dueAt!)))).toLocaleDateString("ru-RU")}.</p>}
            <details><summary>Ошибки этой темы ({item.allCount})</summary><div className="course-review-list">{sortedActiveMistakes.filter((entry) => entry.lesson.slug === item.lesson.slug).map(renderMistake)}</div></details>
          </div>
        </li>)}</ol>
      </section>
      <details className="course-review-details"><summary>Разобрать отдельные ошибки: {sortedActiveMistakes.length}</summary><div className="course-review-list">{sortedActiveMistakes.map(renderMistake)}</div></details>
    </>}
    {masteredMistakes.length > 0 && <details className="course-mastered-mistakes"><summary>Закреплённые ошибки: {masteredMistakes.length}</summary><div className="course-review-list">{masteredMistakes.map(renderMistake)}</div></details>}
    <div className="course-actions"><button type="button" className="secondary" onClick={actions.back}>← К обучению</button></div>
    </div>
  </section>;
}

export type CourseFinalActions = { selectAnswer: (question: ModuleFinalQuestion, option: string) => void; submit: () => void; startAttempt: () => void; back: () => void; openLesson: (lesson: CourseLesson) => void; nextModule: () => void };

export type CourseFinalViewModel = { module: CourseModule; moduleCount: number; lessons: CourseLesson[]; questions: ModuleFinalQuestion[]; selections: Record<string, string>; completed: boolean; passingPercent: number };

export function CourseFinalView({ model: { module, moduleCount, lessons, questions, selections, completed, passingPercent }, actions }: { model: CourseFinalViewModel; actions: CourseFinalActions }) {
  const score = questions.filter((question) => selections[question.id] === question.answer).length;
  const passingScore = Math.ceil(questions.length * passingPercent / 100);
  const percentage = questions.length === 0 ? 0 : Math.round(score / questions.length * 100);
  const passed = completed && score >= passingScore;
  const incorrectLessons = completed ? module.lessons.filter((lesson) => questions.some((question) => question.lessonSlug === lesson.slug && selections[question.id] !== question.answer)) : [];
  const displayLessonNumber = (lesson: CourseLesson) => lessons.findIndex((item) => item.slug === lesson.slug) + 1;
  return <section className="course-final">
    <div className="course-section-heading"><div><span>Финал {module.title}</span><h3>Итоговый тест</h3></div><p>По 2 ключевых вопроса из каждой темы · всего {questions.length}. Для сдачи нужно не менее {passingPercent}% ({passingScore} правильных ответов).</p></div>
    {completed && <div className={`course-final-score ${passed ? "passed" : "failed"}`} role="status" aria-live="polite"><strong>{percentage}%</strong><span><b>{passed ? "Модуль сдан" : "Порог пока не достигнут"}</b>{score}/{questions.length} правильных ответов · нужно минимум {passingScore}</span>{passed && module.order < moduleCount && <button type="button" onClick={actions.nextModule}>Перейти к Module {module.order + 1} →</button>}</div>}
    {completed && !passed && incorrectLessons.length > 0 && <div className="course-final-review" aria-labelledby="course-final-review-title"><div><strong id="course-final-review-title">Что повторить перед новой попыткой</strong><span>Ошибки уже записаны. Посмотрите объяснения и повторите материал этих тем.</span></div><div>{incorrectLessons.map((lesson) => <button type="button" key={lesson.slug} onClick={() => actions.openLesson(lesson)}>{displayLessonNumber(lesson)}. {lesson.title} →</button>)}</div></div>}
    <div className="course-check-list">{questions.map((question, index) => { const selected = selections[question.id]; const showResult = completed && Boolean(selected); return <fieldset className={showResult ? selected === question.answer ? "correct" : "incorrect" : ""} key={question.id}><legend>{index + 1}. {question.question}</legend><small>{question.lessonTitle}</small><div>{question.options.map((option) => <button type="button" className={selected === option ? "selected" : ""} key={option} disabled={completed} onClick={() => actions.selectAnswer(question, option)}>{option}</button>)}</div>{showResult && <aside><b>{selected === question.answer ? "✓ Верно" : `Правильный ответ: ${question.answer}`}</b><span><strong>Почему:</strong> {question.explanation}</span></aside>}</fieldset>; })}</div>
    <div className="course-actions"><button type="button" className="secondary" onClick={actions.back}>← К темам</button>{completed ? <button type="button" onClick={actions.startAttempt}>Начать новую попытку</button> : <button type="button" disabled={questions.some((question) => !selections[question.id])} onClick={actions.submit}>Завершить и проверить</button>}</div>
  </section>;
}
