"use client";

import { type ModuleFinalQuestion } from "../data/coursePractice";
import { type CourseLesson, type CourseModule } from "../data/courseTypes";
import { type MistakeRecord } from "../hooks/useCourseSession";

export type CourseReviewViewModel = { mistakes: Record<string, MistakeRecord>; modules: CourseModule[] };
export type CourseReviewActions = { openMistake: (module: CourseModule, lesson: CourseLesson, mistake: MistakeRecord) => void; back: () => void };

export function CourseReviewView({ model: { mistakes, modules }, actions }: { model: CourseReviewViewModel; actions: CourseReviewActions }) {
  const lessonLocations = new Map(modules.flatMap((module) => module.lessons.map((lesson) => [lesson.slug, { module, lesson }] as const)));
  const allMistakes = Object.values(mistakes).flatMap((mistake) => {
    const location = lessonLocations.get(mistake.lessonSlug);
    return location ? [{ mistake, ...location }] : [];
  });
  const activeMistakes = allMistakes.filter(({ mistake }) => !mistake.mastered);
  const masteredMistakes = allMistakes.filter(({ mistake }) => mistake.mastered);
  const isDue = (mistake: MistakeRecord) => !mistake.dueAt || new Date(mistake.dueAt).getTime() <= Date.now();
  const dueCount = activeMistakes.filter(({ mistake }) => isDue(mistake)).length;
  const repeatedCount = activeMistakes.filter(({ mistake }) => mistake.attempts > 1).length;
  const gaps = [...activeMistakes.reduce((byLesson, item) => {
    const current = byLesson.get(item.lesson.slug) ?? { module: item.module, lesson: item.lesson, mistakes: 0, attempts: 0, due: 0 };
    current.mistakes += 1;
    current.attempts += item.mistake.attempts;
    current.due += isDue(item.mistake) ? 1 : 0;
    byLesson.set(item.lesson.slug, current);
    return byLesson;
  }, new Map<string, { module: CourseModule; lesson: CourseLesson; mistakes: number; attempts: number; due: number }>()).values()]
    .sort((left, right) => right.attempts - left.attempts || right.mistakes - left.mistakes || left.module.order - right.module.order);
  const sortedActiveMistakes = [...activeMistakes].sort((left, right) => right.mistake.attempts - left.mistake.attempts || Number(isDue(right.mistake)) - Number(isDue(left.mistake)));
  const renderMistake = ({ mistake, module, lesson }: typeof allMistakes[number]) => {
    const reviewLocked = !mistake.mastered && !isDue(mistake);
    return <article key={mistake.id} className={mistake.mastered ? "mastered" : ""}>
      <span>{module.title} · {lesson.title} · {mistake.attempts} ошиб.</span>
      <h4>{mistake.prompt}</h4>
      <p>Правильный ответ: <b>{mistake.answer}</b></p>
      <small>{mistake.mastered ? "Закреплено" : isDue(mistake) ? "Можно повторить сейчас" : `Следующее повторение: ${new Date(mistake.dueAt!).toLocaleDateString("ru-RU")}`}</small>
      <button type="button" disabled={reviewLocked} onClick={() => actions.openMistake(module, lesson, mistake)}>{mistake.mastered ? "Повторить ещё раз" : "Исправить в теме →"}</button>
    </article>;
  };
  return <section className="course-review">
    <div className="course-section-heading"><div><span>Весь курс Slovak A1</span><h3>Где нужно подтянуть знания</h3></div><p>{dueCount ? `Можно проработать сейчас: ${dueCount}` : activeMistakes.length ? "Следующее повторение уже запланировано" : "Активных ошибок сейчас нет."}</p></div>
    <div className="course-review-overview" aria-label="Сводка ошибок по курсу">
      <article><strong>{activeMistakes.length}</strong><span>активных ошибок</span></article>
      <article><strong>{gaps.length}</strong><span>тем с пробелами</span></article>
      <article><strong>{repeatedCount}</strong><span>повторных промахов</span></article>
      <article><strong>{dueCount}</strong><span>можно повторить сейчас</span></article>
    </div>
    {!activeMistakes.length ? <div className="course-empty"><strong>Ошибок по курсу пока нет</strong><p>Неверные ответы из тем и итоговых тестов автоматически появятся здесь.</p></div> : <>
      <section className="course-gap-priorities" aria-labelledby="course-gap-priorities-title">
        <div><strong id="course-gap-priorities-title">Что проработать в первую очередь</strong><span>Темы выше допущены чаще или содержат больше активных ошибок.</span></div>
        <div>{gaps.map((gap, index) => <button type="button" key={gap.lesson.slug} onClick={() => actions.openMistake(gap.module, gap.lesson, sortedActiveMistakes.find((item) => item.lesson.slug === gap.lesson.slug)!.mistake)}>
          <span>{index + 1}</span><b>{gap.lesson.title}</b><small>{gap.module.title} · {gap.mistakes} активн. · {gap.attempts} попыт.</small><i>{gap.due ? `${gap.due} сейчас` : "позже"}</i>
        </button>)}</div>
      </section>
      <div className="course-review-list">{sortedActiveMistakes.map(renderMistake)}</div>
    </>}
    {masteredMistakes.length > 0 && <details className="course-mastered-mistakes"><summary>Закреплённые ошибки: {masteredMistakes.length}</summary><div className="course-review-list">{masteredMistakes.map(renderMistake)}</div></details>}
    <div className="course-actions"><button type="button" className="secondary" onClick={actions.back}>← К обучению</button></div>
  </section>;
}

export type CourseFinalActions = { selectAnswer: (question: ModuleFinalQuestion, option: string) => void; submit: () => void; back: () => void; openLesson: (lesson: CourseLesson) => void; nextModule: () => void };

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
    {completed && !passed && incorrectLessons.length > 0 && <div className="course-final-review" aria-labelledby="course-final-review-title"><div><strong id="course-final-review-title">Что повторить перед новой попыткой</strong><span>Исправьте ответы сразу или вернитесь к материалу этих тем.</span></div><div>{incorrectLessons.map((lesson) => <button type="button" key={lesson.slug} onClick={() => actions.openLesson(lesson)}>{displayLessonNumber(lesson)}. {lesson.title} →</button>)}</div></div>}
    <div className="course-check-list">{questions.map((question, index) => { const selected = selections[question.id]; const showResult = completed && Boolean(selected); return <fieldset className={showResult ? selected === question.answer ? "correct" : "incorrect" : ""} key={question.id}><legend>{index + 1}. {question.question}</legend><small>{question.lessonTitle}</small><div>{question.options.map((option) => <button type="button" className={selected === option ? "selected" : ""} key={option} onClick={() => actions.selectAnswer(question, option)}>{option}</button>)}</div>{showResult && <aside><b>{selected === question.answer ? "✓ Верно" : `Правильный ответ: ${question.answer}`}</b><span><strong>Почему:</strong> {question.explanation}</span></aside>}</fieldset>; })}</div>
    <div className="course-actions"><button type="button" className="secondary" onClick={actions.back}>← К темам</button><button type="button" disabled={questions.some((question) => !selections[question.id])} onClick={actions.submit}>Проверить итоговый тест</button></div>
  </section>;
}
