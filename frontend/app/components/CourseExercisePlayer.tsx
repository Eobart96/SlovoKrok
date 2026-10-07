"use client";

import { type KeyboardEvent, type RefObject, useState } from "react";

import { applySlovakAltShortcut } from "../data/slovakKeyboard";
import { type CourseExercise } from "../lib/api";
import { SlovakKeyboard } from "./SlovakKeyboard";

export function CourseExercisePlayer({ exercise, answer, onAnswerChange, answerRef, disabled, onInsertKey }: {
  exercise: CourseExercise;
  answer: string;
  onAnswerChange: (answer: string) => void;
  answerRef: RefObject<HTMLTextAreaElement | null>;
  disabled: boolean;
  onInsertKey: (key: string) => void;
}) {
  const [orderedIndexes, setOrderedIndexes] = useState<number[]>([]);
  const [matches, setMatches] = useState<Record<string, string>>({});
  const kind = exercise.interaction_type ?? "text";
  const options = exercise.options ?? [];
  const tokens = exercise.tokens ?? [];
  const pairPrompts = exercise.pair_prompts ?? [];
  const pairOptions = exercise.pair_options ?? [];

  const handleAltShortcut = (event: KeyboardEvent<HTMLTextAreaElement>) => {
    if (!event.altKey || event.ctrlKey || event.metaKey) return;
    const field = answerRef.current;
    const inserted = applySlovakAltShortcut(answer, event.code, event.shiftKey, field?.selectionStart ?? answer.length, field?.selectionEnd ?? answer.length);
    if (!inserted) return;
    event.preventDefault();
    onAnswerChange(inserted.value);
    requestAnimationFrame(() => {
      field?.focus();
      field?.setSelectionRange(inserted.caret, inserted.caret);
    });
  };

  const updateOrder = (indexes: number[]) => {
    setOrderedIndexes(indexes);
    onAnswerChange(indexes.map((index) => tokens[index]).join(" "));
  };
  const updateMatch = (prompt: string, value: string) => {
    const next = { ...matches, [prompt]: value };
    if (!value) delete next[prompt];
    setMatches(next);
    onAnswerChange(pairPrompts.every((item) => next[item]) ? pairPrompts.map((item) => `${item} → ${next[item]}`).join("; ") : "");
  };

  if (kind === "choice" && options.length >= 2) return <div className="course-mini-choice" role="group" aria-label="Выберите ответ">
    {options.map((option) => <button type="button" key={option} className={answer === option ? "selected" : ""} aria-pressed={answer === option} disabled={disabled} onClick={() => onAnswerChange(option)}>{option}</button>)}
  </div>;

  if (kind === "order" && tokens.length >= 2) return <div className="course-mini-order">
    <div className={orderedIndexes.length ? "course-mini-built" : "course-mini-built empty"} aria-live="polite">{orderedIndexes.length ? orderedIndexes.map((index, position) => <button type="button" key={`${index}-${position}`} disabled={disabled} aria-label={`Убрать ${tokens[index]}`} onClick={() => updateOrder(orderedIndexes.filter((_, itemPosition) => itemPosition !== position))}>{tokens[index]}</button>) : <span>Нажимайте на слова в правильном порядке</span>}</div>
    <div className="course-mini-tokens" role="group" aria-label="Доступные слова">{tokens.map((token, index) => <button type="button" key={`${token}-${index}`} disabled={disabled || orderedIndexes.includes(index)} aria-label={`Добавить ${token}`} onClick={() => updateOrder([...orderedIndexes, index])}>{token}</button>)}</div>
    <button type="button" className="course-mini-clear" disabled={disabled || !orderedIndexes.length} onClick={() => updateOrder([])}>Собрать заново</button>
  </div>;

  if (kind === "match" && pairPrompts.length >= 2 && pairOptions.length >= 2) return <div className="course-mini-match" aria-label="Соедините пары">
    {pairPrompts.map((prompt) => <label key={prompt}><span>{prompt}</span><select value={matches[prompt] ?? ""} disabled={disabled} onChange={(event) => updateMatch(prompt, event.target.value)}><option value="">Выберите пару</option>{pairOptions.map((option) => <option key={option} value={option} disabled={Object.entries(matches).some(([otherPrompt, selected]) => otherPrompt !== prompt && selected === option)}>{option}</option>)}</select></label>)}
  </div>;

  return <><textarea ref={answerRef} rows={5} value={answer} onChange={(event) => onAnswerChange(event.target.value)} onKeyDown={handleAltShortcut} placeholder="Напишите ответ по-словацки…" disabled={disabled} /><SlovakKeyboard onInsert={onInsertKey} disabled={disabled} /></>;
}
