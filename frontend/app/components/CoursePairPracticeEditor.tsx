"use client";

import { type CSSProperties, type KeyboardEvent, useRef, useState } from "react";

import { getPairAnswers, getPairMatches } from "../data/coursePractice";
import { type StepPractice } from "../data/courseTypes";
import { applySlovakAltShortcut } from "../data/slovakKeyboard";
import { SlovakKeyboard } from "./SlovakKeyboard";

export function CoursePairPracticeEditor({ practice, value, checked, onChange }: { practice: StepPractice; value: string; checked: boolean; onChange: (value: string) => void }) {
  const inputRefs = useRef<Array<HTMLInputElement | null>>([]);
  const pairs = practice.pairs ?? [];
  const answers = getPairAnswers(practice, value);
  const matches = checked ? getPairMatches(practice, value) : [];
  const [activePair, setActivePair] = useState(0);
  const update = (index: number, answer: string) => {
    const next = [...answers];
    next[index] = answer;
    onChange(JSON.stringify(next));
  };
  const insertKey = (key: string) => {
    const input = inputRefs.current[activePair];
    const answer = answers[activePair] ?? "";
    const start = input?.selectionStart ?? answer.length;
    const end = input?.selectionEnd ?? start;
    update(activePair, `${answer.slice(0, start)}${key}${answer.slice(end)}`);
    requestAnimationFrame(() => {
      input?.focus();
      input?.setSelectionRange(start + key.length, start + key.length);
    });
  };
  const hasTextInputs = pairs.some((pair) => !pair.options?.length);
  const handleAltShortcut = (event: KeyboardEvent<HTMLInputElement>, index: number) => {
    if (!event.altKey || event.ctrlKey || event.metaKey) return;
    const input = inputRefs.current[index];
    const answer = answers[index] ?? "";
    const inserted = applySlovakAltShortcut(answer, event.code, event.shiftKey, input?.selectionStart ?? answer.length, input?.selectionEnd ?? answer.length);
    if (!inserted) return;
    event.preventDefault();
    update(index, inserted.value);
    requestAnimationFrame(() => {
      input?.focus();
      input?.setSelectionRange(inserted.caret, inserted.caret);
    });
  };
  return <div className="course-pair-practice">
    <div className="course-pair-list">
      {pairs.map((pair, index) => {
        const answer = answers[index] ?? "";
        const match = matches[index];
        return <div className={`course-pair-row ${checked ? match === "correct" ? "correct" : "incorrect" : ""}`} key={`${pair.prompt}-${index}`}>
          <strong>{pair.prompt}</strong>
          {pair.options?.length
            ? <div className="course-pair-options" style={{ "--course-pair-option-count": pair.options.length } as CSSProperties}>{pair.options.map((option) => <button type="button" className={answer === option ? "selected" : ""} key={option} onClick={() => update(index, option)}>{option}</button>)}</div>
            : <input ref={(element) => { inputRefs.current[index] = element; }} aria-label={pair.prompt} value={answer} onFocus={() => setActivePair(index)} onChange={(event) => update(index, event.target.value)} onKeyDown={(event) => handleAltShortcut(event, index)} placeholder={pair.inputHint ?? "Введите ответ"} autoComplete="off" />}
          {checked && match !== "correct" && <small>Правильно: <span lang="sk">{pair.answer}</span></small>}
          {checked && match === "correct" && <small>Верно</small>}
        </div>;
      })}
    </div>
    {hasTextInputs && practice.showSlovakKeyboard !== false && <SlovakKeyboard onInsert={insertKey} />}
  </div>;
}
