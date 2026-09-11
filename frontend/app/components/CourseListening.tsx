"use client";

import { useState } from "react";
import { type CourseLesson } from "../data/courseTypes";

export function CourseListening({ lesson, back }: { lesson: CourseLesson; back: () => void }) {
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [checked, setChecked] = useState<Record<string, boolean>>({});
  const [played, setPlayed] = useState<Record<string, boolean>>({});
  const [errors, setErrors] = useState<Record<string, boolean>>({});
  return <section className="course-listening" aria-labelledby="listening-title">
    <h3 id="listening-title">Сначала послушайте</h3>
    <p>Прослушайте короткое сообщение и выберите ответ. После проверки откроется расшифровка. Это дополнительная практика; её результаты не входят в оценку темы.</p>
    <p>Синтезированная словацкая речь, немного замедленная для начинающих.</p>
    {lesson.listening?.map((clip, index) => <fieldset key={clip.id}>
      <legend>Сообщение {index + 1}</legend>
      <audio controls preload="metadata" aria-label={`Слушать сообщение ${index + 1}`} onPlay={(event) => {
        const current = event.currentTarget;
        current.closest("section")?.querySelectorAll("audio").forEach((other) => { if (other !== current) other.pause(); });
        setPlayed((state) => ({ ...state, [clip.id]: true }));
      }} onError={() => setErrors((state) => ({ ...state, [clip.id]: true }))} src={clip.audio} />
      {errors[clip.id] && <p role="alert">Запись не загрузилась. Перезагрузите страницу или откройте текстовый материал.</p>}
      <p>{clip.question}</p>
      <div className="course-listening-options">{clip.options.map((option) => <button type="button" key={option} aria-pressed={answers[clip.id] === option} onClick={() => {
        setAnswers((state) => ({ ...state, [clip.id]: option }));
        setChecked((state) => ({ ...state, [clip.id]: false }));
      }}>{option}</button>)}</div>
      <button type="button" disabled={!answers[clip.id] || !played[clip.id]} onClick={() => setChecked((state) => ({ ...state, [clip.id]: true }))}>Проверить ответ</button>
      {checked[clip.id] && <div role="status"><p>{answers[clip.id] === clip.answer ? "Верно." : "Пока неверно."} {clip.explanation}</p><p lang="sk">{clip.transcript}</p></div>}
    </fieldset>)}
    <button type="button" onClick={back}>К текстовому материалу</button>
  </section>;
}
