import { useMemo } from "react";
import { compareHomeworkAnswers } from "../data/homeworkReview";

export function HomeworkAnswerComparison({ original, corrected }: { original: string; corrected: string }) {
  const comparison = useMemo(() => compareHomeworkAnswers(original, corrected), [original, corrected]);
  return <div className="homework-comparison">
    <p className="homework-comparison-legend">Слева выделено то, что изменено или убрано; справа — исправления и добавления.</p>
    <div className="homework-comparison-columns">
      <section aria-label="Ваш отправленный ответ"><strong>Ваш ответ</strong><p lang="sk">{comparison.original.map((token, index) => token.changed ? <del key={index}>{token.text}</del> : token.text)}</p></section>
      <section aria-label="Исправленный вариант"><strong>Исправленный вариант</strong><p lang="sk">{comparison.corrected.map((token, index) => token.changed ? <ins key={index}>{token.text}</ins> : token.text)}</p></section>
    </div>
    {original === corrected && <p>Исправлений в тексте нет.</p>}
  </div>;
}
