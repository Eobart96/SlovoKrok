"use client";

import { type FormEvent, type KeyboardEvent, type PointerEvent as ReactPointerEvent, useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";

import { editTranslationDraft, swapTranslationDraft, type TranslationDraftReset } from "../data/translationState";
import {
  askTutorTranslationQuestion,
  translateWithTutor,
  type TranslationDirection,
  type TutorTranslation,
} from "../lib/api";

type Position = { x: number; y: number };
type DragState = { pointerId: number; offsetX: number; offsetY: number };

const panelWidth = 380;
const viewportGap = 12;

function clampPosition(position: Position, width: number, height: number): Position {
  return {
    x: Math.max(viewportGap, Math.min(position.x, window.innerWidth - width - viewportGap)),
    y: Math.max(viewportGap, Math.min(position.y, window.innerHeight - height - viewportGap)),
  };
}

export function FloatingTranslator() {
  const panelRef = useRef<HTMLElement>(null);
  const dragRef = useRef<DragState | null>(null);
  const [open, setOpen] = useState(false);
  const [collapsed, setCollapsed] = useState(false);
  const [position, setPosition] = useState<Position>({ x: viewportGap, y: 88 });
  const [direction, setDirection] = useState<TranslationDirection>("ru-sk");
  const [text, setText] = useState("");
  const [result, setResult] = useState<TutorTranslation | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [questionOpen, setQuestionOpen] = useState(false);
  const [question, setQuestion] = useState("");
  const [questionAnswer, setQuestionAnswer] = useState("");
  const [questionLoading, setQuestionLoading] = useState(false);
  const [questionError, setQuestionError] = useState("");

  const keepInsideViewport = (next = position) => {
    const rect = panelRef.current?.getBoundingClientRect();
    if (!rect) return;
    setPosition(clampPosition(next, rect.width, rect.height));
  };

  useEffect(() => {
    if (!open) return;
    const frame = window.requestAnimationFrame(() => {
      const rect = panelRef.current?.getBoundingClientRect();
      if (!rect) return;
      setPosition(clampPosition({ x: window.innerWidth - Math.min(panelWidth, rect.width) - 24, y: 96 }, rect.width, rect.height));
    });
    return () => window.cancelAnimationFrame(frame);
  }, [open]);

  useEffect(() => {
    if (!open) return;
    const onResize = () => keepInsideViewport();
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  });

  useEffect(() => {
    if (!open) return;
    const frame = window.requestAnimationFrame(() => keepInsideViewport());
    return () => window.cancelAnimationFrame(frame);
  }, [collapsed, error, open, questionAnswer, questionError, questionOpen, result]);

  useEffect(() => {
    const onPointerMove = (event: PointerEvent) => {
      const drag = dragRef.current;
      const rect = panelRef.current?.getBoundingClientRect();
      if (!drag || !rect || event.pointerId !== drag.pointerId) return;
      setPosition(clampPosition({ x: event.clientX - drag.offsetX, y: event.clientY - drag.offsetY }, rect.width, rect.height));
    };
    const stopDragging = (event: PointerEvent) => {
      if (dragRef.current?.pointerId === event.pointerId) dragRef.current = null;
    };
    window.addEventListener("pointermove", onPointerMove);
    window.addEventListener("pointerup", stopDragging);
    window.addEventListener("pointercancel", stopDragging);
    return () => {
      window.removeEventListener("pointermove", onPointerMove);
      window.removeEventListener("pointerup", stopDragging);
      window.removeEventListener("pointercancel", stopDragging);
    };
  }, []);

  const startDragging = (event: ReactPointerEvent<HTMLButtonElement>) => {
    const rect = panelRef.current?.getBoundingClientRect();
    if (!rect) return;
    dragRef.current = { pointerId: event.pointerId, offsetX: event.clientX - rect.left, offsetY: event.clientY - rect.top };
    event.currentTarget.setPointerCapture(event.pointerId);
  };

  const moveWithKeyboard = (event: KeyboardEvent<HTMLButtonElement>) => {
    const movement: Record<string, Position> = {
      ArrowLeft: { x: -16, y: 0 }, ArrowRight: { x: 16, y: 0 }, ArrowUp: { x: 0, y: -16 }, ArrowDown: { x: 0, y: 16 },
    };
    const delta = movement[event.key];
    const rect = panelRef.current?.getBoundingClientRect();
    if (!delta || !rect) return;
    event.preventDefault();
    setPosition((current) => clampPosition({ x: current.x + delta.x, y: current.y + delta.y }, rect.width, rect.height));
  };

  const applyDraftReset = (next: TranslationDraftReset<TutorTranslation>) => {
    setDirection(next.direction);
    setText(next.text);
    setResult(next.result);
    setError(next.error);
    setQuestionOpen(next.questionOpen);
    setQuestion(next.question);
    setQuestionAnswer(next.questionAnswer);
    setQuestionError(next.questionError);
  };

  const swapDirection = () => {
    applyDraftReset(swapTranslationDraft({ direction, text, result }));
  };

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    const source = text.trim();
    if (!source || loading) return;
    setLoading(true);
    setError("");
    setQuestionOpen(false);
    setQuestion("");
    setQuestionAnswer("");
    setQuestionError("");
    try {
      const translated = await translateWithTutor(source, direction);
      setResult(translated);
    } catch (requestError) {
      setResult(null);
      setError(requestError instanceof Error ? requestError.message : "Не удалось выполнить перевод");
    } finally {
      setLoading(false);
    }
  };

  const askQuestion = async () => {
    const source = text.trim();
    const query = question.trim();
    if (!result || !source || !query || questionLoading) return;
    setQuestionLoading(true);
    setQuestionError("");
    setQuestionAnswer("");
    try {
      const response = await askTutorTranslationQuestion({
        history_id: result.history_id,
        source_text: source,
        translation: result.translation,
        direction,
        question: query,
      });
      setQuestionAnswer(response.answer);
    } catch (requestError) {
      setQuestionError(requestError instanceof Error ? requestError.message : "Не удалось получить ответ");
    } finally {
      setQuestionLoading(false);
    }
  };

  if (!open) {
    return <button type="button" className="floating-translator-launch" onClick={() => setOpen(true)}><span aria-hidden="true">А↔A</span> Переводчик</button>;
  }

  return createPortal(
    <aside
      ref={panelRef}
      className={`floating-translator${collapsed ? " collapsed" : ""}`}
      aria-label="Переводчик"
      style={{ left: position.x, top: position.y }}
    >
      <header>
        <button type="button" className="floating-translator-drag" aria-label="Перетащить переводчик" onPointerDown={startDragging} onKeyDown={moveWithKeyboard} title="Перетащите окно или используйте стрелки клавиатуры">
          <span aria-hidden="true">⠿</span><strong>Переводчик</strong>
        </button>
        <div>
          <button type="button" aria-label={collapsed ? "Развернуть переводчик" : "Свернуть переводчик"} onClick={() => setCollapsed((current) => !current)}>{collapsed ? "□" : "−"}</button>
          <button type="button" aria-label="Закрыть переводчик" onClick={() => setOpen(false)}>×</button>
        </div>
      </header>
      {!collapsed && <form onSubmit={submit}>
        <div className="floating-translator-languages">
          <span>{direction === "ru-sk" ? "Русский" : "Словацкий"}</span>
          <button type="button" onClick={swapDirection} aria-label="Поменять языки местами">⇄</button>
          <span>{direction === "ru-sk" ? "Словацкий" : "Русский"}</span>
        </div>
        <label>
          <span>Текст для перевода</span>
          <textarea value={text} onChange={(event) => applyDraftReset(editTranslationDraft({ direction, text, result }, event.target.value))} maxLength={2000} rows={4} placeholder={direction === "ru-sk" ? "Введите текст по-русски" : "Zadajte text po slovensky"} />
        </label>
        <div className="floating-translator-submit">
          <small>{text.length}/2000</small>
          <button type="submit" disabled={!text.trim() || loading}>{loading ? "Перевожу…" : "Перевести"}</button>
        </div>
        {error && <p className="floating-translator-error" role="alert">{error}</p>}
        {result && <section className="floating-translator-result" aria-live="polite">
          <span>Перевод</span>
          <strong>{result.translation}</strong>
          {result.alternatives.length > 0 && <p>Также: {result.alternatives.join(" · ")}</p>}
          {result.note && <small>{result.note}</small>}
          <div className="floating-translator-result-footer">
            <button type="button" className="floating-translator-ask-toggle" onClick={() => setQuestionOpen((current) => !current)} aria-expanded={questionOpen}>? Спросить</button>
            <em>Сохранено · ИИ {result.provider}</em>
          </div>
          {questionOpen && <div className="floating-translator-question">
            <label>
              <span>Вопрос о переводе</span>
              <textarea value={question} onChange={(event) => setQuestion(event.target.value)} maxLength={1000} rows={2} placeholder="Например: почему здесь это слово?" />
            </label>
            <button type="button" onClick={askQuestion} disabled={!question.trim() || questionLoading}>{questionLoading ? "Отвечаю…" : "Задать вопрос"}</button>
            {questionError && <p className="floating-translator-error" role="alert">{questionError}</p>}
            {questionAnswer && <p className="floating-translator-question-answer" aria-live="polite">{questionAnswer}</p>}
          </div>}
        </section>}
      </form>}
    </aside>,
    document.body,
  );
}
