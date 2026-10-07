"use client";

import type { TaskMistakeInput } from "../data/taskMistakes";

export function CourseTaskMistakeButton({ mistake, recorded, disabled, onRecord }: { mistake: TaskMistakeInput; recorded: boolean; disabled: boolean; onRecord: (mistake: TaskMistakeInput) => void }) {
  return <button type="button" disabled={disabled || recorded} onClick={() => onRecord(mistake)}>{recorded ? "Ошибка записана" : "Записать ошибку"}</button>;
}
