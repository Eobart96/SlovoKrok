"use client";

import { useEffect, useId, useRef, useState } from "react";
import { askCourseHomeworkQuestion } from "../lib/api";
import type { LearningMode } from "../data/learningMode";

/** Mount per attempt so a late reply never appears under another correction. */
export function HomeworkQuestion({ homeworkId, attemptId, learningMode }: { homeworkId: number; attemptId: number; learningMode: LearningMode }) {
  const [open, setOpen] = useState(false);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const active = useRef(true);
  const busy = useRef(false);
  const panelId = useId();
  useEffect(() => { active.current = true; return () => { active.current = false; }; }, []);

  const ask = async () => {
    const query = question.trim();
    if (!query || busy.current || learningMode === "offline") return;
    busy.current = true;
    setLoading(true); setError(""); setAnswer("");
    try {
      const response = await askCourseHomeworkQuestion(homeworkId, attemptId, query);
      if (active.current) setAnswer(response.answer);
    } catch (cause) {
      if (active.current) setError(cause instanceof Error ? cause.message : "Не удалось получить объяснение. Попробуйте ещё раз.");
    } finally {
      busy.current = false;
      if (active.current) setLoading(false);
    }
  };

  return <div className="homework-question">
    <button type="button" onClick={() => setOpen((value) => !value)} aria-expanded={open} aria-controls={panelId}>Спросить</button>
    {open && <div id={panelId} className="homework-question-panel">
      <label htmlFor={`${panelId}-input`}>Что уточнить в объяснении исправления?</label>
      <textarea id={`${panelId}-input`} rows={3} maxLength={2000} value={question} onChange={(event) => setQuestion(event.target.value)} disabled={loading || learningMode === "offline"} placeholder="Например: почему здесь нужно ho, а не jo?" />
      {learningMode === "offline" && <p>Чтобы спросить преподавателя, включите онлайн-режим.</p>}
      <button type="button" onClick={() => void ask()} disabled={loading || !question.trim() || learningMode === "offline"}>{loading ? "Отвечаю…" : "Отправить вопрос"}</button>
      {error && <p role="alert">{error}</p>}
      {answer && <div className="homework-question-answer" role="status"><strong>Ответ преподавателя</strong><p>{answer}</p></div>}
    </div>}
  </div>;
}
